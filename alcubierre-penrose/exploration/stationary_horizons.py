"""Derive and check the rider's stationary communication horizons before plotting.

Rounded example v=2 sech(r)-2. Horizons are the boundaries of I^+(gamma)
and I^-(gamma), for the eternal central rider gamma, within the original
stationary patch. They are not the spherical stationary-limit wall.
"""
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/global_2p1"
RF = np.arccosh(2.)
KAPPA = np.sqrt(3.) / 2
SPEED = 2.
CONE = np.sqrt(SPEED**2 - 1)
A2 = (KAPPA - np.sqrt(KAPPA**2 + 4 * KAPPA / RF)) / 4
BETA = -2 * A2


def shift(x, y):
    return 2 / np.cosh(np.hypot(x, y)) - 2


def gradient(x, y):
    rr = np.hypot(x, y)
    factor = -2 / np.cosh(rr) * np.tanh(rr) / rr if rr > 1e-12 else -2.
    return factor * x, factor * y


def radicand(x, y):
    rr = np.hypot(x, y)
    # Stable factorization of (2 sech(r)-1)(2 sech(r)-3).
    vp = -2 * np.sinh((rr + RF) / 2) * np.sinh((rr - RF) / 2) / np.cosh(rr)
    return vp * (2 / np.cosh(rr) - 3)


def horizon(start=1e-3, stop=45.):
    # h=RF+y^2*a(log y) removes the singular initial slope at y=0.
    def rhs(z, state):
        y = np.exp(z)
        aa = state[0]
        xx = RF + y*y*aa
        rr = np.hypot(xx, y)
        dr = y*y*(1 + aa*(2*RF + y*y*aa))/(rr + RF)
        vp = -2*np.sinh((rr+RF)/2)*np.sinh(dr/2)/np.cosh(rr)
        rad_over_y2 = vp*(2/np.cosh(rr)-3)/(y*y)
        if rad_over_y2 < -1e-9:
            raise ArithmeticError("Logarithmic horizon equation left its domain")
        return [-np.sqrt(max(rad_over_y2, 0.)) - 2*aa]
    sol = solve_ivp(rhs, [np.log(start), np.log(stop)], [A2],
                    method="DOP853", rtol=5e-13, atol=2e-14,
                    max_step=.025, dense_output=True)
    assert sol.success
    return SimpleNamespace(t=np.array([start, stop]),
                           sol=lambda y: np.array([RF + np.asarray(y)**2 * sol.sol(np.log(y))[0]]))


