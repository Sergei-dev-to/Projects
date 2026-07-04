#!/usr/bin/env python3
"""Plot variable-length spin-chain robustness scan."""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def read_rows(path: pathlib.Path):
    with path.open(newline="") as fh:
        return list(csv.DictReader(fh))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--summary",
        type=pathlib.Path,
        default=DATADIR / "variable_length_spin_chain_robustness_summary.csv",
    )
    parser.add_argument(
        "--advantage",
        type=pathlib.Path,
        default=DATADIR / "variable_length_spin_chain_robustness_advantage.csv",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "variable_length_spin_chain_robustness.pdf",
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

    summary = read_rows(args.summary)
    advantage = read_rows(args.advantage)
    bandwidths = sorted({float(row["bandwidth"]) for row in summary})
    operators = ["boundary", "bulk", "scrambled"]
    colors = {"boundary": "C0", "bulk": "C1", "scrambled": "C2"}

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.6))

    ax = axes[0]
    for operator in operators:
        for mass_law, linestyle in [("sqrt", "-"), ("linear", "--")]:
            rows = [
                row
                for row in summary
                if row["operator"] == operator and row["mass_law"] == mass_law
            ]
            rows = sorted(rows, key=lambda row: float(row["bandwidth"]))
            ax.plot(
                [float(row["bandwidth"]) for row in rows],
                [float(row["accel_mean"]) for row in rows],
                color=colors[operator],
                linestyle=linestyle,
                marker="o",
                label=f"{operator} {mass_law}",
            )
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("bandwidth")
    ax.set_ylabel("mean mid/early power")
    ax.set_title("Acceleration")
    ax.legend(frameon=False, fontsize=7, ncol=2)

    ax = axes[1]
    for operator in operators:
        rows = [
            row
            for row in summary
            if row["operator"] == operator and row["mass_law"] == "sqrt"
        ]
        rows = sorted(rows, key=lambda row: float(row["bandwidth"]))
        ax.plot(
            [float(row["bandwidth"]) for row in rows],
            [float(row["sector_w_mean"]) for row in rows],
            color=colors[operator],
            marker="o",
            label=operator,
        )
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("bandwidth")
    ax.set_ylabel("mean sector-W ratio")
    ax.set_title("Sqrt sector profile")

    ax = axes[2]
    for operator, marker in [("boundary", "o"), ("bulk", "s")]:
        for mass_law, linestyle in [("sqrt", "-"), ("linear", "--")]:
            rows = [
                row
                for row in advantage
                if row["operator"] == operator and row["mass_law"] == mass_law
            ]
            means = []
            for bandwidth in bandwidths:
                vals = [
                    float(row["accel_advantage"])
                    for row in rows
                    if float(row["bandwidth"]) == bandwidth
                ]
                means.append(float(np.mean(vals)))
            ax.plot(
                bandwidths,
                means,
                color=colors[operator],
                linestyle=linestyle,
                marker=marker,
                label=f"{operator} {mass_law}",
            )
    ax.axhline(0.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("bandwidth")
    ax.set_ylabel("accel advantage over scrambled")
    ax.set_title("Local-removal advantage")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
