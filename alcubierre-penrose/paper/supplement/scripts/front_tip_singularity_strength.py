"""Generic front-tip PP curvature and Jacobi strength.

This turns the sech-specific front-tip calculation into a profile-independent
local statement for a smooth spherical Alcubierre bubble.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    lam, lam_star, R, kappa = sp.symbols("lambda lambda_* R kappa", positive=True)
    s = sp.symbols("s", positive=True)

    tidal = -1 / (kappa * R * (lam_star - lam) ** 2)

    # Jacobi equation in one transverse direction.  With this sign convention:
    #   D^2 eta / d lambda^2 = - R(K,e,K,e) eta
    # and R(K,e,K,e) = -A/s^2 with A = 1/(kappa R), s=lambda_*-lambda.
    A = sp.symbols("A", positive=True)
    p = sp.symbols("p")
    indicial = sp.factor(p * (p - 1) - A)
    p_plus = sp.simplify((1 + sp.sqrt(1 + 4 * A)) / 2)
    p_minus = sp.simplify((1 - sp.sqrt(1 + 4 * A)) / 2)

    # For the sech profile.
    A_sech = sp.simplify(2 / (sp.sqrt(3) * sp.acosh(2)))
    p_plus_sech = sp.simplify(p_plus.subs(A, A_sech))
    p_minus_sech = sp.simplify(p_minus.subs(A, A_sech))

    # Krolak and Tipler integrals for |R_KeKe| ~ A/s^2.
    eps = sp.symbols("epsilon", positive=True)
    single_integral = sp.integrate(A / s**2, (s, eps, 1))
    double_integral = sp.integrate(single_integral.subs(eps, sp.symbols("u", positive=True)), (sp.symbols("u", positive=True), eps, 1))

    lines = [
        "Generic 3+1 Alcubierre front-tip singularity strength",
        "",
        "Assumptions:",
        "  ds^2 = -dt^2 + [dx - v(r) dt]^2 + dy^2 + dz^2",
        "  r = sqrt(x^2+y^2+z^2)",
        "  front tip is x=R>0, y=z=0",
        "  v(R) = -1",
        "  v_r(R) = -kappa with kappa>0",
        "  v is smooth and spherical near r=R",
        "",
        "Profile-independent local curvature:",
        "  On the axis, v_y=0 and v_yy=v_r/R.",
        "  Since R_tyty = -v v_yy, at the front tip",
        "    R_tyty = -kappa/R.",
        "",
        "Affine scaling:",
        "  partial_t is the null horizon tangent but is not affine:",
        "    nabla_{partial_t} partial_t = -kappa partial_t.",
        "  Therefore",
        "    dt/dlambda = 1/[kappa(lambda_* - lambda)]",
        "  for a future-directed generator ending at lambda=lambda_*.",
        "",
        "Parallel-propagated tidal component:",
        "  e_y=partial_y and e_z=partial_z are parallel on the axis.",
        "  Hence",
        "    R(K,e_y,K,e_y)",
        f"      = {sp.sstr(tidal)}",
        "  This is generic for any smooth spherical profile with finite R and kappa>0.",
        "",
        "Jacobi equation:",
        "  Let s=lambda_* - lambda and A=1/(kappa R).",
        "  The transverse deviation equation is",
        "    d^2 eta/dlambda^2 = -R(K,e,K,e) eta",
        "  so near the endpoint",
        "    eta'' = A eta/s^2.",
        "  Trying eta ~ s^p gives",
        f"    {sp.sstr(indicial)} = 0",
        f"    p_+ = {sp.sstr(p_plus)}",
        f"    p_- = {sp.sstr(p_minus)}",
        "",
        "Behavior:",
        "  p_+ > 1 gives one Jacobi solution that shrinks to zero.",
        "  p_- < 0 gives an independent Jacobi solution that diverges.",
        "  So a generic transverse separation is infinitely stretched unless",
        "  tuned onto the shrinking mode.",
        "",
        "For the sech profile:",
        f"  A = 1/(kappa R) = {sp.sstr(A_sech)} = {float(A_sech):.12e}",
        f"  p_+ = {sp.sstr(p_plus_sech)} = {float(p_plus_sech):.12e}",
        f"  p_- = {sp.sstr(p_minus_sech)} = {float(p_minus_sech):.12e}",
        "",
        "Integrated-strength checks for this transverse channel:",
        "  For |R(K,e,K,e)| ~ A/s^2, with s -> 0:",
        f"    single integral int A/s^2 ds = {sp.sstr(single_integral)}",
        "    diverges like A/s.",
        "    double integral int int A/s^2 ds ds diverges logarithmically.",
        "",
        "Conclusion:",
        "  This is a genuine integrated tidal divergence in the transverse",
        "  screen directions, not a removable coordinate effect.",
        "  The front endpoint is a strong null PP-curvature singularity",
        "  in this transverse tidal channel.",
        "  That is enough to rule out a C^2 extension through the endpoint.",
        "  Mapping the result onto a specific Tipler/Krolak convention is",
        "  then a bookkeeping task: build the full parallel null frame and",
        "  evaluate the associated Jacobi area criterion in that convention.",
        "",
        "Scope:",
        "  This is a local result at the axis endpoint. It rules out smooth",
        "  C^2 extension there. It is not a statement about possible weaker",
        "  C^0-type extensions, and it does not require scalar polynomial",
        "  curvature invariants to diverge.",
    ]

    (OUT / "front_tip_singularity_strength.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:28]))


if __name__ == "__main__":
    main()
