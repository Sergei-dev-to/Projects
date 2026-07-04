#!/usr/bin/env python3
"""Geometry schematic for concentric charged shells in an Ellis wormhole.

The shells are surfaces x = const in

    dl^2 = dx^2 + r(x)^2 dOmega^2,   r(x)=sqrt(x^2+a^2).

In a meridional embedding-style diagram they are vertical cross-sections at
fixed x, not off-axis objects.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_PNG = Path("fig_concentric_shell_geometry.png")
OUT_PDF = Path("fig_concentric_shell_geometry.pdf")

A = 1.0


def r_of_x(x: np.ndarray | float) -> np.ndarray | float:
    return np.sqrt(np.asarray(x) * np.asarray(x) + A * A)


def main() -> None:
    x = np.linspace(-6.0, 8.5, 1200)
    r = r_of_x(x)
    shell_positions = [7.0, 3.5, 1.35]
    colors = ["#8b78c6", "#3f8fc5", "#c43c39"]
    labels = ["early", "middle", "late"]

    fig, ax = plt.subplots(figsize=(11.2, 4.9), constrained_layout=True)

    ax.fill_between(x, -r, r, color="#f2f2f2", alpha=1.0, zorder=0)
    ax.plot(x, r, color="0.18", lw=1.6)
    ax.plot(x, -r, color="0.18", lw=1.6)
    ax.axvline(0.0, color="0.25", lw=1.2)
    ax.text(-0.35, -2.05, "throat\n$x=0$", ha="right", va="top", fontsize=10)

    # Draw shell cross-sections x=X.  Each full spherical shell is represented
    # in the meridional section by the vertical diameter at fixed x.
    for x0, color, label in zip(shell_positions, colors, labels):
        rr = float(r_of_x(x0))
        ax.plot([x0, x0], [-rr, rr], color=color, lw=2.2)
        ax.scatter([x0, x0], [-rr, rr], color=color, s=18, zorder=3)
        if label == "early":
            xytext = (x0 - 1.8, rr + 0.45)
            ha = "left"
        elif label == "middle":
            xytext = (x0 - 2.35, rr + 0.35)
            ha = "left"
        else:
            xytext = (x0 - 2.1, rr + 0.35)
            ha = "left"
        ax.text(*xytext, rf"{label}: $X={x0:g}a$", ha=ha,
                color=color, fontsize=9)

    # Indicate inward motion along the radial coordinate x.
    ax.annotate(
        "inward motion",
        xy=(2.0, -8.35),
        xytext=(5.8, -8.35),
        ha="center",
        va="center",
        arrowprops={"arrowstyle": "->", "lw": 1.4, "color": "0.25"},
        color="0.2",
        fontsize=10,
    )

    text_box = {"boxstyle": "round,pad=0.18", "fc": "white", "ec": "none", "alpha": 0.78}
    ax.text(-4.7, 3.35, r"$x<0$ end", ha="center", fontsize=10, bbox=text_box)
    ax.text(6.5, 3.35, r"$x>0$ source end", ha="center", fontsize=10, bbox=text_box)
    ax.set_xlabel(r"wormhole coordinate $x/a$")
    ax.set_ylabel(r"areal radius $r/a$")
    ax.set_xlim(-6.0, 8.5)
    ax.set_ylim(-9.3, 8.9)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(r"concentric charged shell: surface $x=X$ in an Ellis wormhole")
    ax.grid(alpha=0.18)

    fig.savefig(OUT_PNG, dpi=180)
    fig.savefig(OUT_PDF)
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
