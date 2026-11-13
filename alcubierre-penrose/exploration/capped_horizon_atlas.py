"""Globally bounded capped profile and independently checked horizon wings.

The plotting stage is separate from the audit: no compactified boundary is
identified from appearances in a bounded coordinate box.
"""
from pathlib import Path
from types import SimpleNamespace
import json
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import expi, expit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/global_2p1"
L, APERTURE, D, SPEED = 1., .6, .2, 2.
CONE = np.sqrt(SPEED**2-1)


def step(z):
    z = np.asarray(z, dtype=float)
    safe = np.clip(z, 1e-15, 1-1e-15)
    value = expit(-1/safe+1/(1-safe))
    return np.where(z <= 0, 0., np.where(z >= 1, 1., value))


def stepprime(z):
    z = np.asarray(z, dtype=float)
    safe = np.clip(z, 1e-15, 1-1e-15)
    ss = step(safe)
    ans = ss*(1-ss)*(1/safe**2+1/(1-safe)**2)
    return np.where((z > 0) & (z < 1), ans, 0.)


def eta(z):
    z = np.asarray(z, dtype=float)
    safe = np.maximum(z, 1e-15)
    return np.where(z > 0, safe*np.exp(-1/safe)+expi(-1/safe), 0.)


NORM = float(eta((1-APERTURE**2)/D))


def psi(y):
    return eta((np.asarray(y)**2-APERTURE**2)/D)/NORM


def psiprime(y):
    y = np.asarray(y, dtype=float)
    z = (y*y-APERTURE**2)/D
    return np.where(z > 0, np.exp(-1/np.maximum(z, 1e-15))*2*y/D/NORM, 0.)


def W(phi):
    phi = np.asarray(phi, dtype=float)
    inside = -(1+phi/2)*step((phi+.75)/.5)
    outside = -2+(1-phi/2)*(1-step((phi-.25)/1.75))
    return np.where(phi < -.25, inside, np.where(phi > .25, outside, -1-phi/2))


def Wprime(phi):
    phi = np.asarray(phi, dtype=float)
    inside = -.5*step((phi+.75)/.5)-(1+phi/2)*stepprime((phi+.75)/.5)/.5
    outside = -.5*(1-step((phi-.25)/1.75))-(1-phi/2)*stepprime((phi-.25)/1.75)/1.75
    return np.where(phi < -.25, inside, np.where(phi > .25, outside, -.5))


def shift(x, y):
    return W(np.asarray(x)**2+psi(y)-1)


def gradient(x, y):
    ww = Wprime(x*x+psi(y)-1)
    return 2*x*ww, psiprime(y)*ww


Y_EXTERIOR = brentq(lambda y: psi(y)-3, 1., 2.)


def build_horizon(start=.61, switch=.67):
    # Near the infinitely flat rim, solve for k=-h' instead of subtracting
    # almost equal h and wall positions. W is exactly affine here.
    def recover(y, k):
        phi = 2*k*k/(np.hypot(1, k)+1)
        return np.sqrt(1-psi(y)+phi)
    kinitial = psiprime(start)/(2*np.sqrt(1-psi(start)))
    def slope_rhs(y, z):
        kk = z[0]
        hh = recover(y, kk)
        return [np.hypot(1, kk)*(psiprime(y)/(2*kk)-hh)]
    near = solve_ivp(slope_rhs, [start, switch], [kinitial], method="Radau",
                     rtol=2e-11, atol=2e-15, max_step=.001, dense_output=True)
    assert near.success and np.min(near.y[0]) > 0
    hswitch = recover(switch, near.y[0, -1])
    assert hswitch*hswitch+psi(switch)-1 < .25
    def rhs(y, z):
        vv = shift(z[0], y)
        rad = (vv+1)*(vv-1)
        return [-np.sqrt(max(rad, 0.))]
    outer = solve_ivp(rhs, [switch, Y_EXTERIOR+.1], [hswitch],
                      method="DOP853", rtol=2e-12, atol=2e-13,
                      max_step=.004, dense_output=True)
    assert outer.success
    cvalue = float(outer.sol(Y_EXTERIOR)[0]+CONE*Y_EXTERIOR)
    def hh(y):
        arr = np.asarray(y, dtype=float)
        absy = np.abs(arr).reshape(-1)
        # Below the numeric near-rim start, use the asymptotic wall track.
        # This is NOT advertised as a resolved numerical horizon there.
        small = np.sqrt(np.maximum(1-psi(np.minimum(absy, start)), 0.))
        nk = near.sol(np.clip(absy, start, switch))[0]
        nh = recover(np.clip(absy, start, switch), nk)
        oh = outer.sol(np.clip(absy, switch, Y_EXTERIOR))[0]
        result = np.where(absy <= APERTURE, L,
               np.where(absy < start, small,
               np.where(absy < switch, nh,
               np.where(absy < Y_EXTERIOR, oh, cvalue-CONE*absy))))
        return result.reshape(arr.shape)
    return SimpleNamespace(h=hh, near=near, outer=outer, C=cvalue,
                           start=start, switch=switch, recover=recover)


