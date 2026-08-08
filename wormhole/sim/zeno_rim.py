"""
Boost-weight +2 check on the chronology boundary B=0 of the localized Zeno
metric, draft Eq. (4.2), INCLUDING the transition region 0<chi<1.

  ds^2 = -(dt - R*chi*dphi)^2 + Q^2 dphi^2 + drho^2 + dz^2
  Q^2  = (1-chi)*rho^2 + chi*R^2*(1+b(t)),      chi = chi(rho,z), b = b(t)

so   g_tt=-1, g_tphi=R*chi, g_phiphi = B = Q^2 - R^2 chi^2, g_rr=g_zz=1
with B = (1-chi)*rho^2 + R^2*chi*(1-chi+b)      [matches draft Eq. (4.4)]

K = d_phi is null on B=0.  With
    N   = -(1/(R chi)) d_t - (1/(2R^2 chi^2)) d_phi     (null, g(K,N)=-1)
    E_1 = d_rho,  E_2 = d_z                              (unit, orthogonal to K,N)
the boost-weight +2 components are simply the coordinate components
    R_{phi rho phi rho},  R_{phi z phi z},  R_{phi rho phi z}
evaluated on B=0.  Nonzero => they scale as q^2 under the affine boost and the
endpoint is a non-scalar (pp) curvature singularity, as in the Alcubierre case.
"""
import sympy as sp

t, rho, phi, z, R = sp.symbols('t rho phi z R', positive=True)
chi = sp.Function('chi')(rho, z)
b = sp.Function('b')(t)

B = (1 - chi) * rho**2 + R**2 * chi * (1 - chi + b)

coords = (t, rho, phi, z)
g = sp.Matrix([
    [-1,        0, R * chi, 0],
    [0,         1, 0,       0],
    [R * chi,   0, B,       0],
    [0,         0, 0,       1],
])

n = 4
gi = g.inv()
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, bb], coords[c])
                                     + sp.diff(g[d, c], coords[bb])
                                     - sp.diff(g[bb, c], coords[d])) for d in range(n)) / 2)
         for c in range(n)] for bb in range(n)] for a in range(n)]

def riem_low(a, bb, c, d):
    expr = sp.diff(Gam[a][bb][d], coords[c]) - sp.diff(Gam[a][bb][c], coords[d])
    for e in range(n):
        expr += Gam[a][c][e] * Gam[e][bb][d] - Gam[a][d][e] * Gam[e][bb][c]
    return expr

def Rlow(i, j, k, l):
    return sp.simplify(sum(g[i, a] * riem_low(a, j, k, l) for a in range(n)))

T, RHO, PHI, Z = 0, 1, 2, 3

print("=" * 72)
print("Boost-weight +2 components on the chronology boundary B = 0")
print("=" * 72)

comps = {
    'R_{phi rho phi rho}': (PHI, RHO, PHI, RHO),
    'R_{phi z   phi z  }': (PHI, Z, PHI, Z),
    'R_{phi rho phi z  }': (PHI, RHO, PHI, Z),
}

raw = {}
for name, idx in comps.items():
    raw[name] = sp.simplify(Rlow(*idx))

# solve B = 0 for b(t) and substitute
bsol = sp.solve(sp.Eq(B, 0), b)[0]
print("\nB = 0  <=>  b(t) =", sp.simplify(bsol), "\n")

for name, expr in raw.items():
    on_shell = sp.simplify(expr.subs(b, bsol).doit())
    print(f"{name} on B=0 :")
    print("   ", sp.simplify(sp.factor(on_shell)))
    print()

print("-" * 72)
print("Same components in the CORE (chi = 1, all chi derivatives = 0)")
print("-" * 72)
core = {sp.Derivative(chi, rho): 0, sp.Derivative(chi, z): 0,
        sp.Derivative(chi, rho, 2): 0, sp.Derivative(chi, z, 2): 0,
        sp.Derivative(chi, rho, z): 0}
for name, expr in raw.items():
    e = expr.subs(core).subs(chi, 1)
    e = sp.simplify(e.subs(b, sp.solve(sp.Eq(B.subs(core).subs(chi, 1), 0), b)[0]))
    print(f"{name} on B=0, core :", sp.simplify(e))

print("\n" + "-" * 72)
print("Is d_phi geodesic on B=0?   (nabla_K K)_a = -(1/2) d_a B")
print("-" * 72)
for lbl, var in (('t', t), ('rho', rho), ('z', z)):
    d = sp.simplify(-sp.diff(B, var) / 2)
    print(f"  -(1/2) d_{lbl} B = {sp.simplify(d)}")
print("\n  K_a on B=0 = (R*chi, 0, 0, 0)  -> geodesic requires d_rho B = d_z B = 0")
print("  core (chi=1, dchi=0):  d_rho B =", sp.simplify(sp.diff(B, rho).subs(core).subs(chi, 1)),
      "   d_z B =", sp.simplify(sp.diff(B, z).subs(core).subs(chi, 1)))
