"""Numerical 1+1 eternal Alcubierre warp-drive causal patch.

Metric convention:
    ds^2 = -dt^2 + (dr - v(r) dt)^2
    v(r) = v_s * (f(r) - 1)

The bubble center/rider is r = 0.  For v_s > 1, the roots of
v(r) + 1 = 0 are the two horizon locations in the stationary patch.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.optimize import brentq


@dataclass(frozen=True)
class Params:
    v_s: float = 2.0
    radius: float = 1.0
    sigma: float = 6.0
    r_max: float = 5.0
    n_grid: int = 3000
    t_max: float = 8.0
    out_dir: Path = Path("output")


def shape(r: np.ndarray | float, radius: float, sigma: float) -> np.ndarray | float:
    """Alcubierre wall profile, approximately 1 inside and 0 outside."""
    denom = 2.0 * np.tanh(sigma * radius)
    return (np.tanh(sigma * (np.asarray(r) + radius)) - np.tanh(sigma * (np.asarray(r) - radius))) / denom


def flow(r: np.ndarray | float, p: Params) -> np.ndarray | float:
    """Shift-flow velocity v(r) in the stationary 1+1 metric."""
    return p.v_s * (shape(r, p.radius, p.sigma) - 1.0)


def find_horizons(p: Params) -> tuple[float, float]:
    """Solve v(r) + 1 = 0 for the rear/front horizons."""
    h = lambda x: float(flow(x, p) + 1.0)
    left = brentq(h, -p.r_max, 0.0)
    right = brentq(h, 0.0, p.r_max)
    return left, right


def flow_derivative(r: float, p: Params) -> float:
    """Numerical derivative of the stationary flow at a horizon."""
    step = 1.0e-5 * max(1.0, abs(r), p.radius)
    return float((flow(r + step, p) - flow(r - step, p)) / (2.0 * step))


def cumulative_from_zero(r: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Return integral of y dr with reference value 0 at r closest to 0."""
    i0 = int(np.argmin(np.abs(r)))
    out = np.zeros_like(r)
    out[i0:] = cumulative_trapezoid(y[i0:], r[i0:], initial=0.0)
    left_r = r[: i0 + 1][::-1]
    left_y = y[: i0 + 1][::-1]
    out[: i0 + 1] = cumulative_trapezoid(left_y, left_r, initial=0.0)[::-1]
    return out


