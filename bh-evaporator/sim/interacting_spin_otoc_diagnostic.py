from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from interacting_spin_stress_test import build_parameters, get_edges
from interacting_spin_trotter_page import (
    apply_one,
    apply_two,
    one_qubit_gate,
    two_qubit_gate,
)


@dataclass(frozen=True)
class OTOCRow:
    graph: str
    model: str
    L0: int
    seed: int
    sample: int
    source: int
    target: int
    time: float
    commutator: float


@dataclass(frozen=True)
class OTOCSummary:
    graph: str
    model: str
    L0: int
    source: int
    time: float
    mean_commutator: float
    max_commutator: float
    opposite_commutator: float
    fraction_above_025: float
    fraction_above_05: float


def random_state(dim: int, rng: np.random.Generator) -> np.ndarray:
    state = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    return state / np.linalg.norm(state)


def apply_z(state: np.ndarray, n_qubits: int, q: int) -> np.ndarray:
    basis = np.arange(1 << n_qubits, dtype=np.uint64)
    bit = (basis >> np.uint64(q)) & np.uint64(1)
    signs = 1.0 - 2.0 * bit.astype(float)
    return signs * state


def dagger_one(gate: np.ndarray) -> np.ndarray:
    return gate.conj().T


def dagger_two(gate: np.ndarray) -> np.ndarray:
    return gate.reshape(4, 4).conj().T.reshape(2, 2, 2, 2)


def build_step_gates(
    L0: int,
    graph: str,
    model: str,
    seed: int,
    dt: float,
) -> tuple[dict[int, np.ndarray], dict[tuple[int, int], np.ndarray]]:
    fields, couplings = build_parameters(L0, graph, model, seed)
    n_qubits = L0 * L0
    one_gates = {q: one_qubit_gate(*fields[q], dt) for q in range(n_qubits)}
    two_gates = {
        (i, j): two_qubit_gate(jx, jy, jz, dt)
        for (i, j), (jx, jy, jz) in couplings.items()
    }
    return one_gates, two_gates


def apply_step(
    state: np.ndarray,
    n_qubits: int,
    one_gates: dict[int, np.ndarray],
    two_gates: dict[tuple[int, int], np.ndarray],
    inverse: bool = False,
) -> np.ndarray:
    if not inverse:
        for q in sorted(one_gates):
            state = apply_one(state, n_qubits, q, one_gates[q])
        for i, j in sorted(two_gates):
            state = apply_two(state, n_qubits, i, j, two_gates[(i, j)])
        return state

    for i, j in reversed(sorted(two_gates)):
        state = apply_two(state, n_qubits, i, j, dagger_two(two_gates[(i, j)]))
    for q in reversed(sorted(one_gates)):
        state = apply_one(state, n_qubits, q, dagger_one(one_gates[q]))
    return state


def apply_evolution(
    state: np.ndarray,
    n_qubits: int,
    one_gates: dict[int, np.ndarray],
    two_gates: dict[tuple[int, int], np.ndarray],
    steps: int,
    inverse: bool = False,
) -> np.ndarray:
    for _ in range(steps):
        state = apply_step(state, n_qubits, one_gates, two_gates, inverse=inverse)
    return state


def otoc_sample(
    psi: np.ndarray,
    n_qubits: int,
    source: int,
    target: int,
    one_gates: dict[int, np.ndarray],
    two_gates: dict[tuple[int, int], np.ndarray],
    steps: int,
) -> float:
    vector = apply_z(psi, n_qubits, target)
    vector = apply_evolution(vector, n_qubits, one_gates, two_gates, steps)
    vector = apply_z(vector, n_qubits, source)
    vector = apply_evolution(vector, n_qubits, one_gates, two_gates, steps, inverse=True)
    vector = apply_z(vector, n_qubits, target)
    vector = apply_evolution(vector, n_qubits, one_gates, two_gates, steps)
    vector = apply_z(vector, n_qubits, source)
    vector = apply_evolution(vector, n_qubits, one_gates, two_gates, steps, inverse=True)
    otoc = np.vdot(psi, vector)
    commutator = (1.0 - float(np.real(otoc))) / 2.0
    return max(0.0, min(1.0, commutator))


def summarize(rows: list[OTOCRow], graph: str, model: str, L0: int, source: int) -> list[OTOCSummary]:
    summaries: list[OTOCSummary] = []
    opposite = L0 * L0 - 1
    for time in sorted({row.time for row in rows if row.graph == graph}):
        time_rows = [row for row in rows if row.graph == graph and row.time == time]
        by_target: dict[int, list[float]] = {}
        for row in time_rows:
            by_target.setdefault(row.target, []).append(row.commutator)
        target_means = {
            target: float(np.mean(values)) for target, values in by_target.items()
        }
        values = list(target_means.values())
        summaries.append(
            OTOCSummary(
                graph=graph,
                model=model,
                L0=L0,
                source=source,
                time=time,
                mean_commutator=float(np.mean(values)),
                max_commutator=float(np.max(values)),
                opposite_commutator=target_means.get(opposite, 0.0),
                fraction_above_025=float(np.mean([value >= 0.25 for value in values])),
                fraction_above_05=float(np.mean([value >= 0.5 for value in values])),
            )
        )
    return summaries


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
    graphs = ["grid", "margulis", "complete"]
    model = "random_heisenberg"
    L0 = 4
    n_qubits = L0 * L0
    source = 0
    dt = 0.5
    times = [0.0, 0.5, 1.0, 2.0]
    seeds = list(range(3))
    samples_per_seed = 1
    targets = sorted({1, 2, 3, 5, 10, 15})

    rows: list[OTOCRow] = []
    for graph in graphs:
        # Touch the graph builder here so bad graph names fail early and the
        # diagnostic records the intended comparison.
        get_edges(graph, L0)
        for seed in seeds:
            one_gates, two_gates = build_step_gates(
                L0, graph, model, seed, dt
            )
            rng = np.random.default_rng(seed + 50_000)
            for sample in range(samples_per_seed):
                psi = random_state(1 << n_qubits, rng)
                for time in times:
                    steps = max(0, round(time / dt))
                    for target in targets:
                        commutator = 0.0 if steps == 0 else otoc_sample(
                            psi,
                            n_qubits,
                            source,
                            target,
                            one_gates,
                            two_gates,
                            steps,
                        )
                        rows.append(
                            OTOCRow(
                                graph=graph,
                                model=model,
                                L0=L0,
                                seed=seed,
                                sample=sample,
                                source=source,
                                target=target,
                                time=time,
                                commutator=commutator,
                            )
                        )

    summaries: list[OTOCSummary] = []
    for graph in graphs:
        graph_summaries = summarize(rows, graph, model, L0, source)
        summaries.extend(graph_summaries)
        print(graph)
        for summary in graph_summaries:
            print(
                " ",
                f"t={summary.time:g}",
                f"mean={summary.mean_commutator:.3f}",
                f"max={summary.max_commutator:.3f}",
                f"opposite={summary.opposite_commutator:.3f}",
                f"frac>0.25={summary.fraction_above_025:.3f}",
                f"frac>0.5={summary.fraction_above_05:.3f}",
            )

    write_dataclass_rows(rows, out_dir / "interacting_spin_otoc_rows.csv")
    write_dataclass_rows(summaries, out_dir / "interacting_spin_otoc_summary.csv")


if __name__ == "__main__":
    main()
