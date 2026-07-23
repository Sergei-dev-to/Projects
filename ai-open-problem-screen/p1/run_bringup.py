"""Adjudicate P1 and exercise the orchestration-only checkpoint state flow.

This bounded integration driver never starts scientific B0 or P2.  It creates a
fresh campaign state, binds it to the already passing P1 manifest/gate, performs
an intentional toy-pilot stop, transitions through the checkpoint state, resumes
to completion, and emits a compact report.  Existing state or pilot artifacts
are refused so an operator cannot accidentally rewrite prior history.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from p1.control.atomic import atomic_write_json
from p1.control.canonical import sha256_file
from p1.control.pilot import (
    checkpoint_snapshot_path,
    run_pilot,
    verify_checkpoint_snapshot,
    verify_pilot,
)
from p1.control.state import StateLease, StateStore, make_initial_state


OWNER = "codex-root"


def _now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _evidence(repo_root: Path, kind: str, path: Path) -> dict[str, str]:
    resolved = path.resolve()
    logical = resolved.relative_to(repo_root.resolve()).as_posix()
    return {"kind": kind, "path": logical, "sha256": sha256_file(resolved)}


def _transition(
    store: StateStore,
    repo_root: Path,
    target: str,
    reason: str,
    evidence: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    current, digest = store.read()
    at = _now()
    with StateLease.acquire(store.lock_path, OWNER, at) as lease:
        updated, updated_digest = store.transition(
            lease=lease,
            expected_revision=current["revision"],
            expected_sha256=digest,
            target=target,
            actor_role="integrator",
            actor_id=OWNER,
            at_utc=at,
            reason=reason,
            evidence=evidence or [],
            evidence_root=repo_root,
        )
    return {
        "target": target,
        "revision": updated["revision"],
        "state_sha256": updated_digest,
        "at_utc": at,
    }


def run(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    state_path = repo_root / "run" / "state.json"
    pilot_dir = repo_root / "run" / "pilot-resume"
    report_path = repo_root / "run" / "bringup_report.json"
    if state_path.exists() or pilot_dir.exists() or report_path.exists():
        raise FileExistsError(
            "bring-up outputs already exist; validate/resume them explicitly instead of rewriting"
        )

    manifest_path = repo_root / "run" / "p1" / "evidence_manifest.json"
    gate_path = repo_root / "run" / "p1" / "gate_report.json"
    if not manifest_path.is_file() or not gate_path.is_file():
        raise FileNotFoundError("final P1 manifest and gate report are required")

    store = StateStore(state_path)
    initialized_at = _now()
    initial = make_initial_state(
        campaign="lr-positivity",
        run_id="lr-positivity-20260723-bringup",
        owner_id=OWNER,
        at_utc=initialized_at,
    )
    with StateLease.acquire(store.lock_path, OWNER, initialized_at) as lease:
        initial_digest = store.initialize(initial, lease)
    transitions: list[dict[str, Any]] = [
        {
            "target": "P0_READY",
            "revision": 0,
            "state_sha256": initial_digest,
            "at_utc": initialized_at,
        }
    ]

    transitions.append(
        _transition(
            store,
            repo_root,
            "P1_FIXTURES_READY",
            "pinned E1/E2 fixture evidence manifest verified",
            [_evidence(repo_root, "fixture-manifest", manifest_path)],
        )
    )
    transitions.append(
        _transition(
            store,
            repo_root,
            "P1_ORACLE_VALIDATED",
            "hardened P1 gate passed after fresh manifest revalidation",
            [
                _evidence(repo_root, "p1-gate-report", gate_path),
                _evidence(repo_root, "p1-evidence-manifest", manifest_path),
            ],
        )
    )
    transitions.append(
        _transition(
            store,
            repo_root,
            "PILOT_READY",
            "P1 accepted; orchestration-only resume exercise ready",
        )
    )
    transitions.append(
        _transition(
            store,
            repo_root,
            "PILOT_RUNNING",
            "start orchestration-only deterministic resume exercise",
        )
    )

    stopped = run_pilot(pilot_dir, stop_after=3)
    if stopped.get("completed") is not False:
        raise RuntimeError("intentional toy-pilot stop unexpectedly completed")
    snapshot_path = checkpoint_snapshot_path(pilot_dir, stopped["next_index"])
    current_snapshot = verify_checkpoint_snapshot(
        pilot_dir, snapshot_path, require_current=True
    )
    transitions.append(
        _transition(
            store,
            repo_root,
            "PILOT_CHECKPOINTED",
            "intentional stop after three durable toy records",
            [
                _evidence(
                    repo_root,
                    "pilot-checkpoint-snapshot",
                    snapshot_path,
                )
            ],
        )
    )
    transitions.append(
        _transition(
            store,
            repo_root,
            "PILOT_RUNNING",
            "resume from independently verified durable checkpoint prefix",
        )
    )
    resumed = run_pilot(pilot_dir)
    verified = verify_pilot(pilot_dir, require_complete=True)
    historical_snapshot = verify_checkpoint_snapshot(pilot_dir, snapshot_path)
    completion_path = pilot_dir / "completion.json"
    transitions.append(
        _transition(
            store,
            repo_root,
            "PILOT_COMPLETE",
            "resumed toy run is byte-identical to deterministic completion",
            [_evidence(repo_root, "pilot-completion", completion_path)],
        )
    )

    final_state, final_digest = store.read()
    report = {
        "schema_version": "lr-bringup-report/v1",
        "classification": "orchestration-only; not scientific evidence",
        "p1_gate_report_sha256": sha256_file(gate_path),
        "p1_evidence_manifest_sha256": sha256_file(manifest_path),
        "intentional_stop": stopped,
        "checkpoint_snapshot_at_stop": current_snapshot,
        "checkpoint_snapshot_after_completion": historical_snapshot,
        "resumed_completion": resumed,
        "pilot_verification": verified,
        "transitions": transitions,
        "final_phase_state": final_state["phase_state"],
        "final_state_revision": final_state["revision"],
        "final_state_sha256": final_digest,
        "next_action": (
            "run read-only readiness audit and separately authorize bounded B0; "
            "do not infer P2 authorization"
        ),
    }
    atomic_write_json(report_path, report, overwrite=False)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    report = run(args.repo_root)
    print(
        f"state={report['final_phase_state']} revision={report['final_state_revision']} "
        f"pilot_complete={report['pilot_verification']['complete']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
