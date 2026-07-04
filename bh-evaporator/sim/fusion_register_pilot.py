#!/usr/bin/env python3
"""Fibonacci fusion-register evaporator pilot."""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.linalg as la
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from scan_bose_hubbard_dos import DATADIR


VAC = 0
TAU = 1


@dataclass(frozen=True)
class FusionSector:
    n: int
    paths: tuple[tuple[int, ...], ...]
    mass: float
    entropy: float
    evals: NDArray[np.float64]
    evecs: NDArray[np.float64]

    @property
    def dim(self) -> int:
        return len(self.paths)


def random_symmetric(rng: np.random.Generator, dim: int) -> NDArray[np.float64]:
    raw = rng.normal(size=(dim, dim))
    mat = (raw + raw.T) / 2.0
    return mat / np.sqrt(float(max(dim, 1)))


def fusion_paths(n: int) -> tuple[tuple[int, ...], ...]:
    paths: list[tuple[int, ...]] = []

    def extend(prefix: tuple[int, ...], charge: int) -> None:
        if len(prefix) == n:
            paths.append(prefix)
            return
        if charge == VAC:
            extend(prefix + (TAU,), TAU)
        else:
            extend(prefix + (VAC,), VAC)
            extend(prefix + (TAU,), TAU)

    extend((), VAC)
    return tuple(paths)


def build_sectors(
    n_min: int,
    n_max: int,
    alpha: float,
    bandwidth: float,
    mass_law: str,
    seed: int,
) -> dict[int, FusionSector]:
    rng = np.random.default_rng(seed)
    sectors = {}
    for n in range(n_min, n_max + 1):
        paths = fusion_paths(n)
        if mass_law == "sqrt":
            mass = alpha * np.sqrt(float(n))
        elif mass_law == "linear":
            mass = alpha * float(n)
        else:
            raise ValueError(f"unknown mass law: {mass_law}")
        dim = len(paths)
        h = mass * np.eye(dim)
        if bandwidth > 0.0:
            h += bandwidth * random_symmetric(rng, dim)
        evals, evecs = la.eigh(h)
        sectors[n] = FusionSector(
            n=n,
            paths=paths,
            mass=mass,
            entropy=float(np.log(dim)),
            evals=evals,
            evecs=evecs,
        )
    return sectors


def prefix_removal_ops(high: FusionSector, low: FusionSector) -> list[NDArray[np.float64]]:
    low_index = {path: idx for idx, path in enumerate(low.paths)}
    ops = [np.zeros((low.dim, high.dim), dtype=float) for _ in range(2)]
    for col, path in enumerate(high.paths):
        prefix = path[:-1]
        label = path[-1]
        row = low_index[prefix]
        ops[label][row, col] = 1.0
    return ops


def scrambled_removal_ops(
    high: FusionSector,
    low: FusionSector,
    rng: np.random.Generator,
) -> list[NDArray[np.float64]]:
    ops = prefix_removal_ops(high, low)
    raw_h = rng.normal(size=(high.dim, high.dim))
    uh, _ = np.linalg.qr(raw_h)
    raw_l = rng.normal(size=(low.dim, low.dim))
    ul, _ = np.linalg.qr(raw_l)
    return [ul @ op @ uh.T for op in ops]


def build_rate_maps(
    sectors: dict[int, FusionSector],
    operator: str,
    seed: int,
    pmax: float,
    min_gap: float,
    max_gap: float,
    ohmic_power: float,
) -> tuple[dict[int, NDArray[np.float64]], dict[int, NDArray[np.float64]]]:
    rng = np.random.default_rng(seed + 100_000)
    raw_maps = {}
    omega_maps = {}
    for n in sorted(sectors):
        if n - 1 not in sectors:
            continue
        high = sectors[n]
        low = sectors[n - 1]
        if operator == "fusion":
            ops = prefix_removal_ops(high, low)
        elif operator == "scrambled":
            ops = scrambled_removal_ops(high, low, rng)
        else:
            raise ValueError(f"unknown operator: {operator}")
        omega = high.evals[None, :] - low.evals[:, None]
        mask = (omega >= min_gap) & (omega <= max_gap)
        weights = np.where(mask, np.maximum(omega, 0.0) ** ohmic_power, 0.0)
        rates = np.zeros((low.dim, high.dim), dtype=float)
        for op in ops:
            op_e = low.evecs.T @ op @ high.evecs
            rates += (np.abs(op_e) ** 2) * weights
        raw_maps[n] = rates
        omega_maps[n] = omega

    max_col = max(float(np.max(np.sum(rates, axis=0))) for rates in raw_maps.values())
    if max_col <= 0.0:
        raise ValueError("all fusion-register rates vanished")
    return {n: rates * (pmax / max_col) for n, rates in raw_maps.items()}, omega_maps


