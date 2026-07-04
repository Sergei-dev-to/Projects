#!/usr/bin/env python3
"""Search connector spectra for Hawking-scale soft thermal modes.

The previous connector gate showed that complete-graph incidence spectra do not
produce omega ~ 1/N softness.  This script tests a broader class: connector
degrees organized into collective critical spectra with O(N^2) modes.

For each spectrum and each N, we compute one-particle thermal sums at
T = eta / N:

  Z(T) = sum_m exp(-omega_m / T)
  <omega>_T = sum_m omega_m exp(-omega_m/T) / Z(T)

The useful gate is whether <omega>_T / T remains O(1) while the number of
thermally available connector modes grows with N.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np

from scan_bose_hubbard_dos import DATADIR


def normalize_positive(eigs: np.ndarray) -> np.ndarray:
    vals = np.asarray(eigs, dtype=float)
    vals = vals[np.isfinite(vals)]
    vals = vals[vals > 1e-12]
    return np.sort(vals)


def line_graph_complete(n: int, scale_power: float) -> np.ndarray:
    lam0 = 2.0 * (n - 2)
    eigs = [0.0]
    eigs.extend([(lam0 - (n - 4)) / (n**scale_power)] * (n - 1))
    eigs.extend([(lam0 + 2.0) / (n**scale_power)] * (n * (n - 3) // 2))
    return normalize_positive(np.asarray(eigs))


def ring_laplacian(length: int, scale: float = 1.0) -> np.ndarray:
    k = np.arange(length)
    eigs = scale * (2.0 - 2.0 * np.cos(2.0 * np.pi * k / length))
    return normalize_positive(eigs)


def ring_linear(length: int, scale: float = 1.0) -> np.ndarray:
    k = np.arange(length)
    eigs = scale * np.sqrt(np.maximum(0.0, 2.0 - 2.0 * np.cos(2.0 * np.pi * k / length)))
    return normalize_positive(eigs)


def grid_laplacian(side_x: int, side_y: int, scale: float = 1.0) -> np.ndarray:
    kx = np.arange(side_x)
    ky = np.arange(side_y)
    ex = 2.0 - 2.0 * np.cos(2.0 * np.pi * kx / side_x)
    ey = 2.0 - 2.0 * np.cos(2.0 * np.pi * ky / side_y)
    eigs = scale * (ex[:, None] + ey[None, :]).ravel()
    return normalize_positive(eigs)


def critical_powerlaw(n_modes: int, exponent: float) -> np.ndarray:
    """Toy sorted spectrum omega_k=(k/n_modes)^exponent."""
    k = np.arange(1, n_modes + 1, dtype=float)
    return np.power(k / n_modes, exponent)


def thermal_stats(eigs: np.ndarray, temperature: float) -> dict[str, float]:
    vals = normalize_positive(eigs)
    if vals.size == 0:
        return {
            "n_modes": 0,
            "gap": np.nan,
            "median_gap": np.nan,
            "soft_count": 0,
            "soft_fraction": 0.0,
            "Z": 0.0,
            "mean_omega": np.nan,
            "mean_over_T": np.nan,
            "thermal_participation": 0.0,
        }
    weights = np.exp(-vals / max(temperature, 1e-300))
    z = float(np.sum(weights))
    z_local = z / float(vals.size)
    mean = float(np.sum(vals * weights) / max(z, 1e-300))
    p = weights / max(z, 1e-300)
    participation = float(1.0 / max(np.sum(p * p), 1e-300))
    soft = vals <= temperature
    return {
        "n_modes": int(vals.size),
        "gap": float(vals[0]),
        "median_gap": float(np.median(vals)),
        "soft_count": int(np.sum(soft)),
        "soft_fraction": float(np.mean(soft)),
        "Z": z,
        "Z_local": z_local,
        "power_local": z_local * mean,
        "mean_omega": mean,
        "mean_over_T": mean / max(temperature, 1e-300),
        "thermal_participation": participation,
    }


def fit_power(ns: np.ndarray, values: np.ndarray) -> float:
    mask = np.isfinite(values) & (values > 0)
    if np.sum(mask) < 2:
        return np.nan
    return float(np.polyfit(np.log(ns[mask]), np.log(values[mask]), 1)[0])


def spectra_for_n(n: int) -> dict[str, np.ndarray]:
    n_conn = n * (n - 1) // 2
    side = max(2, n)
    rect_y = max(2, (n_conn + side - 1) // side)
    return {
        "complete_line_graph_kac": line_graph_complete(n, 1.0),
        "connector_ring_crit": ring_laplacian(n_conn),
        "connector_ring_linear_crit": ring_linear(n_conn),
        "connector_grid_NxN_crit": grid_laplacian(side, side),
        "connector_rect_exactish_crit": grid_laplacian(side, rect_y),
        "powerlaw_alpha1": critical_powerlaw(n_conn, 1.0),
        "powerlaw_alpha2": critical_powerlaw(n_conn, 2.0),
    }


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    rows: list[dict[str, float | str]] = []
    for n in range(args.n_min, args.n_max + 1):
        temp = args.eta / n
        for model, eigs in spectra_for_n(n).items():
            stats = thermal_stats(eigs, temp)
            rows.append({"N": n, "T": temp, "model": model, **stats})

    models = sorted({str(row["model"]) for row in rows})
    summary: list[dict[str, float | str]] = []
    for model in models:
        sub = [row for row in rows if row["model"] == model]
        ns = np.asarray([float(row["N"]) for row in sub])
        gap = np.asarray([float(row["gap"]) for row in sub])
        mean_over_t = np.asarray([float(row["mean_over_T"]) for row in sub])
        part = np.asarray([float(row["thermal_participation"]) for row in sub])
        z = np.asarray([float(row["Z"]) for row in sub])
        z_local = np.asarray([float(row["Z_local"]) for row in sub])
        power_local = np.asarray([float(row["power_local"]) for row in sub])
        soft_count = np.asarray([float(row["soft_count"]) for row in sub])
        # Pass if the thermal mean stays on the Hawking scale and the number
        # of thermally participating modes grows with N.
        mean_ok = 0.25 <= mean_over_t[-1] <= 4.0
        part_power = fit_power(ns, part)
        pass_gate = mean_ok and part_power > 0.25
        power_exp = fit_power(ns, power_local)
        power_ok = -2.5 <= power_exp <= -1.5
        summary.append(
            {
                "model": model,
                "gap_power": fit_power(ns, gap),
                "Z_power": fit_power(ns, z),
                "Z_local_power": fit_power(ns, z_local),
                "power_local_power": power_exp,
                "participation_power": part_power,
                "soft_count_power": fit_power(ns, soft_count),
                "mean_over_T_at_nmax": float(mean_over_t[-1]),
                "thermal_participation_at_nmax": float(part[-1]),
                "Z_at_nmax": float(z[-1]),
                "soft_count_at_nmax": float(soft_count[-1]),
                "passes_collective_softness_gate": "yes" if pass_gate else "no",
                "passes_local_power_gate": "yes" if pass_gate and power_ok else "no",
            }
        )
    return rows, summary


def write_csv(path: pathlib.Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-min", type=int, default=8)
    parser.add_argument("--n-max", type=int, default=128)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument(
        "--rows-csv",
        type=pathlib.Path,
        default=DATADIR / "collective_connector_softness_rows.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "collective_connector_softness_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    write_csv(args.rows_csv, rows)
    write_csv(args.summary_csv, summary)
    print(f"[collective-softness] wrote {args.rows_csv}")
    print(f"[collective-softness] wrote {args.summary_csv}")
    for row in summary:
        print(
            "{model}: pass={passes_collective_softness_gate} "
            "power={passes_local_power_gate} "
            "mean/T={mean_over_T_at_nmax:.3f} part_pow={participation_power:.3f} "
            "part={thermal_participation_at_nmax:.2f} Zpow={Z_power:.3f} "
            "Plocpow={power_local_power:.3f}".format(**row)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
