"""Build and validate the content-addressed Phase-1 evidence bundle.

The repository root is the evidence root so the immutable dry-run baseline can
be manifested without copying it.  This command never changes campaign state;
it emits evidence for a separate integrator transition.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from p1.control.atomic import atomic_write_json
from p1.control.gate import validate_p1_gate
from p1.control.manifest import build_manifest


def artifact_specs(repo_root: Path) -> list[dict[str, str]]:
    fixed = [
        ("dryrun/frontier_baseline.json", "baseline-frontier"),
        ("dryrun/frontier_baseline.sha256", "baseline-payload-sidecar"),
        ("p1/e1/out/parity_report.json", "e1-parity-report"),
        ("p1/e1/out/actual_frontier.json", "e1-frontier-payload"),
        ("p1/e1/out/mismatches.json", "e1-mismatch-bundle"),
        ("p1/e1/out/artifact_manifest.json", "e1-artifact-manifest"),
        ("p1/e2/reports/fixture_agreement.json", "fixture-agreement"),
        ("p1/e2/fixtures.json", "fixture-definition-set"),
        ("p1/e2/reports/lrcalc_interp_evaluator.json", "fixture-evaluator-lrcalc"),
        ("p1/e2/reports/normaliz_ehrhart_evaluator.json", "fixture-evaluator-normaliz"),
        ("p1/e2/reports/fixtures_summary.json", "e2-fixture-summary"),
        ("p1/e2/reports/fixtures_summary.sha256", "e2-summary-sidecar"),
    ]
    specs = [
        {"logical_path": path, "role": role, "media_type": "application/json"}
        for path, role in fixed
    ]
    # Correct the two plain-text sidecars' media type.
    for spec in specs:
        if spec["logical_path"].endswith(".sha256"):
            spec["media_type"] = "text/plain"

    patterns = (
        ("p1/e2/reports/fixtures", "*.report.json", "fixture-comparison-report", "application/json"),
        ("p1/e2/reports/inputs", "*.hive.json", "explicit-hive-input", "application/json"),
        ("p1/e2/reports/normaliz", "*.in", "normaliz-input", "text/plain"),
        ("p1/e2/reports/normaliz", "*.out", "normaliz-raw-output", "text/plain"),
    )
    for directory, pattern, role, media_type in patterns:
        for path in sorted((repo_root / directory).glob(pattern)):
            specs.append(
                {
                    "logical_path": path.relative_to(repo_root).as_posix(),
                    "role": role,
                    "media_type": media_type,
                }
            )
    return specs


def integrate(repo_root: Path, *, checked_at_utc: str) -> tuple[dict, dict]:
    repo_root = repo_root.resolve()
    manifest = build_manifest(
        root=repo_root,
        artifact_specs=artifact_specs(repo_root),
        producer={
            "actor": "integrator",
            "writer_id": "codex-root",
            "tool": "p1.integrate_p1",
            "tool_version": "1.0.0",
        },
        scope="P1 oracle parity and fixed independent hive-fixture evidence",
        created_utc=checked_at_utc,
    )
    gate = validate_p1_gate(
        evidence_root=repo_root,
        manifest=manifest,
        checked_at_utc=checked_at_utc,
    )
    output_dir = repo_root / "run" / "p1"
    output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write_json(output_dir / "evidence_manifest.json", manifest)
    atomic_write_json(output_dir / "gate_report.json", gate)
    return manifest, gate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--at", required=True, help="UTC timestamp recorded in emitted artifacts")
    args = parser.parse_args()
    manifest, gate = integrate(args.repo_root, checked_at_utc=args.at)
    print(f"manifest={manifest['manifest_id']}")
    print(f"gate={'PASS' if gate['passed'] else 'FAIL'}")
    if not gate["passed"]:
        for failure in gate["failures"]:
            print(f"{failure['code']}: {failure['message']}")
    return 0 if gate["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
