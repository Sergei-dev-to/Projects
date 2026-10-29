"""
Where is d_t geodesic on the |X|=1 surface?

Method: compute a^mu = Gamma^mu_tt symbolically, THEN substitute local data
(function value and derivatives as independent symbols) so derivatives survive.
"""
import sympy as sp

t, r, th, ph, vs = sp.symbols('t r theta phi v_s', positive=True)
coords = (t, r, th, ph)
n = 4
V, K1, K2 = sp.symbols('V k1 k2')          # v, v', v''   (Alcubierre)
F, F1, F2 = sp.symbols('F F1 F2')          # f, f', f''   (Natario)


def accel(Xr_hat, Xth_hat):
    Xr, Xth = Xr_hat, Xth_hat / r
    W = Xr_hat**2 + Xth_hat**2
    g = sp.Matrix([
        [-1 + W,     -Xr, -r**2 * Xth, 0],
        [-Xr,          1,  0,          0],
        [-r**2 * Xth,  0,  r**2,       0],
        [0,            0,  0,          r**2 * sp.sin(th)**2]])
    gi = g.inv()
    a = []
    for mu in range(n):
        s = 0
        for d in range(n):
            s += gi[mu, d] * (2 * sp.diff(g[d, 0], coords[0]) - sp.diff(g[0, 0], coords[d]))
        a.append(sp.simplify(s / 2))
    return a, sp.simplify(W)


def localise(expr, fn, syms):
    """replace fn, fn', fn'' by independent symbols"""
    e = expr
    e = e.subs(sp.Derivative(fn, (r, 2)), syms[2])
    e = e.subs(sp.Derivative(fn, r), syms[1])
    e = e.subs(fn, syms[0])
    return sp.simplify(e)


print("=" * 74)
print("CONTROL — Alcubierre,  X = v(r) d_x  :  X^rhat = v cos(th), X^thhat = -v sin(th)")
print("=" * 74)
v = sp.Function('v')(r)
aA, WA = accel(v * sp.cos(th), -v * sp.sin(th))
print("|X|^2 =", WA)
aA = [localise(x, v, (V, K1, K2)) for x in aA]
onshell = {V: -1}                       # front: v = -1
lbl = ['t', 'r', 'theta', 'phi']
for i in range(n):
    print(f"  a^{lbl[i]:<6s} = {sp.simplify(sp.factor(aA[i].subs(onshell)))}")
print("\n  -> spatial part vanishes iff sin(th)=0 : the two AXIAL points. Matches the paper.")

print()
print("=" * 74)
print("NATARIO zero-expansion field")
print("=" * 74)
f = sp.Function('f')(r)
aN, WN = accel(-2 * vs * f * sp.cos(th), vs * (2 * f + r * sp.Derivative(f, r)) * sp.sin(th))
WN = localise(WN, f, (F, F1, F2))
aN = [localise(x, f, (F, F1, F2)) for x in aN]
print("|X|^2 =", sp.simplify(sp.factor(WN)))

print("\n--- ON THE AXIS  sin(th)=0  (cos(th)=1), with |X|^2=1  =>  4 v_s^2 F^2 = 1 ---")
axis = {sp.sin(th): 0, sp.cos(th): 1}
for i in range(n):
    e = sp.simplify(aN[i].subs(axis))
    e = sp.simplify(e.subs(F, 1 / (2 * vs)))     # 4 vs^2 F^2 = 1, F>0 branch
    print(f"  a^{lbl[i]:<6s} = {sp.simplify(sp.factor(e))}")

print("\n--- ON THE EQUATOR  cos(th)=0  (sin(th)=1), with |X|^2=1 => v_s(2F+rF1)=1 ---")
eq = {sp.cos(th): 0, sp.sin(th): 1}
sub_eq = {F1: (1 / vs - 2 * F) / r}              # 2F + r F1 = 1/vs
for i in range(n):
    e = sp.simplify(aN[i].subs(eq))
    e = sp.simplify(e.subs(sub_eq))
    print(f"  a^{lbl[i]:<6s} = {sp.simplify(sp.factor(e))}")

print("\n--- GENERIC point of |X|=1 : is the theta-component identically zero? ---")
print("  a^theta =", sp.simplify(sp.factor(aN[2])))
