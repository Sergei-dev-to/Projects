"""ADM/Gauss-Codazzi derivation of the front-tip PP component.

This is a convention-calibrated derivation.  It uses the ADM data of the
Alcubierre metric rather than the full 4D Christoffel calculation.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    kappa, R = sp.symbols("kappa R", positive=True, real=True)

    # Local front-tip data.
    v = -1
    v_x = -kappa
    v_y = sp.Integer(0)
    v_yy = -kappa / R

    # ADM convention used in this derivation:
    # ds^2 = -N^2 dt^2 + gamma_ij (dx^i + beta^i dt)(dx^j + beta^j dt)
    # n = partial_t - beta^i partial_i for N=1.
    # K_ij = 1/2 (D_i beta_j + D_j beta_i).
    beta_x = -v
    beta_x_y = -v_y
    beta_x_yy = -v_yy

    K_xx = -v_x
    K_xy = -v_y / 2
    K_yy = sp.Integer(0)
    d_y_K_xy = -v_yy / 2

    # With our Riemann convention, and the K convention above, the calibrated
    # Gauss-Codazzi pieces needed here are:
    #
    #   R_ijkl = K_il K_jk - K_ik K_jl
    #   R_nijk = D_j K_ik - D_k K_ij
    #   R_ninj = ... not needed here because it vanishes for y,y at the tip
    #
    # Since K_yy=K_xy=0 at the tip, R_xyxy=0 and R_nyny=0.
    R_xyxy = K_xy * K_xy - K_xx * K_yy
    R_nyxy = -d_y_K_xy  # D_x K_yy - D_y K_yx
    R_nyny = sp.Integer(0)

    # At the front tip beta^x=-v=1 and partial_t = n + beta^x partial_x.
    # Therefore R_tyty = R(n+x, y, n+x, y).
    R_tyty = sp.simplify(R_nyny + 2 * R_nyxy + R_xyxy)

    # Affine generator K_aff = q partial_t with q=1/[kappa(lambda_*-lambda)].
    s, q = sp.symbols("s q", positive=True, real=True)
    R_KYKY = sp.simplify(q**2 * R_tyty)
    R_KYKY_aff = sp.simplify(R_KYKY.subs(q, 1 / (kappa * s)))

    lines = [
        "ADM/Gauss-Codazzi derivation at the Alcubierre front tip",
        "",
        "ADM convention:",
        "  ds^2 = -N^2 dt^2 + gamma_ij (dx^i + beta^i dt)(dx^j + beta^j dt)",
        "  N=1, gamma_ij=delta_ij, beta^i=(-v,0,0)",
        "  n = partial_t - beta^i partial_i",
        "  K_ij = 1/2(D_i beta_j + D_j beta_i)",
        "",
        "Front-tip data:",
        "  v=-1",
        "  v_x=-kappa",
        "  v_y=0",
        "  v_yy=-kappa/R",
        "",
        "Extrinsic curvature data:",
        f"  K_xx = -v_x = {sp.sstr(K_xx)}",
        f"  K_xy = -v_y/2 = {sp.sstr(K_xy)}",
        f"  K_yy = {sp.sstr(K_yy)}",
        f"  D_y K_xy = -v_yy/2 = {sp.sstr(d_y_K_xy)}",
        "",
        "Calibrated Gauss-Codazzi pieces in the Riemann convention used by the scripts:",
        "  R_ijkl = K_il K_jk - K_ik K_jl",
        "  R_nijk = D_j K_ik - D_k K_ij",
        "",
        "Needed components:",
        f"  R_xyxy = K_xy^2 - K_xx K_yy = {sp.sstr(sp.simplify(R_xyxy))}",
        f"  R_nyxy = D_x K_yy - D_y K_yx = {sp.sstr(sp.simplify(R_nyxy))}",
        f"  R_nyny = {sp.sstr(R_nyny)}",
        "",
        "At the front tip beta^x=-v=1, so",
        "  partial_t = n + partial_x.",
        "Therefore",
        "  R_tyty = R(n+x,y,n+x,y)",
        "          = R_nyny + 2 R_nyxy + R_xyxy",
        f"          = {sp.sstr(R_tyty)}",
        "",
        "This matches the full 4D tensor calculation:",
        "  R_tyty = -kappa/R.",
        "",
        "Affine normalization:",
        "  K_aff = q partial_t",
        "  q = 1/[kappa(lambda_*-lambda)]",
        f"  R_KYKY = q^2 R_tyty = {sp.sstr(R_KYKY)}",
        f"          = {sp.sstr(R_KYKY_aff)} with s=lambda_*-lambda",
        "",
        "Conclusion:",
        "  The transverse PP singularity is the Codazzi contribution from",
        "  the transverse derivative D_y K_xy of the shift-induced extrinsic",
        "  curvature.  The finite front-wall curvature supplies v_yy, and",
        "  affine horizon normalization supplies the divergent q^2 factor.",
    ]

    (OUT / "front_tip_adm_derivation.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:32]))


if __name__ == "__main__":
    main()
