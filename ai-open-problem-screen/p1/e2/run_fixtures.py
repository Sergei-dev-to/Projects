#!/usr/bin/env python3
"""Run the fixed E2 hive/Normaliz fixture gate and preserve raw artifacts."""

from __future__ import annotations

import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

try:
    from .hive_e2 import (
        build_hive_polytope,
        canonical_json_bytes,
        evaluate_polynomial,
        evaluate_with_normaliz,
        interpolate_polynomial,
        load_fixtures,
        lr_count,
    )
except ImportError:  # direct script execution
    from hive_e2 import (  # type: ignore
        build_hive_polytope,
        canonical_json_bytes,
        evaluate_polynomial,
        evaluate_with_normaliz,
        interpolate_polynomial,
        load_fixtures,
        lr_count,
    )

from fractions import Fraction


HERE = Path(__file__).resolve().parent
DEFAULT_FIXTURES = HERE / "fixtures.json"
DEFAULT_REPORTS = HERE / "reports"


def _atomic_write(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8", newline="\n")
    temporary.replace(path)


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def _package_version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "installed-without-visible-package-metadata"


def _normaliz_version(executable: str) -> str:
    completed = subprocess.run(
        [executable, "--version"],
        text=True,
        capture_output=True,
        check=False,
    )
    first_line = (completed.stdout or completed.stderr).splitlines()
    return first_line[0].strip() if first_line else f"exit-{completed.returncode}"


def _one_variable_bounds(polytope: Any) -> dict[str, Any] | None:
    if polytope.ambient_dimension != 1:
        return None
    lower: Fraction | None = None
    upper: Fraction | None = None
    lower_witnesses: list[dict[str, Any]] = []
    upper_witnesses: list[dict[str, Any]] = []
    for rhombus in polytope.rhombi:
        coefficient = rhombus.form.coefficients[0]
        constant = rhombus.form.constant
        if coefficient > 0:
            candidate = Fraction(-constant, coefficient)
            if lower is None or candidate > lower:
                lower = candidate
                lower_witnesses = []
            if candidate == lower:
                lower_witnesses.append(
                    {"family": rhombus.family, "base": list(rhombus.base), "row": rhombus.form.row()}
                )
        elif coefficient < 0:
            candidate = Fraction(-constant, coefficient)
            if upper is None or candidate < upper:
                upper = candidate
                upper_witnesses = []
            if candidate == upper:
                upper_witnesses.append(
                    {"family": rhombus.family, "base": list(rhombus.base), "row": rhombus.form.row()}
                )
    return {
        "variable": polytope.variable_names[0],
        "lower_bound": None if lower is None else str(lower),
        "upper_bound": None if upper is None else str(upper),
        "lower_bound_witnesses": lower_witnesses,
        "upper_bound_witnesses": upper_witnesses,
    }


def _run_cli(executable: str, project: Path) -> dict[str, Any]:
    # Do not request Normaliz's optional .gen/.inv/.cst files here.  Debian's
    # Normaliz 3.10.2 aborts in Matrix::append after completing some bounded
    # inhomogeneous computations when --files is combined with this goal set.
    # The ordinary invocation always writes the complete, replayable .out file.
    command = [executable, "--BigInt", str(project)]
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    output_path = project.with_suffix(".out")
    output_text = output_path.read_text(encoding="utf-8") if output_path.exists() else None
    return {
        "command": command,
        "exit": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "output_path": str(output_path),
        "output_sha256": (
            hashlib.sha256(output_text.encode("utf-8")).hexdigest()
            if output_text is not None
            else None
        ),
        "output_present": output_text is not None,
    }


def _record_check(checks: list[dict[str, Any]], name: str, actual: Any, expected: Any) -> None:
    checks.append(
        {"name": name, "actual": actual, "expected": expected, "pass": actual == expected}
    )


def run_fixture(
    fixture: dict[str, Any],
    reports_dir: Path,
    normaliz_executable: str,
    run_cli: bool,
) -> dict[str, Any]:
    fixture_id = fixture["id"]
    polytope = build_hive_polytope(
        fixture["lam"], fixture["mu"], fixture["nu"], n=fixture["n"]
    )
    input_dict = polytope.input_dict()
    input_json_path = reports_dir / "inputs" / f"{fixture_id}.hive.json"
    input_json_text = _json_text(input_dict)
    _atomic_write(input_json_path, input_json_text)

    normaliz_input_path: Path | None = None
    cli_result: dict[str, Any] | None = None
    if polytope.ambient_dimension:
        normaliz_input_path = reports_dir / "normaliz" / f"{fixture_id}.in"
        _atomic_write(normaliz_input_path, polytope.normaliz_input_text())
        if run_cli:
            cli_result = _run_cli(normaliz_executable, normaliz_input_path.with_suffix(""))

    e2 = evaluate_with_normaliz(polytope)
    expected_poly = [Fraction(value) for value in fixture["expected_polynomial"]]
    # Interpolate lrcalc independently at positive stretches using the universal
    # hive-dimension degree bound, then reserve one further point for validation.
    degree_bound = polytope.ambient_dimension
    max_stretch = max(3, degree_bound + 2)
    lrcalc_counts = {
        str(stretch): lr_count(
            fixture["lam"], fixture["mu"], fixture["nu"], stretch
        )
        for stretch in range(1, max_stretch + 1)
    }
    expected_counts = {
        str(stretch): int(evaluate_polynomial(expected_poly, stretch))
        for stretch in range(1, max_stretch + 1)
    }
    interpolation_samples = {
        stretch: lrcalc_counts[str(stretch)]
        for stretch in range(1, degree_bound + 2)
    }
    interpolated_poly = interpolate_polynomial(interpolation_samples)
    interpolated_poly_strings = [str(value) for value in interpolated_poly]
    interpolation_verified = all(
        evaluate_polynomial(interpolated_poly, stretch) == lrcalc_counts[str(stretch)]
        for stretch in range(1, max_stretch + 1)
    )

    checks: list[dict[str, Any]] = []
    _record_check(
        checks,
        "three rhombus families have n(n-1)/2 members each",
        input_dict["rhombus_family_counts"],
        {
            "east_north": polytope.expected_rhombi_per_family,
            "north_northwest": polytope.expected_rhombi_per_family,
            "northwest_west": polytope.expected_rhombi_per_family,
        },
    )
    _record_check(
        checks,
        "Normaliz canonical polynomial matches fixture",
        e2["canonical_polynomial"],
        fixture["expected_polynomial"],
    )
    _record_check(
        checks,
        "Normaliz affine dimension matches fixture",
        e2["affine_dimension"],
        fixture["expected_affine_dimension"],
    )
    _record_check(
        checks,
        "Normaliz lattice count at N=1 matches fixture",
        e2["number_lattice_points"],
        fixture["expected_lr_at_1"],
    )
    _record_check(
        checks,
        "lrcalc coefficient at N=1 matches fixture",
        lrcalc_counts["1"],
        fixture["expected_lr_at_1"],
    )
    _record_check(
        checks,
        "lrcalc positive-stretch counts match expected polynomial",
        lrcalc_counts,
        expected_counts,
    )
    _record_check(
        checks,
        "independently interpolated lrcalc polynomial matches fixture",
        interpolated_poly_strings,
        fixture["expected_polynomial"],
    )
    _record_check(
        checks,
        "lrcalc interpolation matches reserved positive-stretch checks",
        interpolation_verified,
        True,
    )
    _record_check(
        checks,
        "lrcalc-interp and normaliz-ehrhart agree exactly",
        interpolated_poly_strings,
        e2["canonical_polynomial"],
    )
    _record_check(
        checks,
        "Normaliz quasiperiod collapses to one polynomial",
        e2["period_collapses_to_one"],
        True,
    )

    bounds = _one_variable_bounds(polytope)
    if "audit" in fixture:
        if bounds is None:
            checks.append(
                {"name": "one-variable audit is available", "actual": None, "expected": fixture["audit"], "pass": False}
            )
        else:
            _record_check(checks, "audited variable", bounds["variable"], fixture["audit"]["variable"])
            _record_check(
                checks,
                "audited lower bound",
                bounds["lower_bound"],
                str(fixture["audit"]["lower_bound"]),
            )
            _record_check(
                checks,
                "audited upper bound",
                bounds["upper_bound"],
                str(fixture["audit"]["upper_bound"]),
            )
    if cli_result is not None:
        _record_check(checks, "Normaliz CLI exited successfully", cli_result["exit"], 0)
        _record_check(checks, "Normaliz CLI emitted raw .out", cli_result["output_present"], True)

    report = {
        "schema_version": 1,
        "fixture": fixture,
        "input_artifact": {
            "path": str(input_json_path),
            "file_sha256": hashlib.sha256(input_json_text.encode("utf-8")).hexdigest(),
            "canonical_payload_sha256": hashlib.sha256(
                canonical_json_bytes(input_dict)
            ).hexdigest(),
            "normaliz_input_path": None if normaliz_input_path is None else str(normaliz_input_path),
        },
        "one_variable_audit": bounds,
        "e2_normaliz": e2,
        "e1_lrcalc_interp": {
            "degree_bound": degree_bound,
            "interpolation_domain": [1, degree_bound + 1],
            "reserved_check_domain": [degree_bound + 2, max_stretch],
            "samples": {str(x): y for x, y in interpolation_samples.items()},
            "canonical_polynomial": interpolated_poly_strings,
            "all_available_samples_verified": interpolation_verified,
        },
        "e1_lrcalc_positive_stretches": lrcalc_counts,
        "expected_positive_stretches": expected_counts,
        "normaliz_cli": cli_result,
        "checks": checks,
        "pass": all(check["pass"] for check in checks),
    }
    report_path = reports_dir / "fixtures" / f"{fixture_id}.report.json"
    report["report_path"] = str(report_path)
    report_text = _json_text(report)
    _atomic_write(report_path, report_text)
    report["report_sha256"] = hashlib.sha256(report_text.encode("utf-8")).hexdigest()
    return report


def _coverage_tags(fixture_id: str) -> list[str]:
    common_geometry = [
        "boundary.lambda",
        "boundary.mu",
        "boundary.nu",
        "rhombus.type-a",
        "rhombus.type-b",
        "rhombus.type-c",
    ]
    fixture_tags = {
        "buch_n3_interval": ["dimension.positive", "coefficient.multiple"],
        "n3_degenerate_point": [
            "dimension.zero",
            "dimension.degenerate",
            "coefficient.one",
        ],
        "n3_empty_horn_failure": [
            "dimension.degenerate",
            "dimension.empty",
            "coefficient.zero",
        ],
        "n2_no_interior_vertex": ["dimension.zero", "coefficient.one"],
        "n4_asymmetric_degree2": ["dimension.positive", "coefficient.multiple"],
        "campaign_degree6_anchor": [
            "dimension.positive",
            "coefficient.multiple",
            "anchor.degree6",
        ],
    }
    return sorted(set(common_geometry + fixture_tags.get(fixture_id, [])))


def _write_controller_adapter(
    reports_dir: Path, reports: list[dict[str, Any]]
) -> dict[str, Any]:
    complete = [report for report in reports if report.get("pass") is True]
    complete.sort(key=lambda report: report["fixture"]["id"])

    lrcalc_artifact = {
        "schema_version": "lr-p1-lrcalc-fixture-evaluator/v1",
        "evaluator": "lrcalc-interp",
        "method": "positive-stretch lrcalc counts plus independent exact Lagrange interpolation",
        "fixtures": [
            {
                "id": report["fixture"]["id"],
                "degree_bound": report["e1_lrcalc_interp"]["degree_bound"],
                "samples": report["e1_lrcalc_positive_stretches"],
                "poly": report["e1_lrcalc_interp"]["canonical_polynomial"],
                "verified": report["e1_lrcalc_interp"]["all_available_samples_verified"],
            }
            for report in complete
        ],
    }
    normaliz_artifact = {
        "schema_version": "lr-p1-normaliz-fixture-evaluator/v1",
        "evaluator": "normaliz-ehrhart",
        "method": "explicit hive inhomogeneous inequalities plus PyNormaliz EhrhartQuasiPolynomial",
        "fixtures": [
            {
                "id": report["fixture"]["id"],
                "input_canonical_payload_sha256": report["input_artifact"][
                    "canonical_payload_sha256"
                ],
                "normaliz_cli_output_sha256": (
                    report["normaliz_cli"]["output_sha256"]
                    if report.get("normaliz_cli") is not None
                    else None
                ),
                "raw_ehrhart_quasipolynomial": report["e2_normaliz"][
                    "ehrhart_quasipolynomial_raw"
                ],
                "raw_ehrhart_series": report["e2_normaliz"]["ehrhart_series_raw"],
                "affine_dimension": report["e2_normaliz"]["affine_dimension"],
                "number_lattice_points": report["e2_normaliz"]["number_lattice_points"],
                "poly": report["e2_normaliz"]["canonical_polynomial"],
                "period_collapses_to_one": report["e2_normaliz"][
                    "period_collapses_to_one"
                ],
            }
            for report in complete
        ],
    }

    lrcalc_path = reports_dir / "lrcalc_interp_evaluator.json"
    normaliz_path = reports_dir / "normaliz_ehrhart_evaluator.json"
    lrcalc_text = _json_text(lrcalc_artifact)
    normaliz_text = _json_text(normaliz_artifact)
    _atomic_write(lrcalc_path, lrcalc_text)
    _atomic_write(normaliz_path, normaliz_text)
    lrcalc_hash = hashlib.sha256(lrcalc_text.encode("utf-8")).hexdigest()
    normaliz_hash = hashlib.sha256(normaliz_text.encode("utf-8")).hexdigest()

    fixture_records = []
    for report in complete:
        fixture_id = report["fixture"]["id"]
        e1_poly = report["e1_lrcalc_interp"]["canonical_polynomial"]
        e2_poly = report["e2_normaliz"]["canonical_polynomial"]
        fixture_records.append(
            {
                "id": fixture_id,
                "coverage": _coverage_tags(fixture_id),
                "evaluators": [
                    {
                        "name": "lrcalc-interp",
                        "poly": e1_poly,
                        "artifact_sha256": lrcalc_hash,
                    },
                    {
                        "name": "normaliz-ehrhart",
                        "poly": e2_poly,
                        "artifact_sha256": normaliz_hash,
                    },
                ],
                "agreement": e1_poly == e2_poly,
            }
        )
    adapter = {
        "schema_version": "lr-p1-fixture-agreement/v1",
        "fixture_count": len(fixture_records),
        "all_agree": (
            len(fixture_records) == len(reports)
            and all(record["agreement"] for record in fixture_records)
        ),
        "fixtures": fixture_records,
    }
    adapter_path = reports_dir / "fixture_agreement.json"
    adapter_text = _json_text(adapter)
    _atomic_write(adapter_path, adapter_text)
    adapter_hash = hashlib.sha256(adapter_text.encode("utf-8")).hexdigest()

    specs = {
        "evidence_root_hint": str(reports_dir),
        "artifact_specs": [
            {
                "logical_path": lrcalc_path.name,
                "role": "fixture-evaluator-lrcalc",
                "media_type": "application/json",
                "sha256": lrcalc_hash,
            },
            {
                "logical_path": normaliz_path.name,
                "role": "fixture-evaluator-normaliz",
                "media_type": "application/json",
                "sha256": normaliz_hash,
            },
            {
                "logical_path": adapter_path.name,
                "role": "fixture-agreement",
                "media_type": "application/json",
                "sha256": adapter_hash,
            },
        ],
    }
    _atomic_write(reports_dir / "controller_adapter_artifacts.json", _json_text(specs))
    return {
        "fixture_agreement_path": str(adapter_path),
        "fixture_agreement_sha256": adapter_hash,
        "lrcalc_evaluator_path": str(lrcalc_path),
        "lrcalc_evaluator_sha256": lrcalc_hash,
        "normaliz_evaluator_path": str(normaliz_path),
        "normaliz_evaluator_sha256": normaliz_hash,
        "all_agree": adapter["all_agree"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=DEFAULT_FIXTURES)
    parser.add_argument("--reports", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument("--normaliz", default="/usr/bin/normaliz")
    parser.add_argument(
        "--skip-cli",
        action="store_true",
        help="use PyNormaliz only; do not create independent CLI .out artifacts",
    )
    args = parser.parse_args(argv)

    fixtures = load_fixtures(args.fixtures)
    args.reports.mkdir(parents=True, exist_ok=True)
    reports: list[dict[str, Any]] = []
    for fixture in fixtures:
        try:
            report = run_fixture(
                fixture, args.reports, args.normaliz, run_cli=not args.skip_cli
            )
        except Exception as exc:
            failure = {
                "schema_version": 1,
                "fixture": fixture,
                "pass": False,
                "exception_type": type(exc).__name__,
                "exception": str(exc),
            }
            failure_path = args.reports / "fixtures" / f"{fixture['id']}.failure.json"
            _atomic_write(failure_path, _json_text(failure))
            reports.append(failure)
            print(f"FAIL {fixture['id']}: {type(exc).__name__}: {exc}", file=sys.stderr)
            continue
        reports.append(report)
        print(f"{'PASS' if report['pass'] else 'FAIL'} {fixture['id']}")

    adapter = _write_controller_adapter(args.reports, reports)

    summary_core = {
        "schema_version": 1,
        "gate": "E2 fixed hive fixtures",
        "tool_versions": {
            "python": sys.version.split()[0],
            "lrcalc": _package_version("lrcalc"),
            "pynormaliz": _package_version("PyNormaliz"),
            "normaliz": _normaliz_version(args.normaliz),
        },
        "fixture_count": len(fixtures),
        "passed": sum(bool(report.get("pass")) for report in reports),
        "failed": sum(not bool(report.get("pass")) for report in reports),
        "all_pass": bool(reports) and all(bool(report.get("pass")) for report in reports),
        "controller_adapter": adapter,
        "reports": [
            {
                "id": report["fixture"]["id"],
                "pass": bool(report.get("pass")),
                "report_path": report.get("report_path"),
                "report_sha256": report.get("report_sha256"),
                "exception": report.get("exception"),
            }
            for report in reports
        ],
    }
    digest = hashlib.sha256(canonical_json_bytes(summary_core)).hexdigest()
    summary = {**summary_core, "canonical_payload_sha256": digest}
    _atomic_write(args.reports / "fixtures_summary.json", _json_text(summary))
    _atomic_write(
        args.reports / "fixtures_summary.sha256",
        f"{digest}  fixtures_summary.json:summary_core (canonical payload)\n",
    )
    print(
        f"fixtures={summary['fixture_count']} passed={summary['passed']} "
        f"failed={summary['failed']} sha256={digest}"
    )
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
