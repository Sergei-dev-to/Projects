"""Tipler/Krolak-style singularity-strength bookkeeping for the front tip."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    s, A, C1, C2 = sp.symbols("s A C_1 C_2", positive=True, real=True)
    p = sp.symbols("p", real=True)

    indicial = sp.factor(p * (p - 1) - A)
    p_plus = sp.simplify((1 + sp.sqrt(1 + 4 * A)) / 2)
    p_minus = sp.simplify((1 - sp.sqrt(1 + 4 * A)) / 2)

    eps = sp.symbols("epsilon", positive=True)
    u = sp.symbols("u", positive=True)
    single = sp.integrate(A / s**2, (s, eps, 1))
    inner = sp.integrate(A / s**2, (s, u, 1))
    double = sp.integrate(inner, (u, eps, 1))

    A1 = C1 / sp.symbols("kappa", positive=True)
    A2 = C2 / sp.symbols("kappa", positive=True)

    lines = [
        "Tipler/Krolak-style strength bookkeeping for the front-tip PP singularity",
        "",
        "Definitions used in this note:",
        "  s = lambda_* - lambda",
        "  R_KYKY = -A_y/s^2",
        "  R_KZKZ = -A_z/s^2",
        "  A_y,A_z>0 for a smooth convex front cap.",
        "",
        "For the spherical case:",
        "  A_y = A_z = A = 1/(kappa R).",
        "",
        "For the general convex front cap:",
        f"  A_y = {sp.sstr(A1)}",
        f"  A_z = {sp.sstr(A2)}",
        "  where C_1,C_2 are principal curvatures of the wall tip.",
        "",
        "Curvature integrals in one transverse channel:",
        f"  int_epsilon^1 A/s^2 ds = {sp.sstr(single)}",
        f"  int_epsilon^1 du int_u^1 A/s^2 ds = {sp.sstr(double)}",
        "  Thus the single integral diverges like A/epsilon.",
        "  The double integral diverges like A log(1/epsilon).",
        "",
        "Jacobi equation in each transverse channel:",
        "  eta'' = A eta/s^2",
        "  eta ~ s^p gives",
        f"    {sp.sstr(indicial)} = 0",
        f"    p_+ = {sp.sstr(p_plus)}",
        f"    p_- = {sp.sstr(p_minus)}",
        "",
        "Since A>0:",
        "  p_+ > 1 and p_- < 0.",
        "  The shrinking solution behaves as s^p_+.",
        "  The independent generic solution behaves as s^p_- and diverges.",
        "",
        "Two-screen area behavior:",
        "  In the spherical case both transverse channels have the same exponents.",
        "  A generic screen area contains products involving the divergent mode,",
        "  so it diverges rather than approaching a finite nonzero regular limit.",
        "  A special choice of Jacobi fields can be tuned onto the shrinking modes,",
        "  with area ~ s^(2 p_+) -> 0.",
        "",
        "Interpretation:",
        "  The transverse tidal channel has both divergent single and double",
        "  curvature integrals.  In the common integral-test language this is",
        "  strong curvature behavior.",
        "  The Jacobi equations show that the transverse screen is not regular:",
        "  generic separations are infinitely stretched, while a tuned pair is",
        "  crushed to zero area.",
        "  Therefore this is a deformationally strong null PP singularity.",
        "  If one reserves the phrase Tipler-strong strictly for generic",
        "  crushing of all transverse volume/area elements to zero, this",
        "  singularity should be described as stretching-strong rather than",
        "  Tipler-crushing.",
        "",
        "Conclusion:",
        "  The front endpoint is a strong null PP-curvature singularity with",
        "  divergent transverse curvature integrals and generic infinite",
        "  stretching.  This strengthens, but is separate from, the",
        "  C^2-inextendibility statement.",
    ]

    (OUT / "front_tip_tipler_krolak.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:28]))


if __name__ == "__main__":
    main()
