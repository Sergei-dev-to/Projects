#!/usr/bin/env python3
"""Secular reduced-density variable-N Bose-Hubbard evaporator.

This keeps the successful variable-N particle-loss rates, but upgrades the
population evolution to a core density-matrix channel. The channel is the
secular Kraus dilation of the rate process: each allowed energy-lowering
transition is a distinct emitted radiation label, and the no-emission Kraus
operator damps coherences according to the survival probabilities.

It is still not full radiation tracking, but if the total state is purified by
the emitted bins then S2(core) is the Renyi-2 entropy of all radiation.
"""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from variable_n_bose_hubbard_evaporation import (
    Sector,
    build_jump_maps,
    build_sectors,
    parse_list,
    summarize,
)


def initial_density(
    sectors: dict[int, Sector],
    n_max: int,
    e_min: float,
    e_max: float,
    seed: int,
) -> dict[tuple[int, int], NDArray[np.complex128]]:
    rng = np.random.default_rng(seed)
    blocks: dict[tuple[int, int], NDArray[np.complex128]] = {}
    for n, sector in sectors.items():
        blocks[(n, n)] = np.zeros((sector.dim, sector.dim), dtype=np.complex128)

    evals = sectors[n_max].evals_internal
    mask = (evals >= e_min) & (evals <= e_max)
    if not np.any(mask):
        raise ValueError(f"initial N={n_max} window has no states: [{e_min}, {e_max}]")
    psi = np.zeros(sectors[n_max].dim, dtype=np.complex128)
    raw = rng.normal(size=int(np.sum(mask))) + 1j * rng.normal(size=int(np.sum(mask)))
    raw = raw / np.sqrt(float(np.vdot(raw, raw).real))
    psi[mask] = raw
    blocks[(n_max, n_max)] = np.outer(psi, psi.conj())
    return blocks


def trace_blocks(blocks: dict[tuple[int, int], NDArray[np.complex128]]) -> float:
    total = 0.0
    for (n, m), block in blocks.items():
        if n == m:
            total += float(np.trace(block).real)
    return total


def normalize_blocks(blocks: dict[tuple[int, int], NDArray[np.complex128]]) -> None:
    tr = trace_blocks(blocks)
    if tr <= 0.0:
        raise FloatingPointError("density trace vanished")
    for key in blocks:
        blocks[key] /= tr


def apply_secular_channel(
    sectors: dict[int, Sector],
    blocks: dict[tuple[int, int], NDArray[np.complex128]],
    jump_maps: dict[int, NDArray[np.float64]],
) -> tuple[dict[tuple[int, int], NDArray[np.complex128]], float]:
    ns = sorted(sectors)
    stays: dict[int, NDArray[np.float64]] = {}
    for n in ns:
        if n in jump_maps:
            stays[n] = np.maximum(1.0 - np.sum(jump_maps[n], axis=0), 0.0)
        else:
            stays[n] = np.ones(sectors[n].dim)

    next_blocks: dict[tuple[int, int], NDArray[np.complex128]] = {}
    for n in ns:
        sn = np.sqrt(stays[n])
        next_blocks[(n, n)] = blocks[(n, n)] * sn[:, None] * sn[None, :]

    emitted_probability = 0.0
    for n, jump in jump_maps.items():
        src_diag = np.real(np.diag(blocks[(n, n)]))
        emitted_probability += float(np.sum(np.sum(jump, axis=0) * src_diag))
        lower = n - 1
        added_diag = jump @ src_diag
        idx = np.diag_indices(sectors[lower].dim)
        next_blocks[(lower, lower)][idx] += added_diag

    for key, block in next_blocks.items():
        next_blocks[key] = (block + block.conj().T) / 2.0
    normalize_blocks(next_blocks)
    return next_blocks, emitted_probability


def observables(
    sectors: dict[int, Sector],
    blocks: dict[tuple[int, int], NDArray[np.complex128]],
    mu: float,
) -> dict[str, float]:
    ns = sorted(sectors)
    energy = 0.0
    internal_energy = 0.0
    particles = 0.0
    sector_probs = {}
    for n in ns:
        diag = np.real(np.diag(blocks[(n, n)]))
        p = float(np.sum(diag))
        sector_probs[n] = p
        energy += float(diag @ (mu * n + sectors[n].evals_internal))
        internal_energy += float(diag @ sectors[n].evals_internal)
        particles += n * p

    purity = 0.0
    for n in ns:
        purity += float(np.einsum("ij,ji->", blocks[(n, n)], blocks[(n, n)]).real)
    purity = max(purity, 1e-300)

    dim_entropy = 0.0
    effective_dim = 0.0
    for n, p in sector_probs.items():
        dim_entropy += p * np.log(float(sectors[n].dim))
        effective_dim += p * sectors[n].dim

    return {
        "energy": energy,
        "internal_energy": internal_energy,
        "particles": particles,
        "purity": purity,
        "renyi2_core": -float(np.log(purity)),
        "dimension_entropy": float(dim_entropy),
        "effective_dimension": float(effective_dim),
        **{f"sector_prob_N{n}": p for n, p in sector_probs.items()},
    }


