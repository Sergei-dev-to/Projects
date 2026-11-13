"""Exact check of the note's compact regular extension metric."""
import sympy as s

U, V, kappa, d = s.symbols("U V kappa d", nonzero=True, real=True)
v = -1-kappa*U*V+U**2*V**2*d
# t=-log(U)/kappa, x=x_H+UV; d denotes d(UV,y,z).
jacobian = s.Matrix([[-1/(kappa*U), 0], [V, U]])
original = s.Matrix([[v*v-1, -v], [-v, 1]])
pulled_back = s.simplify(jacobian.T*original*jacobian)
b = V**2*d/kappa
compact = s.Matrix([[U**2*b*b-2*b/kappa, U**2*b-1/kappa],
                    [U**2*b-1/kappa, U**2]])
assert s.simplify(pulled_back-compact) == s.zeros(2)
assert s.simplify(compact.det()) == -1/kappa**2
print("Exact pullback and determinant verified; coefficients are smooth at U=0.")
