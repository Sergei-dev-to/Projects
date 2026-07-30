"""Local 3+1 expansion near the front Alcubierre tip.

This checks whether the 1+1 endpoint variable can be lifted naively to the
real 3+1 metric near x=r2, y=z=0.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    xi, y, z, r2, kappa, v2 = sp.symbols("xi y z r2 kappa v2", positive=True, real=True)
    rho2 = y * y + z * z
    r = sp.sqrt((r2 + xi) ** 2 + rho2)

    # Multivariate expansion in small xi,y,z through the terms relevant for
    # the horizon distance.  We expand sqrt(r2^2 + 2r2 xi + xi^2 + rho2).
    eps = sp.symbols("eps", real=True)
    r_eps = sp.sqrt((r2 + eps * xi) ** 2 + eps * eps * rho2)
    r_series = sp.series(r_eps, eps, 0, 4).removeO().subs(eps, 1)
    s_series = sp.simplify(r_series - r2)

    # At the front tip v(r2)=-1 and v'(r2)=-kappa in the 1+1 sign convention.
    s = sp.symbols("s", real=True)
    v_expansion = -1 - kappa * s + sp.Rational(1, 2) * v2 * s * s
    one_plus_v = sp.expand(v_expansion + 1).subs(s, s_series)

    lines = [
        "3+1 front-tip expansion",
        "",
        "Coordinates near the front tip:",
        "  x = r2 + xi",
        "  rho^2 = y^2 + z^2",
        "  r = sqrt((r2+xi)^2 + rho^2)",
        "",
        "Expansion of radial distance s = r-r2:",
        f"  s = {sp.sstr(s_series)} + O(4)",
        "",
        "Leading terms:",
        "  s = xi + (y^2+z^2)/(2 r2) + higher terms",
        "",
        "Front horizon behavior:",
        "  v(r2) = -1",
        "  v'(r2) = -kappa",
        "  1+v(r) = -kappa s + O(s^2)",
        "",
        "Substituting the 3+1 expansion:",
        f"  1+v = {sp.sstr(one_plus_v)} + higher terms",
        "",
        "Implication for lifting the 1+1 endpoint variable:",
        "  In 1+1, the horizon distance is xi ~ X where X is the oriented UV branch.",
        "  In 3+1, the horizon distance is",
        "    s = xi + rho^2/(2 r2) + ...",
        "  so the natural local branch condition is",
        "    X ~ xi + rho^2/(2 r2), not xi alone.",
        "",
        "This is the key obstruction/rule:",
        "  Keeping ordinary transverse coordinates y,z while continuing X through",
        "  zero forces xi = X - rho^2/(2r2) + ... .",
        "  For fixed nonzero rho, X=0 is not the front tip; it is a nearby point",
        "  on the spherical wall r=r2.",
        "",
        "Therefore the 1+1 C+ point does not lift to a codimension-one edge in",
        "the same way. The real 3+1 issue is concentrated at rho=0, matching the",
        "Warp Drive Aerodynamics result that the Cauchy behavior is pointlike at",
        "the front tip for a smooth convex bubble.",
        "",
        "Next implication:",
        "  A smooth 3+1 extension cannot be obtained by blindly applying the 1+1",
        "  U,V transformation at every transverse point. One must build a local",
        "  tip chart that treats rho as part of the expansion of s=r-r2.",
    ]
    (OUT / "front_tip_3p1_expansion.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()
