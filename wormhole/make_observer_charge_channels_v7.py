"""Generate the v7 charge-balance channel schematic.

The observer-side measuring surface, rather than a cut through the throat, is
the boundary relevant to the Maxwell and Iyer--Wald balance laws.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch, Rectangle


BLUE = "#286f9f"
RED = "#b23b3b"
GOLD = "#b88420"
INK = "#222222"
MUTED = "#667085"
PANEL = "#f8f7f2"
THROAT = "#e8edf3"


def arrow(ax, xy0, xy1, color=INK, lw=1.6, mutation_scale=13, **kwargs) -> None:
    ax.add_patch(
        FancyArrowPatch(
            xy0,
            xy1,
            arrowstyle="-|>",
            mutation_scale=mutation_scale,
            lw=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            **kwargs,
        )
    )


def setup_axis(ax, title: str, subtitle: str) -> None:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    ax.add_patch(Rectangle((0.12, 0.16), 9.76, 5.88, fc=PANEL, ec="#d8d2c4", lw=1.0))
    ax.text(0.48, 5.74, title, fontsize=17.0, fontweight="bold", ha="left", va="top", color=INK)
    ax.text(0.48, 5.22, subtitle, fontsize=13.0, ha="left", va="top", color=MUTED)


def draw_geometry(ax) -> None:
    """Draw two mouths and the observer-side measuring surface S_t."""
    ax.add_patch(Rectangle((4.25, 2.15), 1.5, 1.45, fc=THROAT, ec="#a8b2bf", lw=1.0))
    ax.add_patch(Ellipse((3.48, 2.88), 0.95, 1.52, fc="white", ec=INK, lw=1.35))
    ax.add_patch(Ellipse((6.52, 2.88), 0.95, 1.52, fc="white", ec=INK, lw=1.35))
    ax.plot([3.48, 4.28], [3.48, 3.38], color=INK, lw=1.05)
    ax.plot([3.48, 4.28], [2.28, 2.38], color=INK, lw=1.05)
    ax.plot([5.72, 6.52], [3.38, 3.48], color=INK, lw=1.05)
    ax.plot([5.72, 6.52], [2.38, 2.28], color=INK, lw=1.05)
    ax.text(3.48, 2.88, "A", fontsize=12.0, color=MUTED, ha="center", va="center")
    ax.text(6.52, 2.88, "B", fontsize=12.0, color=MUTED, ha="center", va="center")

    # Spatial section of the fixed observer-side measuring worldtube.
    ax.add_patch(Ellipse((3.48, 2.88), 2.35, 3.55, fill=False, ec=BLUE, lw=2.0))
    ax.text(3.48, 4.38, r"measuring surface $S_t$", fontsize=10.5, color=BLUE, ha="center")


def draw_source_motion(ax) -> None:
    ax.add_patch(Circle((8.20, 2.30), 0.13, fc=INK, ec=INK))
    ax.add_patch(Circle((7.72, 3.55), 0.09, fc=INK, ec=INK, alpha=0.35))
    arrow(ax, (7.78, 3.40), (8.14, 2.50), color=INK, lw=1.15, mutation_scale=10)
    ax.text(8.16, 1.98, "source motion", fontsize=11.5, ha="center", va="top")


def panel_fixed(ax) -> None:
    setup_axis(ax, "Fixed monopole", "no source flux across measuring tube")
    draw_geometry(ax)
    draw_source_motion(ax)
    ax.plot([2.0, 4.95], [1.02, 1.02], color=RED, lw=1.4, ls="--")
    ax.plot([3.25, 3.70], [0.78, 1.26], color=RED, lw=2.0)
    ax.plot([3.25, 3.70], [1.26, 0.78], color=RED, lw=2.0)
    ax.text(3.48, 0.52, r"$\delta H_\xi(t_2)=\delta H_\xi(t_1)$", fontsize=12.0, color=RED, ha="center")


def panel_multipoles(ax) -> None:
    setup_axis(ax, "Allowed response", r"higher modes; fixed $\ell=0$ charge")
    draw_geometry(ax)
    xs = [8.1, 7.35, 6.62, 5.88, 5.15, 4.42, 3.72, 2.98, 2.15]
    ys = [3.72, 3.25, 3.62, 3.10, 3.55, 3.00, 3.44, 2.95, 3.32]
    ax.plot(xs, ys, color=BLUE, lw=2.0)
    arrow(ax, (2.55, 3.18), (2.12, 3.33), color=BLUE, lw=1.4, mutation_scale=10)
    ax.add_patch(Ellipse((1.55, 2.62), 0.82, 0.43, angle=25, fc="#d8eaf6", ec=BLUE, lw=1.0))
    ax.add_patch(Ellipse((1.55, 2.02), 0.82, 0.43, angle=-25, fc="#f2d8d8", ec=RED, lw=1.0))
    ax.text(3.30, 0.72, "higher modes and waves", fontsize=12.5, color=BLUE, ha="center")


def panel_sourced(ax) -> None:
    setup_axis(ax, "Charge can change", "source flux across measuring tube")
    draw_geometry(ax)
    ax.add_patch(Circle((6.95, 2.88), 0.13, fc=GOLD, ec="#6f4e0f", lw=0.8))
    arrow(ax, (6.82, 2.88), (2.55, 2.88), color=GOLD, lw=2.2, mutation_scale=15)
    ax.text(
        8.10,
        3.55,
        "first-order\nsource flux",
        fontsize=11.5,
        ha="center",
        va="bottom",
        color=GOLD,
        linespacing=1.25,
    )
    ax.text(3.48, 0.82, r"$\delta H_\xi(t_2)-\delta H_\xi(t_1)$", fontsize=12.0, color=GOLD, ha="center")
    ax.text(3.48, 0.48, r"$=-\int_{\mathcal{T}}\delta C_\xi$", fontsize=12.0, color=GOLD, ha="center")


def main() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.7))
    fig.subplots_adjust(left=0.012, right=0.988, top=0.985, bottom=0.025, wspace=0.045)
    panel_fixed(axes[0])
    panel_multipoles(axes[1])
    panel_sourced(axes[2])
    fig.savefig("fig_observer_charge_channels_v7.pdf", bbox_inches="tight")
    fig.savefig("fig_observer_charge_channels_v7.png", dpi=240, bbox_inches="tight")


if __name__ == "__main__":
    main()
