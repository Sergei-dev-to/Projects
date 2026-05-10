"""
Generate Fig. 1: D-S static family versus conserved-sector dynamics.

The figure compares the same three source positions in two models:
top row: Dai--Stojkovic matched static family;
bottom row: conservation-preserving sector with the same source positions.
An inset summarizes the forbidden sector drift in the monopole coefficient.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.cm as _cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm

from short_throat_fields import E_field_conserved, E_field_ds, L_TUBE, draw_tube


def _draw_field_panel(ax, U, Y, RHO, S, R, q, field_fn, side_plus, side_minus, title, row_label=None):
    Eu, Er = field_fn(U, RHO, S, R, q, l_max=30)
    Ey = Er * np.sign(Y)

    Eu_plus = np.where(side_plus, Eu, np.nan)
    Ey_plus = np.where(side_plus, Ey, np.nan)
    Eu_minus = np.where(side_minus, Eu, np.nan)
    Ey_minus = np.where(side_minus, Ey, np.nan)

    blues = LinearSegmentedColormap.from_list(
        "blues_trunc", _cm.Blues(np.linspace(0.25, 1.0, 256))
    )
    reds = LinearSegmentedColormap.from_list(
        "reds_trunc", _cm.Reds(np.linspace(0.25, 1.0, 256))
    )
    norm = LogNorm(vmin=4e-3, vmax=2.0)

    ax.streamplot(
        U, Y, Eu_plus, Ey_plus,
        color=np.sqrt(Eu_plus ** 2 + Ey_plus ** 2),
        cmap=blues, norm=norm,
        density=0.95, linewidth=0.78, arrowsize=0.78,
        broken_streamlines=True,
    )
    ax.streamplot(
        U, Y, Eu_minus, Ey_minus,
        color=np.sqrt(Eu_minus ** 2 + Ey_minus ** 2),
        cmap=reds, norm=norm,
        density=0.95, linewidth=0.78, arrowsize=0.78,
        broken_streamlines=True,
    )

    draw_tube(ax, L_TUBE, R)
    ax.plot([S], [0], "ko", ms=6, zorder=6)
    ax.annotate(r"$q$", xy=(S, 0), xytext=(S + 0.33, 0.30), fontsize=11)

    half = L_TUBE / 2
    ax.text(
        -(half + 5.7), 3.65, r"side $+$",
        fontsize=8.8, color="C0", ha="left", va="top",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.72),
    )
    ax.text(
        +(half + 5.7), 3.65, r"side $-$",
        fontsize=8.8, color="C3", ha="right", va="top",
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.72),
    )

    if row_label:
        ax.text(
            0.02, 0.06, row_label,
            transform=ax.transAxes,
            fontsize=9.0, ha="left", va="bottom",
            bbox=dict(facecolor="white", edgecolor="0.7", alpha=0.90, boxstyle="round,pad=0.22"),
        )

    ax.set_title(title, fontsize=9.8)
    ax.set_xlim(-(half + 6.0), +(half + 6.0))
    ax.set_ylim(-4.0, 4.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])


def make_fig1_static_vs_dynamic():
    R = 1.0
    q = 1.0
    L = L_TUBE
    half = L / 2

    A_vals = [8.0, 3.0, 1.15]
    S_vals = [-(half + A) for A in A_vals]

    side_ext = 6.0
    ext_rho = 4.0
    N = 360
    u_lo = -(half + side_ext)
    u_hi = +(half + side_ext)
    u_1d = np.linspace(u_lo, u_hi, N)
    y_1d = np.linspace(-ext_rho, ext_rho, N)
    U, Y = np.meshgrid(u_1d, y_1d)
    RHO = np.abs(Y) + 1e-4

    side_plus = (U < -half) & ((U + half) ** 2 + Y ** 2 > R ** 2)
    side_minus = (U > half) & ((U - half) ** 2 + Y ** 2 > R ** 2)

    fig = plt.figure(figsize=(15.8, 8.8))
    gs = fig.add_gridspec(
        2, 4,
        width_ratios=[1.0, 1.0, 1.0, 0.95],
        hspace=0.12,
        wspace=0.06,
    )

    for col, (A, S) in enumerate(zip(A_vals, S_vals)):
        title = rf"$A/R={A:g}$"
        _draw_field_panel(
            fig.add_subplot(gs[0, col]),
            U, Y, RHO, S, R, q, E_field_ds, side_plus, side_minus, title,
            row_label=r"D-S static family",
        )
        _draw_field_panel(
            fig.add_subplot(gs[1, col]),
            U, Y, RHO, S, R, q, E_field_conserved, side_plus, side_minus, "",
            row_label=r"fixed conserved sector",
        )

    ax = fig.add_subplot(gs[:, 3])
    A = np.linspace(1.01, 10.0, 400)
    B0_ds = 0.5 / A
    ax.plot(A, B0_ds, "k--", lw=2.0, label=r"D-S: $B_0^{\rm DS}=qR/(2A)$")
    ax.plot(A, np.zeros_like(A), color="C3", lw=3.0, label=r"dynamics: $B_0=0$")
    ax.fill_between(A, 0, B0_ds, color="C3", alpha=0.11)
    ax.scatter(A_vals, [0.5 / a for a in A_vals], color="k", s=28, zorder=5)
    ax.scatter(A_vals, [0.0 for _ in A_vals], color="C3", s=28, zorder=5)
    for a in A_vals:
        ax.annotate(
            "",
            xy=(a, 0.5 / a),
            xytext=(a, 0.0),
            arrowprops=dict(arrowstyle="<->", color="0.35", lw=0.9),
        )
    ax.text(
        4.7, 0.30,
        "forbidden\nsector drift",
        fontsize=9.2,
        color="0.25",
        ha="center", va="center",
        bbox=dict(facecolor="white", edgecolor="0.75", alpha=0.92, boxstyle="round,pad=0.25"),
    )
    ax.set_title("monopole sector", fontsize=10.5)
    ax.set_xlabel(r"source distance $A/R$")
    ax.set_ylabel(r"$B_0$  (units of $q/R$)")
    ax.set_xlim(1.0, 10.0)
    ax.set_ylim(-0.035, 0.55)
    ax.grid(alpha=0.25)
    ax.legend(loc="upper right", fontsize=8.2, framealpha=0.95)

    fig.suptitle(
        "Dai--Stojkovic static family versus a physical conserved-sector evolution",
        fontsize=13,
        y=0.985,
    )
    fig.text(
        0.50, 0.035,
        "The top row compares static solutions selected by the D-S matching prescription.  "
        "The bottom row uses the same source positions but keeps the conserved sector fixed; "
        "the opposite-side response starts in higher multipoles, not in a changing monopole.",
        ha="center", va="center", fontsize=10.0,
    )
    fig.savefig("fig1_static_vs_dynamic.pdf", bbox_inches="tight")
    fig.savefig("fig1_static_vs_dynamic.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig1_static_vs_dynamic.pdf")
    print("wrote fig1_static_vs_dynamic.png")


if __name__ == "__main__":
    make_fig1_static_vs_dynamic()
