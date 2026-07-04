"""Local scrambling before shell erosion.

This diagnostic tests whether local plaquette-flux mixing can repair the
initial-state dependence found in the structured erosion channel.

The droplet is represented as L0^2 q-dits ordered by square shells:

    shell L has 2L - 1 plaquettes.

Before each erosion step, a local nearest-neighbor random circuit is applied to
the remaining L x L plaquette grid. Then the outer shell is mapped to hard and
soft radiation using the same structured shift/clock maps as before.
"""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np

from erosion_channel_diagnostic import haar_state, haar_unitary, reduced_density, trace_distance_to_diag


def shell_order(L0: int) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    for L in range(1, L0 + 1):
        for i in range(L):
            for j in range(L):
                if max(i, j) == L - 1:
                    coords.append((i, j))
    return coords


def nearest_neighbor_pairs(L: int, coord_to_axis: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for i in range(L):
        for j in range(L):
            if i + 1 < L:
                pairs.append((coord_to_axis[(i, j)], coord_to_axis[(i + 1, j)]))
            if j + 1 < L:
                pairs.append((coord_to_axis[(i, j)], coord_to_axis[(i, j + 1)]))
    return pairs


def basis_state(dim: int, index: int = 0) -> np.ndarray:
    state = np.zeros(dim, dtype=complex)
    state[index] = 1.0
    return state


def uniform_state(dim: int) -> np.ndarray:
    return np.ones(dim, dtype=complex) / np.sqrt(dim)


def kron_all(parts: list[np.ndarray]) -> np.ndarray:
    out = parts[0]
    for part in parts[1:]:
        out = np.kron(out, part)
    return out


def make_initial_state(kind: str, n_qdits: int, q: int, rng: np.random.Generator) -> np.ndarray:
    total_dim = q**n_qdits
    if kind == "basis_all":
        return basis_state(total_dim)
    if kind == "uniform_all":
        return uniform_state(total_dim)
    if kind == "factor_haar":
        return kron_all([haar_state(q, rng) for _ in range(n_qdits)])
    if kind == "haar_full":
        return haar_state(total_dim, rng)
    raise ValueError(kind)


def entropy_subsystem(state: np.ndarray, dims: list[int], keep: list[int]) -> float:
    keep = list(keep)
    trace = [i for i in range(len(dims)) if i not in keep]
    d_keep = int(np.prod([dims[i] for i in keep], dtype=np.int64))
    d_trace = int(np.prod([dims[i] for i in trace], dtype=np.int64))
    if d_trace < d_keep:
        keep, trace = trace, keep
        d_keep, d_trace = d_trace, d_keep
    perm = keep + trace
    psi = np.transpose(state.reshape(dims), perm).reshape(d_keep, d_trace)
    rho = psi @ psi.conj().T
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-14]
    return float(-np.sum(vals * np.log(vals)))


def mutual_information(state: np.ndarray, dims: list[int], axes_a: list[int], axes_b: list[int]) -> float:
    return (
        entropy_subsystem(state, dims, axes_a)
        + entropy_subsystem(state, dims, axes_b)
        - entropy_subsystem(state, dims, axes_a + axes_b)
    )


def shell_metrics(state: np.ndarray, dims: list[int], shell_axes: list[int]) -> tuple[float, float]:
    rho = reduced_density(state, dims, shell_axes)
    entropy = entropy_subsystem(state, dims, shell_axes)
    purity = float(np.real(np.trace(rho @ rho)))
    return entropy, purity


def flux_conserving_gate(q: int, rng: np.random.Generator) -> np.ndarray:
    dim = q * q
    gate = np.zeros((dim, dim), dtype=complex)
    for charge in range(q):
        block_indices = [a * q + b for a in range(q) for b in range(q) if (a + b) % q == charge]
        block = haar_unitary(len(block_indices), rng)
        for row, full_row in enumerate(block_indices):
            for col, full_col in enumerate(block_indices):
                gate[full_row, full_col] = block[row, col]
    return gate


def random_two_site_gate(q: int, kind: str, rng: np.random.Generator) -> np.ndarray:
    if kind == "generic":
        return haar_unitary(q * q, rng)
    if kind == "flux_conserving":
        return flux_conserving_gate(q, rng)
    raise ValueError(kind)


def apply_two_site_gate(
    state: np.ndarray,
    dims: list[int],
    axis_a: int,
    axis_b: int,
    gate: np.ndarray,
) -> np.ndarray:
    if axis_a == axis_b:
        raise ValueError("gate axes must differ")
    axes = [axis_a, axis_b]
    rest = [i for i in range(len(dims)) if i not in axes]
    perm = rest + axes
    inv_perm = np.argsort(perm)
    d_pair = dims[axis_a] * dims[axis_b]
    tensor = np.transpose(state.reshape(dims), perm)
    flat = tensor.reshape(-1, d_pair)
    flat = flat @ gate.T
    tensor = flat.reshape([dims[i] for i in rest] + [dims[axis_a], dims[axis_b]])
    return np.transpose(tensor, inv_perm).reshape(-1)