def conformal_coords(t: np.ndarray, f_plus: np.ndarray, f_minus: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Compactified null coordinates for u=t-F_+, w=t-F_-."""
    u = t - f_plus
    w = t - f_minus
    u_bar = np.arctan(u)
    w_bar = np.arctan(w)
    big_t = 0.5 * (u_bar + w_bar)
    big_x = 0.5 * (w_bar - u_bar)
    return big_t, big_x


def plot_stationary_characteristics(p: Params, r1: float, r2: float) -> None:
    r = np.linspace(-p.r_max, p.r_max, 1400)
    vp = flow(r, p) + 1.0
    vm = flow(r, p) - 1.0

    fig, ax = plt.subplots(figsize=(10, 5.8), constrained_layout=True)
    ax.plot(r, vp, color="#1f6f8b", lw=2, label=r"$dr/dt = v(r)+1$")
    ax.plot(r, vm, color="#7d4fa3", lw=2, label=r"$dr/dt = v(r)-1$")
    ax.axhline(0, color="black", lw=1)
    ax.axvline(r1, color="#0b7a63", lw=2, ls="--", label=rf"horizons $r_1={r1:.4f}$, $r_2={r2:.4f}$")
    ax.axvline(r2, color="#0b7a63", lw=2, ls="--")
    ax.axvline(0, color="#c14d3f", lw=2, label="rider, r=0")
    ax.set_xlabel("comoving coordinate r")
    ax.set_ylabel("null coordinate speed dr/dt")
    ax.set_title("Eternal 1+1 Alcubierre null slopes")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.25)
    fig.savefig(p.out_dir / "null_slopes.png", dpi=180)
    plt.close(fig)


def plot_central_conformal_patch(p: Params, r1: float, r2: float) -> None:
    eps = 1.0e-4 * (r2 - r1)
    r = np.linspace(r1 + eps, r2 - eps, p.n_grid)
    v = flow(r, p)
    f_plus = cumulative_from_zero(r, 1.0 / (v + 1.0))
    f_minus = cumulative_from_zero(r, 1.0 / (v - 1.0))

    fig, ax = plt.subplots(figsize=(7.4, 8.4), constrained_layout=True)

    t_values = np.linspace(-p.t_max, p.t_max, 13)
    for t0 in t_values:
        t = np.full_like(r, t0)
        big_t, big_x = conformal_coords(t, f_plus, f_minus)
        ax.plot(big_x, big_t, color="#555555", lw=0.8, ls=(0, (6, 5)), alpha=0.8)

    r_values = np.r_[np.linspace(r1 + 0.08, -0.15, 5), [0.0], np.linspace(0.15, r2 - 0.08, 5)]
    t = np.linspace(-p.t_max, p.t_max, 1200)
    for r0 in r_values:
        fp = np.interp(r0, r, f_plus)
        fm = np.interp(r0, r, f_minus)
        big_t, big_x = conformal_coords(t, fp, fm)
        color = "#c14d3f" if abs(r0) < 1.0e-12 else "#20252b"
        lw = 2.4 if abs(r0) < 1.0e-12 else 1.1
        label = "rider r=0" if abs(r0) < 1.0e-12 else None
        ax.plot(big_x, big_t, color=color, lw=lw, label=label)

    for r0, label in [(r1 + eps, r"$r_1$ horizon"), (r2 - eps, r"$r_2$ horizon")]:
        fp = np.interp(r0, r, f_plus)
        fm = np.interp(r0, r, f_minus)
        big_t, big_x = conformal_coords(t, fp, fm)
        ax.plot(big_x, big_t, color="#0b7a63", lw=2.0, ls="--", label=label)

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"compact coordinate $X=(\bar w-\bar u)/2$")
    ax.set_ylabel(r"compact coordinate $T=(\bar u+\bar w)/2$")
    ax.set_title("Central conformal patch: eternal 1+1 warp drive")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.2)
    fig.savefig(p.out_dir / "central_conformal_patch.png", dpi=180)
    plt.close(fig)


def integrate_region(r: np.ndarray, y: np.ndarray, ref: float) -> np.ndarray:
    """Integral of y dr on a monotone r grid, shifted to vanish at ref."""
    raw = cumulative_trapezoid(y, r, initial=0.0)
    return raw - np.interp(ref, r, raw)


def paper_u_to_U(region: str, u: np.ndarray, kappa: float) -> np.ndarray:
    """Finazzi-Liberati-Barcelo style regular U coordinate in each region."""
    if region == "I":
        return 0.5 + np.exp(-kappa * u)
    if region == "II":
        return 0.5 * np.tanh(0.5 * kappa * u)
    if region == "III":
        return -0.5 - np.exp(kappa * u)
    raise ValueError(region)


def plot_extended_paper_patch(p: Params, r1: float, r2: float, kappa: float) -> None:
    """Plot the three-region eternal warp-drive conformal patch.

    This follows the construction in Finazzi, Liberati, and Barcelo:
    piecewise regularized U(u) for regions I/II/III, and W=arctan(w).
    """
    eps = 5.0e-4 * (r2 - r1)
    regions = {
        "I": np.linspace(-p.r_max, r1 - eps, p.n_grid),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, p.r_max, p.n_grid),
    }
    refs = {"I": -0.5 * (p.r_max + abs(r1)), "II": 0.0, "III": 0.5 * (p.r_max + r2)}

    global_r = np.linspace(-p.r_max, p.r_max, 3 * p.n_grid)
    global_w_integral = cumulative_from_zero(global_r, 1.0 / (1.0 - flow(global_r, p)))

    data: dict[str, dict[str, np.ndarray]] = {}
    for name, r in regions.items():
        v = flow(r, p)
        f_plus = integrate_region(r, 1.0 / (v + 1.0), refs[name])
        f_minus = np.interp(r, global_r, global_w_integral)
        data[name] = {"r": r, "f_plus": f_plus, "f_minus": f_minus}

    fig, ax = plt.subplots(figsize=(8.8, 8.8), constrained_layout=True)

    def xy_for(region: str, t: np.ndarray, r_or_index: np.ndarray | int) -> tuple[np.ndarray, np.ndarray]:
        item = data[region]
        if isinstance(r_or_index, int):
            fp = item["f_plus"][r_or_index]
            fm = item["f_minus"][r_or_index]
        else:
            fp = item["f_plus"]
            fm = item["f_minus"]
        u = t - fp
        w = t + fm
        U = paper_u_to_U(region, u, kappa)
        ubar = np.arctan(U)
        wbar = np.arctan(w)
        return 0.5 * (wbar - ubar), 0.5 * (wbar + ubar)

    def xy_for_r_value(region: str, t: np.ndarray, r0: float) -> tuple[np.ndarray, np.ndarray]:
        item = data[region]
        fp = np.interp(r0, item["r"], item["f_plus"])
        fm = np.interp(r0, item["r"], item["f_minus"])
        u = t - fp
        w = t + fm
        U = paper_u_to_U(region, u, kappa)
        ubar = np.arctan(U)
        wbar = np.arctan(w)
        return 0.5 * (wbar - ubar), 0.5 * (wbar + ubar)

    def point(region: str, r0: float, t0: float) -> tuple[float, float]:
        x, y = xy_for_r_value(region, np.array([t0]), r0)
        return float(x[0]), float(y[0])

    def add_label(text: str, xy: tuple[float, float], dx: float = 0.0, dy: float = 0.0, size: int = 10) -> None:
        ax.text(
            xy[0] + dx,
            xy[1] + dy,
            text,
            ha="center",
            va="center",
            fontsize=size,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.72, "pad": 1.5},
        )

    # Constant t curves, dashed.
    for t0 in np.linspace(-p.t_max, p.t_max, 13):
        for region in ("I", "II", "III"):
            t = np.full_like(data[region]["r"], t0)
            x, y = xy_for(region, t, data[region]["r"])
            ax.plot(x, y, color="#6b6f73", lw=0.75, ls=(0, (7, 6)), alpha=0.75)

    # Constant r curves, solid. Include the rider explicitly.
    r_samples = {
        "I": np.linspace(-p.r_max + 0.25, r1 - 0.16, 5),
        "II": np.r_[np.linspace(r1 + 0.16, -0.18, 4), [0.0], np.linspace(0.18, r2 - 0.16, 4)],
        "III": np.linspace(r2 + 0.16, p.r_max - 0.25, 5),
    }
    t = np.linspace(-p.t_max, p.t_max, 1600)
    for region, samples in r_samples.items():
        item = data[region]
        for r0 in samples:
            idx = int(np.argmin(np.abs(item["r"] - r0)))
            x, y = xy_for(region, t, idx)
            is_rider = region == "II" and abs(r0) < 1.0e-12
            ax.plot(
                x,
                y,
                color="#c14d3f" if is_rider else "#20252b",
                lw=2.8 if is_rider else 1.05,
                label="rider r=0" if is_rider else None,
            )

    # Horizon boundaries are approached from adjacent regions.
    horizon_specs = [
        ("I", -1, r"$r_1$ outer side"),
        ("II", 0, r"$r_1$ central side"),
        ("II", -1, r"$r_2$ central side"),
        ("III", 0, r"$r_2$ outer side"),
    ]
    for region, idx, label in horizon_specs:
        x, y = xy_for(region, t, idx)
        ax.plot(x, y, color="#0b7a63", lw=2.0, ls="--", label=label)

    # Exact conformal boundary skeleton in (mathcal U, mathcal W).
    b = 0.5 * np.pi
    a = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    def const_u(ubar: float) -> None:
        s = np.linspace(-b, b, 300)
        x, y = from_null(np.full_like(s, ubar), s)
        ax.plot(x, y, color="#555555", lw=1.5, alpha=0.95)

    def const_w(umin: float, umax: float, wbar: float) -> None:
        s = np.linspace(umin, umax, 300)
        x, y = from_null(s, np.full_like(s, wbar))
        ax.plot(x, y, color="#555555", lw=1.5, alpha=0.95)

    def coord(ubar: float, wbar: float) -> tuple[float, float]:
        x, y = from_null(ubar, wbar)
        return float(x), float(y)

    const_u(b)
    const_u(-b)
    for umin, umax in [(a, b), (-a, a), (-b, -a)]:
        const_w(umin, umax, b)
        const_w(umin, umax, -b)

    add_label(r"$i^+$", coord(a, b), dx=0.04, dy=0.05, size=13)
    add_label(r"$i^-$", coord(-a, -b), dx=-0.04, dy=-0.05, size=13)
    add_label(r"$i^0_L$", coord(b, -b), dx=-0.08, dy=0.04, size=12)
    add_label(r"$i^0_R$", coord(-b, b), dx=0.08, dy=-0.04, size=12)

    add_label(r"$\mathscr{I}^+_L$", coord(0.5 * (a + b), b), dx=0.00, dy=0.05)
    add_label(r"$\mathscr{I}^-_L$", coord(0.5 * (a + b), -b), dx=-0.03, dy=-0.05)
    add_label(r"$\mathscr{I}^+_C$", coord(0.0, b), dx=0.00, dy=0.05)
    add_label(r"$\mathscr{I}^-_C$", coord(0.0, -b), dx=0.00, dy=-0.05)
    add_label(r"$\mathscr{I}^+_R$", coord(-0.5 * (a + b), b), dx=0.03, dy=0.05)
    add_label(r"$\mathscr{I}^-_R$", coord(-0.5 * (a + b), -b), dx=0.03, dy=-0.05)

    add_label(r"$\mathscr{H}^+$", coord(a, 0.72 * b), dx=-0.04, dy=0.00)
    add_label(r"$\mathscr{H}^-$", coord(-a, -0.72 * b), dx=0.04, dy=0.00)

    ax.text(-0.62, 0.02, "I\nleft exterior", ha="center", va="center", fontsize=10)
    ax.text(0.0, 0.02, "II\nbubble", ha="center", va="center", fontsize=10)
    ax.text(0.62, 0.02, "III\nright exterior", ha="center", va="center", fontsize=10)
    ax.text(0.03, 0.58, r"$r=0$ rider", color="#c14d3f", fontsize=10)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"compact coordinate $(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"compact coordinate $(\mathcal{W}+\mathcal{U})/2$")
    ax.set_title("Extended eternal 1+1 warp-drive conformal patch")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.18)
    fig.savefig(p.out_dir / "extended_paper_patch.png", dpi=180)
    plt.close(fig)


def plot_trip_overlay(p: Params, r1: float, r2: float, kappa: float) -> None:
    """Overlay asymptotic-trip worldlines on the conformal patch.

    We use lab-frame x=t*speed curves and transform to the stationary
    bubble coordinate r=x-v_s t.  Curves are only drawn where they pass through
    one of the three stationary regions represented by the eternal diagram.
    """
    eps = 5.0e-4 * (r2 - r1)
    r_extent = 40.0
    n_overlay = max(p.n_grid, 6000)
    regions = {
        "I": np.linspace(-r_extent, r1 - eps, n_overlay),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, r_extent, n_overlay),
    }
    refs = {"I": -0.5 * (r_extent + abs(r1)), "II": 0.0, "III": 0.5 * (r_extent + r2)}
    global_r = np.linspace(-r_extent, r_extent, 3 * n_overlay)
    global_w_integral = cumulative_from_zero(global_r, 1.0 / (1.0 - flow(global_r, p)))

    data: dict[str, dict[str, np.ndarray]] = {}
    for name, r in regions.items():
        v = flow(r, p)
        data[name] = {
            "r": r,
            "f_plus": integrate_region(r, 1.0 / (v + 1.0), refs[name]),
            "f_minus": np.interp(r, global_r, global_w_integral),
        }

    def region_for_r(r: np.ndarray) -> np.ndarray:
        out = np.full(r.shape, "", dtype=object)
        out[r < r1 - eps] = "I"
        out[(r > r1 + eps) & (r < r2 - eps)] = "II"
        out[r > r2 + eps] = "III"
        return out

    def xy(region: str, t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        item = data[region]
        fp = np.interp(r, item["r"], item["f_plus"])
        fm = np.interp(r, item["r"], item["f_minus"])
        u = t - fp
        w = t + fm
        U = paper_u_to_U(region, u, kappa)
        ubar = np.arctan(U)
        wbar = np.arctan(w)
        return 0.5 * (wbar - ubar), 0.5 * (wbar + ubar)

    def plot_param_curve(ax, label: str, t: np.ndarray, r: np.ndarray, color: str, lw: float, ls: str = "-") -> None:
        regions_for_points = region_for_r(r)
        first_label = True
        for region in ("I", "II", "III"):
            mask = regions_for_points == region
            if not np.any(mask):
                continue
            idx = np.where(mask)[0]
            splits = np.where(np.diff(idx) > 1)[0] + 1
            for block in np.split(idx, splits):
                if len(block) < 3:
                    continue
                x, y = xy(region, t[block], r[block])
                ax.plot(x, y, color=color, lw=lw, ls=ls, label=label if first_label else None)
                first_label = False

    fig, ax = plt.subplots(figsize=(9.5, 8.8), constrained_layout=True)
    b = 0.5 * np.pi
    a = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    def const_u(ubar: float) -> None:
        s = np.linspace(-b, b, 300)
        ax.plot(*from_null(np.full_like(s, ubar), s), color="#dddddd", lw=1.0)

    def const_w(umin: float, umax: float, wbar: float) -> None:
        s = np.linspace(umin, umax, 300)
        ax.plot(*from_null(s, np.full_like(s, wbar)), color="#dddddd", lw=1.0)

    const_u(b)
    const_u(-b)
    for umin, umax in [(a, b), (-a, a), (-b, -a)]:
        const_w(umin, umax, b)
        const_w(umin, umax, -b)

    # Plot horizons and rider from stationary coordinates for context.
    t_context = np.linspace(-p.t_max, p.t_max, 1400)
    for region, idx in [("I", -1), ("II", 0), ("II", -1), ("III", 0)]:
        r_edge = np.full_like(t_context, data[region]["r"][idx])
        xh, yh = xy(region, t_context, r_edge)
        ax.plot(xh, yh, color="#0b7a63", lw=1.6, ls="--", alpha=0.75)
    plot_param_curve(ax, "bubble rider r=0", t_context, np.zeros_like(t_context), "#c14d3f", 3.0)

    # Trip scenario in asymptotic lab coordinates.
    L = 2.0
    u_ship = 0.75
    t_trip = np.linspace(-0.2, L / u_ship + 0.6, 1800)
    t_star = np.linspace((L - r_extent) / p.v_s, r_extent / p.v_s, 4000)
    star_a_r = -p.v_s * t_star
    star_b_r = L - p.v_s * t_star
    light_r = (1.0 - p.v_s) * t_trip
    slow_r = (u_ship - p.v_s) * t_trip

    plot_param_curve(ax, "star A: x=0", t_star, star_a_r, "#6f6f6f", 2.0, ":")
    plot_param_curve(ax, "star B: x=L", t_star, star_b_r, "#303030", 2.0, ":")
    plot_param_curve(ax, "Minkowski light from A", t_trip, light_r, "#d99022", 2.1, "--")
    plot_param_curve(ax, f"subluminal traveler u={u_ship}", t_trip, slow_r, "#1f6f8b", 2.1, "-.")

    # Mark key crossing events.
    for name, t0, dy in [("depart A", 0.0, -0.06), ("bubble reaches B", L / p.v_s, 0.06)]:
        x0, y0 = xy("II", np.array([t0]), np.array([0.0]))
        ax.scatter(x0, y0, s=42, color="#c14d3f", zorder=5)
        ax.text(float(x0[0]) + 0.035, float(y0[0]) + dy, name, color="#c14d3f", fontsize=9)

    comparison_events = [
        ("light reaches B", L, L - p.v_s * L, "#d99022", 0.05),
        ("slow traveler reaches B", L / u_ship, L - p.v_s * (L / u_ship), "#1f6f8b", -0.07),
    ]
    for name, t0, r0, color, dy in comparison_events:
        region = "I" if r0 < r1 else "II" if r0 < r2 else "III"
        x0, y0 = xy(region, np.array([t0]), np.array([r0]))
        ax.scatter(x0, y0, s=36, color=color, zorder=5)
        ax.text(float(x0[0]) + 0.04, float(y0[0]) + dy, name, color=color, fontsize=9)

    ax.text(-1.42, 1.42, r"$\mathscr{I}^+_L$", fontsize=10)
    ax.text(1.28, -1.42, r"$\mathscr{I}^-_R$", fontsize=10)
    ax.text(0.03, 1.04, r"$i^+$", fontsize=12)
    ax.text(-0.62, 0.02, "I", ha="center", va="center", fontsize=10)
    ax.text(0.0, 0.02, "II", ha="center", va="center", fontsize=10)
    ax.text(0.62, 0.02, "III", ha="center", va="center", fontsize=10)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"compact coordinate $(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"compact coordinate $(\mathcal{W}+\mathcal{U})/2$")
    ax.set_title("Trip comparison overlay: L=2, warp speed=2, ordinary speed=0.75")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.15)
    fig.savefig(p.out_dir / "trip_overlay.png", dpi=180)
    plt.close(fig)


def plot_proper_trip_overlay(p: Params, r1: float, r2: float, kappa: float) -> None:
    """Trip overlay with causal character checked in the full warp metric.

    A lab-frame curve x(t) has
        ds^2/dt^2 = -1 + [dx/dt - v_s f(x-v_s t)]^2.
    Static stars x=const are not timelike while the superluminal bubble core
    passes over them.  This plot makes that failure explicit.
    """
    eps = 5.0e-4 * (r2 - r1)
    r_extent = 40.0
    n_overlay = max(p.n_grid, 6000)
    regions = {
        "I": np.linspace(-r_extent, r1 - eps, n_overlay),
        "II": np.linspace(r1 + eps, r2 - eps, p.n_grid),
        "III": np.linspace(r2 + eps, r_extent, n_overlay),
    }
    refs = {"I": -0.5 * (r_extent + abs(r1)), "II": 0.0, "III": 0.5 * (r_extent + r2)}
    global_r = np.linspace(-r_extent, r_extent, 3 * n_overlay)
    global_w_integral = cumulative_from_zero(global_r, 1.0 / (1.0 - flow(global_r, p)))

    data: dict[str, dict[str, np.ndarray]] = {}
    for name, r in regions.items():
        v = flow(r, p)
        data[name] = {
            "r": r,
            "f_plus": integrate_region(r, 1.0 / (v + 1.0), refs[name]),
            "f_minus": np.interp(r, global_r, global_w_integral),
        }

    def region_for_r(r: np.ndarray) -> np.ndarray:
        out = np.full(r.shape, "", dtype=object)
        out[r < r1 - eps] = "I"
        out[(r > r1 + eps) & (r < r2 - eps)] = "II"
        out[r > r2 + eps] = "III"
        return out

    def xy(region: str, t: np.ndarray, r: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        item = data[region]
        fp = np.interp(r, item["r"], item["f_plus"])
        fm = np.interp(r, item["r"], item["f_minus"])
        u = t - fp
        w = t + fm
        U = paper_u_to_U(region, u, kappa)
        ubar = np.arctan(U)
        wbar = np.arctan(w)
        return 0.5 * (wbar - ubar), 0.5 * (wbar + ubar)

    def plot_segments(ax, label: str, t: np.ndarray, r: np.ndarray, mask: np.ndarray, color: str, lw: float, ls: str) -> None:
        regions_for_points = region_for_r(r)
        first_label = True
        for region in ("I", "II", "III"):
            combined = (regions_for_points == region) & mask
            if not np.any(combined):
                continue
            idx = np.where(combined)[0]
            splits = np.where(np.diff(idx) > 1)[0] + 1
            for block in np.split(idx, splits):
                if len(block) < 3:
                    continue
                x, y = xy(region, t[block], r[block])
                ax.plot(x, y, color=color, lw=lw, ls=ls, label=label if first_label else None)
                first_label = False

    def interval_where_spacelike_for_static_star(x0: float) -> tuple[float, float]:
        # Static x=x0 is null where v_s f(r)=1.  Between those roots it is spacelike.
        root_left = brentq(lambda rr: p.v_s * shape(rr, p.radius, p.sigma) - 1.0, -p.r_max, 0.0)
        root_right = brentq(lambda rr: p.v_s * shape(rr, p.radius, p.sigma) - 1.0, 0.0, p.r_max)
        return (x0 - root_right) / p.v_s, (x0 - root_left) / p.v_s

    fig, ax = plt.subplots(figsize=(9.5, 8.8), constrained_layout=True)

    b = 0.5 * np.pi
    a = float(np.arctan(0.5))

    def from_null(ubar: np.ndarray | float, wbar: np.ndarray | float) -> tuple[np.ndarray, np.ndarray]:
        return 0.5 * (np.asarray(wbar) - np.asarray(ubar)), 0.5 * (np.asarray(wbar) + np.asarray(ubar))

    for ubar in (b, -b):
        s = np.linspace(-b, b, 300)
        ax.plot(*from_null(np.full_like(s, ubar), s), color="#dddddd", lw=1.0)
    for umin, umax in [(a, b), (-a, a), (-b, -a)]:
        s = np.linspace(umin, umax, 300)
        ax.plot(*from_null(s, np.full_like(s, b)), color="#dddddd", lw=1.0)
        ax.plot(*from_null(s, np.full_like(s, -b)), color="#dddddd", lw=1.0)

    t_context = np.linspace(-p.t_max, p.t_max, 1400)
    for region, idx in [("I", -1), ("II", 0), ("II", -1), ("III", 0)]:
        r_edge = np.full_like(t_context, data[region]["r"][idx])
        xh, yh = xy(region, t_context, r_edge)
        ax.plot(xh, yh, color="#0b7a63", lw=1.4, ls="--", alpha=0.55)
    rider_x, rider_y = xy("II", t_context, np.zeros_like(t_context))
    ax.plot(rider_x, rider_y, color="#c14d3f", lw=3.0, label="rider r=0, timelike")

    L = 2.0
    t = np.linspace((L - r_extent) / p.v_s, r_extent / p.v_s, 5000)
    for label, x0, color in [("star A x=0", 0.0, "#6f6f6f"), ("star B x=L", L, "#303030")]:
        r = x0 - p.v_s * t
        norm = -1.0 + (0.0 - p.v_s * shape(r, p.radius, p.sigma)) ** 2
        plot_segments(ax, f"{label}: timelike parts", t, r, norm < -1.0e-4, color, 2.0, ":")
        plot_segments(ax, f"{label}: spacelike through bubble", t, r, norm > 1.0e-4, "#b23b3b", 2.4, (0, (3, 2)))
        t0, t1 = interval_where_spacelike_for_static_star(x0)
        ax.text(0.66 if x0 else -0.72, 0.43 if x0 else -0.47, f"{label} spacelike\nfor t in [{t0:.2f}, {t1:.2f}]", color="#8b2f2f", fontsize=8)

    # Asymptotic comparison events only; the B crossing by the eternal bubble is a coordinate event,
    # not a meeting with a timelike static-star worldline.
    events = [
        ("depart A", 0.0, 0.0, "#c14d3f", -0.06),
        ("coordinate x=L reached by rider", L / p.v_s, 0.0, "#c14d3f", 0.06),
        ("light reaches x=L", L, L - p.v_s * L, "#d99022", 0.05),
        ("u=.75 reaches x=L", L / 0.75, L - p.v_s * (L / 0.75), "#1f6f8b", -0.07),
    ]
    for name, t0, r0, color, dy in events:
        region = "I" if r0 < r1 else "II" if r0 < r2 else "III"
        x0, y0 = xy(region, np.array([t0]), np.array([r0]))
        ax.scatter(x0, y0, s=38, color=color, zorder=5)
        ax.text(float(x0[0]) + 0.035, float(y0[0]) + dy, name, color=color, fontsize=8.5)

    ax.text(-1.42, 1.42, r"$\mathscr{I}^+_L$", fontsize=10)
    ax.text(1.28, -1.42, r"$\mathscr{I}^-_R$", fontsize=10)
    ax.text(0.03, 1.04, r"$i^+$", fontsize=12)
    ax.text(-0.62, 0.02, "I", ha="center", va="center", fontsize=10)
    ax.text(0.0, 0.02, "II", ha="center", va="center", fontsize=10)
    ax.text(0.62, 0.02, "III", ha="center", va="center", fontsize=10)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"compact coordinate $(\mathcal{W}-\mathcal{U})/2$")
    ax.set_ylabel(r"compact coordinate $(\mathcal{W}+\mathcal{U})/2$")
    ax.set_title("Proper trip overlay: static lab stars fail to stay timelike in the bubble")
    ax.legend(loc="upper right", fontsize=7.6)
    ax.grid(True, alpha=0.15)
    fig.savefig(p.out_dir / "proper_trip_overlay.png", dpi=180)
    plt.close(fig)


def main() -> None:
    p = Params()
    p.out_dir.mkdir(parents=True, exist_ok=True)
    print("finding horizons...", flush=True)
    r1, r2 = find_horizons(p)
    k1 = flow_derivative(r1, p)
    k2 = flow_derivative(r2, p)
    print(f"horizons: r1={r1:.10f}, r2={r2:.10f}", flush=True)
    print(f"flow derivatives: v'(r1)={k1:.10f}, v'(r2)={k2:.10f}", flush=True)
    print("plotting stationary characteristics...", flush=True)
    plot_stationary_characteristics(p, r1, r2)
    print("plotting central conformal patch...", flush=True)
    plot_central_conformal_patch(p, r1, r2)
    print("plotting extended three-region conformal patch...", flush=True)
    plot_extended_paper_patch(p, r1, r2, abs(k1))
    print("plotting asymptotic trip overlay...", flush=True)
    plot_trip_overlay(p, r1, r2, abs(k1))
    print("plotting causal-character checked trip overlay...", flush=True)
    plot_proper_trip_overlay(p, r1, r2, abs(k1))

    summary = (
        "Eternal 1+1 Alcubierre calculation\n"
        f"v_s = {p.v_s}\n"
        f"R = {p.radius}\n"
        f"sigma = {p.sigma}\n"
        f"rear/front roots of v(r)+1=0: r1 = {r1:.10f}, r2 = {r2:.10f}\n"
        f"flow derivatives at roots: v'(r1) = {k1:.10f}, v'(r2) = {k2:.10f}\n"
        f"surface-gravity scales: kappa1 = {abs(k1):.10f}, kappa2 = {abs(k2):.10f}\n"
        "rider worldline: r = 0, ds^2 = -dt^2\n"
        "outputs:\n"
        "  null_slopes.png\n"
        "  central_conformal_patch.png\n"
        "  extended_paper_patch.png\n"
        "  trip_overlay.png\n"
        "  proper_trip_overlay.png\n"
    )
    (p.out_dir / "summary.txt").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
