#!/usr/bin/env python3
"""Zero-Wheeler-flux field lines for a flat spherical thin-shell wormhole.

Geometry: two copies of Euclidean exterior r >= a glued at r=a.  A point
charge q sits on the source-side axis at r=r0.  The l=0 Wheeler-flux sector is
set to zero, so only l>=1 throat-polarization modes are included in the
source-side correction and the opposite-side field.

Field lines are contours of the axisymmetric stream function Psi.  Each panel
is an ordinary Euclidean meridional slice of one exterior region.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from scipy.special import eval_legendre


A = 1.0
Q = 1.0
R0 = 2.0
R_MAX = 6.0
N_R = 700
N_THETA = 421
L_MAX = 80

OUT_PNG = Path("fig_thinshell_zero_flux_field.png")
OUT_PDF = Path("fig_thinshell_zero_flux_field.pdf")


def integral_sin_pl(ell: int, mu: np.ndarray) -> np.ndarray:
    """I_l(theta)=int_0^theta sin(t) P_l(cos t) dt."""
    if ell == 0:
        return 1.0 - mu
    return (eval_legendre(ell - 1, mu) - eval_legendre(ell + 1, mu)) / (2 * ell + 1)


def build_stream_functions(r: np.ndarray, theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return source-side and opposite-side stream functions."""
    mu = np.cos(theta)
    rr, tt = np.meshgrid(r, theta)
    cyl_r = rr * np.sin(tt)
    z = rr * np.cos(tt)
    dist_q = np.sqrt(cyl_r * cyl_r + (z - R0) ** 2)
    # Exact Coulomb stream function for a point charge on the symmetry axis:
    # Psi=q(1-cos theta_q), where theta_q is measured from the charge.
    psi_src = Q * (1.0 - (z - R0) / dist_q)
    psi_opp = np.zeros((theta.size, r.size), dtype=float)

    # Correction/image coefficients for zero Wheeler flux.
    # Source side: A_l r^{-l-1}; opposite side: B_l r^{-l-1}.
    # A_l = -q a^{2l+1}/[2(l+1) r0^{l+1}]
    # B_l = +(2l+1) q a^{2l+1}/[2(l+1) r0^{l+1}]
    for ell in range(1, L_MAX + 1):
        I = integral_sin_pl(ell, mu)[:, None]
        Aell = -Q * A ** (2 * ell + 1) / (2 * (ell + 1) * R0 ** (ell + 1))
        Bell = (2 * ell + 1) * Q * A ** (2 * ell + 1) / (
            2 * (ell + 1) * R0 ** (ell + 1)
        )
        # For V=C r^{-l-1} P_l, E_r=(l+1) C r^{-l-2} P_l and
        # Psi=(l+1) C r^{-l} I_l.
        psi_src += (ell + 1) * Aell * (r[None, :] ** (-ell)) * I
        psi_opp += (ell + 1) * Bell * (r[None, :] ** (-ell)) * I

    return psi_src, psi_opp


def triangulate_panel(
    r: np.ndarray, theta: np.ndarray, psi: np.ndarray, has_charge: bool
) -> tuple[mtri.Triangulation, np.ndarray]:
    rr, tt = np.meshgrid(r, theta)
    x = rr * np.sin(tt)
    y = rr * np.cos(tt)

    mask = rr < A * 1.002
    if has_charge:
        mask |= (x * x + (y - R0) ** 2) < 0.10**2

    x_full = np.concatenate([x.ravel(), -x.ravel()])
    y_full = np.concatenate([y.ravel(), y.ravel()])
    psi_full = np.concatenate([psi.ravel(), psi.ravel()])
    mask_full = np.concatenate([mask.ravel(), mask.ravel()])

    tri = mtri.Triangulation(x_full, y_full)
    triangles = tri.triangles
    tx = x_full[triangles]
    ty = y_full[triangles]
    max_edge = np.maximum.reduce(
        [
            np.hypot(tx[:, 0] - tx[:, 1], ty[:, 0] - ty[:, 1]),
            np.hypot(tx[:, 1] - tx[:, 2], ty[:, 1] - ty[:, 2]),
            np.hypot(tx[:, 2] - tx[:, 0], ty[:, 2] - ty[:, 0]),
        ]
    )
    tri.set_mask(np.any(mask_full[triangles], axis=1) | (max_edge > 0.40))
    return tri, psi_full


