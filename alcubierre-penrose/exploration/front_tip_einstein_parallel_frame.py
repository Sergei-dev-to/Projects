"""Einstein tensor in the front-tip parallel frame.

This checks whether the stress-energy supporting the 3+1 Alcubierre metric has
divergent components in the same affine parallel frame where the Riemann tensor
has a PP-curvature singularity.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    t, x, y, z = sp.symbols("t x y z", real=True)
    kappa, R, mu, q = sp.symbols("kappa R mu q", positive=True, real=True)
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

    ric = [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            expr = sp.Integer(0)
            for c in range(4):
                expr += sp.diff(gamma[c][b][a], coords[c])
                expr -= sp.diff(gamma[c][c][a], coords[b])
                for d in range(4):
                    expr += gamma[c][c][d] * gamma[d][b][a]
                    expr -= gamma[c][b][d] * gamma[d][c][a]
            ric[a][b] = sp.simplify(expr)

    scalar = sp.simplify(sum(gi[a, b] * ric[a][b] for a in range(4) for b in range(4)))
    ein = [[sp.simplify(ric[a][b] - sp.Rational(1, 2) * g[a, b] * scalar) for b in range(4)] for a in range(4)]

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

    frame = {
        "K": sp.Matrix([q, 0, 0, 0]),
        "N": sp.Matrix([sp.Rational(1, 2) / q, -1 / q, 0, 0]),
        "Y": sp.Matrix([0, 0, 1, 0]),
        "Z": sp.Matrix([0, 0, 0, 1]),
    }
    labels = ["K", "N", "Y", "Z"]

    def eframe(a_label: str, b_label: str) -> sp.Expr:
        A = frame[a_label]
        B = frame[b_label]
        expr = sp.Integer(0)
        for a in range(4):
            for b in range(4):
                expr += ein[a][b] * A[a] * B[b]
        return sp.factor(sp.simplify(expr.subs(subs)))

    components = {}
    for i, a in enumerate(labels):
        for b in labels[i:]:
            components[a, b] = eframe(a, b)

    nonzero = [(a, b, val) for (a, b), val in components.items() if val != 0]
    sech_subs = {R: sp.acosh(2), kappa: sp.sqrt(3) / 2}
    gkk_coeff = sp.simplify(components["K", "K"].subs(sech_subs) / q**2)

    lines = [
        "Einstein tensor in the front-tip parallel frame",
        "",
        "Assumptions:",
        "  front tip x=R>0, y=z=0",
        "  v(R)=-1",
        "  v_x(R)=-kappa, kappa>0",
        "  v_xx(R)=mu",
        "  spherical smoothness gives v_yy=v_zz=-kappa/R",
        "",
        "Parallel frame:",
        "  K = q partial_t",
        "  N = q^-1 (1/2 partial_t - partial_x)",
        "  Y = partial_y",
        "  Z = partial_z",
        "  q = 1/[kappa(lambda_* - lambda)] up to normalization",
        "",
        "Independent nonzero frame Einstein components G_AB:",
    ]
    for a, b, val in nonzero:
        lines.append(f"  G_{a}{b} = {sp.sstr(val)}")

    lines.extend(
        [
            "",
            "Divergent stress-energy channel:",
            "  If T_AB = G_AB/(8*pi), then",
            "    T_KK = -2*kappa*q^2/R / (8*pi)",
            "         = -1/[4*pi*kappa R (lambda_* - lambda)^2].",
            "",
            "Interpretation:",
            "  The affine null energy density measured along the incomplete",
            "  generator diverges in the same transverse-curvature channel as",
            "  the PP Riemann component.",
            "  The divergence is independent of mu=v_xx(R).",
            "",
            "Sech profile coefficient:",
            f"  G_KK/q^2 = {sp.sstr(gkk_coeff)} = {float(gkk_coeff): .12e}",
        ]
    )

    (OUT / "front_tip_einstein_parallel_frame.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:24]))


if __name__ == "__main__":
    main()
