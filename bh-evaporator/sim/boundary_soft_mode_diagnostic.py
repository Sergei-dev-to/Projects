"""Boundary soft-mode diagnostic for the edge-tension droplet.

Model a droplet with:

    bulk constrained entropy: S_bulk = L^2 log q
    boundary tension mass:    M = 4 sigma L
    acoustic boundary modes:  omega_n = v n / L

At the droplet temperature T ~ 1/L, the dimensionless mode energies
beta omega_n are independent of L. This script checks:

1. boundary soft entropy is subleading compared with S_bulk;
2. microscopic emitted quanta have omega ~ T;
3. golden-rule power from boundary modes scales as P ~ M^-d for a d-dimensional
   exterior bath, giving P ~ M^-2 in d=2.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


def beta_of_L(L: int, q: int, sigma: float) -> float:
    mass = 4.0 * sigma * L
    return mass * math.log(q) / (8.0 * sigma**2)


def boson_entropy_from_x(x: np.ndarray) -> np.ndarray:
    """Entropy of bosonic oscillators with x = beta omega."""
    nbar = 1.0 / np.expm1(x)
    return (nbar + 1.0) * np.log(nbar + 1.0) - nbar * np.log(nbar)


def row_for_L(
    L: int,
    q: int,
    sigma: float,
    velocity: float,
    degeneracy: int,
    n_modes: int,
    bath_dim: int,
) -> dict[str, float]:
    mass = 4.0 * sigma * L
    beta = beta_of_L(L, q, sigma)
    temp = 1.0 / beta
    n = np.arange(1, n_modes + 1, dtype=float)
    omega = velocity * n / L
    x = beta * omega
    occupation = 1.0 / np.expm1(x)
    entropy_modes = degeneracy * boson_entropy_from_x(x)
    energy_modes = degeneracy * omega * occupation

    # Weak-coupling emission into a d-dimensional bath.  Up to a constant
    # coupling, rho_bath(omega) * emitted energy gives omega^d.
    power_terms = degeneracy * (omega**bath_dim) * occupation
    number_terms = degeneracy * (omega ** max(bath_dim - 1, 0)) * occupation
    power = float(np.sum(power_terms))
    number_rate = float(np.sum(number_terms))
    mean_omega = power / number_rate if number_rate > 0.0 else 0.0

    s_bulk = L * L * math.log(q)
    s_edge = float(np.sum(entropy_modes))
    e_edge = float(np.sum(energy_modes))

    return {
        "L": float(L),
        "q": float(q),
        "sigma": sigma,
        "velocity": velocity,
        "degeneracy": float(degeneracy),
        "n_modes": float(n_modes),
        "bath_dim": float(bath_dim),
        "mass": mass,
        "beta": beta,
        "temperature": temp,
        "S_bulk": s_bulk,
        "S_edge": s_edge,
        "S_edge_over_S_bulk": s_edge / s_bulk,
        "E_edge": e_edge,
        "E_edge_over_M": e_edge / mass,
        "power": power,
        "number_rate": number_rate,
        "mean_omega": mean_omega,
        "mean_omega_over_T": mean_omega / temp,
        "M2_power": mass * mass * power,
        "Md_power": (mass**bath_dim) * power,
    }


def fit_power_law(rows: list[dict[str, float]], key: str, min_L: int) -> float:
    xs = []
    ys = []
    for row in rows:
        if row["L"] >= min_L and row[key] > 0.0:
            xs.append(math.log(row["mass"]))
            ys.append(math.log(row[key]))
    return float(np.polyfit(np.array(xs), np.array(ys), 1)[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--velocity", type=float, default=1.0)
    parser.add_argument("--degeneracy", type=int, default=2)
    parser.add_argument("--n-modes", type=int, default=200)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--max-L", type=int, default=100)
    parser.add_argument("--min-fit-L", type=int, default=20)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/boundary_soft_mode_diagnostic.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/boundary_soft_mode_diagnostic_summary.csv"),
    )
    args = parser.parse_args()

    rows = [
        row_for_L(
            L,
            args.q,
            args.sigma,
            args.velocity,
            args.degeneracy,
            args.n_modes,
            args.bath_dim,
        )
        for L in range(2, args.max_L + 1)
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    slope = fit_power_law(rows, "power", args.min_fit_L)
    summary = {
        "q": args.q,
        "sigma": args.sigma,
        "velocity": args.velocity,
        "degeneracy": args.degeneracy,
        "n_modes": args.n_modes,
        "bath_dim": args.bath_dim,
        "fit_min_L": args.min_fit_L,
        "power_law_slope_logP_logM": slope,
        "target_slope": -float(args.bath_dim),
        "mean_MdP_last10": float(np.mean([row["Md_power"] for row in rows[-10:]])),
        "std_MdP_last10": float(np.std([row["Md_power"] for row in rows[-10:]])),
        "mean_edge_entropy_last10": float(np.mean([row["S_edge"] for row in rows[-10:]])),
        "mean_edge_over_bulk_last10": float(np.mean([row["S_edge_over_S_bulk"] for row in rows[-10:]])),
        "mean_omega_over_T_last10": float(np.mean([row["mean_omega_over_T"] for row in rows[-10:]])),
    }

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print(f"power slope logP/logM: {slope:.4f} (target {-args.bath_dim:.1f})")
    print(f"mean M^d P last10: {summary['mean_MdP_last10']:.4f}")
    print(f"mean S_edge last10: {summary['mean_edge_entropy_last10']:.4f}")
    print(f"mean S_edge/S_bulk last10: {summary['mean_edge_over_bulk_last10']:.6e}")
    print(f"mean omega/T last10: {summary['mean_omega_over_T_last10']:.4f}")
    print()
    print("L   T          S_edge/S_bulk    E_edge/M       omega/T      M^d P")
    for row in rows[:5] + rows[-5:]:
        print(
            f"{int(row['L']):3d} "
            f"{row['temperature']:10.5f} "
            f"{row['S_edge_over_S_bulk']:15.6e} "
            f"{row['E_edge_over_M']:12.6e} "
            f"{row['mean_omega_over_T']:11.4f} "
            f"{row['Md_power']:12.4f}"
        )


if __name__ == "__main__":
    main()
