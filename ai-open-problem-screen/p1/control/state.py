"""Schema-versioned campaign state with exclusive, atomic transitions."""

from __future__ import annotations

import json
import os
import secrets
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

from .atomic import atomic_write_json, load_json
from .canonical import is_sha256, sha256_file, sha256_json
from .errors import LockError, TransitionError, ValidationError

STATE_SCHEMA = "lr-campaign-state/v1"

# There is intentionally no transition into P2_RUNNING.  The final state means
# that an integrator may adjudicate launch; it is not launch authorization.
ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    "P0_READY": frozenset({"P1_FIXTURES_READY"}),
    "P1_FIXTURES_READY": frozenset({"P1_ORACLE_VALIDATED"}),
    "P1_ORACLE_VALIDATED": frozenset({"PILOT_READY"}),
    "PILOT_READY": frozenset({"PILOT_RUNNING"}),
    "PILOT_RUNNING": frozenset({"PILOT_CHECKPOINTED", "PILOT_COMPLETE"}),
    "PILOT_CHECKPOINTED": frozenset({"PILOT_RUNNING"}),
    "PILOT_COMPLETE": frozenset({"P2_AWAITING_AUTHORIZATION"}),
    "P2_AWAITING_AUTHORIZATION": frozenset(),
}

EVIDENCE_REQUIRED = frozenset(
    {
        "P1_FIXTURES_READY",
        "P1_ORACLE_VALIDATED",
        "PILOT_CHECKPOINTED",
        "PILOT_COMPLETE",
        "P2_AWAITING_AUTHORIZATION",
    }
)

TARGET_EVIDENCE_KINDS: dict[str, frozenset[str]] = {
    "P1_FIXTURES_READY": frozenset({"fixture-manifest"}),
    "P1_ORACLE_VALIDATED": frozenset({"p1-gate-report", "p1-evidence-manifest"}),
    "PILOT_CHECKPOINTED": frozenset({"pilot-checkpoint-snapshot"}),
    "PILOT_COMPLETE": frozenset({"pilot-completion"}),
    "P2_AWAITING_AUTHORIZATION": frozenset(
        {
            "readiness-report",
            "p1-gate-report",
            "p1-evidence-manifest",
            "pilot-completion",
            "campaign-state-snapshot",
        }
    ),
}


def make_initial_state(
    *,
    campaign: str,
    run_id: str,
    owner_id: str,
    at_utc: str,
) -> dict[str, Any]:
    initial_transition = {
        "from": None,
        "to": "P0_READY",
        "actor_role": "integrator",
        "actor_id": owner_id,
        "at_utc": at_utc,
        "reason": "state initialized",
        "evidence": [],
    }
    state = {
        "schema_version": STATE_SCHEMA,
        "campaign": _nonempty(campaign, "campaign"),
        "run_id": _nonempty(run_id, "run_id"),
        "phase_state": "P0_READY",
        "revision": 0,
        "state_owner": {"role": "integrator", "id": _nonempty(owner_id, "owner_id")},
        "updated_utc": _nonempty(at_utc, "at_utc"),
        "previous_document_sha256": None,
        "last_transition": initial_transition,
        "transition_history": [initial_transition],
    }
    validate_state(state)
    return state


