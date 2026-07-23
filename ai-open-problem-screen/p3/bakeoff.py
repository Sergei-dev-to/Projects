"""Shared Reeve-scan helpers plus a superseded arm-bake-off draft.

The arm comparison in this module must not be run: hostile review established
that its geometry pass already determines the target polynomial, invalidating
the claimed efficiency comparison.  The active, honest entry point is
``python -m p3.reeve_scan``.  The exact enumeration, hashing, vertex decoding,
and saturated-volume helpers remain here so their already-tested code can be
reused by that direct scan.
"""

from __future__ import annotations

import argparse
from collections import Counter
from contextlib import contextmanager
from fractions import Fraction
import hashlib
import heapq
from importlib.metadata import PackageNotFoundError, version as package_version
from itertools import combinations
import math
from pathlib import Path
import sys
from typing import Any, Iterable, Iterator, Mapping, Sequence

import lrcalc

from p1.control.atomic import atomic_write_bytes, load_json
from p1.control.canonical import canonical_json_bytes, sha256_file, sha256_json
from p1.e1 import evaluator as e1
from p1.e2 import hive_e2 as e2


PLAN_SCHEMA = "lr-p3-reeve-bakeoff-plan/v1"
SUPERSEDED_DO_NOT_RUN = True
PANEL_SCHEMA = "lr-p3-reeve-bakeoff-panel/v1"
GEOMETRY_ITEM_SCHEMA = "lr-p3-reeve-geometry-item/v1"
GEOMETRY_SCHEMA = "lr-p3-reeve-geometry/v1"
RANKINGS_SCHEMA = "lr-p3-reeve-rankings/v1"
EVALUATION_ITEM_SCHEMA = "lr-p3-reeve-evaluation-item/v1"
EVALUATIONS_SCHEMA = "lr-p3-reeve-evaluations/v1"
ADJUDICATION_SCHEMA = "lr-p3-reeve-adjudication/v1"
MANIFEST_SCHEMA = "lr-p3-reeve-manifest/v1"

ROWS = 6
MAXIMUM_INNER_SIZE = 12
B0_MAXIMUM_INNER_SIZE = 7
ELIGIBLE_OUTER_ROWS = (4, 5, 6)
PANEL_SIZE = 512
ARM_BUDGET = 64
SEED = 20260723
ARMS = (
    "reeve_volume",
    "integral_tetrahedron_ablation",
    "affine_dimension_3",
    "rows_size",
    "stratified_random",
)
EXPECTED_B1_BY_OUTER_ROWS = {
    0: 1,
    1: 90,
    2: 3_997,
    3: 42_604,
    4: 173_349,
    5: 363_220,
    6: 491_496,
}
EXPECTED_UNIVERSE_BY_OUTER_ROWS = {
    4: 170_627,
    5: 360_570,
    6: 489_567,
}
EXPECTED_UNIVERSE_SIZE = 1_020_764
EXPECTED_B1_SUPPORT_SIZE = 1_074_757
EXPECTED_B1_UNORDERED_INNER_PAIRS = 25_878


class BakeoffError(RuntimeError):
    """Fail-closed error for a malformed artifact or evaluator disagreement."""


@contextmanager
def _run_lock(work_dir: Path) -> Iterator[None]:
    """Prevent two CLI processes from freezing or scoring the same run."""

    try:
        import fcntl
    except ImportError as exc:  # pragma: no cover - target is WSL
        raise BakeoffError("the bake-off requires Linux/WSL file locking") from exc
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    lock_path = work_dir / "run.lock"
    with lock_path.open("a+", encoding="utf-8") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise BakeoffError(f"another bake-off process holds {lock_path}") from exc
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _package(name: str) -> str:
    try:
        return package_version(name)
    except PackageNotFoundError:
        return "unknown"


