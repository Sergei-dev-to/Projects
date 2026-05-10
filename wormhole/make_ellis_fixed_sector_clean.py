#!/usr/bin/env python3
"""
Cleaned-up rendering of the Ellis-wormhole electrostatic field in the
conserved Q_wh = 0 sector.

Physics is identical to make_ellis_fixed_sector_field.py:
  - Khusnutdinov-Bakhmatov radial Green function via spherical-harmonic mode
    sum on the Ellis background ds^2 = d rho^2 + (rho^2 + a^2) dOmega^2.
  - Homogeneous l=0 correction proportional to arctan(rho/a) added to bring
    the throat ell=0 flux to zero.

Rendering changes vs the original:
  - Field lines are contours of the axisymmetric stream function
        psi(rho, theta) = int_0^theta (rho^2 + a^2) sin(theta') E^rho dtheta'.
    Contours of psi are exact integral curves of the field in the meridional
    plane.  No ODE integration, no seeding heuristics, no wobble near the
    point source.
  - No Gaussian smoothing of the potential.  The spectral filter on the
    multipole sum already does anti-aliasing.
  - Throat-flux arrows are evaluated directly from E^rho at rho = 0 (the
    throat) and oriented so that "field exiting source side" and "field
    entering opposite side" point in matching directions (out on source-side
    panel, in on opposite-side panel).
  - The point-charge singularity is masked once with a single circular mask;
    no median-fill / re-differentiate trick.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
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

# Anti-aliasing filter applied to the multipole sum for plotting.
PLOT_FILTER_SCALE = 42.0
PLOT_FILTER_ORDER = 8

# Number of stream-function contours per side, drawn symmetrically about psi=0.
# The actual count is 2 * N_FIELD_LINES (positive and negative levels).
N_FIELD_LINES = 12

# Sampling around the throat circle for the flux-density arrows.
N_THROAT_ARROWS = 30
THROAT_ARROW_MAX_LEN = 0.45

# Source-charge mask radius in areal units (just for the contour plots).
CHARGE_MASK_RADIUS = 0.22

OUT_PNG = Path("fig_ellis_fixed_sector_clean.png")
OUT_PDF = Path("fig_ellis_fixed_sector_clean.pdf")


# ---------------------------------------------------------------------------
# Physics: radial mode solve, multipole sum, l=0 correction.  Unchanged from
# the original script.
# ---------------------------------------------------------------------------

def solve_radial_modes(rho: np.ndarray, rho0: float, l_max: int) -> np.ndarray:
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
    corr = (
        -CHARGE
        * c_far
        / A_THROAT
        * (np.arctan(rho / A_THROAT) - math.pi / 2.0)
    )
    pot_fixed = pot_kb + corr[None, :]
    return pot_kb, pot_fixed, corr


def spectral_filter_array(l_max: int) -> np.ndarray:
    ell = np.arange(l_max + 1, dtype=float)
    filt = np.exp(-((ell / PLOT_FILTER_SCALE) ** PLOT_FILTER_ORDER))
    filt[0] = 1.0
    return filt


def field_components(
    rho: np.ndarray, theta: np.ndarray, potential: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Contravariant components E^rho and E^theta on the (theta, rho) grid."""
    dtheta = theta[1] - theta[0]
    drho = rho[1] - rho[0]
    d_a_drho = np.gradient(potential, drho, axis=1, edge_order=2)
    d_a_dtheta = np.gradient(potential, dtheta, axis=0, edge_order=2)
    r2 = rho[None, :] ** 2 + A_THROAT**2
    e_rho = -d_a_drho
    e_theta = -d_a_dtheta / r2
    return e_rho, e_theta


