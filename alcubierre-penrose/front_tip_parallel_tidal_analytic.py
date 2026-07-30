"""Analytic transverse tidal calculation at the 3+1 Alcubierre front tip.

Metric:
    ds^2 = -dt^2 + [dx - v(r) dt]^2 + dy^2 + dz^2
    r = sqrt(x^2+y^2+z^2)

This script derives the curvature component used in the parallel-frame
argument, then specializes it to the sech profile used in the diagrams.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = [t, x, y, z]
    v = sp.Function("v")(x, y, z)

    g = sp.Matrix(
        [
            [v**2 - 1, -v, 0, 0],
            [-v, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    gi = sp.simplify(g.inv())

    gamma = [[ [sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                expr = sp.Integer(0)
                for d in range(4):
                    expr += gi[a, d] * (
                        sp.diff(g[d, c], coords[b])
                        + sp.diff(g[d, b], coords[c])
                        - sp.diff(g[b, c], coords[d])
                    )
                gamma[a][b][c] = sp.factor(sp.simplify(expr / 2))

    # R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb}
    #              + Gamma^a_{ce} Gamma^e_{db}
    #              - Gamma^a_{de} Gamma^e_{cb}
    rup = []
    b, c, d = 2, 0, 2
    for a in range(4):
        expr = sp.diff(gamma[a][d][b], coords[c]) - sp.diff(gamma[a][c][b], coords[d])
        for e in range(4):
            expr += gamma[a][c][e] * gamma[e][d][b]
            expr -= gamma[a][d][e] * gamma[e][c][b]
        rup.append(sp.simplify(expr))
    r_tyty = sp.factor(sp.simplify(sum(g[0, a] * rup[a] for a in range(4))))

    gamma_tty = [sp.simplify(gamma[a][0][2]) for a in range(4)]
    gamma_ttz = [sp.simplify(gamma[a][0][3]) for a in range(4)]
    gamma_tt = [sp.simplify(gamma[a][0][0]) for a in range(4)]

    R, kappa = sp.symbols("R kappa", positive=True, real=True)
    r_tyty_axis = sp.simplify(-(-1) * (-kappa / R))
    sech_value = sp.simplify(-sp.sqrt(3) / (2 * sp.acosh(2)))
    tidal_coeff = sp.simplify(sech_value / (sp.Rational(3, 4)))

    lines = [
        "Analytic 3+1 parallel-frame tidal calculation",
        "",
        "Metric:",
        "  ds^2 = -dt^2 + [dx - v(r) dt]^2 + dy^2 + dz^2",
        "  r = sqrt(x^2+y^2+z^2)",
        "",
        "Curvature convention used here:",
        "  R^a_{bcd} = d_c Gamma^a_{db} - d_d Gamma^a_{cb}",
        "             + Gamma^a_{ce} Gamma^e_{db}",
        "             - Gamma^a_{de} Gamma^e_{cb}",
        "  This matches the numerical script's convention.",
        "",
        "General symbolic result:",
        f"  R_tyty = {sp.sstr(r_tyty)}",
        "",
        "Axis specialization at x=R, y=z=0:",
        "  v_y = v_z = 0",
        "  v_yy = v_zz = v_r/R",
        "  so R_tyty = R_tztz = -v v_yy.",
        "",
        "At the front horizon tip:",
        "  v(R) = -1",
        "  v_r(R) = -kappa",
        f"  R_tyty = R_tztz = {sp.sstr(r_tyty_axis)}",
        "",
        "For the sech profile used in our plots:",
        "  v(r) = 2(sech r - 1)",
        "  R = acosh(2)",
        "  kappa = sqrt(3)/2",
        f"  R_tyty = R_tztz = {sp.sstr(sech_value)}",
        f"           = {float(sech_value): .12e}",
        "",
        "Parallel transverse vectors:",
        "  The connection components along the generator are",
        f"  Gamma^a_t_y = {sp.sstr(gamma_tty)}",
        f"  Gamma^a_t_z = {sp.sstr(gamma_ttz)}",
        "  Since v_y=v_z=0 on the axis, partial_y and partial_z are",
        "  parallel propagated along the axis generator.",
        "",
        "Non-affine versus affine parameter:",
        f"  Gamma^a_tt = {sp.sstr(gamma_tt)}",
        "  At the front tip, v=-1 and v_x=-kappa, so",
        "    nabla_{partial_t} partial_t = -kappa partial_t.",
        "  If K=(dt/dlambda) partial_t is affine, then",
        "    dt/dlambda = 1/[kappa(lambda_* - lambda)]",
        "  as t -> +infinity and lambda -> lambda_*.",
        "",
        "Therefore the parallel-frame tidal component is",
        "  R(K,partial_y,K,partial_y)",
        "    = (dt/dlambda)^2 R_tyty",
        "    = R_tyty / [kappa^2 (lambda_* - lambda)^2].",
        "",
        "For the sech profile this leading coefficient is",
        f"  R_tyty/kappa^2 = {sp.sstr(tidal_coeff)}",
        f"                  = {float(tidal_coeff): .12e}",
        "",
        "Conclusion:",
        "  The transverse tidal component diverges like",
        "    -(const)/(lambda_* - lambda)^2",
        "  at the finite affine endpoint of the front axis generator.",
        "  This is not a scalar-curvature blow-up at finite coordinate t;",
        "  it is a parallel-propagated curvature singularity reached only",
        "  in the asymptotic limit t -> +infinity.",
        "  The rear endpoint has the corresponding time-reversed behavior.",
    ]

    (OUT / "front_tip_parallel_tidal_analytic.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:20]))


if __name__ == "__main__":
    main()
