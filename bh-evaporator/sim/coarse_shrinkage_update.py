"""Coarse shrinkage update after microscopic emissions.

This diagnostic targets the next bottleneck:

    many microscopic emissions happen first;
    then the effective bulk register shrinks H_L -> H_(L-1);
    information that no longer fits in the smaller bulk must already be in
    emitted records.

We model this abstractly with qubits:

    initial bulk: n_bulk qubits maximally entangled with a reference;
    microscopic emissions: energy-aware Hamiltonian block with golden weights;
    coarse shrinkage: keep n_keep bulk qubits and move n_lost qubits into a
    shrink record.

The shrink record is not counted as hard radiation.  It is the soft/internal
record required for the unitary embedding when the effective bulk capacity
shrinks.  The test asks how much reference information is in:

    hard radiation alone,
    microscopic hard+soft records,
    shrink record,
    all records together,
    remaining bulk.
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
    beta_of_mass,
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


def append_shrink_record_from_axis(
    state: np.ndarray,
    dims: list[int],
    source_axis: int,
) -> tuple[np.ndarray, list[int], int]:
    """Copy a bulk qubit into a new shrink-record qubit and reset source.

    This is the unitary action on the subspace with shrink ancilla initialized
    to |0>:

        |i>_source |0>_record -> |0>_source |i>_record.

    Keeping the reset source qubit as a fixed dummy lets axis bookkeeping stay
    simple; the effective smaller bulk excludes it.
    """
    rest_axes = [i for i in range(len(dims)) if i != source_axis]
    transposed = np.transpose(state, [source_axis] + rest_axes)
    rest_shape = [dims[i] for i in rest_axes]
    rest_dim = int(np.prod(rest_shape))
    matrix = transposed.reshape(2, rest_dim)
    out = np.zeros((2, rest_dim, 2), dtype=np.complex128)
    for i in range(2):
        out[0, :, i] = matrix[i, :]
    out = out.reshape([2] + rest_shape + [2])
    # Current order: source, rest_axes, record. Desired: original axes, record.
    current_labels: list[int | str] = [source_axis] + rest_axes + ["record"]
    desired_labels: list[int | str] = list(range(len(dims))) + ["record"]
    perm = [current_labels.index(label) for label in desired_labels]
    updated = np.transpose(out, perm)
    return updated, dims + [2], len(dims)


def run_once(
    variant: str,
    n_bulk: int,
    n_keep: int,
    n_events: int,
    hard_probs_by_event: list[np.ndarray],
    local_depth: int,
    theta: float,
    seed: int,
) -> dict[str, float | int | str]:
    rng = np.random.default_rng(seed)
    state, dims = maximally_entangled_state(n_bulk)
    ref_axes = list(range(n_bulk))
    bulk_axes = list(range(n_bulk, 2 * n_bulk))
    port_axis = bulk_axes[-1]
    fixed_local_gates = make_local_gates(n_bulk, local_depth, rng)

    hard_axes: list[int] = []
    soft_axes: list[int] = []
    flag_axes: list[int] = []
    edge_axes: list[int] = []

    for event in range(1, n_events + 1):
        hard_probs = hard_probs_by_event[event - 1]
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
        decay = unitary_from_hamiltonian(emission_hamiltonian(hard_probs), theta)
        state = apply_unitary_to_axes(
            state,
            dims,
            [port_axis, edge_axis, flag_axis, hard_axis, soft_axis],
            decay,
        )

        edge_axes.append(edge_axis)
        flag_axes.append(flag_axis)
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

    n_lost = n_bulk - n_keep
    shrink_axes: list[int] = []
    # Remove from the interior side first so the shrink record actually tests
    # capacity transfer rather than just recording the already reset port. This
    # is a coarse register update, not a physical spatial prescription.
    lost_axes = bulk_axes[:n_lost]
    remaining_bulk_axes = bulk_axes[n_lost:]
    for axis in lost_axes:
        state, dims, record_axis = append_shrink_record_from_axis(state, dims, axis)
        shrink_axes.append(record_axis)

    microscopic_record_axes = flag_axes + hard_axes + soft_axes
    all_record_axes = microscopic_record_axes + shrink_axes
    latest_hard = [hard_axes[-1]]

    rho_latest_hard = reduced_density(state, dims, latest_hard)
    d_latest = trace_distance_to_target(rho_latest_hard, hard_probs_by_event[-1])

    return {
        "variant": variant,
        "seed": seed,
        "n_bulk": n_bulk,
        "n_keep": n_keep,
        "n_lost": n_lost,
        "n_events": n_events,
        "D_latest_hard_to_target": d_latest,
        "S_hard_all": entropy_of_axes(state, dims, hard_axes),
        "I_ref_hard_all": mutual_information(state, dims, ref_axes, hard_axes),
        "I_ref_microscopic_records": mutual_information(state, dims, ref_axes, microscopic_record_axes),
        "I_ref_shrink_record": mutual_information(state, dims, ref_axes, shrink_axes),
        "I_ref_all_records": mutual_information(state, dims, ref_axes, all_record_axes),
        "I_ref_remaining_bulk": mutual_information(state, dims, ref_axes, remaining_bulk_axes),
        "I_ref_dummy_lost_bulk": mutual_information(state, dims, ref_axes, lost_axes),
    }


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | int | str]]:
    grouped: dict[str, list[dict[str, float | int | str]]] = {}
    for row in rows:
        grouped.setdefault(str(row["variant"]), []).append(row)

    metrics = [
        "D_latest_hard_to_target",
        "S_hard_all",
        "I_ref_hard_all",
        "I_ref_microscopic_records",
        "I_ref_shrink_record",
        "I_ref_all_records",
        "I_ref_remaining_bulk",
        "I_ref_dummy_lost_bulk",
    ]
    summary = []
    for variant, group in sorted(grouped.items()):
        out: dict[str, float | int | str] = {"variant": variant, "n": len(group)}
        for metric in metrics:
            vals = np.array([float(row[metric]) for row in group])
            out[f"{metric}_mean"] = float(np.mean(vals))
            out[f"{metric}_std"] = float(np.std(vals))
        summary.append(out)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-bulk", type=int, default=4)
    parser.add_argument("--n-keep", type=int, default=3)
    parser.add_argument("--n-events", type=int, default=3)
    parser.add_argument("--local-depth", type=int, default=1)
    parser.add_argument("--seeds", type=int, default=1)
    parser.add_argument("--theta", type=float, default=math.pi / 2.0)
    parser.add_argument("--L0", type=float, default=20.0)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--x-edges", nargs="+", type=float, default=[0.0, 2.0, 8.0])
    parser.add_argument("--n-grid", type=int, default=1001)
    parser.add_argument(
        "--variants",
        nargs="+",
        default=["none", "local", "scrambled"],
        choices=["none", "local", "scrambled"],
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/coarse_shrinkage_update.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/coarse_shrinkage_update_summary.csv"),
    )
    args = parser.parse_args()

    hard_probs_by_event = []
    mass = 4.0 * args.sigma * args.L0
    for _event in range(args.n_events):
        probs, mean_omega, _temp = golden_rule_hard_distribution(
            mass,
            args.q,
            args.sigma,
            args.bath_dim,
            np.array(args.x_edges, dtype=float),
            args.n_grid,
        )
        hard_probs_by_event.append(probs)
        mass = max(1e-12, mass - mean_omega)

    rows = []
    for variant in args.variants:
        for seed in range(args.seeds):
            rows.append(
                run_once(
                    variant,
                    args.n_bulk,
                    args.n_keep,
                    args.n_events,
                    hard_probs_by_event,
                    args.local_depth,
                    args.theta,
                    seed,
                )
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print("variant    D_hard  I(R:hard)  I(R:micro)  I(R:shrink)  I(R:allrec)  I(R:bulk)")
    for row in summary:
        print(
            f"{str(row['variant']):10s} "
            f"{float(row['D_latest_hard_to_target_mean']):7.4f} "
            f"{float(row['I_ref_hard_all_mean']):10.4f} "
            f"{float(row['I_ref_microscopic_records_mean']):10.4f} "
            f"{float(row['I_ref_shrink_record_mean']):11.4f} "
            f"{float(row['I_ref_all_records_mean']):11.4f} "
            f"{float(row['I_ref_remaining_bulk_mean']):10.4f}"
        )


if __name__ == "__main__":
    main()
