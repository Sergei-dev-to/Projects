#!/usr/bin/env python3
"""Plot the tiny full-radiation area-register diagnostic."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def load_case(operator: str, mass_law: str, seed: int):
    path = DATADIR / f"area_register_full_radiation_tiny_{operator}_{mass_law}_seed{seed}.npz"
    return np.load(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "track_b_full_radiation_tiny.pdf",
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
        ("local", "sqrt", "C0", "local, sqrt mass"),
        ("scrambled", "sqrt", "C1", "scrambled, sqrt mass"),
        ("local", "linear", "C2", "local, linear mass"),
        ("scrambled", "linear", "C3", "scrambled, linear mass"),
    ]
    runs = [(load_case(op, law, args.seed), color, label) for op, law, color, label in cases]
    steps = np.arange(len(runs[0][0]["energy"]))

    fig, axes = plt.subplots(2, 2, figsize=(8.0, 5.8))

    ax = axes[0, 0]
    for run, color, label in runs:
        ax.plot(steps[1:], run["emitted_power"][1:], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("emitted energy")
    ax.set_title("Emission rate")
    ax.legend(frameon=False, fontsize=7)

    ax = axes[0, 1]
    for run, color, label in runs:
        ax.plot(steps, run["area"], color=color, label=label)
    ax.set_xlabel("step")
    ax.set_ylabel("mean area register n")
    ax.set_title("Shrinking register")

    ax = axes[1, 0]
    for run, color, label in runs:
        ax.plot(steps, run["renyi2_core"], color=color, label=label)
        ax.plot(steps, run["renyi2_radiation"], color=color, linestyle="--", alpha=0.7)
    ax.set_xlabel("step")
    ax.set_ylabel("Renyi-2 entropy")
    ax.set_title("Core and total radiation")

    ax = axes[1, 1]
    for run, color, label in runs:
        ax.plot(steps, run["renyi2_early_late_mutual"], color=color, label=label)
    ax.axvline(int(runs[0][0]["split_step"]), color="0.4", linestyle=":", linewidth=1.0)
    ax.set_xlabel("step")
    ax.set_ylabel("S2(E)+S2(L)-S2(EL)")
    ax.set_title("Early/late radiation diagnostic")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
