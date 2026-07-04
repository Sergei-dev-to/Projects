#!/usr/bin/env python3
"""Sector-level outgoing phase-space diagnostics.

This tests whether acceleration can be predicted from coarse sector structure,
rather than only recovered from the identity P(t)=<W>_t after evolving the full
state distribution.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from argparse import Namespace
from collections import defaultdict

import numpy as np
from numpy.typing import NDArray

from area_register_rate_scan import (
    build_rate_maps as build_area_rate_maps,
    build_sectors as build_area_sectors,
)
from phase_space_acceleration_diagnostic import (
    area_omegas,
    initial_area_population,
    initial_varn_population,
    step_population,
    weighted_columns,
)
from scan_bose_hubbard_dos import DATADIR
from variable_n_bose_hubbard_evaporation import (
    build_jump_maps as build_varn_jump_maps,
    build_sectors as build_varn_sectors,
)


def read_rows(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def safe_float(row: dict[str, str], key: str) -> float:
    value = row.get(key, "")
    return float(value) if value not in {"", None} else float("nan")


def summarize_series(values: NDArray[np.float64]) -> dict[str, float]:
    active = values[1:] if len(values) > 1 else values
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]
    late = active[max(third + 1, 2 * len(active) // 3) :]
    return {
        "early": float(np.mean(early)),
        "mid": float(np.mean(mid)),
        "late": float(np.mean(late)) if len(late) else float("nan"),
        "mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
    }


def sector_means(cols: dict[int, NDArray[np.float64]]) -> dict[int, float]:
    return {n: float(np.mean(values)) for n, values in cols.items()}


def sector_profile_scores(mean_w: dict[int, float], n_initial: int) -> dict[str, float]:
    valid = sorted((n, w) for n, w in mean_w.items() if np.isfinite(w) and w > 0.0)
    if not valid or n_initial not in mean_w or mean_w[n_initial] <= 0.0:
        return {
            "structural_ratio_all_lower_over_initial": float("nan"),
            "structural_ratio_next_over_initial": float("nan"),
            "structural_log_slope_against_sector": float("nan"),
            "structural_lower_fraction_above_initial": float("nan"),
        }

    lower = [(n, w) for n, w in valid if n < n_initial]
    initial = mean_w[n_initial]
    if lower:
        lower_values = np.asarray([w for _n, w in lower], dtype=float)
        ratio_all = float(np.mean(lower_values) / initial)
        fraction_above = float(np.mean(lower_values > initial))
    else:
        ratio_all = float("nan")
        fraction_above = float("nan")

    next_ratio = mean_w.get(n_initial - 1, float("nan")) / initial
    ns = np.asarray([n for n, _w in valid], dtype=float)
    logw = np.log(np.asarray([w for _n, w in valid], dtype=float))
    slope = float(np.polyfit(ns, logw, 1)[0]) if len(valid) >= 2 else float("nan")
    return {
        "structural_ratio_all_lower_over_initial": ratio_all,
        "structural_ratio_next_over_initial": float(next_ratio),
        # Since evaporation moves toward lower sector labels, a negative slope
        # means W tends to increase along the shrinking direction.
        "structural_log_slope_against_sector": slope,
        "structural_lower_fraction_above_initial": fraction_above,
    }


def trajectory_diagnostics(
    pops: dict[int, NDArray[np.float64]],
    rates: dict[int, NDArray[np.float64]],
    power_cols: dict[int, NDArray[np.float64]],
    jump_cols: dict[int, NDArray[np.float64]],
    steps: int,
) -> dict[str, NDArray[np.float64] | float]:
    mean_w = sector_means(power_cols)
    mean_jump = sector_means(jump_cols)
    actual_w = []
    sector_w = []
    actual_jump = []
    sector_jump = []
    mean_sector = []
    selection_ratio = []

    for _step in range(steps + 1):
        aw = 0.0
        sw = 0.0
        aj = 0.0
        sj = 0.0
        ms = 0.0
        for n, pop in pops.items():
            p_sector = float(np.sum(pop))
            ms += n * p_sector
            if n in power_cols:
                aw += float(pop @ power_cols[n])
                sw += p_sector * mean_w[n]
                aj += float(pop @ jump_cols[n])
                sj += p_sector * mean_jump[n]
        actual_w.append(aw)
        sector_w.append(sw)
        actual_jump.append(aj)
        sector_jump.append(sj)
        mean_sector.append(ms)
        selection_ratio.append(aw / max(sw, 1e-300))
        pops = step_population(pops, rates)

    actual_w_arr = np.asarray(actual_w, dtype=float)
    sector_w_arr = np.asarray(sector_w, dtype=float)
    denom = np.maximum(np.abs(actual_w_arr), 1e-300)
    rel_err = np.abs(actual_w_arr - sector_w_arr) / denom
    finite = np.isfinite(actual_w_arr) & np.isfinite(sector_w_arr)
    corr = (
        float(np.corrcoef(actual_w_arr[finite], sector_w_arr[finite])[0, 1])
        if np.sum(finite) > 1
        else float("nan")
    )
    return {
        "actual_w": actual_w_arr,
        "sector_w": sector_w_arr,
        "actual_jump": np.asarray(actual_jump, dtype=float),
        "sector_jump": np.asarray(sector_jump, dtype=float),
        "mean_sector": np.asarray(mean_sector, dtype=float),
        "selection_ratio": np.asarray(selection_ratio, dtype=float),
        "sector_reconstruction_corr": corr,
        "sector_reconstruction_mean_relerr": float(np.mean(rel_err[finite])),
        "sector_reconstruction_max_relerr": float(np.max(rel_err[finite])),
    }


def analyze_case(
    *,
    model: str,
    sectors,
    rates,
    omegas,
    pops,
    n_initial: int,
    steps: int,
    metadata: dict[str, float | str],
) -> dict[str, float | str]:
    power_cols, jump_cols = weighted_columns(rates, omegas)
    mean_w = sector_means(power_cols)
    mean_jump = sector_means(jump_cols)
    traj = trajectory_diagnostics(pops, rates, power_cols, jump_cols, steps)
    actual_summary = summarize_series(traj["actual_w"])
    sector_summary = summarize_series(traj["sector_w"])
    selection_summary = summarize_series(traj["selection_ratio"])

    out: dict[str, float | str] = {
        "model": model,
        **metadata,
        **sector_profile_scores(mean_w, n_initial),
        "actual_w_mid_over_early": actual_summary["mid_over_early"],
        "sector_w_mid_over_early": sector_summary["mid_over_early"],
        "selection_mid_over_early": selection_summary["mid_over_early"],
        "sector_reconstruction_corr": float(traj["sector_reconstruction_corr"]),
        "sector_reconstruction_mean_relerr": float(traj["sector_reconstruction_mean_relerr"]),
        "sector_reconstruction_max_relerr": float(traj["sector_reconstruction_max_relerr"]),
        "initial_mean_sector": float(traj["mean_sector"][0]),
        "final_mean_sector": float(traj["mean_sector"][-1]),
    }
    for n, value in mean_w.items():
        out[f"mean_w_sector_{n}"] = value
    for n, value in mean_jump.items():
        out[f"mean_jump_sector_{n}"] = value
    return out


def area_cases(args: argparse.Namespace) -> list[dict[str, float | str]]:
    rows = [
        row
        for row in read_rows(args.area_csv)
        if row.get("error", "") == "" and row.get("mass_law") in {"sqrt", "linear"}
    ]
    out = []
    for row in rows:
        seed = int(float(row["seed"]))
        operator = row["operator"]
        mass_law = row["mass_law"]
        max_gap = float(row["max_gap"])
        print(f"[sector-W] area seed={seed} {operator} {mass_law} gap={max_gap:g}", flush=True)
        sectors = build_area_sectors(
            n_min=args.area_n_min,
            n_max=args.area_n_max,
            q=args.q,
            alpha=args.alpha,
            bandwidth=args.bandwidth,
            mass_law=mass_law,
            seed=seed,
        )
        rates = build_area_rate_maps(
            sectors,
            q=args.q,
            operator=operator,
            seed=seed,
            pmax=args.pmax,
            min_gap=args.area_min_gap,
            max_gap=max_gap,
            ohmic_power=args.ohmic_power,
        )
        pops = initial_area_population(sectors, args.area_n_max, seed + 50_000)
        out.append(
            analyze_case(
                model="area",
                sectors=sectors,
                rates=rates,
                omegas=area_omegas(sectors),
                pops=pops,
                n_initial=args.area_n_max,
                steps=args.steps,
                metadata={
                    "seed": seed,
                    "operator": operator,
                    "mass_law": mass_law,
                    "max_gap": max_gap,
                    "observed_accel": safe_float(row, "accel_ratio_mid_over_early"),
                },
            )
        )
    return out


def varn_cases(args: argparse.Namespace) -> list[dict[str, float | str]]:
    rows = [row for row in read_rows(args.varn_csv) if row.get("error", "") == ""]
    out = []
    sectors_cache = {}
    for row in rows:
        seed = int(float(row["seed"]))
        if seed not in sectors_cache:
            print(f"[sector-W] building varN sectors seed={seed}", flush=True)
            ns = Namespace(
                sites=args.sites,
                n_max=args.varn_n_max,
                n_min=args.varn_n_min,
                geometry=args.geometry,
                j=args.j,
                u=args.u,
                v_nn=args.v_nn,
                j_inter=args.j_inter,
                disorder=args.disorder,
            )
            sectors_cache[seed] = build_varn_sectors(ns, seed)

        mu = float(row["mu"])
        max_gap = float(row["max_gap"])
        e_min = float(row["initial_e_min"])
        e_max = float(row["initial_e_max"])
        print(
            f"[sector-W] varN seed={seed} mu={mu:g} gap={max_gap:g} init=[{e_min:g},{e_max:g}]",
            flush=True,
        )
        sectors = sectors_cache[seed]
        rates, omegas = build_varn_jump_maps(
            sectors,
            mu=mu,
            pmax=args.pmax,
            min_gap=args.varn_min_gap,
            max_gap=max_gap,
            ohmic_power=args.ohmic_power,
        )
        pops = initial_varn_population(sectors, args.varn_n_max, e_min, e_max, seed + 50_000)
        out.append(
            analyze_case(
                model="variable_n_bose_hubbard",
                sectors=sectors,
                rates=rates,
                omegas=omegas,
                pops=pops,
                n_initial=args.varn_n_max,
                steps=args.steps,
                metadata={
                    "seed": seed,
                    "mu": mu,
                    "max_gap": max_gap,
                    "initial_e_min": e_min,
                    "initial_e_max": e_max,
                    "observed_accel": safe_float(row, "accel_ratio_mid_over_early"),
                },
            )
        )
    return out


def write_csv(path: pathlib.Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    out = []
    for label in ["area", "variable_n_bose_hubbard", "combined"]:
        subset = rows if label == "combined" else [row for row in rows if row["model"] == label]
        actual = np.asarray([float(row["observed_accel"]) for row in subset], dtype=float)
        sector = np.asarray([float(row["sector_w_mid_over_early"]) for row in subset], dtype=float)
        structural = np.asarray(
            [float(row["structural_ratio_all_lower_over_initial"]) for row in subset],
            dtype=float,
        )
        recon = np.asarray([float(row["sector_reconstruction_corr"]) for row in subset], dtype=float)
        sector_sign = (actual > 1.0) == (sector > 1.0)
        structural_sign = (actual > 1.0) == (structural > 1.0)
        out.append(
            {
                "group": label,
                "rows": float(len(subset)),
                "sector_trajectory_sign_match": float(np.mean(sector_sign)),
                "sector_trajectory_corr": float(np.corrcoef(actual, sector)[0, 1]),
                "structural_ratio_sign_match": float(np.mean(structural_sign)),
                "structural_ratio_corr": float(np.corrcoef(actual, structural)[0, 1]),
                "mean_sector_reconstruction_corr": float(np.nanmean(recon)),
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run sector-level W profile diagnostics.")
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--area-n-min", type=int, default=4)
    parser.add_argument("--area-n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--area-min-gap", type=float, default=0.01)
    parser.add_argument("--sites", type=int, default=6)
    parser.add_argument("--varn-n-max", type=int, default=8)
    parser.add_argument("--varn-n-min", type=int, default=3)
    parser.add_argument("--geometry", default="ring")
    parser.add_argument("--j", type=float, default=0.5)
    parser.add_argument("--u", type=float, default=-1.0)
    parser.add_argument("--v-nn", type=float, default=-0.2)
    parser.add_argument("--j-inter", type=float, default=0.2)
    parser.add_argument("--disorder", type=float, default=0.02)
    parser.add_argument("--varn-min-gap", type=float, default=0.05)
    parser.add_argument(
        "--area-csv",
        type=pathlib.Path,
        default=DATADIR / "area_register_rate_scan_wide.csv",
    )
    parser.add_argument(
        "--varn-csv",
        type=pathlib.Path,
        default=DATADIR / "variable_n_bose_hubbard_kraus_scan.csv",
    )
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "sector_phase_space_profile.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "sector_phase_space_profile_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = area_cases(args) + varn_cases(args)
    write_csv(args.output_csv, rows)
    summary_rows = summarize(rows)
    write_csv(args.summary_csv, summary_rows)
    print(f"[sector-W] wrote {args.output_csv}")
    print(f"[sector-W] wrote {args.summary_csv}")
    for row in summary_rows:
        print(
            f"  {row['group']}: "
            f"sector sign={row['sector_trajectory_sign_match']:.3f}, "
            f"sector corr={row['sector_trajectory_corr']:.3f}, "
            f"struct sign={row['structural_ratio_sign_match']:.3f}, "
            f"struct corr={row['structural_ratio_corr']:.3f}, "
            f"recon corr={row['mean_sector_reconstruction_corr']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
