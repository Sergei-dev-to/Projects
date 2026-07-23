from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from p1.control.atomic import atomic_write_json, load_json
from p1.control.canonical import canonical_fraction, sha256_file, sha256_json
from p1.control.errors import LockError, TransitionError, ValidationError
from p1.control.gate import REQUIRED_GATE_CHECK_CODES, validate_gate_report, validate_p1_gate
from p1.control.manifest import build_manifest, verify_manifest
from p1.control.pilot import (
    checkpoint_snapshot_path,
    run_pilot,
    verify_checkpoint_snapshot,
    verify_pilot,
)
from p1.control.readiness import REQUIRED_SCHEMA_FILES, audit_readiness, validate_readiness_report
from p1.control.state import (
    StateLease,
    StateStore,
    make_initial_state,
    transition_document,
    validate_state,
)


class CanonicalTests(unittest.TestCase):
    def test_fraction_requires_reduced_canonical_spelling(self) -> None:
        self.assertEqual(canonical_fraction("-3/2"), "-3/2")
        self.assertEqual(canonical_fraction("4"), "4")
        for invalid in ("2/2", "+1", "01", "0/4", "1/-2", 1):
            with self.subTest(invalid=invalid), self.assertRaises(ValidationError):
                canonical_fraction(invalid)


class StateTests(unittest.TestCase):
    def _fixture_evidence(self, root: Path) -> list[dict[str, str]]:
        repo = Path(__file__).resolve().parents[3]
        source = repo / "p1" / "e2"
        specs: list[dict[str, str]] = []
        fixed = (
            (source / "fixtures.json", "fixture_definitions.json", "fixture-definition-set", "application/json"),
            (source / "reports" / "fixture_agreement.json", "fixture_agreement.json", "fixture-agreement", "application/json"),
            (source / "reports" / "lrcalc_interp_evaluator.json", "lrcalc_evaluator.json", "fixture-evaluator-lrcalc", "application/json"),
            (source / "reports" / "normaliz_ehrhart_evaluator.json", "normaliz_evaluator.json", "fixture-evaluator-normaliz", "application/json"),
            (source / "reports" / "fixtures_summary.json", "e2_summary.json", "e2-fixture-summary", "application/json"),
            (source / "reports" / "fixtures_summary.sha256", "e2_summary.sha256", "e2-summary-sidecar", "text/plain"),
        )
        for source_path, logical, role, media_type in fixed:
            shutil.copy2(source_path, root / logical)
            specs.append({"logical_path": logical, "role": role, "media_type": media_type})
        for directory, pattern, target_dir, role, media_type in (
            (source / "reports" / "fixtures", "*.report.json", "reports", "fixture-comparison-report", "application/json"),
            (source / "reports" / "inputs", "*.hive.json", "inputs", "explicit-hive-input", "application/json"),
            (source / "reports" / "normaliz", "*.in", "normaliz", "normaliz-input", "text/plain"),
            (source / "reports" / "normaliz", "*.out", "normaliz", "normaliz-raw-output", "text/plain"),
        ):
            (root / target_dir).mkdir(exist_ok=True)
            for source_path in sorted(directory.glob(pattern)):
                logical = f"{target_dir}/{source_path.name}"
                shutil.copy2(source_path, root / logical)
                specs.append({"logical_path": logical, "role": role, "media_type": media_type})
        manifest = build_manifest(
            root=root,
            artifact_specs=specs,
            producer={
                "actor": "integrator",
                "writer_id": "integrator-1",
                "tool": "test",
                "tool_version": "1",
            },
            scope="fixed fixture readiness evidence",
            created_utc="2026-07-23T00:00:00Z",
        )
        manifest_path = root / "fixture-manifest.json"
        atomic_write_json(manifest_path, manifest)
        return [
            {
                "kind": "fixture-manifest",
                "path": "fixture-manifest.json",
                "sha256": sha256_file(manifest_path),
            }
        ]

    def test_lock_cas_and_allowed_transition(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "state.json"
            store = StateStore(path)
            state = make_initial_state(
                campaign="lr-positivity",
                run_id="run-test",
                owner_id="integrator-1",
                at_utc="2026-07-23T00:00:00Z",
            )
            with StateLease.acquire(
                store.lock_path, "integrator-1", "2026-07-23T00:00:00Z"
            ) as lease:
                with self.assertRaises(LockError):
                    StateLease.acquire(
                        store.lock_path, "integrator-1", "2026-07-23T00:00:01Z"
                    )
                initial_digest = store.initialize(state, lease)
            current, digest = store.read()
            self.assertEqual(digest, initial_digest)
            evidence = self._fixture_evidence(Path(raw))
            with StateLease.acquire(
                store.lock_path, "integrator-1", "2026-07-23T00:01:00Z"
            ) as lease:
                updated, updated_digest = store.transition(
                    lease=lease,
                    expected_revision=0,
                    expected_sha256=digest,
                    target="P1_FIXTURES_READY",
                    actor_role="integrator",
                    actor_id="integrator-1",
                    at_utc="2026-07-23T00:01:00Z",
                    reason="fixture evidence reviewed",
                    evidence=evidence,
                    evidence_root=Path(raw),
                )
            self.assertEqual(updated["revision"], 1)
            self.assertEqual(updated["phase_state"], "P1_FIXTURES_READY")
            self.assertEqual(updated["previous_document_sha256"], digest)
            self.assertEqual(store.read()[1], updated_digest)

            with StateLease.acquire(
                store.lock_path, "integrator-1", "2026-07-23T00:02:00Z"
            ) as lease, self.assertRaises(TransitionError):
                store.transition(
                    lease=lease,
                    expected_revision=0,
                    expected_sha256=digest,
                    target="P1_ORACLE_VALIDATED",
                    actor_role="integrator",
                    actor_id="integrator-1",
                    at_utc="2026-07-23T00:02:00Z",
                    reason="stale attempt",
                    evidence=evidence,
                    evidence_root=Path(raw),
                )

    def test_state_cannot_skip_gate_or_be_written_by_runner(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "state.json"
            store = StateStore(path)
            state = make_initial_state(
                campaign="lr-positivity",
                run_id="run-test",
                owner_id="integrator-1",
                at_utc="2026-07-23T00:00:00Z",
            )
            with StateLease.acquire(store.lock_path, "integrator-1", "t0") as lease:
                digest = store.initialize(state, lease)
            evidence = self._fixture_evidence(Path(raw))
            with StateLease.acquire(store.lock_path, "runner-1", "t1") as lease:
                with self.assertRaises(TransitionError):
                    store.transition(
                        lease=lease,
                        expected_revision=0,
                        expected_sha256=digest,
                        target="P1_FIXTURES_READY",
                        actor_role="runner",
                        actor_id="runner-1",
                        at_utc="t1",
                        reason="invalid",
                        evidence=evidence,
                        evidence_root=Path(raw),
                    )

    def test_forged_checkpoint_snapshot_without_plan_or_results_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            state = make_initial_state(
                campaign="lr-positivity",
                run_id="run-test",
                owner_id="integrator-1",
                at_utc="t0",
            )
            prior_evidence = {
                "P1_FIXTURES_READY": [
                    {"kind": "fixture-manifest", "path": "old-fixtures.json", "sha256": "1" * 64}
                ],
                "P1_ORACLE_VALIDATED": [
                    {"kind": "p1-gate-report", "path": "old-gate.json", "sha256": "2" * 64},
                    {"kind": "p1-evidence-manifest", "path": "old-manifest.json", "sha256": "3" * 64},
                ],
                "PILOT_READY": [],
                "PILOT_RUNNING": [],
            }
            for index, target in enumerate(prior_evidence, start=1):
                state = transition_document(
                    state,
                    target=target,
                    actor_role="integrator",
                    actor_id="integrator-1",
                    at_utc=f"t{index}",
                    reason="test setup",
                    evidence=prior_evidence[target],
                )
            state_path = root / "state.json"
            atomic_write_json(state_path, state)
            forged = {
                "schema_version": "lr-resume-pilot-checkpoint-snapshot/v1",
                "kind": "orchestration-only",
                "not_scientific_evidence": True,
                "plan_sha256": "a" * 64,
                "next_index": 3,
                "total": 10,
                "prefix_sha256": "b" * 64,
                "completed": False,
                "checkpoint_sha256": "c" * 64,
            }
            snapshot = root / "pilot" / "checkpoint-snapshots" / "000003.json"
            snapshot.parent.mkdir(parents=True)
            atomic_write_json(snapshot, forged)
            evidence = [
                {
                    "kind": "pilot-checkpoint-snapshot",
                    "path": "pilot/checkpoint-snapshots/000003.json",
                    "sha256": sha256_file(snapshot),
                }
            ]
            store = StateStore(state_path)
            _, digest = store.read()
            with StateLease.acquire(store.lock_path, "integrator-1", "t5") as lease:
                with self.assertRaises((TransitionError, ValidationError)):
                    store.transition(
                        lease=lease,
                        expected_revision=state["revision"],
                        expected_sha256=digest,
                        target="PILOT_CHECKPOINTED",
                        actor_role="integrator",
                        actor_id="integrator-1",
                        at_utc="t5",
                        reason="forged checkpoint",
                        evidence=evidence,
                        evidence_root=root,
                    )

    def test_state_records_immutable_checkpoint_snapshot_not_mutable_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            state = make_initial_state(
                campaign="lr-positivity", run_id="run-test", owner_id="integrator-1", at_utc="t0"
            )
            prior_evidence = {
                "P1_FIXTURES_READY": [
                    {"kind": "fixture-manifest", "path": "old-fixtures.json", "sha256": "1" * 64}
                ],
                "P1_ORACLE_VALIDATED": [
                    {"kind": "p1-gate-report", "path": "old-gate.json", "sha256": "2" * 64},
                    {"kind": "p1-evidence-manifest", "path": "old-manifest.json", "sha256": "3" * 64},
                ],
                "PILOT_READY": [],
                "PILOT_RUNNING": [],
            }
            for index, target in enumerate(prior_evidence, start=1):
                state = transition_document(
                    state,
                    target=target,
                    actor_role="integrator",
                    actor_id="integrator-1",
                    at_utc=f"t{index}",
                    reason="test setup",
                    evidence=prior_evidence[target],
                )
            state_path = root / "state.json"
            atomic_write_json(state_path, state)

            pilot_dir = root / "pilot"
            run_pilot(pilot_dir, stop_after=3)
            snapshot = checkpoint_snapshot_path(pilot_dir, 3)
            evidence = [
                {
                    "kind": "pilot-checkpoint-snapshot",
                    "path": "pilot/checkpoint-snapshots/000003.json",
                    "sha256": sha256_file(snapshot),
                }
            ]
            store = StateStore(state_path)
            _, digest = store.read()
            with StateLease.acquire(store.lock_path, "integrator-1", "t5") as lease:
                updated, _ = store.transition(
                    lease=lease,
                    expected_revision=state["revision"],
                    expected_sha256=digest,
                    target="PILOT_CHECKPOINTED",
                    actor_role="integrator",
                    actor_id="integrator-1",
                    at_utc="t5",
                    reason="durable paused prefix",
                    evidence=evidence,
                    evidence_root=root,
                )
            self.assertEqual(
                updated["last_transition"]["evidence"][0]["kind"],
                "pilot-checkpoint-snapshot",
            )

            run_pilot(pilot_dir)
            self.assertTrue(verify_checkpoint_snapshot(pilot_dir, snapshot)["historical"])

    def test_standalone_forged_p1_pass_is_rechecked_against_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            state = make_initial_state(
                campaign="lr-positivity", run_id="r", owner_id="i", at_utc="t0"
            )
            state = transition_document(
                state,
                target="P1_FIXTURES_READY",
                actor_role="integrator",
                actor_id="i",
                at_utc="t1",
                reason="synthetic prior state",
                evidence=[
                    {"kind": "fixture-manifest", "path": "prior.json", "sha256": "4" * 64}
                ],
            )
            state_path = root / "state.json"
            atomic_write_json(state_path, state)
            payload = root / "payload.txt"
            payload.write_text("not scientific evidence", encoding="utf-8")
            manifest = build_manifest(
                root=root,
                artifact_specs=[{"logical_path": "payload.txt", "role": "fake", "media_type": "text/plain"}],
                producer={"actor": "x", "writer_id": "x", "tool": "x", "tool_version": "1"},
                scope="forgery",
                created_utc="t",
            )
            manifest_path = root / "manifest.json"
            atomic_write_json(manifest_path, manifest)
            forged_report = {
                "schema_version": "lr-p1-gate-report/v1",
                "gate_id": "P1",
                "passed": True,
                "checked_at_utc": "t",
                "policy_sha256": "a" * 64,
                "evidence_manifest_sha256": sha256_json(manifest),
                "checks": [
                    {"code": code, "passed": True, "detail": "forged"}
                    for code in sorted(REQUIRED_GATE_CHECK_CODES)
                ],
                "failures": [],
                "next_action": "forged",
            }
            self.assertEqual(validate_gate_report(forged_report), [])
            report_path = root / "gate.json"
            atomic_write_json(report_path, forged_report)
            evidence = [
                {"kind": "p1-gate-report", "path": "gate.json", "sha256": sha256_file(report_path)},
                {"kind": "p1-evidence-manifest", "path": "manifest.json", "sha256": sha256_file(manifest_path)},
            ]
            store = StateStore(state_path)
            _, digest = store.read()
            with StateLease.acquire(store.lock_path, "i", "t2") as lease:
                with self.assertRaises(TransitionError):
                    store.transition(
                        lease=lease,
                        expected_revision=1,
                        expected_sha256=digest,
                        target="P1_ORACLE_VALIDATED",
                        actor_role="integrator",
                        actor_id="i",
                        at_utc="t2",
                        reason="attempt forged pass",
                        evidence=evidence,
                        evidence_root=root,
                    )

    def test_high_revision_without_full_history_is_invalid(self) -> None:
        state = make_initial_state(
            campaign="lr-positivity", run_id="r", owner_id="i", at_utc="t0"
        )
        state["revision"] = 99
        with self.assertRaises(ValidationError):
            validate_state(state)


class ManifestTests(unittest.TestCase):
    def test_manifest_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            artifact = root / "result.txt"
            artifact.write_text("exact output\n", encoding="utf-8")
            manifest = build_manifest(
                root=root,
                artifact_specs=[
                    {"logical_path": "result.txt", "role": "raw-output", "media_type": "text/plain"}
                ],
                producer={
                    "actor": "runner",
                    "writer_id": "runner-1",
                    "tool": "test",
                    "tool_version": "1",
                },
                scope="test",
                created_utc="2026-07-23T00:00:00Z",
            )
            self.assertTrue(verify_manifest(root, manifest).valid)
            artifact.write_text("tampered\n", encoding="utf-8")
            result = verify_manifest(root, manifest)
            self.assertFalse(result.valid)
            self.assertTrue(any("mismatch" in error for error in result.errors))

    def test_manifest_rejects_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            with self.assertRaises(ValidationError):
                build_manifest(
                    root=Path(raw),
                    artifact_specs=[{"logical_path": "../escape", "role": "x"}],
                    producer={"actor": "a", "writer_id": "w", "tool": "t", "tool_version": "1"},
                    scope="test",
                    created_utc="t",
                )


class GateTests(unittest.TestCase):
    def _legacy_evidence(
        self,
        root: Path,
        *,
        disagree: bool = False,
        omit_e1: bool = False,
        fail_e1: bool = False,
        swap_evaluator_roles: bool = False,
        arbitrary_evaluator: bool = False,
    ):
        triples = [{"lam": [], "mu": [], "nu": [], "poly": ["1"]}]
        payload_hash = sha256_json(triples)
        baseline = {
            "meta": {
                "scope": {"max_length": 1, "max_size": 0},
                "canonicalization": "swap-only test",
            },
            "sha256": payload_hash,
            "triples": triples,
        }
        atomic_write_json(root / "baseline.json", baseline)
        mismatch = {
            "gate": "P1_E1_BASELINE_PARITY",
            "items": [] if not fail_e1 else [{"id": "forced-failure"}],
            "schema_version": 1,
            "status": "empty" if not fail_e1 else "nonempty",
        }
        atomic_write_json(root / "mismatches.json", mismatch)
        parity = {
            "actual": {"record_count": 1, "triples_payload_sha256": payload_hash},
            "anchors": [
                {"id": "asymmetric-raw-order-positive", "actual": 1, "expected": 1, "pass": True},
                {"id": "rotated-raw-order-is-zero", "actual": 0, "expected": 0, "pass": True},
                {"id": "documented-order-known-two", "actual": 2, "expected": 2, "pass": True},
                {"id": "empty-partition-normalization", "actual": 1, "expected": 1, "pass": True},
                {
                    "id": "campaign-degree-six-polynomial",
                    "actual": ["1", "13/4", "37/8", "4", "9/4", "3/4", "1/8"],
                    "expected": ["1", "13/4", "37/8", "4", "9/4", "3/4", "1/8"],
                    "pass": True,
                },
            ],
            "baseline_integrity": {
                "embedded_payload_sha256": payload_hash,
                "errors": [],
                "record_count": 1,
                "sidecar_payload_sha256": payload_hash,
                "status": "pass",
                "triples_payload_sha256": payload_hash,
            },
            "canonicalization": {
                "name": "order-2 swap-only",
                "sort": "(len(nu), nu, lam, mu)",
                "version": "swap-only-v1",
            },
            "comparison": {
                "anchor_failures": 0,
                "baseline_integrity_errors": 0,
                "evaluation_errors": 0,
                "extra_triples": 0,
                "mismatch_bundle": "mismatches.json",
                "missing_triples": 0,
                "polynomial_mismatches": 1 if fail_e1 else 0,
            },
            "enumeration": {"nonzero_triple_count": 1, "structural_candidate_count": 1},
            "evaluator": {
                "interpolation_mode": "adaptive",
                "lrcalc_version": "2.1",
                "name": "lrcalc-interp",
            },
            "expected": {
                "record_count": 1,
                "scope": {"max_length": 1, "max_size": 0},
                "triples_payload_sha256": payload_hash,
            },
            "gate": "P1_E1_BASELINE_PARITY",
            "schema_version": 1,
            "status": "fail" if fail_e1 else "pass",
            "workers": 1,
        }
        atomic_write_json(root / "parity_report.json", parity)
        frontier = {
            "canonicalization": parity["canonicalization"],
            "gate": "P1_E1_BASELINE_PARITY",
            "record_count": len(triples),
            "schema_version": 1,
            "triples": triples,
            "triples_payload_sha256": payload_hash,
        }
        atomic_write_json(root / "actual_frontier.json", frontier)
        internal = {
            "artifacts": [
                {
                    "bytes": (root / "actual_frontier.json").stat().st_size,
                    "path": "actual_frontier.json",
                    "sha256": sha256_file(root / "actual_frontier.json"),
                },
                {
                    "bytes": (root / "parity_report.json").stat().st_size,
                    "path": "parity_report.json",
                    "sha256": sha256_file(root / "parity_report.json"),
                },
                {
                    "bytes": (root / "mismatches.json").stat().st_size,
                    "path": "mismatches.json",
                    "sha256": sha256_file(root / "mismatches.json"),
                },
            ],
            "gate": "P1_E1_BASELINE_PARITY",
            "schema_version": 1,
        }
        atomic_write_json(root / "e1_internal_manifest.json", internal)

        fixtures = []
        lrcalc_fixtures = []
        normaliz_fixtures = []
        for index in range(2):
            fixture_id = f"fixture-{index}"
            lrcalc_fixtures.append(
                {
                    "degree_bound": 1,
                    "id": fixture_id,
                    "poly": ["1", "2"],
                    "samples": {"1": 3, "2": 5},
                    "verified": True,
                }
            )
            normaliz_fixtures.append(
                {
                    "affine_dimension": 1,
                    "id": fixture_id,
                    "number_lattice_points": 3,
                    "period_collapses_to_one": True,
                    "poly": ["1", "2"] if not disagree or index == 0 else ["1", "3"],
                }
            )
        lrcalc_document = {
            "evaluator": "lrcalc-interp",
            "fixtures": lrcalc_fixtures,
            "method": "positive-stretch exact lrcalc counts",
            "schema_version": "lr-p1-lrcalc-fixture-evaluator/v1",
        }
        normaliz_document = {
            "evaluator": "normaliz-ehrhart",
            "fixtures": normaliz_fixtures,
            "method": "explicit hive plus exact Normaliz Ehrhart",
            "schema_version": "lr-p1-normaliz-fixture-evaluator/v1",
        }
        if arbitrary_evaluator:
            lrcalc_document = {"evaluator": "lrcalc-interp", "fixtures": [], "forged": True}
        atomic_write_json(root / "lrcalc_evaluator.json", lrcalc_document)
        atomic_write_json(root / "normaliz_evaluator.json", normaliz_document)
        lrcalc_hash = sha256_file(root / "lrcalc_evaluator.json")
        normaliz_hash = sha256_file(root / "normaliz_evaluator.json")
        for index in range(2):
            second_poly = ["1", "2"] if not disagree or index else ["1", "3"]
            fixtures.append(
                {
                    "id": f"fixture-{index}",
                    "coverage": ["coverage-a"] if index == 0 else ["coverage-b"],
                    "evaluators": [
                        {
                            "name": "lrcalc-interp",
                            "poly": ["1", "2"],
                            "artifact_sha256": lrcalc_hash,
                        },
                        {
                            "name": "normaliz-ehrhart",
                            "poly": second_poly,
                            "artifact_sha256": normaliz_hash,
                        },
                    ],
                    "agreement": not (disagree and index == 1),
                }
            )
        fixture_report = {
            "schema_version": "lr-p1-fixture-agreement/v1",
            "fixture_count": len(fixtures),
            "all_agree": not disagree,
            "fixtures": fixtures,
        }
        atomic_write_json(root / "fixtures.json", fixture_report)
        specs = [
            {"logical_path": "baseline.json", "role": "baseline-frontier", "media_type": "application/json"},
            {"logical_path": "fixtures.json", "role": "fixture-agreement", "media_type": "application/json"},
            {
                "logical_path": "lrcalc_evaluator.json",
                "role": "fixture-evaluator-normaliz"
                if swap_evaluator_roles
                else "fixture-evaluator-lrcalc",
                "media_type": "application/json",
            },
            {
                "logical_path": "normaliz_evaluator.json",
                "role": "fixture-evaluator-lrcalc"
                if swap_evaluator_roles
                else "fixture-evaluator-normaliz",
                "media_type": "application/json",
            },
        ]
        if not omit_e1:
            specs.extend(
                [
                    {"logical_path": "parity_report.json", "role": "e1-parity-report", "media_type": "application/json"},
                    {"logical_path": "actual_frontier.json", "role": "e1-frontier-payload", "media_type": "application/json"},
                    {"logical_path": "mismatches.json", "role": "e1-mismatch-bundle", "media_type": "application/json"},
                    {"logical_path": "e1_internal_manifest.json", "role": "e1-artifact-manifest", "media_type": "application/json"},
                ]
            )
        manifest = build_manifest(
            root=root,
            artifact_specs=specs,
            producer={"actor": "runner", "writer_id": "r1", "tool": "test", "tool_version": "1"},
            scope="test P1",
            created_utc="2026-07-23T00:00:00Z",
        )
        policy = {
            "schema_version": "lr-p1-gate-policy/v1",
            "gate_id": "P1",
            "baseline": {
                "triples_payload_sha256": payload_hash,
                "count": 1,
                "scope": {"max_length": 1, "max_size": 0},
                "canonicalization_token": "swap-only",
            },
            "e1": {
                "schema_version": 1,
                "gate": "P1_E1_BASELINE_PARITY",
                "evaluator_name": "lrcalc-interp",
                "canonicalizer_version": "swap-only-v1",
                "allowed_interpolation_modes": ["adaptive", "conservative"],
                "zero_comparison_fields": [
                    "anchor_failures",
                    "baseline_integrity_errors",
                    "evaluation_errors",
                    "extra_triples",
                    "missing_triples",
                    "polynomial_mismatches",
                ],
                "required_anchors": {
                    "asymmetric-raw-order-positive": 1,
                    "rotated-raw-order-is-zero": 0,
                    "documented-order-known-two": 2,
                    "empty-partition-normalization": 1,
                    "campaign-degree-six-polynomial": [
                        "1",
                        "13/4",
                        "37/8",
                        "4",
                        "9/4",
                        "3/4",
                        "1/8",
                    ],
                },
            },
            "fixtures": {
                "min_count": 2,
                "evaluator_names": ["lrcalc-interp", "normaliz-ehrhart"],
                "required_coverage": ["coverage-a", "coverage-b"],
            },
        }
        return manifest, policy

    def _evidence(
        self,
        root: Path,
        *,
        disagree: bool = False,
        omit_e1: bool = False,
        fail_e1: bool = False,
        swap_evaluator_roles: bool = False,
        arbitrary_evaluator: bool = False,
        normaliz_count_forgery: bool = False,
    ):
        _, policy = self._legacy_evidence(root)
        parity = load_json(root / "parity_report.json")
        parity["evaluator"]["python"] = "3.12.3"
        if fail_e1:
            parity["status"] = "fail"
            parity["comparison"]["polynomial_mismatches"] = 1
            mismatch = load_json(root / "mismatches.json")
            mismatch["status"] = "mismatches"
            mismatch["items"] = [{"kind": "forced-failure"}]
            atomic_write_json(root / "mismatches.json", mismatch)
        atomic_write_json(root / "parity_report.json", parity)
        internal = {
            "artifacts": [
                {
                    "bytes": (root / name).stat().st_size,
                    "path": name,
                    "sha256": sha256_file(root / name),
                }
                for name in ("actual_frontier.json", "parity_report.json", "mismatches.json")
            ],
            "gate": "P1_E1_BASELINE_PARITY",
            "schema_version": 1,
        }
        atomic_write_json(root / "e1_internal_manifest.json", internal)

        for directory in ("reports", "inputs", "normaliz"):
            (root / directory).mkdir(exist_ok=True)
        definitions: list[dict] = []
        lrcalc_records: list[dict] = []
        normaliz_records: list[dict] = []
        report_ledger: list[dict] = []
        extra_specs: list[dict[str, str]] = []
        for index in range(2):
            fixture_id = f"fixture-{index}"
            definition = {
                "description": f"fixed test fixture {index}",
                "expected_affine_dimension": 1,
                "expected_lr_at_1": 3,
                "expected_polynomial": ["1", "2"],
                "id": fixture_id,
                "lam": [1],
                "mu": [1],
                "n": 2,
                "nu": [2],
            }
            definitions.append(definition)
            input_doc = {
                "schema_version": 1,
                "n": 2,
                "lam": [1],
                "mu": [1],
                "nu": [2],
                "normaliz": {"rows": [[1, 0]]},
            }
            input_path = root / "inputs" / f"{fixture_id}.hive.json"
            atomic_write_json(input_path, input_doc)
            in_path = root / "normaliz" / f"{fixture_id}.in"
            out_path = root / "normaliz" / f"{fixture_id}.out"
            in_path.write_text("amb_space 1\n", encoding="utf-8")
            out_path.write_text(f"Normaliz {fixture_id}\n", encoding="utf-8")
            changed = disagree and index == 1
            normaliz_poly = ["1", "3"] if changed else ["1", "2"]
            raw_quasi = [[1, 3], 1] if changed else [[1, 2], 1]
            count = 4 if changed else 3
            lrcalc_records.append(
                {
                    "degree_bound": 1,
                    "id": fixture_id,
                    "poly": ["1", "2"],
                    "samples": {"1": 3, "2": 5, "3": 7},
                    "verified": True,
                }
            )
            normaliz_records.append(
                {
                    "affine_dimension": 1,
                    "id": fixture_id,
                    "input_canonical_payload_sha256": sha256_json(input_doc),
                    "normaliz_cli_output_sha256": sha256_file(out_path),
                    "number_lattice_points": 999
                    if normaliz_count_forgery and index == 0
                    else count,
                    "period_collapses_to_one": True,
                    "poly": normaliz_poly,
                    "raw_ehrhart_quasipolynomial": [[999], 1]
                    if normaliz_count_forgery and index == 0
                    else raw_quasi,
                    "raw_ehrhart_series": [[1], [1, 1], 0],
                }
            )
            comparison = {
                "schema_version": 1,
                "fixture": definition,
                "input_artifact": {
                    "path": str(input_path),
                    "file_sha256": sha256_file(input_path),
                    "canonical_payload_sha256": sha256_json(input_doc),
                    "normaliz_input_path": str(in_path),
                },
                "one_variable_audit": None,
                "e2_normaliz": {
                    "affine_dimension": 1,
                    "canonical_polynomial": normaliz_poly,
                    "ehrhart_quasipolynomial_raw": raw_quasi,
                    "ehrhart_series_raw": [[1], [1, 1], 0],
                    "empty": False,
                    "number_lattice_points": count,
                    "period_collapses_to_one": True,
                    "raw_period": 1,
                },
                "e1_lrcalc_interp": {
                    "degree_bound": 1,
                    "interpolation_domain": [1, 2],
                    "reserved_check_domain": [3, 3],
                    "samples": {"1": 3, "2": 5},
                    "canonical_polynomial": ["1", "2"],
                    "all_available_samples_verified": True,
                },
                "e1_lrcalc_positive_stretches": {"1": 3, "2": 5, "3": 7},
                "expected_positive_stretches": {"1": 3, "2": 5, "3": 7},
                "normaliz_cli": {
                    "exit": 0,
                    "output_present": True,
                    "output_path": str(out_path),
                    "output_sha256": sha256_file(out_path),
                },
                "checks": [
                    {
                        "actual": normaliz_poly,
                        "expected": ["1", "2"],
                        "name": "fixture polynomial",
                        "pass": not changed,
                    }
                ],
                "pass": not changed,
                "report_path": str(root / "reports" / f"{fixture_id}.report.json"),
            }
            report_path = root / "reports" / f"{fixture_id}.report.json"
            atomic_write_json(report_path, comparison)
            report_ledger.append(
                {
                    "id": fixture_id,
                    "pass": not changed,
                    "report_path": str(report_path),
                    "report_sha256": sha256_file(report_path),
                    "exception": None,
                }
            )
            extra_specs.extend(
                [
                    {"logical_path": f"reports/{fixture_id}.report.json", "role": "fixture-comparison-report", "media_type": "application/json"},
                    {"logical_path": f"inputs/{fixture_id}.hive.json", "role": "explicit-hive-input", "media_type": "application/json"},
                    {"logical_path": f"normaliz/{fixture_id}.in", "role": "normaliz-input", "media_type": "text/plain"},
                    {"logical_path": f"normaliz/{fixture_id}.out", "role": "normaliz-raw-output", "media_type": "text/plain"},
                ]
            )
        definition_doc = {"schema_version": 1, "fixtures": definitions}
        atomic_write_json(root / "fixture_definitions.json", definition_doc)
        lrcalc_doc = {
            "evaluator": "lrcalc-interp",
            "fixtures": lrcalc_records,
            "method": "positive-stretch exact lrcalc counts",
            "schema_version": "lr-p1-lrcalc-fixture-evaluator/v1",
        }
        if arbitrary_evaluator:
            lrcalc_doc = {"evaluator": "lrcalc-interp", "fixtures": [], "forged": True}
        normaliz_doc = {
            "evaluator": "normaliz-ehrhart",
            "fixtures": normaliz_records,
            "method": "explicit hive plus exact Normaliz Ehrhart",
            "schema_version": "lr-p1-normaliz-fixture-evaluator/v1",
        }
        atomic_write_json(root / "lrcalc_evaluator.json", lrcalc_doc)
        atomic_write_json(root / "normaliz_evaluator.json", normaliz_doc)
        lrcalc_hash = sha256_file(root / "lrcalc_evaluator.json")
        normaliz_hash = sha256_file(root / "normaliz_evaluator.json")
        coverage = [
            "boundary.lambda",
            "boundary.mu",
            "boundary.nu",
            "coefficient.multiple",
            "dimension.positive",
            "rhombus.type-a",
            "rhombus.type-b",
            "rhombus.type-c",
        ]
        agreement = {
            "schema_version": "lr-p1-fixture-agreement/v1",
            "fixture_count": 2,
            "all_agree": not disagree,
            "fixtures": [
                {
                    "id": f"fixture-{index}",
                    "coverage": coverage,
                    "evaluators": [
                        {"name": "lrcalc-interp", "poly": ["1", "2"], "artifact_sha256": lrcalc_hash},
                        {"name": "normaliz-ehrhart", "poly": ["1", "3"] if disagree and index == 1 else ["1", "2"], "artifact_sha256": normaliz_hash},
                    ],
                    "agreement": not (disagree and index == 1),
                }
                for index in range(2)
            ],
        }
        atomic_write_json(root / "fixtures.json", agreement)
        summary_core = {
            "schema_version": 1,
            "gate": "E2 fixed hive fixtures",
            "tool_versions": {"python": "3.12.3", "lrcalc": "2.1", "pynormaliz": "2.19", "normaliz": "Normaliz 3.10.2"},
            "fixture_count": 2,
            "passed": 1 if disagree else 2,
            "failed": 1 if disagree else 0,
            "all_pass": not disagree,
            "controller_adapter": {
                "all_agree": not disagree,
                "fixture_agreement_sha256": sha256_file(root / "fixtures.json"),
                "lrcalc_evaluator_sha256": lrcalc_hash,
                "normaliz_evaluator_sha256": normaliz_hash,
            },
            "reports": report_ledger,
        }
        summary = {**summary_core, "canonical_payload_sha256": sha256_json(summary_core)}
        atomic_write_json(root / "e2_summary.json", summary)
        (root / "e2_summary.sha256").write_text(
            f"{summary['canonical_payload_sha256']}  e2_summary.json:summary_core\n",
            encoding="utf-8",
        )
        specs = [
            {"logical_path": "baseline.json", "role": "baseline-frontier", "media_type": "application/json"},
            {"logical_path": "fixtures.json", "role": "fixture-agreement", "media_type": "application/json"},
            {"logical_path": "fixture_definitions.json", "role": "fixture-definition-set", "media_type": "application/json"},
            {"logical_path": "e2_summary.json", "role": "e2-fixture-summary", "media_type": "application/json"},
            {"logical_path": "e2_summary.sha256", "role": "e2-summary-sidecar", "media_type": "text/plain"},
            {"logical_path": "lrcalc_evaluator.json", "role": "fixture-evaluator-normaliz" if swap_evaluator_roles else "fixture-evaluator-lrcalc", "media_type": "application/json"},
            {"logical_path": "normaliz_evaluator.json", "role": "fixture-evaluator-lrcalc" if swap_evaluator_roles else "fixture-evaluator-normaliz", "media_type": "application/json"},
            *extra_specs,
        ]
        if not omit_e1:
            specs.extend(
                [
                    {"logical_path": "parity_report.json", "role": "e1-parity-report", "media_type": "application/json"},
                    {"logical_path": "actual_frontier.json", "role": "e1-frontier-payload", "media_type": "application/json"},
                    {"logical_path": "mismatches.json", "role": "e1-mismatch-bundle", "media_type": "application/json"},
                    {"logical_path": "e1_internal_manifest.json", "role": "e1-artifact-manifest", "media_type": "application/json"},
                ]
            )
        manifest = build_manifest(
            root=root,
            artifact_specs=specs,
            producer={"actor": "runner", "writer_id": "r1", "tool": "test", "tool_version": "1"},
            scope="test P1",
            created_utc="2026-07-23T00:00:00Z",
        )
        policy["tools"] = summary_core["tool_versions"]
        policy["fixtures"] = {
            "min_count": 2,
            "definition_file_sha256": sha256_file(root / "fixture_definitions.json"),
            "evaluator_names": ["lrcalc-interp", "normaliz-ehrhart"],
            "required_coverage": ["boundary.lambda", "coefficient.multiple", "dimension.positive"],
        }
        return manifest, policy

    def test_gate_passes_only_complete_exact_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            manifest, policy = self._evidence(root)
            report = validate_p1_gate(
                evidence_root=root,
                manifest=manifest,
                checked_at_utc="2026-07-23T00:00:00Z",
                policy=policy,
            )
            self.assertTrue(report["passed"], report["failures"])
            self.assertEqual(validate_gate_report(report), [])

    def test_gate_fails_on_disagreement_and_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            manifest, policy = self._evidence(root, disagree=True)
            report = validate_p1_gate(
                evidence_root=root,
                manifest=manifest,
                checked_at_utc="t",
                policy=policy,
            )
            self.assertFalse(report["passed"])
            self.assertTrue(any(item["code"].startswith("P1.FIXTURE") for item in report["failures"]))
            (root / "parity_report.json").write_text("changed", encoding="utf-8")
            tampered = validate_p1_gate(
                evidence_root=root,
                manifest=manifest,
                checked_at_utc="t",
                policy=policy,
            )
            self.assertFalse(tampered["passed"])
            self.assertTrue(any(item["code"] == "P1.MANIFEST" for item in tampered["failures"]))

    def test_gate_rejects_missing_or_failing_e1(self) -> None:
        for label, options in (
            ("missing", {"omit_e1": True}),
            ("failing", {"fail_e1": True}),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                manifest, policy = self._evidence(root, **options)
                report = validate_p1_gate(
                    evidence_root=root,
                    manifest=manifest,
                    checked_at_utc="t",
                    policy=policy,
                )
                self.assertFalse(report["passed"])
                self.assertTrue(
                    any(item["code"].startswith("P1.E1") for item in report["failures"]),
                    report["failures"],
                )

    def test_gate_rejects_swapped_or_arbitrary_evaluator_artifacts(self) -> None:
        for label, options in (
            ("swapped", {"swap_evaluator_roles": True}),
            ("arbitrary", {"arbitrary_evaluator": True}),
            ("normaliz-999-forgery", {"normaliz_count_forgery": True}),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as raw:
                root = Path(raw)
                manifest, policy = self._evidence(root, **options)
                report = validate_p1_gate(
                    evidence_root=root,
                    manifest=manifest,
                    checked_at_utc="t",
                    policy=policy,
                )
                self.assertFalse(report["passed"])
                self.assertTrue(
                    any(
                        item["code"]
                        in {"P1.FIXTURE_LRCALC_ARTIFACT", "P1.FIXTURE_NORMALIZ_ARTIFACT"}
                        for item in report["failures"]
                    ),
                    report["failures"],
                )

    def test_gate_report_validator_rejects_forged_pass(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            manifest, policy = self._evidence(root)
            report = validate_p1_gate(
                evidence_root=root,
                manifest=manifest,
                checked_at_utc="t",
                policy=policy,
            )
            forged = dict(report)
            forged["checks"] = [
                {"code": "P1.POLICY", "passed": True, "detail": "trust me"}
            ]
            self.assertTrue(validate_gate_report(forged))
            forged = json.loads(json.dumps(report))
            forged["checks"][0]["passed"] = False
            self.assertTrue(validate_gate_report(forged))
            for field, invalid in (
                ("checked_at_utc", None),
                ("checked_at_utc", "  "),
                ("next_action", None),
                ("next_action", ""),
            ):
                with self.subTest(field=field, invalid=invalid):
                    forged = json.loads(json.dumps(report))
                    forged[field] = invalid
                    self.assertTrue(validate_gate_report(forged))
            with self.assertRaises(ValidationError):
                validate_p1_gate(
                    evidence_root=root,
                    manifest=manifest,
                    checked_at_utc=None,  # type: ignore[arg-type]
                    policy=policy,
                )


class PilotTests(unittest.TestCase):
    def test_interrupted_and_one_shot_runs_are_identical(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            one_shot = root / "one"
            resumed = root / "resumed"
            run_pilot(one_shot)
            first = run_pilot(resumed, stop_after=3)
            self.assertFalse(first["completed"])
            run_pilot(resumed, stop_after=2)
            run_pilot(resumed)
            self.assertEqual(load_json(one_shot / "completion.json"), load_json(resumed / "completion.json"))
            self.assertTrue(verify_pilot(one_shot)["complete"])
            self.assertTrue(verify_pilot(resumed)["complete"])

    def test_checkpoint_lag_recovers_but_tamper_fails(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "source"
            target = root / "target"
            run_pilot(source)
            run_pilot(target, stop_after=2)
            # Simulate a crash after the third immutable result was committed but
            # before checkpoint replacement.
            third = load_json(source / "results" / "000002.json")
            atomic_write_json(target / "results" / "000002.json", third, overwrite=False)
            resumed = run_pilot(target, stop_after=0)
            self.assertEqual(resumed["next_index"], 3)
            run_pilot(target)
            tampered_path = target / "results" / "000001.json"
            tampered = load_json(tampered_path)
            tampered["ordinal"] = 99
            atomic_write_json(tampered_path, tampered)
            with self.assertRaises(ValidationError):
                verify_pilot(target)

    def test_checkpoint_snapshot_survives_resume_and_completion(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            work = Path(raw) / "resumed"
            checkpoint = run_pilot(work, stop_after=3)
            snapshot_path = checkpoint_snapshot_path(work, 3)
            self.assertTrue(snapshot_path.is_file())
            snapshot_bytes = snapshot_path.read_bytes()
            snapshot_digest = sha256_file(snapshot_path)

            current = verify_checkpoint_snapshot(
                work, snapshot_path, require_current=True
            )
            self.assertFalse(current["historical"])
            self.assertEqual(current["next_index"], checkpoint["next_index"])

            run_pilot(work)
            self.assertEqual(snapshot_path.read_bytes(), snapshot_bytes)
            self.assertEqual(sha256_file(snapshot_path), snapshot_digest)
            historical = verify_checkpoint_snapshot(work, snapshot_path)
            self.assertTrue(historical["valid"])
            self.assertTrue(historical["historical"])
            self.assertTrue(historical["pilot_complete"])
            self.assertEqual(historical["durable_result_count"], 10)
            with self.assertRaises(ValidationError):
                verify_checkpoint_snapshot(work, snapshot_path, require_current=True)

    def test_snapshot_validator_checks_the_historical_result_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            work = Path(raw) / "resumed"
            run_pilot(work, stop_after=3)
            snapshot_path = checkpoint_snapshot_path(work, 3)
            run_pilot(work)
            first_result = work / "results" / "000001.json"
            tampered = load_json(first_result)
            tampered["ordinal"] = 99
            atomic_write_json(first_result, tampered)
            with self.assertRaises(ValidationError):
                verify_checkpoint_snapshot(work, snapshot_path)


class SchemaAndAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[3]

    def test_schema_catalog_is_valid_json(self) -> None:
        for name in REQUIRED_SCHEMA_FILES:
            with self.subTest(name=name):
                value = json.loads((self.repo_root / "run" / "schemas" / name).read_text("utf-8"))
                self.assertIn("$schema", value)
                self.assertIn("$id", value)

    def test_runtime_state_fields_match_declared_json_schema(self) -> None:
        schema = json.loads(
            (self.repo_root / "run" / "schemas" / "campaign-state-v1.schema.json").read_text(
                "utf-8"
            )
        )
        state = make_initial_state(
            campaign="lr-positivity", run_id="schema-test", owner_id="integrator", at_utc="t"
        )
        self.assertEqual(set(state), set(schema["required"]))
        self.assertTrue(set(state) <= set(schema["properties"]))
        self.assertIn("transition_history", schema["properties"])

    def test_readiness_fails_closed_without_gate_state_or_pilot(self) -> None:
        report = audit_readiness(
            repo_root=self.repo_root,
            checked_at_utc="2026-07-23T00:00:00Z",
            probe_tools=False,
        )
        self.assertFalse(report["ready_for_p2_adjudication"])
        self.assertFalse(report["p2_launch_authorized"])
        self.assertIn("P1.GATE", report["blockers"])
        self.assertIn("P2.NAIVE_BOX_FEASIBILITY", report["blockers"])
        boxes = report["planning_inputs"]["boxes"]
        b4 = next(item for item in boxes if item["box"] == "B4")
        self.assertEqual(b4["estimate_status"], "sample estimate, not completeness certificate")
        self.assertEqual(validate_readiness_report(report), [])
        for field, invalid in (
            ("checked_at_utc", None),
            ("checked_at_utc", ""),
            ("repo_root", None),
            ("repo_root", "  "),
            ("next_action", None),
            ("next_action", ""),
        ):
            with self.subTest(field=field, invalid=invalid):
                forged = json.loads(json.dumps(report))
                forged[field] = invalid
                self.assertTrue(validate_readiness_report(forged))
        with self.assertRaises(ValidationError):
            audit_readiness(
                repo_root=self.repo_root,
                checked_at_utc=None,  # type: ignore[arg-type]
                probe_tools=False,
            )

    def test_readiness_validator_rejects_forged_shallow_pass(self) -> None:
        forged = {
            "schema_version": "lr-readiness-report/v1",
            "ready_for_p2_adjudication": True,
            "p2_launch_authorized": False,
            "checks": [
                {"code": "P1.GATE", "passed": True, "required": True, "detail": "trust me"}
            ],
            "blockers": [],
            "warnings": [],
            "planning_inputs": {},
        }
        self.assertTrue(validate_readiness_report(forged))


if __name__ == "__main__":
    unittest.main()
