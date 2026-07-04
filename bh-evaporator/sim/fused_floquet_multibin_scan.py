from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import TypeAlias

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_hard_register_evaporator import evolve_axes, random_product_state_axes
from interacting_spin_hamiltonian_page import shell_qubits
from microscopic_boundary_emission import beta_of_mass, entropy_of_mass
from threshold_integrated_statevector_evaporator import (
    normalize_sparse,
    transfer_next_shell,
    transferred_probabilities,
)


SoftEvent: TypeAlias = tuple[int, int]
StateKeyMB: TypeAlias = tuple[
    int,
    int,
    int,
    tuple[int, int, int],
    tuple[int, ...],
    tuple[int, ...],
    tuple[SoftEvent, ...],
]


@dataclass(frozen=True)
class MultiBinRow:
    d_hard: int
    seed: int
    scrambler: str
    threshold: int
    micro_emissions: int
    basis_terms: int
    transferred_mean: float
    p_done: float
    s_hard: float
    s_soft: float
    s_full_radiation: float
    s_core_acc: float
    mi_old_new_full: float
    hard_entropy_target: float
    hard_entropy_error: float
    soft_minus_none: float
    old_new_minus_none: float


@dataclass(frozen=True)
class MultiBinSummary:
    d_hard: int
    cases: int
    scrambled_soft_mean: float
    none_soft_mean: float
    soft_gap_mean: float
    scrambled_old_new_mean: float
    none_old_new_mean: float
    old_new_gap_mean: float
    hard_entropy_error_max: float
    transferred_mean_scrambled: float
    max_basis_terms: int


def golden_multibin_distribution(
    mass: float,
    q: int,
    sigma: float,
    bath_dim: int,
    d_hard: int,
    x_max: float,
    n_grid: int,
) -> tuple[tuple[float, ...], float, float]:
    beta = beta_of_mass(mass, q, sigma)
    s0 = entropy_of_mass(mass, q, sigma)
    x_edges = np.linspace(0.0, x_max, d_hard + 1)
    weights: list[float] = []
    energy_weights: list[float] = []
    for x0, x1 in zip(x_edges[:-1], x_edges[1:]):
        capped_x1 = min(float(x1), beta * mass)
        if capped_x1 <= float(x0):
            weights.append(0.0)
            energy_weights.append(0.0)
            continue
        xs = np.linspace(float(x0), capped_x1, n_grid)
        omega = xs / beta
        delta_s = np.array([entropy_of_mass(mass - w, q, sigma) - s0 for w in omega])
        integrand = (omega ** max(bath_dim - 1, 0)) * np.exp(delta_s)
        weights.append(float(np.trapezoid(integrand, omega)))
        energy_weights.append(float(np.trapezoid(omega * integrand, omega)))
    probs = np.array(weights, dtype=float)
    probs = probs / np.sum(probs)
    mean_omega = float(np.sum(energy_weights) / np.sum(weights))
    return tuple(float(p) for p in probs), mean_omega, 1.0 / beta


def golden_multibin_schedule(
    rate_L0: float,
    micro_emissions: int,
    d_hard: int,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    x_max: float = 8.0,
    n_grid: int = 1001,
) -> tuple[tuple[tuple[float, ...], ...], tuple[float, ...], tuple[float, ...]]:
    mass = 4.0 * sigma * rate_L0
    schedules: list[tuple[float, ...]] = []
    means: list[float] = []
    temps: list[float] = []
    for _ in range(micro_emissions):
        probs, mean_omega, temp = golden_multibin_distribution(
            mass, q, sigma, bath_dim, d_hard, x_max, n_grid
        )
        schedules.append(probs)
        means.append(mean_omega)
        temps.append(temp)
        mass = max(1e-12, mass - mean_omega)
    return tuple(schedules), tuple(means), tuple(temps)


