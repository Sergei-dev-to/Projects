from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_hard_register_evaporator import evolve_axes, random_product_state_axes
from interacting_spin_hamiltonian_page import shell_qubits
from threshold_density_scaling import entropy_from_state, mutual_information
from threshold_integrated_statevector_evaporator import (
    StateKey,
    normalize_sparse,
    transferred_probabilities,
    transfer_next_shell,
)


@dataclass(frozen=True)
class FinalFloquetRow:
    seed: int
    scrambler: str
    threshold: int
    micro_emissions: int
    hard_prob_one: float
    basis_terms: int
    transferred_mean: float
    p_done: float
    s_soft: float
    s_hard: float
    s_bath: float
    s_visible: float
    s_full_radiation: float
    s_core_acc: float
    mi_soft_hard: float
    mi_soft_bath: float
    mi_hard_bath: float
    hard_entropy_target: float
    hard_entropy_error: float
    soft_minus_none: float
    score: float


@dataclass(frozen=True)
class FinalFloquetSummary:
    L0: int
    cases: int
    best_threshold: int
    best_micro_emissions: int
    best_hard_prob_one: float
    best_scrambled_mean_soft: float
    best_none_mean_soft: float
    best_soft_gap: float
    best_p_done_mean: float
    best_score: float
    max_basis_terms: int
    status: str


def hard_entropy_per_emission(p_one: float) -> float:
    probs = np.array([1.0 - p_one, p_one], dtype=float)
    probs = probs[probs > 1e-15]
    return float(-np.sum(probs * np.log(probs)))


def build_initial_sparse(
    L0: int,
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> dict[StateKey, complex]:
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
            (core_index, 0, 0, (0, 0, 0), 0, 0): complex(amplitude)
            for core_index, amplitude in enumerate(scrambled)
            if abs(amplitude) > 1e-14
        }
    )


def emit_weighted_quantum(
    state: dict[StateKey, complex],
    threshold: int,
    n_bits: int,
    shell_axes_by_stage: tuple[list[int], list[int], list[int]],
    p_one: float,
) -> dict[StateKey, complex]:
    next_state: dict[StateKey, complex] = {}
    for key, amplitude in state.items():
        core, acc, transferred, soft_labels, hard_bits, bath_bits = key
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
            if new_acc >= threshold and transferred < 3:
                new_acc -= threshold
                new_core, new_transferred, new_soft = transfer_next_shell(
                    new_core,
                    new_transferred,
                    new_soft,
                    n_bits,
                    shell_axes_by_stage,
                )
            new_key = (
                new_core,
                new_acc,
                new_transferred,
                new_soft,
                (hard_bits << 1) | hard_bit,
                (bath_bits << 1) | hard_bit,
            )
            next_state[new_key] = next_state.get(new_key, 0.0j) + amplitude * math.sqrt(
                probability
            )
    return normalize_sparse(next_state)


