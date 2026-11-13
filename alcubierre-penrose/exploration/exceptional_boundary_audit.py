"""Check rim formulas and the two-limit obstruction at ordinary scri.

Analytic arguments are in notes/joint_boundary_limits.md, sections 11--15.
The plot is a boundary-incidence diagnostic, not a conformal embedding.
"""
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.integrate import quad
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import capped_horizon_atlas as cap

OUT = Path(__file__).resolve().parents[1] / 'output/exceptional_boundary_audit'


def main():
    q, lam, psi = sp.symbols('q lambda psi', real=True)
    v = -(1+(1+q*lam)**2+psi)/2
    # Columns are d/dlambda, d/dq, d/dy in physical t,x,y coordinates.
    jac = sp.Matrix([[0, -1/q, 0], [q, lam, 0], [0, 0, 1]])
    metric = sp.Matrix([[v*v-1, -v, 0], [-v, 1, 0], [0, 0, 1]])
    pulled = sp.simplify(jac.T*metric*jac)
    qq = (lam**2*(1+psi/2) + q*q*lam**4/4 + (psi+psi**2/4)/q**2)
    assert sp.simplify(pulled[1, 1]-qq) == 0
    assert sp.simplify(pulled.det()+1) == 0
    zeta = sp.symbols('zeta', nonnegative=True)
    assert sp.limit(qq.subs(psi, zeta*q*q), q, 0) == lam**2+zeta

    # An upper right Riemann sum, using monotonicity of psi and -W.
    # |h|<=1 on [a,YE] follows first from |h'|<=sqrt(3).
    assert 1-cap.CONE*(cap.Y_EXTERIOR-cap.APERTURE) > -1
    edges = np.linspace(cap.APERTURE, cap.Y_EXTERIOR, 20001)
    integrand = np.sqrt(np.maximum(cap.W(cap.psi(edges))**2-1, 0))
    assert np.min(np.diff(integrand)) > -1e-13
    lower_h = 1-float(np.sum(np.diff(edges)*integrand[1:]))
    assert lower_h > .26
    horizon = cap.build_horizon()
    assert float(horizon.h(cap.Y_EXTERIOR)) > lower_h

    theta_m = np.pi/3
    um = -horizon.C/2
    u0 = um-1
    # Timelike departure with u_x=-1/2, u_y=0, from x=0 to x=-3.
    departure_duration = quad(lambda x: 1/(.5-float(cap.shift(x, 0))),
                              -3, 0, epsabs=1e-11)[0]
    rows = []
    for angle_gap in (.2, .1, .05, .02, .01, .005, .001):
        theta = theta_m-angle_gap
        nx = np.cos(theta)
        departure_time = (3*nx-u0+1)/(2*nx-1)-departure_duration
        exit_time = departure_time+departure_duration
        exit_retarded = (1-2*nx)*exit_time+3*nx
        assert abs(exit_retarded-(u0-1)) < 1e-11
        rows.append(dict(angle_gap=angle_gap, theta=theta,
                         rider_departure_time=departure_time,
                         flat_exit_retarded_time=exit_retarded))
    assert all(b['rider_departure_time'] > a['rider_departure_time']
               for a, b in zip(rows, rows[1:]))

    # Witness in I^-(Q) but outside the rider's receiving region.
    witness_x, witness_y = -3., 10.
    witness_retarded = -witness_x/2-np.sqrt(3)*witness_y/2
    witness_receiving_function = witness_x+float(horizon.h(witness_y))
    assert witness_retarded < u0 and witness_receiving_function < 0
    # At the Mach angle, late points with retarded time u0 are outside I+(gamma).
    sending_gap_at_Q = -2*u0-horizon.C
    assert sending_gap_at_Q > 0

    rim_rows = []
    for lam0 in (-2., 0., 2.):
        slope = lam0**2/2+2
        # Curve lambda(q)=lambda0+slope*q on y=a has a timelike limiting tangent.
        limit_norm = lam0**2-2*slope
        assert limit_norm < 0
        rim_rows.append(dict(cap_lambda=lam0, lambda_slope=slope,
                             limiting_curve_norm=limit_norm))

    report = dict(scope='Checks of proofs, not a global compactification',
                  metric_determinant=str(sp.factor(pulled.det())),
                  rim_path_dependent_qq_limit='lambda^2+zeta when psi=zeta*q^2',
                  analytic_riemann_lower_bound_for_h_at_YE=lower_h,
                  measured_h_at_YE=float(horizon.h(cap.Y_EXTERIOR)),
                  theta_M=theta_m, u_M=um, chosen_scri_u=u0,
                  departure_duration=departure_duration,
                  forward_angle_sequence=rows,
                  non_rider_witness=dict(x=witness_x,y=witness_y,
                      retarded_value=witness_retarded,
                      receiving_function=witness_receiving_function),
                  sending_gap_at_limiting_Q=sending_gap_at_Q,
                  canonical_rim_timelike_curves=rim_rows,
                  conclusion='The standard chronological c-boundary has distinct simultaneous limits P_r+ and Q; a Hausdorff faithful embedding is impossible.')
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    draw(theta_m, um, u0)
    print(json.dumps(dict(checks='passed',h_lower_bound=lower_h,u_M=um,
                         witness_retarded_value=witness_retarded,
                         maximum_departure_time=rows[-1]['rider_departure_time'],
                         output=str(OUT)),indent=2))


