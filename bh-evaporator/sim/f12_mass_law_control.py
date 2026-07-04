"""F12 mass-law control for the edge-tension evaporator.

F12 in the project matrix is "sqrt-mass vs linear-mass controls".  This script
checks whether the missing F12 entry is a showstopper.

Assume:
    S(L) ~ L^2
    M(L) ~ L^a
    boundary length B(L) ~ L
    bath dimension d
    P(L) ~ B(L) T(L)^(d+1)

Then:
    T(L) ~ (dS/dM)^-1 ~ L^(a-2)
    P(L) ~ L * T^(d+1)

For a 2D bath and Schwarzschild-like evaporation, we want:
    T ~ M^-1
    P ~ M^-2

This diagnostic scans a and reports the exponents.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


def exponents(a: float, bath_dim: int) -> dict[str, float]:
    # S ~ L^2, M ~ L^a.
    # T ~ L^(a - 2) ~ M^((a - 2)/a).
    temp_vs_M = (a - 2.0) / a
    # C < 0 when dT/dM < 0, i.e. temp_vs_M < 0.
    # P ~ L * T^(d+1) ~ L^(1 + (a - 2)(d+1)).
    power_vs_L = 1.0 + (a - 2.0) * (bath_dim + 1.0)
    power_vs_M = power_vs_L / a
    # Lifetime tau ~ integral dM/P ~ M^(1 - power_vs_M), for power_vs_M != 1.
    lifetime_vs_M0 = 1.0 - power_vs_M
    return {
        "a_mass_vs_L": a,
        "bath_dim": float(bath_dim),
        "T_vs_M_exponent": temp_vs_M,
        "P_vs_L_exponent": power_vs_L,
        "P_vs_M_exponent": power_vs_M,
        "lifetime_vs_M0_exponent": lifetime_vs_M0,
        "negative_heat_capacity": float(temp_vs_M < 0.0),
        "T_error_from_BH": abs(temp_vs_M + 1.0),
        "P_error_from_BH": abs(power_vs_M + 2.0),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--a-min", type=float, default=0.5)
    parser.add_argument("--a-max", type=float, default=2.5)
    parser.add_argument("--n", type=int, default=81)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/f12_mass_law_control.csv"),
    )
    args = parser.parse_args()

    rows = [exponents(float(a), args.bath_dim) for a in np.linspace(args.a_min, args.a_max, args.n)]
    best_T = min(rows, key=lambda row: row["T_error_from_BH"])
    best_P = min(rows, key=lambda row: row["P_error_from_BH"])
    best_both = min(rows, key=lambda row: row["T_error_from_BH"] + row["P_error_from_BH"])

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    controls = [0.5, 1.0, 2.0]
    print(f"wrote {args.out}")
    print("control a   T~M^x      P~M^y      tau~M0^z   C<0")
    for a in controls:
        row = exponents(a, args.bath_dim)
        print(
            f"{a:8.3f} "
            f"{row['T_vs_M_exponent']:10.3f} "
            f"{row['P_vs_M_exponent']:10.3f} "
            f"{row['lifetime_vs_M0_exponent']:10.3f} "
            f"{bool(row['negative_heat_capacity'])}"
        )
    print()
    print(
        "best combined BH match: "
        f"a={best_both['a_mass_vs_L']:.4f}, "
        f"T~M^{best_both['T_vs_M_exponent']:.4f}, "
        f"P~M^{best_both['P_vs_M_exponent']:.4f}"
    )
    print(
        "best T match: "
        f"a={best_T['a_mass_vs_L']:.4f}; "
        "best P match: "
        f"a={best_P['a_mass_vs_L']:.4f}"
    )


if __name__ == "__main__":
    main()
