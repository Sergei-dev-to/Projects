from __future__ import annotations

import csv
import math
import random
from dataclasses import dataclass
from pathlib import Path

from stabilizer_shell_page_diagnostic import (
    StabilizerState,
    build_edge_sets,
    grid_positions,
    scramble,
    shell_positions,
)


@dataclass(frozen=True)
class HardSoftAccountingRow:
    seed: int
    geometry: str
    L0: int
    hard_emissions_per_shell: int
    L_before: int
    L_after: int
    soft_rad_qubits: int
    shell_qubits: int
    remaining_qubits: int
    page_capacity: int
    soft_radiation_entropy: int
    old_new_soft_mi: int
    accumulated_hard_entropy: float
    apparent_coarse_radiation_entropy: float
    hard_entropy_monotone: bool


@dataclass(frozen=True)
class HardSoftAccountingSummary:
    seed: int
    geometry: str
    L0: int
    warmup_depth: int
    cycle_depth: int
    hard_emissions_per_shell: int
    total_page_deficit: int
    peak_soft_entropy: int
    final_soft_entropy: int
    final_accumulated_hard_entropy: float
    final_apparent_coarse_radiation_entropy: float
    first_old_new_soft_mi: str
    status: str


def run_hard_soft_accounting(
    L0: int = 8,
    geometry: str = "expander8",
    warmup_depth: int = 8,
    cycle_depth: int = 2,
    hard_emissions_per_shell: int = 3,
    seed: int = 0,
) -> tuple[list[HardSoftAccountingRow], HardSoftAccountingSummary]:
    rng = random.Random(seed)
    ids = grid_positions(L0)
    edge_sets = build_edge_sets(L0, ids, geometry, seed)
    state = StabilizerState(L0 * L0)
    soft_radiation: set[int] = set()
    rows: list[HardSoftAccountingRow] = []
    accumulated_hard_entropy = 0.0
    previous_hard_entropy = 0.0
    first_old_new_mi = ""

    scramble(state, L0, ids, edge_sets, rng, warmup_depth)

    for L in range(L0, 0, -1):
        scramble(state, L, ids, edge_sets, rng, cycle_depth)

        old_soft = set(soft_radiation)
        new_shell = {ids[pos] for pos in shell_positions(L)}
        soft_radiation |= new_shell
        remaining = (L - 1) * (L - 1)

        s_old = state.entropy(old_soft)
        s_new = state.entropy(new_shell)
        s_soft = state.entropy(soft_radiation)
        old_new_soft_mi = s_old + s_new - s_soft
        if not first_old_new_mi and old_new_soft_mi > 0:
            first_old_new_mi = f"{L}->{L - 1}"

        page_capacity = min(len(soft_radiation), remaining)
        # This is the apparent entropy of coarse hard bins after hidden bath
        # records are traced. With the max_momentum=1 bath used in the global
        # rule, each hard emission has two equally likely coarse bins.
        accumulated_hard_entropy += hard_emissions_per_shell * math.log(2.0)
        hard_entropy_monotone = accumulated_hard_entropy >= previous_hard_entropy
        previous_hard_entropy = accumulated_hard_entropy

        rows.append(
            HardSoftAccountingRow(
                seed=seed,
                geometry=geometry,
                L0=L0,
                hard_emissions_per_shell=hard_emissions_per_shell,
                L_before=L,
                L_after=L - 1,
                soft_rad_qubits=len(soft_radiation),
                shell_qubits=len(new_shell),
                remaining_qubits=remaining,
                page_capacity=page_capacity,
                soft_radiation_entropy=s_soft,
                old_new_soft_mi=old_new_soft_mi,
                accumulated_hard_entropy=accumulated_hard_entropy,
                apparent_coarse_radiation_entropy=s_soft + accumulated_hard_entropy,
                hard_entropy_monotone=hard_entropy_monotone,
            )
        )

    summary = HardSoftAccountingSummary(
        seed=seed,
        geometry=geometry,
        L0=L0,
        warmup_depth=warmup_depth,
        cycle_depth=cycle_depth,
        hard_emissions_per_shell=hard_emissions_per_shell,
        total_page_deficit=sum(
            abs(row.soft_radiation_entropy - row.page_capacity) for row in rows
        ),
        peak_soft_entropy=max(row.soft_radiation_entropy for row in rows),
        final_soft_entropy=rows[-1].soft_radiation_entropy,
        final_accumulated_hard_entropy=rows[-1].accumulated_hard_entropy,
        final_apparent_coarse_radiation_entropy=rows[
            -1
        ].apparent_coarse_radiation_entropy,
        first_old_new_soft_mi=first_old_new_mi or "none",
        status=(
            "soft shell records carry the fine Page diagnostic; hard bins are "
            "coarse locally thermal observer entropy and remain monotone"
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
    summaries: list[HardSoftAccountingSummary] = []
    for geometry, warmup_depth, cycle_depth in (
        ("grid", 16, 8),
        ("expander8", 8, 2),
        ("complete", 8, 2),
    ):
        all_rows: list[HardSoftAccountingRow] = []
        for seed in range(5):
            rows, summary = run_hard_soft_accounting(
                geometry=geometry,
                warmup_depth=warmup_depth,
                cycle_depth=cycle_depth,
                seed=seed,
            )
            all_rows.extend(rows)
            summaries.append(summary)
            print(
                f"geometry={geometry}",
                f"seed={seed}",
                f"page_deficit={summary.total_page_deficit}",
                f"peak_soft={summary.peak_soft_entropy}",
                f"final_soft={summary.final_soft_entropy}",
                f"final_hard={summary.final_accumulated_hard_entropy:.3f}",
                f"first_soft_MI={summary.first_old_new_soft_mi}",
            )
        write_dataclass_rows(
            all_rows,
            out_dir / f"hard_soft_page_accounting_{geometry}.csv",
        )
    write_dataclass_rows(summaries, out_dir / "hard_soft_page_accounting_summary.csv")


if __name__ == "__main__":
    main()
