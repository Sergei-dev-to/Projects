"""Uniform boundary classification and the transverse correction at scri.

No diagram topology is assumed. Symbolic identities, exact exterior
domains, and controlled numerical examples accompany the analytic proof
in notes/joint_boundary_limits.md.
"""
from pathlib import Path
from functools import lru_cache
import json
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.integrate import solve_ivp
import capped_horizon_atlas as profile
import global_spacelike_flow as flow

OUT=Path(__file__).resolve().parents[1]/'output/joint_boundary_limits'


@lru_cache(maxsize=128)
def label_from_B(B):
    # For A <= -sqrt(3), the trajectory is entirely in the exact flat
    # region at t>=0, hence B(A)=A. Otherwise invert the exterior solution
    # by backward integration from a finite event well past the exit.
    if B<=-np.sqrt(3):return float(B)
    labels=[]
    for end in (20.,30.):
        initial=-end+flow.ETA*np.tanh(end)+B
        assert initial<-2
        sol=solve_ivp(lambda t,z:[float(profile.shift(z[0],0))+1+flow.epsilon(t)],
                      [end,0],[initial],method='DOP853',rtol=2e-12,atol=2e-13,max_step=.05)
        assert sol.success
        labels.append(float(sol.y[0,-1]))
    assert abs(labels[0]-labels[1])<2e-10
    return labels[-1]


def check():
    # Exact scalar identities that remove assumptions about transverse rate.
    t,x,y,R,theta,u=sp.symbols('t x y R theta u',real=True)
    labx=x+2*t
    assert sp.expand(t-labx)==-t-x
    xx=R*sp.cos(theta)-2*(R+u)
    Delta=R*(1-sp.cos(theta))
    assert sp.simplify((R+u)+xx+u+Delta)==0
    # Same conformal gauge as before, regular on ALL angular compact sets.
    r=sp.symbols('r',positive=True)
    J=sp.Matrix([u+1/r,sp.cos(theta)/r,sp.sin(theta)/r]).jacobian([u,r,theta])
    physical_flat=sp.diag(-1,1,1)
    radial=(r*r/(1+r*r)*J.T*physical_flat*J).applyfunc(sp.trigsimp)
    target=sp.Matrix([[-r*r,1,0],[1,0,0],[0,0,1]])/(1+r*r)
    assert (radial-target).applyfunc(sp.simplify)==sp.zeros(3)
    assert sp.simplify(radial.det()+1/(1+r*r)**3)==0
    assert radial.subs(r,0)==sp.Matrix([[0,1,0],[1,0,0],[0,0,1]])
    # Projective chart's actual factor, rather than silently changing gauge.
    U,Q,Y=sp.symbols('U Q Y',real=True)
    D=(1+Y*Y-U*Q)**2+4*Q*Q*Y*Y
    ratio2=4/(4*Q*Q+D) # (Omega_previous/Q)^2
    assert sp.simplify(ratio2.subs(Q,0)-4/(1+Y*Y)**2)==0
    # At scri, projective coordinates have theta=2 atan(Y), u=U/(1+Y^2).
    # The conformal metric induced on scri is exactly dtheta^2.
    assert sp.diff(2*sp.atan(Y),Y)**2==4/(1+Y*Y)**2
    # Full angular scri chart built from the corrected GLOBAL flow label.
    # du=alpha dAbar+beta dr. epsilon is flat at r=0 for bounded u.
    bp,ee=sp.symbols('Bprime epsilon',positive=True)
    alpha=-bp/(1+ee);beta=ee/(r*r*(1+ee))
    JJ=sp.Matrix([[alpha,beta,0],[0,1,0],[0,0,1]])
    corrected_metric=(JJ.T*target*JJ).applyfunc(sp.simplify)
    assert sp.simplify(corrected_metric.det()+alpha*alpha/(1+r*r)**3)==0
    # Flatness of epsilon permits its boundary substitution before r->0.
    corrected_boundary=corrected_metric.subs(ee,0).subs(r,0)
    assert corrected_boundary==sp.Matrix([[0,-bp,0],[-bp,0,0],[0,0,1]])

    mp.mp.dps=65
    ret=mp.mpf('.7')
    corrected=label_from_B(-float(ret)-flow.ETA)
    examples=[]
    for radius in (mp.mpf('100'),mp.mpf('10000'),mp.mpf('1000000')):
        angles=[('axial',mp.mpf(0)),('sqrt_R',1/mp.sqrt(radius)),
                ('twice_sqrt_R',2/mp.sqrt(radius)),
                ('R_three_quarters',radius**(-mp.mpf('.25')))]
        for name,ang in angles:
            time=radius+ret
            delta=radius*(1-mp.cos(ang))
            xx=radius*mp.cos(ang)-2*time
            yy=radius*mp.sin(ang)
            B=-ret-delta-flow.ETA*mp.tanh(time)
            A=label_from_B(float(B))
            rhs=-B-flow.ETA*mp.tanh(time)-delta
            assert abs(rhs-ret)<mp.mpf('1e-55')
            corrected_B=B+delta
            corrected_A=label_from_B(float(corrected_B))
            assert abs(corrected_A-corrected)<2e-10
            # All endpoints in this family have u=.7, theta->0, while
            # their uncorrected global labels have inequivalent limits.
            examples.append(dict(R=float(radius),family=name,theta=float(ang),
                y=float(yy),Delta=float(delta),raw_A=A,corrected_A=corrected_A,
                u=float(rhs),exact_flat_exterior=bool(xx*xx+yy*yy>9)))
    # Critical-label approaches are subject to u <= -(t+F) for every y.
    # Numerically illustrate with the fixed central orbit; the uniform
    # theorem itself follows from monotonicity and continuity, not sampling.
    critical_transverse=[]
    for time in (10.,100.,1000.):
        for name,yy in [('bounded',.3),('sqrt_t',np.sqrt(time)),
                        ('linear_t',time),('quadratic_t',time*time)]:
            radius=np.hypot(2*time,yy)
            retarded=time-radius
            assert retarded<=-time+1e-12
            critical_transverse.append(dict(t=time,scaling=name,y=float(yy),
                                              u=float(retarded),upper_bound=-time))
    # Uniform exterior domain: |u|<=M gives comoving radius >=R-2M.
    M=3.;RR=20.
    for retarded in (-M,0,M):
        time=RR+retarded
        for ang in np.linspace(-np.pi,np.pi,101):
            xx=RR*np.cos(ang)-2*time;yy=RR*np.sin(ang)
            assert np.hypot(xx,yy)>=RR-2*M-1e-12
            assert profile.shift(xx,yy)==-2
    report=dict(uniform_exclusion_proof='H=t+F has H_t=v0(F)+2+epsilon>=0; H(t,A*)->infinity. Continuity in A and monotonicity in t imply H(t_n,A_n)->infinity whenever A_n->A* and t_n->infinity. u=t-R<=-H for arbitrary y_n.',
        exact_angular_correction='u=-B(A)-eta tanh(t)-Delta; Delta=R(1-cos(theta))>=0',
        corrected_label='Abar=B^{-1}(B(A)+Delta); Abar -> B^{-1}(-u-eta)',
        corrected_label_boundary_metric='-2 Bprime(Abar) dAbar dr+dtheta^2; det=-Bprime(Abar)^2',
        corrected_label_inverse='R=1/r; solve u+eta tanh(R+u)=-B(Abar), a strictly increasing equation; t=R+u; x=R cos(theta)-2t; y=R sin(theta)',
        uniform_scri_metric='[[-r^2,1,0],[1,0,0],[0,0,1]]/(1+r^2), all theta',
        scri_determinant='-1/(1+r^2)^3',
        projective_gauge_ratio_squared='4/[4Q^2+(1+Y^2-UQ)^2+4Q^2Y^2]',
        projective_boundary_identification='theta=2 atan(Y), u=U/(1+Y^2)',
        common_scri_point=dict(u=.7,theta=0,corrected_label=corrected),
        angular_examples=examples,critical_transverse_examples=critical_transverse,
        scope='Uniform exclusion of finite scri at the critical label; full angular identification of ordinary scri and uniform regular-boundary collars. Exceptional-end topology and a global compact drawing remain unconstructed.')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('angular_examples','critical_transverse_examples')},indent=2))
    return report


