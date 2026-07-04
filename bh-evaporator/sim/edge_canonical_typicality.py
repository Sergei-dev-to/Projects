"""Canonical typicality diagnostic for the boundary edge mode.

Question:
    Can the boundary edge occupation used by the energy-aware emission block
    arise from typicality of a large droplet reservoir?

For edge energy bins omega_h, the exact microcanonical reduced state of the edge
inside a total energy shell is

    p_h ~ g_h exp[S(M - omega_h)].

For large L this should match

    p_h ~ g_h exp[-beta(M) omega_h]

with O(L^-2) corrections.  A Haar-typical pure state in the corresponding
microcanonical subspace should have an edge reduced density close to these
weights, with fluctuations controlled by the reservoir dimension.

This script builds a finite reservoir with integer degeneracies approximating
exp[S(M - omega_h)] and samples typical pure states in the energy shell.
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


def edge_bins(beta: float, x_edges: np.ndarray, bath_dim: int, n_grid: int) -> tuple[np.ndarray, np.ndarray]:
    """Return representative omega_h and bin degeneracy factors g_h."""
    omegas = []
    factors = []
    for x0, x1 in zip(x_edges[:-1], x_edges[1:]):
        xs = np.linspace(float(x0), float(x1), n_grid)
        omega = xs / beta
        density = omega ** max(bath_dim - 1, 0)
        factor = float(np.trapezoid(density, omega))
        mean_omega = float(np.trapezoid(omega * density, omega) / factor)
        omegas.append(mean_omega)
        factors.append(factor)
    return np.array(omegas), np.array(factors)


def target_weights(
    mass: float,
    q: int,
    sigma: float,
    omegas: np.ndarray,
    factors: np.ndarray,
    exact: bool,
) -> np.ndarray:
    beta = beta_of_mass(mass, q, sigma)
    if exact:
        s0 = entropy_of_mass(mass, q, sigma)
        weights = factors * np.array([math.exp(entropy_of_mass(mass - w, q, sigma) - s0) for w in omegas])
    else:
        weights = factors * np.exp(-beta * omegas)
    return weights / np.sum(weights)


def integer_counts(probs: np.ndarray, total_dim: int) -> np.ndarray:
    raw = probs * total_dim
    counts = np.maximum(1, np.floor(raw).astype(int))
    while int(np.sum(counts)) < total_dim:
        idx = int(np.argmax(raw - counts))
        counts[idx] += 1
    while int(np.sum(counts)) > total_dim:
        candidates = np.where(counts > 1)[0]
        idx = int(candidates[np.argmin(raw[candidates] - counts[candidates])])
        counts[idx] -= 1
    return counts


def sample_edge_probs(counts: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Sample Haar-typical state weights over edge sectors.

    The total Hilbert space is a direct sum over edge sectors:

        H_shell = direct_sum_h |h>_edge tensor C^(counts_h).

    Haar-random pure-state weights in the sectors are Dirichlet distributed
    with parameters counts_h.
    """
    return rng.dirichlet(counts.astype(float))


def trace_distance(p: np.ndarray, q: np.ndarray) -> float:
    return float(0.5 * np.sum(np.abs(p - q)))