def initial_density(sectors: dict[int, FusionSector], n_max: int, seed: int):
    rng = np.random.default_rng(seed)
    blocks = {n: np.zeros((sector.dim, sector.dim), dtype=np.complex128) for n, sector in sectors.items()}
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
    sectors: dict[int, FusionSector],
    blocks: dict[int, NDArray[np.complex128]],
    rates: dict[int, NDArray[np.float64]],
) -> tuple[dict[int, NDArray[np.complex128]], float]:
    next_blocks = {}
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
        added = jump @ diag
        idx = np.diag_indices(sectors[n - 1].dim)
        next_blocks[n - 1][idx] += added

    for n in next_blocks:
        next_blocks[n] = (next_blocks[n] + next_blocks[n].conj().T) / 2.0
    normalize_blocks(next_blocks)
    return next_blocks, emitted


def weighted_columns(rates, omegas):
    power_cols = {}
    jump_cols = {}
    for n, rate in rates.items():
        omega = np.maximum(omegas[n], 0.0)
        power_cols[n] = np.sum(rate * omega, axis=0)
        jump_cols[n] = np.sum(rate, axis=0)
    return power_cols, jump_cols


def observables(
    sectors: dict[int, FusionSector],
    blocks: dict[int, NDArray[np.complex128]],
    power_cols: dict[int, NDArray[np.float64]],
    jump_cols: dict[int, NDArray[np.float64]],
):
    energy = 0.0
    area = 0.0
    dim_entropy = 0.0
    effective_dim = 0.0
    purity = 0.0
    w_actual = 0.0
    jump_actual = 0.0
    sector_w = 0.0
    for n, sector in sectors.items():
        diag = np.real(np.diag(blocks[n]))
        p = float(np.sum(diag))
        energy += float(diag @ sector.evals)
        area += n * p
        dim_entropy += p * sector.entropy
        effective_dim += p * sector.dim
        purity += float(np.einsum("ij,ji->", blocks[n], blocks[n]).real)
        if n in power_cols:
            mean_w_n = float(np.mean(power_cols[n]))
            w_actual += float(diag @ power_cols[n])
            jump_actual += float(diag @ jump_cols[n])
            sector_w += p * mean_w_n
    return {
        "energy": energy,
        "area": area,
        "dimension_entropy": dim_entropy,
        "effective_dimension": effective_dim,
        "renyi2_core": -float(np.log(max(purity, 1e-300))),
        "w_actual": w_actual,
        "jump_probability": jump_actual,
        "conditional_omega": w_actual / max(jump_actual, 1e-300),
        "sector_w": sector_w,
        "selection_ratio": w_actual / max(sector_w, 1e-300),
    }


