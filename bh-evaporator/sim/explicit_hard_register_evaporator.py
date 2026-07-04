from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_bath_hamiltonian_emission import run_bath_spectrum_check
from finite_bath_density_emission import integer_degeneracies
from interacting_spin_hamiltonian_page import active_qubits, shell_qubits
from interacting_spin_trotter_page import one_qubit_gate, two_qubit_gate
from stitched_floquet_evaporator import golden_rule_bins, mass_L


@dataclass(frozen=True)
class ExplicitHardRow:
    seed: int
    scrambler: str
    bath_source: str
    L0: int
    L_before: int
    L_after: int
    hard_axis: int
    hard_probability_0: float
    hard_probability_1: float
    latest_hard_entropy: float
    target_hard_entropy: float
    latest_hard_trace_distance: float
    hard_entropy: float
    full_radiation_entropy: float
    core_entropy: float
    page_capacity: float
    entropy_deficit: float
    old_new_mi: float
    first_last_hard_mi: float


@dataclass(frozen=True)
class ExplicitHardSummary:
    seed: int
    scrambler: str
    bath_source: str
    L0: int
    d_hard: int
    total_entropy_deficit: float
    max_latest_hard_trace_distance: float
    max_latest_hard_entropy_error: float
    final_full_radiation_entropy: float
    final_hard_entropy: float
    first_old_new_mi: str
    final_first_last_hard_mi: float
    final_state_dimension: int
    status: str


X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)


