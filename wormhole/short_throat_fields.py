"""
Reusable short-throat field model for the wormhole figures.

This module collects the static multipole machinery used by the short-throat
illustrations.  It supports both the Dai--Stojkovic matched static family and
the conservation-preserving family used elsewhere in the paper.
"""

from __future__ import annotations

import numpy as np


L_TUBE = 4.0
DEFAULT_L_MAX = 30


def B_coef(l, A, R=1.0, q=1.0):
    return (2 * l + 1) / (2 * (l + 1)) * q * R ** (2 * l + 1) / A ** (l + 1)


def T_coef(l, A, R=1.0, q=1.0):
    return -1.0 / (2 * (l + 1)) * q * R ** (2 * l + 1) / A ** (l + 1)


def P(l, x):
    if l == 0:
        return np.ones_like(x)
    if l == 1:
        return np.asarray(x, dtype=float)
    pm1 = np.ones_like(x)
    pm0 = np.asarray(x, dtype=float)
    for k in range(2, l + 1):
        pnew = ((2 * k - 1) * x * pm0 - (k - 1) * pm1) / k
        pm1, pm0 = pm0, pnew
    return pm0


def V_side1_DS(r1, cos_t1, A, R=1.0, q=1.0, l_max=DEFAULT_L_MAX):
    """Side-1 potential for the D-S matched static family."""
    dist = np.sqrt(r1 ** 2 + A ** 2 - 2 * A * r1 * cos_t1 + 1e-30)
    out = q / dist
    for l in range(0, l_max + 1):
        out = out + T_coef(l, A, R, q) * P(l, cos_t1) / r1 ** (l + 1)
    return out


def V_side2_DS(r2, cos_t2, A, R=1.0, q=1.0, l_max=DEFAULT_L_MAX):
    """Side-2 potential for the D-S matched static family."""
    out = np.zeros_like(r2 * cos_t2)
    for l in range(0, l_max + 1):
        out = out + B_coef(l, A, R, q) * P(l, cos_t2) / r2 ** (l + 1)
    return out


def V_side1_cons(r1, cos_t1, S, R=1.0, q=1.0, l_max=DEFAULT_L_MAX):
    """
    Conservation-preserving side-1 potential.

    S > R: source on side 1 at radius S from the left mouth.
    S < -R: source on side 2 at radius |S| from the right mouth.
    """
    if S > R:
        A = S
        out = V_side1_DS(r1, cos_t1, A, R, q, l_max=l_max)
        out = out + (q * R / (2 * A)) / r1
        return out
    if S < -R:
        ap = -S
        out = np.zeros_like(r1 * cos_t1)
        for l in range(0, l_max + 1):
            out = out + B_coef(l, ap, R, q) * P(l, cos_t1) / r1 ** (l + 1)
        out = out + (q - q * R / (2 * ap)) / r1
        return out
    raise ValueError("S inside the mouth")


def V_side2_cons(r2, cos_t2, S, R=1.0, q=1.0, l_max=DEFAULT_L_MAX):
    """Conservation-preserving side-2 potential."""
    if S > R:
        A = S
        out = np.zeros_like(r2 * cos_t2)
        for l in range(1, l_max + 1):
            out = out + B_coef(l, A, R, q) * P(l, cos_t2) / r2 ** (l + 1)
        return out
    if S < -R:
        ap = -S
        out = V_side1_DS(r2, cos_t2, ap, R, q, l_max=l_max)
        out = out - (q - q * R / (2 * ap)) / r2
        return out
    raise ValueError("S inside the mouth")


def side_coords_1(U, RHO, L=L_TUBE):
    """
    Side-1 spherical coordinates relative to the mouth centered at u = -L/2.
    """
    u1 = U + L / 2
    r1 = np.sqrt(u1 ** 2 + RHO ** 2) + 1e-12
    cos_t1 = -u1 / r1
    return r1, cos_t1


def side_coords_2(U, RHO, L=L_TUBE):
    """Side-2 spherical coordinates relative to the mouth centered at u = +L/2."""
    u2 = U - L / 2
    r2 = np.sqrt(u2 ** 2 + RHO ** 2) + 1e-12
    cos_t2 = u2 / r2
    return r2, cos_t2


