"""Dynamical typicalization of a boundary edge mode.

This tests the remaining assumption after edge_canonical_typicality.py:

    Does a finite Hamiltonian on edge + reservoir drive non-typical edge
    populations toward the microcanonical sector weights?

The microcanonical shell is modeled as a direct sum:

    H_shell = direct_sum_h |h>_edge tensor C^(d_h)

where d_h approximates the reservoir degeneracy exp[S(M - omega_h)] times the
bin density factor.  A Hamiltonian is then chosen in this shell.

Variants:
    full_random:
        one GOE/GUE-like Hamiltonian on the full shell.  This is the strongest
        scrambling/ETH-like control.

    banded:
        a random Hermitian matrix with a finite bandwidth after grouping basis
        states by edge sector.  This is less idealized and tests whether weaker
        mixing still relaxes populations.

The initial state starts entirely in one edge sector.  We evolve and measure
the edge population trace distance to the microcanonical weights.
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


def exact_weights(mass: float, q: int, sigma: float, omegas: np.ndarray, factors: np.ndarray) -> np.ndarray:
    s0 = entropy_of_mass(mass, q, sigma)
    weights = factors * np.array([math.exp(entropy_of_mass(mass - w, q, sigma) - s0) for w in omegas])
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


def sector_slices(counts: np.ndarray) -> list[slice]:
    out = []
    start = 0
    for count in counts:
        stop = start + int(count)
        out.append(slice(start, stop))
        start = stop
    return out


def random_hermitian(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    h = (z + z.conj().T) / (2.0 * math.sqrt(dim))
    return h


def banded_hermitian(dim: int, bandwidth: int, rng: np.random.Generator) -> np.ndarray:
    h = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(dim):
        j0 = max(0, i - bandwidth)
        j1 = min(dim, i + bandwidth + 1)
        vals = rng.normal(size=j1 - j0) + 1j * rng.normal(size=j1 - j0)
        h[i, j0:j1] = vals
    h = (h + h.conj().T) / 2.0
    norm = np.linalg.norm(h, ord="fro")
    if norm > 0:
        h *= math.sqrt(dim) / norm
    return h


def initial_state_in_sector(sector: slice, dim: int, rng: np.random.Generator) -> np.ndarray:
    psi = np.zeros(dim, dtype=np.complex128)
    size = sector.stop - sector.start
    z = rng.normal(size=size) + 1j * rng.normal(size=size)
    z = z / np.linalg.norm(z)
    psi[sector] = z
    return psi


def edge_populations(psi: np.ndarray, sectors: list[slice]) -> np.ndarray:
    return np.array([float(np.vdot(psi[sl], psi[sl]).real) for sl in sectors])


def trace_distance(p: np.ndarray, q: np.ndarray) -> float:
    return float(0.5 * np.sum(np.abs(p - q)))


def evolve_populations(
    hmat: np.ndarray,
    psi0: np.ndarray,
    sectors: list[slice],
    target: np.ndarray,
    times: np.ndarray,
) -> list[dict[str, float]]:
    evals, evecs = np.linalg.eigh(hmat)
    coeff = evecs.conj().T @ psi0
    rows = []
    for t in times:
        psi = evecs @ (np.exp(-1j * evals * t) * coeff)
        pops = edge_populations(psi, sectors)
        rows.append(
            {
                "time": float(t),
                "D_to_target": trace_distance(pops, target),
                "p_last": float(pops[-1]),
                "participation": float(1.0 / np.sum(pops**2)),
            }
        )
    return rows


def run_case(
    variant: str,
    counts: np.ndarray,
    target: np.ndarray,
    initial_sector_index: int,
    times: np.ndarray,
    bandwidth: int,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    dim = int(np.sum(counts))
    sectors = sector_slices(counts)
    if variant == "full_random":
        hmat = random_hermitian(dim, rng)
    elif variant == "banded":
        hmat = banded_hermitian(dim, bandwidth, rng)
    else:
        raise ValueError(f"unknown variant {variant!r}")
    psi0 = initial_state_in_sector(sectors[initial_sector_index], dim, rng)
    rows = evolve_populations(hmat, psi0, sectors, target, times)
    for row in rows:
        row["variant"] = variant
        row["seed"] = seed
        row["initial_sector"] = initial_sector_index
        row["dim"] = dim
        row["bandwidth"] = bandwidth
    return rows


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[str, float], list[dict[str, float | int | str]]] = {}
    for row in rows:
        grouped.setdefault((str(row["variant"]), float(row["time"])), []).append(row)
    summary = []
    for (variant, time), group in sorted(grouped.items()):
        dvals = np.array([float(row["D_to_target"]) for row in group])
        pvals = np.array([float(row["p_last"]) for row in group])
        out: dict[str, float | int | str] = {
            "variant": variant,
            "time": time,
            "n": len(group),
            "D_to_target_mean": float(np.mean(dvals)),
            "D_to_target_std": float(np.std(dvals)),
            "p_last_mean": float(np.mean(pvals)),
            "p_last_std": float(np.std(pvals)),
        }
        summary.append(out)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=40)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--x-edges", nargs="+", type=float, default=[0.0, 2.0, 8.0])
    parser.add_argument("--n-grid", type=int, default=2001)
    parser.add_argument("--total-dim", type=int, default=256)
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--initial-sector", type=int, default=0)
    parser.add_argument("--t-max", type=float, default=30.0)
    parser.add_argument("--n-times", type=int, default=61)
    parser.add_argument("--bandwidth", type=int, default=12)
    parser.add_argument(
        "--variants",
        nargs="+",
        default=["full_random", "banded"],
        choices=["full_random", "banded"],
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/edge_dynamical_typicalization.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/edge_dynamical_typicalization_summary.csv"),
    )
    args = parser.parse_args()

    mass = 4.0 * args.sigma * args.L
    beta = beta_of_mass(mass, args.q, args.sigma)
    omegas, factors = edge_bins(beta, np.array(args.x_edges), args.bath_dim, args.n_grid)
    target = exact_weights(mass, args.q, args.sigma, omegas, factors)
    counts = integer_counts(target, args.total_dim)
    finite_target = counts / np.sum(counts)
    times = np.linspace(0.0, args.t_max, args.n_times)

    rows: list[dict[str, float | int | str]] = []
    for variant in args.variants:
        for seed in range(args.seeds):
            rows.extend(
                run_case(
                    variant,
                    counts,
                    finite_target,
                    args.initial_sector,
                    times,
                    args.bandwidth,
                    seed,
                )
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    final_rows = [row for row in summary if abs(float(row["time"]) - args.t_max) < 1e-12]
    min_rows = []
    for variant in args.variants:
        variant_rows = [row for row in summary if row["variant"] == variant]
        min_rows.append(min(variant_rows, key=lambda row: float(row["D_to_target_mean"])))

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print(f"target weights: {', '.join(f'{p:.4f}' for p in finite_target)}")
    print(f"counts: {', '.join(str(int(c)) for c in counts)}")
    print("variant      D(t=0)   D(final)  D(best)   t_best")
    for variant in args.variants:
        v0 = next(row for row in summary if row["variant"] == variant and abs(float(row["time"])) < 1e-12)
        vf = next(row for row in final_rows if row["variant"] == variant)
        vb = next(row for row in min_rows if row["variant"] == variant)
        print(
            f"{variant:12s} "
            f"{float(v0['D_to_target_mean']):8.4f} "
            f"{float(vf['D_to_target_mean']):9.4f} "
            f"{float(vb['D_to_target_mean']):8.4f} "
            f"{float(vb['time']):8.3f}"
        )


if __name__ == "__main__":
    main()
