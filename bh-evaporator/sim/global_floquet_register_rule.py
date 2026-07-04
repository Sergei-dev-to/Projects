from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from multishell_shrinkage_floquet import shell_ranges, step_update


@dataclass(frozen=True)
class BathMode:
    mode_id: int
    nx: int
    ny: int
    energy: float
    hard_bin: int
    emitted_units: int


@dataclass(frozen=True)
class GlobalFloquetSummary:
    L0: int
    q: int
    shell_gap: int
    accumulator_modulus: int
    sequence_length: int
    bath_mode_count: int
    input_count: int
    unique_full_outputs: int
    full_injective: bool
    unique_without_bath_microstate: int
    injective_without_bath_microstate: bool
    unique_without_shrink_record: int
    injective_without_shrink_record: bool
    shrink_event_count: int
    max_shrinks_in_sequence: int
    hard_bin_histogram: str


@dataclass(frozen=True)
class GlobalFloquetSample:
    bath_sequence: str
    hard_bin_sequence: str
    emitted_unit_sequence: str
    L_initial: int
    accumulator_initial: int
    shell_labels_initial: str
    L_final: int
    accumulator_final: int
    shell_labels_final: str
    shrink_record: str
    shrink_count: int


def box2d_bath_modes(max_momentum: int = 1) -> tuple[BathMode, ...]:
    modes: list[BathMode] = []
    mode_id = 0
    for nx in range(-max_momentum, max_momentum + 1):
        for ny in range(-max_momentum, max_momentum + 1):
            if nx == 0 and ny == 0:
                continue
            energy = math.sqrt(nx * nx + ny * ny)
            # Integer emitted units are the accumulator's coarse energy bins.
            # For max_momentum=1 this gives axis modes as unit-1 emissions
            # and diagonal modes as unit-2 emissions.
            emitted_units = max(1, int(math.ceil(energy)))
            hard_bin = emitted_units
            modes.append(
                BathMode(
                    mode_id=mode_id,
                    nx=nx,
                    ny=ny,
                    energy=energy,
                    hard_bin=hard_bin,
                    emitted_units=emitted_units,
                )
            )
            mode_id += 1
    return tuple(modes)


def run_global_sequence(
    L0: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    bath_sequence: tuple[int, ...],
    bath_modes: tuple[BathMode, ...],
    shell_gap: int,
    accumulator_modulus: int,
) -> tuple[
    int,
    int,
    tuple[int, ...],
    tuple[tuple[int, int], ...],
    tuple[int, ...],
    tuple[int, ...],
]:
    L = L0
    acc = accumulator
    labels = shell_labels
    hard_bins: list[int] = []
    emitted_units: list[int] = []
    shrink_records: list[tuple[int, int]] = []
    for mode_id in bath_sequence:
        mode = bath_modes[mode_id]
        hard_bins.append(mode.hard_bin)
        emitted_units.append(mode.emitted_units)
        L, acc, labels, shrink_record = step_update(
            L=L,
            accumulator=acc,
            shell_labels=labels,
            emitted_bin=mode.emitted_units,
            shell_gap=shell_gap,
            accumulator_modulus=accumulator_modulus,
        )
        if shrink_record is not None:
            shrink_records.append(shrink_record)
    return L, acc, labels, tuple(shrink_records), tuple(hard_bins), tuple(emitted_units)


def full_output_key(
    L: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    bath_sequence: tuple[int, ...],
    hard_bins: tuple[int, ...],
    emitted_units: tuple[int, ...],
    shrink_records: tuple[tuple[int, int], ...],
) -> tuple[object, ...]:
    return (
        L,
        accumulator,
        shell_labels,
        bath_sequence,
        hard_bins,
        emitted_units,
        shrink_records,
    )


def no_bath_microstate_key(
    L: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    hard_bins: tuple[int, ...],
    emitted_units: tuple[int, ...],
    shrink_records: tuple[tuple[int, int], ...],
) -> tuple[object, ...]:
    return (L, accumulator, shell_labels, hard_bins, emitted_units, shrink_records)


def no_shrink_record_key(
    L: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    bath_sequence: tuple[int, ...],
    hard_bins: tuple[int, ...],
    emitted_units: tuple[int, ...],
) -> tuple[object, ...]:
    return (L, accumulator, shell_labels, bath_sequence, hard_bins, emitted_units)