def stream_function(
    rho: np.ndarray,
    theta: np.ndarray,
    modes: np.ndarray,
    spectral_filter: np.ndarray,
) -> np.ndarray:
    """Axisymmetric stream function via direct multipole sum.

    Each radial mode contributes analytically.  Starting from the multipole
    expansion of the potential

        V(rho, theta) = sum_l q (2l+1) R_l(rho) P_l(cos theta) filter[l],

    the radial field component is E^rho = -dV/drho, and the stream function
    is obtained by integrating (rho^2+a^2) sin theta E^rho in theta.  Using
    the identity P'_{l+1}(u) - P'_{l-1}(u) = (2l+1) P_l(u),

        int_0^theta sin t P_l(cos t) dt
            = (P_{l-1}(cos theta) - P_{l+1}(cos theta)) / (2l+1),

    with the convention P_{-1} := 1, so that l=0 reproduces the standard
    1 - cos theta.  The (2l+1) factors cancel and we get

        psi(rho, theta) = -(rho^2+a^2) q sum_l filter[l] R'_l(rho)
                          * (P_{l-1}(cos theta) - P_{l+1}(cos theta)).

    The Q_wh=0 correction adds an analytic piece to R_0:
        R_0_full = R_0_KB + corr(rho)/q,
        corr(rho) = -q (c_far / a) (arctan(rho/a) - pi/2),
    so its derivative contribution to R'_0 is -c_far / (rho^2 + a^2).

    No numerical integration in theta is performed and no derivative of the
    near-singular potential is taken.  psi is exact (per mode) up to the
    accuracy of the radial-mode solver and the spectral truncation.
    """
    drho = rho[1] - rho[0]
    n_l = modes.shape[0]
    cos_theta = np.cos(theta)
    r2 = rho**2 + A_THROAT**2

    c_far = 0.5 - math.atan(RHO0 / A_THROAT) / math.pi

    R_prime = np.gradient(modes, drho, axis=1, edge_order=2)
    R_prime[0] = R_prime[0] - c_far / r2

    legendre_table = np.empty((n_l + 1, theta.size), dtype=float)
    for ell in range(n_l + 1):
        legendre_table[ell] = eval_legendre(ell, cos_theta)
    p_minus_one = np.ones_like(cos_theta)

    psi = np.zeros((theta.size, rho.size), dtype=float)
    prefactor = -r2[None, :] * CHARGE

    for ell in range(n_l):
        p_low = p_minus_one if ell == 0 else legendre_table[ell - 1]
        p_high = legendre_table[ell + 1]
        angular = (p_low - p_high)[:, None]
        radial = (spectral_filter[ell] * R_prime[ell])[None, :]
        psi += prefactor * radial * angular

    return psi


# ---------------------------------------------------------------------------
# Rendering.
# ---------------------------------------------------------------------------