def build_initial_sparse(
    L0: int,
    seed: int,
    scrambler: str,
    warmup_time: float = 8.0,
    dt: float = 0.2,
) -> dict[StateKeyMB, complex]:
    n_bits = L0 * L0
    initial = random_product_state_axes(n_bits, seed + 120_000)
    fields, couplings = deterministic_parameters(L0, scrambler)
    scrambled = evolve_axes(
        initial,
        [2] * n_bits,
        active=set(range(n_bits)),
        fields=fields,
        couplings=couplings,
        time=warmup_time,
        dt=dt,
    )
    return normalize_sparse(
        {
            (core_index, 0, 0, (0, 0, 0), (), (), ()): complex(amplitude)
            for core_index, amplitude in enumerate(scrambled)
            if abs(amplitude) > 1e-14
        }
    )


def emit_multibin(
    state: dict[StateKeyMB, complex],
    threshold: int,
    n_bits: int,
    shell_axes_by_stage: tuple[list[int], list[int], list[int]],
    probs: tuple[float, ...],
) -> dict[StateKeyMB, complex]:
    next_state: dict[StateKeyMB, complex] = {}
    for key, amplitude in state.items():
        core, acc, transferred, soft_labels, hard_history, bath_history, soft_history = key
        for hard_label, probability in enumerate(probs):
            if probability <= 0.0:
                continue
            new_acc = acc + hard_label + 1
            new_core = core
            new_transferred = transferred
            new_soft = soft_labels
            soft_event: SoftEvent = (0, 0)
            if new_acc >= threshold and transferred < 3:
                new_acc -= threshold
                old_transferred = transferred
                new_core, new_transferred, new_soft = transfer_next_shell(
                    new_core,
                    new_transferred,
                    new_soft,
                    n_bits,
                    shell_axes_by_stage,
                )
                soft_event = (old_transferred + 1, new_soft[old_transferred])
            new_key = (
                new_core,
                new_acc,
                new_transferred,
                new_soft,
                hard_history + (hard_label,),
                bath_history + (hard_label,),
                soft_history + (soft_event,),
            )
            next_state[new_key] = next_state.get(new_key, 0.0j) + amplitude * math.sqrt(
                probability
            )
    return normalize_sparse(next_state)


def factors_from_key(key: StateKeyMB, split_step: int) -> dict[str, object]:
    core, acc, transferred, soft_labels, hard_history, bath_history, soft_history = key
    return {
        "core_acc": (core, acc),
        "hard_old": hard_history[:split_step],
        "hard_new": hard_history[split_step:],
        "bath_old": bath_history[:split_step],
        "bath_new": bath_history[split_step:],
        "soft_old": soft_history[:split_step],
        "soft_new": soft_history[split_step:],
        "soft": (transferred, soft_labels, soft_history),
    }


def expand_atoms(atoms: tuple[str, ...]) -> tuple[str, ...]:
    groups = {
        "core_acc": ("core_acc",),
        "hard": ("hard_old", "hard_new"),
        "soft": ("soft_old", "soft_new"),
        "full_radiation": (
            "hard_old",
            "hard_new",
            "bath_old",
            "bath_new",
            "soft_old",
            "soft_new",
        ),
        "full_old": ("hard_old", "bath_old", "soft_old"),
        "full_new": ("hard_new", "bath_new", "soft_new"),
    }
    expanded: list[str] = []
    for atom in atoms:
        for primitive in groups[atom]:
            if primitive not in expanded:
                expanded.append(primitive)
    return tuple(expanded)


