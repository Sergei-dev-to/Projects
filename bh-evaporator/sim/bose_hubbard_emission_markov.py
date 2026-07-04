#!/usr/bin/env python3
"""Weak-coupling emission dynamics for a Bose-Hubbard natural core.

This is a Step 3 screening test. It uses local Bose-Hubbard observables to
generate energy-lowering transition rates in the eigenbasis, then evolves the
core populations with a trace-preserving Markov map. A successful run here is
not yet the full collision-Hamiltonian evaporator; it is a cheap test of
whether the natural core's convex DOS window produces accelerating emission
under physical local couplings.
"""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.linalg as la
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from scan_bose_hubbard_dos import DATADIR, build_bose_hubbard, make_edges


def build_local_operators(
    basis: list[tuple[int, ...]],
    geometry: str,
    j_inter: float,
    mode: str,
) -> list[NDArray[np.float64]]:
    sites = len(basis[0])
    index = {state: idx for idx, state in enumerate(basis)}
    dim = len(basis)
    ops: list[NDArray[np.float64]] = []

    if mode in {"density", "both"}:
        for site in range(sites):
            op = np.zeros((dim, dim), dtype=float)
            avg = np.mean([state[site] for state in basis])
            for a, state in enumerate(basis):
                op[a, a] = state[site] - avg
            ops.append(op)

    if mode in {"hopping", "both"}:
        for i, k, edge_scale in make_edges(sites, geometry, j_inter):
            op = np.zeros((dim, dim), dtype=float)
            for a, state in enumerate(basis):
                n = np.array(state, dtype=int)
                if n[k] > 0:
                    moved = list(state)
                    moved[i] += 1
                    moved[k] -= 1
                    b = index[tuple(moved)]
                    op[b, a] += edge_scale * np.sqrt((n[i] + 1) * n[k])
                if n[i] > 0:
                    moved = list(state)
                    moved[i] -= 1
                    moved[k] += 1
                    b = index[tuple(moved)]
                    op[b, a] += edge_scale * np.sqrt(n[i] * (n[k] + 1))
            ops.append((op + op.T) / 2.0)

    if not ops:
        raise ValueError(f"unknown operator mode: {mode}")
    return ops


def transition_matrix(
    evals: NDArray[np.float64],
    evecs: NDArray[np.float64],
    ops: list[NDArray[np.float64]],
    pmax: float,
    min_gap: float,
    max_gap: float,
    ohmic_power: float,
) -> NDArray[np.float64]:
    dim = len(evals)
    gaps = evals[None, :] - evals[:, None]  # final row lower than initial col when positive
    mask = (gaps >= min_gap) & (gaps <= max_gap)
    rates = np.zeros((dim, dim), dtype=float)
    weights = np.power(np.maximum(gaps, 0.0), ohmic_power, where=gaps >= 0.0)
    weights[~np.isfinite(weights)] = 0.0

    for op in ops:
        op_e = evecs.T @ op @ evecs
        rates += (np.abs(op_e) ** 2) * weights * mask

    np.fill_diagonal(rates, 0.0)
    col_sum = np.sum(rates, axis=0)
    max_col = float(np.max(col_sum))
    if max_col <= 0.0:
        raise ValueError("all transition rates vanished")
    jump = rates * (pmax / max_col)
    stay = 1.0 - np.sum(jump, axis=0)
    if np.min(stay) < -1e-10:
        raise FloatingPointError("transition matrix is not stochastic")
    trans = jump.copy()
    trans[np.diag_indices(dim)] = np.maximum(stay, 0.0)
    return trans


def initial_distribution(
    evals: NDArray[np.float64],
    e_min: float,
    e_max: float,
) -> NDArray[np.float64]:
    mask = (evals >= e_min) & (evals <= e_max)
    if not np.any(mask):
        raise ValueError(f"initial window contains no states: [{e_min}, {e_max}]")
    p = np.zeros_like(evals, dtype=float)
    p[mask] = 1.0 / float(np.sum(mask))
    return p


