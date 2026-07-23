"""Command-line entrypoint for the executable orchestration controls."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .atomic import atomic_write_json, load_json
from .canonical import sha256_json
from .errors import ControlError, ValidationError
from .gate import validate_p1_gate
from .manifest import build_manifest, verify_manifest
from .pilot import run_pilot, verify_checkpoint_snapshot, verify_pilot
from .readiness import audit_readiness
from .state import StateLease, StateStore, make_initial_state, validate_state


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _emit(value: Any) -> None:
    print(json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False))


def _write_optional(path: str | None, value: Any) -> None:
    if path:
        atomic_write_json(Path(path), value)


def _cmd_manifest_build(args: argparse.Namespace) -> int:
    specs = load_json(Path(args.spec))
    if not isinstance(specs, list):
        raise ValidationError("manifest spec file must contain a JSON array")
    manifest = build_manifest(
        root=Path(args.root),
        artifact_specs=specs,
        producer={
            "actor": args.actor,
            "writer_id": args.writer_id,
            "tool": "p1.control",
            "tool_version": __version__,
        },
        scope=args.scope,
        created_utc=args.at,
    )
    atomic_write_json(Path(args.out), manifest)
    _emit({"written": args.out, "manifest_sha256": sha256_json(manifest)})
    return 0


def _cmd_manifest_verify(args: argparse.Namespace) -> int:
    result = verify_manifest(Path(args.root), load_json(Path(args.manifest)))
    payload = {
        "valid": result.valid,
        "manifest_sha256": result.manifest_sha256,
        "errors": list(result.errors),
        "artifact_count": len(result.artifacts),
    }
    _emit(payload)
    return 0 if result.valid else 1


def _cmd_gate(args: argparse.Namespace) -> int:
    policy = load_json(Path(args.policy)) if args.policy else None
    report = validate_p1_gate(
        evidence_root=Path(args.root),
        manifest=load_json(Path(args.manifest)),
        checked_at_utc=args.at,
        policy=policy,
    )
    _write_optional(args.out, report)
    _emit(report)
    return 0 if report["passed"] else 1


def _cmd_pilot_run(args: argparse.Namespace) -> int:
    result = run_pilot(Path(args.work_dir), stop_after=args.stop_after)
    _emit(result)
    return 0


def _cmd_pilot_verify(args: argparse.Namespace) -> int:
    result = verify_pilot(Path(args.work_dir), require_complete=not args.allow_partial)
    _emit(result)
    return 0


def _cmd_pilot_verify_snapshot(args: argparse.Namespace) -> int:
    result = verify_checkpoint_snapshot(
        Path(args.work_dir),
        Path(args.snapshot),
        require_current=args.require_current,
    )
    _emit(result)
    return 0


def _cmd_readiness(args: argparse.Namespace) -> int:
    report = audit_readiness(
        repo_root=Path(args.repo_root),
        checked_at_utc=args.at,
        probe_tools=not args.no_probe_tools,
        p1_evidence_root=Path(args.p1_evidence_root) if args.p1_evidence_root else None,
        p1_manifest_path=Path(args.p1_manifest) if args.p1_manifest else None,
        pilot_dir=Path(args.pilot_dir) if args.pilot_dir else None,
        state_path=Path(args.state) if args.state else None,
    )
    _write_optional(args.out, report)
    _emit(report)
    return 0 if report["ready_for_p2_adjudication"] else 1


def _cmd_state_init(args: argparse.Namespace) -> int:
    store = StateStore(Path(args.path))
    state = make_initial_state(
        campaign=args.campaign,
        run_id=args.run_id,
        owner_id=args.owner_id,
        at_utc=args.at,
    )
    with StateLease.acquire(store.lock_path, args.owner_id, args.at) as lease:
        digest = store.initialize(state, lease)
    _emit({"path": args.path, "state": state, "sha256": digest})
    return 0


def _cmd_state_validate(args: argparse.Namespace) -> int:
    state = load_json(Path(args.path))
    validate_state(state)
    _emit({"valid": True, "state": state, "sha256": sha256_json(state)})
    return 0


def _cmd_state_transition(args: argparse.Namespace) -> int:
    evidence = load_json(Path(args.evidence))
    if not isinstance(evidence, list):
        raise ValidationError("transition evidence file must contain a JSON list")
    store = StateStore(Path(args.path))
    with StateLease.acquire(store.lock_path, args.actor_id, args.at) as lease:
        state, digest = store.transition(
            lease=lease,
            expected_revision=args.expected_revision,
            expected_sha256=args.expected_sha256,
            target=args.target,
            actor_role="integrator",
            actor_id=args.actor_id,
            at_utc=args.at,
            reason=args.reason,
            evidence=evidence,
            evidence_root=Path(args.evidence_root),
        )
    _emit({"path": args.path, "state": state, "sha256": digest})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    subcommands = parser.add_subparsers(dest="command", required=True)

    manifest = subcommands.add_parser("manifest", help="build or verify artifact manifests")
    manifest_sub = manifest.add_subparsers(dest="manifest_command", required=True)
    build = manifest_sub.add_parser("build")
    build.add_argument("--root", required=True)
    build.add_argument("--spec", required=True, help="JSON array of logical_path/role/media_type")
    build.add_argument("--out", required=True)
    build.add_argument("--actor", required=True)
    build.add_argument("--writer-id", required=True)
    build.add_argument("--scope", required=True)
    build.add_argument("--at", default=_utc_now())
    build.set_defaults(func=_cmd_manifest_build)
    verify = manifest_sub.add_parser("verify")
    verify.add_argument("--root", required=True)
    verify.add_argument("--manifest", required=True)
    verify.set_defaults(func=_cmd_manifest_verify)

    gate = subcommands.add_parser("gate", help="validate P1 evidence without changing state")
    gate.add_argument("--root", required=True, help="evidence artifact root")
    gate.add_argument("--manifest", required=True)
    gate.add_argument("--policy", help="optional integrator-pinned policy JSON")
    gate.add_argument("--out")
    gate.add_argument("--at", default=_utc_now())
    gate.set_defaults(func=_cmd_gate)

    pilot = subcommands.add_parser("pilot", help="run or verify orchestration-only resume pilot")
    pilot_sub = pilot.add_subparsers(dest="pilot_command", required=True)
    pilot_run = pilot_sub.add_parser("run")
    pilot_run.add_argument("--work-dir", required=True)
    pilot_run.add_argument("--stop-after", type=int)
    pilot_run.set_defaults(func=_cmd_pilot_run)
    pilot_verify = pilot_sub.add_parser("verify")
    pilot_verify.add_argument("--work-dir", required=True)
    pilot_verify.add_argument("--allow-partial", action="store_true")
    pilot_verify.set_defaults(func=_cmd_pilot_verify)
    pilot_snapshot = pilot_sub.add_parser(
        "verify-snapshot",
        help="verify an immutable paused-prefix snapshot, including after completion",
    )
    pilot_snapshot.add_argument("--work-dir", required=True)
    pilot_snapshot.add_argument("--snapshot", required=True)
    pilot_snapshot.add_argument("--require-current", action="store_true")
    pilot_snapshot.set_defaults(func=_cmd_pilot_verify_snapshot)

    readiness = subcommands.add_parser("readiness", help="read-only pre-P2 audit")
    readiness.add_argument("--repo-root", required=True)
    readiness.add_argument("--p1-evidence-root")
    readiness.add_argument("--p1-manifest")
    readiness.add_argument("--pilot-dir")
    readiness.add_argument("--state")
    readiness.add_argument("--no-probe-tools", action="store_true")
    readiness.add_argument("--out")
    readiness.add_argument("--at", default=_utc_now())
    readiness.set_defaults(func=_cmd_readiness)

    state = subcommands.add_parser("state", help="initialize, inspect, or transition state")
    state_sub = state.add_subparsers(dest="state_command", required=True)
    state_init = state_sub.add_parser("init")
    state_init.add_argument("--path", required=True)
    state_init.add_argument("--campaign", default="lr-positivity")
    state_init.add_argument("--run-id", required=True)
    state_init.add_argument("--owner-id", required=True)
    state_init.add_argument("--at", default=_utc_now())
    state_init.set_defaults(func=_cmd_state_init)
    state_validate = state_sub.add_parser("validate")
    state_validate.add_argument("--path", required=True)
    state_validate.set_defaults(func=_cmd_state_validate)
    state_transition = state_sub.add_parser("transition")
    state_transition.add_argument("--path", required=True)
    state_transition.add_argument("--target", required=True)
    state_transition.add_argument("--actor-id", required=True)
    state_transition.add_argument("--expected-revision", type=int, required=True)
    state_transition.add_argument("--expected-sha256", required=True)
    state_transition.add_argument("--reason", required=True)
    state_transition.add_argument("--evidence", required=True)
    state_transition.add_argument(
        "--evidence-root",
        required=True,
        help="repository root against which evidence.path values are resolved",
    )
    state_transition.add_argument("--at", default=_utc_now())
    state_transition.set_defaults(func=_cmd_state_transition)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except (ControlError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
