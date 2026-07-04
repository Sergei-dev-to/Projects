"""Fixed local Hamiltonian scrambling before shell erosion.

This diagnostic replaces the fixed Floquet circuit with time evolution under a
single nearest-neighbor Hamiltonian on the plaquette-flux q-dits:

    U(t) = exp(-i H_mix t), H_mix = sum_<ij> h_ij.

The goal is to test whether a fixed local Hamiltonian can make the outer shell
locally mixed enough for the structured hard/soft erosion channel.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np
from scipy.linalg import expm

from erosion_channel_diagnostic import reduced_density, trace_distance_to_diag
from local_scrambling_before_erosion import (
    apply_shell_erosion,
    entropy_subsystem,
    make_initial_state,
    mutual_information,
    nearest_neighbor_pairs,
    shell_metrics,
    shell_order,
)


def hermitian_from_random(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    h = z + z.conj().T
    return h / np.linalg.norm(h)


def two_site_hamiltonian(q: int, kind: str, rng: np.random.Generator) -> np.ndarray:
    dim = q * q
    if kind == "generic":
        return hermitian_from_random(dim, rng)
    if kind == "flux_conserving":
        h = np.zeros((dim, dim), dtype=complex)
        for charge in range(q):
            indices = [a * q + b for a in range(q) for b in range(q) if (a + b) % q == charge]
            block = hermitian_from_random(len(indices), rng)
            for row, full_row in enumerate(indices):
                for col, full_col in enumerate(indices):
                    h[full_row, full_col] = block[row, col]
        return h
    raise ValueError(kind)


def build_term_bank(
    L0: int,
    q: int,
    layout: str,
    term_kind: str,
    rng: np.random.Generator,
) -> dict[tuple[int, int], np.ndarray]:
    coords = shell_order(L0)
    coord_to_axis = {coord: axis for axis, coord in enumerate(coords)}
    pairs = nearest_neighbor_pairs(L0, coord_to_axis)
    if layout == "edge_fixed":
        return {tuple(sorted(pair)): two_site_hamiltonian(q, term_kind, rng) for pair in pairs}
    if layout == "uniform_fixed":
        h = two_site_hamiltonian(q, term_kind, rng)
        return {tuple(sorted(pair)): h for pair in pairs}
    raise ValueError(layout)


def embed_two_site_hamiltonian(dims: list[int], axis_a: int, axis_b: int, h2: np.ndarray) -> np.ndarray:
    dim_total = int(np.prod(dims, dtype=np.int64))
    out = np.zeros((dim_total, dim_total), dtype=complex)
    q = dims[axis_a]
    if dims[axis_b] != q:
        raise ValueError("only equal local dimensions are supported")

    for left in range(dim_total):
        digits_left = np.unravel_index(left, dims)
        pair_left = digits_left[axis_a] * q + digits_left[axis_b]
        for pair_right in range(q * q):
            amp = h2[pair_right, pair_left]
            if abs(amp) < 1e-14:
                continue
            a_right, b_right = divmod(pair_right, q)
            digits_right = list(digits_left)
            digits_right[axis_a] = a_right
            digits_right[axis_b] = b_right
            right = np.ravel_multi_index(tuple(digits_right), dims)
            out[right, left] += amp
    return out


def build_full_hamiltonian(
    dims: list[int],
    L: int,
    coord_to_axis: dict[tuple[int, int], int],
    term_bank: dict[tuple[int, int], np.ndarray],
) -> np.ndarray:
    pairs = nearest_neighbor_pairs(L, coord_to_axis)
    dim_total = int(np.prod(dims, dtype=np.int64))
    h_total = np.zeros((dim_total, dim_total), dtype=complex)
    for axis_a, axis_b in pairs:
        h2 = term_bank[tuple(sorted((axis_a, axis_b)))]
        h_total += embed_two_site_hamiltonian(dims, axis_a, axis_b, h2)
    h_total = (h_total + h_total.conj().T) / 2
    return h_total


def apply_hamiltonian_evolution(
    state: np.ndarray,
    dims: list[int],
    L: int,
    coord_to_axis: dict[tuple[int, int], int],
    term_bank: dict[tuple[int, int], np.ndarray],
    time: float,
) -> np.ndarray:
    if time == 0:
        return state
    h_total = build_full_hamiltonian(dims, L, coord_to_axis, term_bank)
    u = expm(-1j * time * h_total)
    return u @ state


def run_model(
    L0: int,
    q: int,
    d_hard: int,
    initial: str,
    layout: str,
    term_kind: str,
    channel: str,
    time: float,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    coords = shell_order(L0)
    coord_to_initial_axis = {coord: axis for axis, coord in enumerate(coords)}
    dims = [q] * (L0 * L0)
    state = make_initial_state(initial, L0 * L0, q, rng)
    term_bank = build_term_bank(L0, q, layout, term_kind, rng)

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
        state = apply_hamiltonian_evolution(state, dims, L, coord_to_axis, term_bank, time)

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
            "layout": layout,
            "term_kind": term_kind,
            "channel": channel,
            "time": time,
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
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--out", type=Path, default=Path("sim/data/hamiltonian_scrambling_before_erosion.csv"))
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/hamiltonian_scrambling_before_erosion_summary.csv"),
    )
    args = parser.parse_args()

    configs = [(3, 2), (3, 3)]
    if args.smoke:
        configs = [(3, 2)]
    elif args.include_L4:
        configs.append((4, 2))
    if args.smoke:
        initials = ["basis_all", "uniform_all"]
        layouts = ["edge_fixed"]
        term_kinds = ["flux_conserving"]
        channels = ["shift_minimal", "clock_minimal"]
        times = [0.0, 4.0]
    elif args.quick:
        initials = ["basis_all", "uniform_all"]
        layouts = ["edge_fixed"]
        term_kinds = ["flux_conserving"]
        channels = ["shift_minimal", "clock_minimal"]
        times = [0.0, 1.0, 2.0, 4.0, 8.0]
    else:
        initials = ["basis_all", "uniform_all", "factor_haar"]
        layouts = ["edge_fixed", "uniform_fixed"]
        term_kinds = ["generic", "flux_conserving"]
        channels = ["shift_minimal", "clock_minimal"]
        times = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0]

    rows: list[dict[str, float | int | str]] = []
    for L0, d_hard in configs:
        for initial in initials:
            for layout in layouts:
                for term_kind in term_kinds:
                    for channel in channels:
                        for time in times:
                            for offset in range(args.seeds):
                                seed = args.seed0 + offset
                                run_rows = run_model(
                                    L0,
                                    args.q,
                                    d_hard,
                                    initial,
                                    layout,
                                    term_kind,
                                    channel,
                                    time,
                                    seed,
                                )
                                final = run_rows[-1]
                                rows.append(
                                    {
                                        "L0": L0,
                                        "q": args.q,
                                        "d_hard": d_hard,
                                        "initial": initial,
                                        "layout": layout,
                                        "term_kind": term_kind,
                                        "channel": channel,
                                        "time": time,
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

    grouped: dict[tuple[int, int, str, str, str, str, float], list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                int(row["L0"]),
                int(row["d_hard"]),
                str(row["initial"]),
                str(row["layout"]),
                str(row["term_kind"]),
                str(row["channel"]),
                float(row["time"]),
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
    for (L0, d_hard, initial, layout, term_kind, channel, time), group in sorted(grouped.items()):
        summary: dict[str, float | int | str] = {
            "L0": L0,
            "d_hard": d_hard,
            "initial": initial,
            "layout": layout,
            "term_kind": term_kind,
            "channel": channel,
            "time": time,
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
    print("L0 d init        layout        term            chan   t    S_shell pur_shell maxD   I_pair S_h/therm")
    for row in summary_rows:
        if float(row["time"]) not in (0.0, 1.0, 4.0, 8.0):
            continue
        print(
            f"{row['L0']:>2} {row['d_hard']:>1} "
            f"{row['initial']:<11} {row['layout']:<13} "
            f"{row['term_kind']:<15} {str(row['channel']).replace('_minimal', ''):<6} "
            f"{row['time']:>4.1f} "
            f"{row['mean_before_shell_entropy_mean']:7.3f} "
            f"{row['mean_before_shell_purity_mean']:9.3f} "
            f"{row['max_latest_hard_trace_distance_mean']:5.3f} "
            f"{row['final_I_pair_pair_mean']:7.3f} "
            f"{row['final_latest_hard_entropy_mean']:5.3f}/"
            f"{row['thermal_hard_entropy_mean']:.3f}"
        )


if __name__ == "__main__":
    main()
