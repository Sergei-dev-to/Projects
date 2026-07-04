"""Hard/soft erosion-channel diagnostic for the gauge droplet.

This compares two Stinespring maps for one-shell erosion:

Level 1 archive:
    |a> -> sum_h sqrt(p_h) |h> |a,h>
    hard radiation is exactly thermal, but soft capacity is enlarged.

Level 2 minimal soft:
    |psi> -> sum_h sqrt(p_h) |h> U_h |psi>
    soft capacity equals shell capacity; hard thermality is approximate.

The simulation uses the plaquette-flux factorization of an L x L Z_q gauge
patch and starts with a Haar-random pure state over H_L0.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


def haar_state(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    return z / np.linalg.norm(z)


def haar_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = phases / np.maximum(np.abs(phases), 1e-15)
    return q * phases.conj()


def entropy_subsystem(state: np.ndarray, dims: list[int], keep: list[int]) -> float:
    keep = list(keep)
    trace = [i for i in range(len(dims)) if i not in keep]
    perm = keep + trace
    psi = np.transpose(state.reshape(dims), perm).reshape(
        int(np.prod([dims[i] for i in keep], dtype=np.int64)),
        int(np.prod([dims[i] for i in trace], dtype=np.int64)),
    )
    singular = np.linalg.svd(psi, compute_uv=False)
    probs = singular**2
    probs = probs[probs > 1e-14]
    return float(-np.sum(probs * np.log(probs)))


def reduced_density(state: np.ndarray, dims: list[int], keep: list[int]) -> np.ndarray:
    keep = list(keep)
    trace = [i for i in range(len(dims)) if i not in keep]
    perm = keep + trace
    d_keep = int(np.prod([dims[i] for i in keep], dtype=np.int64))
    d_trace = int(np.prod([dims[i] for i in trace], dtype=np.int64))
    psi = np.transpose(state.reshape(dims), perm).reshape(d_keep, d_trace)
    return psi @ psi.conj().T


def trace_distance_to_diag(rho: np.ndarray, probs: np.ndarray) -> float:
    target = np.diag(probs)
    evals = np.linalg.eigvalsh(rho - target)
    return float(0.5 * np.sum(np.abs(evals)))


def apply_level1_archive(
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
) -> tuple[np.ndarray, list[int], int, int]:
    """Replace shell axis D by hard axis d_h and archive soft axis D*d_h."""
    d_shell = dims[shell_axis]
    d_hard = len(probs)
    tensor = state.reshape(dims)
    tensor = np.moveaxis(tensor, shell_axis, -1)
    rest_shape = tensor.shape[:-1]
    out = np.zeros(rest_shape + (d_hard, d_shell * d_hard), dtype=complex)
    for h, p in enumerate(probs):
        soft_offset = h * d_shell
        out[..., h, soft_offset : soft_offset + d_shell] = math.sqrt(float(p)) * tensor
    new_dims = dims[:shell_axis] + dims[shell_axis + 1 :] + [d_hard, d_shell * d_hard]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def apply_level2_minimal_soft(
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
    rng: np.random.Generator,
) -> tuple[np.ndarray, list[int], int, int]:
    """Replace shell axis D by hard axis d_h and minimal soft axis D."""
    d_shell = dims[shell_axis]
    d_hard = len(probs)
    tensor = state.reshape(dims)
    tensor = np.moveaxis(tensor, shell_axis, -1)
    rest_shape = tensor.shape[:-1]
    flat = tensor.reshape(-1, d_shell)
    out = np.zeros((flat.shape[0], d_hard, d_shell), dtype=complex)
    for h, p in enumerate(probs):
        u = haar_unitary(d_shell, rng)
        out[:, h, :] = math.sqrt(float(p)) * (flat @ u.T)
    out = out.reshape(rest_shape + (d_hard, d_shell))
    new_dims = dims[:shell_axis] + dims[shell_axis + 1 :] + [d_hard, d_shell]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def mutual_information(state: np.ndarray, dims: list[int], axes_a: list[int], axes_b: list[int]) -> float:
    s_a = entropy_subsystem(state, dims, axes_a)
    s_b = entropy_subsystem(state, dims, axes_b)
    s_ab = entropy_subsystem(state, dims, axes_a + axes_b)
    return s_a + s_b - s_ab


def run_model(model: str, L0: int, q: int, d_hard: int, seed: int) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    shell_dims = {L: q ** (2 * L - 1) for L in range(2, L0 + 1)}
    dims = [q] + [shell_dims[L] for L in range(2, L0 + 1)]
    state = haar_state(int(np.prod(dims, dtype=np.int64)), rng)

    # Energies epsilon_h = h * T_L make p_h independent of L but keep the
    # hard quantum energy scale proportional to T_L.
    hard_energies_over_T = np.arange(d_hard)
    probs = np.exp(-hard_energies_over_T)
    probs = probs / probs.sum()
    thermal_entropy = float(-np.sum(probs * np.log(probs)))

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    rows: list[dict[str, float | int | str]] = []

    for L in range(L0, 1, -1):
        shell_axis = L - 1  # dims = [core1, shell2, ..., shellL, rad...]
        if model == "level1_archive":
            state, dims, hard_axis, soft_axis = apply_level1_archive(state, dims, shell_axis, probs)
        elif model == "level2_minimal":
            state, dims, hard_axis, soft_axis = apply_level2_minimal_soft(state, dims, shell_axis, probs, rng)
        else:
            raise ValueError(model)

        hard_axes = [axis - 1 if axis > shell_axis else axis for axis in hard_axes]
        soft_axes = [axis - 1 if axis > shell_axis else axis for axis in soft_axes]
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)
        core_axes = list(range(0, L - 1))
        rad_axes = hard_axes + soft_axes
        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        hard_trace_dist = trace_distance_to_diag(latest_hard_rho, probs)

        row: dict[str, float | int | str] = {
            "model": model,
            "after_erosion_L": L,
            "remaining_core_L": L - 1,
            "total_dim": int(np.prod(dims, dtype=np.int64)),
            "core_entropy": entropy_subsystem(state, dims, core_axes),
            "all_radiation_entropy": entropy_subsystem(state, dims, rad_axes),
            "hard_entropy": entropy_subsystem(state, dims, hard_axes),
            "soft_entropy": entropy_subsystem(state, dims, soft_axes),
            "latest_hard_entropy": entropy_subsystem(state, dims, [hard_axis]),
            "thermal_hard_entropy": thermal_entropy,
            "latest_hard_trace_distance": hard_trace_dist,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L0", type=int, default=3)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--d-hard", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260531)
    parser.add_argument("--out", type=Path, default=Path("sim/data/erosion_channel_diagnostic.csv"))
    args = parser.parse_args()

    rows = []
    for model in ["level1_archive", "level2_minimal"]:
        rows.extend(run_model(model, args.L0, args.q, args.d_hard, args.seed))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {args.out}")
    print(
        "model             L->  S_core  S_hard  S_soft  "
        "S_hard_latest  D_hard  I_hh    I_pair"
    )
    for row in rows:
        print(
            f"{row['model']:<17} "
            f"{row['after_erosion_L']:>2}->{row['remaining_core_L']:<2} "
            f"{row['core_entropy']:7.3f} "
            f"{row['hard_entropy']:7.3f} "
            f"{row['soft_entropy']:7.3f} "
            f"{row['latest_hard_entropy']:13.3f} "
            f"{row['latest_hard_trace_distance']:7.3g} "
            f"{row['I_first_hard_last_hard']:7.3f} "
            f"{row['I_first_pair_last_pair']:7.3f}"
        )


if __name__ == "__main__":
    main()
