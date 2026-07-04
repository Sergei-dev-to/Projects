from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import numpy as np

from global_floquet_register_rule import (
    box2d_bath_modes,
    full_output_key,
    no_bath_microstate_key,
    no_shrink_record_key,
    run_global_sequence,
)
from multishell_shrinkage_floquet import shell_ranges


@dataclass(frozen=True)
class StatevectorLiftSummary:
    L0: int
    q: int
    shell_gap: int
    accumulator_modulus: int
    sequence_length: int
    max_momentum: int
    input_dimension: int
    output_dimension: int
    full_injective: bool
    input_norm: float
    output_norm: float
    norm_error: float
    inverse_fidelity: float
    hard_visible_rank: int
    hard_visible_entropy: float
    hard_visible_purity: float
    no_bath_collision_count: int
    no_shrink_collision_count: int
    status: str


def entropy_from_probs(probs: np.ndarray) -> float:
    kept = probs[probs > 1e-15]
    return float(-np.sum(kept * np.log(kept)))


def random_state(dimension: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    state = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
    return state / np.linalg.norm(state)


def run_statevector_lift(
    L0: int = 3,
    q: int = 2,
    shell_gap: int = 8,
    accumulator_modulus: int = 8,
    sequence_length: int = 3,
    max_momentum: int = 1,
    seed: int = 1234,
) -> StatevectorLiftSummary:
    bath_modes = box2d_bath_modes(max_momentum=max_momentum)
    output_index: dict[tuple[object, ...], int] = {}
    inverse_map: list[int] = []
    hard_probs: dict[tuple[int, ...], float] = {}
    no_bath_outputs: set[tuple[object, ...]] = set()
    no_shrink_outputs: set[tuple[object, ...]] = set()

    input_dimension = 0
    shell_label_iterables = shell_ranges(L0, q)
    input_state: np.ndarray | None = None
    output_state: np.ndarray | None = None

    # First pass: enumerate the basis and create a compact output encoding.
    input_keys: list[
        tuple[int, tuple[int, ...], tuple[int, ...], tuple[object, ...], tuple[int, ...]]
    ] = []
    for accumulator in range(accumulator_modulus):
        for shell_labels_raw in product(*shell_label_iterables):
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
                key = full_output_key(
                    L_final,
                    acc_final,
                    labels_final,
                    bath_sequence,
                    hard_bins,
                    emitted_units,
                    shrink_records,
                )
                if key not in output_index:
                    output_index[key] = len(output_index)
                inverse_map.append(output_index[key])
                input_keys.append(
                    (
                        accumulator,
                        shell_labels,
                        bath_sequence,
                        key,
                        hard_bins,
                    )
                )
                no_bath_outputs.add(
                    no_bath_microstate_key(
                        L_final,
                        acc_final,
                        labels_final,
                        hard_bins,
                        emitted_units,
                        shrink_records,
                    )
                )
                no_shrink_outputs.add(
                    no_shrink_record_key(
                        L_final,
                        acc_final,
                        labels_final,
                        bath_sequence,
                        hard_bins,
                        emitted_units,
                    )
                )
                input_dimension += 1

    full_injective = len(output_index) == input_dimension
    input_state = random_state(input_dimension, seed=seed)
    output_state = np.zeros(len(output_index), dtype=np.complex128)
    for input_axis, output_axis in enumerate(inverse_map):
        output_state[output_axis] += input_state[input_axis]

    # Since the map is injective, this is the exact inverse on the image.
    reconstructed = np.zeros_like(input_state)
    for input_axis, output_axis in enumerate(inverse_map):
        reconstructed[input_axis] = output_state[output_axis]

    # Treat the hard-bin sequence as a visible coarse radiation record. The
    # hidden records include the bath microstate and shrink data. For this
    # computational-basis lift the reduced hard state is diagonal.
    for input_axis, (_acc, _labels, _bath, _key, hard_bins) in enumerate(input_keys):
        hard_probs[hard_bins] = hard_probs.get(hard_bins, 0.0) + float(
            abs(input_state[input_axis]) ** 2
        )
    hard_prob_array = np.array(list(hard_probs.values()), dtype=float)
    hard_prob_array /= hard_prob_array.sum()
    hard_entropy = entropy_from_probs(hard_prob_array)
    hard_purity = float(np.sum(hard_prob_array**2))

    input_norm = float(np.linalg.norm(input_state))
    output_norm = float(np.linalg.norm(output_state))
    fidelity = float(abs(np.vdot(input_state, reconstructed)) ** 2)

    return StatevectorLiftSummary(
        L0=L0,
        q=q,
        shell_gap=shell_gap,
        accumulator_modulus=accumulator_modulus,
        sequence_length=sequence_length,
        max_momentum=max_momentum,
        input_dimension=input_dimension,
        output_dimension=len(output_index),
        full_injective=full_injective,
        input_norm=input_norm,
        output_norm=output_norm,
        norm_error=abs(input_norm - output_norm),
        inverse_fidelity=fidelity,
        hard_visible_rank=len(hard_probs),
        hard_visible_entropy=hard_entropy,
        hard_visible_purity=hard_purity,
        no_bath_collision_count=input_dimension - len(no_bath_outputs),
        no_shrink_collision_count=input_dimension - len(no_shrink_outputs),
        status=(
            "state-vector lift of the global register rule; exact on the "
            "finite computational basis, not a Hamiltonian time evolution"
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
    summary = run_statevector_lift()
    write_dataclass_rows(
        [summary], out_dir / "global_floquet_statevector_lift_summary.csv"
    )
    print(
        f"dim={summary.input_dimension}",
        f"injective={summary.full_injective}",
        f"norm_error={summary.norm_error:.3e}",
        f"inverse_fidelity={summary.inverse_fidelity:.12f}",
        f"hard_rank={summary.hard_visible_rank}",
        f"hard_entropy={summary.hard_visible_entropy:.6f}",
        f"no_bath_collisions={summary.no_bath_collision_count}",
        f"no_shrink_collisions={summary.no_shrink_collision_count}",
    )


if __name__ == "__main__":
    main()
