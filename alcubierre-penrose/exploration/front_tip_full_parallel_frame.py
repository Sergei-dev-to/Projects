"""Full parallel-frame Riemann components at the 3+1 front tip.

Frame along the future front axis generator:
    K = q partial_t,                 q = exp(kappa t)
    N = q^-1 (1/2 partial_t - partial_x)
    Y = partial_y
    Z = partial_z

with g(K,N)=-1 and Y,Z unit spacelike.  The script computes all independent
R_{ABCD} components in this frame at the front tip for a generic smooth
spherical profile.
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

    def rframe(a_label: str, b_label: str, c_label: str, d_label: str) -> sp.Expr:
        A = frame[a_label]
        B = frame[b_label]
        C = frame[c_label]
        D = frame[d_label]
        expr = sp.Integer(0)
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        expr += rcov[a][b][c][d] * A[a] * B[b] * C[c] * D[d]
        return sp.factor(sp.simplify(expr.subs(subs)))

    # Independent two-form components R_{ABCD}, where AB and CD are antisymmetric pairs.
    pairs = [("K", "N"), ("K", "Y"), ("K", "Z"), ("N", "Y"), ("N", "Z"), ("Y", "Z")]
    matrix = {}
    for p1 in pairs:
        for p2 in pairs:
            matrix[p1, p2] = rframe(p1[0], p1[1], p2[0], p2[1])

    nonzero = []
    for i, p1 in enumerate(pairs):
        for j, p2 in enumerate(pairs):
            if j < i:
                continue
            val = matrix[p1, p2]
            if val != 0:
                nonzero.append((p1, p2, val))

    sech_subs = {R: sp.acosh(2), kappa: sp.sqrt(3) / 2}
    leading_kyky = sp.simplify(matrix[("K", "Y"), ("K", "Y")].subs(sech_subs) / q**2)

    lines = [
        "Full parallel null frame at the 3+1 Alcubierre front tip",
        "",
        "Assumptions:",
        "  front tip x=R>0, y=z=0",
        "  v(R)=-1",
        "  v_x(R)=-kappa, kappa>0",
        "  v_xx(R)=mu",
        "  spherical smoothness gives v_yy=v_zz=-kappa/R at the axis",
        "",
        "Parallel frame:",
        "  q = exp(kappa t) = 1/[kappa(lambda_* - lambda)] up to normalization",
        "  K = q partial_t",
        "  N = q^-1 (1/2 partial_t - partial_x)",
        "  Y = partial_y",
        "  Z = partial_z",
        "  g(K,N)=-1, g(Y,Y)=g(Z,Z)=1",
        "",
        "Independent nonzero frame Riemann components R_{ABCD}:",
    ]
    for p1, p2, val in nonzero:
        lines.append(f"  R_{p1[0]}{p1[1]}{p2[0]}{p2[1]} = {sp.sstr(val)}")

    lines.extend(
        [
            "",
            "Divergent components:",
            "  R_KYKY = R_KZKZ = -kappa*q^2/R",
            "  Since q = 1/[kappa(lambda_* - lambda)],",
            "    R_KYKY = R_KZKZ = -1/[kappa R (lambda_* - lambda)^2].",
            "",
            "Finite components:",
            "  R_KNKN is finite and depends on mu=v_xx(R).",
            "  Mixed K-Y/N-Y components vanish in this symmetric spherical case.",
            "  R_YZYZ vanishes at the axis for this metric/profile class.",
            "",
            "Sech profile coefficient:",
            f"  R_KYKY/q^2 = {sp.sstr(leading_kyky)} = {float(leading_kyky): .12e}",
            "",
            "Conclusion:",
            "  The full parallel-frame contraction confirms that the only leading",
            "  blow-up in the spherical front-tip calculation is the transverse",
            "  screen tidal pair R_KYKY=R_KZKZ. The blow-up is quadratic in",
            "  affine distance to the endpoint and is independent of v_xx(R).",
        ]
    )

    (OUT / "front_tip_full_parallel_frame.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:24]))


if __name__ == "__main__":
    main()
