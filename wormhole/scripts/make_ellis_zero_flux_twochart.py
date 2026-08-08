#!/usr/bin/env python3
"""Two-chart areal rendering of zero-flux Ellis electrostatic field lines.

This figure is meant for interpretation rather than for solving anything new:
the potential is the same fixed-Q_wh=0 Ellis mode sum used in
make_ellis_fixed_sector_clean.py.  Field lines are contours of the
axisymmetric Maxwell stream function, not ODE-integrated streamlines.

Each panel is a separate areal-radius chart for one asymptotic end.  A curve
that reaches the throat circle in one panel continues from the corresponding
point of the throat circle in the other panel.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

import make_ellis_fixed_sector_clean as ellis


RHO0_PLOT = 1.0
RHO_MAX_PLOT = 8.0
N_RHO_PLOT = 1601
N_THETA_PLOT = 501
L_MAX_PLOT = 110

OUT_PNG = Path("fig_ellis_zero_flux_twochart.png")
OUT_PDF = Path("fig_ellis_zero_flux_twochart.pdf")
OUT_NATIVE_PNG = Path("fig_ellis_zero_flux_native.png")
OUT_NATIVE_PDF = Path("fig_ellis_zero_flux_native.pdf")
OUT_CONFORMAL_PNG = Path("fig_ellis_zero_flux_conformal.png")
OUT_CONFORMAL_PDF = Path("fig_ellis_zero_flux_conformal.pdf")


def triangulated_end(
    rho_side: np.ndarray,
    theta: np.ndarray,
    psi_side: np.ndarray,
    has_charge: bool,
) -> tuple[mtri.Triangulation, np.ndarray, np.ndarray, np.ndarray]:
    rr, tt = np.meshgrid(rho_side, theta)
    r_areal = np.sqrt(rr * rr + ellis.A_THROAT**2)
    x = r_areal * np.sin(tt)
    y = r_areal * np.cos(tt)

    mask = np.zeros_like(x, dtype=bool)
    if has_charge:
        q_y = math.sqrt(RHO0_PLOT**2 + ellis.A_THROAT**2)
        mask = (x * x + (y - q_y) ** 2) < 0.18**2

    x_full = np.concatenate([x.ravel(), -x.ravel()])
    y_full = np.concatenate([y.ravel(), y.ravel()])
    psi_full = np.concatenate([psi_side.ravel(), psi_side.ravel()])
    mask_full = np.concatenate([mask.ravel(), mask.ravel()])

    tri = mtri.Triangulation(x_full, y_full)
    triangles = tri.triangles
    tri_x = x_full[triangles]
    tri_y = y_full[triangles]
    centroid_r = np.sqrt(np.mean(tri_x, axis=1) ** 2 + np.mean(tri_y, axis=1) ** 2)
    edges = [
        np.hypot(tri_x[:, 0] - tri_x[:, 1], tri_y[:, 0] - tri_y[:, 1]),
        np.hypot(tri_x[:, 1] - tri_x[:, 2], tri_y[:, 1] - tri_y[:, 2]),
        np.hypot(tri_x[:, 2] - tri_x[:, 0], tri_y[:, 2] - tri_y[:, 0]),
    ]
    max_edge = np.maximum.reduce(edges)
    hole_mask = centroid_r < 1.02 * ellis.A_THROAT
    long_edge_mask = max_edge > 0.55
    tri.set_mask(np.any(mask_full[triangles], axis=1) | hole_mask | long_edge_mask)
    return tri, x_full, y_full, psi_full


def draw_end(
    ax,
    rho_side: np.ndarray,
    theta: np.ndarray,
    psi_side: np.ndarray,
    title: str,
    has_charge: bool,
    crossing_levels: np.ndarray,
    source_levels: np.ndarray,
) -> None:
    tri, _, _, psi_full = triangulated_end(rho_side, theta, psi_side, has_charge)

    # Flux tubes that cross the throat.  The same levels are used on both ends.
    ax.tricontour(
        tri,
        psi_full,
        levels=crossing_levels,
        colors="#1f5f8b",
        linewidths=1.35,
        alpha=0.95,
        linestyles="solid",
    )

    # Ordinary source-end flux tubes going from q to source-side infinity.
    # These levels simply do not occur on the opposite end.
    if has_charge:
        ax.tricontour(
            tri,
            psi_full,
            levels=source_levels,
            colors="#1f5f8b",
            linewidths=1.15,
            alpha=0.80,
            linestyles="solid",
        )

    throat = plt.Circle(
        (0.0, 0.0),
        ellis.A_THROAT,
        fill=False,
        lw=2.3,
        color="#111827",
        zorder=6,
    )
    ax.add_patch(throat)
    ax.text(0.0, -1.18, "throat", ha="center", va="top", fontsize=10)

    if has_charge:
        q_y = math.sqrt(RHO0_PLOT**2 + ellis.A_THROAT**2)
        ax.scatter([0.0], [q_y], s=78, color="#b42318", zorder=7)
        ax.text(0.15, q_y + 0.09, "$q$", color="#8b1a10", fontsize=14)

    ax.text(0.0, -3.25, title, ha="center", va="center", fontsize=11, color="#374151")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-3.05, 3.05)
    ax.set_ylim(-3.5, 3.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


def main() -> None:
    # make_ellis_fixed_sector_clean.py uses module constants in a few helper
    # functions.  Set them here so the generated field and labels are
    # self-consistent for this visualization.
    old_rho0 = ellis.RHO0
    old_lmax = ellis.L_MAX
    try:
        ellis.RHO0 = RHO0_PLOT
        ellis.L_MAX = L_MAX_PLOT

        rho = np.linspace(-RHO_MAX_PLOT, RHO_MAX_PLOT, N_RHO_PLOT)
        theta = np.linspace(1.0e-3, math.pi - 1.0e-3, N_THETA_PLOT)
        modes = ellis.solve_radial_modes(rho, RHO0_PLOT, L_MAX_PLOT)
        filt = ellis.spectral_filter_array(L_MAX_PLOT)
        psi = ellis.stream_function(rho, theta, modes, filt)

        idx0 = int(np.argmin(np.abs(rho)))
        throat_psi = psi[:, idx0]
        psi_min = float(np.min(throat_psi))

        # Negative stream-function levels cross the throat in this zero-flux
        # configuration.  Positive levels mostly show ordinary flux from the
        # source charge to source-side infinity.
        # Avoid the most external crossing contours: in the areal chart they
        # form large loops close to the charge and read visually as spurious
        # rings.  The remaining levels show the same throat-crossing family
        # without passing through the charge marker.
        crossing_levels = np.linspace(0.72 * psi_min, 0.22 * psi_min, 7)
        source_levels = np.array([0.16, 0.30, 0.48, 0.70, 0.95, 1.20, 1.45, 1.68, 1.84])

        # Native meridional chart: rho is horizontal, theta is vertical.  This
        # is less pictorial, but it shows the throat crossing continuously.
        fig_native, axn = plt.subplots(figsize=(8.6, 4.5), constrained_layout=True)
        axn.axvline(0.0, color="#111827", lw=2.0)
        axn.contour(
            rho,
            theta,
            psi,
            levels=crossing_levels,
            colors="#1f5f8b",
            linewidths=1.2,
            linestyles="solid",
        )
        axn.contour(
            rho,
            theta,
            psi,
            levels=source_levels,
            colors="#1f5f8b",
            linewidths=1.0,
            alpha=0.75,
            linestyles="solid",
        )
        axn.scatter([RHO0_PLOT], [1.0e-3], s=65, color="#b42318", zorder=5)
        axn.text(RHO0_PLOT + 0.12, 0.12, "$q$", color="#8b1a10", fontsize=14)
        axn.text(0.08, math.pi - 0.15, "throat $\\rho=0$", fontsize=10, color="#111827")
        axn.text(-5.4, 0.2, "opposite end", fontsize=11, color="#374151")
        axn.text(3.4, 0.2, "source end", fontsize=11, color="#374151")
        axn.set_xlim(-6.0, 6.0)
        axn.set_ylim(0.0, math.pi)
        axn.set_xlabel(r"Ellis radial coordinate $\rho/a$")
        axn.set_ylabel(r"polar angle $\theta$")
        axn.set_yticks([0, math.pi / 2, math.pi])
        axn.set_yticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
        axn.set_title("Zero-flux Ellis stream-function contours in native coordinates")
        axn.grid(alpha=0.18)
        fig_native.savefig(OUT_NATIVE_PNG, dpi=240)
        fig_native.savefig(OUT_NATIVE_PDF)

        # Conformal meridional chart.  With rho=a sinh u, the Ellis meridional
        # metric is a^2 cosh^2(u)(du^2+dtheta^2), so (u, theta) preserves
        # local angles in the meridional slice.  This is the closest plotted
        # analogue of a hand sketch with the charge on the bottom axis.
        u = np.arcsinh(rho / ellis.A_THROAT)
        uu, tt = np.meshgrid(u, theta)
        u_charge = math.asinh(RHO0_PLOT / ellis.A_THROAT)
        psi_masked = np.ma.array(
            psi,
            mask=(
                (((uu - u_charge) ** 2 + tt**2) < 0.13**2)
                # The point charge sits on the coordinate boundary theta=0.
                # The truncated mode sum can generate a spurious contour ray
                # at u=u_charge; mask a very narrow strip through the source
                # to avoid drawing that singular artifact as a field line.
                | ((np.abs(uu - u_charge) < 0.018) & (tt < 3.05))
            ),
        )

        fig_conf, axc = plt.subplots(figsize=(8.6, 4.9), constrained_layout=True)
        axc.axvline(0.0, color="#111827", lw=1.8)
        axc.contour(
            u,
            theta,
            psi_masked,
            levels=crossing_levels,
            colors="#1f5f8b",
            linewidths=1.25,
            linestyles="solid",
        )
        axc.contour(
            u,
            theta,
            psi_masked,
            levels=source_levels,
            colors="#1f5f8b",
            linewidths=1.05,
            alpha=0.78,
            linestyles="solid",
        )
        axc.scatter([u_charge], [0.0], s=70, color="#b42318", zorder=6)
        axc.text(u_charge + 0.08, 0.10, "$q$", color="#8b1a10", fontsize=14)
        axc.text(0.05, 2.85, "throat $\\rho=0$", fontsize=10, color="#111827")
        axc.text(-2.5, 0.18, "opposite end", fontsize=11, color="#374151")
        axc.text(1.6, 0.18, "source end", fontsize=11, color="#374151")
        axc.set_xlim(-2.9, 2.9)
        axc.set_ylim(0.0, math.pi)
        axc.set_xlabel(r"conformal radial coordinate $u=\operatorname{arsinh}(\rho/a)$")
        axc.set_ylabel(r"polar angle $\theta$")
        axc.set_yticks([0, math.pi / 2, math.pi])
        axc.set_yticklabels([r"$0$", r"$\pi/2$", r"$\pi$"])
        axc.set_title("Zero-flux Ellis stream-function contours in a conformal meridional chart")
        axc.grid(alpha=0.18)
        fig_conf.savefig(OUT_CONFORMAL_PNG, dpi=240)
        fig_conf.savefig(OUT_CONFORMAL_PDF)

        pos = rho >= 0
        neg = rho <= 0
        rho_pos = rho[pos]
        rho_neg = -rho[neg][::-1]
        psi_pos = psi[:, pos]
        psi_neg = psi[:, neg][:, ::-1]

        fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.9), constrained_layout=True)
        draw_end(
            axes[0],
            rho_neg,
            theta,
            psi_neg,
            title="opposite end",
            has_charge=False,
            crossing_levels=crossing_levels,
            source_levels=source_levels,
        )
        draw_end(
            axes[1],
            rho_pos,
            theta,
            psi_pos,
            title="source end",
            has_charge=True,
            crossing_levels=crossing_levels,
            source_levels=source_levels,
        )
        fig.suptitle(
            "Zero-flux Ellis field lines in two areal-radius charts",
            fontsize=13,
        )
        fig.savefig(OUT_PNG, dpi=260)
        fig.savefig(OUT_PDF)

        # Basic sector diagnostics.
        print(f"rho0/a = {RHO0_PLOT:.3f}")
        print(f"throat stream-function min/max = {np.min(throat_psi):+.6e}, {np.max(throat_psi):+.6e}")
        print(f"wrote {OUT_PNG}")
        print(f"wrote {OUT_PDF}")
        print(f"wrote {OUT_NATIVE_PNG}")
        print(f"wrote {OUT_NATIVE_PDF}")
        print(f"wrote {OUT_CONFORMAL_PNG}")
        print(f"wrote {OUT_CONFORMAL_PDF}")
    finally:
        ellis.RHO0 = old_rho0
        ellis.L_MAX = old_lmax


if __name__ == "__main__":
    main()
