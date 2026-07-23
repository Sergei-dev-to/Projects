"""Frozen, bounded direct scan for empty-Reeve LR hive polytopes.

The geometric signature used here determines the Ehrhart polynomial exactly,
so this is intentionally *not* described as a ranking bake-off.  Every
prospective artifact is immutable and hash-pinned; a zero-hit run is only a
budget stop for the frozen 512-case panel.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import heapq
from importlib.metadata import PackageNotFoundError, version as package_version
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Any, Mapping, Sequence

import lrcalc

from p1.control.canonical import canonical_json_bytes, sha256_file, sha256_json
from p1.e1 import evaluator as e1
from p1.e2 import hive_e2 as e2
from p3 import bakeoff as core


PLAN_SCHEMA = "lr-p3-empty-reeve-direct-scan-plan/v1"
PANEL_SCHEMA = "lr-p3-empty-reeve-direct-scan-panel/v1"
GEOMETRY_ITEM_SCHEMA = "lr-p3-empty-reeve-direct-geometry-item/v1"
GEOMETRY_SCHEMA = "lr-p3-empty-reeve-direct-geometry/v1"
VERIFICATION_ITEM_SCHEMA = "lr-p3-empty-reeve-candidate-verification-item/v1"
VERIFICATIONS_SCHEMA = "lr-p3-empty-reeve-candidate-verifications/v1"
ADJUDICATION_SCHEMA = "lr-p3-empty-reeve-direct-adjudication/v1"
MANIFEST_SCHEMA = "lr-p3-empty-reeve-direct-manifest/v1"

PANEL_SIZE = 512
SEED = 20260723
DEFAULT_WORK_DIR = Path("run/p3/empty-reeve-scan-v2")
REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_ROOT = (REPO_ROOT / "run" / "p3").resolve()


class ScanError(RuntimeError):
    """Fail-closed direct-scan error."""


def _package(name: str) -> str:
    try:
        return package_version(name)
    except PackageNotFoundError:
        return "unknown"


def _validate_work_dir(path: Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    lexical = Path(os.path.abspath(candidate))
    if lexical == RUN_ROOT or RUN_ROOT not in lexical.parents:
        raise ScanError(f"work directory must be a lexical child of {RUN_ROOT}: {lexical}")
    relative = lexical.relative_to(RUN_ROOT)
    cursor = RUN_ROOT
    for component in relative.parts:
        cursor = cursor / component
        if cursor.exists() and cursor.is_symlink():
            raise ScanError(f"work-directory path contains a symlink: {cursor}")
    resolved = candidate.resolve(strict=False)
    if resolved == RUN_ROOT or RUN_ROOT not in resolved.parents:
        raise ScanError(f"work directory must be a child of {RUN_ROOT}: {resolved}")
    if candidate.exists() and candidate.is_symlink():
        raise ScanError(f"work directory may not be a symlink: {candidate}")
    return resolved


def _validate_max_items(value: int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ScanError("max_items must be a nonnegative integer or null")
    return value


def _runtime_identity() -> dict[str, Any]:
    try:
        import PyNormaliz
        import PyNormaliz_cpp
    except ImportError as exc:
        raise ScanError("PyNormaliz is required") from exc
    os_release = ""
    release_path = Path("/proc/sys/kernel/osrelease")
    if release_path.is_file():
        os_release = release_path.read_text(encoding="utf-8").strip()
    normaliz_path_text = shutil.which("normaliz")
    if normaliz_path_text is None:
        raise ScanError("Normaliz CLI is missing from PATH")
    normaliz_path = Path(normaliz_path_text).resolve()
    try:
        normaliz_version = subprocess.run(
            [str(normaliz_path), "--version"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.splitlines()[0].strip()
    except (OSError, subprocess.SubprocessError, IndexError) as exc:
        raise ScanError("cannot identify the Normaliz CLI") from exc
    identity = {
        "python_version": platform.python_version(),
        "python_executable_invoked": sys.executable,
        "python_executable_resolved": str(Path(sys.executable).resolve()),
        "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix,
        "platform_system": platform.system(),
        "kernel_release": os_release,
        "wsl": platform.system() == "Linux" and "microsoft" in os_release.lower(),
        "lrcalc_version": _package("lrcalc"),
        "pynormaliz_version": _package("PyNormaliz"),
        "normaliz_cli_version": normaliz_version,
        "normaliz_cli_sha256": sha256_file(normaliz_path),
        "lrcalc_module_sha256": sha256_file(Path(lrcalc.__file__).resolve()),
        "pynormaliz_module_sha256": sha256_file(Path(PyNormaliz.__file__).resolve()),
        "pynormaliz_extension_sha256": sha256_file(
            Path(PyNormaliz_cpp.__file__).resolve()
        ),
    }
    expected_venv = (REPO_ROOT / ".venv-wsl").resolve()
    if Path(sys.prefix).resolve() != expected_venv:
        raise ScanError(
            f"scan must use repository venv {expected_venv}, got {sys.prefix}"
        )
    envelope = core.load_json(REPO_ROOT / "run" / "env.json")
    versions = envelope.get("tool_versions", {})
    expected_python = str(versions.get("python", ""))
    expected_lrcalc = str(versions.get("lrcalc", ""))
    expected_pynormaliz = str(versions.get("pynormaliz", "")).split("+")[0]
    expected_normaliz = str(versions.get("normaliz", "")).split("+")[0]
    observed_normaliz = normaliz_version.removeprefix("Normaliz ").strip()
    if (
        identity["python_version"] != expected_python
        or identity["lrcalc_version"] != expected_lrcalc
        or identity["pynormaliz_version"] != expected_pynormaliz
        or observed_normaliz != expected_normaliz
    ):
        raise ScanError(
            "runtime versions do not match run/env.json: "
            f"python={identity['python_version']}, lrcalc={identity['lrcalc_version']}, "
            f"PyNormaliz={identity['pynormaliz_version']}, Normaliz={observed_normaliz}"
        )
    identity["envelope_versions_match"] = True
    return identity


def _source_hashes() -> dict[str, str]:
    from p1.control import atomic, canonical

    return {
        "reeve_scan_py_sha256": sha256_file(Path(__file__).resolve()),
        "reeve_core_py_sha256": sha256_file(Path(core.__file__).resolve()),
        "e1_source_sha256": sha256_file(Path(e1.__file__).resolve()),
        "e2_source_sha256": sha256_file(Path(e2.__file__).resolve()),
        "control_atomic_source_sha256": sha256_file(Path(atomic.__file__).resolve()),
        "control_canonical_source_sha256": sha256_file(Path(canonical.__file__).resolve()),
        "env_json_sha256": sha256_file(REPO_ROOT / "run" / "env.json"),
    }


def build_plan() -> dict[str, Any]:
    runtime = _runtime_identity()
    if not runtime["wsl"]:
        raise ScanError("the direct scan must run inside the pinned WSL environment")
    return {
        "schema_version": PLAN_SCHEMA,
        "classification": "internal-bounded-non-certifying-direct-search",
        "created_date": "2026-07-23",
        "replacement_reason": (
            "the proposed Reeve geometry pass determines the target polynomial; "
            "post-geometry ranking controls would not be a valid efficiency bake-off"
        ),
        "superseded_gate_revived": False,
        "runtime": runtime,
        "sources": _source_hashes(),
        "universe": {
            "scope": "B1 positive N=1 support minus B0-7, len(nu)>=4",
            "maximum_length": core.ROWS,
            "maximum_size_each_inner": core.MAXIMUM_INNER_SIZE,
            "excluded_if_both_inner_sizes_at_most": core.B0_MAXIMUM_INNER_SIZE,
            "eligible_outer_rows": list(core.ELIGIBLE_OUTER_ROWS),
            "expected_count": core.EXPECTED_UNIVERSE_SIZE,
            "expected_count_by_outer_rows": {
                str(key): value
                for key, value in core.EXPECTED_UNIVERSE_BY_OUTER_ROWS.items()
            },
            "swap_only_canonicalization": True,
        },
        "mechanism_slice": {
            "condition": "c^nu_lam,mu(1)==4",
            "interpretation": "paid common N=1 preprocessing; not label-free",
            "scope_caveat": "results say nothing about other negative mechanisms",
        },
        "panel": {
            "size": PANEL_SIZE,
            "seed": SEED,
            "selection": (
                "largest-remainder proportional allocation over "
                "(len(nu),max inner size), then lowest domain-separated hashes"
            ),
            "no_reroll": True,
        },
        "geometry": {
            "calls_per_panel_item": ["AffineDim", "VerticesOfPolyhedron"],
            "cone_constructions": PANEL_SIZE,
            "normaliz_geometry_calls": 2 * PANEL_SIZE,
            "ehrhart_calls_before_signature_freeze": 0,
            "signature": (
                "affine dimension 3; exactly four integral vertices; "
                "normalized saturated-lattice volume Delta>12"
            ),
            "formula": ["1", "(12-Delta)/6", "1", "Delta/6"],
        },
        "candidate_verification": {
            "scope": "every frozen Delta>12 signature and no other panel item",
            "e1_modes": ["bounded", "conservative"],
            "e2": "explicit hive plus raw period-one Normaliz Ehrhart",
            "require_bit_identical_polynomial": True,
        },
        "budget_accounting": {
            "n1_schur_product_queries": core.EXPECTED_B1_UNORDERED_INNER_PAIRS,
            "b1_positive_support_records_visited": core.EXPECTED_B1_SUPPORT_SIZE,
            "prospective_universe_records": core.EXPECTED_UNIVERSE_SIZE,
            "panel_geometry_items": PANEL_SIZE,
            "candidate_polynomial_evaluations": "number of frozen signatures only",
        },
        "outcomes": {
            "hit": "CANDIDATE_VERIFICATION_EVENT; no automatic scaling or publication",
            "zero_hit": "BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL",
            "zero_hit_caveat": (
                "not evidence the mechanism is absent from the universe and not "
                "evidence for LR positivity"
            ),
        },
    }


def _require_plan(work_dir: Path) -> tuple[dict[str, Any], str]:
    plan, digest = core._load_pinned_json(work_dir / "plan.json")
    expected = build_plan()
    if plan != expected:
        raise ScanError("loaded plan is not exactly the current pinned plan")
    return plan, digest


def _selection_hash(triple: e1.Triple) -> str:
    return sha256_json({
        "domain": "lr-p3-empty-reeve-direct-panel/v1",
        "seed": SEED,
        "triple": core._triple_dict(triple),
    })


def _stream_step(digest: Any, triple: e1.Triple) -> None:
    encoded = canonical_json_bytes(core._triple_dict(triple))
    digest.update(len(encoded).to_bytes(4, "big"))
    digest.update(encoded)


def _generate_panel_artifact(plan_sha: str) -> dict[str, Any]:
    """Regenerate the complete support hashes and deterministic frozen panel."""

    b1_counts: Counter[int] = Counter()
    universe_counts: Counter[int] = Counter()
    pool_counts: Counter[tuple[int, int]] = Counter()
    universe_digest = hashlib.sha256(b"lr-p3-empty-reeve-universe/v1\0")
    pool_digest = hashlib.sha256(b"lr-p3-empty-reeve-c1-equals-4-pool/v1\0")
    heaps: dict[tuple[int, int], list[tuple[int, int, dict[str, Any]]]] = {}

    for triple, coefficient in core.iter_b1_support():
        lam, mu, nu = triple
        b1_counts[len(nu)] += 1
        if max(sum(lam), sum(mu)) <= core.B0_MAXIMUM_INNER_SIZE:
            continue
        if len(nu) not in core.ELIGIBLE_OUTER_ROWS:
            continue
        universe_counts[len(nu)] += 1
        _stream_step(universe_digest, triple)
        if coefficient != 4:
            continue
        _stream_step(pool_digest, triple)
        stratum = (len(nu), max(sum(lam), sum(mu)))
        pool_counts[stratum] += 1
        selection_key = _selection_hash(triple)
        triple_id = core._triple_id(triple)
        entry = {
            "triple_id": triple_id,
            "triple": core._triple_dict(triple),
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

    if dict(sorted(b1_counts.items())) != core.EXPECTED_B1_BY_OUTER_ROWS:
        raise ScanError(f"B1 support anchor mismatch: {dict(b1_counts)!r}")
    if dict(sorted(universe_counts.items())) != core.EXPECTED_UNIVERSE_BY_OUTER_ROWS:
        raise ScanError(f"universe anchor mismatch: {dict(universe_counts)!r}")
    quotas = core._largest_remainder_quotas(pool_counts, PANEL_SIZE)
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
    if len(selected) != PANEL_SIZE or len({x["triple_id"] for x in selected}) != PANEL_SIZE:
        raise ScanError("panel selection failed size or uniqueness check")
    artifact = {
        "schema_version": PANEL_SCHEMA,
        "plan_sha256": plan_sha,
        "universe": {
            "count": sum(universe_counts.values()),
            "count_by_outer_rows": {
                str(key): universe_counts[key] for key in sorted(universe_counts)
            },
            "stream_sha256": universe_digest.hexdigest(),
        },
        "mechanism_pool": {
            "condition": "c(1)==4",
            "count": sum(pool_counts.values()),
            "stream_sha256": pool_digest.hexdigest(),
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
        "cost": {
            "n1_schur_product_queries": core.EXPECTED_B1_UNORDERED_INNER_PAIRS,
            "b1_positive_support_records_visited": sum(b1_counts.values()),
            "prospective_universe_records": sum(universe_counts.values()),
            "mechanism_pool_coefficients_equal_to_4": sum(pool_counts.values()),
        },
    }
    _validate_panel(artifact, plan_sha)
    return artifact


def freeze_panel(work_dir: Path) -> dict[str, Any]:
    work_dir = _validate_work_dir(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    plan = build_plan()
    plan_sha = core._write_pinned_json(work_dir / "plan.json", plan)
    _require_plan(work_dir)
    panel_path = work_dir / "panel.json"
    if panel_path.exists() and core._sidecar(panel_path).exists():
        panel, panel_sha = core._load_pinned_json(panel_path)
        _validate_panel(panel, plan_sha)
        return {
            "stage": "panel-frozen",
            "panel_sha256": panel_sha,
            "mechanism_pool_count": panel["mechanism_pool"]["count"],
            "reused": True,
        }
    if not panel_path.exists() and core._sidecar(panel_path).exists():
        raise ScanError("panel digest sidecar exists without panel JSON")

    artifact = _generate_panel_artifact(plan_sha)
    panel_sha = core._write_pinned_json(panel_path, artifact)
    return {
        "stage": "panel-frozen",
        "panel_sha256": panel_sha,
        "universe_count": artifact["universe"]["count"],
        "mechanism_pool_count": artifact["mechanism_pool"]["count"],
        "panel_size": PANEL_SIZE,
        "reused": False,
    }


def _validate_panel(panel: Mapping[str, Any], plan_sha: str) -> None:
    if panel.get("schema_version") != PANEL_SCHEMA or panel.get("plan_sha256") != plan_sha:
        raise ScanError("invalid panel schema or plan provenance")
    if panel.get("universe", {}).get("count") != core.EXPECTED_UNIVERSE_SIZE:
        raise ScanError("panel universe count mismatch")
    entries = panel.get("panel", {}).get("entries")
    if not isinstance(entries, list) or len(entries) != PANEL_SIZE:
        raise ScanError("panel entry count mismatch")
    identifiers: set[str] = set()
    observed: Counter[tuple[int, int]] = Counter()
    for entry in entries:
        triple = core._dict_triple(entry["triple"])
        identifier = core._triple_id(triple)
        stratum = (len(triple[2]), max(sum(triple[0]), sum(triple[1])))
        if (
            entry.get("triple_id") != identifier
            or entry.get("n1_coefficient") != 4
            or entry.get("stratum") != list(stratum)
            or entry.get("selection_key_sha256") != _selection_hash(triple)
        ):
            raise ScanError("panel entry identity or selection metadata mismatch")
        identifiers.add(identifier)
        observed[stratum] += 1
    if len(identifiers) != PANEL_SIZE:
        raise ScanError("panel contains duplicate identifiers")
    encoded_pool = panel.get("mechanism_pool", {}).get("count_by_stratum")
    if not isinstance(encoded_pool, dict):
        raise ScanError("mechanism pool stratum counts are missing")
    pool_counts: dict[tuple[int, int], int] = {}
    for label, count in encoded_pool.items():
        try:
            rows_text, size_text = label.split(",")
            key = (
                int(rows_text.removeprefix("rows=")),
                int(size_text.removeprefix("max_inner_size=")),
            )
        except (AttributeError, TypeError, ValueError) as exc:
            raise ScanError(f"invalid mechanism-pool stratum label {label!r}") from exc
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ScanError("invalid mechanism-pool stratum count")
        pool_counts[key] = count
    expected_quotas = core._largest_remainder_quotas(pool_counts, PANEL_SIZE)
    encoded_expected = {
        f"rows={key[0]},max_inner_size={key[1]}": expected_quotas[key]
        for key in sorted(expected_quotas)
    }
    if panel["panel"]["quota_by_stratum"] != encoded_expected:
        raise ScanError("panel quotas are not the frozen largest-remainder allocation")
    encoded_observed = {
        f"rows={key[0]},max_inner_size={key[1]}": observed[key]
        for key in sorted(expected_quotas)
    }
    if panel["panel"]["quota_by_stratum"] != encoded_observed:
        raise ScanError("panel stratum quotas do not match entries")


def _failure_path(work_dir: Path, stage: str, triple_id: str) -> Path:
    return work_dir / "failures" / f"{stage}-{triple_id}.json"


def _persist_failure(
    work_dir: Path,
    *,
    stage: str,
    triple_id: str,
    plan_sha: str,
    upstream_sha: str,
    exc: Exception,
) -> None:
    path = _failure_path(work_dir, stage, triple_id)
    value = {
        "schema_version": "lr-p3-empty-reeve-failure/v1",
        "stage": stage,
        "triple_id": triple_id,
        "plan_sha256": plan_sha,
        "upstream_sha256": upstream_sha,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "blocks_adjudication": True,
    }
    core._write_pinned_json(path, value)


def _geometry_record(
    entry: Mapping[str, Any], *, plan_sha: str, panel_sha: str
) -> dict[str, Any]:
    triple = core._dict_triple(entry["triple"])
    polytope = e2.build_hive_polytope(*triple, n=len(triple[2]))
    try:
        from PyNormaliz import Cone
    except ImportError as exc:
        raise ScanError("PyNormaliz is required for geometry") from exc
    rows = polytope.normaliz_rows
    cone = Cone(inhom_inequalities=rows)
    affine_dimension = int(cone.AffineDim())
    raw_vertices = cone.VerticesOfPolyhedron()
    vertices, integral = core._decode_vertices(raw_vertices, polytope.ambient_dimension)
    tetrahedron = affine_dimension == 3 and len(vertices) == 4 and integral
    volume: int | None = None
    if tetrahedron:
        volume = core.normalized_tetrahedron_volume(
            [[int(value) for value in vertex] for vertex in vertices]
        )
    signature = bool(volume is not None and volume > 12)
    return {
        "schema_version": GEOMETRY_ITEM_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "triple_id": entry["triple_id"],
        "triple": entry["triple"],
        "n1_coefficient_from_frozen_pool": 4,
        "normaliz_rows_sha256": sha256_json(rows),
        "ambient_dimension": polytope.ambient_dimension,
        "query_trace": ["AffineDim", "VerticesOfPolyhedron"],
        "affine_dimension": affine_dimension,
        "vertices_raw": raw_vertices,
        "vertices_canonical": [
            [str(value) for value in vertex] for vertex in vertices
        ],
        "vertex_count": len(vertices),
        "all_vertices_integral": integral,
        "empty_integral_tetrahedron_prediction": tetrahedron,
        "normalized_saturated_lattice_volume": volume,
        "predicted_polynomial": core._reeve_polynomial(volume) if volume is not None else None,
        "delta_gt_12_signature": signature,
    }


def build_geometry(work_dir: Path, *, max_items: int | None = None) -> dict[str, Any]:
    max_items = _validate_max_items(max_items)
    work_dir = _validate_work_dir(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = core._load_pinned_json(work_dir / "panel.json")
    _validate_panel(panel, plan_sha)
    item_dir = work_dir / "geometry" / "items"
    item_dir.mkdir(parents=True, exist_ok=True)
    completed: list[dict[str, Any]] = []
    new_items = 0
    for entry in panel["panel"]["entries"]:
        identifier = entry["triple_id"]
        path = item_dir / f"{identifier}.json"
        try:
            if path.exists() and core._sidecar(path).exists():
                record, record_sha = core._load_pinned_json(path)
            else:
                if max_items is not None and new_items >= max_items:
                    continue
                record = _geometry_record(entry, plan_sha=plan_sha, panel_sha=panel_sha)
                record_sha = core._write_pinned_json(path, record)
                new_items += 1
        except Exception as exc:
            _persist_failure(
                work_dir,
                stage="geometry",
                triple_id=identifier,
                plan_sha=plan_sha,
                upstream_sha=panel_sha,
                exc=exc,
            )
            raise ScanError(f"geometry failed for {identifier}: {exc}") from exc
        _validate_geometry_item(record, entry, plan_sha, panel_sha)
        completed.append({
            "triple_id": identifier,
            "item_sha256": record_sha,
            "affine_dimension": record["affine_dimension"],
            "vertex_count": record["vertex_count"],
            "all_vertices_integral": record["all_vertices_integral"],
            "empty_integral_tetrahedron_prediction": record[
                "empty_integral_tetrahedron_prediction"
            ],
            "normalized_saturated_lattice_volume": record[
                "normalized_saturated_lattice_volume"
            ],
            "predicted_polynomial": record["predicted_polynomial"],
            "delta_gt_12_signature": record["delta_gt_12_signature"],
        })
    if len(completed) != PANEL_SIZE:
        return {
            "stage": "geometry-partial",
            "completed": len(completed),
            "total": PANEL_SIZE,
            "new_items": new_items,
        }
    signatures = [item["triple_id"] for item in completed if item["delta_gt_12_signature"]]
    artifact = {
        "schema_version": GEOMETRY_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "query_contract": ["AffineDim", "VerticesOfPolyhedron"],
        "ehrhart_queries_before_signature_freeze": 0,
        "item_count": PANEL_SIZE,
        "cone_constructions": PANEL_SIZE,
        "normaliz_geometry_call_count": 2 * PANEL_SIZE,
        "items": completed,
        "summary": {
            "affine_dimension_counts": {
                str(value): sum(item["affine_dimension"] == value for item in completed)
                for value in sorted({item["affine_dimension"] for item in completed})
            },
            "empty_integral_tetrahedron_predictions": sum(
                item["empty_integral_tetrahedron_prediction"] for item in completed
            ),
            "delta_gt_12_signature_count": len(signatures),
            "signature_triple_ids": signatures,
        },
    }
    geometry_sha = core._write_pinned_json(work_dir / "geometry.json", artifact)
    return {
        "stage": "geometry-frozen",
        "geometry_sha256": geometry_sha,
        **artifact["summary"],
        "new_items": new_items,
    }


def _validate_geometry_item(
    record: Mapping[str, Any],
    panel_entry: Mapping[str, Any],
    plan_sha: str,
    panel_sha: str,
) -> None:
    if (
        record.get("schema_version") != GEOMETRY_ITEM_SCHEMA
        or record.get("plan_sha256") != plan_sha
        or record.get("panel_sha256") != panel_sha
        or record.get("triple_id") != panel_entry["triple_id"]
        or record.get("triple") != panel_entry["triple"]
        or record.get("query_trace") != ["AffineDim", "VerticesOfPolyhedron"]
    ):
        raise ScanError("invalid geometry item identity or provenance")
    triple = core._dict_triple(record["triple"])
    polytope = e2.build_hive_polytope(*triple, n=len(triple[2]))
    if record.get("normaliz_rows_sha256") != sha256_json(polytope.normaliz_rows):
        raise ScanError("geometry item hive-row hash mismatch")
    vertices, integral = core._decode_vertices(
        record.get("vertices_raw"), polytope.ambient_dimension
    )
    canonical_vertices = [[str(value) for value in vertex] for vertex in vertices]
    tetrahedron = (
        record.get("affine_dimension") == 3 and len(vertices) == 4 and integral
    )
    volume = None
    if tetrahedron:
        volume = core.normalized_tetrahedron_volume(
            [[int(value) for value in vertex] for vertex in vertices]
        )
    if (
        record.get("ambient_dimension") != polytope.ambient_dimension
        or record.get("vertex_count") != len(vertices)
        or record.get("vertices_canonical") != canonical_vertices
        or record.get("all_vertices_integral") != integral
        or record.get("empty_integral_tetrahedron_prediction") != tetrahedron
        or record.get("normalized_saturated_lattice_volume") != volume
        or record.get("predicted_polynomial")
        != (core._reeve_polynomial(volume) if volume is not None else None)
        or record.get("delta_gt_12_signature") != bool(volume is not None and volume > 12)
    ):
        raise ScanError("geometry item deterministic feature mismatch")


def _candidate_record(
    geometry_record: Mapping[str, Any],
    *,
    plan_sha: str,
    panel_sha: str,
    geometry_sha: str,
) -> dict[str, Any]:
    if not geometry_record.get("delta_gt_12_signature"):
        raise ScanError("refusing to verify a non-signature panel item")
    triple = core._dict_triple(geometry_record["triple"])
    n1 = e1.lr_coefficient(*triple)
    if n1 != 4:
        raise ScanError("candidate no longer has frozen c(1)=4 membership")
    bounded = e1.evaluate_stretched(*triple, mode="bounded", known_n1=n1)
    conservative = e1.evaluate_stretched(
        *triple, mode="conservative", known_n1=n1
    )
    bounded_poly = e1.canonical_polynomial_strings(bounded.polynomial)
    conservative_poly = e1.canonical_polynomial_strings(conservative.polynomial)
    polytope = e2.build_hive_polytope(*triple, n=len(triple[2]))
    hive_input = polytope.input_dict()
    second = e2.evaluate_with_normaliz(polytope)
    second_poly = e1.canonical_polynomial_strings(
        [Fraction(value) for value in second["canonical_polynomial"]]
    )
    predicted = geometry_record["predicted_polynomial"]
    if (
        not second.get("period_collapses_to_one")
        or second.get("raw_period") != 1
        or not isinstance(second.get("residue_polynomials"), list)
        or len(second["residue_polynomials"]) != 1
    ):
        raise ScanError("candidate E2 did not return exactly one raw residue")
    if second.get("number_lattice_points") != n1:
        raise ScanError("candidate E1/E2 N=1 disagreement")
    if not (bounded_poly == conservative_poly == second_poly == predicted):
        raise ScanError("candidate formula/E1/E2 polynomial disagreement")
    negative_indices = [
        index for index, value in enumerate(map(Fraction, predicted)) if value < 0
    ]
    if not negative_indices:
        raise ScanError("Delta>12 signature produced no negative coefficient")
    return {
        "schema_version": VERIFICATION_ITEM_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "triple_id": geometry_record["triple_id"],
        "triple": geometry_record["triple"],
        "normalized_saturated_lattice_volume": geometry_record[
            "normalized_saturated_lattice_volume"
        ],
        "canonical_polynomial": predicted,
        "negative_coefficient_indices": negative_indices,
        "all_exact_paths_agree": True,
        "e1_bounded": bounded.evidence(),
        "e1_conservative": conservative.evidence(),
        "e2_typed_hive_input": hive_input,
        "e2_typed_hive_input_sha256": sha256_json(hive_input),
        "e2_raw_evidence": second,
    }


def verify_candidates(
    work_dir: Path,
    *,
    expected_geometry_sha256: str,
    max_items: int | None = None,
) -> dict[str, Any]:
    max_items = _validate_max_items(max_items)
    work_dir = _validate_work_dir(work_dir)
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = core._load_pinned_json(work_dir / "panel.json")
    _validate_panel(panel, plan_sha)
    geometry, geometry_sha = core._load_pinned_json(work_dir / "geometry.json")
    if expected_geometry_sha256 != geometry_sha:
        raise ScanError("geometry hash acknowledgement does not match frozen geometry")
    if (
        geometry.get("schema_version") != GEOMETRY_SCHEMA
        or geometry.get("plan_sha256") != plan_sha
        or geometry.get("panel_sha256") != panel_sha
    ):
        raise ScanError("invalid geometry aggregate provenance")
    signature_ids = geometry["summary"]["signature_triple_ids"]
    geometry_by_id = {
        item["triple_id"]: item for item in geometry["items"]
    }
    panel_by_id = {
        entry["triple_id"]: entry for entry in panel["panel"]["entries"]
    }
    item_dir = work_dir / "candidate-verifications" / "items"
    item_dir.mkdir(parents=True, exist_ok=True)
    completed: list[dict[str, Any]] = []
    new_items = 0
    for identifier in signature_ids:
        geometry_item_path = work_dir / "geometry" / "items" / f"{identifier}.json"
        geometry_record, geometry_item_sha = core._load_pinned_json(geometry_item_path)
        if geometry_item_sha != geometry_by_id[identifier]["item_sha256"]:
            raise ScanError("geometry item hash differs from frozen aggregate")
        _validate_geometry_item(
            geometry_record, panel_by_id[identifier], plan_sha, panel_sha
        )
        path = item_dir / f"{identifier}.json"
        try:
            if path.exists() and core._sidecar(path).exists():
                record, record_sha = core._load_pinned_json(path)
            else:
                if max_items is not None and new_items >= max_items:
                    continue
                record = _candidate_record(
                    geometry_record,
                    plan_sha=plan_sha,
                    panel_sha=panel_sha,
                    geometry_sha=geometry_sha,
                )
                record_sha = core._write_pinned_json(path, record)
                new_items += 1
        except Exception as exc:
            _persist_failure(
                work_dir,
                stage="candidate-verification",
                triple_id=identifier,
                plan_sha=plan_sha,
                upstream_sha=geometry_sha,
                exc=exc,
            )
            raise ScanError(f"candidate verification failed for {identifier}: {exc}") from exc
        _validate_candidate_item(record, geometry_record, plan_sha, panel_sha, geometry_sha)
        completed.append({
            "triple_id": identifier,
            "item_sha256": record_sha,
            "triple": record["triple"],
            "canonical_polynomial": record["canonical_polynomial"],
            "negative_coefficient_indices": record["negative_coefficient_indices"],
        })
    if len(completed) != len(signature_ids):
        return {
            "stage": "candidate-verification-partial",
            "completed": len(completed),
            "total": len(signature_ids),
            "new_items": new_items,
        }
    artifact = {
        "schema_version": VERIFICATIONS_SCHEMA,
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "signature_count": len(signature_ids),
        "verified_candidate_count": len(completed),
        "all_exact_paths_agree": True,
        "items": completed,
    }
    verifications_sha = core._write_pinned_json(
        work_dir / "candidate-verifications.json", artifact
    )
    return {
        "stage": "candidate-verification-complete",
        "candidate_verifications_sha256": verifications_sha,
        "signature_count": len(signature_ids),
        "verified_candidate_count": len(completed),
        "new_items": new_items,
    }


def _validate_candidate_item(
    record: Mapping[str, Any],
    geometry_record: Mapping[str, Any],
    plan_sha: str,
    panel_sha: str,
    geometry_sha: str,
) -> None:
    if (
        record.get("schema_version") != VERIFICATION_ITEM_SCHEMA
        or record.get("plan_sha256") != plan_sha
        or record.get("panel_sha256") != panel_sha
        or record.get("geometry_sha256") != geometry_sha
        or record.get("triple_id") != geometry_record["triple_id"]
        or record.get("triple") != geometry_record["triple"]
        or record.get("canonical_polynomial") != geometry_record["predicted_polynomial"]
        or record.get("all_exact_paths_agree") is not True
    ):
        raise ScanError("candidate verification identity or agreement mismatch")
    polynomial = [Fraction(value) for value in record["canonical_polynomial"]]
    indices = [index for index, value in enumerate(polynomial) if value < 0]
    if record.get("negative_coefficient_indices") != indices or not indices:
        raise ScanError("candidate negative-index summary mismatch")
    hive_input = record.get("e2_typed_hive_input")
    if record.get("e2_typed_hive_input_sha256") != sha256_json(hive_input):
        raise ScanError("candidate typed hive input hash mismatch")
    triple = core._dict_triple(record["triple"])
    expected_hive_input = e2.build_hive_polytope(
        *triple, n=len(triple[2])
    ).input_dict()
    if hive_input != expected_hive_input:
        raise ScanError("candidate typed hive input does not match its triple")
    second = record.get("e2_raw_evidence", {})
    if (
        second.get("canonical_polynomial") != record["canonical_polynomial"]
        or second.get("number_lattice_points") != 4
        or second.get("period_collapses_to_one") is not True
        or second.get("raw_period") != 1
        or not isinstance(second.get("residue_polynomials"), list)
        or len(second["residue_polynomials"]) != 1
    ):
        raise ScanError("candidate stored E2 evidence mismatch")
    for key in ("e1_bounded", "e1_conservative"):
        if record.get(key, {}).get("polynomial") != record["canonical_polynomial"]:
            raise ScanError(f"candidate stored {key} evidence mismatch")


def _failure_files(work_dir: Path) -> list[Path]:
    directory = work_dir / "failures"
    return sorted(directory.glob("*.json")) if directory.is_dir() else []


def _decision_text(signature_count: int) -> tuple[str, str]:
    if signature_count:
        return (
            "CANDIDATE_VERIFICATION_EVENT",
            "Every frozen Delta>12 signature agreed under the exact formula, "
            "bounded and conservative E1, and raw-period-one E2.",
        )
    return (
        "BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL",
        "The frozen 512-case panel contained no Delta>12 empty-Reeve "
        "signature. This does not exclude the mechanism elsewhere.",
    )


def _adjudication_value(
    panel: Mapping[str, Any],
    geometry: Mapping[str, Any],
    verifications: Mapping[str, Any],
    *,
    plan_sha: str,
    panel_sha: str,
    geometry_sha: str,
    verifications_sha: str,
) -> dict[str, Any]:
    signature_count = geometry["summary"]["delta_gt_12_signature_count"]
    decision, rationale = _decision_text(signature_count)
    return {
        "schema_version": ADJUDICATION_SCHEMA,
        "classification": "internal-bounded-non-certifying-direct-search",
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "geometry_sha256": geometry_sha,
        "candidate_verifications_sha256": verifications_sha,
        "cost": {
            **panel["cost"],
            "cone_constructions": geometry["cone_constructions"],
            "normaliz_geometry_calls": geometry["normaliz_geometry_call_count"],
            "dual_evaluator_candidate_verifications": signature_count,
        },
        "geometry_summary": geometry["summary"],
        "verified_candidates": verifications["items"],
        "decision": decision,
        "rationale": rationale,
        "zero_hit_scope_caveat": (
            "not evidence of mechanism absence and not evidence for positivity"
        ),
        "full_p3_authorized": False,
        "outcome_claim": None,
    }


def _summary_value(
    panel: Mapping[str, Any], geometry: Mapping[str, Any], signature_count: int
) -> str:
    decision, rationale = _decision_text(signature_count)
    return "\n".join([
        "# Frozen empty-Reeve direct scan",
        "",
        f"**Decision: {decision}.**",
        "",
        rationale,
        "",
        f"- Prospective universe: {panel['universe']['count']:,} triples.",
        f"- Complete c(1)=4 mechanism pool: {panel['mechanism_pool']['count']:,} triples.",
        f"- Frozen geometry panel: {geometry['item_count']} triples.",
        f"- Empty integral tetrahedron predictions: "
        f"{geometry['summary']['empty_integral_tetrahedron_predictions']}.",
        f"- Delta>12 signatures / dual verifications: {signature_count}.",
        "",
        "This is a bounded resource decision, not a certified frontier, proof of "
        "positivity, or claim that the mechanism is absent from the full universe.",
        "",
    ])


def adjudicate(work_dir: Path) -> dict[str, Any]:
    work_dir = _validate_work_dir(work_dir)
    if _failure_files(work_dir):
        raise ScanError("durable failure records exist; adjudication is blocked")
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = core._load_pinned_json(work_dir / "panel.json")
    geometry, geometry_sha = core._load_pinned_json(work_dir / "geometry.json")
    verifications, verifications_sha = core._load_pinned_json(
        work_dir / "candidate-verifications.json"
    )
    signature_count = geometry["summary"]["delta_gt_12_signature_count"]
    if (
        verifications.get("geometry_sha256") != geometry_sha
        or verifications.get("signature_count") != signature_count
        or verifications.get("verified_candidate_count") != signature_count
        or verifications.get("all_exact_paths_agree") is not True
    ):
        raise ScanError("candidate-verification aggregate does not cover signatures")
    artifact = _adjudication_value(
        panel,
        geometry,
        verifications,
        plan_sha=plan_sha,
        panel_sha=panel_sha,
        geometry_sha=geometry_sha,
        verifications_sha=verifications_sha,
    )
    decision = artifact["decision"]
    adjudication_sha = core._write_pinned_json(work_dir / "adjudication.json", artifact)
    summary = _summary_value(panel, geometry, signature_count)
    summary_sha = core._write_pinned_text(work_dir / "SUMMARY.md", summary)
    top_names = (
        "plan.json",
        "panel.json",
        "geometry.json",
        "candidate-verifications.json",
        "adjudication.json",
        "SUMMARY.md",
    )
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "classification": "internal-bounded-non-certifying-direct-search",
        "files": [
            {"path": name, "sha256": sha256_file(work_dir / name)}
            for name in top_names
        ],
        "geometry_items": {
            "count": geometry["item_count"],
            "aggregate_sha256": geometry_sha,
        },
        "candidate_verification_items": {
            "count": verifications["verified_candidate_count"],
            "aggregate_sha256": verifications_sha,
        },
        "adjudication_sha256": adjudication_sha,
        "summary_sha256": summary_sha,
    }
    manifest_sha = core._write_pinned_json(work_dir / "manifest.json", manifest)
    return {
        "stage": "adjudicated",
        "decision": decision,
        "signature_count": signature_count,
        "adjudication_sha256": adjudication_sha,
        "manifest_sha256": manifest_sha,
    }


def _exact_json_item_set(directory: Path, expected: set[str]) -> None:
    actual = {path.stem for path in directory.glob("*.json")} if directory.is_dir() else set()
    if actual != expected:
        raise ScanError(
            f"item set mismatch in {directory}: missing={sorted(expected-actual)!r}, "
            f"unexpected={sorted(actual-expected)!r}"
        )
    sidecars = {
        path.name[:-len(".json.sha256")]
        for path in directory.glob("*.json.sha256")
    } if directory.is_dir() else set()
    if sidecars != expected:
        raise ScanError(f"item sidecar set mismatch in {directory}")


def verify(work_dir: Path, *, require_complete: bool = True) -> dict[str, Any]:
    work_dir = _validate_work_dir(work_dir)
    if _failure_files(work_dir):
        raise ScanError("durable failure records exist")
    _, plan_sha = _require_plan(work_dir)
    panel, panel_sha = core._load_pinned_json(work_dir / "panel.json")
    _validate_panel(panel, plan_sha)
    regenerated_panel = _generate_panel_artifact(plan_sha)
    if panel != regenerated_panel:
        raise ScanError(
            "deep verification regenerated a different universe, pool, or panel"
        )
    result: dict[str, Any] = {
        "plan_sha256": plan_sha,
        "panel_sha256": panel_sha,
        "panel_items": PANEL_SIZE,
        "universe_and_panel_regenerated": True,
        "complete": False,
    }
    geometry_path = work_dir / "geometry.json"
    if not geometry_path.exists():
        if require_complete:
            raise ScanError("geometry aggregate is missing")
        return result
    geometry, geometry_sha = core._load_pinned_json(geometry_path)
    if (
        geometry.get("schema_version") != GEOMETRY_SCHEMA
        or geometry.get("plan_sha256") != plan_sha
        or geometry.get("panel_sha256") != panel_sha
        or geometry.get("item_count") != PANEL_SIZE
        or geometry.get("ehrhart_queries_before_signature_freeze") != 0
    ):
        raise ScanError("invalid geometry aggregate")
    panel_by_id = {entry["triple_id"]: entry for entry in panel["panel"]["entries"]}
    geometry_ids = [item["triple_id"] for item in geometry["items"]]
    if len(geometry_ids) != PANEL_SIZE or set(geometry_ids) != set(panel_by_id):
        raise ScanError("geometry aggregate item identity mismatch")
    _exact_json_item_set(work_dir / "geometry" / "items", set(panel_by_id))
    signatures: list[str] = []
    for summary in geometry["items"]:
        path = work_dir / "geometry" / "items" / f"{summary['triple_id']}.json"
        record, digest = core._load_pinned_json(path)
        if digest != summary["item_sha256"]:
            raise ScanError("geometry item digest differs from aggregate")
        _validate_geometry_item(
            record, panel_by_id[summary["triple_id"]], plan_sha, panel_sha
        )
        for key in (
            "affine_dimension",
            "vertex_count",
            "all_vertices_integral",
            "empty_integral_tetrahedron_prediction",
            "normalized_saturated_lattice_volume",
            "predicted_polynomial",
            "delta_gt_12_signature",
        ):
            if summary[key] != record[key]:
                raise ScanError(f"geometry aggregate feature mismatch: {key}")
        if record["delta_gt_12_signature"]:
            signatures.append(record["triple_id"])
    expected_summary = {
        "affine_dimension_counts": {
            str(value): sum(item["affine_dimension"] == value for item in geometry["items"])
            for value in sorted({item["affine_dimension"] for item in geometry["items"]})
        },
        "empty_integral_tetrahedron_predictions": sum(
            item["empty_integral_tetrahedron_prediction"] for item in geometry["items"]
        ),
        "delta_gt_12_signature_count": len(signatures),
        "signature_triple_ids": signatures,
    }
    if geometry.get("summary") != expected_summary:
        raise ScanError("geometry deterministic summary mismatch")
    result["geometry_sha256"] = geometry_sha
    result["signature_count"] = len(signatures)

    verifications_path = work_dir / "candidate-verifications.json"
    if not verifications_path.exists():
        if require_complete:
            raise ScanError("candidate verification aggregate is missing")
        return result
    verifications, verifications_sha = core._load_pinned_json(verifications_path)
    if (
        verifications.get("schema_version") != VERIFICATIONS_SCHEMA
        or verifications.get("plan_sha256") != plan_sha
        or verifications.get("panel_sha256") != panel_sha
        or verifications.get("geometry_sha256") != geometry_sha
        or verifications.get("signature_count") != len(signatures)
        or verifications.get("verified_candidate_count") != len(signatures)
        or verifications.get("all_exact_paths_agree") is not True
    ):
        raise ScanError("invalid candidate-verification aggregate")
    _exact_json_item_set(
        work_dir / "candidate-verifications" / "items", set(signatures)
    )
    geometry_item_by_id: dict[str, Mapping[str, Any]] = {}
    for identifier in signatures:
        geometry_item_by_id[identifier], _ = core._load_pinned_json(
            work_dir / "geometry" / "items" / f"{identifier}.json"
        )
    if [item["triple_id"] for item in verifications["items"]] != signatures:
        raise ScanError("candidate-verification order/identity mismatch")
    for summary in verifications["items"]:
        path = work_dir / "candidate-verifications" / "items" / f"{summary['triple_id']}.json"
        record, digest = core._load_pinned_json(path)
        if digest != summary["item_sha256"]:
            raise ScanError("candidate verification digest differs from aggregate")
        _validate_candidate_item(
            record,
            geometry_item_by_id[summary["triple_id"]],
            plan_sha,
            panel_sha,
            geometry_sha,
        )
        regenerated_candidate = _candidate_record(
            geometry_item_by_id[summary["triple_id"]],
            plan_sha=plan_sha,
            panel_sha=panel_sha,
            geometry_sha=geometry_sha,
        )
        if record != regenerated_candidate:
            raise ScanError(
                "deep verification regenerated different candidate evidence"
            )
        for key in (
            "triple",
            "canonical_polynomial",
            "negative_coefficient_indices",
        ):
            if summary[key] != record[key]:
                raise ScanError(f"candidate aggregate mismatch: {key}")
    result["candidate_verifications_sha256"] = verifications_sha

    adjudication_path = work_dir / "adjudication.json"
    manifest_path = work_dir / "manifest.json"
    summary_path = work_dir / "SUMMARY.md"
    if not (adjudication_path.exists() and manifest_path.exists() and summary_path.exists()):
        if require_complete:
            raise ScanError("final adjudication, manifest, or summary is missing")
        return result
    adjudication, adjudication_sha = core._load_pinned_json(adjudication_path)
    expected_decision = (
        "CANDIDATE_VERIFICATION_EVENT"
        if signatures else "BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL"
    )
    expected_adjudication = _adjudication_value(
        panel,
        geometry,
        verifications,
        plan_sha=plan_sha,
        panel_sha=panel_sha,
        geometry_sha=geometry_sha,
        verifications_sha=verifications_sha,
    )
    if adjudication != expected_adjudication:
        raise ScanError("deep verification regenerated a different adjudication")
    expected_summary_text = _summary_value(panel, geometry, len(signatures))
    if summary_path.read_text(encoding="utf-8") != expected_summary_text:
        raise ScanError("deep verification regenerated a different summary")
    manifest, manifest_sha = core._load_pinned_json(manifest_path)
    if manifest.get("schema_version") != MANIFEST_SCHEMA:
        raise ScanError("invalid manifest schema")
    expected_files = {
        "plan.json",
        "panel.json",
        "geometry.json",
        "candidate-verifications.json",
        "adjudication.json",
        "SUMMARY.md",
    }
    listed = {item["path"] for item in manifest.get("files", [])}
    if listed != expected_files or len(manifest["files"]) != len(expected_files):
        raise ScanError("manifest file set mismatch")
    for item in manifest["files"]:
        path = work_dir / item["path"]
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise ScanError(f"manifest digest mismatch for {path}")
        sidecar = core._sidecar(path)
        if not sidecar.is_file() or sidecar.read_text(encoding="ascii").strip() != item["sha256"]:
            raise ScanError(f"sidecar mismatch for {path}")
    if (
        manifest.get("geometry_items")
        != {"count": PANEL_SIZE, "aggregate_sha256": geometry_sha}
        or manifest.get("candidate_verification_items")
        != {"count": len(signatures), "aggregate_sha256": verifications_sha}
        or manifest.get("adjudication_sha256") != adjudication_sha
        or manifest.get("summary_sha256") != sha256_file(summary_path)
    ):
        raise ScanError("manifest aggregate metadata mismatch")
    result.update({
        "adjudication_sha256": adjudication_sha,
        "manifest_sha256": manifest_sha,
        "decision": expected_decision,
        "complete": True,
    })
    return result


def run_all(work_dir: Path) -> dict[str, Any]:
    panel = freeze_panel(work_dir)
    geometry = build_geometry(work_dir)
    geometry_sha = geometry["geometry_sha256"]
    candidates = verify_candidates(
        work_dir, expected_geometry_sha256=geometry_sha
    )
    final = adjudicate(work_dir)
    return {
        "stages": [panel, geometry, candidates, final],
        "verification": verify(work_dir),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, default=DEFAULT_WORK_DIR)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("freeze")
    geometry = commands.add_parser("geometry")
    geometry.add_argument("--max-items", type=int)
    candidates = commands.add_parser("verify-candidates")
    candidates.add_argument("--expected-geometry-sha256", required=True)
    candidates.add_argument("--max-items", type=int)
    commands.add_parser("adjudicate")
    check = commands.add_parser("verify")
    check.add_argument("--allow-partial", action="store_true")
    commands.add_parser("run")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        work_dir = _validate_work_dir(args.work_dir)
        with core._run_lock(work_dir):
            if args.command == "freeze":
                result = freeze_panel(work_dir)
            elif args.command == "geometry":
                result = build_geometry(work_dir, max_items=args.max_items)
            elif args.command == "verify-candidates":
                result = verify_candidates(
                    work_dir,
                    expected_geometry_sha256=args.expected_geometry_sha256,
                    max_items=args.max_items,
                )
            elif args.command == "adjudicate":
                result = adjudicate(work_dir)
            elif args.command == "verify":
                result = verify(work_dir, require_complete=not args.allow_partial)
            elif args.command == "run":
                result = run_all(work_dir)
            else:  # pragma: no cover
                raise AssertionError(args.command)
    except (ScanError, core.BakeoffError, OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    import json

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
