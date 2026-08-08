"""
Generate Fig. 1: the Dai--Stojkovic claimed static-family signal.

This figure intentionally shows no transit.  It depicts the D-S matched static
family: a source stays on side + and approaches the throat, while the matched
solution assigns an increasing monopole coefficient to side -.
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.cm as _cm
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LogNorm

from short_throat_fields import E_field_ds, L_TUBE, draw_tube


def make_fig1_ds_claim():
    R = 1.0
    q = 1.0
    L = L_TUBE
    half = L / 2

    A_vals = [8.0, 3.0, 1.15]
    S_vals = [-(half + A) for A in A_vals]
    Q2_vals = [q * R / (2 * A) for A in A_vals]
    panel_labels = ["(a)", "(b)", "(c)"]

    side_ext = 6.0
    ext_rho = 4.0
    N = 380
    u_lo = -(half + side_ext)
    u_hi = +(half + side_ext)
    u_1d = np.linspace(u_lo, u_hi, N)
    y_1d = np.linspace(-ext_rho, ext_rho, N)
    U, Y = np.meshgrid(u_1d, y_1d)
    RHO = np.abs(Y) + 1e-4

    side_plus = (U < -half) & ((U + half) ** 2 + Y ** 2 > R ** 2)
    side_minus = (U > half) & ((U - half) ** 2 + Y ** 2 > R ** 2)

    blues = LinearSegmentedColormap.from_list(
        "blues_trunc", _cm.Blues(np.linspace(0.25, 1.0, 256))
    )
    reds = LinearSegmentedColormap.from_list(
        "reds_trunc", _cm.Reds(np.linspace(0.25, 1.0, 256))
    )
    norm = LogNorm(vmin=4e-3, vmax=2.0)

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(15.5, 4.8),
        sharex=True,
        sharey=True,
        gridspec_kw={"wspace": 0.04},
    )

    for ax, S, A, Q2, label in zip(axes, S_vals, A_vals, Q2_vals, panel_labels):
        Eu, Er = E_field_ds(U, RHO, S, R, q, l_max=30)
        Ey = Er * np.sign(Y)

        Eu_plus = np.where(side_plus, Eu, np.nan)
        Ey_plus = np.where(side_plus, Ey, np.nan)
        Eu_minus = np.where(side_minus, Eu, np.nan)
        Ey_minus = np.where(side_minus, Ey, np.nan)

        ax.streamplot(
            U,
            Y,
            Eu_plus,
            Ey_plus,
            color=np.sqrt(Eu_plus ** 2 + Ey_plus ** 2),
            cmap=blues,
            norm=norm,
            density=0.95,
            linewidth=0.8,
            arrowsize=0.85,
            broken_streamlines=True,
        )
        ax.streamplot(
            U,
            Y,
            Eu_minus,
            Ey_minus,
            color=np.sqrt(Eu_minus ** 2 + Ey_minus ** 2),
            cmap=reds,
            norm=norm,
            density=0.95,
            linewidth=0.8,
            arrowsize=0.85,
            broken_streamlines=True,
        )

        draw_tube(ax, L, R)
        ax.plot([S], [0], "ko", ms=7, zorder=6)
        ax.annotate(r"$q$", xy=(S, 0), xytext=(S + 0.35, 0.33), fontsize=12)

        ax.text(
            u_hi - 0.35,
            -ext_rho + 0.35,
            rf"claimed $Q_-^{{\rm DS}}=\frac{{qR}}{{2A}}={Q2:.3g}\,q$",
            fontsize=8.7,
            ha="right",
            va="bottom",
            color="C3",
            bbox=dict(
                facecolor="white",
                edgecolor="C3",
                alpha=0.9,
                boxstyle="round,pad=0.22",
                linewidth=0.8,
            ),
        )

        ax.text(
            u_lo + 0.28,
            ext_rho - 0.28,
            r"side $+$: hidden source",
            fontsize=9.6,
            color="C0",
            ha="left",
            va="top",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.75),
        )
        ax.text(
            u_hi - 0.28,
            ext_rho - 0.28,
            r"side $-$: claimed signal",
            fontsize=9.6,
            color="C3",
            ha="right",
            va="top",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.75),
        )
        ax.text(
            0.03,
            0.96,
            label,
            transform=ax.transAxes,
            fontsize=11,
            va="top",
            ha="left",
            fontweight="bold",
        )
        ax.set_title(rf"source distance $A/R={A:g}$", fontsize=10.5)
        ax.set_xlim(u_lo, u_hi)
        ax.set_ylim(-ext_rho, ext_rho)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])

    axes[0].set_ylabel(r"$\rho/R$", fontsize=10)
    fig.supxlabel(r"cartoon coordinate $u/R$  (side $+$ left, throat center, side $-$ right)", fontsize=10)
    fig.suptitle(
        r"Dai--Stojkovic static-family claim: as a source approaches the throat on side $+$, "
        r"the matched static solution assigns a growing monopole to side $-$.",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig("fig1_ds_claim.pdf", bbox_inches="tight")
    fig.savefig("fig1_ds_claim.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig1_ds_claim.pdf")
    print("wrote fig1_ds_claim.png")


if __name__ == "__main__":
    make_fig1_ds_claim()