def audit():
    phis = np.linspace(-2, 4, 2001)
    assert np.max(Wprime(phis)) <= 1e-14
    assert np.min(W(phis)) >= -2 and np.max(W(phis)) <= 0
    assert W(-1) == 0 and W(0) == -1 and W(2) == -2
    assert Wprime(0) == -.5
    assert abs(psi(1)-1) < 1e-14 and psi(APERTURE) == 0
    assert abs(shift(L, 0)+1) < 1e-14 and gradient(L, 0)[0] == -1
    h = build_horizon()
    other = build_horizon(start=.615, switch=.68)
    ys = np.linspace(.69, 3, 500)
    discrepancy = float(np.max(np.abs(h.h(ys)-other.h(ys))))
    assert discrepancy < 1e-9
    assert np.all(h.h(np.linspace(0, APERTURE, 20)) == L)
    ys = np.linspace(h.start, Y_EXTERIOR, 600)
    xs = h.h(ys)
    v = shift(xs, ys)
    assert np.max(v+1) < 0
    slopes = -np.sqrt((v+1)*(v-1))
    assert np.max(np.abs(1+slopes**2-v**2)) < 2e-15
    # Near-rim ODE also implies h'=-k; check this independently by finite differences.
    errs = []
    for y in (.625, .64, .66):
        kk = float(h.near.sol(y)[0])
        eps = 1e-6
        diff = (h.h(y+eps)-h.h(y-eps))/(2*eps)
        errs.append(float(abs(diff+kk)))
    assert max(errs) < 2e-8
    assert abs(h.C-other.C) < 1e-9
    # Below the numerical start, the true h is bracketed by the stationary
    # wall and wall+Kwall^2/(2*wall), Kwall=psi'/(2*wall).
    wallstart = np.sqrt(1-psi(h.start))
    near_rim_bound = float((psiprime(h.start)/(2*wallstart))**2/(2*wallstart))
    assert near_rim_bound < 1e-14
    assert abs(h.outer.sol(Y_EXTERIOR+.05)[0]+CONE*(Y_EXTERIOR+.05)-h.C) < 1e-10
    # Full Hamilton geodesics, not constrained to the horizon graph.
    null_errors, energy_errors = [], []
    for y0 in (.64, .75, 1.05):
        x0 = float(h.h(y0))
        slope = -np.sqrt(shift(x0, y0)**2-1)
        def geodesic_rhs(t, z):
            x, y, p, q = z
            vv = shift(x, y)
            vx, vy = gradient(x, y)
            kt = np.hypot(p, q)
            return [vv+p/kt, q/kt, -vx*p, -vy*p]
        sol = solve_ivp(geodesic_rhs, [0, 8.], [x0, y0, 1., -slope],
                        method="DOP853", rtol=2e-12, atol=1e-13,
                        max_step=.01, dense_output=True)
        assert sol.success
        z = sol.sol(np.linspace(0, 8., 600))
        null_errors.append(float(np.max(np.abs(z[0]-h.h(z[1])))))
        energy_errors.append(float(np.max(np.abs(np.hypot(z[2], z[3])+shift(z[0], z[1])*z[2]))))
    assert max(null_errors) < 2e-8 and max(energy_errors) < 2e-9
    # Exterior horizon is exactly a Minkowski null plane on each wing.
    # In s=1/R,u=t-R,theta: s*(u-u_M)+1-cos(theta-theta_M)=0.
    thetaM = np.arccos(1/SPEED)
    uM = -h.C/SPEED
    for rr in (100., 1e4, 1e6):
        for deficit in (.1, 1., 3.):
            theta = thetaM+2*np.arcsin(np.sqrt(deficit/(2*rr)))
            y = rr*np.sin(theta)
            x = h.h(y)
            t = (rr*np.cos(theta)-x)/SPEED
            u = t-rr
            assert abs(u-(uM-deficit)) < 2e-9
            assert abs((u-uM)/rr+1-np.cos(theta-thetaM)) < 1e-14
    # The cap chart is the already verified local metric, but now check that
    # the entire displayed geodesic lies in THIS global W's affine region.
    sys.path.insert(0, str(ROOT/"paper/supplement/scripts"))
    from meridional_geometry import FrontCollar
    collar = FrontCollar("cap")
    crossing, crossing_tau = collar.geodesic()
    z = crossing.sol(np.linspace(0, crossing.t[-1], 300))
    cvalues = []
    normalizations = []
    phivals = []
    for pp, qq, dp, dq in z.T:
        x = collar.x_from_product(pp*qq)
        phivals.append(x*x-1)
        cval = collar.C(x)
        cvalues.append(cval)
        normalizations.append(cval*dp*dq)
        assert abs(shift(x, .3)-collar.v0(x)) < 1e-13
    assert max(np.abs(np.array(phivals))) < .25
    assert max(np.abs(np.array(normalizations)+1)) < 1e-9
    assert min(cvalues) > 0
    summary = dict(L=L, aperture=APERTURE, speed=SPEED,
                   exterior_transverse_threshold=Y_EXTERIOR,
                   intercept_C=h.C, theta_M=thetaM, u_M=uM,
                   wing_start_convergence=discrepancy,
                   unresolved_rim_wall_track_bound=near_rim_bound,
                   near_rim_derivative_errors=errs,
                   hamilton_surface_errors=null_errors,
                   hamilton_energy_errors=energy_errors,
                   crossing_phi_range=[min(phivals),max(phivals)],
                   crossing_unit_norm_error=float(max(np.abs(np.array(normalizations)+1))),
                   crossing_proper_time=float(crossing_tau))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"capped_horizon_check.json").write_text(json.dumps(summary, indent=2)+"\n")
    print(json.dumps(summary, indent=2))
    return h, summary


