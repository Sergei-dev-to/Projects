from __future__ import annotations

import csv
from dataclasses import dataclass
from itertools import product
from pathlib import Path


@dataclass(frozen=True)
class MultiShellSummary:
    L0: int
    q: int
    shell_gap: int
    accumulator_modulus: int
    emitted_bins: str
    sequence_length: int
    input_count: int
    unique_output_count: int
    injective: bool
    shrink_event_count: int
    max_shrinks_in_sequence: int
    zero_shrink_outputs: int
    one_shrink_outputs: int
    multi_shrink_outputs: int


@dataclass(frozen=True)
class MultiShellSample:
    emitted_sequence: str
    L_initial: int
    accumulator_initial: int
    shell_labels_initial: str
    L_final: int
    accumulator_final: int
    shell_labels_final: str
    radiation_record: str
    shrink_record: str
    shrink_count: int


def shell_dim(L: int, q: int) -> int:
    return q ** max(0, 2 * L - 1)


def shell_ranges(L0: int, q: int) -> list[range]:
    # Index 0 corresponds to the trivial L=1 core. Shell labels begin at L=2.
    return [range(1)] + [range(shell_dim(L, q)) for L in range(2, L0 + 1)]


def step_update(
    L: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    emitted_bin: int,
    shell_gap: int,
    accumulator_modulus: int,
) -> tuple[int, int, tuple[int, ...], tuple[int, int] | None]:
    updated = accumulator + emitted_bin
    if L > 1 and updated >= shell_gap:
        labels = list(shell_labels)
        moved_label = labels[L - 1]
        labels[L - 1] = 0
        return L - 1, updated - shell_gap, tuple(labels), (L, moved_label)
    return L, updated % accumulator_modulus, shell_labels, None


def run_sequence(
    L0: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    emitted_sequence: tuple[int, ...],
    shell_gap: int,
    accumulator_modulus: int,
) -> tuple[int, int, tuple[int, ...], tuple[int, ...], tuple[tuple[int, int], ...]]:
    L = L0
    radiation: list[int] = []
    shrink_records: list[tuple[int, int]] = []
    labels = shell_labels
    acc = accumulator
    for emitted_bin in emitted_sequence:
        L, acc, labels, shrink_record = step_update(
            L=L,
            accumulator=acc,
            shell_labels=labels,
            emitted_bin=emitted_bin,
            shell_gap=shell_gap,
            accumulator_modulus=accumulator_modulus,
        )
        radiation.append(emitted_bin)
        if shrink_record is not None:
            shrink_records.append(shrink_record)
    return L, acc, labels, tuple(radiation), tuple(shrink_records)


def output_key(
    L: int,
    accumulator: int,
    shell_labels: tuple[int, ...],
    radiation: tuple[int, ...],
    shrink_records: tuple[tuple[int, int], ...],
) -> tuple[object, ...]:
    return (L, accumulator, shell_labels, radiation, shrink_records)


def run_multishell_check(
    L0: int = 3,
    q: int = 2,
    shell_gap: int = 8,
    accumulator_modulus: int = 8,
    emitted_bins: tuple[int, ...] = (1, 2, 3),
    sequence_length: int = 4,
    sample_limit: int = 16,
) -> tuple[list[MultiShellSample], MultiShellSummary]:
    outputs: set[tuple[object, ...]] = set()
    samples: list[MultiShellSample] = []
    input_count = 0
    shrink_event_count = 0
    max_shrinks = 0
    shrink_histogram: dict[int, int] = {}

    for accumulator in range(accumulator_modulus):
        for shell_labels in product(*shell_ranges(L0, q)):
            for emitted_sequence in product(emitted_bins, repeat=sequence_length):
                result = run_sequence(
                    L0=L0,
                    accumulator=accumulator,
                    shell_labels=tuple(shell_labels),
                    emitted_sequence=tuple(emitted_sequence),
                    shell_gap=shell_gap,
                    accumulator_modulus=accumulator_modulus,
                )
                L_final, acc_final, labels_final, radiation, shrink_records = result
                key = output_key(
                    L_final, acc_final, labels_final, radiation, shrink_records
                )
                outputs.add(key)
                input_count += 1
                shrink_count = len(shrink_records)
                shrink_event_count += shrink_count
                max_shrinks = max(max_shrinks, shrink_count)
                shrink_histogram[shrink_count] = shrink_histogram.get(shrink_count, 0) + 1
                if len(samples) < sample_limit and shrink_count > 0:
                    samples.append(
                        MultiShellSample(
                            emitted_sequence=",".join(map(str, emitted_sequence)),
                            L_initial=L0,
                            accumulator_initial=accumulator,
                            shell_labels_initial=",".join(map(str, shell_labels)),
                            L_final=L_final,
                            accumulator_final=acc_final,
                            shell_labels_final=",".join(map(str, labels_final)),
                            radiation_record=",".join(map(str, radiation)),
                            shrink_record=";".join(
                                f"L{L}:{label}" for L, label in shrink_records
                            ),
                            shrink_count=shrink_count,
                        )
                    )

    summary = MultiShellSummary(
        L0=L0,
        q=q,
        shell_gap=shell_gap,
        accumulator_modulus=accumulator_modulus,
        emitted_bins=",".join(map(str, emitted_bins)),
        sequence_length=sequence_length,
        input_count=input_count,
        unique_output_count=len(outputs),
        injective=input_count == len(outputs),
        shrink_event_count=shrink_event_count,
        max_shrinks_in_sequence=max_shrinks,
        zero_shrink_outputs=shrink_histogram.get(0, 0),
        one_shrink_outputs=shrink_histogram.get(1, 0),
        multi_shrink_outputs=sum(
            count for shrink_count, count in shrink_histogram.items() if shrink_count >= 2
        ),
    )
    return samples, summary


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
    samples, summary = run_multishell_check()
    write_dataclass_rows(samples, out_dir / "multishell_shrinkage_floquet_sample.csv")
    write_dataclass_rows([summary], out_dir / "multishell_shrinkage_floquet_summary.csv")
    print(
        f"inputs={summary.input_count}",
        f"unique={summary.unique_output_count}",
        f"injective={summary.injective}",
        f"shrink_events={summary.shrink_event_count}",
        f"max_shrinks={summary.max_shrinks_in_sequence}",
        f"zero/one/multi={summary.zero_shrink_outputs}/"
        f"{summary.one_shrink_outputs}/{summary.multi_shrink_outputs}",
    )


if __name__ == "__main__":
    main()
