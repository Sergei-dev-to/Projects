from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_hard_register_evaporator import evolve_axes, random_product_state_axes
from final_floquet_candidate_scan import hard_entropy_per_emission
from interacting_spin_hamiltonian_page import shell_qubits
from microcanonical_emission_weights import row_for_L as power_row_for_L
from microscopic_boundary_emission import golden_rule_hard_distribution
from threshold_integrated_statevector_evaporator import (
    normalize_sparse,
    transfer_next_shell,
    transferred_probabilities,
)


SoftEvent: TypeAlias = tuple[int, int]
StateKeyTR: TypeAlias = tuple[
    int,
    int,
    int,
    tuple[int, int, int],
    int,
    int,
    tuple[SoftEvent, ...],
]


@dataclass(frozen=True)
class FusedFloquetRow:
    seed: int
    scrambler: str
    rate_L0: float
    threshold: int
    micro_emissions: int
    split_step: int
    hard_prob_one: float
    hard_prob_one_last: float
    mean_omega_total: float
    mean_omega_first: float
    mean_omega_last: float
    first_omega_over_T: float
    last_omega_over_T: float
    basis_terms: int
    transferred_mean: float
    p_done: float
    s_hard: float
    s_soft: float
    s_visible: float
    s_full_radiation: float
    s_core_acc: float
    mi_soft_hard: float
    mi_hard_bath: float
    mi_old_new_hard: float
    mi_old_new_visible: float
    mi_old_new_full: float
    hard_entropy_target: float
    hard_entropy_error: float
    soft_minus_none: float
    old_new_full_minus_none: float
    score: float


@dataclass(frozen=True)
class FusedFloquetSummary:
    L0: int
    rate_L0: float
    cases: int
    best_threshold: int
    best_micro_emissions: int
    best_hard_prob_one: float
    best_hard_prob_one_last: float
    best_mean_omega_total: float
    best_scrambled_mean_soft: float
    best_none_mean_soft: float
    best_soft_gap: float
    best_scrambled_old_new_full: float
    best_none_old_new_full: float
    best_old_new_full_gap: float
    best_p_done_mean: float
    best_score: float
    max_basis_terms: int
    status: str


def build_initial_sparse(
    L0: int,
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> dict[StateKeyTR, complex]:
    n_bits = L0 * L0
    initial = random_product_state_axes(n_bits, seed + 90_000)
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
            (core_index, 0, 0, (0, 0, 0), 0, 0, ()): complex(amplitude)
            for core_index, amplitude in enumerate(scrambled)
            if abs(amplitude) > 1e-14
        }
    )


def emit_weighted_quantum_time_resolved(
    state: dict[StateKeyTR, complex],
    threshold: int,
    n_bits: int,
    shell_axes_by_stage: tuple[list[int], list[int], list[int]],
    p_one: float,
) -> dict[StateKeyTR, complex]:
    next_state: dict[StateKeyTR, complex] = {}
    for key, amplitude in state.items():
        core, acc, transferred, soft_labels, hard_bits, bath_bits, soft_history = key
        for hard_bit, energy, probability in (
            (0, 1, 1.0 - p_one),
            (1, 2, p_one),
        ):
            if probability <= 0.0:
                continue
            new_acc = acc + energy
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
                (hard_bits << 1) | hard_bit,
                (bath_bits << 1) | hard_bit,
                soft_history + (soft_event,),
            )
            next_state[new_key] = next_state.get(new_key, 0.0j) + amplitude * math.sqrt(
                probability
            )
    return normalize_sparse(next_state)


def hard_entropy_for_schedule(prob_schedule: tuple[float, ...]) -> float:
    return sum(hard_entropy_per_emission(prob) for prob in prob_schedule)