def draw_panel(
    ax,
    r: np.ndarray,
    theta: np.ndarray,
    psi: np.ndarray,
    levels: np.ndarray,
    extra_levels: np.ndarray | None,
    title: str,
    has_charge: bool,
) -> None:
    tri, psi_full = triangulate_panel(r, theta, psi, has_charge)
    ax.tricontour(
        tri,
        psi_full,
        levels=levels,
        colors="#1f5f8b",
        linewidths=1.2,
        linestyles="solid",
    )
    if extra_levels is not None and extra_levels.size:
        ax.tricontour(
            tri,
            psi_full,
            levels=extra_levels,
            colors="#1f5f8b",
            linewidths=1.0,
            alpha=0.55,
            linestyles="solid",
        )
    ax.add_patch(plt.Circle((0, 0), A, fill=False, lw=2.5, color="#111827", zorder=6))
    ax.text(0, -1.17, "throat", ha="center", va="top", fontsize=10)
    if has_charge:
        ax.scatter([0], [R0], s=72, color="#b42318", zorder=7)
        ax.text(0.12, R0 + 0.08, "$q$", fontsize=14, color="#8b1a10")
    ax.text(0, -4.9, title, ha="center", va="center", fontsize=11, color="#374151")
    ax.set_aspect("equal")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-5.2, 5.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


def main() -> None:
    r = np.linspace(A, R_MAX, N_R)
    theta = np.linspace(1.0e-4, math.pi - 1.0e-4, N_THETA)
    psi_src, psi_opp = build_stream_functions(r, theta)

    # Use the opposite-side range to define crossing flux-tube levels.  These
    # same levels are drawn on both ends.
    pmin = max(1.0e-4, float(np.percentile(psi_opp, 1.0)))
    pmax = float(np.percentile(psi_opp, 99.2))

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.5), constrained_layout=True)
    # Choose every displayed source-side line by its launch angle at the
    # charge.  For a point charge, Psi_q=q(1-cos alpha), where alpha is the
    # local angle measured from the upward symmetry axis through the charge.
    # Using alpha=k*pi/32 gives visually uniform angular spacing at q.
    ray_angles = np.arange(1, 32, dtype=float) * math.pi / 32.0
    source_angle_levels = Q * (1.0 - np.cos(ray_angles))

    # With the stream-function gauges used here, matching flux tubes satisfy
    # Psi_source + Psi_opposite = 2q on the throat.  Only the downward cone
    # whose mapped opposite-side levels fit in the opposite-end range crosses
    # the throat; the rest go to source-side infinity.
    opposite_from_source = 2.0 * Q - source_angle_levels
    crosses = (opposite_from_source >= pmin) & (opposite_from_source <= pmax)
    levels = np.sort(opposite_from_source[crosses])
    source_crossing_levels = source_angle_levels[crosses]
    source_to_infinity_levels = source_angle_levels[~crosses]

    draw_panel(axes[0], r, theta, psi_opp, levels, None, "opposite end", False)
    draw_panel(
        axes[1],
        r,
        theta,
        psi_src,
        source_crossing_levels,
        source_to_infinity_levels,
        "source end",
        True,
    )
    fig.suptitle("Flat thin-shell wormhole: zero Wheeler-flux field lines", fontsize=13)
    fig.savefig(OUT_PNG, dpi=260)
    fig.savefig(OUT_PDF)

    # Numerical checks: zero l=0 sector and known fixed-flux force.
    f_fixed = -Q * Q * A**3 / (2 * R0**3 * (R0 * R0 - A * A))
    print(f"R0/a = {R0 / A:.3f}, L_MAX={L_MAX}")
    print(f"fixed-zero-flux self-force = {f_fixed:+.8e}")
    print(f"opposite stream level range = [{levels[0]:+.4e}, {levels[-1]:+.4e}]")
    print(f"source launch angles crossing throat = {np.sum(crosses)} of {ray_angles.size}")
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
