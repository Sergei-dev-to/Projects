"""Fail-closed validation of the scientific Phase-1 gate."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from .atomic import load_json
from .canonical import canonical_fraction, is_sha256, sha256_json
from .errors import ValidationError
from .manifest import artifacts_by_role, verify_manifest

GATE_REPORT_SCHEMA = "lr-p1-gate-report/v1"
FIXTURE_REPORT_SCHEMA = "lr-p1-fixture-agreement/v1"

REQUIRED_GATE_CHECK_CODES = frozenset(
    {
        "P1.POLICY",
        "P1.MANIFEST",
        "P1.BASELINE_ROLE",
        "P1.E1_PARITY_ROLE",
        "P1.E1_FRONTIER_ROLE",
        "P1.E1_MISMATCH_ROLE",
        "P1.E1_MANIFEST_ROLE",
        "P1.FIXTURE_ROLE",
        "P1.FIXTURE_DEFINITION_ROLE",
        "P1.FIXTURE_LRCALC_ROLE",
        "P1.FIXTURE_NORMALIZ_ROLE",
        "P1.E2_SUMMARY_ROLE",
        "P1.E2_SIDECAR_ROLE",
        "P1.BASELINE_HASH",
        "P1.BASELINE_COUNT",
        "P1.BASELINE_SCOPE",
        "P1.BASELINE_CANONICALIZER",
        "P1.E1_PARITY_REPORT",
        "P1.E1_FRONTIER_PAYLOAD",
        "P1.E1_MISMATCH_BUNDLE",
        "P1.E1_ARTIFACT_LINKAGE",
        "P1.FIXTURE_LRCALC_ARTIFACT",
        "P1.FIXTURE_NORMALIZ_ARTIFACT",
        "P1.FIXTURE_EVALUATOR_ID_SET",
        "P1.FIXTURE_EVIDENCE_CHAIN",
        "P1.E2_SUMMARY",
        "P1.FIXTURE_SCHEMA",
        "P1.FIXTURE_COUNT",
        "P1.FIXTURE_TOPLEVEL_AGREEMENT",
        "P1.FIXTURE_RECORDS",
        "P1.FIXTURE_COVERAGE",
        "P1.FIXTURE_ADAPTER_ID_SET",
    }
)

DEFAULT_P1_POLICY: dict[str, Any] = {
    "schema_version": "lr-p1-gate-policy/v1",
    "gate_id": "P1",
    "baseline": {
        "triples_payload_sha256": "b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7",
        "count": 7549,
        "scope": {"max_length": 5, "max_size": 7},
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
    "tools": {
        "python": "3.12.3",
        "lrcalc": "2.1",
        "pynormaliz": "2.19",
        "normaliz": "Normaliz 3.10.2",
    },
    "fixtures": {
        "min_count": 6,
        "definition_file_sha256": "3437ad9b81c4ef4a267413b00a8b6843432a19b41d048d43f046b585cf8179e6",
        "evaluator_names": ["lrcalc-interp", "normaliz-ehrhart"],
        "required_coverage": [
            "boundary.lambda",
            "boundary.mu",
            "boundary.nu",
            "rhombus.type-a",
            "rhombus.type-b",
            "rhombus.type-c",
            "dimension.zero",
            "dimension.positive",
            "dimension.degenerate",
            "dimension.empty",
            "coefficient.zero",
            "coefficient.one",
            "coefficient.multiple",
            "anchor.degree6",
        ],
    },
}


@dataclass
class _Collector:
    checks: list[dict[str, Any]]
    failures: list[dict[str, str]]

    def check(self, code: str, passed: bool, detail: str) -> None:
        self.checks.append({"code": code, "passed": bool(passed), "detail": detail})
        if not passed:
            self.failures.append({"code": code, "message": detail})


def validate_p1_gate(
    *,
    evidence_root: Path,
    manifest: Any,
    checked_at_utc: str,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a gate report; malformed or missing evidence always means failure."""

    if not isinstance(checked_at_utc, str) or not checked_at_utc.strip():
        raise ValidationError("checked_at_utc must be a non-empty string")

    policy = DEFAULT_P1_POLICY if policy is None else policy
    collector = _Collector([], [])
    policy_errors = _validate_policy(policy)
    collector.check(
        "P1.POLICY",
        not policy_errors,
        "policy valid" if not policy_errors else "; ".join(policy_errors),
    )

    verification = verify_manifest(evidence_root, manifest)
    collector.check(
        "P1.MANIFEST",
        verification.valid,
        "all manifested artifacts verified"
        if verification.valid
        else "; ".join(verification.errors),
    )

    if not policy_errors and verification.valid:
        grouped = artifacts_by_role(verification.artifacts)
        required_roles = {
            "P1.BASELINE_ROLE": "baseline-frontier",
            "P1.E1_PARITY_ROLE": "e1-parity-report",
            "P1.E1_FRONTIER_ROLE": "e1-frontier-payload",
            "P1.E1_MISMATCH_ROLE": "e1-mismatch-bundle",
            "P1.E1_MANIFEST_ROLE": "e1-artifact-manifest",
            "P1.FIXTURE_ROLE": "fixture-agreement",
            "P1.FIXTURE_DEFINITION_ROLE": "fixture-definition-set",
            "P1.FIXTURE_LRCALC_ROLE": "fixture-evaluator-lrcalc",
            "P1.FIXTURE_NORMALIZ_ROLE": "fixture-evaluator-normaliz",
            "P1.E2_SUMMARY_ROLE": "e2-fixture-summary",
            "P1.E2_SIDECAR_ROLE": "e2-summary-sidecar",
        }
        selected: dict[str, dict[str, Any]] = {}
        for code, role in required_roles.items():
            entries = grouped.get(role, [])
            collector.check(
                code,
                len(entries) == 1,
                f"expected exactly one {role} artifact; found {len(entries)}",
            )
            if len(entries) == 1:
                selected[role] = entries[0]
        if "baseline-frontier" in selected:
            _validate_baseline(
                Path(evidence_root) / selected["baseline-frontier"]["logical_path"],
                policy,
                collector,
            )
        e1_roles = {
            "e1-parity-report",
            "e1-frontier-payload",
            "e1-mismatch-bundle",
            "e1-artifact-manifest",
        }
        if e1_roles <= selected.keys():
            _validate_e1_parity(Path(evidence_root), selected, policy, collector)
        evaluator_roles = {"fixture-evaluator-lrcalc", "fixture-evaluator-normaliz"}
        evaluator_maps: dict[str, dict[str, list[str]]] | None = None
        if evaluator_roles <= selected.keys():
            evaluator_maps = _validate_fixture_evaluator_artifacts(
                Path(evidence_root), selected, collector
            )
        expected_coverage_by_id: dict[str, list[str]] | None = None
        if (
            evaluator_maps is not None
            and "fixture-definition-set" in selected
            and "fixture-evaluator-lrcalc" in selected
            and "fixture-evaluator-normaliz" in selected
            and "e2-fixture-summary" in selected
            and "e2-summary-sidecar" in selected
        ):
            expected_coverage_by_id = _validate_fixture_evidence_chain(
                Path(evidence_root), selected, grouped, evaluator_maps, policy, collector
            )
        if (
            "fixture-agreement" in selected
            and evaluator_maps is not None
            and expected_coverage_by_id is not None
        ):
            _validate_fixtures(
                Path(evidence_root) / selected["fixture-agreement"]["logical_path"],
                policy,
                {
                    "lrcalc-interp": selected["fixture-evaluator-lrcalc"]["sha256"],
                    "normaliz-ehrhart": selected["fixture-evaluator-normaliz"]["sha256"],
                },
                evaluator_maps,
                expected_coverage_by_id,
                collector,
            )
    elif not verification.valid:
        collector.check(
            "P1.EVIDENCE_NOT_EVALUATED",
            False,
            "scientific evidence was not evaluated because its manifest failed",
        )

    return {
        "schema_version": GATE_REPORT_SCHEMA,
        "gate_id": "P1",
        "passed": not collector.failures,
        "checked_at_utc": checked_at_utc,
        "policy_sha256": sha256_json(policy),
        "evidence_manifest_sha256": verification.manifest_sha256,
        "checks": collector.checks,
        "failures": collector.failures,
        "next_action": (
            "integrator may adjudicate P1_ORACLE_VALIDATED; this report does not transition state"
            if not collector.failures
            else "STOP: reconcile evidence; do not advance campaign state"
        ),
    }


