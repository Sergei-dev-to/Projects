"""Exact successive resolutions of the background spatial-infinity junction.

Distinguishes a directional blow-up (not a regular conformal boundary),
regular ordinary scri, regular cap crossings, and a degenerate stationary
end face. This is a boundary analysis, not a completed global diagram.
"""
from pathlib import Path
import json
import sympy as sp
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
import capped_horizon_atlas as cap
import global_spacelike_flow as flow

OUT=Path(__file__).resolve().parents[1]/'output/junction_blowup'


def check():
    r,s,theta=sp.symbols('r s theta',positive=True,real=True)
    # Lab coordinates t=s/r, X=cos(theta)/r, y=sin(theta)/r.
    lab=sp.Matrix([s/r,sp.cos(theta)/r,sp.sin(theta)/r])
    J=lab.jacobian([r,s,theta]);flat=sp.diag(-1,1,1)
    directional=(J.T*flat*J).applyfunc(sp.trigsimp)
    expected=sp.Matrix([[(1-s*s)/r**4,s/r**3,0],
                        [s/r**3,-1/r**2,0],[0,0,1/r**2]])
    assert (directional-expected).applyfunc(sp.simplify)==sp.zeros(3)
    # Ordinary scri is the secondary scaling s=1+u*r.
    u=sp.symbols('u',real=True)
    K=sp.Matrix([r,1+u*r,theta]).jacobian([r,u,theta])
    scri=(r*r*K.T*directional.subs(s,1+u*r)*K).applyfunc(sp.simplify)
    target=sp.Matrix([[0,1,0],[1,-r*r,0],[0,0,1]])
    assert scri==target and scri.det()==-1
    assert scri.inv()[0,0].subs(r,0)==0
    # Exponentially resolved cap: x=1+q*lambda, t=-log(q).
    q,lam,y=sp.symbols('q lam y',real=True)
    xx=1+q*lam;v=-(1+xx*xx)/2
    physical=sp.Matrix([[v*v-1,-v,0],[-v,1,0],[0,0,1]])
    Jcap=sp.Matrix([[-1/q,0,0],[lam,q,0],[0,0,1]]) # q,lambda,y
    gc=(Jcap.T*physical*Jcap).applyfunc(sp.simplify)
    expected_cap=sp.Matrix([[lam*lam+q*q*lam**4/4,-1-q*q*lam*lam/2,0],
                           [-1-q*q*lam*lam/2,q*q,0],[0,0,1]])
    assert (gc-expected_cap).applyfunc(sp.simplify)==sp.zeros(3)
    assert sp.simplify(gc.det())==-1
    inverse=gc.inv().applyfunc(sp.simplify)
    assert inverse[0,0].subs(q,0)==0
    time_covector=sp.Matrix([-1,-1,0]) # T_cap=-q-lambda
    time_norm=sp.expand((time_covector.T*inverse*time_covector)[0])
    assert sp.simplify(time_norm+2+lam*lam+q*q*(1+lam*lam+lam**4/4))==0
    # A timelike crossing from the original interior: lambda=-.4+q.
    velocity=sp.Matrix([1,1,0])
    crossing_norm=sp.expand((velocity.T*gc*velocity)[0].subs(lam,-sp.Rational(2,5)+q))
    crossing=sp.lambdify(q,crossing_norm,'mpmath')
    assert max(crossing(mp.mpf(k)/1000) for k in range(51))<0
    # Retain finite comoving x,y while q->0: Omega=q times a smooth
    # positive coefficient gives a rank-one boundary tensor in this zoom.
    x,vv=sp.symbols('x vv',real=True)
    Jstationary=sp.Matrix([[-1/q,0,0],[0,1,0],[0,0,1]])
    old=sp.Matrix([[vv*vv-1,-vv,0],[-vv,1,0],[0,0,1]])
    stationary=(q*q*Jstationary.T*old*Jstationary).applyfunc(sp.simplify)
    assert stationary==sp.Matrix([[vv*vv-1,vv*q,0],[vv*q,q*q,0],[0,0,q*q]])
    assert stationary.subs(q,0)==sp.diag(vv*vv-1,0,0)

    mp.mp.dps=70
    tests=[];inverse_error=mp.mpf(0)
    for tt in (mp.mpf(5),mp.mpf(10),mp.mpf(20)):
        qq=mp.exp(-tt)
        for name,xx,yy in [('rider',mp.mpf(0),mp.mpf(0)),
                            ('cap',1+qq*(-mp.mpf('.4')+qq),mp.mpf('.3'))]:
            labx=xx+2*tt;R=mp.sqrt(labx*labx+yy*yy)
            rr=1/R;ss=tt/R;th=mp.atan2(yy,labx)
            xi=(mp.cos(th)-2*ss)/rr;yi=mp.sin(th)/rr
            lc=(xi-1)/qq
            inverse_error=max(inverse_error,abs(xi-xx),abs(yi-yy))
            tests.append(dict(kind=name,t=float(tt),s=float(ss),theta=float(th),
                              recovered_x=float(xi),lambda_coordinate=float(lc)))
    ordinary=[]
    for angle in (mp.mpf(0),mp.pi/3):
        R=mp.mpf('1000000');ret=mp.mpf('.7');tt=R+ret
        xx=R*mp.cos(angle)-2*tt;yy=R*mp.sin(angle)
        ordinary.append(dict(theta=float(angle),s=float(tt/R),
                             recovered_retarded_time=float((tt/R-1)*R),
                             comoving_x=float(xx),comoving_y=float(yy)))
    proper=mp.quad(lambda qq:mp.sqrt(-crossing(qq)),[0,mp.mpf('.05')])
    labels=[]
    for time in (5.,10.,20.):
        qq=np.exp(-time)
        for name,xx in [('rider',0.),('cap',1+qq*(-.4+qq)),('ordinary_forward_scri',-time-.7)]:
            sol=solve_ivp(lambda t,z:[float(cap.shift(z[0],0))+1+flow.epsilon(t)],
                          [time,0],[xx],method='DOP853',rtol=2e-12,atol=2e-13,max_step=.04)
            assert sol.success
            labels.append(dict(kind=name,t=time,A=float(sol.y[0,-1])))
    crit=float(json.loads((flow.OUT/'checks.json').read_text())['separatrix_shooting'][-1])
    final={row['kind']:row['A'] for row in labels if row['t']==20.}
    assert final['ordinary_forward_scri']<crit<final['cap']
    assert abs(final['rider']-crit)<1e-7
    asymptotics=[]
    for gap in (.03,.01,.003,.001,.0003):
        Acap=crit+gap
        regular,qstart=flow.cap_limit(Acap)
        L0=float(regular.sol(0)[0])
        def exit_left(t,z):return z[0]+2
        exit_left.terminal=True
        exit_left.direction=-1
        sol=solve_ivp(lambda t,z:[float(cap.shift(z[0],0))+1+flow.epsilon(t)],
                      [0,50],[crit-gap],events=exit_left,method='DOP853',
                      rtol=2e-12,atol=2e-13,max_step=.04)
        assert sol.success and len(sol.t_events[0])==1
        time=float(sol.t_events[0][0])
        scattering=-2+time-flow.ETA*np.tanh(time)
        ret=-flow.ETA-scattering
        asymptotics.append(dict(gap=gap,cap_lambda=L0,minus_gap_lambda=-gap*L0,
                               ordinary_u=ret,u_minus_log_gap=ret-np.log(gap)))
    report=dict(directional_metric='r^-4(1-s^2)dr^2+2s r^-3 dr ds-r^-2 ds^2+r^-2 dtheta^2',
                ordinary_scri='s=1+u r; r^2 g=2 du dr-r^2 du^2+dtheta^2; det=-1',
                future_bubble_direction=dict(s=.5,theta=0),
                bubble_zoom='x=(cos(theta)-2s)/r; y=sin(theta)/r',
                cap_zoom='q=exp(-s/r); lambda=(x-1)/q',
                cap_metric=sp.sstr(gc),cap_determinant=-1,
                cap_time_norm=sp.sstr(time_norm),
                cap_Omega_limit='1/sqrt(1+lambda^2)>0',
                timelike_crossing_proper_time=float(proper),
                stationary_end_metric='Omega=q: diag(v^2-1,0,0) at q=0; degenerate',
                inverse_error=float(inverse_error),approach_tests=tests,ordinary_scri_tests=ordinary,
                global_flow_separatrix=crit,global_flow_labels=labels,
                junction_asymptotics=asymptotics,
                scope='Exact separation of approach sectors and regular cap/scri metrics; rider end retained as a singular ideal end, not a smooth conformal vertex. No complete global diagram claimed.')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':check()