def run(args: argparse.Namespace) -> dict[str, NDArray[np.float64] | float | int | str]:
    h, basis = build_bose_hubbard(
        sites=args.sites,
        particles=args.particles,
        geometry=args.geometry,
        j=args.j,
        u=args.u,
        v_nn=args.v_nn,
        j_inter=args.j_inter,
        disorder=args.disorder,
        seed=args.seed,
    )
    evals, evecs = la.eigh(h)
    ops = build_local_operators(basis, args.geometry, args.j_inter, args.operator_mode)
    trans = transition_matrix(
        evals,
        evecs,
        ops,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=args.max_gap,
        ohmic_power=args.ohmic_power,
    )
    p = initial_distribution(evals, args.initial_e_min, args.initial_e_max)

    energy = []
    emitted_power = []
    emitted_probability = []
    renyi2_core = []
    shannon_core = []
    previous_energy = None

    for step in range(args.steps + 1):
        e_mean = float(p @ evals)
        purity = float(p @ p)
        entropy = -float(np.sum(p[p > 0.0] * np.log(p[p > 0.0])))
        energy.append(e_mean)
        emitted_power.append(0.0 if previous_energy is None else previous_energy - e_mean)
        renyi2_core.append(-float(np.log(max(purity, 1e-300))))
        shannon_core.append(entropy)

        if step < args.steps:
            previous_energy = e_mean
            next_p = trans @ p
            emitted_probability.append(float(1.0 - np.sum(np.diag(trans) * p)))
            p = next_p / np.sum(next_p)

    emitted_probability.append(0.0)
    return {
        "evals": evals,
        "energy": np.asarray(energy),
        "emitted_power": np.asarray(emitted_power),
        "emitted_probability": np.asarray(emitted_probability),
        "renyi2_core": np.asarray(renyi2_core),
        "shannon_core": np.asarray(shannon_core),
        "transition_col_sum": np.sum(trans - np.diag(np.diag(trans)), axis=0),
        "initial_state_count": int(np.sum((evals >= args.initial_e_min) & (evals <= args.initial_e_max))),
        "dimension": len(evals),
    }


def summarize(result: dict[str, NDArray[np.float64] | float | int | str]) -> dict[str, float]:
    emitted = np.asarray(result["emitted_power"])[1:]
    third = max(2, len(emitted) // 3)
    early = emitted[:third]
    mid = emitted[third : max(third + 1, 2 * len(emitted) // 3)]
    late = emitted[max(third + 1, 2 * len(emitted) // 3) :]
    s2 = np.asarray(result["renyi2_core"])
    return {
        "initial_energy": float(np.asarray(result["energy"])[0]),
        "final_energy": float(np.asarray(result["energy"])[-1]),
        "mean_power_early": float(np.mean(early)),
        "mean_power_mid": float(np.mean(mid)),
        "mean_power_late": float(np.mean(late)) if len(late) else float("nan"),
        "accel_ratio_mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
        "peak_renyi2_core": float(np.max(s2)),
        "peak_renyi2_step": float(np.argmax(s2)),
        "mean_emitted_probability": float(np.mean(np.asarray(result["emitted_probability"])[:-1])),
        "max_jump_probability": float(np.max(np.asarray(result["transition_col_sum"]))),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Bose-Hubbard weak-coupling emission test.")
    parser.add_argument("--sites", type=int, default=6)
    parser.add_argument("--particles", type=int, default=8)
    parser.add_argument("--geometry", default="ring")
    parser.add_argument("--j", type=float, default=0.5)
    parser.add_argument("--u", type=float, default=-1.0)
    parser.add_argument("--v-nn", type=float, default=-0.2)
    parser.add_argument("--j-inter", type=float, default=0.2)
    parser.add_argument("--disorder", type=float, default=0.02)
    parser.add_argument("--operator-mode", choices=["density", "hopping", "both"], default="both")
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.05)
    parser.add_argument("--max-gap", type=float, default=2.0)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--initial-e-min", type=float, default=-18.5)
    parser.add_argument("--initial-e-max", type=float, default=-17.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "bose_hubbard_emission_markov.npz",
    )
    args = parser.parse_args(argv)

    result = run(args)
    summary = summarize(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.output,
        **{key: value for key, value in vars(args).items() if key != "output"},
        **result,
        **{f"summary_{key}": value for key, value in summary.items()},
    )
    print(f"[bh-markov] wrote {args.output}")
    print(f"[bh-markov] dimension={result['dimension']} initial states={result['initial_state_count']}")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
