from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_hard_register_evaporator import evolve_axes, random_product_state_axes
from interacting_spin_hamiltonian_page import shell_qubits
from threshold_integrated_statevector_evaporator import (
    StateKey,
    emit_one_quantum,
    normalize_sparse,
    transferred_probabilities,
)


ATOMS = ("core", "acc", "transferred", "soft_labels", "hard", "bath")


@dataclass(frozen=True)
class ThresholdDensityRow:
    seed: int
    scrambler: str
    micro_emissions: int
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
    page_proxy: float
    none_gap_proxy: float


@dataclass(frozen=True)
class ThresholdDensitySummary:
    L0: int
    threshold: int
    warmup_time: float
    dt: float
    cases: int
    max_micro_emissions: int
    max_basis_terms: int
    status: str


def factors_from_key(key: StateKey) -> dict[str, object]:
    core, acc, transferred, soft_labels, hard_bits, bath_bits = key
    return {
        "core": core,
        "acc": acc,
        "transferred": transferred,
        "soft_labels": soft_labels,
        "hard": hard_bits,
        "bath": bath_bits,
    }


def key_for_atoms(factors: dict[str, object], atoms: tuple[str, ...]) -> tuple[object, ...]:
    return tuple(factors[atom] for atom in atoms)


def entropy_from_state(state: dict[StateKey, complex], keep: tuple[str, ...]) -> float:
    keep_set = set(keep)
    complement = tuple(atom for atom in ATOMS if atom not in keep_set)
    keep = tuple(atom for atom in ATOMS if atom in keep_set)
    if not keep or not complement:
        return 0.0

    factor_cache = {key: factors_from_key(key) for key in state}
    keep_keys = {key_for_atoms(factors, keep) for factors in factor_cache.values()}
    comp_keys = {key_for_atoms(factors, complement) for factors in factor_cache.values()}

    if len(keep_keys) <= len(comp_keys):
        row_atoms, col_atoms = keep, complement
    else:
        row_atoms, col_atoms = complement, keep

    row_index: dict[tuple[object, ...], int] = {}
    col_index: dict[tuple[object, ...], int] = {}
    entries: list[tuple[int, int, complex]] = []
    for key, amplitude in state.items():
        factors = factor_cache[key]
        row_key = key_for_atoms(factors, row_atoms)
        col_key = key_for_atoms(factors, col_atoms)
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
    state: dict[StateKey, complex],
    atoms_a: tuple[str, ...],
    atoms_b: tuple[str, ...],
) -> float:
    union = tuple(dict.fromkeys(atoms_a + atoms_b))
    return max(
        0.0,
        entropy_from_state(state, atoms_a)
        + entropy_from_state(state, atoms_b)
        - entropy_from_state(state, union),
    )


def build_initial_sparse(
    L0: int,
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> dict[StateKey, complex]:
    n_bits = L0 * L0
    initial = random_product_state_axes(n_bits, seed + 80_000)
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
    sparse = {
        (core_index, 0, 0, (0, 0, 0), 0, 0): complex(amplitude)
        for core_index, amplitude in enumerate(scrambled)
        if abs(amplitude) > 1e-14
    }
    return normalize_sparse(sparse)


def evolve_threshold_state(
    L0: int,
    threshold: int,
    micro_emissions: int,
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
    for emission_step in range(1, micro_emissions + 1):
        state = emit_one_quantum(
            state,
            emission_step=emission_step,
            threshold=threshold,
            n_bits=n_bits,
            shell_axes_by_stage=shell_axes_by_stage,
        )
    return state


def row_for_case(
    L0: int,
    threshold: int,
    micro_emissions: int,
    warmup_time: float,
    dt: float,
    seed: int,
    scrambler: str,
) -> ThresholdDensityRow:
    state = evolve_threshold_state(
        L0=L0,
        threshold=threshold,
        micro_emissions=micro_emissions,
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
    hard_target = micro_emissions * math.log(2.0)
    # A rough Page proxy for the soft record: its entropy should be nonzero and
    # bounded by the smaller of soft record entropy capacity and remaining core.
    page_proxy = min(s_soft, s_core_acc)
    return ThresholdDensityRow(
        seed=seed,
        scrambler=scrambler,
        micro_emissions=micro_emissions,
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
        page_proxy=page_proxy,
        none_gap_proxy=0.0,
    )


def run_threshold_density_scaling(
    L0: int = 3,
    threshold: int = 4,
    warmup_time: float = 8.0,
    dt: float = 0.2,
    micro_emission_values: tuple[int, ...] = (4, 5, 6),
    scramblers: tuple[str, ...] = ("margulis", "grid", "none"),
    seeds: tuple[int, ...] = (0, 1),
) -> tuple[list[ThresholdDensityRow], ThresholdDensitySummary]:
    rows: list[ThresholdDensityRow] = []
    for micro_emissions in micro_emission_values:
        for scrambler in scramblers:
            for seed in seeds:
                rows.append(
                    row_for_case(
                        L0=L0,
                        threshold=threshold,
                        micro_emissions=micro_emissions,
                        warmup_time=warmup_time,
                        dt=dt,
                        seed=seed,
                        scrambler=scrambler,
                    )
                )

    # Fill in a simple none-gap proxy: scrambled soft entropy minus the average
    # no-scrambling soft entropy at the same emission count and seed set.
    none_by_emissions: dict[int, float] = {}
    for micro_emissions in micro_emission_values:
        none_values = [
            row.s_soft
            for row in rows
            if row.micro_emissions == micro_emissions and row.scrambler == "none"
        ]
        none_by_emissions[micro_emissions] = sum(none_values) / len(none_values)
    rows = [
        ThresholdDensityRow(
            **{
                **row.__dict__,
                "none_gap_proxy": row.s_soft - none_by_emissions[row.micro_emissions],
            }
        )
        for row in rows
    ]
    summary = ThresholdDensitySummary(
        L0=L0,
        threshold=threshold,
        warmup_time=warmup_time,
        dt=dt,
        cases=len(rows),
        max_micro_emissions=max(micro_emission_values),
        max_basis_terms=max(row.basis_terms for row in rows),
        status=(
            "full reduced-density threshold scaling diagnostic over emission "
            "count, with scrambling controls"
        ),
    )
    return rows, summary


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
    rows, summary = run_threshold_density_scaling()
    write_dataclass_rows(rows, out_dir / "threshold_density_scaling_rows.csv")
    write_dataclass_rows([summary], out_dir / "threshold_density_scaling_summary.csv")
    for row in rows:
        print(
            f"emissions={row.micro_emissions}",
            f"scrambler={row.scrambler}",
            f"seed={row.seed}",
            f"terms={row.basis_terms}",
            f"<shells>={row.transferred_mean:.3f}",
            f"p_done={row.p_done:.3f}",
            f"S_soft={row.s_soft:.3f}",
            f"S_hard={row.s_hard:.3f}",
            f"S_rad={row.s_full_radiation:.3f}",
            f"Dhard={row.hard_entropy_error:.2e}",
            f"gap={row.none_gap_proxy:.3f}",
        )
    print(
        f"cases={summary.cases}",
        f"max_emissions={summary.max_micro_emissions}",
        f"max_terms={summary.max_basis_terms}",
    )


if __name__ == "__main__":
    main()
