from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from fused_floquet_time_resolved_scan import (
    row_for_case,
    golden_hard_schedule,
)
import numpy as np


@dataclass(frozen=True)
class PageProbeRow:
    scrambler: str
    emission_count: int
    threshold: int
    rate_L0: float
    basis_terms: int
    transferred_mean: float
    p_done: float
    s_core_acc: float
    s_full_radiation: float
    s_visible: float
    s_soft: float
    s_hard: float
    mi_old_new_full: float
    hard_entropy_error: float


def run_page_probe(
    L0: int = 3,
    rate_L0: float = 20.0,
    threshold: int = 4,
    emission_counts: tuple[int, ...] = (2, 4, 6, 8),
    scramblers: tuple[str, ...] = ("margulis", "none"),
    seed: int = 0,
) -> list[PageProbeRow]:
    rows: list[PageProbeRow] = []
    for emission_count in emission_counts:
        hard_probs, mean_omegas, temperatures = golden_hard_schedule(
            L0=rate_L0,
            micro_emissions=emission_count,
            q=2,
            sigma=1.0,
            bath_dim=2,
            x_edges=np.array((0.0, 2.0, 8.0), dtype=float),
            n_grid=1001,
        )
        for scrambler in scramblers:
            row = row_for_case(
                L0=L0,
                rate_L0=rate_L0,
                threshold=threshold,
                micro_emissions=emission_count,
                hard_prob_schedule=hard_probs,
                mean_omega_schedule=mean_omegas,
                temperature_schedule=temperatures,
                warmup_time=8.0,
                dt=0.2,
                seed=seed,
                scrambler=scrambler,
            )
            rows.append(
                PageProbeRow(
                    scrambler=scrambler,
                    emission_count=emission_count,
                    threshold=threshold,
                    rate_L0=rate_L0,
                    basis_terms=row.basis_terms,
                    transferred_mean=row.transferred_mean,
                    p_done=row.p_done,
                    s_core_acc=row.s_core_acc,
                    s_full_radiation=row.s_full_radiation,
                    s_visible=row.s_visible,
                    s_soft=row.s_soft,
                    s_hard=row.s_hard,
                    mi_old_new_full=row.mi_old_new_full,
                    hard_entropy_error=row.hard_entropy_error,
                )
            )
    return rows


def write_rows(rows: list[PageProbeRow], path: Path) -> None:
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
    out = Path(__file__).resolve().parent / "data" / "fused_floquet_page_probe.csv"
    rows = run_page_probe()
    write_rows(rows, out)
    print(f"wrote {out}")
    print("scrambler emissions S_rad S_core S_soft I_old_new <shells> terms")
    for row in rows:
        print(
            f"{row.scrambler:9s} "
            f"{row.emission_count:9d} "
            f"{row.s_full_radiation:5.3f} "
            f"{row.s_core_acc:5.3f} "
            f"{row.s_soft:6.3f} "
            f"{row.mi_old_new_full:9.3f} "
            f"{row.transferred_mean:7.3f} "
            f"{row.basis_terms:6d}"
        )


if __name__ == "__main__":
    main()
