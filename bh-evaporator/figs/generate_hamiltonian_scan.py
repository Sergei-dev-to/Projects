#!/usr/bin/env python3
"""Generate heatmaps for the Hamiltonian density-channel scan."""
from __future__ import annotations

import argparse
import pathlib

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_density_scan.npz",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "hamiltonian_density_scan.pdf",
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
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    data = np.load(args.input)
    curvatures = data["curvatures"]
    channels = data["channels"]
    g_values = data["g_values"]
    accel = data["accel_ratio"]

    fig, axes = plt.subplots(1, len(curvatures), figsize=(9.0, 2.8), sharey=True)
    if len(curvatures) == 1:
        axes = [axes]

    vmin = min(0.0, float(np.nanmin(accel)))
    vmax = max(1.25, float(np.nanmax(accel)))
    image = None
    for i, curvature in enumerate(curvatures):
        ax = axes[i]
        image = ax.imshow(
            accel[i],
            origin="lower",
            aspect="auto",
            vmin=vmin,
            vmax=vmax,
            cmap="viridis",
        )
        ax.contour(
            np.arange(len(g_values)),
            np.arange(len(channels)),
            accel[i],
            levels=[1.0],
            colors="white",
            linewidths=1.0,
        )
        ax.set_title(f"curvature {curvature:g}")
        ax.set_xticks(np.arange(len(g_values)), [f"{g:g}" for g in g_values])
        ax.set_yticks(np.arange(len(channels)), [str(int(c)) for c in channels])
        ax.set_xlabel("g")
        if i == 0:
            ax.set_ylabel("channels")
        for y in range(len(channels)):
            for x in range(len(g_values)):
                ax.text(
                    x,
                    y,
                    f"{accel[i, y, x]:.2f}",
                    ha="center",
                    va="center",
                    color="white" if accel[i, y, x] < 0.75 else "black",
                    fontsize=7,
                )

    assert image is not None
    cbar = fig.colorbar(image, ax=axes, shrink=0.88)
    cbar.set_label("mid/early emitted-power ratio")
    fig.savefig(args.output, bbox_inches="tight")
    print(f"[figs] wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
