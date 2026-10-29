"""Symbolic checks for the Natario omega-limit reduction."""

import sympy as sp


# A generic smooth axisymmetric no-swirl field can be written locally as
# X=(A(x,rho^2), B(x,rho^2)y, B(x,rho^2)z).
x, y, z = sp.symbols("x y z", real=True)
A, B = sp.symbols("A B", real=True)
Ax, Au, Bx, Bu = sp.symbols("A_x A_u B_x B_u", real=True)
lam = sp.symbols("lambda", real=True)
px, py, pz = sp.symbols("p_x p_y p_z", real=True)

X = sp.Matrix([A, B * y, B * z])
P = sp.Matrix([px, py, pz])

# Rows label vector components and columns label x,y,z derivatives.
DX = sp.Matrix(
    [
        [Ax, 2 * y * Au, 2 * z * Au],
        [y * Bx, B + 2 * y**2 * Bu, 2 * y * z * Bu],
        [z * Bx, 2 * y * z * Bu, B + 2 * z**2 * Bu],
    ]
)

position_prime = X + lam * P
momentum_prime = -DX.T * P
J_prime = sp.expand(
    position_prime[1] * pz
    + y * momentum_prime[2]
    - position_prime[2] * py
    - z * momentum_prime[1]
)

# For the limiting flow, H=X.m obeys H'=(1+H)m^T DX m on |m|=1.
mx, my, mz = sp.symbols("m_x m_y m_z", real=True)
m = sp.Matrix([mx, my, mz])
H = (X.T * m)[0]
m_prime = -(sp.eye(3) - m * m.T) * DX.T * m
H_prime = (DX.T * m).dot(X + m) + X.dot(m_prime)
constraint_target = (1 + H) * (m.T * DX * m)[0]

# The H identity is exact even off the unit sphere. The unit-norm identity
# has the expected (|m|^2-1) factor.
constraint_residual = sp.factor(H_prime - constraint_target)

unit_prime = sp.expand(2 * m.dot(m_prime))
unit_target = sp.expand(
    2 * (m.dot(m) - 1) * (m.T * DX.T * m)[0]
)

print("angular momentum residual =", sp.factor(J_prime))
print("constraint residual =", constraint_residual)
print("unit-sphere residual =", sp.factor(unit_prime - unit_target))

assert sp.simplify(J_prime) == 0
assert sp.simplify(constraint_residual) == 0
assert sp.simplify(unit_prime - unit_target) == 0