def validate_state(state: Any) -> None:
    if not isinstance(state, dict):
        raise ValidationError("state must be a JSON object")
    if state.get("schema_version") != STATE_SCHEMA:
        raise ValidationError(f"unsupported state schema: {state.get('schema_version')!r}")
    for field in ("campaign", "run_id", "updated_utc"):
        _nonempty(state.get(field), field)
    phase = state.get("phase_state")
    if phase not in ALLOWED_TRANSITIONS:
        raise ValidationError(f"unknown phase_state: {phase!r}")
    revision = state.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise ValidationError("revision must be a non-negative integer")
    owner = state.get("state_owner")
    if not isinstance(owner, dict) or owner.get("role") != "integrator":
        raise ValidationError("state_owner.role must be 'integrator'")
    _nonempty(owner.get("id"), "state_owner.id")
    previous = state.get("previous_document_sha256")
    if previous is not None and not is_sha256(previous):
        raise ValidationError("previous_document_sha256 must be null or lowercase SHA-256")
    transition = state.get("last_transition")
    _validate_transition_record(transition, phase, owner)
    history = state.get("transition_history")
    if not isinstance(history, list) or len(history) != revision + 1:
        raise ValidationError("transition_history length must equal revision + 1")
    for index, record in enumerate(history):
        if not isinstance(record, dict):
            raise ValidationError(f"transition_history[{index}] must be an object")
        record_phase = record.get("to")
        if record_phase not in ALLOWED_TRANSITIONS:
            raise ValidationError(f"transition_history[{index}].to is unknown")
        _validate_transition_record(record, record_phase, owner)
        if index == 0:
            if record.get("from") is not None or record_phase != "P0_READY":
                raise ValidationError("transition history must begin with P0_READY initialization")
        elif record.get("from") != history[index - 1].get("to"):
            raise ValidationError(f"transition_history[{index}] is not contiguous")
    if history[-1] != transition:
        raise ValidationError("last_transition must equal the final transition_history record")
    if revision == 0:
        if phase != "P0_READY" or previous is not None or transition.get("from") is not None:
            raise ValidationError("revision 0 must be the unhashed P0_READY initialization state")
    elif previous is None or transition.get("from") is None:
        raise ValidationError("revisions after initialization require prior hash and source state")


def _validate_transition_record(record: Any, phase: str, owner: dict[str, str]) -> None:
    if not isinstance(record, dict):
        raise ValidationError("last_transition must be an object")
    if record.get("to") != phase:
        raise ValidationError("last_transition.to must equal phase_state")
    if record.get("actor_role") != "integrator":
        raise ValidationError("only the integrator may own campaign-state transitions")
    if record.get("actor_id") != owner.get("id"):
        raise ValidationError("last_transition actor does not match state owner")
    for field in ("at_utc", "reason"):
        _nonempty(record.get(field), f"last_transition.{field}")
    source = record.get("from")
    if source is not None:
        if source not in ALLOWED_TRANSITIONS or phase not in ALLOWED_TRANSITIONS[source]:
            raise ValidationError(f"last transition {source!r} -> {phase!r} is not allowed")
    evidence = record.get("evidence")
    if not isinstance(evidence, list):
        raise ValidationError("last_transition.evidence must be a list")
    for item in evidence:
        if not isinstance(item, dict):
            raise ValidationError("each evidence record must be an object")
        _nonempty(item.get("kind"), "evidence.kind")
        _validate_evidence_path(item.get("path"))
        if not is_sha256(item.get("sha256")):
            raise ValidationError("evidence.sha256 must be a lowercase SHA-256")
    if phase in EVIDENCE_REQUIRED and not evidence:
        raise ValidationError(f"transition to {phase} requires hashed evidence")
    required_kinds = TARGET_EVIDENCE_KINDS.get(phase, frozenset())
    present_kinds = {item["kind"] for item in evidence}
    missing_kinds = required_kinds - present_kinds
    if missing_kinds:
        raise ValidationError(
            f"transition to {phase} lacks evidence kinds: {', '.join(sorted(missing_kinds))}"
        )


def transition_document(
    current: dict[str, Any],
    *,
    target: str,
    actor_role: str,
    actor_id: str,
    at_utc: str,
    reason: str,
    evidence: list[dict[str, str]],
) -> dict[str, Any]:
    validate_state(current)
    source = current["phase_state"]
    if target not in ALLOWED_TRANSITIONS.get(source, frozenset()):
        raise TransitionError(f"transition {source} -> {target} is not allowed")
    owner = current["state_owner"]
    if actor_role != "integrator" or actor_role != owner["role"]:
        raise TransitionError("only the designated integrator may transition state")
    if actor_id != owner["id"]:
        raise TransitionError("actor_id does not match the designated state owner")

    updated = dict(current)
    updated["phase_state"] = target
    updated["revision"] = current["revision"] + 1
    updated["updated_utc"] = _nonempty(at_utc, "at_utc")
    updated["previous_document_sha256"] = sha256_json(current)
    transition_record = {
        "from": source,
        "to": target,
        "actor_role": actor_role,
        "actor_id": actor_id,
        "at_utc": at_utc,
        "reason": _nonempty(reason, "reason"),
        "evidence": evidence,
    }
    updated["last_transition"] = transition_record
    updated["transition_history"] = list(current["transition_history"]) + [transition_record]
    validate_state(updated)
    return updated


