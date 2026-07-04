from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from global_fixed_floquet_page import margulis_gabber_galil_edges
from stabilizer_shell_page_diagnostic import grid_positions, shell_positions


@dataclass(frozen=True)
class MajoranaPageRow:
    seed: int
    geometry: str
    L0: int
    coupling: str
    warmup_time: float
    cycle_time: float
    L_before: int
    L_after: int
    rad_modes: int
    shell_modes: int
    remaining_modes: int
    page_capacity: float
    s_rad: float
    old_new_mi: float
    entropy_deficit: float


def active_modes(L: int, ids: dict[tuple[int, int], int]) -> list[int]:
    return [ids[(r, c)] for r in range(L) for c in range(L)]


def mode_majoranas(mode: int) -> tuple[int, int]:
    return 2 * mode, 2 * mode + 1


def initial_vacuum_covariance(n_modes: int) -> np.ndarray:
    gamma = np.zeros((2 * n_modes, 2 * n_modes), dtype=float)
    for mode in range(n_modes):
        a, b = mode_majoranas(mode)
        gamma[a, b] = 1.0
        gamma[b, a] = -1.0
    return gamma


def add_antisymmetric(a_matrix: np.ndarray, i: int, j: int, value: float) -> None:
    a_matrix[i, j] += value
    a_matrix[j, i] -= value


