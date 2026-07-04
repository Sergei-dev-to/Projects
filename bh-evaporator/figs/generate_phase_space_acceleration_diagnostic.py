#!/usr/bin/env python3
"""Plot outgoing phase-space acceleration diagnostics."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def load(name: str):
    return np.load(DATADIR / name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "phase_space_acceleration_diagnostic.pdf",
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

    cases = [
        (load(f"phase_space_area_local_sqrt_seed{args.seed}.npz"), "C0", "area sqrt"),
        (load(f"phase_space_area_local_linear_seed{args.seed}.npz"), "C1", "area linear"),
        (load(f"phase_space_varn_seed{args.seed}.npz"), "C2", "variable-N Bose-Hubbard"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(8.0, 5.8))

    ax = axes[0, 0]
    for run, color, label in cases:
        steps = np.arange(len(run["predicted_power"]))
        ax.plot(steps[1:], run["predicted_power"][1:], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("state-averaged W")
    ax.set_title("Outgoing weighted phase space")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[0, 1]
    for run, color, label in cases:
        steps = np.arange(len(run["jump_probability"]))
        ax.plot(steps[1:], run["jump_probability"][1:], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("jump probability")
    ax.set_title("Escape probability")

    ax = axes[1, 0]
    for run, color, label in cases:
        steps = np.arange(len(run["conditional_omega"]))
        ax.plot(steps[1:], run["conditional_omega"][1:], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("mean emitted energy | jump")
    ax.set_title("Emission energy")

    ax = axes[1, 1]
    for run, color, label in cases:
        steps = np.arange(len(run["mean_sector"]))
        ax.plot(steps, run["mean_sector"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("mean sector")
    ax.set_title("Shrinking sector")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
