"""
Six exact field-line snapshots on a wormhole tunnel cross-section.

The electric potential is the exact Boisseau--Linet closed-form potential
for the Ellis--Bronnikov wormhole, with the conservation-preserving sector
choice lambda = 1/pi.  Streamlines are computed from the projected electric
field E = -grad(V) on the displayed cross-section.

Outputs:
- fig6_fieldlines_snapshots.pdf
- fig6_fieldlines_snapshots.png
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from make_ellis_crosssection import W, E, LAMBDA_FIXED, tunnel_radius, v_lambda


def build_grid(nx: int = 420, ny: int = 240):
    x = np.linspace(-4.8, 4.8, nx)
    y = np.linspace(-3.2, 3.2, ny)
    X, Y = np.meshgrid(x, y)
    R = tunnel_radius(X)
    inside = np.abs(Y) <= R
    return x, y, X, Y, R, inside


def potential_on_grid(X, Y, inside, l0):
    R = np.sqrt(1.0 + X**2)
    costh = np.zeros_like(X)
    tmp = 1.0 - (Y**2 / np.maximum(R**2, 1e-12))
    tmp = np.maximum(tmp, 0.0)
    costh[inside] = np.sqrt(tmp[inside])
    V = np.full_like(X, np.nan, dtype=float)
    V[inside] = v_lambda(X[inside], costh[inside], l0, LAMBDA_FIXED, W, E)
    # excise a small neighborhood of the source to avoid singular numerics
    src_mask = (X - l0) ** 2 + Y**2 < 0.10**2
    V[src_mask] = np.nan
    return V


def gradient_field(x, y, V, inside):
    Vfill = np.array(V, copy=True)
    finite = np.isfinite(Vfill)
    if np.any(finite):
        Vfill[~finite] = np.nanmedian(Vfill[finite])
    dVy, dVx = np.gradient(Vfill, y, x)
    Ex = -dVx
    Ey = -dVy
    Ex[~inside] = np.nan
    Ey[~inside] = np.nan
    return Ex, Ey


def draw_geometry(ax):
    xx = np.linspace(-4.8, 4.8, 1000)
    rr = tunnel_radius(xx)
    ax.fill_between(xx, -rr, rr, color="#f7f7f7", zorder=0)
    ax.plot(xx, rr, color="black", lw=1.55)
    ax.plot(xx, -rr, color="black", lw=1.55)
    ax.axvline(0, color="0.85", lw=0.8, ls=":")


def make_figure():
    x, y, X, Y, R, inside = build_grid()

    lvals = [-4.0, -2.4, -1.0, 0.0, 1.0, 3.4]
    titles = [
        r"1. far on side $+$",
        r"2. approaching the throat",
        r"3. close to the throat",
        r"4. at the throat",
        r"5. just emerged on side $-$",
        r"6. farther on side $-$",
    ]

    fig, axes = plt.subplots(2, 3, figsize=(13.5, 8.6), sharex=True, sharey=True)

    for ax, l0, title in zip(axes.flat, lvals, titles):
        V = potential_on_grid(X, Y, inside, l0)
        Ex, Ey = gradient_field(x, y, V, inside)

        draw_geometry(ax)

        # Use a very soft background potential map just to show sign structure.
        finite = np.isfinite(V)
        vmax = np.nanpercentile(np.abs(V[finite]), 95.0)
        if not np.isfinite(vmax) or vmax <= 0:
            vmax = 1.0
        ax.imshow(
            np.ma.masked_invalid(V),
            extent=[x.min(), x.max(), y.min(), y.max()],
            origin="lower",
            cmap="coolwarm",
            vmin=-vmax, vmax=vmax,
            alpha=0.33,
            interpolation="bilinear",
            zorder=1,
        )

        # Exact field lines from projected gradient.
        ax.streamplot(
            x, y, Ex, Ey,
            color="#244cba",
            density=1.15,
            linewidth=1.0,
            arrowsize=1.0,
            minlength=0.10,
            maxlength=7.0,
            zorder=2,
        )

        # zero-potential contour helps show opposite-side dipolar structure
        try:
            ax.contour(X, Y, V, levels=[0.0], colors="#333333", linewidths=0.8, linestyles="dotted", zorder=3)
        except Exception:
            pass

        ax.plot([l0], [0], "ko", ms=6, zorder=5)
        ax.text(l0 + 0.12, 0.17, r"$+q$", fontsize=11, zorder=5)

        ax.text(
            0.98, 0.96,
            rf"$Q_+=+q,\ Q_-=0,\ \lambda=1/\pi$" + "\n" + rf"$l_0/w={l0:.1f}$",
            transform=ax.transAxes,
            ha="right", va="top",
            fontsize=8.7,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="0.6", alpha=0.92),
        )

        ax.set_title(title, fontsize=11)
        ax.set_xlim(-4.8, 4.8)
        ax.set_ylim(-3.0, 3.0)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle(
        "Exact projected field lines from the Boisseau--Linet Ellis--Bronnikov potential "
        "in the conservation-preserving sector",
        fontsize=13,
        y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.965])
    fig.savefig("fig6_fieldlines_snapshots.pdf", bbox_inches="tight")
    fig.savefig("fig6_fieldlines_snapshots.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig6_fieldlines_snapshots.pdf")
    print("wrote fig6_fieldlines_snapshots.png")


if __name__ == "__main__":
    make_figure()
