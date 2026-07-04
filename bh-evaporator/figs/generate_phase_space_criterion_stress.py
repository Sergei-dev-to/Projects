#!/usr/bin/env python3
"""Plot W-criterion stress-test results."""
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
        "--input",
        type=pathlib.Path,
        default=DATADIR / "phase_space_criterion_stress_test.csv",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "phase_space_criterion_stress_test.pdf",
    )
    parser.add_argument(
        "--shell-input",
        type=pathlib.Path,
        default=DATADIR / "shell_phase_space_diagnostic.csv",
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

    rows = read_rows(args.input)
    shell_rows = read_rows(args.shell_input) if args.shell_input.exists() else []
    groups = [
        ("area", "C0", "area register"),
        ("variable_n_bose_hubbard", "C2", "variable-N Bose-Hubbard"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.6))

    ax = axes[0]
    for model, color, label in groups:
        subset = [row for row in rows if row["model"] == model]
        actual = np.asarray([float(row["actual_accel"]) for row in subset])
        pred = np.asarray([float(row["w_accel"]) for row in subset])
        ax.scatter(actual, pred, s=28, alpha=0.8, color=color, label=label)
    if shell_rows:
        actual = np.asarray([float(row["power_mid_over_early"]) for row in shell_rows])
        pred = np.asarray([float(row["w_mid_over_early"]) for row in shell_rows])
        ax.scatter(
            actual,
            pred,
            s=54,
            alpha=0.9,
            color="C4",
            marker="D",
            label="engineered shell",
        )
    lims = [0.55, 1.5]
    ax.plot(lims, lims, color="0.4", linestyle="--", linewidth=1)
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.axvline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel("observed power mid/early")
    ax.set_ylabel("W diagnostic mid/early")
    ax.set_title("Criterion classification")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    for model, color, label in groups:
        subset = [row for row in rows if row["model"] == model]
        jump = np.asarray([float(row["jump_accel"]) for row in subset])
        omega = np.asarray([float(row["omega_accel"]) for row in subset])
        ax.scatter(jump, omega, s=28, alpha=0.8, color=color, label=label)
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.axvline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("jump probability mid/early")
    ax.set_ylabel("conditional energy mid/early")
    ax.set_title("What drives W")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
