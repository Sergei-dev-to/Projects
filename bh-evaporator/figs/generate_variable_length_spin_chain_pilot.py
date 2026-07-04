#!/usr/bin/env python3
"""Plot variable-length spin-chain pilot diagnostics."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def load(block: str, operator: str, mass_law: str, seed: int):
    return np.load(DATADIR / f"variable_length_spin_chain_{block}_{operator}_{mass_law}_seed{seed}.npz")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--block-model", default="local")
    parser.add_argument("--output", type=pathlib.Path, default=PROJECT / "variable_length_spin_chain_pilot.pdf")
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
        ("boundary", "sqrt", "C0", "boundary, sqrt"),
        ("bulk", "sqrt", "C1", "bulk, sqrt"),
        ("scrambled", "sqrt", "C2", "scrambled, sqrt"),
        ("boundary", "linear", "C3", "boundary, linear"),
    ]
    runs = [(load(args.block_model, op, law, args.seed), color, label) for op, law, color, label in cases]
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
    ax.set_ylabel("mean chain length n")
    ax.set_title("Shrinking chain")

    ax = axes[1, 0]
    for run, color, label in runs:
        ax.plot(steps[1:], run["w_actual"][1:], color=color, label=label)
        ax.plot(steps[1:], run["sector_w"][1:], color=color, linestyle="--", alpha=0.6)
    ax.set_xlabel("step")
    ax.set_ylabel("W")
    ax.set_title("Actual W and sector W")

    ax = axes[1, 1]
    for run, color, label in runs:
        ax.plot(steps, run["selection_ratio"], color=color, label=label)
    ax.axhline(1.0, color="0.5", linestyle=":", linewidth=1)
    ax.set_xlabel("step")
    ax.set_ylabel("selection ratio")
    ax.set_title("Intrasection selection")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
