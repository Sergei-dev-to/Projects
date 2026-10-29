import math
vs, r0, sig = 2.0, 1.0, 3.0
def f(r):  return 0.25*(1.0+math.tanh(sig*(r-r0)))
def fp(r): return 0.25*sig/math.cosh(sig*(r-r0))**2
def metric(P):
    t,x,y,z=P
    r=math.sqrt(x*x+y*y+z*z); rho2=y*y+z*z
    F,Fp=f(r),fp(r)
    X=[-vs*(2*F*x*x+(2*F+r*Fp)*rho2)/r**2, vs*Fp*x*y/r, vs*Fp*x*z/r]
    g=[[0.0]*4 for _ in range(4)]
    g[0][0]=-1.0+sum(c*c for c in X)
    for i in range(3):
        g[0][i+1]=g[i+1][0]=-X[i]; g[i+1][i+1]=1.0
    return g
def inv4(m):
    n=4; a=[row[:]+[1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(m)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(a[r][c])); a[c],a[p]=a[p],a[c]
        d=a[c][c]
        a[c]=[v/d for v in a[c]]
        for r_ in range(n):
            if r_!=c and a[r_][c]!=0.0:
                fac=a[r_][c]; a[r_]=[v-fac*w for v,w in zip(a[r_],a[c])]
    return [row[n:] for row in a]
def shift(P,c,h): Q=list(P); Q[c]+=h; return Q
h1,h2=1e-4,4e-3
def dg(P,c):
    A=metric(shift(P,c,h1)); B=metric(shift(P,c,-h1))
    return [[(A[i][j]-B[i][j])/(2*h1) for j in range(4)] for i in range(4)]
def ddg(P,c,d):
    pp=metric(shift(shift(P,c,h2),d,h2)); pm=metric(shift(shift(P,c,h2),d,-h2))
    mp=metric(shift(shift(P,c,-h2),d,h2)); mm=metric(shift(shift(P,c,-h2),d,-h2))
    return [[(pp[i][j]-pm[i][j]-mp[i][j]+mm[i][j])/(4*h2*h2) for j in range(4)] for i in range(4)]
P=[0.0,1.0,0.0,0.0]
g=metric(P); gi=inv4(g)
D=[dg(P,c) for c in range(4)]
DD=[[ddg(P,c,d) for d in range(4)] for c in range(4)]
dgi=[[[-sum(gi[a][p]*D[e][p][q]*gi[q][b] for p in range(4) for q in range(4)) for e in range(4)] for b in range(4)] for a in range(4)]
def Gam(a,b,c): return 0.5*sum(gi[a][d]*(D[c][d][b]+D[b][d][c]-D[d][b][c]) for d in range(4))
G=[[[Gam(a,b,c) for c in range(4)] for b in range(4)] for a in range(4)]
def dGam(a,b,c,e):
    s=0.5*sum(gi[a][d]*(DD[e][c][d][b]+DD[e][b][d][c]-DD[e][d][b][c]) for d in range(4))
    s+=0.5*sum(dgi[a][d][e]*(D[c][d][b]+D[b][d][c]-D[d][b][c]) for d in range(4))
    return s
def Riem(a,b,c,d):
    return dGam(a,b,d,c)-dGam(a,b,c,d)+sum(G[a][c][m]*G[m][b][d]-G[a][d][m]*G[m][b][c] for m in range(4))
def Rl(i,j,k,l): return sum(g[i][a]*Riem(a,j,k,l) for a in range(4))
r=1.0
print("X^x at front axial point =", -vs*2*f(r))
print("|X|^2                    =", (vs*2*f(r))**2)
print("kappa = Gamma^t_tt       =", G[0][0][0], "  predicted -2 v_s f'(R_F) =", -2*vs*fp(r0))
print("R_tyty                   =", Rl(0,2,0,2))
print("R_tztz                   =", Rl(0,3,0,3))
print("R_tytz                   =", Rl(0,2,0,3))
print("R_txtx                   =", Rl(0,1,0,1))
print("Ric_tt                    =", sum(Riem(a,0,a,0) for a in range(4)))
