from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path

from stabilizer_shell_page_diagnostic import (
    StabilizerState,
    build_edge_sets,
    grid_positions,
    shell_positions,
)


@dataclass(frozen=True)
class FloquetPageRow:
    seed: int
    geometry: str
    L0: int
    period_width: int
    warmup_periods: int
    cycle_periods: int
    L_before: int
    L_after: int
    rad_qubits: int
    shell_qubits: int
    remaining_qubits: int
    page_capacity: int
    s_rad: int
    old_new_mi: int


@dataclass(frozen=True)
class FloquetLayer:
    one_qubit_gates: tuple[tuple[int, int], ...]
    cnots: tuple[tuple[int, int], ...]


def active_qubits(L: int, ids: dict[tuple[int, int], int]) -> list[int]:
    return [ids[(r, c)] for r in range(L) for c in range(L)]


def build_floquet_period(
    L: int,
    ids: dict[tuple[int, int], int],
    edges: list[tuple[int, int]],
    width: int,
    seed: int,
) -> tuple[FloquetLayer, ...]:
    rng = random.Random((seed + 1) * 10_000_019 + L * 97_409 + width)
    qubits = active_qubits(L, ids)
    layers: list[FloquetLayer] = []

    for _ in range(width):
        one_qubit_gates = tuple((q, rng.randrange(4)) for q in qubits)

        shuffled_edges = list(edges)
        rng.shuffle(shuffled_edges)
        used: set[int] = set()
        cnots: list[tuple[int, int]] = []
        for a, b in shuffled_edges:
            if a in used or b in used:
                continue
            if rng.random() < 0.5:
                cnots.append((a, b))
            else:
                cnots.append((b, a))
            used.add(a)
            used.add(b)

        layers.append(FloquetLayer(one_qubit_gates, tuple(cnots)))

    return tuple(layers)


def apply_layer(state: StabilizerState, layer: FloquetLayer) -> None:
    for q, gate in layer.one_qubit_gates:
        if gate == 1:
            state.h(q)
        elif gate == 2:
            state.s(q)
        elif gate == 3:
            state.h(q)
            state.s(q)

    for control, target in layer.cnots:
        state.cnot(control, target)


def apply_periods(
    state: StabilizerState,
    period: tuple[FloquetLayer, ...],
    period_count: int,
) -> None:
    for _ in range(period_count):
        for layer in period:
            apply_layer(state, layer)


def run_floquet_page_diagnostic(
    L0: int,
    geometry: str,
    period_width: int,
    warmup_periods: int,
    cycle_periods: int,
    seed: int,
) -> list[FloquetPageRow]:
    ids = grid_positions(L0)
    edge_sets = build_edge_sets(L0, ids, geometry, seed)
    periods = {
        L: build_floquet_period(L, ids, edge_sets[L], period_width, seed)
        for L in range(1, L0 + 1)
    }

    state = StabilizerState(L0 * L0)
    radiation: set[int] = set()
    rows: list[FloquetPageRow] = []

    apply_periods(state, periods[L0], warmup_periods)

    for L in range(L0, 0, -1):
        apply_periods(state, periods[L], cycle_periods)

        old_radiation = set(radiation)
        new_shell = {ids[pos] for pos in shell_positions(L)}
        radiation |= new_shell

        remaining = L * L - len(new_shell)
        s_old = state.entropy(old_radiation)
        s_new = state.entropy(new_shell)
        s_rad = state.entropy(radiation)
        old_new_mi = s_old + s_new - s_rad

        rows.append(
            FloquetPageRow(
                seed=seed,
                geometry=geometry,
                L0=L0,
                period_width=period_width,
                warmup_periods=warmup_periods,
                cycle_periods=cycle_periods,
                L_before=L,
                L_after=L - 1,
                rad_qubits=len(radiation),
                shell_qubits=len(new_shell),
                remaining_qubits=remaining,
                page_capacity=min(len(radiation), remaining),
                s_rad=s_rad,
                old_new_mi=old_new_mi,
            )
        )

    return rows


def write_rows(rows: list[FloquetPageRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(FloquetPageRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("grid", 8, 4, 4, 2),
        ("grid", 8, 4, 4, 8),
        ("expander4", 8, 4, 4, 1),
        ("expander4", 8, 4, 4, 2),
        ("expander8", 8, 4, 4, 1),
        ("expander8", 8, 4, 4, 2),
        ("expander8", 8, 8, 4, 1),
        ("expander8", 8, 16, 2, 1),
        ("expander8", 12, 4, 4, 1),
        ("expander8", 12, 4, 4, 2),
        ("expander8", 12, 8, 4, 1),
        ("expander12", 12, 8, 4, 1),
        ("complete", 8, 4, 4, 1),
    ]
    seeds = list(range(10))

    for geometry, L0, width, warmup, cycle in cases:
        all_rows: list[FloquetPageRow] = []
        errors: list[int] = []
        exact = 0
        first_mis: list[str] = []

        for seed in seeds:
            rows = run_floquet_page_diagnostic(
                L0=L0,
                geometry=geometry,
                period_width=width,
                warmup_periods=warmup,
                cycle_periods=cycle,
                seed=seed,
            )
            all_rows.extend(rows)
            error = sum(abs(row.s_rad - row.page_capacity) for row in rows)
            errors.append(error)
            exact += int(error == 0)
            first_mi = next((row for row in rows if row.old_new_mi > 0), None)
            if first_mi is not None:
                first_mis.append(f"{first_mi.L_before}->{first_mi.L_after}")

        out_path = out_dir / (
            "fixed_floquet_page_"
            f"{geometry}_L{L0}_w{width}_warm{warmup}_cyc{cycle}.csv"
        )
        write_rows(all_rows, out_path)
        print(
            geometry,
            f"L0={L0}",
            f"period_width={width}",
            f"warmup={warmup}",
            f"cycle={cycle}",
            f"mean |S-cap|={sum(errors) / len(errors):.2f}",
            f"max |S-cap|={max(errors)}",
            f"exact seeds={exact}/{len(seeds)}",
            "first MI modes=" + ",".join(sorted(set(first_mis))) if first_mis else "",
        )


if __name__ == "__main__":
    main()