def _canonical_file_bytes(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _sidecar(path: Path) -> Path:
    return path.with_name(path.name + ".sha256")


def _write_pinned_json(path: Path, value: Any) -> str:
    """Create an immutable canonical JSON artifact, or verify an identical one."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _canonical_file_bytes(value)
    digest = hashlib.sha256(payload).hexdigest()
    digest_payload = (digest + "\n").encode("ascii")
    if path.exists():
        if path.read_bytes() != payload:
            raise BakeoffError(f"immutable artifact differs: {path}")
    else:
        atomic_write_bytes(path, payload, overwrite=False)
    sidecar = _sidecar(path)
    if sidecar.exists():
        if sidecar.read_bytes() != digest_payload:
            raise BakeoffError(f"digest sidecar differs: {sidecar}")
    else:
        atomic_write_bytes(sidecar, digest_payload, overwrite=False)
    return digest


def _write_pinned_text(path: Path, text: str) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = text.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    digest_payload = (digest + "\n").encode("ascii")
    if path.exists():
        if path.read_bytes() != payload:
            raise BakeoffError(f"immutable artifact differs: {path}")
    else:
        atomic_write_bytes(path, payload, overwrite=False)
    sidecar = _sidecar(path)
    if sidecar.exists():
        if sidecar.read_bytes() != digest_payload:
            raise BakeoffError(f"digest sidecar differs: {sidecar}")
    else:
        atomic_write_bytes(sidecar, digest_payload, overwrite=False)
    return digest


def _load_pinned_json(path: Path) -> tuple[Any, str]:
    path = Path(path)
    if not path.is_file() or not _sidecar(path).is_file():
        raise BakeoffError(f"missing pinned artifact or sidecar: {path}")
    digest = sha256_file(path)
    claimed = _sidecar(path).read_text(encoding="ascii").strip()
    if claimed != digest:
        raise BakeoffError(f"digest mismatch for {path}: {digest} != {claimed}")
    value = load_json(path)
    if path.read_bytes() != _canonical_file_bytes(value):
        raise BakeoffError(f"artifact is not canonical JSON: {path}")
    return value, digest


def _source_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parents[1]
    env = root / "run" / "env.json"
    return {
        "bakeoff_py_sha256": sha256_file(Path(__file__).resolve()),
        "e1_source_sha256": sha256_file(Path(e1.__file__).resolve()),
        "e2_source_sha256": sha256_file(Path(e2.__file__).resolve()),
        "env_json_sha256": sha256_file(env),
    }


def build_plan() -> dict[str, Any]:
    return {
        "schema_version": PLAN_SCHEMA,
        "classification": "internal-non-certifying-bakeoff",
        "created_date": "2026-07-23",
        "superseded_gate_status": {
            "heldout_gain_prereg": "SUPERSEDED-provenance-only",
            "sol_ultra_p3": "SUSPENDED-DO-NOT-DISPATCH",
            "revived": False,
        },
        "environment": {
            "python_major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
            "lrcalc_version": _package("lrcalc"),
            "pynormaliz_version": _package("PyNormaliz"),
        },
        "sources": _source_hashes(),
        "universe": {
            "name": "B1-minus-B0-7-positive-support-rows-at-least-4",
            "maximum_length": ROWS,
            "maximum_size_each_inner": MAXIMUM_INNER_SIZE,
            "exclude_if_both_inner_sizes_at_most": B0_MAXIMUM_INNER_SIZE,
            "require_positive_lr_at_n1": True,
            "eligible_outer_rows": list(ELIGIBLE_OUTER_ROWS),
            "expected_count": EXPECTED_UNIVERSE_SIZE,
            "expected_count_by_outer_rows": {
                str(k): v for k, v in EXPECTED_UNIVERSE_BY_OUTER_ROWS.items()
            },
            "canonicalization": "swap-only-order2",
            "stream_order": "(sum(lam),lam),(sum(mu),mu),sorted(nu); length-prefixed canonical JSON",
        },
        "panel": {
            "common_filter": "c^nu_lam,mu(1) == 4",
            "filter_rationale": "necessary N=1 count for an empty integral tetrahedron",
            "coefficient_value_as_ranking_feature": False,
            "size": PANEL_SIZE,
            "seed": SEED,
            "selection": "proportional largest-remainder strata then lowest domain-separated SHA-256",
            "strata": "(len(nu),max(|lam|,|mu|))",
        },
        "geometry": {
            "queries_per_panel_item": ["AffineDim", "VerticesOfPolyhedron"],
            "forbidden_before_ranking_freeze": [
                "EhrhartSeries",
                "EhrhartQuasiPolynomial",
                "stretched LR coefficient at N>1",
            ],
            "empty_tetrahedron_formula": ["1", "(12-Delta)/6", "1", "Delta/6"],
            "negative_signature": "affine_dim=3, four integral vertices, c(1)=4, Delta>12",
        },
        "arms": {
            "names": list(ARMS),
            "exact_polynomial_budget_each": ARM_BUDGET,
            "overlap_policy": "credit original rank; do not replace overlaps",
        },
        "evaluation": {
            "ordinary_e1_mode": "bounded",
            "negative_e1_mode": "conservative",
            "e2": "explicit hive plus raw period-one Normaliz Ehrhart",
            "require_canonical_polynomial_agreement": True,
            "evaluate_fixed_union_only": True,
        },
        "decision_rule": {
            "negative_any_arm": "candidate-verification event; never automatic scaling",
            "no_negative": "NO-GO for empty-Reeve P3 route",
            "positive_proxy_metrics": "descriptive only; cannot authorize scaling",
            "control_only_negative": "scientific candidate and Reeve ranking-advantage rejected",
        },
    }


def _require_plan(work_dir: Path) -> tuple[dict[str, Any], str]:
    plan, digest = _load_pinned_json(Path(work_dir) / "plan.json")
    if not isinstance(plan, dict) or plan.get("schema_version") != PLAN_SCHEMA:
        raise BakeoffError("invalid bake-off plan schema")
    if plan.get("sources") != _source_hashes():
        raise BakeoffError("current source or envelope hashes differ from frozen plan")
    expected_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    environment = plan.get("environment", {})
    if environment.get("python_major_minor") != expected_python:
        raise BakeoffError("current Python major/minor differs from frozen plan")
    if environment.get("lrcalc_version") != _package("lrcalc"):
        raise BakeoffError("current lrcalc differs from frozen plan")
    if environment.get("pynormaliz_version") != _package("PyNormaliz"):
        raise BakeoffError("current PyNormaliz differs from frozen plan")
    return plan, digest


def _triple_dict(triple: e1.Triple) -> dict[str, list[int]]:
    lam, mu, nu = triple
    return {"lam": list(lam), "mu": list(mu), "nu": list(nu)}


def _dict_triple(value: Mapping[str, Any]) -> e1.Triple:
    try:
        return e1.canonical_triple(value["lam"], value["mu"], value["nu"])
    except (KeyError, TypeError, ValueError) as exc:
        raise BakeoffError(f"invalid triple record: {value!r}") from exc


def _triple_id(triple: e1.Triple) -> str:
    return sha256_json({
        "domain": "lr-p3-reeve-bakeoff-triple/v1",
        "triple": _triple_dict(triple),
    })


def _domain_hash(domain: str, triple: e1.Triple) -> str:
    return sha256_json({
        "domain": domain,
        "seed": SEED,
        "triple": _triple_dict(triple),
    })


def _contains(outer: Sequence[int], inner: Sequence[int]) -> bool:
    return len(inner) <= len(outer) and all(
        inner[index] <= outer[index] for index in range(len(inner))
    )


def iter_b1_support() -> Iterator[tuple[e1.Triple, int]]:
    """Yield the exact B1 support in a pinned deterministic traversal order."""

    partitions = sorted(
        e1.partitions_upto(ROWS, MAXIMUM_INNER_SIZE),
        key=lambda p: (sum(p), p),
    )
    for left_index, left in enumerate(partitions):
        for right in partitions[left_index:]:
            outputs = lrcalc.mult(list(left), list(right), rows=ROWS)
            if not isinstance(outputs, Mapping):
                raise BakeoffError("lrcalc.mult did not return a mapping")
            target_weight = sum(left) + sum(right)
            normalized: list[tuple[e1.Partition, int]] = []
            for raw_outer, raw_coefficient in outputs.items():
                outer = tuple(raw_outer)
                if (
                    (not outer and target_weight != 0)
                    or any(type(part) is not int or part <= 0 for part in outer)
                    or any(outer[i] < outer[i + 1] for i in range(len(outer) - 1))
                    or len(outer) > ROWS
                    or sum(outer) != target_weight
                    or not _contains(outer, left)
                    or not _contains(outer, right)
                ):
                    raise BakeoffError(
                        f"invalid lrcalc support output {outer!r} for {left!r},{right!r}"
                    )
                if type(raw_coefficient) is not int or raw_coefficient <= 0:
                    raise BakeoffError(
                        f"invalid N=1 coefficient {raw_coefficient!r} for {outer!r}"
                    )
                normalized.append((outer, raw_coefficient))
            for outer, coefficient in sorted(normalized, key=lambda item: item[0]):
                yield e1.canonical_triple(left, right, outer), coefficient


def _largest_remainder_quotas(
    counts: Mapping[tuple[int, int], int], target: int
) -> dict[tuple[int, int], int]:
    if target < 0:
        raise ValueError("target must be nonnegative")
    total = sum(counts.values())
    if total < target:
        raise BakeoffError(f"pool has only {total} records for target {target}")
    if total == 0:
        return {key: 0 for key in counts}
    quotas = {key: target * count // total for key, count in counts.items()}
    remainder = target - sum(quotas.values())
    order = sorted(
        counts,
        key=lambda key: (-(target * counts[key] % total), key),
    )
    for key in order[:remainder]:
        quotas[key] += 1
    if sum(quotas.values()) != target:
        raise AssertionError("largest-remainder allocation failed")
    return quotas


def freeze_panel(work_dir: Path) -> dict[str, Any]:
    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    plan = build_plan()
    plan_sha = _write_pinned_json(work_dir / "plan.json", plan)
    _require_plan(work_dir)
    panel_path = work_dir / "panel.json"
    if panel_path.exists():
        artifact, panel_sha = _load_pinned_json(panel_path)
        if (
            artifact.get("schema_version") != PANEL_SCHEMA
            or artifact.get("plan_sha256") != plan_sha
            or artifact.get("universe", {}).get("count") != EXPECTED_UNIVERSE_SIZE
            or artifact.get("panel", {}).get("size") != PANEL_SIZE
        ):
            raise BakeoffError("existing panel does not match the frozen plan")
        return {
            "stage": "panel-frozen",
            "plan_sha256": plan_sha,
            "panel_sha256": panel_sha,
            "universe_count": EXPECTED_UNIVERSE_SIZE,
            "reeve_family_pool_count": artifact["reeve_family_pool"]["count"],
            "panel_size": PANEL_SIZE,
            "reused": True,
        }

    b1_counts: Counter[int] = Counter()
    universe_counts: Counter[int] = Counter()
    pool_counts: Counter[tuple[int, int]] = Counter()
    heaps: dict[tuple[int, int], list[tuple[int, int, dict[str, Any]]]] = {}
    universe_digest = hashlib.sha256(b"lr-p3-reeve-universe-stream/v1\0")

    for triple, coefficient in iter_b1_support():
        lam, mu, nu = triple
        outer_rows = len(nu)
        b1_counts[outer_rows] += 1
        if max(sum(lam), sum(mu)) <= B0_MAXIMUM_INNER_SIZE:
            continue
        if outer_rows not in ELIGIBLE_OUTER_ROWS:
            continue
        universe_counts[outer_rows] += 1
        encoded = canonical_json_bytes(_triple_dict(triple))
        universe_digest.update(len(encoded).to_bytes(4, "big"))
        universe_digest.update(encoded)
        if coefficient != 4:
            continue
        stratum = (outer_rows, max(sum(lam), sum(mu)))
        pool_counts[stratum] += 1
        selection_key = _domain_hash("lr-p3-reeve-panel-selection/v1", triple)
        triple_id = _triple_id(triple)
        entry = {
            "triple_id": triple_id,
            "triple": _triple_dict(triple),
            "n1_coefficient": 4,
            "stratum": [stratum[0], stratum[1]],
            "selection_key_sha256": selection_key,
        }
        heap = heaps.setdefault(stratum, [])
        heap_entry = (-int(selection_key, 16), -int(triple_id, 16), entry)
        if len(heap) < PANEL_SIZE:
            heapq.heappush(heap, heap_entry)
        elif (int(selection_key, 16), int(triple_id, 16)) < (
            -heap[0][0], -heap[0][1]
        ):
            heapq.heapreplace(heap, heap_entry)

    if dict(sorted(b1_counts.items())) != EXPECTED_B1_BY_OUTER_ROWS:
        raise BakeoffError(
            f"B1 support anchor mismatch: {dict(sorted(b1_counts.items()))!r}"
        )
    if dict(sorted(universe_counts.items())) != EXPECTED_UNIVERSE_BY_OUTER_ROWS:
        raise BakeoffError(
            "prospective universe anchor mismatch: "
            f"{dict(sorted(universe_counts.items()))!r}"
        )
    if sum(universe_counts.values()) != EXPECTED_UNIVERSE_SIZE:
        raise BakeoffError("prospective universe total mismatch")

    quotas = _largest_remainder_quotas(pool_counts, PANEL_SIZE)
    selected: list[dict[str, Any]] = []
    for stratum in sorted(pool_counts):
        retained = [item[2] for item in heaps[stratum]]
        retained.sort(key=lambda item: (
            item["selection_key_sha256"], item["triple_id"]
        ))
        selected.extend(retained[:quotas[stratum]])
    selected.sort(key=lambda item: (
        item["stratum"], item["selection_key_sha256"], item["triple_id"]
    ))
    if len(selected) != PANEL_SIZE:
        raise AssertionError("panel selection did not produce its frozen size")
    if len({item["triple_id"] for item in selected}) != PANEL_SIZE:
        raise AssertionError("panel contains a duplicate triple")

    artifact = {
        "schema_version": PANEL_SCHEMA,
        "plan_sha256": plan_sha,
        "universe": {
            "count": sum(universe_counts.values()),
            "count_by_outer_rows": {
                str(k): universe_counts[k] for k in sorted(universe_counts)
            },
            "stream_sha256": universe_digest.hexdigest(),
        },
        "reeve_family_pool": {
            "condition": "c(1)==4",
            "count": sum(pool_counts.values()),
            "count_by_stratum": {
                f"rows={key[0]},max_inner_size={key[1]}": pool_counts[key]
                for key in sorted(pool_counts)
            },
        },
        "panel": {
            "size": PANEL_SIZE,
            "quota_by_stratum": {
                f"rows={key[0]},max_inner_size={key[1]}": quotas[key]
                for key in sorted(quotas)
            },
            "entries": selected,
        },
    }
    panel_sha = _write_pinned_json(work_dir / "panel.json", artifact)
    return {
        "stage": "panel-frozen",
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "universe_count": EXPECTED_UNIVERSE_SIZE,
        "reeve_family_pool_count": sum(pool_counts.values()),
        "panel_size": PANEL_SIZE,
    }


def _decode_vertices(
    raw_vertices: Any, ambient_dimension: int
) -> tuple[list[list[Fraction]], bool]:
    if not isinstance(raw_vertices, list):
        raise BakeoffError("Normaliz vertices are not a list")
    vertices: list[list[Fraction]] = []
    for raw in raw_vertices:
        if (
            not isinstance(raw, list)
            or len(raw) != ambient_dimension + 1
            or any(type(value) is not int for value in raw)
            or raw[-1] == 0
        ):
            raise BakeoffError(f"malformed Normaliz vertex {raw!r}")
        denominator = raw[-1]
        vertices.append([Fraction(value, denominator) for value in raw[:-1]])
    integral = all(value.denominator == 1 for vertex in vertices for value in vertex)
    return vertices, integral


def _determinant3(matrix: Sequence[Sequence[int]], cols: tuple[int, int, int]) -> int:
    a, b, c = cols
    x = matrix
    return (
        x[0][a] * (x[1][b] * x[2][c] - x[1][c] * x[2][b])
        - x[0][b] * (x[1][a] * x[2][c] - x[1][c] * x[2][a])
        + x[0][c] * (x[1][a] * x[2][b] - x[1][b] * x[2][a])
    )


def normalized_tetrahedron_volume(vertices: Sequence[Sequence[int]]) -> int:
    """Return normalized volume in the saturated affine lattice."""

    if len(vertices) != 4:
        raise ValueError("a tetrahedron needs exactly four vertices")
    ambient = len(vertices[0])
    if ambient < 3 or any(len(vertex) != ambient for vertex in vertices):
        raise ValueError("tetrahedron vertices have incompatible ambient dimensions")
    edges = [
        [vertices[row + 1][col] - vertices[0][col] for col in range(ambient)]
        for row in range(3)
    ]
    volume = 0
    for cols in combinations(range(ambient), 3):
        volume = math.gcd(volume, abs(_determinant3(edges, cols)))
    if volume == 0:
        raise BakeoffError("four claimed tetrahedron vertices are affinely dependent")
    return volume


def _reeve_polynomial(volume: int) -> list[str]:
    return [
        "1",
        str(Fraction(12 - volume, 6)),
        "1",
        str(Fraction(volume, 6)),
    ]


def _geometry_record(
    panel_entry: Mapping[str, Any], plan_sha: str, panel_sha: str
) -> dict[str, Any]:
    triple = _dict_triple(panel_entry["triple"])
    if panel_entry.get("n1_coefficient") != 4:
        raise BakeoffError("geometry panel is not uniformly c(1)=4")
    polytope = e2.build_hive_polytope(*triple, n=len(triple[2]))
    try:
        from PyNormaliz import Cone
    except ImportError as exc:
        raise BakeoffError("PyNormaliz is required for geometry") from exc
    cone = Cone(inhom_inequalities=polytope.normaliz_rows)
    affine_dimension = int(cone.AffineDim())
    raw_vertices = cone.VerticesOfPolyhedron()
    vertices, integral = _decode_vertices(raw_vertices, polytope.ambient_dimension)
    volume: int | None = None
    exact_empty_tetrahedron = (
        affine_dimension == 3 and len(vertices) == 4 and integral
    )
    if exact_empty_tetrahedron:
        integral_vertices = [
            [int(value) for value in vertex] for vertex in vertices
        ]
        volume = normalized_tetrahedron_volume(integral_vertices)
    return {
        "schema_version": GEOMETRY_ITEM_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "triple_id": panel_entry["triple_id"],
        "triple": panel_entry["triple"],
        "query_contract": ["AffineDim", "VerticesOfPolyhedron"],
        "ambient_dimension": polytope.ambient_dimension,
        "affine_dimension": affine_dimension,
        "vertex_count": len(vertices),
        "vertices_raw": raw_vertices,
        "vertices_canonical": [
            [str(value) for value in vertex] for vertex in vertices
        ],
        "all_vertices_integral": integral,
        "predicted_empty_integral_tetrahedron": exact_empty_tetrahedron,
        "normalized_volume": volume,
        "predicted_polynomial": _reeve_polynomial(volume) if volume is not None else None,
        "predicted_reeve_negative_signature": bool(volume is not None and volume > 12),
    }


def build_geometry(work_dir: Path, *, max_items: int | None = None) -> dict[str, Any]:
    work_dir = Path(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = _load_pinned_json(work_dir / "panel.json")
    if panel.get("schema_version") != PANEL_SCHEMA or panel.get("plan_sha256") != plan_sha:
        raise BakeoffError("panel does not belong to frozen plan")
    entries = panel["panel"]["entries"]
    item_dir = work_dir / "geometry" / "items"
    item_dir.mkdir(parents=True, exist_ok=True)
    completed: list[dict[str, Any]] = []
    new_count = 0
    for entry in entries:
        item_path = item_dir / f"{entry['triple_id']}.json"
        if item_path.exists() and _sidecar(item_path).exists():
            record, record_sha = _load_pinned_json(item_path)
        else:
            if max_items is not None and new_count >= max_items:
                continue
            record = _geometry_record(entry, plan_sha, panel_sha)
            record_sha = _write_pinned_json(item_path, record)
            new_count += 1
        if (
            record.get("schema_version") != GEOMETRY_ITEM_SCHEMA
            or record.get("plan_sha256") != plan_sha
            or record.get("panel_sha256") != panel_sha
            or record.get("triple_id") != entry["triple_id"]
        ):
            raise BakeoffError(f"invalid geometry record {item_path}")
        completed.append({
            "triple_id": entry["triple_id"],
            "item_sha256": record_sha,
            "features": {
                key: record[key]
                for key in (
                    "ambient_dimension",
                    "affine_dimension",
                    "vertex_count",
                    "all_vertices_integral",
                    "predicted_empty_integral_tetrahedron",
                    "normalized_volume",
                    "predicted_polynomial",
                    "predicted_reeve_negative_signature",
                )
            },
        })
    if len(completed) != len(entries):
        return {
            "stage": "geometry-partial",
            "completed": len(completed),
            "total": len(entries),
            "new_items": new_count,
        }
    artifact = {
        "schema_version": GEOMETRY_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "query_contract": ["AffineDim", "VerticesOfPolyhedron"],
        "ehrhart_queries_before_rank_freeze": 0,
        "item_count": len(completed),
        "items": completed,
        "summary": {
            "affine_dimension_counts": {
                str(d): sum(item["features"]["affine_dimension"] == d for item in completed)
                for d in sorted({item["features"]["affine_dimension"] for item in completed})
            },
            "predicted_empty_integral_tetrahedra": sum(
                item["features"]["predicted_empty_integral_tetrahedron"] for item in completed
            ),
            "predicted_reeve_negative_signatures": sum(
                item["features"]["predicted_reeve_negative_signature"] for item in completed
            ),
        },
    }
    geometry_sha = _write_pinned_json(work_dir / "geometry.json", artifact)
    return {
        "stage": "geometry-frozen",
        "geometry_sha256": geometry_sha,
        **artifact["summary"],
        "new_items": new_count,
    }


def _ranking_key(
    arm: str, entry: Mapping[str, Any], features: Mapping[str, Any]
) -> tuple[Any, ...]:
    triple = _dict_triple(entry["triple"])
    lam, mu, nu = triple
    tie = _domain_hash(f"lr-p3-reeve-ranking-{arm}/v1", triple)
    if arm == "reeve_volume":
        certificate = bool(features["predicted_reeve_negative_signature"])
        exact = bool(features["predicted_empty_integral_tetrahedron"])
        volume = features["normalized_volume"]
        return (
            0 if certificate else 1,
            0 if exact else 1,
            -(volume if isinstance(volume, int) else -1),
            abs(int(features["affine_dimension"]) - 3),
            abs(int(features["vertex_count"]) - 4),
            tie,
        )
    if arm == "integral_tetrahedron_ablation":
        exact = bool(features["predicted_empty_integral_tetrahedron"])
        return (
            0 if exact else 1,
            abs(int(features["affine_dimension"]) - 3),
            abs(int(features["vertex_count"]) - 4),
            tie,
        )
    if arm == "affine_dimension_3":
        dimension = int(features["affine_dimension"])
        return (0 if dimension == 3 else 1, abs(dimension - 3), tie)
    if arm == "rows_size":
        left_size, right_size = sum(lam), sum(mu)
        return (
            -len(nu),
            -max(left_size, right_size),
            abs(left_size - right_size),
            -min(left_size, right_size),
            tie,
        )
    if arm == "stratified_random":
        return (tie,)
    raise AssertionError(f"unknown arm {arm}")


def freeze_rankings(work_dir: Path) -> dict[str, Any]:
    work_dir = Path(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = _load_pinned_json(work_dir / "panel.json")
    geometry, geometry_sha = _load_pinned_json(work_dir / "geometry.json")
    if geometry.get("schema_version") != GEOMETRY_SCHEMA:
        raise BakeoffError("invalid geometry artifact")
    if geometry.get("plan_sha256") != plan_sha or geometry.get("panel_sha256") != panel_sha:
        raise BakeoffError("geometry provenance mismatch")
    panel_by_id = {
        entry["triple_id"]: entry for entry in panel["panel"]["entries"]
    }
    features_by_id = {
        item["triple_id"]: item["features"] for item in geometry["items"]
    }
    rankings: dict[str, list[dict[str, Any]]] = {}
    selection_details: dict[str, Any] = {}
    for arm in ARMS:
        if arm == "stratified_random":
            counts = Counter(
                tuple(entry["stratum"]) for entry in panel_by_id.values()
            )
            quotas = _largest_remainder_quotas(counts, ARM_BUDGET)
            selected: list[Mapping[str, Any]] = []
            for stratum in sorted(counts):
                within = sorted(
                    (
                        entry for entry in panel_by_id.values()
                        if tuple(entry["stratum"]) == stratum
                    ),
                    key=lambda entry: _ranking_key(
                        arm, entry, features_by_id[entry["triple_id"]]
                    ),
                )
                selected.extend(within[:quotas[stratum]])
            ordered = sorted(
                selected,
                key=lambda entry: _ranking_key(
                    arm, entry, features_by_id[entry["triple_id"]]
                ),
            )
            selection_details[arm] = {
                "method": "proportional-stratified-domain-hash",
                "quota_by_stratum": {
                    f"rows={key[0]},max_inner_size={key[1]}": quotas[key]
                    for key in sorted(quotas)
                },
            }
        else:
            ordered = sorted(
                panel_by_id.values(),
                key=lambda entry: _ranking_key(
                    arm, entry, features_by_id[entry["triple_id"]]
                ),
            )
            selection_details[arm] = {"method": "global-score-order"}
        rankings[arm] = [
            {
                "rank": index + 1,
                "triple_id": entry["triple_id"],
                "score_key": list(_ranking_key(
                    arm, entry, features_by_id[entry["triple_id"]]
                )),
            }
            for index, entry in enumerate(ordered[:ARM_BUDGET])
        ]
        if len({item["triple_id"] for item in rankings[arm]}) != ARM_BUDGET:
            raise AssertionError(f"arm {arm} contains duplicate candidates")
    union = {item["triple_id"] for arm in ARMS for item in rankings[arm]}
    artifact = {
        "schema_version": RANKINGS_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "stretched_polynomial_queries_before_freeze": 0,
        "arm_budget": ARM_BUDGET,
        "arms": rankings,
        "selection_details": selection_details,
        "fixed_union_size": len(union),
        "overlap_count": len(ARMS) * ARM_BUDGET - len(union),
    }
    rankings_sha = _write_pinned_json(work_dir / "rankings.json", artifact)
    return {
        "stage": "rankings-frozen",
        "rankings_sha256": rankings_sha,
        "arm_budget": ARM_BUDGET,
        "fixed_union_size": len(union),
        "overlap_count": artifact["overlap_count"],
    }


def _polynomial_metrics(polynomial: Sequence[str]) -> dict[str, Any]:
    values = [Fraction(value) for value in polynomial]
    negative_indices = [index for index, value in enumerate(values) if value < 0]
    if len(values) >= 3:
        q = min(values[1:-1])
        gain = max(Fraction(0), Fraction(1) - q)
    else:
        q = None
        gain = Fraction(0)
    return {
        "degree": len(values) - 1,
        "negative_indices": negative_indices,
        "has_negative_coefficient": bool(negative_indices),
        "min_interior_coefficient": str(q) if q is not None else None,
        "subunit_interior": bool(q is not None and q < 1),
        "gain": str(gain),
    }


def _evaluation_record(
    panel_entry: Mapping[str, Any],
    geometry_features: Mapping[str, Any],
    *,
    plan_sha: str,
    panel_sha: str,
    geometry_sha: str,
    rankings_sha: str,
) -> dict[str, Any]:
    triple = _dict_triple(panel_entry["triple"])
    n1 = e1.lr_coefficient(*triple)
    if n1 != 4:
        raise BakeoffError(f"frozen c(1)=4 membership failed for {triple!r}: {n1}")
    first = e1.evaluate_stretched(*triple, mode="bounded", known_n1=n1)
    first_polynomial = e1.canonical_polynomial_strings(first.polynomial)
    polytope = e2.build_hive_polytope(*triple, n=len(triple[2]))
    second_raw = e2.evaluate_with_normaliz(polytope)
    second_polynomial = second_raw.get("canonical_polynomial")
    if not isinstance(second_polynomial, list):
        raise BakeoffError("E2 did not return a canonical polynomial")
    second_polynomial = e1.canonical_polynomial_strings(
        [Fraction(value) for value in second_polynomial]
    )
    if not second_raw.get("period_collapses_to_one"):
        raise BakeoffError("E2 returned a nontrivial quasiperiod")
    if type(second_raw.get("number_lattice_points")) is not int:
        raise BakeoffError("E2 N=1 count is not an exact integer")
    if second_raw["number_lattice_points"] != n1:
        raise BakeoffError("E1/E2 N=1 disagreement")
    if first_polynomial != second_polynomial:
        raise BakeoffError(
            f"E1/E2 polynomial disagreement for {triple!r}: "
            f"{first_polynomial!r} != {second_polynomial!r}"
        )
    predicted = geometry_features.get("predicted_polynomial")
    if predicted is not None and predicted != first_polynomial:
        raise BakeoffError(
            f"empty-tetrahedron formula disagrees with evaluators for {triple!r}: "
            f"{predicted!r} != {first_polynomial!r}"
        )
    metrics = _polynomial_metrics(first_polynomial)
    conservative: dict[str, Any] | None = None
    if metrics["has_negative_coefficient"]:
        checked = e1.evaluate_stretched(
            *triple, mode="conservative", known_n1=n1
        )
        checked_polynomial = e1.canonical_polynomial_strings(checked.polynomial)
        if checked_polynomial != first_polynomial:
            raise BakeoffError("conservative E1 candidate check changed polynomial")
        conservative = checked.evidence()
    return {
        "schema_version": EVALUATION_ITEM_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "rankings_sha256": rankings_sha,
        "triple_id": panel_entry["triple_id"],
        "triple": panel_entry["triple"],
        "canonical_polynomial": first_polynomial,
        "metrics": metrics,
        "agreement": {
            "canonical_polynomials_match": True,
            "n1_counts_match": True,
            "empty_tetrahedron_formula_match": predicted is None or predicted == first_polynomial,
        },
        "e1": {
            "engine": "lrcalc-exact-interpolation",
            "bounded_evidence": first.evidence(),
            "conservative_candidate_evidence": conservative,
        },
        "e2": {
            "engine": second_raw.get("engine"),
            "canonical_polynomial": second_polynomial,
            "number_lattice_points_at_n1": second_raw["number_lattice_points"],
            "affine_dimension": second_raw.get("affine_dimension"),
            "raw_period": second_raw.get("raw_period"),
            "raw_common_denominator": second_raw.get("raw_common_denominator"),
            "residue_polynomials": second_raw.get("residue_polynomials"),
            "period_collapses_to_one": second_raw.get("period_collapses_to_one"),
            "ehrhart_quasipolynomial_raw": second_raw.get("ehrhart_quasipolynomial_raw"),
        },
        "geometry_prediction": {
            "predicted_empty_integral_tetrahedron": geometry_features.get(
                "predicted_empty_integral_tetrahedron"
            ),
            "normalized_volume": geometry_features.get("normalized_volume"),
            "predicted_polynomial": predicted,
            "predicted_reeve_negative_signature": geometry_features.get(
                "predicted_reeve_negative_signature"
            ),
        },
    }


def evaluate_union(work_dir: Path, *, max_items: int | None = None) -> dict[str, Any]:
    work_dir = Path(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = _load_pinned_json(work_dir / "panel.json")
    geometry, geometry_sha = _load_pinned_json(work_dir / "geometry.json")
    rankings, rankings_sha = _load_pinned_json(work_dir / "rankings.json")
    if rankings.get("schema_version") != RANKINGS_SCHEMA:
        raise BakeoffError("invalid rankings artifact")
    if (
        rankings.get("plan_sha256") != plan_sha
        or rankings.get("panel_sha256") != panel_sha
        or rankings.get("geometry_sha256") != geometry_sha
    ):
        raise BakeoffError("rankings provenance mismatch")
    panel_by_id = {
        entry["triple_id"]: entry for entry in panel["panel"]["entries"]
    }
    features_by_id = {
        item["triple_id"]: item["features"] for item in geometry["items"]
    }
    ordered_union: list[str] = []
    seen: set[str] = set()
    for rank in range(ARM_BUDGET):
        for arm in ARMS:
            triple_id = rankings["arms"][arm][rank]["triple_id"]
            if triple_id not in seen:
                seen.add(triple_id)
                ordered_union.append(triple_id)
    if len(ordered_union) != rankings["fixed_union_size"]:
        raise BakeoffError("frozen union identity mismatch")
    item_dir = work_dir / "evaluations" / "items"
    item_dir.mkdir(parents=True, exist_ok=True)
    completed: list[dict[str, Any]] = []
    new_count = 0
    for triple_id in ordered_union:
        item_path = item_dir / f"{triple_id}.json"
        if item_path.exists() and _sidecar(item_path).exists():
            record, record_sha = _load_pinned_json(item_path)
        else:
            if max_items is not None and new_count >= max_items:
                continue
            record = _evaluation_record(
                panel_by_id[triple_id],
                features_by_id[triple_id],
                plan_sha=plan_sha,
                panel_sha=panel_sha,
                geometry_sha=geometry_sha,
                rankings_sha=rankings_sha,
            )
            record_sha = _write_pinned_json(item_path, record)
            new_count += 1
        if (
            record.get("schema_version") != EVALUATION_ITEM_SCHEMA
            or record.get("plan_sha256") != plan_sha
            or record.get("rankings_sha256") != rankings_sha
            or record.get("triple_id") != triple_id
        ):
            raise BakeoffError(f"invalid evaluation record {item_path}")
        completed.append({
            "triple_id": triple_id,
            "item_sha256": record_sha,
            "canonical_polynomial": record["canonical_polynomial"],
            "metrics": record["metrics"],
        })
    if len(completed) != len(ordered_union):
        return {
            "stage": "evaluation-partial",
            "completed": len(completed),
            "total": len(ordered_union),
            "new_items": new_count,
        }
    artifact = {
        "schema_version": EVALUATIONS_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "rankings_sha256": rankings_sha,
        "fixed_union_size": len(ordered_union),
        "all_e1_e2_agree": True,
        "negative_count": sum(
            item["metrics"]["has_negative_coefficient"] for item in completed
        ),
        "items": completed,
    }
    evaluations_sha = _write_pinned_json(work_dir / "evaluations.json", artifact)
    return {
        "stage": "evaluation-complete",
        "evaluations_sha256": evaluations_sha,
        "fixed_union_size": len(completed),
        "negative_count": artifact["negative_count"],
        "new_items": new_count,
    }


def _arm_summary(
    ranking: Sequence[Mapping[str, Any]], records: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    negatives: list[dict[str, Any]] = []
    q_values: list[Fraction] = []
    gains: list[Fraction] = []
    subunit = 0
    degrees: Counter[int] = Counter()
    for ranked in ranking:
        record = records[ranked["triple_id"]]
        metrics = record["metrics"]
        degrees[int(metrics["degree"])] += 1
        if metrics["has_negative_coefficient"]:
            negatives.append({
                "rank": ranked["rank"],
                "triple_id": ranked["triple_id"],
                "polynomial": record["canonical_polynomial"],
            })
        if metrics["min_interior_coefficient"] is not None:
            q_values.append(Fraction(metrics["min_interior_coefficient"]))
        if metrics["subunit_interior"]:
            subunit += 1
        gains.append(Fraction(metrics["gain"]))
    return {
        "evaluated": len(ranking),
        "negative_count": len(negatives),
        "negative_candidates": negatives,
        "first_negative_rank": negatives[0]["rank"] if negatives else None,
        "subunit_interior_count_descriptive_only": subunit,
        "best_min_interior_descriptive_only": str(min(q_values)) if q_values else None,
        "sum_gain_descriptive_only": str(sum(gains, Fraction(0))),
        "degree_distribution_post_scoring": {
            str(degree): degrees[degree] for degree in sorted(degrees)
        },
    }


def adjudicate(work_dir: Path) -> dict[str, Any]:
    work_dir = Path(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = _load_pinned_json(work_dir / "panel.json")
    geometry, geometry_sha = _load_pinned_json(work_dir / "geometry.json")
    rankings, rankings_sha = _load_pinned_json(work_dir / "rankings.json")
    evaluations, evaluations_sha = _load_pinned_json(work_dir / "evaluations.json")
    if evaluations.get("schema_version") != EVALUATIONS_SCHEMA:
        raise BakeoffError("invalid evaluations artifact")
    if evaluations.get("rankings_sha256") != rankings_sha:
        raise BakeoffError("evaluation provenance mismatch")
    records = {item["triple_id"]: item for item in evaluations["items"]}
    arm_summaries = {
        arm: _arm_summary(rankings["arms"][arm], records) for arm in ARMS
    }
    all_negative_ids = sorted({
        item["triple_id"]
        for item in evaluations["items"]
        if item["metrics"]["has_negative_coefficient"]
    })
    if all_negative_ids:
        decision = "CANDIDATE_VERIFICATION_EVENT"
        control_ranks = [
            arm_summaries[arm]["first_negative_rank"]
            for arm in ARMS[1:]
            if arm_summaries[arm]["first_negative_rank"] is not None
        ]
        reeve_rank = arm_summaries["reeve_volume"]["first_negative_rank"]
        earliest_control = min(control_ranks) if control_ranks else ARM_BUDGET + 1
        reeve_ranking_advantage = bool(
            reeve_rank is not None and 2 * reeve_rank <= earliest_control
        )
        rationale = (
            "At least one negative passed both exact evaluators and conservative "
            "E1 checking; candidate verification supersedes bake-off scaling."
        )
    else:
        decision = "NO_GO_EMPTY_REEVE_P3_ROUTE"
        reeve_ranking_advantage = False
        rationale = (
            "No arm found the target. Positive near-zero proxies are deliberately "
            "non-authorizing, so the empty-Reeve route stops at this budget."
        )
    artifact = {
        "schema_version": ADJUDICATION_SCHEMA,
        "classification": "internal-non-certifying-bakeoff",
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "rankings_sha256": rankings_sha,
        "evaluations_sha256": evaluations_sha,
        "cost": {
            "n1_schur_product_queries": EXPECTED_B1_UNORDERED_INNER_PAIRS,
            "b1_positive_support_records_visited": EXPECTED_B1_SUPPORT_SIZE,
            "prospective_universe_records": EXPECTED_UNIVERSE_SIZE,
            "geometry_proxy_queries": geometry["item_count"],
            "exact_distinct_polynomial_evaluations": evaluations["fixed_union_size"],
            "nominal_exact_evaluations_per_arm": ARM_BUDGET,
            "overlaps_not_replaced": rankings["overlap_count"],
        },
        "geometry_summary": geometry["summary"],
        "arms": arm_summaries,
        "negative_triple_ids": all_negative_ids,
        "conditional_rank_advantage_after_shared_geometry_if_candidate": (
            reeve_ranking_advantage
        ),
        "rank_advantage_scope": (
            "conditional on the shared 512-item geometry pass; not an end-to-end "
            "lower-compute claim against cheap controls"
        ),
        "decision": decision,
        "rationale": rationale,
        "full_p3_authorized": False,
        "outcome_claim": None,
    }
    adjudication_sha = _write_pinned_json(work_dir / "adjudication.json", artifact)

    summary_lines = [
        "# P3 empty-Reeve bake-off result",
        "",
        f"**Decision: {decision}.**",
        "",
        rationale,
        "",
        f"- Prospective universe: {EXPECTED_UNIVERSE_SIZE:,} positive-support triples.",
        f"- Frozen c(1)=4 panel: {panel['panel']['size']} of "
        f"{panel['reeve_family_pool']['count']:,} eligible triples.",
        f"- Geometry queries: {geometry['item_count']}; exact polynomial union: "
        f"{evaluations['fixed_union_size']}.",
        f"- Predicted empty integral tetrahedra: "
        f"{geometry['summary']['predicted_empty_integral_tetrahedra']}; "
        f"predicted Delta>12 signatures: "
        f"{geometry['summary']['predicted_reeve_negative_signatures']}.",
        f"- Verified negatives: {len(all_negative_ids)}.",
        "",
        "Per-arm positive minima and subunit counts are recorded in "
        "`adjudication.json` as descriptive diagnostics only.",
        "",
        "This artifact is internal and non-certifying. It neither revives the "
        "superseded held-out gate nor authorizes a full P3 campaign.",
        "",
    ]
    summary_sha = _write_pinned_text(work_dir / "SUMMARY.md", "\n".join(summary_lines))
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "classification": "internal-non-certifying-bakeoff",
        "files": [
            {"path": name, "sha256": sha256_file(work_dir / name)}
            for name in (
                "plan.json",
                "panel.json",
                "geometry.json",
                "rankings.json",
                "evaluations.json",
                "adjudication.json",
                "SUMMARY.md",
            )
        ],
        "item_collections": {
            "geometry": {
                "count": geometry["item_count"],
                "aggregate_sha256": geometry_sha,
            },
            "evaluations": {
                "count": evaluations["fixed_union_size"],
                "aggregate_sha256": evaluations_sha,
            },
        },
        "adjudication_sha256": adjudication_sha,
        "summary_sha256": summary_sha,
    }
    manifest_sha = _write_pinned_json(work_dir / "manifest.json", manifest)
    return {
        "stage": "adjudicated",
        "decision": decision,
        "negative_count": len(all_negative_ids),
        "adjudication_sha256": adjudication_sha,
        "manifest_sha256": manifest_sha,
    }


def verify(work_dir: Path, *, require_complete: bool = True) -> dict[str, Any]:
    work_dir = Path(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = _load_pinned_json(work_dir / "panel.json")
    verified: dict[str, Any] = {
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "panel_items": panel["panel"]["size"],
    }
    for name, schema in (
        ("geometry.json", GEOMETRY_SCHEMA),
        ("rankings.json", RANKINGS_SCHEMA),
        ("evaluations.json", EVALUATIONS_SCHEMA),
        ("adjudication.json", ADJUDICATION_SCHEMA),
        ("manifest.json", MANIFEST_SCHEMA),
    ):
        path = work_dir / name
        if not path.exists():
            if require_complete:
                raise BakeoffError(f"missing completion artifact {path}")
            continue
        value, digest = _load_pinned_json(path)
        if value.get("schema_version") != schema:
            raise BakeoffError(f"invalid schema in {path}")
        verified[name] = digest
    if (work_dir / "geometry.json").exists():
        geometry, _ = _load_pinned_json(work_dir / "geometry.json")
        for item in geometry["items"]:
            path = work_dir / "geometry" / "items" / f"{item['triple_id']}.json"
            _, digest = _load_pinned_json(path)
            if digest != item["item_sha256"]:
                raise BakeoffError(f"geometry aggregate hash mismatch for {path}")
    if (work_dir / "evaluations.json").exists():
        evaluations, _ = _load_pinned_json(work_dir / "evaluations.json")
        for item in evaluations["items"]:
            path = work_dir / "evaluations" / "items" / f"{item['triple_id']}.json"
            _, digest = _load_pinned_json(path)
            if digest != item["item_sha256"]:
                raise BakeoffError(f"evaluation aggregate hash mismatch for {path}")
    verified["complete"] = (work_dir / "manifest.json").exists()
    return verified


def run_all(work_dir: Path) -> dict[str, Any]:
    stages = [
        freeze_panel(work_dir),
        build_geometry(work_dir),
        freeze_rankings(work_dir),
        evaluate_union(work_dir),
        adjudicate(work_dir),
    ]
    return {"stages": stages, "verification": verify(work_dir)}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--work-dir", type=Path, default=Path("run/p3/reeve-bakeoff")
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("freeze")
    geometry = subparsers.add_parser("geometry")
    geometry.add_argument("--max-items", type=int)
    subparsers.add_parser("rank")
    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("--max-items", type=int)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--allow-partial", action="store_true")
    subparsers.add_parser("adjudicate")
    subparsers.add_parser("run")
    return parser


def main(argv: list[str] | None = None) -> int:
    del argv
    print(
        "ERROR: the arm bake-off is superseded and must not run; "
        "use `python -m p3.reeve_scan`",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