@dataclass
class StateLease:
    path: Path
    owner_id: str
    nonce: str
    _released: bool = False

    @classmethod
    def acquire(cls, path: Path, owner_id: str, at_utc: str) -> "StateLease":
        path = Path(path)
        if not path.parent.is_dir():
            raise LockError(f"lock parent does not exist: {path.parent}")
        nonce = secrets.token_hex(16)
        record = {
            "schema_version": "lr-state-lock/v1",
            "owner_id": _nonempty(owner_id, "owner_id"),
            "pid": os.getpid(),
            "acquired_utc": _nonempty(at_utc, "at_utc"),
            "nonce": nonce,
        }
        try:
            descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise LockError(
                f"state lock already exists at {path}; inspect it manually, never steal it automatically"
            ) from exc
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8", closefd=True) as handle:
                json.dump(record, handle, sort_keys=True, separators=(",", ":"))
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
        except BaseException:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
            raise
        return cls(path=path, owner_id=owner_id, nonce=nonce)

    def release(self) -> None:
        if self._released:
            return
        try:
            record = load_json(self.path)
        except ValidationError as exc:
            raise LockError(f"cannot safely release modified lock {self.path}: {exc}") from exc
        if record.get("nonce") != self.nonce or record.get("owner_id") != self.owner_id:
            raise LockError("lock ownership changed; refusing to remove another writer's lock")
        try:
            self.path.unlink()
        except FileNotFoundError as exc:
            raise LockError("state lock disappeared before release") from exc
        self._released = True

    def __enter__(self) -> "StateLease":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.release()


