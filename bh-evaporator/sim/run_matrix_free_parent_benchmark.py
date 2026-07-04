#!/usr/bin/env python3
"""Run the autonomous sector-parent comparison set.

This driver keeps the benchmark design in one place.  It compares the
square-root mass law against a linear mass law whose initial inverse
temperature is matched at n_max, plus a no-scrambling square-root control.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics as stats
from argparse import Namespace
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scan_bose_hubbard_dos import DATADIR

import matrix_free_autonomous_sector_parent as parent


def parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def matched_linear_alpha(q: int, sqrt_alpha: float, n_ref: int) -> float:
    """Choose alpha_linear so beta_linear equals beta_sqrt at n_ref."""
    _ = q  # q cancels, kept in the signature to document the matching.
    return sqrt_alpha * (math.sqrt(float(n_ref)) - math.sqrt(float(n_ref - 1)))


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def case_args(args: argparse.Namespace, case: str, mass_law: str, alpha: float, scramble: float, seed: int) -> Namespace:
    suffix = f"{args.case_prefix}_{case}_seed{seed}"
    return Namespace(
        case_name=suffix,
        q=args.q,
        n_min=args.n_min,
        n_max=args.n_max,
        alpha=alpha,
        mass_law=mass_law,
        dos=args.dos,
        width_x=args.width_x,
        mode_x=args.mode_x,
        mode_copies=args.mode_copies,
        max_quanta=args.max_quanta,
        scramble_strength=scramble,
        scramble_degree=args.scramble_degree,
        emission_coupling=args.emission_coupling,
        emission_degree=args.emission_degree,
        emission_area_power=(
            0.0 if case == "sqrt_o1_emission_scramble" else args.emission_area_power
        ),
        emission_area_reference=args.emission_area_reference,
        detuning_width_x=args.detuning_width_x,
        ohmic_power=args.ohmic_power,
        matrix_cutoff=args.matrix_cutoff,
        initial_state=args.initial_state,
        seed=seed,
        t_max=args.t_max,
        time_points=args.time_points,
        x_edges=args.x_edges,
        quiet=args.quiet,
        incremental_timeseries=args.incremental_timeseries,
        timeseries_csv=args.output_dir / f"{suffix}_timeseries.csv",
        summary_csv=args.output_dir / f"{suffix}_summary.csv",
    )


def run_case_task(task: tuple[str, int, Namespace, float]) -> dict[str, float | int | str]:
    case, seed, run_args, linear_alpha = task
    rows, summary = parent.run(run_args)
    parent.write_csv(run_args.timeseries_csv, rows)
    parent.write_csv(run_args.summary_csv, [summary])
    summary = dict(summary)
    summary["seed"] = seed
    summary["comparison_case"] = case
    summary["linear_alpha_matched_to_sqrt_nmax"] = linear_alpha
    summary["t_max"] = run_args.t_max
    summary["time_points"] = run_args.time_points
    summary["max_quanta"] = run_args.max_quanta
    summary["mode_copies"] = run_args.mode_copies
    return summary


def parse_seeds(value: str) -> list[int]:
    return [int(part.strip()) for part in value.split(",") if part.strip()]


def occupation_counts(mode_count: int, max_quanta: int) -> tuple[int, int]:
    total = 0
    expandable = 0
    for count in range(max_quanta + 1):
        ways = math.comb(mode_count, count)
        total += ways
        if count < max_quanta:
            expandable += ways * (mode_count - count)
    return total, expandable


def resource_estimate(args: argparse.Namespace) -> dict[str, int | float | str]:
    mode_count = len(parent.parse_float_list(args.mode_x)) * args.mode_copies
    occ_count, expandable_occ_mode_count = occupation_counts(mode_count, args.max_quanta)
    sector_dims = {n: args.q**n for n in range(args.n_min, args.n_max + 1)}
    basis_dim = occ_count * sum(sector_dims.values())
    # Symmetric random edge generator gives at most dim * degree / 2 unique
    # edges per sector, copied over radiation occupations.
    scramble_edge_upper = 0
    if args.scramble_strength > 0.0 and args.scramble_degree > 0:
        scramble_edge_upper = occ_count * sum(
            dim * min(args.scramble_degree, dim - 1) // 2
            for dim in sector_dims.values()
        )
    emission_edge_upper = expandable_occ_mode_count * args.emission_degree * sum(
        sector_dims[n] for n in range(args.n_min + 1, args.n_max + 1)
    )
    # This is only the model-construction footprint scale.  Krylov evolution
    # keeps additional complex work vectors, and Python object overhead can be
    # substantial while building the edge lists.
    model_storage_gb = (
        basis_dim * 900.0 + (scramble_edge_upper + emission_edge_upper) * 260.0
    ) / (1024.0**3)
    recommended_free_ram_gb = max(12.0, 8.0 * model_storage_gb + 6.0)
    return {
        "mode_count": mode_count,
        "occupation_count": occ_count,
        "basis_dim": basis_dim,
        "scramble_edge_upper": scramble_edge_upper,
        "emission_edge_upper": emission_edge_upper,
        "edge_upper": scramble_edge_upper + emission_edge_upper,
        "model_storage_scale_gb": round(model_storage_gb, 2),
        "recommended_free_ram_gb": round(recommended_free_ram_gb, 1),
    }


def finite_float(value: str | float | int) -> float:
    try:
        return float(value)
    except ValueError:
        return float("nan")


def aggregate_summaries(
    rows: list[dict[str, float | int | str]],
    *,
    energy_drift_tol: float,
    thermal_tv_tol: float,
) -> list[dict[str, float | int | str]]:
    grouped: dict[str, list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["comparison_case"])].append(row)

    out: list[dict[str, float | int | str]] = []
    for case, case_rows in sorted(grouped.items()):
        item: dict[str, float | int | str] = {
            "comparison_case": case,
            "run_count": len(case_rows),
            "mass_law": case_rows[0]["mass_law"],
            "alpha": case_rows[0]["alpha"],
            "scramble_strength": case_rows[0]["scramble_strength"],
            "emission_area_power": case_rows[0]["emission_area_power"],
            "emission_area_reference": case_rows[0]["emission_area_reference"],
            "ohmic_power": case_rows[0]["ohmic_power"],
            "predicted_power_exponent_n": case_rows[0]["predicted_power_exponent_n"],
            "predicted_power_exponent_m": case_rows[0]["predicted_power_exponent_m"],
        }
        for key in [
            "mean_n_drop",
            "final_radiation_energy",
            "early_outward_power",
            "mid_outward_power",
            "late_outward_power",
            "power_mid_over_early",
            "power_late_over_early",
            "mean_flux_tv_to_thermal_x",
            "max_energy_drift",
        ]:
            vals = [finite_float(row[key]) for row in case_rows]
            vals = [val for val in vals if math.isfinite(val)]
            item[f"{key}_mean"] = stats.mean(vals) if vals else float("nan")
            item[f"{key}_sd"] = stats.pstdev(vals) if len(vals) > 1 else 0.0
        item["energy_pass_count"] = sum(
            finite_float(row["max_energy_drift"]) < energy_drift_tol
            for row in case_rows
        )
        item["thermal_pass_count"] = sum(
            finite_float(row["mean_flux_tv_to_thermal_x"]) <= thermal_tv_tol
            for row in case_rows
        )
        item["late_power_growth_count"] = sum(
            finite_float(row["power_late_over_early"]) > 1.0
            for row in case_rows
        )
        out.append(item)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark the matrix-free autonomous sector parent.")
    parser.add_argument("--case-prefix", default="matrix_free_parent_benchmark")
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
    parser.add_argument("--emission-coupling", type=float, default=0.08)
    parser.add_argument("--emission-degree", type=int, default=6)
    parser.add_argument(
        "--emission-area-power",
        type=float,
        default=1.0,
        help=(
            "Rate-level power of n in the emission strength. "
            "The target area-emission case uses 1. The O(1) control uses 0."
        ),
    )
    parser.add_argument(
        "--emission-area-reference",
        type=float,
        default=1.0,
        help="Reference n used in the area-emission matrix-element factor.",
    )
    parser.add_argument(
        "--skip-o1-emission-control",
        action="store_true",
        help="Do not run the fixed-emission-strength sqrt control.",
    )
    parser.add_argument("--detuning-width-x", type=float, default=0.5)
    parser.add_argument("--ohmic-power", type=float, default=2.0)
    parser.add_argument("--matrix-cutoff", type=float, default=1e-10)
    parser.add_argument("--initial-state", choices=["haar", "basis"], default="haar")
    parser.add_argument("--seeds", default="2468")
    parser.add_argument("--t-max", type=float, default=120.0)
    parser.add_argument("--time-points", type=int, default=41)
    parser.add_argument("--dry-run-estimate", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--no-incremental-timeseries",
        action="store_true",
        help="Only write case time-series CSV files after each case completes.",
    )
    parser.add_argument(
        "--cases",
        default="sqrt_scramble,linear_matched_scramble,sqrt_no_scramble,sqrt_o1_emission_scramble",
        help=(
            "Comma-separated subset of cases to run: sqrt_scramble, "
            "linear_matched_scramble, sqrt_no_scramble, sqrt_o1_emission_scramble."
        ),
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=1,
        help="Number of independent case/seed runs to execute concurrently.",
    )
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
        "--combined-summary-csv",
        type=Path,
        default=DATADIR / "matrix_free_parent_benchmark_summary.csv",
    )
    parser.add_argument(
        "--aggregate-summary-csv",
        type=Path,
        default=DATADIR / "matrix_free_parent_benchmark_aggregate.csv",
    )
    args = parser.parse_args(argv)
    args.incremental_timeseries = not args.no_incremental_timeseries

    linear_alpha = matched_linear_alpha(args.q, args.sqrt_alpha, args.n_max)
    estimate = resource_estimate(args)
    print(
        "[estimate] modes={mode_count} occ={occupation_count} dim={basis_dim} "
        "edge_upper={edge_upper} model_storage_scale={model_storage_scale_gb} GB "
        "recommended_free_ram={recommended_free_ram_gb} GB".format(
            **estimate
        ),
        flush=True,
    )
    if args.dry_run_estimate:
        return 0

    tasks: list[tuple[str, int, Namespace, float]] = []
    requested_cases = {part.strip() for part in args.cases.split(",") if part.strip()}
    allowed_cases = {
        "sqrt_scramble",
        "linear_matched_scramble",
        "sqrt_no_scramble",
        "sqrt_o1_emission_scramble",
    }
    unknown_cases = requested_cases - allowed_cases
    if unknown_cases:
        raise SystemExit(f"unknown --cases entries: {', '.join(sorted(unknown_cases))}")

    for seed in parse_seeds(args.seeds):
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
            if case not in requested_cases:
                continue
            run_args = case_args(args, case, mass_law, alpha, scramble, seed)
            tasks.append((case, seed, run_args, linear_alpha))

    print(f"[benchmark] running {len(tasks)} case/seed tasks with jobs={max(1, args.jobs)}", flush=True)
    summaries: list[dict[str, float | int | str]] = []
    if args.jobs <= 1:
        for task in tasks:
            summaries.append(run_case_task(task))
    else:
        with ProcessPoolExecutor(max_workers=args.jobs) as executor:
            future_map = {executor.submit(run_case_task, task): task for task in tasks}
            for future in as_completed(future_map):
                summaries.append(future.result())

    case_order = {
        "sqrt_scramble": 0,
        "linear_matched_scramble": 1,
        "sqrt_no_scramble": 2,
        "sqrt_o1_emission_scramble": 3,
    }
    summaries.sort(
        key=lambda row: (
            int(row["seed"]),
            case_order.get(str(row["comparison_case"]), 99),
        )
    )

    for summary in summaries:
        summary["energy_pass"] = (
            float(summary["max_energy_drift"]) < args.energy_drift_tol
        )
        summary["thermal_pass"] = (
            float(summary["mean_flux_tv_to_thermal_x"]) <= args.thermal_tv_tol
        )
        summary["late_power_growth"] = (
            float(summary["power_late_over_early"]) > 1.0
        )
        print(
            f"[{summary['comparison_case']} seed={summary['seed']}] "
            f"dim={summary['basis_dim']} "
            f"dn={float(summary['mean_n_drop']):.3f} "
            f"P late/early={float(summary['power_late_over_early']):.3f} "
            f"TV={float(summary['mean_flux_tv_to_thermal_x']):.3f} "
            f"drift={float(summary['max_energy_drift']):.2e}",
            flush=True,
        )

    write_csv(args.combined_summary_csv, summaries)
    aggregate = aggregate_summaries(
        summaries,
        energy_drift_tol=args.energy_drift_tol,
        thermal_tv_tol=args.thermal_tv_tol,
    )
    write_csv(args.aggregate_summary_csv, aggregate)
    print(f"[benchmark] wrote {args.combined_summary_csv}")
    print(f"[benchmark] wrote {args.aggregate_summary_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
