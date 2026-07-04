"""Microscopic boundary-emission information-flow diagnostic.

This is a small finite model for the layered evaporator picture:

    bulk register -> boundary port -> hard bath quantum + soft record.

It does not try to be the full edge-tension Hamiltonian.  It tests whether many
microscopic boundary emissions can have the qualitative black-hole information
pattern:

    hard radiation alone is locally thermal;
    hard radiation alone carries little reference information;
    hard+soft emitted records carry information out of the bulk;
    information transfer depends on bulk-to-boundary scrambling.

The initial bulk is maximally entangled with a reference.  A boundary emission
acts on one port qubit.  The port is reset, a hard qubit is emitted with either
fixed thermal weights or golden-rule weights from the droplet entropy curve,
and a soft record stores the purifying information:

    |i>_port -> |0>_port sum_h sqrt(p_h) |h>_hard |i,h>_soft.

Different variants control how much bulk information reaches the boundary port
between emissions:

    none:      no bulk mixing after the first port reset;
    local:     fixed nearest-neighbor two-qubit gates on a bulk chain;
    scrambled: fresh Haar unitary on the full bulk register.
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


def haar_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
    z = (rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))) / math.sqrt(2.0)
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = phases / np.abs(phases)
    return q * phases.conj()


def entropy_of_mass(mass: float, q: int, sigma: float) -> float:
    if mass <= 0.0:
        return 0.0
    return (mass / (4.0 * sigma)) ** 2 * math.log(q)


def beta_of_mass(mass: float, q: int, sigma: float) -> float:
    return mass * math.log(q) / (8.0 * sigma**2)


def golden_rule_hard_distribution(
    mass: float,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
) -> tuple[np.ndarray, float, float]:
    """Return hard-bin probabilities and mean omega from entropy-ratio rates.

    The bins are dimensionless x = beta omega bins.  The number-rate integrand
    is

        omega^(bath_dim - 1) exp[S(M - omega) - S(M)].
    """
    beta = beta_of_mass(mass, q, sigma)
    s0 = entropy_of_mass(mass, q, sigma)
    weights = []
    energy_weights = []
    for x0, x1 in zip(x_edges[:-1], x_edges[1:]):
        capped_x1 = min(float(x1), beta * mass)
        if capped_x1 <= float(x0):
            weights.append(0.0)
            energy_weights.append(0.0)
            continue
        xs = np.linspace(float(x0), capped_x1, n_grid)
        omega = xs / beta
        delta_s = np.array([entropy_of_mass(mass - w, q, sigma) - s0 for w in omega])
        number_integrand = (omega ** max(bath_dim - 1, 0)) * np.exp(delta_s)
        weights.append(float(np.trapezoid(number_integrand, omega)))
        energy_weights.append(float(np.trapezoid(omega * number_integrand, omega)))

    probs = np.array(weights, dtype=float)
    probs = probs / np.sum(probs)
    mean_omega = float(np.sum(energy_weights) / np.sum(weights))
    return probs, mean_omega, 1.0 / beta


def maximally_entangled_state(n_qubits: int) -> tuple[np.ndarray, list[int]]:
    dim = 2**n_qubits
    state = np.zeros((dim, dim), dtype=np.complex128)
    for i in range(dim):
        state[i, i] = 1.0 / math.sqrt(dim)
    dims = [2] * n_qubits + [2] * n_qubits
    return state.reshape(dims), dims


def apply_unitary_to_axes(
    state: np.ndarray,
    dims: list[int],
    axes: list[int],
    unitary: np.ndarray,
) -> np.ndarray:
    axes = list(axes)
    rest = [i for i in range(len(dims)) if i not in axes]
    perm = axes + rest
    inv_perm = np.argsort(perm)
    transposed = np.transpose(state, perm)
    target_dim = int(np.prod([dims[i] for i in axes]))
    rest_dim = int(np.prod([dims[i] for i in rest]))
    matrix = transposed.reshape(target_dim, rest_dim)
    updated = unitary @ matrix
    updated = updated.reshape([dims[i] for i in axes] + [dims[i] for i in rest])
    return np.transpose(updated, inv_perm)


def apply_emission(
    state: np.ndarray,
    dims: list[int],
    port_axis: int,
    hard_probs: np.ndarray,
) -> tuple[np.ndarray, list[int]]:
    """Apply |i> -> |0>_port sum_h sqrt(p_h)|h>|i,h>."""
    rest_axes = [i for i in range(len(dims)) if i != port_axis]
    transposed = np.transpose(state, [port_axis] + rest_axes)
    rest_shape = [dims[i] for i in rest_axes]
    rest_dim = int(np.prod(rest_shape))
    matrix = transposed.reshape(2, rest_dim)

    out = np.zeros((2, 2, 4, rest_dim), dtype=np.complex128)
    for i in range(2):
        for h in range(2):
            soft = 2 * i + h
            out[0, h, soft, :] += math.sqrt(float(hard_probs[h])) * matrix[i, :]

    out = out.reshape([2, 2, 4] + rest_shape)
    # Current axis order is [new_port, hard, soft] + rest_axes.  Restore the
    # port to its original position, with hard/soft appended at the end.
    current_labels = ["port", "hard", "soft"] + rest_axes
    desired_labels: list[int | str] = []
    for old_axis in range(len(dims)):
        if old_axis == port_axis:
            desired_labels.append("port")
        else:
            desired_labels.append(old_axis)
    desired_labels += ["hard", "soft"]
    perm = [current_labels.index(label) for label in desired_labels]
    updated = np.transpose(out, perm)

    new_dims = list(dims)
    new_dims[port_axis] = 2
    new_dims += [2, 4]
    return updated, new_dims


def entropy_of_axes(state: np.ndarray, dims: list[int], keep_axes: list[int], tol: float = 1e-12) -> float:
    if not keep_axes:
        return 0.0
    keep_axes = sorted(keep_axes)
    rest_axes = [i for i in range(len(dims)) if i not in keep_axes]
    keep_dim = int(np.prod([dims[i] for i in keep_axes]))
    rest_dim = int(np.prod([dims[i] for i in rest_axes]))
    perm = keep_axes + rest_axes
    matrix = np.transpose(state, perm).reshape(keep_dim, rest_dim)
    # Entanglement entropy is set by the Schmidt spectrum.  SVD avoids forming
    # very large reduced density matrices.
    singular = np.linalg.svd(matrix, compute_uv=False)
    probs = singular**2
    probs = probs[probs > tol]
    return float(-np.sum(probs * np.log(probs)))


def reduced_density(state: np.ndarray, dims: list[int], keep_axes: list[int]) -> np.ndarray:
    keep_axes = sorted(keep_axes)
    rest_axes = [i for i in range(len(dims)) if i not in keep_axes]
    keep_dim = int(np.prod([dims[i] for i in keep_axes]))
    rest_dim = int(np.prod([dims[i] for i in rest_axes]))
    matrix = np.transpose(state, keep_axes + rest_axes).reshape(keep_dim, rest_dim)
    return matrix @ matrix.conj().T


def mutual_information(state: np.ndarray, dims: list[int], axes_a: list[int], axes_b: list[int]) -> float:
    axes_a = sorted(axes_a)
    axes_b = sorted(axes_b)
    return (
        entropy_of_axes(state, dims, axes_a)
        + entropy_of_axes(state, dims, axes_b)
        - entropy_of_axes(state, dims, sorted(set(axes_a + axes_b)))
    )


def trace_distance_to_target(rho: np.ndarray, target_probs: np.ndarray) -> float:
    target = np.diag(target_probs.astype(np.complex128))
    diff = rho - target
    eigvals = np.linalg.eigvalsh(diff)
    return float(0.5 * np.sum(np.abs(eigvals)))


def make_local_gates(n_bulk: int, depth: int, rng: np.random.Generator) -> list[tuple[int, int, np.ndarray]]:
    gates: list[tuple[int, int, np.ndarray]] = []
    for _ in range(depth):
        for parity in (0, 1):
            for i in range(parity, n_bulk - 1, 2):
                gates.append((i, i + 1, haar_unitary(4, rng)))
    return gates


def run_once(
    variant: str,
    n_bulk: int,
    n_events: int,
    hard_probs_by_event: list[np.ndarray],
    event_mean_omega: list[float],
    event_temperature: list[float],
    event_mass: list[float],
    local_depth: int,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    state, dims = maximally_entangled_state(n_bulk)
    ref_axes = list(range(n_bulk))
    bulk_axes = list(range(n_bulk, 2 * n_bulk))
    port_axis = bulk_axes[-1]
    fixed_local_gates = make_local_gates(n_bulk, local_depth, rng)

    rows: list[dict[str, float | int | str]] = []
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

        state, dims = apply_emission(state, dims, port_axis, hard_probs)

        hard_axes = [2 * n_bulk + 2 * k for k in range(event)]
        soft_axes = [axis + 1 for axis in hard_axes]
        pair_axes = hard_axes + soft_axes
        latest_hard = [hard_axes[-1]]
        latest_pair = [hard_axes[-1], soft_axes[-1]]

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
                "hard_p0": float(hard_probs[0]),
                "hard_p1": float(hard_probs[1]),
                "event_mass": event_mass[event - 1],
                "event_temperature": event_temperature[event - 1],
                "event_mean_omega": event_mean_omega[event - 1],
                "event_mean_omega_over_T": event_mean_omega[event - 1] / event_temperature[event - 1],
                "D_latest_hard_to_target": d_latest,
                "S_latest_hard": entropy_of_axes(state, dims, latest_hard),
                "S_hard_all": entropy_of_axes(state, dims, hard_axes),
                "S_pair_all": entropy_of_axes(state, dims, pair_axes),
                "I_ref_hard_all": mutual_information(state, dims, ref_axes, hard_axes),
                "I_ref_pair_all": mutual_information(state, dims, ref_axes, pair_axes),
                "I_ref_latest_hard": mutual_information(state, dims, ref_axes, latest_hard),
                "I_ref_latest_pair": mutual_information(state, dims, ref_axes, latest_pair),
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
        "S_pair_all",
        "I_ref_hard_all",
        "I_ref_pair_all",
        "I_ref_latest_hard",
        "I_ref_latest_pair",
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
    parser.add_argument("--hard-p1", type=float, default=0.25)
    parser.add_argument(
        "--weight-model",
        choices=["golden", "fixed"],
        default="golden",
    )
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
        default=Path("sim/data/microscopic_boundary_emission.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/microscopic_boundary_emission_summary.csv"),
    )
    args = parser.parse_args()

    hard_probs_by_event: list[np.ndarray] = []
    event_mean_omega: list[float] = []
    event_temperature: list[float] = []
    event_mass: list[float] = []
    mass = 4.0 * args.sigma * args.L0
    if args.weight_model == "fixed":
        fixed_probs = np.array([1.0 - args.hard_p1, args.hard_p1], dtype=float)
    else:
        fixed_probs = np.array([], dtype=float)
    x_edges = np.array(args.x_edges, dtype=float)
    if len(x_edges) != 3:
        raise ValueError("this diagnostic currently expects exactly two hard bins, so provide three x-edges")

    for _event in range(args.n_events):
        if args.weight_model == "fixed":
            probs = fixed_probs
            beta = beta_of_mass(mass, args.q, args.sigma)
            temp = 1.0 / beta
            mean_omega = temp
        else:
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
    print(
        "weights: "
        + ", ".join(
            f"event {i + 1} p1={probs[1]:.4f} <omega>/T={event_mean_omega[i] / event_temperature[i]:.4f}"
            for i, probs in enumerate(hard_probs_by_event)
        )
    )
    print("variant    event  D_hard  I(R:hard)  I(R:pair)  I(R:bulk)")
    for row in summary:
        if int(row["event"]) == args.n_events:
            print(
                f"{str(row['variant']):10s} "
                f"{int(row['event']):5d} "
                f"{float(row['D_latest_hard_to_target_mean']):7.4f} "
                f"{float(row['I_ref_hard_all_mean']):10.4f} "
                f"{float(row['I_ref_pair_all_mean']):10.4f} "
                f"{float(row['I_ref_bulk_remaining_mean']):10.4f}"
            )


if __name__ == "__main__":
    main()
