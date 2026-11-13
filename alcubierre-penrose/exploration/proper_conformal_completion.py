"""One explicit global conformal factor, regular scri and regular cap passage.

This constructs the actual curved rescaled metric, not a flat cone proxy.
The regular open completion is checked; singular rider/spatial/rim ideal
ends are not claimed to have been compactified into a global closed domain.
"""
import json
import sys

import numpy as np
import sympy as sp
import mpmath as mp

import capped_horizon_atlas as cap


def cap_factor(t,x):
    t,x=np.broadcast_arrays(np.asarray(t,dtype=float),np.asarray(x,dtype=float))
    with np.errstate(divide='ignore'):
        plus=2*t+2*np.log(np.abs(1-x))
        minus=-2*t+2*np.log(np.abs(1+x))
    front=np.exp(-.5*np.logaddexp(0,plus)-.5*np.logaddexp(0,-2*t))
    rear=np.exp(-.5*np.logaddexp(0,minus)-.5*np.logaddexp(0,2*t))
    return front+rear


def global_factor(t,x,y):
    t,x,y=np.broadcast_arrays(np.asarray(t,dtype=float),np.asarray(x,dtype=float),
                               np.asarray(y,dtype=float))
    cutoff=1-cap.step((x*x+y*y-4)/5)
    radius2=(x+2*t)**2+y*y
    infinity=1/np.sqrt(1+radius2)
    return cutoff*cap_factor(t,x)+(1-cutoff)*infinity


def outer_metric(r,past=False):
    z=1-r;d=r*r+z*z;H=r/np.sqrt(d)
    sign=1 if past else -1
    return np.array([[-z*z,sign*H,0],[sign*H,1/d,0],[0,0,r*r]])/d


def cap_extension_factor(p,q,collar):
    x=collar.x_from_product(p*q)
    Q=collar.pq_factors(x)[1]
    k=q/Q
    s=p*(1+x)/collar.scale
    front=1/np.sqrt((1+s*s)*(1+k*k))
    # Signed k is the smooth continuation across q=0. The original
    # finite-t formula gives k>0; no absolute value is inserted at the exit.
    rear=k/np.sqrt((1+(1+x)**2*k*k)*(1+k*k))
    return front+rear,x


def audit():
    r=sp.symbols('r',positive=True)
    z=1-r;d=r*r+z*z
    g=sp.Matrix([[-z*z,-r/sp.sqrt(d),0],[-r/sp.sqrt(d),1/d,0],[0,0,r*r]])/d
    assert sp.simplify(g.det()+r*r/d**3)==0
    assert sp.simplify(g.inv()[0,0]+1)==0
    assert g.subs(r,1)==sp.Matrix([[0,-1,0],[-1,1,0],[0,0,1]])
    assert sp.simplify(g.inv()[1,1].subs(r,1))==0
    # Interior global rescaling is positive and Lorentzian.
    rng=np.random.default_rng(1101)
    t=rng.uniform(-20,20,4000);x=rng.uniform(-4,4,4000);y=rng.uniform(-3,3,4000)
    omega=global_factor(t,x,y)
    assert np.all(np.isfinite(omega)) and np.min(omega)>0
    time=np.linspace(-20,20,101)
    assert np.max(np.abs(global_factor(time,0*time,0*time)-1/np.cosh(time)))<1e-14

    # Independent high-precision pullback in the exact exterior, including
    # the near-scri cancellations which are unsuitable for ordinary floats.
    mp.mp.dps=70
    errors=[]
    for rtext in ('.98','.999','.999999'):
        rr=mp.mpf(rtext);zz=1-rr;dd=rr*rr+zz*zz
        R=rr/zz;H=R/mp.sqrt(1+R*R)
        om=1/mp.sqrt(1+R*R)
        for past in (False,True):
            sign=1 if past else -1
            # t=tau+sqrt(...) for future, minus sqrt(...) for past.
            time_sign=1 if not past else -1
            for angle in (mp.mpf(0),mp.pi/3,mp.pi):
                tau=mp.mpf('.7')
                tt=tau+time_sign*mp.sqrt(1+R*R)
                xx=R*mp.cos(angle)-2*tt;yy=R*mp.sin(angle)
                assert xx*xx+yy*yy>9
                jac=mp.matrix([[1,time_sign*H/zz**2,0],
                               [-2,(mp.cos(angle)-2*time_sign*H)/zz**2,-R*mp.sin(angle)],
                               [0,mp.sin(angle)/zz**2,R*mp.cos(angle)]])
                physical=mp.matrix([[3,2,0],[2,1,0],[0,0,1]])
                pulled=om*om*jac.T*physical*jac
                expected=mp.matrix([[-zz*zz,sign*rr/mp.sqrt(dd),0],
                                    [sign*rr/mp.sqrt(dd),1/dd,0],[0,0,rr*rr]])/dd
                errors.append(float(max(abs(v) for v in pulled-expected)))
    assert max(errors)<1e-50

    sys.path.insert(0,str(cap.ROOT/'paper/supplement/scripts'))
    from meridional_geometry import FrontCollar
    collar=FrontCollar('cap')
    match=[];exits=[];minimum_eigenvalue_gap=1.
    for p in (-1.,0.,1.):
        expected=1/np.sqrt(1+(2*p/collar.scale)**2)
        for q in (-.003,0.,.003):
            om,xcap=cap_extension_factor(p,q,collar)
            assert om>0 and abs(xcap*xcap-1)<.25
            cc=collar.C(xcap)
            gg=om*om*np.array([[0,cc/2,0],[cc/2,0,0],[0,0,1]])
            eigen=np.linalg.eigvalsh(gg)
            assert eigen[0]<0<eigen[1]
            assert abs(np.linalg.det(gg)+om**6*cc**2/4)<1e-13
            if q>0:
                Q=collar.pq_factors(xcap)[1]
                tt=np.log(Q/q)
                err=abs(float(global_factor(tt,xcap,.3))-om)
                match.append(err)
            if q==0:
                assert abs(om-expected)<1e-14
                exits.append(dict(p=p,Omega=om,metric_determinant=float(np.linalg.det(gg))))
    assert max(match)<1e-13
    # Near each finite future-scri cut, the global factor is EXACTLY the
    # exterior factor: the compact comoving cutoff is identically zero.
    cutoff_errors=[]
    for rr in (.98,.999,.9999):
        R=rr/(1-rr)
        for tau in (-2.,0.,2.):
            tt=tau+np.sqrt(1+R*R)
            for th in (0.,np.pi/2,np.pi):
                xx=R*np.cos(th)-2*tt;yy=R*np.sin(th)
                cutoff_errors.append(abs(float(global_factor(tt,xx,yy))-1/np.sqrt(1+R*R)))
    assert max(cutoff_errors)<1e-14
    report=dict(exterior_metric='[[-z^2,-r/sqrt(d),0],[-r/sqrt(d),1/d,0],[0,0,r^2]]/d; z=1-r,d=r^2+z^2',
                exterior_determinant='-r^2/d^3',inverse_time_metric=-1,
                future_scri_metric=[[0,-1,0],[-1,1,0],[0,0,1]],
                independent_pullback_error=max(errors),global_factor_min_on_sample=float(np.min(omega)),
                cap_chart_factor_matching_error=max(match),regular_cap_exits=exits,
                scri_cutoff_error=max(cutoff_errors),
                scope='One global rescaling and a regular conformal completion at open ordinary scri, with regular cap continuation. Rider/spatial/rim corner completion is not constructed.')
    (cap.OUT/'proper_conformal_completion_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    audit()
