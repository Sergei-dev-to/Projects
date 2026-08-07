"""Local screen-curvature check for Natario's zero-expansion shift.

The calculation retains the two-jet of a stationary axisymmetric vector shift
at its front axial point.  It verifies the pregeodesic and parallel-screen
claims as well as the curvature coefficient quoted in the paper.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = (t, x, y, z)
    a, c, bx, by, bz, d = sp.symbols(
        "a c b_x b_y b_z d", real=True
    )
    kappa, radius, q = sp.symbols("kappa R_F q", positive=True, real=True)

    # General axisymmetric two-jet at X=-e_x.
    shift = (
        -1 + a * x + sp.Rational(1, 2) * (bx * x**2 + by * y**2 + bz * z**2),
        c * y + d * x * y,
        c * z + d * x * z,
    )

    metric = sp.zeros(4)
    metric[0, 0] = -1 + sum(component**2 for component in shift)
    for i in range(3):
        metric[0, i + 1] = metric[i + 1, 0] = -shift[i]
        metric[i + 1, i + 1] = 1

    origin = {x: 0, y: 0, z: 0}
    metric_at_origin = sp.simplify(metric.subs(origin))
    inverse_at_origin = sp.simplify(metric_at_origin.inv())

    first = [
        [
            [sp.diff(metric[i, j], coords[k]).subs(origin) for k in range(4)]
            for j in range(4)
        ]
        for i in range(4)
    ]
    second = [
        [
            [
                [
                    sp.diff(metric[i, j], coords[k], coords[l]).subs(origin)
                    for l in range(4)
                ]
                for k in range(4)
            ]
            for j in range(4)
        ]
        for i in range(4)
    ]

    def gamma(up: int, low1: int, low2: int) -> sp.Expr:
        return sp.simplify(
            sp.Rational(1, 2)
            * sum(
                inverse_at_origin[up, m]
                * (
                    first[m][low1][low2]
                    + first[m][low2][low1]
                    - first[low1][low2][m]
                )
                for m in range(4)
            )
        )

    connection = [
        [[gamma(i, j, k) for k in range(4)] for j in range(4)]
        for i in range(4)
    ]

    def inverse_derivative(up1: int, up2: int, derivative: int) -> sp.Expr:
        return sp.simplify(
            -sum(
                inverse_at_origin[up1, p]
                * first[p][r][derivative]
                * inverse_at_origin[r, up2]
                for p in range(4)
                for r in range(4)
            )
        )

    def gamma_derivative(
        up: int, low1: int, low2: int, derivative: int
    ) -> sp.Expr:
        inverse_term = sp.Rational(1, 2) * sum(
            inverse_derivative(up, m, derivative)
            * (
                first[m][low1][low2]
                + first[m][low2][low1]
                - first[low1][low2][m]
            )
            for m in range(4)
        )
        second_term = sp.Rational(1, 2) * sum(
            inverse_at_origin[up, m]
            * (
                second[m][low1][derivative][low2]
                + second[m][low2][derivative][low1]
                - second[low1][low2][derivative][m]
            )
            for m in range(4)
        )
        return sp.simplify(inverse_term + second_term)

    def riemann_up(up: int, b: int, c_index: int, d_index: int) -> sp.Expr:
        return sp.simplify(
            gamma_derivative(up, b, d_index, c_index)
            - gamma_derivative(up, b, c_index, d_index)
            + sum(
                connection[up][c_index][m] * connection[m][b][d_index]
                - connection[up][d_index][m] * connection[m][b][c_index]
                for m in range(4)
            )
        )

    def riemann_down(i: int, j: int, k: int, l: int) -> sp.Expr:
        return sp.factor(
            sum(
                metric_at_origin[i, m] * riemann_up(m, j, k, l)
                for m in range(4)
            )
        )

    def ricci(i: int, j: int) -> sp.Expr:
        return sp.factor(sum(riemann_up(m, i, m, j) for m in range(4)))

    natario = {
        a: -kappa,
        c: kappa / 2,
        by: -2 * kappa / radius,
        bz: -2 * kappa / radius,
    }
    target = -2 * kappa / radius - sp.Rational(3, 4) * kappa**2

    gamma_tt = [
        sp.factor(connection[i][0][0].subs(natario)) for i in range(4)
    ]
    gamma_ty = [
        sp.factor(connection[i][0][2].subs(natario)) for i in range(4)
    ]
    gamma_tz = [
        sp.factor(connection[i][0][3].subs(natario)) for i in range(4)
    ]
    r_tyty = sp.factor(riemann_down(0, 2, 0, 2).subs(natario))
    r_tztz = sp.factor(riemann_down(0, 3, 0, 3).subs(natario))
    ricci_tt = sp.factor(ricci(0, 0).subs(natario))

    assert gamma_tt == [-kappa, 0, 0, 0]
    assert gamma_ty == [0, 0, 0, 0]
    assert gamma_tz == [0, 0, 0, 0]
    assert sp.simplify(r_tyty - target) == 0
    assert sp.simplify(r_tztz - target) == 0
    assert sp.simplify(ricci_tt - 2 * target) == 0

    lines = [
        "Natario front-axis local-jet check",
        "",
        "Local data:",
        "  X=-e_x,  d_x X^x=-kappa,",
        "  d_y X^y=d_z X^z=kappa/2,",
        "  d_yy X^x=d_zz X^x=-2*kappa/R_F.",
        "",
        f"Gamma^a_tt = {gamma_tt}",
        f"Gamma^a_ty = {gamma_ty}",
        f"Gamma^a_tz = {gamma_tz}",
        "Thus d_t is pregeodesic, q is proportional to exp(kappa*t),",
        "and d_y,d_z are parallel along the axial generator.",
        "",
        f"R_tyty = {r_tyty}",
        f"R_tztz = {r_tztz}",
        f"Ric_tt = {ricci_tt}",
        f"R_KYKY = {sp.factor(q**2 * r_tyty)}",
    ]

    text = "\n".join(lines) + "\n"
    (OUT / "natario_local_jet.txt").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