def draw_streamline_arrows(
    ax,
    rho: np.ndarray,
    theta: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
    panel_side: float,
    n_arrows: int = N_THROAT_ARROWS,
    eps_factor: float = 0.07,
    max_length: float = THROAT_ARROW_MAX_LEN,
) -> None:
    """Draw arrows just outside the throat in the meridional-plane
    visualization, oriented along the local field direction so they match
    the streamlines.

    The Ellis vector (E^rho, E^theta) is pushed forward to the (x_areal,
    y_areal) plane via the chart Jacobian:

        V_x = E^rho (rho/r_areal) sin theta + E^theta r_areal cos theta,
        V_y = E^rho (rho/r_areal) cos theta - E^theta r_areal sin theta,

    evaluated at rho = panel_side * sqrt(r_eval^2 - a^2) with
    r_eval = a (1 + eps_factor) just outside the throat.  Arrow positions
    on the left half-plane are obtained by mirroring x and the x-component
    of the field.

    panel_side = +1 for the source-end panel, -1 for the opposite-end panel.
    """
    interp_er = RegularGridInterpolator(
        (theta, rho), e_rho, bounds_error=False, fill_value=np.nan
    )
    interp_et = RegularGridInterpolator(
        (theta, rho), e_theta, bounds_error=False, fill_value=np.nan
    )

    r_eval = A_THROAT * (1.0 + eps_factor)
    rho_eval_mag = math.sqrt(max(r_eval**2 - A_THROAT**2, 0.0))
    rho_eval = panel_side * rho_eval_mag

    n_half = max(2, n_arrows // 2)
    ellis_thetas = np.linspace(0.06 * math.pi, 0.94 * math.pi, n_half)

    samples: list[tuple[float, float, float, float]] = []
    for ellis_th in ellis_thetas:
        er = float(interp_er((ellis_th, rho_eval)))
        et = float(interp_et((ellis_th, rho_eval)))
        if not (np.isfinite(er) and np.isfinite(et)):
            continue
        sin_th = math.sin(ellis_th)
        cos_th = math.cos(ellis_th)
        rho_over_r = rho_eval / r_eval
        Vx = er * rho_over_r * sin_th + et * r_eval * cos_th
        Vy = er * rho_over_r * cos_th - et * r_eval * sin_th
        x0 = r_eval * sin_th
        y0 = r_eval * cos_th
        samples.append((x0, y0, Vx, Vy))

    if not samples:
        return

    abs_max = max(math.hypot(s[2], s[3]) for s in samples) or 1.0
    for x0, y0, Vx, Vy in samples:
        norm = math.hypot(Vx, Vy)
        if norm < 1.0e-12:
            continue
        length = (norm / abs_max) * max_length
        if length < 0.025:
            continue
        ux = Vx / norm
        uy = Vy / norm
        for x_sign in (+1.0, -1.0):
            xx = x_sign * x0
            ux_sign = x_sign * ux
            ax.arrow(
                xx - 0.5 * length * ux_sign,
                y0 - 0.5 * length * uy,
                length * ux_sign,
                length * uy,
                width=0.008,
                head_width=0.058,
                head_length=0.065,
                color="#1f5f8b",
                alpha=0.92,
                length_includes_head=True,
                zorder=7,
            )


def draw_panel(
    ax,
    rho_side: np.ndarray,
    theta: np.ndarray,
    pot_side: np.ndarray,
    psi_side: np.ndarray,
    rho_full: np.ndarray,
    e_rho_full: np.ndarray,
    e_theta_full: np.ndarray,
    title: str,
    has_charge: bool,
    panel_side: float,
) -> None:
    rr, tt = np.meshgrid(rho_side, theta)
    r_areal = np.sqrt(rr**2 + A_THROAT**2)
    x = r_areal * np.sin(tt)
    y = r_areal * np.cos(tt)

    # Single mask: just the source charge if present.
    mask = np.zeros_like(x, dtype=bool)
    if has_charge:
        q_y = math.sqrt(RHO0**2 + A_THROAT**2)
        mask = (x**2 + (y - q_y) ** 2) < CHARGE_MASK_RADIUS**2

    # Mirror x -> -x to fill the full meridional plane.  Both pot and psi are
    # axisymmetric (functions of (R, z) where R = |x|, z = y), so they take
    # the same value at (x, y) and (-x, y).
    x_full = np.concatenate([x.ravel(), -x.ravel()])
    y_full = np.concatenate([y.ravel(), y.ravel()])
    pot_full = np.concatenate([pot_side.ravel(), pot_side.ravel()])
    psi_full = np.concatenate([psi_side.ravel(), psi_side.ravel()])
    mask_full = np.concatenate([mask.ravel(), mask.ravel()])

    tri = mtri.Triangulation(x_full, y_full)
    tri.set_mask(np.any(mask_full[tri.triangles], axis=1))

    valid_pot = pot_full[~mask_full]
    if has_charge:
        # Clip extreme values from the source-charge tail to keep contour
        # spacing meaningful in the rest of the panel.
        lo, hi = np.percentile(valid_pot, [3, 90])
    else:
        lo, hi = np.percentile(valid_pot, [3, 97])
    pot_levels = np.linspace(lo, hi, 22)
    ax.tricontour(
        tri,
        pot_full,
        levels=pot_levels,
        colors="#9aa1aa",
        linewidths=0.6,
        alpha=0.55,
    )

    valid_psi = psi_full[~mask_full]
    psi_amp = float(np.percentile(np.abs(valid_psi), 96))
    if psi_amp <= 0.0:
        psi_amp = 1.0
    # Symmetric levels excluding zero (axis is psi=0 by construction).
    pos_levels = np.linspace(psi_amp / N_FIELD_LINES, psi_amp, N_FIELD_LINES)
    psi_levels = np.concatenate([-pos_levels[::-1], pos_levels])
    ax.tricontour(
        tri,
        psi_full,
        levels=psi_levels,
        colors="#1f5f8b",
        linewidths=1.05,
        alpha=0.9,
        linestyles="solid",
    )

    # Throat circle.
    ax.add_patch(
        plt.Circle((0.0, 0.0), A_THROAT, fill=False, lw=2.6, color="#111827")
    )
    ax.text(0.0, 1.18, "throat", ha="center", va="bottom", fontsize=10, color="#111827")

    # Streamline-aligned arrows just outside the throat.
    draw_streamline_arrows(
        ax, rho_full, theta, e_rho_full, e_theta_full, panel_side
    )

    if has_charge:
        q_y = math.sqrt(RHO0**2 + A_THROAT**2)
        ax.scatter([0.0], [q_y], s=72, color="#b42318", zorder=8)
        ax.text(0.16, q_y + 0.10, "$q$", color="#8b1a10", fontsize=14)

    ax.text(0.0, -3.55, title, ha="center", va="center", fontsize=11, color="#374151")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-3.85, 3.85)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)


