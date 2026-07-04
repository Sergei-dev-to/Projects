#!/usr/bin/env python3
"""Plot Track B area-register rate kill-test results."""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def read_rows(path: pathlib.Path) -> list[dict[str, float | str]]:
    rows = []
    with path.open() as fh:
        for row in csv.DictReader(fh):
            if row.get("error"):
                continue
            parsed: dict[str, float | str] = {}
            for key, value in row.items():
                if key in {"operator", "mass_law"}:
                    parsed[key] = value
                elif value != "":
                    parsed[key] = float(value)
            rows.append(parsed)
    return rows


def grouped(rows):
    buckets = defaultdict(list)
    for row in rows:
        buckets[(row["operator"], row["mass_law"], row["max_gap"])].append(row)
    out = []
    for key, vals in buckets.items():
        if len(vals) < 2:
            continue
        acc = np.array([v["accel_ratio_mid_over_early"] for v in vals], dtype=float)
        early = np.array([v["mean_power_early"] for v in vals], dtype=float)
        mid = np.array([v["mean_power_mid"] for v in vals], dtype=float)
        late = np.array([v["mean_power_late"] for v in vals], dtype=float)
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
    return sorted(out, key=lambda item: item["mean_acc"], reverse=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scan",
        type=pathlib.Path,
        default=DATADIR / "area_register_rate_scan_wide.csv",
    )
    parser.add_argument(
        "--best",
        type=pathlib.Path,
        default=DATADIR / "area_register_rate_wide_best.npz",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "track_b_area_register_rate_scan.pdf",
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
    best = np.load(args.best)
    fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.2))

    ax = axes[0]
    x = np.arange(len(best["area_grid"]))
    ax.plot(best["area_grid"], best["mass_grid"], "o-", color="C0", label="M")
    ax2 = ax.twinx()
    ax2.plot(best["area_grid"], best["temperature_grid"], "s-", color="C3", label="T")
    ax.invert_xaxis()
    ax.set_xlabel("area register n")
    ax.set_ylabel("mass")
    ax2.set_ylabel("temperature")
    ax.set_title("BH-like scaling")
    ax2.grid(False)

    ax = axes[1]
    steps = np.arange(len(best["energy"]))
    ax.plot(steps[1:], best["emitted_power"][1:], color="C1")
    ax.set_xlabel("step")
    ax.set_ylabel("emitted energy")
    ax.set_title("Best matrix-element run")

    ax = axes[2]
    selected = [
        row
        for row in rows
        if row["key"][2] in {4.0, 8.0, 10.0, 12.0}
        and (row["key"][1] == "sqrt" and row["key"][2] == 4.0 or row["key"][1] == "linear")
    ]
    selected = sorted(selected, key=lambda row: (row["key"][1], row["key"][0], row["key"][2]))
    labels = []
    vals = []
    for row in selected:
        op, mass, gap = row["key"]
        labels.append(f"{mass}, {op}\ngap={gap:g}")
        vals.append(row["min_acc"])
    y = np.arange(len(labels))
    ax.barh(y, vals, color=["C0" if "sqrt" in label else "C2" for label in labels])
    ax.axvline(1.0, color="0.25", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("min mid/early over seeds")
    ax.set_title("Controls")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
