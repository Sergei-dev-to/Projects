"""Exact checks for the cohomogeneity-one Zeno cylinder.

Metric (phi is periodic):

    ds^2 = -dt^2 + 2 dt dphi + b(t) dphi^2 + dx^2 + dy^2.

The script deliberately leaves b(t) symbolic.  It verifies the connection,
curvature, Einstein tensor, and the parallel-propagated frame used in
``zeno_chronology_exact_results.md``.
"""

from __future__ import annotations

import sympy as sp


t, phi, x, y = sp.symbols("t phi x y", real=True)
coords = (t, phi, x, y)
n = len(coords)
b = sp.Function("b")(t)

g = sp.Matrix(
    [
        [-1, 1, 0, 0],
        [1, b, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
)
g_inv = sp.simplify(g.inv())


def simp(expr: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.simplify(expr)))


Gamma = [
    [
        [
            simp(
                sp.Rational(1, 2)
                * sum(
                    g_inv[rho, sigma]
                    * (
                        sp.diff(g[sigma, nu], coords[mu])
                        + sp.diff(g[sigma, mu], coords[nu])
                        - sp.diff(g[mu, nu], coords[sigma])
                    )
                    for sigma in range(n)
                )
            )
            for nu in range(n)
        ]
        for mu in range(n)
    ]
    for rho in range(n)
]

Ricci = sp.MutableDenseMatrix.zeros(n, n)
for mu in range(n):
    for nu in range(n):
        Ricci[mu, nu] = simp(
            sum(
                sp.diff(Gamma[rho][mu][nu], coords[rho])
                - sp.diff(Gamma[rho][mu][rho], coords[nu])
                + sum(
                    Gamma[rho][rho][sigma] * Gamma[sigma][mu][nu]
                    - Gamma[rho][nu][sigma] * Gamma[sigma][mu][rho]
                    for sigma in range(n)
                )
                for rho in range(n)
            )
        )

scalar_R = simp(sum(g_inv[mu, nu] * Ricci[mu, nu] for mu in range(n) for nu in range(n)))
Einstein = sp.simplify(Ricci - sp.Rational(1, 2) * scalar_R * g)

# Orthonormal frame vectors: e_0 = d_t and
# e_1 = (d_t + d_phi)/sqrt(1+b), followed by d_x,d_y.
a = sp.sqrt(1 + b)
frame = (
    sp.Matrix([1, 0, 0, 0]),
    sp.Matrix([1 / a, 1 / a, 0, 0]),
    sp.Matrix([0, 0, 1, 0]),
    sp.Matrix([0, 0, 0, 1]),
)


def covariant_derivative_along(vector: sp.Matrix, field: sp.Matrix) -> sp.Matrix:
    result = sp.MutableDenseMatrix.zeros(n, 1)
    for rho in range(n):
        result[rho] = simp(
            sum(vector[mu] * sp.diff(field[rho], coords[mu]) for mu in range(n))
            + sum(
                Gamma[rho][mu][nu] * vector[mu] * field[nu]
                for mu in range(n)
                for nu in range(n)
            )
        )
    return sp.Matrix(result)


expected_R = simp(
    (2 * (1 + b) * sp.diff(b, t, 2) - sp.diff(b, t) ** 2)
    / (2 * (1 + b) ** 2)
)

assert simp(scalar_R - expected_R) == 0
assert covariant_derivative_along(frame[0], frame[0]) == sp.zeros(n, 1)
for basis_vector in frame:
    assert covariant_derivative_along(frame[0], basis_vector) == sp.zeros(n, 1)

for i in range(2):
    for j in range(2):
        assert simp(Einstein[i, j]) == 0
assert simp(Einstein[2, 2] + scalar_R / 2) == 0
assert simp(Einstein[3, 3] + scalar_R / 2) == 0


if __name__ == "__main__":
    labels = ("t", "phi", "x", "y")
    print("g^{-1} =")
    sp.pprint(g_inv)
    print("\nNonzero Christoffel symbols:")
    for rho in range(n):
        for mu in range(n):
            for nu in range(mu, n):
                value = simp(Gamma[rho][mu][nu])
                if value != 0:
                    print(f"Gamma^{labels[rho]}_{{{labels[mu]} {labels[nu]}}} = {value}")
    print("\nScalar curvature R =")
    sp.pprint(scalar_R)
    print("\nRicci tensor =")
    sp.pprint(Ricci)
    print("\nEinstein tensor =")
    sp.pprint(Einstein.applyfunc(simp))
    print("\nAll exact assertions passed.")
