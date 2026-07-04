#!/usr/bin/env python3
"""Diagnose acceleration from outgoing weighted phase space.

For a secular evaporator with transitions i -> f, define

    W_i = sum_f Gamma_{f i} omega_{f i}

where Gamma is the one-step jump probability and omega is the emitted energy.
The instantaneous emitted power is the state average of W_i. This script checks
whether the acceleration seen in Track A/B is captured by the state drifting
toward larger W_i as the internal sector shrinks.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from argparse import Namespace

import numpy as np
from numpy.typing import NDArray

from area_register_rate_scan import (
    build_rate_maps as build_area_rate_maps,
    build_sectors as build_area_sectors,
)
from scan_bose_hubbard_dos import DATADIR
from variable_n_bose_hubbard_evaporation import (
    build_jump_maps as build_varn_jump_maps,
    build_sectors as build_varn_sectors,
)


def summarize_series(prefix: str, values: NDArray[np.float64]) -> dict[str, float]:
    body = values[1:] if len(values) > 1 else values
    third = max(2, len(body) // 3)
    early = body[:third]
    mid = body[third : max(third + 1, 2 * len(body) // 3)]
    late = body[max(third + 1, 2 * len(body) // 3) :]
    return {
        f"{prefix}_early": float(np.mean(early)),
        f"{prefix}_mid": float(np.mean(mid)),
        f"{prefix}_late": float(np.mean(late)) if len(late) else float("nan"),
        f"{prefix}_mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
    }


def area_omegas(sectors) -> dict[int, NDArray[np.float64]]:
    omegas = {}
    for n in sorted(sectors):
        if n - 1 not in sectors:
            continue
        high = sectors[n]
        low = sectors[n - 1]
        omegas[n] = high.evals[None, :] - low.evals[:, None]
    return omegas


def weighted_columns(
    rates: dict[int, NDArray[np.float64]],
    omegas: dict[int, NDArray[np.float64]],
) -> tuple[dict[int, NDArray[np.float64]], dict[int, NDArray[np.float64]]]:
    power_cols = {}
    jump_cols = {}
    for n, rate in rates.items():
        omega = np.maximum(omegas[n], 0.0)
        power_cols[n] = np.sum(rate * omega, axis=0)
        jump_cols[n] = np.sum(rate, axis=0)
    return power_cols, jump_cols


def initial_area_population(sectors, n_max: int, seed: int) -> dict[int, NDArray[np.float64]]:
    rng = np.random.default_rng(seed)
    pops = {n: np.zeros(sector.dim, dtype=float) for n, sector in sectors.items()}
    raw = rng.normal(size=sectors[n_max].dim) + 1j * rng.normal(size=sectors[n_max].dim)
    raw = raw / np.sqrt(float(np.vdot(raw, raw).real))
    pops[n_max] = np.abs(raw) ** 2
    return pops


def initial_varn_population(sectors, n_max: int, e_min: float, e_max: float, seed: int):
    rng = np.random.default_rng(seed)
    pops = {n: np.zeros(sector.dim, dtype=float) for n, sector in sectors.items()}
    evals = sectors[n_max].evals_internal
    mask = (evals >= e_min) & (evals <= e_max)
    if not np.any(mask):
        raise ValueError(f"empty initial window [{e_min}, {e_max}]")
    raw = rng.normal(size=int(np.sum(mask))) + 1j * rng.normal(size=int(np.sum(mask)))
    raw = raw / np.sqrt(float(np.vdot(raw, raw).real))
    pops[n_max][mask] = np.abs(raw) ** 2
    return pops


def step_population(pops, rates):
    next_pops = {n: pop.copy() for n, pop in pops.items()}
    for n, rate in rates.items():
        colsum = np.sum(rate, axis=0)
        leaving = colsum * pops[n]
        next_pops[n] -= leaving
        next_pops[n - 1] += rate @ pops[n]
    total = sum(float(np.sum(pop)) for pop in next_pops.values())
    if total <= 0.0:
        raise FloatingPointError("population vanished")
    for n in next_pops:
        next_pops[n] = np.maximum(next_pops[n], 0.0) / total
    return next_pops


def population_averages(pops, power_cols, jump_cols, sector_energy) -> dict[str, float]:
    power = 0.0
    jump = 0.0
    sector = 0.0
    energy = 0.0
    support = 0.0
    for n, pop in pops.items():
        p = float(np.sum(pop))
        sector += n * p
        energy += float(pop @ sector_energy[n])
        support += p * len(pop)
        if n in power_cols:
            power += float(pop @ power_cols[n])
            jump += float(pop @ jump_cols[n])
    return {
        "predicted_power": power,
        "jump_probability": jump,
        "conditional_omega": power / max(jump, 1e-300),
        "mean_sector": sector,
        "energy": energy,
        "effective_dimension": support,
    }


def sector_phase_space_table(power_cols, jump_cols) -> dict[str, float]:
    rows = {}
    for n in sorted(power_cols):
        rows[f"sector_{n}_mean_power_col"] = float(np.mean(power_cols[n]))
        rows[f"sector_{n}_mean_jump_col"] = float(np.mean(jump_cols[n]))
        rows[f"sector_{n}_max_power_col"] = float(np.max(power_cols[n]))
    return rows


def run_population_diagnostic(
    pops,
    rates,
    omegas,
    sector_energy,
    steps: int,
) -> tuple[dict[str, NDArray[np.float64]], dict[str, float]]:
    power_cols, jump_cols = weighted_columns(rates, omegas)
    records: dict[str, list[float]] = {
        "predicted_power": [],
        "jump_probability": [],
        "conditional_omega": [],
        "mean_sector": [],
        "energy": [],
        "effective_dimension": [],
    }
    for _step in range(steps + 1):
        obs = population_averages(pops, power_cols, jump_cols, sector_energy)
        for key in records:
            records[key].append(obs[key])
        pops = step_population(pops, rates)
    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    summary = {
        **summarize_series("power", result["predicted_power"]),
        **summarize_series("jump", result["jump_probability"]),
        **summarize_series("conditional_omega", result["conditional_omega"]),
        "initial_sector": float(result["mean_sector"][0]),
        "final_sector": float(result["mean_sector"][-1]),
        "initial_effective_dimension": float(result["effective_dimension"][0]),
        "final_effective_dimension": float(result["effective_dimension"][-1]),
        **sector_phase_space_table(power_cols, jump_cols),
    }
    return result, summary


def run_area_case(args, seed: int, operator: str, mass_law: str, max_gap: float):
    sectors = build_area_sectors(
        n_min=args.area_n_min,
        n_max=args.area_n_max,
        q=args.q,
        alpha=args.alpha,
        bandwidth=args.bandwidth,
        mass_law=mass_law,
        seed=seed,
    )
    rates = build_area_rate_maps(
        sectors,
        q=args.q,
        operator=operator,
        seed=seed,
        pmax=args.pmax,
        min_gap=args.area_min_gap,
        max_gap=max_gap,
        ohmic_power=args.ohmic_power,
    )
    omegas = area_omegas(sectors)
    pops = initial_area_population(sectors, args.area_n_max, seed + 50_000)
    energy = {n: sector.evals for n, sector in sectors.items()}
    result, summary = run_population_diagnostic(pops, rates, omegas, energy, args.steps)
    summary.update(
        {
            "model": "area",
            "seed": seed,
            "operator": operator,
            "mass_law": mass_law,
            "max_gap": max_gap,
        }
    )
    return result, summary


def run_varn_case(args, seed: int, mu: float, max_gap: float, e_min: float, e_max: float):
    ns = Namespace(
        sites=args.sites,
        n_max=args.varn_n_max,
        n_min=args.varn_n_min,
        geometry=args.geometry,
        j=args.j,
        u=args.u,
        v_nn=args.v_nn,
        j_inter=args.j_inter,
        disorder=args.disorder,
    )
    sectors = build_varn_sectors(ns, seed)
    rates, omegas = build_varn_jump_maps(
        sectors,
        mu=mu,
        pmax=args.pmax,
        min_gap=args.varn_min_gap,
        max_gap=max_gap,
        ohmic_power=args.ohmic_power,
    )
    pops = initial_varn_population(sectors, args.varn_n_max, e_min, e_max, seed + 50_000)
    energy = {n: mu * n + sector.evals_internal for n, sector in sectors.items()}
    result, summary = run_population_diagnostic(pops, rates, omegas, energy, args.steps)
    summary.update(
        {
            "model": "variable_n_bose_hubbard",
            "seed": seed,
            "mu": mu,
            "max_gap": max_gap,
            "initial_e_min": e_min,
            "initial_e_max": e_max,
        }
    )
    return result, summary


def save_npz(path: pathlib.Path, result: dict[str, NDArray[np.float64]], summary: dict[str, float | str]):
    payload = {key: value for key, value in result.items()}
    payload.update({f"summary_{key}": value for key, value in summary.items()})
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, **payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Diagnose acceleration from outgoing phase space.")
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--seeds", default="2468,2469")

    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--area-n-min", type=int, default=4)
    parser.add_argument("--area-n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--area-min-gap", type=float, default=0.01)
    parser.add_argument("--sqrt-gap", type=float, default=4.0)
    parser.add_argument("--linear-gap", type=float, default=12.0)

    parser.add_argument("--sites", type=int, default=6)
    parser.add_argument("--varn-n-max", type=int, default=8)
    parser.add_argument("--varn-n-min", type=int, default=3)
    parser.add_argument("--geometry", default="ring")
    parser.add_argument("--j", type=float, default=0.5)
    parser.add_argument("--u", type=float, default=-1.0)
    parser.add_argument("--v-nn", type=float, default=-0.2)
    parser.add_argument("--j-inter", type=float, default=0.2)
    parser.add_argument("--disorder", type=float, default=0.02)
    parser.add_argument("--mu", type=float, default=6.0)
    parser.add_argument("--varn-gap", type=float, default=4.0)
    parser.add_argument("--varn-min-gap", type=float, default=0.05)
    parser.add_argument("--initial-e-min", type=float, default=-18.5)
    parser.add_argument("--initial-e-max", type=float, default=-17.0)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "phase_space_acceleration_diagnostic.csv",
    )
    args = parser.parse_args(argv)

    seeds = [int(part.strip()) for part in args.seeds.split(",") if part.strip()]
    rows = []

    for seed in seeds:
        for operator in ["local", "scrambled"]:
            for mass_law, gap in [("sqrt", args.sqrt_gap), ("linear", args.linear_gap)]:
                print(f"[phase-space] area seed={seed} {operator} {mass_law}", flush=True)
                result, summary = run_area_case(args, seed, operator, mass_law, gap)
                save_npz(
                    DATADIR / f"phase_space_area_{operator}_{mass_law}_seed{seed}.npz",
                    result,
                    summary,
                )
                rows.append(summary)

        print(f"[phase-space] variable-N seed={seed}", flush=True)
        result, summary = run_varn_case(
            args,
            seed,
            mu=args.mu,
            max_gap=args.varn_gap,
            e_min=args.initial_e_min,
            e_max=args.initial_e_max,
        )
        save_npz(DATADIR / f"phase_space_varn_seed{seed}.npz", result, summary)
        rows.append(summary)

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[phase-space] wrote {args.output_csv}")
    for row in rows:
        tag = row["model"]
        if tag == "area":
            tag += f" {row['operator']} {row['mass_law']}"
        print(
            f"  {tag} seed={int(row['seed'])}: "
            f"power mid/early={row['power_mid_over_early']:.3f}, "
            f"jump mid/early={row['jump_mid_over_early']:.3f}, "
            f"omega mid/early={row['conditional_omega_mid_over_early']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
