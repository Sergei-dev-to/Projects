from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_hard_register_evaporator import (
    entropy_subsystem,
    evolve_axes,
    random_product_state_axes,
    reduced_density,
    trace_distance_to_diag,
)
from interacting_spin_hamiltonian_page import active_qubits, shell_qubits


@dataclass(frozen=True)
class IntegratedStateRow:
    seed: int
    scrambler: str
    L0: int
    L_before: int
    L_after: int
    core_qubits: int
    soft_qubits: int
    hard_axes: int
    bath_axes: int
    page_capacity: float
    soft_entropy: float
    full_radiation_entropy: float
    visible_radiation_entropy: float
    hard_visible_entropy: float
    latest_hard_entropy: float
    latest_hard_trace_distance: float
    old_new_soft_mi: float
    old_new_visible_mi: float
    entropy_deficit: float


@dataclass(frozen=True)
class IntegratedStateSummary:
    seed: int
    scrambler: str
    L0: int
    warmup_time: float
    cycle_time: float
    dt: float
    final_dimension: int
    total_soft_page_deficit: float
    peak_soft_entropy: float
    final_soft_entropy: float
    final_hard_visible_entropy: float
    final_full_radiation_entropy: float
    max_latest_hard_trace_distance: float
    first_old_new_soft_mi: str
    first_old_new_visible_mi: str
    status: str


def append_hard_bath_pair(
    state: np.ndarray,
    dims: list[int],
) -> tuple[np.ndarray, list[int], int, int]:
    # Coarse hidden bath purifier for the two visible hard bins. The larger
    # global-register tests use eight 2D-box bath microstates; here we collapse
    # that to the minimal hidden dimension needed to test hard-local thermality
    # inside a full state-vector Page diagnostic.
    pair = np.zeros((2, 2), dtype=np.complex128)
    amplitude = 1.0 / math.sqrt(2.0)
    pair[0, 0] = amplitude
    pair[1, 1] = amplitude

    new_state = np.kron(state, pair.reshape(-1))
    hard_axis = len(dims)
    bath_axis = len(dims) + 1
    new_dims = dims + [2, 2]
    return new_state / np.linalg.norm(new_state), new_dims, hard_axis, bath_axis


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