def draw(report):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4.7),layout='constrained')
    colors=['#4278a3','#aa6a30','#7953a2','#348777']
    names=['axial','sqrt_R','twice_sqrt_R','R_three_quarters']
    labels=[r'$y=0$',r'$y\sim\sqrt{R}$',r'$y\sim2\sqrt{R}$',r'$y\sim R^{3/4}$']
    for name,label,color in zip(names,labels,colors):
        rows=[r for r in report['angular_examples'] if r['family']==name]
        rad=[r['R'] for r in rows]
        axes[0].plot(rad,[r['raw_A'] for r in rows],'o-',color=color,label=label)
        axes[1].plot(rad,[r['corrected_A'] for r in rows],'o-',color=color,label=label,alpha=.8)
    for ax in axes:
        ax.set_xscale('log');ax.set_xlabel('Laboratory radius R');ax.grid(alpha=.2)
    axes[0].set_yscale('symlog',linthresh=2)
    axes[0].set_ylim(-700,-1)
    axes[0].set_ylabel('Raw global flow label A')
    axes[0].set_title('Different limits at the same scri point')
    axes[0].legend(fontsize=9)
    aa=report['common_scri_point']['corrected_label']
    axes[1].set_ylim(aa-.05,aa+.05)
    axes[1].set_ylabel('Corrected label Abar')
    axes[1].set_title('Transverse correction identifies that point')
    axes[1].text(.05,.12,f'All four approaches: u = 0.7, theta -> 0\nAbar = {aa:.9f}',
                 transform=axes[1].transAxes,fontsize=10)
    fig.suptitle('Joint angular limit check — not a Penrose diagram',fontsize=14)
    fig.savefig(OUT/'angular_identification_check.png',dpi=170)
    plt.close(fig)


if __name__=='__main__':draw(check())