def path_temperature(energy: NDArray[np.float64], entropy: NDArray[np.float64]) -> NDArray[np.float64]:
    d_s = np.gradient(entropy)
    d_e = np.gradient(energy)
    beta = np.divide(d_s, d_e, out=np.full_like(d_s, np.nan), where=np.abs(d_e) > 1e-14)
    temp = np.divide(1.0, beta, out=np.full_like(beta, np.nan), where=np.abs(beta) > 1e-14)
    return temp


def run_one(args: argparse.Namespace) -> dict[str, NDArray[np.float64]]:
    sectors = build_sectors(args, args.seed)
    jump_maps, _ = build_jump_maps(
        sectors,
        mu=args.mu,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=args.max_gap,
        ohmic_power=args.ohmic_power,
    )
    blocks = initial_density(
        sectors,
        args.n_max,
        args.initial_e_min,
        args.initial_e_max,
        args.seed + 50_000,
    )

    records: dict[str, list[float]] = {
        "energy": [],
        "internal_energy": [],
        "particles": [],
        "purity": [],
        "renyi2_core": [],
        "dimension_entropy": [],
        "effective_dimension": [],
        "emitted_power": [],
        "emitted_probability": [],
        "norm_error": [],
    }
    for n in sorted(sectors):
        records[f"sector_prob_N{n}"] = []

    previous_energy = None
    for step in range(args.steps + 1):
        obs = observables(sectors, blocks, args.mu)
        for key in records:
            if key == "emitted_power":
                records[key].append(0.0 if previous_energy is None else previous_energy - obs["energy"])
            elif key == "emitted_probability":
                continue
            elif key == "norm_error":
                records[key].append(abs(trace_blocks(blocks) - 1.0))
            else:
                records[key].append(float(obs.get(key, 0.0)))

        if step < args.steps:
            previous_energy = obs["energy"]
            blocks, emitted = apply_secular_channel(sectors, blocks, jump_maps)
            records["emitted_probability"].append(emitted)

    records["emitted_probability"].append(0.0)
    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    result["path_temperature"] = path_temperature(result["energy"], result["dimension_entropy"])
    result["dimensions"] = np.asarray([sectors[n].dim for n in sorted(sectors)], dtype=float)
    result["particle_numbers"] = np.asarray(sorted(sectors), dtype=float)
    result["initial_state_count"] = np.asarray(
        int(
            np.sum(
                (sectors[args.n_max].evals_internal >= args.initial_e_min)
                & (sectors[args.n_max].evals_internal <= args.initial_e_max)
            )
        ),
        dtype=float,
    )
    result["max_jump_probability"] = np.asarray(
        max(float(np.max(np.sum(jump, axis=0))) for jump in jump_maps.values()),
        dtype=float,
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run secular Kraus variable-N Bose-Hubbard evaporator.")
    parser.add_argument("--sites", type=int, default=6)
    parser.add_argument("--n-max", type=int, default=8)
    parser.add_argument("--n-min", type=int, default=3)
    parser.add_argument("--geometry", default="ring")
    parser.add_argument("--j", type=float, default=0.5)
    parser.add_argument("--u", type=float, default=-1.0)
    parser.add_argument("--v-nn", type=float, default=-0.2)
    parser.add_argument("--j-inter", type=float, default=0.2)
    parser.add_argument("--disorder", type=float, default=0.02)
    parser.add_argument("--mu", type=float, default=6.0)
    parser.add_argument("--max-gap", type=float, default=4.0)
    parser.add_argument("--initial-e-min", type=float, default=-18.5)
    parser.add_argument("--initial-e-max", type=float, default=-17.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.05)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "variable_n_bose_hubbard_kraus.npz",
    )
    args = parser.parse_args(argv)

    result = run_one(args)
    summary = summarize(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.output,
        **{key: value for key, value in vars(args).items() if key != "output"},
        **result,
        **{f"summary_{key}": value for key, value in summary.items()},
        summary_final_dimension_entropy=float(result["dimension_entropy"][-1]),
        summary_initial_dimension_entropy=float(result["dimension_entropy"][0]),
        summary_final_effective_dimension=float(result["effective_dimension"][-1]),
        summary_initial_effective_dimension=float(result["effective_dimension"][0]),
        summary_final_path_temperature=float(result["path_temperature"][-1]),
    )
    print(f"[varN-kraus] wrote {args.output}")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    print(f"  initial_dimension_entropy: {result['dimension_entropy'][0]:.6g}")
    print(f"  final_dimension_entropy: {result['dimension_entropy'][-1]:.6g}")
    print(f"  initial_effective_dimension: {result['effective_dimension'][0]:.6g}")
    print(f"  final_effective_dimension: {result['effective_dimension'][-1]:.6g}")
    print(f"  final_path_temperature: {result['path_temperature'][-1]:.6g}")
    print(f"  max_norm_error: {np.max(result['norm_error']):.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
