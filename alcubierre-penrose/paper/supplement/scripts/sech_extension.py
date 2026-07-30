"""Analytic sech-profile 1+1 eternal warp-drive extension playground.

This script follows Finazzi/Liberati/Barcelo's simple profile

    f(r) = sech(r/a)
    vbar(r) = alpha [sech(r/a) - 1]       (c=1)

and treats the resulting 1+1 metric as a fixed analytic Lorentzian metric:

    ds^2 = -dt^2 + [dr - vbar(r) dt]^2.

The first goal is to reproduce the non-maximal three-region conformal patch
from the paper using their explicit null coordinates.  Later extension work can
build from this script without relying on numerical quadrature choices.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq


@dataclass(frozen=True)
class Params:
    alpha: float = 2.0
    a: float = 1.0
    r_max: float = 8.0
    t_max: float = 8.0
    n_grid: int = 2400
    out_dir: Path = Path("output/sech")


def sech(x: np.ndarray | float) -> np.ndarray | float:
    return 1.0 / np.cosh(x)


def vbar(r: np.ndarray | float, p: Params) -> np.ndarray | float:
    return p.alpha * (sech(np.asarray(r) / p.a) - 1.0)


def horizons(p: Params) -> tuple[float, float]:
    beta = p.alpha / (p.alpha - 1.0)
    h = p.a * np.log(beta + np.sqrt(beta * beta - 1.0))
    return -float(h), float(h)


def kappa(p: Params) -> float:
    beta = p.alpha / (p.alpha - 1.0)
    return float((p.alpha - 1.0) * np.sqrt(beta * beta - 1.0) / (p.a * beta))


def u_region(region: str, t: np.ndarray, r: np.ndarray, p: Params) -> np.ndarray:
    """Closed-form u_i coordinates from the paper, c=1."""
    r1, r2 = horizons(p)
    beta = p.alpha / (p.alpha - 1.0)
    coeff = p.a * beta / ((p.alpha - 1.0) * np.sqrt(beta * beta - 1.0))
    base = t + r / (p.alpha - 1.0)

    e1 = np.exp(-(r - r1) / p.a)
    e2 = np.exp(-(r - r2) / p.a)
    if region == "I":
        arg = (e1 - 1.0) / (e2 - 1.0)
    elif region == "II":
        arg = (1.0 - e1) / (e2 - 1.0)
    elif region == "III":
        arg = (1.0 - e1) / (1.0 - e2)
    else:
        raise ValueError(region)
    return base - coeff * np.log(arg)


def w_coord(t: np.ndarray, r: np.ndarray, p: Params) -> np.ndarray:
    gamma = p.alpha / (p.alpha + 1.0)
    coeff = 2.0 * p.a * gamma / ((p.alpha + 1.0) * np.sqrt(1.0 - gamma * gamma))
    return t + r / (p.alpha + 1.0) + coeff * np.arctan((np.exp(r / p.a) - gamma) / np.sqrt(1.0 - gamma * gamma))


def U_region(region: str, u: np.ndarray, kap: float) -> np.ndarray:
    if region == "I":
        return 0.5 + np.exp(-kap * u)
    if region == "II":
        return 0.5 * np.tanh(0.5 * kap * u)
    if region == "III":
        return -0.5 - np.exp(kap * u)
    raise ValueError(region)


def compact(region: str, t: np.ndarray, r: np.ndarray, p: Params) -> tuple[np.ndarray, np.ndarray]:
    kap = kappa(p)
    u = u_region(region, t, r, p)
    w = w_coord(t, r, p)
    U = U_region(region, u, kap)
    ubar = np.arctan(U)
    wbar = np.arctan(w)
    return 0.5 * (wbar - ubar), 0.5 * (wbar + ubar)


def plot_three_region_patch(p: Params) -> None:
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    eps = 1.0e-5 * (r2 - r1)
    grids = {
        "I": np.linspace(-p.r_max, r1 - eps, p.n_grid),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, p.r_max, p.n_grid),
    }

    fig, ax = plt.subplots(figsize=(8.6, 8.6), constrained_layout=True)

    for t0 in np.linspace(-p.t_max, p.t_max, 15):
        for region, r in grids.items():
            x, y = compact(region, np.full_like(r, t0), r, p)
            ax.plot(x, y, color="#6b6f73", lw=0.75, ls=(0, (7, 6)), alpha=0.72)

    r_samples = {
        "I": np.linspace(-p.r_max + 0.3, r1 - 0.22, 5),
        "II": np.r_[np.linspace(r1 + 0.22, -0.18, 4), [0.0], np.linspace(0.18, r2 - 0.22, 4)],
        "III": np.linspace(r2 + 0.22, p.r_max - 0.3, 5),
    }
    t = np.linspace(-p.t_max, p.t_max, 1500)
    for region, values in r_samples.items():
        for r0 in values:
            x, y = compact(region, t, np.full_like(t, r0), p)
            rider = region == "II" and abs(r0) < 1.0e-12
            ax.plot(x, y, color="#c14d3f" if rider else "#20252b", lw=2.8 if rider else 1.05, label="rider r=0" if rider else None)

    # Horizon boundaries, approached from both sides.
    for region, r0, label in [
        ("I", r1 - eps, r"$r_1$ exterior side"),
        ("II", r1 + eps, r"$r_1$ bubble side"),
        ("II", r2 - eps, r"$r_2$ bubble side"),
        ("III", r2 + eps, r"$r_2$ exterior side"),
    ]:
        x, y = compact(region, t, np.full_like(t, r0), p)
        ax.plot(x, y, color="#0b7a63", lw=2.0, ls="--", label=label)

    b = 0.5 * np.pi
    a0 = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    for ubar in (b, -b):
        s = np.linspace(-b, b, 300)
        ax.plot(*from_null(np.full_like(s, ubar), s), color="#555555", lw=1.4, alpha=0.8)
    for umin, umax in [(a0, b), (-a0, a0), (-b, -a0)]:
        s = np.linspace(umin, umax, 300)
        ax.plot(*from_null(s, np.full_like(s, b)), color="#555555", lw=1.4, alpha=0.8)
        ax.plot(*from_null(s, np.full_like(s, -b)), color="#555555", lw=1.4, alpha=0.8)

    ax.text(-0.62, 0.02, "I", ha="center", va="center", fontsize=10)
    ax.text(0.0, 0.02, "II\nbubble", ha="center", va="center", fontsize=10)
    ax.text(0.62, 0.02, "III", ha="center", va="center", fontsize=10)
    ax.text(0.05, 0.57, r"$r=0$ rider", color="#c14d3f", fontsize=10)
    ax.text(
        -1.55,
        1.48,
        "Line key:\n"
        "solid black: constant r worldlines\n"
        "gray dashed: constant t slices\n"
        "red solid: rider r=0\n"
        "green dashed: r=r1,r2 horizons",
        fontsize=9,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.annotate(
        "constant r curves\n(timelike in bubble region)",
        xy=(0.18, 0.62),
        xytext=(0.72, 1.05),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=9,
        ha="center",
    )
    ax.annotate(
        "constant t curves",
        xy=(-0.36, -0.36),
        xytext=(-1.12, -0.88),
        arrowprops={"arrowstyle": "->", "color": "#777777", "lw": 1.0},
        fontsize=9,
        color="#555555",
        ha="center",
    )
    ax.annotate(
        r"horizon $r=r_1$",
        xy=(-0.37, -0.37),
        xytext=(-0.96, -0.58),
        arrowprops={"arrowstyle": "->", "color": "#0b7a63", "lw": 1.0},
        fontsize=9,
        color="#0b7a63",
        ha="center",
    )
    ax.annotate(
        r"horizon $r=r_2$",
        xy=(0.50, -0.50),
        xytext=(0.96, -0.82),
        arrowprops={"arrowstyle": "->", "color": "#0b7a63", "lw": 1.0},
        fontsize=9,
        color="#0b7a63",
        ha="center",
    )
    ax.text(
        -1.55,
        -1.53,
        "Boundary caution: the gray outer frame is a compactification frame.\n"
        "Edges reached by r->+-infinity are scri; edges reached at finite r or r=r1,r2 are not.",
        fontsize=8.2,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.88},
    )
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"$(\mathcal{W}+\mathcal{U})/2$")
    ax.set_title("Sech-profile eternal warp-drive patch from closed-form coordinates")
    ax.legend(loc="upper right", fontsize=7.8)
    ax.grid(True, alpha=0.16)
    fig.savefig(p.out_dir / "sech_three_region_patch.png", dpi=180)
    fig.savefig(p.out_dir / "sech_three_region_patch_labeled.png", dpi=180)
    plt.close(fig)


def plot_crossing_observer_on_patch(p: Params) -> None:
    """Draw the finite-proper-time observer r=-0.5t on the conformal patch."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    eps = 1.0e-5 * (r2 - r1)
    q = -0.5
    t_cross = r1 / q

    fig, ax = plt.subplots(figsize=(8.8, 8.8), constrained_layout=True)

    # Background constant-r and constant-t curves, lighter than the main plot.
    grids = {
        "I": np.linspace(-p.r_max, r1 - eps, p.n_grid),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, p.r_max, p.n_grid),
    }
    for t0 in np.linspace(-p.t_max, p.t_max, 11):
        for region, r in grids.items():
            x, y = compact(region, np.full_like(r, t0), r, p)
            ax.plot(x, y, color="#8b9095", lw=0.65, ls=(0, (7, 6)), alpha=0.45)

    t_bg = np.linspace(-p.t_max, p.t_max, 1000)
    for r0 in np.r_[np.linspace(r1 + 0.22, -0.18, 3), [0.0], np.linspace(0.18, r2 - 0.22, 3)]:
        x, y = compact("II", t_bg, np.full_like(t_bg, r0), p)
        ax.plot(x, y, color="#20252b", lw=0.85, alpha=0.58)

    # Horizons.
    for region, r0 in [("I", r1 - eps), ("II", r1 + eps), ("II", r2 - eps), ("III", r2 + eps)]:
        x, y = compact(region, t_bg, np.full_like(t_bg, r0), p)
        ax.plot(x, y, color="#0b7a63", lw=1.8, ls="--", alpha=0.85)

    # Rider r=0 for comparison.
    x, y = compact("II", t_bg, np.zeros_like(t_bg), p)
    ax.plot(x, y, color="#c14d3f", lw=2.6, label="rider r=0")

    # Crossing observer, split by regions.
    t_obs_ii = np.linspace(0.0, t_cross - 1.0e-5, 500)
    r_obs_ii = q * t_obs_ii
    x, y = compact("II", t_obs_ii, r_obs_ii, p)
    ax.plot(x, y, color="#1f6f8b", lw=3.0, label=r"observer $r=-0.5t$")

    r_null = brentq(lambda rr: q - float(vbar(rr, p)) - 1.0, -p.r_max, r1 - 1.0e-8)
    t_null = r_null / q
    t_obs_i = np.linspace(t_cross + 1.0e-5, t_null - 1.0e-5, 500)
    r_obs_i = q * t_obs_i
    x, y = compact("I", t_obs_i, r_obs_i, p)
    ax.plot(x, y, color="#1f6f8b", lw=3.0, ls=(0, (6, 3)), label="same q, timelike in I until null")

    # Mark start and crossing.
    x0, y0 = compact("II", np.array([0.0]), np.array([0.0]), p)
    ax.scatter(x0, y0, s=48, color="#1f6f8b", zorder=5)
    ax.text(float(x0[0]) + 0.04, float(y0[0]) - 0.07, "start\nr=0,t=0", color="#1f6f8b", fontsize=9)

    xh, yh = compact("II", np.array([t_cross - 1.0e-5]), np.array([r1 + abs(q) * 1.0e-5]), p)
    ax.scatter(xh, yh, s=52, color="#d99022", zorder=6)
    ax.text(
        float(xh[0]) - 0.35,
        float(yh[0]) + 0.08,
        f"crosses r1\nτ=2.482758\nt={t_cross:.3f}",
        color="#9b5d00",
        fontsize=9,
        ha="center",
    )
    x_after, y_after = compact("I", np.array([0.5 * (t_cross + t_null)]), np.array([q * 0.5 * (t_cross + t_null)]), p)
    ax.text(
        float(x_after[0]) - 0.28,
        float(y_after[0]) + 0.06,
        "continues in\nregion I",
        color="#1f6f8b",
        fontsize=9,
        ha="center",
    )
    xn, yn = compact("I", np.array([t_null]), np.array([r_null]), p)
    ax.scatter(xn, yn, s=42, color="#8b2f2f", zorder=6)
    ax.text(
        float(xn[0]) - 0.36,
        float(yn[0]) - 0.07,
        f"same q becomes null\nr={r_null:.3f}\nt={t_null:.3f}",
        color="#8b2f2f",
        fontsize=8.5,
        ha="center",
    )

    b = 0.5 * np.pi
    a0 = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    for ubar in (b, -b):
        s = np.linspace(-b, b, 300)
        ax.plot(*from_null(np.full_like(s, ubar), s), color="#555555", lw=1.2, alpha=0.65)
    for umin, umax in [(a0, b), (-a0, a0), (-b, -a0)]:
        s = np.linspace(umin, umax, 300)
        ax.plot(*from_null(s, np.full_like(s, b)), color="#555555", lw=1.2, alpha=0.65)
        ax.plot(*from_null(s, np.full_like(s, -b)), color="#555555", lw=1.2, alpha=0.65)

    ax.text(-0.62, 0.02, "I", ha="center", va="center", fontsize=10)
    ax.text(0.0, 0.02, "II\nbubble", ha="center", va="center", fontsize=10)
    ax.text(0.62, 0.02, "III", ha="center", va="center", fontsize=10)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"$(\mathcal{W}+\mathcal{U})/2$")
    ax.set_title("Timelike crossing of r1; constant-q continuation later becomes null")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.16)
    fig.savefig(p.out_dir / "timelike_crossing_on_patch.png", dpi=180)
    plt.close(fig)


def diamond(center: tuple[float, float], radius: float = 1.0) -> np.ndarray:
    x, y = center
    return np.array([[x, y + radius], [x + radius, y], [x, y - radius], [x - radius, y], [x, y + radius]])