def make_clean_figure(
    rho: np.ndarray,
    theta: np.ndarray,
    pot_fixed: np.ndarray,
    e_rho: np.ndarray,
    e_theta: np.ndarray,
    modes: np.ndarray,
    spectral_filter: np.ndarray,
) -> None:
    psi = stream_function(rho, theta, modes, spectral_filter)

    pos = rho >= 0
    neg = rho <= 0
    rho_pos = rho[pos]
    rho_neg = -rho[neg][::-1]
    pot_pos = pot_fixed[:, pos]
    pot_neg = pot_fixed[:, neg][:, ::-1]
    psi_pos = psi[:, pos]
    psi_neg = psi[:, neg][:, ::-1]

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.1), constrained_layout=True)
    draw_panel(
        axes[0], rho_neg, theta, pot_neg, psi_neg,
        rho, e_rho, e_theta,
        title="opposite end", has_charge=False, panel_side=-1.0,
    )
    draw_panel(
        axes[1], rho_pos, theta, pot_pos, psi_pos,
        rho, e_rho, e_theta,
        title="source end", has_charge=True, panel_side=+1.0,
    )
    fig.suptitle(
        "Ellis wormhole electrostatics: conserved $Q_{\\rm wh}=0$ sector",
        fontsize=13,
    )
    fig.savefig(OUT_PNG, dpi=240)
    fig.savefig(OUT_PDF)


def main() -> None:
    rho = np.linspace(-RHO_MAX, RHO_MAX, N_RHO)
    theta = np.linspace(1.0e-3, math.pi - 1.0e-3, N_THETA)

    modes = solve_radial_modes(rho, RHO0, L_MAX)
    pot_kb, pot_fixed, _ = build_potential(rho, theta, modes)
    _, pot_plot, _ = build_potential(
        rho, theta, modes, spectral_filter=spectral_filter_array(L_MAX)
    )
    e_rho_plot, e_theta_plot = field_components(rho, theta, pot_plot)
    e_rho_unfiltered, _ = field_components(rho, theta, pot_fixed)

    drho = rho[1] - rho[0]
    sin_th = np.sin(theta)
    norm = np.trapezoid(sin_th, theta)
    avg_kb = np.trapezoid(pot_kb * sin_th[:, None], theta, axis=0) / norm
    avg_fixed = np.trapezoid(pot_fixed * sin_th[:, None], theta, axis=0) / norm
    idx0 = int(np.argmin(np.abs(rho)))
    flux_kb = (rho[idx0] ** 2 + A_THROAT**2) * np.gradient(avg_kb, drho)[idx0]
    flux_fixed = (rho[idx0] ** 2 + A_THROAT**2) * np.gradient(avg_fixed, drho)[idx0]

    # Asymptotic l=1, 2, 3 amplitudes on the opposite side: read off the
    # large-|rho| behaviour of the radial modes there.  For rho <= rho0 the
    # mode goes like A_l * (R_l(rho)/R_l(-RHO_MAX)) where the regular solution
    # at the negative end provides the falloff.  We just sample the mode value
    # at large negative rho as a proxy for the dipole/quadrupole reach.
    print(f"rho0/a = {RHO0 / A_THROAT:.3f}")
    print(f"L_MAX = {L_MAX}, N_RHO = {N_RHO}, RHO_MAX/a = {RHO_MAX / A_THROAT:.1f}")
    print(f"throat l=0 flux coefficient (KB only)  = {flux_kb:.6e}")
    print(f"throat l=0 flux coefficient (fixed Q)  = {flux_fixed:.6e}")
    sample_idx = max(0, int(0.95 * idx0))
    for ell in (1, 2, 3, 4):
        print(f"opposite-side mode l={ell} at rho/a={rho[sample_idx]/A_THROAT:.2f}: "
              f"R_l = {modes[ell, sample_idx]:.3e}")

    filter_arr = spectral_filter_array(L_MAX)
    make_clean_figure(
        rho, theta, pot_plot, e_rho_plot, e_theta_plot, modes, filter_arr
    )
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
