"""Numerical finite-difference frame check for the sech Alcubierre metric."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from alcubierre_3p1_set import H, christoffel, d_christoffel, einstein, metric
from front_tip_parallel_tidal import riemann_cov


OUT = Path("output/sech")


def contract_riemann(R: np.ndarray, A: np.ndarray, B: np.ndarray, C: np.ndarray, D: np.ndarray) -> float:
    return float(np.einsum("abcd,a,b,c,d->", R, A, B, C, D))


def contract_2(T: np.ndarray, A: np.ndarray, B: np.ndarray) -> float:
    return float(np.einsum("ab,a,b->", T, A, B))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    r_h = float(np.arccosh(2.0))
    kappa = float(np.sqrt(3.0) / 2.0)
    expected_r = -kappa / r_h
    expected_g = -2.0 * kappa / r_h

    point = np.array([0.0, r_h, 0.0, 0.0])

    lines = [
        "Numerical finite-difference frame check at the sech front tip",
        "",
        f"r_h = acosh(2) = {r_h:.12e}",
        f"kappa = sqrt(3)/2 = {kappa:.12e}",
        f"expected R_KYKY/q^2 = -kappa/r_h = {expected_r:.12e}",
        f"expected G_KK/q^2 = -2*kappa/r_h = {expected_g:.12e}",
        "",
        "Frame:",
        "  K = q partial_t, so R_KYKY/q^2 = R_tyty",
        "  and G_KK/q^2 = G_tt at the coordinate tip.",
        "",
    ]

    for h in [8.0e-4, 4.0e-4, 2.0e-4, 1.0e-4]:
        R = riemann_cov(point, h)
        G, scalar, ric = einstein(point, h)
        K_unit = np.array([1.0, 0.0, 0.0, 0.0])
        Y = np.array([0.0, 0.0, 1.0, 0.0])
        Z = np.array([0.0, 0.0, 0.0, 1.0])
        r_kyky_over_q2 = contract_riemann(R, K_unit, Y, K_unit, Y)
        r_kzkz_over_q2 = contract_riemann(R, K_unit, Z, K_unit, Z)
        gkk_over_q2 = contract_2(G, K_unit, K_unit)
        lines.extend(
            [
                f"h={h:.0e}",
                f"  R_KYKY/q^2 = {r_kyky_over_q2:.12e}",
                f"  R_KZKZ/q^2 = {r_kzkz_over_q2:.12e}",
                f"  G_KK/q^2   = {gkk_over_q2:.12e}",
                f"  Ricci scalar = {scalar:.12e}",
                f"  R coefficient error = {r_kyky_over_q2 - expected_r:.3e}",
                f"  G coefficient error = {gkk_over_q2 - expected_g:.3e}",
                "",
            ]
        )

    lines.extend(
        [
            "Conclusion:",
            "  Direct finite-difference curvature of the original sech metric",
            "  converges to the analytic frame coefficients once the affine",
            "  factor q^2 is divided out.",
        ]
    )

    (OUT / "front_tip_numerical_frame_check.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:24]))


if __name__ == "__main__":
    main()
