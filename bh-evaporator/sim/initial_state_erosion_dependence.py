"""Initial-state dependence for structured erosion channels.

The structured erosion scan starts from a Haar-random state over the full
droplet. This diagnostic keeps the erosion maps fixed and changes only the
initial droplet state.

The point is to test whether thermal-looking hard radiation is a property of
the channel itself, or a property of typical/scrambled shell states.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

import numpy as np

from erosion_channel_diagnostic import (
    haar_state,
    reduced_density,
    trace_distance_to_diag,
)
from structured_erosion_channel import apply_model


def kron_all(parts: list[np.ndarray]) -> np.ndarray:
    out = parts[0]
    for part in parts[1:]:
        out = np.kron(out, part)
    return out


def basis_state(dim: int, index: int = 0) -> np.ndarray:
    state = np.zeros(dim, dtype=complex)
    state[index] = 1.0
    return state


def uniform_state(dim: int) -> np.ndarray:
    return np.ones(dim, dtype=complex) / np.sqrt(dim)


def entropy_subsystem_balanced(state: np.ndarray, dims: list[int], keep: list[int]) -> float:
    """Entropy of a pure-state subsystem, diagonalizing the smaller density matrix."""
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
    probs = np.linalg.eigvalsh(rho)
    probs = probs[probs > 1e-14]
    return float(-np.sum(probs * np.log(probs)))


def mutual_information_balanced(state: np.ndarray, dims: list[int], axes_a: list[int], axes_b: list[int]) -> float:
    s_a = entropy_subsystem_balanced(state, dims, axes_a)
    s_b = entropy_subsystem_balanced(state, dims, axes_b)
    s_ab = entropy_subsystem_balanced(state, dims, axes_a + axes_b)
    return s_a + s_b - s_ab


def outer_shell_maximally_mixed_state(dims: list[int], rng: np.random.Generator) -> np.ndarray:
    """Pure state whose outer shell is as mixed as the interior allows."""
    inner_dim = int(np.prod(dims[:-1], dtype=np.int64))
    shell_dim = dims[-1]
    schmidt_rank = min(inner_dim, shell_dim)
    z_inner = rng.normal(size=(inner_dim, schmidt_rank)) + 1j * rng.normal(size=(inner_dim, schmidt_rank))
    z_shell = rng.normal(size=(shell_dim, schmidt_rank)) + 1j * rng.normal(size=(shell_dim, schmidt_rank))
    q_inner, _ = np.linalg.qr(z_inner)
    q_shell, _ = np.linalg.qr(z_shell)
    coeffs = (q_inner[:, :schmidt_rank] @ q_shell[:, :schmidt_rank].T) / np.sqrt(schmidt_rank)
    return coeffs.reshape(-1)


def make_initial_state(kind: str, dims: list[int], rng: np.random.Generator) -> np.ndarray:
    total_dim = int(np.prod(dims, dtype=np.int64))
    if kind == "haar_full":
        return haar_state(total_dim, rng)
    if kind == "factor_haar":
        return kron_all([haar_state(dim, rng) for dim in dims])
    if kind == "basis_all":
        return basis_state(total_dim)
    if kind == "uniform_all":
        return kron_all([uniform_state(dim) for dim in dims])
    if kind == "outer_basis":
        inner = haar_state(int(np.prod(dims[:-1], dtype=np.int64)), rng)
        return np.kron(inner, basis_state(dims[-1]))
    if kind == "outer_uniform":
        inner = haar_state(int(np.prod(dims[:-1], dtype=np.int64)), rng)
        return np.kron(inner, uniform_state(dims[-1]))
    if kind == "outer_maxmix":
        return outer_shell_maximally_mixed_state(dims, rng)
    raise ValueError(kind)


def shell_reduced_metrics(state: np.ndarray, dims: list[int], shell_axis: int) -> tuple[float, float]:
    rho = reduced_density(state, dims, [shell_axis])
    entropy = entropy_subsystem_balanced(state, dims, [shell_axis])
    purity = float(np.real(np.trace(rho @ rho)))
    return entropy, purity


def run_model(
    model: str,
    initial: str,
    L0: int,
    q: int,
    d_hard: int,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    shell_dims = {L: q ** (2 * L - 1) for L in range(2, L0 + 1)}
    dims = [q] + [shell_dims[L] for L in range(2, L0 + 1)]
    state = make_initial_state(initial, dims, rng)

    initial_outer_entropy, initial_outer_purity = shell_reduced_metrics(state, dims, len(dims) - 1)

    energies_over_T = np.arange(d_hard)
    probs = np.exp(-energies_over_T)
    probs = probs / probs.sum()
    thermal_entropy = float(-np.sum(probs * np.log(probs)))

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    rows: list[dict[str, float | int | str]] = []
    for L in range(L0, 1, -1):
        shell_axis = L - 1
        before_shell_entropy, before_shell_purity = shell_reduced_metrics(state, dims, shell_axis)

        state, dims, hard_axis, soft_axis = apply_model(model, state, dims, shell_axis, probs, rng)
        hard_axes = [axis - 1 if axis > shell_axis else axis for axis in hard_axes]
        soft_axes = [axis - 1 if axis > shell_axis else axis for axis in soft_axes]
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        row: dict[str, float | int | str] = {
            "model": model,
            "initial": initial,
            "L0": L0,
            "q": q,
            "d_hard": d_hard,
            "seed": seed,
            "after_erosion_L": L,
            "remaining_core_L": L - 1,
            "initial_outer_shell_entropy": initial_outer_entropy,
            "initial_outer_shell_purity": initial_outer_purity,
            "before_shell_entropy": before_shell_entropy,
            "before_shell_purity": before_shell_purity,
            "latest_hard_entropy": entropy_subsystem_balanced(state, dims, [hard_axis]),
            "thermal_hard_entropy": thermal_entropy,
            "latest_hard_trace_distance": trace_distance_to_diag(latest_hard_rho, probs),
        }
        if len(hard_axes) >= 2:
            row["I_first_hard_last_hard"] = mutual_information_balanced(
                state, dims, [hard_axes[0]], [hard_axes[-1]]
            )
            row["I_first_pair_last_pair"] = mutual_information_balanced(
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
    parser.add_argument("--out", type=Path, default=Path("sim/data/initial_state_erosion_dependence.csv"))
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/initial_state_erosion_dependence_summary.csv"),
    )
    args = parser.parse_args()

    models = ["shift_minimal", "clock_minimal", "flux_partition"]
    initials = [
        "haar_full",
        "outer_maxmix",
        "factor_haar",
        "outer_basis",
        "outer_uniform",
        "basis_all",
        "uniform_all",
    ]
    configs = [(3, 2), (3, 3), (4, 2)]

    rows: list[dict[str, float | int | str]] = []
    for L0, d_hard in configs:
        for model in models:
            for initial in initials:
                for offset in range(args.seeds):
                    seed = args.seed0 + offset
                    run_rows = run_model(model, initial, L0, args.q, d_hard, seed)
                    final = run_rows[-1]
                    rows.append(
                        {
                            "model": model,
                            "initial": initial,
                            "L0": L0,
                            "q": args.q,
                            "d_hard": d_hard,
                            "seed": seed,
                            "initial_outer_shell_entropy": float(run_rows[0]["initial_outer_shell_entropy"]),
                            "initial_outer_shell_purity": float(run_rows[0]["initial_outer_shell_purity"]),
                            "mean_before_shell_entropy": mean(float(r["before_shell_entropy"]) for r in run_rows),
                            "mean_before_shell_purity": mean(float(r["before_shell_purity"]) for r in run_rows),
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

    grouped: dict[tuple[str, str, int, int], list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["model"]), str(row["initial"]), int(row["L0"]), int(row["d_hard"]))].append(row)

    summary_rows: list[dict[str, float | int | str]] = []
    metrics = [
        "initial_outer_shell_entropy",
        "initial_outer_shell_purity",
        "mean_before_shell_entropy",
        "mean_before_shell_purity",
        "max_latest_hard_trace_distance",
        "final_I_hard_hard",
        "final_I_pair_pair",
        "final_latest_hard_entropy",
        "thermal_hard_entropy",
    ]
    for (model, initial, L0, d_hard), group in sorted(grouped.items()):
        summary: dict[str, float | int | str] = {
            "model": model,
            "initial": initial,
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
    print("model          initial        L0 d_h  S_shell  pur_shell  maxD    I_hh    I_pair  S_h/therm")
    for row in summary_rows:
        print(
            f"{row['model']:<14} {row['initial']:<14} {row['L0']:>2} {row['d_hard']:>3} "
            f"{row['mean_before_shell_entropy_mean']:7.3f} "
            f"{row['mean_before_shell_purity_mean']:9.3f} "
            f"{row['max_latest_hard_trace_distance_mean']:6.3f} "
            f"{row['final_I_hard_hard_mean']:7.4f} "
            f"{row['final_I_pair_pair_mean']:7.3f} "
            f"{row['final_latest_hard_entropy_mean']:6.3f}/"
            f"{row['thermal_hard_entropy_mean']:.3f}"
        )


if __name__ == "__main__":
    main()
