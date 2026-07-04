#!/usr/bin/env python3
"""Validate the exact Stinespring purification of the Track E channel."""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from variable_length_spin_chain_pilot import (
    SpinSector,
    apply_channel,
    build_rate_maps,
    build_sectors,
    initial_density,
    observables,
    weighted_columns,
)


# Labels are (step, source_n, source_i, target_f). For no-jump outcomes,
# source_i and target_f are -1 so the no-jump Kraus preserves coherence within
# a sector at that step.
History = tuple[tuple[int, int, int, int], ...]
StateKey = tuple[int, int, History]


@dataclass(frozen=True)
class Case:
    seed: int
    operator: str
    mass_law: str
    max_gap: float


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def initial_pure_history(
    sectors: dict[int, SpinSector],
    n_max: int,
    seed: int,
) -> dict[StateKey, complex]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=sectors[n_max].dim) + 1j * rng.normal(size=sectors[n_max].dim)
    raw = raw / np.sqrt(float(np.vdot(raw, raw).real))
    return {
        (n_max, i, ()): complex(amp)
        for i, amp in enumerate(raw)
        if abs(amp) > 0.0
    }


def initial_density_from_same_state(
    sectors: dict[int, SpinSector],
    n_max: int,
    state: dict[StateKey, complex],
) -> dict[int, NDArray[np.complex128]]:
    blocks = {
        n: np.zeros((sector.dim, sector.dim), dtype=np.complex128)
        for n, sector in sectors.items()
    }
    amps = np.zeros(sectors[n_max].dim, dtype=np.complex128)
    for (n, i, history), amp in state.items():
        if n != n_max or history:
            raise ValueError("unexpected initial history state")
        amps[i] = amp
    blocks[n_max] = np.outer(amps, amps.conj())
    return blocks


def normalize_state(state: dict[StateKey, complex]) -> None:
    norm = sum(float(abs(amp) ** 2) for amp in state.values())
    if norm <= 0.0:
        raise FloatingPointError("state norm vanished")
    scale = 1.0 / np.sqrt(norm)
    for key in list(state):
        state[key] *= scale


def evolve_stinespring(
    state: dict[StateKey, complex],
    rates: dict[int, NDArray[np.float64]],
    step: int,
    amplitude_cutoff: float,
    max_branches: int,
) -> dict[StateKey, complex]:
    next_state: defaultdict[StateKey, complex] = defaultdict(complex)
    for (n, i, history), amp in state.items():
        if n not in rates:
            next_state[(n, i, history)] += amp
            continue

        jump = rates[n][:, i]
        total_jump = float(np.sum(jump))
        stay = np.sqrt(max(1.0 - total_jump, 0.0))
        if abs(amp * stay) > amplitude_cutoff:
            next_state[(n, i, history + ((step, n, -1, -1),))] += amp * stay

        for f in np.nonzero(jump > 0.0)[0]:
            jump_amp = amp * np.sqrt(float(jump[f]))
            if abs(jump_amp) <= amplitude_cutoff:
                continue
            next_state[(n - 1, int(f), history + ((step, n, i, int(f)),))] += jump_amp

    compact = dict(next_state)
    if len(compact) > max_branches:
        raise MemoryError(f"branch cap exceeded: {len(compact)} > {max_branches}")
    normalize_state(compact)
    return compact


def trace_radiation(
    sectors: dict[int, SpinSector],
    state: dict[StateKey, complex],
) -> dict[int, NDArray[np.complex128]]:
    groups: dict[History, list[tuple[int, int, complex]]] = defaultdict(list)
    for (n, i, history), amp in state.items():
        groups[history].append((n, i, amp))

    blocks = {
        n: np.zeros((sector.dim, sector.dim), dtype=np.complex128)
        for n, sector in sectors.items()
    }
    for entries in groups.values():
        by_sector: dict[int, list[tuple[int, complex]]] = defaultdict(list)
        for n, i, amp in entries:
            by_sector[n].append((i, amp))
        for n, sector_entries in by_sector.items():
            for i, amp_i in sector_entries:
                for j, amp_j in sector_entries:
                    blocks[n][i, j] += amp_i * amp_j.conjugate()
    return blocks


def block_frobenius_error(
    left: dict[int, NDArray[np.complex128]],
    right: dict[int, NDArray[np.complex128]],
) -> tuple[float, float]:
    diff_norm_sq = 0.0
    ref_norm_sq = 0.0
    for n in left:
        diff = left[n] - right[n]
        diff_norm_sq += float(np.vdot(diff, diff).real)
        ref_norm_sq += float(np.vdot(left[n], left[n]).real)
    diff_norm = float(np.sqrt(diff_norm_sq))
    rel = diff_norm / max(float(np.sqrt(ref_norm_sq)), 1e-300)
    return diff_norm, rel


