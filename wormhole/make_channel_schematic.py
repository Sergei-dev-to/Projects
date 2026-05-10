"""Generate the v5 channel schematic figure.

The figure is deliberately schematic: it separates the forbidden passive
monopole channel from the two allowed channels that remain in the paper.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Rectangle


BLUE = "#2f6f9f"
RED = "#b23b3b"
GREEN = "#3a7d44"
GOLD = "#b88420"
INK = "#222222"
MUTED = "#6b7280"
PANEL = "#f7f5ee"
TUBE = "#e8edf3"


def setup_axis(ax, title: str, subtitle: str) -> None:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.8)
    ax.set_aspect("auto")
    ax.axis("off")
    ax.add_patch(Rectangle((0.12, 0.12), 9.76, 5.56, fc=PANEL, ec="#d8d2c4", lw=1.0))
    ax.text(0.45, 5.38, title, fontsize=16.5, fontweight="bold", ha="left", va="top", color=INK)
    ax.text(0.45, 4.92, subtitle, fontsize=12.2, ha="left", va="top", color=MUTED)


def draw_wormhole(ax) -> None:
    # Two mouths connected by a throat, drawn as a cartoon geometry plus a
    # translucent worldtube surrounding the throat.
    ax.add_patch(Rectangle((4.25, 1.65), 1.5, 2.0, fc=TUBE, ec="#9aa7b5", lw=1.0, alpha=0.75))
    ax.text(5.0, 1.42, r"$\mathcal{W}$", fontsize=13, ha="center", va="top", color=MUTED)

    ax.add_patch(Ellipse((3.35, 2.65), 1.05, 1.8, fc="white", ec=INK, lw=1.35))
    ax.add_patch(Ellipse((6.65, 2.65), 1.05, 1.8, fc="white", ec=INK, lw=1.35))
    ax.plot([3.35, 4.35], [3.35, 3.2], color=INK, lw=1.15)
    ax.plot([3.35, 4.35], [1.95, 2.1], color=INK, lw=1.15)
    ax.plot([5.65, 6.65], [3.2, 3.35], color=INK, lw=1.15)
    ax.plot([5.65, 6.65], [2.1, 1.95], color=INK, lw=1.15)
    ax.text(3.35, 2.65, "A", fontsize=13.0, color=MUTED, ha="center", va="center")
    ax.text(6.65, 2.65, "B", fontsize=13.0, color=MUTED, ha="center", va="center")


def arrow(ax, xy0, xy1, color=INK, lw=1.6, style="-|>", mutation_scale=13, **kwargs) -> None:
    ax.add_patch(
        FancyArrowPatch(
            xy0,
            xy1,
            arrowstyle=style,
            mutation_scale=mutation_scale,
            lw=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            **kwargs,
        )
    )


def draw_cross(ax, x: float, y: float, size: float = 0.42, color: str = RED) -> None:
    ax.plot([x - size, x + size], [y - size, y + size], color=color, lw=2.2)
    ax.plot([x - size, x + size], [y + size, y - size], color=color, lw=2.2)


def panel_forbidden(ax) -> None:
    setup_axis(ax, "Forbidden channel", "source near B moves; no throat flux")
    draw_wormhole(ax)

    # Hidden source motion near B.
    ax.add_patch(Circle((7.85, 2.2), 0.13, fc=INK, ec=INK))
    ax.add_patch(Circle((7.35, 3.25), 0.09, fc=INK, ec=INK, alpha=0.35))
    arrow(ax, (7.42, 3.12), (7.78, 2.38), color=INK, lw=1.2, mutation_scale=10)
    ax.text(7.8, 1.85, "source\nmotion", fontsize=11.2, ha="center", va="top")

    # No crossing of the worldtube.
    ax.plot([4.0, 6.0], [4.03, 4.03], color=RED, lw=1.5, ls="--")
    draw_cross(ax, 5.0, 4.03, 0.20, RED)
    ax.text(5.0, 4.34, "no current or stress-energy flux", fontsize=11.0, ha="center", color=RED)

    # Crossed-out changing monopole at A.
    for r in [0.35, 0.62, 0.9]:
        ax.add_patch(Circle((2.35, 2.65), r, fill=False, ec=RED, lw=1.15, alpha=0.85))
    draw_cross(ax, 2.35, 2.65, 0.62, RED)
    ax.text(1.15, 4.05, r"monopole fixed", fontsize=14.0, color=RED, ha="left")
    ax.text(0.75, 0.75, r"cross-throat $1/r$ induction is absent", fontsize=11.8, ha="left", color=INK)


def panel_multipoles(ax) -> None:
    setup_axis(ax, "Allowed channel", r"higher multipoles and waves")
    draw_wormhole(ax)

    # Wavy wave path through the throat.
    xs = [7.6, 6.8, 6.0, 5.2, 4.4, 3.6, 2.7]
    ys = [3.8, 3.2, 3.75, 3.05, 3.55, 2.95, 3.35]
    ax.plot(xs, ys, color=BLUE, lw=2.0)
    arrow(ax, (3.05, 3.28), (2.65, 3.37), color=BLUE, lw=1.4, mutation_scale=10)

    # Dipole-like pattern at A.
    ax.add_patch(Ellipse((2.2, 2.95), 0.75, 0.42, angle=25, fc="#d9e8f5", ec=BLUE, lw=1.0))
    ax.add_patch(Ellipse((2.2, 2.25), 0.75, 0.42, angle=-25, fc="#f2d8d8", ec=RED, lw=1.0))
    ax.text(1.0, 4.35, r"$\ell\geq 1$", fontsize=15, color=BLUE)
    ax.text(0.72, 1.15, r"potential $\sim r^{-(\ell+1)}$", fontsize=11.6, ha="left")
    ax.text(0.72, 0.84, r"finite throat: $\mathcal{T}_\ell\sim e^{-\sqrt{\ell(\ell+1)}L/R}$", fontsize=10.0, ha="left")
    ax.text(6.95, 4.15, "waves may\nscatter", fontsize=11.0, ha="center", color=BLUE)


def panel_flux(ax) -> None:
    setup_axis(ax, "Allowed channel", "actual transit or boundary work")
    draw_wormhole(ax)

    # Particle/radiation crossing the worldtube.
    ax.add_patch(Circle((6.95, 2.65), 0.12, fc=GOLD, ec="#6f4e0f", lw=0.8))
    arrow(ax, (7.0, 2.65), (3.1, 2.65), color=GOLD, lw=2.2, mutation_scale=15)
    ax.text(5.0, 3.85, "flux through\nworldtube", fontsize=11.2, ha="center", color=GOLD)

    # Boundary work indication.
    arrow(ax, (4.2, 1.45), (4.2, 1.0), color=GREEN, lw=1.4, mutation_scale=11)
    arrow(ax, (5.8, 1.0), (5.8, 1.45), color=GREEN, lw=1.4, mutation_scale=11)
    ax.text(5.0, 0.92, "geometry can do work", fontsize=11.0, ha="center", color=GREEN)

    ax.text(0.72, 4.35, r"$\Delta E_{\mathcal{W}}\neq 0$", fontsize=15, color=GOLD, ha="left")
    ax.text(0.72, 1.36, "Brown--York balance", fontsize=11.8, ha="left", color=INK)
    ax.text(0.72, 1.07, "transit or backreaction", fontsize=11.8, ha="left", color=INK)


def main() -> None:
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 9.2), constrained_layout=True)
    panel_forbidden(axes[0])
    panel_multipoles(axes[1])
    panel_flux(axes[2])
    fig.savefig("fig_channel_schematic.pdf", bbox_inches="tight")
    fig.savefig("fig_channel_schematic.png", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
