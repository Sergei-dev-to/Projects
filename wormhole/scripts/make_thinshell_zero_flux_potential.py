#!/usr/bin/env python3
"""Potential contours for a point charge near a flat thin-shell wormhole.

This is the potential companion to make_thinshell_zero_flux_field.py.  The
sector is fixed zero Wheeler flux: the l=0 field does not pass through the
throat.  Consequently the opposite end carries no monopole electric field, but
its potential is shifted by the constant q/r0.
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
N_R = 520
N_THETA = 361
L_MAX = 80

OUT_PNG = Path("fig_thinshell_zero_flux_potential.png")
OUT_PDF = Path("fig_thinshell_zero_flux_potential.pdf")


def build_potentials(r: np.ndarray, theta: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return source-side and opposite-side scalar potentials."""
    mu = np.cos(theta)
    rr, tt = np.meshgrid(r, theta)
    cyl_r = rr * np.sin(tt)
    z = rr * np.cos(tt)
    dist_q = np.sqrt(cyl_r * cyl_r + (z - R0) ** 2)

    # Source-side Coulomb field, normalized to Phi -> 0 at source-side infinity.
    phi_src = Q / dist_q

    # The l=0 fixed-flux contribution on the opposite side is a constant.  It
    # is the spherical-shell result for a charge at radius R0.
    phi_opp = np.full_like(phi_src, Q / R0)

    # l>=1 throat-polarization modes.  These are the same coefficients used in
    # the zero-flux streamline figure.
    for ell in range(1, L_MAX + 1):
        pell = eval_legendre(ell, mu)[:, None]
        Aell = -Q * A ** (2 * ell + 1) / (2 * (ell + 1) * R0 ** (ell + 1))
        Bell = (2 * ell + 1) * Q * A ** (2 * ell + 1) / (
            2 * (ell + 1) * R0 ** (ell + 1)
        )
        radial = r[None, :] ** (-ell - 1)
        phi_src += Aell * radial * pell
        phi_opp += Bell * radial * pell

    return phi_src, phi_opp


def triangulate_panel(
    r: np.ndarray, theta: np.ndarray, values: np.ndarray, has_charge: bool
) -> tuple[mtri.Triangulation, np.ndarray]:
    rr, tt = np.meshgrid(r, theta)
    x = rr * np.sin(tt)
    y = rr * np.cos(tt)

    mask = rr < A * 1.002
    if has_charge:
        mask |= (x * x + (y - R0) ** 2) < 0.12**2

    x_full = np.concatenate([x.ravel(), -x.ravel()])
    y_full = np.concatenate([y.ravel(), y.ravel()])
    val_full = np.concatenate([values.ravel(), values.ravel()])
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
    return tri, val_full


def draw_panel(
    ax,
    r: np.ndarray,
    theta: np.ndarray,
    phi: np.ndarray,
    title: str,
    has_charge: bool,
    levels: np.ndarray,
    contour_levels: np.ndarray,
):
    tri, vals = triangulate_panel(r, theta, phi, has_charge)
    image = ax.tricontourf(tri, vals, levels=levels, cmap="Greys", extend="max")
    contours = ax.tricontour(
        tri,
        vals,
        levels=contour_levels,
        colors="black",
        linewidths=0.55,
        alpha=0.50,
    )
    ax.clabel(contours, inline=True, fontsize=7, fmt="%.2f")
    ax.add_patch(plt.Circle((0, 0), A, fill=False, lw=2.5, color="#111827", zorder=6))
    ax.text(0, -1.17, "throat", ha="center", va="top", fontsize=10)
    if has_charge:
        ax.scatter([0], [R0], s=72, color="#b42318", zorder=7)
        ax.text(0.13, R0 + 0.10, "$q$", fontsize=14, color="#7f1d1d")
    ax.set_title(title, fontsize=11, pad=8)
    ax.set_aspect("equal")
    ax.set_xlim(-4.5, 4.5)
    ax.set_ylim(-5.25, 5.25)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    return image


def main() -> None:
    r = np.linspace(A, R_MAX, N_R)
    theta = np.linspace(1.0e-4, math.pi - 1.0e-4, N_THETA)
    phi_src, phi_opp = build_potentials(r, theta)

    # Avoid letting the near-charge singularity consume the shared color scale.
    # Keep the far-side offset q/r0=0.50 inside a gray band rather than on a
    # bin edge; otherwise the tiny dipole correction looks like two different
    # asymptotic potentials above and below the equator.
    vmax = 1.625
    levels = np.concatenate(([0.0], np.arange(0.0625, vmax + 0.125, 0.125)))

    fig, axes = plt.subplots(1, 2, figsize=(9.8, 5.4), constrained_layout=True)
    image = draw_panel(
        axes[0],
        r,
        theta,
        phi_opp,
        r"opposite end: $\Phi_\infty \simeq q/r_0$ plus dipole",
        False,
        levels,
        np.array([0.375, 0.625, 0.875, 1.125, 1.375]),
    )
    draw_panel(
        axes[1],
        r,
        theta,
        phi_src,
        r"source end: $\Phi_\infty=0$",
        True,
        levels,
        np.array([0.25, 0.50, 0.75, 1.00, 1.25, 1.50]),
    )
    axes[0].text(
        -4.15,
        4.45,
        r"far infinity: $\Phi\simeq0.50$",
        fontsize=9,
        color="black",
        bbox={"facecolor": "white", "alpha": 0.82, "edgecolor": "none", "pad": 3},
    )
    axes[1].text(
        -4.15,
        4.45,
        r"far infinity: $\Phi\to0$",
        fontsize=9,
        color="black",
        bbox={"facecolor": "white", "alpha": 0.82, "edgecolor": "none", "pad": 3},
    )
    cbar = fig.colorbar(image, ax=axes, shrink=0.82, pad=0.02)
    cbar.set_label(r"potential $\Phi$; source-side infinity sets zero")
    fig.suptitle(
        r"Flat thin-shell wormhole: fixed-flux potential, $q/r_0=0.50$ far-side offset",
        fontsize=12,
    )
    fig.savefig(OUT_PNG, dpi=260)
    fig.savefig(OUT_PDF)

    print(f"far-side mean Phi at R_MAX = {np.mean(phi_opp[:, -1]):.8f}")
    print(f"far-side dipole half-range at R_MAX = {(np.max(phi_opp[:, -1]) - np.min(phi_opp[:, -1])) / 2:.8e}")
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
