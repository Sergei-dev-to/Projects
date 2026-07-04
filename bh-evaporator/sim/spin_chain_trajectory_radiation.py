#!/usr/bin/env python3
"""Trajectory-level radiation diagnostic for the variable-length spin chain.

This is an intermediate diagnostic, not a full quantum radiation calculation.
It samples the jump unraveling of the Track E reduced channel and records
coarse early/late radiation histories. The goal is to test whether the
thermodynamic evaporator also produces discriminating radiation records at
sizes where exact radiation Hilbert-space tracking is too expensive.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import Counter, defaultdict
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from variable_length_spin_chain_pilot import (
    build_rate_maps,
    build_sectors,
    initial_density,
    ratio_mid_early,
)


@dataclass(frozen=True)
class Case:
    seed: int
    operator: str
    mass_law: str
    max_gap: float


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def entropy_from_counter(counter: Counter[tuple[int, int]]) -> float:
    total = float(sum(counter.values()))
    if total <= 0.0:
        return 0.0
    out = 0.0
    for count in counter.values():
        p = count / total
        out -= p * np.log(p)
    return float(out)


def mutual_information(
    joint: Counter[tuple[tuple[int, int], tuple[int, int]]],
) -> float:
    total = float(sum(joint.values()))
    if total <= 0.0:
        return 0.0
    left = Counter()
    right = Counter()
    for (a, b), count in joint.items():
        left[a] += count
        right[b] += count
    out = 0.0
    for (a, b), count in joint.items():
        p_ab = count / total
        p_a = left[a] / total
        p_b = right[b] / total
        out += p_ab * np.log(p_ab / max(p_a * p_b, 1e-300))
    return float(out)


def choose_index(rng: np.random.Generator, probs: NDArray[np.float64]) -> int:
    total = float(np.sum(probs))
    if total <= 0.0:
        raise ValueError("cannot choose from zero probabilities")
    return int(np.searchsorted(np.cumsum(probs), rng.random() * total, side="right"))


def summarize_time_series(values: NDArray[np.float64]) -> tuple[float, float, float]:
    active = values[1:]
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]
    late = active[max(third + 1, 2 * len(active) // 3) :]
    return (
        float(np.mean(early)),
        float(np.mean(mid)),
        float(np.mean(late)) if len(late) else float("nan"),
    )


def run_case(args: argparse.Namespace, case: Case) -> tuple[dict[str, NDArray[np.float64]], dict[str, float]]:
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

    rho0 = initial_density(sectors, args.n_max, case.seed + 50_000)[args.n_max]
    initial_probs = np.maximum(np.real(np.diag(rho0)), 0.0)
    initial_probs /= np.sum(initial_probs)

    rng = np.random.default_rng(case.seed + args.sample_seed_offset)

    energy_sum = np.zeros(args.steps + 1, dtype=float)
    n_sum = np.zeros(args.steps + 1, dtype=float)
    power_sum = np.zeros(args.steps + 1, dtype=float)
    jump_sum = np.zeros(args.steps + 1, dtype=float)

    early_counter: Counter[tuple[int, int]] = Counter()
    late_counter: Counter[tuple[int, int]] = Counter()
    joint_counter: Counter[tuple[tuple[int, int], tuple[int, int]]] = Counter()

    final_n = []
    final_energy = []

    for _traj in range(args.trajectories):
        n = args.n_max
        i = choose_index(rng, initial_probs)
        prev_energy = float(sectors[n].evals[i])
        early_count = 0
        late_count = 0
        early_energy = 0.0
        late_energy = 0.0

        energy_sum[0] += prev_energy
        n_sum[0] += n

        for step in range(args.steps):
            emitted = 0.0
            jumped = 0.0
            if n in rates:
                probs = rates[n][:, i]
                total_jump = float(np.sum(probs))
                if rng.random() < total_jump:
                    f = choose_index(rng, probs)
                    emitted = float(max(omegas[n][f, i], 0.0))
                    jumped = 1.0
                    if step < args.split_step:
                        early_count += 1
                        early_energy += emitted
                    else:
                        late_count += 1
                        late_energy += emitted
                    n -= 1
                    i = f

            current_energy = float(sectors[n].evals[i])
            energy_sum[step + 1] += current_energy
            n_sum[step + 1] += n
            power_sum[step + 1] += prev_energy - current_energy if jumped else 0.0
            jump_sum[step + 1] += jumped
            prev_energy = current_energy

        early_label = (
            early_count,
            int(np.floor(early_energy / args.energy_bin_width + 1e-12)),
        )
        late_label = (
            late_count,
            int(np.floor(late_energy / args.energy_bin_width + 1e-12)),
        )
        early_counter[early_label] += 1
        late_counter[late_label] += 1
        joint_counter[(early_label, late_label)] += 1
        final_n.append(n)
        final_energy.append(prev_energy)

    inv = 1.0 / float(args.trajectories)
    result = {
        "mean_energy": energy_sum * inv,
        "mean_n": n_sum * inv,
        "mean_power": power_sum * inv,
        "jump_probability": jump_sum * inv,
    }

    early_power, mid_power, late_power = summarize_time_series(result["mean_power"])
    early_jump, mid_jump, late_jump = summarize_time_series(result["jump_probability"])
    mi = mutual_information(joint_counter)
    h_early = entropy_from_counter(early_counter)
    h_late = entropy_from_counter(late_counter)

    summary = {
        "seed": case.seed,
        "operator": case.operator,
        "mass_law": case.mass_law,
        "max_gap": case.max_gap,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "trajectories": args.trajectories,
        "energy_bin_width": args.energy_bin_width,
        "initial_energy": float(result["mean_energy"][0]),
        "final_energy": float(result["mean_energy"][-1]),
        "initial_n": float(result["mean_n"][0]),
        "final_n": float(result["mean_n"][-1]),
        "mean_power_early": early_power,
        "mean_power_mid": mid_power,
        "mean_power_late": late_power,
        "accel_ratio_mid_over_early": float(mid_power / max(early_power, 1e-300)),
        "mean_jump_early": early_jump,
        "mean_jump_mid": mid_jump,
        "mean_jump_late": late_jump,
        "jump_ratio_mid_over_early": float(mid_jump / max(early_jump, 1e-300)),
        "early_record_entropy": h_early,
        "late_record_entropy": h_late,
        "early_late_record_mi": mi,
        "normalized_record_mi": float(mi / max(min(h_early, h_late), 1e-300)),
        "early_record_support": float(len(early_counter)),
        "late_record_support": float(len(late_counter)),
        "joint_record_support": float(len(joint_counter)),
        "final_n_std": float(np.std(final_n)),
        "final_energy_std": float(np.std(final_energy)),
    }
    return result, summary


def save_case(
    output_dir: pathlib.Path,
    case: Case,
    result: dict[str, NDArray[np.float64]],
    summary: dict[str, float],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = (
        "spin_chain_trajectory_radiation_"
        f"{case.operator}_{case.mass_law}_seed{case.seed}.npz"
    )
    np.savez(
        output_dir / stem,
        **result,
        **{f"summary_{key}": value for key, value in summary.items()},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sample Track E radiation trajectories.")
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
    parser.add_argument("--split-step", type=int, default=40)
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument("--trajectories", type=int, default=20000)
    parser.add_argument("--sample-seed-offset", type=int, default=230_000)
    parser.add_argument("--energy-bin-width", type=float, default=1.0)
    parser.add_argument("--output-dir", type=pathlib.Path, default=DATADIR)
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "spin_chain_trajectory_radiation_summary.csv",
    )
    args = parser.parse_args(argv)

    operators = parse_list(args.operators, str)
    mass_laws = parse_list(args.mass_laws, str)
    seeds = parse_list(args.seeds, int)
    rows = []
    total = len(seeds) * len(operators) * len(mass_laws)
    count = 0
    for seed in seeds:
        for operator in operators:
            for mass_law in mass_laws:
                count += 1
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                case = Case(seed=seed, operator=operator, mass_law=mass_law, max_gap=max_gap)
                print(
                    f"[traj-rad] {count}/{total}: seed={seed} "
                    f"operator={operator} mass={mass_law}",
                    flush=True,
                )
                result, summary = run_case(args, case)
                save_case(args.output_dir, case, result, summary)
                rows.append(summary)

    args.summary_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with args.summary_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[traj-rad] wrote {args.summary_csv}")
    for row in rows:
        print(
            f"  {row['operator']} {row['mass_law']} seed={row['seed']}: "
            f"accel={row['accel_ratio_mid_over_early']:.3f}, "
            f"MI={row['early_late_record_mi']:.3f}, "
            f"nMI={row['normalized_record_mi']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
