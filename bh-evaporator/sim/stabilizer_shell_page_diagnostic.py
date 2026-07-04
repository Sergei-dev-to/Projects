from __future__ import annotations

import csv
import random
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class ShellPageRow:
    seed: int
    geometry: str
    L0: int
    warmup_depth: int
    cycle_depth: int
    L_before: int
    L_after: int
    rad_qubits: int
    shell_qubits: int
    remaining_qubits: int
    page_capacity: int
    s_rad: int
    old_new_mi: int


def gf2_rank(matrix: np.ndarray) -> int:
    a = np.array(matrix, dtype=np.uint8, copy=True)
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if a[row, col]:
                pivot = row
                break
        if pivot is None:
            continue
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        for row in range(rows):
            if row != rank and a[row, col]:
                a[row] ^= a[rank]
        rank += 1
        if rank == rows:
            break
    return rank


class StabilizerState:
    def __init__(self, n_qubits: int) -> None:
        self.n = n_qubits
        self.x = np.zeros((n_qubits, n_qubits), dtype=np.uint8)
        self.z = np.eye(n_qubits, dtype=np.uint8)

    def h(self, q: int) -> None:
        self.x[:, [q]], self.z[:, [q]] = self.z[:, [q]].copy(), self.x[:, [q]].copy()

    def s(self, q: int) -> None:
        self.z[:, q] ^= self.x[:, q]

    def cnot(self, control: int, target: int) -> None:
        self.x[:, target] ^= self.x[:, control]
        self.z[:, control] ^= self.z[:, target]

    def entropy(self, subset: set[int]) -> int:
        if not subset:
            return 0
        if len(subset) == self.n:
            return 0
        complement = [q for q in range(self.n) if q not in subset]
        restricted = np.concatenate(
            (self.x[:, complement], self.z[:, complement]), axis=1
        )
        stabilizers_inside_subset = self.n - gf2_rank(restricted)
        return len(subset) - stabilizers_inside_subset


def grid_positions(L0: int) -> dict[tuple[int, int], int]:
    return {(r, c): r * L0 + c for r in range(L0) for c in range(L0)}


def active_positions(L: int) -> list[tuple[int, int]]:
    return [(r, c) for r in range(L) for c in range(L)]


def shell_positions(L: int) -> list[tuple[int, int]]:
    return [(L - 1, c) for c in range(L)] + [(r, L - 1) for r in range(L - 1)]


