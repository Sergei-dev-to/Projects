"""Golden-rule evaporator diagnostic for the edge-tension droplet.

This script separates two questions that are easy to conflate:

1. Does the entropy curve S(M) plus smooth matrix elements give Hawking-like
   small-quantum emission rates?
2. Does a literal one-step shell transition L -> L-1 do the same thing?

For the finite-group gauge droplet,

    S_L = L^2 log q,  M_L = 4 sigma L.

The small-quantum golden-rule model uses

    dGamma ~ B_L |M(omega)|^2 rho(omega)
              exp[S(M_L - omega) - S(M_L)] d omega,

and the power integral uses an extra factor of omega.

The whole-shell model forces omega = M_L - M_{L-1} = 4 sigma. It is included
as a stress test, because a Schwarzschild-like black hole emits quanta with
typical omega ~ T ~ 1/L, not quanta of order the entire shell gap.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np


def entropy_of_mass(mass: float, q: int, sigma: float) -> float:
    if mass <= 0.0:
        return 0.0
    return (mass / (4.0 * sigma)) ** 2 * math.log(q)


def entropy_of_L(L: int, q: int) -> float:
    return L * L * math.log(q)


def beta_of_L(L: int, q: int, sigma: float) -> float:
    mass = 4.0 * sigma * L
    return mass * math.log(q) / (8.0 * sigma**2)


def matrix_profile(omega: np.ndarray, cutoff: float, profile: str) -> np.ndarray:
    """Return |M(omega)|^2 up to an irrelevant coupling constant."""
    if profile == "flat":
        return np.ones_like(omega)
    if profile == "soft_cutoff":
        return np.exp(-2.0 * omega / cutoff)
    if profile == "mild_power":
        return 1.0 / (1.0 + omega / cutoff) ** 2
    raise ValueError(f"unknown profile {profile!r}")


def small_quantum_rates(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_max: float,
    n_grid: int,
    profile: str,
    cutoff_multiple_T: float,
) -> dict[str, float]:
    """Golden-rule rate and power for small emitted quanta."""
    mass = 4.0 * sigma * L
    beta = beta_of_L(L, q, sigma)
    temp = 1.0 / beta
    boundary = 4.0 * L
    omega_max = min(mass, x_max / beta)
    omega = np.linspace(0.0, omega_max, n_grid)

    s0 = entropy_of_mass(mass, q, sigma)
    delta_s = np.array([entropy_of_mass(mass - w, q, sigma) - s0 for w in omega])
    density_number = omega ** max(bath_dim - 1, 0)
    profile_weight = matrix_profile(omega, cutoff_multiple_T * temp, profile)
    weight = density_number * np.exp(delta_s) * profile_weight

    number_rate = boundary * float(np.trapezoid(weight, omega))
    power = boundary * float(np.trapezoid(omega * weight, omega))
    mean_omega = power / number_rate if number_rate > 0.0 else 0.0

    return {
        "small_number_rate": number_rate,
        "small_power": power,
        "small_mean_omega": mean_omega,
        "small_mean_omega_over_T": mean_omega / temp,
    }


def whole_shell_rates(L: int, q: int, sigma: float, bath_dim: int, profile: str) -> dict[str, float]:
    """Golden-rule stress test for a literal L -> L-1 shell jump."""
    if L <= 1:
        return {
            "shell_number_rate": 0.0,
            "shell_power": 0.0,
            "shell_omega_over_T": 0.0,
            "shell_boltzmann_suppression": 0.0,
        }

    omega = 4.0 * sigma
    beta = beta_of_L(L, q, sigma)
    temp = 1.0 / beta
    boundary = 4.0 * L
    delta_s = entropy_of_L(L - 1, q) - entropy_of_L(L, q)
    density_number = omega ** max(bath_dim - 1, 0)
    profile_weight = float(matrix_profile(np.array([omega]), cutoff=temp, profile=profile)[0])
    number_rate = boundary * density_number * math.exp(delta_s) * profile_weight

    return {
        "shell_number_rate": number_rate,
        "shell_power": omega * number_rate,
        "shell_omega_over_T": omega / temp,
        "shell_boltzmann_suppression": math.exp(delta_s),
    }


def fit_power_law(rows: list[dict[str, float]], key: str, min_L: int) -> tuple[float, float]:
    xs = []
    ys = []
    for row in rows:
        if row["L"] >= min_L and row[key] > 0.0:
            xs.append(math.log(row["mass"]))
            ys.append(math.log(row[key]))
    coeff = np.polyfit(np.array(xs), np.array(ys), 1)
    slope = float(coeff[0])
    intercept = float(coeff[1])
    return slope, intercept


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--max-L", type=int, default=80)
    parser.add_argument("--min-fit-L", type=int, default=20)
    parser.add_argument("--x-max", type=float, default=10.0)
    parser.add_argument("--n-grid", type=int, default=6001)
    parser.add_argument(
        "--profile",
        choices=["flat", "soft_cutoff", "mild_power"],
        default="flat",
    )
    parser.add_argument("--cutoff-multiple-T", type=float, default=50.0)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/golden_rule_evaporator.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/golden_rule_evaporator_summary.csv"),
    )
    args = parser.parse_args()

    rows: list[dict[str, float]] = []
    for L in range(2, args.max_L + 1):
        mass = 4.0 * args.sigma * L
        beta = beta_of_L(L, args.q, args.sigma)
        row: dict[str, float] = {
            "L": float(L),
            "q": float(args.q),
            "sigma": args.sigma,
            "bath_dim": float(args.bath_dim),
            "mass": mass,
            "entropy": entropy_of_L(L, args.q),
            "beta": beta,
            "temperature": 1.0 / beta,
            "boundary": 4.0 * L,
        }
        row.update(
            small_quantum_rates(
                L,
                args.q,
                args.sigma,
                args.bath_dim,
                args.x_max,
                args.n_grid,
                args.profile,
                args.cutoff_multiple_T,
            )
        )
        row.update(whole_shell_rates(L, args.q, args.sigma, args.bath_dim, args.profile))
        row["M2_small_power"] = row["mass"] ** 2 * row["small_power"]
        row["M2_shell_power"] = row["mass"] ** 2 * row["shell_power"]
        rows.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    small_slope, small_intercept = fit_power_law(rows, "small_power", args.min_fit_L)
    shell_slope, shell_intercept = fit_power_law(rows, "shell_power", args.min_fit_L)
    summary = [
        {
            "model": "small_quantum",
            "profile": args.profile,
            "bath_dim": args.bath_dim,
            "fit_min_L": args.min_fit_L,
            "power_law_slope_logP_logM": small_slope,
            "power_law_intercept": small_intercept,
            "target_slope_for_2D_BH_like": -2.0,
            "mean_M2P_last10": float(np.mean([row["M2_small_power"] for row in rows[-10:]])),
            "std_M2P_last10": float(np.std([row["M2_small_power"] for row in rows[-10:]])),
        },
        {
            "model": "whole_shell",
            "profile": args.profile,
            "bath_dim": args.bath_dim,
            "fit_min_L": args.min_fit_L,
            "power_law_slope_logP_logM": shell_slope,
            "power_law_intercept": shell_intercept,
            "target_slope_for_2D_BH_like": -2.0,
            "mean_M2P_last10": float(np.mean([row["M2_shell_power"] for row in rows[-10:]])),
            "std_M2P_last10": float(np.std([row["M2_shell_power"] for row in rows[-10:]])),
        },
    ]

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print("model          slope log P/log M   mean M^2 P last10   comment")
    print(
        f"small_quantum  {small_slope:17.4f}   "
        f"{summary[0]['mean_M2P_last10']:17.4f}   "
        "works if slope is near -2"
    )
    print(
        f"whole_shell    {shell_slope:17.4f}   "
        f"{summary[1]['mean_M2P_last10']:17.4e}   "
        "stress test; should fail"
    )
    print()
    print("L   T          <omega>/T small   shell omega/T   M^2 P small      M^2 P shell")
    for row in rows[:5] + rows[-5:]:
        print(
            f"{int(row['L']):2d} "
            f"{row['temperature']:10.5f} "
            f"{row['small_mean_omega_over_T']:16.4f} "
            f"{row['shell_omega_over_T']:15.4f} "
            f"{row['M2_small_power']:15.4f} "
            f"{row['M2_shell_power']:15.4e}"
        )


if __name__ == "__main__":
    main()