def draw(theta_m, um, u0):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), constrained_layout=True)
    fig.suptitle('Verified boundary relations — not a global conformal embedding',fontsize=14)
    ax=axes[0]
    ax.fill_between([-1.2,1.2],-.6,.6,color='#e1f0ed')
    for yy in (-.6,.6):
        ax.plot([-1.2,1.2],[yy,yy],color='#af413f',lw=2.5)
    ax.text(0,0,'Regular front-cap face\nfinite $\\lambda$, $|y|<a$',ha='center',va='center')
    ax.text(0,.68,'rim curve: $y=+a$',ha='center',color='#af413f')
    ax.text(0,-.76,'rim curve: $y=-a$',ha='center',color='#af413f')
    ax.annotate('',(-2.0,0),(-1.25,0),arrowprops=dict(arrowstyle='->',color='#117d80',lw=2))
    ax.plot(-2.05,0,'o',color='#117d80')
    ax.text(-2.05,-.3,'$P_r^+$\none causal point',ha='center',color='#117d80')
    ax.text(-1.65,.22,'$\\lambda\\to-\\infty$',ha='center',fontsize=10)
    ax.annotate('',(2.05,0),(1.25,0),arrowprops=dict(arrowstyle='->',color='#6d647d',lw=2))
    ax.text(1.7,.22,'$\\lambda\\to+\\infty$',ha='center',fontsize=10)
    ax.text(1.85,-.3,'No limit in the\nfuture c-boundary',ha='center',color='#6d647d')
    ax.set(xlim=(-2.7,2.7),ylim=(-1.2,1.25),title='Cap labels and their ends')
    ax.axis('off')
    ax=axes[1]
    ax.axvspan(theta_m-.45,theta_m,alpha=.13,color='#117d80')
    ax.axvline(theta_m,color='#999999',lw=1)
    ax.plot([theta_m,theta_m],[um-1.8,um],color='#af413f',lw=3)
    gaps=np.array([.32,.2,.12,.07,.035,.012])
    ax.plot(theta_m-gaps,np.full_like(gaps,u0),'o',ms=5,color='#147b89')
    ax.annotate('',(theta_m-.005,u0),(theta_m-.32,u0),arrowprops=dict(arrowstyle='->',lw=1.5))
    ax.plot(theta_m,u0,'o',color='#af413f',ms=7)
    ax.text(theta_m+.025,u0,'$Q$',va='center',color='#af413f')
    ax.plot(theta_m-.28,um-1.65,'o',color='#117d80',ms=7)
    ax.text(theta_m-.25,um-1.65,'$P_r^+$ (separate ideal point)',va='center',fontsize=9)
    ax.annotate('',(theta_m-.28,um-1.6),(theta_m-.04,u0-.08),
                arrowprops=dict(arrowstyle='->',lw=1.5,connectionstyle='arc3,rad=-.3',color='#117d80'))
    ax.text(theta_m-.35,um-.4,'Every $Q_n$ receives arbitrarily\nlate rider signals',fontsize=9,color='#117d80')
    ax.text(theta_m+.025,um+.09,'$u_M$',fontsize=10)
    ax.set(xlim=(theta_m-.45,theta_m+.37),ylim=(um-1.9,um+.5),
           xlabel='Angle on ordinary future null infinity',ylabel='Retarded time $u$',
           title='One sequence, two chronological limits')
    ax.set_xticks([theta_m-.3,theta_m,theta_m+.3],['forward side','$\\theta_M$','other side'])
    ax.text(.02,.02,'The rider symbol has no (angle, u) coordinates; it marks the second limit.',
            transform=ax.transAxes,fontsize=8)
    fig.savefig(OUT/'boundary_incidence.png',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    main()
