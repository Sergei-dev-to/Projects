#!/usr/bin/env python3
"""Variable-length spin-chain area-register pilot."""
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


@dataclass(frozen=True)
class SpinSector:
    n: int
    dim: int
    mass: float
    entropy: float
    evals: NDArray[np.float64]
    evecs: NDArray[np.float64]


def pauli() -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=float)
    eye = np.eye(2, dtype=float)
    return sx, sz, eye


def kron_n(ops: list[NDArray[np.float64]]) -> NDArray[np.float64]:
    out = ops[0]
    for op in ops[1:]:
        out = np.kron(out, op)
    return out


def one_site_op(n: int, site: int, op: NDArray[np.float64]) -> NDArray[np.float64]:
    _sx, _sz, eye = pauli()
    ops = [eye] * n
    ops[site] = op
    return kron_n(ops)


def two_site_op(
    n: int,
    site_a: int,
    op_a: NDArray[np.float64],
    site_b: int,
    op_b: NDArray[np.float64],
) -> NDArray[np.float64]:
    _sx, _sz, eye = pauli()
    ops = [eye] * n
    ops[site_a] = op_a
    ops[site_b] = op_b
    return kron_n(ops)


def build_local_spin_hamiltonian(
    n: int,
    jx: float,
    jz: float,
    hx: float,
    hz_disorder: float,
    seed: int,
) -> NDArray[np.float64]:
    sx, sz, _eye = pauli()
    rng = np.random.default_rng(seed + 7919 * n)
    dim = 2**n
    h = np.zeros((dim, dim), dtype=float)

    for i in range(n - 1):
        h += jx * two_site_op(n, i, sx, i + 1, sx)
        h += jz * two_site_op(n, i, sz, i + 1, sz)
    for i in range(n):
        h += hx * one_site_op(n, i, sx)
        if hz_disorder > 0.0:
            h += hz_disorder * rng.uniform(-1.0, 1.0) * one_site_op(n, i, sz)

    h = (h + h.T) / 2.0
    scale = float(np.std(np.linalg.eigvalsh(h)))
    if scale > 1e-12:
        h /= scale
    return h


def random_symmetric(rng: np.random.Generator, dim: int) -> NDArray[np.float64]:
    raw = rng.normal(size=(dim, dim))
    return (raw + raw.T) / (2.0 * np.sqrt(float(dim)))


def build_sectors(args: argparse.Namespace, mass_law: str, seed: int) -> dict[int, SpinSector]:
    rng = np.random.default_rng(seed)
    sectors = {}
    for n in range(args.n_min, args.n_max + 1):
        dim = 2**n
        if mass_law == "sqrt":
            mass = args.alpha * np.sqrt(float(n))
        elif mass_law == "linear":
            mass = args.alpha * float(n)
        else:
            raise ValueError(f"unknown mass law: {mass_law}")

        if args.block_model == "local":
            h0 = build_local_spin_hamiltonian(
                n=n,
                jx=args.jx,
                jz=args.jz,
                hx=args.hx,
                hz_disorder=args.hz_disorder,
                seed=seed,
            )
        elif args.block_model == "random":
            h0 = random_symmetric(rng, dim)
            std = float(np.std(np.linalg.eigvalsh(h0)))
            if std > 1e-12:
                h0 /= std
        else:
            raise ValueError(f"unknown block model: {args.block_model}")

        h = mass * np.eye(dim) + args.bandwidth * h0
        evals, evecs = la.eigh(h)
        sectors[n] = SpinSector(
            n=n,
            dim=dim,
            mass=mass,
            entropy=float(n * np.log(2.0)),
            evals=evals,
            evecs=evecs,
        )
    return sectors


def boundary_removal_ops(high: SpinSector, low: SpinSector) -> list[NDArray[np.float64]]:
    ops = []
    for label in range(2):
        op = np.zeros((low.dim, high.dim), dtype=float)
        for prefix in range(low.dim):
            col = prefix * 2 + label
            op[prefix, col] = 1.0
        ops.append(op)
    return ops


def remove_bit(index: int, site: int, n: int) -> tuple[int, int]:
    bits = [(index >> (n - 1 - k)) & 1 for k in range(n)]
    label = bits[site]
    reduced = bits[:site] + bits[site + 1 :]
    out = 0
    for bit in reduced:
        out = (out << 1) | bit
    return out, label