def run_global_floquet_check(
    L0: int = 3,
    q: int = 2,
    shell_gap: int = 8,
    accumulator_modulus: int = 8,
    sequence_length: int = 3,
    max_momentum: int = 1,
    sample_limit: int = 16,
) -> tuple[list[BathMode], list[GlobalFloquetSample], GlobalFloquetSummary]:
    bath_modes = box2d_bath_modes(max_momentum=max_momentum)
    full_outputs: set[tuple[object, ...]] = set()
    no_bath_outputs: set[tuple[object, ...]] = set()
    no_shrink_outputs: set[tuple[object, ...]] = set()
    samples: list[GlobalFloquetSample] = []
    input_count = 0
    shrink_event_count = 0
    max_shrinks = 0
    hard_hist: dict[int, int] = {}

    for accumulator in range(accumulator_modulus):
        for shell_labels in product(*shell_ranges(L0, q)):
            for bath_sequence in product(
                range(len(bath_modes)), repeat=sequence_length
            ):
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
                    shell_labels=tuple(shell_labels),
                    bath_sequence=tuple(bath_sequence),
                    bath_modes=bath_modes,
                    shell_gap=shell_gap,
                    accumulator_modulus=accumulator_modulus,
                )
                full_outputs.add(
                    full_output_key(
                        L_final,
                        acc_final,
                        labels_final,
                        tuple(bath_sequence),
                        hard_bins,
                        emitted_units,
                        shrink_records,
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
                        tuple(bath_sequence),
                        hard_bins,
                        emitted_units,
                    )
                )
                input_count += 1
                shrink_count = len(shrink_records)
                shrink_event_count += shrink_count
                max_shrinks = max(max_shrinks, shrink_count)
                for hard_bin in hard_bins:
                    hard_hist[hard_bin] = hard_hist.get(hard_bin, 0) + 1
                if len(samples) < sample_limit and shrink_count > 0:
                    samples.append(
                        GlobalFloquetSample(
                            bath_sequence=",".join(map(str, bath_sequence)),
                            hard_bin_sequence=",".join(map(str, hard_bins)),
                            emitted_unit_sequence=",".join(map(str, emitted_units)),
                            L_initial=L0,
                            accumulator_initial=accumulator,
                            shell_labels_initial=",".join(map(str, shell_labels)),
                            L_final=L_final,
                            accumulator_final=acc_final,
                            shell_labels_final=",".join(map(str, labels_final)),
                            shrink_record=";".join(
                                f"L{L}:{label}" for L, label in shrink_records
                            ),
                            shrink_count=shrink_count,
                        )
                    )

    summary = GlobalFloquetSummary(
        L0=L0,
        q=q,
        shell_gap=shell_gap,
        accumulator_modulus=accumulator_modulus,
        sequence_length=sequence_length,
        bath_mode_count=len(bath_modes),
        input_count=input_count,
        unique_full_outputs=len(full_outputs),
        full_injective=len(full_outputs) == input_count,
        unique_without_bath_microstate=len(no_bath_outputs),
        injective_without_bath_microstate=len(no_bath_outputs) == input_count,
        unique_without_shrink_record=len(no_shrink_outputs),
        injective_without_shrink_record=len(no_shrink_outputs) == input_count,
        shrink_event_count=shrink_event_count,
        max_shrinks_in_sequence=max_shrinks,
        hard_bin_histogram=",".join(
            f"{key}:{hard_hist[key]}" for key in sorted(hard_hist)
        ),
    )
    return list(bath_modes), samples, summary


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
    bath_modes, samples, summary = run_global_floquet_check()
    write_dataclass_rows(bath_modes, out_dir / "global_floquet_bath_modes.csv")
    write_dataclass_rows(samples, out_dir / "global_floquet_register_rule_sample.csv")
    write_dataclass_rows([summary], out_dir / "global_floquet_register_rule_summary.csv")
    print(
        f"inputs={summary.input_count}",
        f"full_unique={summary.unique_full_outputs}",
        f"full_injective={summary.full_injective}",
        f"no_bath_unique={summary.unique_without_bath_microstate}",
        f"no_bath_injective={summary.injective_without_bath_microstate}",
        f"no_shrink_unique={summary.unique_without_shrink_record}",
        f"no_shrink_injective={summary.injective_without_shrink_record}",
        f"shrinks={summary.shrink_event_count}",
        f"max_shrinks={summary.max_shrinks_in_sequence}",
    )


if __name__ == "__main__":
    main()
