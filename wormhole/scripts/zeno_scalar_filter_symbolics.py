"""Symbolic checks for the classical radiation filter on a Misner ribbon.

The canonical two-dimensional metric is

    ds^2 = 2 dT dpsi + B(T) dpsi^2,    psi ~ psi + P.

This script verifies the wave operator, its chiral homogeneous solutions, and
the integrating-factor identity used for the source moment conditions in the
companion research memo.
"""

from __future__ import annotations

import sympy as sp


T, psi, k = sp.symbols("T psi k", real=True)
B = sp.Function("B")(T)
Phi = sp.Function("Phi")(T, psi)

g = sp.Matrix([[0, 1], [1, B]])
g_inv = sp.simplify(g.inv())

# det(g)=-1, so no volume-factor derivatives are hidden.
box_phi = sp.expand(
    sp.diff(g_inv[0, 0] * sp.diff(Phi, T) + g_inv[0, 1] * sp.diff(Phi, psi), T)
    + sp.diff(
        g_inv[1, 0] * sp.diff(Phi, T) + g_inv[1, 1] * sp.diff(Phi, psi),
        psi,
    )
)
expected_box = (
    -B * sp.diff(Phi, T, 2)
    - sp.diff(B, T) * sp.diff(Phi, T)
    + 2 * sp.diff(Phi, T, psi)
)
assert sp.simplify(box_phi - expected_box) == 0

# Verify Phi=F(psi)+G(psi+H(T)) when H'=2/B.
H = sp.Function("H")(T)
F = sp.Function("F")
G = sp.Function("G")
trial = F(psi) + G(psi + H)
trial_box = expected_box.xreplace({Phi: trial}).doit()
trial_box = trial_box.subs(sp.diff(H, T, 2), -2 * sp.diff(B, T) / B**2)
trial_box = trial_box.subs(sp.diff(H, T), 2 / B)
assert sp.simplify(trial_box) == 0

# For a Fourier mode f(T)e^{ik psi}, verify
# d/dT[B exp(-ikH) f'] = exp(-ikH)[(Bf')'-2ik f'].
f = sp.Function("f")(T)
integrating_factor = B * sp.exp(-sp.I * k * H) * sp.diff(f, T)
lhs = sp.diff(integrating_factor, T).subs(sp.diff(H, T), 2 / B)
rhs = sp.exp(-sp.I * k * H) * (
    sp.diff(B * sp.diff(f, T), T) - 2 * sp.I * k * sp.diff(f, T)
)
assert sp.simplify(lhs - rhs) == 0


if __name__ == "__main__":
    print("g^{-1} =")
    sp.pprint(g_inv)
    print("\nBox Phi =")
    sp.pprint(box_phi)
    print("\nChiral solution and source integrating-factor assertions passed.")
