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
class RateScaleSummaryRow:
    rate_L0: float
    cases: int
    seeds: int
    threshold: int
    micro_emissions: int
    p1_first: float
    p1_last: float
    mean_omega_total: float
    first_omega_over_T: float
    last_omega_over_T: float
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


def summarize_rate(rows: list[FusedFloquetRow]) -> RateScaleSummaryRow:
    rates = {row.rate_L0 for row in rows}
    thresholds = {row.threshold for row in rows}
    emissions = {row.micro_emissions for row in rows}
    if len(rates) != 1 or len(thresholds) != 1 or len(emissions) != 1:
        raise ValueError("summarize_rate expects one rate, threshold, and emission count")

    scrambled = [row for row in rows if row.scrambler in {"margulis", "grid"}]
    none = [row for row in rows if row.scrambler == "none"]
    none_soft_by_seed = {row.seed: row.s_soft for row in none}
    none_old_new_by_seed = {row.seed: row.mi_old_new_full for row in none}
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
    first = rows[0]
    return RateScaleSummaryRow(
        rate_L0=first.rate_L0,
        cases=len(rows),
        seeds=len({row.seed for row in rows}),
        threshold=first.threshold,
        micro_emissions=first.micro_emissions,
        p1_first=first.hard_prob_one,
        p1_last=first.hard_prob_one_last,
        mean_omega_total=first.mean_omega_total,
        first_omega_over_T=first.first_omega_over_T,
        last_omega_over_T=first.last_omega_over_T,
        scrambled_soft_mean=mean(row.s_soft for row in scrambled),
        scrambled_soft_std=pstdev(row.s_soft for row in scrambled),
        none_soft_mean=mean(row.s_soft for row in none),
        soft_gap_mean=mean(soft_gaps),
        soft_gap_std=pstdev(soft_gaps),
        scrambled_old_new_mean=mean(row.mi_old_new_full for row in scrambled),
        none_old_new_mean=mean(row.mi_old_new_full for row in none),
        old_new_gap_mean=mean(old_new_gaps),
        old_new_gap_std=pstdev(old_new_gaps),
        hard_entropy_error_max=max(row.hard_entropy_error for row in rows),
        transferred_mean_scrambled=mean(row.transferred_mean for row in scrambled),
        p_done_scrambled=mean(row.p_done for row in scrambled),
    )


def write_summary(rows: list[RateScaleSummaryRow], path: Path) -> None:
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
    rate_values = (8.0, 12.0, 20.0, 40.0)
    all_rows: list[FusedFloquetRow] = []
    summaries: list[RateScaleSummaryRow] = []
    for rate_L0 in rate_values:
        rows, _summary = run_fused_scan(
            rate_L0=rate_L0,
            thresholds=(5,),
            micro_emission_values=(6,),
            seeds=(0, 1),
        )
        all_rows.extend(rows)
        summaries.append(summarize_rate(rows))

    write_dataclass_rows(all_rows, out_dir / "fused_floquet_rate_scale_rows.csv")
    write_summary(summaries, out_dir / "fused_floquet_rate_scale_summary.csv")

    print("rate_L0  p1_first  soft_gap  old_new_gap  hard_err  <shells>")
    for row in summaries:
        print(
            f"{row.rate_L0:7.1f} "
            f"{row.p1_first:8.3f} "
            f"{row.soft_gap_mean:8.3f} "
            f"{row.old_new_gap_mean:11.3f} "
            f"{row.hard_entropy_error_max:9.1e} "
            f"{row.transferred_mean_scrambled:8.3f}"
        )


if __name__ == "__main__":
    main()
