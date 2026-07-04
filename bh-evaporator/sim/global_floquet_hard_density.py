from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np

from global_floquet_register_rule import box2d_bath_modes, run_global_sequence
from global_floquet_statevector_lift import entropy_from_probs, random_state
from multishell_shrinkage_floquet import shell_ranges


@dataclass(frozen=True)
class HardDensitySummary:
    L0: int
    q: int
    shell_gap: int
    accumulator_modulus: int
    sequence_length: int
    max_momentum: int
    seed: int
    input_dimension: int
    hard_dimension: int
    hidden_dimension: int
    hard_entropy: float
    target_entropy: float
    trace_distance_to_target: float
    offdiag_frobenius_norm: float
    purity: float
    max_probability_error: float
    status: str


@dataclass(frozen=True)
class HardProbabilityRow:
    hard_sequence: str
    probability: float
    target_probability: float
    probability_error: float


def hard_id_from_bins(hard_bins: tuple[int, ...]) -> int:
    hard_id = 0
    for hard_bin in hard_bins:
        hard_id *= 2
        hard_id += hard_bin - 1
    return hard_id


def hard_sequence_from_id(hard_id: int, sequence_length: int) -> tuple[int, ...]:
    bins = []
    for _ in range(sequence_length):
        bins.append((hard_id % 2) + 1)
        hard_id //= 2
    return tuple(reversed(bins))


def run_hard_density_check(
    L0: int = 3,
    q: int = 2,
    shell_gap: int = 8,
    accumulator_modulus: int = 8,
    sequence_length: int = 3,
    max_momentum: int = 1,
    seed: int = 4321,
) -> tuple[list[HardProbabilityRow], HardDensitySummary]:
    bath_modes = box2d_bath_modes(max_momentum=max_momentum)
    hard_dimension = 2**sequence_length
    hidden_index: dict[tuple[object, ...], int] = {}
    output_pairs: list[tuple[int, int]] = []

    for accumulator in range(accumulator_modulus):
        for shell_labels_raw in product(*shell_ranges(L0, q)):
            shell_labels = tuple(shell_labels_raw)
            for bath_sequence_raw in product(
                range(len(bath_modes)), repeat=sequence_length
            ):
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
                    accumulator=accumulator,
                    shell_labels=shell_labels,
                    bath_sequence=bath_sequence,
                    bath_modes=bath_modes,
                    shell_gap=shell_gap,
                    accumulator_modulus=accumulator_modulus,
                )
                hard_id = hard_id_from_bins(hard_bins)
                # Hidden records are everything except the visible coarse hard
                # bins. The bath microstate remains hidden, so it can decohere
                # hard bins that arose from distinct microscopic bath modes.
                hidden_key = (
                    L_final,
                    acc_final,
                    labels_final,
                    bath_sequence,
                    emitted_units,
                    shrink_records,
                )
                if hidden_key not in hidden_index:
                    hidden_index[hidden_key] = len(hidden_index)
                output_pairs.append((hard_id, hidden_index[hidden_key]))

    input_dimension = len(output_pairs)
    hidden_dimension = len(hidden_index)
    state = random_state(input_dimension, seed=seed)
    psi = np.zeros((hard_dimension, hidden_dimension), dtype=np.complex128)
    for input_axis, (hard_id, hidden_id) in enumerate(output_pairs):
        psi[hard_id, hidden_id] += state[input_axis]

    rho_hard = psi @ psi.conj().T
    rho_hard = 0.5 * (rho_hard + rho_hard.conj().T)
    probs = np.real(np.diag(rho_hard))
    probs = probs / probs.sum()

    # With max_momentum=1 there are four axis and four diagonal modes, so each
    # coarse hard bin has probability 1/2 per emission.
    target = np.ones(hard_dimension, dtype=float) / hard_dimension
    eigvals = np.linalg.eigvalsh(rho_hard - np.diag(target))
    trace_distance = float(0.5 * np.sum(np.abs(eigvals)))
    offdiag = rho_hard - np.diag(np.diag(rho_hard))
    offdiag_norm = float(np.linalg.norm(offdiag))
    purity = float(np.real(np.trace(rho_hard @ rho_hard)))

    rows = [
        HardProbabilityRow(
            hard_sequence=",".join(map(str, hard_sequence_from_id(i, sequence_length))),
            probability=float(probs[i]),
            target_probability=float(target[i]),
            probability_error=float(probs[i] - target[i]),
        )
        for i in range(hard_dimension)
    ]
    summary = HardDensitySummary(
        L0=L0,
        q=q,
        shell_gap=shell_gap,
        accumulator_modulus=accumulator_modulus,
        sequence_length=sequence_length,
        max_momentum=max_momentum,
        seed=seed,
        input_dimension=input_dimension,
        hard_dimension=hard_dimension,
        hidden_dimension=hidden_dimension,
        hard_entropy=entropy_from_probs(probs),
        target_entropy=float(math.log(hard_dimension)),
        trace_distance_to_target=trace_distance,
        offdiag_frobenius_norm=offdiag_norm,
        purity=purity,
        max_probability_error=float(np.max(np.abs(probs - target))),
        status=(
            "reduced hard density matrix after tracing hidden bath/shrink "
            "records in the global state-vector lift"
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
    rows, summary = run_hard_density_check()
    write_dataclass_rows(rows, out_dir / "global_floquet_hard_density_rows.csv")
    write_dataclass_rows([summary], out_dir / "global_floquet_hard_density_summary.csv")
    print(
        f"input_dim={summary.input_dimension}",
        f"hard_dim={summary.hard_dimension}",
        f"hidden_dim={summary.hidden_dimension}",
        f"S_hard={summary.hard_entropy:.6f}",
        f"S_target={summary.target_entropy:.6f}",
        f"trace_distance={summary.trace_distance_to_target:.3e}",
        f"offdiag={summary.offdiag_frobenius_norm:.3e}",
        f"purity={summary.purity:.6f}",
    )


if __name__ == "__main__":
    main()
