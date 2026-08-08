"""
Exact Ellis-Bronnikov cross-section visuals based on the closed-form
Boisseau-Linet potential.

Screen mapping:
- horizontal coordinate X = l / w
- vertical coordinate Y runs in the tunnel-shaped domain
  |Y| <= sqrt(1 + X^2)

The source sits on the centerline Y = 0.  The potential is evaluated using
the exact closed form V_lambda with the conservation-preserving choice
lambda = 1/pi, which fixes the asymptotic charge at the + end.

Outputs:
- fig4_ellis_crosssection_storyboard.pdf
- fig4_ellis_crosssection_storyboard.png
"""

from __future__ import annotations

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


W = 1.0
E = 1.0
LAMBDA_FIXED = 1.0 / np.pi


def g0(x: np.ndarray) -> np.ndarray:
    return np.pi / 2.0 - np.arctan(x)


def v_exact(l: np.ndarray, costh: np.ndarray, l0: float, w: float = W, e: float = E) -> np.ndarray:
    sin2 = np.maximum(0.0, 1.0 - costh**2)
    denom = np.sqrt(np.maximum(1e-15, l**2 - 2 * l * l0 * costh + l0**2 + w**2 * sin2))
    arg = (l * l0 + w**2 * costh) / (np.sqrt(l**2 + w**2) * np.sqrt(l0**2 + w**2))
    arg = np.clip(arg, -1.0, 1.0)
    return e / denom * (0.5 + (1.0 / np.pi) * np.arcsin(arg))


def v_lambda(l: np.ndarray, costh: np.ndarray, l0: float, lam: float, w: float = W, e: float = E) -> np.ndarray:
    return v_exact(l, costh, l0, w, e) + lam * e / w * g0(l0 / w) * g0(l / w)


def tunnel_radius(x: np.ndarray) -> np.ndarray:
    return np.sqrt(1.0 + x**2)


def make_grid(nx: int = 900, ny: int = 500):
    x = np.linspace(-4.8, 4.8, nx)
    y = np.linspace(-3.4, 3.4, ny)
    X, Y = np.meshgrid(x, y)
    R = tunnel_radius(X)
    mask = np.abs(Y) <= R
    s = np.zeros_like(X)
    s[mask] = Y[mask] / R[mask]
    costh = np.zeros_like(X)
    costh[mask] = np.sqrt(np.maximum(0.0, 1.0 - s[mask] ** 2))
    return X, Y, mask, costh


def setup_ax(ax: plt.Axes, title: str):
    ax.set_xlim(-4.8, 4.8)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=11)


def draw_geometry(ax: plt.Axes):
    x = np.linspace(-4.8, 4.8, 800)
    r = tunnel_radius(x)
    ax.fill_between(x, -r, r, color="#f7f8fc", zorder=0)
    ax.plot(x, r, color="black", lw=1.45)
    ax.plot(x, -r, color="black", lw=1.45)
    ax.axvline(0, color="0.8", lw=0.8, ls=":")


def draw_gaussians(ax: plt.Axes):
    end_style = dict(fill=False, ls="--", lw=1.15, ec="0.45")
    mouth_style = dict(fill=False, ls=":", lw=1.15, ec="0.55")
    ax.add_patch(Circle((-3.9, 0), 0.7, **end_style))
    ax.add_patch(Circle((3.9, 0), 0.7, **end_style))
    ax.add_patch(Circle((-0.95, 0), 0.65, **mouth_style))
    ax.add_patch(Circle((0.95, 0), 0.65, **mouth_style))


def annotate_box(ax: plt.Axes, qwh: str, note: str):
    txt = "\n".join([
        r"$Q_+ = +q$",
        r"$Q_- = 0$",
        rf"$Q_{{\rm wh}} = {qwh}$",
        note,
    ])
    ax.text(
        0.98, 0.98, txt,
        transform=ax.transAxes,
        ha="right", va="top",
        fontsize=9,
        bbox=dict(boxstyle="round,pad=0.28", facecolor="white", alpha=0.94, edgecolor="0.55"),
    )


def plot_panel(ax: plt.Axes, X, Y, mask, costh, l0: float, title: str, qwh: str, note: str):
    draw_geometry(ax)
    draw_gaussians(ax)

    V = np.full_like(X, np.nan, dtype=float)
    V[mask] = v_lambda(X[mask], costh[mask], l0, LAMBDA_FIXED)

    # Clip the singular core a bit for plotting.
    Vplot = np.array(V, copy=True)
    finite = np.isfinite(Vplot)
    if np.any(finite):
        vmax = np.nanpercentile(Vplot[finite], 96.5)
        vmin = np.nanpercentile(Vplot[finite], 12.0)
        Vplot = np.clip(Vplot, vmin, vmax)
        pos = np.geomspace(max(1e-3, 0.08 * vmax), vmax, 8)
        neg = -pos[::-1]
        ax.contour(X, Y, Vplot, levels=pos, colors="#cf2f2f", linewidths=1.0)
        ax.contour(X, Y, Vplot, levels=neg, colors="#2aa745", linewidths=1.0, linestyles="dashed")
        ax.contour(X, Y, Vplot, levels=[0.0], colors="#333333", linewidths=0.8, linestyles="dotted")

    ax.plot([l0], [0], "ko", ms=5.5, zorder=5)
    ax.text(l0 + 0.1, 0.14, r"$+q$", fontsize=10, zorder=5)

    annotate_box(ax, qwh, note)
    setup_ax(ax, title)


def make_storyboard():
    X, Y, mask, costh = make_grid()
    stages = [
        (-3.5, "Charge far on side $+$", "0", r"far-side response present, no monopole drift"),
        (-1.4, "Charge near the throat", "0", r"stronger dipole, same end charges"),
        (0.0, "Charge at the throat center", "0", r"exact center frame from summed solution"),
        (1.4, "Charge emerged on side $-$", "+q", r"same $Q_\pm$, shifted harmonic bookkeeping"),
        (3.5, "Charge far on side $-$", "+q", r"local monopoles separated, asymptotics unchanged"),
    ]

    fig, axes = plt.subplots(1, 5, figsize=(18.2, 4.45))
    for ax, (l0, title, qwh, note) in zip(axes, stages):
        plot_panel(ax, X, Y, mask, costh, l0, title, qwh, note)

    fig.suptitle(
        "Exact Ellis--Bronnikov cross-section snapshots from the Boisseau--Linet potential "
        "with the conservation-preserving sector choice $\\lambda = 1/\\pi$.",
        fontsize=12,
        y=0.995,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig("fig4_ellis_crosssection_storyboard.pdf", bbox_inches="tight")
    fig.savefig("fig4_ellis_crosssection_storyboard.png", dpi=220, bbox_inches="tight")
    plt.close(fig)
    print("wrote fig4_ellis_crosssection_storyboard.pdf")
    print("wrote fig4_ellis_crosssection_storyboard.png")


if __name__ == "__main__":
    make_storyboard()
