"""Fixed local Floquet scrambling before shell erosion.

This is the next naturalness test after local_scrambling_before_erosion.py.
The earlier diagnostic redrew local random gates at every layer. Here the gate
set is generated once and then reused for every layer, so the pre-erosion
scrambler is one fixed local Floquet circuit.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np

from erosion_channel_diagnostic import haar_unitary, reduced_density, trace_distance_to_diag
from local_scrambling_before_erosion import (
    apply_shell_erosion,
    apply_two_site_gate,
    entropy_subsystem,
    flux_conserving_gate,
    make_initial_state,
    mutual_information,
    nearest_neighbor_pairs,
    shell_metrics,
    shell_order,
)


def fixed_gate(q: int, gate_kind: str, rng: np.random.Generator) -> np.ndarray:
    if gate_kind == "generic":
        return haar_unitary(q * q, rng)
    if gate_kind == "flux_conserving":
        return flux_conserving_gate(q, rng)
    raise ValueError(gate_kind)


def build_gate_bank(
    L0: int,
    q: int,
    floquet_kind: str,
    gate_kind: str,
    rng: np.random.Generator,
) -> dict[tuple[int, int], np.ndarray]:
    coords = shell_order(L0)
    coord_to_axis = {coord: axis for axis, coord in enumerate(coords)}
    pairs = nearest_neighbor_pairs(L0, coord_to_axis)
    if floquet_kind == "edge_fixed":
        return {tuple(sorted(pair)): fixed_gate(q, gate_kind, rng) for pair in pairs}
    if floquet_kind == "uniform_fixed":
        gate = fixed_gate(q, gate_kind, rng)
        return {tuple(sorted(pair)): gate for pair in pairs}
    raise ValueError(floquet_kind)


def apply_fixed_floquet(
    state: np.ndarray,
    dims: list[int],
    L: int,
    coord_to_axis: dict[tuple[int, int], int],
    gate_bank: dict[tuple[int, int], np.ndarray],
    depth: int,
) -> np.ndarray:
    pairs = nearest_neighbor_pairs(L, coord_to_axis)
    for _ in range(depth):
        for axis_a, axis_b in pairs:
            gate = gate_bank[tuple(sorted((axis_a, axis_b)))]
            state = apply_two_site_gate(state, dims, axis_a, axis_b, gate)
    return state


def run_model(
    L0: int,
    q: int,
    d_hard: int,
    initial: str,
    floquet_kind: str,
    gate_kind: str,
    channel: str,
    depth: int,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    coords = shell_order(L0)
    coord_to_initial_axis = {coord: axis for axis, coord in enumerate(coords)}
    dims = [q] * (L0 * L0)
    state = make_initial_state(initial, L0 * L0, q, rng)
    gate_bank = build_gate_bank(L0, q, floquet_kind, gate_kind, rng)

    probs = np.exp(-np.arange(d_hard))
    probs = probs / probs.sum()
    thermal_entropy = float(-np.sum(probs * np.log(probs)))

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    rows: list[dict[str, float | int | str]] = []

    for L in range(L0, 1, -1):
        coord_to_axis = {
            coord: axis
            for coord, axis in coord_to_initial_axis.items()
            if coord[0] < L and coord[1] < L and axis < L * L
        }
        if depth > 0:
            state = apply_fixed_floquet(state, dims, L, coord_to_axis, gate_bank, depth)

        shell_axes = list(range((L - 1) * (L - 1), L * L))
        before_shell_entropy, before_shell_purity = shell_metrics(state, dims, shell_axes)
        state, dims, hard_axis, soft_axis = apply_shell_erosion(state, dims, shell_axes, probs, channel)

        n_removed = len(shell_axes)
        hard_axes = [axis - n_removed if axis > shell_axes[-1] else axis for axis in hard_axes]
        soft_axes = [axis - n_removed if axis > shell_axes[-1] else axis for axis in soft_axes]
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        row: dict[str, float | int | str] = {
            "L0": L0,
            "q": q,
            "d_hard": d_hard,
            "initial": initial,
            "floquet_kind": floquet_kind,
            "gate_kind": gate_kind,
            "channel": channel,
            "depth": depth,
            "seed": seed,
            "after_erosion_L": L,
            "remaining_core_L": L - 1,
            "before_shell_entropy": before_shell_entropy,
            "before_shell_purity": before_shell_purity,
            "latest_hard_entropy": entropy_subsystem(state, dims, [hard_axis]),
            "thermal_hard_entropy": thermal_entropy,
            "latest_hard_trace_distance": trace_distance_to_diag(latest_hard_rho, probs),
        }
        if len(hard_axes) >= 2:
            row["I_first_hard_last_hard"] = mutual_information(state, dims, [hard_axes[0]], [hard_axes[-1]])
            row["I_first_pair_last_pair"] = mutual_information(
                state, dims, [hard_axes[0], soft_axes[0]], [hard_axes[-1], soft_axes[-1]]
            )
        else:
            row["I_first_hard_last_hard"] = 0.0
            row["I_first_pair_last_pair"] = 0.0
        rows.append(row)
    return rows


def summarize(values: list[float]) -> tuple[float, float]:
    return mean(values), pstdev(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--seeds", type=int, default=4)
    parser.add_argument("--seed0", type=int, default=20260601)
    parser.add_argument("--include-L4", action="store_true")
    parser.add_argument("--out", type=Path, default=Path("sim/data/fixed_floquet_before_erosion.csv"))
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/fixed_floquet_before_erosion_summary.csv"),
    )
    args = parser.parse_args()

    configs = [(3, 2), (3, 3)]
    if args.include_L4:
        configs.append((4, 2))
    initials = ["basis_all", "uniform_all", "factor_haar"]
    floquet_kinds = ["edge_fixed", "uniform_fixed"]
    gate_kinds = ["generic", "flux_conserving"]
    channels = ["shift_minimal", "clock_minimal"]
    depths = [0, 1, 2, 4, 8, 16]

    rows: list[dict[str, float | int | str]] = []
    for L0, d_hard in configs:
        for initial in initials:
            for floquet_kind in floquet_kinds:
                for gate_kind in gate_kinds:
                    for channel in channels:
                        for depth in depths:
                            for offset in range(args.seeds):
                                seed = args.seed0 + offset
                                run_rows = run_model(
                                    L0,
                                    args.q,
                                    d_hard,
                                    initial,
                                    floquet_kind,
                                    gate_kind,
                                    channel,
                                    depth,
                                    seed,
                                )
                                final = run_rows[-1]
                                rows.append(
                                    {
                                        "L0": L0,
                                        "q": args.q,
                                        "d_hard": d_hard,
                                        "initial": initial,
                                        "floquet_kind": floquet_kind,
                                        "gate_kind": gate_kind,
                                        "channel": channel,
                                        "depth": depth,
                                        "seed": seed,
                                        "mean_before_shell_entropy": mean(
                                            float(r["before_shell_entropy"]) for r in run_rows
                                        ),
                                        "mean_before_shell_purity": mean(
                                            float(r["before_shell_purity"]) for r in run_rows
                                        ),
                                        "max_latest_hard_trace_distance": max(
                                            float(r["latest_hard_trace_distance"]) for r in run_rows
                                        ),
                                        "final_latest_hard_trace_distance": float(
                                            final["latest_hard_trace_distance"]
                                        ),
                                        "final_latest_hard_entropy": float(final["latest_hard_entropy"]),
                                        "thermal_hard_entropy": float(final["thermal_hard_entropy"]),
                                        "final_I_hard_hard": float(final["I_first_hard_last_hard"]),
                                        "final_I_pair_pair": float(final["I_first_pair_last_pair"]),
                                    }
                                )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    grouped: dict[tuple[int, int, str, str, str, str, int], list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                int(row["L0"]),
                int(row["d_hard"]),
                str(row["initial"]),
                str(row["floquet_kind"]),
                str(row["gate_kind"]),
                str(row["channel"]),
                int(row["depth"]),
            )
        ].append(row)

    metrics = [
        "mean_before_shell_entropy",
        "mean_before_shell_purity",
        "max_latest_hard_trace_distance",
        "final_I_hard_hard",
        "final_I_pair_pair",
        "final_latest_hard_entropy",
        "thermal_hard_entropy",
    ]
    summary_rows: list[dict[str, float | int | str]] = []
    for (L0, d_hard, initial, floquet_kind, gate_kind, channel, depth), group in sorted(grouped.items()):
        summary: dict[str, float | int | str] = {
            "L0": L0,
            "d_hard": d_hard,
            "initial": initial,
            "floquet_kind": floquet_kind,
            "gate_kind": gate_kind,
            "channel": channel,
            "depth": depth,
            "n": len(group),
        }
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            m, s = summarize(vals)
            summary[f"{metric}_mean"] = m
            summary[f"{metric}_std"] = s
        summary_rows.append(summary)

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print("L0 d init        floquet       gate            chan   D  S_shell pur_shell maxD   I_pair S_h/therm")
    for row in summary_rows:
        if int(row["depth"]) not in (0, 1, 4, 16):
            continue
        print(
            f"{row['L0']:>2} {row['d_hard']:>1} "
            f"{row['initial']:<11} {row['floquet_kind']:<13} "
            f"{row['gate_kind']:<15} {str(row['channel']).replace('_minimal', ''):<6} "
            f"{row['depth']:>2} "
            f"{row['mean_before_shell_entropy_mean']:7.3f} "
            f"{row['mean_before_shell_purity_mean']:9.3f} "
            f"{row['max_latest_hard_trace_distance_mean']:5.3f} "
            f"{row['final_I_pair_pair_mean']:7.3f} "
            f"{row['final_latest_hard_entropy_mean']:5.3f}/"
            f"{row['thermal_hard_entropy_mean']:.3f}"
        )


if __name__ == "__main__":
    main()