def run_case(args: argparse.Namespace, case: Case) -> tuple[list[dict[str, float]], dict[str, float]]:
    sectors = build_sectors(args, case.mass_law, case.seed)
    rates, omegas = build_rate_maps(
        sectors,
        operator=case.operator,
        seed=case.seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=case.max_gap,
        ohmic_power=args.ohmic_power,
    )
    power_cols, jump_cols = weighted_columns(rates, omegas)

    pure_state = initial_pure_history(sectors, args.n_max, case.seed + 120_000)
    reduced_blocks = initial_density_from_same_state(sectors, args.n_max, pure_state)

    rows = []
    max_abs_error = 0.0
    max_rel_error = 0.0
    max_energy_error = 0.0
    max_area_error = 0.0
    max_power_error = 0.0
    max_branch_count = 0
    previous_reduced_energy = None
    previous_purified_energy = None

    for step in range(args.steps + 1):
        purified_blocks = trace_radiation(sectors, pure_state)
        abs_err, rel_err = block_frobenius_error(reduced_blocks, purified_blocks)
        reduced_obs = observables(sectors, reduced_blocks, power_cols, jump_cols)
        purified_obs = observables(sectors, purified_blocks, power_cols, jump_cols)

        reduced_power = (
            0.0
            if previous_reduced_energy is None
            else previous_reduced_energy - reduced_obs["energy"]
        )
        purified_power = (
            0.0
            if previous_purified_energy is None
            else previous_purified_energy - purified_obs["energy"]
        )

        energy_error = abs(reduced_obs["energy"] - purified_obs["energy"])
        area_error = abs(reduced_obs["area"] - purified_obs["area"])
        power_error = abs(reduced_power - purified_power)
        row = {
            "step": step,
            "seed": case.seed,
            "operator": case.operator,
            "mass_law": case.mass_law,
            "abs_fro_error": abs_err,
            "rel_fro_error": rel_err,
            "energy_error": energy_error,
            "area_error": area_error,
            "power_error": power_error,
            "reduced_energy": reduced_obs["energy"],
            "purified_energy": purified_obs["energy"],
            "reduced_area": reduced_obs["area"],
            "purified_area": purified_obs["area"],
            "reduced_power": reduced_power,
            "purified_power": purified_power,
            "branch_count": len(pure_state),
        }
        rows.append(row)

        max_abs_error = max(max_abs_error, abs_err)
        max_rel_error = max(max_rel_error, rel_err)
        max_energy_error = max(max_energy_error, energy_error)
        max_area_error = max(max_area_error, area_error)
        max_power_error = max(max_power_error, power_error)
        max_branch_count = max(max_branch_count, len(pure_state))

        if step < args.steps:
            previous_reduced_energy = reduced_obs["energy"]
            previous_purified_energy = purified_obs["energy"]
            reduced_blocks, _emitted = apply_channel(sectors, reduced_blocks, rates)
            pure_state = evolve_stinespring(
                pure_state,
                rates=rates,
                step=step,
                amplitude_cutoff=args.amplitude_cutoff,
                max_branches=args.max_branches,
            )

    summary = {
        "seed": case.seed,
        "operator": case.operator,
        "mass_law": case.mass_law,
        "max_gap": case.max_gap,
        "max_abs_fro_error": max_abs_error,
        "max_rel_fro_error": max_rel_error,
        "max_energy_error": max_energy_error,
        "max_area_error": max_area_error,
        "max_power_error": max_power_error,
        "max_branch_count": float(max_branch_count),
        "final_energy": rows[-1]["reduced_energy"],
        "final_area": rows[-1]["reduced_area"],
    }
    return rows, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Track E Stinespring faithfulness.")
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=7)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--block-model", choices=["local", "random"], default="local")
    parser.add_argument("--jx", type=float, default=0.8)
    parser.add_argument("--jz", type=float, default=0.6)
    parser.add_argument("--hx", type=float, default=0.7)
    parser.add_argument("--hz-disorder", type=float, default=0.25)
    parser.add_argument("--operators", default="boundary,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--sqrt-max-gap", type=float, default=4.0)
    parser.add_argument("--linear-max-gap", type=float, default=12.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=24)
    parser.add_argument("--seeds", default="2468")
    parser.add_argument("--amplitude-cutoff", type=float, default=1e-14)
    parser.add_argument("--max-branches", type=int, default=2_000_000)
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "spin_chain_stinespring_faithfulness_summary.csv",
    )
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "spin_chain_stinespring_faithfulness_timeseries.csv",
    )
    args = parser.parse_args(argv)

    all_rows = []
    summaries = []
    cases = []
    for seed in parse_list(args.seeds, int):
        for operator in parse_list(args.operators, str):
            for mass_law in parse_list(args.mass_laws, str):
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                cases.append(Case(seed, operator, mass_law, max_gap))

    for idx, case in enumerate(cases, start=1):
        print(
            f"[faithful] {idx}/{len(cases)}: seed={case.seed} "
            f"operator={case.operator} mass={case.mass_law}",
            flush=True,
        )
        rows, summary = run_case(args, case)
        all_rows.extend(rows)
        summaries.append(summary)

    args.summary_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_csv.open("w", newline="") as fh:
        fields = sorted({key for row in summaries for key in row})
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)

    with args.timeseries_csv.open("w", newline="") as fh:
        fields = sorted({key for row in all_rows for key in row})
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"[faithful] wrote {args.summary_csv}")
    for row in summaries:
        print(
            f"  {row['operator']} {row['mass_law']} seed={row['seed']}: "
            f"rel_err={row['max_rel_fro_error']:.3e}, "
            f"energy_err={row['max_energy_error']:.3e}, "
            f"branches={row['max_branch_count']:.0f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
