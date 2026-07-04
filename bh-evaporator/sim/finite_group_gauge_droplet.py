"""Finite-group gauge droplet counting diagnostic.

For an L x L square patch with Z_q link variables and Gauss constraints:

    dim H_phys = q^(E - V + 1) = q^(L^2)

Add boundary line-tension energy M_L = 4 sigma L and compute the
finite-difference temperature and 2D bath power scaling.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def row_for_L(L: int, q: int, sigma: float, kappa: float) -> dict[str, float | int]:
    vertices = (L + 1) ** 2
    edges = 2 * L * (L + 1)
    plaquettes = L**2
    boundary = 4 * L
    exponent = edges - vertices + 1
    entropy = plaquettes * math.log(q)
    mass = sigma * boundary

    if L > 1:
        delta_entropy = (2 * L - 1) * math.log(q)
        delta_mass = 4 * sigma
        temp_discrete = delta_mass / delta_entropy
    else:
        delta_entropy = math.log(q)
        delta_mass = mass
        temp_discrete = delta_mass / delta_entropy

    temp_continuum = 2 * sigma / (L * math.log(q))
    power_discrete = kappa * boundary * temp_discrete**3
    power_continuum = kappa * boundary * temp_continuum**3

    return {
        "L": L,
        "q": q,
        "vertices": vertices,
        "edges": edges,
        "plaquettes": plaquettes,
        "boundary": boundary,
        "gauss_exponent": exponent,
        "entropy": entropy,
        "mass": mass,
        "delta_entropy": delta_entropy,
        "delta_mass": delta_mass,
        "temp_discrete": temp_discrete,
        "temp_continuum": temp_continuum,
        "power_discrete": power_discrete,
        "power_continuum": power_continuum,
        "mass_power_product": mass**2 * power_discrete,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--kappa", type=float, default=1.0)
    parser.add_argument("--max-L", type=int, default=20)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/finite_group_gauge_droplet.csv"),
    )
    args = parser.parse_args()

    rows = [row_for_L(L, args.q, args.sigma, args.kappa) for L in range(1, args.max_L + 1)]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {args.out}")
    print("L  exponent  plaquettes  S        M        T_disc   P_disc   M^2 P")
    for row in rows[: min(8, len(rows))]:
        print(
            f"{row['L']:2d} "
            f"{row['gauss_exponent']:8d} "
            f"{row['plaquettes']:10d} "
            f"{row['entropy']:8.3f} "
            f"{row['mass']:8.3f} "
            f"{row['temp_discrete']:8.3f} "
            f"{row['power_discrete']:8.3f} "
            f"{row['mass_power_product']:8.3f}"
        )


if __name__ == "__main__":
    main()