def bulk_removal_ops(high: SpinSector, low: SpinSector) -> list[NDArray[np.float64]]:
    ops = []
    n = high.n
    scale = 1.0 / np.sqrt(float(n))
    for site in range(n):
        for label in range(2):
            op = np.zeros((low.dim, high.dim), dtype=float)
            for col in range(high.dim):
                row, bit = remove_bit(col, site, n)
                if bit == label:
                    op[row, col] = scale
            ops.append(op)
    return ops


def scrambled_removal_ops(
    high: SpinSector,
    low: SpinSector,
    rng: np.random.Generator,
) -> list[NDArray[np.float64]]:
    ops = boundary_removal_ops(high, low)
    raw_h = rng.normal(size=(high.dim, high.dim))
    uh, _ = np.linalg.qr(raw_h)
    raw_l = rng.normal(size=(low.dim, low.dim))
    ul, _ = np.linalg.qr(raw_l)
    return [ul @ op @ uh.T for op in ops]


def build_rate_maps(
    sectors: dict[int, SpinSector],
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
        if operator == "boundary":
            ops = boundary_removal_ops(high, low)
        elif operator == "bulk":
            ops = bulk_removal_ops(high, low)
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
        raise ValueError("all spin-chain rates vanished")
    return {n: rates * (pmax / max_col) for n, rates in raw_maps.items()}, omega_maps


def initial_density(sectors: dict[int, SpinSector], n_max: int, seed: int):
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


def apply_channel(sectors, blocks, rates):
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


def ratio_mid_early(values: NDArray[np.float64]) -> float:
    active = values[1:]
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]
    return float(np.mean(mid) / max(np.mean(early), 1e-300))


def observables(sectors, blocks, power_cols, jump_cols):
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


def sector_profile_scores(power_cols: dict[int, NDArray[np.float64]], n_initial: int):
    means = {n: float(np.mean(values)) for n, values in power_cols.items()}
    initial = means[n_initial]
    lower = [value for n, value in means.items() if n < n_initial]
    return {
        "structural_ratio_all_lower_over_initial": float(np.mean(lower) / initial),
        "structural_ratio_next_over_initial": float(means[n_initial - 1] / initial),
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
        "jump_mid_over_early": ratio_mid_early(result["jump_probability"]),
        "omega_mid_over_early": ratio_mid_early(result["conditional_omega"]),
        "sector_w_mid_over_early": ratio_mid_early(result["sector_w"]),
        "selection_mid_over_early": ratio_mid_early(result["selection_ratio"]),
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "final_dimension_entropy": float(result["dimension_entropy"][-1]),
        "final_effective_dimension": float(result["effective_dimension"][-1]),
    }


def run_case(args: argparse.Namespace, seed: int, operator: str, mass_law: str, max_gap: float):
    sectors = build_sectors(args, mass_law, seed)
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
        "block_model": args.block_model,
        "max_gap": max_gap,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "dim_max": sectors[args.n_max].dim,
        **summarize(result),
        **sector_profile_scores(power_cols, args.n_max),
    }
    return result, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run variable-length spin-chain evaporator pilot.")
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--block-model", choices=["local", "random"], default="local")
    parser.add_argument("--jx", type=float, default=0.8)
    parser.add_argument("--jz", type=float, default=0.6)
    parser.add_argument("--hx", type=float, default=0.7)
    parser.add_argument("--hz-disorder", type=float, default=0.25)
    parser.add_argument("--operators", default="boundary,bulk,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--sqrt-max-gap", type=float, default=4.0)
    parser.add_argument("--linear-max-gap", type=float, default=12.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "variable_length_spin_chain_pilot.csv",
    )
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
                    f"[spin-chain] {count}/{total}: seed={seed} operator={operator} "
                    f"mass={mass_law} block={args.block_model}",
                    flush=True,
                )
                result, summary = run_case(args, seed, operator, mass_law, max_gap)
                stem = f"variable_length_spin_chain_{args.block_model}_{operator}_{mass_law}_seed{seed}.npz"
                np.savez(args.output_dir / stem, **result, **{f"summary_{k}": v for k, v in summary.items()})
                rows.append(summary)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[spin-chain] wrote {args.output_csv}")
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
