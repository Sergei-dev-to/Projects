#!/usr/bin/env python3
"""Secular Kraus upgrade for the Track B area-register evaporator."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
from numpy.typing import NDArray

from area_register_rate_scan import (
    AreaSector,
    build_rate_maps,
    build_sectors,
    summarize,
    thermo_arrays,
)
from scan_bose_hubbard_dos import DATADIR


def initial_density(sectors: dict[int, AreaSector], n_max: int, seed: int):
    rng = np.random.default_rng(seed)
    blocks: dict[int, NDArray[np.complex128]] = {}
    for n, sector in sectors.items():
        blocks[n] = np.zeros((sector.dim, sector.dim), dtype=np.complex128)
    raw = rng.normal(size=sectors[n_max].dim) + 1j * rng.normal(size=sectors[n_max].dim)
    raw = raw / np.sqrt(float(np.vdot(raw, raw).real))
    blocks[n_max] = np.outer(raw, raw.conj())
    return blocks


def trace_blocks(blocks: dict[int, NDArray[np.complex128]]) -> float:
    return sum(float(np.trace(block).real) for block in blocks.values())


def normalize_blocks(blocks: dict[int, NDArray[np.complex128]]) -> None:
    tr = trace_blocks(blocks)
    if tr <= 0.0:
        raise FloatingPointError("density trace vanished")
    for n in blocks:
        blocks[n] /= tr


def apply_channel(
    sectors: dict[int, AreaSector],
    blocks: dict[int, NDArray[np.complex128]],
    rates: dict[int, NDArray[np.float64]],
) -> tuple[dict[int, NDArray[np.complex128]], float]:
    next_blocks: dict[int, NDArray[np.complex128]] = {}
    stays = {}
    for n, sector in sectors.items():
        if n in rates:
            stays[n] = np.maximum(1.0 - np.sum(rates[n], axis=0), 0.0)
        else:
            stays[n] = np.ones(sector.dim)
        s = np.sqrt(stays[n])
        next_blocks[n] = blocks[n] * s[:, None] * s[None, :]

    emitted = 0.0
    for n, jump in rates.items():
        diag = np.real(np.diag(blocks[n]))
        colsum = np.sum(jump, axis=0)
        emitted += float(np.sum(colsum * diag))
        lower = n - 1
        added = jump @ diag
        idx = np.diag_indices(sectors[lower].dim)
        next_blocks[lower][idx] += added

    for n in next_blocks:
        next_blocks[n] = (next_blocks[n] + next_blocks[n].conj().T) / 2.0
    normalize_blocks(next_blocks)
    return next_blocks, emitted


def observables(sectors: dict[int, AreaSector], blocks: dict[int, NDArray[np.complex128]]):
    energy = 0.0
    area = 0.0
    dimension_entropy = 0.0
    effective_dimension = 0.0
    purity = 0.0
    for n, sector in sectors.items():
        diag = np.real(np.diag(blocks[n]))
        p = float(np.sum(diag))
        energy += float(diag @ sector.evals)
        area += n * p
        dimension_entropy += p * sector.entropy
        effective_dimension += p * sector.dim
        purity += float(np.einsum("ij,ji->", blocks[n], blocks[n]).real)
    return {
        "energy": energy,
        "area": area,
        "dimension_entropy": dimension_entropy,
        "effective_dimension": effective_dimension,
        "purity": max(purity, 1e-300),
        "renyi2_core": -float(np.log(max(purity, 1e-300))),
    }


def run_one(args: argparse.Namespace):
    sectors = build_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        alpha=args.alpha,
        bandwidth=args.bandwidth,
        mass_law=args.mass_law,
        seed=args.seed,
    )
    rates = build_rate_maps(
        sectors,
        q=args.q,
        operator=args.operator,
        seed=args.seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=args.max_gap,
        ohmic_power=args.ohmic_power,
    )
    blocks = initial_density(sectors, args.n_max, args.seed + 50_000)

    records = {
        "energy": [],
        "area": [],
        "dimension_entropy": [],
        "effective_dimension": [],
        "purity": [],
        "renyi2_core": [],
        "emitted_power": [],
        "emitted_probability": [],
        "norm_error": [],
    }
    previous_energy = None
    for step in range(args.steps + 1):
        obs = observables(sectors, blocks)
        for key in records:
            if key == "emitted_power":
                records[key].append(0.0 if previous_energy is None else previous_energy - obs["energy"])
            elif key == "emitted_probability":
                continue
            elif key == "norm_error":
                records[key].append(abs(trace_blocks(blocks) - 1.0))
            else:
                records[key].append(obs[key])
        if step < args.steps:
            previous_energy = obs["energy"]
            blocks, emitted = apply_channel(sectors, blocks, rates)
            records["emitted_probability"].append(emitted)
    records["emitted_probability"].append(0.0)

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    ns, mass, entropy, temp, heat = thermo_arrays(sectors)
    result["area_grid"] = ns
    result["mass_grid"] = mass
    result["entropy_grid"] = entropy
    result["temperature_grid"] = temp
    result["heat_capacity_grid"] = heat
    result["max_jump_probability"] = np.asarray(
        max(float(np.max(np.sum(rate, axis=0))) for rate in rates.values())
    )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run area-register secular Kraus test.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--operator", choices=["local", "scrambled"], default="local")
    parser.add_argument("--mass-law", choices=["sqrt", "linear"], default="sqrt")
    parser.add_argument("--max-gap", type=float, default=4.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "area_register_kraus.npz",
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
        summary_max_norm_error=float(np.max(result["norm_error"])),
    )
    print(f"[area-kraus] wrote {args.output}")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    print(f"  max_norm_error: {np.max(result['norm_error']):.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
