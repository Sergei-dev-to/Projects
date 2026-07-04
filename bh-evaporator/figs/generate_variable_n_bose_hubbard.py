#!/usr/bin/env python3
"""Plot variable-N Bose-Hubbard evaporation diagnostic."""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def read_scan(path: pathlib.Path) -> list[dict[str, float]]:
    rows = []
    with path.open() as fh:
        for row in csv.DictReader(fh):
            if row.get("error"):
                continue
            rows.append({key: float(value) for key, value in row.items() if value != ""})
    return rows


def grouped_scan(rows: list[dict[str, float]]):
    grouped = defaultdict(list)
    for row in rows:
        key = (row["mu"], row["max_gap"], row["initial_e_min"], row["initial_e_max"])
        grouped[key].append(row)
    out = []
    for key, vals in grouped.items():
        if len(vals) < 2:
            continue
        acc = np.asarray([v["accel_ratio_mid_over_early"] for v in vals])
        early = np.asarray([v["mean_power_early"] for v in vals])
        mid = np.asarray([v["mean_power_mid"] for v in vals])
        late = np.asarray([v["mean_power_late"] for v in vals])
        out.append(
            {
                "key": key,
                "min_acc": float(np.min(acc)),
                "mean_acc": float(np.mean(acc)),
                "early": float(np.mean(early)),
                "mid": float(np.mean(mid)),
                "late": float(np.mean(late)),
            }
        )
    return sorted(out, key=lambda row: row["min_acc"], reverse=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--best",
        type=pathlib.Path,
        default=DATADIR / "variable_n_bose_hubbard_evaporation_best.npz",
    )
    parser.add_argument(
        "--scan",
        type=pathlib.Path,
        default=DATADIR / "variable_n_bose_hubbard_evaporation_scan.csv",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "step3_variable_n_bose_hubbard.pdf",
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

    best = np.load(args.best)
    rows = read_scan(args.scan)
    grouped = grouped_scan(rows)[:6]

    steps = np.arange(len(best["energy"]))
    fig, axes = plt.subplots(2, 2, figsize=(7.6, 5.4))

    ax = axes[0, 0]
    ax.plot(steps, best["energy"], color="C0", label="total energy")
    ax.set_xlabel("step")
    ax.set_ylabel("core energy")
    ax.set_title("Energy decreases")

    ax2 = ax.twinx()
    ax2.plot(steps, best["particles"], color="C3", label="particles")
    ax2.set_ylabel("mean particle number")
    ax2.grid(False)

    ax = axes[0, 1]
    ax.plot(steps[1:], best["emitted_power"][1:], color="C1")
    ax.set_xlabel("step")
    ax.set_ylabel("emitted energy")
    ax.set_title("Emission accelerates")

    ax = axes[1, 0]
    for n in best["particle_numbers"]:
        key = f"sector_prob_N{int(n)}"
        ax.plot(steps, best[key], label=f"N={int(n)}")
    ax.set_xlabel("step")
    ax.set_ylabel("sector probability")
    ax.set_title("Shrinking sectors")
    ax.legend(frameon=False, fontsize=7, ncol=2)

    ax = axes[1, 1]
    labels = []
    min_acc = []
    mean_acc = []
    for row in grouped[::-1]:
        mu, gap, emin, emax = row["key"]
        labels.append(f"mu={mu:g}, gap={gap:g}\n[{emin:g},{emax:g}]")
        min_acc.append(row["min_acc"])
        mean_acc.append(row["mean_acc"])
    y = np.arange(len(labels))
    ax.barh(y, min_acc, color="C0", alpha=0.75, label="min over seeds")
    ax.plot(mean_acc, y, "o", color="C3", label="mean")
    ax.axvline(1.0, color="0.25", linewidth=1.0)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("mid / early emitted power")
    ax.set_title("Robust scan cases")
    ax.legend(frameon=False, fontsize=7)

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
