from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, pstdev

from fused_floquet_time_resolved_scan import (
    FusedFloquetRow,
    run_fused_scan,
    write_dataclass_rows,
)


@dataclass(frozen=True)
class RobustnessSummaryRow:
    threshold: int
    cases: int
    seeds: int
    scrambled_soft_mean: float
    scrambled_soft_std: float
    none_soft_mean: float
    soft_gap_mean: float
    soft_gap_std: float
    scrambled_old_new_mean: float
    none_old_new_mean: float
    old_new_gap_mean: float
    old_new_gap_std: float
    hard_entropy_error_max: float
    transferred_mean_scrambled: float
    p_done_scrambled: float
    score_mean: float


def summarize_by_threshold(rows: list[FusedFloquetRow]) -> list[RobustnessSummaryRow]:
    thresholds = sorted({row.threshold for row in rows})
    out: list[RobustnessSummaryRow] = []
    for threshold in thresholds:
        group = [row for row in rows if row.threshold == threshold]
        scrambled = [row for row in group if row.scrambler in {"margulis", "grid"}]
        none = [row for row in group if row.scrambler == "none"]
        seed_values = sorted({row.seed for row in group})
        none_soft_by_seed = {
            row.seed: row.s_soft for row in none
        }
        none_old_new_by_seed = {
            row.seed: row.mi_old_new_full for row in none
        }
        soft_gaps = [
            row.s_soft - none_soft_by_seed[row.seed]
            for row in scrambled
            if row.seed in none_soft_by_seed
        ]
        old_new_gaps = [
            row.mi_old_new_full - none_old_new_by_seed[row.seed]
            for row in scrambled
            if row.seed in none_old_new_by_seed
        ]
        out.append(
            RobustnessSummaryRow(
                threshold=threshold,
                cases=len(group),
                seeds=len(seed_values),
                scrambled_soft_mean=mean(row.s_soft for row in scrambled),
                scrambled_soft_std=pstdev(row.s_soft for row in scrambled),
                none_soft_mean=mean(row.s_soft for row in none),
                soft_gap_mean=mean(soft_gaps),
                soft_gap_std=pstdev(soft_gaps),
                scrambled_old_new_mean=mean(row.mi_old_new_full for row in scrambled),
                none_old_new_mean=mean(row.mi_old_new_full for row in none),
                old_new_gap_mean=mean(old_new_gaps),
                old_new_gap_std=pstdev(old_new_gaps),
                hard_entropy_error_max=max(row.hard_entropy_error for row in group),
                transferred_mean_scrambled=mean(row.transferred_mean for row in scrambled),
                p_done_scrambled=mean(row.p_done for row in scrambled),
                score_mean=mean(row.score for row in group),
            )
        )
    return out


def write_summary(rows: list[RobustnessSummaryRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].__dataclass_fields__),  # type: ignore[attr-defined]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    rows, scan_summary = run_fused_scan(
        thresholds=(4, 5, 6),
        micro_emission_values=(6,),
        seeds=(0, 1),
    )
    threshold_summary = summarize_by_threshold(rows)
    write_dataclass_rows(rows, out_dir / "fused_floquet_robustness_rows.csv")
    write_dataclass_rows(
        [scan_summary],
        out_dir / "fused_floquet_robustness_scan_summary.csv",
    )
    write_summary(
        threshold_summary,
        out_dir / "fused_floquet_robustness_by_threshold.csv",
    )

    print(
        f"cases={scan_summary.cases}",
        f"best_threshold={scan_summary.best_threshold}",
        f"best_score={scan_summary.best_score:.3f}",
        f"max_terms={scan_summary.max_basis_terms}",
    )
    print("threshold  soft_gap  old_new_gap  hard_err  <shells>  p_done")
    for row in threshold_summary:
        print(
            f"{row.threshold:9d} "
            f"{row.soft_gap_mean:8.3f} "
            f"{row.old_new_gap_mean:11.3f} "
            f"{row.hard_entropy_error_max:9.1e} "
            f"{row.transferred_mean_scrambled:8.3f} "
            f"{row.p_done_scrambled:7.3f}"
        )


if __name__ == "__main__":
    main()
