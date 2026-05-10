#!/usr/bin/env python3
"""
Numerical counterexample hunt for fixed-zero-flux electrostatic self-force.

This is an exploratory script, not a publication-quality solver.  It scans
ultrastatic, spherically symmetric two-ended metrics

    ds^2_spatial = dl^2 + r(l)^2 dOmega^2

and estimates the radial self-force on a unit charge after projecting the
two-ended Green function to the sector with zero flux through the opposite
end.  The radial Green modes obey

    d/dl [ r(l)^2 dR_l/dl ] - l(l+1) R_l = -delta(l-l0)

with zero potential at the two large numerical ends.  The l=0 homogeneous
mode is then added to cancel the opposite-end flux.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.interpolate import CubicSpline
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve


L_DOMAIN = 45.0
N_GRID = 3601
L_MAX = 95

@dataclass(frozen=True)
class Profile:
    name: str
    radius: Callable[[np.ndarray], np.ndarray]


def ellis(a: float = 1.0) -> Profile:
    return Profile(f"Ellis a={a:g}", lambda l: np.sqrt(l * l + a * a))


def fat_throat(a: float = 1.0, amp: float = 0.8, width: float = 2.0) -> Profile:
    def r(l: np.ndarray) -> np.ndarray:
        base = np.sqrt(l * l + a * a)
        # Keep r(0)=a but make the near-throat flare wider.
        return base + amp * (l * l / (l * l + width * width)) * np.exp(-(l / width) ** 2)

    return Profile(f"fat flare amp={amp:g}, w={width:g}", r)


def narrow_neck(a: float = 1.0, amp: float = 0.45, width: float = 1.4) -> Profile:
    def r(l: np.ndarray) -> np.ndarray:
        base = np.sqrt(l * l + a * a)
        # A smooth shoulder outside the throat; positive for the amplitudes scanned.
        return base * (1.0 - amp * (l * l / (l * l + a * a)) * np.exp(-(l / width) ** 2))

    return Profile(f"narrow shoulder amp={amp:g}, w={width:g}", r)


def long_cylinder(a: float = 1.0, length: float = 3.0) -> Profile:
    def r(l: np.ndarray) -> np.ndarray:
        # Smoothly interpolates from a cylindrical neck to AF behaviour.
        return a + (np.sqrt(l * l + length * length) - length)

    return Profile(f"long compact neck L={length:g}", r)


def solve_modes(l_grid: np.ndarray, r_grid: np.ndarray, l0: float) -> np.ndarray:
    h = l_grid[1] - l_grid[0]
    n = l_grid.size
    modes = np.zeros((L_MAX + 1, n), dtype=float)

    j = int(np.searchsorted(l_grid, l0) - 1)
    j = max(1, min(n - 3, j))
    t = (l0 - l_grid[j]) / h
    src = np.zeros(n - 2)
    src[j - 1] -= (1.0 - t) / h
    src[j] -= t / h

    r_half = 0.5 * (r_grid[:-1] + r_grid[1:])
    p_half = r_half * r_half
    lower_base = p_half[:-1] / h**2
    upper_base = p_half[1:] / h**2
    main_base = -(p_half[:-1] + p_half[1:]) / h**2

    for ell in range(L_MAX + 1):
        main = main_base - ell * (ell + 1.0)
        mat = diags(
            [lower_base[1:], main, upper_base[:-1]],
            [-1, 0, 1],
            shape=(n - 2, n - 2),
            format="csc",
        )
        modes[ell, 1:-1] = spsolve(mat, src)

    return modes


def fixed_flux_axis_potential(
    l_grid: np.ndarray, r_grid: np.ndarray, modes: np.ndarray
) -> tuple[np.ndarray, float]:
    """Return fixed-flux axis potential and homogeneous correction coefficient."""
    pot_eq = np.tensordot(2 * np.arange(L_MAX + 1) + 1, modes, axes=(0, 0))

    h = l_grid[1] - l_grid[0]
    # Opposite-end flux of the equal-voltage l=0 piece.  The first interior
    # point avoids the Dirichlet endpoint.
    flux_neg = r_grid[1] ** 2 * (modes[0, 2] - modes[0, 0]) / (2.0 * h)

    inv_p = 1.0 / (r_grid * r_grid)
    # H(l)=int_l^{+L} ds/r(s)^2, so r^2 H'=-1 and H(+L)=0.
    rev = inv_p[::-1]
    h_rev = np.zeros_like(rev)
    h_rev[1:] = np.cumsum(0.5 * (rev[:-1] + rev[1:]) * h)
    harmonic = h_rev[::-1]

    # Add flux_neg * H, because r^2 d(flux_neg H)/dl = -flux_neg.
    return pot_eq + flux_neg * harmonic, flux_neg


def estimate_force(
    l_grid: np.ndarray, r_grid: np.ndarray, pot_axis: np.ndarray, l0: float
) -> float:
    interp = CubicSpline(l_grid, pot_axis)
    r0 = float(np.interp(l0, l_grid, r_grid))
    # The truncated angular mode sum resolves the Coulomb singularity only
    # outside a physical angular scale ~r0/L_MAX.  Use an adaptive annulus:
    # close enough to see the regular field, far enough to avoid spectral
    # ringing from the unresolved singular point.
    inner = max(0.18, 4.0 * r0 / L_MAX)
    outer = max(0.75, 0.38 * r0)
    outer = min(outer, 0.42 * L_DOMAIN)
    xs = np.r_[-np.linspace(outer, inner, 9), np.linspace(inner, outer, 9)]
    vals = interp(l0 + xs) - 1.0 / np.abs(xs)
    # The residual is smooth.  A cubic fit keeps the odd/even parts separated
    # well in the Ellis validation; higher degree tends to chase truncation
    # ripples near the charge.
    coeff = np.polyfit(xs, vals, deg=3)
    dphi_reg = coeff[-2]
    return -dphi_reg


def ellis_exact_fixed_force(x: float, a: float = 1.0) -> float:
    return (
        (1.0 / (1.0 + x * x))
        * (0.5 - math.atan(x) / math.pi)
        - x / (math.pi * (1.0 + x * x) ** 2)
    ) / (a * a)


def scan_profile(profile: Profile, positions: list[float]) -> list[tuple[float, float, float]]:
    l_grid = np.linspace(-L_DOMAIN, L_DOMAIN, N_GRID)
    r_grid = profile.radius(l_grid)
    rows = []
    for l0 in positions:
        modes = solve_modes(l_grid, r_grid, l0)
        pot_fixed, flux = fixed_flux_axis_potential(l_grid, r_grid, modes)
        force = estimate_force(l_grid, r_grid, pot_fixed, l0)
        rows.append((l0, force, flux))
    return rows


def main() -> None:
    positions = [0.55, 0.8, 1.1, 1.6, 2.4, 3.5, 5.0]
    profiles = [
        ellis(),
        fat_throat(amp=0.45, width=1.5),
        fat_throat(amp=1.25, width=2.8),
        narrow_neck(amp=0.25, width=1.2),
        narrow_neck(amp=0.55, width=1.8),
        long_cylinder(length=1.5),
        long_cylinder(length=4.0),
    ]

    print(
        f"domain=[-{L_DOMAIN},{L_DOMAIN}], N={N_GRID}, L_MAX={L_MAX}, "
        "unit charge, ultrastatic"
    )
    print("positive force means repulsion toward the source end infinity\n")

    for profile in profiles:
        print(profile.name)
        rows = scan_profile(profile, positions)
        for l0, force, flux in rows:
            extra = ""
            if profile.name.startswith("Ellis"):
                exact = ellis_exact_fixed_force(l0)
                extra = f", exact={exact:+.4e}, err={force - exact:+.1e}"
            flag = "  <-- attractive" if force < -2e-4 else ""
            print(f"  l0={l0:4.2f}: F={force:+.4e}, Qeq(-end)={flux:+.4e}{extra}{flag}")
        print()


if __name__ == "__main__":
    main()
