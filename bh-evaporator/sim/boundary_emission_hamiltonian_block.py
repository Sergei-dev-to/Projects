"""Hamiltonian block for microscopic golden boundary emission.

This upgrades the diagnostic channel

    |i>_port -> |0>_port sum_h sqrt(p_h) |h>_hard |i,h>_soft

to an explicit finite local Hamiltonian pulse.  Fresh emission ancillas are
added for each event:

    flag in {in, out}, hard in {0, 1}, soft in {0, 1, 2, 3}.

The Hamiltonian couples

    |i, in, 0, 0> <-> |0, out, h, 2*i+h>

with amplitude sqrt(p_h).  At theta = pi/2, exp(-i theta H) maps the input
subspace exactly to the hard/soft emission isometry, up to a phase.

The point is not that this block form is mathematically new.  The point is to
remove one artificial step from the current edge-tension evaporator diagnostic:
the boundary emission is now a finite Hamiltonian pulse with golden-rule hard
weights.
"""

from __future__ import annotations

import argparse
import csv
import gc
import math
import os
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np

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


def local_index(port: int, flag: int, hard: int, soft: int) -> int:
    return (((port * 2) + flag) * 2 + hard) * 4 + soft


def emission_hamiltonian(hard_probs: np.ndarray) -> np.ndarray:
    dim = 2 * 2 * 2 * 4
    hmat = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(2):
        in_idx = local_index(i, 0, 0, 0)
        for h in range(2):
            out_idx = local_index(0, 1, h, 2 * i + h)
            amp = math.sqrt(float(hard_probs[h]))
            hmat[out_idx, in_idx] += amp
            hmat[in_idx, out_idx] += amp
    return hmat


def unitary_from_hamiltonian(hmat: np.ndarray, theta: float) -> np.ndarray:
    vals, vecs = np.linalg.eigh(hmat)
    phases = np.exp(-1j * theta * vals)
    return (vecs * phases) @ vecs.conj().T


def append_emission_ancillas(state: np.ndarray, dims: list[int]) -> tuple[np.ndarray, list[int]]:
    new_shape = list(state.shape) + [2, 2, 4]
    out = np.zeros(new_shape, dtype=np.complex128)
    out[(..., 0, 0, 0)] = state
    return out, dims + [2, 2, 4]


def local_block_error(hard_probs: np.ndarray, theta: float) -> float:
    unitary = unitary_from_hamiltonian(emission_hamiltonian(hard_probs), theta)
    max_err = 0.0
    for i in range(2):
        vec = np.zeros(32, dtype=np.complex128)
        vec[local_index(i, 0, 0, 0)] = 1.0
        evolved = unitary @ vec
        target = np.zeros(32, dtype=np.complex128)
        for h in range(2):
            target[local_index(0, 1, h, 2 * i + h)] = -1j * math.sqrt(float(hard_probs[h]))
        max_err = max(max_err, float(np.linalg.norm(evolved - target)))
    return max_err