def plot_formal_block_extension(p: Params) -> None:
    """Draw a formal block-extension schematic for the fixed 1+1 metric.

    This is a causal block diagram, not a metric-coordinate plot.  It shows the
    idea of continuing the analytic Killing-horizon blocks beyond the non-maximal
    three-region patch used in the paper.  The continuation is a chosen analytic
    tiling, not a unique physical matter extension.
    """
    p.out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(11.0, 8.2), constrained_layout=True)

    # A simple null-grid tiling.  The original FLB patch is the highlighted
    # left/bubble/right chain; adjacent faint blocks are the formal continuations.
    centers = []
    for j in range(-2, 3):
        for i in range(-4, 5):
            if (i + j) % 2 == 0:
                centers.append((i, j))

    for c in centers:
        poly = diamond(c, 0.92)
        ax.plot(poly[:, 0], poly[:, 1], color="#c8cdd2", lw=0.8, alpha=0.55)

    original = {
        "I": (-1, 1),
        "II bubble": (0, 0),
        "III": (1, -1),
    }
    colors = {"I": "#f4f0e8", "II bubble": "#eef6f8", "III": "#f4f0e8"}
    for label, c in original.items():
        poly = diamond(c, 0.92)
        ax.fill(poly[:, 0], poly[:, 1], color=colors[label], ec="#20252b", lw=1.5, alpha=0.92)
        ax.text(c[0], c[1], label, ha="center", va="center", fontsize=11)

    # Horizon chains, drawn as null diagonals through the tile network.
    x = np.linspace(-4.4, 4.4, 300)
    ax.plot(x, x, color="#0b7a63", lw=2.0, ls="--", label=r"$r=r_1$ horizon family")
    ax.plot(x, x - 2.0, color="#0b7a63", lw=2.0, ls=(0, (8, 4)), label=r"$r=r_2$ horizon family")

    # The central rider in the original bubble block and its formal continuation copies.
    for c, alpha in [((0, 0), 1.0), ((-2, 2), 0.28), ((2, -2), 0.28)]:
        ax.plot([c[0] - 0.14, c[0] + 0.14], [c[1] - 0.62, c[1] + 0.62], color="#c14d3f", lw=3.0, alpha=alpha)
    ax.text(0.22, 0.48, r"$r=0$ rider", color="#c14d3f", fontsize=10)

    # Mark the non-maximal patch boundaries that prompted the extension.
    ax.annotate(
        "future extension\nacross horizon blocks",
        xy=(0.9, 0.9),
        xytext=(2.1, 1.9),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.0},
        fontsize=10,
        ha="center",
    )
    ax.annotate(
        "past extension\nacross horizon blocks",
        xy=(-0.9, -0.9),
        xytext=(-2.25, -1.8),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.0},
        fontsize=10,
        ha="center",
    )

    ax.text(
        -4.25,
        2.55,
        "Formal extension of the fixed analytic 1+1 sech metric\n"
        "not a unique physical Alcubierre matter extension",
        fontsize=10,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.9},
    )
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-2.7, 2.7)
    ax.axis("off")
    ax.legend(loc="lower right", fontsize=9)
    fig.savefig(p.out_dir / "formal_block_extension_schematic.png", dpi=180)
    plt.close(fig)


def C_factor(r: np.ndarray, p: Params) -> np.ndarray:
    """Conformal factor in ds^2 = -C(r) du dw."""
    vv = vbar(r, p)
    return 1.0 - vv * vv


def plot_kruskal_horizon_charts(p: Params) -> None:
    """Build local Kruskal-like charts across r1 and r2.

    For r1, u -> +infinity on both sides, so use U1=-exp(-kappa u).
    For r2, u -> -infinity on both sides, so use U2=+exp(kappa u).

    In each chart W=w.  The metric takes the form
        ds^2 = -C(r) du dw = -(C/(kappa |U|)) dU dW
    up to sign conventions, and C/|U| should approach a finite limit at the
    corresponding horizon.
    """
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)
    eps = 1.0e-5
    r_windows = {
        "r1": {
            "left": ("I", np.linspace(r1 - 1.2, r1 - eps, 1200)),
            "right": ("II", np.linspace(r1 + eps, r1 + 1.2, 1200)),
            "sign": -1.0,
            "exp": -1.0,
            "horizon": r1,
        },
        "r2": {
            "left": ("II", np.linspace(r2 - 1.2, r2 - eps, 1200)),
            "right": ("III", np.linspace(r2 + eps, r2 + 1.2, 1200)),
            "sign": 1.0,
            "exp": 1.0,
            "horizon": r2,
        },
    }

    fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.8), constrained_layout=True)
    t_values = np.linspace(-4.0, 4.0, 13)

    diagnostics = []
    transition_lines = []
    for ax, (name, spec) in zip(axes, r_windows.items()):
        side_limits: dict[str, float] = {}
        for side, (region, r) in [("left", spec["left"]), ("right", spec["right"])]:
            for t0 in t_values:
                t = np.full_like(r, t0)
                u = u_region(region, t, r, p)
                w = w_coord(t, r, p)
                U = spec["sign"] * np.exp(spec["exp"] * kap * u)
                ax.plot(U, w, color="#20252b", lw=0.65, alpha=0.6)

            for r0 in np.linspace(r[0], r[-1], 6):
                tt = np.linspace(-4.0, 4.0, 500)
                rr = np.full_like(tt, r0)
                u = u_region(region, tt, rr, p)
                w = w_coord(tt, rr, p)
                U = spec["sign"] * np.exp(spec["exp"] * kap * u)
                ax.plot(U, w, color="#6b6f73", lw=0.65, ls=(0, (5, 5)), alpha=0.55)

            # Conformal-factor regularity diagnostic at fixed t=0.
            rr = r
            uu = u_region(region, np.zeros_like(rr), rr, p)
            UU = np.abs(spec["sign"] * np.exp(spec["exp"] * kap * uu))
            regular_factor = C_factor(rr, p) / (kap * UU)
            near = regular_factor[-12:] if side == "left" else regular_factor[:12]
            side_limits[side] = float(np.nanmean(near))
            diagnostics.append(f"{name} {side} {region}: C/(kappa|U|) near horizon ~ {side_limits[side]: .8f}")

        if "left" in side_limits and "right" in side_limits:
            # If U_right = lambda U_left, then C/(kappa|U|) rescales by 1/|lambda|.
            # A same-orientation smooth normalization can match magnitudes with:
            # |lambda| = |F_right| / |F_left|.
            lam = abs(side_limits["right"]) / abs(side_limits["left"])
            transition_lines.append(f"{name}: horizon-normalization magnitude |U_right/U_left| = {lam:.10f}")
            transition_lines.append(
                f"{name}: orientation sign is chart-convention dependent; conformal-factor signs are "
                f"{np.sign(side_limits['left']):+.0f} and {np.sign(side_limits['right']):+.0f}"
            )

        ax.axvline(0.0, color="#0b7a63", lw=2.0, ls="--", label="horizon U=0")
        ax.set_title(f"Kruskal-like chart across {name}")
        ax.set_xlabel("regular horizon coordinate U")
        ax.set_ylabel("global null coordinate w")
        ax.grid(True, alpha=0.2)
        ax.legend(loc="best")

    fig.savefig(p.out_dir / "kruskal_horizon_charts.png", dpi=180)
    plt.close(fig)
    (p.out_dir / "kruskal_diagnostics.txt").write_text(
        "\n".join(diagnostics) + "\n\n" + "\n".join(transition_lines) + "\n",
        encoding="utf-8",
    )


def plot_atlas_extension_graph(p: Params) -> None:
    """Generate a repeated block atlas from horizon adjacency rules.

    This is still a Penrose-block diagram rather than one global coordinate
    chart.  The nontrivial input is the adjacency:

        I --r1-- II --r2-- III

    and the local Kruskal calculation verifies that crossing each horizon is a
    regular chart transition for the fixed analytic metric.  Repeating those
    transitions creates the formal maximal-extension candidate.
    """
    p.out_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(13.0, 8.5), constrained_layout=True)

    # Coordinates are Penrose-block coordinates, not spacetime coordinates.
    # The highlighted FLB patch is the chain I_0, II_0, III_0.
    blocks = []
    for n in range(-3, 4):
        blocks.extend(
            [
                {"kind": "I", "label": f"I$_{{{n}}}$", "center": (3 * n - 1, 1), "patch": n == 0},
                {"kind": "II", "label": f"II$_{{{n}}}$", "center": (3 * n, 0), "patch": n == 0},
                {"kind": "III", "label": f"III$_{{{n}}}$", "center": (3 * n + 1, -1), "patch": n == 0},
            ]
        )

    fill = {"I": "#f4f0e8", "II": "#eef6f8", "III": "#f4f0e8"}
    edge = {"I": "#60656b", "II": "#264653", "III": "#60656b"}
    for block in blocks:
        poly = diamond(block["center"], 0.92)
        alpha = 0.92 if block["patch"] else 0.35
        lw = 1.7 if block["patch"] else 0.8
        ax.fill(poly[:, 0], poly[:, 1], color=fill[block["kind"]], ec=edge[block["kind"]], lw=lw, alpha=alpha)
        if -2 <= int(block["label"].split("{")[1].split("}")[0]) <= 2:
            ax.text(block["center"][0], block["center"][1], block["label"], ha="center", va="center", fontsize=10, alpha=0.95 if block["patch"] else 0.55)

    # Horizon adjacency lines.  These are the null sides glued by the local
    # Kruskal charts.  They are drawn as families rather than as single horizons.
    x = np.linspace(-10.4, 10.4, 800)
    ax.plot(x, x, color="#0b7a63", lw=2.2, ls="--", label=r"$r_1$ crossing family")
    ax.plot(x, x - 2, color="#0b7a63", lw=2.2, ls=(0, (9, 4)), label=r"$r_2$ crossing family")

    # Mark one generating chain of the original patch.
    for c in [(-1, 1), (0, 0), (1, -1)]:
        ax.plot([c[0] - 0.92, c[0] + 0.92, c[0] + 0.92, c[0] - 0.92, c[0] - 0.92],
                [c[1], c[1] + 0.92, c[1], c[1] - 0.92, c[1]], color="#111111", lw=1.1)

    # Rider copies in each II block.  In a maximal extension these are distinct
    # continuation branches unless an extra identification is imposed.
    for n in range(-2, 3):
        cx, cy = 3 * n, 0
        ax.plot([cx - 0.13, cx + 0.13], [cy - 0.62, cy + 0.62], color="#c14d3f", lw=2.5, alpha=0.9 if n == 0 else 0.35)
    ax.text(0.26, 0.58, r"$r=0$ branch in original II block", color="#c14d3f", fontsize=10)

    ax.annotate(
        "local Kruskal charts\nmake these crossings regular",
        xy=(0.78, 0.78),
        xytext=(2.0, 2.25),
        arrowprops={"arrowstyle": "->", "color": "#333333", "lw": 1.1},
        fontsize=10,
        ha="center",
    )
    ax.text(
        -10.2,
        3.0,
        "Repeated analytic block atlas for the fixed 1+1 sech metric\n"
        "No extra physical identification or matter continuation imposed",
        fontsize=10,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-10.5, 10.5)
    ax.set_ylim(-3.2, 3.2)
    ax.axis("off")
    ax.legend(loc="lower right", fontsize=9)
    fig.savefig(p.out_dir / "atlas_extension_graph.png", dpi=180)
    plt.close(fig)


def write_extension_notes(p: Params) -> None:
    """Write the current atlas/transition-map status in equations."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)
    notes = f"""Formal analytic extension notes for the fixed 1+1 sech warp metric

Metric:
  ds^2 = -dt^2 + [dr - vbar(r) dt]^2
  vbar(r) = alpha [sech(r/a) - 1]

Parameters:
  alpha = {p.alpha}
  a = {p.a}
  r1 = {r1:.12f}
  r2 = {r2:.12f}
  kappa = {kap:.12f}

Null coordinates:
  du_i = dt - dr/[1 + vbar(r)]  in region i
  dw   = dt + dr/[1 - vbar(r)]  globally across I, II, III

Horizon behavior:
  r = r1: u_I -> +infinity and u_II -> +infinity
  r = r2: u_II -> -infinity and u_III -> -infinity

Local Kruskal-like coordinates:
  across r1:
    U_1,I  = -A_1,I  exp[-kappa u_I]
    U_1,II = +A_1,II exp[-kappa u_II]
    W_1    = w

  across r2:
    U_2,II  = -A_2,II  exp[+kappa u_II]
    U_2,III = +A_2,III exp[+kappa u_III]
    W_2     = w

The constants A are free positive normalizations until we demand a particular
matching convention. The diagnostic file estimates the relative magnitudes
needed to match |C/(kappa U)| across each horizon.

Metric regularity check:
  In (u,w), ds^2 = -C(r) du dw with C(r)=1-vbar(r)^2.
  If U = +/- A exp(+- kappa u), then du = dU/(+- kappa U).
  Hence ds^2 = finite_factor(r) dU dw, where finite_factor is proportional to
  C(r)/(kappa U). The numerical diagnostics verify this has a finite nonzero
  limit at r1 and r2 from both adjacent regions.

What is completed:
  - horizon roots and kappa
  - closed-form three-region patch
  - local regular Kruskal charts across r1 and r2
  - repeated block atlas graph based on these regular crossings

What is not yet completed:
  - proof that the repeated atlas is geodesically maximal
  - treatment of all possible analytic identifications
  - physical stress-energy continuation beyond the non-maximal FLB patch
