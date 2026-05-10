"""
Cross-section storyboard and animation for wormhole charge bookkeeping.

This version drops the previous meridional half-plane look and uses a
true left-right cross-section through the wormhole tunnel.

Outputs:
- fig4_crosssection_storyboard.pdf
- fig4_crosssection_storyboard.png
- wormhole_crosssection_story.gif
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle, PathPatch
from matplotlib.path import Path


XMIN, XMAX = -6.0, 6.0
YMIN, YMAX = -2.5, 2.5


def tunnel_radius(x: np.ndarray) -> np.ndarray:
    throat = 0.55
    exterior = 1.65
    scale = 2.8
    return throat + (exterior - throat) * (1.0 - np.exp(-(np.abs(x) / scale) ** 2))


def draw_wormhole(ax: plt.Axes) -> None:
    x = np.linspace(XMIN, XMAX, 800)
    r = tunnel_radius(x)
    ax.fill_between(x, -r, r, color="#eef3ff", zorder=0)
    ax.plot(x, r, color="black", lw=1.5)
    ax.plot(x, -r, color="black", lw=1.5)
    ax.axvline(0, color="0.75", lw=0.7, ls=":")


def draw_gaussians(ax: plt.Axes, q_plus: str, q_minus: str, q_left_mouth: str, q_right_mouth: str) -> None:
    end_style = dict(fill=False, ls="--", lw=1.3, ec="0.35")
    mouth_style = dict(fill=False, ls=":", lw=1.3, ec="0.45")

    ax.add_patch(Circle((-4.65, 0), 0.85, **end_style))
    ax.add_patch(Circle((4.65, 0), 0.85, **end_style))
    ax.add_patch(Circle((-1.05, 0), 0.82, **mouth_style))
    ax.add_patch(Circle((1.05, 0), 0.82, **mouth_style))

    ax.text(-5.75, 1.36, rf"$Q_+ = {q_plus}$", fontsize=9, color="0.25")
    ax.text(3.82, 1.36, rf"$Q_- = {q_minus}$", fontsize=9, color="0.25")
    ax.text(-2.0, -1.98, rf"$q^{{L}}_{{\rm enc}} = {q_left_mouth}$", fontsize=8.8, color="0.35")
    ax.text(0.42, -1.98, rf"$q^{{R}}_{{\rm enc}} = {q_right_mouth}$", fontsize=8.8, color="0.35")


def bezier(ax: plt.Axes, points, color, lw=1.5, ls="-", alpha=1.0) -> None:
    verts = [points[0], points[1], points[2], points[3]]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
    patch = PathPatch(Path(verts, codes), fill=False, lw=lw, ls=ls, ec=color, alpha=alpha)
    ax.add_patch(patch)


def draw_field_lines(ax: plt.Axes, stage: str, source_x: float) -> None:
    blue = "#2a6fdb"
    red = "#cf2f2f"
    green = "#2aa745"
    amber = "#d08b00"

    # Left-side source lines
    if stage in {"far", "near", "crossing"}:
        starts = [(source_x, 0.0), (source_x, 0.0), (source_x, 0.0), (source_x, 0.0)]
        ends = [(-5.7, 1.4), (-5.7, 0.4), (-5.7, -0.4), (-5.7, -1.4)]
        ctrls = [
            ((source_x - 0.7, 1.0), (-4.9, 1.4)),
            ((source_x - 0.9, 0.4), (-4.8, 0.5)),
            ((source_x - 0.9, -0.4), (-4.8, -0.5)),
            ((source_x - 0.7, -1.0), (-4.9, -1.4)),
        ]
        for st, en, (c1, c2) in zip(starts, ends, ctrls):
            bezier(ax, [st, c1, c2, en], blue, lw=1.4)

    # Lines threading the throat / snagged on topology
    if stage == "far":
        bezier(ax, [(source_x, 0.0), (-2.9, 1.0), (-1.4, 0.95), (-0.2, 0.55)], amber, lw=1.6)
        bezier(ax, [(0.2, 0.45), (1.0, 0.9), (2.4, 1.05), (4.2, 0.7)], red, lw=1.5)
        bezier(ax, [(0.2, -0.45), (1.0, -0.9), (2.4, -1.05), (4.2, -0.7)], green, lw=1.5, ls="--")
    elif stage == "near":
        bezier(ax, [(source_x, 0.0), (-1.8, 1.1), (-0.8, 0.95), (-0.05, 0.55)], amber, lw=1.8)
        bezier(ax, [(0.1, 0.48), (0.9, 1.08), (2.2, 1.15), (4.55, 0.85)], red, lw=1.7)
        bezier(ax, [(0.1, -0.48), (0.9, -1.08), (2.2, -1.15), (4.55, -0.85)], green, lw=1.7, ls="--")
    elif stage == "crossing":
        bezier(ax, [(-0.12, 0.05), (0.05, 0.55), (0.55, 0.85), (1.35, 0.95)], amber, lw=1.9)
        bezier(ax, [(-0.1, -0.05), (0.05, -0.55), (0.55, -0.85), (1.35, -0.95)], amber, lw=1.9)
        bezier(ax, [(1.25, 0.9), (2.0, 1.2), (3.2, 1.0), (4.6, 0.6)], red, lw=1.6)
        bezier(ax, [(1.25, -0.9), (2.0, -1.2), (3.2, -1.0), (4.6, -0.6)], green, lw=1.6, ls="--")
    elif stage == "emerged":
        bezier(ax, [(-1.0, 0.55), (-0.3, 0.95), (0.5, 0.95), (1.2, 0.6)], amber, lw=1.8)
        bezier(ax, [(-1.0, -0.55), (-0.3, -0.95), (0.5, -0.95), (1.2, -0.6)], amber, lw=1.8)
        starts = [(source_x, 0.0), (source_x, 0.0), (source_x, 0.0)]
        ends = [(5.6, 1.25), (5.7, 0.1), (5.6, -1.25)]
        ctrls = [
            ((source_x + 0.5, 0.95), (4.8, 1.3)),
            ((source_x + 0.8, 0.2), (4.95, 0.2)),
            ((source_x + 0.5, -0.95), (4.8, -1.3)),
        ]
        for st, en, (c1, c2) in zip(starts, ends, ctrls):
            bezier(ax, [st, c1, c2, en], blue, lw=1.5)
    elif stage == "separated":
        bezier(ax, [(-1.0, 0.58), (-0.25, 1.0), (0.55, 0.98), (1.25, 0.62)], amber, lw=1.9)
        bezier(ax, [(-1.0, -0.58), (-0.25, -1.0), (0.55, -0.98), (1.25, -0.62)], amber, lw=1.9)
        starts = [(source_x, 0.0), (source_x, 0.0), (source_x, 0.0), (source_x, 0.0)]
        ends = [(5.75, 1.55), (5.8, 0.55), (5.8, -0.55), (5.75, -1.55)]
        ctrls = [
            ((source_x + 0.3, 0.75), (5.0, 1.55)),
            ((source_x + 0.55, 0.25), (5.05, 0.6)),
            ((source_x + 0.55, -0.25), (5.05, -0.6)),
            ((source_x + 0.3, -0.75), (5.0, -1.55)),
        ]
        for st, en, (c1, c2) in zip(starts, ends, ctrls):
            bezier(ax, [st, c1, c2, en], blue, lw=1.45)


def draw_source(ax: plt.Axes, x: float, y: float = 0.0) -> None:
    ax.plot([x], [y], "ko", ms=5.5, zorder=6)
    ax.text(x + 0.12, y + 0.16, r"$+q$", fontsize=10, zorder=6)


def add_state_box(ax: plt.Axes, qwh: str, note: str) -> None:
    txt = rf"$Q_{{\rm wh}} = {qwh}$" + "\n" + note
    ax.text(
        0.98, 0.97, txt,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", alpha=0.92, edgecolor="0.55"),
    )


STAGES = [
    dict(name="far", title="Approach from far away", source_x=-4.1, qwh="0",
         ql="0", qr="0", note=r"dipole induced on far side"),
    dict(name="near", title="Near the throat, no transit", source_x=-1.7, qwh="0",
         ql="0", qr="0", note=r"$Q_\pm$ fixed, no induced monopole"),
    dict(name="crossing", title="Transit through the throat", source_x=0.0, qwh=r"\uparrow",
         ql=r"\approx +q/2", qr=r"\approx -q/2", note=r"$Q_{\rm wh}$ shifts during crossing"),
    dict(name="emerged", title="Just emerged on side $-$", source_x=1.9, qwh="+q",
         ql="+q", qr="-q", note=r"end charges still unchanged"),
    dict(name="separated", title="Separated from the exit mouth", source_x=4.1, qwh="+q",
         ql="+q", qr="-q", note=r"local apparent charges, fixed asymptotics"),
]


def setup_panel(ax: plt.Axes, stage: dict) -> None:
    ax.clear()
    draw_wormhole(ax)
    draw_gaussians(ax, "+q", "0", stage["ql"], stage["qr"])
    draw_field_lines(ax, stage["name"], stage["source_x"])
    draw_source(ax, stage["source_x"])
    add_state_box(ax, stage["qwh"], stage["note"])
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(stage["title"], fontsize=11)


def make_storyboard() -> None:
    fig, axes = plt.subplots(1, 5, figsize=(16.5, 4.3))
    for ax, stage in zip(axes, STAGES):
        setup_panel(ax, stage)

    fig.suptitle(
        "Cross-section through the wormhole: asymptotic end charges stay fixed, "
        "finite Gaussian enclosed charges near the mouths change, and the harmonic "
        "label shifts only during actual transit.",
        fontsize=12,
        y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig("fig4_crosssection_storyboard.pdf", bbox_inches="tight")
    fig.savefig("fig4_crosssection_storyboard.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig4_crosssection_storyboard.pdf")
    print("wrote fig4_crosssection_storyboard.png")


def interpolate_stage(i0: int, i1: int, t: float) -> dict:
    s0 = STAGES[i0]
    s1 = STAGES[i1]
    return dict(
        name=s0["name"] if t < 0.5 else s1["name"],
        title=s1["title"],
        source_x=(1 - t) * s0["source_x"] + t * s1["source_x"],
        qwh=s0["qwh"] if t < 0.5 else s1["qwh"],
        ql=s0["ql"] if t < 0.5 else s1["ql"],
        qr=s0["qr"] if t < 0.5 else s1["qr"],
        note=s1["note"],
    )


def make_gif() -> None:
    fig, ax = plt.subplots(figsize=(7.8, 4.5))

    timeline = []
    timeline += [STAGES[0]] * 6
    timeline += [interpolate_stage(0, 1, t) for t in np.linspace(0, 1, 10)]
    timeline += [STAGES[1]] * 5
    timeline += [interpolate_stage(1, 2, t) for t in np.linspace(0, 1, 8)]
    timeline += [STAGES[2]] * 5
    timeline += [interpolate_stage(2, 3, t) for t in np.linspace(0, 1, 8)]
    timeline += [STAGES[3]] * 5
    timeline += [interpolate_stage(3, 4, t) for t in np.linspace(0, 1, 10)]
    timeline += [STAGES[4]] * 10

    def update(i):
        setup_panel(ax, timeline[i])
        ax.set_title(timeline[i]["title"], fontsize=12)
        return []

    ani = FuncAnimation(fig, update, frames=len(timeline), interval=180, blit=False)
    ani.save("wormhole_crosssection_story.gif", writer=PillowWriter(fps=6))
    plt.close(fig)
    print("wrote wormhole_crosssection_story.gif")


if __name__ == "__main__":
    make_storyboard()
    make_gif()
