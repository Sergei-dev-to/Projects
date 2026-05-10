#!/usr/bin/env python3
"""
Calculated electrostatic field for a point charge near a smooth Ellis wormhole.

The script builds the Khusnutdinov--Bakhmatov two-ended Green function by a
radial spherical-harmonic mode sum, then adds the homogeneous l=0 correction
that keeps the opposite-end / throat flux fixed to zero.  The output figure is
a meridional coordinate slice: rho is the wormhole radial coordinate and theta
is the polar angle from the charge axis.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.interpolate import RegularGridInterpolator
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve
from scipy.special import eval_legendre


A_THROAT = 1.0
CHARGE = 1.0
RHO0 = 2.55
RHO_MAX = 12.0
N_RHO = 1801
N_THETA = 361
L_MAX = 90
PLOT_FILTER_SCALE = 42.0
PLOT_FILTER_ORDER = 8

OUT_PNG = Path("fig_ellis_fixed_sector_field.png")
OUT_PDF = Path("fig_ellis_fixed_sector_field.pdf")
OUT_NATIVE_PNG = Path("fig_ellis_fixed_sector_native.png")
OUT_NATIVE_PDF = Path("fig_ellis_fixed_sector_native.pdf")
OUT_AREAL_PNG = Path("fig_ellis_fixed_sector_areal.png")
OUT_AREAL_PDF = Path("fig_ellis_fixed_sector_areal.pdf")
OUT_AREAL_CLEAN_PNG = Path("fig_ellis_fixed_sector_areal_clean.png")
OUT_AREAL_CLEAN_PDF = Path("fig_ellis_fixed_sector_areal_clean.pdf")


def solve_radial_modes(rho: np.ndarray, rho0: float, l_max: int) -> np.ndarray:
    """Solve radial Green modes with zero potential at both numerical ends.

    The l=0 mode is filled analytically.  For l>=1 we solve

        d/d rho [(rho^2+a^2) dR_l/d rho] - l(l+1) R_l = -delta(rho-rho0)

    with R_l=0 at rho=+-RHO_MAX.  This is the decaying two-ended Green function
    on a large finite interval.
    """

    h = rho[1] - rho[0]
    n = rho.size
    modes = np.zeros((l_max + 1, n), dtype=float)

    x = rho / A_THROAT
    x0 = rho0 / A_THROAT
    y_minus = math.pi / 2.0 + np.arctan(x)
    y_plus = math.pi / 2.0 - np.arctan(x)
    y0_minus = math.pi / 2.0 + math.atan(x0)
    y0_plus = math.pi / 2.0 - math.atan(x0)
    left = rho <= rho0
    modes[0, left] = y_minus[left] * y0_plus / (math.pi * A_THROAT)
    modes[0, ~left] = y0_minus * y_plus[~left] / (math.pi * A_THROAT)

    # Source deposition into the nearest two radial cells.
    j = int(np.searchsorted(rho, rho0) - 1)
    j = max(1, min(n - 3, j))
    t = (rho0 - rho[j]) / h
    src = np.zeros(n - 2)
    src[j - 1] -= (1.0 - t) / h
    src[j] -= t / h

    p_half = ((rho[:-1] + rho[1:]) * 0.5) ** 2 + A_THROAT**2
    lower_base = p_half[:-1] / h**2
    upper_base = p_half[1:] / h**2
    main_base = -(p_half[:-1] + p_half[1:]) / h**2

    for ell in range(1, l_max + 1):
        main = main_base - ell * (ell + 1.0)
        mat = diags(
            diagonals=[lower_base[1:], main, upper_base[:-1]],
            offsets=[-1, 0, 1],
            shape=(n - 2, n - 2),
            format="csc",
        )
        modes[ell, 1:-1] = spsolve(mat, src)

    return modes


def build_potential(
    rho: np.ndarray,
    theta: np.ndarray,
    modes: np.ndarray,
    spectral_filter: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return KB potential, fixed-sector potential, and l=0 correction."""

    mu = np.cos(theta)
    pot_kb = np.zeros((theta.size, rho.size), dtype=float)
    if spectral_filter is None:
        spectral_filter = np.ones(modes.shape[0], dtype=float)

    for ell in range(modes.shape[0]):
        pl = eval_legendre(ell, mu)[:, None]
        pot_kb += (
            spectral_filter[ell]
            * CHARGE
            * (2 * ell + 1)
            * pl
            * modes[ell][None, :]
        )

    c_far = 0.5 - math.atan(RHO0 / A_THROAT) / math.pi
    # This is e*(-c_far/a)*atan(rho/a), plus a gauge constant chosen so that
    # the positive infinity asymptotic constant is zero.
    corr = (
        -CHARGE
        * c_far
        / A_THROAT
        * (np.arctan(rho / A_THROAT) - math.pi / 2.0)
    )
    pot_fixed = pot_kb + corr[None, :]
    return pot_kb, pot_fixed, corr