def entropy_from_state(
    state: dict[StateKeyMB, complex],
    keep: tuple[str, ...],
    split_step: int,
) -> float:
    all_atoms = (
        "core_acc",
        "hard_old",
        "hard_new",
        "bath_old",
        "bath_new",
        "soft_old",
        "soft_new",
    )
    keep = expand_atoms(keep)
    keep_set = set(keep)
    complement = tuple(atom for atom in all_atoms if atom not in keep_set)
    keep = tuple(atom for atom in all_atoms if atom in keep_set)
    if not keep or not complement:
        return 0.0
    factor_cache = {key: factors_from_key(key, split_step) for key in state}
    keep_keys = {
        tuple(factors[atom] for atom in keep) for factors in factor_cache.values()
    }
    comp_keys = {
        tuple(factors[atom] for atom in complement)
        for factors in factor_cache.values()
    }
    if len(keep_keys) <= len(comp_keys):
        row_atoms, col_atoms = keep, complement
    else:
        row_atoms, col_atoms = complement, keep
    row_index: dict[tuple[object, ...], int] = {}
    col_index: dict[tuple[object, ...], int] = {}
    entries: list[tuple[int, int, complex]] = []
    for key, amplitude in state.items():
        factors = factor_cache[key]
        row_key = tuple(factors[atom] for atom in row_atoms)
        col_key = tuple(factors[atom] for atom in col_atoms)
        if row_key not in row_index:
            row_index[row_key] = len(row_index)
        if col_key not in col_index:
            col_index[col_key] = len(col_index)
        entries.append((row_index[row_key], col_index[col_key], amplitude))
    psi = np.zeros((len(row_index), len(col_index)), dtype=np.complex128)
    for row, col, amplitude in entries:
        psi[row, col] += amplitude
    rho = psi @ psi.conj().T
    rho = 0.5 * (rho + rho.conj().T)
    eigvals = np.linalg.eigvalsh(rho)
    eigvals = eigvals[eigvals > 1e-13]
    return float(-np.sum(eigvals * np.log(eigvals)))


def mutual_information(
    state: dict[StateKeyMB, complex],
    atoms_a: tuple[str, ...],
    atoms_b: tuple[str, ...],
    split_step: int,
) -> float:
    union = tuple(dict.fromkeys(atoms_a + atoms_b))
    return max(
        0.0,
        entropy_from_state(state, atoms_a, split_step)
        + entropy_from_state(state, atoms_b, split_step)
        - entropy_from_state(state, union, split_step),
    )


def hard_entropy_target(prob_schedule: tuple[tuple[float, ...], ...]) -> float:
    total = 0.0
    for probs in prob_schedule:
        arr = np.array(probs, dtype=float)
        arr = arr[arr > 1e-15]
        total += float(-np.sum(arr * np.log(arr)))
    return total


def run_case(
    d_hard: int,
    seed: int,
    scrambler: str,
    L0: int = 3,
    rate_L0: float = 20.0,
    threshold: int = 5,
    micro_emissions: int = 4,
) -> MultiBinRow:
    n_bits = L0 * L0
    split_step = micro_emissions // 2
    shell_axes_by_stage = (
        sorted(shell_qubits(L0, 3)),
        sorted(shell_qubits(L0, 2)),
        sorted(shell_qubits(L0, 1)),
    )
    prob_schedule, _means, _temps = golden_multibin_schedule(
        rate_L0=rate_L0,
        micro_emissions=micro_emissions,
        d_hard=d_hard,
    )
    state = build_initial_sparse(L0, seed, scrambler)
    for probs in prob_schedule:
        state = emit_multibin(state, threshold, n_bits, shell_axes_by_stage, probs)
    old_style_state = {
        (core, acc, transferred, soft_labels, 0, 0): amplitude
        for (
            core,
            acc,
            transferred,
            soft_labels,
            _hard_history,
            _bath_history,
            _soft_history,
        ), amplitude in state.items()
    }
    transferred_probs = transferred_probabilities(old_style_state)
    transferred_mean = sum(count * prob for count, prob in transferred_probs.items())
    s_hard = entropy_from_state(state, ("hard",), split_step)
    target = hard_entropy_target(prob_schedule)
    return MultiBinRow(
        d_hard=d_hard,
        seed=seed,
        scrambler=scrambler,
        threshold=threshold,
        micro_emissions=micro_emissions,
        basis_terms=len(state),
        transferred_mean=transferred_mean,
        p_done=transferred_probs[3],
        s_hard=s_hard,
        s_soft=entropy_from_state(state, ("soft",), split_step),
        s_full_radiation=entropy_from_state(state, ("full_radiation",), split_step),
        s_core_acc=entropy_from_state(state, ("core_acc",), split_step),
        mi_old_new_full=mutual_information(state, ("full_old",), ("full_new",), split_step),
        hard_entropy_target=target,
        hard_entropy_error=abs(s_hard - target),
        soft_minus_none=0.0,
        old_new_minus_none=0.0,
    )


