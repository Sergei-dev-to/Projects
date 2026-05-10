"""Spacetime worldtube schematic for Theorem 1 of the paper.

Layout: time vertical, one suppressed spatial direction. Two horizontal
spatial slices at t=t1 and t=t2. Mouth A and mouth B sit on each slice.
A blue closed loop S_t surrounds mouth A on each slice. The vertical
translucent cylinder T = union_t S_t is the conserved object: a spacetime
worldtube, not a spatial surface. A green source worldline near mouth B
runs alongside T from t1 to t2 without ever piercing it.

A small inset shows the spatial-Gauss alternative (S = boundary of a
3-ball V) crossed out, to forestall the wrong intuition explicitly.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, Polygon
from matplotlib.lines import Line2D


def draw_slice(ax, y, x_left, x_right, depth, color, label=None, label_x=None):
    """Draw a horizontal spatial slice as a parallelogram (perspective)."""
    x_back_left = x_left + depth * 0.6
    x_back_right = x_right + depth * 0.6
    y_back = y + depth
    pts = [
        (x_left, y),
        (x_right, y),
        (x_back_right, y_back),
        (x_back_left, y_back),
    ]
    poly = Polygon(pts, closed=True, facecolor="#f0f0f0", edgecolor="#a0a0a0",
                   lw=1.0, alpha=0.7, zorder=1)
    ax.add_patch(poly)
    if label is not None:
        ax.text(label_x if label_x is not None else x_left - 0.15,
                y + depth * 0.5, label, fontsize=15, ha="right", va="center",
                color="#444444")


def draw_mouth(ax, x, y, depth_offset, label=None, label_below=False):
    """Draw a mouth (small circle with center dot) at perspective-shifted position."""
    cx = x + depth_offset * 0.6
    cy = y + depth_offset
    ax.add_patch(Ellipse((cx, cy), 0.42, 0.20, fill=False,
                         edgecolor="#222222", lw=1.5, zorder=4))
    ax.add_patch(Ellipse((cx, cy), 0.13, 0.06, color="#222222", zorder=5))
    if label is not None:
        if label_below:
            ax.text(cx, cy - 0.30, label, ha="center", va="top",
                    fontsize=15, color="#222222")
        else:
            ax.text(cx + 0.30, cy + 0.05, label, ha="left", va="center",
                    fontsize=15, color="#222222")
    return cx, cy


def draw_loop(ax, cx, cy, label=None, color="#245b8f", label_offset=(-1.0, 0.4)):
    """Draw a closed 2-surface S_t as an ellipse at given center."""
    ax.add_patch(Ellipse((cx, cy), 1.05, 0.50, fill=False,
                         edgecolor=color, lw=2.4, zorder=6))
    if label is not None:
        ax.text(cx + label_offset[0], cy + label_offset[1], label,
                color=color, fontsize=18, ha="center", va="center")


def draw_cylinder(ax, x_center, y_bottom_center, y_top_center, depth_offset,
                  color="#245b8f", alpha=0.18):
    """Draw the vertical worldtube T as a translucent cylinder.

    Two ellipses (top and bottom) connected by vertical sides.
    """
    cx = x_center + depth_offset * 0.6
    cy_bot = y_bottom_center + depth_offset
    cy_top = y_top_center + depth_offset
    rx, ry = 0.525, 0.25  # match the loop ellipses
    # Side fill (a quadrilateral approximating the visible cylinder side)
    side_pts = [
        (cx - rx, cy_bot),
        (cx + rx, cy_bot),
        (cx + rx, cy_top),
        (cx - rx, cy_top),
    ]
    side = Polygon(side_pts, closed=True, facecolor=color, alpha=alpha,
                   edgecolor=color, lw=1.0, zorder=2)
    ax.add_patch(side)
    # Faint vertical generators on the sides
    for xs in [cx - rx, cx + rx]:
        ax.plot([xs, xs], [cy_bot, cy_top], color=color, lw=1.0,
                alpha=0.6, zorder=3)


def draw_source_worldline(ax, x_center, y_bottom_center, y_top_center,
                          depth_offset, color="#3f7f4f"):
    """Draw a wavy green worldline next to mouth B going from t1 to t2."""
    cx = x_center + depth_offset * 0.6 + 0.85  # offset to the right of mouth B
    ys = np.linspace(y_bottom_center + depth_offset,
                     y_top_center + depth_offset, 200)
    # Small horizontal wiggle to read as a worldline that "moves"
    xs = cx + 0.18 * np.sin(2.5 * (ys - ys[0]))
    ax.plot(xs, ys, color=color, lw=2.0, zorder=5)
    # Two event dots
    ax.add_patch(Ellipse((xs[40], ys[40]), 0.10, 0.10, color=color, zorder=6))
    ax.add_patch(Ellipse((xs[160], ys[160]), 0.10, 0.10, color=color, zorder=6))
    return cx


def draw_no_cross_marker(ax, x, y, color="#3f7f4f"):
    """Small ✗ on the cylinder side indicating no current crosses T."""
    s = 0.12
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=1.8, zorder=7)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=1.8, zorder=7)


def draw_time_axis(ax, x, y_bottom, y_top):
    arr = FancyArrowPatch((x, y_bottom), (x, y_top + 0.25),
                          arrowstyle="->", mutation_scale=14,
                          color="#666666", lw=1.2)
    ax.add_patch(arr)
    ax.text(x - 0.05, y_top + 0.55, "time", ha="right", va="bottom",
            fontsize=14, color="#666666")


def draw_inset_spatial_gauss(ax):
    """Small 'NOT this' inset: spatial Gauss surface bounding a 3-ball V,
    crossed out to indicate inapplicability for non-separating surfaces."""
    # Inset axes in upper-right corner
    inset = ax.inset_axes([0.74, 0.66, 0.24, 0.30])
    inset.set_xlim(-1.4, 1.4)
    inset.set_ylim(-1.6, 1.0)
    inset.set_aspect("equal")
    inset.axis("off")
    # Title above the figure
    inset.text(0, 0.95, "NOT this:", ha="center", va="bottom",
               fontsize=12, color="#7a1a1a", style="italic")
    # The 3-ball V (filled disk) and its boundary S
    inset.add_patch(Ellipse((0, 0), 1.6, 0.95, facecolor="#fde4e4",
                            edgecolor="#b03030", lw=1.5))
    inset.text(0, 0, "V", ha="center", va="center", fontsize=14,
               color="#7a1a1a")
    # Big red ✗ (drawn first, label drawn on top)
    inset.plot([-1.25, 1.25], [-0.85, 0.85], color="#b03030", lw=2.8,
               alpha=0.7)
    inset.plot([-1.25, 1.25], [0.85, -0.85], color="#b03030", lw=2.8,
               alpha=0.7)
    # Label S = boundary V positioned outside the X crossing point
    inset.text(-1.35, 0.55, r"$S=\partial V$", color="#7a1a1a",
               fontsize=12, ha="right", va="center",
               bbox=dict(facecolor='white', edgecolor='none', alpha=0.85,
                         boxstyle='round,pad=0.15'))
    inset.text(0, -1.25, "spatial Gauss requires\n$S$ to bound a 3-ball $V$",
               ha="center", va="top", fontsize=11, color="#7a1a1a")


def main():
    fig, ax = plt.subplots(figsize=(11.0, 8.8))
    ax.set_xlim(-0.8, 9.2)
    ax.set_ylim(-2.2, 6.5)
    ax.set_aspect("equal")
    ax.axis("off")

    blue = "#245b8f"
    green = "#3f7f4f"

    # Two slices: t=t1 (bottom) at y=0, t=t2 (top) at y=3.6
    y_bot = 0.0
    y_top = 3.6
    depth = 0.55
    x_left, x_right = 0.6, 7.2

    draw_slice(ax, y_bot, x_left, x_right, depth, "#f0f0f0",
               label="$t=t_1$", label_x=x_left - 0.15)
    draw_slice(ax, y_top, x_left, x_right, depth, "#f0f0f0",
               label="$t=t_2$", label_x=x_left - 0.15)

    # Mouth A on each slice (left). Mouth B on each slice (right).
    x_a = 2.0
    x_b = 5.5
    cx_a_bot, cy_a_bot = draw_mouth(ax, x_a, y_bot, 0.0,
                                    label="mouth A", label_below=True)
    cx_b_bot, cy_b_bot = draw_mouth(ax, x_b, y_bot, 0.0,
                                    label="mouth B", label_below=True)
    cx_a_top, cy_a_top = draw_mouth(ax, x_a, y_top, 0.0)
    cx_b_top, cy_b_top = draw_mouth(ax, x_b, y_top, 0.0)

    # Loops S_{t1}, S_{t2} around mouth A
    draw_loop(ax, cx_a_bot, cy_a_bot, label=r"$S_{t_1}$", color=blue,
              label_offset=(-0.95, -0.05))
    draw_loop(ax, cx_a_top, cy_a_top, label=r"$S_{t_2}$", color=blue,
              label_offset=(-0.95, -0.05))

    # Worldtube cylinder T connecting them
    draw_cylinder(ax, x_a, y_bot, y_top, 0.0, color=blue, alpha=0.18)
    ax.text(cx_a_bot + 0.85, (y_bot + y_top) / 2 + 0.35,
            r"$\mathcal{T}=\bigcup_t \, S_t$",
            color=blue, fontsize=18, ha="left", va="center")

    # Source worldline near mouth B
    cx_src = draw_source_worldline(ax, x_b, y_bot, y_top, 0.0, color=green)
    ax.text(cx_src + 0.55, (y_bot + y_top) / 2,
            "source motion\nnear B", ha="left", va="center",
            fontsize=14, color=green)

    # No-current marker on cylinder side
    draw_no_cross_marker(ax, cx_a_bot + 0.525, (y_bot + y_top) / 2 + 0.15,
                         color=green)
    ax.text(cx_a_bot + 0.7, (y_bot + y_top) / 2 - 0.25,
            r"no current crosses $\mathcal{T}$",
            color=green, fontsize=14, ha="left", va="center")

    # Conserved-flux equation, below the diagram (and above the bottom note)
    ax.text((x_left + x_right) / 2, y_bot - 1.25,
            r"$\int_{S_{t_1}}\!\star F \;=\; \int_{S_{t_2}}\!\star F$",
            ha="center", va="center", fontsize=20, color=blue)

    # Time axis
    draw_time_axis(ax, x_left - 0.5, y_bot - 0.1, y_top + 0.4)

    # Bottom note
    ax.text((x_left + x_right) / 2, -2.05,
            r"$S_t$ need not bound any spatial 3-region; "
            r"conservation is a 4D Stokes statement on $\mathcal{T}$.",
            ha="center", va="bottom", fontsize=14, color="#444444",
            style="italic")

    fig.tight_layout(pad=0.1)
    fig.savefig("fig_worldtube_stokes.pdf", bbox_inches="tight")
    fig.savefig("fig_worldtube_stokes.png", dpi=220, bbox_inches="tight")


if __name__ == "__main__":
    main()