def plot_spectral_filter(l_max: int) -> np.ndarray:
    ell = np.arange(l_max + 1, dtype=float)
    filt = np.exp(-((ell / PLOT_FILTER_SCALE) ** PLOT_FILTER_ORDER))
    filt[0] = 1.0
    return filt


def field_components(
    rho: np.ndarray, theta: np.ndarray, potential: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Contravariant field components E^rho and E^theta."""

    dtheta = theta[1] - theta[0]
    drho = rho[1] - rho[0]
    d_a_drho = np.gradient(potential, drho, axis=1, edge_order=2)
    d_a_dtheta = np.gradient(potential, dtheta, axis=0, edge_order=2)
    r2 = rho[None, :] ** 2 + A_THROAT**2
    e_rho = -d_a_drho
    e_theta = -d_a_dtheta / r2
    return e_rho, e_theta


def trace_field_lines(
    rho: np.ndarray,
    theta: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
    seeds: list[tuple[float, float]],
    step: float = 0.035,
    n_steps: int = 1500,
) -> list[np.ndarray]:
    """Integrate field lines in the (rho, theta) coordinate plane."""

    interp_er = RegularGridInterpolator(
        (theta, rho), e_rho, bounds_error=False, fill_value=np.nan
    )
    interp_et = RegularGridInterpolator(
        (theta, rho), e_theta, bounds_error=False, fill_value=np.nan
    )

    def unit_vec(point: np.ndarray) -> np.ndarray | None:
        th, rr = point
        vec = np.array([interp_et((th, rr)), interp_er((th, rr))], dtype=float)
        if not np.all(np.isfinite(vec)):
            return None
        scale = math.hypot(vec[0], vec[1])
        if scale < 1e-10:
            return None
        return vec / scale

    lines: list[np.ndarray] = []
    for rr0, th0 in seeds:
        for sign in (-1.0, 1.0):
            pts = []
            p = np.array([th0, rr0], dtype=float)
            for _ in range(n_steps):
                if not (rho[2] < p[1] < rho[-3] and theta[2] < p[0] < theta[-3]):
                    break
                # Stop just outside the point charge.
                if (p[1] - RHO0) ** 2 + (A_THROAT * p[0]) ** 2 < 0.035**2:
                    break
                pts.append([p[1], p[0]])
                k1 = unit_vec(p)
                if k1 is None:
                    break
                k2 = unit_vec(p + 0.5 * sign * step * k1)
                if k2 is None:
                    break
                k3 = unit_vec(p + 0.5 * sign * step * k2)
                if k3 is None:
                    break
                k4 = unit_vec(p + sign * step * k3)
                if k4 is None:
                    break
                p = p + sign * step * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            if len(pts) > 20:
                lines.append(np.array(pts))
    return lines


def trace_field_lines_oneway(
    rho: np.ndarray,
    theta: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
    seeds: list[tuple[float, float]],
    step: float = 0.045,
    n_steps: int = 2600,
) -> list[np.ndarray]:
    """Integrate field lines forward from seeds in native (rho, theta)."""

    interp_er = RegularGridInterpolator(
        (theta, rho), e_rho, bounds_error=False, fill_value=np.nan
    )
    interp_et = RegularGridInterpolator(
        (theta, rho), e_theta, bounds_error=False, fill_value=np.nan
    )

    def unit_vec(point: np.ndarray) -> np.ndarray | None:
        th, rr = point
        vec = np.array([interp_et((th, rr)), interp_er((th, rr))], dtype=float)
        if not np.all(np.isfinite(vec)):
            return None
        scale = math.hypot(vec[0], vec[1])
        if scale < 1e-11:
            return None
        return vec / scale

    lines: list[np.ndarray] = []
    for rr0, th0 in seeds:
        pts = []
        p = np.array([th0, rr0], dtype=float)
        for _ in range(n_steps):
            if not (rho[3] < p[1] < rho[-4] and theta[2] < p[0] < theta[-3]):
                break
            pts.append([p[1], p[0]])
            k1 = unit_vec(p)
            if k1 is None:
                break
            k2 = unit_vec(p + 0.5 * step * k1)
            if k2 is None:
                break
            k3 = unit_vec(p + 0.5 * step * k2)
            if k3 is None:
                break
            k4 = unit_vec(p + step * k3)
            if k4 is None:
                break
            p = p + step * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        if len(pts) > 8:
            lines.append(np.array(pts))
    return lines


def make_figure(
    rho: np.ndarray,
    theta: np.ndarray,
    pot_fixed: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
) -> None:
    fig, ax = plt.subplots(figsize=(8.2, 5.2), constrained_layout=True)

    # Conformal meridional map.  With u=asinh(rho/a), the Ellis meridional
    # metric is a^2 cosh(u)^2 (du^2+dtheta^2).  Mapping s=exp(u) to polar
    # coordinates is conformal and sends the throat u=0 to the unit circle.
    rr, tt = np.meshgrid(rho, theta)
    uu = np.arcsinh(rr / A_THROAT)
    ss = np.exp(uu)
    xx = ss * np.cos(tt)
    yy = ss * np.sin(tt)
    masked = np.ma.masked_where(
        (rr - RHO0) ** 2 + ((np.sqrt(RHO0**2 + A_THROAT**2)) * tt) ** 2 < 0.10**2,
        pot_fixed,
    )
    levels = np.linspace(
        np.percentile(masked.compressed(), 5),
        np.percentile(masked.compressed(), 95),
        34,
    )
    tri = mtri.Triangulation(xx.ravel(), yy.ravel())
    point_mask = np.ma.getmaskarray(masked).ravel()
    tri.set_mask(np.any(point_mask[tri.triangles], axis=1))
    for sign in (1.0, -1.0):
        tri_plot = mtri.Triangulation(xx.ravel(), (sign * yy).ravel())
        tri_plot.set_mask(np.any(point_mask[tri_plot.triangles], axis=1))
        ax.tricontour(
            tri_plot,
            pot_fixed.ravel(),
            levels=levels,
            colors="#8a8f98",
            linewidths=0.55,
            alpha=0.54,
        )

    seeds: list[tuple[float, float]] = []
    for th in np.linspace(0.08, 1.05, 9):
        seeds.append((RHO0 + 0.055 * math.cos(th), 0.055 * math.sin(th)))
    # Seeds on both sides of the throat expose the zero-net-flux pattern:
    # some field lines cross one way and others cross back.
    for th in np.linspace(0.24, math.pi - 0.24, 13):
        seeds.append((0.035, th))
        seeds.append((-0.035, th))
    for line in trace_field_lines(rho, theta, e_rho, e_theta, seeds):
        line_r = line[:, 0]
        line_t = line[:, 1]
        line_s = np.exp(np.arcsinh(line_r / A_THROAT))
        line_x = line_s * np.cos(line_t)
        line_y = line_s * np.sin(line_t)
        ax.plot(line_x, line_y, color="#1f5f8b", lw=0.95, alpha=0.86)
        ax.plot(line_x, -line_y, color="#1f5f8b", lw=0.95, alpha=0.60)

    throat_ang = np.linspace(0.0, 2.0 * math.pi, 600)
    ax.plot(np.cos(throat_ang), np.sin(throat_ang), color="#111827", lw=2.6, alpha=0.9)
    source_s = math.exp(math.asinh(RHO0 / A_THROAT))
    ax.scatter([source_s], [0.0], s=70, color="#b42318", zorder=5)
    ax.annotate(
        "$q$",
        (source_s, 0.0),
        xytext=(8, 8),
        textcoords="offset points",
        color="#8b1a10",
        fontsize=13,
    )
    ax.text(-0.52, 1.16, "throat $S^2$", fontsize=10, color="#111827")
    ax.text(-0.42, -0.08, "opposite\nend", fontsize=9, color="#374151", ha="center", va="center")
    ax.text(5.95, -2.1, "source end", fontsize=10, color="#374151")

    ax.set_xlim(-2.4, 8.0)
    ax.set_ylim(-2.8, 2.8)
    ax.set_xlabel("conformal meridional coordinate")
    ax.set_ylabel("conformal meridional coordinate")
    ax.set_title("Ellis wormhole, fixed zero-flux sector", fontsize=12)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color="#e5e7eb", lw=0.6, alpha=0.8)
    fig.savefig(OUT_PNG, dpi=260)
    fig.savefig(OUT_PDF)


def make_native_figure(
    rho: np.ndarray,
    theta: np.ndarray,
    pot_fixed: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
) -> None:
    fig, ax = plt.subplots(figsize=(8.0, 4.6), constrained_layout=True)

    rr, tt = np.meshgrid(rho, theta)
    charge_mask = (rr - RHO0) ** 2 + (np.sqrt(RHO0**2 + A_THROAT**2) * tt) ** 2 < 0.13**2
    potential = np.ma.masked_where(charge_mask, pot_fixed)
    levels = np.linspace(
        np.percentile(potential.compressed(), 6),
        np.percentile(potential.compressed(), 94),
        30,
    )
    ax.contour(rho, theta, potential, levels=levels, colors="#a8adb5", linewidths=0.65, alpha=0.7)

    # Axisymmetric Maxwell stream function.  Its contours are flux tubes in
    # the meridional plane and are much less arbitrary than seeded ODE traces.
    r2 = rho[None, :] ** 2 + A_THROAT**2
    integrand = r2 * np.sin(theta)[:, None] * e_rho
    dtheta = theta[1] - theta[0]
    psi = np.zeros_like(integrand)
    psi[1:, :] = np.cumsum(0.5 * (integrand[:-1, :] + integrand[1:, :]) * dtheta, axis=0)
    psi = np.ma.masked_where(charge_mask, psi)
    psi_vals = psi.compressed()
    # Use symmetric flux levels; exclude the near-singular tails.
    psi_lim = np.percentile(np.abs(psi_vals), 88)
    psi_levels = np.r_[
        np.linspace(-psi_lim, -0.08 * psi_lim, 8),
        np.linspace(0.08 * psi_lim, psi_lim, 8),
    ]
    ax.contour(
        rho,
        theta,
        psi,
        levels=psi_levels,
        colors="#1f5f8b",
        linewidths=1.05,
        alpha=0.9,
        linestyles="solid",
    )

    ax.axvline(0.0, color="#111827", lw=2.0)
    ax.scatter([RHO0], [0.0], s=76, color="#b42318", zorder=6, clip_on=False)
    ax.text(RHO0 + 0.16, 0.12, "$q$", color="#8b1a10", fontsize=14)
    ax.text(0.08, 2.92, "throat $S^2$ ($\\rho=0$)", fontsize=10, color="#111827")
    ax.text(-7.5, 0.18, "opposite end", fontsize=10, color="#374151")
    ax.text(5.7, 0.18, "source end", fontsize=10, color="#374151")

    ax.set_xlim(-8.0, 8.0)
    ax.set_ylim(0.0, math.pi)
    ax.set_xlabel("$\\rho/a$")
    ax.set_ylabel("$\\theta$")
    ax.set_yticks([0, math.pi / 2, math.pi])
    ax.set_yticklabels(["0", "$\\pi/2$", "$\\pi$"])
    ax.set_title("Ellis fixed zero-flux sector: native meridional chart", fontsize=12)
    ax.grid(color="#e5e7eb", lw=0.6, alpha=0.8)
    fig.savefig(OUT_NATIVE_PNG, dpi=260)
    fig.savefig(OUT_NATIVE_PDF)


def _side_triangulation(
    rho_side: np.ndarray,
    theta_side: np.ndarray,
    values: np.ndarray,
    offset_x: float,
    stride_rho: int = 4,
    stride_theta: int = 3,
) -> tuple[mtri.Triangulation, np.ndarray]:
    rr, tt = np.meshgrid(rho_side[::stride_rho], theta_side[::stride_theta])
    vals = values[::stride_theta, ::stride_rho]
    areal = np.sqrt(rr**2 + A_THROAT**2)
    x = areal * np.sin(tt)
    y = areal * np.cos(tt)

    x_full = np.concatenate([offset_x + x.ravel(), offset_x - x.ravel()])
    y_full = np.concatenate([y.ravel(), y.ravel()])
    v_full = np.concatenate([vals.ravel(), vals.ravel()])
    tri = mtri.Triangulation(x_full, y_full)
    return tri, v_full


def make_areal_two_panel_figure(
    rho: np.ndarray,
    theta: np.ndarray,
    pot_fixed: np.ndarray,
    e_rho: np.ndarray,
) -> None:
    """A readable two-end rendering using areal-radius meridional planes.

    Each end is shown in its own polar/Cartesian plane with
    r_areal=sqrt(rho^2+a^2).  This makes each throat appear as a circle.
    The radial scale is a visualization coordinate, not the proper radial
    distance of the Ellis metric.
    """

    r2 = rho[None, :] ** 2 + A_THROAT**2
    integrand = r2 * np.sin(theta)[:, None] * e_rho
    dtheta = theta[1] - theta[0]
    psi = np.zeros_like(integrand)
    psi[1:, :] = np.cumsum(0.5 * (integrand[:-1, :] + integrand[1:, :]) * dtheta, axis=0)

    pos = rho >= 0
    neg = rho <= 0
    rho_pos = rho[pos]
    rho_neg = -rho[neg][::-1]
    pot_pos = pot_fixed[:, pos]
    pot_neg = pot_fixed[:, neg][:, ::-1]
    psi_pos = psi[:, pos]
    psi_neg = psi[:, neg][:, ::-1]

    fig, axes = plt.subplots(1, 2, figsize=(9.0, 4.4), constrained_layout=True)
    specs = [
        (axes[0], rho_neg, pot_neg, psi_neg, "opposite end", False),
        (axes[1], rho_pos, pot_pos, psi_pos, "source end", True),
    ]
    for ax, rho_side, pot_side, psi_side, title, has_charge in specs:
        tri_p, val_p = _side_triangulation(rho_side, theta, pot_side, 0.0)
        p_lo, p_hi = np.percentile(val_p, [7, 93])
        ax.tricontour(
            tri_p,
            val_p,
            levels=np.linspace(p_lo, p_hi, 24),
            colors="#a8adb5",
            linewidths=0.55,
            alpha=0.62,
        )

        tri_s, val_s = _side_triangulation(rho_side, theta, psi_side, 0.0)
        lim = np.percentile(np.abs(val_s), 86)
        levels = np.r_[np.linspace(-lim, -0.12 * lim, 7), np.linspace(0.12 * lim, lim, 7)]
        ax.tricontour(
            tri_s,
            val_s,
            levels=levels,
            colors="#1f5f8b",
            linewidths=0.95,
            alpha=0.88,
            linestyles="solid",
        )

        throat = plt.Circle((0.0, 0.0), A_THROAT, fill=False, lw=2.6, color="#111827")
        ax.add_patch(throat)
        if has_charge:
            q_r = math.sqrt(RHO0**2 + A_THROAT**2)
            ax.scatter([0.0], [q_r], s=72, color="#b42318", zorder=8)
            ax.text(0.13, q_r + 0.12, "$q$", color="#8b1a10", fontsize=14)
        ax.text(0.0, -3.55, title, ha="center", va="center", fontsize=11, color="#374151")
        ax.text(0.0, 1.18, "throat", ha="center", va="bottom", fontsize=9, color="#111827")
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-3.55, 3.55)
        ax.set_ylim(-3.85, 3.85)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

    fig.suptitle("Ellis fixed zero-flux sector: areal-radius rendering", fontsize=13)
    fig.savefig(OUT_AREAL_PNG, dpi=260)
    fig.savefig(OUT_AREAL_PDF)


def make_areal_clean_figure(
    rho: np.ndarray,
    theta: np.ndarray,
    pot_fixed: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
) -> None:
    pos = rho >= 0
    neg = rho <= 0
    rho_pos = rho[pos]
    rho_neg = -rho[neg][::-1]
    pot_pos = pot_fixed[:, pos]
    pot_neg = pot_fixed[:, neg][:, ::-1]
    er_pos = e_rho[:, pos]
    er_neg = -e_rho[:, neg][:, ::-1]
    et_pos = e_theta[:, pos]
    et_neg = e_theta[:, neg][:, ::-1]

    r0 = math.sqrt(RHO0**2 + A_THROAT**2)
    seed_radius_native = 0.16
    seed_angles = np.linspace(0.10, 2.0 * math.pi - 0.10, 22)
    seeds: list[tuple[float, float]] = []
    for alpha in seed_angles:
        rr0 = RHO0 + seed_radius_native * math.cos(alpha)
        th0 = max(theta[2], abs(seed_radius_native * math.sin(alpha)) / r0)
        seeds.append((rr0, th0))
    charge_lines = trace_field_lines_oneway(rho, theta, e_rho, e_theta, seeds)
    throat_seeds = [(0.03, th) for th in (0.62, 1.05, 2.09, 2.52)]
    throat_lines = trace_field_lines(
        rho,
        theta,
        e_rho,
        e_theta,
        throat_seeds,
        step=0.045,
        n_steps=1200,
    )

    fig, axes = plt.subplots(1, 2, figsize=(8.7, 4.2), constrained_layout=True)
    specs = [
        (axes[0], rho_neg, pot_neg, er_neg, et_neg, "opposite end", False),
        (axes[1], rho_pos, pot_pos, er_pos, et_pos, "source end", True),
    ]
    grid = np.linspace(-3.45, 3.45, 360)
    xx, yy = np.meshgrid(grid, grid)
    rad = np.sqrt(xx**2 + yy**2)
    th_grid = np.arccos(np.clip(yy / np.maximum(rad, 1e-12), -1.0, 1.0))
    rho_grid = np.sqrt(np.maximum(rad**2 - A_THROAT**2, 0.0))
    outside = rad >= A_THROAT

    for ax, rho_side, pot_side, er_side, et_side, title, has_charge in specs:
        interp_p = RegularGridInterpolator(
            (theta, rho_side), pot_side, bounds_error=False, fill_value=np.nan
        )
        p_grid_raw = interp_p((th_grid, rho_grid))
        finite = outside & np.isfinite(p_grid_raw)
        if has_charge:
            q_r = math.sqrt(RHO0**2 + A_THROAT**2)
            finite &= (xx**2 + (yy - q_r) ** 2) > 0.92**2
        fill_value = np.nanmedian(p_grid_raw[finite])
        filled = np.where(finite, p_grid_raw, fill_value)
        p_smooth = gaussian_filter(filled, sigma=2.1)
        p_grid = np.ma.masked_where(~finite, p_smooth)
        p_lo, p_hi = np.percentile(p_grid.compressed(), [12, 80 if has_charge else 88])
        ax.contour(
            xx,
            yy,
            p_grid,
            levels=np.linspace(p_lo, p_hi, 18),
            colors="#9aa1aa",
            linewidths=0.62,
            alpha=0.58,
        )

        ax.add_patch(plt.Circle((0.0, 0.0), A_THROAT, fill=False, lw=2.7, color="#111827"))
        ax.text(0.0, 1.18, "throat", ha="center", va="bottom", fontsize=9, color="#111827")

        dp_dy, dp_dx = np.gradient(p_smooth, grid, grid)
        gx = -dp_dx
        gy = -dp_dy
        gx = np.where(finite, gx, 0.0)
        gy = np.where(finite, gy, 0.0)
        gnorm = np.hypot(gx, gy)
        gx = np.divide(gx, gnorm, out=np.zeros_like(gx), where=gnorm > 1e-11)
        gy = np.divide(gy, gnorm, out=np.zeros_like(gy), where=gnorm > 1e-11)

        for line_family, line_alpha, line_width in (
            (charge_lines, 0.88, 0.92),
            (throat_lines, 0.58, 0.78),
        ):
            for line in line_family:
                rr_line = line[:, 0]
                th_line = line[:, 1]
                if has_charge:
                    mask = rr_line >= 0.0
                    rr_side = rr_line[mask]
                    th_side = th_line[mask]
                else:
                    mask = rr_line <= 0.0
                    rr_side = -rr_line[mask]
                    th_side = th_line[mask]
                if rr_side.size < 2:
                    continue
                breaks = np.where(np.diff(np.flatnonzero(mask)) > 1)[0] + 1
                rr_segments = np.split(rr_side, breaks)
                th_segments = np.split(th_side, breaks)
                for rr_seg, th_seg in zip(rr_segments, th_segments):
                    if rr_seg.size < 2:
                        continue
                    areal = np.sqrt(rr_seg**2 + A_THROAT**2)
                    x_seg = areal * np.sin(th_seg)
                    y_seg = areal * np.cos(th_seg)
                    for mirror in (-1.0, 1.0):
                        ax.plot(
                            mirror * x_seg,
                            y_seg,
                            color="#1f5f8b",
                            lw=line_width,
                            alpha=line_alpha,
                            zorder=5,
                        )
        interp_gx = RegularGridInterpolator(
            (grid, grid), -dp_dx, bounds_error=False, fill_value=np.nan
        )
        interp_gy = RegularGridInterpolator(
            (grid, grid), -dp_dy, bounds_error=False, fill_value=np.nan
        )
        arrow_thetas = np.linspace(0.34, math.pi - 0.34, 11)
        for th in arrow_thetas:
            for mirror in (-1.0, 1.0):
                # Put arrows just outside the throat and orient them normal to
                # the displayed equipotential contours.
                r_eval = 1.14
                x0 = mirror * r_eval * math.sin(th)
                y0 = r_eval * math.cos(th)
                ex = float(interp_gx((y0, x0)))
                ey = float(interp_gy((y0, x0)))
                norm = math.hypot(ex, ey)
                if not np.isfinite(norm) or norm < 1e-12:
                    continue
                ex /= norm
                ey /= norm
                length = 0.23
                ax.arrow(
                    x0 - 0.5 * length * ex,
                    y0 - 0.5 * length * ey,
                    length * ex,
                    length * ey,
                    width=0.007,
                    head_width=0.05,
                    head_length=0.06,
                    color="#1f5f8b",
                    alpha=0.85,
                    length_includes_head=True,
                    zorder=6,
                )

        if has_charge:
            q_r = math.sqrt(RHO0**2 + A_THROAT**2)
            ax.scatter([0.0], [q_r], s=74, color="#b42318", zorder=8)
            ax.text(0.14, q_r + 0.1, "$q$", color="#8b1a10", fontsize=14)

        ax.text(0.0, -3.45, title, ha="center", va="center", fontsize=11, color="#374151")
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlim(-3.35, 3.35)
        ax.set_ylim(-3.7, 3.7)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

    fig.suptitle("Ellis fixed zero-flux sector: equipotentials and throat flux density", fontsize=13)
    fig.savefig(OUT_AREAL_CLEAN_PNG, dpi=260)
    fig.savefig(OUT_AREAL_CLEAN_PDF)


def main() -> None:
    rho = np.linspace(-RHO_MAX, RHO_MAX, N_RHO)
    theta = np.linspace(1.0e-3, math.pi - 1.0e-3, N_THETA)

    modes = solve_radial_modes(rho, RHO0, L_MAX)
    pot_kb, pot_fixed, corr = build_potential(rho, theta, modes)
    e_rho, e_theta = field_components(rho, theta, pot_fixed)
    _, pot_plot, _ = build_potential(
        rho, theta, modes, spectral_filter=plot_spectral_filter(L_MAX)
    )
    e_plot_rho, e_plot_theta = field_components(rho, theta, pot_plot)

    c_far = 0.5 - math.atan(RHO0 / A_THROAT) / math.pi
    f_kb = -CHARGE**2 * A_THROAT * RHO0 / (
        math.pi * (RHO0**2 + A_THROAT**2) ** 2
    )
    f_corr = CHARGE**2 / (RHO0**2 + A_THROAT**2) * c_far
    f_fixed = f_kb + f_corr

    # l=0 flux coefficient p dA/drho in the rho<rho0 vacuum region.  It should
    # be c_far for the KB Green function and zero after the correction.
    idx0 = int(np.argmin(np.abs(rho)))
    drho = rho[1] - rho[0]
    sin_th = np.sin(theta)
    norm = np.trapezoid(sin_th, theta)
    avg_kb = np.trapezoid(pot_kb * sin_th[:, None], theta, axis=0) / norm
    avg_fixed = np.trapezoid(pot_fixed * sin_th[:, None], theta, axis=0) / norm
    flux_coeff_kb = (rho[idx0] ** 2 + A_THROAT**2) * np.gradient(avg_kb, drho)[idx0]
    flux_coeff_fixed = (rho[idx0] ** 2 + A_THROAT**2) * np.gradient(avg_fixed, drho)[idx0]

    print(f"rho0/a = {RHO0 / A_THROAT:.3f}")
    print(f"L_MAX = {L_MAX}, N_RHO = {N_RHO}, RHO_MAX/a = {RHO_MAX / A_THROAT:.1f}")
    print(f"KB opposite-end charge fraction c = {c_far:.8f}")
    print(f"throat l=0 flux coefficient before correction = {flux_coeff_kb:.8e}")
    print(f"throat l=0 flux coefficient after correction  = {flux_coeff_fixed:.8e}")
    print(f"KB self-force/a units      = {f_kb:.8e}")
    print(f"correction self-force      = {f_corr:.8e}")
    print(f"fixed-sector self-force    = {f_fixed:.8e}")

    # The conformal-circle rendering is useful as a diagnostic, but it tends
    # to be visually misleading for a paper figure.  The native chart below is
    # the default output.
    # make_figure(rho, theta, pot_fixed, e_rho, e_theta)
    # make_native_figure(rho, theta, pot_plot, e_plot_rho, e_plot_theta)
    # make_areal_two_panel_figure(rho, theta, pot_plot, e_plot_rho)
    make_areal_clean_figure(rho, theta, pot_plot, e_plot_rho, e_plot_theta)
    print(f"wrote {OUT_AREAL_CLEAN_PNG}")
    print(f"wrote {OUT_AREAL_CLEAN_PDF}")


if __name__ == "__main__":
    main()