def run_integrated_statevector(
    L0: int = 3,
    warmup_time: float = 8.0,
    cycle_time: float = 2.0,
    dt: float = 0.2,
    seed: int = 0,
    scrambler: str = "margulis",
) -> tuple[list[IntegratedStateRow], IntegratedStateSummary]:
    n_qubits = L0 * L0
    state = random_product_state_axes(n_qubits, seed + 50_000)
    dims = [2] * n_qubits
    fields, couplings = deterministic_parameters(L0, scrambler)
    soft_axes: list[int] = []
    hard_axes: list[int] = []
    bath_axes: list[int] = []
    rows: list[IntegratedStateRow] = []
    first_old_new_soft_mi = ""
    first_old_new_visible_mi = ""

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

        old_soft = list(soft_axes)
        old_visible = list(soft_axes + hard_axes)
        new_shell = sorted(shell_qubits(L0, L))
        state, dims, hard_axis, bath_axis = append_hard_bath_pair(state, dims)
        hard_axes.append(hard_axis)
        bath_axes.append(bath_axis)
        soft_axes.extend(new_shell)

        core_axes = sorted(active_qubits(L0, L - 1))
        visible_radiation = soft_axes + hard_axes
        full_radiation = soft_axes + hard_axes + bath_axes
        latest_visible = new_shell + [hard_axis]

        soft_entropy = entropy_subsystem(state, dims, soft_axes)
        full_radiation_entropy = entropy_subsystem(state, dims, full_radiation)
        visible_radiation_entropy = entropy_subsystem(state, dims, visible_radiation)
        hard_visible_entropy = entropy_subsystem(state, dims, hard_axes)
        latest_hard_entropy = entropy_subsystem(state, dims, [hard_axis])
        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        latest_hard_trace_distance = trace_distance_to_diag(
            latest_hard_rho, np.array([0.5, 0.5], dtype=float)
        )

        old_new_soft_mi = mutual_information(state, dims, old_soft, new_shell)
        old_new_visible_mi = mutual_information(
            state, dims, old_visible, latest_visible
        )
        if not first_old_new_soft_mi and old_new_soft_mi > 1e-6:
            first_old_new_soft_mi = f"{L}->{L - 1}"
        if not first_old_new_visible_mi and old_new_visible_mi > 1e-6:
            first_old_new_visible_mi = f"{L}->{L - 1}"

        page_capacity = min(len(soft_axes), len(core_axes)) * math.log(2.0)
        rows.append(
            IntegratedStateRow(
                seed=seed,
                scrambler=scrambler,
                L0=L0,
                L_before=L,
                L_after=L - 1,
                core_qubits=len(core_axes),
                soft_qubits=len(soft_axes),
                hard_axes=len(hard_axes),
                bath_axes=len(bath_axes),
                page_capacity=page_capacity,
                soft_entropy=soft_entropy,
                full_radiation_entropy=full_radiation_entropy,
                visible_radiation_entropy=visible_radiation_entropy,
                hard_visible_entropy=hard_visible_entropy,
                latest_hard_entropy=latest_hard_entropy,
                latest_hard_trace_distance=latest_hard_trace_distance,
                old_new_soft_mi=old_new_soft_mi,
                old_new_visible_mi=old_new_visible_mi,
                entropy_deficit=page_capacity - soft_entropy,
            )
        )

    summary = IntegratedStateSummary(
        seed=seed,
        scrambler=scrambler,
        L0=L0,
        warmup_time=warmup_time,
        cycle_time=cycle_time,
        dt=dt,
        final_dimension=int(np.prod(dims, dtype=np.int64)),
        total_soft_page_deficit=sum(max(0.0, row.entropy_deficit) for row in rows),
        peak_soft_entropy=max(row.soft_entropy for row in rows),
        final_soft_entropy=rows[-1].soft_entropy,
        final_hard_visible_entropy=rows[-1].hard_visible_entropy,
        final_full_radiation_entropy=rows[-1].full_radiation_entropy,
        max_latest_hard_trace_distance=max(
            row.latest_hard_trace_distance for row in rows
        ),
        first_old_new_soft_mi=first_old_new_soft_mi or "none",
        first_old_new_visible_mi=first_old_new_visible_mi or "none",
        status=(
            "small integrated state-vector evaporator with scrambling, soft "
            "shell records, visible hard bins, and hidden bath records"
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
    summaries: list[IntegratedStateSummary] = []
    for scrambler in ("margulis", "grid", "none"):
        for seed in range(3):
            rows, summary = run_integrated_statevector(
                seed=seed,
                scrambler=scrambler,
            )
            write_dataclass_rows(
                rows,
                out_dir
                / f"integrated_statevector_evaporator_{scrambler}_seed{seed}.csv",
            )
            summaries.append(summary)
            print(
                f"scrambler={scrambler}",
                f"seed={seed}",
                f"deficit={summary.total_soft_page_deficit:.3f}",
                f"peak_soft={summary.peak_soft_entropy:.3f}",
                f"final_soft={summary.final_soft_entropy:.3f}",
                f"hard={summary.final_hard_visible_entropy:.3f}",
                f"full_rad={summary.final_full_radiation_entropy:.3f}",
                f"maxD={summary.max_latest_hard_trace_distance:.3e}",
                f"softMI={summary.first_old_new_soft_mi}",
                f"visibleMI={summary.first_old_new_visible_mi}",
                f"dim={summary.final_dimension}",
            )
    write_dataclass_rows(summaries, out_dir / "integrated_statevector_evaporator_summary.csv")


if __name__ == "__main__":
    main()
