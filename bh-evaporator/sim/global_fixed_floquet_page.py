from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path

from stabilizer_shell_page_diagnostic import (
    StabilizerState,
    grid_positions,
    nearest_neighbor_edges,
    shell_positions,
)


@dataclass(frozen=True)
class GlobalFloquetPageRow:
    seed: int
    geometry: str
    L0: int
    degree: int
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
class GlobalFloquetLayer:
    one_qubit_gates: tuple[tuple[int, int], ...]
    cnots: tuple[tuple[int, int], ...]


def active_set(L: int, ids: dict[tuple[int, int], int]) -> set[int]:
    return {ids[(r, c)] for r in range(L) for c in range(L)}


def global_expander_like_edges(qubits: list[int], degree: int, seed: int) -> list[tuple[int, int]]:
    rng = random.Random((seed + 1) * 1_000_003 + degree * 9_176)
    edges: set[tuple[int, int]] = set()
    for _ in range(degree):
        shuffled = list(qubits)
        rng.shuffle(shuffled)
        for i in range(0, len(shuffled) - 1, 2):
            a, b = shuffled[i], shuffled[i + 1]
            edges.add((min(a, b), max(a, b)))
    return list(edges)


def margulis_gabber_galil_edges(L0: int, ids: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    """Deterministic algebraic expander-style graph on Z_L0 x Z_L0.

    The directed generators are the standard Margulis/Gabber-Galil maps:

        (x, y) -> (x +/- 2y, y)
        (x, y) -> (x +/- (2y + 1), y)
        (x, y) -> (x, y +/- 2x)
        (x, y) -> (x, y +/- (2x + 1))

    reduced modulo L0. We store the underlying undirected graph.
    """

    edges: set[tuple[int, int]] = set()
    for x in range(L0):
        for y in range(L0):
            src = ids[(x, y)]
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
            for target in targets:
                dst = ids[target]
                if src != dst:
                    edges.add((min(src, dst), max(src, dst)))
    return list(edges)


def build_global_period(
    qubits: list[int],
    edges: list[tuple[int, int]],
    width: int,
    seed: int,
) -> tuple[GlobalFloquetLayer, ...]:
    rng = random.Random((seed + 1) * 10_000_019 + width * 97_409)
    layers: list[GlobalFloquetLayer] = []
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
        layers.append(GlobalFloquetLayer(one_qubit_gates, tuple(cnots)))
    return tuple(layers)


def apply_periods(
    state: StabilizerState,
    period: tuple[GlobalFloquetLayer, ...],
    active: set[int],
    count: int,
) -> None:
    for _ in range(count):
        for layer in period:
            for q, gate in layer.one_qubit_gates:
                if q not in active:
                    continue
                if gate == 1:
                    state.h(q)
                elif gate == 2:
                    state.s(q)
                elif gate == 3:
                    state.h(q)
                    state.s(q)

            for control, target in layer.cnots:
                if control in active and target in active:
                    state.cnot(control, target)


def build_edges(
    geometry: str,
    L0: int,
    ids: dict[tuple[int, int], int],
    degree: int,
    seed: int,
) -> list[tuple[int, int]]:
    if geometry == "grid":
        return nearest_neighbor_edges(L0, ids)
    if geometry == "global_expander":
        return global_expander_like_edges(list(range(L0 * L0)), degree, seed)
    if geometry == "margulis":
        return margulis_gabber_galil_edges(L0, ids)
    raise ValueError(f"unknown geometry: {geometry}")


def run_global_floquet_page_diagnostic(
    L0: int,
    geometry: str,
    degree: int,
    period_width: int,
    warmup_periods: int,
    cycle_periods: int,
    seed: int,
) -> list[GlobalFloquetPageRow]:
    ids = grid_positions(L0)
    edges = build_edges(geometry, L0, ids, degree, seed)
    period = build_global_period(list(range(L0 * L0)), edges, period_width, seed)
    state = StabilizerState(L0 * L0)
    radiation: set[int] = set()
    rows: list[GlobalFloquetPageRow] = []

    apply_periods(state, period, active_set(L0, ids), warmup_periods)

    for L in range(L0, 0, -1):
        active = active_set(L, ids)
        apply_periods(state, period, active, cycle_periods)

        old_radiation = set(radiation)
        new_shell = {ids[pos] for pos in shell_positions(L)}
        radiation |= new_shell

        remaining = L * L - len(new_shell)
        s_old = state.entropy(old_radiation)
        s_new = state.entropy(new_shell)
        s_rad = state.entropy(radiation)
        old_new_mi = s_old + s_new - s_rad

        rows.append(
            GlobalFloquetPageRow(
                seed=seed,
                geometry=geometry,
                L0=L0,
                degree=degree,
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


def write_rows(rows: list[GlobalFloquetPageRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(GlobalFloquetPageRow.__dataclass_fields__)
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("grid", 8, 0, 8, 4, 4),
        ("grid", 8, 0, 16, 2, 2),
        ("global_expander", 8, 8, 8, 4, 1),
        ("global_expander", 8, 16, 8, 4, 1),
        ("global_expander", 8, 16, 16, 2, 1),
        ("global_expander", 12, 12, 8, 4, 1),
        ("global_expander", 12, 24, 8, 4, 1),
        ("global_expander", 12, 24, 16, 2, 1),
        ("margulis", 8, 0, 8, 4, 1),
        ("margulis", 8, 0, 16, 2, 1),
        ("margulis", 12, 0, 8, 4, 1),
        ("margulis", 12, 0, 16, 2, 1),
        ]
    seeds = list(range(10))

    for geometry, L0, degree, width, warmup, cycle in cases:
        all_rows: list[GlobalFloquetPageRow] = []
        errors: list[int] = []
        exact = 0
        first_mis: list[str] = []
        for seed in seeds:
            rows = run_global_floquet_page_diagnostic(
                L0=L0,
                geometry=geometry,
                degree=degree,
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
            "global_fixed_floquet_page_"
            f"{geometry}_L{L0}_d{degree}_w{width}_warm{warmup}_cyc{cycle}.csv"
        )
        write_rows(all_rows, out_path)
        print(
            geometry,
            f"L0={L0}",
            f"degree={degree}",
            f"width={width}",
            f"warmup={warmup}",
            f"cycle={cycle}",
            f"mean |S-cap|={sum(errors) / len(errors):.2f}",
            f"max |S-cap|={max(errors)}",
            f"exact seeds={exact}/{len(seeds)}",
            "first MI modes=" + ",".join(sorted(set(first_mis))) if first_mis else "",
        )


if __name__ == "__main__":
    main()