def summarize(rows: list[MultiBinRow]) -> list[MultiBinSummary]:
    out: list[MultiBinSummary] = []
    for d_hard in sorted({row.d_hard for row in rows}):
        group = [row for row in rows if row.d_hard == d_hard]
        scrambled = [row for row in group if row.scrambler in {"margulis", "grid"}]
        none = [row for row in group if row.scrambler == "none"]
        none_soft = {row.seed: row.s_soft for row in none}
        none_old_new = {row.seed: row.mi_old_new_full for row in none}
        soft_gaps = [
            row.s_soft - none_soft[row.seed]
            for row in scrambled
            if row.seed in none_soft
        ]
        old_new_gaps = [
            row.mi_old_new_full - none_old_new[row.seed]
            for row in scrambled
            if row.seed in none_old_new
        ]
        out.append(
            MultiBinSummary(
                d_hard=d_hard,
                cases=len(group),
                scrambled_soft_mean=mean(row.s_soft for row in scrambled),
                none_soft_mean=mean(row.s_soft for row in none),
                soft_gap_mean=mean(soft_gaps),
                scrambled_old_new_mean=mean(row.mi_old_new_full for row in scrambled),
                none_old_new_mean=mean(row.mi_old_new_full for row in none),
                old_new_gap_mean=mean(old_new_gaps),
                hard_entropy_error_max=max(row.hard_entropy_error for row in group),
                transferred_mean_scrambled=mean(row.transferred_mean for row in scrambled),
                max_basis_terms=max(row.basis_terms for row in group),
            )
        )
    return out


def write_dataclass_rows(rows: list[object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].__dataclass_fields__),  # type: ignore[attr-defined]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    rows: list[MultiBinRow] = []
    for d_hard in (2, 3, 4):
        for scrambler in ("margulis", "grid", "none"):
            for seed in (0, 1):
                rows.append(run_case(d_hard=d_hard, scrambler=scrambler, seed=seed))

    none_soft_by_key = {
        (row.d_hard, row.seed): row.s_soft for row in rows if row.scrambler == "none"
    }
    none_old_by_key = {
        (row.d_hard, row.seed): row.mi_old_new_full
        for row in rows
        if row.scrambler == "none"
    }
    rows = [
        MultiBinRow(
            **{
                **row.__dict__,
                "soft_minus_none": row.s_soft
                - none_soft_by_key.get((row.d_hard, row.seed), row.s_soft),
                "old_new_minus_none": row.mi_old_new_full
                - none_old_by_key.get((row.d_hard, row.seed), row.mi_old_new_full),
            }
        )
        for row in rows
    ]
    summaries = summarize(rows)
    out_dir = Path(__file__).resolve().parent / "data"
    write_dataclass_rows(rows, out_dir / "fused_floquet_multibin_rows.csv")
    write_dataclass_rows(summaries, out_dir / "fused_floquet_multibin_summary.csv")
    print("d_hard  soft_gap  old_new_gap  hard_err  <shells>  max_terms")
    for row in summaries:
        print(
            f"{row.d_hard:6d} "
            f"{row.soft_gap_mean:8.3f} "
            f"{row.old_new_gap_mean:11.3f} "
            f"{row.hard_entropy_error_max:9.1e} "
            f"{row.transferred_mean_scrambled:8.3f} "
            f"{row.max_basis_terms:9d}"
        )


if __name__ == "__main__":
    main()
