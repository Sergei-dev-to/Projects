#!/usr/bin/env python3
"""Plot Step 3 Bose-Hubbard emission probe results."""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def read_scan(path: pathlib.Path) -> list[dict[str, float | str]]:
    rows = []
    with path.open() as fh:
        for row in csv.DictReader(fh):
            parsed: dict[str, float | str] = {}
            for key, value in row.items():
                if key == "operator_mode":
                    parsed[key] = value
                else:
                    parsed[key] = float(value)
            rows.append(parsed)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        type=pathlib.Path,
        default=DATADIR / "bose_hubbard_emission_markov.npz",
    )
    parser.add_argument(
        "--scan",
        type=pathlib.Path,
        default=DATADIR / "bose_hubbard_emission_markov_scan.csv",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "step3_bose_hubbard_emission_probe.pdf",
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

    run = np.load(args.run)
    scan = read_scan(args.scan)
    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.0))

    steps = np.arange(len(run["energy"]))
    ax = axes[0]
    ax.plot(steps, run["energy"], color="C0")
    ax.axhspan(-22.44, -18.17, color="C3", alpha=0.12, label="convex DOS window")
    ax.set_xlabel("step")
    ax.set_ylabel("mean core energy")
    ax.set_title("Best DOS candidate")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.plot(steps[1:], run["emitted_power"][1:], color="C1")
    ax.set_xlabel("step")
    ax.set_ylabel("energy emitted")
    ax.set_title("Emission decelerates")

    ax = axes[2]
    modes = ["density", "hopping", "both"]
    data = []
    labels = []
    for mode in modes:
        vals = [
            float(row["accel_ratio_mid_over_early"])
            for row in scan
            if row["operator_mode"] == mode
            and float(row["initial_e_min"]) == -18.5
            and float(row["initial_e_max"]) == -17.0
        ]
        data.append(vals)
        labels.append(mode)
    ax.boxplot(data, labels=labels, showfliers=True)
    ax.axhline(1.0, color="0.25", linewidth=1.0)
    ax.set_ylabel("mid / early emitted power")
    ax.set_title("Local-operator scan")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
