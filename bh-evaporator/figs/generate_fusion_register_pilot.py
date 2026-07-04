#!/usr/bin/env python3
"""Plot Fibonacci fusion-register pilot diagnostics."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def load(operator: str, mass_law: str, seed: int):
    return np.load(DATADIR / f"fusion_register_{operator}_{mass_law}_seed{seed}.npz")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--output", type=pathlib.Path, default=PROJECT / "fusion_register_pilot.pdf")
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

    cases = [
        ("fusion", "sqrt", "C0", "fusion, sqrt"),
        ("scrambled", "sqrt", "C1", "scrambled, sqrt"),
        ("fusion", "linear", "C2", "fusion, linear"),
        ("scrambled", "linear", "C3", "scrambled, linear"),
    ]
    runs = [(load(op, law, args.seed), color, label) for op, law, color, label in cases]
    steps = np.arange(len(runs[0][0]["energy"]))

    fig, axes = plt.subplots(2, 2, figsize=(8.0, 5.8))

    ax = axes[0, 0]
    for run, color, label in runs:
        ax.plot(steps[1:], run["emitted_power"][1:], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("emitted energy")
    ax.set_title("Emission")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    for run, color, label in runs:
        ax.plot(steps, run["area"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("mean anyon number n")
    ax.set_title("Shrinking fusion register")

    ax = axes[1, 0]
    for run, color, label in runs:
        ax.plot(steps[1:], run["w_actual"][1:], color=color, label=label)
        ax.plot(steps[1:], run["sector_w"][1:], color=color, linestyle="--", alpha=0.65)
    ax.set_xlabel("step")
    ax.set_ylabel("W")
    ax.set_title("Actual W and sector W")

    ax = axes[1, 1]
    for run, color, label in runs:
        ax.plot(steps, run["renyi2_core"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("S2(core)")
    ax.set_title("Reduced-channel entropy")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
