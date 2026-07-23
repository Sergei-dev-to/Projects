"""Read-only, fail-closed pre-P2 readiness audit."""

from __future__ import annotations

import json
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .atomic import load_json
from .canonical import is_sha256, sha256_json
from .errors import ValidationError
from .gate import validate_p1_gate
from .pilot import verify_pilot
from .state import validate_state

READINESS_SCHEMA = "lr-readiness-report/v1"

REQUIRED_READINESS_CHECK_CODES = frozenset(
    {
        "REPO.REQUIRED_FILES",
        "ENV.SHAPE",
        "SCHEMAS.CATALOG",
        "BASELINE.PAYLOAD",
        "BASELINE.EMBEDDED_HASH",
        "BASELINE.SIDECAR",
        "TOOLS.PROBE",
        "P1.GATE",
        "PILOT.RESUME",
        "STATE.ADJUDICATION",
        "P2.BOX_ESTIMATES",
        "P2.NAIVE_BOX_FEASIBILITY",
    }
)

REQUIRED_SCHEMA_FILES = (
    "artifact-manifest-v1.schema.json",
    "campaign-state-v1.schema.json",
    "p1-fixture-agreement-v1.schema.json",
    "p1-gate-policy-v1.schema.json",
    "p1-gate-report-v1.schema.json",
    "resume-pilot-v1.schema.json",
    "readiness-report-v1.schema.json",
)


@dataclass
class _Audit:
    checks: list[dict[str, Any]]
    warnings: list[str]

    def check(self, code: str, passed: bool, detail: str, *, required: bool = True) -> None:
        self.checks.append(
            {"code": code, "passed": bool(passed), "required": required, "detail": detail}
        )

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def audit_readiness(
    *,
    repo_root: Path,
    checked_at_utc: str,
    probe_tools: bool = True,
    p1_evidence_root: Path | None = None,
    p1_manifest_path: Path | None = None,
    pilot_dir: Path | None = None,
    state_path: Path | None = None,
) -> dict[str, Any]:
    """Audit launch prerequisites without modifying any campaign artifact."""

    if not isinstance(checked_at_utc, str) or not checked_at_utc.strip():
        raise ValidationError("checked_at_utc must be a non-empty string")

    repo_root = Path(repo_root).resolve()
    audit = _Audit([], [])
    required_docs = (
        "ORCHESTRATION.md",
        "CAMPAIGN_LR_POSITIVITY.md",
        "DECISION_LOG.md",
        "run/env.json",
    )
    missing_docs = [name for name in required_docs if not (repo_root / name).is_file()]
    audit.check(
        "REPO.REQUIRED_FILES",
        not missing_docs,
        "required run-book files present"
        if not missing_docs
        else f"missing: {', '.join(missing_docs)}",
    )

    env: dict[str, Any] | None = None
    try:
        env_value = load_json(repo_root / "run" / "env.json")
        if not isinstance(env_value, dict):
            raise ValueError("env.json is not an object")
        env = env_value
        required_env = (
            ("campaign", env.get("campaign")),
            ("compute_envelope", env.get("compute_envelope")),
            ("execution_environment", env.get("execution_environment")),
            ("tool_versions", env.get("tool_versions")),
            ("parity_baseline", env.get("parity_baseline")),
        )
        missing = [name for name, value in required_env if value in (None, "", {})]
        audit.check(
            "ENV.SHAPE",
            not missing,
            "environment envelope has required fields"
            if not missing
            else f"missing/empty env fields: {', '.join(missing)}",
        )
    except Exception as exc:
        audit.check("ENV.SHAPE", False, f"cannot validate run/env.json: {exc}")

    _audit_schemas(repo_root, audit)
    if env is not None:
        _audit_baseline(repo_root, env, audit)
        _audit_tools(repo_root, env, audit, probe_tools)
    else:
        audit.check("BASELINE.PAYLOAD", False, "not checked because env.json is invalid")
        audit.check("TOOLS.PROBE", False, "not checked because env.json is invalid")

    _audit_p1_gate(p1_evidence_root, p1_manifest_path, checked_at_utc, audit)
    _audit_pilot(pilot_dir, audit)
    _audit_state(state_path, audit)
    planning_inputs = _audit_box_estimates(repo_root, audit)

    blockers = [
        check["code"]
        for check in audit.checks
        if check["required"] and not check["passed"]
    ]
    return {
        "schema_version": READINESS_SCHEMA,
        "checked_at_utc": checked_at_utc,
        "repo_root": str(repo_root),
        "ready_for_p2_adjudication": not blockers,
        "p2_launch_authorized": False,
        "checks": audit.checks,
        "blockers": blockers,
        "warnings": audit.warnings,
        "planning_inputs": planning_inputs,
        "next_action": (
            "integrator may adjudicate whether to authorize P2; this audit never starts it"
            if not blockers
            else "resolve blockers; do not start P2"
        ),
    }