def evolve_candidate_state(
    L0: int,
    threshold: int,
    micro_emissions: int,
    hard_prob_one: float,
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> dict[StateKey, complex]:
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
    for _ in range(micro_emissions):
        state = emit_weighted_quantum(
            state=state,
            threshold=threshold,
            n_bits=n_bits,
            shell_axes_by_stage=shell_axes_by_stage,
            p_one=hard_prob_one,
        )
    return state


def row_for_case(
    L0: int,
    threshold: int,
    micro_emissions: int,
    hard_prob_one: float,
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> FinalFloquetRow:
    state = evolve_candidate_state(
        L0=L0,
        threshold=threshold,
        micro_emissions=micro_emissions,
        hard_prob_one=hard_prob_one,
        warmup_time=warmup_time,
        dt=dt,
        seed=seed,
        scrambler=scrambler,
    )
    probs = transferred_probabilities(state)
    transferred_mean = sum(count * prob for count, prob in probs.items())
    s_soft = entropy_from_state(state, ("transferred", "soft_labels"))
    s_hard = entropy_from_state(state, ("hard",))
    s_bath = entropy_from_state(state, ("bath",))
    s_visible = entropy_from_state(state, ("transferred", "soft_labels", "hard"))
    s_full_radiation = entropy_from_state(
        state, ("transferred", "soft_labels", "hard", "bath")
    )
    s_core_acc = entropy_from_state(state, ("core", "acc"))
    hard_target = micro_emissions * hard_entropy_per_emission(hard_prob_one)
    return FinalFloquetRow(
        seed=seed,
        scrambler=scrambler,
        threshold=threshold,
        micro_emissions=micro_emissions,
        hard_prob_one=hard_prob_one,
        basis_terms=len(state),
        transferred_mean=transferred_mean,
        p_done=probs[3],
        s_soft=s_soft,
        s_hard=s_hard,
        s_bath=s_bath,
        s_visible=s_visible,
        s_full_radiation=s_full_radiation,
        s_core_acc=s_core_acc,
        mi_soft_hard=mutual_information(
            state, ("transferred", "soft_labels"), ("hard",)
        ),
        mi_soft_bath=mutual_information(
            state, ("transferred", "soft_labels"), ("bath",)
        ),
        mi_hard_bath=mutual_information(state, ("hard",), ("bath",)),
        hard_entropy_target=hard_target,
        hard_entropy_error=abs(s_hard - hard_target),
        soft_minus_none=0.0,
        score=0.0,
    )


def score_group(rows: list[FinalFloquetRow]) -> tuple[float, float, float, float, float]:
    scrambled = [row for row in rows if row.scrambler in {"margulis", "grid"}]
    none = [row for row in rows if row.scrambler == "none"]
    scrambled_soft = sum(row.s_soft for row in scrambled) / len(scrambled)
    none_soft = sum(row.s_soft for row in none) / len(none)
    gap = scrambled_soft - none_soft
    p_done = sum(row.p_done for row in scrambled) / len(scrambled)
    hard_error = max(row.hard_entropy_error for row in rows)
    # Favor nontrivial but incomplete evaporation, large scrambling gap, and
    # exact hard thermality. This is a trajectory-readability score, not a
    # physical observable.
    completion_penalty = abs(p_done - 0.25)
    score = gap - completion_penalty - 10.0 * hard_error
    return score, scrambled_soft, none_soft, gap, p_done


def run_final_candidate_scan(
    L0: int = 3,
    warmup_time: float = 8.0,
    dt: float = 0.2,
    thresholds: tuple[int, ...] = (5,),
    micro_emission_values: tuple[int, ...] = (6, 7),
    hard_prob_values: tuple[float, ...] = (0.35, 0.5),
    scramblers: tuple[str, ...] = ("margulis", "grid", "none"),
    seeds: tuple[int, ...] = (0,),
) -> tuple[list[FinalFloquetRow], FinalFloquetSummary]:
    all_rows: list[FinalFloquetRow] = []
    best_summary_tuple: tuple[int, int, float, float, float, float, float, float] | None = None
    best_group_rows: list[FinalFloquetRow] = []

    for threshold in thresholds:
        for micro_emissions in micro_emission_values:
            for hard_prob_one in hard_prob_values:
                group_rows: list[FinalFloquetRow] = []
                for scrambler in scramblers:
                    for seed in seeds:
                        row = row_for_case(
                            L0=L0,
                            threshold=threshold,
                            micro_emissions=micro_emissions,
                            hard_prob_one=hard_prob_one,
                            warmup_time=warmup_time,
                            dt=dt,
                            seed=seed,
                            scrambler=scrambler,
                        )
                        group_rows.append(row)
                score, scrambled_soft, none_soft, gap, p_done = score_group(group_rows)
                none_soft_by_seed = {
                    row.seed: row.s_soft for row in group_rows if row.scrambler == "none"
                }
                scored_rows = [
                    FinalFloquetRow(
                        **{
                            **row.__dict__,
                            "soft_minus_none": row.s_soft
                            - none_soft_by_seed.get(row.seed, none_soft),
                            "score": score,
                        }
                    )
                    for row in group_rows
                ]
                all_rows.extend(scored_rows)
                if best_summary_tuple is None or score > best_summary_tuple[3]:
                    best_summary_tuple = (
                        threshold,
                        micro_emissions,
                        hard_prob_one,
                        score,
                        scrambled_soft,
                        none_soft,
                        gap,
                        p_done,
                    )
                    best_group_rows = scored_rows

    assert best_summary_tuple is not None
    best_threshold, best_emissions, best_p, best_score, best_scrambled, best_none, best_gap, best_done = (
        best_summary_tuple
    )
    summary = FinalFloquetSummary(
        L0=L0,
        cases=len(all_rows),
        best_threshold=best_threshold,
        best_micro_emissions=best_emissions,
        best_hard_prob_one=best_p,
        best_scrambled_mean_soft=best_scrambled,
        best_none_mean_soft=best_none,
        best_soft_gap=best_gap,
        best_p_done_mean=best_done,
        best_score=best_score,
        max_basis_terms=max(row.basis_terms for row in all_rows),
        status=(
            "final-candidate full-density Floquet scan with weighted hard "
            "emissions, threshold shrinkage, thermality, and controls"
        ),
    )
    return all_rows, summary


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
    rows, summary = run_final_candidate_scan()
    write_dataclass_rows(rows, out_dir / "final_floquet_candidate_scan_rows.csv")
    write_dataclass_rows([summary], out_dir / "final_floquet_candidate_scan_summary.csv")
    print(
        f"cases={summary.cases}",
        f"best_threshold={summary.best_threshold}",
        f"best_emissions={summary.best_micro_emissions}",
        f"best_p1={summary.best_hard_prob_one:.2f}",
        f"scrambled_soft={summary.best_scrambled_mean_soft:.3f}",
        f"none_soft={summary.best_none_mean_soft:.3f}",
        f"gap={summary.best_soft_gap:.3f}",
        f"p_done={summary.best_p_done_mean:.3f}",
        f"score={summary.best_score:.3f}",
        f"max_terms={summary.max_basis_terms}",
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
                f"p_done={row.p_done:.3f}",
                f"S_soft={row.s_soft:.3f}",
                f"S_hard={row.s_hard:.3f}",
                f"target={row.hard_entropy_target:.3f}",
                f"Dhard={row.hard_entropy_error:.2e}",
                f"gap={row.soft_minus_none:.3f}",
            )


if __name__ == "__main__":
    main()