def golden_hard_schedule(
    L0: float,
    micro_emissions: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
) -> tuple[tuple[float, ...], tuple[float, ...], tuple[float, ...]]:
    mass = 4.0 * sigma * L0
    p_ones: list[float] = []
    mean_omegas: list[float] = []
    temperatures: list[float] = []
    for _event in range(micro_emissions):
        probs, mean_omega, temp = golden_rule_hard_distribution(
            mass,
            q,
            sigma,
            bath_dim,
            x_edges,
            n_grid,
        )
        p_ones.append(float(probs[1]))
        mean_omegas.append(mean_omega)
        temperatures.append(temp)
        mass = max(1e-12, mass - mean_omega)
    return tuple(p_ones), tuple(mean_omegas), tuple(temperatures)


def split_bits(value: int, total_bits: int, split_step: int) -> tuple[int, int]:
    new_bits_count = total_bits - split_step
    old_bits = value >> new_bits_count
    new_bits = value & ((1 << new_bits_count) - 1)
    return old_bits, new_bits


def factors_from_key(
    key: StateKeyTR,
    micro_emissions: int,
    split_step: int,
) -> dict[str, object]:
    core, acc, transferred, soft_labels, hard_bits, bath_bits, soft_history = key
    hard_old, hard_new = split_bits(hard_bits, micro_emissions, split_step)
    bath_old, bath_new = split_bits(bath_bits, micro_emissions, split_step)
    soft_old = soft_history[:split_step]
    soft_new = soft_history[split_step:]
    return {
        "core_acc": (core, acc),
        "hard_old": hard_old,
        "hard_new": hard_new,
        "bath_old": bath_old,
        "bath_new": bath_new,
        "soft_old": soft_old,
        "soft_new": soft_new,
        "hard": hard_bits,
        "bath": bath_bits,
        "soft": (transferred, soft_labels, soft_history),
        "visible": (transferred, soft_labels, soft_history, hard_bits),
        "full_radiation": (transferred, soft_labels, soft_history, hard_bits, bath_bits),
        "visible_old": (hard_old, soft_old),
        "visible_new": (hard_new, soft_new),
        "full_old": (hard_old, bath_old, soft_old),
        "full_new": (hard_new, bath_new, soft_new),
    }


def expand_atoms(atoms: tuple[str, ...]) -> tuple[str, ...]:
    groups = {
        "core_acc": ("core_acc",),
        "hard": ("hard_old", "hard_new"),
        "bath": ("bath_old", "bath_new"),
        "soft": ("soft_old", "soft_new"),
        "visible": ("hard_old", "hard_new", "soft_old", "soft_new"),
        "full_radiation": (
            "hard_old",
            "hard_new",
            "bath_old",
            "bath_new",
            "soft_old",
            "soft_new",
        ),
        "hard_old": ("hard_old",),
        "hard_new": ("hard_new",),
        "visible_old": ("hard_old", "soft_old"),
        "visible_new": ("hard_new", "soft_new"),
        "full_old": ("hard_old", "bath_old", "soft_old"),
        "full_new": ("hard_new", "bath_new", "soft_new"),
    }
    expanded: list[str] = []
    for atom in atoms:
        for primitive in groups[atom]:
            if primitive not in expanded:
                expanded.append(primitive)
    return tuple(expanded)


def entropy_from_factors(
    state: dict[StateKeyTR, complex],
    keep: tuple[str, ...],
    micro_emissions: int,
    split_step: int,
) -> float:
    factor_cache = {
        key: factors_from_key(key, micro_emissions, split_step) for key in state
    }
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


def mutual_information_from_factors(
    state: dict[StateKeyTR, complex],
    atoms_a: tuple[str, ...],
    atoms_b: tuple[str, ...],
    micro_emissions: int,
    split_step: int,
) -> float:
    union = tuple(dict.fromkeys(atoms_a + atoms_b))
    return max(
        0.0,
        entropy_from_factors(state, atoms_a, micro_emissions, split_step)
        + entropy_from_factors(state, atoms_b, micro_emissions, split_step)
        - entropy_from_factors(state, union, micro_emissions, split_step),
    )


