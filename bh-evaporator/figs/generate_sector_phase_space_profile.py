#!/usr/bin/env python3
"""Plot sector-level W profile diagnostics."""
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


def arr(rows, key):
    return np.asarray([float(row[key]) for row in rows], dtype=float)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=DATADIR / "sector_phase_space_profile.csv",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "sector_phase_space_profile.pdf",
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
    groups = [
        ("area", "C0", "area register"),
        ("variable_n_bose_hubbard", "C2", "variable-N Bose-Hubbard"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.5))

    ax = axes[0]
    for model, color, label in groups:
        subset = [row for row in rows if row["model"] == model]
        ax.scatter(
            arr(subset, "observed_accel"),
            arr(subset, "sector_w_mid_over_early"),
            s=28,
            alpha=0.8,
            color=color,
            label=label,
        )
    lims = [0.45, 1.45]
    ax.plot(lims, lims, color="0.4", linestyle="--", linewidth=1)
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.axvline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlim(lims)
    ax.set_ylim(lims)
    ax.set_xlabel("observed power mid/early")
    ax.set_ylabel("sector-only W mid/early")
    ax.set_title("Sector trajectory")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    for model, color, label in groups:
        subset = [row for row in rows if row["model"] == model]
        ax.scatter(
            arr(subset, "observed_accel"),
            arr(subset, "structural_ratio_all_lower_over_initial"),
            s=28,
            alpha=0.8,
            color=color,
            label=label,
        )
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.axvline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("observed power mid/early")
    ax.set_ylabel("mean lower-sector W / initial W")
    ax.set_title("Pre-evolution profile")

    ax = axes[2]
    for model, color, label in groups:
        subset = [row for row in rows if row["model"] == model]
        ax.scatter(
            arr(subset, "sector_reconstruction_mean_relerr"),
            arr(subset, "selection_mid_over_early"),
            s=28,
            alpha=0.8,
            color=color,
            label=label,
        )
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("mean relative error")
    ax.set_ylabel("selection ratio mid/early")
    ax.set_title("Intrasection selection")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