def validate_fixture_manifest(
    *,
    evidence_root: Path,
    manifest: Any,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Freshly validate the complete fixed E2 fixture evidence bundle."""

    policy = DEFAULT_P1_POLICY if policy is None else policy
    collector = _Collector([], [])
    policy_errors = _validate_policy(policy)
    collector.check(
        "FIXTURES.POLICY",
        not policy_errors,
        "policy valid" if not policy_errors else "; ".join(policy_errors),
    )
    verification = verify_manifest(evidence_root, manifest)
    collector.check(
        "FIXTURES.MANIFEST",
        verification.valid,
        "all manifested fixture artifacts verified"
        if verification.valid
        else "; ".join(verification.errors),
    )
    if not policy_errors and verification.valid:
        grouped = artifacts_by_role(verification.artifacts)
        roles = {
            "fixture-definition-set",
            "fixture-agreement",
            "fixture-evaluator-lrcalc",
            "fixture-evaluator-normaliz",
            "e2-fixture-summary",
            "e2-summary-sidecar",
        }
        selected: dict[str, dict[str, Any]] = {}
        for role in sorted(roles):
            entries = grouped.get(role, [])
            collector.check(
                f"FIXTURES.ROLE.{role}",
                len(entries) == 1,
                f"expected exactly one {role}; found {len(entries)}",
            )
            if len(entries) == 1:
                selected[role] = entries[0]
        if roles <= selected.keys():
            maps = _validate_fixture_evaluator_artifacts(Path(evidence_root), selected, collector)
            coverage_map = None
            if maps is not None:
                coverage_map = _validate_fixture_evidence_chain(
                    Path(evidence_root), selected, grouped, maps, policy, collector
                )
            if maps is not None and coverage_map is not None:
                _validate_fixtures(
                    Path(evidence_root) / selected["fixture-agreement"]["logical_path"],
                    policy,
                    {
                        "lrcalc-interp": selected["fixture-evaluator-lrcalc"]["sha256"],
                        "normaliz-ehrhart": selected["fixture-evaluator-normaliz"]["sha256"],
                    },
                    maps,
                    coverage_map,
                    collector,
                )
    return {
        "schema_version": "lr-p1-fixture-gate-report/v1",
        "passed": not collector.failures,
        "manifest_sha256": verification.manifest_sha256,
        "checks": collector.checks,
        "failures": collector.failures,
    }


def validate_gate_report(report: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(report, dict):
        return ["gate report must be an object"]
    if report.get("schema_version") != GATE_REPORT_SCHEMA:
        errors.append("unsupported gate-report schema")
    if report.get("gate_id") != "P1":
        errors.append("gate_id must be P1")
    if not isinstance(report.get("passed"), bool):
        errors.append("passed must be boolean")
    if not isinstance(report.get("checked_at_utc"), str) or not report["checked_at_utc"].strip():
        errors.append("checked_at_utc must be a non-empty string")
    if not isinstance(report.get("next_action"), str) or not report["next_action"].strip():
        errors.append("next_action must be a non-empty string")
    if not is_sha256(report.get("policy_sha256")):
        errors.append("policy_sha256 is invalid")
    evidence_digest = report.get("evidence_manifest_sha256")
    if report.get("passed") is True and not is_sha256(evidence_digest):
        errors.append("a passing report requires a valid evidence_manifest_sha256")
    elif report.get("passed") is False and evidence_digest is not None and not is_sha256(evidence_digest):
        errors.append("evidence_manifest_sha256 must be null or valid")
    checks = report.get("checks")
    check_codes: set[str] = set()
    failed_check_codes: set[str] = set()
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty list")
    else:
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{index}] must be an object")
                continue
            code = check.get("code")
            if not isinstance(code, str) or not code or code in check_codes:
                errors.append(f"checks[{index}] has missing/duplicate code")
                continue
            check_codes.add(code)
            if not isinstance(check.get("passed"), bool):
                errors.append(f"checks[{index}].passed must be boolean")
            elif check["passed"] is False:
                failed_check_codes.add(code)
            if not isinstance(check.get("detail"), str):
                errors.append(f"checks[{index}].detail must be a string")
        missing = REQUIRED_GATE_CHECK_CODES - check_codes
        if missing:
            errors.append("gate report lacks required checks: " + ", ".join(sorted(missing)))
    failures = report.get("failures")
    if not isinstance(failures, list):
        errors.append("failures must be a list")
    elif report.get("passed") is True and failures:
        errors.append("a passing gate report cannot contain failures")
    elif report.get("passed") is False and not failures:
        errors.append("a failing gate report must contain failures")
    if report.get("passed") is True and failed_check_codes:
        errors.append("passing gate report contains failed checks")
    if isinstance(failures, list):
        failure_codes = {
            item.get("code") for item in failures if isinstance(item, dict) and item.get("code")
        }
        if failure_codes != failed_check_codes:
            errors.append("failure codes do not exactly match failed checks")
    return errors


def _validate_policy(policy: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(policy, dict):
        return ["policy must be an object"]
    if policy.get("schema_version") != "lr-p1-gate-policy/v1":
        errors.append("unsupported policy schema")
    if policy.get("gate_id") != "P1":
        errors.append("policy gate_id must be P1")
    baseline = policy.get("baseline")
    if not isinstance(baseline, dict):
        errors.append("policy.baseline must be an object")
    else:
        if not is_sha256(baseline.get("triples_payload_sha256")):
            errors.append("policy baseline hash is invalid")
        if not isinstance(baseline.get("count"), int) or baseline.get("count", 0) < 1:
            errors.append("policy baseline count must be positive")
        if not isinstance(baseline.get("scope"), dict):
            errors.append("policy baseline scope must be an object")
        if not isinstance(baseline.get("canonicalization_token"), str):
            errors.append("policy canonicalization token is missing")
    e1 = policy.get("e1")
    if not isinstance(e1, dict):
        errors.append("policy.e1 must be an object")
    else:
        if e1.get("schema_version") != 1:
            errors.append("policy e1 schema_version must be 1")
        if e1.get("gate") != "P1_E1_BASELINE_PARITY":
            errors.append("policy e1 gate is invalid")
        if e1.get("evaluator_name") != "lrcalc-interp":
            errors.append("policy e1 evaluator_name is invalid")
        if e1.get("canonicalizer_version") != "swap-only-v1":
            errors.append("policy e1 canonicalizer_version is invalid")
        modes = e1.get("allowed_interpolation_modes")
        if not isinstance(modes, list) or not modes or not all(
            isinstance(mode, str) and mode for mode in modes
        ):
            errors.append("policy e1 allowed_interpolation_modes is invalid")
        zero_fields = e1.get("zero_comparison_fields")
        if not isinstance(zero_fields, list) or not zero_fields or len(set(zero_fields)) != len(
            zero_fields
        ):
            errors.append("policy e1 zero_comparison_fields is invalid")
        anchors = e1.get("required_anchors")
        if not isinstance(anchors, dict) or not anchors or not all(
            isinstance(anchor_id, str) and anchor_id for anchor_id in anchors
        ):
            errors.append("policy e1 required_anchors is invalid")
    tools = policy.get("tools")
    if not isinstance(tools, dict) or set(tools) != {
        "python",
        "lrcalc",
        "pynormaliz",
        "normaliz",
    } or not all(isinstance(value, str) and value for value in tools.values()):
        errors.append("policy.tools must pin all four exact tool-version strings")
    fixtures = policy.get("fixtures")
    if not isinstance(fixtures, dict):
        errors.append("policy.fixtures must be an object")
    else:
        if not isinstance(fixtures.get("min_count"), int) or fixtures.get("min_count", 0) < 1:
            errors.append("fixture min_count must be positive")
        if not is_sha256(fixtures.get("definition_file_sha256")):
            errors.append("fixture definition_file_sha256 must be pinned")
        names = fixtures.get("evaluator_names")
        if not isinstance(names, list) or len(names) != 2 or len(set(names)) != 2:
            errors.append("exactly two distinct evaluator_names are required")
        coverage = fixtures.get("required_coverage")
        if not isinstance(coverage, list) or not coverage or len(set(coverage)) != len(coverage):
            errors.append("required_coverage must be a non-empty unique list")
    return errors


def _validate_baseline(path: Path, policy: dict[str, Any], collector: _Collector) -> None:
    try:
        baseline = load_json(path)
        triples = baseline.get("triples") if isinstance(baseline, dict) else None
        if not isinstance(triples, list):
            raise ValueError("baseline.triples must be a list")
        actual_hash = sha256_json(triples)
        expected = policy["baseline"]
        collector.check(
            "P1.BASELINE_HASH",
            actual_hash == expected["triples_payload_sha256"],
            f"expected {expected['triples_payload_sha256']}; computed {actual_hash}",
        )
        collector.check(
            "P1.BASELINE_COUNT",
            len(triples) == expected["count"],
            f"expected {expected['count']} triples; found {len(triples)}",
        )
        meta = baseline.get("meta")
        scope = meta.get("scope") if isinstance(meta, dict) else None
        canonicalization = meta.get("canonicalization") if isinstance(meta, dict) else None
        collector.check(
            "P1.BASELINE_SCOPE",
            scope == expected["scope"],
            f"expected scope {expected['scope']!r}; found {scope!r}",
        )
        token = expected["canonicalization_token"]
        collector.check(
            "P1.BASELINE_CANONICALIZER",
            isinstance(canonicalization, str) and token in canonicalization,
            f"canonicalization must contain {token!r}; found {canonicalization!r}",
        )
    except Exception as exc:  # fail closed on malformed scientific evidence
        collector.check("P1.BASELINE_PARSE", False, f"cannot validate baseline: {exc}")


def _validate_e1_parity(
    evidence_root: Path,
    selected: dict[str, dict[str, Any]],
    policy: dict[str, Any],
    collector: _Collector,
) -> None:
    try:
        parity_entry = selected["e1-parity-report"]
        frontier_entry = selected["e1-frontier-payload"]
        mismatch_entry = selected["e1-mismatch-bundle"]
        internal_entry = selected["e1-artifact-manifest"]
        report = load_json(evidence_root / parity_entry["logical_path"])
        frontier = load_json(evidence_root / frontier_entry["logical_path"])
        mismatch = load_json(evidence_root / mismatch_entry["logical_path"])
        internal = load_json(evidence_root / internal_entry["logical_path"])
        errors: list[str] = []
        expected = policy["baseline"]
        e1_policy = policy["e1"]
        if not isinstance(report, dict) or report.get("schema_version") != e1_policy["schema_version"]:
            errors.append("unsupported E1 parity-report schema")
        if report.get("gate") != e1_policy["gate"] or report.get("status") != "pass":
            errors.append("E1 report gate/status is not a pass")
        actual = report.get("actual")
        if not isinstance(actual, dict):
            errors.append("E1 actual block is missing")
        else:
            if actual.get("record_count") != expected["count"]:
                errors.append("E1 actual record_count does not match policy")
            if actual.get("triples_payload_sha256") != expected["triples_payload_sha256"]:
                errors.append("E1 actual payload hash does not match policy")
        report_expected = report.get("expected")
        if report_expected != {
            "record_count": expected["count"],
            "scope": expected["scope"],
            "triples_payload_sha256": expected["triples_payload_sha256"],
        }:
            errors.append("E1 expected block is not linked exactly to the gate policy")
        integrity = report.get("baseline_integrity")
        if not isinstance(integrity, dict):
            errors.append("E1 baseline_integrity block is missing")
        else:
            integrity_hash_fields = (
                "embedded_payload_sha256",
                "sidecar_payload_sha256",
                "triples_payload_sha256",
            )
            if integrity.get("status") != "pass" or integrity.get("errors") != []:
                errors.append("E1 baseline integrity did not pass cleanly")
            if integrity.get("record_count") != expected["count"]:
                errors.append("E1 baseline integrity count differs from policy")
            if any(
                integrity.get(field) != expected["triples_payload_sha256"]
                for field in integrity_hash_fields
            ):
                errors.append("E1 baseline integrity hashes differ from policy")
        comparison = report.get("comparison")
        if not isinstance(comparison, dict):
            errors.append("E1 comparison block is missing")
        else:
            for field in e1_policy["zero_comparison_fields"]:
                if comparison.get(field) != 0:
                    errors.append(f"E1 comparison.{field} is not zero")
            if comparison.get("mismatch_bundle") != Path(
                mismatch_entry["logical_path"]
            ).name:
                errors.append("E1 mismatch-bundle linkage is wrong")
        canonicalization = report.get("canonicalization")
        if not isinstance(canonicalization, dict):
            errors.append("E1 canonicalization block is missing")
        else:
            if canonicalization.get("version") != e1_policy["canonicalizer_version"]:
                errors.append("E1 canonicalizer version is not policy-pinned swap-only-v1")
            if expected["canonicalization_token"] not in str(canonicalization.get("name", "")):
                errors.append("E1 canonicalizer name lacks the swap-only token")
            if canonicalization.get("sort") != "(len(nu), nu, lam, mu)":
                errors.append("E1 enumeration sort is not canonical")
        evaluator = report.get("evaluator")
        if not isinstance(evaluator, dict):
            errors.append("E1 evaluator block is missing")
        else:
            if evaluator.get("name") != e1_policy["evaluator_name"]:
                errors.append("E1 evaluator name is wrong")
            if evaluator.get("interpolation_mode") not in e1_policy["allowed_interpolation_modes"]:
                errors.append("E1 interpolation mode is not policy-approved")
            if evaluator.get("lrcalc_version") != policy["tools"]["lrcalc"]:
                errors.append("E1 lrcalc version differs from policy")
            if evaluator.get("python") != policy["tools"]["python"]:
                errors.append("E1 Python version differs from policy")
        anchors = report.get("anchors")
        required_anchors = e1_policy["required_anchors"]
        if not isinstance(anchors, list) or not anchors:
            errors.append("E1 anchors are missing")
        else:
            anchors_by_id = {
                anchor.get("id"): anchor
                for anchor in anchors
                if isinstance(anchor, dict) and isinstance(anchor.get("id"), str)
            }
            if set(anchors_by_id) != set(required_anchors):
                errors.append("E1 anchor-id set is not exactly policy-pinned")
            for anchor_id, expected_value in required_anchors.items():
                anchor = anchors_by_id.get(anchor_id)
                if (
                    not isinstance(anchor, dict)
                    or anchor.get("pass") is not True
                    or anchor.get("expected") != expected_value
                    or anchor.get("actual") != expected_value
                ):
                    errors.append(f"E1 anchor {anchor_id!r} does not match pinned value")
        if not isinstance(report.get("workers"), int) or report.get("workers", 0) < 1:
            errors.append("E1 worker count is invalid")
        enumeration = report.get("enumeration")
        if not isinstance(enumeration, dict) or enumeration.get("nonzero_triple_count") != expected[
            "count"
        ]:
            errors.append("E1 enumeration count is not linked to parity count")
        collector.check(
            "P1.E1_PARITY_REPORT",
            not errors,
            "typed E1 report proves exact parity against pinned expectation"
            if not errors
            else "; ".join(errors),
        )

        frontier_errors: list[str] = []
        if not isinstance(frontier, dict) or frontier.get("schema_version") != 1:
            frontier_errors.append("E1 frontier schema is invalid")
        else:
            records = frontier.get("triples")
            if not isinstance(records, list):
                frontier_errors.append("E1 frontier triples payload is missing")
            else:
                direct_hash = sha256_json(records)
                if len(records) != expected["count"]:
                    frontier_errors.append("E1 frontier record count differs from policy")
                if direct_hash != expected["triples_payload_sha256"]:
                    frontier_errors.append("E1 recomputed frontier bytes differ from baseline")
                if frontier.get("record_count") != len(records):
                    frontier_errors.append("E1 frontier self-count is inconsistent")
                if frontier.get("triples_payload_sha256") != direct_hash:
                    frontier_errors.append("E1 frontier embedded hash is inconsistent")
                if isinstance(actual, dict) and (
                    actual.get("record_count") != len(records)
                    or actual.get("triples_payload_sha256") != direct_hash
                ):
                    frontier_errors.append("E1 report actual block is not linked to frontier bytes")
            if frontier.get("gate") != e1_policy["gate"]:
                frontier_errors.append("E1 frontier gate identity is wrong")
            if frontier.get("canonicalization") != report.get("canonicalization"):
                frontier_errors.append("E1 frontier canonicalization differs from report")
        collector.check(
            "P1.E1_FRONTIER_PAYLOAD",
            not frontier_errors,
            "controller directly hashed the production E1 frontier payload"
            if not frontier_errors
            else "; ".join(frontier_errors),
        )

        mismatch_ok = (
            isinstance(mismatch, dict)
            and mismatch.get("schema_version") == e1_policy["schema_version"]
            and mismatch.get("gate") == e1_policy["gate"]
            and mismatch.get("status") == "empty"
            and mismatch.get("items") == []
        )
        collector.check(
            "P1.E1_MISMATCH_BUNDLE",
            mismatch_ok,
            "E1 mismatch bundle is typed and empty"
            if mismatch_ok
            else "E1 mismatch bundle is malformed or nonempty",
        )

        linkage_errors: list[str] = []
        if (
            not isinstance(internal, dict)
            or internal.get("schema_version") != e1_policy["schema_version"]
            or internal.get("gate") != e1_policy["gate"]
            or not isinstance(internal.get("artifacts"), list)
        ):
            linkage_errors.append("E1 internal artifact manifest is malformed")
        else:
            internal_by_name = {
                item.get("path"): item
                for item in internal["artifacts"]
                if isinstance(item, dict) and isinstance(item.get("path"), str)
            }
            for name, entry in (
                ("actual_frontier.json", frontier_entry),
                ("parity_report.json", parity_entry),
                ("mismatches.json", mismatch_entry),
            ):
                linked = internal_by_name.get(name)
                physical = evidence_root / entry["logical_path"]
                if (
                    not isinstance(linked, dict)
                    or linked.get("sha256") != entry["sha256"]
                    or linked.get("bytes") != physical.stat().st_size
                    or Path(entry["logical_path"]).name != name
                ):
                    linkage_errors.append(f"E1 internal linkage failed for {name}")
            if set(internal_by_name) != {
                "actual_frontier.json",
                "parity_report.json",
                "mismatches.json",
            }:
                linkage_errors.append("E1 internal artifact set is not exact")
        collector.check(
            "P1.E1_ARTIFACT_LINKAGE",
            not linkage_errors,
            "E1 report and mismatch bytes are bound through both manifests"
            if not linkage_errors
            else "; ".join(linkage_errors),
        )
    except Exception as exc:
        collector.check("P1.E1_PARSE", False, f"cannot validate E1 parity evidence: {exc}")


def _validate_fixture_evaluator_artifacts(
    evidence_root: Path,
    selected: dict[str, dict[str, Any]],
    collector: _Collector,
) -> dict[str, dict[str, list[str]]] | None:
    maps: dict[str, dict[str, list[str]]] = {}
    overall_ok = True
    for role, expected_name, expected_schema in (
        (
            "fixture-evaluator-lrcalc",
            "lrcalc-interp",
            "lr-p1-lrcalc-fixture-evaluator/v1",
        ),
        (
            "fixture-evaluator-normaliz",
            "normaliz-ehrhart",
            "lr-p1-normaliz-fixture-evaluator/v1",
        ),
    ):
        errors: list[str] = []
        try:
            document = load_json(evidence_root / selected[role]["logical_path"])
            if not isinstance(document, dict) or document.get("schema_version") != expected_schema:
                errors.append("schema_version is wrong")
            if not isinstance(document, dict) or document.get("evaluator") != expected_name:
                errors.append("evaluator identity is wrong")
            if not isinstance(document, dict) or not isinstance(document.get("method"), str):
                errors.append("method description is missing")
            fixtures = document.get("fixtures") if isinstance(document, dict) else None
            if not isinstance(fixtures, list) or not fixtures:
                errors.append("fixtures must be a non-empty list")
                fixtures = []
            fixture_map: dict[str, list[str]] = {}
            for index, fixture in enumerate(fixtures):
                if not isinstance(fixture, dict):
                    errors.append(f"fixture[{index}] is not an object")
                    continue
                fixture_id = fixture.get("id")
                if not isinstance(fixture_id, str) or not fixture_id or fixture_id in fixture_map:
                    errors.append(f"fixture[{index}] has missing/duplicate id")
                    continue
                raw_poly = fixture.get("poly")
                try:
                    if not isinstance(raw_poly, list) or not raw_poly:
                        raise ValueError("poly is empty")
                    poly = [canonical_fraction(value) for value in raw_poly]
                except Exception as exc:
                    errors.append(f"fixture {fixture_id} polynomial is invalid: {exc}")
                    continue
                fixture_map[fixture_id] = poly
                if expected_name == "lrcalc-interp":
                    if fixture.get("verified") is not True:
                        errors.append(f"fixture {fixture_id} is not verified")
                    degree_bound = fixture.get("degree_bound")
                    if (
                        not isinstance(degree_bound, int)
                        or isinstance(degree_bound, bool)
                        or degree_bound < max(0, len(poly) - 1)
                    ):
                        errors.append(f"fixture {fixture_id} degree_bound is invalid")
                    samples = fixture.get("samples")
                    if not isinstance(samples, dict) or not samples:
                        errors.append(f"fixture {fixture_id} has no lrcalc samples")
                    else:
                        parsed_domain: list[int] = []
                        for raw_n, count in samples.items():
                            try:
                                n = int(raw_n)
                                parsed_domain.append(n)
                                evaluated = sum(
                                    Fraction(coefficient) * n**degree
                                    for degree, coefficient in enumerate(poly)
                                )
                                if str(n) != raw_n or evaluated.denominator != 1 or int(
                                    evaluated
                                ) != count:
                                    errors.append(
                                        f"fixture {fixture_id} sample N={raw_n} does not match poly"
                                    )
                            except Exception:
                                errors.append(f"fixture {fixture_id} has malformed sample {raw_n!r}")
                        parsed_domain.sort()
                        if (
                            parsed_domain != list(range(1, max(parsed_domain, default=0) + 1))
                            or not isinstance(degree_bound, int)
                            or max(parsed_domain, default=0) < degree_bound + 2
                        ):
                            errors.append(
                                f"fixture {fixture_id} sample domain is not consecutive through B+2"
                            )
                else:
                    if fixture.get("period_collapses_to_one") is not True:
                        errors.append(f"fixture {fixture_id} period did not collapse to one")
                    if not isinstance(fixture.get("affine_dimension"), int):
                        errors.append(f"fixture {fixture_id} affine_dimension is invalid")
                    if not isinstance(fixture.get("number_lattice_points"), int):
                        errors.append(f"fixture {fixture_id} lattice count is invalid")
                    raw_quasi = fixture.get("raw_ehrhart_quasipolynomial")
                    try:
                        decoded = _decode_raw_quasipolynomial(
                            raw_quasi,
                            empty=fixture.get("affine_dimension") == -1,
                        )
                        if decoded != poly:
                            errors.append(
                                f"fixture {fixture_id} raw quasipolynomial does not decode to poly"
                            )
                        p_at_one = sum(Fraction(value) for value in decoded)
                        if (
                            p_at_one.denominator != 1
                            or int(p_at_one) != fixture.get("number_lattice_points")
                        ):
                            errors.append(
                                f"fixture {fixture_id} P(1) differs from number_lattice_points"
                            )
                    except Exception as exc:
                        errors.append(
                            f"fixture {fixture_id} raw quasipolynomial is invalid: {exc}"
                        )
            maps[expected_name] = fixture_map
        except Exception as exc:
            errors.append(f"cannot parse evaluator artifact: {exc}")
        code = (
            "P1.FIXTURE_LRCALC_ARTIFACT"
            if expected_name == "lrcalc-interp"
            else "P1.FIXTURE_NORMALIZ_ARTIFACT"
        )
        collector.check(
            code,
            not errors,
            f"typed {expected_name} fixture artifact is internally consistent"
            if not errors
            else "; ".join(errors),
        )
        overall_ok = overall_ok and not errors
    same_ids = (
        set(maps.get("lrcalc-interp", {})) == set(maps.get("normaliz-ehrhart", {}))
        and bool(maps.get("lrcalc-interp"))
    )
    collector.check(
        "P1.FIXTURE_EVALUATOR_ID_SET",
        same_ids,
        "typed evaluator artifacts cover the same nonempty fixture-id set"
        if same_ids
        else "typed evaluator fixture-id sets differ or are empty",
    )
    return maps if overall_ok and same_ids else None


def _decode_raw_quasipolynomial(raw: Any, *, empty: bool) -> list[str]:
    if (
        not isinstance(raw, list)
        or len(raw) != 2
        or not isinstance(raw[0], list)
        or not isinstance(raw[1], int)
        or isinstance(raw[1], bool)
        or raw[1] <= 0
        or not all(isinstance(value, int) and not isinstance(value, bool) for value in raw[0])
    ):
        raise ValueError("expected [integer coefficient numerators, positive denominator]")
    numerators, denominator = raw
    if not numerators:
        if not empty:
            raise ValueError("empty coefficient list is allowed only for an empty polytope")
        return ["0"]
    coefficients = [str(Fraction(value, denominator)) for value in numerators]
    while len(coefficients) > 1 and coefficients[-1] == "0":
        coefficients.pop()
    return coefficients


def _validate_fixture_evidence_chain(
    evidence_root: Path,
    selected: dict[str, dict[str, Any]],
    grouped: dict[str, list[dict[str, Any]]],
    evaluator_maps: dict[str, dict[str, list[str]]],
    policy: dict[str, Any],
    collector: _Collector,
) -> dict[str, list[str]] | None:
    """Bind fixed fixtures -> reports -> inputs/raw outputs -> typed adapters."""

    errors: list[str] = []
    expected_coverage_by_id: dict[str, list[str]] = {}
    try:
        definition_entry = selected["fixture-definition-set"]
        if definition_entry["sha256"] != policy["fixtures"]["definition_file_sha256"]:
            errors.append("fixture-definition bytes do not match the policy-pinned SHA-256")
        definitions_doc = load_json(evidence_root / definition_entry["logical_path"])
        definitions = definitions_doc.get("fixtures") if isinstance(definitions_doc, dict) else None
        if (
            not isinstance(definitions_doc, dict)
            or definitions_doc.get("schema_version") != 1
            or not isinstance(definitions, list)
            or len(definitions) < policy["fixtures"]["min_count"]
        ):
            raise ValueError("fixture definition set is malformed")
        definitions_by_id: dict[str, dict[str, Any]] = {}
        for definition in definitions:
            fixture_id = definition.get("id") if isinstance(definition, dict) else None
            if not isinstance(fixture_id, str) or not fixture_id or fixture_id in definitions_by_id:
                errors.append("fixture definitions contain a missing/duplicate id")
                continue
            try:
                expected_poly = [
                    canonical_fraction(value) for value in definition["expected_polynomial"]
                ]
                if sum(Fraction(value) for value in expected_poly) != definition["expected_lr_at_1"]:
                    errors.append(f"definition {fixture_id} polynomial disagrees at N=1")
            except Exception as exc:
                errors.append(f"definition {fixture_id} expected values are invalid: {exc}")
            definitions_by_id[fixture_id] = definition
            expected_coverage_by_id[fixture_id] = _derived_coverage_tags(definition)

        report_entries = _entries_by_fixture_id(
            grouped.get("fixture-comparison-report", []), ".report.json", errors
        )
        input_entries = _entries_by_fixture_id(
            grouped.get("explicit-hive-input", []), ".hive.json", errors
        )
        normaliz_input_entries = _entries_by_fixture_id(
            grouped.get("normaliz-input", []), ".in", errors
        )
        raw_output_entries = _entries_by_fixture_id(
            grouped.get("normaliz-raw-output", []), ".out", errors
        )
        definition_ids = set(definitions_by_id)
        if set(report_entries) != definition_ids:
            errors.append("per-fixture report set differs from fixed definition set")
        if set(input_entries) != definition_ids:
            errors.append("explicit hive-input set differs from fixed definition set")

        lrcalc_doc = load_json(
            evidence_root / selected["fixture-evaluator-lrcalc"]["logical_path"]
        )
        normaliz_doc = load_json(
            evidence_root / selected["fixture-evaluator-normaliz"]["logical_path"]
        )
        typed_lrcalc = {
            item["id"]: item for item in lrcalc_doc["fixtures"] if isinstance(item, dict)
        }
        typed_normaliz = {
            item["id"]: item for item in normaliz_doc["fixtures"] if isinstance(item, dict)
        }
        expected_cli_ids: set[str] = set()
        for fixture_id, definition in definitions_by_id.items():
            if fixture_id not in report_entries:
                continue
            report = load_json(evidence_root / report_entries[fixture_id]["logical_path"])
            if not isinstance(report, dict) or report.get("schema_version") != 1:
                errors.append(f"report {fixture_id} schema is invalid")
                continue
            if report.get("fixture") != definition:
                errors.append(f"report {fixture_id} is not bound to the fixed definition")
            checks = report.get("checks")
            if (
                report.get("pass") is not True
                or not isinstance(checks, list)
                or not checks
                or any(
                    not isinstance(check, dict)
                    or check.get("pass") is not True
                    or check.get("actual") != check.get("expected")
                    for check in checks
                )
            ):
                errors.append(f"report {fixture_id} does not have an exact all-pass check set")

            expected_poly = [
                canonical_fraction(value) for value in definition["expected_polynomial"]
            ]
            lrcalc = report.get("e1_lrcalc_interp")
            positive_samples = report.get("e1_lrcalc_positive_stretches")
            typed_l = typed_lrcalc.get(fixture_id, {})
            if (
                not isinstance(lrcalc, dict)
                or lrcalc.get("canonical_polynomial") != expected_poly
                or lrcalc.get("all_available_samples_verified") is not True
                or typed_l.get("poly") != expected_poly
                or typed_l.get("degree_bound") != lrcalc.get("degree_bound")
                or typed_l.get("samples") != positive_samples
                or typed_l.get("verified") is not True
            ):
                errors.append(f"report {fixture_id} lrcalc chain is inconsistent")
            try:
                _validate_positive_sample_map(
                    positive_samples,
                    expected_poly,
                    int(lrcalc["degree_bound"]),
                )
            except Exception as exc:
                errors.append(f"report {fixture_id} lrcalc samples are invalid: {exc}")

            normaliz = report.get("e2_normaliz")
            typed_n = typed_normaliz.get(fixture_id, {})
            if not isinstance(normaliz, dict):
                errors.append(f"report {fixture_id} Normaliz block is missing")
            else:
                try:
                    decoded = _decode_raw_quasipolynomial(
                        normaliz.get("ehrhart_quasipolynomial_raw"),
                        empty=normaliz.get("empty") is True,
                    )
                    p_at_one = sum(Fraction(value) for value in decoded)
                    if (
                        decoded != expected_poly
                        or normaliz.get("canonical_polynomial") != expected_poly
                        or normaliz.get("period_collapses_to_one") is not True
                        or normaliz.get("raw_period") != 1
                        or p_at_one.denominator != 1
                        or int(p_at_one) != normaliz.get("number_lattice_points")
                        or normaliz.get("number_lattice_points") != definition["expected_lr_at_1"]
                        or normaliz.get("affine_dimension")
                        != definition["expected_affine_dimension"]
                    ):
                        errors.append(f"report {fixture_id} Normaliz arithmetic is inconsistent")
                    typed_expected = {
                        "poly": expected_poly,
                        "affine_dimension": normaliz.get("affine_dimension"),
                        "number_lattice_points": normaliz.get("number_lattice_points"),
                        "period_collapses_to_one": True,
                        "raw_ehrhart_quasipolynomial": normaliz.get(
                            "ehrhart_quasipolynomial_raw"
                        ),
                        "raw_ehrhart_series": normaliz.get("ehrhart_series_raw"),
                    }
                    for field, expected_value in typed_expected.items():
                        if typed_n.get(field) != expected_value:
                            errors.append(
                                f"typed Normaliz {fixture_id}.{field} differs from report"
                            )
                except Exception as exc:
                    errors.append(f"report {fixture_id} Normaliz raw data is invalid: {exc}")

            input_artifact = report.get("input_artifact")
            input_entry = input_entries.get(fixture_id)
            if not isinstance(input_artifact, dict) or input_entry is None:
                errors.append(f"report {fixture_id} input artifact is missing")
            else:
                input_path = evidence_root / input_entry["logical_path"]
                input_doc = load_json(input_path)
                if input_entry["sha256"] != input_artifact.get("file_sha256"):
                    errors.append(f"fixture {fixture_id} hive input file hash is not linked")
                if sha256_json(input_doc) != input_artifact.get("canonical_payload_sha256"):
                    errors.append(f"fixture {fixture_id} hive canonical payload hash is wrong")
                if Path(str(input_artifact.get("path", ""))).name != input_path.name:
                    errors.append(f"fixture {fixture_id} hive input path linkage is wrong")
                for field in ("n", "lam", "mu", "nu"):
                    if input_doc.get(field) != definition.get(field):
                        errors.append(f"fixture {fixture_id} hive input {field} differs from definition")
                if typed_n.get("input_canonical_payload_sha256") != input_artifact.get(
                    "canonical_payload_sha256"
                ):
                    errors.append(f"typed Normaliz {fixture_id} input payload hash is wrong")

            cli = report.get("normaliz_cli")
            if cli is None:
                if typed_n.get("normaliz_cli_output_sha256") is not None:
                    errors.append(f"fixture {fixture_id} unexpectedly claims a CLI output")
            else:
                expected_cli_ids.add(fixture_id)
                raw_entry = raw_output_entries.get(fixture_id)
                normaliz_input_entry = normaliz_input_entries.get(fixture_id)
                if (
                    not isinstance(cli, dict)
                    or cli.get("exit") != 0
                    or cli.get("output_present") is not True
                    or raw_entry is None
                    or normaliz_input_entry is None
                    or raw_entry["sha256"] != cli.get("output_sha256")
                    or typed_n.get("normaliz_cli_output_sha256") != cli.get("output_sha256")
                    or Path(str(cli.get("output_path", ""))).name
                    != Path(raw_entry["logical_path"]).name
                    or Path(str(input_artifact.get("normaliz_input_path", ""))).name
                    != Path(normaliz_input_entry["logical_path"]).name
                ):
                    errors.append(f"fixture {fixture_id} Normaliz CLI artifacts are not linked")
        if set(normaliz_input_entries) != expected_cli_ids:
            errors.append("Normaliz .in artifact set differs from reports")
        if set(raw_output_entries) != expected_cli_ids:
            errors.append("Normaliz raw-output artifact set differs from reports")
        if set(evaluator_maps["lrcalc-interp"]) != definition_ids:
            errors.append("lrcalc typed fixture set differs from fixed definitions")
        if set(evaluator_maps["normaliz-ehrhart"]) != definition_ids:
            errors.append("Normaliz typed fixture set differs from fixed definitions")
    except Exception as exc:
        errors.append(f"cannot validate fixed fixture evidence chain: {exc}")
    summary_ok = _validate_e2_summary(
        evidence_root,
        selected,
        grouped,
        policy,
        set(expected_coverage_by_id),
        collector,
    )
    if not summary_ok:
        errors.append("E2 summary/tool-version chain failed")
    collector.check(
        "P1.FIXTURE_EVIDENCE_CHAIN",
        not errors,
        "policy-pinned definitions, reports, hive inputs, raw outputs, and adapters are linked"
        if not errors
        else "; ".join(errors),
    )
    return expected_coverage_by_id if not errors else None


def _validate_e2_summary(
    evidence_root: Path,
    selected: dict[str, dict[str, Any]],
    grouped: dict[str, list[dict[str, Any]]],
    policy: dict[str, Any],
    expected_fixture_ids: set[str],
    collector: _Collector,
) -> bool:
    errors: list[str] = []
    try:
        summary = load_json(evidence_root / selected["e2-fixture-summary"]["logical_path"])
        sidecar_path = evidence_root / selected["e2-summary-sidecar"]["logical_path"]
        sidecar_tokens = sidecar_path.read_text(encoding="utf-8").split()
        if not isinstance(summary, dict) or summary.get("schema_version") != 1:
            raise ValueError("E2 summary schema is invalid")
        core = {key: value for key, value in summary.items() if key != "canonical_payload_sha256"}
        direct_digest = sha256_json(core)
        if summary.get("canonical_payload_sha256") != direct_digest:
            errors.append("E2 summary canonical payload hash is inconsistent")
        if not sidecar_tokens or sidecar_tokens[0] != direct_digest:
            errors.append("E2 summary sidecar is not linked")
        if summary.get("tool_versions") != policy["tools"]:
            errors.append("E2 summary tool versions differ from policy")
        expected_count = len(expected_fixture_ids)
        if (
            summary.get("gate") != "E2 fixed hive fixtures"
            or summary.get("all_pass") is not True
            or summary.get("fixture_count") != expected_count
            or summary.get("passed") != expected_count
            or summary.get("failed") != 0
        ):
            errors.append("E2 summary counts/status do not prove an all-pass fixture run")
        adapter = summary.get("controller_adapter")
        if not isinstance(adapter, dict) or adapter.get("all_agree") is not True:
            errors.append("E2 summary controller adapter did not agree")
        else:
            for field, role in (
                ("fixture_agreement_sha256", "fixture-agreement"),
                ("lrcalc_evaluator_sha256", "fixture-evaluator-lrcalc"),
                ("normaliz_evaluator_sha256", "fixture-evaluator-normaliz"),
            ):
                if adapter.get(field) != selected[role]["sha256"]:
                    errors.append(f"E2 summary adapter field {field} is not role-bound")
        report_entries = _entries_by_fixture_id(
            grouped.get("fixture-comparison-report", []), ".report.json", errors
        )
        summary_reports = summary.get("reports")
        if not isinstance(summary_reports, list):
            errors.append("E2 summary report ledger is missing")
        else:
            ledger = {
                item.get("id"): item
                for item in summary_reports
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            }
            if set(ledger) != expected_fixture_ids or len(ledger) != len(summary_reports):
                errors.append("E2 summary report ledger fixture IDs are not exact")
            for fixture_id in expected_fixture_ids:
                item = ledger.get(fixture_id, {})
                entry = report_entries.get(fixture_id)
                if (
                    item.get("pass") is not True
                    or item.get("exception") is not None
                    or entry is None
                    or item.get("report_sha256") != entry["sha256"]
                    or Path(str(item.get("report_path", ""))).name
                    != Path(entry["logical_path"]).name
                ):
                    errors.append(f"E2 summary report ledger is not linked for {fixture_id}")
    except Exception as exc:
        errors.append(f"cannot validate E2 summary: {exc}")
    collector.check(
        "P1.E2_SUMMARY",
        not errors,
        "E2 all-pass summary, sidecar, report ledger, adapters, and tool versions are linked"
        if not errors
        else "; ".join(errors),
    )
    return not errors


def _derived_coverage_tags(definition: dict[str, Any]) -> list[str]:
    tags = {
        "boundary.lambda",
        "boundary.mu",
        "boundary.nu",
        "rhombus.type-a",
        "rhombus.type-b",
        "rhombus.type-c",
    }
    coefficient = definition.get("expected_lr_at_1")
    dimension = definition.get("expected_affine_dimension")
    if coefficient == 0:
        tags.add("coefficient.zero")
    elif coefficient == 1:
        tags.add("coefficient.one")
    elif isinstance(coefficient, int) and coefficient > 1:
        tags.add("coefficient.multiple")
    if dimension == -1:
        tags.update({"dimension.empty", "dimension.degenerate"})
    elif dimension == 0:
        tags.add("dimension.zero")
        if definition.get("n", 0) > 2:
            tags.add("dimension.degenerate")
    elif isinstance(dimension, int) and dimension > 0:
        tags.add("dimension.positive")
    if definition.get("id") == "campaign_degree6_anchor":
        tags.add("anchor.degree6")
    return sorted(tags)


def _entries_by_fixture_id(
    entries: list[dict[str, Any]], suffix: str, errors: list[str]
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for entry in entries:
        name = Path(entry["logical_path"]).name
        if not name.endswith(suffix) or len(name) <= len(suffix):
            errors.append(f"role artifact has unexpected filename {name!r} for suffix {suffix!r}")
            continue
        fixture_id = name[: -len(suffix)]
        if fixture_id in result:
            errors.append(f"duplicate role artifact for fixture {fixture_id}")
        result[fixture_id] = entry
    return result


def _validate_positive_sample_map(
    samples: Any, poly: list[str], degree_bound: int
) -> None:
    if not isinstance(samples, dict) or not samples:
        raise ValueError("sample map is empty")
    domain: list[int] = []
    for raw_n, count in samples.items():
        n = int(raw_n)
        if str(n) != raw_n or n < 1 or not isinstance(count, int) or isinstance(count, bool):
            raise ValueError(f"malformed sample {raw_n!r}")
        value = sum(Fraction(coefficient) * n**degree for degree, coefficient in enumerate(poly))
        if value.denominator != 1 or int(value) != count:
            raise ValueError(f"sample N={n} differs from polynomial")
        domain.append(n)
    domain.sort()
    if domain != list(range(1, domain[-1] + 1)) or domain[-1] < degree_bound + 2:
        raise ValueError("sample domain must be consecutive from 1 through at least B+2")


def _validate_fixtures(
    path: Path,
    policy: dict[str, Any],
    expected_artifact_hashes: dict[str, str],
    evaluator_maps: dict[str, dict[str, list[str]]],
    expected_coverage_by_id: dict[str, list[str]],
    collector: _Collector,
) -> None:
    try:
        report = load_json(path)
        if not isinstance(report, dict):
            raise ValueError("fixture report must be an object")
        collector.check(
            "P1.FIXTURE_SCHEMA",
            report.get("schema_version") == FIXTURE_REPORT_SCHEMA,
            f"fixture schema is {report.get('schema_version')!r}",
        )
        fixtures = report.get("fixtures")
        if not isinstance(fixtures, list):
            raise ValueError("fixtures must be a list")
        expected = policy["fixtures"]
        collector.check(
            "P1.FIXTURE_COUNT",
            len(fixtures) >= expected["min_count"]
            and report.get("fixture_count") == len(fixtures),
            f"found {len(fixtures)} fixtures; minimum is {expected['min_count']}",
        )
        collector.check(
            "P1.FIXTURE_TOPLEVEL_AGREEMENT",
            report.get("all_agree") is True,
            f"all_agree is {report.get('all_agree')!r}",
        )
        ids: set[str] = set()
        coverage: set[str] = set()
        records_ok = True
        record_errors: list[str] = []
        expected_names = set(expected["evaluator_names"])
        for index, fixture in enumerate(fixtures):
            prefix = f"fixture[{index}]"
            if not isinstance(fixture, dict):
                records_ok = False
                record_errors.append(f"{prefix} is not an object")
                continue
            fixture_id = fixture.get("id")
            if not isinstance(fixture_id, str) or not fixture_id or fixture_id in ids:
                records_ok = False
                record_errors.append(f"{prefix} has missing/duplicate id")
            else:
                ids.add(fixture_id)
            tags = fixture.get("coverage")
            if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
                records_ok = False
                record_errors.append(f"{prefix}.coverage is invalid")
            else:
                coverage.update(tags)
                if sorted(set(tags)) != expected_coverage_by_id.get(fixture_id):
                    records_ok = False
                    record_errors.append(
                        f"{prefix}.coverage is not derived exactly from pinned fixture facts"
                    )
            evaluators = fixture.get("evaluators")
            if not isinstance(evaluators, list) or len(evaluators) != 2:
                records_ok = False
                record_errors.append(f"{prefix} must contain exactly two evaluators")
                continue
            names = {item.get("name") for item in evaluators if isinstance(item, dict)}
            if names != expected_names:
                records_ok = False
                record_errors.append(f"{prefix} evaluator names are {sorted(map(str, names))}")
            polys: list[list[str]] = []
            evaluator_artifact_hashes: list[str] = []
            for evaluator in evaluators:
                if not isinstance(evaluator, dict):
                    records_ok = False
                    record_errors.append(f"{prefix} evaluator is not an object")
                    continue
                raw_poly = evaluator.get("poly")
                parsed_poly: list[str] | None = None
                if not isinstance(raw_poly, list) or not raw_poly:
                    records_ok = False
                    record_errors.append(f"{prefix} evaluator poly is empty/invalid")
                    continue
                try:
                    parsed_poly = [canonical_fraction(value) for value in raw_poly]
                    polys.append(parsed_poly)
                except Exception as exc:
                    records_ok = False
                    record_errors.append(f"{prefix} has invalid polynomial: {exc}")
                artifact_hash = evaluator.get("artifact_sha256")
                evaluator_name = evaluator.get("name")
                if (
                    not is_sha256(artifact_hash)
                    or artifact_hash != expected_artifact_hashes.get(evaluator_name)
                ):
                    records_ok = False
                    record_errors.append(
                        f"{prefix} {evaluator_name!r} hash is not bound to its typed role"
                    )
                else:
                    evaluator_artifact_hashes.append(artifact_hash)
                if (
                    isinstance(evaluator_name, str)
                    and fixture_id in evaluator_maps.get(evaluator_name, {})
                    and parsed_poly is not None
                ):
                    if parsed_poly != evaluator_maps[evaluator_name][fixture_id]:
                        records_ok = False
                        record_errors.append(
                            f"{prefix} {evaluator_name!r} poly differs from typed artifact"
                        )
                elif isinstance(evaluator_name, str):
                    records_ok = False
                    record_errors.append(
                        f"{prefix} {evaluator_name!r} fixture id is absent from typed artifact"
                    )
            if len(set(evaluator_artifact_hashes)) != 2:
                records_ok = False
                record_errors.append(f"{prefix} evaluators do not have distinct raw artifacts")
            if len(polys) != 2 or polys[0] != polys[1] or fixture.get("agreement") is not True:
                records_ok = False
                record_errors.append(f"{prefix} evaluator polynomials do not agree exactly")
        collector.check(
            "P1.FIXTURE_RECORDS",
            records_ok,
            "all fixture records are exact and independently manifested"
            if records_ok
            else "; ".join(record_errors),
        )
        missing = sorted(set(expected["required_coverage"]) - coverage)
        collector.check(
            "P1.FIXTURE_COVERAGE",
            not missing,
            "all required fixture coverage tags present"
            if not missing
            else f"missing coverage tags: {', '.join(missing)}",
        )
        adapter_ids = {fixture.get("id") for fixture in fixtures if isinstance(fixture, dict)}
        typed_ids = set(evaluator_maps["lrcalc-interp"])
        collector.check(
            "P1.FIXTURE_ADAPTER_ID_SET",
            adapter_ids == typed_ids,
            "agreement adapter and both typed evaluators cover exactly the same fixtures"
            if adapter_ids == typed_ids
            else "agreement adapter fixture-id set differs from typed evaluator artifacts",
        )
    except Exception as exc:  # fail closed on malformed scientific evidence
        collector.check("P1.FIXTURE_PARSE", False, f"cannot validate fixture evidence: {exc}")