def potential_field_conserved(U, RHO, S, R=1.0, q=1.0, L=L_TUBE, l_max=DEFAULT_L_MAX):
    """Conservation-preserving potential on the meridional cartoon plane."""
    side1 = U < -L / 2
    side2 = U > L / 2
    r1, cos_t1 = side_coords_1(U, RHO, L)
    r2, cos_t2 = side_coords_2(U, RHO, L)
    if S <= -L / 2 - R:
        A = -L / 2 - S
        V_s1 = V_side1_cons(r1, cos_t1, +A, R, q, l_max=l_max)
        V_s2 = V_side2_cons(r2, cos_t2, +A, R, q, l_max=l_max)
    elif S >= L / 2 + R:
        A = S - L / 2
        V_s1 = V_side1_cons(r1, cos_t1, -A, R, q, l_max=l_max)
        V_s2 = V_side2_cons(r2, cos_t2, -A, R, q, l_max=l_max)
    else:
        raise ValueError("S inside the tube")
    V = np.zeros_like(U + RHO)
    V = np.where(side1, V_s1, V)
    V = np.where(side2, V_s2, V)
    return V


def potential_field_ds(U, RHO, S, R=1.0, q=1.0, L=L_TUBE, l_max=DEFAULT_L_MAX):
    """D-S matched static potential on the meridional cartoon plane."""
    A = -L / 2 - S
    r1, cos_t1 = side_coords_1(U, RHO, L)
    r2, cos_t2 = side_coords_2(U, RHO, L)
    V_s1 = V_side1_DS(r1, cos_t1, A, R, q, l_max=l_max)
    V_s2 = V_side2_DS(r2, cos_t2, A, R, q, l_max=l_max)
    side1 = U < -L / 2
    side2 = U > L / 2
    return np.where(side1, V_s1, np.where(side2, V_s2, 0.0))


def E_field_from_potential(potential_fn, U, RHO, S, R=1.0, q=1.0, eps=2e-3, L=L_TUBE, l_max=DEFAULT_L_MAX):
    """Numerical field extraction from a potential evaluator."""
    V_pu = potential_fn(U + eps, RHO, S, R, q, L, l_max=l_max)
    V_mu = potential_fn(U - eps, RHO, S, R, q, L, l_max=l_max)
    V_pr = potential_fn(U, RHO + eps, S, R, q, L, l_max=l_max)
    V_mr = potential_fn(U, np.maximum(RHO - eps, 1e-4), S, R, q, L, l_max=l_max)
    E_u = -(V_pu - V_mu) / (2 * eps)
    E_r = -(V_pr - V_mr) / (2 * eps)
    return E_u, E_r


def E_field_conserved(U, RHO, S, R=1.0, q=1.0, eps=2e-3, L=L_TUBE, l_max=DEFAULT_L_MAX):
    return E_field_from_potential(
        potential_field_conserved, U, RHO, S, R, q, eps=eps, L=L, l_max=l_max
    )


def E_field_ds(U, RHO, S, R=1.0, q=1.0, eps=2e-3, L=L_TUBE, l_max=DEFAULT_L_MAX):
    return E_field_from_potential(
        potential_field_ds, U, RHO, S, R, q, eps=eps, L=L, l_max=l_max
    )


def draw_tube(ax, L, R):
    """Fill the throat as a gray stadium in the (u, y) meridional plane."""
    n = 120
    theta_l = np.linspace(np.pi / 2, 3 * np.pi / 2, n)
    theta_r = np.linspace(-np.pi / 2, np.pi / 2, n)
    xs = np.concatenate(
        [-L / 2 + R * np.cos(theta_l), L / 2 + R * np.cos(theta_r)]
    )
    ys = np.concatenate([R * np.sin(theta_l), R * np.sin(theta_r)])
    ax.fill(xs, ys, color="0.87", edgecolor="k", linewidth=1.3, zorder=3)
    ax.plot([-L / 2, L / 2], [R, R], "k-", lw=1.3, zorder=4)
    ax.plot([-L / 2, L / 2], [-R, -R], "k-", lw=1.3, zorder=4)
