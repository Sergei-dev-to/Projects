"""Audit smooth conformal resolution of the tube's pinched rider endpoints.

Does not assume that a singular global diagram is impossible. Checks a
specific coordinate-limit failure, and invariant regularity obstructions
to replacing the pinched ends by smooth conformal boundary points.
"""
import json
import numpy as np
import sympy as sp

import band_tube_shape as band


def christoffel(g,coords):
    n=len(coords);inv=g.inv()
    return [[[sp.simplify(sum(inv[a,d]*(sp.diff(g[d,b],coords[c])+
                 sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
                 for d in range(n))/2) for c in range(n)]
                 for b in range(n)] for a in range(n)]


def curvature(g,coords):
    n=len(coords);ga=christoffel(g,coords)
    ric=sp.Matrix(n,n,lambda a,b:sp.simplify(sum(
        sp.diff(ga[c][a][b],coords[c])-sp.diff(ga[c][a][c],coords[b])+
        sum(ga[c][c][d]*ga[d][a][b]-ga[c][b][d]*ga[d][a][c] for d in range(n))
        for c in range(n))))
    scalar=sp.simplify(sum(g.inv()[a,b]*ric[a,b] for a in range(n) for b in range(n)))
    return ga,ric,scalar


def cotton(g,coords):
    n=3;ga,ric,scalar=curvature(g,coords)
    sch=ric-scalar*g/4
    def deriv(a,b,c):
        return sp.diff(sch[a,b],coords[c])-sum(
            ga[d][c][a]*sch[d,b]+ga[d][c][b]*sch[a,d] for d in range(n))
    result={}
    for a in range(n):
        for b in range(n):
            for c in range(n):
                val=sp.simplify(deriv(a,b,c)-deriv(a,c,b))
                if val!=0:result[a,b,c]=val
    return result,scalar


def norm(tensor,g):
    inv=g.inv()
    return sp.simplify(sum(v*w*inv[a,d]*inv[b,e]*inv[c,f]
        for (a,b,c),v in tensor.items() for (d,e,f),w in tensor.items()))


def audit():
    t,x,y=sp.symbols('t x y',real=True)
    v=-(1+x*x)/2
    g=sp.Matrix([[v*v-1,-v,0],[-v,1,0],[0,0,1]])
    C,R=cotton(g,(t,x,y))
    assert sp.simplify(R-(1+3*x*x))==0
    c2=norm(C,g)
    assert sp.simplify(c2-(1-v*v)*sp.diff(R,x)**2/4)==0
    # Check the (0,3) Cotton convention against an actual nonconstant
    # conformal rescaling, independently of the norm-weight argument.
    rescaled=sp.exp(2*x)*g
    Cr,_=cotton(rescaled,(t,x,y))
    assert set(C)==set(Cr)
    assert all(sp.simplify(C[k]-Cr[k])==0 for k in C)
    assert sp.simplify(norm(Cr,rescaled)-sp.exp(-6*x)*c2)==0
    # In 4D the exact cap is the product g2+dy^2+dz^2. Its invariants:
    # Riemann^2=R2^2, Ricci^2=R2^2/2, Weyl^2=Riem^2-2 Ricci^2+R^2/3.
    weyl2=sp.simplify(R**2-2*(R**2/2)+R**2/3)
    assert weyl2==R**2/3

    tube=band.Tube()
    probes=[]
    for xx in (0.,.5,.9,.95):
        F=np.exp(-float(tube.Jpos(xx)))
        coef=float(tube.Cpos(xx))*(1+F)**2/tube.C0
        probes.append(dict(x=xx,limiting_axial_metric_coefficient=coef))
    assert abs(probes[0]['limiting_axial_metric_coefficient']-
               probes[-1]['limiting_axial_metric_coefficient'])>.1
    xx=.95
    Rvalue=float(R.subs(x,xx))
    Cvalue=float(c2.subs(x,xx))
    Wvalue=float(weyl2.subs(x,xx))
    assert Cvalue>0 and Wvalue>0
    assert abs(float(band.cap.shift(xx,.3))-float(v.subs(x,xx)))<1e-14
    growth=[]
    # Construct p and q at a fixed x using Q and F; only their product is
    # needed for the late-time rate. Arbitrary finite positive Q is sufficient
    # for the divergence test; use Q=1 as a time-origin normalization.
    F=np.exp(-float(tube.Jpos(xx)))
    for tt in (5.,10.,20.):
        pp=F*np.exp(tt);qq=np.exp(-tt)
        sigma=(pp-1)/(pp+1);beta=(1-qq)/(1+qq)
        omega=np.sqrt(band.WEIGHT/tube.C0)*(1-sigma*beta)
        growth.append(dict(t=tt,Omega=omega,
                           unphysical_Cotton_squared=Cvalue/omega**6,
                           unphysical_4D_Weyl_squared=Wvalue/omega**4))
    report=dict(cap_curvature_scalar=str(R),cotton_squared=str(sp.factor(c2)),
                four_dimensional_weyl_squared=str(sp.factor(weyl2)),
                fixed_cap_orbit=dict(x=xx,y=.3,physical_R=Rvalue,
                                    physical_Cotton_squared=Cvalue,physical_4D_Weyl_squared=Wvalue),
                incompatible_metric_limits=probes,conformal_growth=growth,
                conclusion='No smooth conformal rider endpoint with Omega->0 along these fixed cap orbits; singular global compactifications are not excluded.',
                regularity='3D obstruction uses C3 unphysical metric; 4D Weyl obstruction uses C2. Neither proves nonexistence of a singular diagram.')
    (band.OUT/'corner_resolution_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    audit()
