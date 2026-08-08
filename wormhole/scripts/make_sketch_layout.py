"""
Make a figure closer to the user's sketch:
- left column: three stacked exact Ellis--Bronnikov snapshots
- right column: one schematic bookkeeping panel for post-transit separation

Outputs:
- fig5_sketch_layout.pdf
- fig5_sketch_layout.png
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Circle, FancyArrowPatch

from make_ellis_crosssection import (
    W,
    E,
    LAMBDA_FIXED,
    tunnel_radius,
    v_lambda,
)


def setup_panel(ax, title=""):
    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, fontsize=11, loc="left")


def draw_geometry(ax):
    x = np.linspace(-4.8, 4.8, 800)
    r = tunnel_radius(x)
    ax.plot(x, r, color="black", lw=1.6)
    ax.plot(x, -r, color="black", lw=1.6)
    ax.fill_between(x, -r, r, color="#f5f7fb", zorder=0)


def exact_snapshot(ax, l0, note):
    x = np.linspace(-4.8, 4.8, 700)
    y = np.linspace(-3.0, 3.0, 420)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(1.0 + X**2)
    mask = np.abs(Y) <= R
    s = np.zeros_like(X)
    s[mask] = Y[mask] / R[mask]
    costh = np.zeros_like(X)
    costh[mask] = np.sqrt(np.maximum(0.0, 1.0 - s[mask] ** 2))

    V = np.full_like(X, np.nan, dtype=float)
    V[mask] = v_lambda(X[mask], costh[mask], l0, LAMBDA_FIXED, W, E)
    finite = np.isfinite(V)
    vmax = np.nanpercentile(V[finite], 97.0)
    vmin = np.nanpercentile(V[finite], 8.0)
    Vplot = np.clip(V, vmin, vmax)

    draw_geometry(ax)

    # Filled field map plus sparse contours for readability
    levels = np.linspace(vmin, vmax, 24)
    ax.contourf(X, Y, Vplot, levels=levels, cmap="coolwarm", alpha=0.85)
    pos = np.linspace(max(0.08 * vmax, 0.02), vmax * 0.92, 6)
    neg = np.linspace(min(-0.02, 0.85 * vmin), -0.02, 4) if vmin < 0 else np.array([])
    if neg.size:
        ax.contour(X, Y, Vplot, levels=neg, colors="#2aa745", linewidths=1.0, linestyles="dashed")
    ax.contour(X, Y, Vplot, levels=pos, colors="#c92e2e", linewidths=1.0)

    ax.plot([l0], [0], "ko", ms=6, zorder=5)
    ax.text(l0 + 0.12, 0.18, r"$+q$", fontsize=11)

    ax.text(
        0.98, 0.92, note,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9.5,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="0.55", alpha=0.92),
    )

    setup_panel(ax)


def bookkeeping_panel(ax):
    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Post-transit bookkeeping", fontsize=12)

    # Tunnel
    x = np.linspace(-4.4, 4.4, 500)
    top = 0.55 + 0.12 * np.exp(-(x / 2.2) ** 2)
    bot = -top
    ax.plot(x, top, color="black", lw=1.8)
    ax.plot(x, bot, color="black", lw=1.8)
    ax.fill_between(x, bot, top, color="#f4f4f4")

    # Mouth cross-sections
    ax.plot([-3.0, -3.0], [-0.7, 0.7], color="0.35", lw=2.0)
    ax.plot([ 3.0,  3.0], [-0.7, 0.7], color="0.35", lw=2.0)

    # Flux lines inside tunnel
    for yy in [-0.25, 0.0, 0.25]:
        ax.plot(np.linspace(-2.9, 2.9, 120), yy * np.ones(120), color="#5a6e8a", lw=1.3)

    # Apparent mouth charges
    ax.text(-3.95, 0.9, r"$+q$", fontsize=14, color="#b55a00")
    ax.text( 2.55, 1.55, r"$-q$", fontsize=14, color="#2b6cb0")
    ax.text( 3.25, 1.08, r"$+q$", fontsize=14, color="#b55a00")

    # Emerged particle
    ax.plot([4.0], [0.0], "ko", ms=7)
    ax.text(4.14, 0.16, r"$+q$", fontsize=12)

    # Local Gaussian surfaces
    ax.add_patch(Circle((4.0, 0.0), 0.55, fill=False, ec="0.45", ls="--", lw=1.3))
    ax.add_patch(Circle((3.0, 0.0), 0.9, fill=False, ec="0.55", ls=":", lw=1.3))
    ax.add_patch(Circle((-3.0, 0.0), 0.9, fill=False, ec="0.55", ls=":", lw=1.3))

    # End Gaussians
    ax.add_patch(Circle((-4.1, 0.0), 0.65, fill=False, ec="0.4", ls="--", lw=1.2))
    ax.add_patch(Circle((4.75, 0.0), 0.65, fill=False, ec="0.4", ls="--", lw=1.2))

    # Labels
    ax.text(-4.65, 2.45, r"$Q_+ = +q$", fontsize=10)
    ax.text( 2.65, 2.45, r"$Q_- = 0$", fontsize=10)
    ax.text(-4.65, -2.25, r"$q^{L}_{\rm enc} = +q$", fontsize=9.5, color="0.35")
    ax.text( 2.15, -2.25, r"$q^{R}_{\rm enc} = -q$", fontsize=9.5, color="0.35")
    ax.text(0.15, 2.45, r"$Q_{\rm wh}\ \to\ Q_{\rm wh}+q$", fontsize=10.5)

    ax.text(
        0.02, 0.10,
        "Asymptotic end charges stay fixed.\n"
        "Finite enclosed charges around the mouths change.\n"
        "After transit, the transported object and the mouths can each\n"
        "look locally monopolar even though the far-end charges are unchanged.",
        transform=ax.transAxes,
        fontsize=9.5,
        ha="left",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", edgecolor="0.6", alpha=0.93),
    )

    # Small arrows
    ax.add_patch(FancyArrowPatch((3.15, 0.58), (3.85, 0.18), arrowstyle="->", mutation_scale=11, lw=1.1))
    ax.add_patch(FancyArrowPatch((-3.15, 0.58), (-3.85, 0.18), arrowstyle="->", mutation_scale=11, lw=1.1))


def make_figure():
    fig = plt.figure(figsize=(14.5, 9.5))
    gs = GridSpec(3, 2, width_ratios=[1.05, 1.25], hspace=0.22, wspace=0.18)

    left_stages = [
        (-3.6, "1. Far from the mouth", "fixed sector: $Q_+=+q$, $Q_-=0$, $Q_{\\rm wh}=0$"),
        (-1.45, "2. Near the mouth", "field distorts strongly, but no opposite-end monopole is induced"),
        (0.0, "3. At the throat", "exact center snapshot from the summed Boisseau--Linet solution"),
    ]

    for i, (l0, title, note) in enumerate(left_stages):
        ax = fig.add_subplot(gs[i, 0])
        exact_snapshot(ax, l0, note)
        ax.set_title(title, fontsize=12, loc="left")

    axr = fig.add_subplot(gs[:, 1])
    bookkeeping_panel(axr)

    fig.suptitle(
        "Field evolution and charge bookkeeping in the conservation-preserving Ellis--Bronnikov sector",
        fontsize=13,
        y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig("fig5_sketch_layout.pdf", bbox_inches="tight")
    fig.savefig("fig5_sketch_layout.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig5_sketch_layout.pdf")
    print("wrote fig5_sketch_layout.png")


if __name__ == "__main__":
    make_figure()
