#!/usr/bin/env python3
"""Static potential profiles for a concentric shell in an Ellis wormhole.

Uses the same shell-position colors as fig_concentric_shell_geometry:
early/middle/late shell positions in the fixed-flux sector, plus a contrast
with the zero-potential-at-both-infinities Dirichlet sector.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


OUT_PNG = Path("fig_shell_static_profiles.png")
OUT_PDF = Path("fig_shell_static_profiles.pdf")

A = 1.0
Q = 1.0
SHELL_POSITIONS = [7.0, 3.5, 1.35]
COLORS = ["#8b78c6", "#3f8fc5", "#c43c39"]
LABELS = ["early", "middle", "late"]


def integral_from_to(x1: np.ndarray | float, x2: np.ndarray | float) -> np.ndarray | float:
    return (Q / A) * (np.arctan(np.asarray(x2) / A) - np.arctan(np.asarray(x1) / A))


def fixed_flux_phi(x: np.ndarray, x_shell: float) -> np.ndarray:
    """Phi(+infty)=0, zero flux on the x<X side."""
    out = np.empty_like(x)
    left = x <= x_shell
    out[left] = integral_from_to(x_shell, np.inf)
    out[~left] = integral_from_to(x[~left], np.inf)
    return out


def dirichlet_phi(x: np.ndarray, x_shell: float) -> np.ndarray:
    """Static solution with Phi(-infty)=Phi(+infty)=0."""
    i_left = integral_from_to(-np.inf, x_shell)
    i_right = integral_from_to(x_shell, np.inf)
    i_total = i_left + i_right
    d_left = Q * i_right / i_total
    d_right = d_left - Q

    out = np.empty_like(x)
    left = x <= x_shell
    out[left] = d_left * integral_from_to(-np.inf, x[left])
    out[~left] = -d_right * integral_from_to(x[~left], np.inf)
    return out


def main() -> None:
    x = np.linspace(-12.0, 12.0, 1800)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8), constrained_layout=True)

    ax = axes[0]
    for x0, color, label in zip(SHELL_POSITIONS, COLORS, LABELS):
        ax.plot(x, fixed_flux_phi(x, x0), color=color, lw=2.0,
                label=rf"{label}: $X={x0:g}a$")
        ax.axvline(x0, color=color, lw=0.9, ls="--", alpha=0.55)
    ax.axvline(0.0, color="0.25", lw=1.1)
    ax.text(0.0, 0.045, "throat", ha="center", va="bottom", fontsize=9)
    ax.set_xlabel(r"wormhole coordinate $x/a$")
    ax.set_ylabel(r"potential $\Phi$")
    ax.set_title("fixed-flux sector: far end is a voltage plateau")
    ax.set_xlim(-10.0, 10.0)
    ax.set_ylim(-0.02, 0.95)
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    ax = axes[1]
    x0 = SHELL_POSITIONS[1]
    color = COLORS[1]
    ax.plot(x, fixed_flux_phi(x, x0), color=color, lw=2.2,
            label="fixed flux")
    ax.plot(x, dirichlet_phi(x, x0), color="0.15", lw=1.9, ls="--",
            label=r"$\Phi_+=\Phi_-=0$")
    ax.axvline(0.0, color="0.25", lw=1.1)
    ax.axvline(x0, color=color, lw=0.9, ls="--", alpha=0.55)
    ax.text(x0 + 0.18, 0.07, rf"shell $X={x0:g}a$", color=color, fontsize=9)
    ax.annotate(
        "Dirichlet sector has\nfar-side slope/flux",
        xy=(-6.0, float(dirichlet_phi(np.array([-6.0]), x0)[0])),
        xytext=(-8.6, 0.36),
        arrowprops={"arrowstyle": "->", "lw": 1.1, "color": "0.2"},
        ha="left",
        fontsize=9,
    )
    ax.annotate(
        "fixed-flux sector has\nflat far-side potential",
        xy=(-6.0, float(fixed_flux_phi(np.array([-6.0]), x0)[0])),
        xytext=(-8.8, 0.68),
        arrowprops={"arrowstyle": "->", "lw": 1.1, "color": color},
        ha="left",
        color=color,
        fontsize=9,
    )
    ax.set_xlabel(r"wormhole coordinate $x/a$")
    ax.set_ylabel(r"potential $\Phi$")
    ax.set_title("same shell position, different static sectors")
    ax.set_xlim(-10.0, 10.0)
    ax.set_ylim(-0.02, 0.95)
    ax.grid(alpha=0.22)
    ax.legend(frameon=False, fontsize=9, loc="upper right")

    fig.savefig(OUT_PNG, dpi=180)
    fig.savefig(OUT_PDF)
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