def draw(h, summary):
    """A horizon atlas, explicitly not a single completed Penrose diamond."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    teal, orange, blue, purple, red = "#087d80", "#bd542c", "#3c75b4", "#7751a0", "#ad2543"
    fig = plt.figure(figsize=(16, 12))
    fig.subplots_adjust(left=.055, right=.98, top=.925, bottom=.19, wspace=.13, hspace=.32)
    fig.suptitle("Capped Alcubierre bubble: checked global horizon atlas", fontsize=20)

    # (a) The complete spatial cross-sections specify the stationary surfaces.
    ax = fig.add_subplot(221)
    yy = np.linspace(-2.3,2.3,1200)
    hh = h.h(yy)
    ax.plot(hh, yy, color=teal, lw=2.4, label="Sending horizon")
    ax.plot(-hh, yy, color=orange, lw=2.4, label="Receiving horizon")
    capyy = np.linspace(-APERTURE, APERTURE, 100)
    ax.plot(np.full_like(capyy, L), capyy, color=teal, lw=5)
    ax.plot(np.full_like(capyy, -L), capyy, color=orange, lw=5)
    wall_y = np.linspace(-1, 1, 600)
    wall_x = np.sqrt(np.maximum(1-psi(wall_y),0))
    ax.plot(wall_x, wall_y, color=".5", ls="--", lw=1.1)
    ax.plot(-wall_x, wall_y, color=".5", ls="--", lw=1.1, label="Stationary-limit wall")
    ax.fill_betweenx(yy,-hh,hh,where=hh>0,color="#e8dfb1",alpha=.5)
    ax.scatter([0],[0],c="black",s=22)
    ax.scatter([L,L,-L,-L],[APERTURE,-APERTURE,APERTURE,-APERTURE],c=red,s=20,zorder=5)
    ax.text(1.12,0,"Planar\ncap",color=teal,fontsize=10,va="center")
    ax.set(xlim=(-3,3),ylim=(-2.3,2.3),xlabel="Comoving x",ylabel="Signed transverse y",
           title="(a) Entire stationary horizons: these curves × time")
    ax.set_aspect("equal",adjustable="box")
    ax.grid(alpha=.12)
    ax.legend(loc="upper center",ncol=3,fontsize=8,framealpha=.9)

    # (b) Genuine exterior Penrose chart, where the global metric is exactly flat.
    ax = fig.add_subplot(222, projection="3d")
    theta = np.linspace(0,2*np.pi,130)
    for sign in (-1,1):
        for tt in np.linspace(.15,np.pi-.12,9):
            chi = np.pi-tt
            ax.plot(chi*np.cos(theta),chi*np.sin(theta),np.full_like(theta,sign*tt),
                    color=blue,alpha=.15,lw=.6)
        for ang in np.linspace(0,2*np.pi,13):
            tt = np.linspace(.05,np.pi,120)
            chi = np.pi-tt
            ax.plot(chi*np.cos(ang),chi*np.sin(ang),sign*tt,color=blue,alpha=.15,lw=.6)
    ax.plot(np.pi*np.cos(theta),np.pi*np.sin(theta),np.zeros_like(theta),
            color=".4",ls="--",lw=1)
    uM, thetaM = summary["u_M"],summary["theta_M"]
    # A null-plane wing in the exterior: U=atan(u), angle theta. Its two
    # branches touch scri at theta_M for every u<=u_M.
    U = np.linspace(-np.pi/2+.018,np.arctan(uM)-1e-5,100)
    uu = np.tan(U)
    minimum_y = 2.5
    deficit = (uM-uu)/minimum_y
    center = CONE/SPEED+deficit
    root = np.sqrt(deficit**2+2*deficit*CONE/SPEED)
    lowz = (1-1/SPEED)/(center+root)
    highz = (center+root)/(1+1/SPEED)
    thlo, thhi = 2*np.arctan(lowz),2*np.arctan(highz)
    zeta = np.linspace(-1,1,91)
    ang = np.where(zeta[None,:]<0,
                   thetaM+(thetaM-thlo[:,None])*zeta[None,:],
                   thetaM+(thhi[:,None]-thetaM)*zeta[None,:])
    den = 2*np.sin((ang-thetaM)/2)**2
    # At den=0 this is the analytically checked scri limit, not a finite point.
    radius = np.divide((uM-uu)[:,None],den,out=np.full_like(den,np.inf),where=den>1e-26)
    w = uM+radius*(1+np.cos(ang-thetaM))
    TT = U[:,None]+np.arctan(w)
    chi = np.arctan(w)-U[:,None]
    xc, yc = chi*np.cos(ang),chi*np.sin(ang)
    for reflection in (-1,1):
        ax.plot_surface(xc,reflection*yc,TT,color=teal,alpha=.30,linewidth=0,
                        rstride=3,cstride=3,shade=False)
        ax.plot_surface(-xc,reflection*yc,-TT,color=orange,alpha=.24,linewidth=0,
                        rstride=3,cstride=3,shade=False)
        ub = np.linspace(-50,uM,200)
        Tb = np.pi/2+np.arctan(ub)
        cb = np.pi-Tb
        ax.plot(cb*np.cos(thetaM),reflection*cb*np.sin(thetaM),Tb,color=teal,lw=2.5)
        ax.plot(-cb*np.cos(thetaM),reflection*cb*np.sin(thetaM),-Tb,color=orange,lw=2.5)
        tm = np.pi/2+np.arctan(uM)
        cm = np.pi-tm
        ax.scatter([cm*np.cos(thetaM)],[reflection*cm*np.sin(thetaM)],[tm],color=teal,s=26)
        ax.scatter([-cm*np.cos(thetaM)],[reflection*cm*np.sin(thetaM)],[-tm],color=orange,s=26)
    ax.text(1.25,0,1.8,r"$\mathcal{I}^+$",color=blue,fontsize=13)
    ax.text(1.25,0,-1.8,r"$\mathcal{I}^-$",color=blue,fontsize=13)
    ax.text(0,0,3.05,r"$i^+_{ext}$",color=".25",fontsize=10)
    ax.text(0,0,-3.2,r"$i^-_{ext}$",color=".25",fontsize=10)
    ax.set(xlim=(-3.2,3.2),ylim=(-3.2,3.2),zlim=(-3.2,3.2),
           title="(b) Exterior conformal chart: horizon wings meet null infinity")
    ax.view_init(elev=18,azim=-65)
    ax.set_box_aspect((1,1,1),zoom=1.25)
    ax.set_axis_off()
    ax.text2D(.02,.02,"Bold: surface closure on scri; dots: fixed-generator endpoints.\n"
              "Dashed base: spatial corner omitted; cap ends are not identified there.",
              transform=ax.transAxes,fontsize=8)

    # (c) Full finite-time inner horizons in a future temporal chart. No
    # constant-time coordinate cut is declared a physical conformal boundary.
    ax = fig.add_subplot(223,projection="3d")
    y = np.linspace(-3,3,200)
    tau = np.linspace(-.96,.96,55)
    yy, zz = np.meshgrid(y,tau)
    xx = h.h(yy)
    ax.plot_surface(xx,yy,zz,color=teal,alpha=.33,linewidth=0,shade=False)
    ax.plot_surface(-xx,yy,zz,color=orange,alpha=.29,linewidth=0,shade=False)
    for xpos,sgn,col in ((1,1,teal),(-1,-1,orange)):
        ax.plot(np.full_like(capyy,xpos),capyy,np.full_like(capyy,sgn),color=col,lw=4)
        ax.scatter([xpos,xpos],[APERTURE,-APERTURE],[sgn,sgn],color=red,s=17)
    ax.plot([0,0],[0,0],[-.98,.98],color="black",lw=1.3)
    ax.scatter([0,0],[0,0],[-1,1],facecolors="white",edgecolors="black",s=24)
    ax.text(1.2,0,1.08,"Cap generator ends → (d)",color=teal,fontsize=8)
    ax.set(xlim=(-3,3),ylim=(-3,3),zlim=(-1.12,1.15),xlabel="x",ylabel="y",
           zlabel=r"$\tau=(2/\pi)\arctan t$",title="(c) Inner horizon chart, joined to (b) in the flat exterior")
    ax.view_init(elev=21,azim=-62)
    ax.set_box_aspect((1,1,.8))
    fig.text(.10,.115,"Time is future-increasing. Mesh edges are chart cuts.\n"
             "Front cap: finite future affine length; rear cap: time reverse.",fontsize=9)

    # (d) Actual regular cap crossing metric C(dp dq)+dy^2, not an extrusion
    # of a Minkowski conformal diamond. Longitudinal X,T are defined explicitly.
    ax = fig.add_subplot(224,projection="3d")
    ycap = np.linspace(-APERTURE+.002,APERTURE-.002,40)
    p = np.linspace(-.72,.72,50)
    pp,yy = np.meshgrid(p,ycap)
    ax.plot_surface(pp/2,yy,pp/2,color=purple,alpha=.25,linewidth=0,shade=False)
    q = np.linspace(-.14,.14,35)
    qq,yy = np.meshgrid(q,ycap)
    ax.plot_surface(qq/2,yy,-qq/2,color=teal,alpha=.42,linewidth=0,shade=False)
    ax.plot(np.zeros_like(ycap),ycap,np.zeros_like(ycap),color=teal,lw=3)
    ax.scatter([0,0],[-APERTURE,APERTURE],[0,0],color=red,s=27)
    from meridional_geometry import FrontCollar
    collar = FrontCollar("cap")
    sol,tcross = collar.geodesic()
    traj = sol.sol(np.linspace(0,sol.t[-1],200))
    ax.plot((traj[0]+traj[1])/2,np.full(200,.3),(traj[0]-traj[1])/2,color="#242424",lw=2.2)
    z = sol.sol(tcross)
    ax.scatter([(z[0]+z[1])/2],[.3],[(z[0]-z[1])/2],color="#242424",s=25)
    ax.text(.27,-.5,.31,"q = 0: regular crossing",color=purple,fontsize=8)
    ax.text(-.06,.1,-.13,"p = 0: sending horizon",color=teal,fontsize=8)
    ax.set(xlabel="X = (p + q)/2",ylabel="y",zlabel="T = (p − q)/2",
           xlim=(-.4,.45),ylim=(-.7,.7),zlim=(-.4,.5),
           title="(d) Cap chart: crossing surface and continued horizon")
    ax.view_init(elev=20,azim=-62)
    ax.set_box_aspect((1,1.2,1))
    fig.text(.58,.115,r"$g=C(pq)(dX^2-dT^2)+dy^2$, C > 0; black: unit timelike geodesic."
             "\nOpen aperture |y| < 0.6; rim excluded. Rear chart is time reversed.",fontsize=9)

    fig.text(.5,.025,"A conformal atlas of the global horizon geometry, not a completed single Penrose diagram. "
             "Finite cap crossings and ordinary null infinity use different boundary charts.\n"
             "The exterior cone is a directional display; the bubble's infinite-time ends are not identified with its dashed base.\n"
             "Signed meridional double: fold y and -y together for the angular quotient of the four-dimensional spacetime.",
             ha="center",fontsize=10)
    fig.savefig(OUT/"capped_global_horizon_atlas.png",dpi=180,bbox_inches="tight",pad_inches=.22)
    plt.close(fig)


if __name__ == "__main__":
    h, summary = audit()
    draw(h, summary)
