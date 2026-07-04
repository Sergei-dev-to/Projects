from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Transition:
    L_before: int
    accumulator_before: int
    shell_label_before: int
    emitted_bin: int
    L_after: int
    accumulator_after: int
    shell_label_after: int
    shrink_record: tuple[int, int] | None
    radiation_record: tuple[int, ...]


@dataclass(frozen=True)
class AutomatonSummary:
    L_min: int
    L_max: int
    shell_gap: int
    accumulator_modulus: int
    emitted_bins: str
    transition_count: int
    unique_output_count: int
    injective: bool
    shrink_transition_count: int
    nonshrink_transition_count: int


def shell_dim(L: int, q: int = 2) -> int:
    return q ** max(0, 2 * L - 1)


def transition(
    L: int,
    accumulator: int,
    shell_label: int,
    emitted_bin: int,
    shell_gap: int,
    accumulator_modulus: int,
) -> Transition:
    updated_accumulator = accumulator + emitted_bin
    radiation_record = (emitted_bin,)

    if L > 1 and updated_accumulator >= shell_gap:
        return Transition(
            L_before=L,
            accumulator_before=accumulator,
            shell_label_before=shell_label,
            emitted_bin=emitted_bin,
            L_after=L - 1,
            accumulator_after=updated_accumulator - shell_gap,
            shell_label_after=0,
            shrink_record=(L, shell_label),
            radiation_record=radiation_record,
        )

    return Transition(
        L_before=L,
        accumulator_before=accumulator,
        shell_label_before=shell_label,
        emitted_bin=emitted_bin,
        L_after=L,
        accumulator_after=updated_accumulator % accumulator_modulus,
        shell_label_after=shell_label,
        shrink_record=None,
        radiation_record=radiation_record,
    )


def output_key(item: Transition) -> tuple[object, ...]:
    """Full output register key.

    Including the emitted radiation record and shrink record is what makes the
    update reversible. If those records are erased, shrinkage would look
    nonunitary.
    """

    return (
        item.L_after,
        item.accumulator_after,
        item.shell_label_after,
        item.shrink_record,
        item.radiation_record,
    )


def run_automaton_check(
    L_min: int = 1,
    L_max: int = 5,
    shell_gap: int = 8,
    accumulator_modulus: int = 8,
    emitted_bins: tuple[int, ...] = (1, 2, 3),
    q: int = 2,
) -> tuple[list[Transition], AutomatonSummary]:
    transitions: list[Transition] = []
    for L in range(L_min, L_max + 1):
        for accumulator in range(accumulator_modulus):
            for shell_label in range(shell_dim(L, q)):
                for emitted_bin in emitted_bins:
                    transitions.append(
                        transition(
                            L=L,
                            accumulator=accumulator,
                            shell_label=shell_label,
                            emitted_bin=emitted_bin,
                            shell_gap=shell_gap,
                            accumulator_modulus=accumulator_modulus,
                        )
                    )

    output_keys = {output_key(item) for item in transitions}
    shrink_count = sum(1 for item in transitions if item.shrink_record is not None)
    summary = AutomatonSummary(
        L_min=L_min,
        L_max=L_max,
        shell_gap=shell_gap,
        accumulator_modulus=accumulator_modulus,
        emitted_bins=",".join(str(item) for item in emitted_bins),
        transition_count=len(transitions),
        unique_output_count=len(output_keys),
        injective=len(output_keys) == len(transitions),
        shrink_transition_count=shrink_count,
        nonshrink_transition_count=len(transitions) - shrink_count,
    )
    return transitions, summary


def write_dataclass_rows(rows: list[object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].__dataclass_fields__))  # type: ignore[attr-defined]
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    transitions, summary = run_automaton_check()
    write_dataclass_rows(
        transitions[:200], out_dir / "reversible_shrinkage_automaton_sample.csv"
    )
    write_dataclass_rows([summary], out_dir / "reversible_shrinkage_automaton_summary.csv")

    print(
        f"transitions={summary.transition_count}",
        f"unique_outputs={summary.unique_output_count}",
        f"injective={summary.injective}",
        f"shrink={summary.shrink_transition_count}",
        f"nonshrink={summary.nonshrink_transition_count}",
    )


if __name__ == "__main__":
    main()
