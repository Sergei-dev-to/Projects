#!/usr/bin/env python3
"""Plot Track B area-register Kraus diagnostics."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        type=pathlib.Path,
        default=DATADIR / "area_register_kraus_local_seed2468.npz",
    )
    parser.add_argument(
        "--scrambled",
        type=pathlib.Path,
        default=DATADIR / "area_register_kraus_scrambled_seed2468.npz",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "track_b_area_register_kraus.pdf",
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

    runs = [np.load(args.local), np.load(args.scrambled)]
    labels = ["local removal", "scrambled removal"]
    colors = ["C0", "C1"]
    steps = np.arange(len(runs[0]["energy"]))

    fig, axes = plt.subplots(2, 2, figsize=(7.6, 5.4))

    ax = axes[0, 0]
    for run, label, color in zip(runs, labels, colors):
        ax.plot(steps, run["energy"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("energy")
    ax.set_title("Energy decreases")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    for run, label, color in zip(runs, labels, colors):
        ax.plot(steps[1:], run["emitted_power"][1:], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("emitted energy")
    ax.set_title("Kraus acceleration")

    ax = axes[1, 0]
    for run, label, color in zip(runs, labels, colors):
        ax.plot(steps, run["dimension_entropy"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("dimension entropy")
    ax.set_title("Area entropy shrinks")

    ax = axes[1, 1]
    for run, label, color in zip(runs, labels, colors):
        ax.plot(steps, run["renyi2_core"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("S2(core) = S2(rad)")
    ax.set_title("Core-radiation entropy grows")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
