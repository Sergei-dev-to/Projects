"""
Visualize the harmonic monopole term alone for the Ellis-Bronnikov wormhole.

We plot equipotential contours of

    V_harm(l; l0) = (e/w) * g0(l0/w) * g0(l/w)

with

    g0(x) = pi/2 - arctan(x).

This term is independent of theta, so the contours in the (l, y) cross-section
are vertical. That is the point: the harmonic contribution is a pure end-to-end
monopole sector, not a localized source response.

Outputs:
- fig_harmonic_term.pdf
- fig_harmonic_term.png
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from make_ellis_crosssection import tunnel_radius


def g0(x):
    return np.pi / 2.0 - np.arctan(x)


def make_figure(l0=-1.5, w=1.0, e=1.0):
    x = np.linspace(-5.2, 5.2, 700)
    y = np.linspace(-3.2, 3.2, 360)
    X, Y = np.meshgrid(x, y)
    R = tunnel_radius(X)
    inside = np.abs(Y) <= R

    V = np.full_like(X, np.nan, dtype=float)
    pref = (e / w) * g0(l0 / w)
    V[inside] = pref * g0(X[inside] / w)

    fig, ax = plt.subplots(figsize=(8.8, 4.5))

    # Wormhole geometry
    xx = np.linspace(-5.2, 5.2, 1000)
    rr = tunnel_radius(xx)
    ax.fill_between(xx, -rr, rr, color="#f7f7f7", zorder=0)
    ax.plot(xx, rr, color="black", lw=1.5)
    ax.plot(xx, -rr, color="black", lw=1.5)
    ax.axvline(0, color="0.8", lw=0.8, ls=":")

    # Soft background map plus equipotentials
    finite = np.isfinite(V)
    vmin = np.nanmin(V[finite])
    vmax = np.nanmax(V[finite])
    im = ax.imshow(
        np.ma.masked_invalid(V),
        extent=[x.min(), x.max(), y.min(), y.max()],
        origin="lower",
        cmap="viridis",
        vmin=vmin,
        vmax=vmax,
        alpha=0.82,
        interpolation="bilinear",
        zorder=1,
    )

    levels = np.linspace(vmin + 0.08 * (vmax - vmin), vmax - 0.08 * (vmax - vmin), 8)
    ax.contour(X, Y, V, levels=levels, colors="white", linewidths=1.0, zorder=2)

    ax.text(
        0.98, 0.96,
        rf"$V_{{\rm harm}} = \frac{{e}}{{w}} g_0(l_0/w) g_0(l/w)$" + "\n" +
        rf"$g_0(x)=\frac{{\pi}}{{2}}-\arctan x$" + "\n" +
        rf"$l_0/w={l0:.1f}$",
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white", edgecolor="0.6", alpha=0.95),
    )

    ax.set_title("Harmonic monopole term alone on the Ellis--Bronnikov cross-section", fontsize=12)
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-3.0, 3.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    cbar = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cbar.set_label(r"$V_{\rm harm}$", rotation=90)

    fig.tight_layout()
    fig.savefig("fig_harmonic_term.pdf", bbox_inches="tight")
    fig.savefig("fig_harmonic_term.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig_harmonic_term.pdf")
    print("wrote fig_harmonic_term.png")


if __name__ == "__main__":
    make_figure()
