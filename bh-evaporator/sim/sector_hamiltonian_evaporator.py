#!/usr/bin/env python3
"""Sector-Hamiltonian evaporator diagnostic.

This repackages the successful area-register rate model as a single explicit
Hamiltonian-level test:

  H = direct sum_n H_n,
  X_n : H_n -> H_{n-1},
  Gamma_{f i}^{(n)} proportional to |<f,n-1|X_n|i,n>|^2 J(omega).

The script checks what this construction generates by itself:

  * negative-heat-capacity sector thermodynamics,
  * accelerating/decelerating emitted power,
  * outgoing weighted phase-space drift,
  * the shape of the emitted hard-energy spectrum in beta omega units.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from area_register_rate_scan import (
    AreaSector,
    build_sectors,
    initial_populations,
    local_removal_ops,
    observables,
    scrambled_removal_ops,
    step_pops,
)
from scan_bose_hubbard_dos import DATADIR


@dataclass(frozen=True)
class TransitionData:
    rates: dict[int, NDArray[np.float64]]
    omegas: dict[int, NDArray[np.float64]]
    beta_down: dict[int, float]


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def beta_for_downward_step(high: AreaSector, low: AreaSector) -> float:
    return (high.entropy - low.entropy) / max(high.mass - low.mass, 1e-300)


def build_transition_data(
    sectors: dict[int, AreaSector],
    q: int,
    operator: str,
    seed: int,
    pmax: float,
    min_gap: float,
    max_gap: float,
    ohmic_power: float,
) -> TransitionData:
    rng = np.random.default_rng(seed + 100_000)
    raw_rates: dict[int, NDArray[np.float64]] = {}
    omegas: dict[int, NDArray[np.float64]] = {}
    beta_down: dict[int, float] = {}

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
        bath_weight = np.where(mask, np.maximum(omega, 0.0) ** ohmic_power, 0.0)
        rates = np.zeros((low.dim, high.dim), dtype=float)
        for op in ops:
            op_e = low.evecs.T @ op @ high.evecs
            rates += (np.abs(op_e) ** 2) * bath_weight
        raw_rates[n] = rates
        omegas[n] = omega
        beta_down[n] = beta_for_downward_step(high, low)

    max_col = max(float(np.max(np.sum(rates, axis=0))) for rates in raw_rates.values())
    if max_col <= 0.0:
        raise ValueError("all transition rates vanished")
    scale = pmax / max_col
    return TransitionData(
        rates={n: rates * scale for n, rates in raw_rates.items()},
        omegas=omegas,
        beta_down=beta_down,
    )


def target_x_distribution(edges: NDArray[np.float64], ohmic_power: float) -> NDArray[np.float64]:
    x_max = 20.0
    x = np.linspace(0.0, x_max, 20001)
    density = np.maximum(x, 0.0) ** ohmic_power * np.exp(-x)
    total = float(np.trapezoid(density, x))
    probs = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        upper = x_max if np.isinf(hi) else hi
        mask = (x >= lo) & (x < upper)
        probs.append(float(np.trapezoid(density[mask], x[mask])) / max(total, 1e-300))
    out = np.asarray(probs, dtype=float)
    return out / max(float(np.sum(out)), 1e-300)


def spectrum_observables(
    pops: dict[int, NDArray[np.float64]],
    transitions: TransitionData,
    x_edges: NDArray[np.float64],
    target_probs: NDArray[np.float64],
) -> dict[str, float]:
    hist = np.zeros(len(x_edges) - 1, dtype=float)
    number = 0.0
    power = 0.0
    weighted_phase_space = 0.0

    for n, rates in transitions.rates.items():
        pop = pops[n]
        omega = np.maximum(transitions.omegas[n], 0.0)
        weighted = rates * pop[None, :]
        beta_omega = transitions.beta_down[n] * omega
        number += float(np.sum(weighted))
        power += float(np.sum(weighted * omega))
        weighted_phase_space += float(pop @ np.sum(rates * omega, axis=0))
        hist += np.histogram(beta_omega.ravel(), bins=x_edges, weights=weighted.ravel())[0]

    if np.sum(hist) > 0.0:
        probs = hist / np.sum(hist)
        tv = 0.5 * float(np.sum(np.abs(probs - target_probs)))
        mean_x = float(
            np.sum(
                [
                    probs[i]
                    * (0.5 * (x_edges[i] + (20.0 if np.isinf(x_edges[i + 1]) else x_edges[i + 1])))
                    for i in range(len(probs))
                ]
            )
        )
        max_bin_prob = float(np.max(probs))
    else:
        tv = float("nan")
        mean_x = float("nan")
        max_bin_prob = float("nan")

    return {
        "jump_probability": number,
        "emitted_power": power,
        "conditional_omega": power / max(number, 1e-300),
        "weighted_phase_space": weighted_phase_space,
        "spectrum_tv_to_thermal_x": tv,
        "mean_beta_omega": mean_x,
        "max_spectrum_bin_probability": max_bin_prob,
    }


def summarize_series(values: NDArray[np.float64]) -> dict[str, float]:
    body = values[1:] if len(values) > 1 else values
    third = max(2, len(body) // 3)
    early = body[:third]
    mid = body[third : max(third + 1, 2 * len(body) // 3)]
    late = body[max(third + 1, 2 * len(body) // 3) :]
    return {
        "early": float(np.mean(early)),
        "mid": float(np.mean(mid)),
        "late": float(np.mean(late)) if len(late) else float("nan"),
        "mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
    }


def thermo_arrays_clean(sectors: dict[int, AreaSector]) -> tuple[NDArray[np.float64], ...]:
    ns = np.asarray(sorted(sectors), dtype=float)
    mass = np.asarray([sectors[int(n)].mass for n in ns], dtype=float)
    entropy = np.asarray([sectors[int(n)].entropy for n in ns], dtype=float)
    beta = np.gradient(entropy, mass)
    temp = 1.0 / beta
    heat_edges = []
    for dm, dt in zip(np.diff(mass), np.diff(temp)):
        if abs(dt) <= 1e-12:
            heat_edges.append(float("inf"))
        else:
            heat_edges.append(float(dm / dt))
    if heat_edges:
        heat = np.asarray([heat_edges[0], *heat_edges], dtype=float)
    else:
        heat = np.asarray([float("nan")], dtype=float)
    return ns, mass, entropy, temp, heat


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
    transitions = build_transition_data(
        sectors=sectors,
        q=args.q,
        operator=operator,
        seed=seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=max_gap,
        ohmic_power=args.ohmic_power,
    )
    pops = initial_populations(sectors, args.n_max)
    x_edges = np.asarray(args.x_edges, dtype=float)
    target_probs = target_x_distribution(x_edges, args.ohmic_power)

    records: dict[str, list[float]] = {
        "energy": [],
        "area": [],
        "renyi2_core": [],
        "dimension_entropy": [],
        "effective_dimension": [],
        "jump_probability": [],
        "emitted_power": [],
        "conditional_omega": [],
        "weighted_phase_space": [],
        "spectrum_tv_to_thermal_x": [],
        "mean_beta_omega": [],
        "max_spectrum_bin_probability": [],
    }
    time_rows = []
    for step in range(args.steps + 1):
        obs = observables(sectors, pops)
        spec = spectrum_observables(pops, transitions, x_edges, target_probs)
        row = {"step": step, **obs, **spec}
        for key in records:
            records[key].append(float(row[key]))
        time_rows.append(row)
        if step < args.steps:
            pops, _emitted = step_pops(sectors, pops, transitions.rates)

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    ns, mass, entropy, temp, heat = thermo_arrays_clean(sectors)
    result["area_grid"] = ns
    result["mass_grid"] = mass
    result["entropy_grid"] = entropy
    result["temperature_grid"] = temp
    result["heat_capacity_grid"] = heat
    result["max_jump_probability"] = np.asarray(
        max(float(np.max(np.sum(rate, axis=0))) for rate in transitions.rates.values())
    )
    power_summary = summarize_series(result["emitted_power"])
    jump_summary = summarize_series(result["jump_probability"])
    omega_summary = summarize_series(result["conditional_omega"])
    w_summary = summarize_series(result["weighted_phase_space"])
    tv_summary = summarize_series(result["spectrum_tv_to_thermal_x"])
    finite_heat = heat[np.isfinite(heat)]
    summary = {
        "initial_energy": float(result["energy"][0]),
        "final_energy": float(result["energy"][-1]),
        "initial_area": float(result["area"][0]),
        "final_area": float(result["area"][-1]),
        "mean_power_early": power_summary["early"],
        "mean_power_mid": power_summary["mid"],
        "mean_power_late": power_summary["late"],
        "accel_ratio_mid_over_early": power_summary["mid_over_early"],
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "final_dimension_entropy": float(result["dimension_entropy"][-1]),
        "final_effective_dimension": float(result["effective_dimension"][-1]),
        "mean_jump_probability": float(np.mean(result["jump_probability"][1:])),
        "max_jump_probability": float(result["max_jump_probability"]),
        "power_mid_over_early": power_summary["mid_over_early"],
        "jump_mid_over_early": jump_summary["mid_over_early"],
        "conditional_omega_mid_over_early": omega_summary["mid_over_early"],
        "weighted_phase_space_mid_over_early": w_summary["mid_over_early"],
        "mean_spectrum_tv_to_thermal_x": float(np.nanmean(result["spectrum_tv_to_thermal_x"])),
        "mid_spectrum_tv_to_thermal_x": tv_summary["mid"],
        "mean_beta_omega": float(np.nanmean(result["mean_beta_omega"])),
        "min_heat_capacity_grid": float(np.min(finite_heat)) if len(finite_heat) else float("nan"),
        "max_heat_capacity_grid": float(np.max(finite_heat)) if len(finite_heat) else float("nan"),
    }
    return result, summary, time_rows


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run sector-Hamiltonian evaporator diagnostic.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--operators", default="local,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--sqrt-max-gap", type=float, default=4.0)
    parser.add_argument("--linear-max-gap", type=float, default=12.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "sector_hamiltonian_evaporator_summary.csv",
    )
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "sector_hamiltonian_evaporator_timeseries.csv",
    )
    parser.add_argument(
        "--output-npz",
        type=pathlib.Path,
        default=DATADIR / "sector_hamiltonian_evaporator_best.npz",
    )
    args = parser.parse_args(argv)

    rows = []
    time_rows_all = []
    best = None
    best_payload = None
    seeds = parse_list(args.seeds, int)
    operators = parse_list(args.operators, str)
    mass_laws = parse_list(args.mass_laws, str)
    total = len(seeds) * len(operators) * len(mass_laws)
    count = 0
    for seed in seeds:
        for operator in operators:
            for mass_law in mass_laws:
                count += 1
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                print(
                    f"[sector-H] {count}/{total}: seed={seed} "
                    f"operator={operator} mass={mass_law} gap={max_gap:g}",
                    flush=True,
                )
                try:
                    result, summary, time_rows = run_case(args, seed, operator, mass_law, max_gap)
                    row = {
                        "seed": seed,
                        "operator": operator,
                        "mass_law": mass_law,
                        "max_gap": max_gap,
                        **summary,
                    }
                    if best is None or row["power_mid_over_early"] > best["power_mid_over_early"]:
                        best = row
                        best_payload = (result, row)
                    for time_row in time_rows:
                        time_rows_all.append(
                            {
                                "seed": seed,
                                "operator": operator,
                                "mass_law": mass_law,
                                "max_gap": max_gap,
                                **time_row,
                            }
                        )
                except Exception as exc:
                    row = {
                        "seed": seed,
                        "operator": operator,
                        "mass_law": mass_law,
                        "max_gap": max_gap,
                        "error": str(exc),
                    }
                rows.append(row)

    write_csv(args.summary_csv, rows)
    write_csv(args.timeseries_csv, time_rows_all)
    print(f"[sector-H] wrote {args.summary_csv}")
    print(f"[sector-H] wrote {args.timeseries_csv}")

    if best_payload is not None:
        result, row = best_payload
        args.output_npz.parent.mkdir(parents=True, exist_ok=True)
        np.savez(
            args.output_npz,
            **result,
            **{f"summary_{key}": value for key, value in row.items() if isinstance(value, (int, float, str))},
        )
        print(f"[sector-H] wrote {args.output_npz}")

    print("case                         power    jump     omega    W        TV")
    for row in rows:
        if "error" in row:
            print(f"{row['operator']} {row['mass_law']} seed={row['seed']}: ERROR {row['error']}")
            continue
        tag = f"{row['operator']} {row['mass_law']} seed={row['seed']}"
        print(
            f"{tag:28s} "
            f"{row['power_mid_over_early']:7.3f} "
            f"{row['jump_mid_over_early']:7.3f} "
            f"{row['conditional_omega_mid_over_early']:7.3f} "
            f"{row['weighted_phase_space_mid_over_early']:7.3f} "
            f"{row['mean_spectrum_tv_to_thermal_x']:7.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
