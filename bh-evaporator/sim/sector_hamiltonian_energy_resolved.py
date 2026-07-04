#!/usr/bin/env python3
"""Energy-resolved sector-Hamiltonian evaporator.

This tests the next refinement after sector_hamiltonian_evaporator.py.  The
previous sector Hamiltonian had nearly flat blocks, so every shrinkage event
released approximately the adjacent sector gap.  Here each sector has an
internal density of states over an energy window of order T_n.  The transition
rates are still golden-rule rates from shrinkage matrix elements:

    Gamma_fi proportional to |<f,n-1|X_n|i,n>|^2 omega_fi^p.

The question is whether final-state counting in the explicit sector spectra
can generate both a thermal hard-energy shape and accelerating evaporation.
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
    initial_populations,
    local_removal_ops,
    observables,
    scrambled_removal_ops,
    step_pops,
)
from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_evaporator import (
    spectrum_observables,
    summarize_series,
    target_x_distribution,
    write_csv,
)


@dataclass(frozen=True)
class TransitionData:
    rates: dict[int, NDArray[np.float64]]
    omegas: dict[int, NDArray[np.float64]]
    beta_down: dict[int, float]


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def sector_mass(n: int, alpha: float, mass_law: str) -> float:
    if mass_law == "sqrt":
        return alpha * np.sqrt(float(n))
    if mass_law == "linear":
        return alpha * float(n)
    raise ValueError(f"unknown mass law: {mass_law}")


def sector_temperature(n: int, q: int, alpha: float, mass_law: str) -> float:
    if n <= 1:
        return 1.0
    s_hi = n * np.log(q)
    s_lo = (n - 1) * np.log(q)
    m_hi = sector_mass(n, alpha, mass_law)
    m_lo = sector_mass(n - 1, alpha, mass_law)
    beta = (s_hi - s_lo) / max(m_hi - m_lo, 1e-300)
    return 1.0 / beta


def quantile_grid(dim: int) -> NDArray[np.float64]:
    return (np.arange(dim, dtype=float) + 0.5) / float(dim)


def internal_offsets(
    dim: int,
    beta: float,
    temp: float,
    width_x: float,
    dos: str,
) -> NDArray[np.float64]:
    """Return deterministic quantiles for the internal sector energies."""
    u = quantile_grid(dim)
    width = width_x * temp
    if width <= 0.0:
        return np.zeros(dim, dtype=float)

    if dos == "flat":
        offsets = -width + 2.0 * width * u
    elif dos == "exponential":
        lo = -width
        hi = width
        blo = np.exp(beta * lo)
        bhi = np.exp(beta * hi)
        offsets = np.log(blo + u * (bhi - blo)) / beta
    elif dos == "semicircle":
        # Cheap deterministic approximation to a Wigner-like compact DOS.
        theta = np.pi * u
        offsets = width * np.cos(theta)
        offsets = np.sort(offsets)
    else:
        raise ValueError(f"unknown DOS: {dos}")
    return offsets - float(np.mean(offsets))


def random_orthogonal(dim: int, rng: np.random.Generator) -> NDArray[np.float64]:
    raw = rng.normal(size=(dim, dim))
    qmat, rmat = np.linalg.qr(raw)
    signs = np.sign(np.diag(rmat))
    signs[signs == 0.0] = 1.0
    return qmat * signs[None, :]


def build_energy_resolved_sectors(
    *,
    n_min: int,
    n_max: int,
    q: int,
    alpha: float,
    mass_law: str,
    width_x: float,
    dos: str,
    seed: int,
) -> dict[int, AreaSector]:
    rng = np.random.default_rng(seed)
    sectors: dict[int, AreaSector] = {}
    for n in range(n_min, n_max + 1):
        dim = int(q**n)
        mass = sector_mass(n, alpha, mass_law)
        entropy = n * np.log(q)
        temp = sector_temperature(n, q, alpha, mass_law)
        beta = 1.0 / max(temp, 1e-300)
        offsets = internal_offsets(dim, beta, temp, width_x, dos)
        evals = mass + offsets
        evecs = random_orthogonal(dim, rng)
        sectors[n] = AreaSector(
            n=n,
            dim=dim,
            mass=mass,
            entropy=float(entropy),
            evals=evals,
            evecs=evecs,
        )
    return sectors


def beta_for_downward_step(high: AreaSector, low: AreaSector) -> float:
    return (high.entropy - low.entropy) / max(high.mass - low.mass, 1e-300)


def build_transition_data(
    *,
    sectors: dict[int, AreaSector],
    q: int,
    operator: str,
    seed: int,
    pmax: float,
    x_min: float,
    x_max: float,
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
        beta = beta_for_downward_step(high, low)
        if operator == "local":
            ops = local_removal_ops(high, low, q)
        elif operator == "scrambled":
            ops = scrambled_removal_ops(high, low, q, rng)
        else:
            raise ValueError(f"unknown operator: {operator}")

        omega = high.evals[None, :] - low.evals[:, None]
        x = beta * omega
        mask = (omega > 0.0) & (x >= x_min) & (x <= x_max)
        weights = np.where(mask, np.maximum(omega, 0.0) ** ohmic_power, 0.0)
        rates = np.zeros((low.dim, high.dim), dtype=float)
        for op in ops:
            op_e = low.evecs.T @ op @ high.evecs
            rates += (np.abs(op_e) ** 2) * weights
        raw_rates[n] = rates
        omegas[n] = omega
        beta_down[n] = beta

    max_col = max(float(np.max(np.sum(rates, axis=0))) for rates in raw_rates.values())
    if max_col <= 0.0:
        raise ValueError("all transition rates vanished")
    scale = pmax / max_col
    return TransitionData(
        rates={n: rates * scale for n, rates in raw_rates.items()},
        omegas=omegas,
        beta_down=beta_down,
    )


def run_case(args: argparse.Namespace, seed: int, operator: str, mass_law: str, dos: str, width_x: float):
    sectors = build_energy_resolved_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        alpha=args.alpha,
        mass_law=mass_law,
        width_x=width_x,
        dos=dos,
        seed=seed,
    )
    transitions = build_transition_data(
        sectors=sectors,
        q=args.q,
        operator=operator,
        seed=seed,
        pmax=args.pmax,
        x_min=args.x_min,
        x_max=args.x_max,
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
    }
    for _step in range(args.steps + 1):
        obs = observables(sectors, pops)
        spec = spectrum_observables(pops, transitions, x_edges, target_probs)
        row = {**obs, **spec}
        for key in records:
            records[key].append(float(row[key]))
        pops, _emitted = step_pops(sectors, pops, transitions.rates)
        if args.sector_mixing == "uniform":
            for n, pop in pops.items():
                weight = float(np.sum(pop))
                if weight > 0.0:
                    pops[n] = np.full_like(pop, weight / len(pop))
        elif args.sector_mixing != "none":
            raise ValueError(f"unknown sector mixing: {args.sector_mixing}")

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    power = summarize_series(result["emitted_power"])
    jump = summarize_series(result["jump_probability"])
    omega = summarize_series(result["conditional_omega"])
    tv = summarize_series(result["spectrum_tv_to_thermal_x"])
    summary = {
        "seed": seed,
        "operator": operator,
        "mass_law": mass_law,
        "dos": dos,
        "width_x": width_x,
        "sector_mixing": args.sector_mixing,
        "power_mid_over_early": power["mid_over_early"],
        "jump_mid_over_early": jump["mid_over_early"],
        "conditional_omega_mid_over_early": omega["mid_over_early"],
        "mean_spectrum_tv_to_thermal_x": float(np.nanmean(result["spectrum_tv_to_thermal_x"])),
        "mid_spectrum_tv_to_thermal_x": tv["mid"],
        "mean_beta_omega": float(np.nanmean(result["mean_beta_omega"])),
        "initial_area": float(result["area"][0]),
        "final_area": float(result["area"][-1]),
        "initial_energy": float(result["energy"][0]),
        "final_energy": float(result["energy"][-1]),
        "final_dimension_entropy": float(result["dimension_entropy"][-1]),
    }
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run energy-resolved sector-Hamiltonian scan.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--operators", default="scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--dos-list", default="flat,exponential,semicircle")
    parser.add_argument("--width-x-list", default="1,2,4,8")
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--x-min", type=float, default=0.0)
    parser.add_argument("--x-max", type=float, default=8.0)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument("--sector-mixing", choices=["none", "uniform"], default="none")
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "sector_hamiltonian_energy_resolved_summary.csv",
    )
    args = parser.parse_args(argv)

    seeds = parse_list(args.seeds, int)
    operators = parse_list(args.operators, str)
    mass_laws = parse_list(args.mass_laws, str)
    dos_list = parse_list(args.dos_list, str)
    width_list = parse_list(args.width_x_list, float)

    rows = []
    total = len(seeds) * len(operators) * len(mass_laws) * len(dos_list) * len(width_list)
    count = 0
    for seed in seeds:
        for operator in operators:
            for mass_law in mass_laws:
                for dos in dos_list:
                    for width_x in width_list:
                        count += 1
                        print(
                            f"[sector-energy] {count}/{total}: seed={seed} "
                            f"{operator} {mass_law} dos={dos} width_x={width_x:g}",
                            flush=True,
                        )
                        try:
                            rows.append(run_case(args, seed, operator, mass_law, dos, width_x))
                        except Exception as exc:
                            rows.append(
                                {
                                    "seed": seed,
                                    "operator": operator,
                                    "mass_law": mass_law,
                                    "dos": dos,
                                    "width_x": width_x,
                                    "error": str(exc),
                                }
                            )

    write_csv(args.summary_csv, rows)
    print(f"[sector-energy] wrote {args.summary_csv}")
    good = [row for row in rows if "error" not in row]
    good.sort(key=lambda row: (float(row["mean_spectrum_tv_to_thermal_x"]), -float(row["power_mid_over_early"])))
    print("best by thermal spectrum:")
    print("mass dos          width  power   jump    omega   TV")
    for row in good[:12]:
        print(
            f"{row['mass_law']:6s} {row['dos']:12s} {float(row['width_x']):5.1f} "
            f"{float(row['power_mid_over_early']):7.3f} "
            f"{float(row['jump_mid_over_early']):7.3f} "
            f"{float(row['conditional_omega_mid_over_early']):7.3f} "
            f"{float(row['mean_spectrum_tv_to_thermal_x']):7.3f}"
        )
    viable = [
        row
        for row in good
        if row["mass_law"] == "sqrt"
        and float(row["power_mid_over_early"]) > 1.0
        and float(row["mean_spectrum_tv_to_thermal_x"]) < 0.3
    ]
    print(f"sqrt cases with acceleration and TV < 0.3: {len(viable)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
