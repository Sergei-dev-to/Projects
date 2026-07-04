"""Robustness scan for the Level 2 erosion channel.

The scan intentionally stays small enough for exact state-vector diagnostics.
It summarizes whether the minimal-soft random-unitary channel robustly gives:

    hard-only early/late mutual information near zero,
    hard+soft early/late mutual information nonzero,
    latest hard bins close to the target thermal marginal.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, pstdev

from erosion_channel_diagnostic import run_model


def summarize(values: list[float]) -> tuple[float, float, float, float]:
    return mean(values), pstdev(values), min(values), max(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--seed0", type=int, default=20260601)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/erosion_channel_robustness.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/erosion_channel_robustness_summary.csv"),
    )
    args = parser.parse_args()

    # L0=4, d_hard>2 becomes expensive for exact dense SVD diagnostics.
    configs = [(3, 2), (3, 3), (3, 4), (4, 2)]
    rows: list[dict[str, float | int | str]] = []
    for L0, d_hard in configs:
        for offset in range(args.seeds):
            seed = args.seed0 + offset
            run_rows = run_model("level2_minimal", L0, args.q, d_hard, seed)
            final = run_rows[-1]
            rows.append(
                {
                    "L0": L0,
                    "q": args.q,
                    "d_hard": d_hard,
                    "seed": seed,
                    "max_latest_hard_trace_distance": max(
                        float(r["latest_hard_trace_distance"]) for r in run_rows
                    ),
                    "final_latest_hard_trace_distance": float(final["latest_hard_trace_distance"]),
                    "final_latest_hard_entropy": float(final["latest_hard_entropy"]),
                    "thermal_hard_entropy": float(final["thermal_hard_entropy"]),
                    "final_hard_entropy": float(final["hard_entropy"]),
                    "final_soft_entropy": float(final["soft_entropy"]),
                    "final_core_entropy": float(final["core_entropy"]),
                    "final_I_hard_hard": float(final["I_first_hard_last_hard"]),
                    "final_I_pair_pair": float(final["I_first_pair_last_pair"]),
                }
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    grouped: dict[tuple[int, int], list[dict[str, float | int | str]]] = defaultdict(list)
    for row in rows:
        grouped[(int(row["L0"]), int(row["d_hard"]))].append(row)

    summary_rows: list[dict[str, float | int]] = []
    metrics = [
        "max_latest_hard_trace_distance",
        "final_I_hard_hard",
        "final_I_pair_pair",
        "final_latest_hard_entropy",
        "thermal_hard_entropy",
    ]
    for (L0, d_hard), group in sorted(grouped.items()):
        summary: dict[str, float | int] = {"L0": L0, "d_hard": d_hard, "n": len(group)}
        for metric in metrics:
            vals = [float(row[metric]) for row in group]
            m, s, lo, hi = summarize(vals)
            summary[f"{metric}_mean"] = m
            summary[f"{metric}_std"] = s
            summary[f"{metric}_min"] = lo
            summary[f"{metric}_max"] = hi
        summary_rows.append(summary)

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print("L0 d_h n  maxD(mean)  I_hh(mean)  I_pair(mean)  S_hard_latest/thermal")
    for row in summary_rows:
        print(
            f"{row['L0']:>2} {row['d_hard']:>3} {row['n']:>2} "
            f"{row['max_latest_hard_trace_distance_mean']:10.4f} "
            f"{row['final_I_hard_hard_mean']:11.4f} "
            f"{row['final_I_pair_pair_mean']:12.4f} "
            f"{row['final_latest_hard_entropy_mean']:8.4f}/"
            f"{row['thermal_hard_entropy_mean']:.4f}"
        )


if __name__ == "__main__":
    main()
