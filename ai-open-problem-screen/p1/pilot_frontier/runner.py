"""Deterministic, crash-safe runner for a real post-P1 LR frontier pilot.

The work list consists of every swap-canonical, support-compatible structural
triple in a finite ``(maximum_length, maximum_size)`` box.  Each triple is
evaluated with the production :mod:`p1.e1.evaluator` path:

* ``lrcalc`` decides whether the unstretched LR coefficient is zero;
* new nonzero triples use exact integer samples and ``Fraction`` interpolation
  in E1's bounded mode (fit ``N=0..B`` and reserve ``N=B+1`` as a holdout);
* all structural triples receive exactly one durable result record.

Results are committed in fixed immutable chunks.  A mutable checkpoint is only
a cache: every invocation reconstructs the durable prefix from the chunk hash
chain and repairs a missing or lagging checkpoint.  A checkpoint ahead of the
durable prefix, a gap, or any digest mismatch fails closed.

Even a completed run produced here is labelled ``partial-extension`` and is
explicitly *not* outcome B.  New nonzero cases have E1/E2 agreement, but any
negative candidate still requires the campaign's separately frozen verification
workflow; the preregistered outcome-B boxes start at B1, not at B0-7.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from importlib.metadata import PackageNotFoundError, version as package_version
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterator, Sequence
import uuid

from p1.control.gate import validate_gate_report, validate_p1_gate
from p1.control.manifest import verify_manifest
from p1.e1 import evaluator as e1
from p1.e2 import hive_e2 as e2


PLAN_SCHEMA = "lr-scientific-pilot-plan/v1"
AUTHORIZATION_SCHEMA = "lr-scientific-pilot-authorization/v1"
RECORD_SCHEMA = "lr-scientific-pilot-record/v1"
BASELINE_RECORD_SCHEMA = "lr-scientific-pilot-baseline-record/v1"
E1_RECORD_SCHEMA = "lr-scientific-pilot-e1-record/v1"
E2_RECORD_SCHEMA = "lr-scientific-pilot-e2-record/v1"
AGREEMENT_RECORD_SCHEMA = "lr-scientific-pilot-agreement-record/v1"
CHUNK_SCHEMA = "lr-scientific-pilot-chunk/v1"
CHECKPOINT_SCHEMA = "lr-scientific-pilot-checkpoint/v1"
COMPLETION_SCHEMA = "lr-scientific-pilot-completion/v1"
VERIFICATION_SCHEMA = "lr-scientific-pilot-verification/v1"

EVIDENCE_CLASSIFICATION = "partial-extension"
OUTCOME_LABEL = "not-outcome-B"
CANONICALIZER_VERSION = "swap-only-v1"
SORT_KEY = "(len(nu),nu,lam,mu)"
EVALUATOR_MODE = "bounded"
B0_7_EXPECTED_STRUCTURAL_COUNT = 18_287
B0_7_EXPECTED_NEW_STRUCTURAL_COUNT = 3_985
B0_7_EXPECTED_TOTAL_NONZERO_COUNT = 9_478
B0_7_EXPECTED_NEW_NONZERO_COUNT = 1_929
B0_7_EXPECTED_FROZEN_ZERO_COUNT = 6_753
B0_7_EXPECTED_NEW_ZERO_COUNT = 2_056
B0_7_EXPECTED_TOTAL_ZERO_COUNT = 8_809
P1_BASELINE_MAXIMUM_LENGTH = 5
P1_BASELINE_MAXIMUM_SIZE = 7
P1_BASELINE_NONZERO_COUNT = 7_549
P1_BASELINE_STRUCTURAL_COUNT = 14_302
P1_BASELINE_PAYLOAD_SHA256 = (
    "b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7"
)

_CHUNK_RE = re.compile(r"^chunk-(\d{8})-(\d{8})\.json$")
_COUNTER_KEYS = ("zero", "nonzero", "error")
_PLAN_DIGEST_CACHE: dict[str, str] = {}


class FrontierError(RuntimeError):
    """Raised when a run artifact or transition fails validation."""


@dataclass(frozen=True)
class DurableState:
    next_ordinal: int
    prefix_sha256: str
    counts: dict[str, int]
    chunk_count: int
    snapshots: dict[int, tuple[str, dict[str, int], int]]


def canonical_bytes(value: Any) -> bytes:
    """Return the one canonical JSON encoding used for identity hashes."""

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise FrontierError(f"value is not canonical-JSON serializable: {exc}") from exc


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _plan_digest(plan: dict[str, Any]) -> str:
    """Hash a validated multi-megabyte plan once, then reuse its identity."""

    plan_id = plan.get("plan_id")
    if not isinstance(plan_id, str):
        raise FrontierError("plan has no identity")
    digest = _PLAN_DIGEST_CACHE.get(plan_id)
    if digest is None:
        digest = sha256_json(plan)
        _PLAN_DIGEST_CACHE[plan_id] = digest
    return digest


def load_json(path: Path) -> Any:
    try:
        with Path(path).open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise FrontierError(f"cannot read JSON artifact {path}: {exc}") from exc


def _render_json(value: Any) -> bytes:
    return (json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ) + "\n").encode("utf-8")


def _fsync_directory(directory: Path) -> None:
    """Best-effort directory fsync (supported by the target Linux/WSL host)."""

    try:
        descriptor = os.open(directory, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


def atomic_write_json(path: Path, value: Any, *, immutable: bool = False) -> None:
    """Durably replace a JSON artifact, or create it once when immutable."""

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _render_json(value)
    if immutable and path.exists():
        if path.read_bytes() != data:
            raise FrontierError(f"immutable artifact already differs: {path}")
        return
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if immutable and path.exists():
            if path.read_bytes() != data:
                raise FrontierError(f"immutable artifact appeared with different data: {path}")
            temporary.unlink(missing_ok=True)
            return
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


def atomic_write_text(path: Path, value: str, *, immutable: bool = False) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value.encode("utf-8")
    if immutable and path.exists():
        if path.read_bytes() != data:
            raise FrontierError(f"immutable artifact already differs: {path}")
        return
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}-{uuid.uuid4().hex}")
    try:
        with temporary.open("xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if immutable and path.exists():
            if path.read_bytes() != data:
                raise FrontierError(f"immutable artifact appeared with different data: {path}")
            temporary.unlink(missing_ok=True)
            return
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


@contextmanager
def run_lock(work_dir: Path) -> Iterator[None]:
    """Take an OS-released advisory lock, preventing concurrent chunk writers."""

    try:
        import fcntl
    except ImportError as exc:  # pragma: no cover - target is explicitly WSL
        raise FrontierError("the scientific runner requires Linux/WSL file locking") from exc
    lock_path = Path(work_dir) / "run.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as stream:
        try:
            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise FrontierError(f"another frontier writer holds {lock_path}") from exc
        try:
            yield
        finally:
            fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _validate_positive_integer(value: int, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise FrontierError(f"{label} must be a positive integer")
    return value


def _source_sha256() -> str:
    source = Path(e1.__file__).resolve()
    return sha256_file(source)


def _e2_source_sha256() -> str:
    return sha256_file(Path(e2.__file__).resolve())


def _package_version(name: str) -> str:
    try:
        return package_version(name)
    except PackageNotFoundError:
        return "unknown"


def _baseline_path() -> Path:
    return Path(__file__).resolve().parents[2] / "dryrun" / "frontier_baseline.json"


@lru_cache(maxsize=4)
def _baseline_bundle(
    expected_file_sha256: str,
    expected_payload_sha256: str,
) -> tuple[dict[tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]], tuple[str, ...]], dict[str, Any]]:
    """Load and fully validate the frozen nonzero baseline once per process."""

    path = _baseline_path()
    if sha256_file(path) != expected_file_sha256:
        raise FrontierError("frozen baseline file hash differs from the plan")
    payload = load_json(path)
    if not isinstance(payload, dict) or not isinstance(payload.get("triples"), list):
        raise FrontierError("frozen baseline artifact is malformed")
    triples = payload["triples"]
    if sha256_json(triples) != expected_payload_sha256:
        raise FrontierError("frozen baseline triples payload hash mismatch")
    if payload.get("sha256") != expected_payload_sha256:
        raise FrontierError("frozen baseline embedded payload hash mismatch")
    if len(triples) != P1_BASELINE_NONZERO_COUNT:
        raise FrontierError("frozen baseline nonzero count mismatch")
    mapping: dict[
        tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]], tuple[str, ...]
    ] = {}
    for index, entry in enumerate(triples):
        if not isinstance(entry, dict):
            raise FrontierError(f"baseline entry {index} is not an object")
        triple = _exact_triple_fields(entry, context=f"baseline entry {index}")
        if triple != e1.canonical_triple(*triple):
            raise FrontierError(f"baseline entry {index} is not swap-canonical")
        raw_polynomial = entry.get("poly")
        if not isinstance(raw_polynomial, list) or not raw_polynomial:
            raise FrontierError(f"baseline entry {index} lacks a polynomial")
        try:
            polynomial = tuple(Fraction(value) for value in raw_polynomial)
        except (TypeError, ValueError, ZeroDivisionError) as exc:
            raise FrontierError(f"baseline entry {index} polynomial is malformed") from exc
        canonical = tuple(e1.canonical_polynomial_strings(polynomial))
        if list(canonical) != raw_polynomial:
            raise FrontierError(f"baseline entry {index} polynomial is not canonical")
        if triple in mapping:
            raise FrontierError(f"duplicate triple in frozen baseline at entry {index}")
        mapping[triple] = canonical
    meta = {
        "file_sha256": expected_file_sha256,
        "triples_payload_sha256": expected_payload_sha256,
        "nonzero_record_count": len(mapping),
    }
    return mapping, meta


def _baseline_identity() -> dict[str, Any]:
    path = _baseline_path()
    file_digest = sha256_file(path)
    _, identity = _baseline_bundle(file_digest, P1_BASELINE_PAYLOAD_SHA256)
    return identity


def _exact_partition(value: Any, name: str) -> tuple[int, ...]:
    """Fail closed unless a persisted tool input is built from exact JSON ints."""

    if not isinstance(value, list):
        raise FrontierError(f"{name} must be a JSON array of exact integers")
    if any(type(part) is not int for part in value):
        raise FrontierError(f"{name} contains a bool, float, or non-exact integer")
    try:
        return e1.normalize_partition(value)
    except ValueError as exc:
        raise FrontierError(f"{name} is not a normalized partition: {exc}") from exc


def _exact_triple_fields(value: dict[str, Any], *, context: str) -> e1.Triple:
    return (
        _exact_partition(value.get("lam"), f"{context}.lam"),
        _exact_partition(value.get("mu"), f"{context}.mu"),
        _exact_partition(value.get("nu"), f"{context}.nu"),
    )


def _triple_item(
    ordinal: int,
    triple: e1.Triple,
    *,
    provenance_class: str,
) -> dict[str, Any]:
    lam, mu, nu = triple
    core = {
        "ordinal": ordinal,
        "lam": list(lam),
        "mu": list(mu),
        "nu": list(nu),
        "provenance_class": provenance_class,
    }
    return {**core, "work_sha256": sha256_json(core)}


def make_plan(
    maximum_length: int,
    maximum_size: int,
    *,
    chunk_size: int = 32,
    champion_limit: int = 100,
    expected_structural_count: int | None = None,
) -> dict[str, Any]:
    """Materialize the deterministic swap-only structural work plan."""

    _validate_positive_integer(maximum_length, "maximum_length")
    _validate_positive_integer(maximum_size, "maximum_size")
    _validate_positive_integer(chunk_size, "chunk_size")
    _validate_positive_integer(champion_limit, "champion_limit")
    triples = e1.enumerate_structural_triples(maximum_length, maximum_size)
    if expected_structural_count is not None:
        _validate_positive_integer(expected_structural_count, "expected_structural_count")
        if len(triples) != expected_structural_count:
            raise FrontierError(
                "structural plan count mismatch: "
                f"expected {expected_structural_count}, enumerated {len(triples)}"
            )
    baseline_reuse = maximum_size <= P1_BASELINE_MAXIMUM_SIZE
    baseline_cutoff_length = min(maximum_length, P1_BASELINE_MAXIMUM_LENGTH)
    items = [
        _triple_item(
            index,
            triple,
            provenance_class=(
                "frozen-p1-baseline-scope"
                if baseline_reuse and len(triple[2]) <= baseline_cutoff_length
                else "new-extension"
            ),
        )
        for index, triple in enumerate(triples)
    ]
    frozen_prefix_count = sum(
        item["provenance_class"] == "frozen-p1-baseline-scope" for item in items
    )
    if any(
        item["provenance_class"] == "new-extension"
        for item in items[:frozen_prefix_count]
    ) or any(
        item["provenance_class"] == "frozen-p1-baseline-scope"
        for item in items[frozen_prefix_count:]
    ):
        raise FrontierError("frozen baseline scope is not a contiguous plan prefix")
    baseline_identity = _baseline_identity()
    identity = {
        "schema_version": PLAN_SCHEMA,
        "campaign_stage": "post-P1-scientific-pilot",
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "outcome_b_eligible": False,
        "scope": {
            "maximum_length": maximum_length,
            "maximum_size_each_of_lam_mu": maximum_size,
            "outer_weight_rule": "|nu|=|lam|+|mu|",
            "support_filter": "nu componentwise contains lam and mu",
        },
        "canonicalization": {
            "version": CANONICALIZER_VERSION,
            "group_order": 2,
            "rule": "lexicographically sort (lam,mu) only; never conjugate",
        },
        "enumeration": {
            "sort_key": SORT_KEY,
            "structural_triple_count": len(items),
            "items_sha256": sha256_json(items),
        },
        "frozen_prefix": {
            "enabled": baseline_reuse,
            "coalesce_as_one_immutable_chunk": (
                (maximum_length, maximum_size) == (6, 7)
            ),
            "maximum_length": baseline_cutoff_length if baseline_reuse else None,
            "maximum_size_each_of_lam_mu": maximum_size if baseline_reuse else None,
            "structural_triple_count": frozen_prefix_count,
            "source_nonzero_count": P1_BASELINE_NONZERO_COUNT,
            "source_file_sha256": baseline_identity["file_sha256"],
            "source_triples_payload_sha256": baseline_identity["triples_payload_sha256"],
            "zero_rule": (
                "structural triple absent from exhaustive nonzero baseline; "
                "N=1 is zero, and saturation excludes positive stretches"
            ),
        },
        "b0_7_expected_counts": (
            {
                "structural_total": B0_7_EXPECTED_STRUCTURAL_COUNT,
                "frozen_structural_prefix": P1_BASELINE_STRUCTURAL_COUNT,
                "new_structural_suffix": B0_7_EXPECTED_NEW_STRUCTURAL_COUNT,
                "frozen_nonzero": P1_BASELINE_NONZERO_COUNT,
                "frozen_zero": B0_7_EXPECTED_FROZEN_ZERO_COUNT,
                "new_nonzero": B0_7_EXPECTED_NEW_NONZERO_COUNT,
                "new_zero": B0_7_EXPECTED_NEW_ZERO_COUNT,
                "nonzero_total": B0_7_EXPECTED_TOTAL_NONZERO_COUNT,
                "zero_total": B0_7_EXPECTED_TOTAL_ZERO_COUNT,
            }
            if (maximum_length, maximum_size) == (6, 7)
            else None
        ),
        "evaluator": {
            "names": ["p1.e1.lrcalc-interp", "p1.e2.normaliz-ehrhart"],
            "interpolation_mode": EVALUATOR_MODE,
            "arithmetic": "exact integers + fractions.Fraction",
            "lrcalc_version": e1.lrcalc_version(),
            "e1_source_sha256": _source_sha256(),
            "pynormaliz_version": _package_version("PyNormaliz"),
            "e2_source_sha256": _e2_source_sha256(),
            "new_nonzero_policy": "require canonical E1/E2 polynomial and N=1 agreement",
            "python_major_minor": f"{sys.version_info.major}.{sys.version_info.minor}",
        },
        "chunk_size": chunk_size,
        "champion_limit": champion_limit,
        "items": items,
    }
    return {**identity, "plan_id": f"sha256:{sha256_json(identity)}"}


def _validate_plan(plan: Any) -> None:
    if not isinstance(plan, dict) or plan.get("schema_version") != PLAN_SCHEMA:
        raise FrontierError("unsupported or malformed frontier plan")
    identity = {key: value for key, value in plan.items() if key != "plan_id"}
    if plan.get("plan_id") != f"sha256:{sha256_json(identity)}":
        raise FrontierError("plan_id does not match canonical plan content")
    if plan.get("evidence_classification") != EVIDENCE_CLASSIFICATION:
        raise FrontierError("plan is not labelled partial-extension")
    if plan.get("outcome_label") != OUTCOME_LABEL or plan.get("outcome_b_eligible") is not False:
        raise FrontierError("plan must be explicitly labelled not-outcome-B")
    canonicalization = plan.get("canonicalization")
    if not isinstance(canonicalization, dict) or canonicalization.get("version") != CANONICALIZER_VERSION:
        raise FrontierError("plan does not use swap-only-v1 canonicalization")
    evaluator = plan.get("evaluator")
    if not isinstance(evaluator, dict) or evaluator.get("interpolation_mode") != EVALUATOR_MODE:
        raise FrontierError("plan does not pin bounded E1 with its reserved holdout")
    frozen = plan.get("frozen_prefix")
    if not isinstance(frozen, dict):
        raise FrontierError("plan lacks frozen-prefix provenance")
    if frozen.get("source_triples_payload_sha256") != P1_BASELINE_PAYLOAD_SHA256:
        raise FrontierError("plan binds an unexpected P1 baseline payload")
    chunk_size = plan.get("chunk_size")
    champion_limit = plan.get("champion_limit")
    _validate_positive_integer(chunk_size, "plan.chunk_size")
    _validate_positive_integer(champion_limit, "plan.champion_limit")
    items = plan.get("items")
    enumeration = plan.get("enumeration")
    if not isinstance(items, list) or not isinstance(enumeration, dict):
        raise FrontierError("plan items/enumeration are malformed")
    if enumeration.get("structural_triple_count") != len(items):
        raise FrontierError("plan structural count does not match item count")
    if enumeration.get("items_sha256") != sha256_json(items):
        raise FrontierError("plan item payload hash mismatch")
    frozen_count = frozen.get("structural_triple_count")
    if type(frozen_count) is not int or not 0 <= frozen_count <= len(items):
        raise FrontierError("plan frozen-prefix count is invalid")
    previous_key: tuple[Any, ...] | None = None
    seen: set[str] = set()
    for ordinal, item in enumerate(items):
        _validate_plan_item(item, ordinal)
        key = _item_sort_key(item)
        if previous_key is not None and key < previous_key:
            raise FrontierError("plan items are not in deterministic sort order")
        previous_key = key
        if item["work_sha256"] in seen:
            raise FrontierError("plan has duplicate structural triples")
        seen.add(item["work_sha256"])
        expected_provenance = (
            "frozen-p1-baseline-scope" if ordinal < frozen_count else "new-extension"
        )
        if item["provenance_class"] != expected_provenance:
            raise FrontierError("plan provenance classes do not form a frozen prefix")
    expected_b0 = plan.get("b0_7_expected_counts")
    scope = plan.get("scope", {})
    if (scope.get("maximum_length"), scope.get("maximum_size_each_of_lam_mu")) == (6, 7):
        required_b0 = {
            "structural_total": B0_7_EXPECTED_STRUCTURAL_COUNT,
            "frozen_structural_prefix": P1_BASELINE_STRUCTURAL_COUNT,
            "new_structural_suffix": B0_7_EXPECTED_NEW_STRUCTURAL_COUNT,
            "frozen_nonzero": P1_BASELINE_NONZERO_COUNT,
            "frozen_zero": B0_7_EXPECTED_FROZEN_ZERO_COUNT,
            "new_nonzero": B0_7_EXPECTED_NEW_NONZERO_COUNT,
            "new_zero": B0_7_EXPECTED_NEW_ZERO_COUNT,
            "nonzero_total": B0_7_EXPECTED_TOTAL_NONZERO_COUNT,
            "zero_total": B0_7_EXPECTED_TOTAL_ZERO_COUNT,
        }
        if expected_b0 != required_b0 or len(items) != B0_7_EXPECTED_STRUCTURAL_COUNT:
            raise FrontierError("B0-7 plan invariants differ from preregistered counts")


def _validate_plan_item(item: Any, ordinal: int) -> None:
    if (
        not isinstance(item, dict)
        or type(item.get("ordinal")) is not int
        or type(ordinal) is not int
        or item.get("ordinal") != ordinal
    ):
        raise FrontierError(f"plan item {ordinal} has wrong ordinal")
    core = {
        key: item.get(key)
        for key in ("ordinal", "lam", "mu", "nu", "provenance_class")
    }
    if item.get("work_sha256") != sha256_json(core):
        raise FrontierError(f"plan item {ordinal} work hash mismatch")
    triple = _exact_triple_fields(core, context=f"plan item {ordinal}")
    if list(triple[0]) != core["lam"] or list(triple[1]) != core["mu"] or list(triple[2]) != core["nu"]:
        raise FrontierError(f"plan item {ordinal} is not swap-canonical")
    if sum(triple[0]) + sum(triple[1]) != sum(triple[2]):
        raise FrontierError(f"plan item {ordinal} violates weight balance")
    if not e1.contains(triple[2], triple[0]) or not e1.contains(triple[2], triple[1]):
        raise FrontierError(f"plan item {ordinal} violates structural containment")
    if core["provenance_class"] not in ("frozen-p1-baseline-scope", "new-extension"):
        raise FrontierError(f"plan item {ordinal} has invalid provenance class")


def _item_sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
    return (len(item["nu"]), tuple(item["nu"]), tuple(item["lam"]), tuple(item["mu"]))


def initialize_run(
    work_dir: Path,
    *,
    maximum_length: int,
    maximum_size: int,
    chunk_size: int = 32,
    champion_limit: int = 100,
    expected_structural_count: int | None = None,
) -> dict[str, Any]:
    """Create or verify an immutable plan without authorizing evaluation."""

    work_dir = Path(work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "chunks").mkdir(exist_ok=True)
    intended = make_plan(
        maximum_length,
        maximum_size,
        chunk_size=chunk_size,
        champion_limit=champion_limit,
        expected_structural_count=expected_structural_count,
    )
    path = work_dir / "plan.json"
    with run_lock(work_dir):
        if path.exists():
            actual = load_json(path)
            if actual != intended:
                raise FrontierError("existing run plan differs; use a new work directory")
        else:
            atomic_write_json(path, intended, immutable=True)
        state = _reconcile(work_dir, intended, repair_checkpoint=True)
    return _public_status(intended, state, authorized=(work_dir / "authorization.json").exists())


def authorize_run(
    work_dir: Path,
    *,
    gate_report_path: Path,
    evidence_manifest_path: Path,
    evidence_root: Path,
    explicit_confirmation: bool,
) -> dict[str, Any]:
    """Validate and freeze a passing P1 gate before any scientific evaluation."""

    if explicit_confirmation is not True:
        raise FrontierError("authorization requires explicit P1-pass confirmation")
    work_dir = Path(work_dir)
    plan = _load_plan(work_dir)
    report = load_json(Path(gate_report_path))
    manifest = load_json(Path(evidence_manifest_path))
    errors = validate_gate_report(report)
    if errors:
        raise FrontierError("invalid P1 gate report: " + "; ".join(errors))
    if report.get("passed") is not True:
        raise FrontierError("P1 gate report does not pass")
    if not isinstance(report.get("checked_at_utc"), str) or not report["checked_at_utc"].strip():
        raise FrontierError("P1 gate report lacks a checked_at_utc timestamp")
    verification = verify_manifest(Path(evidence_root), manifest)
    if not verification.valid:
        raise FrontierError("P1 evidence manifest fails: " + "; ".join(verification.errors))
    if report.get("evidence_manifest_sha256") != verification.manifest_sha256:
        raise FrontierError("P1 report does not bind the supplied evidence manifest")
    # Shape validation alone would allow a synthetically constructed list of
    # passing checks.  Re-run the complete scientific gate and require the
    # supplied adjudication artifact to be exactly its deterministic output.
    fresh_report = validate_p1_gate(
        evidence_root=Path(evidence_root),
        manifest=manifest,
        checked_at_utc=report["checked_at_utc"],
    )
    if fresh_report.get("passed") is not True:
        failures = fresh_report.get("failures", [])
        raise FrontierError(f"fresh P1 gate evaluation fails: {failures}")
    if fresh_report != report:
        raise FrontierError("supplied P1 gate report is stale or not reproducible")

    authorization_core = {
        "schema_version": AUTHORIZATION_SCHEMA,
        "gate_id": "P1",
        "gate_passed": True,
        "explicit_operator_confirmation": True,
        "plan_sha256": _plan_digest(plan),
        "gate_report_sha256": sha256_json(report),
        "evidence_manifest_sha256": verification.manifest_sha256,
        "gate_checked_at_utc": report.get("checked_at_utc"),
        "evidence_was_reverified_at_authorization": True,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
    }
    authorization = {
        **authorization_core,
        "authorization_id": f"sha256:{sha256_json(authorization_core)}",
    }
    with run_lock(work_dir):
        state = _reconcile(work_dir, plan, repair_checkpoint=False)
        if state.next_ordinal != 0:
            raise FrontierError("cannot add or change authorization after evaluation starts")
        auth_path = work_dir / "authorization.json"
        if auth_path.exists():
            if load_json(auth_path) != authorization:
                raise FrontierError("existing authorization binds different P1 evidence")
        else:
            atomic_write_json(auth_path, authorization, immutable=True)
        copies = work_dir / "authorization_evidence"
        copies.mkdir(exist_ok=True)
        atomic_write_json(copies / "gate_report.json", report, immutable=True)
        atomic_write_json(copies / "evidence_manifest.json", manifest, immutable=True)
    return authorization


def _validate_authorization(work_dir: Path, plan: dict[str, Any]) -> dict[str, Any]:
    path = Path(work_dir) / "authorization.json"
    if not path.is_file():
        raise FrontierError(
            "scientific evaluation is not authorized; validate and freeze a passing P1 gate first"
        )
    authorization = load_json(path)
    if not isinstance(authorization, dict) or authorization.get("schema_version") != AUTHORIZATION_SCHEMA:
        raise FrontierError("unsupported authorization artifact")
    core = {key: value for key, value in authorization.items() if key != "authorization_id"}
    if authorization.get("authorization_id") != f"sha256:{sha256_json(core)}":
        raise FrontierError("authorization identity hash mismatch")
    required = {
        "gate_id": "P1",
        "gate_passed": True,
        "explicit_operator_confirmation": True,
        "plan_sha256": _plan_digest(plan),
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
    }
    for key, expected in required.items():
        if authorization.get(key) != expected:
            raise FrontierError(f"authorization field {key!r} is invalid")
    report = load_json(Path(work_dir) / "authorization_evidence" / "gate_report.json")
    manifest = load_json(Path(work_dir) / "authorization_evidence" / "evidence_manifest.json")
    if sha256_json(report) != authorization.get("gate_report_sha256"):
        raise FrontierError("frozen P1 gate report hash mismatch")
    if sha256_json(manifest) != authorization.get("evidence_manifest_sha256"):
        raise FrontierError("frozen P1 evidence manifest hash mismatch")
    if validate_gate_report(report) or report.get("passed") is not True:
        raise FrontierError("frozen P1 gate report is not a valid pass")
    return authorization


def _validate_runtime(plan: dict[str, Any]) -> None:
    evaluator = plan["evaluator"]
    if evaluator.get("lrcalc_version") != e1.lrcalc_version():
        raise FrontierError("current lrcalc version differs from the immutable plan")
    if evaluator.get("e1_source_sha256") != _source_sha256():
        raise FrontierError("current E1 evaluator source differs from the immutable plan")
    if evaluator.get("pynormaliz_version") != _package_version("PyNormaliz"):
        raise FrontierError("current PyNormaliz version differs from the immutable plan")
    if evaluator.get("e2_source_sha256") != _e2_source_sha256():
        raise FrontierError("current E2 evaluator source differs from the immutable plan")
    expected_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    if evaluator.get("python_major_minor") != expected_python:
        raise FrontierError("current Python major/minor differs from the immutable plan")
    frozen = plan["frozen_prefix"]
    _baseline_bundle(
        frozen["source_file_sha256"],
        frozen["source_triples_payload_sha256"],
    )


def _initial_prefix(plan_sha256: str) -> str:
    return sha256_json({
        "domain": "lr-scientific-pilot-prefix/v1",
        "plan_sha256": plan_sha256,
    })


def _extend_prefix(prefix: str, record_sha256: str) -> str:
    return sha256_json({
        "domain": "lr-scientific-pilot-prefix-step/v1",
        "previous_prefix_sha256": prefix,
        "record_sha256": record_sha256,
    })


def _zero_counts() -> dict[str, int]:
    return {key: 0 for key in _COUNTER_KEYS}


def _add_counts(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    return {key: left[key] + right[key] for key in _COUNTER_KEYS}


def _subrecord(schema: str, core: dict[str, Any]) -> dict[str, Any]:
    payload = {"schema_version": schema, **core}
    return {**payload, "record_sha256": sha256_json(payload)}


def _validate_hive_typed_input(
    hive_input: dict[str, Any],
    triple: e1.Triple,
    *,
    n: int,
) -> None:
    """Validate the exact integer matrix before it crosses the Normaliz API."""

    if type(n) is not int or n < 1:
        raise FrontierError("E2 hive side length must be an exact positive integer")
    if hive_input.get("n") != n or type(hive_input.get("n")) is not int:
        raise FrontierError("typed hive input has an invalid exact side length")
    for key, expected in zip(("lam", "mu", "nu"), triple):
        actual = hive_input.get(key)
        if not isinstance(actual, list) or any(type(value) is not int for value in actual):
            raise FrontierError(f"typed hive input {key} is not an exact-integer array")
        if tuple(actual) != expected:
            raise FrontierError(f"typed hive input {key} disagrees with the plan")
    normaliz = hive_input.get("normaliz")
    rows = normaliz.get("rows") if isinstance(normaliz, dict) else None
    if not isinstance(rows, list):
        raise FrontierError("typed hive input lacks Normaliz rows")
    expected_width = hive_input.get("ambient_dimension")
    if type(expected_width) is not int or expected_width < 0:
        raise FrontierError("typed hive ambient dimension is not an exact integer")
    for index, row in enumerate(rows):
        if not isinstance(row, list) or len(row) != expected_width + 1:
            raise FrontierError(f"Normaliz row {index} has the wrong exact width")
        if any(type(value) is not int for value in row):
            raise FrontierError(
                f"Normaliz row {index} contains a bool, float, or non-exact integer"
            )
    boundary = hive_input.get("boundary")
    if not isinstance(boundary, dict) or any(type(value) is not int for value in boundary.values()):
        raise FrontierError("typed hive boundary is not exact-integer data")


def _canonical_polynomial(value: Any, *, context: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise FrontierError(f"{context} canonical polynomial is missing")
    try:
        polynomial = tuple(Fraction(coefficient) for coefficient in value)
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise FrontierError(f"{context} polynomial contains an invalid rational") from exc
    canonical = e1.canonical_polynomial_strings(polynomial)
    if canonical != value:
        raise FrontierError(f"{context} polynomial is not canonical")
    return canonical


def _baseline_record(plan: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    frozen = plan["frozen_prefix"]
    mapping, identity = _baseline_bundle(
        frozen["source_file_sha256"],
        frozen["source_triples_payload_sha256"],
    )
    triple = _exact_triple_fields(item, context=f"work item {item['ordinal']}")
    polynomial = mapping.get(triple)
    if polynomial is None:
        return _subrecord(
            BASELINE_RECORD_SCHEMA,
            {
                "source": "frozen-p1-baseline-complement",
                "typed_input": {
                    "lam": item["lam"], "mu": item["mu"], "nu": item["nu"]
                },
                "baseline_triples_payload_sha256": identity["triples_payload_sha256"],
                "unstretched_coefficient": 0,
                "positive_stretches_excluded_by_saturation": True,
            },
        )
    return _subrecord(
        BASELINE_RECORD_SCHEMA,
        {
            "source": "frozen-p1-baseline-nonzero-record",
            "typed_input": {
                "lam": item["lam"], "mu": item["mu"], "nu": item["nu"]
            },
            "baseline_triples_payload_sha256": identity["triples_payload_sha256"],
            "baseline_entry_sha256": sha256_json({
                "lam": item["lam"],
                "mu": item["mu"],
                "nu": item["nu"],
                "poly": list(polynomial),
            }),
            "canonical_polynomial": list(polynomial),
        },
    )


def _new_e1_record(item: dict[str, Any], triple: e1.Triple, n1: int) -> dict[str, Any]:
    if type(n1) is not int or n1 <= 0:
        raise FrontierError("new E1 nonzero record requires an exact positive N=1 count")
    evaluation = e1.evaluate_stretched(
        *triple,
        mode=EVALUATOR_MODE,
        known_n1=n1,
    )
    evidence = evaluation.evidence()
    if any(type(value) is not int for value in evidence["values"]):
        raise FrontierError("E1 returned a non-exact sampled count")
    polynomial = _canonical_polynomial(evidence["polynomial"], context="E1")
    return _subrecord(
        E1_RECORD_SCHEMA,
        {
            "evaluator": "lrcalc-interp",
            "typed_input": {
                "lam": item["lam"], "mu": item["mu"], "nu": item["nu"]
            },
            "interpolation_mode": EVALUATOR_MODE,
            "unstretched_coefficient": n1,
            "canonical_polynomial": polynomial,
            "raw_evidence": evidence,
        },
    )


def _new_e2_record(item: dict[str, Any], triple: e1.Triple) -> dict[str, Any]:
    n = len(triple[2])
    if n != 6 and item.get("provenance_class") == "new-extension":
        # Generic boxes with baseline reuse disabled may legitimately evaluate
        # other row counts.  B0-7 itself reaches this path exactly at n=6.
        n = max(len(partition) for partition in triple)
    if type(n) is not int or n < 1:
        n = 1
    polytope = e2.build_hive_polytope(*triple, n=n)
    hive_input = polytope.input_dict()
    _validate_hive_typed_input(hive_input, triple, n=n)
    raw_evidence = e2.evaluate_with_normaliz(polytope)
    polynomial = _canonical_polynomial(
        raw_evidence.get("canonical_polynomial"), context="E2"
    )
    lattice_points = raw_evidence.get("number_lattice_points")
    if type(lattice_points) is not int or lattice_points < 0:
        raise FrontierError("E2 returned a non-exact N=1 lattice count")
    return _subrecord(
        E2_RECORD_SCHEMA,
        {
            "evaluator": "normaliz-ehrhart",
            "typed_input": hive_input,
            "canonical_polynomial": polynomial,
            "number_lattice_points_at_n1": lattice_points,
            "raw_evidence": raw_evidence,
        },
    )


def _agreement_record(e1_record: dict[str, Any], e2_record: dict[str, Any]) -> dict[str, Any]:
    polynomial_match = (
        e1_record["canonical_polynomial"] == e2_record["canonical_polynomial"]
    )
    n1_match = (
        e1_record["unstretched_coefficient"]
        == e2_record["number_lattice_points_at_n1"]
    )
    return _subrecord(
        AGREEMENT_RECORD_SCHEMA,
        {
            "e1_record_sha256": e1_record["record_sha256"],
            "e2_record_sha256": e2_record["record_sha256"],
            "e1_canonical_polynomial": e1_record["canonical_polynomial"],
            "e2_canonical_polynomial": e2_record["canonical_polynomial"],
            "canonical_polynomials_match": polynomial_match,
            "n1_counts_match": n1_match,
            "all_agree": polynomial_match and n1_match,
        },
    )


def _record_core(plan: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    plan_sha256 = _plan_digest(plan)
    triple = _exact_triple_fields(item, context=f"work item {item['ordinal']}")
    base: dict[str, Any] = {
        "schema_version": RECORD_SCHEMA,
        "plan_sha256": plan_sha256,
        "ordinal": item["ordinal"],
        "work_sha256": item["work_sha256"],
        "lam": item["lam"],
        "mu": item["mu"],
        "nu": item["nu"],
        "provenance_class": item["provenance_class"],
    }
    if item["provenance_class"] == "frozen-p1-baseline-scope":
        baseline_record = _baseline_record(plan, item)
        if baseline_record["source"] == "frozen-p1-baseline-complement":
            return {
                **base,
                "status": "zero",
                "source": "frozen-p1-baseline",
                "unstretched_coefficient": 0,
                "baseline_record": baseline_record,
            }
        return {
            **base,
            "status": "nonzero",
            "source": "frozen-p1-baseline",
            "canonical_polynomial": baseline_record["canonical_polynomial"],
            "baseline_record": baseline_record,
        }
    phase = "unstretched-lrcalc"
    e1_record: dict[str, Any] | None = None
    try:
        n1 = e1.lr_coefficient(*triple)
        if type(n1) is not int:
            raise FrontierError("lrcalc returned a non-exact integer count")
        base["unstretched_coefficient"] = n1
        if n1 == 0:
            return {
                **base,
                "status": "zero",
                "source": "new-extension-lrcalc-zero",
                "reason": "lrcalc unstretched coefficient is zero; saturation excludes all stretches",
            }
        phase = "bounded-stretched-e1-with-holdout"
        e1_record = _new_e1_record(item, triple, n1)
        phase = "explicit-hive-normaliz-e2"
        e2_record = _new_e2_record(item, triple)
        phase = "e1-e2-agreement"
        agreement = _agreement_record(e1_record, e2_record)
        if not agreement["all_agree"]:
            return {
                **base,
                "status": "error",
                "source": "new-extension-cross-evaluated",
                "e1_record": e1_record,
                "e2_record": e2_record,
                "agreement_record": agreement,
                "error": {
                    "phase": phase,
                    "type": "p1.pilot_frontier.EvaluatorDisagreement",
                    "message": "E1 and E2 canonical polynomial or N=1 count differs",
                },
            }
        return {
            **base,
            "status": "nonzero",
            "source": "new-extension-cross-evaluated",
            "canonical_polynomial": e1_record["canonical_polynomial"],
            "e1_record": e1_record,
            "e2_record": e2_record,
            "agreement_record": agreement,
        }
    except Exception as exc:
        error_record = {
            **base,
            "status": "error",
            "source": "new-extension-cross-evaluated",
            "error": {
                "phase": phase,
                "type": f"{type(exc).__module__}.{type(exc).__qualname__}",
                "message": str(exc),
            },
        }
        if e1_record is not None:
            error_record["e1_record"] = e1_record
        return error_record


def evaluate_item(plan: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    _validate_plan_item(item, item.get("ordinal"))
    core = _record_core(plan, item)
    return {**core, "record_sha256": sha256_json(core)}


def _build_chunk(
    plan: dict[str, Any],
    start: int,
    previous_prefix: str,
) -> dict[str, Any]:
    total = len(plan["items"])
    end = _next_chunk_end(plan, start)
    plan_hash = _plan_digest(plan)
    prefix = previous_prefix
    records: list[dict[str, Any]] = []
    counts = _zero_counts()
    for item in plan["items"][start:end]:
        record = evaluate_item(plan, item)
        records.append(record)
        counts[record["status"]] += 1
        prefix = _extend_prefix(prefix, record["record_sha256"])
    core = {
        "schema_version": CHUNK_SCHEMA,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "plan_sha256": plan_hash,
        "start_ordinal": start,
        "end_ordinal_exclusive": end,
        "previous_prefix_sha256": previous_prefix,
        "prefix_sha256": prefix,
        "counts": counts,
        "records": records,
    }
    return {**core, "chunk_payload_sha256": sha256_json(core)}


def _chunk_name(start: int, end: int) -> str:
    return f"chunk-{start:08d}-{end:08d}.json"


def _next_chunk_end(plan: dict[str, Any], start: int) -> int:
    """Return the preregistered fixed boundary following ``start``.

    B0-7 imports its inexpensive frozen prefix as one immutable chunk, then
    uses the configured small chunk size for the Normaliz-bearing extension.
    This avoids hundreds of tiny baseline-only files without changing any
    record or prefix hash.
    """

    total = len(plan["items"])
    frozen = plan["frozen_prefix"]
    frozen_end = frozen["structural_triple_count"]
    if (
        start == 0
        and frozen.get("coalesce_as_one_immutable_chunk") is True
        and frozen_end > 0
    ):
        return frozen_end
    return min(start + plan["chunk_size"], total)


def _remaining_chunk_count(plan: dict[str, Any], start: int) -> int:
    count = 0
    cursor = start
    while cursor < len(plan["items"]):
        following = _next_chunk_end(plan, cursor)
        if following <= cursor:
            raise FrontierError("plan chunk boundaries do not advance")
        cursor = following
        count += 1
    return count


def _commit_chunk(work_dir: Path, chunk: dict[str, Any]) -> None:
    name = _chunk_name(chunk["start_ordinal"], chunk["end_ordinal_exclusive"])
    path = Path(work_dir) / "chunks" / name
    atomic_write_json(path, chunk, immutable=True)
    digest = sha256_file(path)
    atomic_write_text(path.with_suffix(".json.sha256"), f"{digest}  {name}\n", immutable=True)


def _checkpoint(plan: dict[str, Any], state: DurableState) -> dict[str, Any]:
    return {
        "schema_version": CHECKPOINT_SCHEMA,
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "outcome_b_eligible": False,
        "plan_sha256": _plan_digest(plan),
        "next_ordinal": state.next_ordinal,
        "structural_triple_count": len(plan["items"]),
        "chunk_count": state.chunk_count,
        "prefix_sha256": state.prefix_sha256,
        "counts": state.counts,
        "complete": state.next_ordinal == len(plan["items"]),
        "partial": state.next_ordinal != len(plan["items"]),
        "minima_and_champions_available": False,
    }


def _write_checkpoint(work_dir: Path, plan: dict[str, Any], state: DurableState) -> None:
    atomic_write_json(Path(work_dir) / "checkpoint.json", _checkpoint(plan, state))


def run_frontier(work_dir: Path, *, max_chunks: int | None = None) -> dict[str, Any]:
    """Run or resume fixed chunks; ``None`` consumes the remaining plan."""

    if max_chunks is not None:
        if isinstance(max_chunks, bool) or not isinstance(max_chunks, int) or max_chunks < 0:
            raise FrontierError("max_chunks must be a nonnegative integer or null")
    work_dir = Path(work_dir)
    plan = _load_plan(work_dir)
    with run_lock(work_dir):
        _validate_authorization(work_dir, plan)
        _validate_runtime(plan)
        state = _reconcile(work_dir, plan, repair_checkpoint=True)
        if state.counts["error"]:
            raise FrontierError(
                "durable prefix contains an evaluator error/disagreement; refusing to advance"
            )
        total = len(plan["items"])
        remaining_chunks = _remaining_chunk_count(plan, state.next_ordinal)
        budget = remaining_chunks if max_chunks is None else min(max_chunks, remaining_chunks)
        for _ in range(budget):
            chunk = _build_chunk(plan, state.next_ordinal, state.prefix_sha256)
            _commit_chunk(work_dir, chunk)
            # The just-written immutable chunk is already fully constructed and
            # hashed.  Advance in memory instead of rescanning an ever-growing
            # prefix after every chunk.  A crash in the narrow window before the
            # checkpoint write is recovered by the full reconciliation at the
            # start of the next invocation.
            new_counts = _add_counts(state.counts, chunk["counts"])
            new_cursor = chunk["end_ordinal_exclusive"]
            new_chunk_count = state.chunk_count + 1
            state = DurableState(
                next_ordinal=new_cursor,
                prefix_sha256=chunk["prefix_sha256"],
                counts=new_counts,
                chunk_count=new_chunk_count,
                snapshots={
                    new_cursor: (
                        chunk["prefix_sha256"],
                        dict(new_counts),
                        new_chunk_count,
                    )
                },
            )
            _write_checkpoint(work_dir, plan, state)
            if state.counts["error"]:
                raise FrontierError(
                    "frontier evaluator error/disagreement was preserved; refusing the next chunk"
                )
        if state.next_ordinal == total:
            _write_or_verify_completion(work_dir, plan, state, allow_create=True)
        elif (work_dir / "completion.json").exists():
            raise FrontierError("incomplete run has a completion artifact")
        return _public_status(plan, state, authorized=True)


def _validate_record(record: Any, plan_hash: str, item: dict[str, Any]) -> None:
    if not isinstance(record, dict) or record.get("schema_version") != RECORD_SCHEMA:
        raise FrontierError(f"malformed result record for ordinal {item['ordinal']}")
    core = {key: value for key, value in record.items() if key != "record_sha256"}
    if record.get("record_sha256") != sha256_json(core):
        raise FrontierError(f"record digest mismatch at ordinal {item['ordinal']}")
    for key in ("ordinal", "work_sha256", "lam", "mu", "nu", "provenance_class"):
        if record.get(key) != item.get(key):
            raise FrontierError(f"record {item['ordinal']} disagrees with plan field {key}")
    if record.get("plan_sha256") != plan_hash:
        raise FrontierError(f"record {item['ordinal']} has wrong plan hash")
    status_value = record.get("status")
    if status_value not in _COUNTER_KEYS:
        raise FrontierError(f"record {item['ordinal']} has invalid status")
    triple = _exact_triple_fields(record, context=f"record {item['ordinal']}")

    def validate_subrecord(value: Any, schema: str, label: str) -> dict[str, Any]:
        if not isinstance(value, dict) or value.get("schema_version") != schema:
            raise FrontierError(f"record {item['ordinal']} has malformed {label}")
        subcore = {key: field for key, field in value.items() if key != "record_sha256"}
        if value.get("record_sha256") != sha256_json(subcore):
            raise FrontierError(f"record {item['ordinal']} {label} digest mismatch")
        return value

    provenance = item["provenance_class"]
    if provenance == "frozen-p1-baseline-scope":
        baseline = validate_subrecord(
            record.get("baseline_record"), BASELINE_RECORD_SCHEMA, "baseline record"
        )
        if record.get("source") != "frozen-p1-baseline":
            raise FrontierError(f"record {item['ordinal']} has wrong frozen source")
        typed = baseline.get("typed_input")
        if not isinstance(typed, dict) or _exact_triple_fields(
            typed, context=f"record {item['ordinal']} baseline input"
        ) != triple:
            raise FrontierError(f"record {item['ordinal']} frozen typed input differs")
        if baseline.get("baseline_triples_payload_sha256") != P1_BASELINE_PAYLOAD_SHA256:
            raise FrontierError(f"record {item['ordinal']} frozen payload hash differs")
        if status_value == "zero":
            if baseline.get("source") != "frozen-p1-baseline-complement":
                raise FrontierError(f"record {item['ordinal']} zero lacks baseline-complement proof")
            if record.get("unstretched_coefficient") != 0 or baseline.get("unstretched_coefficient") != 0:
                raise FrontierError(f"zero record {item['ordinal']} is inconsistent")
        elif status_value == "nonzero":
            if baseline.get("source") != "frozen-p1-baseline-nonzero-record":
                raise FrontierError(f"record {item['ordinal']} nonzero lacks frozen evidence")
            polynomial = _canonical_polynomial(
                baseline.get("canonical_polynomial"), context="frozen baseline"
            )
            if record.get("canonical_polynomial") != polynomial:
                raise FrontierError(f"record {item['ordinal']} frozen polynomial differs")
        else:
            raise FrontierError(f"frozen-prefix record {item['ordinal']} cannot be an error")
        if any(key in record for key in ("e1_record", "e2_record", "agreement_record")):
            raise FrontierError(f"frozen-prefix record {item['ordinal']} mixes evaluator evidence")
        return

    if status_value == "zero":
        if (
            record.get("source") != "new-extension-lrcalc-zero"
            or record.get("unstretched_coefficient") != 0
            or any(key in record for key in ("e1_record", "e2_record", "agreement_record", "error"))
        ):
            raise FrontierError(f"zero record {item['ordinal']} is inconsistent")
    elif status_value == "nonzero":
        if type(record.get("unstretched_coefficient")) is not int or record["unstretched_coefficient"] <= 0:
            raise FrontierError(f"nonzero record {item['ordinal']} has invalid N=1 count")
        e1_record = validate_subrecord(record.get("e1_record"), E1_RECORD_SCHEMA, "E1 record")
        e2_record = validate_subrecord(record.get("e2_record"), E2_RECORD_SCHEMA, "E2 record")
        agreement = validate_subrecord(
            record.get("agreement_record"), AGREEMENT_RECORD_SCHEMA, "agreement record"
        )
        if record.get("source") != "new-extension-cross-evaluated":
            raise FrontierError(f"record {item['ordinal']} has wrong extension source")
        e1_input = e1_record.get("typed_input")
        if not isinstance(e1_input, dict) or _exact_triple_fields(
            e1_input, context=f"record {item['ordinal']} E1 input"
        ) != triple:
            raise FrontierError(f"record {item['ordinal']} E1 typed input differs")
        if e1_record.get("interpolation_mode") != EVALUATOR_MODE:
            raise FrontierError(f"record {item['ordinal']} E1 mode differs")
        coefficients = _canonical_polynomial(e1_record.get("canonical_polynomial"), context="E1")
        evidence = e1_record.get("raw_evidence")
        values = evidence.get("values") if isinstance(evidence, dict) else None
        if not isinstance(values, list) or any(type(value) is not int or value < 0 for value in values):
            raise FrontierError(f"record {item['ordinal']} has non-exact E1 samples")
        polynomial = tuple(Fraction(value) for value in coefficients)
        if evidence.get("polynomial") != coefficients:
            raise FrontierError(f"record {item['ordinal']} E1 raw/canonical polynomial differs")
        if e1_record.get("unstretched_coefficient") != record["unstretched_coefficient"]:
            raise FrontierError(f"record {item['ordinal']} E1/top-level N=1 count differs")
        for point, expected in enumerate(values):
            if e1.evaluate_polynomial(polynomial, point) != expected:
                raise FrontierError(f"record {item['ordinal']} polynomial/sample mismatch")
        if len(values) <= 1 or values[1] != record["unstretched_coefficient"]:
            raise FrontierError(f"record {item['ordinal']} N=1 evidence mismatch")
        if evidence.get("mode") != EVALUATOR_MODE or evidence.get("inferred_degree") != len(coefficients) - 1:
            raise FrontierError(f"record {item['ordinal']} inferred degree mismatch")
        hive_input = e2_record.get("typed_input")
        if not isinstance(hive_input, dict):
            raise FrontierError(f"record {item['ordinal']} lacks typed E2 input")
        _validate_hive_typed_input(hive_input, triple, n=hive_input.get("n"))
        e2_polynomial = _canonical_polynomial(
            e2_record.get("canonical_polynomial"), context="E2"
        )
        raw_e2 = e2_record.get("raw_evidence")
        if not isinstance(raw_e2, dict) or raw_e2.get("canonical_polynomial") != e2_polynomial:
            raise FrontierError(f"record {item['ordinal']} E2 raw/canonical evidence differs")
        if type(e2_record.get("number_lattice_points_at_n1")) is not int:
            raise FrontierError(f"record {item['ordinal']} E2 N=1 count is not exact")
        if raw_e2.get("number_lattice_points") != e2_record["number_lattice_points_at_n1"]:
            raise FrontierError(f"record {item['ordinal']} E2 raw/typed N=1 count differs")
        if e2_record["number_lattice_points_at_n1"] != record["unstretched_coefficient"]:
            raise FrontierError(f"record {item['ordinal']} E2/top-level N=1 count differs")
        required_agreement = {
            "e1_record_sha256": e1_record["record_sha256"],
            "e2_record_sha256": e2_record["record_sha256"],
            "e1_canonical_polynomial": coefficients,
            "e2_canonical_polynomial": e2_polynomial,
            "canonical_polynomials_match": True,
            "n1_counts_match": True,
            "all_agree": True,
        }
        for key, expected in required_agreement.items():
            if agreement.get(key) != expected:
                raise FrontierError(f"record {item['ordinal']} agreement field {key} differs")
        if record.get("canonical_polynomial") != coefficients:
            raise FrontierError(f"record {item['ordinal']} top-level polynomial differs")
    else:
        error = record.get("error")
        if not isinstance(error, dict) or not all(isinstance(error.get(key), str) for key in ("phase", "type", "message")):
            raise FrontierError(f"error record {item['ordinal']} lacks deterministic diagnostics")
        if record.get("source") != "new-extension-cross-evaluated":
            raise FrontierError(f"error record {item['ordinal']} has wrong source")
        optional_schemas = (
            ("e1_record", E1_RECORD_SCHEMA),
            ("e2_record", E2_RECORD_SCHEMA),
            ("agreement_record", AGREEMENT_RECORD_SCHEMA),
        )
        for key, schema in optional_schemas:
            if key in record:
                validate_subrecord(record[key], schema, key.replace("_", " "))
        if "agreement_record" in record and record["agreement_record"].get("all_agree") is not False:
            raise FrontierError(f"error record {item['ordinal']} has inconsistent agreement")


def _validate_chunk(
    chunk: Any,
    plan: dict[str, Any],
    expected_start: int,
    expected_prefix: str,
) -> tuple[str, dict[str, int]]:
    if not isinstance(chunk, dict) or chunk.get("schema_version") != CHUNK_SCHEMA:
        raise FrontierError(f"malformed chunk starting at {expected_start}")
    core = {key: value for key, value in chunk.items() if key != "chunk_payload_sha256"}
    if chunk.get("chunk_payload_sha256") != sha256_json(core):
        raise FrontierError(f"chunk payload digest mismatch at {expected_start}")
    expected_end = _next_chunk_end(plan, expected_start)
    fixed = {
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "plan_sha256": _plan_digest(plan),
        "start_ordinal": expected_start,
        "end_ordinal_exclusive": expected_end,
        "previous_prefix_sha256": expected_prefix,
    }
    for key, expected in fixed.items():
        if chunk.get(key) != expected:
            raise FrontierError(f"chunk {expected_start} has invalid field {key}")
    records = chunk.get("records")
    if not isinstance(records, list) or len(records) != expected_end - expected_start:
        raise FrontierError(f"chunk {expected_start} has wrong record count")
    prefix = expected_prefix
    counts = _zero_counts()
    for offset, record in enumerate(records):
        item = plan["items"][expected_start + offset]
        _validate_record(record, _plan_digest(plan), item)
        counts[record["status"]] += 1
        prefix = _extend_prefix(prefix, record["record_sha256"])
    if chunk.get("counts") != counts:
        raise FrontierError(f"chunk {expected_start} counter mismatch")
    if chunk.get("prefix_sha256") != prefix:
        raise FrontierError(f"chunk {expected_start} prefix hash mismatch")
    return prefix, counts


def _chunk_artifacts(chunks_dir: Path) -> list[tuple[int, int, Path]]:
    entries: list[tuple[int, int, Path]] = []
    if not chunks_dir.is_dir():
        raise FrontierError("chunks directory is missing")
    for path in chunks_dir.iterdir():
        if path.name.startswith(".") and ".tmp-" in path.name:
            continue
        if path.name.endswith(".json.sha256"):
            continue
        match = _CHUNK_RE.fullmatch(path.name)
        if not match or not path.is_file():
            raise FrontierError(f"unexpected entry in chunks directory: {path.name}")
        entries.append((int(match.group(1)), int(match.group(2)), path))
    entries.sort()
    return entries


def _verify_or_create_sidecar(path: Path, *, repair: bool) -> None:
    digest = sha256_file(path)
    expected = f"{digest}  {path.name}\n"
    sidecar = path.with_suffix(".json.sha256")
    if sidecar.exists():
        try:
            actual = sidecar.read_text(encoding="utf-8")
        except OSError as exc:
            raise FrontierError(f"cannot read chunk sidecar {sidecar}: {exc}") from exc
        if actual != expected:
            raise FrontierError(f"chunk file digest mismatch: {path.name}")
    elif repair:
        atomic_write_text(sidecar, expected, immutable=True)
    else:
        raise FrontierError(f"chunk sidecar is missing: {sidecar.name}")


def _validate_checkpoint(
    checkpoint: Any,
    plan: dict[str, Any],
    state: DurableState,
) -> None:
    if not isinstance(checkpoint, dict) or checkpoint.get("schema_version") != CHECKPOINT_SCHEMA:
        raise FrontierError("malformed checkpoint")
    required = {
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "outcome_b_eligible": False,
        "plan_sha256": _plan_digest(plan),
        "structural_triple_count": len(plan["items"]),
        "minima_and_champions_available": False,
    }
    for key, expected in required.items():
        if checkpoint.get(key) != expected:
            raise FrontierError(f"checkpoint field {key!r} is invalid")
    cursor = checkpoint.get("next_ordinal")
    if not isinstance(cursor, int) or isinstance(cursor, bool) or cursor not in state.snapshots:
        if isinstance(cursor, int) and cursor > state.next_ordinal:
            raise FrontierError("checkpoint is ahead of durable chunks")
        raise FrontierError("checkpoint cursor is not a durable chunk boundary")
    prefix, counts, chunk_count = state.snapshots[cursor]
    if checkpoint.get("prefix_sha256") != prefix or checkpoint.get("counts") != counts:
        raise FrontierError("checkpoint digest/counters disagree with its durable prefix")
    if checkpoint.get("chunk_count") != chunk_count:
        raise FrontierError("checkpoint chunk count disagrees with durable prefix")
    if checkpoint.get("complete") != (cursor == len(plan["items"])):
        raise FrontierError("checkpoint complete flag is inconsistent")
    if checkpoint.get("partial") != (cursor != len(plan["items"])):
        raise FrontierError("checkpoint partial flag is inconsistent")


def _reconcile(work_dir: Path, plan: dict[str, Any], *, repair_checkpoint: bool) -> DurableState:
    _validate_plan(plan)
    plan_hash = _plan_digest(plan)
    prefix = _initial_prefix(plan_hash)
    counts = _zero_counts()
    cursor = 0
    chunk_count = 0
    snapshots: dict[int, tuple[str, dict[str, int], int]] = {
        0: (prefix, dict(counts), 0)
    }
    for start, end, path in _chunk_artifacts(Path(work_dir) / "chunks"):
        expected_end = _next_chunk_end(plan, cursor)
        if start != cursor or end != expected_end or path.name != _chunk_name(cursor, expected_end):
            raise FrontierError("chunk artifacts are not the fixed contiguous plan prefix")
        chunk = load_json(path)
        new_prefix, chunk_counts = _validate_chunk(chunk, plan, cursor, prefix)
        _verify_or_create_sidecar(path, repair=repair_checkpoint)
        prefix = new_prefix
        counts = _add_counts(counts, chunk_counts)
        cursor = end
        chunk_count += 1
        snapshots[cursor] = (prefix, dict(counts), chunk_count)
    state = DurableState(cursor, prefix, counts, chunk_count, snapshots)
    checkpoint_path = Path(work_dir) / "checkpoint.json"
    if checkpoint_path.exists():
        checkpoint = load_json(checkpoint_path)
        _validate_checkpoint(checkpoint, plan, state)
        if checkpoint["next_ordinal"] < state.next_ordinal:
            if not repair_checkpoint:
                raise FrontierError("checkpoint lags durable chunks")
            _write_checkpoint(work_dir, plan, state)
    elif repair_checkpoint:
        _write_checkpoint(work_dir, plan, state)
    elif cursor:
        raise FrontierError("durable chunks exist without a checkpoint")
    return state


def _iter_records(work_dir: Path) -> Iterator[dict[str, Any]]:
    for _, _, path in _chunk_artifacts(Path(work_dir) / "chunks"):
        chunk = load_json(path)
        yield from chunk["records"]


def _fraction_string(value: Fraction) -> str:
    return str(value)


def _champion_entry(record: dict[str, Any], coefficient_index: int) -> dict[str, Any]:
    polynomial = record["canonical_polynomial"]
    return {
        "ordinal": record["ordinal"],
        "lam": record["lam"],
        "mu": record["mu"],
        "nu": record["nu"],
        "hive_rows": len(record["nu"]),
        "degree": len(polynomial) - 1,
        "coefficient_index": coefficient_index,
        "coefficient": polynomial[coefficient_index],
        "record_sha256": record["record_sha256"],
    }


def _summarize_completed(work_dir: Path, plan: dict[str, Any], state: DurableState) -> dict[str, Any]:
    if state.next_ordinal != len(plan["items"]):
        raise FrontierError("minima and champions are forbidden for incomplete runs")
    if state.counts["error"]:
        raise FrontierError("completion/minima are forbidden when any evaluator record errored")
    overall: dict[str, list[tuple[Fraction, dict[str, Any]]]] = {
        "all_coefficients": [],
        "nonleading_coefficients": [],
    }
    strata: dict[tuple[int, int], dict[str, list[tuple[Fraction, dict[str, Any]]]]] = {}
    negative_records: dict[int, dict[str, Any]] = {}
    provenance_counts = {
        "frozen_structural": 0,
        "frozen_zero": 0,
        "frozen_nonzero": 0,
        "new_structural": 0,
        "new_zero": 0,
        "new_nonzero_e1_e2_agreed": 0,
        "new_error": 0,
    }
    for record in _iter_records(work_dir):
        if record["provenance_class"] == "frozen-p1-baseline-scope":
            provenance_counts["frozen_structural"] += 1
            provenance_counts[f"frozen_{record['status']}"] += 1
        else:
            provenance_counts["new_structural"] += 1
            if record["status"] == "nonzero":
                provenance_counts["new_nonzero_e1_e2_agreed"] += 1
            else:
                provenance_counts[f"new_{record['status']}"] += 1
        if record["status"] != "nonzero":
            continue
        coefficients = [Fraction(value) for value in record["canonical_polynomial"]]
        degree = len(coefficients) - 1
        stratum = strata.setdefault(
            (len(record["nu"]), degree),
            {"all_coefficients": [], "nonleading_coefficients": []},
        )
        for index, coefficient in enumerate(coefficients):
            entry = _champion_entry(record, index)
            overall["all_coefficients"].append((coefficient, entry))
            stratum["all_coefficients"].append((coefficient, entry))
            if index < degree:
                overall["nonleading_coefficients"].append((coefficient, entry))
                stratum["nonleading_coefficients"].append((coefficient, entry))
            if coefficient < 0:
                negative_records[record["ordinal"]] = {
                    "ordinal": record["ordinal"],
                    "lam": record["lam"],
                    "mu": record["mu"],
                    "nu": record["nu"],
                    "polynomial": record["canonical_polynomial"],
                    "record_sha256": record["record_sha256"],
                }

    expected_b0 = plan.get("b0_7_expected_counts")
    if expected_b0 is not None:
        actual_b0 = {
            "structural_total": state.next_ordinal,
            "frozen_structural_prefix": provenance_counts["frozen_structural"],
            "new_structural_suffix": provenance_counts["new_structural"],
            "frozen_nonzero": provenance_counts["frozen_nonzero"],
            "frozen_zero": provenance_counts["frozen_zero"],
            "new_nonzero": provenance_counts["new_nonzero_e1_e2_agreed"],
            "new_zero": provenance_counts["new_zero"],
            "nonzero_total": state.counts["nonzero"],
            "zero_total": state.counts["zero"],
        }
        if actual_b0 != expected_b0:
            raise FrontierError(
                f"completed B0-7 counts disagree with preregistration: {actual_b0}"
            )

    def metric(values: Sequence[tuple[Fraction, dict[str, Any]]]) -> dict[str, Any] | None:
        if not values:
            return None
        minimum = min(value for value, _ in values)
        tied = [entry for value, entry in values if value == minimum]
        tied.sort(key=lambda entry: (entry["ordinal"], entry["coefficient_index"]))
        return {
            "minimum": _fraction_string(minimum),
            "tie_count": len(tied),
            "champions_truncated": len(tied) > plan["champion_limit"],
            "champions": tied[: plan["champion_limit"]],
        }

    stratum_rows = []
    for (rows, degree), values in sorted(strata.items()):
        stratum_rows.append({
            "hive_rows": rows,
            "degree": degree,
            "min_coefficient": metric(values["all_coefficients"]),
            "min_nonleading_coefficient": metric(values["nonleading_coefficients"]),
        })
    return {
        "min_coefficient": metric(overall["all_coefficients"]),
        "min_nonleading_coefficient": metric(overall["nonleading_coefficients"]),
        "provenance_counts": provenance_counts,
        "b0_7_expected_counts_verified": expected_b0 is not None,
        "strata": stratum_rows,
        "has_negative_coefficient": bool(negative_records),
        "negative_record_count": len(negative_records),
        "negative_candidates": [negative_records[index] for index in sorted(negative_records)],
        "negative_candidates_require_independent_verification": True,
    }


def _completion(plan: dict[str, Any], state: DurableState, summary: dict[str, Any], work_dir: Path) -> dict[str, Any]:
    chunks = []
    for start, end, path in _chunk_artifacts(Path(work_dir) / "chunks"):
        chunks.append({
            "path": f"chunks/{path.name}",
            "start_ordinal": start,
            "end_ordinal_exclusive": end,
            "file_sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })
    core = {
        "schema_version": COMPLETION_SCHEMA,
        "campaign_stage": "post-P1-scientific-pilot",
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "outcome_b_eligible": False,
        "certified_outcome_b": False,
        "classification_note": (
            "A completed pilot imports the verified P1 prefix and cross-evaluates "
            "new nonzero records with E1 and E2; it is not preregistered outcome B."
        ),
        "plan_sha256": _plan_digest(plan),
        "authorization_sha256": sha256_json(load_json(Path(work_dir) / "authorization.json")),
        "complete": True,
        "structural_triple_count": len(plan["items"]),
        "processed_record_count": state.next_ordinal,
        "chunk_count": state.chunk_count,
        "prefix_sha256": state.prefix_sha256,
        "counts": state.counts,
        "evaluation_complete_without_errors": state.counts["error"] == 0,
        "chunks": chunks,
        "summary": summary,
    }
    return {**core, "completion_sha256": sha256_json(core)}


def _write_or_verify_completion(
    work_dir: Path,
    plan: dict[str, Any],
    state: DurableState,
    *,
    allow_create: bool,
) -> dict[str, Any]:
    if state.next_ordinal != len(plan["items"]):
        raise FrontierError("cannot complete an unconsumed plan")
    summary = _summarize_completed(work_dir, plan, state)
    expected = _completion(plan, state, summary, work_dir)
    path = Path(work_dir) / "completion.json"
    if path.exists():
        if load_json(path) != expected:
            raise FrontierError("completion artifact is stale or tampered")
    elif allow_create:
        atomic_write_json(path, expected, immutable=True)
        atomic_write_text(
            path.with_suffix(".json.sha256"),
            f"{sha256_file(path)}  {path.name}\n",
            immutable=True,
        )
    else:
        raise FrontierError("completed durable prefix lacks completion artifact")
    sidecar = path.with_suffix(".json.sha256")
    expected_sidecar = f"{sha256_file(path)}  {path.name}\n"
    if not sidecar.exists() and allow_create:
        # Recover the narrow crash window after the immutable completion rename
        # but before its sidecar rename.  The completion content was recomputed
        # and matched above, so creating the missing digest is safe.
        atomic_write_text(sidecar, expected_sidecar, immutable=True)
    if not sidecar.exists() or sidecar.read_text(encoding="utf-8") != expected_sidecar:
        raise FrontierError("completion sidecar is missing or invalid")
    return expected


def _load_plan(work_dir: Path) -> dict[str, Any]:
    path = Path(work_dir) / "plan.json"
    if not path.is_file():
        raise FrontierError(f"frontier plan is missing: {path}")
    plan = load_json(path)
    _validate_plan(plan)
    return plan


def _public_status(plan: dict[str, Any], state: DurableState, *, authorized: bool) -> dict[str, Any]:
    total = len(plan["items"])
    # Intentionally no minima/champion fields here.  Those are valid only in a
    # verified completion artifact after the entire structural plan is consumed.
    return {
        "schema_version": "lr-scientific-pilot-status/v1",
        "evidence_classification": EVIDENCE_CLASSIFICATION,
        "outcome_label": OUTCOME_LABEL,
        "outcome_b_eligible": False,
        "authorized": authorized,
        "complete": state.next_ordinal == total,
        "partial": state.next_ordinal != total,
        "next_ordinal": state.next_ordinal,
        "structural_triple_count": total,
        "remaining": total - state.next_ordinal,
        "chunk_count": state.chunk_count,
        "prefix_sha256": state.prefix_sha256,
        "counts": state.counts,
        "minima_and_champions_available": state.next_ordinal == total,
    }


def status(work_dir: Path, *, repair_checkpoint: bool = False) -> dict[str, Any]:
    work_dir = Path(work_dir)
    plan = _load_plan(work_dir)
    with run_lock(work_dir):
        state = _reconcile(work_dir, plan, repair_checkpoint=repair_checkpoint)
        authorized = (work_dir / "authorization.json").exists()
        if authorized:
            _validate_authorization(work_dir, plan)
        return _public_status(plan, state, authorized=authorized)


def verify_run(work_dir: Path, *, require_complete: bool = True) -> dict[str, Any]:
    """Verify every artifact and return a non-mutating verification report."""

    work_dir = Path(work_dir)
    plan = _load_plan(work_dir)
    with run_lock(work_dir):
        _validate_authorization(work_dir, plan)
        _validate_runtime(plan)
        state = _reconcile(work_dir, plan, repair_checkpoint=False)
        total = len(plan["items"])
        if require_complete and state.next_ordinal != total:
            raise FrontierError(f"run is incomplete: {state.next_ordinal}/{total}")
        completion_digest = None
        if state.next_ordinal == total:
            completion = _write_or_verify_completion(
                work_dir, plan, state, allow_create=False
            )
            completion_digest = completion["completion_sha256"]
        elif (work_dir / "completion.json").exists():
            raise FrontierError("partial run has an invalid completion artifact")
        return {
            "schema_version": VERIFICATION_SCHEMA,
            "valid": True,
            "complete": state.next_ordinal == total,
            "partial": state.next_ordinal != total,
            "evidence_classification": EVIDENCE_CLASSIFICATION,
            "outcome_label": OUTCOME_LABEL,
            "outcome_b_eligible": False,
            "plan_sha256": _plan_digest(plan),
            "next_ordinal": state.next_ordinal,
            "structural_triple_count": total,
            "prefix_sha256": state.prefix_sha256,
            "counts": state.counts,
            "completion_sha256": completion_digest,
        }
