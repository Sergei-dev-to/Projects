from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from audited_repeated_interaction_evaporator import deterministic_parameters
from explicit_hard_register_evaporator import evolve_axes, random_product_state_axes
from interacting_spin_hamiltonian_page import shell_qubits


@dataclass(frozen=True)
class ThresholdIntegratedRow:
    seed: int
    scrambler: str
    emission_step: int
    basis_terms: int
    transferred_mean: float
    p_transferred_0: float
    p_transferred_1: float
    p_transferred_2: float
    p_transferred_3: float
    s_core_acc: float
    s_soft: float
    s_hard: float
    s_full_radiation: float
    s_visible_radiation: float
    mi_soft_hard: float
    mi_soft_bath: float
    mi_hard_bath: float


@dataclass(frozen=True)
class ThresholdIntegratedSummary:
    seed: int
    scrambler: str
    L0: int
    threshold: int
    micro_emissions: int
    warmup_time: float
    dt: float
    initial_core_terms: int
    final_basis_terms: int
    final_transferred_mean: float
    final_complete_evaporation_probability: float
    final_s_core_acc: float
    final_s_soft: float
    final_s_hard: float
    final_s_full_radiation: float
    final_s_visible_radiation: float
    final_mi_hard_bath: float
    status: str


StateKey = tuple[int, int, int, tuple[int, int, int], int, int]


def bits_of(index: int, n_bits: int) -> list[int]:
    return [(index >> (n_bits - 1 - axis)) & 1 for axis in range(n_bits)]


def index_of(bits: list[int]) -> int:
    value = 0
    for bit in bits:
        value = (value << 1) | int(bit)
    return value


def extract_and_zero(core_index: int, n_bits: int, axes: list[int]) -> tuple[int, int]:
    bits = bits_of(core_index, n_bits)
    label = 0
    for axis in axes:
        label = (label << 1) | bits[axis]
        bits[axis] = 0
    return index_of(bits), label


def entropy_density(rho: np.ndarray) -> float:
    rho = 0.5 * (rho + rho.conj().T)
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-13]
    return float(-np.sum(evals * np.log(evals)))


def factors_from_key(key: StateKey) -> dict[str, object]:
    core, acc, transferred, soft_labels, hard_bits, bath_bits = key
    return {
        "core": core,
        "acc": acc,
        "transferred": transferred,
        "soft": (transferred, soft_labels),
        "hard": hard_bits,
        "bath": bath_bits,
        "radiation": (transferred, soft_labels, hard_bits, bath_bits),
        "visible": (transferred, soft_labels, hard_bits),
        "core_acc": (core, acc),
    }


def entropy_group(state: dict[StateKey, complex], keep: tuple[str, ...]) -> float:
    # This threshold diagnostic tracks branch/record entropy rather than full
    # reduced-density entropy. The previous integrated_statevector_evaporator
    # script performs the actual density-matrix check at smaller branch count.
    probs: dict[tuple[object, ...], float] = {}
    for key, amplitude in state.items():
        factors = factors_from_key(key)
        selected_key = tuple(factors[name] for name in keep)
        probs[selected_key] = probs.get(selected_key, 0.0) + abs(amplitude) ** 2
    values = np.array(list(probs.values()), dtype=float)
    values = values[values > 1e-15]
    return float(-np.sum(values * np.log(values)))


def mutual_information(
    state: dict[StateKey, complex],
    group_a: tuple[str, ...],
    group_b: tuple[str, ...],
) -> float:
    return max(
        0.0,
        entropy_group(state, group_a)
        + entropy_group(state, group_b)
        - entropy_group(state, group_a + group_b),
    )


def normalize_sparse(state: dict[StateKey, complex]) -> dict[StateKey, complex]:
    norm = math.sqrt(sum(abs(amplitude) ** 2 for amplitude in state.values()))
    return {key: amplitude / norm for key, amplitude in state.items()}


def transfer_next_shell(
    core_index: int,
    transferred: int,
    soft_labels: tuple[int, int, int],
    n_bits: int,
    shell_axes_by_stage: tuple[list[int], list[int], list[int]],
) -> tuple[int, int, tuple[int, int, int]]:
    if transferred >= 3:
        return core_index, transferred, soft_labels
    new_core, label = extract_and_zero(
        core_index, n_bits, shell_axes_by_stage[transferred]
    )
    labels = list(soft_labels)
    labels[transferred] = label + 1
    return new_core, transferred + 1, tuple(labels)  # type: ignore[return-value]


def emit_one_quantum(
    state: dict[StateKey, complex],
    emission_step: int,
    threshold: int,
    n_bits: int,
    shell_axes_by_stage: tuple[list[int], list[int], list[int]],
) -> dict[StateKey, complex]:
    next_state: dict[StateKey, complex] = {}
    for key, amplitude in state.items():
        core, acc, transferred, soft_labels, hard_bits, bath_bits = key
        for hard_bit, energy in ((0, 1), (1, 2)):
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
            next_state[new_key] = next_state.get(new_key, 0.0j) + amplitude / math.sqrt(2.0)
    return normalize_sparse(next_state)


