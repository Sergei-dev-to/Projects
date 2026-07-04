from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from interacting_spin_hamiltonian_page import (
    active_qubits,
    entropy_of_subset,
    random_product_state,
    shell_qubits,
)
from interacting_spin_trotter_page import (
    apply_one,
    apply_two,
    one_qubit_gate,
    two_qubit_gate,
)


@dataclass(frozen=True)
class StressSummary:
    graph: str
    model: str
    L0: int
    warmup_time: float
    cycle_time: float
    dt: float
    seeds: int
    mean_total_deficit: float
    max_total_deficit: float
    mean_peak_deficit: float
    first_mi_modes: str


@dataclass(frozen=True)
class StressRow:
    seed: int
    graph: str
    model: str
    L0: int
    warmup_time: float
    cycle_time: float
    dt: float
    L_before: int
    L_after: int
    rad_qubits: int
    remaining_qubits: int
    page_capacity: float
    s_rad: float
    old_new_mi: float
    entropy_deficit: float


def grid_id(L0: int, x: int, y: int) -> int:
    return x * L0 + y


def grid_edges(L0: int) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for x in range(L0):
        for y in range(L0):
            if x + 1 < L0:
                edges.append((grid_id(L0, x, y), grid_id(L0, x + 1, y)))
            if y + 1 < L0:
                edges.append((grid_id(L0, x, y), grid_id(L0, x, y + 1)))
    return edges


def complete_edges(L0: int) -> list[tuple[int, int]]:
    n = L0 * L0
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def margulis_edges(L0: int) -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for x in range(L0):
        for y in range(L0):
            src = grid_id(L0, x, y)
            targets = [
                ((x + 2 * y) % L0, y),
                ((x - 2 * y) % L0, y),
                ((x + 2 * y + 1) % L0, y),
                ((x - 2 * y - 1) % L0, y),
                (x, (y + 2 * x) % L0),
                (x, (y - 2 * x) % L0),
                (x, (y + 2 * x + 1) % L0),
                (x, (y - 2 * x - 1) % L0),
            ]
            for tx, ty in targets:
                dst = grid_id(L0, tx, ty)
                if src != dst:
                    edges.add((min(src, dst), max(src, dst)))
    return list(edges)


def get_edges(graph: str, L0: int) -> list[tuple[int, int]]:
    if graph == "grid":
        return grid_edges(L0)
    if graph == "margulis":
        return margulis_edges(L0)
    if graph == "complete":
        return complete_edges(L0)
    raise ValueError(f"unknown graph: {graph}")


def build_parameters(
    L0: int,
    graph: str,
    model: str,
    seed: int,
) -> tuple[
    dict[int, tuple[float, float]],
    dict[tuple[int, int], tuple[float, float, float]],
]:
    rng = np.random.default_rng(seed)
    n_qubits = L0 * L0
    fields: dict[int, tuple[float, float]] = {}
    for q in range(n_qubits):
        if model == "random_heisenberg":
            fields[q] = tuple(rng.normal(scale=0.7, size=2))  # type: ignore[assignment]
        elif model == "deterministic":
            fields[q] = (
                0.73 + 0.11 * ((q % 5) - 2),
                0.37 + 0.07 * ((q % 7) - 3),
            )
        else:
            raise ValueError(f"unknown model: {model}")

    edges = get_edges(graph, L0)
    degree_scale = math.sqrt(max(1.0, 2.0 * len(edges) / n_qubits))
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
    one_gates = {q: one_qubit_gate(*fields[q], step_dt) for q in active}
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


def run_case(
    graph: str,
    model: str,
    L0: int,
    warmup_time: float,
    cycle_time: float,
    dt: float,
    seed: int,
) -> list[StressRow]:
    n_qubits = L0 * L0
    fields, couplings = build_parameters(L0, graph, model, seed)
    state = random_product_state(n_qubits, seed + 10_000)
    radiation: set[int] = set()
    rows: list[StressRow] = []

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
        state = evolve_trotter(
            state,
            n_qubits,
            set(active_qubits(L0, L)),
            fields,
            couplings,
            cycle_time,
            dt,
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
            StressRow(
                seed=seed,
                graph=graph,
                model=model,
                L0=L0,
                warmup_time=warmup_time,
                cycle_time=cycle_time,
                dt=dt,
                L_before=L,
                L_after=L - 1,
                rad_qubits=len(radiation),
                remaining_qubits=remaining,
                page_capacity=capacity,
                s_rad=s_rad,
                old_new_mi=old_new_mi,
                entropy_deficit=capacity - s_rad,
            )
        )
    return rows


def summarize(rows_by_seed: list[list[StressRow]]) -> StressSummary:
    first = rows_by_seed[0][0]
    total_deficits = [
        sum(max(0.0, row.entropy_deficit) for row in rows)
        for rows in rows_by_seed
    ]
    peak_deficits = [
        max(max(0.0, row.entropy_deficit) for row in rows)
        for rows in rows_by_seed
    ]
    first_mis: list[str] = []
    for rows in rows_by_seed:
        first_mi = next((row for row in rows if row.old_new_mi > 1e-6), None)
        if first_mi is not None:
            first_mis.append(f"{first_mi.L_before}->{first_mi.L_after}")
    return StressSummary(
        graph=first.graph,
        model=first.model,
        L0=first.L0,
        warmup_time=first.warmup_time,
        cycle_time=first.cycle_time,
        dt=first.dt,
        seeds=len(rows_by_seed),
        mean_total_deficit=float(np.mean(total_deficits)),
        max_total_deficit=float(np.max(total_deficits)),
        mean_peak_deficit=float(np.mean(peak_deficits)),
        first_mi_modes=",".join(sorted(set(first_mis))),
    )


def write_dataclass_rows(rows: list[object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].__dataclass_fields__))  # type: ignore[attr-defined]
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("grid", "random_heisenberg", 4, 8.0, 2.0, 0.2),
        ("margulis", "random_heisenberg", 4, 8.0, 2.0, 0.2),
        ("complete", "random_heisenberg", 4, 8.0, 2.0, 0.2),
        ("margulis", "deterministic", 4, 8.0, 2.0, 0.2),
        ("margulis", "random_heisenberg", 4, 8.0, 2.0, 0.1),
        ("margulis", "random_heisenberg", 4, 8.0, 2.0, 0.4),
        ("margulis", "random_heisenberg", 4, 4.0, 1.0, 0.2),
        ("margulis", "random_heisenberg", 4, 12.0, 3.0, 0.25),
    ]
    seeds = list(range(3))
    summaries: list[StressSummary] = []
    all_rows: list[StressRow] = []

    for graph, model, L0, warmup, cycle, dt in cases:
        rows_by_seed = [
            run_case(graph, model, L0, warmup, cycle, dt, seed)
            for seed in seeds
        ]
        rows = [row for seed_rows in rows_by_seed for row in seed_rows]
        all_rows.extend(rows)
        summary = summarize(rows_by_seed)
        summaries.append(summary)
        print(
            graph,
            model,
            f"L0={L0}",
            f"warmup={warmup:g}",
            f"cycle={cycle:g}",
            f"dt={dt:g}",
            f"mean total deficit={summary.mean_total_deficit:.3f}",
            f"max total deficit={summary.max_total_deficit:.3f}",
            f"mean peak deficit={summary.mean_peak_deficit:.3f}",
            f"first MI={summary.first_mi_modes}",
        )

    write_dataclass_rows(all_rows, out_dir / "interacting_spin_stress_rows.csv")
    write_dataclass_rows(summaries, out_dir / "interacting_spin_stress_summary.csv")


if __name__ == "__main__":
    main()
