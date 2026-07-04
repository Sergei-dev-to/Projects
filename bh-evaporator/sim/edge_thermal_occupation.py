"""Boundary edge thermal occupation versus microcanonical golden weights.

The energy-aware emission block still prepares the edge excitation with
golden-rule weights.  This diagnostic asks whether those weights can instead
come from an ordinary boundary soft-mode Hamiltonian at the droplet temperature.

For each droplet size L, compare:

    exact microcanonical bin weights:
        p_h ~ int_bin d omega omega^(d-1) exp[S(M - omega) - S(M)]

    canonical edge/bath bin weights:
        p_h ~ int_bin d omega omega^(d-1) exp[-beta(M) omega]

If the trace distance goes to zero at large L, then a thermal edge mode at
T_L = 1 / beta(M) reproduces the same hard-bin occupation asymptotically.  The
finite-size mismatch is the entropy-curvature correction.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


def entropy_of_mass(mass: float, q: int, sigma: float) -> float:
    if mass <= 0.0:
        return 0.0
    return (mass / (4.0 * sigma)) ** 2 * math.log(q)


def beta_of_mass(mass: float, q: int, sigma: float) -> float:
    return mass * math.log(q) / (8.0 * sigma**2)


def bin_weights(
    mass: float,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    exact: bool,
) -> tuple[np.ndarray, float]:
    beta = beta_of_mass(mass, q, sigma)
    s0 = entropy_of_mass(mass, q, sigma)
    weights = []
    energy_weights = []
    for x0, x1 in zip(x_edges[:-1], x_edges[1:]):
        xs = np.linspace(float(x0), float(x1), n_grid)
        omega = xs / beta
        if exact:
            exponent = np.array([entropy_of_mass(mass - w, q, sigma) - s0 for w in omega])
        else:
            exponent = -xs
        number_integrand = (omega ** max(bath_dim - 1, 0)) * np.exp(exponent)
        weights.append(float(np.trapezoid(number_integrand, omega)))
        energy_weights.append(float(np.trapezoid(omega * number_integrand, omega)))

    probs = np.array(weights, dtype=float)
    probs = probs / np.sum(probs)
    mean_omega = float(np.sum(energy_weights) / np.sum(weights))
    return probs, mean_omega


def integer_degeneracy_approx(probs: np.ndarray, total: int) -> np.ndarray:
    raw = probs * total
    counts = np.maximum(1, np.floor(raw).astype(int))
    while int(np.sum(counts)) < total:
        idx = int(np.argmax(raw - counts))
        counts[idx] += 1
    while int(np.sum(counts)) > total:
        candidates = np.where(counts > 1)[0]
        idx = int(candidates[np.argmin(raw[candidates] - counts[candidates])])
        counts[idx] -= 1
    return counts / np.sum(counts)


def row_for_L(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    finite_total: int,
) -> dict[str, float | int]:
    mass = 4.0 * sigma * L
    beta = beta_of_mass(mass, q, sigma)
    exact, mean_exact = bin_weights(mass, q, sigma, bath_dim, x_edges, n_grid, exact=True)
    canonical, mean_canonical = bin_weights(mass, q, sigma, bath_dim, x_edges, n_grid, exact=False)
    finite = integer_degeneracy_approx(canonical, finite_total)
    return {
        "L": L,
        "mass": mass,
        "beta": beta,
        "temperature": 1.0 / beta,
        "bath_dim": bath_dim,
        "n_bins": len(exact),
        "exact_p_last": float(exact[-1]),
        "canonical_p_last": float(canonical[-1]),
        "finite_p_last": float(finite[-1]),
        "D_exact_canonical": float(0.5 * np.sum(np.abs(exact - canonical))),
        "D_exact_finite": float(0.5 * np.sum(np.abs(exact - finite))),
        "mean_omega_over_T_exact": mean_exact * beta,
        "mean_omega_over_T_canonical": mean_canonical * beta,
        "finite_total": finite_total,
    }


def fit_decay(rows: list[dict[str, float | int]], key: str, min_L: int) -> float:
    xs = []
    ys = []
    for row in rows:
        val = float(row[key])
        if int(row["L"]) >= min_L and val > 0.0:
            xs.append(math.log(float(row["L"])))
            ys.append(math.log(val))
    return float(np.polyfit(np.array(xs), np.array(ys), 1)[0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--x-edges", nargs="+", type=float, default=[0.0, 2.0, 8.0])
    parser.add_argument("--n-grid", type=int, default=2001)
    parser.add_argument("--max-L", type=int, default=100)
    parser.add_argument("--min-fit-L", type=int, default=20)
    parser.add_argument("--finite-total", type=int, default=64)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/edge_thermal_occupation.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/edge_thermal_occupation_summary.csv"),
    )
    args = parser.parse_args()

    x_edges = np.array(args.x_edges, dtype=float)
    rows = [
        row_for_L(L, args.q, args.sigma, args.bath_dim, x_edges, args.n_grid, args.finite_total)
        for L in range(2, args.max_L + 1)
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "q": args.q,
        "sigma": args.sigma,
        "bath_dim": args.bath_dim,
        "n_bins": len(x_edges) - 1,
        "finite_total": args.finite_total,
        "fit_min_L": args.min_fit_L,
        "D_exact_canonical_decay_slope": fit_decay(rows, "D_exact_canonical", args.min_fit_L),
        "mean_D_exact_canonical_last10": float(np.mean([row["D_exact_canonical"] for row in rows[-10:]])),
        "mean_D_exact_finite_last10": float(np.mean([row["D_exact_finite"] for row in rows[-10:]])),
        "mean_exact_p_last_last10": float(np.mean([row["exact_p_last"] for row in rows[-10:]])),
        "mean_canonical_p_last_last10": float(np.mean([row["canonical_p_last"] for row in rows[-10:]])),
        "mean_omega_over_T_exact_last10": float(np.mean([row["mean_omega_over_T_exact"] for row in rows[-10:]])),
        "mean_omega_over_T_canonical_last10": float(np.mean([row["mean_omega_over_T_canonical"] for row in rows[-10:]])),
    }
    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print(f"D(exact, canonical) decay slope: {summary['D_exact_canonical_decay_slope']:.4f}")
    print(f"mean D(exact, canonical) last10: {summary['mean_D_exact_canonical_last10']:.6e}")
    print(f"mean D(exact, finite {args.finite_total}) last10: {summary['mean_D_exact_finite_last10']:.6e}")
    print()
    print("L   exact_p_last  canon_p_last  D_exact_can  mean_w/T exact  mean_w/T can")
    for row in rows[:5] + rows[-5:]:
        print(
            f"{int(row['L']):3d} "
            f"{row['exact_p_last']:12.6f} "
            f"{row['canonical_p_last']:12.6f} "
            f"{row['D_exact_canonical']:12.6e} "
            f"{row['mean_omega_over_T_exact']:14.6f} "
            f"{row['mean_omega_over_T_canonical']:13.6f}"
        )


if __name__ == "__main__":
    main()