def row_for_case(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    total_dim: int,
    samples: int,
    seed: int,
) -> dict[str, float | int]:
    rng = np.random.default_rng(seed + L)
    mass = 4.0 * sigma * L
    beta = beta_of_mass(mass, q, sigma)
    omegas, factors = edge_bins(beta, x_edges, bath_dim, n_grid)
    exact = target_weights(mass, q, sigma, omegas, factors, exact=True)
    canonical = target_weights(mass, q, sigma, omegas, factors, exact=False)
    counts = integer_counts(exact, total_dim)
    finite_exact = counts / np.sum(counts)

    sample_distances = []
    sample_distances_to_can = []
    sample_high = []
    for _ in range(samples):
        sample = sample_edge_probs(counts, rng)
        sample_distances.append(trace_distance(sample, finite_exact))
        sample_distances_to_can.append(trace_distance(sample, canonical))
        sample_high.append(float(sample[-1]))

    return {
        "L": L,
        "mass": mass,
        "beta": beta,
        "temperature": 1.0 / beta,
        "bath_dim": bath_dim,
        "n_bins": len(exact),
        "total_dim": total_dim,
        "samples": samples,
        "exact_p_last": float(exact[-1]),
        "canonical_p_last": float(canonical[-1]),
        "finite_p_last": float(finite_exact[-1]),
        "mean_sample_p_last": float(np.mean(sample_high)),
        "std_sample_p_last": float(np.std(sample_high)),
        "D_exact_canonical": trace_distance(exact, canonical),
        "D_finite_exact": trace_distance(finite_exact, exact),
        "mean_D_sample_finite": float(np.mean(sample_distances)),
        "std_D_sample_finite": float(np.std(sample_distances)),
        "mean_D_sample_canonical": float(np.mean(sample_distances_to_can)),
        "std_D_sample_canonical": float(np.std(sample_distances_to_can)),
        "min_count": int(np.min(counts)),
        "max_count": int(np.max(counts)),
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
    parser.add_argument("--total-dim", type=int, default=4096)
    parser.add_argument("--samples", type=int, default=512)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/edge_canonical_typicality.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/edge_canonical_typicality_summary.csv"),
    )
    args = parser.parse_args()

    x_edges = np.array(args.x_edges, dtype=float)
    rows = [
        row_for_case(
            L,
            args.q,
            args.sigma,
            args.bath_dim,
            x_edges,
            args.n_grid,
            args.total_dim,
            args.samples,
            args.seed,
        )
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
        "total_dim": args.total_dim,
        "samples": args.samples,
        "fit_min_L": args.min_fit_L,
        "D_exact_canonical_decay_slope": fit_decay(rows, "D_exact_canonical", args.min_fit_L),
        "mean_D_exact_canonical_last10": float(np.mean([row["D_exact_canonical"] for row in rows[-10:]])),
        "mean_D_finite_exact_last10": float(np.mean([row["D_finite_exact"] for row in rows[-10:]])),
        "mean_D_sample_finite_last10": float(np.mean([row["mean_D_sample_finite"] for row in rows[-10:]])),
        "mean_D_sample_canonical_last10": float(np.mean([row["mean_D_sample_canonical"] for row in rows[-10:]])),
        "mean_sample_p_last_last10": float(np.mean([row["mean_sample_p_last"] for row in rows[-10:]])),
        "mean_exact_p_last_last10": float(np.mean([row["exact_p_last"] for row in rows[-10:]])),
        "mean_canonical_p_last_last10": float(np.mean([row["canonical_p_last"] for row in rows[-10:]])),
    }

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print(f"D(exact, canonical) decay slope: {summary['D_exact_canonical_decay_slope']:.4f}")
    print(f"mean D(exact, canonical) last10: {summary['mean_D_exact_canonical_last10']:.6e}")
    print(f"mean D(sample, finite shell) last10: {summary['mean_D_sample_finite_last10']:.6e}")
    print(f"mean D(sample, canonical) last10: {summary['mean_D_sample_canonical_last10']:.6e}")
    print()
    print("L   exact_p_last  sample_p_last  D_samp_fin  D_samp_can  min/max counts")
    for row in rows[:5] + rows[-5:]:
        print(
            f"{int(row['L']):3d} "
            f"{row['exact_p_last']:12.6f} "
            f"{row['mean_sample_p_last']:13.6f} "
            f"{row['mean_D_sample_finite']:11.6e} "
            f"{row['mean_D_sample_canonical']:11.6e} "
            f"{int(row['min_count']):4d}/{int(row['max_count']):4d}"
        )


if __name__ == "__main__":
    main()
