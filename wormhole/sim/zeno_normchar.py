import sympy as sp
t, rho, phi, z, R = sp.symbols('t rho phi z R', positive=True)
chi = sp.Function('chi')(rho, z); b = sp.Function('b')(t)
B  = (1-chi)*rho**2 + R**2*chi*(1-chi+b)
Q2 = B + R**2*chi**2
coords=(t,rho,phi,z)
g = sp.Matrix([[-1,0,R*chi,0],[0,1,0,0],[R*chi,0,B,0],[0,0,0,1]])
gi = sp.simplify(g.inv())
print("inverse metric entries:")
for lbl,(i,j) in {'g^tt':(0,0),'g^tphi':(0,2),'g^phiphi':(2,2)}.items():
    print(f"   {lbl} =", sp.simplify(gi[i,j]))
dB = sp.Matrix([sp.diff(B,c) for c in coords])
norm = sp.simplify(sum(gi[i,j]*dB[i]*dB[j] for i in range(4) for j in range(4)))
print("\n|dB|^2 (general) =", sp.simplify(sp.factor(norm)))
# on the surface B = 0
bsol = sp.solve(sp.Eq(B,0), b)[0]
norm0 = sp.simplify(norm.subs(b, bsol).doit())
print("\n|dB|^2 ON B=0 =", sp.simplify(sp.factor(norm0)))
print("   compare (dB/drho)^2+(dB/dz)^2 =",
      sp.simplify(sp.factor((sp.diff(B,rho)**2 + sp.diff(B,z)**2).subs(b,bsol).doit())))
core = {sp.Derivative(chi,rho):0, sp.Derivative(chi,z):0}
print("\nON B=0 in the CORE (chi=1, dchi=0):",
      sp.simplify(norm0.subs(core).subs(chi,1)))
