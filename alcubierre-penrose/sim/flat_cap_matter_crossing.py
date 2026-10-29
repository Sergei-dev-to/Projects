"""Exact checks for matter crossing a regular planar-cap extension.

This is a follow-up calculation, not an ingredient of the paper's extension
theorem.  It checks three claims:

1.  The scalar-shift germ

        v(s) = -sqrt(1 + 2*kappa*s)

    has v(0)=-1, v'(0)=-kappa and is locally flat.  It is therefore an
    admissible constant-inaffinity planar cap whose Kruskal extension is a
    Minkowski neighborhood.

2.  Finite-energy timelike data in a flat bubble core have an outgoing branch
    that reaches such a cap in finite proper time.

3.  The Brinkmann metric

        ds^2 = -2 dU dV + dy^2 + dz^2 + H(V,y,z) dV^2

    solves the full Einstein equations with aligned null dust

        T_VV = rho,   rho = -Delta_perp(H)/(16*pi*G).

    Its matter rays are tangent to -partial_U and cross U=0 smoothly.  This is
    an exact nonlinear solution; no expansion in the amplitude of H is used.
"""

from __future__ import annotations

import sympy as sp


def christoffel(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    """Return Gamma^a_bc for a symbolic metric."""

    inverse = sp.simplify(metric.inv())
    dimension = len(coordinates)
    return [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        for d in range(dimension)
                    )
                    / 2
                )
                for c in range(dimension)
            ]
            for b in range(dimension)
        ]
        for a in range(dimension)
    ]


def ricci_tensor(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    """Return R_ab using the convention employed in the paper's scripts."""

    gamma = christoffel(metric, coordinates)
    dimension = len(coordinates)
    ricci = sp.MutableDenseMatrix(dimension, dimension, [0] * dimension**2)
    for a in range(dimension):
        for b in range(dimension):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(gamma[c][a][b], coordinates[c])
                    - sp.diff(gamma[c][a][c], coordinates[b])
                    + sum(
                        gamma[c][c][d] * gamma[d][a][b]
                        - gamma[c][b][d] * gamma[d][a][c]
                        for d in range(dimension)
                    )
                    for c in range(dimension)
                )
            )
    return ricci, gamma


def flat_cap_germ_check():
    t, s = sp.symbols("t s", real=True)
    kappa = sp.symbols("kappa", positive=True, real=True)
    v = sp.Function("v")(s)
    metric = sp.Matrix([[v**2 - 1, -v], [-v, 1]])
    ricci, _ = ricci_tensor(metric, (t, s))
    inverse = sp.simplify(metric.inv())
    scalar = sp.factor(
        sum(inverse[a, b] * ricci[a, b] for a in range(2) for b in range(2))
    )
    expected = sp.diff(v**2, s, 2)
    assert sp.simplify(scalar - expected) == 0

    flat_v = -sp.sqrt(1 + 2 * kappa * s)
    flat_scalar = sp.simplify(scalar.subs(v, flat_v).doit())
    assert flat_scalar == 0
    assert flat_v.subs(s, 0) == -1
    assert sp.diff(flat_v, s).subs(s, 0) == -kappa
    return scalar, flat_scalar


def timelike_accessibility_check():
    E, mu, v = sp.symbols("E mu v", positive=True, real=True)
    discriminant = sp.sqrt(E**2 - mu**2 * (1 - v**2))
    momentum = (-E * v + discriminant) / (1 - v**2)
    t_dot = sp.simplify(E - v * momentum)
    x_dot = sp.simplify(momentum + v * t_dot)

    assert sp.simplify(t_dot**2 - momentum**2 - mu**2) == 0
    assert sp.simplify(x_dot - discriminant) == 0

    epsilon = sp.symbols("epsilon", positive=True, real=True)
    horizon_substitution = {v: -1 + epsilon}
    assert sp.limit(epsilon * momentum.subs(horizon_substitution), epsilon, 0) == E
    assert sp.limit(epsilon * t_dot.subs(horizon_substitution), epsilon, 0) == E
    assert sp.limit(x_dot.subs(horizon_substitution), epsilon, 0) == E
    assert (
        sp.limit(
            (x_dot / t_dot).subs(horizon_substitution) / epsilon,
            epsilon,
            0,
        )
        == 1
    )
    return momentum, t_dot, x_dot


def exact_null_dust_check():
    U, V, y, z = sp.symbols("U V y z", real=True)
    coordinates = (U, V, y, z)
    H = sp.Function("H")(V, y, z)
    metric = sp.Matrix(
        [
            [0, -1, 0, 0],
            [-1, H, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    ricci, gamma = ricci_tensor(metric, coordinates)
    inverse = sp.simplify(metric.inv())
    scalar = sp.simplify(
        sum(inverse[a, b] * ricci[a, b] for a in range(4) for b in range(4))
    )
    expected_vv = -(
        sp.diff(H, y, 2) + sp.diff(H, z, 2)
    ) / 2

    assert metric.det() == -1
    assert scalar == 0
    for a in range(4):
        for b in range(4):
            expected = expected_vv if (a, b) == (1, 1) else 0
            assert sp.simplify(ricci[a, b] - expected) == 0

    # k=-partial_U is null and covariantly constant, so rho(V,y,z) k_a k_b
    # is conserved for every rho independent of U.
    k = sp.Matrix([-1, 0, 0, 0])
    assert sp.simplify((k.T * metric * k)[0]) == 0
    for upper in range(4):
        for lower in range(4):
            covariant_derivative = sum(
                gamma[upper][lower][index] * k[index] for index in range(4)
            )
            assert sp.simplify(covariant_derivative) == 0

    return expected_vv


def main() -> None:
    scalar, flat_scalar = flat_cap_germ_check()
    momentum, t_dot, x_dot = timelike_accessibility_check()
    ricci_vv = exact_null_dust_check()

    print("Flat planar-cap and exact matter-crossing audit")
    print(f"  general 1+1 scalar curvature: {scalar}")
    print(f"  flat-germ scalar curvature: {flat_scalar}")
    print(f"  outgoing P(v): {sp.factor(momentum)}")
    print(f"  outgoing t_dot(v): {sp.factor(t_dot)}")
    print(f"  outgoing x_dot(v): {sp.factor(x_dot)}")
    print(f"  Brinkmann R_VV: {ricci_vv}")
    print("  determinant: -1; k=-partial_U is null and covariantly constant")
    print("  RESULT: exact aligned null matter crosses U=0 with a smooth metric")


if __name__ == "__main__":
    main()