def validate_readiness_report(report: Any) -> list[str]:
    """Validate full check coverage and all derived pass/blocker relationships."""

    errors: list[str] = []
    if not isinstance(report, dict):
        return ["readiness report must be an object"]
    if report.get("schema_version") != READINESS_SCHEMA:
        errors.append("unsupported readiness schema")
    if not isinstance(report.get("checked_at_utc"), str) or not report["checked_at_utc"].strip():
        errors.append("checked_at_utc must be a non-empty string")
    if not isinstance(report.get("repo_root"), str) or not report["repo_root"].strip():
        errors.append("repo_root must be a non-empty string")
    if not isinstance(report.get("next_action"), str) or not report["next_action"].strip():
        errors.append("next_action must be a non-empty string")
    if report.get("p2_launch_authorized") is not False:
        errors.append("control-plane readiness must never authorize P2")
    checks = report.get("checks")
    codes: set[str] = set()
    failed_required: set[str] = set()
    if not isinstance(checks, list) or not checks:
        errors.append("readiness checks must be a non-empty list")
    else:
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{index}] must be an object")
                continue
            code = check.get("code")
            if not isinstance(code, str) or not code or code in codes:
                errors.append(f"checks[{index}] has missing/duplicate code")
                continue
            codes.add(code)
            if not isinstance(check.get("passed"), bool):
                errors.append(f"checks[{index}].passed must be boolean")
            if not isinstance(check.get("required"), bool):
                errors.append(f"checks[{index}].required must be boolean")
            if not isinstance(check.get("detail"), str):
                errors.append(f"checks[{index}].detail must be a string")
            if check.get("required") is True and check.get("passed") is False:
                failed_required.add(code)
        missing = REQUIRED_READINESS_CHECK_CODES - codes
        if missing:
            errors.append("readiness report lacks required checks: " + ", ".join(sorted(missing)))
        for required_code in REQUIRED_READINESS_CHECK_CODES & codes:
            record = next(check for check in checks if check.get("code") == required_code)
            if record.get("required") is not True:
                errors.append(f"required readiness check {required_code} was marked optional")
    blockers = report.get("blockers")
    if not isinstance(blockers, list) or not all(isinstance(code, str) for code in blockers):
        errors.append("blockers must be a string list")
        blockers_set: set[str] = set()
    else:
        blockers_set = set(blockers)
        if len(blockers_set) != len(blockers):
            errors.append("blockers contain duplicates")
    if blockers_set != failed_required:
        errors.append("blockers do not exactly equal failed required checks")
    ready = report.get("ready_for_p2_adjudication")
    if not isinstance(ready, bool):
        errors.append("ready_for_p2_adjudication must be boolean")
    elif ready != (not failed_required):
        errors.append("ready_for_p2_adjudication contradicts required checks")
    if not isinstance(report.get("warnings"), list) or not all(
        isinstance(item, str) for item in report.get("warnings", [])
    ):
        errors.append("warnings must be a string list")
    planning = report.get("planning_inputs")
    if not isinstance(planning, dict):
        errors.append("planning_inputs must be an object")
    elif "box_estimates_sha256" in planning and not is_sha256(
        planning.get("box_estimates_sha256")
    ):
        errors.append("box_estimates_sha256 must be a string")
    return errors


def _audit_schemas(repo_root: Path, audit: _Audit) -> None:
    schema_dir = repo_root / "run" / "schemas"
    errors: list[str] = []
    for name in REQUIRED_SCHEMA_FILES:
        path = schema_dir / name
        try:
            value = load_json(path)
            if not isinstance(value, dict) or "$schema" not in value or "$id" not in value:
                errors.append(f"{name}: missing $schema/$id")
        except Exception as exc:
            errors.append(f"{name}: {exc}")
    audit.check(
        "SCHEMAS.CATALOG",
        not errors,
        "all required schema documents parse"
        if not errors
        else "; ".join(errors),
    )