def transferred_probabilities(state: dict[StateKey, complex]) -> dict[int, float]:
    probs = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
    for key, amplitude in state.items():
        probs[key[2]] += abs(amplitude) ** 2
    return probs


def mean_transferred(state: dict[StateKey, complex]) -> float:
    probs = transferred_probabilities(state)
    return sum(count * prob for count, prob in probs.items())


def row_for_state(
    state: dict[StateKey, complex],
    seed: int,
    scrambler: str,
    emission_step: int,
) -> ThresholdIntegratedRow:
    probs = transferred_probabilities(state)
    return ThresholdIntegratedRow(
        seed=seed,
        scrambler=scrambler,
        emission_step=emission_step,
        basis_terms=len(state),
        transferred_mean=mean_transferred(state),
        p_transferred_0=probs[0],
        p_transferred_1=probs[1],
        p_transferred_2=probs[2],
        p_transferred_3=probs[3],
        s_core_acc=entropy_group(state, ("core_acc",)),
        s_soft=entropy_group(state, ("soft",)),
        s_hard=entropy_group(state, ("hard",)),
        s_full_radiation=entropy_group(state, ("radiation",)),
        s_visible_radiation=entropy_group(state, ("visible",)),
        mi_soft_hard=mutual_information(state, ("soft",), ("hard",)),
        mi_soft_bath=mutual_information(state, ("soft",), ("bath",)),
        mi_hard_bath=mutual_information(state, ("hard",), ("bath",)),
    )


def run_threshold_integrated(
    L0: int = 3,
    threshold: int = 4,
    micro_emissions: int = 8,
    warmup_time: float = 8.0,
    dt: float = 0.2,
    seed: int = 0,
    scrambler: str = "margulis",
) -> tuple[list[ThresholdIntegratedRow], ThresholdIntegratedSummary]:
    if L0 != 3:
        raise ValueError("this sparse threshold diagnostic is specialized to L0=3")
    n_bits = L0 * L0
    initial = random_product_state_axes(n_bits, seed + 70_000)
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
    state: dict[StateKey, complex] = {
        core_index: complex(amplitude)
        for core_index, amplitude in enumerate(scrambled)
        if abs(amplitude) > 1e-14
    }
    sparse: dict[StateKey, complex] = {
        (core_index, 0, 0, (0, 0, 0), 0, 0): amplitude
        for core_index, amplitude in state.items()
    }
    sparse = normalize_sparse(sparse)
    initial_terms = len(sparse)
    shell_axes_by_stage = (
        sorted(shell_qubits(L0, 3)),
        sorted(shell_qubits(L0, 2)),
        sorted(shell_qubits(L0, 1)),
    )

    rows: list[ThresholdIntegratedRow] = []
    for emission_step in range(1, micro_emissions + 1):
        sparse = emit_one_quantum(
            sparse,
            emission_step=emission_step,
            threshold=threshold,
            n_bits=n_bits,
            shell_axes_by_stage=shell_axes_by_stage,
        )
        rows.append(row_for_state(sparse, seed, scrambler, emission_step))

    final = rows[-1]
    summary = ThresholdIntegratedSummary(
        seed=seed,
        scrambler=scrambler,
        L0=L0,
        threshold=threshold,
        micro_emissions=micro_emissions,
        warmup_time=warmup_time,
        dt=dt,
        initial_core_terms=initial_terms,
        final_basis_terms=final.basis_terms,
        final_transferred_mean=final.transferred_mean,
        final_complete_evaporation_probability=final.p_transferred_3,
        final_s_core_acc=final.s_core_acc,
        final_s_soft=final.s_soft,
        final_s_hard=final.s_hard,
        final_s_full_radiation=final.s_full_radiation,
        final_s_visible_radiation=final.s_visible_radiation,
        final_mi_hard_bath=final.mi_hard_bath,
        status=(
            "sparse state-vector evaporator with microscopic hard emissions, "
            "energy accumulation, and threshold-triggered shell transfer"
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
    summaries: list[ThresholdIntegratedSummary] = []
    for scrambler in ("margulis", "grid", "none"):
        for seed in range(3):
            rows, summary = run_threshold_integrated(seed=seed, scrambler=scrambler)
            write_dataclass_rows(
                rows,
                out_dir
                / f"threshold_integrated_statevector_{scrambler}_seed{seed}.csv",
            )
            summaries.append(summary)
            print(
                f"scrambler={scrambler}",
                f"seed={seed}",
                f"terms={summary.final_basis_terms}",
                f"<transferred>={summary.final_transferred_mean:.3f}",
                f"p_done={summary.final_complete_evaporation_probability:.3f}",
                f"S_soft={summary.final_s_soft:.3f}",
                f"S_hard={summary.final_s_hard:.3f}",
                f"S_full_rad={summary.final_s_full_radiation:.3f}",
                f"S_vis_rad={summary.final_s_visible_radiation:.3f}",
                f"I_hb={summary.final_mi_hard_bath:.3f}",
            )
    write_dataclass_rows(
        summaries,
        out_dir / "threshold_integrated_statevector_summary.csv",
    )


if __name__ == "__main__":
    main()