def build_majorana_hamiltonian(
    n_modes: int,
    edges: list[tuple[int, int]],
    seed: int,
    coupling: str,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    a_matrix = np.zeros((2 * n_modes, 2 * n_modes), dtype=float)

    for mode in range(n_modes):
        m0, m1 = mode_majoranas(mode)
        add_antisymmetric(a_matrix, m0, m1, 0.3 * rng.normal())

    for i, j in edges:
        i0, i1 = mode_majoranas(i)
        j0, j1 = mode_majoranas(j)

        if coupling == "hopping":
            value = rng.normal() / math.sqrt(max(1, len(edges) / n_modes))
            add_antisymmetric(a_matrix, i0, j1, value)
            add_antisymmetric(a_matrix, i1, j0, -value)
        elif coupling == "generic":
            scale = 1.0 / math.sqrt(max(1, len(edges) / n_modes))
            for left in (i0, i1):
                for right in (j0, j1):
                    add_antisymmetric(a_matrix, left, right, scale * rng.normal())
        else:
            raise ValueError(f"unknown coupling: {coupling}")

    return a_matrix


def evolve_active(
    gamma: np.ndarray,
    a_matrix: np.ndarray,
    active: list[int],
    time: float,
) -> np.ndarray:
    if time == 0.0 or not active:
        return gamma
    majoranas: list[int] = []
    for mode in active:
        majoranas.extend(mode_majoranas(mode))
    idx = np.array(majoranas, dtype=int)
    sub_a = a_matrix[np.ix_(idx, idx)]
    o_matrix = expm(sub_a * time)
    all_idx = np.arange(gamma.shape[0])
    evolved = gamma.copy()
    evolved[np.ix_(idx, all_idx)] = o_matrix @ gamma[np.ix_(idx, all_idx)]
    evolved[np.ix_(all_idx, idx)] = evolved[np.ix_(all_idx, idx)] @ o_matrix.T
    return 0.5 * (evolved - evolved.T)


def gaussian_entropy(gamma: np.ndarray, modes: set[int]) -> float:
    if not modes:
        return 0.0
    majoranas: list[int] = []
    for mode in sorted(modes):
        majoranas.extend(mode_majoranas(mode))
    sub = gamma[np.ix_(majoranas, majoranas)]
    eigvals = np.linalg.eigvalsh(1j * sub)
    positive = [min(1.0, max(0.0, float(v.real))) for v in eigvals if v.real > 1e-9]
    entropy = 0.0
    for nu in positive:
        p_plus = (1.0 + nu) / 2.0
        p_minus = (1.0 - nu) / 2.0
        if p_plus > 1e-12:
            entropy -= p_plus * math.log(p_plus)
        if p_minus > 1e-12:
            entropy -= p_minus * math.log(p_minus)
    return entropy


def run_majorana_page_diagnostic(
    L0: int,
    geometry: str,
    coupling: str,
    warmup_time: float,
    cycle_time: float,
    seed: int,
) -> list[MajoranaPageRow]:
    ids = grid_positions(L0)
    if geometry == "margulis":
        edges = margulis_gabber_galil_edges(L0, ids)
    else:
        raise ValueError(f"unknown geometry: {geometry}")

    n_modes = L0 * L0
    a_matrix = build_majorana_hamiltonian(n_modes, edges, seed, coupling)
    gamma = initial_vacuum_covariance(n_modes)
    radiation: set[int] = set()
    rows: list[MajoranaPageRow] = []

    gamma = evolve_active(gamma, a_matrix, active_modes(L0, ids), warmup_time)

    for L in range(L0, 0, -1):
        gamma = evolve_active(gamma, a_matrix, active_modes(L, ids), cycle_time)

        old_radiation = set(radiation)
        new_shell = {ids[pos] for pos in shell_positions(L)}
        radiation |= new_shell

        remaining = L * L - len(new_shell)
        capacity = min(len(radiation), remaining) * math.log(2.0)
        s_old = gaussian_entropy(gamma, old_radiation)
        s_new = gaussian_entropy(gamma, new_shell)
        s_rad = gaussian_entropy(gamma, radiation)
        old_new_mi = max(0.0, s_old + s_new - s_rad)

        rows.append(
            MajoranaPageRow(
                seed=seed,
                geometry=geometry,
                L0=L0,
                coupling=coupling,
                warmup_time=warmup_time,
                cycle_time=cycle_time,
                L_before=L,
                L_after=L - 1,
                rad_modes=len(radiation),
                shell_modes=len(new_shell),
                remaining_modes=remaining,
                page_capacity=capacity,
                s_rad=s_rad,
                old_new_mi=old_new_mi,
                entropy_deficit=capacity - s_rad,
            )
        )
    return rows


def write_rows(rows: list[MajoranaPageRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(MajoranaPageRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("margulis", "hopping", 8, 4.0, 1.0),
        ("margulis", "hopping", 8, 8.0, 2.0),
        ("margulis", "generic", 8, 4.0, 1.0),
        ("margulis", "generic", 8, 8.0, 2.0),
        ("margulis", "generic", 12, 4.0, 1.0),
    ]
    seeds = list(range(5))

    for geometry, coupling, L0, warmup, cycle in cases:
        all_rows: list[MajoranaPageRow] = []
        deficits: list[float] = []
        first_mis: list[str] = []
        for seed in seeds:
            rows = run_majorana_page_diagnostic(
                L0=L0,
                geometry=geometry,
                coupling=coupling,
                warmup_time=warmup,
                cycle_time=cycle,
                seed=seed,
            )
            all_rows.extend(rows)
            deficits.append(sum(max(0.0, row.entropy_deficit) for row in rows))
            first_mi = next((row for row in rows if row.old_new_mi > 1e-6), None)
            if first_mi is not None:
                first_mis.append(f"{first_mi.L_before}->{first_mi.L_after}")

        out_path = out_dir / (
            "majorana_hamiltonian_page_"
            f"{geometry}_{coupling}_L{L0}_warm{warmup:g}_cyc{cycle:g}.csv"
        )
        write_rows(all_rows, out_path)
        print(
            geometry,
            coupling,
            f"L0={L0}",
            f"warmup={warmup:g}",
            f"cycle={cycle:g}",
            f"mean total deficit={sum(deficits) / len(deficits):.3f}",
            f"max total deficit={max(deficits):.3f}",
            "first MI modes=" + ",".join(sorted(set(first_mis))) if first_mis else "",
        )


if __name__ == "__main__":
    main()