def _audit_baseline(repo_root: Path, env: dict[str, Any], audit: _Audit) -> None:
    try:
        policy = env["parity_baseline"]
        baseline = load_json(repo_root / policy["source"])
        triples = baseline["triples"]
        expected_hash = policy["triples_payload_sha256"]
        expected_count = policy["count"]
        actual_hash = sha256_json(triples)
        audit.check(
            "BASELINE.PAYLOAD",
            actual_hash == expected_hash and len(triples) == expected_count,
            f"payload sha256={actual_hash}, count={len(triples)}; "
            f"expected sha256={expected_hash}, count={expected_count}",
        )
        embedded = baseline.get("sha256")
        audit.check(
            "BASELINE.EMBEDDED_HASH",
            embedded == actual_hash,
            f"embedded={embedded!r}, computed={actual_hash}",
        )
        sidecar = (repo_root / "dryrun" / "frontier_baseline.sha256").read_text(
            encoding="utf-8"
        )
        sidecar_token = sidecar.split()[0] if sidecar.split() else ""
        audit.check(
            "BASELINE.SIDECAR",
            sidecar_token == actual_hash,
            f"sidecar={sidecar_token!r}, computed={actual_hash}",
        )
    except Exception as exc:
        audit.check("BASELINE.PAYLOAD", False, f"cannot validate parity baseline: {exc}")


def _audit_tools(
    repo_root: Path,
    env: dict[str, Any],
    audit: _Audit,
    probe_tools: bool,
) -> None:
    if not probe_tools:
        audit.check("TOOLS.PROBE", False, "tool probes disabled; versions are unverified")
        return
    try:
        execution = env["execution_environment"]
        versions = env["tool_versions"]
        python_entry = execution["python_entrypoint"]
        normaliz_entry = execution["normaliz_entrypoint"]
        commands = _tool_commands(repo_root, execution, python_entry, normaliz_entry)
        observations: dict[str, str] = {}
        failures: list[str] = []
        probes = {
            "python": (commands(python_entry, "--version"), str(versions["python"]).split("+")[0]),
            "lrcalc": (
                commands(
                    python_entry,
                    "-c",
                    "from importlib.metadata import version; import lrcalc; print(version('lrcalc'))",
                ),
                str(versions["lrcalc"]).split("+")[0],
            ),
            "pynormaliz": (
                commands(
                    python_entry,
                    "-c",
                    "from importlib.metadata import version; import PyNormaliz; print(version('PyNormaliz'))",
                ),
                str(versions["pynormaliz"]).split("+")[0],
            ),
            "normaliz": (
                commands(normaliz_entry, "--version"),
                str(versions["normaliz"]).split("+")[0],
            ),
        }
        for name, (command, expected_token) in probes.items():
            completed = subprocess.run(
                command,
                cwd=repo_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=20,
                check=False,
            )
            output = completed.stdout.strip()
            observations[name] = output[:500]
            if completed.returncode != 0:
                failures.append(f"{name} exit={completed.returncode}: {output[:160]}")
            elif expected_token and expected_token.lower() not in output.lower():
                failures.append(f"{name} output lacks expected token {expected_token!r}: {output[:160]}")
        audit.check(
            "TOOLS.PROBE",
            not failures,
            f"observed {json.dumps(observations, sort_keys=True)}"
            if not failures
            else "; ".join(failures),
        )
    except Exception as exc:
        audit.check("TOOLS.PROBE", False, f"tool probing failed: {exc}")


