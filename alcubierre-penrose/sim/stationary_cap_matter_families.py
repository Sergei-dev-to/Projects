"""Exact source and crossing families for planar scalar-shift caps.

This script audits the follow-up note `notes/stationary_cap_matter_families.md`.
It verifies:

* the Einstein tensor of a general planar scalar shift;
* the constant-curvature family v^2=1+2*kappa*s-alpha*s^2;
* its Einstein-Maxwell-Lambda and two-axion-Lambda realizations;
* simple perfect-fluid and normal-scalar no-go statements;
* an exact Kundt null-radiation pulse on the curved cap background.

No perturbative expansion is used.
"""

from __future__ import annotations

import sympy as sp


def connection_and_ricci(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    inverse = sp.simplify(metric.inv())
    dimension = len(coordinates)
    gamma = [
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
    ricci = sp.MutableDenseMatrix(
        dimension, dimension, [sp.Integer(0)] * dimension**2
    )
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
    scalar = sp.simplify(
        sum(
            inverse[a, b] * ricci[a, b]
            for a in range(dimension)
            for b in range(dimension)
        )
    )
    einstein = (ricci - metric * scalar / 2).applyfunc(sp.simplify)
    return gamma, ricci, sp.factor(scalar), einstein


def planar_scalar_shift():
    t, s, y, z = sp.symbols("t s y z", real=True)
    v = sp.Function("v")(s)
    metric = sp.Matrix(
        [
            [v**2 - 1, -v, 0, 0],
            [-v, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    _, _, scalar, einstein = connection_and_ricci(metric, (t, s, y, z))
    expected_scalar = sp.diff(v**2, s, 2)
    expected_pressure = -expected_scalar / 2
    assert sp.simplify(scalar - expected_scalar) == 0
    expected = sp.diag(0, 0, expected_pressure, expected_pressure)
    assert (einstein - expected).applyfunc(sp.simplify) == sp.zeros(4)
    return scalar, expected_pressure


def constant_curvature_and_sources():
    s = sp.symbols("s", real=True)
    kappa, alpha = sp.symbols("kappa alpha", positive=True, real=True)
    v_squared = 1 + 2 * kappa * s - alpha * s**2
    scalar = sp.diff(v_squared, s, 2)
    pressure_geometric = -scalar / 2
    assert scalar == -2 * alpha
    assert pressure_geometric == alpha

    eta = sp.diag(-1, 1, 1, 1)
    einstein_orthonormal = sp.diag(0, 0, alpha, alpha)

    # Uniform electric or magnetic field normal to the cap.  Here q is
    # 8*pi*G times its energy density.
    q = alpha / 2
    lambda_em = -alpha / 2
    maxwell = sp.diag(q, -q, q, q)
    assert einstein_orthonormal + lambda_em * eta == maxwell

    # Two canonical massless scalars phi_1=c*y and phi_2=c*z.  In units where
    # their combined 8*pi*G stress has amplitude alpha.
    lambda_axion = -alpha
    axions = sp.diag(alpha, -alpha, 0, 0)
    assert einstein_orthonormal + lambda_axion * eta == axions

    # Isotropic perfect fluid plus Lambda can match only alpha=0: equality of
    # its longitudinal and transverse pressures would require 0=alpha.
    rho, pressure, cosmological = sp.symbols("rho pressure cosmological")
    perfect_fluid_equations = [
        sp.Eq(-cosmological, rho),
        sp.Eq(cosmological, pressure),
        sp.Eq(alpha + cosmological, pressure),
    ]
    perfect_fluid_solution = sp.solve(
        perfect_fluid_equations, (rho, pressure, cosmological, alpha), dict=True
    )
    assert all(solution.get(alpha, alpha) == 0 for solution in perfect_fluid_solution)

    # A canonical scalar depending only on s also forces its kinetic energy
    # and alpha to vanish.
    kinetic, potential = sp.symbols("kinetic potential")
    normal_scalar_equations = [
        sp.Eq(-cosmological, kinetic + potential),
        sp.Eq(cosmological, kinetic - potential),
        sp.Eq(alpha + cosmological, -kinetic - potential),
    ]
    normal_scalar_solution = sp.solve(
        normal_scalar_equations,
        (kinetic, potential, cosmological, alpha),
        dict=True,
    )
    assert all(solution.get(kinetic, kinetic) == 0 for solution in normal_scalar_solution)
    assert all(solution.get(alpha, alpha) == 0 for solution in normal_scalar_solution)

    return scalar, einstein_orthonormal, maxwell, axions


def exact_curved_cap_pulse():
    u, r, y, z = sp.symbols("u r y z", real=True)
    kappa, alpha = sp.symbols("kappa alpha", positive=True, real=True)
    H = sp.Function("H")(u, y, z)
    A = -2 * kappa * r + alpha * r**2
    metric = sp.Matrix(
        [
            [H - A, -1, 0, 0],
            [-1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    gamma, _, scalar, einstein = connection_and_ricci(metric, (u, r, y, z))
    laplacian_h = sp.diff(H, y, 2) + sp.diff(H, z, 2)
    expected = sp.diag(-laplacian_h / 2, 0, alpha, alpha)
    assert (einstein - expected).applyfunc(sp.simplify) == sp.zeros(4)
    assert scalar == -2 * alpha
    assert metric.det() == -1

    # The background Maxwell field has q=alpha/2.  Its stress on the curved
    # two-dimensional factor is -q*g_ab and on the transverse plane is +q.
    q = alpha / 2
    cosmological = -q
    maxwell = sp.zeros(4)
    for a in (0, 1):
        for b in (0, 1):
            maxwell[a, b] = -q * metric[a, b]
    maxwell[2, 2] = q
    maxwell[3, 3] = q
    null_radiation = sp.zeros(4)
    null_radiation[0, 0] = -laplacian_h / 2
    assert (
        einstein + cosmological * metric - maxwell - null_radiation
    ).applyfunc(sp.simplify) == sp.zeros(4)

    # k=-partial_r is a null, affinely parametrized geodesic direction.  It
    # crosses r=0; when H is nonzero, r=0 is no longer a null Killing horizon.
    k_vector = sp.Matrix([0, -1, 0, 0])
    assert sp.simplify((k_vector.T * metric * k_vector)[0]) == 0
    acceleration = sp.Matrix(
        [
            sp.simplify(
                sum(
                    gamma[a][b][c] * k_vector[b] * k_vector[c]
                    for b in range(4)
                    for c in range(4)
                )
            )
            for a in range(4)
        ]
    )
    assert acceleration == sp.zeros(4, 1)
    inverse = sp.simplify(metric.inv())
    normal_squared_at_old_horizon = sp.simplify(inverse[1, 1].subs(r, 0))
    assert normal_squared_at_old_horizon == -H

    return scalar, einstein, null_radiation[0, 0], normal_squared_at_old_horizon


def main() -> None:
    scalar, pressure = planar_scalar_shift()
    curved_scalar, curved_g, maxwell, axions = constant_curvature_and_sources()
    pulse_scalar, pulse_g, radiation, old_horizon_norm = exact_curved_cap_pulse()

    print("Stationary planar-cap matter audit")
    print(f"  general scalar curvature: {sp.factor(scalar)}")
    print(f"  geometric transverse pressure: {sp.factor(pressure)}")
    print(f"  constant-curvature scalar: {curved_scalar}")
    print(f"  constant-curvature Einstein tensor: {curved_g}")
    print(f"  Maxwell+Lambda source: {maxwell}")
    print(f"  two-axion+Lambda source: {axions}")
    print("Exact curved-cap radiation audit")
    print(f"  scalar curvature: {pulse_scalar}")
    print(f"  Einstein tensor: {pulse_g}")
    print(f"  null-radiation component: {radiation}")
    print(f"  norm of dr at the old horizon: {old_horizon_norm}")
    print("  RESULT: stationary nonvacuum caps and exact dynamical crossing verified")


if __name__ == "__main__":
    main()
