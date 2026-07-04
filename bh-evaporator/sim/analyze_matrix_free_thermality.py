#!/usr/bin/env python3
"""Analyze local thermality diagnostics from a matrix-free parent time series.

The parent simulation records an instantaneous positive-current spectrum in
beta*omega bins.  This script adds windowed and flux-weighted summaries so the
finite Hamiltonian can be compared with the rate-level thermal expectation
without relying only on pointwise coherent-current TV distances.
"""
from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

from sector_hamiltonian_evaporator import target_x_distribution


def parse_probs(value: str) -> np.ndarray:
    return np.asarray([float(part) for part in value.split(";") if part], dtype=float)


def finite_float(value: str) -> float:
    try:
        out = float(value)
    except ValueError:
        return float("nan")
    return out


def tv_distance(probs: np.ndarray, target: np.ndarray) -> float:
    return 0.5 * float(np.sum(np.abs(probs - target)))


def weighted_average(rows: list[dict[str, str]], weight_key: str) -> tuple[np.ndarray | None, float]:
    total = 0.0
    acc: np.ndarray | None = None
    for row in rows:
        weight = finite_float(row[weight_key])
        if not math.isfinite(weight) or weight <= 0.0:
            continue
        probs = parse_probs(row["flux_x_probs"])
        if acc is None:
            acc = np.zeros_like(probs)
        acc += weight * probs
        total += weight
    if acc is None or total <= 0.0:
        return None, total
    return acc / total, total


def summarize_window(
    name: str,
    rows: list[dict[str, str]],
    target: np.ndarray,
) -> dict[str, float | int | str]:
    finite_rows = [
        row
        for row in rows
        if math.isfinite(finite_float(row["flux_tv_to_thermal_x"]))
    ]
    tvs = np.asarray(
        [finite_float(row["flux_tv_to_thermal_x"]) for row in finite_rows],
        dtype=float,
    )
    flux_weighted, total_flux = weighted_average(finite_rows, "outward_flux")
    power_weighted, total_power = weighted_average(finite_rows, "outward_power")

    out: dict[str, float | int | str] = {
        "window": name,
        "row_count": len(rows),
        "finite_tv_count": len(finite_rows),
        "mean_pointwise_tv": float(np.mean(tvs)) if len(tvs) else float("nan"),
        "min_pointwise_tv": float(np.min(tvs)) if len(tvs) else float("nan"),
        "max_pointwise_tv": float(np.max(tvs)) if len(tvs) else float("nan"),
        "total_outward_flux": total_flux,
        "total_outward_power": total_power,
    }

    if flux_weighted is not None:
        out["flux_weighted_tv"] = tv_distance(flux_weighted, target)
        out["flux_weighted_probs"] = ";".join(f"{p:.8g}" for p in flux_weighted)
    else:
        out["flux_weighted_tv"] = float("nan")
        out["flux_weighted_probs"] = ""

    if power_weighted is not None:
        out["power_weighted_tv"] = tv_distance(power_weighted, target)
        out["power_weighted_probs"] = ";".join(f"{p:.8g}" for p in power_weighted)
    else:
        out["power_weighted_tv"] = float("nan")
        out["power_weighted_probs"] = ""

    if rows:
        out["first_time"] = finite_float(rows[0]["time"])
        out["last_time"] = finite_float(rows[-1]["time"])
        out["first_mean_n"] = finite_float(rows[0]["mean_n"])
        out["last_mean_n"] = finite_float(rows[-1]["mean_n"])
        out["first_radiation_energy"] = finite_float(rows[0]["radiation_energy"])
        out["last_radiation_energy"] = finite_float(rows[-1]["radiation_energy"])
    return out


def split_windows(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    finite_rows = [
        row
        for row in rows
        if math.isfinite(finite_float(row["flux_tv_to_thermal_x"]))
    ]
    if not finite_rows:
        return {"all": rows, "early": [], "mid": [], "late": []}
    n = len(finite_rows)
    third = max(1, n // 3)
    return {
        "all": finite_rows,
        "early": finite_rows[:third],
        "mid": finite_rows[third : 2 * third],
        "late": finite_rows[2 * third :],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("timeseries_csv", type=Path)
    parser.add_argument("--ohmic-power", type=float, default=2.0)
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument("--output-csv", type=Path)
    args = parser.parse_args(argv)

    with args.timeseries_csv.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    target = target_x_distribution(np.asarray(args.x_edges, dtype=float), args.ohmic_power)
    windows = split_windows(rows)
    summaries = [
        summarize_window(name, window_rows, target)
        for name, window_rows in windows.items()
    ]
    for item in summaries:
        item["target_probs"] = ";".join(f"{p:.8g}" for p in target)
        item["ohmic_power"] = args.ohmic_power

    fields = sorted({key for row in summaries for key in row})
    if args.output_csv:
        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.output_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(summaries)

    print(",".join(fields))
    for row in summaries:
        print(",".join(str(row.get(field, "")) for field in fields))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