def apply_local_scrambler(
    state: np.ndarray,
    dims: list[int],
    L: int,
    q: int,
    coord_to_axis: dict[tuple[int, int], int],
    depth: int,
    kind: str,
    rng: np.random.Generator,
) -> np.ndarray:
    pairs = nearest_neighbor_pairs(L, coord_to_axis)
    for _ in range(depth):
        rng.shuffle(pairs)
        for axis_a, axis_b in pairs:
            gate = random_two_site_gate(q, kind, rng)
            state = apply_two_site_gate(state, dims, axis_a, axis_b, gate)
    return state


def flatten_axes_to_end(
    state: np.ndarray,
    dims: list[int],
    axes: list[int],
) -> tuple[np.ndarray, list[int], int]:
    axes = sorted(axes)
    rest = [i for i in range(len(dims)) if i not in axes]
    perm = rest + axes
    shell_dim = int(np.prod([dims[i] for i in axes], dtype=np.int64))
    tensor = np.transpose(state.reshape(dims), perm)
    new_dims = [dims[i] for i in rest] + [shell_dim]
    return tensor.reshape(-1), new_dims, len(new_dims) - 1


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


def apply_shell_erosion(
    state: np.ndarray,
    dims: list[int],
    shell_axes: list[int],
    probs: np.ndarray,
    channel: str,
) -> tuple[np.ndarray, list[int], int, int]:
    state, dims, shell_axis = flatten_axes_to_end(state, dims, shell_axes)
    d_shell = dims[shell_axis]
    d_hard = len(probs)
    tensor = state.reshape(dims)
    flat = tensor.reshape(-1, d_shell)
    out = np.zeros((flat.shape[0], d_hard, d_shell), dtype=complex)

    if channel == "shift_minimal":
        for h, p in enumerate(probs):
            out[:, h, :] = math.sqrt(float(p)) * np.roll(flat, shift=h, axis=1)
    elif channel == "clock_minimal":
        labels = np.arange(d_shell)
        for h, p in enumerate(probs):
            phases = np.exp(2j * np.pi * h * labels / d_shell)
            out[:, h, :] = math.sqrt(float(p)) * flat * phases
    elif channel == "flux_partition":
        hard_for_label = partition_labels(d_shell, probs)
        for a, h in enumerate(hard_for_label):
            out[:, h, a] = flat[:, a]
    else:
        raise ValueError(channel)

    new_dims = dims[:shell_axis] + [d_hard, d_shell]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def run_model(
    L0: int,
    q: int,
    d_hard: int,
    initial: str,
    scrambler: str,
    channel: str,
    depth: int,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    coords = shell_order(L0)
    coord_to_initial_axis = {coord: axis for axis, coord in enumerate(coords)}
    dims = [q] * (L0 * L0)
    state = make_initial_state(initial, L0 * L0, q, rng)

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
            state = apply_local_scrambler(state, dims, L, q, coord_to_axis, depth, scrambler, rng)

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
            "scrambler": scrambler,
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
    parser.add_argument("--out", type=Path, default=Path("sim/data/local_scrambling_before_erosion.csv"))
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/local_scrambling_before_erosion_summary.csv"),
    )
    parser.add_argument("--include-L4", action="store_true")
    args = parser.parse_args()

    configs = [(3, 2), (3, 3)]
    if args.include_L4:
        configs.append((4, 2))
    initials = ["basis_all", "uniform_all", "factor_haar"]
    scramblers = ["generic", "flux_conserving"]
    channels = ["shift_minimal", "clock_minimal"]
    depths = [0, 1, 2, 4, 8]

    rows: list[dict[str, float | int | str]] = []
    for L0, d_hard in configs:
        for initial in initials:
            for scrambler in scramblers:
                for channel in channels:
                    for depth in depths:
                        for offset in range(args.seeds):
                            seed = args.seed0 + offset
                            run_rows = run_model(
                                L0,
                                args.q,
                                d_hard,
                                initial,
                                scrambler,
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
                                    "scrambler": scrambler,
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

    grouped: dict[tuple[int, int, str, str, str, int], list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                int(row["L0"]),
                int(row["d_hard"]),
                str(row["initial"]),
                str(row["scrambler"]),
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
    for (L0, d_hard, initial, scrambler, channel, depth), group in sorted(grouped.items()):
        summary: dict[str, float | int | str] = {
            "L0": L0,
            "d_hard": d_hard,
            "initial": initial,
            "scrambler": scrambler,
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
    print("L0 d init        scrambler       chan   D  S_shell pur_shell maxD   I_pair S_h/therm")
    for row in summary_rows:
        if int(row["depth"]) not in (0, 1, 4, 8):
            continue
        print(
            f"{row['L0']:>2} {row['d_hard']:>1} "
            f"{row['initial']:<11} {row['scrambler']:<15} "
            f"{str(row['channel']).replace('_minimal', ''):<6} "
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
