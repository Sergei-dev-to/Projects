"""Global transverse-safe time coordinate and regular cap continuation.

This is one coordinate system on the original spacetime and thin front/rear
cap continuations. It is not yet a compactification of ordinary null infinity.
"""
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
import capped_horizon_atlas as cap

ETA=.05
OUT=Path(__file__).resolve().parents[1]/'output/global_spacelike_flow'


def epsilon(t):
    return ETA/np.cosh(t)**2


def flow(A,t):
    def rhs(time,z):
        x,loga=z
        return [float(cap.shift(x,0))+1+epsilon(time),float(cap.gradient(x,0)[0])]
    sol=solve_ivp(rhs,[0,t],[A,0.],method='DOP853',rtol=3e-12,atol=2e-13,
                  max_step=.08,dense_output=True)
    assert sol.success
    return sol


def cap_limit(A):
    # Switch to regular variables only after checking the exact affine collar.
    time=4.
    while True:
        sol=flow(A,time);x,loga=sol.y[:,-1]
        if x>0 and abs(x*x-1)<.20:break
        time+=2
        if time>40:raise ValueError('This trajectory has not entered the front cap collar')
    q=np.exp(-time);L=(x-1)/q;ell=np.exp(loga+time)
    def rhs(q,z):
        L,ell=z
        return [.5*L*L-4*ETA/(1+q*q)**2,L*ell]
    reg=solve_ivp(rhs,[q,-min(.001,q/2)],[L,ell],method='DOP853',
                  rtol=2e-12,atol=2e-13,dense_output=True,max_step=q/20)
    assert reg.success
    return reg,q


def check():
    # An analytic identity valid for the full transverse-dependent shift.
    a,D=sp.symbols('a D',positive=True)
    g=sp.Matrix([[a*a,-a*D,0],[-a*D,D*D-1,0],[0,0,1]]) # T,t,y
    assert sp.simplify(g.det()+a*a)==0
    assert sp.simplify(g.inv()[0,0]+(D*D-1)/(a*a))==0
    q,L,ell,eta=sp.symbols('q L ell eta',real=True)
    delta=4*eta*q*q/(1+q*q)**2
    B=8*eta/(1+q*q)**2+16*eta*eta*q*q/(1+q*q)**4
    regular=sp.Matrix([[q*q*ell*ell,ell*(1+delta),0],
                       [ell*(1+delta),B,0],[0,0,1]]) # T,q,y
    assert sp.simplify(regular.det()+ell*ell)==0
    assert regular.subs(q,0)==sp.Matrix([[0,ell,0],[ell,8*eta,0],[0,0,1]])
    assert sp.simplify(regular.inv()[0,0]+B/(ell*ell))==0
    # The transverse correction is necessary in the regular exterior
    # null-inversion chart. Verify it independently as a full 3D pullback.
    U,Q,Y=sp.symbols('U Q Y',real=True,nonzero=True)
    invmap=sp.Matrix([U+Y*Y/Q,1/Q,Y/Q]) # (u,v,y)
    J=invmap.jacobian([U,Q,Y])
    flat=sp.Matrix([[0,-sp.Rational(1,2),0],[-sp.Rational(1,2),0,0],[0,0,1]])
    target=sp.Matrix([[0,sp.Rational(1,2),0],[sp.Rational(1,2),0,0],[0,0,1]])
    assert (Q*Q*J.T*flat*J-target).applyfunc(sp.simplify)==sp.zeros(3)

    # The flow has globally bounded velocity and bounded spatial derivative;
    # a=exp(integral v0')>0, so it is a diffeomorphism in its initial label.
    # Monotonicity of W gives v(x,y)<=v0(x), hence D>=1+epsilon>1.
    rng=np.random.default_rng(3091);minimum_margin=1.
    for A in np.linspace(-5,5,31):
        for end in (-10.,10.):
            sol=flow(A,end)
            times=np.linspace(0,end,41)
            xx,logs=sol.sol(times)
            yy=rng.uniform(-4,4,len(xx))
            DD=cap.shift(xx,0)+1+epsilon(times)-cap.shift(xx,yy)
            assert np.all(DD>1) and np.all(np.isfinite(logs))
            minimum_margin=min(minimum_margin,float(np.min(DD-1)))

    # Shooting the asymptotic rear separatrix backward is stable.
    thresholds=[]
    for end in (16.,20.,24.):
        initial=-1-(4*ETA/3)*np.exp(-2*end)
        sol=solve_ivp(lambda t,z:[float(cap.shift(z[0],0))+1+epsilon(t)],
                      [end,0],[initial],method='DOP853',rtol=2e-13,atol=2e-14,max_step=.04)
        assert sol.success
        thresholds.append(float(sol.y[0,-1]))
    assert np.ptp(thresholds)<1e-10
    Acrit=thresholds[-1]
    limits=[]
    for A in (-.9,-.5,0.,.5,1.,2.,4.):
        reg,qstart=cap_limit(A)
        L0,ell0=reg.sol(0.)
        assert ell0>0
        for qq in (qstart/2,0.,reg.t[-1]):
            LL,ee=reg.sol(qq);xx=1+qq*LL
            assert abs(xx*xx-1)<.25
            dd=4*ETA*qq*qq/(1+qq*qq)**2
            bb=8*ETA/(1+qq*qq)**2+16*ETA**2*qq*qq/(1+qq*qq)**4
            metric=np.array([[qq*qq*ee*ee,ee*(1+dd),0],
                             [ee*(1+dd),bb,0],[0,0,1]])
            assert np.linalg.det(metric)<0 and np.linalg.inv(metric)[0,0]<0
            om=1/np.sqrt((1+LL*LL)*(1+qq*qq))+qq/np.sqrt((1+(2+qq*LL)**2*qq*qq)*(1+qq*qq))
            assert om>0
        limits.append(dict(A=A,T=-A,L=float(L0),ell=float(ell0),
                           Omega=1/float(np.sqrt(1+L0*L0)),
                           physical_inverse_time=-8*ETA/float(ell0*ell0)))
    report=dict(eta=ETA,global_coordinates='T=-A, z=tanh(t/2), y; x=F(t,A)',
        flow='dF/dt=v(F,0)+1+eta sech(t)^2; F(0,A)=A',
        temporal_identity='g^{-1}(dT,dT)=-(D^2-1)/a^2<0; D=1+epsilon+v0-v',
        sampled_min_D_minus_one=minimum_margin,separatrix_shooting=thresholds,
        front_cap_T_upper=-Acrit,rear_cap_T_lower=Acrit,
        front_cap_limits=limits,
        cap_boundary_metric='in (T,q,y): [[0,ell,0],[ell,8 eta,0],[0,0,1]]',
        cap_Omega='1/sqrt(1+L^2)>0',
        unresolved='Ordinary scri needs a further joint coordinate construction; z=tanh(t/2) is singular there. This is not the requested completed compactification.')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':check()