class StateStore:
    """CAS-style state store; every write requires an exclusive lease."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.lock_path = self.path.with_name(f"{self.path.name}.lock")

    def read(self) -> tuple[dict[str, Any], str]:
        state = load_json(self.path)
        validate_state(state)
        return state, sha256_json(state)

    def initialize(self, state: dict[str, Any], lease: StateLease) -> str:
        self._check_lease(lease)
        validate_state(state)
        if lease.owner_id != state["state_owner"]["id"]:
            raise TransitionError("initializing lease does not match the designated state owner")
        if self.path.exists():
            raise TransitionError(f"state already exists: {self.path}")
        atomic_write_json(self.path, state, overwrite=False)
        persisted, digest = self.read()
        if persisted != state:
            raise TransitionError("post-write state verification failed")
        return digest

    def transition(
        self,
        *,
        lease: StateLease,
        expected_revision: int,
        expected_sha256: str,
        target: str,
        actor_role: str,
        actor_id: str,
        at_utc: str,
        reason: str,
        evidence: list[dict[str, str]],
        evidence_root: Path,
    ) -> tuple[dict[str, Any], str]:
        self._check_lease(lease)
        current, current_digest = self.read()
        if current["revision"] != expected_revision:
            raise TransitionError(
                f"stale revision: expected {expected_revision}, found {current['revision']}"
            )
        if current_digest != expected_sha256:
            raise TransitionError("state digest changed since it was read")
        _verify_evidence_files(evidence_root, target, evidence)
        updated = transition_document(
            current,
            target=target,
            actor_role=actor_role,
            actor_id=actor_id,
            at_utc=at_utc,
            reason=reason,
            evidence=evidence,
        )
        atomic_write_json(self.path, updated)
        persisted, digest = self.read()
        if persisted != updated:
            raise TransitionError("post-transition state verification failed")
        return persisted, digest

    def _check_lease(self, lease: StateLease) -> None:
        if lease.path != self.lock_path or lease._released:
            raise LockError("a live lease for this state path is required")
        record = load_json(lease.path)
        if record.get("nonce") != lease.nonce or record.get("owner_id") != lease.owner_id:
            raise LockError("lease no longer owns the state lock")


def _nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{field} must be a non-empty string")
    return value


def _validate_evidence_path(value: object) -> str:
    value = _nonempty(value, "evidence.path")
    if "\\" in value:
        raise ValidationError("evidence.path must use '/' separators")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        raise ValidationError(f"unsafe evidence.path: {value!r}")
    if path.as_posix() != value:
        raise ValidationError(f"non-canonical evidence.path: {value!r}")
    return value


def _verify_evidence_files(
    evidence_root: Path,
    target: str,
    evidence: list[dict[str, str]],
) -> None:
    """Verify evidence bytes and target-specific pass semantics before a write."""

    root = Path(evidence_root).resolve()
    if not root.is_dir():
        raise TransitionError(f"evidence root is not a directory: {root}")
    records_by_kind: dict[str, list[tuple[Path, dict[str, str]]]] = {}
    for item in evidence:
        logical = _validate_evidence_path(item.get("path"))
        physical = root.joinpath(*PurePosixPath(logical).parts)
        if physical.is_symlink():
            raise TransitionError(f"evidence symlinks are forbidden: {logical}")
        resolved = physical.resolve(strict=False)
        try:
            common = Path(os.path.commonpath((str(root), str(resolved))))
        except ValueError as exc:
            raise TransitionError(f"evidence escapes root: {logical}") from exc
        if common != root or not physical.is_file():
            raise TransitionError(f"evidence missing or outside root: {logical}")
        actual = sha256_file(physical)
        if actual != item["sha256"]:
            raise TransitionError(
                f"evidence SHA-256 mismatch for {logical}: recorded={item['sha256']}, actual={actual}"
            )
        records_by_kind.setdefault(item["kind"], []).append((physical, item))

    duplicate_kinds = sorted(kind for kind, records in records_by_kind.items() if len(records) > 1)
    if duplicate_kinds:
        raise TransitionError("duplicate evidence kinds are forbidden: " + ", ".join(duplicate_kinds))

    for kind in TARGET_EVIDENCE_KINDS.get(target, frozenset()):
        records = records_by_kind.get(kind, [])
        if len(records) != 1:
            raise TransitionError(
                f"transition to {target} needs exactly one {kind!r} record; found {len(records)}"
            )
        _verify_evidence_semantics(kind, records[0][0])
    if target in {"P1_ORACLE_VALIDATED", "P2_AWAITING_AUTHORIZATION"}:
        _verify_fresh_p1_bundle(root, records_by_kind)
    if target == "P1_FIXTURES_READY":
        _verify_fresh_fixture_bundle(root, records_by_kind)
    if target == "P2_AWAITING_AUTHORIZATION":
        _verify_fresh_readiness(root, records_by_kind)


def _verify_evidence_semantics(kind: str, path: Path) -> None:
    value = load_json(path)
    if kind == "fixture-manifest":
        if not isinstance(value, dict) or value.get("schema_version") != "lr-artifact-manifest/v1":
            raise TransitionError("fixture manifest has the wrong schema")
    elif kind == "p1-gate-report":
        from .gate import validate_gate_report

        errors = validate_gate_report(value)
        if errors or value.get("passed") is not True:
            raise TransitionError(
                "P1 gate evidence is not a valid pass: " + "; ".join(errors or ["passed=false"])
            )
    elif kind == "p1-evidence-manifest":
        if not isinstance(value, dict) or value.get("schema_version") != "lr-artifact-manifest/v1":
            raise TransitionError("P1 evidence manifest has the wrong schema")
    elif kind == "pilot-checkpoint-snapshot":
        from .pilot import verify_checkpoint_snapshot

        if (
            not isinstance(value, dict)
            or value.get("schema_version")
            != "lr-resume-pilot-checkpoint-snapshot/v1"
            or value.get("kind") != "orchestration-only"
            or value.get("not_scientific_evidence") is not True
            or value.get("completed") is not False
        ):
            raise TransitionError("pilot checkpoint snapshot scope guard is missing")
        try:
            verification = verify_checkpoint_snapshot(
                path.parent.parent,
                path,
                require_current=True,
            )
        except (OSError, ValidationError) as exc:
            raise TransitionError(
                f"pilot checkpoint snapshot is not bound to its current plan/results prefix: {exc}"
            ) from exc
        if verification.get("valid") is not True:
            raise TransitionError("pilot checkpoint snapshot verification did not pass")
    elif kind == "pilot-completion":
        from .pilot import verify_pilot

        if (
            not isinstance(value, dict)
            or value.get("schema_version") != "lr-resume-pilot-completion/v1"
            or value.get("may_authorize_p2") is not False
        ):
            raise TransitionError("pilot completion scope guard is missing")
        verify_pilot(path.parent, require_complete=True)
    elif kind == "readiness-report":
        from .readiness import validate_readiness_report

        errors = validate_readiness_report(value)
        if errors or value.get("ready_for_p2_adjudication") is not True:
            raise TransitionError(
                "readiness evidence is not an unblocked adjudication report: "
                + "; ".join(errors or ["ready=false"])
            )
    elif kind == "campaign-state-snapshot":
        validate_state(value)
        if value.get("phase_state") != "PILOT_COMPLETE":
            raise TransitionError("readiness state snapshot must be at PILOT_COMPLETE")


def _verify_fresh_p1_bundle(
    evidence_root: Path,
    records_by_kind: dict[str, list[tuple[Path, dict[str, str]]]],
) -> None:
    """Re-run P1 from its manifested bytes; never trust a standalone pass JSON."""

    from .gate import validate_gate_report, validate_p1_gate

    manifest_path = records_by_kind["p1-evidence-manifest"][0][0]
    report_path = records_by_kind["p1-gate-report"][0][0]
    manifest = load_json(manifest_path)
    recorded_report = load_json(report_path)
    errors = validate_gate_report(recorded_report)
    if errors or recorded_report.get("passed") is not True:
        raise TransitionError(
            "recorded P1 gate report is invalid: " + "; ".join(errors or ["passed=false"])
        )
    fresh = validate_p1_gate(
        evidence_root=evidence_root,
        manifest=manifest,
        checked_at_utc=recorded_report.get("checked_at_utc"),
    )
    if fresh.get("passed") is not True:
        raise TransitionError(f"fresh P1 gate rerun failed: {fresh.get('failures')}")
    if fresh != recorded_report:
        raise TransitionError("recorded P1 report is not byte-semantically equal to a fresh gate rerun")


def _verify_fresh_fixture_bundle(
    evidence_root: Path,
    records_by_kind: dict[str, list[tuple[Path, dict[str, str]]]],
) -> None:
    from .gate import validate_fixture_manifest

    manifest = load_json(records_by_kind["fixture-manifest"][0][0])
    fresh = validate_fixture_manifest(evidence_root=evidence_root, manifest=manifest)
    if fresh.get("passed") is not True:
        raise TransitionError(f"fresh fixed-fixture gate failed: {fresh.get('failures')}")


def _verify_fresh_readiness(
    evidence_root: Path,
    records_by_kind: dict[str, list[tuple[Path, dict[str, str]]]],
) -> None:
    from .readiness import audit_readiness, validate_readiness_report

    report_path = records_by_kind["readiness-report"][0][0]
    report = load_json(report_path)
    errors = validate_readiness_report(report)
    if errors or report.get("ready_for_p2_adjudication") is not True:
        raise TransitionError(
            "recorded readiness report is invalid: "
            + "; ".join(errors or ["ready=false"])
        )
    fresh = audit_readiness(
        repo_root=evidence_root,
        checked_at_utc=report.get("checked_at_utc"),
        probe_tools=True,
        p1_evidence_root=evidence_root,
        p1_manifest_path=records_by_kind["p1-evidence-manifest"][0][0],
        pilot_dir=records_by_kind["pilot-completion"][0][0].parent,
        state_path=records_by_kind["campaign-state-snapshot"][0][0],
    )
    if fresh != report:
        raise TransitionError("recorded readiness report differs from a fresh full audit")
