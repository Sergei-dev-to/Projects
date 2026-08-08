"""Exact symbolic checks for the localized Zeno transition rim.

The metric is written in coordinates ``(t, phi, r, z)`` as

    g = -(dt - alpha(r,z) dphi)^2
        + (alpha(r,z)^2 + B(t,r,z)) dphi^2 + dr^2 + dz^2

      = -dt^2 + 2 alpha dt dphi + B dphi^2 + dr^2 + dz^2.

Thus ``K = d_phi`` has squared norm ``B``.  The script uses

    R^a{}_{bcd} = d_c Gamma^a{}_{bd} - d_d Gamma^a{}_{bc} + ...

and verifies, without imposing a special cutoff, the causal character of the
``B = 0`` locus, the condition for its closed K-orbits to be null
pregeodesics, and the boost-weight +2 curvature matrix there.
"""

from __future__ import annotations

import sympy as sp


t, phi, r, z = sp.symbols("t phi r z", real=True)
coords = (t, phi, r, z)
n = len(coords)

alpha = sp.Function("alpha")(r, z)
B = sp.Function("B")(t, r, z)
Q2 = alpha**2 + B

g = sp.Matrix(
    [
        [-1, alpha, 0, 0],
        [alpha, B, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
g_inv = sp.simplify(g.inv())


def simp(expr: sp.Expr) -> sp.Expr:
    """A slightly stronger simplifier for rational tensor expressions."""

    return sp.factor(sp.cancel(sp.simplify(expr)))


Gamma = [
    [
        [
            simp(
                sp.Rational(1, 2)
                * sum(
                    g_inv[a, d]
                    * (
                        sp.diff(g[d, c], coords[b])
                        + sp.diff(g[d, b], coords[c])
                        - sp.diff(g[b, c], coords[d])
                    )
                    for d in range(n)
                )
            )
            for c in range(n)
        ]
        for b in range(n)
    ]
    for a in range(n)
]


def riemann_lower(a: int, b: int, c: int, d: int) -> sp.Expr:
    """Return R_{abcd} in the convention stated in the module docstring."""

    return simp(
        sum(
            g[a, e]
            * (
                sp.diff(Gamma[e][b][d], coords[c])
                - sp.diff(Gamma[e][b][c], coords[d])
                + sum(
                    Gamma[e][c][f] * Gamma[f][b][d]
                    - Gamma[e][d][f] * Gamma[f][b][c]
                    for f in range(n)
                )
            )
            for e in range(n)
        )
    )


# Replacing B by zero with ordinary ``subs`` would also erase its derivatives.
# Treat the value and the required jets as independent symbols instead.
b0, bt, br, bz = sp.symbols("b0 bt br bz", real=True)
btt, btr, btz = sp.symbols("btt btr btz", real=True)
brr, brz, bzz = sp.symbols("brr brz bzz", real=True)
ar, az = sp.symbols("ar az", real=True)

jet_rules = {
    sp.diff(B, t, 2): btt,
    sp.diff(B, t, r): btr,
    sp.diff(B, t, z): btz,
    sp.diff(B, r, 2): brr,
    sp.diff(B, r, z): brz,
    sp.diff(B, z, 2): bzz,
    sp.diff(B, t): bt,
    sp.diff(B, r): br,
    sp.diff(B, z): bz,
    sp.diff(alpha, r): ar,
    sp.diff(alpha, z): az,
    B: b0,
}


def in_jets(expr: sp.Expr) -> sp.Expr:
    """Replace function values and derivatives by independent jet symbols."""

    return simp(expr.xreplace(jet_rules))


def on_rim(expr: sp.Expr) -> sp.Expr:
    """Evaluate an expression at B=0 while retaining derivatives of B."""

    return simp(in_jets(expr).subs(b0, 0))


def at_critical_rim(expr: sp.Expr) -> sp.Expr:
    """Additionally impose the transverse criticality br=bz=0."""

    return simp(on_rim(expr).subs({br: 0, bz: 0}))


# ---------------------------------------------------------------------------
# Inverse metric and causal character of B=0
# ---------------------------------------------------------------------------

expected_inverse = sp.Matrix(
    [
        [-B / Q2, alpha / Q2, 0, 0],
        [alpha / Q2, 1 / Q2, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
assert (g_inv - expected_inverse).applyfunc(simp) == sp.zeros(n)

dB = sp.Matrix([sp.diff(B, coordinate) for coordinate in coords])
grad_B = sp.simplify(g_inv * dB)
grad_B_squared = simp((dB.T * g_inv * dB)[0])

assert simp(
    grad_B_squared
    - (-B * sp.diff(B, t) ** 2 / Q2 + sp.diff(B, r) ** 2 + sp.diff(B, z) ** 2)
) == 0
assert on_rim(grad_B_squared - (sp.diff(B, r) ** 2 + sp.diff(B, z) ** 2)) == 0

expected_rim_grad = sp.Matrix([0, bt / alpha, br, bz])
assert (grad_B.applyfunc(on_rim) - expected_rim_grad).applyfunc(simp) == sp.zeros(n, 1)


# ---------------------------------------------------------------------------
# Killing acceleration and the geodesic-orbit criterion
# ---------------------------------------------------------------------------

# K has constant coordinate components, so nabla_K K = Gamma^a_{phi phi}.
nabla_K_K = sp.Matrix([Gamma[a][1][1] for a in range(n)])
assert (nabla_K_K + grad_B / 2).applyfunc(simp) == sp.zeros(n, 1)

expected_rim_acceleration = sp.Matrix([0, -bt / (2 * alpha), -br / 2, -bz / 2])
assert (
    nabla_K_K.applyfunc(on_rim) - expected_rim_acceleration
).applyfunc(simp) == sp.zeros(n, 1)

# At a critical rim orbit, K is a null pregeodesic with this non-affinity.
kappa = -bt / (2 * alpha)
critical_acceleration = nabla_K_K.applyfunc(at_critical_rim)
assert critical_acceleration == sp.Matrix([0, kappa, 0, 0])


# ---------------------------------------------------------------------------
# Boost-weight +2 curvature R(K,e_A,K,e_B)
# ---------------------------------------------------------------------------

transverse_indices = (2, 3)
first_jets = {2: br, 3: bz}
alpha_jets = {2: ar, 3: az}
second_jets = {
    (2, 2): brr,
    (2, 3): brz,
    (3, 2): brz,
    (3, 3): bzz,
}

rim_optical = sp.MutableDenseMatrix.zeros(2, 2)
critical_optical = sp.MutableDenseMatrix.zeros(2, 2)

for row, A_index in enumerate(transverse_indices):
    for col, C_index in enumerate(transverse_indices):
        component = riemann_lower(1, A_index, 1, C_index)
        actual_rim = on_rim(component)
        expected_rim = simp(
            -second_jets[(A_index, C_index)] / 2
            + (
                alpha_jets[A_index] * first_jets[C_index]
                + alpha_jets[C_index] * first_jets[A_index]
            )
            / (4 * alpha)
            + first_jets[A_index] * first_jets[C_index] / (4 * alpha**2)
        )
        assert simp(actual_rim - expected_rim) == 0

        actual_critical = simp(actual_rim.subs({br: 0, bz: 0}))
        expected_critical = -second_jets[(A_index, C_index)] / 2
        assert simp(actual_critical - expected_critical) == 0

        rim_optical[row, col] = actual_rim
        critical_optical[row, col] = actual_critical


# The coordinate screen becomes parallel modulo K at a critical rim orbit.
# Since adding K to a screen vector cannot change R(K,e_A,K,e_B), the critical
# matrix above is the actual parallel-propagated boost-weight +2 matrix.
for A_index, a_A in ((2, ar), (3, az)):
    nabla_K_eA = sp.Matrix([Gamma[a][1][A_index] for a in range(n)])
    expected = sp.Matrix([0, a_A / (2 * alpha), 0, 0])
    assert (
        nabla_K_eA.applyfunc(at_critical_rim) - expected
    ).applyfunc(simp) == sp.zeros(n, 1)


# An adapted companion null vector at the rim.  This optional check shows that
# the boost-weight +1 component is (1/2) d_A(B_t/alpha) at a critical orbit.
K = sp.Matrix([0, 1, 0, 0])
N = sp.Matrix([-1 / alpha, -1 / (2 * alpha**2), 0, 0])
rim_metric = g.applyfunc(on_rim)
assert simp((K.T * rim_metric * K)[0]) == 0
assert simp((N.T * rim_metric * N)[0]) == 0
assert simp((K.T * rim_metric * N)[0] + 1) == 0

for A_index, b_tA, a_A in ((2, btr, ar), (3, btz, az)):
    # R(K,N,K,e_A) = -(1/alpha) R_{phi t phi A}.
    plus_one = at_critical_rim(-riemann_lower(1, 0, 1, A_index) / alpha)
    expected_plus_one = simp(b_tA / (2 * alpha) - a_A * bt / (2 * alpha**2))
    assert simp(plus_one - expected_plus_one) == 0


if __name__ == "__main__":
    print("Inverse metric, rim-normal norm, and Killing acceleration: verified.")
    print("\nR(K,e_A,K,e_B) on B=0:")
    sp.pprint(rim_optical)
    print("\nAt a transverse critical orbit (B_r=B_z=0):")
    sp.pprint(critical_optical)
    print("\nAll exact transition-rim assertions passed.")
