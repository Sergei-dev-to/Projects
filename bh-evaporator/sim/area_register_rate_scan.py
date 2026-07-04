#!/usr/bin/env python3
"""Track B area-register rate kill test.

This tests whether an entropy-correct qubit area register can produce
accelerating evaporation when rates are derived from concrete Hamiltonian
blocks and shrinkage-operator matrix elements, rather than assigned by hand.
"""
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
class AreaSector:
    n: int
    dim: int
    mass: float
    entropy: float
    evals: NDArray[np.float64]
    evecs: NDArray[np.float64]


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def random_symmetric(rng: np.random.Generator, dim: int) -> NDArray[np.float64]:
    raw = rng.normal(size=(dim, dim))
    mat = (raw + raw.T) / 2.0
    return mat / np.sqrt(float(dim))


def build_sectors(
    n_min: int,
    n_max: int,
    q: int,
    alpha: float,
    bandwidth: float,
    mass_law: str,
    seed: int,
) -> dict[int, AreaSector]:
    rng = np.random.default_rng(seed)
    sectors = {}
    for n in range(n_min, n_max + 1):
        dim = int(q**n)
        if mass_law == "sqrt":
            mass = alpha * np.sqrt(float(n))
        elif mass_law == "linear":
            mass = alpha * float(n)
        else:
            raise ValueError(f"unknown mass law: {mass_law}")
        h = mass * np.eye(dim)
        if bandwidth > 0.0:
            h += bandwidth * random_symmetric(rng, dim)
        evals, evecs = la.eigh(h)
        sectors[n] = AreaSector(
            n=n,
            dim=dim,
            mass=mass,
            entropy=float(n * np.log(q)),
            evals=evals,
            evecs=evecs,
        )
    return sectors


def local_removal_ops(high: AreaSector, low: AreaSector, q: int) -> list[NDArray[np.float64]]:
    # Interpret basis as |prefix> tensor |removed qudit>. Each channel projects
    # the removed qudit onto one basis value and keeps the prefix.
    ops = []
    for label in range(q):
        op = np.zeros((low.dim, high.dim), dtype=float)
        for prefix in range(low.dim):
            col = prefix * q + label
            op[prefix, col] = 1.0
        ops.append(op)
    return ops


def scrambled_removal_ops(
    high: AreaSector,
    low: AreaSector,
    q: int,
    rng: np.random.Generator,
) -> list[NDArray[np.float64]]:
    ops = local_removal_ops(high, low, q)
    # Orthogonal rotations on domain and codomain make this a scrambled
    # shrinkage map while preserving singular values/channel capacity.
    raw_h = rng.normal(size=(high.dim, high.dim))
    uh, _ = np.linalg.qr(raw_h)
    raw_l = rng.normal(size=(low.dim, low.dim))
    ul, _ = np.linalg.qr(raw_l)
    return [ul @ op @ uh.T for op in ops]


def build_rate_maps(
    sectors: dict[int, AreaSector],
    q: int,
    operator: str,
    seed: int,
    pmax: float,
    min_gap: float,
    max_gap: float,
    ohmic_power: float,
) -> dict[int, NDArray[np.float64]]:
    rng = np.random.default_rng(seed + 100_000)
    raw_maps = {}
    for n in sorted(sectors):
        if n - 1 not in sectors:
            continue
        high = sectors[n]
        low = sectors[n - 1]
        if operator == "local":
            ops = local_removal_ops(high, low, q)
        elif operator == "scrambled":
            ops = scrambled_removal_ops(high, low, q, rng)
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

    max_col = max(float(np.max(np.sum(rates, axis=0))) for rates in raw_maps.values())
    if max_col <= 0.0:
        raise ValueError("all area-register rates vanished")
    return {n: rates * (pmax / max_col) for n, rates in raw_maps.items()}


def initial_populations(sectors: dict[int, AreaSector], n_max: int) -> dict[int, NDArray[np.float64]]:
    pops = {n: np.zeros(sector.dim, dtype=float) for n, sector in sectors.items()}
    pops[n_max][:] = 1.0 / sectors[n_max].dim
    return pops


def observables(
    sectors: dict[int, AreaSector],
    pops: dict[int, NDArray[np.float64]],
) -> dict[str, float]:
    energy = 0.0
    area = 0.0
    purity = 0.0
    dimension_entropy = 0.0
    effective_dim = 0.0
    for n, pop in pops.items():
        p = float(np.sum(pop))
        energy += float(pop @ sectors[n].evals)
        area += n * p
        purity += float(pop @ pop)
        dimension_entropy += p * sectors[n].entropy
        effective_dim += p * sectors[n].dim
    return {
        "energy": energy,
        "area": area,
        "renyi2_core": -float(np.log(max(purity, 1e-300))),
        "dimension_entropy": dimension_entropy,
        "effective_dimension": effective_dim,
    }


