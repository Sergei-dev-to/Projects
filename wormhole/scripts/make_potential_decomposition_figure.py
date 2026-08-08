"""
EE-style potential decomposition figure for the Ellis-Bronnikov wormhole.

The goal is to avoid streamline rhetoric and instead show the three ingredients
of the static solution on the same cross-section:

1. the Boisseau-Linet base potential V_BL,
2. the harmonic correction V_harm,
3. the conservation-preserving sum V_BL + V_harm with lambda = 1/pi.

Outputs:
- fig_potential_decomposition.pdf
- fig_potential_decomposition.png
"""

from __future__ import annotations

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from make_ellis_crosssection import (
    E,
    W,
    LAMBDA_FIXED,
    g0,
    tunnel_radius,
    v_exact,
)


def make_grid(nx: int = 900, ny: int = 420):
    x = np.linspace(-5.0, 5.0, nx)
    y = np.linspace(-3.2, 3.2, ny)
    X, Y = np.meshgrid(x, y)
    R = tunnel_radius(X)
    mask = np.abs(Y) <= R
    s = np.zeros_like(X)
    s[mask] = Y[mask] / R[mask]
    costh = np.zeros_like(X)
    costh[mask] = np.sqrt(np.maximum(0.0, 1.0 - s[mask] ** 2))
    return x, y, X, Y, mask, costh


def v_harmonic(l: np.ndarray, l0: float, lam: float = LAMBDA_FIXED, w: float = W, e: float = E):
    return lam * e / w * g0(l0 / w) * g0(l / w)


def setup_panel(ax, title: str):
    xx = np.linspace(-5.0, 5.0, 1000)
    rr = tunnel_radius(xx)
    ax.fill_between(xx, -rr, rr, color="#fafafa", zorder=0)
    ax.plot(xx, rr, color="black", lw=1.3, zorder=3)
    ax.plot(xx, -rr, color="black", lw=1.3, zorder=3)
    ax.axvline(0.0, color="0.8", lw=0.8, ls=":")
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11)


def plot_contours(ax, X, Y, V, source_x: float | None = None):
    finite = np.isfinite(V)
    vals = V[finite]
    vmax = np.nanpercentile(vals, 96.0)
    vmin = np.nanpercentile(vals, 4.0)
    Vclip = np.array(V, copy=True)
    Vclip[finite] = np.clip(vals, vmin, vmax)

    im = ax.imshow(
        np.ma.masked_invalid(Vclip),
        extent=[X.min(), X.max(), Y.min(), Y.max()],
        origin="lower",
        cmap="coolwarm",
        alpha=0.9,
        interpolation="bilinear",
        zorder=1,
    )

    lo = np.nanmin(Vclip[finite])
    hi = np.nanmax(Vclip[finite])
    levels = np.linspace(lo + 0.1 * (hi - lo), hi - 0.1 * (hi - lo), 12)
    ax.contour(X, Y, Vclip, levels=levels, colors="white", linewidths=0.9, zorder=2)
    ax.contour(X, Y, Vclip, levels=[0.0], colors="#303030", linewidths=0.9, linestyles="dotted", zorder=2)

    if source_x is not None:
        ax.plot([source_x], [0.0], "ko", ms=5.0, zorder=4)
        ax.text(source_x + 0.12, 0.14, r"$+q$", fontsize=10, zorder=4)

    return im


def make_figure(l0: float = -2.0):
    _, _, X, Y, mask, costh = make_grid()

    Vbase = np.full_like(X, np.nan, dtype=float)
    Vharm = np.full_like(X, np.nan, dtype=float)
    Vtot = np.full_like(X, np.nan, dtype=float)

    Vbase[mask] = v_exact(X[mask], costh[mask], l0)
    Vharm[mask] = v_harmonic(X[mask], l0)
    Vtot[mask] = Vbase[mask] + Vharm[mask]

    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.6))

    setup_panel(axes[0], "Base static solution $V_{\\rm BL}$")
    im0 = plot_contours(axes[0], X, Y, Vbase, source_x=l0)
    axes[0].text(
        0.98, 0.03,
        r"source-position family" + "\n" + r"(Boisseau--Linet base branch)",
        transform=axes[0].transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="0.65", alpha=0.95),
    )

    setup_panel(axes[1], "Harmonic correction $V_{\\rm harm}$")
    im1 = plot_contours(axes[1], X, Y, Vharm)
    axes[1].text(
        0.98, 0.03,
        r"$\lambda=\frac{1}{\pi}$, $V_{\rm harm}\propto g_0(l_0/w)g_0(l/w)$",
        transform=axes[1].transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="0.65", alpha=0.95),
    )

    setup_panel(axes[2], "Fixed-sector total $V_{\\rm BL}+V_{\\rm harm}$")
    im2 = plot_contours(axes[2], X, Y, Vtot, source_x=l0)
    axes[2].text(
        0.98, 0.03,
        r"conservation-preserving branch" + "\n" + r"$Q_+=q,\;Q_-=0$",
        transform=axes[2].transAxes,
        ha="right",
        va="bottom",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.22", facecolor="white", edgecolor="0.65", alpha=0.95),
    )

    fig.suptitle(
        "Potential decomposition on the Ellis--Bronnikov cross-section\n"
        + rf"source position $l_0/w={l0:.1f}$",
        fontsize=12,
        y=0.98,
    )

    for ax, im in zip(axes, [im0, im1, im2]):
        cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
        cb.ax.tick_params(labelsize=8)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("fig_potential_decomposition.pdf", bbox_inches="tight")
    fig.savefig("fig_potential_decomposition.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig_potential_decomposition.pdf")
    print("wrote fig_potential_decomposition.png")


if __name__ == "__main__":
    make_figure()