def run_once(
    variant: str,
    n_bulk: int,
    n_events: int,
    hard_probs_by_event: list[np.ndarray],
    event_mean_omega: list[float],
    event_temperature: list[float],
    event_mass: list[float],
    local_depth: int,
    theta: float,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    state, dims = maximally_entangled_state(n_bulk)
    ref_axes = list(range(n_bulk))
    bulk_axes = list(range(n_bulk, 2 * n_bulk))
    port_axis = bulk_axes[-1]
    fixed_local_gates = make_local_gates(n_bulk, local_depth, rng)

    rows: list[dict[str, float | int | str]] = []
    hard_axes: list[int] = []
    soft_axes: list[int] = []
    flag_axes: list[int] = []

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
        flag_axis = len(dims) - 3
        hard_axis = len(dims) - 2
        soft_axis = len(dims) - 1
        unitary = unitary_from_hamiltonian(emission_hamiltonian(hard_probs), theta)
        state = apply_unitary_to_axes(state, dims, [port_axis, flag_axis, hard_axis, soft_axis], unitary)

        flag_axes.append(flag_axis)
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

        latest_hard = [hard_axes[-1]]
        latest_record = [flag_axes[-1], hard_axes[-1], soft_axes[-1]]
        emitted_record_axes = flag_axes + hard_axes + soft_axes

        rho_latest_hard = reduced_density(state, dims, latest_hard)
        d_latest = trace_distance_to_target(rho_latest_hard, hard_probs)

        rows.append(
            {
                "variant": variant,
                "seed": seed,
                "event": event,
                "n_bulk": n_bulk,
                "n_events": n_events,
                "local_depth": local_depth,
                "theta": theta,
                "hard_p0": float(hard_probs[0]),
                "hard_p1": float(hard_probs[1]),
                "event_mass": event_mass[event - 1],
                "event_temperature": event_temperature[event - 1],
                "event_mean_omega": event_mean_omega[event - 1],
                "event_mean_omega_over_T": event_mean_omega[event - 1] / event_temperature[event - 1],
                "D_latest_hard_to_target": d_latest,
                "S_latest_hard": entropy_of_axes(state, dims, latest_hard),
                "S_hard_all": entropy_of_axes(state, dims, hard_axes),
                "S_record_all": entropy_of_axes(state, dims, emitted_record_axes),
                "I_ref_hard_all": mutual_information(state, dims, ref_axes, hard_axes),
                "I_ref_record_all": mutual_information(state, dims, ref_axes, emitted_record_axes),
                "I_ref_latest_hard": mutual_information(state, dims, ref_axes, latest_hard),
                "I_ref_latest_record": mutual_information(state, dims, ref_axes, latest_record),
                "I_ref_bulk_remaining": mutual_information(state, dims, ref_axes, bulk_axes),
            }
        )

    return rows


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[str, int], list[dict[str, float | int | str]]] = {}
    for row in rows:
        grouped.setdefault((str(row["variant"]), int(row["event"])), []).append(row)

    metrics = [
        "D_latest_hard_to_target",
        "S_latest_hard",
        "S_hard_all",
        "S_record_all",
        "I_ref_hard_all",
        "I_ref_record_all",
        "I_ref_latest_hard",
        "I_ref_latest_record",
        "I_ref_bulk_remaining",
    ]
    summary = []
    for (variant, event), group in sorted(grouped.items()):
        out: dict[str, float | int | str] = {
            "variant": variant,
            "event": event,
            "n": len(group),
        }
        for metric in metrics:
            vals = np.array([float(row[metric]) for row in group])
            out[f"{metric}_mean"] = float(np.mean(vals))
            out[f"{metric}_std"] = float(np.std(vals))
        summary.append(out)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-bulk", type=int, default=4)
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
        default=Path("sim/data/boundary_emission_hamiltonian_block.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/boundary_emission_hamiltonian_block_summary.csv"),
    )
    args = parser.parse_args()

    hard_probs_by_event: list[np.ndarray] = []
    event_mean_omega: list[float] = []
    event_temperature: list[float] = []
    event_mass: list[float] = []
    mass = 4.0 * args.sigma * args.L0
    x_edges = np.array(args.x_edges, dtype=float)
    if len(x_edges) != 3:
        raise ValueError("this diagnostic currently expects exactly two hard bins")

    for _event in range(args.n_events):
        probs, mean_omega, temp = golden_rule_hard_distribution(
            mass,
            args.q,
            args.sigma,
            args.bath_dim,
            x_edges,
            args.n_grid,
        )
        hard_probs_by_event.append(probs)
        event_mean_omega.append(mean_omega)
        event_temperature.append(temp)
        event_mass.append(mass)
        mass = max(1e-12, mass - mean_omega)

    block_error = local_block_error(hard_probs_by_event[0], args.theta)

    rows: list[dict[str, float | int | str]] = []
    for variant in args.variants:
        for seed in range(args.seeds):
            rows.extend(
                run_once(
                    variant,
                    args.n_bulk,
                    args.n_events,
                    hard_probs_by_event,
                    event_mean_omega,
                    event_temperature,
                    event_mass,
                    args.local_depth,
                    args.theta,
                    seed,
                )
            )
            gc.collect()

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
    print(f"local Hamiltonian block error: {block_error:.3e}")
    print(
        "weights: "
        + ", ".join(
            f"event {i + 1} p1={probs[1]:.4f} <omega>/T={event_mean_omega[i] / event_temperature[i]:.4f}"
            for i, probs in enumerate(hard_probs_by_event)
        )
    )
    print("variant    event  D_hard  I(R:hard)  I(R:record)  I(R:bulk)")
    for row in summary:
        if int(row["event"]) == args.n_events:
            print(
                f"{str(row['variant']):10s} "
                f"{int(row['event']):5d} "
                f"{float(row['D_latest_hard_to_target_mean']):7.4f} "
                f"{float(row['I_ref_hard_all_mean']):10.4f} "
                f"{float(row['I_ref_record_all_mean']):11.4f} "
                f"{float(row['I_ref_bulk_remaining_mean']):10.4f}"
            )


if __name__ == "__main__":
    main()
