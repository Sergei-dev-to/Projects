#!/usr/bin/env python3
"""Local protocol scan for the autonomous sector-parent benchmark.

This is meant for laptop-scale runs.  It scans coupling and time-window choices
at k=2 so the heavier k=3 campaign has a fixed protocol.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics as stats
from pathlib import Path

from scan_bose_hubbard_dos import DATADIR

import run_matrix_free_parent_benchmark as bench


def parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    return stats.mean(values) if values else float("nan")


def score_protocol(aggregate_rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str]:
    by_case = {str(row["comparison_case"]): row for row in aggregate_rows}
    sqrt = by_case["sqrt_scramble"]
    linear = by_case["linear_matched_scramble"]
    no_scramble = by_case["sqrt_no_scramble"]
    o1_emission = by_case.get("sqrt_o1_emission_scramble")

    sqrt_growth = float(sqrt["power_late_over_early_mean"])
    linear_growth = float(linear["power_late_over_early_mean"])
    no_scramble_growth = float(no_scramble["power_late_over_early_mean"])
    o1_drop = (
        float(o1_emission["mean_n_drop_mean"])
        if o1_emission is not None
        else float("nan")
    )
    sqrt_drop = float(sqrt["mean_n_drop_mean"])
    tvs = [
        float(sqrt["mean_flux_tv_to_thermal_x_mean"]),
        float(linear["mean_flux_tv_to_thermal_x_mean"]),
        float(no_scramble["mean_flux_tv_to_thermal_x_mean"]),
    ]
    drifts = [
        float(sqrt["max_energy_drift_mean"]),
        float(linear["max_energy_drift_mean"]),
        float(no_scramble["max_energy_drift_mean"]),
    ]
    # Larger is better.  The sqrt/linear contrast is the main diagnostic; the
    # no-scrambling contrast and absolute sqrt growth are secondary.
    contrast = (
        2.0 * (sqrt_growth - linear_growth)
        + (sqrt_growth - no_scramble_growth)
        + 0.5 * (sqrt_growth - 1.0)
    )
    if o1_emission is not None and o1_drop > 0.0:
        contrast += 0.5 * (sqrt_drop / o1_drop - 1.0)
    score = contrast - max(0.0, mean(tvs) - 0.2) * 2.0
    return {
        "sqrt_power_late_over_early": sqrt_growth,
        "linear_power_late_over_early": linear_growth,
        "no_scramble_power_late_over_early": no_scramble_growth,
        "sqrt_mean_n_drop": sqrt_drop,
        "o1_emission_mean_n_drop": o1_drop,
        "sqrt_over_o1_mean_n_drop": sqrt_drop / o1_drop if o1_drop > 0.0 else float("nan"),
        "sqrt_minus_linear_power_growth": sqrt_growth - linear_growth,
        "sqrt_minus_no_scramble_power_growth": sqrt_growth - no_scramble_growth,
        "mean_flux_tv": mean(tvs),
        "max_energy_drift_mean": max(drifts),
        "protocol_score": score,
    }


def run_one(args: argparse.Namespace, coupling: float, t_max: float) -> tuple[list[dict[str, float | int | str]], list[dict[str, float | int | str]], dict[str, float | int | str]]:
    prefix = f"{args.case_prefix}_g{coupling:g}_t{t_max:g}".replace(".", "p")
    run_args = argparse.Namespace(
        case_prefix=prefix,
        q=args.q,
        n_min=args.n_min,
        n_max=args.n_max,
        sqrt_alpha=args.sqrt_alpha,
        dos=args.dos,
        width_x=args.width_x,
        mode_x=args.mode_x,
        mode_copies=args.mode_copies,
        max_quanta=args.max_quanta,
        scramble_strength=args.scramble_strength,
        scramble_degree=args.scramble_degree,
        emission_coupling=coupling,
        emission_degree=args.emission_degree,
        emission_area_power=args.emission_area_power,
        emission_area_reference=args.emission_area_reference,
        skip_o1_emission_control=args.skip_o1_emission_control,
        detuning_width_x=args.detuning_width_x,
        ohmic_power=args.ohmic_power,
        matrix_cutoff=args.matrix_cutoff,
        initial_state=args.initial_state,
        seeds=args.seeds,
        t_max=t_max,
        time_points=args.time_points,
        x_edges=args.x_edges,
        quiet=args.quiet,
        output_dir=args.output_dir,
        combined_summary_csv=args.output_dir / f"{prefix}_summary.csv",
        aggregate_summary_csv=args.output_dir / f"{prefix}_aggregate.csv",
        dry_run_estimate=False,
        energy_drift_tol=args.energy_drift_tol,
        thermal_tv_tol=args.thermal_tv_tol,
    )

    summaries: list[dict[str, float | int | str]] = []
    linear_alpha = bench.matched_linear_alpha(args.q, args.sqrt_alpha, args.n_max)
    for seed in bench.parse_seeds(args.seeds):
        cases = [
            ("sqrt_scramble", "sqrt", args.sqrt_alpha, args.scramble_strength),
            ("linear_matched_scramble", "linear", linear_alpha, args.scramble_strength),
            ("sqrt_no_scramble", "sqrt", args.sqrt_alpha, 0.0),
        ]
        if not args.skip_o1_emission_control:
            cases.append(
                ("sqrt_o1_emission_scramble", "sqrt", args.sqrt_alpha, args.scramble_strength)
            )
        for case, mass_law, alpha, scramble in cases:
            case_args = bench.case_args(run_args, case, mass_law, alpha, scramble, seed)
            rows, summary = bench.parent.run(case_args)
            bench.parent.write_csv(case_args.timeseries_csv, rows)
            bench.parent.write_csv(case_args.summary_csv, [summary])
            summary = dict(summary)
            summary["seed"] = seed
            summary["comparison_case"] = case
            summary["linear_alpha_matched_to_sqrt_nmax"] = linear_alpha
            summary["t_max"] = t_max
            summary["time_points"] = args.time_points
            summary["max_quanta"] = args.max_quanta
            summary["mode_copies"] = args.mode_copies
            summary["energy_pass"] = float(summary["max_energy_drift"]) < args.energy_drift_tol
            summary["thermal_pass"] = float(summary["mean_flux_tv_to_thermal_x"]) <= args.thermal_tv_tol
            summary["late_power_growth"] = float(summary["power_late_over_early"]) > 1.0
            summaries.append(summary)
            print(
                f"[scan g={coupling:g} t={t_max:g} {case}] "
                f"P late/early={float(summary['power_late_over_early']):.3f} "
                f"TV={float(summary['mean_flux_tv_to_thermal_x']):.3f}",
                flush=True,
            )

    aggregate = bench.aggregate_summaries(
        summaries,
        energy_drift_tol=args.energy_drift_tol,
        thermal_tv_tol=args.thermal_tv_tol,
    )
    write_csv(run_args.combined_summary_csv, summaries)
    write_csv(run_args.aggregate_summary_csv, aggregate)

    protocol = {
        "emission_coupling": coupling,
        "t_max": t_max,
        "time_points": args.time_points,
        "max_quanta": args.max_quanta,
        "mode_copies": args.mode_copies,
        **score_protocol(aggregate),
    }
    return summaries, aggregate, protocol


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan laptop-scale benchmark protocols.")
    parser.add_argument("--case-prefix", default="matrix_free_parent_protocol_scan")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=7)
    parser.add_argument("--sqrt-alpha", type=float, default=8.0)
    parser.add_argument("--dos", default="exponential")
    parser.add_argument("--width-x", type=float, default=4.0)
    parser.add_argument("--mode-x", default="0.5,1.0,1.5,2.0,3.0,5.0")
    parser.add_argument("--mode-copies", type=int, default=2)
    parser.add_argument("--max-quanta", type=int, default=2)
    parser.add_argument("--scramble-strength", type=float, default=1.0)
    parser.add_argument("--scramble-degree", type=int, default=4)
    parser.add_argument("--couplings", default="0.05,0.08,0.12")
    parser.add_argument("--emission-degree", type=int, default=6)
    parser.add_argument("--emission-area-power", type=float, default=1.0)
    parser.add_argument("--emission-area-reference", type=float, default=1.0)
    parser.add_argument("--skip-o1-emission-control", action="store_true")
    parser.add_argument("--detuning-width-x", type=float, default=0.5)
    parser.add_argument("--ohmic-power", type=float, default=2.0)
    parser.add_argument("--matrix-cutoff", type=float, default=1e-10)
    parser.add_argument("--initial-state", choices=["haar", "basis"], default="haar")
    parser.add_argument("--seeds", default="2468")
    parser.add_argument("--t-max-list", default="60,80")
    parser.add_argument("--time-points", type=int, default=25)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--energy-drift-tol", type=float, default=1e-9)
    parser.add_argument("--thermal-tv-tol", type=float, default=0.2)
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument("--output-dir", type=Path, default=DATADIR)
    parser.add_argument(
        "--protocol-summary-csv",
        type=Path,
        default=DATADIR / "matrix_free_parent_protocol_scan_summary.csv",
    )
    args = parser.parse_args(argv)

    estimate = bench.resource_estimate(args)
    print(
        "[scan estimate] modes={mode_count} occ={occupation_count} dim={basis_dim} "
        "edge_upper={edge_upper} model_storage_scale={model_storage_scale_gb} GB "
        "recommended_free_ram={recommended_free_ram_gb} GB".format(
            **estimate
        ),
        flush=True,
    )
    protocol_rows: list[dict[str, float | int | str]] = []
    for coupling in parse_float_list(args.couplings):
        for t_max in parse_float_list(args.t_max_list):
            _, _, protocol = run_one(args, coupling, t_max)
            protocol_rows.append(protocol)

    protocol_rows.sort(key=lambda row: float(row["protocol_score"]), reverse=True)
    write_csv(args.protocol_summary_csv, protocol_rows)
    print(f"[scan] wrote {args.protocol_summary_csv}")
    print("[scan] best protocols:")
    for row in protocol_rows[:5]:
        print(
            "g={emission_coupling:g} t={t_max:g} score={protocol_score:.3f} "
            "sqrt={sqrt_power_late_over_early:.3f} "
            "linear={linear_power_late_over_early:.3f} "
            "noscr={no_scramble_power_late_over_early:.3f} "
            "TV={mean_flux_tv:.3f}".format(**row),
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