def evolve_candidate_state(
    L0: int,
    threshold: int,
    micro_emissions: int,
    hard_prob_schedule: tuple[float, ...],
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> dict[StateKeyTR, complex]:
    if len(hard_prob_schedule) != micro_emissions:
        raise ValueError("hard probability schedule must match micro_emissions")
    n_bits = L0 * L0
    shell_axes_by_stage = (
        sorted(shell_qubits(L0, 3)),
        sorted(shell_qubits(L0, 2)),
        sorted(shell_qubits(L0, 1)),
    )
    state = build_initial_sparse(
        L0=L0,
        warmup_time=warmup_time,
        dt=dt,
        seed=seed,
        scrambler=scrambler,
    )
    for hard_prob_one in hard_prob_schedule:
        state = emit_weighted_quantum_time_resolved(
            state=state,
            threshold=threshold,
            n_bits=n_bits,
            shell_axes_by_stage=shell_axes_by_stage,
            p_one=hard_prob_one,
        )
    return state


def row_for_case(
    L0: int,
    rate_L0: float,
    threshold: int,
    micro_emissions: int,
    hard_prob_schedule: tuple[float, ...],
    mean_omega_schedule: tuple[float, ...],
    temperature_schedule: tuple[float, ...],
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> FusedFloquetRow:
    split_step = micro_emissions // 2
    state = evolve_candidate_state(
        L0=L0,
        threshold=threshold,
        micro_emissions=micro_emissions,
        hard_prob_schedule=hard_prob_schedule,
        warmup_time=warmup_time,
        dt=dt,
        seed=seed,
        scrambler=scrambler,
    )
    old_style_state = {
        (core, acc, transferred, soft_labels, hard_bits, bath_bits): amplitude
        for (
            core,
            acc,
            transferred,
            soft_labels,
            hard_bits,
            bath_bits,
            _soft_history,
        ), amplitude in state.items()
    }
    probs = transferred_probabilities(old_style_state)
    transferred_mean = sum(count * prob for count, prob in probs.items())
    hard_target = hard_entropy_for_schedule(hard_prob_schedule)
    s_hard = entropy_from_factors(state, ("hard",), micro_emissions, split_step)
    return FusedFloquetRow(
        seed=seed,
        scrambler=scrambler,
        rate_L0=rate_L0,
        threshold=threshold,
        micro_emissions=micro_emissions,
        split_step=split_step,
        hard_prob_one=hard_prob_schedule[0],
        hard_prob_one_last=hard_prob_schedule[-1],
        mean_omega_total=sum(mean_omega_schedule),
        mean_omega_first=mean_omega_schedule[0],
        mean_omega_last=mean_omega_schedule[-1],
        first_omega_over_T=mean_omega_schedule[0] / temperature_schedule[0],
        last_omega_over_T=mean_omega_schedule[-1] / temperature_schedule[-1],
        basis_terms=len(state),
        transferred_mean=transferred_mean,
        p_done=probs[3],
        s_hard=s_hard,
        s_soft=entropy_from_factors(state, ("soft",), micro_emissions, split_step),
        s_visible=entropy_from_factors(
            state, ("visible",), micro_emissions, split_step
        ),
        s_full_radiation=entropy_from_factors(
            state, ("full_radiation",), micro_emissions, split_step
        ),
        s_core_acc=entropy_from_factors(
            state, ("core_acc",), micro_emissions, split_step
        ),
        mi_soft_hard=mutual_information_from_factors(
            state, ("soft",), ("hard",), micro_emissions, split_step
        ),
        mi_hard_bath=mutual_information_from_factors(
            state, ("hard",), ("bath",), micro_emissions, split_step
        ),
        mi_old_new_hard=mutual_information_from_factors(
            state, ("hard_old",), ("hard_new",), micro_emissions, split_step
        ),
        mi_old_new_visible=mutual_information_from_factors(
            state, ("visible_old",), ("visible_new",), micro_emissions, split_step
        ),
        mi_old_new_full=mutual_information_from_factors(
            state, ("full_old",), ("full_new",), micro_emissions, split_step
        ),
        hard_entropy_target=hard_target,
        hard_entropy_error=abs(s_hard - hard_target),
        soft_minus_none=0.0,
        old_new_full_minus_none=0.0,
        score=0.0,
    )


def score_group(rows: list[FusedFloquetRow]) -> tuple[float, float, float, float, float, float, float]:
    scrambled = [row for row in rows if row.scrambler in {"margulis", "grid"}]
    none = [row for row in rows if row.scrambler == "none"]
    scrambled_soft = sum(row.s_soft for row in scrambled) / len(scrambled)
    none_soft = sum(row.s_soft for row in none) / len(none)
    soft_gap = scrambled_soft - none_soft
    scrambled_old_new = sum(row.mi_old_new_full for row in scrambled) / len(scrambled)
    none_old_new = sum(row.mi_old_new_full for row in none) / len(none)
    old_new_gap = scrambled_old_new - none_old_new
    p_done = sum(row.p_done for row in scrambled) / len(scrambled)
    hard_error = max(row.hard_entropy_error for row in rows)
    completion_penalty = abs(p_done - 0.25)
    score = soft_gap + old_new_gap - completion_penalty - 10.0 * hard_error
    return score, scrambled_soft, none_soft, soft_gap, scrambled_old_new, none_old_new, old_new_gap


def run_fused_scan(
    L0: int = 3,
    rate_L0: float = 20.0,
    warmup_time: float = 8.0,
    dt: float = 0.2,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    x_edges: tuple[float, ...] = (0.0, 2.0, 8.0),
    n_grid: int = 1001,
    thresholds: tuple[int, ...] = (5,),
    micro_emission_values: tuple[int, ...] = (6,),
    scramblers: tuple[str, ...] = ("margulis", "grid", "none"),
    seeds: tuple[int, ...] = (0,),
) -> tuple[list[FusedFloquetRow], FusedFloquetSummary]:
    all_rows: list[FusedFloquetRow] = []
    best_tuple: tuple[
        int,
        int,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
        float,
    ] | None = None

    for threshold in thresholds:
        for micro_emissions in micro_emission_values:
            hard_prob_schedule, mean_omega_schedule, temperature_schedule = (
                golden_hard_schedule(
                    L0=rate_L0,
                    micro_emissions=micro_emissions,
                    q=q,
                    sigma=sigma,
                    bath_dim=bath_dim,
                    x_edges=np.array(x_edges, dtype=float),
                    n_grid=n_grid,
                )
            )
            group_rows = [
                row_for_case(
                    L0=L0,
                    rate_L0=rate_L0,
                    threshold=threshold,
                    micro_emissions=micro_emissions,
                    hard_prob_schedule=hard_prob_schedule,
                    mean_omega_schedule=mean_omega_schedule,
                    temperature_schedule=temperature_schedule,
                    warmup_time=warmup_time,
                    dt=dt,
                    seed=seed,
                    scrambler=scrambler,
                )
                for scrambler in scramblers
                for seed in seeds
            ]
            (
                score,
                scrambled_soft,
                none_soft,
                soft_gap,
                scrambled_old_new,
                none_old_new,
                old_new_gap,
            ) = score_group(group_rows)
            scrambled_rows = [
                row for row in group_rows if row.scrambler in {"margulis", "grid"}
            ]
            p_done = sum(row.p_done for row in scrambled_rows) / len(scrambled_rows)
            none_soft_by_seed = {
                row.seed: row.s_soft for row in group_rows if row.scrambler == "none"
            }
            none_old_new_by_seed = {
                row.seed: row.mi_old_new_full
                for row in group_rows
                if row.scrambler == "none"
            }
            scored_rows = [
                FusedFloquetRow(
                    **{
                        **row.__dict__,
                        "soft_minus_none": row.s_soft
                        - none_soft_by_seed.get(row.seed, none_soft),
                        "old_new_full_minus_none": row.mi_old_new_full
                        - none_old_new_by_seed.get(row.seed, none_old_new),
                        "score": score,
                    }
                )
                for row in group_rows
            ]
            all_rows.extend(scored_rows)
            if best_tuple is None or score > best_tuple[3]:
                best_tuple = (
                    threshold,
                    micro_emissions,
                    hard_prob_schedule[0],
                    score,
                    scrambled_soft,
                    none_soft,
                    soft_gap,
                    scrambled_old_new,
                    none_old_new,
                    old_new_gap,
                    p_done,
                    hard_prob_schedule[-1],
                    sum(mean_omega_schedule),
                )

    assert best_tuple is not None
    (
        best_threshold,
        best_emissions,
        best_p,
        best_score,
        best_scrambled_soft,
        best_none_soft,
        best_soft_gap,
        best_scrambled_old_new,
        best_none_old_new,
        best_old_new_gap,
        best_done,
        best_p_last,
        best_mean_omega_total,
    ) = best_tuple
    summary = FusedFloquetSummary(
        L0=L0,
        rate_L0=rate_L0,
        cases=len(all_rows),
        best_threshold=best_threshold,
        best_micro_emissions=best_emissions,
        best_hard_prob_one=best_p,
        best_hard_prob_one_last=best_p_last,
        best_mean_omega_total=best_mean_omega_total,
        best_scrambled_mean_soft=best_scrambled_soft,
        best_none_mean_soft=best_none_soft,
        best_soft_gap=best_soft_gap,
        best_scrambled_old_new_full=best_scrambled_old_new,
        best_none_old_new_full=best_none_old_new,
        best_old_new_full_gap=best_old_new_gap,
        best_p_done_mean=best_done,
        best_score=best_score,
        max_basis_terms=max(row.basis_terms for row in all_rows),
        status=(
            "time-resolved fused Floquet scan with golden-rule weighted emissions, "
            "threshold shrinkage, hard thermality, and old/new radiation MI"
        ),
    )
    return all_rows, summary


def write_power_schedule(
    path: Path,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    max_L: int = 40,
    x_max: float = 8.0,
    n_grid: int = 4001,
) -> list[dict[str, float | int]]:
    rows = [
        power_row_for_L(
            L=L,
            q=q,
            sigma=sigma,
            bath_dim=bath_dim,
            x_max=x_max,
            n_grid=n_grid,
        )
        for L in range(2, max_L + 1)
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return rows


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
    rows, summary = run_fused_scan()
    write_dataclass_rows(rows, out_dir / "fused_floquet_time_resolved_rows.csv")
    write_dataclass_rows([summary], out_dir / "fused_floquet_time_resolved_summary.csv")
    power_rows = write_power_schedule(
        out_dir / "fused_floquet_weighted_power_schedule.csv"
    )
    print(
        f"cases={summary.cases}",
        f"best_threshold={summary.best_threshold}",
        f"best_emissions={summary.best_micro_emissions}",
        f"p1={summary.best_hard_prob_one:.3f}->{summary.best_hard_prob_one_last:.3f}",
        f"mean_omega_total={summary.best_mean_omega_total:.3f}",
        f"soft_gap={summary.best_soft_gap:.3f}",
        f"old_new_gap={summary.best_old_new_full_gap:.3f}",
        f"p_done={summary.best_p_done_mean:.3f}",
        f"score={summary.best_score:.3f}",
        f"max_terms={summary.max_basis_terms}",
        )
    first_power = power_rows[1]
    last_power = power_rows[-1]
    print(
        "weighted_power:",
        f"L=3 M^2P={float(first_power['mass_squared_power_exact']):.3f}",
        f"L={int(last_power['L'])} M^2P={float(last_power['mass_squared_power_exact']):.3f}",
        f"ratio={float(last_power['mass_squared_power_exact']) / float(first_power['mass_squared_power_exact']):.3f}",
    )
    for row in rows:
        if (
            row.threshold == summary.best_threshold
            and row.micro_emissions == summary.best_micro_emissions
            and abs(row.hard_prob_one - summary.best_hard_prob_one) < 1e-12
        ):
            print(
                f"  {row.scrambler}",
                f"terms={row.basis_terms}",
                f"<shells>={row.transferred_mean:.3f}",
                f"S_soft={row.s_soft:.3f}",
                f"S_hard={row.s_hard:.3f}",
                f"MI_old_new_full={row.mi_old_new_full:.3f}",
                f"gap_soft={row.soft_minus_none:.3f}",
                f"gap_old_new={row.old_new_full_minus_none:.3f}",
            )


if __name__ == "__main__":
    main()
