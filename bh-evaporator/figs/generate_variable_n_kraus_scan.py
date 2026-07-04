#!/usr/bin/env python3
"""Plot targeted robustness scan for variable-N Kraus evaporator."""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def read_rows(path: pathlib.Path) -> list[dict[str, float]]:
    rows = []
    with path.open() as fh:
        for row in csv.DictReader(fh):
            if row.get("error"):
                continue
            rows.append({key: float(value) for key, value in row.items() if value != ""})
    return rows


def grouped(rows: list[dict[str, float]]):
    buckets = defaultdict(list)
    for row in rows:
        key = (row["mu"], row["max_gap"], row["initial_e_min"], row["initial_e_max"])
        buckets[key].append(row)

    out = []
    for key, vals in buckets.items():
        if len(vals) < 2:
            continue
        acc = np.array([v["accel_ratio_mid_over_early"] for v in vals])
        s2 = np.array([v["peak_renyi2_core"] for v in vals])
        deff = np.array([v["final_effective_dimension"] for v in vals])
        out.append(
            {
                "key": key,
                "min_acc": float(np.min(acc)),
                "mean_acc": float(np.mean(acc)),
                "mean_s2": float(np.mean(s2)),
                "mean_deff": float(np.mean(deff)),
            }
        )
    return sorted(out, key=lambda item: item["min_acc"], reverse=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scan",
        type=pathlib.Path,
        default=DATADIR / "variable_n_bose_hubbard_kraus_scan.csv",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "step3_variable_n_kraus_scan.pdf",
    )
    args = parser.parse_args(argv)

    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"matplotlib is required for plotting: {exc}")

    matplotlib.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.grid": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    rows = grouped(read_rows(args.scan))
    top = rows[:10][::-1]

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.5))

    labels = []
    min_acc = []
    mean_acc = []
    s2 = []
    for row in top:
        mu, gap, emin, emax = row["key"]
        labels.append(f"mu={mu:g}, gap={gap:g}\n[{emin:g},{emax:g}]")
        min_acc.append(row["min_acc"])
        mean_acc.append(row["mean_acc"])
        s2.append(row["mean_s2"])

    y = np.arange(len(labels))
    ax = axes[0]
    ax.barh(y, min_acc, color="C0", alpha=0.75, label="min over seeds")
    ax.plot(mean_acc, y, "o", color="C3", label="mean")
    ax.axvline(1.0, color="0.25", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("mid / early emitted power")
    ax.set_title("Acceleration robustness")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.scatter([row["mean_deff"] for row in rows], [row["mean_acc"] for row in rows], c=[row["mean_s2"] for row in rows])
    ax.axhline(1.0, color="0.25", linewidth=1)
    ax.set_xlabel("final effective dimension")
    ax.set_ylabel("mean acceleration")
    ax.set_title("Scan landscape")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
