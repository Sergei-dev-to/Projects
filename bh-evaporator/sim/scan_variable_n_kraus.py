#!/usr/bin/env python3
"""Targeted robustness scan for the variable-N Bose-Hubbard Kraus model."""
from __future__ import annotations

import argparse
import csv
import pathlib
from argparse import Namespace

import numpy as np

from scan_bose_hubbard_dos import DATADIR
from variable_n_bose_hubbard_evaporation import parse_list, summarize
from variable_n_bose_hubbard_kraus import run_one


def parse_windows(value: str) -> list[tuple[float, float]]:
    windows = []
    for item in value.split(","):
        lo, hi = item.split(":")
        windows.append((float(lo), float(hi)))
    return windows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan nearby variable-N Kraus parameters.")
    parser.add_argument("--sites", type=int, default=6)
    parser.add_argument("--n-max", type=int, default=8)
    parser.add_argument("--n-min", type=int, default=3)
    parser.add_argument("--geometry", default="ring")
    parser.add_argument("--j", type=float, default=0.5)
    parser.add_argument("--u", type=float, default=-1.0)
    parser.add_argument("--v-nn", type=float, default=-0.2)
    parser.add_argument("--j-inter", type=float, default=0.2)
    parser.add_argument("--disorder", type=float, default=0.02)
    parser.add_argument("--mu-list", default="5,6,7")
    parser.add_argument("--max-gap-list", default="3,4,5")
    parser.add_argument("--initial-windows", default="-18.5:-17,-20:-18")
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.05)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "variable_n_bose_hubbard_kraus_scan.csv",
    )
    args = parser.parse_args(argv)

    rows = []
    seeds = parse_list(args.seeds, int)
    mu_values = parse_list(args.mu_list, float)
    gap_values = parse_list(args.max_gap_list, float)
    windows = parse_windows(args.initial_windows)
    total = len(seeds) * len(mu_values) * len(gap_values) * len(windows)
    count = 0

    for seed in seeds:
        for mu in mu_values:
            for gap in gap_values:
                for lo, hi in windows:
                    count += 1
                    print(
                        f"[varN-kraus-scan] {count}/{total}: "
                        f"seed={seed} mu={mu:g} gap={gap:g} init=[{lo:g},{hi:g}]",
                        flush=True,
                    )
                    run_args = Namespace(
                        sites=args.sites,
                        n_max=args.n_max,
                        n_min=args.n_min,
                        geometry=args.geometry,
                        j=args.j,
                        u=args.u,
                        v_nn=args.v_nn,
                        j_inter=args.j_inter,
                        disorder=args.disorder,
                        mu=mu,
                        max_gap=gap,
                        initial_e_min=lo,
                        initial_e_max=hi,
                        pmax=args.pmax,
                        min_gap=args.min_gap,
                        ohmic_power=args.ohmic_power,
                        steps=args.steps,
                        seed=seed,
                    )
                    try:
                        result = run_one(run_args)
                        summary = summarize(result)
                        row = {
                            "seed": seed,
                            "mu": mu,
                            "max_gap": gap,
                            "initial_e_min": lo,
                            "initial_e_max": hi,
                            **summary,
                            "initial_dimension_entropy": float(result["dimension_entropy"][0]),
                            "final_dimension_entropy": float(result["dimension_entropy"][-1]),
                            "initial_effective_dimension": float(result["effective_dimension"][0]),
                            "final_effective_dimension": float(result["effective_dimension"][-1]),
                            "final_path_temperature": float(result["path_temperature"][-1]),
                            "max_norm_error": float(np.max(result["norm_error"])),
                        }
                    except Exception as exc:
                        row = {
                            "seed": seed,
                            "mu": mu,
                            "max_gap": gap,
                            "initial_e_min": lo,
                            "initial_e_max": hi,
                            "error": str(exc),
                        }
                    rows.append(row)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[varN-kraus-scan] wrote {args.output_csv}")
    valid = [row for row in rows if "error" not in row]
    if valid:
        best = max(valid, key=lambda row: row["accel_ratio_mid_over_early"])
        print("[varN-kraus-scan] best")
        for key in sorted(best):
            print(f"  {key}: {best[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
