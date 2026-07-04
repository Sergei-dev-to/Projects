#!/usr/bin/env python3
"""Stress-test the outgoing phase-space acceleration criterion on scan rows."""
from __future__ import annotations

import argparse
import csv
import pathlib
from argparse import Namespace

import numpy as np

from area_register_rate_scan import (
    build_rate_maps as build_area_rate_maps,
    build_sectors as build_area_sectors,
)
from phase_space_acceleration_diagnostic import (
    area_omegas,
    initial_area_population,
    initial_varn_population,
    run_population_diagnostic,
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
    if value is None or value == "":
        return float("nan")
    return float(value)


def summarize_match(rows: list[dict[str, float | str]], label: str) -> dict[str, float | str]:
    valid = [
        row
        for row in rows
        if np.isfinite(float(row["actual_accel"])) and np.isfinite(float(row["w_accel"]))
    ]
    actual = np.asarray([float(row["actual_accel"]) for row in valid])
    pred = np.asarray([float(row["w_accel"]) for row in valid])
    sign_match = (actual > 1.0) == (pred > 1.0)
    corr = float(np.corrcoef(actual, pred)[0, 1]) if len(valid) > 1 else float("nan")
    return {
        "group": label,
        "rows": float(len(valid)),
        "sign_match": float(np.sum(sign_match)),
        "sign_match_fraction": float(np.mean(sign_match)) if len(valid) else float("nan"),
        "pearson_corr": corr,
        "actual_min": float(np.min(actual)) if len(valid) else float("nan"),
        "actual_max": float(np.max(actual)) if len(valid) else float("nan"),
        "w_min": float(np.min(pred)) if len(valid) else float("nan"),
        "w_max": float(np.max(pred)) if len(valid) else float("nan"),
    }


def run_area_stress(args: argparse.Namespace) -> list[dict[str, float | str]]:
    rows = []
    source_rows = [
        row
        for row in read_rows(args.area_csv)
        if row.get("error", "") == "" and row.get("mass_law") in {"sqrt", "linear"}
    ]
    # Limit to the corrected wide controls plus successful sqrt rows.
    for row in source_rows:
        seed = int(float(row["seed"]))
        operator = row["operator"]
        mass_law = row["mass_law"]
        max_gap = float(row["max_gap"])
        print(f"[stress] area seed={seed} {operator} {mass_law} gap={max_gap:g}", flush=True)
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
        energy = {n: sector.evals for n, sector in sectors.items()}
        _result, summary = run_population_diagnostic(
            pops, rates, area_omegas(sectors), energy, args.steps
        )
        rows.append(
            {
                "model": "area",
                "seed": seed,
                "operator": operator,
                "mass_law": mass_law,
                "max_gap": max_gap,
                "actual_accel": safe_float(row, "accel_ratio_mid_over_early"),
                "w_accel": summary["power_mid_over_early"],
                "jump_accel": summary["jump_mid_over_early"],
                "omega_accel": summary["conditional_omega_mid_over_early"],
            }
        )
    return rows


def run_varn_stress(args: argparse.Namespace) -> list[dict[str, float | str]]:
    rows = []
    source_rows = [row for row in read_rows(args.varn_csv) if row.get("error", "") == ""]
    sectors_cache = {}
    for row in source_rows:
        seed = int(float(row["seed"]))
        if seed not in sectors_cache:
            print(f"[stress] building variable-N sectors seed={seed}", flush=True)
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
            f"[stress] varN seed={seed} mu={mu:g} gap={max_gap:g} init=[{e_min:g},{e_max:g}]",
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
        energy = {n: mu * n + sector.evals_internal for n, sector in sectors.items()}
        _result, summary = run_population_diagnostic(pops, rates, omegas, energy, args.steps)
        rows.append(
            {
                "model": "variable_n_bose_hubbard",
                "seed": seed,
                "mu": mu,
                "max_gap": max_gap,
                "initial_e_min": e_min,
                "initial_e_max": e_max,
                "actual_accel": safe_float(row, "accel_ratio_mid_over_early"),
                "w_accel": summary["power_mid_over_early"],
                "jump_accel": summary["jump_mid_over_early"],
                "omega_accel": summary["conditional_omega_mid_over_early"],
            }
        )
    return rows


def write_csv(path: pathlib.Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stress-test W acceleration criterion.")
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
        default=DATADIR / "phase_space_criterion_stress_test.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "phase_space_criterion_stress_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = run_area_stress(args) + run_varn_stress(args)
    write_csv(args.output_csv, rows)
    summary_rows = [
        summarize_match([row for row in rows if row["model"] == "area"], "area"),
        summarize_match(
            [row for row in rows if row["model"] == "variable_n_bose_hubbard"],
            "variable_n_bose_hubbard",
        ),
        summarize_match(rows, "combined"),
    ]
    write_csv(args.summary_csv, summary_rows)

    print(f"[stress] wrote {args.output_csv}")
    print(f"[stress] wrote {args.summary_csv}")
    for row in summary_rows:
        print(
            f"  {row['group']}: sign_match={row['sign_match_fraction']:.3f}, "
            f"corr={row['pearson_corr']:.3f}, rows={int(row['rows'])}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
