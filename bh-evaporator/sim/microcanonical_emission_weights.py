"""Microcanonical emission weights for the edge-tension droplet.

The goal is to check whether thermal hard-emission weights follow from the
finite-gauge droplet entropy curve:

    S_L = L^2 log q,  M_L = 4 sigma L.

Treat M as a continuous variable along the droplet trajectory:

    S(M) = (M / 4 sigma)^2 log q.

Then emission of a hard quantum of energy omega is weighted by

    exp(S(M - omega) - S(M)),

which should approximate exp(-beta omega) at beta = dS/dM.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


def entropy_of_mass(mass: float, q: int, sigma: float) -> float:
    if mass <= 0:
        return 0.0
    return (mass / (4.0 * sigma)) ** 2 * math.log(q)


def beta_continuum(L: int, q: int, sigma: float) -> float:
    mass = 4.0 * sigma * L
    return mass * math.log(q) / (8.0 * sigma**2)


def beta_discrete(L: int, q: int, sigma: float) -> float:
    if L <= 1:
        return math.log(q) / (4.0 * sigma)
    return ((2 * L - 1) * math.log(q)) / (4.0 * sigma)


def normalized_power_integral(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    exact: bool,
    x_max: float,
    n_grid: int,
) -> float:
    """Compute boundary * integral d omega omega^d * weight(omega)."""
    mass = 4.0 * sigma * L
    beta = beta_continuum(L, q, sigma)
    omega_max = min(mass, x_max / beta)
    omega = np.linspace(0.0, omega_max, n_grid)
    if exact:
        s0 = entropy_of_mass(mass, q, sigma)
        weights = np.array([math.exp(entropy_of_mass(mass - w, q, sigma) - s0) for w in omega])
    else:
        weights = np.exp(-beta * omega)
    integrand = omega**bath_dim * weights
    boundary = 4.0 * L
    return float(boundary * np.trapezoid(integrand, omega))


def row_for_L(L: int, q: int, sigma: float, bath_dim: int, x_max: float, n_grid: int) -> dict[str, float | int]:
    mass = 4.0 * sigma * L
    beta = beta_continuum(L, q, sigma)
    temp = 1.0 / beta
    beta_disc = beta_discrete(L, q, sigma)

    xs = np.linspace(0.0, x_max, n_grid)
    omegas = xs / beta
    s0 = entropy_of_mass(mass, q, sigma)
    exact_weights = np.array([math.exp(entropy_of_mass(mass - w, q, sigma) - s0) for w in omegas])
    boltz_weights = np.exp(-xs)
    relative = exact_weights / boltz_weights

    max_rel_minus_1 = float(np.max(np.abs(relative - 1.0)))
    rel_at_x1 = float(np.interp(1.0, xs, relative))
    rel_at_x3 = float(np.interp(3.0, xs, relative))
    rel_at_x5 = float(np.interp(5.0, xs, relative))

    power_exact = normalized_power_integral(L, q, sigma, bath_dim, True, x_max, n_grid)
    power_boltz = normalized_power_integral(L, q, sigma, bath_dim, False, x_max, n_grid)

    return {
        "L": L,
        "q": q,
        "sigma": sigma,
        "bath_dim": bath_dim,
        "mass": mass,
        "entropy": entropy_of_mass(mass, q, sigma),
        "beta_continuum": beta,
        "beta_discrete": beta_disc,
        "temp_continuum": temp,
        "boundary": 4 * L,
        "max_rel_minus_1_xrange": max_rel_minus_1,
        "rel_exact_to_boltz_x1": rel_at_x1,
        "rel_exact_to_boltz_x3": rel_at_x3,
        "rel_exact_to_boltz_x5": rel_at_x5,
        "power_exact": power_exact,
        "power_boltz": power_boltz,
        "power_ratio_exact_to_boltz": power_exact / power_boltz,
        "mass_squared_power_exact": mass**2 * power_exact,
        "mass_squared_power_boltz": mass**2 * power_boltz,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--max-L", type=int, default=40)
    parser.add_argument("--x-max", type=float, default=8.0)
    parser.add_argument("--n-grid", type=int, default=4001)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/microcanonical_emission_weights.csv"),
    )
    args = parser.parse_args()

    rows = [
        row_for_L(L, args.q, args.sigma, args.bath_dim, args.x_max, args.n_grid)
        for L in range(2, args.max_L + 1)
    ]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {args.out}")
    print("L   beta     T        rel@x=1 rel@x=3 rel@x=5 P_exact/P_B  M^2 P_exact")
    for row in rows[:8] + rows[-5:]:
        print(
            f"{row['L']:2d} "
            f"{row['beta_continuum']:8.3f} "
            f"{row['temp_continuum']:8.4f} "
            f"{row['rel_exact_to_boltz_x1']:8.4f} "
            f"{row['rel_exact_to_boltz_x3']:8.4f} "
            f"{row['rel_exact_to_boltz_x5']:8.4f} "
            f"{row['power_ratio_exact_to_boltz']:10.4f} "
            f"{row['mass_squared_power_exact']:12.4f}"
        )


if __name__ == "__main__":
    main()
