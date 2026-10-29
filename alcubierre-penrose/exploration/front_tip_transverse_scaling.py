"""Test scaled transverse coordinates for the 3+1 front-tip extension."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def coeff(expr: sp.Expr, a: sp.Symbol, b: sp.Symbol) -> sp.Expr:
    if a == b:
        return sp.expand(expr).coeff(a, 2)
    return sp.expand(expr).coeff(a, 1).coeff(b, 1) / 2


def metric_with_scaling(power: int) -> dict[tuple[sp.Symbol, sp.Symbol], sp.Expr]:
    U, V, E, N, R, k = sp.symbols("U V E N R k", nonzero=True, real=True)
    dU, dV, dE, dN = sp.symbols("dU dV dE dN", real=True)

    Y = V**power * E
    Z = V**power * N
    dY = sp.diff(Y, U) * dU + sp.diff(Y, V) * dV + sp.diff(Y, E) * dE + sp.diff(Y, N) * dN
    dZ = sp.diff(Z, U) * dU + sp.diff(Z, V) * dV + sp.diff(Z, E) * dE + sp.diff(Z, N) * dN

    rho2 = Y * Y + Z * Z
    s = -U * V
    ds = sp.diff(s, U) * dU + sp.diff(s, V) * dV
    xi = s - rho2 / (2 * R)
    dxi = (
        sp.diff(xi, U) * dU
        + sp.diff(xi, V) * dV
        + sp.diff(xi, E) * dE
        + sp.diff(xi, N) * dN
    )
    dt = (dU / U - ds / s) / k
    v = -1 - k * s
    form = sp.expand(-dt**2 + (dxi - v * dt) ** 2 + dY**2 + dZ**2)
    vars_ = [dU, dV, dE, dN]
    return {(a, b): sp.simplify(coeff(form, a, b)) for i, a in enumerate(vars_) for b in vars_[i:]}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    U, V, E, N, R, k = sp.symbols("U V E N R k", nonzero=True, real=True)
    dU, dV, dE, dN = sp.symbols("dU dV dE dN", real=True)

    lines = [
        "Front-tip transverse scaling test",
        "",
        "Starting issue with naive transverse coordinates:",
        "  g_VY ~ Y/(R V kappa), so fixed Y gives a divergence as V->0.",
        "",
        "Test scalings:",
        "  Y = V^p eta",
        "  Z = V^p zeta",
        "",
        "A smooth nondegenerate 4D chart needs:",
        "  no negative powers of V in metric components",
        "  transverse metric in eta,zeta not collapsing to rank zero at V=0.",
    ]

    for p in [1, 2]:
        g = metric_with_scaling(p)
        lines.extend(["", f"Scaling p={p}: Y=V^{p} eta, Z=V^{p} zeta"])
        for key in [(dU, dU), (dU, dV), (dV, dV), (dV, dE), (dE, dE), (dE, dN), (dN, dN)]:
            expr = sp.factor(g[key])
            lines.append(f"  g_{key[0]}{key[1]} = {sp.sstr(expr)}")
        lines.append(
            "  transverse determinant scale ~ "
            + sp.sstr(sp.factor(g[(dE, dE)] * g[(dN, dN)] - g[(dE, dN)] ** 2))
        )

    lines.extend(
        [
            "",
            "Interpretation:",
            "  p=1 removes the explicit Y/V divergence because Y/V=eta, but",
            "  the transverse metric components scale like V^2 and vanish at V=0.",
            "  The chart collapses transverse directions at the endpoint.",
            "",
            "  Larger p removes divergences even more strongly but collapses the",
            "  transverse metric faster.",
            "",
            "Conclusion:",
            "  Simple scalings Y=V^p eta do not give a nondegenerate smooth 4D",
            "  endpoint chart. They either leave the naive chart singular (p=0)",
            "  or collapse the transverse two-metric at the endpoint (p>=1).",
            "",
            "Implication:",
            "  The 1+1 C+ extension appears to be an axis/separatrix extension,",
            "  not a straightforward smooth 3+1 manifold extension with a regular",
            "  transverse neighborhood.",
        ]
    )

    (OUT / "front_tip_transverse_scaling.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()
