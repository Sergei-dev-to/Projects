from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from interacting_spin_hamiltonian_page import entropy_of_subset, random_product_state
from interacting_spin_stress_test import build_parameters, evolve_trotter, grid_id


@dataclass(frozen=True)
class ScramblingRow:
    seed: int
    graph: str
    model: str
    L0: int
    time: float
    mean_single_entropy: float
    quadrant_entropy: float
    half_entropy: float
    mean_single_fraction: float
    quadrant_fraction: float
    half_fraction: float


def all_qubits(L0: int) -> set[int]:
    return set(range(L0 * L0))


def quadrant_qubits(L0: int) -> set[int]:
    size = max(1, L0 // 2)
    return {grid_id(L0, x, y) for x in range(size) for y in range(size)}


def half_qubits(L0: int) -> set[int]:
    return {grid_id(L0, x, y) for x in range(L0 // 2) for y in range(L0)}


def run_scrambling_case(
    graph: str,
    model: str,
    L0: int,
    times: list[float],
    dt: float,
    seed: int,
) -> list[ScramblingRow]:
    n_qubits = L0 * L0
    fields, couplings = build_parameters(L0, graph, model, seed)
    state = random_product_state(n_qubits, seed + 20_000)
    rows: list[ScramblingRow] = []
    current_time = 0.0
    active = all_qubits(L0)
    quadrant = quadrant_qubits(L0)
    half = half_qubits(L0)

    for target_time in times:
        state = evolve_trotter(
            state,
            n_qubits,
            active,
            fields,
            couplings,
            target_time - current_time,
            dt,
        )
        current_time = target_time

        single_entropies = [
            entropy_of_subset(state, n_qubits, {q}) for q in range(n_qubits)
        ]
        mean_single = float(np.mean(single_entropies))
        quadrant_entropy = entropy_of_subset(state, n_qubits, quadrant)
        half_entropy = entropy_of_subset(state, n_qubits, half)

        rows.append(
            ScramblingRow(
                seed=seed,
                graph=graph,
                model=model,
                L0=L0,
                time=target_time,
                mean_single_entropy=mean_single,
                quadrant_entropy=quadrant_entropy,
                half_entropy=half_entropy,
                mean_single_fraction=mean_single / np.log(2.0),
                quadrant_fraction=quadrant_entropy / (len(quadrant) * np.log(2.0)),
                half_fraction=half_entropy / (len(half) * np.log(2.0)),
            )
        )
    return rows


def write_rows(rows: list[ScramblingRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ScramblingRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def threshold_time(rows: list[ScramblingRow], graph: str, field: str, threshold: float) -> str:
    graph_rows = [row for row in rows if row.graph == graph]
    by_time: dict[float, list[float]] = {}
    for row in graph_rows:
        by_time.setdefault(row.time, []).append(float(getattr(row, field)))
    for time in sorted(by_time):
        if float(np.mean(by_time[time])) >= threshold:
            return f"{time:g}"
    return "not reached"


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    graphs = ["grid", "margulis", "complete"]
    model = "random_heisenberg"
    L0 = 4
    dt = 0.1
    times = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    seeds = list(range(3))

    rows: list[ScramblingRow] = []
    for graph in graphs:
        for seed in seeds:
            rows.extend(run_scrambling_case(graph, model, L0, times, dt, seed))

    write_rows(rows, out_dir / "interacting_spin_scrambling_diagnostic.csv")

    for graph in graphs:
        print(
            graph,
            "single>=0.9",
            threshold_time(rows, graph, "mean_single_fraction", 0.9),
            "quadrant>=0.75",
            threshold_time(rows, graph, "quadrant_fraction", 0.75),
            "half>=0.5",
            threshold_time(rows, graph, "half_fraction", 0.5),
        )
        for time in times:
            same_time = [row for row in rows if row.graph == graph and row.time == time]
            print(
                " ",
                f"t={time:g}",
                f"single={np.mean([r.mean_single_fraction for r in same_time]):.3f}",
                f"quad={np.mean([r.quadrant_fraction for r in same_time]):.3f}",
                f"half={np.mean([r.half_fraction for r in same_time]):.3f}",
            )


if __name__ == "__main__":
    main()
