"""Continue the plotted analytic planar cap germ, independently of its cutoff.

This is not an analytic continuation of the entire nonanalytic compact bubble.
The actual profile equals the polynomial only in a cap collar. Its analytic
germ nevertheless selects this polynomial on a chosen added product branch.
"""
import json
import sys
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'paper/supplement/scripts'))
from meridional_geometry import FrontCollar


def main():
    x=sp.symbols('x',real=True)
    v=-(1+x*x)/2
    F=sp.factor(1-v*v)
    R=sp.simplify(-sp.diff(F,x,2))
    assert sp.simplify(F-(1-x*x)*(x*x+3)/4)==0
    assert R==1+3*x*x
    k,r,T=sp.symbols('k r T',positive=True,real=True)
    minkowski=sp.Matrix([r*sp.sinh(k*T),r*sp.cosh(k*T)])
    jac=minkowski.jacobian([T,r])
    assert sp.simplify(jac.T*sp.diag(-1,1)*jac-sp.diag(-k*k*r*r,1))==sp.zeros(2)
    elapsed,E=sp.symbols('elapsed E',nonnegative=True,real=True)
    outgoing=E*elapsed+k*elapsed**2/2
    assert sp.simplify(sp.diff(outgoing,elapsed)**2-E**2-2*k*outgoing)==0
    collar=FrontCollar('cap');sol,cross=collar.geodesic()
    p,q,dp,dq=sol.sol(0);x0=collar.x_from_product(p*q)
    energy=-collar.C(x0)*(p*dq-q*dp)/2
    proper,err=quad(lambda z:1/np.sqrt(energy*energy-(1-z*z)*(z*z+3)/4),
                    1,np.inf,epsabs=1e-12,epsrel=1e-12)
    limit=-2*np.exp(-2*np.pi/(3*np.sqrt(3)))
    # Near infinity the proper-time integrand is 2/x^2+O(x^-4).
    for xx in [100.,1000.]:
        assert abs(xx*xx/np.sqrt(energy*energy-float(F.subs(x,xx)))-2)<.001
    rows=[]
    for xx in [2.,5.,10.,100.]:
        pp,qq=collar.pq_factors(xx)
        rows.append(dict(x=xx,pq=float(pp*qq),R=1+3*xx*xx))
    assert abs(rows[-1]['pq']-limit)<2e-6
    report=dict(profile='Analytic continuation of plotted affine-W cap germ only; units L=kappa=1',
        F=str(F),Ricci_scalar=str(R),Kretschmann='(1+3*x^2)^2',
        front_horizon_x=1,rear_horizon_x=-1,
        future_outgoing_curvature_end='x tends to +infinity',
        front_chart_product_limit=float(limit),traveler_Killing_energy=float(energy),
        proper_time_from_front_to_singularity=float(proper),integration_error=float(err),samples=rows,
        null_geodesics='Non-generator longitudinal null geodesics have dx/dlambda=constant; x=infinity is at infinite affine parameter',
        flat_variant='F=-2*kappa*(x-L); locally Minkowski, with a full Minkowski analytic development of the isolated germ',
        scope='Analytic planar cap branch, not a maximal extension of the full compact nonanalytic bubble')
    out=ROOT/'output/useful_2p1_view/analytic_cap_continuation_checks.json'
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