"""
    (p.out_dir / "extension_notes.txt").write_text(notes, encoding="utf-8")


def classify_patch_boundaries(p: Params) -> None:
    """Classify boundaries from limits, without relying on the paper's labels."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)

    large_t = 1.0e6
    large_r = 100.0
    eps = 1.0e-7

    samples = [
        ("I r->-infinity, finite t", "I", np.array([0.0]), np.array([-large_r]), "r -> -infinity"),
        ("I r->r1-, finite t", "I", np.array([0.0]), np.array([r1 - eps]), "r -> r1 horizon"),
        ("I t->+infinity, finite exterior r", "I", np.array([large_t]), np.array([(r1 - 3.0)]), "t -> +infinity finite r"),
        ("I t->-infinity, finite exterior r", "I", np.array([-large_t]), np.array([(r1 - 3.0)]), "t -> -infinity finite r"),
        ("II r->r1+, finite t", "II", np.array([0.0]), np.array([r1 + eps]), "r -> r1 horizon"),
        ("II r->r2-, finite t", "II", np.array([0.0]), np.array([r2 - eps]), "r -> r2 horizon"),
        ("II t->+infinity, r=0", "II", np.array([large_t]), np.array([0.0]), "t -> +infinity finite r"),
        ("II t->-infinity, r=0", "II", np.array([-large_t]), np.array([0.0]), "t -> -infinity finite r"),
        ("III r->r2+, finite t", "III", np.array([0.0]), np.array([r2 + eps]), "r -> r2 horizon"),
        ("III r->+infinity, finite t", "III", np.array([0.0]), np.array([large_r]), "r -> +infinity"),
        ("III t->+infinity, finite exterior r", "III", np.array([large_t]), np.array([(r2 + 3.0)]), "t -> +infinity finite r"),
        ("III t->-infinity, finite exterior r", "III", np.array([-large_t]), np.array([(r2 + 3.0)]), "t -> -infinity finite r"),
    ]

    lines = [
        "Boundary classification from limits of the fixed sech metric",
        "No paper labels assumed.",
        "",
        f"r1 = {r1:.12f}, r2 = {r2:.12f}, kappa = {kap:.12f}",
        "",
        "Columns: name | region | limit source | u | w | U_regularized | compact(x,y) | preliminary type",
    ]

    def preliminary_type(source: str) -> str:
        if "infinity" in source and "r ->" in source:
            return "asymptotic spatial/null boundary; not extend through as spacetime"
        if "horizon" in source:
            return "candidate horizon; test Kruskal regularity"
        if "finite r" in source:
            return "infinite Killing time at finite r; check if horizon endpoint or timelike infinity in extension"
        return "unknown"

    for name, region, t, r, source in samples:
        u = u_region(region, t, r, p)
        w = w_coord(t, r, p)
        U = U_region(region, u, kap)
        x, y = compact(region, t, r, p)
        lines.append(
            f"{name} | {region} | {source} | "
            f"u={float(u[0]): .6e} | w={float(w[0]): .6e} | U={float(U[0]): .6e} | "
            f"({float(x[0]): .6f}, {float(y[0]): .6f}) | {preliminary_type(source)}"
        )

    # Direct causal character of t->infinity at finite r: the curve r=const is
    # timelike iff |vbar(r)|<1.  In region II this holds; in exterior regions it
    # fails asymptotically for alpha>1.
    lines.extend(
        [
            "",
            "Causal character of r=const curves:",
            "  ds^2|dr=0 = -(1-vbar(r)^2) dt^2.",
            "  Region II finite-r static/rider curves are timelike where |vbar|<1.",
            "  Exterior finite-r curves can be spacelike where |vbar|>1.",
            "",
            "Kruskal tests already computed:",
            "  r=r1 and r=r2 are locally regular horizons because C/(kappa|U|) has finite nonzero limits.",
            "",
            "Interpretation rule for extension without trusting a diagram:",
            "  Extend only boundaries reached by r->r1,r2 with finite Kruskal chart.",
            "  Do not extend boundaries whose defining limit is r->±infinity.",
            "  Treat t->±infinity at finite r as incomplete until expressed in a local horizon chart.",
        ]
    )
    (p.out_dir / "boundary_classification.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def endpoint_in_kruskal_charts(p: Params) -> None:
    """Classify t->±infinity finite-r endpoints using local horizon charts."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)

    # Large but finite values; exponential maps saturate the endpoint behavior.
    t_values = np.array([-80.0, -40.0, -20.0, 20.0, 40.0, 80.0])
    r_values = {
        "rider r=0": ("II", 0.0),
        "near r1 inside": ("II", r1 + 0.2),
        "near r2 inside": ("II", r2 - 0.2),
        "left exterior sample": ("I", r1 - 1.0),
        "right exterior sample": ("III", r2 + 1.0),
    }

    lines = [
        "Finite-r t->±infinity endpoints in local Kruskal horizon charts",
        "No diagram labels assumed.",
        "",
        "Definitions:",
        "  r1 chart: U1 = -exp(-kappa u), W=w",
        "  r2 chart: U2 = +exp(+kappa u), W=w",
        "If U -> 0 while |W| -> infinity, the endpoint lies on a horizon generator at null infinity of that chart.",
        "If |U| -> infinity and |W| -> infinity, it is not covered by that local horizon chart.",
        "",
    ]

    for label, (region, r0) in r_values.items():
        rr = np.full_like(t_values, r0, dtype=float)
        u = u_region(region, t_values, rr, p)
        w = w_coord(t_values, rr, p)
        U1 = -np.exp(-kap * u)
        U2 = np.exp(kap * u)
        lines.append(f"{label} ({region}, r={r0:.6f})")
        for ti, ui, wi, u1i, u2i in zip(t_values, u, w, U1, U2):
            lines.append(f"  t={ti: .1f}: u={ui: .6e}, w={wi: .6e}, U1={u1i: .6e}, U2={u2i: .6e}")
        lines.append("")

    # Focused asymptotic classification for rider.
    lines.extend(
        [
            "Rider r=0 asymptotics:",
            "  u ~ t + const, w ~ t + const.",
            "  as t -> +infinity: U1=-exp(-kappa u)->0, U2=exp(kappa u)->+infinity, w->+infinity.",
            "    This is covered by the r1-type future horizon chart, not by r2.",
            "  as t -> -infinity: U2=exp(kappa u)->0, U1=-exp(-kappa u)->-infinity, w->-infinity.",
            "    This is covered by the r2-type past horizon chart, not by r1.",
            "",
            "Interpretation:",
            "  The r=0 endpoint at future Killing time is a horizon/Cauchy endpoint in the r1 Kruskal chart.",
            "  The r=0 endpoint at past Killing time is a horizon/Cauchy endpoint in the r2 Kruskal chart.",
            "  Therefore the rider endpoints in the non-maximal patch are not ordinary i±.",
        ]
    )
    (p.out_dir / "finite_r_endpoint_kruskal.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def affine_boundary_analysis(p: Params) -> None:
    """Analyze affine length of null generators from metric identities."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)
    lines = [
        "Affine-parameter boundary analysis",
        "Computed from the fixed 1+1 metric, not from visual labels.",
        "",
        "Metric in null coordinates:",
        "  ds^2 = -C(r) du dw",
        "  C(r) = 1 - vbar(r)^2",
        "",
        "Transverse null rays, u=const:",
        "  dλ/dw ∝ C",
        "  du=0 gives dt/dr = 1/[1+vbar(r)]",
        "  dw/dr = 1/[1+vbar(r)] + 1/[1-vbar(r)] = 2/C(r)",
        "  therefore dλ ∝ C dw = 2 dr.",
        "",
        "Transverse null rays, w=const:",
        "  dλ/du ∝ C",
        "  dw=0 gives dt/dr = -1/[1-vbar(r)]",
        "  du/dr = -1/[1-vbar(r)] - 1/[1+vbar(r)] = -2/C(r)",
        "  therefore dλ ∝ C du = -2 dr.",
        "",
        "Consequence for transverse null crossings:",
        f"  A transverse null ray reaches a finite horizon radius r1={r1:.12f} or r2={r2:.12f} at finite affine distance.",
        "  A boundary reached by r -> +infinity or r -> -infinity is infinite affine distance.",
        "",
        "This does NOT calculate affine length along the horizon generator itself.",
        "At a horizon, the generator is r=constant and the u coordinate is singular,",
        "so the dλ ∝ dr argument above is inapplicable to the generator.",
        "",
        "Horizon-generator calculation:",
        "  k = ∂t is tangent to r=constant horizons because C=1-vbar^2=0 there.",
        "  Directly from the Christoffel symbols, k^a ∇_a k^b = κ_h k^b with",
        "  κ_h = C'(r_h)/2 = vbar'(r_h).",
        f"  κ_h(r1) = +{kap:.12f}; κ_h(r2) = -{kap:.12f}.",
        "  If t is the Killing parameter on the generator, an affine parameter obeys",
        "  dλ/dt ∝ exp(κ_h t).",
        "",
        "Therefore:",
        "  r1 generator: affine length is infinite as t->+infinity and finite as t->-infinity.",
        "  r2 generator: affine length is finite as t->+infinity and infinite as t->-infinity.",
        "",
        "Top-left grey edge of our compactified region-I frame:",
        "  In the plotted coordinates it is mathcal U=+pi/2, i.e. U_I -> +infinity and u_I -> -infinity.",
        "  The generic points on that edge are approached by the left asymptotic limit r -> -infinity, not by r=r1/r2.",
        "  Since dλ ∝ dr along null generators, reaching r -> -infinity takes infinite affine parameter.",
        "",
        "So the generic top-left boundary is scri-like/infinite-affine, not an extendible finite-affine horizon.",
        "Only finite-r horizon crossing points are candidates for local analytic extension.",
    ]
    (p.out_dir / "affine_boundary_analysis.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def timelike_crossing_example(p: Params) -> None:
    """Calculate one finite-proper-time crossing of the r1 horizon."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, _ = horizons(p)
    q = -0.5  # dr/dt, chosen timelike from r=0 through r1 for alpha=2.
    r_start = 0.0
    t_start = 0.0
    t_cross = (r1 - r_start) / q
    r_null = brentq(lambda rr: q - float(vbar(rr, p)) - 1.0, -p.r_max, r1 - 1.0e-8)
    t_null = r_null / q

    def gamma_inv(r: float) -> float:
        return float(np.sqrt(1.0 - (q - float(vbar(r, p))) ** 2))

    def integrand(r: float) -> float:
        return gamma_inv(r) / abs(q)

    tau, err = quad(integrand, r1, r_start, epsabs=1.0e-12, epsrel=1.0e-12, limit=200)
    tau_after, err_after = quad(integrand, r_null, r1, epsabs=1.0e-12, epsrel=1.0e-12, limit=200)
    lines = [
        "Finite-proper-time timelike horizon crossing example",
        "",
        "Curve:",
        "  r(t) = q t, starting at t=0, r=0 in the bubble region",
        f"  q = dr/dt = {q}",
        "",
        "Timelike condition:",
        "  ds^2 = -dt^2 + [dr - vbar(r)dt]^2",
        "  dτ/dt = sqrt(1 - [q - vbar(r)]^2)",
        "  timelike iff |q - vbar(r)| < 1",
        "",
        f"Crosses r1 = {r1:.12f} at t = {t_cross:.12f}",
        f"Proper time from r=0 to r=r1: τ = {tau:.12f}",
        f"quadrature error estimate: {err:.3e}",
        f"dτ/dt at r=0: {gamma_inv(r_start):.12f}",
        f"dτ/dt at r=r1: {gamma_inv(r1):.12f}",
        "",
        "Important correction:",
        "  Keeping the same constant q=-0.5 after crossing is not timelike forever in exterior region I.",
        "  In region I, vbar(r) continues toward -alpha=-2.",
        "  The constant-q curve becomes null when q - vbar(r) = 1.",
        f"  This occurs at r = {r_null:.12f}, t = {t_null:.12f}.",
        f"  Additional proper time from r1 to that null point: Δτ = {tau_after:.12f}",
        f"  Total proper time from r=0 to null point: τ = {tau + tau_after:.12f}",
        "",
        "Interpretation:",
        "  The curve crosses a finite-w point of the r=r1 horizon in finite proper time.",
        "  The post-crossing constant-q continuation is only a local example; a physical observer",
        "  that wants to remain timelike deeper in region I must accelerate/change q.",
    ]
    (p.out_dir / "timelike_crossing_example.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def front_endpoint_timelike_example(p: Params) -> None:
    """Construct a timelike curve that reaches the future r2 endpoint.

    This is not a constant-relative-velocity observer.  It accelerates so that
    its coordinate speed approaches the outgoing null speed near r2.
    """
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)
    a = 0.4

    # Curve: r(t)=r2-r2 exp(-a t), so q=dr/dt=a(r2-r).
    # It starts at r=0,t=0 and approaches r2 as t->infinity.
    def q_of_r(r: float) -> float:
        return a * (r2 - r)

    def timelike_margin(r: float) -> float:
        vv = float(vbar(r, p))
        q = q_of_r(r)
        return 1.0 - (q - vv) ** 2

    def tau_integrand(r: float) -> float:
        return np.sqrt(max(timelike_margin(r), 0.0)) / q_of_r(r)

    tau, err = quad(tau_integrand, 0.0, r2, points=[r2], epsabs=1.0e-11, epsrel=1.0e-11, limit=400)
    rs = np.linspace(0.0, r2 - 1.0e-9, 20001)
    q = q_of_r(rs)
    upper = vbar(rs, p) + 1.0
    lower = vbar(rs, p) - 1.0
    margin_upper = float(np.min(upper - q))
    margin_lower = float(np.min(q - lower))
    min_timelike_margin = float(np.min(1.0 - (q - vbar(rs, p)) ** 2))

    lines = [
        "Front-endpoint timelike curve check",
        "",
        "Purpose:",
        "  Test whether every timelike observer is excluded from the future r2 patch endpoint.",
        "  Answer: no. Bounded-rapidity/fixed-q observers are excluded, but an accelerated",
        "  observer can approach the outgoing null direction fast enough to reach the endpoint",
        "  at finite proper time.",
        "",
        "Curve:",
        "  r(t) = r2 - r2 exp(-a t), starting at t=0, r=0",
        "  q(t) = dr/dt = a [r2-r(t)]",
        f"  a = {a:.12f}, r2 = {r2:.12f}, kappa = {kap:.12f}",
        "",
        "Future timelike condition:",
        "  vbar(r)-1 < q < vbar(r)+1",
        "  equivalently 1 - [q-vbar(r)]^2 > 0.",
        f"  min[vbar+1-q] over sampled 0<=r<r2: {margin_upper:.12e}",
        f"  min[q-(vbar-1)] over sampled 0<=r<r2: {margin_lower:.12e}",
        f"  min timelike margin over sampled 0<=r<r2: {min_timelike_margin:.12e}",
        "",
        "Proper time:",
        "  dτ = sqrt(1-[q-vbar(r)]^2) dt",
        "  dt = dr/[a(r2-r)]",
        f"  τ(0 -> r2 endpoint) = {tau:.12f}",
        f"  quadrature error estimate: {err:.3e}",
        "",
        "Near-endpoint asymptotics:",
        "  let x = r2-r. Then vbar+1 ~ kappa x and q = a x.",
        "  Since a < kappa, the curve remains inside the future light cone.",
        "  dτ/dt ~ sqrt(2(kappa-a)x), while x = r2 exp(-a t).",
        "  Therefore ∫ dτ converges even though t->infinity.",
        "",
        "Caveat:",
        "  The relative gamma diverges as the curve approaches the endpoint.",
        "  So this is an infinitely boosted/asymptotically null timelike worldline,",
        "  not a fixed-velocity traveler and not evidence that ordinary bounded",
        "  observers cross the front horizon.",
    ]
    (p.out_dir / "front_endpoint_timelike_example.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def white_horizon_extension_analysis(p: Params) -> None:
    """Analyze the future endpoint of the front/white horizon r=r2."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    # Near r2, use x=r-r2.  Since vbar'(r2)=-kap:
    #   1+vbar ~ -kap x
    #   C=1-vbar^2 ~ -2 kap x.
    # The coordinates U=exp(kap u), V=exp(-kap w) make both the finite-r
    # horizon (U=0) and its future endpoint (V=0) finite-coordinate loci.
    rows = []
    for side, region, signs in [
        ("inside II", "II", [-1.0]),
        ("outside III", "III", [1.0]),
    ]:
        for eps in [1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6]:
            r = np.array([r2 + signs[0] * eps])
            t = np.array([0.0])
            u = u_region(region, t, r, p)
            w = w_coord(t, r, p)
            U = np.exp(kap * u)
            V = np.exp(-kap * w)
            conformal = C_factor(r, p) / (kap * kap * U * V)
            rows.append((side, eps, float(U[0]), float(V[0]), float(conformal[0])))

    lines = [
        "Front/white horizon r2 extension calculation",
        "",
        "Metric:",
        "  ds^2 = -C(r) du dw,  C(r)=1-vbar(r)^2",
        "",
        f"r2 = {r2:.12f}",
        f"kappa = {kap:.12f}",
        "",
        "Near r2, with x=r-r2:",
        "  vbar(r) = -1 - kappa x + O(x^2)",
        "  1+vbar = -kappa x + O(x^2)",
        "  C(r) = -2 kappa x + O(x^2)",
        "  u = t + (1/kappa) log|x| + O(1)",
        "  w = t + O(1)",
        "",
        "A chart for the future endpoint of the r2 horizon is:",
        "  U = exp(kappa u)",
        "  V = exp(-kappa w)",
        "",
        "Then:",
        "  du = dU/(kappa U)",
        "  dw = -dV/(kappa V)",
        "  ds^2 = [C(r)/(kappa^2 U V)] dU dV.",
        "",
        "Because U V is proportional to |r-r2| near the horizon,",
        "C/(kappa^2 U V) has a finite nonzero limit after choosing",
        "the usual side-dependent orientation/normalization. Thus the",
        "corner U=0,V=0 is locally a regular analytic extension point",
        "of the fixed 1+1 metric, not a curvature singularity.",
        "",
        "Numerical check of unnormalized conformal factor:",
        "  side | eps=|r-r2| | U | V | C/(kappa^2 U V)",
    ]
    for side, eps, U, V, conformal in rows:
        lines.append(f"  {side:11s} | {eps:.0e} | {U:.8e} | {V:.8e} | {conformal: .8e}")

    lines.extend(
        [
            "",
            "Affine parameter along the r2 generator:",
            "  The horizon generator is k=partial_t at r=r2.",
            "  k^a nabla_a k^b = kappa_h k^b with kappa_h = vbar'(r2) = -kappa.",
            "  If t is the Killing parameter, d lambda/dt is proportional to exp(-kappa t).",
            "  Equivalently, along r=r2, V=exp(-kappa w) is proportional to an affine parameter.",
            "",
            "Therefore:",
            "  as t -> -infinity, V -> +infinity: infinite affine length into the past.",
            "  as t -> +infinity, V -> 0: finite affine length into the future.",
            "",
            "Extension statement:",
            "  The past direction of this white-horizon generator is complete within this block.",
            "  The future endpoint is incomplete and can be locally extended by allowing V",
            "  to continue through 0 in the (U,V) chart. This local calculation does not",
            "  by itself impose a unique global matter-filled universe beyond the extension.",
        ]
    )
    (p.out_dir / "white_horizon_extension.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_minimal_front_extension(p: Params) -> None:
    """Plot a minimal local extension through the future r2 Cauchy endpoint.

    This is a local (U,V) chart, not a global Penrose diagram.  The original
    stationary patch occupies V>0 near the endpoint.  Analytic continuation of
    the same local metric coefficient allows V<0.
    """
    p.out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7.0, 5.8), constrained_layout=True)
    U = np.linspace(-1.0, 1.0, 401)
    V = np.linspace(-1.0, 1.0, 401)

    # The original patch near the future front endpoint is the quadrant U>=0,V>=0
    # up to orientation conventions.  The minimal extension across the endpoint
    # is represented by adjoining V<0.
    ax.fill_between([0, 1], 0, 1, color="#eaf3f6", alpha=0.95, label="original patch near C+")
    ax.fill_between([0, 1], -1, 0, color="#f6efe6", alpha=0.95, label="one analytic extension")

    ax.axhline(0.0, color="#0b7a63", lw=2.3, ls="--", label="C+ crossing surface V=0")
    ax.axvline(0.0, color="#60717a", lw=1.2, alpha=0.85, label="horizon line U=0")

    # Null geodesics in 2D conformal coordinates are U=const or V=const.
    # The finite-affine front generator/crossing branch continues through V=0.
    for u0, alpha in [(0.18, 1.0), (0.36, 0.55), (0.58, 0.35)]:
        ax.plot([u0, u0], [0.92, -0.92], color="#c14d3f", lw=3.0 if alpha == 1.0 else 1.8, alpha=alpha)
    ax.annotate(
        "continued null geodesic\nfinite affine at V=0",
        xy=(0.18, 0.0),
        xytext=(0.52, 0.36),
        arrowprops={"arrowstyle": "->", "color": "#8e362c", "lw": 1.0},
        color="#8e362c",
        fontsize=10,
        ha="center",
    )

    # Timelike accelerated curves can approach the same endpoint from inside.
    s = np.linspace(0.02, 0.98, 300)
    U_curve = 0.10 + 0.28 * s
    V_curve = 0.78 * (1 - s) ** 2
    ax.plot(U_curve, V_curve, color="#1f6f8b", lw=2.0)
    ax.annotate(
        "asymptotically-null\ntimelike curve",
        xy=(U_curve[-1], V_curve[-1]),
        xytext=(0.68, 0.13),
        arrowprops={"arrowstyle": "->", "color": "#1f6f8b", "lw": 1.0},
        color="#1f6f8b",
        fontsize=9,
        ha="center",
    )

    ax.scatter([0.0], [0.0], s=50, color="#20252b", zorder=5)
    ax.text(0.03, -0.08, "front Cauchy endpoint\nU=V=0", fontsize=9, ha="left", va="top")

    ax.text(
        -0.96,
        0.94,
        "Local endpoint chart:\n"
        "U = exp(kappa u)\n"
        "V = exp(-kappa w)\n"
        "ds^2 = F(U,V)dU dV\n"
        "F analytic, nonzero at U=V=0",
        fontsize=9,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.text(
        -0.96,
        -0.94,
        "This proves a local extension exists.\n"
        "It does not yet choose a global maximal tiling.",
        fontsize=9,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )

    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("U")
    ax.set_ylabel("V")
    ax.set_title("Minimal local extension through the front Cauchy endpoint")
    ax.grid(True, alpha=0.18)
    ax.legend(loc="upper right", fontsize=8)
    fig.savefig(p.out_dir / "minimal_front_cauchy_extension.png", dpi=180)
    plt.close(fig)


def plot_accurate_local_front_extension(p: Params) -> None:
    """Accurate local conformal diagram across the future front Cauchy point.

    The plotted coordinates are compactified Kruskal-endpoint coordinates:
        U = exp(kappa u), V = exp(-kappa w).
    Curves in the original patch (V>0) are generated from the exact closed-form
    sech coordinates.  The V<0 half is the analytic continuation of the same
    local metric coefficient F(X), where X is the oriented branch of UV;
    constant-X curves are therefore exact
    local constant-r continuations, even though the old t label is unavailable
    there.
    """
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    def endpoint_uv(region: str, t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region(region, t, r, p)
        w = w_coord(t, r, p)
        return np.exp(kap * u), np.exp(-kap * w)

    def penrose(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        uu = np.arctan(U)
        vv = np.arctan(V)
        return 0.5 * (vv - uu), 0.5 * (vv + uu)

    fig, ax = plt.subplots(figsize=(8.0, 7.4), constrained_layout=True)

    # Exact old-patch curves, close enough to r2 for the endpoint chart.
    t_vals = np.linspace(0.0, 18.0, 700)
    r_vals_inside = r2 - np.array([0.72, 0.45, 0.27, 0.16, 0.095, 0.055, 0.032])
    for r0 in r_vals_inside:
        U, V = endpoint_uv("II", t_vals, np.full_like(t_vals, r0))
        x, y = penrose(U, V)
        ax.plot(x, y, color="#20252b", lw=1.0, alpha=0.78)

    for t0 in np.linspace(1.0, 16.0, 8):
        rr = np.linspace(r2 - 0.74, r2 - 0.018, 600)
        tt = np.full_like(rr, t0)
        U, V = endpoint_uv("II", tt, rr)
        x, y = penrose(U, V)
        ax.plot(x, y, color="#8b9095", lw=0.8, ls=(0, (6, 5)), alpha=0.62)

    # Horizon side r2 approached from inside: U->0, V finite-positive.
    Vh = np.geomspace(0.018, 1.2, 400)
    Uh = np.zeros_like(Vh)
    xh, yh = penrose(Uh, Vh)
    ax.plot(xh, yh, color="#0b7a63", lw=2.4, ls="--", label=r"$r_2$ horizon, original side")

    # V=0 is a local null-coordinate line.  We only know that the corner
    # U=V=0 is the C+ endpoint reached by the r2 generator; drawing all of
    # V=0 as a Cauchy surface would overstate the calculation.  Keep it as a
    # faint coordinate guide only.
    Uline = np.geomspace(0.018, 1.2, 400)
    Vzero = np.zeros_like(Uline)
    xc, yc = penrose(Uline, Vzero)
    ax.plot(xc, yc, color="#b7791f", lw=1.0, alpha=0.35, ls=(0, (4, 4)), label=r"local null coordinate $V=0$")

    # The finite-affine null generator is the r2 horizon itself in this local
    # chart: U=0, with V proportional to affine parameter. It reaches the
    # Cauchy endpoint at V=0 and continues by allowing V to change sign.
    Vcurve = np.linspace(0.9, -0.9, 800)
    Ucurve = np.zeros_like(Vcurve)
    x, y = penrose(Ucurve, Vcurve)
    ax.plot(x, y, color="#c14d3f", lw=2.8, alpha=1.0, label="continued finite-affine null generator")
    ax.annotate(
        "single justified finite-affine\nC+ generator/separatrix",
        xy=tuple(float(v[0]) for v in penrose(np.array([0.0]), np.array([0.0]))),
        xytext=(-0.43, 0.23),
        arrowprops={"arrowstyle": "->", "color": "#8e362c", "lw": 1.0},
        color="#8e362c",
        fontsize=9,
        ha="center",
    )

    # Constant-X curves in the extended chart.  For this forward chart
    # orientation, X=-UV matches X<0 to the old bubble side r<r2.
    for Z0 in [0.006, 0.018, 0.045, -0.006, -0.018, -0.045]:
        U = np.geomspace(0.045, 1.15, 500)
        V = -Z0 / U
        mask = np.abs(V) <= 1.15
        x, y = penrose(U[mask], V[mask])
        ax.plot(
            x,
            y,
            color="#3f4750" if Z0 > 0 else "#6f5b45",
            lw=0.9,
            ls="-" if Z0 > 0 else (0, (5, 4)),
            alpha=0.72,
        )

    ax.scatter(*penrose(np.array([0.0]), np.array([0.0])), s=48, color="#20252b", zorder=5)
    ax.text(0.025, -0.035, r"$C^+$ corner" "\n" r"$U=V=0$", fontsize=9, ha="left", va="top")

    ax.text(
        -0.75,
        0.57,
        "Generated from exact sech coordinates on V>0:\n"
        "U=exp(kappa u_II), V=exp(-kappa w).\n"
        "Only the corner U=V=0 is identified as C+.",
        fontsize=8.7,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.text(
        0.15,
        -0.60,
        "solid dark: constant r in old patch\n"
        "gray dashed: constant t in old patch\n"
        "brown dashed: continued constant-X branches\n"
        "red: one established finite-affine generator",
        fontsize=8.5,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )

    ax.set_xlim(-0.78, 0.48)
    ax.set_ylim(-0.68, 0.68)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"$(\arctan V-\arctan U)/2$")
    ax.set_ylabel(r"$(\arctan V+\arctan U)/2$")
    ax.set_title("Accurate local conformal chart across the front Cauchy endpoint")
    ax.grid(True, alpha=0.16)
    ax.legend(loc="lower left", fontsize=8)
    fig.savefig(p.out_dir / "accurate_local_front_extension.png", dpi=180)
    plt.close(fig)

    notes = [
        "Accurate local front Cauchy extension chart",
        "",
        "Coordinates:",
        "  U = exp(kappa u_II)",
        "  V = exp(-kappa w)",
        "  compactified with arctan U, arctan V",
        "",
        "Old patch:",
        "  V > 0, U >= 0 near the future r2 endpoint.",
        "  Solid and dashed curves on V>0 are generated from exact closed-form sech coordinates.",
        "",
        "Analytic continuation:",
        "  The metric is ds^2 = F(X) dU dV with oriented X=-UV in this chart.",
        "  X = a1(r-r2)+O((r-r2)^2), a1 != 0, so r=R(X).",
        "  F(X)=C(R(X))/(kappa^2 X) is analytic and nonzero at X=0.",
        "  Along the generator U=0, allowing V to pass through 0 continues",
        "  the incomplete null geodesic through C+.",
        "",
        "Important non-claim:",
        "  The line V=0 with U>0 is only a local null coordinate line in this",
        "  chart. It is not being identified as a proven Cauchy surface of the",
        "  original global diamond. The established C+ object here is the corner",
        "  U=V=0 reached by the r2 generator.",
        "",
        "Finite-affine geodesic shown:",
        "  Only one globally justified C+ separatrix/generator is highlighted.",
        "  In these coordinates it is U=0, and V is proportional to affine",
        "  parameter on the generator. It reaches C+ at V=0.",
        "  Other local null coordinate lines are not claimed as finite-affine",
        "  exits from the original diamond.",
        "",
        "Limit of this figure:",
        "  It is an accurate local conformal chart, not a full global Penrose diagram.",
        "  The old t coordinate is intentionally not extended to V<0.",
    ]
    (p.out_dir / "accurate_local_front_extension_notes.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")


def front_generator_affine_calculation(p: Params) -> None:
    """Write the explicit affine calculation for the r2 front generator."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)
    vp = -kap
    lines = [
        "Front r2 generator affine calculation",
        "",
        "Metric:",
        "  ds^2 = -dt^2 + (dr - vbar(r)dt)^2",
        "",
        "Horizon:",
        f"  r2 = {r2:.12f}",
        "  vbar(r2) = -1",
        f"  vbar'(r2) = {vp:.12f} = -kappa",
        "",
        "The r=r2 horizon generator:",
        "  tangent k = partial_t = (dt/ds, dr/ds) = (1,0) using Killing parameter s=t.",
        "  Since ds^2(k,k)=-(1-vbar^2)=0 at r2, k is null there.",
        "",
        "Non-affinity:",
        "  Direct Christoffel calculation for k=partial_t gives",
        "    k^a nabla_a k^b = vbar'(r2) k^b = -kappa k^b.",
        "  Therefore t is not affine.",
        "",
        "Affine parameter lambda:",
        "  If k=d/dt and l=d/dlambda = (dt/dlambda) k, the affine condition gives",
        "    d/dt ln(dt/dlambda) = -vbar'(r2) = kappa.",
        "  Hence dt/dlambda proportional to exp(kappa t), so",
        "    dlambda/dt proportional to exp(-kappa t).",
        "  Choose lambda = -A exp(-kappa t), or equivalently V=A exp(-kappa w).",
        "",
        "Endpoint behavior:",
        "  along r=r2, w=t+constant, so V=exp(-kappa w) is proportional to affine parameter.",
        "  t -> -infinity gives |lambda| -> infinity.",
        "  t -> +infinity gives lambda -> 0 finite.",
        "",
        "Endpoint chart:",
        "  U = exp(kappa u), V = exp(-kappa w).",
        "  The r2 horizon is U=0.",
        "  The finite future Cauchy endpoint is U=0,V=0.",
        "  The correct continued finite-affine generator is U=0 crossing V=0.",
        "  The rest of the local line V=0 at U>0 is not identified here as a",
        "  global Cauchy horizon; it is only a coordinate-null line of the local",
        "  endpoint chart unless separately derived.",
        "",
        "Correction to earlier plot:",
        "  A line U=constant>0 crossing V=0 is a local null coordinate line in the",
        "  endpoint chart, but it is not the r2 horizon generator from the original",
        "  diamond and should not be highlighted as the finite-affine C+ generator.",
    ]
    (p.out_dir / "front_generator_affine_calculation.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def front_endpoint_branch_series(p: Params) -> None:
    """Compute the local branch variable around r2 for the endpoint chart."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    rows = []
    for side, region, sign, orient in [
        ("inside II", "II", -1.0, -1.0),
        ("outside III", "III", 1.0, 1.0),
    ]:
        for eps in [1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6]:
            r = np.array([r2 + sign * eps])
            t = np.array([0.0])
            u = u_region(region, t, r, p)
            w = w_coord(t, r, p)
            Z = float(np.exp(kap * (u - w))[0])
            X = orient * Z
            dr = float(r[0] - r2)
            rows.append((side, eps, dr, Z, X, X / dr, float(C_factor(r, p)[0] / X)))

    # Estimate the one-sided Taylor coefficients X = a1 dr + a2 dr^2 + ...
    coeff_rows = []
    for side, region, sign, orient in [
        ("inside II", "II", -1.0, -1.0),
        ("outside III", "III", 1.0, 1.0),
    ]:
        eps = np.geomspace(1.0e-6, 4.0e-2, 80)
        dr = sign * eps
        rr = r2 + dr
        tt = np.zeros_like(rr)
        u = u_region(region, tt, rr, p)
        w = w_coord(tt, rr, p)
        X = orient * np.exp(kap * (u - w))
        # Fit X/dr = a1 + a2 dr + a3 dr^2 near the endpoint.
        y = X / dr
        A = np.column_stack([np.ones_like(dr), dr, dr * dr])
        a1, a2, a3 = np.linalg.lstsq(A, y, rcond=None)[0]
        coeff_rows.append((side, a1, a2, a3))

    lines = [
        "Front endpoint local branch series",
        "",
        "Endpoint chart:",
        "  U = exp(kappa u)",
        "  V = exp(-kappa w)",
        "  raw Z = U V = exp(kappa(u-w))",
        "",
        "Important branch fact:",
        "  The closed-form regional u coordinates use separate logarithmic branches.",
        "  Raw Z is positive on both old-patch sides of r2.",
        "  The oriented analytic radial variable is",
        "    X = -Z on the inside II side",
        "    X = +Z on the outside III side",
        "  so X is proportional to r-r2 with the correct sign.",
        "",
        "Numerical limit:",
        "  X = a1 (r-r2) + O((r-r2)^2), with a1 nonzero.",
        "",
        "side | eps | dr | raw Z | oriented X | X/dr | C/X",
    ]
    for side, eps, dr, Z, X, ratio, c_over_x in rows:
        lines.append(f"{side:10s} | {eps:.0e} | {dr: .8e} | {Z:.8e} | {X: .8e} | {ratio: .8e} | {c_over_x: .8e}")

    lines.extend(["", "Least-squares local Taylor estimates for X/dr = a1 + a2 dr + a3 dr^2:"])
    for side, a1, a2, a3 in coeff_rows:
        lines.append(f"  {side:10s}: a1={a1:.12e}, a2={a2:.12e}, a3={a3:.12e}")

    lines.extend(
        [
            "",
            "Consequence:",
            "  Since a1 != 0, the analytic inverse function theorem gives",
            "    r-r2 = b1 X + b2 X^2 + ...",
            "  locally. The continued side can therefore be described by allowing",
            "  the oriented X branch coordinate to pass through zero.",
            "",
            "Caution:",
            "  This determines the local radial branch across r2/C+.",
            "  It does not by itself identify an entire global diamond beyond the endpoint.",
        ]
    )
    (p.out_dir / "front_endpoint_branch_series.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_forward_extension_atlas(p: Params) -> None:
    """Assemble the justified forward C+ extension as a local atlas diagram."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    fig, axes = plt.subplots(1, 2, figsize=(13.2, 6.2), constrained_layout=True)

    # Left panel: original three-region conformal patch, with the C+ corner and
    # r2 generator highlighted.  This uses the same compact coordinates as the
    # original patch plot.
    ax = axes[0]
    eps = 1.0e-5 * (2 * r2)
    t = np.linspace(-p.t_max, p.t_max, 1200)
    for region, r0, color, label in [
        ("II", r2 - eps, "#c14d3f", r"finite-affine $r_2$ generator"),
        ("III", r2 + eps, "#0b7a63", r"$r_2$ exterior side"),
    ]:
        x, y = compact(region, t, np.full_like(t, r0), p)
        ax.plot(x, y, color=color, lw=2.7 if color == "#c14d3f" else 1.8, ls="-" if color == "#c14d3f" else "--", label=label)

    # Add a light background of region II constant-r curves.
    for r0 in np.linspace(-0.5, r2 - 0.18, 5):
        x, y = compact("II", t, np.full_like(t, r0), p)
        ax.plot(x, y, color="#20252b", lw=0.75, alpha=0.35)
    for t0 in np.linspace(-5.5, 5.5, 7):
        rr = np.linspace(-0.6, r2 - eps, 800)
        x, y = compact("II", np.full_like(rr, t0), rr, p)
        ax.plot(x, y, color="#8b9095", lw=0.65, ls=(0, (6, 5)), alpha=0.35)

    # Mark approximate future endpoint using large t on r2 generator.
    x_end, y_end = compact("II", np.array([p.t_max]), np.array([r2 - eps]), p)
    ax.scatter(x_end, y_end, s=58, color="#20252b", zorder=6)
    ax.annotate(
        r"$C^+$ corner" "\n" r"$r\to r_2,\ t\to+\infty$",
        xy=(float(x_end[0]), float(y_end[0])),
        xytext=(float(x_end[0]) - 0.55, float(y_end[0]) + 0.24),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=9,
        ha="center",
    )
    ax.set_title("Original patch: the only forward endpoint we extend")
    ax.set_xlabel(r"$(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"$(\mathcal{W}+\mathcal{U})/2$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.legend(loc="lower right", fontsize=8)

    # Right panel: local endpoint atlas.  This is a zoomed conformal chart, not
    # a complete next diamond.
    ax = axes[1]

    def penrose(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        uu = np.arctan(U)
        vv = np.arctan(V)
        return 0.5 * (vv - uu), 0.5 * (vv + uu)

    # Original local side and forward extension side along the generator.
    ax.fill_between([0.0, 0.9], 0.0, 0.9, color="#eaf3f6", alpha=0.75, label="old local side near C+")
    ax.fill_between([0.0, 0.9], -0.9, 0.0, color="#f6efe6", alpha=0.75, label="forward local extension")

    V = np.linspace(0.9, -0.9, 800)
    U = np.zeros_like(V)
    x, y = penrose(U, V)
    ax.plot(x, y, color="#c14d3f", lw=3.0, label=r"continued $r_2$ generator $U=0$")
    ax.scatter(*penrose(np.array([0.0]), np.array([0.0])), s=62, color="#20252b", zorder=6)

    # Faint coordinate guides only.
    Uguide = np.linspace(0.02, 0.9, 400)
    xg, yg = penrose(Uguide, np.zeros_like(Uguide))
    ax.plot(xg, yg, color="#b7791f", lw=1.0, alpha=0.35, ls=(0, (4, 4)), label=r"coordinate line $V=0$, not global C+")

    for X0 in [-0.04, -0.015, 0.015, 0.04]:
        Uv = np.geomspace(0.05, 0.9, 400)
        Vv = -X0 / Uv
        mask = np.abs(Vv) <= 0.9
        xp, yp = penrose(Uv[mask], Vv[mask])
        ax.plot(xp, yp, color="#6f5b45" if X0 < 0 else "#3f4750", lw=0.9, ls=(0, (5, 4)) if X0 < 0 else "-", alpha=0.7)

    ax.annotate(
        "glue by analytic continuation\nof F(X), X=-UV",
        xy=tuple(float(v[0]) for v in penrose(np.array([0.0]), np.array([0.0]))),
        xytext=(-0.43, -0.18),
        arrowprops={"arrowstyle": "->", "color": "#333333", "lw": 1.0},
        fontsize=9,
        ha="center",
    )
    ax.text(
        -0.74,
        0.55,
        "Forward atlas data:\n"
        "U=exp(kappa u)\n"
        "V=exp(-kappa w) ~ affine\n"
        "r2 generator: U=0\n"
        "C+ endpoint: U=V=0",
        fontsize=8.7,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.text(
        -0.74,
        -0.55,
        "This is one local extension.\n"
        "No full next diamond is asserted.",
        fontsize=8.7,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.set_title("Forward local extension chart")
    ax.set_xlabel(r"$(\arctan V-\arctan U)/2$")
    ax.set_ylabel(r"$(\arctan V+\arctan U)/2$")
    ax.set_xlim(-0.78, 0.45)
    ax.set_ylim(-0.62, 0.62)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.legend(loc="lower right", fontsize=8)

    fig.savefig(p.out_dir / "forward_cplus_extension_atlas.png", dpi=180)
    plt.close(fig)

    notes = [
        "Forward C+ extension atlas",
        "",
        "This file describes only the extension through the front future endpoint",
        "reached by the r2 horizon generator. It does not claim a full maximal",
        "extension or a full attached diamond.",
        "",
        "Original endpoint:",
        "  r -> r2, t -> +infinity along the r2 generator.",
        "",
        "Endpoint coordinates:",
        "  U = exp(kappa u)",
        "  V = exp(-kappa w)",
        "  r2 generator: U=0",
        "  affine parameter on the generator: V up to a constant factor",
        "  C+ endpoint: U=0,V=0",
        "",
        "Metric:",
        "  ds^2 = F(X) dU dV",
        "  X=-UV in this forward chart, with X=a1(r-r2)+O((r-r2)^2).",
        "  The branch calculation gives a1 about 1.158201, nonzero.",
        "  Therefore r=R(X) locally and F(X) is analytic/nonzero at X=0.",
        "",
        "Gluing/extension:",
        "  The old local side contains V>0 on the r2 generator.",
        "  The forward extension allows V<0 on the same U=0 generator.",
        "  This continues the finite-affine null geodesic through C+.",
        "",
        "Non-claims:",
        "  V=0,U>0 is not identified as a global Cauchy horizon.",
        "  The global boundaries of the attached side are not determined here.",
        "  The diagram is an atlas/coordinate-extension figure, not a global Penrose diagram.",
    ]
    (p.out_dir / "forward_cplus_extension_atlas_notes.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")


def local_front_geodesic_regularization(p: Params) -> None:
    """Check geodesic regularity in the local front C+ extension chart."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    samples = []
    Xs = []
    Fs = []
    for side, region, sign, orient in [
        ("inside II", "II", -1.0, -1.0),
        ("outside III", "III", 1.0, 1.0),
    ]:
        eps = np.geomspace(1.0e-7, 2.0e-2, 120)
        dr = sign * eps
        r = r2 + dr
        t = np.zeros_like(r)
        u = u_region(region, t, r, p)
        w = w_coord(t, r, p)
        raw_z = np.exp(kap * (u - w))
        X = orient * raw_z
        C = C_factor(r, p)
        # In ds^2 = [C/(kappa^2 U V)] dU dV, replace UV by oriented X.
        # Overall orientation signs are conventional; regularity is checked by
        # the existence of a common finite branch F(X).
        F = C / (kap * kap * X)
        Xs.append(X)
        Fs.append(F)
        for idx in [0, 20, 50, 90, 119]:
            samples.append((side, float(dr[idx]), float(X[idx]), float(F[idx])))

    X_all = np.concatenate(Xs)
    F_all = np.concatenate(Fs)
    # Fit F(X)=F0+F1 X+F2 X^2 locally using both sides.
    mask = np.abs(X_all) < 2.5e-3
    A = np.column_stack([np.ones(np.count_nonzero(mask)), X_all[mask], X_all[mask] ** 2])
    F0, F1, F2 = np.linalg.lstsq(A, F_all[mask], rcond=None)[0]

    lines = [
        "Local front C+ geodesic regularization",
        "",
        "Local metric form:",
        "  ds^2 = F(X) dU dV",
        "  X is the oriented branch variable with X=0 at C+.",
        "",
        "Numerical branch fit near X=0:",
        f"  F(X) = F0 + F1 X + F2 X^2 + ...",
        f"  F0 = {F0:.12e}",
        f"  F1 = {F1:.12e}",
        f"  F2 = {F2:.12e}",
        "",
        "Sample values:",
        "  side | dr | X | F=C/(kappa^2 X)",
    ]
    for side, dr, X, F in samples:
        lines.append(f"  {side:10s} | {dr: .8e} | {X: .8e} | {F: .8e}")

    lines.extend(
        [
            "",
            "Christoffels for a 1+1 conformal null metric:",
            "  ds^2 = F(U,V) dU dV",
            "  Gamma^U_UU = partial_U ln|F|",
            "  Gamma^V_VV = partial_V ln|F|",
            "  all mixed null Christoffels vanish in these coordinates.",
            "",
            "Here F=F(X) and, in the forward chart, X=-UV.",
            "Therefore:",
            "  partial_U ln|F| = (F'/F) partial_U X",
            "  partial_V ln|F| = (F'/F) partial_V X.",
            "",
            "On the continued r2 generator:",
            "  U(lambda)=0",
            "  V(lambda)=lambda",
            "  X=0 along the generator",
            "  partial_V X is proportional to U, hence partial_V X=0 on U=0.",
            "",
            "Geodesic equation for V(lambda):",
            "  d2V/dlambda2 + Gamma^V_VV (dV/dlambda)^2 = 0.",
            "  Since Gamma^V_VV=0 on U=0 and V=lambda, this is satisfied.",
            "",
            "Geodesic equation for U(lambda):",
            "  d2U/dlambda2 + Gamma^U_UU (dU/dlambda)^2 = 0.",
            "  Since U=0 and dU/dlambda=0, this is satisfied.",
            "",
            "Conclusion:",
            "  The incomplete r2 generator continues smoothly through lambda=0",
            "  as U=0,V=lambda in the local extension chart.",
            "  F and its first derivative are finite in the fitted branch, so nearby",
            "  geodesic ODEs are regular locally. This is a local result only.",
        ]
    )
    (p.out_dir / "local_front_geodesic_regularization.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def forward_extension_region_classification(p: Params) -> None:
    """Classify the local regions around the forward C+ extension."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    # Use the fitted inverse relation from the branch calculation.  For local
    # classification the first derivative is enough: X ~= a1 (r-r2).
    eps = np.geomspace(1.0e-7, 1.0e-4, 20)
    ratios = []
    for region, sign, orient in [("II", -1.0, -1.0), ("III", 1.0, 1.0)]:
        r = r2 + sign * eps
        t = np.zeros_like(r)
        u = u_region(region, t, r, p)
        w = w_coord(t, r, p)
        X = orient * np.exp(kap * (u - w))
        ratios.extend((X / (r - r2)).tolist())
    a1 = float(np.mean(ratios))

    # C ~= C'(r2)(r-r2), and C'(r2)=2 kappa for our sign convention?
    # Numerically evaluate dC/dX from the fitted local branch.
    xs = np.array([-1.0e-4, -1.0e-5, 1.0e-5, 1.0e-4])
    # r-r2 ~= X/a1
    drs = xs / a1
    Cs = C_factor(r2 + drs, p)
    c_over_x = Cs / xs

    quadrants = [
        ("old-side II neighborhood", "+", "+", "-", "r<r2", "C>0", "constant-r timelike"),
        ("forward continuation across C+", "+", "-", "+", "r>r2 locally", "C<0", "constant-r spacelike"),
        ("other local quadrant", "-", "+", "+", "r>r2 locally", "C<0", "constant-r spacelike"),
        ("other local quadrant", "-", "-", "-", "r<r2 locally", "C>0", "constant-r timelike"),
    ]

    lines = [
        "Forward extension local region classification",
        "",
        "Coordinates near C+:",
        "  U = exp(kappa u), V = exp(-kappa w)",
        "  r2 generator is U=0",
        "  affine parameter along it is V",
        "",
        "Branch convention used for classification:",
        "  X = -U V in the forward local atlas orientation",
        "  X ~= a1 (r-r2)",
        f"  a1 ~= {a1:.12e}",
        "",
        "Numerical check of C/X near X=0:",
    ]
    for x, c, ratio in zip(xs, Cs, c_over_x):
        lines.append(f"  X={x: .1e}: C={c: .8e}, C/X={ratio: .8e}")
    lines.extend(
        [
            "",
            "Thus locally:",
            "  X < 0 corresponds to r<r2, C>0: bubble-side causal character.",
            "  X > 0 corresponds to r>r2, C<0: exterior/trapped-side causal character.",
            "",
        "Quadrant classification using signs of U,V:",
        "  label | sign(U) | sign(V) | sign(X=-UV) | local r-side | C sign | constant-r character",
        ]
    )
    for row in quadrants:
        lines.append("  " + " | ".join(row))
    lines.extend(
        [
            "",
            "Forward continuation from the original r2 generator:",
            "  Original generator approaches C+ along U=0,V>0.",
            "  Continuing through the endpoint gives U=0,V<0.",
            "  With the forward orientation X=-UV, a small neighborhood with",
            "  U>0,V<0 has X>0, hence r>r2 locally and C<0.",
            "",
            "Important limitation:",
            "  This local classification tells us the causal character immediately",
            "  beyond C+. It still does not identify the global far boundary of the",
            "  attached side.",
        ]
    )
    (p.out_dir / "forward_extension_region_classification.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def forward_extension_branch_global_scan(p: Params) -> None:
    """Scan the r>r2 branch in the forward endpoint variables."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    # In region III, raw Z=exp(kappa(u-w)) is positive and locally proportional
    # to r-r2.  In the forward extension chart X=-UV has the same local sign
    # structure for the U>0,V<0 quadrant; numerically we scan X_III=raw Z as
    # the positive radial branch coordinate.
    r = np.r_[r2 + np.geomspace(1.0e-8, 1.0e-2, 500), np.linspace(r2 + 1.0e-2, 60.0, 3000)[1:]]
    t = np.zeros_like(r)
    u = u_region("III", t, r, p)
    w = w_coord(t, r, p)
    X = np.exp(kap * (u - w))
    C = C_factor(r, p)
    dX = np.diff(X)
    monotone = bool(np.all(dX > 0))
    min_dx = float(np.min(dX))

    # Sample larger radii to estimate the asymptotic behavior.
    large_rs = np.array([5.0, 8.0, 12.0, 20.0, 40.0, 80.0, 120.0])
    uu = u_region("III", np.zeros_like(large_rs), large_rs, p)
    ww = w_coord(np.zeros_like(large_rs), large_rs, p)
    XX = np.exp(kap * (uu - ww))

    fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
    ax.loglog(r - r2, X, color="#24495e", lw=1.8)
    ax.set_xlabel(r"$r-r_2$")
    ax.set_ylabel(r"$X_{\mathrm{III}}=\exp[\kappa(u_{III}-w)]$")
    ax.set_title("Forward branch scan: Region III radial coordinate")
    ax.grid(True, which="both", alpha=0.18)
    fig.savefig(p.out_dir / "forward_extension_branch_global_scan.png", dpi=180)
    plt.close(fig)

    lines = [
        "Forward extension branch global scan",
        "",
        "Question:",
        "  Does the local forward C+ side expand along the same radial branch",
        "  as the original Region III exterior r>r2?",
        "",
        "Scanned branch:",
        "  Region III, r>r2",
        "  X_III = exp[kappa(u_III-w)]",
        "  This is positive and locally proportional to r-r2.",
        "",
        f"r2 = {r2:.12f}",
        f"kappa = {kap:.12f}",
        f"monotone increasing on sampled r in (r2, 60]: {monotone}",
        f"minimum sampled dX between adjacent points: {min_dx:.12e}",
        f"X near r2+1e-8: {X[0]:.12e}",
        f"X at r=60: {X[-1]:.12e}",
        "",
        "Selected large-r samples:",
        "  r | X_III | log(X)/r",
    ]
    for rr, xx in zip(large_rs, XX):
        lines.append(f"  {rr: .3f} | {xx:.12e} | {np.log(xx)/rr:.12e}")

    lines.extend(
        [
            "",
            "Interpretation:",
            "  The positive radial branch is monotone in this scan and grows rapidly",
            "  as r increases. Thus there is no finite-r obstruction on the sampled",
            "  Region III branch; the far end appears to be r->+infinity.",
            "",
            "What this supports:",
            "  The forward local extension through C+ opens into a Region-III-type",
            "  exterior branch, at least as a radial branch of the same analytic metric.",
            "",
            "What this does not yet prove:",
            "  It does not by itself provide a full compactified global Penrose block",
            "  with all null boundaries labeled. It only tracks the radial branch.",
        ]
    )
    (p.out_dir / "forward_extension_branch_global_scan.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_forward_regionIII_branch_chart(p: Params) -> None:
    """Calculated conformal chart for the forward-attached Region III branch."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    def coords(t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("III", t, r, p)
        w = w_coord(t, r, p)
        U = np.exp(kap * u)
        V = -np.exp(-kap * w)
        uu = np.arctan(U)
        vv = np.arctan(V)
        return 0.5 * (vv - uu), 0.5 * (vv + uu)

    fig, ax = plt.subplots(figsize=(8.0, 7.0), constrained_layout=True)

    r_values = r2 + np.array([0.025, 0.055, 0.11, 0.22, 0.45, 0.9, 1.8, 3.6, 7.2, 14.0])
    t_values = np.linspace(-8.0, 18.0, 1200)
    for r0 in r_values:
        x, y = coords(t_values, np.full_like(t_values, r0))
        ax.plot(x, y, color="#20252b", lw=1.0, alpha=0.78)

    for t0 in np.linspace(-5.0, 15.0, 11):
        rr = r2 + np.geomspace(0.018, 30.0, 1200)
        x, y = coords(np.full_like(rr, t0), rr)
        ax.plot(x, y, color="#8b9095", lw=0.75, ls=(0, (6, 5)), alpha=0.58)

    # r2 side/horizon: U->0, V<0.  This attaches to the continued generator.
    Vh = -np.geomspace(1.2, 0.018, 400)
    Uh = np.zeros_like(Vh)
    xh = 0.5 * (np.arctan(Vh) - np.arctan(Uh))
    yh = 0.5 * (np.arctan(Vh) + np.arctan(Uh))
    ax.plot(xh, yh, color="#c14d3f", lw=2.8, label=r"continued $r_2$ generator side")

    # r -> +infinity boundary at finite plotted t samples.  This is an
    # asymptotic guide, not an extension surface.
    tt = np.linspace(-8.0, 18.0, 800)
    rr = np.full_like(tt, 80.0)
    xb, yb = coords(tt, rr)
    ax.plot(xb, yb, color="#555555", lw=1.7, alpha=0.8, label=r"large-$r$ asymptotic guide")

    ax.scatter([0.0], [0.0], s=55, color="#20252b", zorder=6)
    ax.text(0.03, -0.04, r"$C^+$ attach point" "\n" r"$U=V=0$", fontsize=9, ha="left", va="top")

    ax.text(
        -1.42,
        0.58,
        "Forward Region-III-type branch:\n"
        "U=exp(kappa u_III)\n"
        "V=-exp(-kappa w)\n"
        "X=-UV>0, r>r2",
        fontsize=8.8,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.text(
        -1.42,
        -0.62,
        "solid: constant r\n"
        "dashed: constant t from Region III formulas\n"
        "gray: large-r guide, not an extension",
        fontsize=8.6,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )

    ax.set_title("Calculated forward Region-III-type branch chart")
    ax.set_xlabel(r"$(\arctan V-\arctan U)/2$")
    ax.set_ylabel(r"$(\arctan V+\arctan U)/2$")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.48, 0.25)
    ax.set_ylim(-0.72, 0.72)
    ax.grid(True, alpha=0.16)
    ax.legend(loc="upper right", fontsize=8)
    fig.savefig(p.out_dir / "forward_regionIII_branch_chart.png", dpi=180)
    plt.close(fig)

    notes = [
        "Forward Region-III-type branch chart",
        "",
        "Coordinates:",
        "  U = exp(kappa u_III)",
        "  V = -exp(-kappa w)",
        "  compactified by arctan U, arctan V",
        "",
        "Branch:",
        "  X = -U V = exp(kappa(u_III-w)) > 0",
        "  X is monotone with r on the scanned r>r2 branch.",
        "  Therefore this chart represents the r>r2 exterior-type branch",
        "  attached locally beyond C+.",
        "",
        "Curves:",
        "  solid black: constant r curves from exact Region III formulas",
        "  gray dashed: constant t curves from exact Region III formulas",
        "  red: U=0 side, the continued r2 generator side",
        "  gray boundary guide: large r, approximating r->+infinity",
        "",
        "Limitations:",
        "  The t labels on this branch are inherited from the Region III analytic",
        "  formulas; they are chart labels for the isometric exterior-type branch,",
        "  not the original bubble-rider time continued through C+.",
        "  The large-r guide is scri/asymptotic behavior, not an extendible surface.",
        "  This is a calculated exterior branch chart, not yet the entire maximal diagram.",
    ]
    (p.out_dir / "forward_regionIII_branch_chart_notes.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")


def forward_regionIII_boundary_classification(p: Params) -> None:
    """Classify boundaries of the forward-attached Region III branch."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    def branch_coords(t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        u = u_region("III", t, r, p)
        w = w_coord(t, r, p)
        U = np.exp(kap * u)
        V = -np.exp(-kap * w)
        X = -U * V
        return U, V, X

    sample_specs = [
        ("near C+ along r2 side", 20.0, r2 + 1.0e-8),
        ("finite r, t->+large", 60.0, r2 + 1.0),
        ("finite r, t->-large", -60.0, r2 + 1.0),
        ("large r, t=0", 0.0, 80.0),
    ]
    samples = []
    for name, tt, rr in sample_specs:
        U, V, X = branch_coords(np.array([tt]), np.array([rr]))
        samples.append((name, tt, rr, float(U[0]), float(V[0]), float(X[0])))

    large_r = np.array([10.0, 20.0, 40.0, 80.0, 120.0])
    U0, V0, X0 = branch_coords(np.zeros_like(large_r), large_r)
    F0 = C_factor(large_r, p) / (kap * kap * X0)

    lines = [
        "Forward Region-III branch boundary classification",
        "",
        "Branch coordinates:",
        "  U = exp(kappa u_III)",
        "  V = -exp(-kappa w)",
        "  X = -U V = exp(kappa(u_III-w)) > 0",
        "  ds^2 = F(X) dU dV",
        "",
        "Coordinate-limit samples:",
        "  name | t | r | U | V | X",
    ]
    for name, tt, rr, U, V, X in samples:
        lines.append(f"  {name:24s} | {tt: .3e} | {rr: .8e} | {U:.8e} | {V:.8e} | {X:.8e}")

    lines.extend(
        [
            "",
            "Large-r conformal factor samples at t=0:",
            "  r | U | V | X | F=C/(kappa^2 X)",
        ]
    )
    for rr, U, V, X, F in zip(large_r, U0, V0, X0, F0):
        lines.append(f"  {rr: .3f} | {U:.8e} | {V:.8e} | {X:.8e} | {F:.8e}")

    lines.extend(
        [
            "",
            "Boundary pieces in this branch:",
            "",
            "1. U=0, V<0:",
            "   This is the continued r2 generator side. It includes the attach",
            "   endpoint C+ at U=V=0. Along U=0, V is affine.",
            "",
            "2. r -> +infinity:",
            "   This is the exterior asymptotic boundary of the Region-III-type branch.",
            "   From the original null-coordinate identity, transverse null rays have",
            "     d lambda proportional to +/- dr,",
            "   so r->+infinity is infinite affine distance. It is scri-like, not",
            "   an extension surface.",
            "",
            "3. finite r, t -> +infinity:",
            "   U -> +infinity and V -> 0-. This is a conformal corner/edge of the",
            "   branch, not the C+ attach point. It must be checked separately if a",
            "   null generator reaches it at finite affine parameter.",
            "",
            "4. finite r, t -> -infinity:",
            "   U -> 0+ and V -> -infinity. This is the opposite end of the r2-side",
            "   generator family and is infinite-affine for the r2 generator direction.",
            "",
            "Current conclusion:",
            "   The attached branch has a genuine asymptotic r->+infinity boundary",
            "   and may have additional conformal endpoints at finite r, t->+/-infinity.",
            "   The next possible extension check is the finite-r, t->+infinity corner",
            "   U->infinity,V->0-, not r->+infinity.",
        ]
    )
    (p.out_dir / "forward_regionIII_boundary_classification.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def forward_regionIII_future_corner_check(p: Params) -> None:
    """Check whether finite-r, t->+infinity corner is a null finite-affine endpoint."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)

    # Pick representative finite radii and show X is fixed while U,V run to
    # infinity/zero as t changes.
    radii = r2 + np.array([0.25, 1.0, 3.0])
    rows = []
    for r0 in radii:
        for t0 in [10.0, 20.0, 40.0]:
            u = u_region("III", np.array([t0]), np.array([r0]), p)
            w = w_coord(np.array([t0]), np.array([r0]), p)
            U = float(np.exp(kap * u)[0])
            V = float(-np.exp(-kap * w)[0])
            X = -U * V
            rows.append((r0, t0, U, V, X))

    # Null families:
    #   U=const: varying V changes X=-UV. V->0 at finite U gives X->0 -> r2,
    #            not finite r>r2.
    #   V=const: U->infinity gives X->infinity -> r->infinity.
    lines = [
        "Forward Region-III finite-r future-corner check",
        "",
        "Corner under question:",
        "  finite r>r2, t -> +infinity in the attached Region-III branch.",
        "  Coordinates: U=exp(kappa u_III)->+infinity, V=-exp(-kappa w)->0-.",
        "  Product X=-UV remains fixed because X=X(r).",
        "",
        "Representative finite-r curves:",
        "  r | t | U | V | X=-UV",
    ]
    for r0, t0, U, V, X in rows:
        lines.append(f"  {r0:.8f} | {t0: .1f} | {U:.8e} | {V:.8e} | {X:.8e}")

    lines.extend(
        [
            "",
            "Null-family check in ds^2=F(X)dU dV:",
            "",
            "1. U=constant null rays:",
            "   Taking V->0- at finite U gives X=-UV->0, hence r->r2.",
            "   These approach the C+ attach/horizon side, not finite r>r2.",
            "",
            "2. V=constant<0 null rays:",
            "   Taking U->+infinity gives X=-UV->+infinity.",
            "   The branch scan shows X->+infinity corresponds to r->+infinity.",
            "   These approach the asymptotic boundary, not finite r.",
            "",
            "Therefore:",
            "  The finite-r, t->+infinity corner is not reached by a single null",
            "  geodesic family as an endpoint. It is the limiting end of spacelike",
            "  constant-r curves in this Region-III-type branch.",
            "",
            "Affine implication:",
            "  Since no null generator has finite r>r2 and U->infinity,V->0- as its",
            "  endpoint, this corner is not currently an extension candidate based",
            "  on null geodesic incompleteness.",
            "",
            "Next boundary to check:",
            "  The only null endpoints of this attached branch are the U=0 generator",
            "  side already continued, and r->+infinity, which has infinite affine",
            "  length. Thus this forward Region-III-type branch may be complete",
            "  in the forward direction relevant to the C+ extension.",
        ]
    )
    (p.out_dir / "forward_regionIII_future_corner_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_forward_extension_composite(p: Params) -> None:
    """Composite figure summarizing the calculated forward extension."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    _, r2 = horizons(p)
    kap = kappa(p)
    eps = 1.0e-5 * (2 * r2)

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.4), constrained_layout=True)

    # Panel 1: original patch around region II/r2.
    ax = axes[0]
    t = np.linspace(-p.t_max, p.t_max, 1100)
    for r0 in np.r_[np.linspace(r2 - 1.0, r2 - 0.2, 4), [0.0]]:
        x, y = compact("II", t, np.full_like(t, r0), p)
        ax.plot(x, y, color="#20252b", lw=0.8, alpha=0.42)
    x, y = compact("II", t, np.full_like(t, r2 - eps), p)
    ax.plot(x, y, color="#c14d3f", lw=2.6, label=r"$r_2$ generator")
    xe, ye = compact("II", np.array([p.t_max]), np.array([r2 - eps]), p)
    ax.scatter(xe, ye, s=55, color="#20252b", zorder=5)
    ax.annotate(
        r"$C^+$ attach point",
        xy=(float(xe[0]), float(ye[0])),
        xytext=(float(xe[0]) - 0.45, float(ye[0]) + 0.2),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=9,
        ha="center",
    )
    ax.set_title("Original patch")
    ax.set_xlabel(r"$(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"$(\mathcal{W}+\mathcal{U})/2$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.legend(loc="lower right", fontsize=8)

    # Panel 2: local C+ extension chart.
    ax = axes[1]

    def penrose(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        uu = np.arctan(U)
        vv = np.arctan(V)
        return 0.5 * (vv - uu), 0.5 * (vv + uu)

    ax.fill_between([0, 0.85], 0, 0.85, color="#eaf3f6", alpha=0.75)
    ax.fill_between([0, 0.85], -0.85, 0, color="#f6efe6", alpha=0.75)
    V = np.linspace(0.85, -0.85, 700)
    U = np.zeros_like(V)
    ax.plot(*penrose(U, V), color="#c14d3f", lw=2.8)
    ax.scatter([0], [0], s=55, color="#20252b", zorder=5)
    Ug = np.linspace(0.02, 0.85, 400)
    ax.plot(*penrose(Ug, np.zeros_like(Ug)), color="#b7791f", lw=1.0, alpha=0.35, ls=(0, (4, 4)))
    for X0 in [-0.035, 0.035]:
        Uv = np.geomspace(0.05, 0.85, 350)
        Vv = -X0 / Uv
        mask = np.abs(Vv) < 0.85
        ax.plot(*penrose(Uv[mask], Vv[mask]), color="#3f4750" if X0 > 0 else "#6f5b45", lw=1.0, alpha=0.72)
    ax.text(
        -0.66,
        0.48,
        "Local chart:\n"
        "U=exp(kappa u)\n"
        "V=exp(-kappa w)\n"
        "r2 generator: U=0\n"
        "continue V through 0",
        fontsize=8.5,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.set_title("Local C+ extension")
    ax.set_xlabel(r"$(\arctan V-\arctan U)/2$")
    ax.set_ylabel(r"$(\arctan V+\arctan U)/2$")
    ax.set_xlim(-0.7, 0.22)
    ax.set_ylim(-0.58, 0.58)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)

    # Panel 3: attached Region III branch.
    ax = axes[2]

    def branch_coords(t0: np.ndarray, r0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("III", t0, r0, p)
        w = w_coord(t0, r0, p)
        U = np.exp(kap * u)
        V = -np.exp(-kap * w)
        return penrose(U, V)

    tv = np.linspace(-7.0, 16.0, 900)
    for r0 in r2 + np.array([0.04, 0.09, 0.2, 0.45, 1.0, 2.3, 5.0, 11.0]):
        ax.plot(*branch_coords(tv, np.full_like(tv, r0)), color="#20252b", lw=0.9, alpha=0.75)
    for t0 in np.linspace(-4.0, 13.0, 8):
        rr = r2 + np.geomspace(0.03, 25.0, 900)
        ax.plot(*branch_coords(np.full_like(rr, t0), rr), color="#8b9095", lw=0.7, ls=(0, (6, 5)), alpha=0.55)
    Vh = -np.geomspace(1.0, 0.018, 350)
    Uh = np.zeros_like(Vh)
    ax.plot(*penrose(Uh, Vh), color="#c14d3f", lw=2.6, label="continued generator side")
    rr = np.full_like(tv, 70.0)
    ax.plot(*branch_coords(tv, rr), color="#555555", lw=1.5, alpha=0.75, label="large-r guide")
    ax.text(
        -1.38,
        0.50,
        "Attached branch:\n"
        "U=exp(kappa u_III)\n"
        "V=-exp(-kappa w)\n"
        "X=-UV>0 => r>r2\n"
        "r->infinity is scri-like",
        fontsize=8.4,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.set_title("Calculated attached exterior branch")
    ax.set_xlabel(r"$(\arctan V-\arctan U)/2$")
    ax.set_ylabel(r"$(\arctan V+\arctan U)/2$")
    ax.set_xlim(-1.45, 0.22)
    ax.set_ylim(-0.65, 0.65)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.legend(loc="lower right", fontsize=8)

    fig.savefig(p.out_dir / "forward_extension_composite.png", dpi=180)
    plt.close(fig)

    notes = [
        "Forward extension composite",
        "",
        "Panels:",
        "  1. Original patch with the r2 generator and C+ attach point.",
        "  2. Local C+ chart showing the analytic continuation through U=V=0.",
        "  3. Calculated attached Region-III-type exterior branch.",
        "",
        "Calculated facts shown:",
        "  The attach is a single point/corner C+, not a whole edge.",
        "  The continued generator is U=0, with V affine.",
        "  The attached branch has X=-UV>0, corresponding to r>r2 and C<0.",
        "  The r->+infinity boundary of that branch is infinite-affine/scri-like.",
        "",
        "Non-claims:",
        "  This is not a maximal Penrose diagram.",
        "  The local coordinate guide V=0 away from U=0 is not a global Cauchy horizon.",
        "  No edge-to-edge diamond gluing is asserted.",
    ]
    (p.out_dir / "forward_extension_composite_notes.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")


def rear_cminus_extension_calculation(p: Params) -> None:
    """Time-reversed local calculation for the rear r1, past C- endpoint."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, _ = horizons(p)
    kap = kappa(p)

    # For r1, vbar'(r1)=+kappa.  The finite affine end is t->-infinity.
    # Use endpoint coordinates that vanish at that end:
    #   U = exp(-kappa u), V = exp(+kappa w)
    # Along r1, U=0 and V~exp(kappa t), finite at t->-infinity.
    rows = []
    for side, region, sign, orient in [
        ("outside I", "I", -1.0, -1.0),
        ("inside II", "II", 1.0, 1.0),
    ]:
        for eps in [1.0e-2, 1.0e-3, 1.0e-4, 1.0e-5, 1.0e-6]:
            r = np.array([r1 + sign * eps])
            t = np.array([0.0])
            u = u_region(region, t, r, p)
            w = w_coord(t, r, p)
            raw_z = float(np.exp(-kap * (u - w))[0])
            X = orient * raw_z
            dr = float(r[0] - r1)
            C = float(C_factor(r, p)[0])
            rows.append((side, eps, dr, raw_z, X, X / dr, C / X))

    ratios = [row[5] for row in rows if row[1] <= 1.0e-4]
    a1 = float(np.mean(ratios))

    lines = [
        "Rear r1 / past C- extension calculation",
        "",
        "Generator:",
        f"  r1 = {r1:.12f}",
        "  vbar(r1) = -1",
        f"  vbar'(r1) = +{kap:.12f} = +kappa",
        "  k=partial_t is null on r=r1 and satisfies",
        "    k^a nabla_a k^b = +kappa k^b.",
        "",
        "Affine parameter:",
        "  d lambda/dt proportional to exp(+kappa t).",
        "  Therefore t->-infinity is finite affine and t->+infinity is infinite affine.",
        "",
        "Endpoint coordinates for the finite past end:",
        "  U = exp(-kappa u)",
        "  V = exp(+kappa w)",
        "  r1 generator: U=0",
        "  V is proportional to affine parameter along the generator.",
        "  C- endpoint: U=0,V=0",
        "",
        "Branch variable:",
        "  raw Z = exp[-kappa(u-w)]",
        "  oriented X is chosen so X ~= a1(r-r1).",
        "",
        "side | eps | dr | raw Z | oriented X | X/dr | C/X",
    ]
    for side, eps, dr, raw_z, X, ratio, c_over_x in rows:
        lines.append(f"  {side:9s} | {eps:.0e} | {dr: .8e} | {raw_z:.8e} | {X: .8e} | {ratio: .8e} | {c_over_x: .8e}")

    lines.extend(
        [
            "",
            f"Estimated a1 = {a1:.12e}, nonzero.",
            "",
            "Local classification:",
            "  X<0 corresponds to r<r1, C<0: rear exterior/trapped-side character.",
            "  X>0 corresponds to r>r1, C>0: bubble-side character.",
            "",
            "Conclusion:",
            "  The rear past C- endpoint is the time-reversed analogue of the",
            "  front C+ endpoint. It admits a local analytic continuation of the",
            "  r1 generator through U=V=0. The attached side should be checked",
            "  next, but locally the branch signs show which side has exterior",
            "  versus bubble causal character.",
        ]
    )
    (p.out_dir / "rear_cminus_extension_calculation.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_rear_regionI_branch_chart(p: Params) -> None:
    """Calculated conformal chart for the rear C- attached Region I branch."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, _ = horizons(p)
    kap = kappa(p)

    def coords(t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("I", t, r, p)
        w = w_coord(t, r, p)
        U = np.exp(-kap * u)
        V = -np.exp(kap * w)
        uu = np.arctan(U)
        vv = np.arctan(V)
        return 0.5 * (vv - uu), 0.5 * (vv + uu)

    # Scan X=-UV on r<r1.
    r = np.r_[r1 - np.geomspace(1.0e-8, 1.0e-2, 500), np.linspace(r1 - 1.0e-2, -60.0, 3000)[1:]]
    t = np.zeros_like(r)
    u = u_region("I", t, r, p)
    w = w_coord(t, r, p)
    X = np.exp(-kap * (u - w))
    # As r decreases from r1 to -infinity, X increases as a positive radial
    # magnitude.  Check monotonicity in |r-r1| ordering.
    monotone = bool(np.all(np.diff(X) > 0))

    fig, ax = plt.subplots(figsize=(8.0, 7.0), constrained_layout=True)
    r_values = r1 - np.array([0.025, 0.055, 0.11, 0.22, 0.45, 0.9, 1.8, 3.6, 7.2, 14.0])
    t_values = np.linspace(-18.0, 8.0, 1200)
    for r0 in r_values:
        x, y = coords(t_values, np.full_like(t_values, r0))
        ax.plot(x, y, color="#20252b", lw=1.0, alpha=0.78)

    for t0 in np.linspace(-15.0, 5.0, 11):
        rr = r1 - np.geomspace(0.018, 30.0, 1200)
        x, y = coords(np.full_like(rr, t0), rr)
        ax.plot(x, y, color="#8b9095", lw=0.75, ls=(0, (6, 5)), alpha=0.58)

    # r1 generator side: U=0, V<0 in this chosen chart.
    Vh = -np.geomspace(1.2, 0.018, 400)
    Uh = np.zeros_like(Vh)
    xh = 0.5 * (np.arctan(Vh) - np.arctan(Uh))
    yh = 0.5 * (np.arctan(Vh) + np.arctan(Uh))
    ax.plot(xh, yh, color="#c14d3f", lw=2.8, label=r"continued $r_1$ generator side")

    tt = np.linspace(-18.0, 8.0, 800)
    rr = np.full_like(tt, -80.0)
    xb, yb = coords(tt, rr)
    ax.plot(xb, yb, color="#555555", lw=1.7, alpha=0.8, label=r"large negative-$r$ guide")

    ax.scatter([0.0], [0.0], s=55, color="#20252b", zorder=6)
    ax.text(0.03, -0.04, r"$C^-$ attach point" "\n" r"$U=V=0$", fontsize=9, ha="left", va="top")

    ax.text(
        -1.42,
        0.58,
        "Rear Region-I-type branch:\n"
        "U=exp(-kappa u_I)\n"
        "V=-exp(kappa w)\n"
        "X=-UV>0 as |r-r1|\n"
        "r<r1 exterior",
        fontsize=8.8,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.text(
        -1.42,
        -0.62,
        f"radial scan monotone: {monotone}\n"
        "solid: constant r\n"
        "dashed: constant t from Region I formulas\n"
        "gray: large negative-r guide",
        fontsize=8.6,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )

    ax.set_title("Calculated rear Region-I-type branch chart")
    ax.set_xlabel(r"$(\arctan V-\arctan U)/2$")
    ax.set_ylabel(r"$(\arctan V+\arctan U)/2$")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.48, 0.25)
    ax.set_ylim(-0.72, 0.72)
    ax.grid(True, alpha=0.16)
    ax.legend(loc="upper right", fontsize=8)
    fig.savefig(p.out_dir / "rear_regionI_branch_chart.png", dpi=180)
    plt.close(fig)

    lines = [
        "Rear Region-I-type branch chart",
        "",
        "Coordinates:",
        "  U = exp(-kappa u_I)",
        "  V = -exp(+kappa w)",
        "  compactified by arctan U, arctan V",
        "",
        "Branch:",
        "  This chart represents the r<r1 exterior-type branch attached locally",
        "  beyond the rear past C- endpoint.",
        f"  radial scan monotone in sampled branch: {monotone}",
        f"  X near r1-1e-8: {X[0]:.12e}",
        f"  X at r=-60: {X[-1]:.12e}",
        "",
        "Curves:",
        "  solid black: constant r curves from exact Region I formulas",
        "  gray dashed: constant t curves from exact Region I formulas",
        "  red: U=0 side, continued r1 generator side",
        "  gray boundary guide: large negative r, approximating r->-infinity",
        "",
        "Limitations:",
        "  This is the rear analogue of the forward Region-III branch chart.",
        "  It is not yet a full maximal diagram.",
    ]
    (p.out_dir / "rear_regionI_branch_chart_notes.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def rear_regionI_boundary_classification(p: Params) -> None:
    """Classify boundaries of the rear-attached Region I branch."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, _ = horizons(p)
    kap = kappa(p)

    def branch_coords(t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        u = u_region("I", t, r, p)
        w = w_coord(t, r, p)
        U = np.exp(-kap * u)
        V = -np.exp(kap * w)
        X = -U * V
        return U, V, X

    sample_specs = [
        ("near C- along r1 side", -20.0, r1 - 1.0e-8),
        ("finite r, t->-large", -60.0, r1 - 1.0),
        ("finite r, t->+large", 60.0, r1 - 1.0),
        ("large negative r, t=0", 0.0, -80.0),
    ]
    samples = []
    for name, tt, rr in sample_specs:
        U, V, X = branch_coords(np.array([tt]), np.array([rr]))
        samples.append((name, tt, rr, float(U[0]), float(V[0]), float(X[0])))

    large_r = np.array([-10.0, -20.0, -40.0, -80.0, -120.0])
    U0, V0, X0 = branch_coords(np.zeros_like(large_r), large_r)
    F0 = C_factor(large_r, p) / (kap * kap * X0)

    lines = [
        "Rear Region-I branch boundary classification",
        "",
        "Branch coordinates:",
        "  U = exp(-kappa u_I)",
        "  V = -exp(+kappa w)",
        "  X = -U V > 0 on the exterior magnitude branch",
        "  ds^2 = F(X) dU dV",
        "",
        "Coordinate-limit samples:",
        "  name | t | r | U | V | X",
    ]
    for name, tt, rr, U, V, X in samples:
        lines.append(f"  {name:25s} | {tt: .3e} | {rr: .8e} | {U:.8e} | {V:.8e} | {X:.8e}")

    lines.extend(
        [
            "",
            "Large-negative-r conformal factor samples at t=0:",
            "  r | U | V | X | F=C/(kappa^2 X)",
        ]
    )
    for rr, U, V, X, F in zip(large_r, U0, V0, X0, F0):
        lines.append(f"  {rr: .3f} | {U:.8e} | {V:.8e} | {X:.8e} | {F:.8e}")

    lines.extend(
        [
            "",
            "Boundary pieces in this branch:",
            "",
            "1. U=0, V<0:",
            "   Continued r1 generator side. It includes the C- attach point at",
            "   U=V=0. Along U=0, V is affine.",
            "",
            "2. r -> -infinity:",
            "   Exterior asymptotic boundary of the Region-I-type branch.",
            "   Transverse null rays have d lambda proportional to +/- dr,",
            "   so r->-infinity is infinite affine distance. It is scri-like.",
            "",
            "3. finite r, t -> -infinity:",
            "   U -> +infinity and V -> 0-. X remains fixed. This is the rear",
            "   analogue of the forward finite-r corner. It is not reached by",
            "   a single null family: U=const with V->0 gives X->0/r->r1, while",
            "   V=const with U->infinity gives X->infinity/r->-infinity.",
            "",
            "4. finite r, t -> +infinity:",
            "   U -> 0+ and V -> -infinity. This is the opposite end of the r1-side",
            "   generator family and is infinite-affine for the r1 generator direction.",
            "",
            "Current conclusion:",
            "   The rear attached Region-I branch has no new finite-affine null",
            "   endpoint in this boundary check. Its radial far end is scri-like.",
        ]
    )
    (p.out_dir / "rear_regionI_boundary_classification.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_two_sided_extension_composite(p: Params) -> None:
    """Composite summary of the C- and C+ local exterior attachments."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)

    fig, axes = plt.subplots(1, 3, figsize=(15.5, 5.4), constrained_layout=True)

    def penrose(U: np.ndarray, V: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        uu = np.arctan(U)
        vv = np.arctan(V)
        return 0.5 * (vv - uu), 0.5 * (vv + uu)

    # Rear attached Region I branch.
    ax = axes[0]

    def rear_coords(t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("I", t, r, p)
        w = w_coord(t, r, p)
        U = np.exp(-kap * u)
        V = -np.exp(kap * w)
        return penrose(U, V)

    tv = np.linspace(-16.0, 7.0, 800)
    for r0 in r1 - np.array([0.05, 0.11, 0.25, 0.55, 1.2, 2.7, 6.0, 13.0]):
        ax.plot(*rear_coords(tv, np.full_like(tv, r0)), color="#20252b", lw=0.85, alpha=0.72)
    Vh = -np.geomspace(1.0, 0.018, 330)
    ax.plot(*penrose(np.zeros_like(Vh), Vh), color="#c14d3f", lw=2.6)
    ax.scatter([0.0], [0.0], s=55, color="#20252b", zorder=6)
    ax.annotate(
        r"local $U=V=0$",
        xy=(0.0, 0.0),
        xytext=(-0.55, -0.22),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=8.5,
        ha="center",
    )
    ax.text(
        -1.38,
        0.50,
        "Separate local chart for C-\nRegion-I-type branch\nr<r1, C<0\nr->-infinity scri-like",
        fontsize=8.5,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.set_title("C- local extension chart")
    ax.set_xlim(-1.45, 0.22)
    ax.set_ylim(-0.65, 0.65)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.set_xlabel("compact null X")
    ax.set_ylabel("compact null T")

    # Original patch.
    ax = axes[1]
    t = np.linspace(-p.t_max, p.t_max, 1300)
    eps = 1.0e-5 * (r2 - r1)
    for r0 in np.r_[np.linspace(r1 + 0.25, -0.15, 3), [0.0], np.linspace(0.15, r2 - 0.25, 3)]:
        ax.plot(*compact("II", t, np.full_like(t, r0), p), color="#20252b", lw=0.8, alpha=0.5)
    ax.plot(*compact("II", t, np.full_like(t, r1 + eps), p), color="#c14d3f", lw=2.2, label=r"$r_1$ generator")
    ax.plot(*compact("II", t, np.full_like(t, r2 - eps), p), color="#c14d3f", lw=2.2, ls=(0, (6, 3)), label=r"$r_2$ generator")
    x1, y1 = compact("II", np.array([-p.t_max]), np.array([r1 + eps]), p)
    x2, y2 = compact("II", np.array([p.t_max]), np.array([r2 - eps]), p)
    ax.scatter([x1[0], x2[0]], [y1[0], y2[0]], s=50, color="#20252b", zorder=5)
    ax.annotate(
        r"$C^-: r_1,\ t\to-\infty$" "\n" "maps to left chart origin",
        xy=(float(x1[0]), float(y1[0])),
        xytext=(float(x1[0]) + 0.18, float(y1[0]) - 0.33),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=8.5,
        ha="left",
    )
    ax.annotate(
        r"$C^+: r_2,\ t\to+\infty$" "\n" "maps to right chart origin",
        xy=(float(x2[0]), float(y2[0])),
        xytext=(float(x2[0]) - 0.7, float(y2[0]) + 0.18),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=8.5,
        ha="center",
    )
    ax.text(
        -0.62,
        0.03,
        "original\nbubble patch",
        fontsize=9,
        ha="center",
        va="center",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.86},
    )
    ax.set_title("Original patch, separate coordinates")
    ax.set_xlabel(r"$(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"$(\mathcal{W}+\mathcal{U})/2$")
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.legend(loc="lower right", fontsize=8)

    # Forward attached Region III branch.
    ax = axes[2]

    def front_coords(t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        u = u_region("III", t, r, p)
        w = w_coord(t, r, p)
        U = np.exp(kap * u)
        V = -np.exp(-kap * w)
        x, y = penrose(U, V)
        return -x, y

    tv = np.linspace(-7.0, 16.0, 800)
    for r0 in r2 + np.array([0.05, 0.11, 0.25, 0.55, 1.2, 2.7, 6.0, 13.0]):
        ax.plot(*front_coords(tv, np.full_like(tv, r0)), color="#20252b", lw=0.85, alpha=0.72)
    Vh = -np.geomspace(1.0, 0.018, 330)
    xh, yh = penrose(np.zeros_like(Vh), Vh)
    ax.plot(-xh, yh, color="#c14d3f", lw=2.6)
    ax.scatter([0.0], [0.0], s=55, color="#20252b", zorder=6)
    ax.annotate(
        r"local $U=V=0$",
        xy=(0.0, 0.0),
        xytext=(0.55, -0.22),
        arrowprops={"arrowstyle": "->", "color": "#20252b", "lw": 1.0},
        fontsize=8.5,
        ha="center",
    )
    ax.text(
        0.10,
        0.50,
        "Separate local chart for C+\nRegion-III-type branch\nr>r2, C<0\nr->+infinity scri-like",
        fontsize=8.5,
        ha="left",
        va="top",
        bbox={"facecolor": "white", "edgecolor": "#d8d8d8", "alpha": 0.92},
    )
    ax.set_title("C+ local extension chart")
    ax.set_xlim(-0.22, 1.45)
    ax.set_ylim(-0.65, 0.65)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(True, alpha=0.16)
    ax.set_xlabel("compact null X")
    ax.set_ylabel("compact null T")

    fig.savefig(p.out_dir / "two_sided_extension_composite.png", dpi=180)
    plt.close(fig)

    notes = [
        "Two-sided local extension summary",
        "",
        "Calculated attachments:",
        "",
        "1. Past/rear C- endpoint:",
        "   Original r1 generator reaches r1,t->-infinity at finite affine parameter.",
        "   Local extension continues it through U=V=0.",
        "   Attached branch has Region-I-type character: r<r1, C<0.",
        "   Its r->-infinity boundary is scri-like/infinite affine.",
        "",
        "2. Future/front C+ endpoint:",
        "   Original r2 generator reaches r2,t->+infinity at finite affine parameter.",
        "   Local extension continues it through U=V=0.",
        "   Attached branch has Region-III-type character: r>r2, C<0.",
        "   Its r->+infinity boundary is scri-like/infinite affine.",
        "",
        "What is not claimed:",
        "   The three panels are not in one shared coordinate system.",
        "   Side panels are local charts whose origins correspond to C-/C+.",
        "   The C+ side chart is horizontally flipped in this composite so its",
        "   local origin faces the original patch; this does not change the chart data.",
        "   No edge-to-edge gluing.",
        "   No full new three-region diamond copy.",
        "   No maximal extension proof yet.",
        "",
        "Current mathematical status:",
        "   Both finite-affine null generator endpoints in the original patch have",
        "   local analytic continuations into exterior-type branches. Boundary checks",
        "   on those branches found no new finite-affine null endpoint.",
    ]
    (p.out_dir / "two_sided_extension_summary.txt").write_text("\n".join(notes) + "\n", encoding="utf-8")


def local_endpoint_geodesic_completeness_check(p: Params) -> None:
    """Check local geodesic ODE regularity at both extended endpoints."""
    p.out_dir.mkdir(parents=True, exist_ok=True)
    r1, r2 = horizons(p)
    kap = kappa(p)

    def fit_front() -> tuple[float, float, float]:
        Xs, Fs = [], []
        for region, sign, orient in [("II", -1.0, -1.0), ("III", 1.0, 1.0)]:
            eps = np.geomspace(1.0e-7, 2.0e-3, 80)
            dr = sign * eps
            r = r2 + dr
            t = np.zeros_like(r)
            u = u_region(region, t, r, p)
            w = w_coord(t, r, p)
            X = orient * np.exp(kap * (u - w))
            F = C_factor(r, p) / (kap * kap * X)
            Xs.append(X)
            Fs.append(F)
        X = np.concatenate(Xs)
        F = np.concatenate(Fs)
        A = np.column_stack([np.ones_like(X), X, X * X])
        return tuple(float(v) for v in np.linalg.lstsq(A, F, rcond=None)[0])

    def fit_rear() -> tuple[float, float, float]:
        Xs, Fs = [], []
        for region, sign, orient in [("I", -1.0, -1.0), ("II", 1.0, 1.0)]:
            eps = np.geomspace(1.0e-7, 2.0e-3, 80)
            dr = sign * eps
            r = r1 + dr
            t = np.zeros_like(r)
            u = u_region(region, t, r, p)
            w = w_coord(t, r, p)
            X = orient * np.exp(-kap * (u - w))
            # For the rear chart U=exp(-ku), V=exp(+kw) before optional
            # display sign flips.  The metric coefficient differs by a sign
            # convention; regularity is the finite nonzero branch.
            F = C_factor(r, p) / (kap * kap * X)
            Xs.append(X)
            Fs.append(F)
        X = np.concatenate(Xs)
        F = np.concatenate(Fs)
        A = np.column_stack([np.ones_like(X), X, X * X])
        return tuple(float(v) for v in np.linalg.lstsq(A, F, rcond=None)[0])

    f_front = fit_front()
    f_rear = fit_rear()

    lines = [
        "Local endpoint geodesic regularity/completeness check",
        "",
        "Purpose:",
        "  Verify that the endpoint extension is a regular Lorentzian metric",
        "  neighborhood once reached. This is not a claim that generic geodesics",
        "  from the original patch reach the endpoint.",
        "",
        "Local form at each endpoint:",
        "  ds^2 = F(X) dU dV",
        "  X is the oriented branch variable with X=0 at the endpoint.",
        "",
        "Fitted endpoint conformal factors:",
        "  F(X)=F0+F1 X+F2 X^2+...",
        f"  C+ front endpoint: F0={f_front[0]: .12e}, F1={f_front[1]: .12e}, F2={f_front[2]: .12e}",
        f"  C- rear endpoint:  F0={f_rear[0]: .12e}, F1={f_rear[1]: .12e}, F2={f_rear[2]: .12e}",
        "",
        "Since F0 is finite and nonzero and F1 is finite at both endpoints,",
        "the metric is nondegenerate and the Christoffels are finite locally.",
        "",
        "Geodesic equations for ds^2=F(U,V)dU dV:",
        "  U'' + (partial_U ln|F|) (U')^2 = 0",
        "  V'' + (partial_V ln|F|) (V')^2 = 0",
        "",
        "Regularity:",
        "  F=F(X), with X proportional to UV up to endpoint orientation.",
        "  partial_U ln|F| = (F'/F) partial_U X",
        "  partial_V ln|F| = (F'/F) partial_V X",
        "  F'/F is finite at X=0.",
        "  partial_U X and partial_V X are smooth functions of U,V.",
        "  Therefore the geodesic ODE has smooth finite coefficients near U=V=0.",
        "",
        "Consequence:",
        "  Any geodesic already represented in this local chart and reaching",
        "  U=V=0 with finite tangent has a unique local continuation by standard",
        "  ODE existence/uniqueness.",
        "",
        "  This does not identify additional geodesics from the original patch.",
        "  The only original-patch geodesics explicitly shown to hit these",
        "  endpoints at finite affine parameter are:",
        "    C+: the future r2 null generator",
        "    C-: the past r1 null generator",
        "",
        "  Accelerated timelike curves can be arranged to reach C+ in finite",
        "  proper time, but those are not geodesics and are not evidence of",
        "  geodesic incompleteness.",
        "",
        "Limit of this result:",
        "  This is local geodesic regularity at C+ and C-. It does not prove",
        "  global geodesic completeness or maximality of the whole spacetime.",
    ]
    (p.out_dir / "local_endpoint_geodesic_completeness_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    p = Params()
    r1, r2 = horizons(p)
    kap = kappa(p)
    plot_three_region_patch(p)
    plot_crossing_observer_on_patch(p)
    plot_formal_block_extension(p)
    plot_kruskal_horizon_charts(p)
    plot_atlas_extension_graph(p)
    write_extension_notes(p)
    classify_patch_boundaries(p)
    endpoint_in_kruskal_charts(p)
    affine_boundary_analysis(p)
    timelike_crossing_example(p)
    front_endpoint_timelike_example(p)
    white_horizon_extension_analysis(p)
    plot_minimal_front_extension(p)
    plot_accurate_local_front_extension(p)
    front_generator_affine_calculation(p)
    front_endpoint_branch_series(p)
    plot_forward_extension_atlas(p)
    local_front_geodesic_regularization(p)
    forward_extension_region_classification(p)
    forward_extension_branch_global_scan(p)
    plot_forward_regionIII_branch_chart(p)
    forward_regionIII_boundary_classification(p)
    forward_regionIII_future_corner_check(p)
    plot_forward_extension_composite(p)
    rear_cminus_extension_calculation(p)
    plot_rear_regionI_branch_chart(p)
    rear_regionI_boundary_classification(p)
    plot_two_sided_extension_composite(p)
    local_endpoint_geodesic_completeness_check(p)
    summary = (
        "Sech-profile 1+1 eternal warp-drive metric\n"
        f"alpha = {p.alpha}, a = {p.a}\n"
        f"r1 = {r1:.12f}, r2 = {r2:.12f}\n"
        f"kappa = {kap:.12f}\n"
        "outputs:\n"
        "  sech_three_region_patch.png\n"
        "  timelike_crossing_on_patch.png\n"
        "  formal_block_extension_schematic.png\n"
        "  kruskal_horizon_charts.png\n"
        "  kruskal_diagnostics.txt\n"
        "  atlas_extension_graph.png\n"
        "  extension_notes.txt\n"
        "  boundary_classification.txt\n"
        "  finite_r_endpoint_kruskal.txt\n"
        "  affine_boundary_analysis.txt\n"
        "  timelike_crossing_example.txt\n"
        "  front_endpoint_timelike_example.txt\n"
        "  white_horizon_extension.txt\n"
        "  minimal_front_cauchy_extension.png\n"
        "  accurate_local_front_extension.png\n"
        "  accurate_local_front_extension_notes.txt\n"
        "  front_generator_affine_calculation.txt\n"
        "  front_endpoint_branch_series.txt\n"
        "  forward_cplus_extension_atlas.png\n"
        "  forward_cplus_extension_atlas_notes.txt\n"
        "  local_front_geodesic_regularization.txt\n"
        "  forward_extension_region_classification.txt\n"
        "  forward_extension_branch_global_scan.txt\n"
        "  forward_extension_branch_global_scan.png\n"
        "  forward_regionIII_branch_chart.png\n"
        "  forward_regionIII_branch_chart_notes.txt\n"
        "  forward_regionIII_boundary_classification.txt\n"
        "  forward_regionIII_future_corner_check.txt\n"
        "  forward_extension_composite.png\n"
        "  forward_extension_composite_notes.txt\n"
        "  rear_cminus_extension_calculation.txt\n"
        "  rear_regionI_branch_chart.png\n"
        "  rear_regionI_branch_chart_notes.txt\n"
        "  rear_regionI_boundary_classification.txt\n"
        "  two_sided_extension_composite.png\n"
        "  two_sided_extension_summary.txt\n"
        "  local_endpoint_geodesic_completeness_check.txt\n"
    )
    (p.out_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
