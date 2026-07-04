#!/usr/bin/env python3
"""Robustness scan for the variable-length spin-chain evaporator."""
from __future__ import annotations

import argparse
import csv
import pathlib
from argparse import Namespace

import numpy as np

from scan_bose_hubbard_dos import DATADIR
from variable_length_spin_chain_pilot import (
    apply_channel,
    build_rate_maps,
    build_sectors,
    initial_density,
    observables,
    sector_profile_scores,
    summarize,
    weighted_columns,
)


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def run_case(args: argparse.Namespace, sectors, seed: int, operator: str, mass_law: str, max_gap: float):
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
    return {
        **summarize(result),
        **sector_profile_scores(power_cols, args.n_max),
    }


def group_summary(rows: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    groups = {}
    for row in rows:
        key = (row["bandwidth"], row["operator"], row["mass_law"])
        groups.setdefault(key, []).append(row)

    out = []
    for (bandwidth, operator, mass_law), subset in sorted(groups.items()):
        accel = np.asarray([float(row["accel_ratio_mid_over_early"]) for row in subset])
        w_ratio = np.asarray([float(row["w_mid_over_early"]) for row in subset])
        sector_w = np.asarray([float(row["sector_w_mid_over_early"]) for row in subset])
        selection = np.asarray([float(row["selection_mid_over_early"]) for row in subset])
        jump = np.asarray([float(row["jump_mid_over_early"]) for row in subset])
        omega = np.asarray([float(row["omega_mid_over_early"]) for row in subset])
        s2 = np.asarray([float(row["peak_renyi2_core"]) for row in subset])
        out.append(
            {
                "bandwidth": bandwidth,
                "operator": operator,
                "mass_law": mass_law,
                "rows": float(len(subset)),
                "accel_mean": float(np.mean(accel)),
                "accel_min": float(np.min(accel)),
                "accel_max": float(np.max(accel)),
                "accel_gt1_fraction": float(np.mean(accel > 1.0)),
                "w_mean": float(np.mean(w_ratio)),
                "sector_w_mean": float(np.mean(sector_w)),
                "selection_mean": float(np.mean(selection)),
                "jump_mean": float(np.mean(jump)),
                "omega_mean": float(np.mean(omega)),
                "peak_s2_mean": float(np.mean(s2)),
            }
        )
    return out


def advantage_summary(rows: list[dict[str, float | str]]) -> list[dict[str, float | str]]:
    indexed = {
        (row["bandwidth"], row["seed"], row["mass_law"], row["operator"]): row
        for row in rows
    }
    out = []
    keys = sorted({(row["bandwidth"], row["seed"], row["mass_law"]) for row in rows})
    for bandwidth, seed, mass_law in keys:
        scrambled = indexed.get((bandwidth, seed, mass_law, "scrambled"))
        if not scrambled:
            continue
        for operator in ["boundary", "bulk"]:
            row = indexed.get((bandwidth, seed, mass_law, operator))
            if not row:
                continue
            out.append(
                {
                    "bandwidth": bandwidth,
                    "seed": seed,
                    "mass_law": mass_law,
                    "operator": operator,
                    "accel_advantage": float(row["accel_ratio_mid_over_early"])
                    - float(scrambled["accel_ratio_mid_over_early"]),
                    "w_advantage": float(row["w_mid_over_early"]) - float(scrambled["w_mid_over_early"]),
                    "sector_w_advantage": float(row["sector_w_mid_over_early"])
                    - float(scrambled["sector_w_mid_over_early"]),
                }
            )
    return out


def write_csv(path: pathlib.Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan variable-length spin-chain robustness.")
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidths", default="0.1,0.25,0.5")
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
    parser.add_argument("--seeds", default="2468,2469,2470,2471,2472,2473")
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "variable_length_spin_chain_robustness.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "variable_length_spin_chain_robustness_summary.csv",
    )
    parser.add_argument(
        "--advantage-csv",
        type=pathlib.Path,
        default=DATADIR / "variable_length_spin_chain_robustness_advantage.csv",
    )
    args = parser.parse_args(argv)

    bandwidths = parse_list(args.bandwidths, float)
    operators = parse_list(args.operators, str)
    mass_laws = parse_list(args.mass_laws, str)
    seeds = parse_list(args.seeds, int)
    rows = []

    total_blocks = len(seeds) * len(bandwidths) * len(mass_laws)
    block_count = 0
    for seed in seeds:
        for bandwidth in bandwidths:
            for mass_law in mass_laws:
                block_count += 1
                block_args = Namespace(**vars(args))
                block_args.bandwidth = bandwidth
                print(
                    f"[spin-robust] block {block_count}/{total_blocks}: "
                    f"seed={seed} bandwidth={bandwidth:g} mass={mass_law}",
                    flush=True,
                )
                sectors = build_sectors(block_args, mass_law, seed)
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                for operator in operators:
                    print(
                        f"[spin-robust]   operator={operator}",
                        flush=True,
                    )
                    try:
                        summary = run_case(block_args, sectors, seed, operator, mass_law, max_gap)
                        rows.append(
                            {
                                "seed": seed,
                                "bandwidth": bandwidth,
                                "operator": operator,
                                "mass_law": mass_law,
                                "block_model": args.block_model,
                                "max_gap": max_gap,
                                **summary,
                            }
                        )
                    except Exception as exc:
                        rows.append(
                            {
                                "seed": seed,
                                "bandwidth": bandwidth,
                                "operator": operator,
                                "mass_law": mass_law,
                                "block_model": args.block_model,
                                "max_gap": max_gap,
                                "error": str(exc),
                            }
                        )

    valid = [row for row in rows if "error" not in row]
    write_csv(args.output_csv, rows)
    summary_rows = group_summary(valid)
    write_csv(args.summary_csv, summary_rows)
    advantage_rows = advantage_summary(valid)
    write_csv(args.advantage_csv, advantage_rows)

    print(f"[spin-robust] wrote {args.output_csv}")
    print(f"[spin-robust] wrote {args.summary_csv}")
    print(f"[spin-robust] wrote {args.advantage_csv}")
    for row in summary_rows:
        print(
            f"  bw={float(row['bandwidth']):g} {row['operator']} {row['mass_law']}: "
            f"accel mean={row['accel_mean']:.3f}, min={row['accel_min']:.3f}, "
            f"gt1={row['accel_gt1_fraction']:.2f}"
        )
    if advantage_rows:
        for mass_law in sorted({row["mass_law"] for row in advantage_rows}):
            subset = [row for row in advantage_rows if row["mass_law"] == mass_law]
            advantage = np.asarray([float(row["accel_advantage"]) for row in subset])
            print(
                f"  local-vs-scrambled {mass_law}: "
                f"mean advantage={np.mean(advantage):.3f}, "
                f"positive fraction={np.mean(advantage > 0.0):.2f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
