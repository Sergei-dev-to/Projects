from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np

from global_floquet_register_rule import box2d_bath_modes, run_global_sequence
from multishell_shrinkage_floquet import shell_dim


@dataclass(frozen=True)
class ReferenceFlowSummary:
    L0: int
    q: int
    shell_gap: int
    accumulator_initial: int
    sequence_length: int
    bath_mode_count: int
    reference_dimension: int
    basis_terms: int
    shrink_probability: float
    reference_entropy: float
    hard_entropy: float
    soft_entropy: float
    core_entropy: float
    radiation_entropy: float
    mutual_info_ref_hard: float
    mutual_info_ref_soft: float
    mutual_info_ref_radiation: float
    mutual_info_ref_core: float
    mutual_info_hard_soft: float
    status: str


def entropy_density(rho: np.ndarray) -> float:
    rho = 0.5 * (rho + rho.conj().T)
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-13]
    return float(-np.sum(evals * np.log(evals)))


def hard_id_from_bins(hard_bins: tuple[int, ...]) -> int:
    hard_id = 0
    for hard_bin in hard_bins:
        hard_id *= 2
        hard_id += hard_bin - 1
    return hard_id


def reduced_density(
    records: list[tuple[complex, dict[str, int]]],
    keep: tuple[str, ...],
) -> np.ndarray:
    selected_index: dict[tuple[int, ...], int] = {}
    hidden_index: dict[tuple[tuple[str, int], ...], int] = {}
    entries: list[tuple[int, int, complex]] = []

    for amplitude, factors in records:
        selected_key = tuple(factors[name] for name in keep)
        hidden_key = tuple(
            sorted((name, value) for name, value in factors.items() if name not in keep)
        )
        if selected_key not in selected_index:
            selected_index[selected_key] = len(selected_index)
        if hidden_key not in hidden_index:
            hidden_index[hidden_key] = len(hidden_index)
        entries.append((selected_index[selected_key], hidden_index[hidden_key], amplitude))

    psi = np.zeros((len(selected_index), len(hidden_index)), dtype=np.complex128)
    for selected_id, hidden_id, amplitude in entries:
        psi[selected_id, hidden_id] += amplitude
    return psi @ psi.conj().T


def mutual_information(
    records: list[tuple[complex, dict[str, int]]],
    group_a: tuple[str, ...],
    group_b: tuple[str, ...],
) -> float:
    s_a = entropy_density(reduced_density(records, group_a))
    s_b = entropy_density(reduced_density(records, group_b))
    s_ab = entropy_density(reduced_density(records, group_a + group_b))
    return max(0.0, s_a + s_b - s_ab)


def run_reference_flow_check(
    L0: int = 2,
    q: int = 2,
    shell_gap: int = 4,
    accumulator_initial: int = 0,
    sequence_length: int = 3,
    max_momentum: int = 1,
) -> ReferenceFlowSummary:
    if L0 != 2:
        raise ValueError("this tiny reference-flow diagnostic is specialized to L0=2")
    bath_modes = box2d_bath_modes(max_momentum=max_momentum)
    reference_dimension = shell_dim(2, q)
    bath_sequences = list(product(range(len(bath_modes)), repeat=sequence_length))
    amplitude = 1.0 / math.sqrt(reference_dimension * len(bath_sequences))
    records: list[tuple[complex, dict[str, int]]] = []
    shrink_weight = 0.0

    for shell_label in range(reference_dimension):
        shell_labels = (0, shell_label)
        for bath_sequence_raw in bath_sequences:
            bath_sequence = tuple(bath_sequence_raw)
            (
                L_final,
                acc_final,
                labels_final,
                shrink_records,
                hard_bins,
                emitted_units,
            ) = run_global_sequence(
                L0=L0,
                accumulator=accumulator_initial,
                shell_labels=shell_labels,
                bath_sequence=bath_sequence,
                bath_modes=bath_modes,
                shell_gap=shell_gap,
                accumulator_modulus=shell_gap,
            )
            hard_id = hard_id_from_bins(hard_bins)
            if shrink_records:
                # For L0=2 there is at most one possible shell shrink.
                soft_id = shrink_records[0][1] + 1
                core_id = 0
                shrink_flag = 1
                shrink_weight += abs(amplitude) ** 2
            else:
                soft_id = 0
                core_id = labels_final[1] + 1
                shrink_flag = 0
            factors = {
                "ref": shell_label,
                "hard": hard_id,
                "soft": soft_id,
                "core": core_id,
                "bath": int(
                    sum(
                        mode_id * (len(bath_modes) ** offset)
                        for offset, mode_id in enumerate(bath_sequence)
                    )
                ),
                "acc": acc_final,
                "L": L_final,
                "shrink_flag": shrink_flag,
                "emitted": int(
                    sum(
                        emitted * (3**offset)
                        for offset, emitted in enumerate(emitted_units)
                    )
                ),
            }
            records.append((complex(amplitude), factors))

    s_ref = entropy_density(reduced_density(records, ("ref",)))
    s_hard = entropy_density(reduced_density(records, ("hard",)))
    s_soft = entropy_density(reduced_density(records, ("soft",)))
    s_core = entropy_density(reduced_density(records, ("core",)))
    s_rad = entropy_density(reduced_density(records, ("hard", "soft")))

    return ReferenceFlowSummary(
        L0=L0,
        q=q,
        shell_gap=shell_gap,
        accumulator_initial=accumulator_initial,
        sequence_length=sequence_length,
        bath_mode_count=len(bath_modes),
        reference_dimension=reference_dimension,
        basis_terms=len(records),
        shrink_probability=shrink_weight,
        reference_entropy=s_ref,
        hard_entropy=s_hard,
        soft_entropy=s_soft,
        core_entropy=s_core,
        radiation_entropy=s_rad,
        mutual_info_ref_hard=mutual_information(records, ("ref",), ("hard",)),
        mutual_info_ref_soft=mutual_information(records, ("ref",), ("soft",)),
        mutual_info_ref_radiation=mutual_information(
            records, ("ref",), ("hard", "soft")
        ),
        mutual_info_ref_core=mutual_information(records, ("ref",), ("core",)),
        mutual_info_hard_soft=mutual_information(records, ("hard",), ("soft",)),
        status=(
            "reference entangled with the L=2 shell label; hard bins are "
            "coarse thermal radiation, soft shrink records carry expelled "
            "shell information when shrinkage occurs"
        ),
    )


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
    summary = run_reference_flow_check()
    write_dataclass_rows([summary], out_dir / "global_floquet_reference_flow_summary.csv")
    print(
        f"terms={summary.basis_terms}",
        f"p_shrink={summary.shrink_probability:.6f}",
        f"S_ref={summary.reference_entropy:.6f}",
        f"I_ref_hard={summary.mutual_info_ref_hard:.6f}",
        f"I_ref_soft={summary.mutual_info_ref_soft:.6f}",
        f"I_ref_rad={summary.mutual_info_ref_radiation:.6f}",
        f"I_ref_core={summary.mutual_info_ref_core:.6f}",
        f"I_hard_soft={summary.mutual_info_hard_soft:.6f}",
    )


if __name__ == "__main__":
    main()