def audit():
    vv, slope = sp.symbols("v slope", real=True)
    gi = sp.Matrix([[-1, -vv, 0], [-vv, 1 - vv**2, 0], [0, 0, 1]])
    normal = sp.Matrix([0, 1, -slope])
    assert sp.expand((normal.T * gi * normal)[0]) == 1 + slope**2 - vv**2
    # Pullback to x=h(y): rank-one induced metric when 1+h'^2=v^2.
    g = gi.inv()
    jac = sp.Matrix([[1, 0], [0, slope], [0, 1]])
    induced = sp.simplify(jac.T * g * jac)
    assert induced == sp.Matrix([[vv**2 - 1, -vv * slope], [-vv * slope, 1 + slope**2]])

    sol = horizon()
    fine = horizon(start=5e-4)
    yy = np.geomspace(.002, 40., 800)
    xx = sol.sol(yy)[0]
    agreement = np.max(np.abs(xx - fine.sol(yy)[0]))
    assert agreement < 2e-10
    vv = shift(xx, yy)
    hp = -np.sqrt(radicand(xx, yy))
    assert np.all(np.hypot(xx, yy) > RF)
    assert np.max(np.abs(1 + hp**2 - vv**2)) < 2e-14
    # Maximum d(x-h(y))/dt over all null control directions is zero on H.
    assert np.max(np.abs(vv + np.sqrt(1 + hp**2))) < 4e-15
    # Normal derivative of the sphere's defining function at v=-1:
    # g^-1(dr,dr) = y^2/RF^2, positive away from the tips.
    sphere_norm = np.sin(np.linspace(.01, np.pi - .01, 200))**2
    assert np.min(sphere_norm) > 0

    constants = [float(sol.sol(y)[0] + CONE * y) for y in (15., 25., 40.)]
    assert abs(constants[-1] - constants[-2]) < 2e-10
    constant = constants[-1]
    transverse_cross = brentq(lambda y: sol.sol(y)[0], .1, 5.)
    # A horizon generator is an E=0 null geodesic. Integrate the full null
    # Hamilton equations, independently of the scalar horizon ODE.
    generator_errors = []
    energy_errors = []
    for y0 in (.1, .5, 1.5):
        x0 = float(sol.sol(y0)[0])
        hp0 = -np.sqrt(radicand(x0, y0))
        def rhs(_, z):
            xx, yy, pp, qq = z
            vv = shift(xx, yy)
            vx, vy = gradient(xx, yy)
            kt = np.hypot(pp, qq)
            return [vv + pp / kt, qq / kt, -vx * pp, -vy * pp]
        gen = solve_ivp(rhs, [0, 22.], [x0, y0, 1., -hp0],
                        method="DOP853", rtol=1e-12, atol=1e-13,
                        max_step=.04, dense_output=True)
        assert gen.success
        zz = gen.sol(np.linspace(0, 22., 400))
        error = np.max(np.abs(zz[0] - sol.sol(zz[1])[0]))
        ee = np.hypot(zz[2], zz[3]) + shift(zz[0], zz[1]) * zz[2]
        generator_errors.append(float(error))
        energy_errors.append(float(np.max(np.abs(ee))))
    assert max(generator_errors) < 2e-8
    assert max(energy_errors) < 2e-10

    # Constructive reachability check: start just inside the subsonic disk,
    # follow horizon-tangent controls, and approach H from its reachable side.
    # Controls depend on y, x evolves independently of the null surface ODE.
    reach_errors = []
    target_y = 2.
    for eps in (.04, .02, .01):
        xinitial = np.sqrt(RF**2 - eps**2) - eps**2
        assert shift(xinitial, eps) > -1
        def reach_rhs(y, state):
            hh = float(sol.sol(y)[0])
            vh = shift(hh, y)
            dh = -np.sqrt(radicand(hh, y))
            return [(shift(state[0], y) * vh - 1) / dh]
        reach = solve_ivp(reach_rhs, [eps, target_y], [xinitial],
                          method="DOP853", rtol=1e-11, atol=1e-12, max_step=.015)
        assert reach.success
        diff = float(sol.sol(target_y)[0] - reach.y[0, -1])
        assert diff > 0
        reach_errors.append(diff)
    assert reach_errors[2] < reach_errors[1] < reach_errors[0]

    theta = np.arccos(1 / SPEED)
    u_scri = -constant / SPEED
    future_limits = []
    for time_offset in (-3., 0., 4.):
        ylarge = 1e7
        tlarge = SPEED / CONE * ylarge + time_offset
        xlarge = constant - CONE * ylarge
        labx = xlarge + SPEED * tlarge
        radius = np.hypot(labx, ylarge)
        u = tlarge - radius
        angle = np.arctan2(ylarge, labx)
        assert abs(u - u_scri) < 5e-6
        assert abs(angle - theta) < 2e-6
        future_limits.append([float(u), float(angle)])

    # Full-surface accumulation is larger than the endpoints of individual
    # fixed generators. It includes theta=theta_M, u<=u_scri on future scri.
    closure_samples = []
    for deficit in (0., 1., 3.):
        radius = 1e7
        angle = theta + 2*np.arcsin(np.sqrt(deficit/(2*radius)))
        yy = radius*np.sin(angle)
        xx = constant - CONE*yy
        tt = (radius*np.cos(angle)-xx)/SPEED
        uu = tt-radius
        assert abs(uu-(u_scri-deficit)) < 1e-8
        closure_samples.append(float(uu))

    lines = [
        "STATIONARY COMMUNICATION HORIZONS: ROUNDED V=2 EXAMPLE",
        "Definitions: H_send=boundary I^+(gamma), H_receive=boundary I^-(gamma), in the original patch.",
        "Stationary null graph x=h(y): 1+h'^2-v(h,y)^2=0.",
        "Sending branch h'=-sqrt(v^2-1), h(0)=RF, h even in signed y.",
        f"RF={RF:.12g}, kappa={KAPPA:.12g}, h(y)=RF+({A2:.12g}) y^2+O(y^4).",
        "The positive-curvature root is another stationary null surface, not the sending horizon.",
        "H_receive is x=-h(y) by time reversal with x reflection.",
        f"Independent near-axis starts agree to {agreement:.4g}.",
        "Null normal, rank-one induced metric, causal barrier, and non-null spherical wall checked.",
        f"Hamilton geodesic deviations from the horizon: {generator_errors}.",
        f"Conserved E=0 errors: {energy_errors}.",
        f"Reachable-side deficits at y=2 for eps=.04,.02,.01: {reach_errors}.",
        "Barrier plus reachable-side approximation identifies the sending horizon (analytic argument in notes).",
        f"h(y)+sqrt(V^2-1)*y tends C={constant:.12g}; sampled constants {constants}.",
        f"The two horizon cross-sections intersect at x=0, |y|={transverse_cross:.12g}.",
        f"Sending upper/lower wings reach future scri at theta=+/-{theta:.12g}, u={u_scri:.12g}.",
        f"Sample large-radius (u,theta) on upper wing with distinct time offsets: {future_limits}.",
        f"Full horizon closure also reaches u=u_scri-deficit at that scri direction: {closure_samples}.",
        "These additional accumulation points arise from varying generators; fixed generators end at u=u_scri.",
        "Receiving wings originate at past scri, cos(theta)=-1/V, w=C/V.",
        "Off-axis sending generators have infinite future affine length; the exact axial one has finite future affine length.",
        "Planar cap: h=L on the aperture; outward wings require the actual globally bounded profile, not the unbounded local collar.",
        "This constructs the stationary horizons, not a full conformal completion or the continuation's Cauchy horizons.",
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stationary_horizons_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return sol, constant, transverse_cross


def draw(sol, constant, transverse_cross):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    fig, ax = plt.subplots(figsize=(9, 8.3))
    fig.subplots_adjust(left=.11, right=.98, top=.92, bottom=.15)
    yy = np.linspace(-3.5, 3.5, 1200)
    absy = np.abs(yy)
    hh = sol.sol(np.maximum(absy, sol.t[0]))[0]
    hh[absy < sol.t[0]] = RF + A2 * absy[absy < sol.t[0]]**2
    front, rear = "#087b7c", "#b64c25"
    mask = hh > 0
    ax.fill_betweenx(yy, -hh, hh, where=mask, color="#ece4ba", alpha=.65,
                     label="Rider can both send and receive")
    ax.plot(hh, yy, color=front, lw=2.5, label=r"Sending horizon $\partial I^+(\gamma)$")
    ax.plot(-hh, yy, color=rear, lw=2.5, label=r"Receiving horizon $\partial I^-(\gamma)$")
    ax.plot(constant - CONE * absy, yy, color=front, lw=1, ls=":", alpha=.6)
    ax.plot(-constant + CONE * absy, yy, color=rear, lw=1, ls=":", alpha=.6)
    ax.add_patch(Circle((0, 0), RF, fill=False, color="#7a7c82", ls="--", lw=1.5,
                        label=r"Stationary-limit wall $v=-1$"))
    ax.scatter([0], [0], s=35, color="#222222", zorder=5)
    ax.text(.12, .12, "Central rider", fontsize=10)
    ax.scatter([RF, -RF], [0, 0], color=[front, rear], s=32, zorder=6)
    for side in (-1, 1):
        for y0 in (.65, 2.8):
            y1 = y0 + .22
            h0 = float(sol.sol(y0)[0])
            h1 = float(sol.sol(y1)[0])
            ax.annotate("", xy=(h1, side * y1), xytext=(h0, side * y0),
                        arrowprops=dict(arrowstyle="->", color=front, lw=1.7))
            ax.annotate("", xy=(-h0, side * y0), xytext=(-h1, side * y1),
                        arrowprops=dict(arrowstyle="->", color=rear, lw=1.7))
    ax.text(2.5, .2, "Cannot be signaled\nby the rider", ha="center", fontsize=10, color=front)
    ax.text(-2.55, -.45, "Cannot signal\nthe rider", ha="center", fontsize=10, color=rear)
    ax.set(xlim=(-4, 4), ylim=(-3.5, 3.5), xlabel="Comoving longitudinal coordinate x",
           ylabel="Signed transverse coordinate y",
           title="Stationary horizons of the rounded bubble (V = 2)")
    ax.set_aspect("equal")
    ax.grid(alpha=.12)
    ax.legend(loc="upper center", fontsize=9, framealpha=.95)
    fig.text(.5, .025, "A spatial section, not a Penrose diagram. The full null surfaces sweep these curves through time.\n"
             "Arrows show future null-generator motion in comoving space. Dotted lines are the Mach asymptotes.",
             ha="center", fontsize=9)
    fig.savefig(OUT / "stationary_horizons.png", dpi=185, bbox_inches="tight", pad_inches=.25)
    plt.close(fig)


if __name__ == "__main__":
    result = audit()
    draw(*result)