def step_pops(
    sectors: dict[int, AreaSector],
    pops: dict[int, NDArray[np.float64]],
    rate_maps: dict[int, NDArray[np.float64]],
) -> tuple[dict[int, NDArray[np.float64]], float]:
    next_pops = {n: pop.copy() for n, pop in pops.items()}
    emitted = 0.0
    for n, rates in rate_maps.items():
        pop = pops[n]
        colsum = np.sum(rates, axis=0)
        leaving = colsum * pop
        emitted += float(np.sum(leaving))
        next_pops[n] -= leaving
        next_pops[n - 1] += rates @ pop
    total = sum(float(np.sum(pop)) for pop in next_pops.values())
    if total <= 0.0:
        raise FloatingPointError("population norm vanished")
    for n in next_pops:
        next_pops[n] = np.maximum(next_pops[n], 0.0) / total
    return next_pops, emitted / total


def thermo_arrays(sectors: dict[int, AreaSector]) -> tuple[NDArray[np.float64], ...]:
    ns = np.asarray(sorted(sectors), dtype=float)
    mass = np.asarray([sectors[int(n)].mass for n in ns])
    entropy = np.asarray([sectors[int(n)].entropy for n in ns])
    beta = np.gradient(entropy, mass)
    temp = 1.0 / beta
    heat = np.gradient(mass, temp)
    return ns, mass, entropy, temp, heat


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
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "final_dimension_entropy": float(result["dimension_entropy"][-1]),
        "final_effective_dimension": float(result["effective_dimension"][-1]),
        "mean_emitted_probability": float(np.mean(result["emitted_probability"][:-1])),
        "max_jump_probability": float(result["max_jump_probability"]),
    }


def run_case(args: argparse.Namespace, seed: int, operator: str, mass_law: str, max_gap: float):
    sectors = build_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        alpha=args.alpha,
        bandwidth=args.bandwidth,
        mass_law=mass_law,
        seed=seed,
    )
    rates = build_rate_maps(
        sectors,
        q=args.q,
        operator=operator,
        seed=seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=max_gap,
        ohmic_power=args.ohmic_power,
    )
    pops = initial_populations(sectors, args.n_max)

    records = {
        "energy": [],
        "area": [],
        "renyi2_core": [],
        "dimension_entropy": [],
        "effective_dimension": [],
        "emitted_power": [],
        "emitted_probability": [],
    }
    previous_energy = None
    for step in range(args.steps + 1):
        obs = observables(sectors, pops)
        for key in records:
            if key == "emitted_power":
                records[key].append(0.0 if previous_energy is None else previous_energy - obs["energy"])
            elif key == "emitted_probability":
                continue
            else:
                records[key].append(obs[key])
        if step < args.steps:
            previous_energy = obs["energy"]
            pops, emitted = step_pops(sectors, pops, rates)
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
    parser = argparse.ArgumentParser(description="Run area-register rate kill test.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--operators", default="local,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--max-gap-list", default="1,2,4")
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "area_register_rate_scan.csv",
    )
    parser.add_argument(
        "--output-npz",
        type=pathlib.Path,
        default=DATADIR / "area_register_rate_best.npz",
    )
    args = parser.parse_args(argv)

    operators = parse_list(args.operators, str)
    mass_laws = parse_list(args.mass_laws, str)
    max_gaps = parse_list(args.max_gap_list, float)
    seeds = parse_list(args.seeds, int)

    rows = []
    best = None
    best_payload = None
    total = len(seeds) * len(operators) * len(mass_laws) * len(max_gaps)
    count = 0
    for seed in seeds:
        for operator in operators:
            for mass_law in mass_laws:
                for max_gap in max_gaps:
                    count += 1
                    print(
                        f"[area-register] {count}/{total}: seed={seed} "
                        f"operator={operator} mass={mass_law} gap={max_gap:g}",
                        flush=True,
                    )
                    try:
                        result = run_case(args, seed, operator, mass_law, max_gap)
                        summary = summarize(result)
                        row = {
                            "seed": seed,
                            "operator": operator,
                            "mass_law": mass_law,
                            "max_gap": max_gap,
                            **summary,
                        }
                        if (
                            best is None
                            or summary["accel_ratio_mid_over_early"] > best["accel_ratio_mid_over_early"]
                        ):
                            best = row
                            best_payload = (result, row)
                    except Exception as exc:
                        row = {
                            "seed": seed,
                            "operator": operator,
                            "mass_law": mass_law,
                            "max_gap": max_gap,
                            "error": str(exc),
                        }
                    rows.append(row)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[area-register] wrote {args.output_csv}")

    if best_payload:
        result, row = best_payload
        np.savez(
            args.output_npz,
            **{key: value for key, value in vars(args).items() if key not in {"output_csv", "output_npz"}},
            **result,
            **{f"summary_{key}": value for key, value in row.items() if isinstance(value, (int, float, str))},
        )
        print(f"[area-register] wrote {args.output_npz}")
        print("[area-register] best")
        for key in sorted(row):
            if key != "error":
                print(f"  {key}: {row[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