def nearest_neighbor_edges(L: int, ids: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    edges: list[tuple[int, int]] = []
    for r in range(L):
        for c in range(L):
            if r + 1 < L:
                edges.append((ids[(r, c)], ids[(r + 1, c)]))
            if c + 1 < L:
                edges.append((ids[(r, c)], ids[(r, c + 1)]))
    return edges


def complete_graph_edges(L: int, ids: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    qubits = [ids[pos] for pos in active_positions(L)]
    return [(a, b) for i, a in enumerate(qubits) for b in qubits[i + 1 :]]


def expander_like_edges(
    L: int,
    ids: dict[tuple[int, int], int],
    degree: int,
    seed: int,
) -> list[tuple[int, int]]:
    """Sparse nonlocal graph built as a union of random matchings.

    This is not a proof-quality expander generator. It is a fixed sparse
    random-regular-ish connectivity pattern, enough to test whether nonlocal
    sparse scrambling can replace nearest-neighbor diffusion in the shell
    diagnostic.
    """

    qubits = [ids[pos] for pos in active_positions(L)]
    graph_rng = random.Random((seed + 1) * 1_000_003 + L * 9_176 + degree)
    edges: set[tuple[int, int]] = set()
    for _ in range(degree):
        shuffled = list(qubits)
        graph_rng.shuffle(shuffled)
        for i in range(0, len(shuffled) - 1, 2):
            a, b = shuffled[i], shuffled[i + 1]
            if a != b:
                edges.add((min(a, b), max(a, b)))
    return list(edges)


def build_edge_sets(
    L0: int,
    ids: dict[tuple[int, int], int],
    geometry: str,
    seed: int,
) -> dict[int, list[tuple[int, int]]]:
    edge_sets: dict[int, list[tuple[int, int]]] = {}
    for L in range(1, L0 + 1):
        if geometry == "grid":
            edge_sets[L] = nearest_neighbor_edges(L, ids)
        elif geometry == "complete":
            edge_sets[L] = complete_graph_edges(L, ids)
        elif geometry.startswith("expander"):
            suffix = geometry.removeprefix("expander")
            degree = int(suffix) if suffix else 4
            edge_sets[L] = expander_like_edges(L, ids, degree, seed)
        else:
            raise ValueError(f"unknown geometry: {geometry}")
    return edge_sets


def apply_random_layer(
    state: StabilizerState,
    L: int,
    ids: dict[tuple[int, int], int],
    edge_sets: dict[int, list[tuple[int, int]]],
    rng: random.Random,
) -> None:
    qubits = [ids[pos] for pos in active_positions(L)]
    for q in qubits:
        gate = rng.randrange(4)
        if gate == 1:
            state.h(q)
        elif gate == 2:
            state.s(q)
        elif gate == 3:
            state.h(q)
            state.s(q)

    edges = list(edge_sets[L])
    rng.shuffle(edges)
    used: set[int] = set()
    for a, b in edges:
        if a in used or b in used:
            continue
        if rng.random() < 0.5:
            state.cnot(a, b)
        else:
            state.cnot(b, a)
        used.add(a)
        used.add(b)


def scramble(
    state: StabilizerState,
    L: int,
    ids: dict[tuple[int, int], int],
    edge_sets: dict[int, list[tuple[int, int]]],
    rng: random.Random,
    depth: int,
) -> None:
    for _ in range(depth):
        apply_random_layer(state, L, ids, edge_sets, rng)


def run_shell_page_diagnostic(
    L0: int,
    geometry: str,
    warmup_depth: int,
    cycle_depth: int,
    seed: int = 12345,
) -> list[ShellPageRow]:
    rng = random.Random(seed)
    ids = grid_positions(L0)
    edge_sets = build_edge_sets(L0, ids, geometry, seed)
    state = StabilizerState(L0 * L0)
    radiation: set[int] = set()
    rows: list[ShellPageRow] = []

    scramble(state, L0, ids, edge_sets, rng, warmup_depth)

    for L in range(L0, 0, -1):
        scramble(state, L, ids, edge_sets, rng, cycle_depth)

        old_radiation = set(radiation)
        new_shell = {ids[pos] for pos in shell_positions(L)}
        radiation |= new_shell

        remaining = L * L - len(new_shell)
        s_old = state.entropy(old_radiation)
        s_new = state.entropy(new_shell)
        s_rad = state.entropy(radiation)
        old_new_mi = s_old + s_new - s_rad

        rows.append(
            ShellPageRow(
                seed=seed,
                geometry=geometry,
                L0=L0,
                warmup_depth=warmup_depth,
                cycle_depth=cycle_depth,
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


def write_rows(rows: list[ShellPageRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ShellPageRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("grid", 8, 0, 0),
        ("grid", 8, 16, 0),
        ("grid", 8, 16, 2),
        ("grid", 8, 16, 8),
        ("expander4", 8, 8, 1),
        ("expander4", 8, 8, 2),
        ("expander4", 8, 8, 4),
        ("expander8", 8, 8, 1),
        ("expander8", 8, 8, 2),
        ("complete", 8, 8, 1),
        ("complete", 8, 8, 4),
        ("grid", 12, 24, 12),
        ("expander4", 12, 12, 2),
        ("expander8", 12, 12, 2),
        ("complete", 12, 12, 2),
    ]

    seeds = list(range(10))
    for geometry, L0, warmup, cycle in cases:
        all_rows: list[ShellPageRow] = []
        errors: list[int] = []
        exact_count = 0
        first_mis: list[str] = []
        for seed in seeds:
            rows = run_shell_page_diagnostic(
                L0=L0,
                geometry=geometry,
                warmup_depth=warmup,
                cycle_depth=cycle,
                seed=seed,
            )
            all_rows.extend(rows)
            error = sum(abs(row.s_rad - row.page_capacity) for row in rows)
            errors.append(error)
            if error == 0:
                exact_count += 1
            first_mi = next((row for row in rows if row.old_new_mi > 0), None)
            if first_mi is not None:
                first_mis.append(f"{first_mi.L_before}->{first_mi.L_after}")
        out_path = out_dir / (
            f"stabilizer_shell_page_{geometry}_L{L0}_w{warmup}_c{cycle}.csv"
        )
        write_rows(all_rows, out_path)
        print(
            geometry,
            f"L0={L0}",
            f"warmup={warmup}",
            f"cycle={cycle}",
            f"mean |S-cap|={sum(errors) / len(errors):.2f}",
            f"max |S-cap|={max(errors)}",
            f"exact seeds={exact_count}/{len(seeds)}",
            "first MI modes=" + ",".join(sorted(set(first_mis))) if first_mis else "",
        )


if __name__ == "__main__":
    main()
