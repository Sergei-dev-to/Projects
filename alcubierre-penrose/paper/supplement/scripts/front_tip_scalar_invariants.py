"""Scalar invariant check at the 3+1 front tip.

This contrasts finite scalar polynomial invariants at the finite coordinate
tip with divergent parallel-propagated frame components along the incomplete
null generator.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    t, x, y, z = sp.symbols("t x y z", real=True)
    kappa, R, mu = sp.symbols("kappa R mu", positive=True, real=True)
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

    gamma = [[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)]
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
                gamma[a][b][c] = sp.simplify(expr / 2)

    rup = [[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    expr = sp.diff(gamma[a][d][b], coords[c]) - sp.diff(gamma[a][c][b], coords[d])
                    for e in range(4):
                        expr += gamma[a][c][e] * gamma[e][d][b]
                        expr -= gamma[a][d][e] * gamma[e][c][b]
                    rup[a][b][c][d] = sp.simplify(expr)

    rcov = [[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    rcov[a][b][c][d] = sp.simplify(sum(g[a, e] * rup[e][b][c][d] for e in range(4)))

    ric = [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            ric[a][b] = sp.simplify(sum(rup[c][a][c][b] for c in range(4)))

    scalar = sp.simplify(sum(gi[a, b] * ric[a][b] for a in range(4) for b in range(4)))
    ein = [[sp.simplify(ric[a][b] - sp.Rational(1, 2) * g[a, b] * scalar) for b in range(4)] for a in range(4)]

    # Raise indices.
    ric_up = [[sp.simplify(sum(gi[a, c] * gi[b, d] * ric[c][d] for c in range(4) for d in range(4))) for b in range(4)] for a in range(4)]
    ein_up = [[sp.simplify(sum(gi[a, c] * gi[b, d] * ein[c][d] for c in range(4) for d in range(4))) for b in range(4)] for a in range(4)]
    rup4 = [[[[sp.simplify(sum(gi[a, e] * gi[b, f] * gi[c, h] * gi[d, i] * rcov[e][f][h][i] for e in range(4) for f in range(4) for h in range(4) for i in range(4))) for d in range(4)] for c in range(4)] for b in range(4)] for a in range(4)]

    ricci2 = sp.simplify(sum(ric[a][b] * ric_up[a][b] for a in range(4) for b in range(4)))
    einstein2 = sp.simplify(sum(ein[a][b] * ein_up[a][b] for a in range(4) for b in range(4)))
    kretsch = sp.simplify(
        sum(
            rcov[a][b][c][d] * rup4[a][b][c][d]
            for a in range(4)
            for b in range(4)
            for c in range(4)
            for d in range(4)
        )
    )
    # Weyl^2 = Riemann^2 - 2 Ricci^2 + R^2/3 in four dimensions.
    weyl2 = sp.simplify(kretsch - 2 * ricci2 + scalar**2 / 3)

    subs = {
        v: -1,
        sp.diff(v, x): -kappa,
        sp.diff(v, y): 0,
        sp.diff(v, z): 0,
        sp.diff(v, x, x): mu,
        sp.diff(v, x, y): 0,
        sp.diff(v, x, z): 0,
        sp.diff(v, y, y): -kappa / R,
        sp.diff(v, y, z): 0,
        sp.diff(v, z, z): -kappa / R,
    }

    invariants = {
        "R": sp.factor(sp.simplify(scalar.subs(subs))),
        "Ricci2": sp.factor(sp.simplify(ricci2.subs(subs))),
        "Kretschmann": sp.factor(sp.simplify(kretsch.subs(subs))),
        "Weyl2": sp.factor(sp.simplify(weyl2.subs(subs))),
        "Einstein2": sp.factor(sp.simplify(einstein2.subs(subs))),
    }

    sech_subs = {R: sp.acosh(2), kappa: sp.sqrt(3) / 2, mu: sp.Rational(1, 2)}
    # For v(r)=2(sech r - 1), v''(acosh(2)) = 1/2.
    sech_vals = {name: sp.simplify(val.subs(sech_subs)) for name, val in invariants.items()}

    lines = [
        "Scalar polynomial invariants at the 3+1 Alcubierre front tip",
        "",
        "Assumptions:",
        "  front tip x=R>0, y=z=0",
        "  v(R)=-1",
        "  v_x(R)=-kappa, kappa>0",
        "  v_xx(R)=mu",
        "  spherical smoothness gives v_yy=v_zz=-kappa/R",
        "",
        "Generic symbolic scalar invariants:",
    ]
    for name, val in invariants.items():
        lines.append(f"  {name} = {sp.sstr(val)}")

    lines.extend(
        [
            "",
            "These are signed Lorentzian contractions; Ricci2, Kretschmann,",
            "and Einstein2 are not positive-definite norms.",
            "",
            "Sech profile values:",
        ]
    )
    for name, val in sech_vals.items():
        lines.append(f"  {name} = {sp.sstr(val)} = {float(val): .12e}")

    lines.extend(
        [
            "",
            "Contrast with PP curvature:",
            "  The scalar invariants above are finite at the finite coordinate tip.",
            "  Along the incomplete affine generator, however,",
            "    K = q partial_t, q = 1/[kappa(lambda_* - lambda)],",
            "  and",
            "    R_KYKY = R_KZKZ = -kappa*q^2/R",
            "             = -1/[kappa R (lambda_* - lambda)^2].",
            "",
            "Conclusion:",
            "  The front endpoint singularity is invisible to these scalar",
            "  polynomial curvature invariants.  It is a non-scalar",
            "  parallel-propagated curvature singularity.",
        ]
    )

    (OUT / "front_tip_scalar_invariants.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:22]))


if __name__ == "__main__":
    main()