def _tool_commands(
    repo_root: Path,
    execution: dict[str, Any],
    python_entry: str,
    normaliz_entry: str,
):
    del python_entry, normaliz_entry
    if os.name != "nt":
        return lambda *parts: list(parts)
    platform = str(execution.get("platform", ""))
    match = re.search(r"Ubuntu-[0-9.]+", platform)
    if not match:
        raise ValueError(f"cannot derive WSL distribution from platform {platform!r}")
    distro = match.group(0)
    converted = subprocess.run(
        ["wsl.exe", "-d", distro, "--", "wslpath", "-a", str(repo_root)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=20,
        check=False,
    )
    if converted.returncode != 0 or not converted.stdout.strip():
        raise ValueError(f"wslpath failed: {converted.stdout.strip()}")
    linux_root = converted.stdout.strip()
    return lambda *parts: ["wsl.exe", "-d", distro, "--cd", linux_root, "--", *parts]


def _audit_p1_gate(
    evidence_root: Path | None,
    manifest_path: Path | None,
    checked_at_utc: str,
    audit: _Audit,
) -> None:
    if evidence_root is None or manifest_path is None:
        audit.check(
            "P1.GATE",
            False,
            "P1 evidence root and manifest were not supplied for fresh validation",
        )
        return
    try:
        report = validate_p1_gate(
            evidence_root=evidence_root,
            manifest=load_json(manifest_path),
            checked_at_utc=checked_at_utc,
        )
        audit.check(
            "P1.GATE",
            report["passed"],
            "fresh P1 gate validation passed"
            if report["passed"]
            else f"fresh P1 gate failed: {report['failures']}",
        )
    except Exception as exc:
        audit.check("P1.GATE", False, f"cannot validate P1 gate: {exc}")


def _audit_pilot(pilot_dir: Path | None, audit: _Audit) -> None:
    if pilot_dir is None:
        audit.check("PILOT.RESUME", False, "deterministic pilot directory was not supplied")
        return
    try:
        result = verify_pilot(pilot_dir, require_complete=True)
        audit.check(
            "PILOT.RESUME",
            result["valid"] and result["complete"],
            f"verified deterministic prefix {result['prefix_sha256']}",
        )
    except Exception as exc:
        audit.check("PILOT.RESUME", False, f"pilot validation failed: {exc}")


def _audit_state(state_path: Path | None, audit: _Audit) -> None:
    if state_path is None:
        audit.check("STATE.ADJUDICATION", False, "campaign state path was not supplied")
        return
    try:
        state = load_json(state_path)
        validate_state(state)
        eligible = state["phase_state"] in {"PILOT_COMPLETE", "P2_AWAITING_AUTHORIZATION"}
        audit.check(
            "STATE.ADJUDICATION",
            eligible,
            f"validated revision {state['revision']} in phase {state['phase_state']}",
        )
    except Exception as exc:
        audit.check("STATE.ADJUDICATION", False, f"state validation failed: {exc}")


def _audit_box_estimates(repo_root: Path, audit: _Audit) -> dict[str, Any]:
    path = repo_root / "run" / "box_estimates.json"
    if not path.is_file():
        audit.check("P2.BOX_ESTIMATES", False, "run/box_estimates.json is missing")
        audit.check(
            "P2.NAIVE_BOX_FEASIBILITY",
            False,
            "no box estimates available; flat P2 launch is not justified",
        )
        return {"box_estimates": None}
    try:
        value = load_json(path)
        boxes = value.get("boxes") if isinstance(value, dict) else None
        if not isinstance(boxes, list) or {box.get("box") for box in boxes} != {
            "B1",
            "B2",
            "B3",
            "B4",
        }:
            raise ValueError("expected exactly B1-B4 estimate records")
        summarized: list[dict[str, Any]] = []
        for box in boxes:
            record = {
                "box": box["box"],
                "method": box["method"],
                "partition_count": box["partition_count"],
                "unordered_pair_count_before_nu_enumeration": box["unordered_pair_count"],
                "quantity": box["quantity"],
            }
            if box["method"] == "exact":
                record["support_compatible_pre_horn_upper_bound"] = box[
                    "support_compatible_triples"
                ]
                record["estimate_status"] = "exact upper bound, not evaluated triple count"
            else:
                record["estimated_support_compatible_pre_horn"] = box[
                    "estimated_support_compatible_triples"
                ]
                record["approx_95pct_interval"] = box["approx_95pct_interval"]
                record["estimate_status"] = "sample estimate, not completeness certificate"
            summarized.append(record)
        audit.check(
            "P2.BOX_ESTIMATES",
            True,
            "loaded B1-B4 planning inputs with exact/sample labels preserved",
        )
        b1 = next(item for item in summarized if item["box"] == "B1")
        b4 = next(item for item in summarized if item["box"] == "B4")
        audit.check(
            "P2.NAIVE_BOX_FEASIBILITY",
            False,
            "naive flat P2 is not launch-ready: B1 has an exact pre-Horn upper bound of "
            f"{b1['support_compatible_pre_horn_upper_bound']:,} support-compatible triples; "
            "B4 has a sampled estimate of "
            f"{b4['estimated_support_compatible_pre_horn']:,}. A proved prefilter, box redesign, "
            "or measured-throughput feasibility case is required.",
        )
        audit.warn(
            "The box figures are planning inputs only: B1-B3 are exact support-compatible "
            "pre-Horn upper bounds; B4 is a sample estimate with an approximate interval. "
            "None is a canonical/evaluated triple count or a completeness certificate."
        )
        audit.warn(
            "Unordered (lambda,mu) pair counts before nu enumeration are B1=25,878, "
            "B2=1,145,341, B3=265,356, B4=71,574,630."
        )
        return {
            "box_estimates_source": "run/box_estimates.json",
            "box_estimates_sha256": sha256_json(value),
            "boxes": summarized,
        }
    except Exception as exc:
        audit.check("P2.BOX_ESTIMATES", False, f"box estimate validation failed: {exc}")
        audit.check(
            "P2.NAIVE_BOX_FEASIBILITY",
            False,
            "box estimates invalid; flat P2 launch is not justified",
        )
        return {"box_estimates_error": str(exc)}
