"""Deterministic orchestration-only checkpoint/resume pilot.

The pilot exercises cursor recovery and immutable per-item artifacts.  Its output
is explicitly barred from serving as mathematical or P2 evidence.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from .atomic import atomic_write_json, load_json
from .canonical import is_sha256, sha256_json
from .errors import ValidationError
from .manifest import build_manifest, verify_manifest

PLAN_SCHEMA = "lr-resume-pilot-plan/v1"
RESULT_SCHEMA = "lr-resume-pilot-result/v1"
CHECKPOINT_SCHEMA = "lr-resume-pilot-checkpoint/v1"
CHECKPOINT_SNAPSHOT_SCHEMA = "lr-resume-pilot-checkpoint-snapshot/v1"
COMPLETION_SCHEMA = "lr-resume-pilot-completion/v1"
CHECKPOINT_SNAPSHOT_DIR = "checkpoint-snapshots"

_DEFAULT_ITEMS = [
    {"lam": [], "mu": [], "nu": []},
    {"lam": [1], "mu": [], "nu": [1]},
    {"lam": [], "mu": [1], "nu": [1]},
    {"lam": [1], "mu": [1], "nu": [1, 1]},
    {"lam": [1], "mu": [1], "nu": [2]},
    {"lam": [2], "mu": [1], "nu": [2, 1]},
    {"lam": [1, 1], "mu": [1], "nu": [1, 1, 1]},
    {"lam": [2, 1], "mu": [1], "nu": [2, 1, 1]},
    {"lam": [2], "mu": [2], "nu": [3, 1]},
    {"lam": [2, 1], "mu": [2, 1], "nu": [3, 2, 1]},
]


def make_plan(items: list[dict[str, list[int]]] | None = None) -> dict[str, Any]:
    items = _DEFAULT_ITEMS if items is None else items
    normalized = [_validate_item(item) for item in items]
    normalized.sort(key=_item_sort_key)
    if len({sha256_json(item) for item in normalized}) != len(normalized):
        raise ValidationError("pilot items must be unique")
    identity = {
        "schema_version": PLAN_SCHEMA,
        "kind": "orchestration-only",
        "not_scientific_evidence": True,
        "sort_key": "(len(nu),nu,lam,mu)",
        "items": normalized,
    }
    return {**identity, "plan_id": f"sha256:{sha256_json(identity)}"}


def run_pilot(
    work_dir: Path,
    *,
    stop_after: int | None = None,
    items: list[dict[str, list[int]]] | None = None,
) -> dict[str, Any]:
    """Run or resume the pilot, processing at most ``stop_after`` new items."""

    if stop_after is not None and (
        not isinstance(stop_after, int) or isinstance(stop_after, bool) or stop_after < 0
    ):
        raise ValidationError("stop_after must be a non-negative integer or null")
    work_dir = Path(work_dir)
    results_dir = work_dir / "results"
    work_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    intended_plan = make_plan(items)
    plan_path = work_dir / "plan.json"
    if plan_path.exists():
        persisted_plan = load_json(plan_path)
        if persisted_plan != intended_plan:
            raise ValidationError("existing pilot plan differs; use a new work directory")
    else:
        atomic_write_json(plan_path, intended_plan, overwrite=False)

    next_index, prefix = _reconcile(work_dir, intended_plan, repair_checkpoint=True)
    total = len(intended_plan["items"])
    budget = total - next_index if stop_after is None else min(stop_after, total - next_index)
    plan_hash = sha256_json(intended_plan)
    for index in range(next_index, next_index + budget):
        result = _expected_result(plan_hash, index, intended_plan["items"][index])
        atomic_write_json(_result_path(results_dir, index), result, overwrite=False)
        prefix = _extend_prefix(prefix, result)
        checkpoint = _checkpoint(plan_hash, index + 1, total, prefix)
        atomic_write_json(work_dir / "checkpoint.json", checkpoint)

    next_index += budget
    if next_index == 0 and not (work_dir / "checkpoint.json").exists():
        atomic_write_json(
            work_dir / "checkpoint.json", _checkpoint(plan_hash, 0, total, prefix)
        )
    if next_index == total:
        _write_or_verify_completion(work_dir, intended_plan, prefix)
    checkpoint = load_json(work_dir / "checkpoint.json")
    if next_index < total:
        _write_or_verify_checkpoint_snapshot(work_dir, checkpoint)
    return checkpoint


def verify_pilot(work_dir: Path, *, require_complete: bool = True) -> dict[str, Any]:
    """Validate the complete immutable prefix and, if present, completion manifest."""

    work_dir = Path(work_dir)
    plan = load_json(work_dir / "plan.json")
    _validate_plan(plan)
    next_index, prefix = _reconcile(work_dir, plan, repair_checkpoint=False)
    total = len(plan["items"])
    if require_complete and next_index != total:
        raise ValidationError(f"pilot is incomplete: cursor {next_index}/{total}")
    if next_index == total:
        _write_or_verify_completion(work_dir, plan, prefix, allow_create=False)
    return {
        "schema_version": "lr-resume-pilot-verification/v1",
        "valid": True,
        "complete": next_index == total,
        "next_index": next_index,
        "total": total,
        "prefix_sha256": prefix,
        "not_scientific_evidence": True,
    }


def checkpoint_snapshot_path(work_dir: Path, next_index: int) -> Path:
    """Return the deterministic path for an immutable paused-prefix snapshot."""

    if not isinstance(next_index, int) or isinstance(next_index, bool) or next_index < 0:
        raise ValidationError("checkpoint snapshot cursor must be a non-negative integer")
    return Path(work_dir) / CHECKPOINT_SNAPSHOT_DIR / f"{next_index:06d}.json"


def verify_checkpoint_snapshot(
    work_dir: Path,
    snapshot_path: Path,
    *,
    require_current: bool = False,
) -> dict[str, Any]:
    """Prove an immutable checkpoint snapshot against its durable result prefix.

    Unlike :func:`verify_pilot`, this deliberately does not require the mutable
    ``checkpoint.json`` cursor to equal the snapshot cursor.  A historical
    snapshot therefore remains verifiable after later results, including a
    completed pilot.  ``require_current`` is reserved for the state transition
    that first records the pause and rejects a stale historical snapshot there.
    """

    work_dir = Path(work_dir)
    snapshot_path = Path(snapshot_path)
    plan = load_json(work_dir / "plan.json")
    _validate_plan(plan)
    plan_hash = sha256_json(plan)
    total = len(plan["items"])
    snapshot = load_json(snapshot_path)
    _validate_checkpoint_snapshot(snapshot, plan_hash, total)
    expected_path = checkpoint_snapshot_path(work_dir, snapshot["next_index"])
    if snapshot_path.resolve() != expected_path.resolve():
        raise ValidationError(
            "checkpoint snapshot is not at its deterministic immutable path"
        )

    prefix_at = _validated_result_prefixes(work_dir, plan)
    cursor = snapshot["next_index"]
    if cursor >= len(prefix_at):
        raise ValidationError("checkpoint snapshot is ahead of durable result artifacts")
    if snapshot["prefix_sha256"] != prefix_at[cursor]:
        raise ValidationError("checkpoint snapshot digest does not match its durable prefix")

    durable_count = len(prefix_at) - 1
    if require_current:
        checkpoint = load_json(work_dir / "checkpoint.json")
        _validate_checkpoint(checkpoint, plan_hash, total)
        if checkpoint != _checkpoint(plan_hash, cursor, total, prefix_at[cursor]):
            raise ValidationError("checkpoint snapshot is not the current mutable checkpoint")
        if durable_count != cursor:
            raise ValidationError("checkpoint snapshot is stale relative to durable results")

    return {
        "schema_version": "lr-resume-pilot-checkpoint-snapshot-verification/v1",
        "valid": True,
        "next_index": cursor,
        "total": total,
        "prefix_sha256": snapshot["prefix_sha256"],
        "durable_result_count": durable_count,
        "historical": durable_count > cursor,
        "pilot_complete": durable_count == total,
        "not_scientific_evidence": True,
    }


def _reconcile(
    work_dir: Path,
    plan: dict[str, Any],
    *,
    repair_checkpoint: bool,
) -> tuple[int, str]:
    _validate_plan(plan)
    plan_hash = sha256_json(plan)
    prefix_at = _validated_result_prefixes(work_dir, plan)
    result_count = len(prefix_at) - 1
    prefix = prefix_at[-1]

    checkpoint_path = work_dir / "checkpoint.json"
    if checkpoint_path.exists():
        checkpoint = load_json(checkpoint_path)
        _validate_checkpoint(checkpoint, plan_hash, len(plan["items"]))
        cursor = checkpoint["next_index"]
        if cursor > result_count:
            raise ValidationError("checkpoint is ahead of durable result artifacts")
        if checkpoint["prefix_sha256"] != prefix_at[cursor]:
            raise ValidationError("checkpoint prefix digest does not match result artifacts")
        if cursor < result_count:
            if not repair_checkpoint:
                raise ValidationError("checkpoint lags result artifacts")
            atomic_write_json(
                checkpoint_path,
                _checkpoint(plan_hash, result_count, len(plan["items"]), prefix),
            )
    elif result_count:
        if not repair_checkpoint:
            raise ValidationError("result artifacts exist without a checkpoint")
        atomic_write_json(
            checkpoint_path,
            _checkpoint(plan_hash, result_count, len(plan["items"]), prefix),
        )
    return result_count, prefix


def _validated_result_prefixes(work_dir: Path, plan: dict[str, Any]) -> list[str]:
    """Return every valid rolling prefix, including the empty prefix at index 0."""

    results_dir = work_dir / "results"
    if not results_dir.is_dir():
        raise ValidationError("pilot results directory is missing")
    files = sorted(results_dir.iterdir(), key=lambda path: path.name)
    if any(not path.is_file() or path.suffix != ".json" for path in files):
        raise ValidationError("pilot results directory contains an unexpected entry")
    expected_names = [f"{index:06d}.json" for index in range(len(files))]
    if [path.name for path in files] != expected_names:
        raise ValidationError("pilot result files are not a contiguous prefix")
    if len(files) > len(plan["items"]):
        raise ValidationError("pilot has more result files than plan items")

    plan_hash = sha256_json(plan)
    prefix = _initial_prefix()
    prefix_at: list[str] = [prefix]
    for index, path in enumerate(files):
        actual = load_json(path)
        expected = _expected_result(plan_hash, index, plan["items"][index])
        if actual != expected:
            raise ValidationError(f"pilot result {path.name} is missing, stale, or tampered")
        prefix = _extend_prefix(prefix, actual)
        prefix_at.append(prefix)
    return prefix_at


def _write_or_verify_checkpoint_snapshot(
    work_dir: Path, checkpoint: dict[str, Any]
) -> Path:
    """Persist one immutable, deterministic snapshot for an incomplete cursor."""

    plan = load_json(work_dir / "plan.json")
    _validate_plan(plan)
    _validate_checkpoint(checkpoint, sha256_json(plan), len(plan["items"]))
    if checkpoint["completed"] is not False:
        raise ValidationError("completed checkpoints are represented by completion.json")
    snapshot = _checkpoint_snapshot(checkpoint)
    path = checkpoint_snapshot_path(work_dir, checkpoint["next_index"])
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        if load_json(path) != snapshot:
            raise ValidationError("immutable checkpoint snapshot conflicts with durable prefix")
    else:
        atomic_write_json(path, snapshot, overwrite=False)
    verify_checkpoint_snapshot(work_dir, path, require_current=True)
    return path


def _write_or_verify_completion(
    work_dir: Path,
    plan: dict[str, Any],
    prefix: str,
    *,
    allow_create: bool = True,
) -> None:
    specs = [
        {"logical_path": "plan.json", "role": "pilot-plan", "media_type": "application/json"},
        {
            "logical_path": "checkpoint.json",
            "role": "pilot-checkpoint",
            "media_type": "application/json",
        },
    ]
    specs.extend(
        {
            "logical_path": f"results/{index:06d}.json",
            "role": "pilot-result",
            "media_type": "application/json",
        }
        for index in range(len(plan["items"]))
    )
    manifest = build_manifest(
        root=work_dir,
        artifact_specs=specs,
        producer={
            "actor": "orchestration-pilot",
            "writer_id": "deterministic-pilot-v1",
            "tool": "p1.control.pilot",
            "tool_version": "1.0.0",
        },
        scope="orchestration-only checkpoint/resume validation; never scientific evidence",
        created_utc="1970-01-01T00:00:00Z",
    )
    completion = {
        "schema_version": COMPLETION_SCHEMA,
        "kind": "orchestration-only",
        "not_scientific_evidence": True,
        "may_authorize_p2": False,
        "plan_sha256": sha256_json(plan),
        "prefix_sha256": prefix,
        "artifact_manifest": manifest,
        "artifact_manifest_sha256": sha256_json(manifest),
    }
    path = work_dir / "completion.json"
    if path.exists():
        actual = load_json(path)
        if actual != completion:
            raise ValidationError("pilot completion artifact is stale or tampered")
        verification = verify_manifest(work_dir, actual["artifact_manifest"])
        if not verification.valid:
            raise ValidationError(
                "pilot completion manifest failed: " + "; ".join(verification.errors)
            )
    elif allow_create:
        atomic_write_json(path, completion, overwrite=False)
    else:
        raise ValidationError("completed pilot has no completion artifact")


def _expected_result(plan_hash: str, index: int, item: dict[str, list[int]]) -> dict[str, Any]:
    work_payload = {"ordinal": index, "item": item, "plan_sha256": plan_hash}
    return {
        "schema_version": RESULT_SCHEMA,
        "kind": "orchestration-only",
        "not_scientific_evidence": True,
        **work_payload,
        "work_sha256": sha256_json(work_payload),
    }


def _checkpoint(plan_hash: str, next_index: int, total: int, prefix: str) -> dict[str, Any]:
    return {
        "schema_version": CHECKPOINT_SCHEMA,
        "kind": "orchestration-only",
        "not_scientific_evidence": True,
        "plan_sha256": plan_hash,
        "next_index": next_index,
        "total": total,
        "prefix_sha256": prefix,
        "completed": next_index == total,
    }


def _checkpoint_snapshot(checkpoint: dict[str, Any]) -> dict[str, Any]:
    """Return the deterministic immutable representation of a paused checkpoint."""

    return {
        "schema_version": CHECKPOINT_SNAPSHOT_SCHEMA,
        "kind": "orchestration-only",
        "not_scientific_evidence": True,
        "plan_sha256": checkpoint["plan_sha256"],
        "next_index": checkpoint["next_index"],
        "total": checkpoint["total"],
        "prefix_sha256": checkpoint["prefix_sha256"],
        "completed": checkpoint["completed"],
        "checkpoint_sha256": sha256_json(checkpoint),
    }


def _validate_plan(plan: Any) -> None:
    if not isinstance(plan, dict) or plan.get("schema_version") != PLAN_SCHEMA:
        raise ValidationError("unsupported pilot plan")
    if plan.get("kind") != "orchestration-only" or plan.get("not_scientific_evidence") is not True:
        raise ValidationError("pilot plan lacks the non-scientific scope guard")
    items = plan.get("items")
    if not isinstance(items, list) or not items:
        raise ValidationError("pilot plan items must be a non-empty list")
    normalized = [_validate_item(item) for item in items]
    if normalized != sorted(normalized, key=_item_sort_key):
        raise ValidationError("pilot items are not in deterministic order")
    identity = {key: value for key, value in plan.items() if key != "plan_id"}
    if plan.get("plan_id") != f"sha256:{sha256_json(identity)}":
        raise ValidationError("pilot plan_id does not match its canonical identity")


def _validate_checkpoint(checkpoint: Any, plan_hash: str, total: int) -> None:
    if not isinstance(checkpoint, dict) or checkpoint.get("schema_version") != CHECKPOINT_SCHEMA:
        raise ValidationError("unsupported pilot checkpoint")
    if set(checkpoint) != {
        "schema_version",
        "kind",
        "not_scientific_evidence",
        "plan_sha256",
        "next_index",
        "total",
        "prefix_sha256",
        "completed",
    }:
        raise ValidationError("pilot checkpoint fields do not match its schema")
    if (
        checkpoint.get("kind") != "orchestration-only"
        or checkpoint.get("not_scientific_evidence") is not True
    ):
        raise ValidationError("pilot checkpoint scope guard is missing")
    if checkpoint.get("plan_sha256") != plan_hash or checkpoint.get("total") != total:
        raise ValidationError("checkpoint belongs to a different pilot plan")
    cursor = checkpoint.get("next_index")
    if not isinstance(cursor, int) or isinstance(cursor, bool) or not 0 <= cursor <= total:
        raise ValidationError("checkpoint cursor is invalid")
    if checkpoint.get("completed") is not (cursor == total):
        raise ValidationError("checkpoint completed flag contradicts cursor")
    if not is_sha256(checkpoint.get("prefix_sha256")):
        raise ValidationError("checkpoint prefix digest is invalid")


def _validate_checkpoint_snapshot(snapshot: Any, plan_hash: str, total: int) -> None:
    if (
        not isinstance(snapshot, dict)
        or snapshot.get("schema_version") != CHECKPOINT_SNAPSHOT_SCHEMA
    ):
        raise ValidationError("unsupported pilot checkpoint snapshot")
    if set(snapshot) != {
        "schema_version",
        "kind",
        "not_scientific_evidence",
        "plan_sha256",
        "next_index",
        "total",
        "prefix_sha256",
        "completed",
        "checkpoint_sha256",
    }:
        raise ValidationError("pilot checkpoint snapshot fields do not match its schema")
    if (
        snapshot.get("kind") != "orchestration-only"
        or snapshot.get("not_scientific_evidence") is not True
    ):
        raise ValidationError("pilot checkpoint snapshot scope guard is missing")
    if snapshot.get("plan_sha256") != plan_hash or snapshot.get("total") != total:
        raise ValidationError("checkpoint snapshot belongs to a different pilot plan")
    cursor = snapshot.get("next_index")
    if (
        not isinstance(cursor, int)
        or isinstance(cursor, bool)
        or not 0 <= cursor < total
        or snapshot.get("completed") is not False
    ):
        raise ValidationError("checkpoint snapshot must represent an incomplete cursor")
    checkpoint = _checkpoint(
        plan_hash,
        cursor,
        total,
        snapshot.get("prefix_sha256"),
    )
    _validate_checkpoint(checkpoint, plan_hash, total)
    if snapshot.get("checkpoint_sha256") != sha256_json(checkpoint):
        raise ValidationError("checkpoint snapshot is not bound to its checkpoint bytes")


def _validate_item(item: Any) -> dict[str, list[int]]:
    if not isinstance(item, dict) or set(item) != {"lam", "mu", "nu"}:
        raise ValidationError("each pilot item must contain exactly lam, mu, nu")
    normalized: dict[str, list[int]] = {}
    for name in ("lam", "mu", "nu"):
        partition = item[name]
        if not isinstance(partition, list) or not all(
            isinstance(value, int) and not isinstance(value, bool) and value > 0
            for value in partition
        ):
            if partition != []:
                raise ValidationError(f"{name} is not a positive-integer partition")
        if partition != sorted(partition, reverse=True):
            raise ValidationError(f"{name} is not weakly decreasing")
        normalized[name] = list(partition)
    return normalized


def _item_sort_key(item: dict[str, list[int]]) -> tuple[Any, ...]:
    return (len(item["nu"]), tuple(item["nu"]), tuple(item["lam"]), tuple(item["mu"]))


def _result_path(results_dir: Path, index: int) -> Path:
    return results_dir / f"{index:06d}.json"


def _initial_prefix() -> str:
    return hashlib.sha256(b"lr-resume-pilot-prefix/v1").hexdigest()


def _extend_prefix(prefix: str, result: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    digest.update(bytes.fromhex(prefix))
    digest.update(bytes.fromhex(sha256_json(result)))
    return digest.hexdigest()
