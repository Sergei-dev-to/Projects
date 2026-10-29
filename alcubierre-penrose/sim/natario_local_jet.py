"""Closed local-jet curvature at the front axis of Natario's shift.

The metric convention is
    ds^2 = -dt^2 + delta_ij (dx^i - X^i dt)(dx^j - X^j dt).
Only the two-jet of X at the axial point is retained.
"""

import sympy as sp

t, x, y, z = sp.symbols("t x y z", real=True)
coords = (t, x, y, z)

a, c, bx, by, bz, d = sp.symbols("a c b_x b_y b_z d", real=True)

# Axisymmetric jet sufficient for R_tyty and R_txtx.
Xx = -1 + a*x + sp.Rational(1, 2)*(bx*x**2 + by*y**2 + bz*z**2)
Xy = c*y + d*x*y
Xz = c*z + d*x*z
X = (Xx, Xy, Xz)

g = sp.zeros(4)
g[0, 0] = -1 + sum(q*q for q in X)
for i in range(3):
    g[0, i + 1] = g[i + 1, 0] = -X[i]
    g[i + 1, i + 1] = 1

origin = {x: 0, y: 0, z: 0}
g0 = sp.simplify(g.subs(origin))
gi0 = sp.simplify(g0.inv())

D = [[[sp.diff(g[i, j], coords[k]).subs(origin)
       for k in range(4)] for j in range(4)] for i in range(4)]
DD = [[[[sp.diff(g[i, j], coords[k], coords[l]).subs(origin)
         for l in range(4)] for k in range(4)]
       for j in range(4)] for i in range(4)]

def gamma(up, lo1, lo2):
    return sp.simplify(sp.Rational(1, 2) * sum(
        gi0[up, m] * (D[m][lo1][lo2] + D[m][lo2][lo1] - D[lo1][lo2][m])
        for m in range(4)
    ))

G = [[[gamma(i, j, k) for k in range(4)] for j in range(4)]
     for i in range(4)]

def d_inverse(up1, up2, deriv):
    return sp.simplify(-sum(
        gi0[up1, p] * D[p][q][deriv] * gi0[q, up2]
        for p in range(4) for q in range(4)
    ))

def dgamma(up, lo1, lo2, deriv):
    first = sp.Rational(1, 2) * sum(
        d_inverse(up, m, deriv)
        * (D[m][lo1][lo2] + D[m][lo2][lo1] - D[lo1][lo2][m])
        for m in range(4)
    )
    second = sp.Rational(1, 2) * sum(
        gi0[up, m]
        * (DD[m][lo1][deriv][lo2]
           + DD[m][lo2][deriv][lo1]
           - DD[lo1][lo2][deriv][m])
        for m in range(4)
    )
    return sp.simplify(first + second)

def riemann_up(up, b, cidx, didx):
    return sp.simplify(
        dgamma(up, b, didx, cidx)
        - dgamma(up, b, cidx, didx)
        + sum(G[up][cidx][m] * G[m][b][didx]
              - G[up][didx][m] * G[m][b][cidx]
              for m in range(4))
    )

def riemann_down(i, j, k, l):
    return sp.factor(sum(g0[i, m] * riemann_up(m, j, k, l)
                         for m in range(4)))

def ricci(i, j):
    return sp.factor(sum(riemann_up(aidx, i, aidx, j)
                         for aidx in range(4)))

print("Gamma^t_tt =", G[0][0][0])
print("R_tyty =", riemann_down(0, 2, 0, 2))
print("R_tztz =", riemann_down(0, 3, 0, 3))
print("R_txtx =", riemann_down(0, 1, 0, 1))
print("Ric_tt =", ricci(0, 0))

R, vs, fp, fpp = sp.symbols("R v_s f_p f_pp", positive=True, real=True)
k = 2*vs*fp
natario = {
    a: -k,
    c: k/2,
    bx: -2*vs*fpp,
    by: -2*k/R,
    bz: -2*k/R,
    d: vs*fpp,
}

print("\nNatario substitutions:")
print("kappa =", k)
print("R_tyty =", sp.factor(riemann_down(0, 2, 0, 2).subs(natario)))
print("R_tztz =", sp.factor(riemann_down(0, 3, 0, 3).subs(natario)))
print("R_txtx =", sp.factor(riemann_down(0, 1, 0, 1).subs(natario)))
print("Ric_tt =", sp.factor(ricci(0, 0).subs(natario)))

target_rtyty = -2*k/R - sp.Rational(3, 4)*k**2
target_rictt = 2*target_rtyty
assert sp.simplify(
    riemann_down(0, 2, 0, 2).subs(natario) - target_rtyty
) == 0
assert sp.simplify(
    riemann_down(0, 3, 0, 3).subs(natario) - target_rtyty
) == 0
assert sp.simplify(ricci(0, 0).subs(natario) - target_rictt) == 0
