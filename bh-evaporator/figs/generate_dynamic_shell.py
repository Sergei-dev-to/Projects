#!/usr/bin/env python3
"""Generate a compact summary figure for the dynamic shell evaporator."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--convex",
        type=pathlib.Path,
        default=DATADIR / "dynamic_shell_evaporator.npz",
    )
    parser.add_argument(
        "--control",
        type=pathlib.Path,
        default=DATADIR / "dynamic_shell_evaporator_linear_control.npz",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "dynamic_shell_summary.pdf",
    )
    args = parser.parse_args(argv)

    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except Exception as exc:
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

    convex = np.load(args.convex)
    control = np.load(args.control)

    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.2))
    ax = axes[0, 0]
    ax.plot(convex["energies"][:-1], convex["emit_probability"][:-1], marker="o", label="convex")
    ax.plot(control["energies"][:-1], control["emit_probability"][:-1], marker="s", label="linear")
    ax.invert_xaxis()
    ax.set_xlabel("core energy shell")
    ax.set_ylabel("emission probability")
    ax.legend(frameon=False)

    ax = axes[0, 1]
    ax.plot(convex["steps"], convex["mean_energy_mean"], label="convex")
    ax.plot(control["steps"], control["mean_energy_mean"], label="linear")
    ax.set_xlabel("step")
    ax.set_ylabel("mean core energy")
    ax.legend(frameon=False)

    ax = axes[1, 0]
    ax.plot(convex["steps"], convex["emitted_power_mean"], label="convex")
    ax.plot(control["steps"], control["emitted_power_mean"], label="linear")
    ax.set_xlabel("step")
    ax.set_ylabel("emitted energy / step")
    ax.legend(frameon=False)

    ax = axes[1, 1]
    ax.plot(convex["steps"], convex["s2_rad_mean"], label="convex")
    ax.plot(control["steps"], control["s2_rad_mean"], label="linear")
    ax.plot(convex["steps"], convex["micro_s_at_mean_mean"], color="C0", ls="--", alpha=0.6)
    ax.plot(control["steps"], control["micro_s_at_mean_mean"], color="C1", ls="--", alpha=0.6)
    ax.set_xlabel("step")
    ax.set_ylabel("radiation Renyi-2")
    ax.legend(frameon=False)

    fig.tight_layout()
    fig.savefig(args.output, bbox_inches="tight")
    print(f"[figs] wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