def random_product_state_axes(n_qubits: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    state = np.array([1.0 + 0.0j])
    for _ in range(n_qubits):
        theta = rng.uniform(0.0, math.pi)
        phi = rng.uniform(0.0, 2.0 * math.pi)
        qubit = np.array(
            [math.cos(theta / 2.0), np.exp(1j * phi) * math.sin(theta / 2.0)],
            dtype=np.complex128,
        )
        state = np.kron(state, qubit)
    return state / np.linalg.norm(state)


def apply_one_axis(
    state: np.ndarray,
    dims: list[int],
    axis: int,
    gate: np.ndarray,
) -> np.ndarray:
    tensor = state.reshape(dims)
    moved = np.moveaxis(tensor, axis, 0)
    updated = np.tensordot(gate, moved, axes=([1], [0]))
    return np.moveaxis(updated, 0, axis).reshape(-1)


def apply_two_axes(
    state: np.ndarray,
    dims: list[int],
    axis0: int,
    axis1: int,
    gate: np.ndarray,
) -> np.ndarray:
    if axis0 == axis1:
        return state
    tensor = state.reshape(dims)
    moved = np.moveaxis(tensor, [axis0, axis1], [0, 1])
    updated = np.tensordot(gate, moved, axes=([2, 3], [0, 1]))
    return np.moveaxis(updated, [0, 1], [axis0, axis1]).reshape(-1)


def evolve_axes(
    state: np.ndarray,
    dims: list[int],
    active: set[int],
    fields: dict[int, tuple[float, float]],
    couplings: dict[tuple[int, int], tuple[float, float, float]],
    time: float,
    dt: float,
) -> np.ndarray:
    if time == 0.0 or (not fields and not couplings):
        return state
    steps = max(1, math.ceil(time / dt))
    step_dt = time / steps
    one_gates = {
        q: one_qubit_gate(*fields[q], step_dt)
        for q in active
        if q in fields
    }
    two_gates = {
        (i, j): two_qubit_gate(jx, jy, jz, step_dt)
        for (i, j), (jx, jy, jz) in couplings.items()
        if i in active and j in active
    }
    for _ in range(steps):
        for q in sorted(one_gates):
            state = apply_one_axis(state, dims, q, one_gates[q])
        for i, j in sorted(two_gates):
            state = apply_two_axes(state, dims, i, j, two_gates[(i, j)])
    return state / np.linalg.norm(state)


def entropy_subsystem(state: np.ndarray, dims: list[int], keep: list[int]) -> float:
    keep = sorted(set(keep))
    if not keep or len(keep) == len(dims):
        return 0.0
    trace = [axis for axis in range(len(dims)) if axis not in keep]
    d_keep = int(np.prod([dims[axis] for axis in keep], dtype=np.int64))
    d_trace = int(np.prod([dims[axis] for axis in trace], dtype=np.int64))
    if d_keep > d_trace:
        keep, trace = trace, keep
        d_keep, d_trace = d_trace, d_keep
    tensor = state.reshape(dims)
    psi = np.transpose(tensor, keep + trace).reshape(d_keep, d_trace)
    singular_values = np.linalg.svd(psi, compute_uv=False)
    probs = singular_values**2
    probs = probs[probs > 1e-13]
    return float(-np.sum(probs * np.log(probs)))


def reduced_density(state: np.ndarray, dims: list[int], keep: list[int]) -> np.ndarray:
    keep = sorted(set(keep))
    trace = [axis for axis in range(len(dims)) if axis not in keep]
    d_keep = int(np.prod([dims[axis] for axis in keep], dtype=np.int64))
    d_trace = int(np.prod([dims[axis] for axis in trace], dtype=np.int64))
    tensor = state.reshape(dims)
    psi = np.transpose(tensor, keep + trace).reshape(d_keep, d_trace)
    return psi @ psi.conj().T


def trace_distance_to_diag(rho: np.ndarray, probs: np.ndarray) -> float:
    target = np.diag(probs)
    evals = np.linalg.eigvalsh(rho - target)
    return float(0.5 * np.sum(np.abs(evals)))


def mutual_information(
    state: np.ndarray,
    dims: list[int],
    axes_a: list[int],
    axes_b: list[int],
) -> float:
    if not axes_a or not axes_b:
        return 0.0
    return max(
        0.0,
        entropy_subsystem(state, dims, axes_a)
        + entropy_subsystem(state, dims, axes_b)
        - entropy_subsystem(state, dims, axes_a + axes_b),
    )


def hard_probs_from_bath(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    d_hard: int,
    bath_microstates: int,
    bath_source: str,
) -> np.ndarray:
    if bath_source == "box2d":
        rows, _summary = run_bath_spectrum_check(
            spectrum="box2d",
            L=L,
            q=q,
            sigma=sigma,
            bath_dim=bath_dim,
            bin_count=d_hard,
            max_quanta=20,
        )
        probs = np.array([row.bath_probability for row in rows], dtype=float)
        return probs / probs.sum()
    if bath_source != "finite_degeneracy":
        raise ValueError(f"unknown bath_source: {bath_source}")
    distribution = golden_rule_bins(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=d_hard,
    )
    targets = [prob for _, prob in distribution]
    degeneracies = integer_degeneracies(targets, bath_microstates)
    probs = np.array(degeneracies, dtype=float) / float(bath_microstates)
    return probs / probs.sum()


def apply_hard_soft_shell_isometry(
    state: np.ndarray,
    dims: list[int],
    shell_axes: list[int],
    probs: np.ndarray,
) -> tuple[np.ndarray, list[int], int]:
    shell_axes = sorted(shell_axes)
    if not shell_axes:
        dims.append(len(probs))
        return np.kron(state, np.sqrt(probs)), dims, len(dims) - 1

    rest_axes = [axis for axis in range(len(dims)) if axis not in shell_axes]
    tensor = state.reshape(dims)
    permuted = np.transpose(tensor, rest_axes + shell_axes)
    rest_shape = [dims[axis] for axis in rest_axes]
    shell_shape = [dims[axis] for axis in shell_axes]
    d_shell = int(np.prod(shell_shape, dtype=np.int64))
    flat = permuted.reshape(-1, d_shell)

    out = np.zeros((flat.shape[0], len(probs), d_shell), dtype=np.complex128)
    for hard, probability in enumerate(probs):
        # Structured minimal-soft map: hard label plus a reversible shift on
        # the shell/soft register. This keeps hard local thermality while
        # allowing hard+soft correlations to carry shell information.
        out[:, hard, :] = math.sqrt(float(probability)) * np.roll(
            flat, shift=hard, axis=1
        )

    out = out.reshape(rest_shape + [len(probs)] + shell_shape)
    current_axes = rest_axes + ["hard"] + shell_axes
    desired_axes = list(range(len(dims))) + ["hard"]
    transpose_order = [current_axes.index(axis) for axis in desired_axes]
    restored = np.transpose(out, transpose_order)
    new_dims = dims + [len(probs)]
    return restored.reshape(-1), new_dims, len(new_dims) - 1


def run_explicit_hard_evaporator(
    L0: int = 4,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    d_hard: int = 2,
    bath_microstates: int = 2048,
    warmup_time: float = 8.0,
    cycle_time: float = 2.0,
    dt: float = 0.2,
    seed: int = 0,
    scrambler: str = "margulis",
    bath_source: str = "finite_degeneracy",
) -> tuple[list[ExplicitHardRow], ExplicitHardSummary]:
    n_qubits = L0 * L0
    dims = [2] * n_qubits
    state = random_product_state_axes(n_qubits, seed + 20_000)
    fields, couplings = deterministic_parameters(L0, scrambler)
    emitted_shell_axes: list[int] = []
    hard_axes: list[int] = []
    rows: list[ExplicitHardRow] = []
    first_old_new_mi = ""

    state = evolve_axes(
        state,
        dims,
        active=set(active_qubits(L0, L0)),
        fields=fields,
        couplings=couplings,
        time=warmup_time,
        dt=dt,
    )

    for L in range(L0, 0, -1):
        state = evolve_axes(
            state,
            dims,
            active=set(active_qubits(L0, L)),
            fields=fields,
            couplings=couplings,
            time=cycle_time,
            dt=dt,
        )

        old_radiation = emitted_shell_axes + hard_axes
        shell = sorted(shell_qubits(L0, L))
        probs = hard_probs_from_bath(
            L=L,
            q=q,
            sigma=sigma,
            bath_dim=bath_dim,
            d_hard=d_hard,
            bath_microstates=bath_microstates,
            bath_source=bath_source,
        )
        state, dims, hard_axis = apply_hard_soft_shell_isometry(
            state, dims, shell, probs
        )
        hard_axes.append(hard_axis)
        emitted_shell_axes.extend(shell)

        active_after = set(active_qubits(L0, max(0, L - 1)))
        core_axes = sorted(active_after)
        full_radiation = emitted_shell_axes + hard_axes
        latest_pair = shell + [hard_axis]
        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        latest_hard_entropy = entropy_subsystem(state, dims, [hard_axis])
        target_hard_entropy = float(-np.sum(probs * np.log(probs + 1e-300)))
        core_entropy = entropy_subsystem(state, dims, core_axes)
        full_radiation_entropy = entropy_subsystem(state, dims, full_radiation)
        page_capacity = min(
            sum(math.log(dims[axis]) for axis in core_axes),
            sum(math.log(dims[axis]) for axis in full_radiation),
        )
        old_new_mi = mutual_information(state, dims, old_radiation, latest_pair)
        if not first_old_new_mi and old_new_mi > 1e-6:
            first_old_new_mi = f"{L}->{L - 1}"
        first_last_hard_mi = mutual_information(
            state, dims, [hard_axes[0]], [hard_axes[-1]]
        )
        rows.append(
            ExplicitHardRow(
                seed=seed,
                scrambler=scrambler,
                bath_source=bath_source,
                L0=L0,
                L_before=L,
                L_after=L - 1,
                hard_axis=hard_axis,
                hard_probability_0=float(probs[0]),
                hard_probability_1=float(probs[1]) if len(probs) > 1 else 0.0,
                latest_hard_entropy=latest_hard_entropy,
                target_hard_entropy=target_hard_entropy,
                latest_hard_trace_distance=trace_distance_to_diag(
                    latest_hard_rho, probs
                ),
                hard_entropy=entropy_subsystem(state, dims, hard_axes),
                full_radiation_entropy=full_radiation_entropy,
                core_entropy=core_entropy,
                page_capacity=page_capacity,
                entropy_deficit=page_capacity - full_radiation_entropy,
                old_new_mi=old_new_mi,
                first_last_hard_mi=first_last_hard_mi,
            )
        )

    summary = ExplicitHardSummary(
        seed=seed,
        scrambler=scrambler,
        bath_source=bath_source,
        L0=L0,
        d_hard=d_hard,
        total_entropy_deficit=sum(max(0.0, row.entropy_deficit) for row in rows),
        max_latest_hard_trace_distance=max(
            row.latest_hard_trace_distance for row in rows
        ),
        max_latest_hard_entropy_error=max(
            abs(row.latest_hard_entropy - row.target_hard_entropy) for row in rows
        ),
        final_full_radiation_entropy=rows[-1].full_radiation_entropy,
        final_hard_entropy=rows[-1].hard_entropy,
        first_old_new_mi=first_old_new_mi or "none",
        final_first_last_hard_mi=rows[-1].first_last_hard_mi,
        final_state_dimension=int(np.prod(dims, dtype=np.int64)),
        status=(
            "explicit hard-bin quantum registers; shell qubits retained as "
            "soft radiation records"
        ),
    )
    return rows, summary


def write_dataclass_rows(rows: list[object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].__dataclass_fields__)  # type: ignore[attr-defined]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    summaries: list[ExplicitHardSummary] = []
    for bath_source in ("finite_degeneracy", "box2d"):
        for scrambler in ("margulis", "grid", "none"):
            for seed in range(3):
                rows, summary = run_explicit_hard_evaporator(
                    seed=seed,
                    scrambler=scrambler,
                    bath_source=bath_source,
                )
                write_dataclass_rows(
                    rows,
                    out_dir
                    / (
                        "explicit_hard_register_evaporator_"
                        f"{bath_source}_{scrambler}_seed{seed}.csv"
                    ),
                )
                summaries.append(summary)
                print(
                    f"bath={bath_source}",
                    f"scrambler={scrambler}",
                    f"seed={seed}",
                    f"deficit={summary.total_entropy_deficit:.3f}",
                    f"max D_hard={summary.max_latest_hard_trace_distance:.3e}",
                    f"hard S={summary.final_hard_entropy:.3f}",
                    f"first MI={summary.first_old_new_mi}",
                    f"dim={summary.final_state_dimension}",
                )
    write_dataclass_rows(
        summaries, out_dir / "explicit_hard_register_evaporator_summary.csv"
    )


if __name__ == "__main__":
    main()
