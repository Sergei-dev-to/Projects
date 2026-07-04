"""Autonomous repeated-interaction cycle diagnostic.

This script combines the previous modules into a fixed repeated step:

    mix bulk -> emit edge quantum -> accumulate emitted energy
    -> if threshold reached, apply finite-gauge shell update.

The exact state-vector part is feasible only for the smallest q=2, L=2
finite-gauge cycle.  The same script also writes a large-L schedule diagnostic
showing how many microscopic emissions are needed to reach one shell gap.

This is still not a single time-independent Hamiltonian.  It is a fixed
repeated-interaction process with a threshold rule, which is the next level
above hand-scheduling separate diagnostics.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

from energy_conserving_emission_block import (
    edge_preparation_unitary,
    emission_hamiltonian,
    unitary_from_hamiltonian,
)
from microscopic_boundary_emission import (
    apply_unitary_to_axes,
    entropy_of_axes,
    golden_rule_hard_distribution,
    haar_unitary,
    make_local_gates,
    maximally_entangled_state,
    mutual_information,
    reduced_density,
    trace_distance_to_target,
)


def append_emission_ancillas(state: np.ndarray, dims: list[int]) -> tuple[np.ndarray, list[int]]:
    out = np.zeros(list(state.shape) + [2, 2, 2, 4], dtype=np.complex128)
    out[(..., 0, 0, 0, 0)] = state
    return out, dims + [2, 2, 2, 4]


def append_record_from_axis(
    state: np.ndarray,
    dims: list[int],
    source_axis: int,
) -> tuple[np.ndarray, list[int], int]:
    rest_axes = [i for i in range(len(dims)) if i != source_axis]
    transposed = np.transpose(state, [source_axis] + rest_axes)
    rest_shape = [dims[i] for i in rest_axes]
    rest_dim = int(np.prod(rest_shape))
    matrix = transposed.reshape(2, rest_dim)
    out = np.zeros((2, rest_dim, 2), dtype=np.complex128)
    for i in range(2):
        out[0, :, i] = matrix[i, :]
    out = out.reshape([2] + rest_shape + [2])
    current_labels: list[int | str] = [source_axis] + rest_axes + ["record"]
    desired_labels: list[int | str] = list(range(len(dims))) + ["record"]
    perm = [current_labels.index(label) for label in desired_labels]
    return np.transpose(out, perm), dims + [2], len(dims)


def large_L_schedule(
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    max_L: int,
    max_steps: int,
) -> list[dict[str, float | int]]:
    rows = []
    for L in range(2, max_L + 1):
        mass = 4.0 * sigma * L
        delta_m = 4.0 * sigma
        emitted = 0.0
        steps = 0
        first_mean = None
        first_temp = None
        while emitted < delta_m and steps < max_steps:
            _probs, mean_omega, temp = golden_rule_hard_distribution(
                mass, q, sigma, bath_dim, x_edges, n_grid
            )
            if first_mean is None:
                first_mean = mean_omega
                first_temp = temp
            emitted += mean_omega
            mass = max(1e-12, mass - mean_omega)
            steps += 1
        rows.append(
            {
                "L": L,
                "q": q,
                "bath_dim": bath_dim,
                "delta_M": delta_m,
                "first_mean_omega": float(first_mean or 0.0),
                "first_temperature": float(first_temp or 0.0),
                "first_omega_over_T": float((first_mean or 0.0) / (first_temp or 1.0)),
                "steps_to_threshold": steps,
                "emitted_over_delta_M": emitted / delta_m,
            }
        )
    return rows


def run_exact_L2_cycle(
    variant: str,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    local_depth: int,
    theta: float,
    max_steps: int,
    seed: int,
) -> dict[str, float | int | str]:
    L = 2
    if q != 2:
        raise ValueError("exact state cycle currently supports q=2 only")

    n_bulk = L * L
    n_core = (L - 1) * (L - 1)
    shell_axes_offset = n_core
    rng = np.random.default_rng(seed)
    state, dims = maximally_entangled_state(n_bulk)
    ref_axes = list(range(n_bulk))
    bulk_axes = list(range(n_bulk, 2 * n_bulk))
    core_axes = bulk_axes[:n_core]
    shell_axes = bulk_axes[shell_axes_offset:]
    port_axis = shell_axes[-1]
    fixed_local_gates = make_local_gates(n_bulk, local_depth, rng)

    mass = 4.0 * sigma * L
    delta_m = 4.0 * sigma
    emitted = 0.0
    shrunk = False
    steps = 0

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    flag_axes: list[int] = []
    shell_record_axes: list[int] = []
    latest_probs = np.array([1.0, 0.0])

    while not shrunk and steps < max_steps:
        if variant == "none":
            pass
        elif variant == "local":
            for i, j, gate in fixed_local_gates:
                state = apply_unitary_to_axes(state, dims, [bulk_axes[i], bulk_axes[j]], gate)
        elif variant == "scrambled":
            state = apply_unitary_to_axes(state, dims, bulk_axes, haar_unitary(2**n_bulk, rng))
        else:
            raise ValueError(f"unknown variant {variant!r}")

        probs, mean_omega, _temp = golden_rule_hard_distribution(
            mass, q, sigma, bath_dim, x_edges, n_grid
        )
        latest_probs = probs

        state, dims = append_emission_ancillas(state, dims)
        edge_axis = len(dims) - 4
        flag_axis = len(dims) - 3
        hard_axis = len(dims) - 2
        soft_axis = len(dims) - 1
        state = apply_unitary_to_axes(state, dims, [edge_axis], edge_preparation_unitary(probs))
        state = apply_unitary_to_axes(
            state,
            dims,
            [port_axis, edge_axis, flag_axis, hard_axis, soft_axis],
            unitary_from_hamiltonian(emission_hamiltonian(probs), theta),
        )

        flag_axes.append(flag_axis)
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

        emitted += mean_omega
        mass = max(1e-12, mass - mean_omega)
        steps += 1

        if emitted >= delta_m:
            for axis in shell_axes:
                state, dims, record_axis = append_record_from_axis(state, dims, axis)
                shell_record_axes.append(record_axis)
            shrunk = True

    micro_record_axes = flag_axes + hard_axes + soft_axes
    all_record_axes = micro_record_axes + shell_record_axes
    rho_latest_hard = reduced_density(state, dims, [hard_axes[-1]])

    return {
        "variant": variant,
        "seed": seed,
        "L": L,
        "q": q,
        "n_bulk": n_bulk,
        "n_core": n_core,
        "n_shell": 2 * L - 1,
        "steps": steps,
        "shrunk": int(shrunk),
        "emitted_over_delta_M": emitted / delta_m,
        "D_latest_hard_to_target": trace_distance_to_target(rho_latest_hard, latest_probs),
        "I_ref_hard_all": mutual_information(state, dims, ref_axes, hard_axes),
        "I_ref_micro_records": mutual_information(state, dims, ref_axes, micro_record_axes),
        "I_ref_shell_record": mutual_information(state, dims, ref_axes, shell_record_axes),
        "I_ref_all_records": mutual_information(state, dims, ref_axes, all_record_axes),
        "I_ref_core_after": mutual_information(state, dims, ref_axes, core_axes),
        "S_all_records": entropy_of_axes(state, dims, all_record_axes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--x-edges", nargs="+", type=float, default=[0.0, 2.0, 8.0])
    parser.add_argument("--n-grid", type=int, default=1001)
    parser.add_argument("--max-L-schedule", type=int, default=40)
    parser.add_argument("--max-steps", type=int, default=200)
    parser.add_argument("--local-depth", type=int, default=1)
    parser.add_argument("--theta", type=float, default=math.pi / 2.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--variants",
        nargs="+",
        default=["none", "local", "scrambled"],
        choices=["none", "local", "scrambled"],
    )
    parser.add_argument(
        "--cycle-out",
        type=Path,
        default=Path("sim/data/autonomous_repeated_cycle_exact_L2.csv"),
    )
    parser.add_argument(
        "--schedule-out",
        type=Path,
        default=Path("sim/data/autonomous_repeated_cycle_schedule.csv"),
    )
    args = parser.parse_args()

    x_edges = np.array(args.x_edges, dtype=float)
    schedule = large_L_schedule(
        args.q,
        args.sigma,
        args.bath_dim,
        x_edges,
        args.n_grid,
        args.max_L_schedule,
        args.max_steps,
    )
    exact_rows = [
        run_exact_L2_cycle(
            variant,
            args.q,
            args.sigma,
            args.bath_dim,
            x_edges,
            args.n_grid,
            args.local_depth,
            args.theta,
            args.max_steps,
            args.seed,
        )
        for variant in args.variants
    ]

    args.schedule_out.parent.mkdir(parents=True, exist_ok=True)
    with args.schedule_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(schedule[0].keys()))
        writer.writeheader()
        writer.writerows(schedule)
    with args.cycle_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(exact_rows[0].keys()))
        writer.writeheader()
        writer.writerows(exact_rows)

    print(f"wrote {args.schedule_out}")
    print(f"wrote {args.cycle_out}")
    print("schedule controls:")
    for row in [schedule[0], schedule[3], schedule[-1]]:
        print(
            f"L={row['L']:2d} steps={row['steps_to_threshold']:3d} "
            f"first_omega/T={row['first_omega_over_T']:.3f} "
            f"emitted/DeltaM={row['emitted_over_delta_M']:.3f}"
        )
    print()
    print("exact L=2 repeated cycle:")
    print("variant    steps  shrunk  D_hard  I(R:hard)  I(R:micro)  I(R:shell)  I(R:allrec)  I(R:core)")
    for row in exact_rows:
        print(
            f"{str(row['variant']):10s} "
            f"{int(row['steps']):5d} "
            f"{int(row['shrunk']):6d} "
            f"{float(row['D_latest_hard_to_target']):7.4f} "
            f"{float(row['I_ref_hard_all']):10.4f} "
            f"{float(row['I_ref_micro_records']):10.4f} "
            f"{float(row['I_ref_shell_record']):10.4f} "
            f"{float(row['I_ref_all_records']):11.4f} "
            f"{float(row['I_ref_core_after']):10.4f}"
        )


if __name__ == "__main__":
    main()
