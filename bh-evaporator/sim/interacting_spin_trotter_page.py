from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from interacting_spin_hamiltonian_page import (
    active_qubits,
    entropy_of_subset,
    margulis_edges,
    random_product_state,
    shell_qubits,
)


@dataclass(frozen=True)
class TrotterPageRow:
    seed: int
    model: str
    L0: int
    warmup_time: float
    cycle_time: float
    dt: float
    L_before: int
    L_after: int
    rad_qubits: int
    shell_qubits: int
    remaining_qubits: int
    page_capacity: float
    s_rad: float
    old_new_mi: float
    entropy_deficit: float


X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
Y = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=np.complex128)
Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
I2 = np.eye(2, dtype=np.complex128)


def one_qubit_gate(hx: float, hz: float, dt: float) -> np.ndarray:
    return expm(-1j * dt * (hx * X + hz * Z))


def two_qubit_gate(jx: float, jy: float, jz: float, dt: float) -> np.ndarray:
    h = (
        jx * np.kron(X, X)
        + jy * np.kron(Y, Y)
        + jz * np.kron(Z, Z)
    )
    return expm(-1j * dt * h).reshape(2, 2, 2, 2)


def apply_one(state: np.ndarray, n_qubits: int, q: int, gate: np.ndarray) -> np.ndarray:
    axis = n_qubits - 1 - q
    tensor = state.reshape((2,) * n_qubits)
    moved = np.moveaxis(tensor, axis, 0)
    updated = np.tensordot(gate, moved, axes=([1], [0]))
    return np.moveaxis(updated, 0, axis).reshape(-1)


def apply_two(
    state: np.ndarray,
    n_qubits: int,
    q0: int,
    q1: int,
    gate: np.ndarray,
) -> np.ndarray:
    if q0 == q1:
        return state
    axes = [n_qubits - 1 - q0, n_qubits - 1 - q1]
    tensor = state.reshape((2,) * n_qubits)
    moved = np.moveaxis(tensor, axes, [0, 1])
    updated = np.tensordot(gate, moved, axes=([2, 3], [0, 1]))
    return np.moveaxis(updated, [0, 1], axes).reshape(-1)


def build_parameters(
    L0: int, seed: int, model: str
) -> tuple[dict[int, tuple[float, float]], dict[tuple[int, int], tuple[float, float, float]]]:
    rng = np.random.default_rng(seed)
    fields: dict[int, tuple[float, float]] = {}
    for q in range(L0 * L0):
        if model == "random_heisenberg":
            fields[q] = tuple(rng.normal(scale=0.7, size=2))  # type: ignore[assignment]
        elif model == "deterministic":
            fields[q] = (
                0.73 + 0.11 * ((q % 5) - 2),
                0.37 + 0.07 * ((q % 7) - 3),
            )
        else:
            raise ValueError(f"unknown model: {model}")

    edges = margulis_edges(L0)
    degree_scale = math.sqrt(max(1.0, 2.0 * len(edges) / (L0 * L0)))
    couplings: dict[tuple[int, int], tuple[float, float, float]] = {}
    for i, j in edges:
        if model == "random_heisenberg":
            couplings[(i, j)] = tuple(rng.normal(size=3) / degree_scale)  # type: ignore[assignment]
        else:
            code = ((i + 3) * (j + 5)) % 17
            couplings[(i, j)] = (
                (0.50 + 0.03 * code) / degree_scale,
                (0.43 + 0.02 * ((code + 5) % 17)) / degree_scale,
                (0.61 + 0.025 * ((code + 11) % 17)) / degree_scale,
            )
    return fields, couplings


