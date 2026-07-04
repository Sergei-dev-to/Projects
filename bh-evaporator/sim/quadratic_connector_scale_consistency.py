#!/usr/bin/env python3
"""Scale bookkeeping for the quadratic connector candidate.

The connector tests use N as the active core size.  If the mass analogue is
M ~ N and the entropy is S ~ N^2, then T ~ 1/N.  A microscopic Hawking quantum
has energy O(T), while a coarse N -> N-1 change has energy O(1).  This script
keeps those scales separate.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np

from scan_bose_hubbard_dos import DATADIR


def active_links(n: int) -> int:
    return n * (n - 1) // 2


def core_entropy(n: int, q: float, sigma: float) -> float:
    return sigma * active_links(n) * np.log(q)


def core_mass(n: int, mu: float) -> float:
    return mu * n


def finite_difference_temperature(n: int, q: float, sigma: float, mu: float) -> float:
    if n <= 1:
        return np.nan
    ds = core_entropy(n, q, sigma) - core_entropy(n - 1, q, sigma)
    de = core_mass(n, mu) - core_mass(n - 1, mu)
    return de / ds


def run(args: argparse.Namespace) -> tuple[list[dict[str, float]], dict[str, float]]:
    rows: list[dict[str, float]] = []
    for n in range(args.n_min, args.n_max + 1):
        mass = core_mass(n, args.mu)
        entropy = core_entropy(n, args.q, args.sigma)
        temp = finite_difference_temperature(n, args.q, args.sigma, args.mu)
        coarse_energy = args.mu
        quantum_energy = args.kappa * temp
        rows.append(
            {
                "N": n,
                "active_links": active_links(n),
                "M": mass,
                "S": entropy,
                "T_fd": temp,
                "coarse_dM_N_to_N_minus_1": coarse_energy,
                "hawking_quantum_kappa_T": quantum_energy,
                "quanta_per_coarse_shrink": coarse_energy / max(quantum_energy, 1e-300),
                "relative_T_jump_per_coarse_shrink": (
                    finite_difference_temperature(n - 1, args.q, args.sigma, args.mu) - temp
                )
                / max(temp, 1e-300)
                if n > 2
                else np.nan,
            }
        )
    ns = np.asarray([row["N"] for row in rows], dtype=float)
    temps = np.asarray([row["T_fd"] for row in rows], dtype=float)
    quanta = np.asarray([row["quanta_per_coarse_shrink"] for row in rows], dtype=float)
    mask = np.isfinite(temps) & (temps > 0)
    temp_power = float(np.polyfit(np.log(ns[mask]), np.log(temps[mask]), 1)[0])
    quanta_power = float(np.polyfit(np.log(ns[mask]), np.log(quanta[mask]), 1)[0])
    summary = {
        "q": args.q,
        "sigma": args.sigma,
        "mu": args.mu,
        "kappa": args.kappa,
        "T_power": temp_power,
        "quanta_per_shrink_power": quanta_power,
        "T_at_nmax": rows[-1]["T_fd"],
        "quanta_per_shrink_at_nmax": rows[-1]["quanta_per_coarse_shrink"],
    }
    return rows, summary


def write_csv(path: pathlib.Path, rows: list[dict[str, float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-min", type=int, default=8)
    parser.add_argument("--n-max", type=int, default=256)
    parser.add_argument("--q", type=float, default=2.0)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--kappa", type=float, default=1.0)
    parser.add_argument(
        "--rows-csv",
        type=pathlib.Path,
        default=DATADIR / "quadratic_connector_scale_consistency_rows.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "quadratic_connector_scale_consistency_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    write_csv(args.rows_csv, rows)
    write_csv(args.summary_csv, [summary])
    print(f"[quadratic-scale] wrote {args.rows_csv}")
    print(f"[quadratic-scale] wrote {args.summary_csv}")
    print(
        "T_power={T_power:.3f} quanta_per_shrink_power={quanta_per_shrink_power:.3f} "
        "T_at_nmax={T_at_nmax:.4e} quanta_per_shrink_at_nmax={quanta_per_shrink_at_nmax:.2f}".format(
            **summary
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