def summarize(result: dict[str, NDArray[np.float64]]) -> dict[str, float]:
    power = result["emitted_power"][1:]
    third = max(2, len(power) // 3)
    early = power[:third]
    mid = power[third : max(third + 1, 2 * len(power) // 3)]
    late = power[max(third + 1, 2 * len(power) // 3) :]
    return {
        "initial_energy": float(result["energy"][0]),
        "final_energy": float(result["energy"][-1]),
        "initial_area": float(result["area"][0]),
        "final_area": float(result["area"][-1]),
        "mean_power_early": float(np.mean(early)),
        "mean_power_mid": float(np.mean(mid)),
        "mean_power_late": float(np.mean(late)) if len(late) else float("nan"),
        "accel_ratio_mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
        "w_mid_over_early": ratio_mid_early(result["w_actual"]),
        "sector_w_mid_over_early": ratio_mid_early(result["sector_w"]),
        "selection_mid_over_early": ratio_mid_early(result["selection_ratio"]),
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "final_dimension_entropy": float(result["dimension_entropy"][-1]),
        "final_effective_dimension": float(result["effective_dimension"][-1]),
    }


def ratio_mid_early(values: NDArray[np.float64]) -> float:
    active = values[1:]
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]
    return float(np.mean(mid) / max(np.mean(early), 1e-300))


def sector_profile_scores(power_cols: dict[int, NDArray[np.float64]], n_initial: int) -> dict[str, float]:
    means = {n: float(np.mean(values)) for n, values in power_cols.items()}
    initial = means.get(n_initial, float("nan"))
    lower = [value for n, value in means.items() if n < n_initial]
    return {
        "structural_ratio_all_lower_over_initial": float(np.mean(lower) / initial),
        "structural_ratio_next_over_initial": float(means.get(n_initial - 1, np.nan) / initial),
    }


def run_case(args: argparse.Namespace, seed: int, operator: str, mass_law: str, max_gap: float):
    sectors = build_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        alpha=args.alpha,
        bandwidth=args.bandwidth,
        mass_law=mass_law,
        seed=seed,
    )
    rates, omegas = build_rate_maps(
        sectors,
        operator=operator,
        seed=seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=max_gap,
        ohmic_power=args.ohmic_power,
    )
    power_cols, jump_cols = weighted_columns(rates, omegas)
    blocks = initial_density(sectors, args.n_max, seed + 50_000)

    records = {
        "energy": [],
        "area": [],
        "dimension_entropy": [],
        "effective_dimension": [],
        "renyi2_core": [],
        "w_actual": [],
        "jump_probability": [],
        "conditional_omega": [],
        "sector_w": [],
        "selection_ratio": [],
        "emitted_power": [],
        "emitted_probability": [],
    }
    previous_energy = None
    for step in range(args.steps + 1):
        obs = observables(sectors, blocks, power_cols, jump_cols)
        for key in records:
            if key == "emitted_power":
                records[key].append(0.0 if previous_energy is None else previous_energy - obs["energy"])
            elif key == "emitted_probability":
                continue
            else:
                records[key].append(obs[key])
        if step < args.steps:
            previous_energy = obs["energy"]
            blocks, emitted = apply_channel(sectors, blocks, rates)
            records["emitted_probability"].append(emitted)
    records["emitted_probability"].append(0.0)

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    summary = {
        "seed": seed,
        "operator": operator,
        "mass_law": mass_law,
        "max_gap": max_gap,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "dim_min": sectors[args.n_min].dim,
        "dim_max": sectors[args.n_max].dim,
        **summarize(result),
        **sector_profile_scores(power_cols, args.n_max),
    }
    return result, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Fibonacci fusion-register pilot.")
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=14)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--operators", default="fusion,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--sqrt-max-gap", type=float, default=4.0)
    parser.add_argument("--linear-max-gap", type=float, default=12.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument("--output-csv", type=pathlib.Path, default=DATADIR / "fusion_register_pilot.csv")
    parser.add_argument("--output-dir", type=pathlib.Path, default=DATADIR)
    args = parser.parse_args(argv)

    operators = [part.strip() for part in args.operators.split(",") if part.strip()]
    mass_laws = [part.strip() for part in args.mass_laws.split(",") if part.strip()]
    seeds = [int(part.strip()) for part in args.seeds.split(",") if part.strip()]
    rows = []
    total = len(seeds) * len(operators) * len(mass_laws)
    count = 0
    for seed in seeds:
        for operator in operators:
            for mass_law in mass_laws:
                count += 1
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                print(
                    f"[fusion] {count}/{total}: seed={seed} operator={operator} "
                    f"mass={mass_law} gap={max_gap:g}",
                    flush=True,
                )
                result, summary = run_case(args, seed, operator, mass_law, max_gap)
                stem = f"fusion_register_{operator}_{mass_law}_seed{seed}.npz"
                np.savez(args.output_dir / stem, **result, **{f"summary_{k}": v for k, v in summary.items()})
                rows.append(summary)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[fusion] wrote {args.output_csv}")
    for row in rows:
        print(
            f"  {row['operator']} {row['mass_law']} seed={row['seed']}: "
            f"accel={row['accel_ratio_mid_over_early']:.3f}, "
            f"W={row['w_mid_over_early']:.3f}, "
            f"sectorW={row['sector_w_mid_over_early']:.3f}, "
            f"select={row['selection_mid_over_early']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
