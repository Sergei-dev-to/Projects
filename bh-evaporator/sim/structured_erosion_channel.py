"""Structured erosion-channel controls.

This compares the random Level 2 minimal-soft channel with simple structured
shell maps:

    random_minimal:
        U_h Haar random.

    shift_minimal:
        U_h is a cyclic shift of shell flux basis labels.

    clock_minimal:
        U_h is a diagonal clock phase on shell flux basis labels.

    flux_partition:
        the hard bin is a deterministic partition of shell flux labels, with
        bin sizes chosen to approximate the target thermal distribution.

All channels use minimal soft capacity:

    dim H_soft = dim H_shell.

The goal is not to claim these are fully local Hamiltonian dynamics. It is to
test whether structured shell-flux operations can reproduce the hard/soft
information split seen in the random channel.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np

from erosion_channel_diagnostic import (
    apply_level2_minimal_soft,
    entropy_subsystem,
    haar_state,
    mutual_information,
    reduced_density,
    trace_distance_to_diag,
)


def apply_shift_minimal(
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
) -> tuple[np.ndarray, list[int], int, int]:
    d_shell = dims[shell_axis]
    d_hard = len(probs)
    tensor = np.moveaxis(state.reshape(dims), shell_axis, -1)
    rest_shape = tensor.shape[:-1]
    flat = tensor.reshape(-1, d_shell)
    out = np.zeros((flat.shape[0], d_hard, d_shell), dtype=complex)
    for h, p in enumerate(probs):
        out[:, h, :] = math.sqrt(float(p)) * np.roll(flat, shift=h, axis=1)
    out = out.reshape(rest_shape + (d_hard, d_shell))
    new_dims = dims[:shell_axis] + dims[shell_axis + 1 :] + [d_hard, d_shell]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def apply_clock_minimal(
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
) -> tuple[np.ndarray, list[int], int, int]:
    d_shell = dims[shell_axis]
    d_hard = len(probs)
    labels = np.arange(d_shell)
    tensor = np.moveaxis(state.reshape(dims), shell_axis, -1)
    rest_shape = tensor.shape[:-1]
    flat = tensor.reshape(-1, d_shell)
    out = np.zeros((flat.shape[0], d_hard, d_shell), dtype=complex)
    for h, p in enumerate(probs):
        phases = np.exp(2j * np.pi * h * labels / d_shell)
        out[:, h, :] = math.sqrt(float(p)) * flat * phases
    out = out.reshape(rest_shape + (d_hard, d_shell))
    new_dims = dims[:shell_axis] + dims[shell_axis + 1 :] + [d_hard, d_shell]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def partition_labels(d_shell: int, probs: np.ndarray) -> np.ndarray:
    raw = probs * d_shell
    counts = np.floor(raw).astype(int)
    remainder = d_shell - int(counts.sum())
    if remainder > 0:
        order = np.argsort(-(raw - counts))
        for idx in order[:remainder]:
            counts[idx] += 1
    labels = np.empty(d_shell, dtype=int)
    start = 0
    for h, count in enumerate(counts):
        labels[start : start + count] = h
        start += count
    return labels


def apply_flux_partition(
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
) -> tuple[np.ndarray, list[int], int, int]:
    """Map |a>_shell -> |h=f(a)>_hard |a>_soft."""
    d_shell = dims[shell_axis]
    d_hard = len(probs)
    hard_for_label = partition_labels(d_shell, probs)
    tensor = np.moveaxis(state.reshape(dims), shell_axis, -1)
    rest_shape = tensor.shape[:-1]
    flat = tensor.reshape(-1, d_shell)
    out = np.zeros((flat.shape[0], d_hard, d_shell), dtype=complex)
    for a, h in enumerate(hard_for_label):
        out[:, h, a] = flat[:, a]
    out = out.reshape(rest_shape + (d_hard, d_shell))
    new_dims = dims[:shell_axis] + dims[shell_axis + 1 :] + [d_hard, d_shell]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def apply_model(
    model: str,
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[int], int, int]:
    if model == "random_minimal":
        return apply_level2_minimal_soft(state, dims, shell_axis, probs, rng)
    if model == "shift_minimal":
        return apply_shift_minimal(state, dims, shell_axis, probs)
    if model == "clock_minimal":
        return apply_clock_minimal(state, dims, shell_axis, probs)
    if model == "flux_partition":
        return apply_flux_partition(state, dims, shell_axis, probs)
    raise ValueError(model)


def run_model(model: str, L0: int, q: int, d_hard: int, seed: int) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    shell_dims = {L: q ** (2 * L - 1) for L in range(2, L0 + 1)}
    dims = [q] + [shell_dims[L] for L in range(2, L0 + 1)]
    state = haar_state(int(np.prod(dims, dtype=np.int64)), rng)

    energies_over_T = np.arange(d_hard)
    probs = np.exp(-energies_over_T)
    probs = probs / probs.sum()
    thermal_entropy = float(-np.sum(probs * np.log(probs)))

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    rows: list[dict[str, float | int | str]] = []
    for L in range(L0, 1, -1):
        shell_axis = L - 1
        state, dims, hard_axis, soft_axis = apply_model(model, state, dims, shell_axis, probs, rng)
        hard_axes = [axis - 1 if axis > shell_axis else axis for axis in hard_axes]
        soft_axes = [axis - 1 if axis > shell_axis else axis for axis in soft_axes]
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

        core_axes = list(range(0, L - 1))
        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        row: dict[str, float | int | str] = {
            "model": model,
            "L0": L0,
            "q": q,
            "d_hard": d_hard,
            "seed": seed,
            "after_erosion_L": L,
            "remaining_core_L": L - 1,
            "core_entropy": entropy_subsystem(state, dims, core_axes),
            "hard_entropy": entropy_subsystem(state, dims, hard_axes),
            "soft_entropy": entropy_subsystem(state, dims, soft_axes),
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
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--seed0", type=int, default=20260601)
    parser.add_argument("--out", type=Path, default=Path("sim/data/structured_erosion_channel.csv"))
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/structured_erosion_channel_summary.csv"),
    )
    args = parser.parse_args()

    models = ["random_minimal", "shift_minimal", "clock_minimal", "flux_partition"]
    configs = [(3, 2), (3, 3), (4, 2)]
    rows: list[dict[str, float | int | str]] = []
    for L0, d_hard in configs:
        for model in models:
            for offset in range(args.seeds):
                seed = args.seed0 + offset
                run_rows = run_model(model, L0, args.q, d_hard, seed)
                final = run_rows[-1]
                rows.append(
                    {
                        "model": model,
                        "L0": L0,
                        "q": args.q,
                        "d_hard": d_hard,
                        "seed": seed,
                        "max_latest_hard_trace_distance": max(
                            float(r["latest_hard_trace_distance"]) for r in run_rows
                        ),
                        "final_latest_hard_trace_distance": float(final["latest_hard_trace_distance"]),
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

    grouped: dict[tuple[str, int, int], list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["model"]), int(row["L0"]), int(row["d_hard"]))].append(row)

    summary_rows: list[dict[str, float | int | str]] = []
    metrics = [
        "max_latest_hard_trace_distance",
        "final_I_hard_hard",
        "final_I_pair_pair",
        "final_latest_hard_entropy",
        "thermal_hard_entropy",
    ]
    for (model, L0, d_hard), group in sorted(grouped.items()):
        summary: dict[str, float | int | str] = {
            "model": model,
            "L0": L0,
            "d_hard": d_hard,
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
    print("model            L0 d_h maxD    I_hh    I_pair  S_latest/thermal")
    for row in summary_rows:
        print(
            f"{row['model']:<16} {row['L0']:>2} {row['d_hard']:>3} "
            f"{row['max_latest_hard_trace_distance_mean']:6.3f} "
            f"{row['final_I_hard_hard_mean']:7.4f} "
            f"{row['final_I_pair_pair_mean']:7.3f} "
            f"{row['final_latest_hard_entropy_mean']:7.3f}/"
            f"{row['thermal_hard_entropy_mean']:.3f}"
        )


if __name__ == "__main__":
    main()
