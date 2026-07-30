"""Near-tip 3+1 metric lift test for the front C+ extension.

This substitutes a Kruskal-like endpoint ansatz into the 3+1 Alcubierre
metric near the front tip and records whether the leading metric components
are finite.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def coeff(expr: sp.Expr, a: sp.Symbol, b: sp.Symbol) -> sp.Expr:
    if a == b:
        return sp.expand(expr).coeff(a, 2)
    return sp.expand(expr).coeff(a, 1).coeff(b, 1) / 2


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    U, V, Y, Z, R, k = sp.symbols("U V Y Z R k", nonzero=True, real=True)
    dU, dV, dY, dZ = sp.symbols("dU dV dY dZ", real=True)

    rho2 = Y**2 + Z**2
    # Oriented horizon distance s=r-r2.  Constants from the exact branch
    # relation are irrelevant for the singularity check, so use s=-UV.
    s = -U * V
    ds = sp.diff(s, U) * dU + sp.diff(s, V) * dV

    # Front-tip spatial relation:
    #   s = xi + rho^2/(2R)+...
    # so xi = s - rho^2/(2R)+... .
    xi = s - rho2 / (2 * R)
    dxi = sp.diff(xi, U) * dU + sp.diff(xi, V) * dV + sp.diff(xi, Y) * dY + sp.diff(xi, Z) * dZ

    # Correct leading endpoint differential relations:
    #   U=exp(k u),  dU/U = k dt + ds/s
    #   V=exp(-k w), dV/V = -k dt - k ds/(1-v)
    # The naive dt=(dU/U-dV/V)/(2k) misses the ds/(1-v) term and fails
    # even in the 1+1 sector.
    q = 2 + k * s  # 1-v to first order when v=-1-k s
    dt = (dU / U - ds / s) / k

    # v=-1-k s+O(s^2) at the front tip.
    v = -1 - k * s
    form = -dt**2 + (dxi - v * dt) ** 2 + dY**2 + dZ**2
    form = sp.expand(form)

    vars_ = [dU, dV, dY, dZ]
    g = {}
    for i, vi in enumerate(vars_):
        for j, vj in enumerate(vars_[i:], start=i):
            g[(vi, vj)] = sp.simplify(coeff(form, vi, vj))

    gUU_axis = sp.simplify(g[(dU, dU)].subs({Y: 0, Z: 0}))
    gVV_axis = sp.simplify(g[(dV, dV)].subs({Y: 0, Z: 0}))

    lines = [
        "Front-tip 3+1 metric lift test",
        "",
        "Ansatz:",
        "  s = r-r2 = -U V at leading branch order",
        "  dU/U = kappa dt + ds/s",
        "  dV/V = -kappa dt - kappa ds/(1-v)",
        "  xi = x-r2 = s - (Y^2+Z^2)/(2 r2) + higher terms",
        "  y=Y, z=Z",
        "  v = -1 - kappa s + O(s^2)",
        "",
        "Metric tested:",
        "  ds^2 = -dt^2 + [dxi - v dt]^2 + dY^2 + dZ^2",
        "",
        "Axis 1+1 cancellation:",
        f"  g_UU on Y=Z=0 = {sp.sstr(gUU_axis)}",
        f"  g_VV on Y=Z=0 = {sp.sstr(gVV_axis)}",
        "",
        "Leading metric coefficients:",
    ]
    for key in [(dU, dU), (dU, dV), (dV, dV), (dU, dY), (dV, dY), (dY, dY), (dY, dZ), (dZ, dZ)]:
        lines.append(f"  g_{key[0]}{key[1]} = {sp.sstr(sp.simplify(g[key]))}")

    lines.extend(
        [
            "",
            "Interpretation:",
            "  With the corrected endpoint differential, the 1+1 axis sector has",
            "  finite leading coefficients.",
            "  However, with ordinary transverse coordinates Y,Z the mixed terms",
            "  g_UY and g_VY still contain Y/U or Y/V factors unless transverse",
            "  coordinates vanish with the endpoint variables.",
            "  Therefore the naive lift y=Y,z=Z is not a smooth 3+1 endpoint chart",
            "  for a full neighborhood of the tip.",
            "",
            "Consequence:",
            "  The 1+1 C+ extension is valid on the symmetry axis, but a real 3+1",
            "  extension needs a different blown-up/tip chart for transverse directions,",
            "  or it may fail to exist as a smooth manifold extension in ordinary",
            "  transverse coordinates.",
        ]
    )

    (OUT / "front_tip_metric_lift.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:18]))


if __name__ == "__main__":
    main()