def evolve_trotter(
    state: np.ndarray,
    n_qubits: int,
    active: set[int],
    fields: dict[int, tuple[float, float]],
    couplings: dict[tuple[int, int], tuple[float, float, float]],
    time: float,
    dt: float,
) -> np.ndarray:
    if time == 0.0:
        return state
    steps = max(1, math.ceil(time / dt))
    step_dt = time / steps

    one_gates = {
        q: one_qubit_gate(*fields[q], step_dt)
        for q in active
    }
    two_gates = {
        (i, j): two_qubit_gate(jx, jy, jz, step_dt)
        for (i, j), (jx, jy, jz) in couplings.items()
        if i in active and j in active
    }

    for _ in range(steps):
        for q in sorted(active):
            state = apply_one(state, n_qubits, q, one_gates[q])
        for i, j in sorted(two_gates):
            state = apply_two(state, n_qubits, i, j, two_gates[(i, j)])

    return state / np.linalg.norm(state)


def run_trotter_page_diagnostic(
    L0: int,
    model: str,
    warmup_time: float,
    cycle_time: float,
    dt: float,
    seed: int,
) -> list[TrotterPageRow]:
    n_qubits = L0 * L0
    fields, couplings = build_parameters(L0, seed, model)
    state = random_product_state(n_qubits, seed + 10_000)
    radiation: set[int] = set()
    rows: list[TrotterPageRow] = []

    state = evolve_trotter(
        state,
        n_qubits,
        set(active_qubits(L0, L0)),
        fields,
        couplings,
        warmup_time,
        dt,
    )

    for L in range(L0, 0, -1):
        active = set(active_qubits(L0, L))
        state = evolve_trotter(
            state, n_qubits, active, fields, couplings, cycle_time, dt
        )

        old_radiation = set(radiation)
        shell = shell_qubits(L0, L)
        radiation |= shell

        remaining = L * L - len(shell)
        capacity = min(len(radiation), remaining) * math.log(2.0)
        s_old = entropy_of_subset(state, n_qubits, old_radiation)
        s_new = entropy_of_subset(state, n_qubits, shell)
        s_rad = entropy_of_subset(state, n_qubits, radiation)
        old_new_mi = max(0.0, s_old + s_new - s_rad)

        rows.append(
            TrotterPageRow(
                seed=seed,
                model=model,
                L0=L0,
                warmup_time=warmup_time,
                cycle_time=cycle_time,
                dt=dt,
                L_before=L,
                L_after=L - 1,
                rad_qubits=len(radiation),
                shell_qubits=len(shell),
                remaining_qubits=remaining,
                page_capacity=capacity,
                s_rad=s_rad,
                old_new_mi=old_new_mi,
                entropy_deficit=capacity - s_rad,
            )
        )
    return rows


def write_rows(rows: list[TrotterPageRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(TrotterPageRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("random_heisenberg", 4, 4.0, 1.0, 0.2),
        ("random_heisenberg", 4, 8.0, 2.0, 0.2),
        ("random_heisenberg", 4, 12.0, 3.0, 0.25),
        ("deterministic", 4, 8.0, 2.0, 0.2),
    ]
    seeds = list(range(5))

    for model, L0, warmup, cycle, dt in cases:
        all_rows: list[TrotterPageRow] = []
        deficits: list[float] = []
        first_mis: list[str] = []
        for seed in seeds:
            rows = run_trotter_page_diagnostic(
                L0=L0,
                model=model,
                warmup_time=warmup,
                cycle_time=cycle,
                dt=dt,
                seed=seed,
            )
            all_rows.extend(rows)
            deficits.append(sum(max(0.0, row.entropy_deficit) for row in rows))
            first_mi = next((row for row in rows if row.old_new_mi > 1e-6), None)
            if first_mi is not None:
                first_mis.append(f"{first_mi.L_before}->{first_mi.L_after}")

        out_path = out_dir / (
            "interacting_spin_trotter_page_"
            f"{model}_L{L0}_warm{warmup:g}_cyc{cycle:g}_dt{dt:g}.csv"
        )
        write_rows(all_rows, out_path)
        print(
            model,
            f"L0={L0}",
            f"warmup={warmup:g}",
            f"cycle={cycle:g}",
            f"dt={dt:g}",
            f"mean total deficit={sum(deficits) / len(deficits):.3f}",
            f"max total deficit={max(deficits):.3f}",
            "first MI modes=" + ",".join(sorted(set(first_mis))) if first_mis else "",
        )


if __name__ == "__main__":
    main()
