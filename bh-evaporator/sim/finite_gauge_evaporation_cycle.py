"""Finite-gauge evaporation cycle diagnostic.

This is the first small "whole-cycle" model:

1. start in the exact finite-gauge factorization

       H_L ~= H_(L-1) tensor H_shell,
       dim H_shell = q^(2L - 1)

   implemented for q=2 as qubits;

2. run microscopic energy-aware boundary emissions with golden-rule weights;

3. accumulate emitted energy until it reaches the shell gap Delta M = 4 sigma;

4. apply the exact shell update by moving the shell qubits into a shrink record;

5. measure where the reference information is.

This is still a scheduled repeated-interaction cycle, not an autonomous
Hamiltonian.  Its purpose is to test compatibility of the components in one
cycle.
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
    """Move a qubit into a new record qubit and reset the source to |0>."""
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


def hard_weights_for_cycle(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    n_events: int,
) -> tuple[list[np.ndarray], list[float], list[float], float]:
    mass = 4.0 * sigma * L
    delta_m = 4.0 * sigma
    probs_by_event: list[np.ndarray] = []
    mean_omegas: list[float] = []
    temps: list[float] = []
    for _ in range(n_events):
        probs, mean_omega, temp = golden_rule_hard_distribution(
            mass,
            q,
            sigma,
            bath_dim,
            x_edges,
            n_grid,
        )
        probs_by_event.append(probs)
        mean_omegas.append(mean_omega)
        temps.append(temp)
        mass = max(1e-12, mass - mean_omega)
    return probs_by_event, mean_omegas, temps, delta_m


def auto_event_count(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    max_events: int,
) -> int:
    mass = 4.0 * sigma * L
    delta_m = 4.0 * sigma
    total = 0.0
    count = 0
    while total < delta_m and count < max_events:
        _probs, mean_omega, _temp = golden_rule_hard_distribution(
            mass, q, sigma, bath_dim, x_edges, n_grid
        )
        total += mean_omega
        mass = max(1e-12, mass - mean_omega)
        count += 1
    return count


def run_cycle(
    variant: str,
    L: int,
    q: int,
    sigma: float,
    n_events: int,
    hard_probs_by_event: list[np.ndarray],
    mean_omegas: list[float],
    local_depth: int,
    theta: float,
    seed: int,
) -> dict[str, float | int | str]:
    if q != 2:
        raise ValueError("this explicit qubit cycle currently supports q=2 only")

    n_bulk = L * L
    n_core = (L - 1) * (L - 1)
    n_shell = 2 * L - 1
    if n_core + n_shell != n_bulk:
        raise ValueError("finite-gauge shell count mismatch")

    rng = np.random.default_rng(seed)
    state, dims = maximally_entangled_state(n_bulk)
    ref_axes = list(range(n_bulk))
    bulk_axes = list(range(n_bulk, 2 * n_bulk))
    core_axes = bulk_axes[:n_core]
    shell_axes = bulk_axes[n_core:]
    port_axis = shell_axes[-1]
    fixed_local_gates = make_local_gates(n_bulk, local_depth, rng)

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    flag_axes: list[int] = []
    edge_axes: list[int] = []

    for event in range(n_events):
        hard_probs = hard_probs_by_event[event]
        if variant == "none":
            pass
        elif variant == "local":
            for i, j, gate in fixed_local_gates:
                state = apply_unitary_to_axes(state, dims, [bulk_axes[i], bulk_axes[j]], gate)
        elif variant == "scrambled":
            state = apply_unitary_to_axes(state, dims, bulk_axes, haar_unitary(2**n_bulk, rng))
        else:
            raise ValueError(f"unknown variant {variant!r}")

        state, dims = append_emission_ancillas(state, dims)
        edge_axis = len(dims) - 4
        flag_axis = len(dims) - 3
        hard_axis = len(dims) - 2
        soft_axis = len(dims) - 1

        state = apply_unitary_to_axes(state, dims, [edge_axis], edge_preparation_unitary(hard_probs))
        state = apply_unitary_to_axes(
            state,
            dims,
            [port_axis, edge_axis, flag_axis, hard_axis, soft_axis],
            unitary_from_hamiltonian(emission_hamiltonian(hard_probs), theta),
        )

        edge_axes.append(edge_axis)
        flag_axes.append(flag_axis)
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

    shell_record_axes: list[int] = []
    for axis in shell_axes:
        state, dims, record_axis = append_record_from_axis(state, dims, axis)
        shell_record_axes.append(record_axis)

    micro_record_axes = flag_axes + hard_axes + soft_axes
    all_record_axes = micro_record_axes + shell_record_axes
    dummy_shell_axes = shell_axes

    rho_latest_hard = reduced_density(state, dims, [hard_axes[-1]])
    d_latest = trace_distance_to_target(rho_latest_hard, hard_probs_by_event[-1])

    emitted_energy = float(np.sum(mean_omegas))
    delta_m = 4.0 * sigma
    return {
        "variant": variant,
        "seed": seed,
        "L": L,
        "q": q,
        "n_bulk": n_bulk,
        "n_core": n_core,
        "n_shell": n_shell,
        "dim_H_L": q ** (L * L),
        "dim_H_L_minus_1": q ** ((L - 1) * (L - 1)),
        "dim_H_shell": q ** (2 * L - 1),
        "n_events": n_events,
        "emitted_energy": emitted_energy,
        "delta_M": delta_m,
        "emitted_over_delta_M": emitted_energy / delta_m,
        "D_latest_hard_to_target": d_latest,
        "S_hard_all": entropy_of_axes(state, dims, hard_axes),
        "I_ref_hard_all": mutual_information(state, dims, ref_axes, hard_axes),
        "I_ref_micro_records": mutual_information(state, dims, ref_axes, micro_record_axes),
        "I_ref_shell_record": mutual_information(state, dims, ref_axes, shell_record_axes),
        "I_ref_all_records": mutual_information(state, dims, ref_axes, all_record_axes),
        "I_ref_core_after": mutual_information(state, dims, ref_axes, core_axes),
        "I_ref_dummy_shell_after": mutual_information(state, dims, ref_axes, dummy_shell_axes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=int, default=2)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--x-edges", nargs="+", type=float, default=[0.0, 2.0, 8.0])
    parser.add_argument("--n-grid", type=int, default=1001)
    parser.add_argument("--n-events", type=int, default=0)
    parser.add_argument("--max-events", type=int, default=4)
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
        "--out",
        type=Path,
        default=Path("sim/data/finite_gauge_evaporation_cycle.csv"),
    )
    args = parser.parse_args()

    x_edges = np.array(args.x_edges, dtype=float)
    n_events = args.n_events
    if n_events <= 0:
        n_events = auto_event_count(
            args.L, args.q, args.sigma, args.bath_dim, x_edges, args.n_grid, args.max_events
        )
    hard_probs_by_event, mean_omegas, temps, delta_m = hard_weights_for_cycle(
        args.L,
        args.q,
        args.sigma,
        args.bath_dim,
        x_edges,
        args.n_grid,
        n_events,
    )

    rows = [
        run_cycle(
            variant,
            args.L,
            args.q,
            args.sigma,
            n_events,
            hard_probs_by_event,
            mean_omegas,
            args.local_depth,
            args.theta,
            args.seed,
        )
        for variant in args.variants
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {args.out}")
    print(
        "weights: "
        + ", ".join(
            f"event {i+1} p1={p[1]:.4f} <omega>={mean_omegas[i]:.4f} T={temps[i]:.4f}"
            for i, p in enumerate(hard_probs_by_event)
        )
    )
    print(f"n_events={n_events}, emitted/deltaM={sum(mean_omegas)/delta_m:.4f}")
    print("variant    D_hard  I(R:hard)  I(R:micro)  I(R:shell)  I(R:allrec)  I(R:core)")
    for row in rows:
        print(
            f"{str(row['variant']):10s} "
            f"{float(row['D_latest_hard_to_target']):7.4f} "
            f"{float(row['I_ref_hard_all']):10.4f} "
            f"{float(row['I_ref_micro_records']):10.4f} "
            f"{float(row['I_ref_shell_record']):10.4f} "
            f"{float(row['I_ref_all_records']):11.4f} "
            f"{float(row['I_ref_core_after']):10.4f}"
        )


if __name__ == "__main__":
    main()
