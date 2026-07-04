#!/usr/bin/env python3
"""Measure whether evaporation transitions select high-W destination states."""
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
from phase_space_acceleration_diagnostic import area_omegas, weighted_columns
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


def transition_bias_scores(rates, omegas) -> dict[str, float]:
    power_cols, _jump_cols = weighted_columns(rates, omegas)
    ratios = []
    fluxes = []
    for n, rate in rates.items():
        dest_n = n - 1
        if dest_n not in power_cols:
            continue
        dest_w = power_cols[dest_n]
        uniform_dest_w = float(np.mean(dest_w))
        if uniform_dest_w <= 0.0:
            continue
        # Uniform source ensemble. Destination distribution induced by one jump.
        dest_flux = np.sum(rate, axis=1)
        total_flux = float(np.sum(dest_flux))
        if total_flux <= 0.0:
            continue
        selected_dest_w = float(dest_flux @ dest_w / total_flux)
        ratios.append(selected_dest_w / uniform_dest_w)
        fluxes.append(total_flux)

    if not ratios:
        return {
            "transition_bias_mean": float("nan"),
            "transition_bias_flux_weighted": float("nan"),
            "transition_bias_min": float("nan"),
            "transition_bias_max": float("nan"),
        }
    ratios_arr = np.asarray(ratios, dtype=float)
    fluxes_arr = np.asarray(fluxes, dtype=float)
    return {
        "transition_bias_mean": float(np.mean(ratios_arr)),
        "transition_bias_flux_weighted": float(ratios_arr @ fluxes_arr / np.sum(fluxes_arr)),
        "transition_bias_min": float(np.min(ratios_arr)),
        "transition_bias_max": float(np.max(ratios_arr)),
    }


def area_rows(args: argparse.Namespace) -> list[dict[str, float | str]]:
    out = []
    rows = [
        row
        for row in read_rows(args.area_csv)
        if row.get("error", "") == "" and row.get("mass_law") in {"sqrt", "linear"}
    ]
    for row in rows:
        seed = int(float(row["seed"]))
        operator = row["operator"]
        mass_law = row["mass_law"]
        max_gap = float(row["max_gap"])
        print(f"[transition-bias] area seed={seed} {operator} {mass_law} gap={max_gap:g}", flush=True)
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
        out.append(
            {
                "model": "area",
                "seed": seed,
                "operator": operator,
                "mass_law": mass_law,
                "max_gap": max_gap,
                "observed_accel": safe_float(row, "accel_ratio_mid_over_early"),
                **transition_bias_scores(rates, area_omegas(sectors)),
            }
        )
    return out


def varn_rows(args: argparse.Namespace) -> list[dict[str, float | str]]:
    out = []
    rows = [row for row in read_rows(args.varn_csv) if row.get("error", "") == ""]
    sectors_cache = {}
    for row in rows:
        seed = int(float(row["seed"]))
        if seed not in sectors_cache:
            print(f"[transition-bias] building varN sectors seed={seed}", flush=True)
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
        print(f"[transition-bias] varN seed={seed} mu={mu:g} gap={max_gap:g}", flush=True)
        rates, omegas = build_varn_jump_maps(
            sectors_cache[seed],
            mu=mu,
            pmax=args.pmax,
            min_gap=args.varn_min_gap,
            max_gap=max_gap,
            ohmic_power=args.ohmic_power,
        )
        out.append(
            {
                "model": "variable_n_bose_hubbard",
                "seed": seed,
                "mu": mu,
                "max_gap": max_gap,
                "initial_e_min": float(row["initial_e_min"]),
                "initial_e_max": float(row["initial_e_max"]),
                "observed_accel": safe_float(row, "accel_ratio_mid_over_early"),
                **transition_bias_scores(rates, omegas),
            }
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
        bias = np.asarray([float(row["transition_bias_flux_weighted"]) for row in subset], dtype=float)
        out.append(
            {
                "group": label,
                "rows": float(len(subset)),
                "bias_mean": float(np.nanmean(bias)),
                "bias_min": float(np.nanmin(bias)),
                "bias_max": float(np.nanmax(bias)),
                "bias_corr_with_accel": float(np.corrcoef(actual, bias)[0, 1]),
                "bias_above_one_fraction": float(np.mean(bias > 1.0)),
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run transition-bias diagnostic.")
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
        default=DATADIR / "transition_bias_diagnostic.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "transition_bias_diagnostic_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = area_rows(args) + varn_rows(args)
    write_csv(args.output_csv, rows)
    summary_rows = summarize(rows)
    write_csv(args.summary_csv, summary_rows)
    print(f"[transition-bias] wrote {args.output_csv}")
    print(f"[transition-bias] wrote {args.summary_csv}")
    for row in summary_rows:
        print(
            f"  {row['group']}: mean={row['bias_mean']:.3f}, "
            f"range=[{row['bias_min']:.3f},{row['bias_max']:.3f}], "
            f"corr={row['bias_corr_with_accel']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
