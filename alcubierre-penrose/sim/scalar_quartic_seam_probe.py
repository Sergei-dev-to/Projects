"""Symbolic rigidity probe for a compact quartically flat scalar-shift wall.

This is an internal falsification/regression test, not an ingredient of the
proof.  It targets the sharp situation in which the screen Hessian and the
transverse derivative of the inaffinity vanish at one stationary generator,
although no open planar cap is present.

The compact wall is the regular level set Phi=0 with

    Phi = x^2/L^2 + h(y,z) - 1,
    h(y,z) = (y^2+z^2)^3/R^6 - (y^4+z^4)/R^4.

Near the front point p=(L,0,0), take W(Phi)=-1-a Phi.  A smooth monotone W
can be made constant in the bubble interior and exterior without changing
this germ, so the local calculation embeds in a bounded nonpositive shift.
The negative quartic in h makes the front locally dimpled and produces the
requested positive quartic term in v.
"""

from __future__ import annotations

import sympy as sp


def derive_scalar_shift_curvature():
    """Derive the two relevant null-frame components from the 2+1 metric."""

    t, x, y = sp.symbols("t x y", real=True)
    coordinates = (t, x, y)
    v = sp.Function("v")(x, y)
    metric = sp.Matrix(
        [
            [v**2 - 1, -v, 0],
            [-v, 1, 0],
            [0, 0, 1],
        ]
    )
    inverse = sp.simplify(metric.inv())
    dimension = 3

    gamma = [
        [[sp.Integer(0) for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for lower_1 in range(dimension):
            for lower_2 in range(dimension):
                gamma[upper][lower_1][lower_2] = sp.simplify(
                    sum(
                        inverse[upper, index]
                        * (
                            sp.diff(metric[index, lower_2], coordinates[lower_1])
                            + sp.diff(metric[index, lower_1], coordinates[lower_2])
                            - sp.diff(metric[lower_1, lower_2], coordinates[index])
                        )
                        for index in range(dimension)
                    )
                    / 2
                )

    riemann_up = [
        [
            [[sp.Integer(0) for _ in range(dimension)] for _ in range(dimension)]
            for _ in range(dimension)
        ]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for second in range(dimension):
            for third in range(dimension):
                for fourth in range(dimension):
                    riemann_up[upper][second][third][fourth] = sp.simplify(
                        sp.diff(gamma[upper][fourth][second], coordinates[third])
                        - sp.diff(gamma[upper][third][second], coordinates[fourth])
                        + sum(
                            gamma[upper][third][index] * gamma[index][fourth][second]
                            - gamma[upper][fourth][index] * gamma[index][third][second]
                            for index in range(dimension)
                        )
                    )

    def riemann_cov(first, second, third, fourth):
        return sp.simplify(
            sum(
                metric[first, index] * riemann_up[index][second][third][fourth]
                for index in range(dimension)
            )
        )

    def contract(first, second, third, fourth):
        result = sp.Integer(0)
        for a_index in range(dimension):
            for b_index in range(dimension):
                for c_index in range(dimension):
                    for d_index in range(dimension):
                        result += (
                            riemann_cov(a_index, b_index, c_index, d_index)
                            * first[a_index]
                            * second[b_index]
                            * third[c_index]
                            * fourth[d_index]
                        )
        return sp.factor(sp.simplify(result))

    ell = sp.Matrix([1, v + 1, 0])
    nu = sp.Matrix([sp.Rational(1, 2), (v - 1) / 2, 0])
    transverse = sp.Matrix([0, 0, 1])
    screen = contract(ell, transverse, ell, transverse)
    mixed = contract(ell, transverse, ell, nu)

    expected_screen = sp.diff(v, y, y) - sp.diff(v, y) ** 2
    expected_mixed = (
        v * sp.diff(v, x, y)
        + 2 * sp.diff(v, x) * sp.diff(v, y)
        - sp.diff(v, x, y)
    ) / 2
    assert sp.simplify(screen - expected_screen) == 0
    assert sp.simplify(mixed - expected_mixed) == 0
    return (x, y, v), sp.factor(screen), sp.factor(mixed)


def substitute_profile(expression, function, profile):
    return sp.factor(sp.simplify(expression.subs(function, profile).doit()))


def main():
    (x, y, function), generic_screen, generic_mixed = derive_scalar_shift_curvature()

    z, s = sp.symbols("z s", real=True)
    L, R, a = sp.symbols("L R a", positive=True, finite=True, real=True)
    u = (y**2 + z**2) / R**2
    quartic = (y**4 + z**4) / R**4
    h = u**3 - quartic
    phi = x**2 / L**2 + h - 1
    profile = -1 - a * phi
    point = {x: L, y: 0, z: 0}

    # Compactness and regularity of the wall are elementary but are recorded
    # explicitly.  Phi is coercive.  Its gradient can vanish only at x=0 and
    # the cases listed below; none lies on Phi=0.
    gradient_phi = tuple(sp.factor(sp.diff(phi, variable)) for variable in (x, y, z))
    critical_phi_values = (
        sp.simplify(phi.subs({x: 0, y: 0, z: 0})),
        sp.simplify(phi.subs({x: 0, y: sp.sqrt(sp.Rational(2, 3)) * R, z: 0})),
        sp.simplify(phi.subs({x: 0, y: R / sp.sqrt(6), z: R / sp.sqrt(6)})),
    )
    assert critical_phi_values == (
        -1,
        -sp.Rational(31, 27),
        -sp.Rational(55, 54),
    )

    kappa = sp.factor(-sp.diff(profile, x).subs(point))
    transverse_hessian = sp.Matrix(
        2,
        2,
        lambda row, column: sp.diff(profile, (y, z)[row], (y, z)[column]).subs(point),
    )
    transverse_kappa_gradient = sp.Matrix(
        [sp.diff(profile, x, transverse).subs(point) for transverse in (y, z)]
    )
    assert sp.simplify(profile.subs(point) + 1) == 0
    assert kappa == 2 * a / L
    assert transverse_hessian == sp.zeros(2)
    assert transverse_kappa_gradient == sp.zeros(2, 1)

    # The local form displays the quartically flat seam directly.
    germ = sp.expand(profile.subs(x, L + s))
    expected_germ = -1 - 2 * a * s / L - a * s**2 / L**2 + a * quartic - a * u**3
    assert sp.simplify(germ - expected_germ) == 0

    screen = substitute_profile(generic_screen, function, profile)
    mixed = substitute_profile(generic_mixed, function, profile)
    screen_line = sp.factor(screen.subs({x: L, z: 0}))
    mixed_line = sp.factor(mixed.subs({x: L, z: 0}))
    screen_at_point = sp.simplify(screen_line.subs(y, 0))
    mixed_at_point = sp.simplify(mixed_line.subs(y, 0))
    screen_leading = sp.factor(sp.limit(screen_line / y**2, y, 0))
    mixed_leading = sp.factor(sp.limit(mixed_line / y**3, y, 0))

    assert screen_at_point == 0
    assert mixed_at_point == 0
    assert screen_leading == 12 * a / R**4
    assert mixed_leading == -8 * a**2 / (L * R**4)
    assert screen_line != 0

    print("Compact quartic-seam rigidity probe")
    print()
    print("Wall defining function:")
    print("  Phi =", phi)
    print("  grad Phi =", gradient_phi)
    print("  Phi at possible critical points =", critical_phi_values)
    print("  Therefore Phi=0 is compact and regular.")
    print()
    print("Front stationary generator p=(L,0,0):")
    print("  v(p) =", profile.subs(point))
    print("  kappa = -v_x(p) =", kappa)
    print("  H_AB(p) =", transverse_hessian)
    print("  partial_A v_x(p) =", transverse_kappa_gradient)
    print("  Both pointwise positive-boost tests vanish at p.")
    print()
    print("Local germ with s=x-L:")
    print("  v =", germ)
    print()
    print("Curvature derived directly from the metric:")
    print("  R(ell,e_y,ell,e_y) =", generic_screen)
    print("  R(ell,e_y,ell,nu) =", generic_mixed)
    print()
    print("On the fixed transverse line x=L, z=0:")
    print("  screen =", screen_line)
    print("  mixed  =", mixed_line)
    print("  screen/y^2 ->", screen_leading)
    print("  mixed/y^3  ->", mixed_leading)
    print()
    print("Conclusion:")
    print("  The central generator is pointwise invisible to both tests, but every")
    print("  transverse neighborhood contains a nonzero screen component of order y^2.")
    print("  A uniformly regular extension disk would therefore force an exact planar")
    print("  cap, exactly as in the transverse-rigidity argument.")


if __name__ == "__main__":
    main()
