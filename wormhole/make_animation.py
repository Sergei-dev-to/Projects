"""
Generate a wormhole transit storyboard and a simple animation.

Outputs:
1. fig4_transit_storyboard.pdf
   Five-panel 2x5 storyboard with:
   - two pre-transit panels using the existing short-throat electrostatic model
   - three schematic transit/post-transit bookkeeping panels

2. wormhole_transit_story.gif
   A lightweight animation emphasizing:
   - fixed asymptotic end charges Q_+, Q_-
   - changing finite Gaussian enclosed charges near the mouths
   - shift of the harmonic label Q_wh during transit

This first version is intentionally hybrid:
- exact pre-transit side- response from the existing electrostatic model
- schematic transit/post-transit bookkeeping

The point is to teach the conservation logic, not to provide a full
time-dependent field solve through throat crossing.
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, FancyArrowPatch

from make_figures import (
    B_coef,
    L_MAX,
    P,
    draw_mouth,
    phi_side1_from_cart,
)


R = 1.0
Q_PLUS = 1.0
Q_MINUS = 0.0


def format_charge(val: float) -> str:
    if abs(val) < 1e-10:
        return "0"
    if abs(val - 1.0) < 1e-10:
        return "+q"
    if abs(val + 1.0) < 1e-10:
        return "-q"
    return f"{val:+.2f} q"


def phi_side2_fixed_sector(rho: np.ndarray, z: np.ndarray, A: float) -> np.ndarray:
    r2 = np.sqrt(rho**2 + z**2) + 1e-12
    cos_t2 = z / r2
    phi2 = np.zeros_like(rho)
    for l in range(1, L_MAX + 1):
        phi2 = phi2 + B_coef(l, A, R, 1.0) * P(l, cos_t2) / r2 ** (l + 1)
    return phi2


def add_common_axes_style(ax: plt.Axes, title: str) -> None:
    ax.set_aspect("equal")
    ax.set_xlim(0, 4.0)
    ax.set_ylim(-4.0, 4.0)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=10)


def add_end_gaussian(ax: plt.Axes) -> None:
    color = "0.35"
    ax.add_patch(Circle((3.1, 0.0), 0.65, fill=False, ls="--", lw=1.2, ec=color))
    ax.text(2.55, 0.95, "end Gaussian", fontsize=8.0, color=color)


def add_mouth_gaussian(ax: plt.Axes) -> None:
    color = "0.45"
    ax.add_patch(Circle((0.0, 0.0), 1.35, fill=False, ls=":", lw=1.2, ec=color))
    ax.text(0.72, 1.55, "mouth Gaussian", fontsize=8.0, color=color)


def draw_exact_panel(ax: plt.Axes, A: float, side: str) -> None:
    N = 280
    extent_rho = 4.0
    extent_z = 4.0
    rho_1d = np.linspace(0.002, extent_rho, N)
    z_1d = np.linspace(-extent_z, extent_z, 2 * N)
    RHO, Z = np.meshgrid(rho_1d, z_1d)
    mouth_mask = np.sqrt(RHO**2 + Z**2) < R

    if side == "+":
        phi = phi_side1_from_cart(RHO, Z, A, R, 1.0)
        phi = np.where(~mouth_mask, phi, np.nan)
        levs_pos = np.array([0.03, 0.06, 0.10, 0.17, 0.28, 0.45, 0.72, 1.15, 1.8, 2.8, 4.5])
        levs = np.concatenate([-levs_pos[::-1], levs_pos])
        ax.contour(RHO, Z, phi, levels=levs, colors="C0", linewidths=0.75, linestyles="solid")
        if A <= extent_z:
            ax.plot([0], [A], "ko", ms=5, zorder=5)
            ax.text(0.18, A + 0.12, r"$+q$", fontsize=11)
    else:
        phi = phi_side2_fixed_sector(RHO, Z, A)
        phi = np.where(~mouth_mask, phi, np.nan)
        m2 = np.nanmax(np.abs(phi))
        if not np.isfinite(m2) or m2 <= 0:
            m2 = 1.0
        levs_pos = m2 * np.array([0.015, 0.035, 0.07, 0.13, 0.22, 0.35, 0.55, 0.80])
        ax.contour(RHO, Z, phi, levels=levs_pos, colors="C3", linewidths=0.85, linestyles="solid")
        ax.contour(RHO, Z, phi, levels=-levs_pos[::-1], colors="C2", linewidths=0.85, linestyles="dashed")
        ax.contour(RHO, Z, phi, levels=[0.0], colors="0.3", linewidths=0.7, linestyles="dotted")

    draw_mouth(ax, R)


def draw_schematic_panel(ax_top: plt.Axes, ax_bot: plt.Axes, phase: str) -> None:
    for ax, side in [(ax_top, "+"), (ax_bot, "-")]:
        draw_mouth(ax, R)
        add_common_axes_style(ax, f"side {side}")
        add_end_gaussian(ax)

    if phase == "crossing":
        add_mouth_gaussian(ax_top)
        add_mouth_gaussian(ax_bot)
        ax_top.plot([0], [0.6], "ko", ms=5)
        ax_top.text(0.15, 0.82, r"$+q$", fontsize=10)
        ax_bot.plot([0], [-0.6], "ko", ms=5)
        ax_bot.text(0.15, -0.38, r"$+q$", fontsize=10)
    elif phase == "emerged":
        add_mouth_gaussian(ax_top)
        add_mouth_gaussian(ax_bot)
        ax_bot.plot([0], [1.55], "ko", ms=5)
        ax_bot.text(0.15, 1.72, r"$+q$", fontsize=10)
        ax_bot.add_patch(FancyArrowPatch((0.22, 0.95), (0.08, 1.42), arrowstyle="->", mutation_scale=10, lw=1.0))
    elif phase == "separated":
        add_mouth_gaussian(ax_top)
        add_mouth_gaussian(ax_bot)
        ax_bot.plot([0], [2.45], "ko", ms=5)
        ax_bot.text(0.15, 2.62, r"$+q$", fontsize=10)
        for sgn in (-1, 1):
            ax_bot.add_patch(FancyArrowPatch((0.15, 0.8 * sgn), (0.15, 1.8 * sgn), arrowstyle="-", lw=1.2, color="C1"))
        ax_bot.add_patch(FancyArrowPatch((0.18, 0.95), (0.12, 2.25), arrowstyle="-", lw=1.2, color="C1"))

    ax_top.text(0.16, 3.35, r"$Q_{\mathrm{wh}}$: fixed $\to$ shifts during transit", fontsize=8.7, color="0.2")


def add_state_box(ax: plt.Axes, end_charge: str, mouth_charge: str, A_label: str, qwh_label: str) -> None:
    text = (
        rf"$Q_{{\rm end}} = {end_charge}$" + "\n" +
        rf"$q_{{\rm enc}}^{{\rm mouth}} = {mouth_charge}$" + "\n" +
        rf"$Q_{{\rm wh}} = {qwh_label}$" + "\n" +
        rf"$A/R = {A_label}$"
    )
    ax.text(
        0.98, 0.97, text,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", alpha=0.9, edgecolor="0.5"),
    )


def make_storyboard() -> None:
    fig, axes = plt.subplots(2, 5, figsize=(14.5, 6.2), sharex=True, sharey=True)

    # Panels 1-2: exact pre-transit
    for col, A in enumerate([5.0, 1.2]):
        draw_exact_panel(axes[0, col], A, "+")
        draw_exact_panel(axes[1, col], A, "-")
        add_common_axes_style(axes[0, col], f"side +, approach ({'far' if col == 0 else 'near'})")
        add_common_axes_style(axes[1, col], f"side -, response ({'far' if col == 0 else 'near'})")
        add_end_gaussian(axes[0, col])
        add_end_gaussian(axes[1, col])
        add_mouth_gaussian(axes[0, col])
        add_mouth_gaussian(axes[1, col])
        add_state_box(axes[0, col], format_charge(Q_PLUS), "0", f"{A:.1f}", "0")
        add_state_box(axes[1, col], format_charge(Q_MINUS), "0", f"{A:.1f}", "0")

    # Panels 3-5: schematic transit bookkeeping
    phases = [("crossing", "crossing", r"\uparrow"), ("emerged", "emerged", "+q"), ("separated", "separated", "+q")]
    titles = ["transit", "just emerged", "separated after transit"]
    for idx, (phase_top, phase_bot, qwh_label) in enumerate(phases, start=2):
        draw_schematic_panel(axes[0, idx], axes[1, idx], phase_top)
        axes[0, idx].set_title(f"side +, {titles[idx-2]}", fontsize=10)
        axes[1, idx].set_title(f"side -, {titles[idx-2]}", fontsize=10)
        if idx == 2:
            add_state_box(axes[0, idx], format_charge(Q_PLUS), r"\approx +q/2", "cross", qwh_label)
            add_state_box(axes[1, idx], format_charge(Q_MINUS), r"\approx -q/2", "cross", qwh_label)
        elif idx == 3:
            add_state_box(axes[0, idx], format_charge(Q_PLUS), "+q", "n/a", qwh_label)
            add_state_box(axes[1, idx], format_charge(Q_MINUS), "-q", "n/a", qwh_label)
        else:
            add_state_box(axes[0, idx], format_charge(Q_PLUS), "+q", "n/a", qwh_label)
            add_state_box(axes[1, idx], format_charge(Q_MINUS), "-q", "n/a", qwh_label)

    fig.suptitle(
        "Storyboard for the charge-transport argument: asymptotic end charges stay fixed, "
        "finite Gaussian enclosed charge near the mouths changes, and the harmonic label "
        "shifts only during actual throat transit.",
        fontsize=11,
        y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig("fig4_transit_storyboard.pdf", bbox_inches="tight")
    plt.close(fig)
    print("wrote fig4_transit_storyboard.pdf")


def make_gif() -> None:
    fig, axes = plt.subplots(2, 1, figsize=(6.5, 7.8), sharex=True, sharey=True)

    def render_exact(ax, A, side, qwh_label):
        ax.clear()
        draw_exact_panel(ax, A, side)
        add_common_axes_style(ax, f"side {side}")
        add_end_gaussian(ax)
        add_mouth_gaussian(ax)
        add_state_box(ax, format_charge(Q_PLUS if side == "+" else Q_MINUS), "0", f"{A:.2f}", qwh_label)

    def render_schematic(phase, qwh_label):
        axes[0].clear()
        axes[1].clear()
        draw_schematic_panel(axes[0], axes[1], phase)
        if phase == "crossing":
            add_state_box(axes[0], format_charge(Q_PLUS), r"\approx +q/2", "cross", qwh_label)
            add_state_box(axes[1], format_charge(Q_MINUS), r"\approx -q/2", "cross", qwh_label)
        else:
            add_state_box(axes[0], format_charge(Q_PLUS), "+q", "n/a", qwh_label)
            add_state_box(axes[1], format_charge(Q_MINUS), "-q", "n/a", qwh_label)

    A_frames = list(np.linspace(5.0, 1.2, 28))
    phases = (
        [("approach", A, "0") for A in A_frames]
        + [("crossing", None, r"\uparrow") for _ in range(10)]
        + [("emerged", None, "+q") for _ in range(8)]
        + [("separated", None, "+q") for _ in range(14)]
    )

    def update(frame_idx):
        phase, A, qwh = phases[frame_idx]
        if phase == "approach":
            render_exact(axes[0], A, "+", qwh)
            render_exact(axes[1], A, "-", qwh)
            axes[0].set_title("side +: source approaches the throat", fontsize=10)
            axes[1].set_title("side -: dipolar response, no induced monopole", fontsize=10)
        else:
            render_schematic(phase, qwh)
            axes[0].set_title("side +", fontsize=10)
            axes[1].set_title("side -", fontsize=10)

        fig.suptitle(
            "Per-end charge bookkeeping during approach and transit",
            fontsize=12,
            y=0.99,
        )
        return []

    ani = animation.FuncAnimation(fig, update, frames=len(phases), interval=160, blit=False)
    writer = animation.PillowWriter(fps=7)
    ani.save("wormhole_transit_story.gif", writer=writer)
    plt.close(fig)
    print("wrote wormhole_transit_story.gif")


if __name__ == "__main__":
    make_storyboard()
    make_gif()
