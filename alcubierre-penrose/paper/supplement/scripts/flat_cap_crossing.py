"""Exact checks for the timelike crossing and locally flat cap in Section 5.

These identities supplement the analytic proof; they do not model a body's
self-gravity.  Run directly with Python and SymPy.
"""

import sympy as sp

E, mu, P0, kappa = sp.symbols("E mu P0 kappa", positive=True)
v = sp.symbols("v", real=True)
D = sp.sqrt(E**2 - mu**2 * (1-v**2))
P = (-E*v + D) / (1-v**2)
Gamma = (E-v*D) / (1-v**2)
assert sp.simplify(P + v*Gamma - D) == 0
assert sp.simplify(Gamma**2 - P**2 - mu**2) == 0
assert sp.simplify((Gamma + v*P) - E) == 0
assert sp.simplify((D**2).subs(E**2, P0**2 + mu**2)
                   - (P0**2 + mu**2*v**2)) == 0

# Generic smooth product cap, approached from s<0.
s, d0 = sp.symbols("s d0", real=True)
v_cap = -1-kappa*s+d0*s**2
D_cap = D.subs(v, v_cap)
Gamma_cap = Gamma.subs(v, v_cap)
assert sp.limit(D_cap, s, 0, dir="-") == E
assert sp.limit(s*Gamma_cap, s, 0, dir="-") == -E/kappa
# Smooth cap data improve the leading equivalence to ds/dt=-kappa*s+O(s**2).
rate_remainder = sp.limit((D_cap/Gamma_cap+kappa*s)/s**2,
                         s, 0, dir="-")
assert sp.simplify(rate_remainder
                   - (d0-mu**2*kappa**2/(2*E**2))) == 0
# For s=UV: Udot=-kappa*U*Gamma and
# Vdot=(D+kappa*s*Gamma)/U.  Both limits are finite at V != 0.
regular_V_factor = sp.limit((D_cap+kappa*s*Gamma_cap)/s,
                            s, 0, dir="-")
assert sp.simplify(regular_V_factor
                   - (mu**2*kappa/(2*E)-E*d0/kappa)) == 0

v_flat = -sp.sqrt(1+2*kappa*s)
assert v_flat.subs(s, 0) == -1
assert sp.diff(v_flat, s).subs(s, 0) == -kappa
assert sp.diff(v_flat**2, s, 2) == 0
print("PASS: energy, normalization, outgoing speed, regular crossing velocity,")
print("      and exactly flat cap germ.")
