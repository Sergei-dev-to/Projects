"""Symbolic check of Natario's streamfunction turning-point sign.

At a zero-angular-momentum zero-energy ray, branch changes can occur only on
the axis or on S=|X|=1.  This script verifies the nonaxial wall identity

    Psi'' = -sin(theta)^2/2 *
            [r(a+b) d_r(S^2) + 2 a (2ab+b^2) cos(theta)^2].

For a monotone inner wall every factor in brackets is positive, so every
turning point is a strict maximum of Psi.
"""

import sympy as sp


r, theta = sp.symbols("r theta", positive=True, real=True)
a = sp.Function("a")(r)
b = sp.Function("b")(r)

s2 = a**2 * sp.cos(theta) ** 2 + (a + b) ** 2 * sp.sin(theta) ** 2
d = sp.expand((a + b) ** 2 - a**2)

# Orthonormal polar components of grad(Psi), where
# Psi=-(a/2) r^2 sin(theta)^2.
grad_psi_r = -r * (a + b) * sp.sin(theta) ** 2
grad_psi_theta = -a * r * sp.sin(theta) * sp.cos(theta)

grad_s2_r = sp.diff(s2, r)
grad_s2_theta = sp.diff(s2, theta) / r

# Meridional orthonormal components of the shift.
shift_r = -a * sp.cos(theta)
shift_theta = (a + b) * sp.sin(theta)
streamline_residual = sp.simplify(
    shift_r * grad_psi_r + shift_theta * grad_psi_theta
)
gradient_norm_residual = sp.simplify(
    grad_psi_r**2
    + grad_psi_theta**2
    - (r * sp.sin(theta)) ** 2 * s2
)

psi_second = sp.factor(
    sp.Rational(1, 2)
    * (grad_psi_r * grad_s2_r + grad_psi_theta * grad_s2_theta)
)
target = -sp.sin(theta) ** 2 / 2 * (
    r * (a + b) * grad_s2_r + 2 * a * d * sp.cos(theta) ** 2
)

print("S^2 =", s2)
print("D =", d)
print("X dot grad(Psi) =", streamline_residual)
print("|grad(Psi)|^2-rho^2 S^2 =", gradient_norm_residual)
print("Psi'' at S=1 =", psi_second)
print("target difference =", sp.simplify(psi_second - target))

assert streamline_residual == 0
assert gradient_norm_residual == 0
assert sp.simplify(psi_second - target) == 0
