"""Generic smooth front-wall tip calculation.

This removes spherical symmetry.  Near the front tip, take x to point in the
direction of travel/front normal and y,z to be transverse coordinates.  The
front endpoint condition is

    v=-1, v_x=-kappa, v_y=v_z=0.

The transverse Hessian H_AB = v_AB controls the PP curvature blow-up.  In
principal-curvature coordinates for the wall v=-1, H_AB=-kappa C_AB, where
C_AB has positive eigenvalues for a convex front cap.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


OUT = Path("output/sech")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    t, x, y, z = sp.symbols("t x y z", real=True)
    kappa, q = sp.symbols("kappa q", positive=True, real=True)
    mu, a, b, Hyy, Hyz, Hzz = sp.symbols("mu a b H_yy H_yz H_zz", real=True)
    C1, C2 = sp.symbols("C_1 C_2", positive=True, real=True)
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
    for A in range(4):
        for B in range(4):
            for C in range(4):
                expr = sp.Integer(0)
                for D in range(4):
                    expr += gi[A, D] * (
                        sp.diff(g[D, C], coords[B])
                        + sp.diff(g[D, B], coords[C])
                        - sp.diff(g[B, C], coords[D])
                    )
                gamma[A][B][C] = sp.simplify(expr / 2)

    rup = [[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for A in range(4):
        for B in range(4):
            for C in range(4):
                for D in range(4):
                    expr = sp.diff(gamma[A][D][B], coords[C]) - sp.diff(gamma[A][C][B], coords[D])
                    for E in range(4):
                        expr += gamma[A][C][E] * gamma[E][D][B]
                        expr -= gamma[A][D][E] * gamma[E][C][B]
                    rup[A][B][C][D] = sp.simplify(expr)

    rcov = [[[[sp.Integer(0) for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for A in range(4):
        for B in range(4):
            for C in range(4):
                for D in range(4):
                    rcov[A][B][C][D] = sp.simplify(sum(g[A, E] * rup[E][B][C][D] for E in range(4)))

    ric = [[sp.Integer(0) for _ in range(4)] for _ in range(4)]
    for A in range(4):
        for B in range(4):
            expr = sp.Integer(0)
            for C in range(4):
                expr += sp.diff(gamma[C][B][A], coords[C])
                expr -= sp.diff(gamma[C][C][A], coords[B])
                for D in range(4):
                    expr += gamma[C][C][D] * gamma[D][B][A]
                    expr -= gamma[C][B][D] * gamma[D][C][A]
            ric[A][B] = sp.simplify(expr)

    scalar = sp.simplify(sum(gi[A, B] * ric[A][B] for A in range(4) for B in range(4)))
    ein = [[sp.simplify(ric[A][B] - sp.Rational(1, 2) * g[A, B] * scalar) for B in range(4)] for A in range(4)]

    subs = {
        v: -1,
        sp.diff(v, x): -kappa,
        sp.diff(v, y): 0,
        sp.diff(v, z): 0,
        sp.diff(v, x, x): mu,
        sp.diff(v, x, y): a,
        sp.diff(v, x, z): b,
        sp.diff(v, y, y): Hyy,
        sp.diff(v, y, z): Hyz,
        sp.diff(v, z, z): Hzz,
    }

    frame = {
        "K": sp.Matrix([q, 0, 0, 0]),
        "N": sp.Matrix([sp.Rational(1, 2) / q, -1 / q, 0, 0]),
        "Y": sp.Matrix([0, 0, 1, 0]),
        "Z": sp.Matrix([0, 0, 0, 1]),
    }

    def rframe(a_label: str, b_label: str, c_label: str, d_label: str) -> sp.Expr:
        A = frame[a_label]
        B = frame[b_label]
        C = frame[c_label]
        D = frame[d_label]
        expr = sp.Integer(0)
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    for ell in range(4):
                        expr += rcov[i][j][k][ell] * A[i] * B[j] * C[k] * D[ell]
        return sp.factor(sp.simplify(expr.subs(subs)))

    def eframe(a_label: str, b_label: str) -> sp.Expr:
        A = frame[a_label]
        B = frame[b_label]
        expr = sp.Integer(0)
        for i in range(4):
            for j in range(4):
                expr += ein[i][j] * A[i] * B[j]
        return sp.factor(sp.simplify(expr.subs(subs)))

    components = {
        "R_KYKY": rframe("K", "Y", "K", "Y"),
        "R_KYKZ": rframe("K", "Y", "K", "Z"),
        "R_KZKZ": rframe("K", "Z", "K", "Z"),
        "R_KNKN": rframe("K", "N", "K", "N"),
        "G_KK": eframe("K", "K"),
        "G_KY": eframe("K", "Y"),
        "G_KZ": eframe("K", "Z"),
    }

    pairs = [("K", "N"), ("K", "Y"), ("K", "Z"), ("N", "Y"), ("N", "Z"), ("Y", "Z")]
    full_riemann = []
    for i, p1 in enumerate(pairs):
        for j, p2 in enumerate(pairs):
            if j < i:
                continue
            value = rframe(p1[0], p1[1], p2[0], p2[1])
            if value != 0:
                full_riemann.append((p1, p2, value))

    flat_hessian = {Hyy: 0, Hyz: 0, Hzz: 0}
    flat_riemann = [
        (p1, p2, sp.factor(sp.simplify(value.subs(flat_hessian))))
        for p1, p2, value in full_riemann
    ]
    flat_riemann = [(p1, p2, value) for p1, p2, value in flat_riemann if value != 0]
    flat_einstein = {
        name: sp.factor(sp.simplify(value.subs(flat_hessian)))
        for name, value in components.items()
        if name.startswith("G_")
    }

    principal_subs = {Hyy: -kappa * C1, Hzz: -kappa * C2, Hyz: 0}
    principal = {name: sp.factor(sp.simplify(val.subs(principal_subs))) for name, val in components.items()}

    lines = [
        "Generic convex front-wall tip calculation",
        "",
        "Local assumptions at the exact front endpoint:",
        "  v=-1",
        "  v_x=-kappa, kappa>0",
        "  v_y=v_z=0",
        "  H_AB = v_AB in transverse coordinates A,B=y,z",
        "",
        "No spherical symmetry is assumed.  Cross derivatives v_xy=a and v_xz=b",
        "are kept in the symbolic substitution.",
        "",
        "Leading PP curvature components:",
    ]
    for name in ["R_KYKY", "R_KYKZ", "R_KZKZ", "R_KNKN"]:
        lines.append(f"  {name} = {sp.sstr(components[name])}")

    lines.extend(
        [
            "",
            "Leading Einstein components:",
            f"  G_KK = {sp.sstr(components['G_KK'])}",
            f"  G_KY = {sp.sstr(components['G_KY'])}",
            f"  G_KZ = {sp.sstr(components['G_KZ'])}",
            "",
            "Wall-curvature interpretation:",
            "  Let the horizon/front wall v=-1 be x=X(y,z).",
            "  Since v_x=-kappa and v_A=0, differentiating v(X(y,z),y,z)=-1 gives",
            "    X_AB = H_AB/kappa.",
            "  In principal transverse coordinates for a convex front cap,",
            "    X_yy=-C_1, X_zz=-C_2, C_i>0,",
            "  hence",
            "    H_yy=-kappa C_1, H_zz=-kappa C_2, H_yz=0.",
            "",
            "Principal-curvature form:",
        ]
    )
    for name in ["R_KYKY", "R_KYKZ", "R_KZKZ", "R_KNKN", "G_KK"]:
        lines.append(f"  {name} = {sp.sstr(principal[name])}")

    lines.extend(
        [
            "",
            "Full nonzero parallel-frame Riemann components in the generic local model:",
        ]
    )
    for p1, p2, value in full_riemann:
        lines.append(f"  R_{p1[0]}{p1[1]}{p2[0]}{p2[1]} = {sp.sstr(value)}")

    lines.extend(
        [
            "",
            "Flat transverse Hessian check H_AB=0:",
        ]
    )
    if flat_riemann:
        for p1, p2, value in flat_riemann:
            lines.append(f"  R_{p1[0]}{p1[1]}{p2[0]}{p2[1]} = {sp.sstr(value)}")
    else:
        lines.append("  all q-divergent Riemann components vanish; only finite components remain")
    lines.extend(
        [
            f"  G_KK = {sp.sstr(flat_einstein['G_KK'])}",
            f"  G_KY = {sp.sstr(flat_einstein['G_KY'])}",
            f"  G_KZ = {sp.sstr(flat_einstein['G_KZ'])}",
        ]
    )

    lines.extend(
        [
            "",
            "With q=1/[kappa(lambda_*-lambda)],",
            "  R_KYKY = -C_1/[kappa(lambda_*-lambda)^2]",
            "  R_KZKZ = -C_2/[kappa(lambda_*-lambda)^2]",
            "  G_KK   = - (C_1+C_2)/[kappa(lambda_*-lambda)^2].",
            "",
            "Conclusion:",
            "  The PP singularity is not a spherical artifact.  For any smooth",
            "  finite-curvature convex front cap with positive principal curvature,",
            "  the exact front generator has transverse tidal blow-up controlled",
            "  by the principal curvatures of the wall.",
        ]
    )

    (OUT / "front_tip_general_convex_wall.txt").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    print("\n".join(lines[:26]))


if __name__ == "__main__":
    main()
