#!/usr/bin/env python3
"""Generate polished Step 2 comparison figures with seed bands."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def sem(arr: np.ndarray) -> np.ndarray:
    if arr.shape[0] <= 1:
        return np.zeros(arr.shape[1:])
    return np.std(arr, axis=0, ddof=1) / np.sqrt(arr.shape[0])


def plot_band(ax, x, mean, err, label, color):
    ax.plot(x, mean, label=label, color=color)
    ax.fill_between(x, mean - err, mean + err, color=color, alpha=0.18, linewidth=0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--convex",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_shell_density_curv3_ch8_g05_s48_seeds12.npz",
    )
    parser.add_argument(
        "--linear",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_shell_density_linear_ch8_g05_s48_seeds12.npz",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "step2_hamiltonian_polished.pdf",
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
    linear = np.load(args.linear)
    steps = convex["steps"]

    fig, axes = plt.subplots(2, 2, figsize=(7.1, 5.2))

    ax = axes[0, 0]
    ax.plot(convex["energies"], convex["temperature"], marker="o", label="convex", color="C0")
    ax.plot(linear["energies"], linear["temperature"], marker="s", label="linear", color="C1")
    ax.invert_xaxis()
    ax.set_xlabel("core energy shell")
    ax.set_ylabel("microcanonical T")
    ax.legend(frameon=False)

    ax = axes[0, 1]
    plot_band(
        ax,
        steps,
        convex["mean_energy_mean"],
        sem(convex["mean_energy"]),
        "convex",
        "C0",
    )
    plot_band(
        ax,
        steps,
        linear["mean_energy_mean"],
        sem(linear["mean_energy"]),
        "linear",
        "C1",
    )
    ax.set_xlabel("collision step")
    ax.set_ylabel("mean core energy")
    ax.legend(frameon=False)

    ax = axes[1, 0]
    plot_band(
        ax,
        steps,
        convex["emitted_power_mean"],
        sem(convex["emitted_power"]),
        "convex",
        "C0",
    )
    plot_band(
        ax,
        steps,
        linear["emitted_power_mean"],
        sem(linear["emitted_power"]),
        "linear",
        "C1",
    )
    ax.set_xlabel("collision step")
    ax.set_ylabel("emitted energy / step")
    ax.legend(frameon=False)

    ax = axes[1, 1]
    plot_band(
        ax,
        steps,
        convex["s2_rad_mean"],
        sem(convex["s2_rad"]),
        "convex",
        "C0",
    )
    plot_band(
        ax,
        steps,
        linear["s2_rad_mean"],
        sem(linear["s2_rad"]),
        "linear",
        "C1",
    )
    ax.set_xlabel("collision step")
    ax.set_ylabel("radiation Renyi-2")
    ax.legend(frameon=False)

    fig.tight_layout()
    fig.savefig(args.output, bbox_inches="tight")
    print(f"[figs] wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
