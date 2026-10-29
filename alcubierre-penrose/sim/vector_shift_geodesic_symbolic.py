"""Exact algebra audit for the stationary vector-shift geodesic equations."""

import sympy as sp


n = 3
T = sp.symbols("T", real=True)
V = sp.symbols("V0:3", real=True)
X = sp.symbols("X0:3", real=True)
dX = sp.Matrix(n, n, lambda i, j: sp.symbols(f"dX{i}{j}", real=True))

P = sp.Matrix([V[i] - X[i] * T for i in range(n)])
Xm = sp.Matrix(X)
L = sp.Rational(1, 2) * (-T**2 + (P.T * P)[0])

# E=-p_t and p_i=P_i.
energy_residual = sp.simplify(-sp.diff(L, T) - (T + (Xm.T * P)[0]))
momentum_residuals = [sp.simplify(sp.diff(L, V[i]) - P[i]) for i in range(n)]

# Partial_i L=-T P_j partial_i X^j, so Euler--Lagrange gives
# dot(P_i)=-T (DX)^T_ij P_j.
spatial_rhs_residuals = []
for i in range(n):
    partial_i_L = sum(sp.diff(L, X[j]) * dX[i, j] for j in range(n))
    target = -T * sum(dX[i, j] * P[j] for j in range(n))
    spatial_rhs_residuals.append(sp.simplify(partial_i_L - target))

# The proper-time normalization is 2L=-1, hence T^2=|P|^2+1.
normalization_residual = sp.simplify(2 * L - (-T**2 + (P.T * P)[0]))

checks = {
    "energy": energy_residual,
    "momenta": momentum_residuals,
    "spatial Euler-Lagrange RHS": spatial_rhs_residuals,
    "normalization identity": normalization_residual,
}

print(checks)
assert energy_residual == 0
assert all(item == 0 for item in momentum_residuals)
assert all(item == 0 for item in spatial_rhs_residuals)
assert normalization_residual == 0
