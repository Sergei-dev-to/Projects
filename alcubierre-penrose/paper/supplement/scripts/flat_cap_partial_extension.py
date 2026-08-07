"""Symbolic check of the local Kruskal-product extension of a flat cap.

Near an exact planar cap, write s=x-x_H and

    v(s) = -1 - kappa*s + c2*s**2 + c3*s**3.

The future endpoint coordinates U=exp(-kappa*t), s=U*V should turn the
apparently incomplete stationary generator into a regular bifurcate-horizon
patch.  This script verifies smooth metric coefficients and nondegeneracy at
U=0.  The accompanying note proves that such a patch can be glued Hausdorffly
to a compact flat-capped bubble.  This script also checks the distinct
transverse-family curvature obstruction at the cap rim.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    U, V = sp.symbols("U V", real=True)
    kappa = sp.symbols("kappa", positive=True, real=True)
    c2, c3 = sp.symbols("c2 c3", real=True)

    s = U * V
    v = -1 - kappa * s + c2 * s**2 + c3 * s**3

    # Old coordinates (t,s) as functions of (U,V).
    jacobian = sp.Matrix(
        [
            [-1 / (kappa * U), 0],
            [V, U],
        ]
    )
    old_metric = sp.Matrix(
        [
            [v**2 - 1, -v],
            [-v, 1],
        ]
    )
    new_metric = sp.simplify(jacobian.T * old_metric * jacobian)

    g_uu = sp.factor(new_metric[0, 0])
    g_uv = sp.factor(new_metric[0, 1])
    g_vv = sp.factor(new_metric[1, 1])
    determinant = sp.factor(new_metric.det())

    limits = {
        "g_UU": sp.factor(sp.limit(g_uu, U, 0)),
        "g_UV": sp.factor(sp.limit(g_uv, U, 0)),
        "g_VV": sp.factor(sp.limit(g_vv, U, 0)),
        "det_g": sp.factor(sp.limit(determinant, U, 0)),
    }

    # Rim calculation in one transverse direction.  For
    #   ds^2 = -dt^2 + (dx-v(x,y)dt)^2 + dy^2,
    # fixed-(t,x) y-lines are candidate unit spacelike geodesics.  Compute
    # both that statement and their null tidal curvature symbolically.
    t, x, y = sp.symbols("t x y", real=True)
    coords = [t, x, y]
    vf = sp.Function("v")(x, y)
    metric_3 = sp.Matrix(
        [
            [vf**2 - 1, -vf, 0],
            [-vf, 1, 0],
            [0, 0, 1],
        ]
    )
    inverse_3 = sp.simplify(metric_3.inv())
    dim = 3
    gamma = [[[sp.Integer(0) for _ in range(dim)] for _ in range(dim)] for _ in range(dim)]
    for a_idx in range(dim):
        for b_idx in range(dim):
            for c_idx in range(dim):
                gamma[a_idx][b_idx][c_idx] = sp.simplify(
                    sum(
                        inverse_3[a_idx, d_idx]
                        * (
                            sp.diff(metric_3[d_idx, c_idx], coords[b_idx])
                            + sp.diff(metric_3[d_idx, b_idx], coords[c_idx])
                            - sp.diff(metric_3[b_idx, c_idx], coords[d_idx])
                        )
                        for d_idx in range(dim)
                    )
                    / 2
                )

    riemann_up = [
        [
            [[sp.Integer(0) for _ in range(dim)] for _ in range(dim)]
            for _ in range(dim)
        ]
        for _ in range(dim)
    ]
    for a_idx in range(dim):
        for b_idx in range(dim):
            for c_idx in range(dim):
                for d_idx in range(dim):
                    riemann_up[a_idx][b_idx][c_idx][d_idx] = sp.simplify(
                        sp.diff(gamma[a_idx][d_idx][b_idx], coords[c_idx])
                        - sp.diff(gamma[a_idx][c_idx][b_idx], coords[d_idx])
                        + sum(
                            gamma[a_idx][c_idx][e_idx] * gamma[e_idx][d_idx][b_idx]
                            - gamma[a_idx][d_idx][e_idx] * gamma[e_idx][c_idx][b_idx]
                            for e_idx in range(dim)
                        )
                    )

    def riemann_cov(a_idx: int, b_idx: int, c_idx: int, d_idx: int) -> sp.Expr:
        return sp.simplify(
            sum(
                metric_3[a_idx, e_idx] * riemann_up[e_idx][b_idx][c_idx][d_idx]
                for e_idx in range(dim)
            )
        )

    null_l = sp.Matrix([1, vf + 1, 0])  # e_0+e_1 in coordinates
    null_n = sp.Matrix([sp.Rational(1, 2), (vf - 1) / 2, 0])
    transverse_y = sp.Matrix([0, 0, 1])

    def contract(
        first: sp.Matrix,
        second: sp.Matrix,
        third: sp.Matrix,
        fourth: sp.Matrix,
    ) -> sp.Expr:
        value = sp.Integer(0)
        for a_idx in range(dim):
            for b_idx in range(dim):
                for c_idx in range(dim):
                    for d_idx in range(dim):
                        value += (
                            riemann_cov(a_idx, b_idx, c_idx, d_idx)
                            * first[a_idx]
                            * second[b_idx]
                            * third[c_idx]
                            * fourth[d_idx]
                        )
        return sp.factor(sp.simplify(value))

    rim_curvature = contract(null_l, transverse_y, null_l, transverse_y)
    mixed_curvature = contract(null_l, transverse_y, null_l, null_n)
    gamma_yy = [sp.factor(gamma[a_idx][2][2]) for a_idx in range(dim)]

    def covariant_y(vector: sp.Matrix) -> sp.Matrix:
        return sp.Matrix(
            [
                sp.simplify(
                    sp.diff(vector[a_idx], y)
                    + sum(
                        gamma[a_idx][2][b_idx] * vector[b_idx]
                        for b_idx in range(dim)
                    )
                )
                for a_idx in range(dim)
            ]
        )

    transport_l = covariant_y(null_l)
    transport_n = covariant_y(null_n)

    phi_y, phi_yy, c_wall = sp.symbols("phi_y phi_yy c", positive=True, real=True)
    affine_wall_value = sp.factor(
        rim_curvature.subs(
            {
                sp.diff(vf, y): -c_wall * phi_y,
                sp.diff(vf, y, y): -c_wall * phi_yy,
            }
        )
    )

    lines = [
        "Flat-cap partial-extension check",
        "",
        "Input:",
        "  v(s) = -1 - kappa*s + c2*s^2 + c3*s^3",
        "  U = exp(-kappa*t),  s = U*V",
        "",
        "Transformed 1+1 metric components:",
        f"  g_UU = {sp.sstr(g_uu)}",
        f"  g_UV = {sp.sstr(g_uv)}",
        f"  g_VV = {sp.sstr(g_vv)}",
        f"  det(g_1+1) = {sp.sstr(determinant)}",
        "",
        "Limits at U=0:",
    ]
    for name, value in limits.items():
        lines.append(f"  {name} -> {sp.sstr(value)}")

    checks = [
        sp.simplify(determinant + 1 / kappa**2) == 0,
        limits["g_UV"] == -1 / kappa,
        limits["g_VV"] == 0,
        limits["det_g"] == -1 / kappa**2,
        gamma_yy == [0, 0, 0],
        sp.simplify(
            rim_curvature
            - (sp.diff(vf, y, y) - sp.diff(vf, y) ** 2)
        )
        == 0,
        sp.simplify(
            mixed_curvature
            - (
                (vf - 1) * sp.diff(vf, x, y) / 2
                + sp.diff(vf, x) * sp.diff(vf, y)
            )
        )
        == 0,
        all(
            sp.simplify(transport_l[idx] - sp.diff(vf, y) * null_l[idx] / 2)
            == 0
            for idx in range(dim)
        ),
        all(
            sp.simplify(transport_n[idx] + sp.diff(vf, y) * null_n[idx] / 2)
            == 0
            for idx in range(dim)
        ),
    ]
    if not all(checks):
        raise AssertionError("flat-cap extension check failed")

    lines.extend(
        [
            "",
            "Conclusion:",
            "  Every coefficient is smooth at U=0.",
            "  The determinant is the nonzero constant -1/kappa^2.",
            "  Adding flat transverse dy^2+dz^2 therefore gives a smooth",
            "  nondegenerate 3+1 extension through the cap-generator endpoint.",
            "",
            "Cap-rim transverse-family check:",
            f"  Gamma^mu_yy = {[sp.sstr(value) for value in gamma_yy]}",
            "  Thus fixed-(t,x) y-lines are unit spacelike geodesics.",
            f"  R(e0+e1, ey, e0+e1, ey) = {sp.sstr(rim_curvature)}",
            f"  R(e0+e1, ey, e0+e1, (e0-e1)/2) = {sp.sstr(mixed_curvature)}",
            "  On v=-1 with v_y=0, the mixed component reduces to -v_xy.",
            f"  nabla_y(e0+e1) = {[sp.sstr(value) for value in transport_l]}",
            f"  nabla_y((e0-e1)/2) = {[sp.sstr(value) for value in transport_n]}",
            "  These are +(v_y/2)(e0+e1) and -(v_y/2)(e0-e1)/2,",
            "  verifying the finite reciprocal transport factors in the rigidity proof.",
            "  For v=-1-c*phi(y), c>0, phi_y>0, phi_yy>0:",
            f"    R = {sp.sstr(affine_wall_value)} < 0",
            "  Parallel transport from the rim changes e0+e1 only by the finite",
            "  factor exp[-(v-v_rim)/2].  An affine endpoint boost q therefore",
            "  makes this neighboring contraction diverge as q^2.",
        ]
    )

    text = "\n".join(lines) + "\n"
    (OUT / "flat_cap_partial_extension.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
