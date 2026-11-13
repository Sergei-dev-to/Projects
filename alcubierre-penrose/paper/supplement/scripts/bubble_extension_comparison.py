"""One checked three-panel figure: shared axial metric, different 4D outcomes.

Panel (a) is a 1+1 conformal diagram of the future and past cap attachments,
each continued across both axial horizons on a disk inside the cap.
Panels (b,c) are finite-time Euclidean spatial wall sections, NOT spacetime
diagrams. The comparison uses an explicit smooth global W with an affine
collar, matching FrontCollar('cap') and its regular null coordinates.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.integrate import solve_ivp

from meridional_geometry import FrontCollar

BASE = Path(__file__).resolve().parent
FIGURES = BASE.parent.parent / "figures"
BLUE = "#37789c"
PALE_BLUE = "#e6eff5"
GREEN = "#167965"
FLAT_FILL = "#e2f2ed"
WALL_FILL = "#d7bea4"
FLAT_EDGE = "#578e85"
RED = "#982f2a"
PURPLE = "#714780"
ORANGE = "#914c10"
GRAY = "#50565c"
B = np.pi / 2
AF = -np.pi / 6
LABEL_SIZE = 16
TITLE_SIZE = 18
HORIZON_STYLE = (0, (3, 3))
CENTER_STYLE = (0, (4, 2, 1, 2))
BACKWARD_STYLE = (0, (7, 2.5))
FLAT_CORE_PHI = -.98
FLAT_EXTERIOR_PHI = 1.8


def smooth_step(z):
    z = np.asarray(z, dtype=float)
    zz = np.clip(z, 1e-10, 1 - 1e-10)
    left, right = np.exp(-1/zz), np.exp(-1/(1-zz))
    result = left / (left + right)
    return np.where(z <= 0, 0., np.where(z >= 1, 1., result))


def W(phi):
    """Smooth nonincreasing W: flat core, affine collar, constant exterior."""
    phi = np.asarray(phi)
    affine = -1 - phi/2
    inside = smooth_step((phi-FLAT_CORE_PHI)/(-.9-FLAT_CORE_PHI)) * affine
    exterior_weight = smooth_step((phi-.9)/(FLAT_EXTERIOR_PHI-.9))
    outside = (1-exterior_weight)*affine - 2*exterior_weight
    return np.where(phi < -.9, inside, np.where(phi > .9, outside, affine))


def xy(aa, bb):
    aa, bb = np.asarray(aa), np.asarray(bb)
    return (bb-aa)/2, (bb+aa)/2


def front_xy(p, q, scales=(1., 1.)):
    p_center, q_center = scales
    return xy(AF+(2/3)*np.arctan(np.asarray(p)/p_center),
              B-2*np.arctan(np.asarray(q)/q_center))


def rectangle(aa0, aa1, bb0, bb1):
    return np.column_stack(xy([aa0, aa1, aa1, aa0], [bb0, bb0, bb1, bb1]))


def axial_flat_boundaries(cap, scales):
    """Map the four constant-x edges of the flat regions to (A, B)."""
    core_edge = np.sqrt(1+FLAT_CORE_PHI)
    exterior_edge = np.sqrt(1+FLAT_EXTERIOR_PHI)

    def log_product_rate(x):
        return 2*cap.kappa/(float(W(x*x-1))**2-1)

    core_product = np.exp(quad(log_product_rate, 0., core_edge)[0])
    x_match = 1.25
    exterior_product = (cap.F(x_match)*np.exp(quad(log_product_rate, x_match, exterior_edge)[0])
                        / np.prod(scales))
    bb = np.linspace(-B, B, 601)
    q_ratio = np.tan((B-bb[1:-1])/2)
    front_exterior = np.r_[AF, AF+(2/3)*np.arctan(exterior_product/q_ratio), -B]
    front_core = np.r_[AF, AF+(2/3)*np.arctan(core_product/q_ratio), -AF]
    boundaries = np.array([front_exterior, front_core, -front_core[::-1], -front_exterior[::-1]])
    assert 0 < core_product < 1 and exterior_product < 0
    assert np.all(np.diff(boundaries[:, 1:-1], axis=0) > 0)
    assert np.all(front_exterior[1:-1] < AF) and np.all(front_core[1:-1] > AF)
    assert np.all(W(np.array([0., core_edge/2])**2-1) == 0)
    assert W((exterior_edge+.1)**2-1) == -2
    return bb, boundaries


def shade_axial_diamond(ax, bb, boundaries, offset=(0., 0.), direction=1):
    """Copy the same metric coloring to an attached axial diamond."""
    edges = np.vstack([np.full_like(bb, -B), boundaries, np.full_like(bb, B)])
    for left, right, color in zip(edges, edges[1:],
                                  (FLAT_FILL, WALL_FILL, FLAT_FILL, WALL_FILL, FLAT_FILL)):
        aa = np.r_[left, right[::-1]]
        bb_polygon = np.r_[bb, bb[::-1]]
        polygon = np.column_stack(xy(*(np.asarray(offset)[:, None]
                                       + direction*np.array([aa, bb_polygon]))))
        ax.add_patch(Polygon(polygon, facecolor=color, edgecolor="none", zorder=3))
    a_offset, b_offset = offset
    for curve in boundaries:
        ax.plot(*xy(a_offset+direction*curve, b_offset+direction*bb),
                color=FLAT_EDGE, lw=.8, zorder=4)


def verify_added_exterior(cap):
    """Match the collar's F=pq to the null coordinates of the flat tail."""
    x_start, x_match = 1.25, 1.30
    x_flat = np.sqrt(1+FLAT_EXTERIOR_PHI)

    def log_product_rhs(x, _):
        shift = float(W(x*x-1))
        return [2*cap.kappa/(shift*shift-1)]

    product = solve_ivp(log_product_rhs, [x_start, x_flat],
                        [np.log(-cap.F(x_start))], rtol=2e-11, atol=1e-12,
                        dense_output=True)
    assert product.success
    assert np.isclose(-np.exp(product.sol(x_match)[0]), cap.F(x_match), rtol=1e-9)
    assert np.all(W(np.array([x_flat+1e-8, 2., 10.])**2-1) == -2)
    assert np.isclose(log_product_rhs(x_flat, None)[0], 2*cap.kappa/3)

    # In the tail F is negative and grows exponentially in magnitude.
    # At fixed q<0, C=(1-v^2)/(kappa^2*p*q) gives d(lambda)/dp ∝ 1/p.
    # Thus p→∞ is future null infinity, approached at infinite affine length.
    scri_x, scri_t = front_xy(np.inf, np.array([0., -np.inf]))
    assert np.allclose(scri_t - scri_x, -AF)
    assert np.isclose(scri_t[0]+scri_x[0], B)
    assert np.isclose(scri_t[1]+scri_x[1], 3*B)
    other_x, other_t = front_xy(np.array([0., np.inf]), -np.inf)
    assert np.allclose(other_x + other_t, 3*B)
    assert np.allclose([scri_x[1], scri_t[1]], [other_x[1], other_t[1]])


def verify_across_blue_edges(cap):
    """Check the cap chart on both sides of each wall in the added copy."""
    kappa = cap.kappa
    for x in (-3., -1., 0., 1., 3.):
        shift = float(W(x*x-1))
        s = x-1
        d = (shift+1+kappa*s)/s**2 if s else -.5
        U = -.7
        V = s/U
        b = V**2*d/kappa
        metric = np.array([[U**2*b**2-2*b/kappa, U**2*b-1/kappa],
                           [U**2*b-1/kappa, U**2]])
        original = np.array([[shift**2-1, -shift], [-shift, 1.]])
        jacobian = np.array([[-1/(kappa*U), 0.], [V, U]])
        assert np.allclose(metric, jacobian.T @ original @ jacobian)
        assert np.isclose(np.linalg.det(metric), -1/kappa**2)


def continue_worldline(cap, energy, x_start, p_start, q_start):
    """Integrate to the flat tail, then use its exact inertial motion."""
    x_flat = np.sqrt(1+FLAT_EXTERIOR_PHI)

    def log_rates(x, _):
        shift = float(W(x*x-1))
        dx = np.sqrt(energy**2+shift**2-1)
        return cap.kappa/dx * np.array([1/(dx+energy), 1/(dx-energy)])

    transition = solve_ivp(log_rates, [x_start, x_flat],
                           np.log([p_start, -q_start]), rtol=2e-11, atol=1e-12,
                           dense_output=True)
    assert transition.success
    dx_flat = np.sqrt(energy**2+3)
    flat_rates = cap.kappa/dx_flat * np.array([1/(dx_flat+energy), 1/(dx_flat-energy)])
    assert np.allclose(log_rates(x_flat, None), flat_rates)
    assert np.all(flat_rates > 0)
    assert np.isclose(3*np.prod(dx_flat*flat_rates)/cap.kappa**2, 1)
    # The straight tail continues to unbounded x at constant dx/dtau.
    # Sample it near i+; the plot appends its exact compactified endpoint.
    flat_distance = np.linspace(0, 40, 360)[1:]
    flat_logs = transition.y[:, -1, None] + flat_rates[:, None]*flat_distance
    transition_logs = transition.sol(np.linspace(x_start, x_flat, 240)[1:])
    p, minus_q = np.exp(np.column_stack([transition_logs, flat_logs]))
    return p, -minus_q


def trace_worldline(cap, xi, energy):
    """Trace the future half of an axial geodesic through the central event.

    Use the global W inside the bubble, matched to the regular cap chart.
    The affine-collar formula must not be extrapolated into the flat core.
    """
    pi, qi = cap.pq_factors(xi)

    def backward_rhs(x, state):
        v = float(W(x*x-1))
        f = 1-v*v
        dx = np.sqrt(energy*energy-f)
        return [(energy-v*dx)/(f*dx), 1/dx,
                -cap.kappa/(v+1), cap.kappa/(v-1)]

    back = solve_ivp(backward_rhs, [xi, 0], [0, 0, np.log(pi), np.log(qi)],
                     rtol=2e-11, atol=1e-12, dense_output=True, max_step=.002)
    assert back.success
    xb = np.linspace(0, xi, 700)
    tb, taub, logp, logq = back.sol(xb)
    # Time translation puts the center crossing at the fixed event of the
    # (t,x) reversal. Its composition with parameter reversal fixes the tangent.
    tb -= tb[0]
    pb, qb = np.exp(logp+cap.kappa*tb), np.exp(logq-cap.kappa*tb)
    vb = W(xb*xb-1)
    dx = np.sqrt(energy*energy-(1-vb*vb))
    dt = (energy-vb*dx)/(1-vb*vb)
    assert np.max(abs(-dt*dt+(dx-vb*dt)**2+1)) < 2e-10
    assert np.max(abs(dt+vb*(dx-vb*dt)-energy)) < 2e-10
    p0, q0 = pb[-1], qb[-1]
    dp0 = cap.kappa*p0/(energy+dx[-1])
    dq0 = -cap.kappa*q0*(energy+dx[-1])/(1-vb[-1]**2)

    def regular_rhs(tau, state):
        p, q, dp, dq = state
        derivative = cap.dlogC_dz(cap.x_from_product(p*q))
        return [dp, dq, -q*derivative*dp*dp, -p*derivative*dq*dq]

    def end_collar(tau, state):
        return state[0]*state[1]-cap.F(1.25)
    end_collar.terminal = True
    end_collar.direction = -1
    forward = solve_ivp(regular_rhs, [0, .6], [p0, q0, dp0, dq0],
                        events=end_collar, rtol=2e-11, atol=1e-12,
                        dense_output=True, max_step=.002)
    assert forward.success and len(forward.t_events[0]) == 1
    tcross = brentq(lambda tau: forward.sol(tau)[1], 0, forward.t[-1], xtol=1e-13)
    tauf = np.linspace(0, forward.t[-1], 400)
    p, q, dp, dq = forward.sol(tauf)
    xx = np.array([cap.x_from_product(z) for z in p*q])
    cc = np.array([cap.C(x) for x in xx])
    assert np.max(abs(cc*dp*dq+1)) < 2e-9
    assert np.max(abs(cap.kappa*cc*(q*dp-p*dq)/2-energy)) < 2e-9
    assert np.all(abs(xx*xx-1) < .9)
    tail_p, tail_q = continue_worldline(cap, energy, xx[-1], p[-1], q[-1])
    pp, qq = np.r_[pb, p[1:], tail_p], np.r_[qb, q[1:], tail_q]
    scales = (pb[0], qb[0])
    X, T = front_xy(pp, qq, scales)
    assert np.all(np.diff(T) > abs(np.diff(X)))
    assert np.hypot(*(np.asarray(front_xy(np.inf, -np.inf))-[X[-1], T[-1]])) < .004
    assert np.allclose([X[0], T[0]], [0, 0], atol=2e-14)
    assert np.allclose([dx[0], dt[0]], [np.sqrt(energy**2-1), energy])
    # The center is x=0 in the SAME globally matched null coordinates.
    center_t = np.linspace(tb[0]-9, tb[0]+9, 500)
    center_p = np.exp(logp[0]+cap.kappa*center_t)
    center_q = np.exp(logq[0]-cap.kappa*center_t)
    return {"future":np.column_stack([X, T]), "center":(center_p, center_q),
            "cross":forward.sol(tcross)[:2], "energy":energy,
            "duration":tcross-taub[0], "collar_index":len(pb)+len(p)-2,
            "scales":scales}


def trace_backward_rider(cap, energy):
    """Trace the x >= 0 half of a geodesic with dx/dtau < 0."""
    x_flat = np.sqrt(1+FLAT_EXTERIOR_PHI)

    def rates(x, _):
        shift = float(W(x*x-1))
        speed = np.sqrt(energy**2+shift**2-1)
        # Rationalize dt/dtau so it stays finite at the front horizon.
        dt_dx = -(energy**2+shift**2)/(speed*(energy-shift*speed))
        # p/p_c=(1-x) exp(log_p_factor + kappa*t). Inside the affine
        # collar the zero at x=1 is explicit in FrontCollar.pq_factors.
        log_p_rate = (-1/(1+x) if abs(x*x-1) <= .9
                      else 1/(1-x)-1/(1+shift))
        return cap.kappa*np.array([dt_dx, log_p_rate, 1/(shift-1)])

    solution = solve_ivp(rates, [0., x_flat], [0., 0., 0.],
                         rtol=2e-11, atol=1e-12, dense_output=True)
    assert solution.success
    x = np.r_[np.linspace(0., 1., 401), np.linspace(1., x_flat, 241)[1:]]
    time, log_p_factor, log_q_factor = solution.sol(x)
    p = (1-x)*np.exp(log_p_factor+time)
    q = np.exp(log_q_factor-time)
    assert p[400] == 0 and q[400] > 0
    assert np.all(np.diff(time) < 0)
    # The flat tail gives linear growth of log(-p) and log(q) with x.
    flat_time_rate = rates(x_flat, None)[0]
    flat_rates = np.array([cap.kappa+flat_time_rate, -cap.kappa/3-flat_time_rate])
    assert np.all(flat_rates > 0)
    flat_distance = np.linspace(0., 58., 701)[1:]
    tail = np.exp(flat_rates[:, None]*flat_distance)
    X, T = front_xy(np.r_[p, p[-1]*tail[0]], np.r_[q, q[-1]*tail[1]])
    assert np.all(np.diff(T) < 0)
    assert np.all(np.diff(T) <= -abs(np.diff(X))+2e-15)
    assert np.hypot(X[-1], T[-1]+B) < .001
    past = np.vstack([np.column_stack([X, T]), [0., -B]])
    # The time-reversing isometry preserves the future tangent when the
    # proper-time parameter is reversed as well.
    return np.vstack([past[:0:-1], -past])


def verify_comparison():
    cap = FrontCollar("cap")
    verify_added_exterior(cap)
    verify_across_blue_edges(cap)
    xx = np.linspace(-4, 4, 1601)
    spherical = W(xx**2 - 1)
    capped = W(xx**2 + cap.psi(np.zeros_like(xx)) - 1)
    assert np.array_equal(spherical, capped)
    assert np.array_equal(W(xx**2-1), W((-xx)**2-1))
    phi = np.linspace(-2, 3, 50001)
    assert np.max(np.diff(W(phi))) < 1e-13
    assert W(-1) == 0 and W(0) == -1 and W(2) == -2
    assert np.allclose(W(np.array([-.8, 0, .8])), [-.6, -1, -1.4])
    # Unique stationary-limit roots on the axis, kappa=-v_x(1)=1.
    root = brentq(lambda x: float(W(x*x-1)+1), .5, 1.5)
    assert abs(root-1) < 1e-12
    eps = 1e-5
    vx = (W((1+eps)**2-1)-W((1-eps)**2-1))/(2*eps)
    assert abs(vx+1) < 1e-9

    yy = np.linspace(-1, 1, 1801)
    psi = cap.psi(yy)
    assert abs(psi[0]-1) < 1e-12 and abs(psi[-1]-1) < 1e-12
    assert np.all(psi[np.abs(yy) <= cap.a] == 0)
    wall_x = np.sqrt(np.maximum(1-psi, 0))
    assert np.max(abs(W(wall_x**2 + psi - 1)+1)) < 1e-12

    sol, tcross = cap.geodesic()
    tau = np.linspace(0, sol.t[-1], 300)
    p, q, dp, dq = sol.sol(tau)
    xx = np.array([cap.x_from_product(z) for z in p*q])
    cc = np.array([cap.C(x) for x in xx])
    norm_error = float(np.max(abs(cc*dp*dq+1)))
    energy = cap.kappa*cc*(q*dp-p*dq)/2
    assert norm_error < 2e-9 and np.ptp(energy) < 2e-9 and energy[0] > 1
    assert q[0] > 0 > q[-1] and np.all(p > 0)
    assert np.all(abs(xx**2-1) < .9)  # The global W is exactly affine here.
    X, T = front_xy(p, q)
    dX, dT = np.gradient(X, tau), np.gradient(T, tau)
    assert np.all(dT > abs(dX))  # Plotted traveler is future timelike.
    xc, tc = front_xy(*sol.sol(tcross)[:2])
    assert abs(xc+tc-B) < 1e-12 and tc > np.pi/6
    # All constant-p and constant-q curves have slopes +/-1 in (X,T).
    for q0 in (-.15, 0, .15):
        x0, t0 = front_xy(np.linspace(-.7, .7, 50), q0)
        assert np.ptp(x0+t0) < 1e-12
    # At q=0, x=1 for all finite p. The front and rear axial horizons
    # meet this edge at p=0 and p=infinity, respectively.
    attachment_x, attachment_t = front_xy(np.array([0., np.inf]), 0)
    assert np.allclose(attachment_x + attachment_t, B)
    assert np.allclose(attachment_t - attachment_x, [AF, -AF])
    seed_p, seed_q = sol.y[:2, 0]
    xi = cap.x_from_product(seed_p*seed_q)
    traveler = trace_worldline(cap, xi, energy[0])
    traveler["backward"] = trace_backward_rider(cap, energy[0])
    p_center, q_center = traveler["scales"]
    p_test, q_test = np.array([.2, 1., 3.])*p_center, np.array([4., .6, 1.])*q_center
    assert np.allclose(front_xy(p_center**2/p_test, q_center**2/q_test, traveler["scales"]),
                       -np.asarray(front_xy(p_test, q_test, traveler["scales"])))
    crossing = np.array(front_xy(*traveler["cross"], traveler["scales"]))
    assert np.isclose(sum(crossing), B)
    assert abs(crossing[1]-crossing[0]) < -AF
    # Only the outward sector is shaded; it lies strictly outside B<=pi/2.
    ax, at = front_xy(np.array([.1, .7]), np.array([-.3, -.1]))
    assert np.all(ax+at > B)
    report = [
        "Matched global profiles: spherical W(x^2+y^2+z^2-1), capped W(x^2+psi(y^2+z^2)-1).",
        "Axial shifts identical; W smooth, bounded, nonincreasing, with flat core and constant exterior.",
        "Both axial horizons at x=+/-1 with |v_x|=1; cap radius a=0.6, transverse outer radius b=1.",
        f"Timelike geodesic: norm error {norm_error:.3g}, E={energy[0]:.12g}, drift {np.ptp(energy):.3g}.",
        f"Crossing tau={tcross:.12g}, p={sol.sol(tcross)[0]:.12g}; q=0, X+T=pi/2.",
        "Null lines have 45-degree slopes. The green edge shows q=0, 0<p<infinity, between the axial horizons and disjoint from ordinary future null infinity.",
        "Spatial sections show the walls at fixed time and z=0.",
        "The even shift makes (t,x) reversal a time-reversing isometry. Center-normalized null coordinates make it (X,T) reversal in the diagram.",
        "Reversing the proper-time parameter after applying the isometry fixes the future tangent at the central event, so the reflected curves are one geodesic.",
        f"Proper time between rear and front crossings: {2*traveler['duration']:.9f}.",
        "The trajectory continues to infinite proper time in both flat exteriors.",
        "The added axial future null edges are A=pi/6 and B=3pi/2; the past edges are their reflections. Each pair meets at added timelike infinity.",
        "The A=pi/6 edge and the rear axial horizon have the common limit (pi/6, pi/2).",
        "Across the blue edges the same cap metric covers all x on each added side. The next axial horizons are regular; dotted segments mark the next cap attachments.",
    ]
    out = BASE / "output/sech"
    out.mkdir(parents=True, exist_ok=True)
    (out/"bubble_extension_comparison_check.txt").write_text("\n".join(report)+"\n", encoding="utf-8")
    print("\n".join(report))
    return cap, traveler


def axial_panel(ax, cap, traveler):
    ax.set_aspect("equal")
    ax.axis("off")
    scales = traveler["scales"]
    bb, flat_boundaries = axial_flat_boundaries(cap, scales)
    shade_axial_diamond(ax, bb, flat_boundaries)
    for aa in [AF, -AF]:
        ax.plot(*xy([aa, aa], [-B, B]), color=BLUE, lw=1.4, ls=HORIZON_STYLE, zorder=5)
    # Outline the original domain and mark both attachments.
    boundary = np.array([(0, -B), (B, 0), (0, B), (-B, 0), (0, -B)])
    ax.plot(*boundary.T, color=GRAY, lw=1.2, zorder=4)
    added = np.column_stack(front_xy([0, np.inf, np.inf, 0], [0, 0, -np.inf, -np.inf]))
    # The entire U<0 copy is the original axial diamond rotated about
    # (A,B)=(AF,B). The other copy is its reflection through the origin.
    added_min_a = 2*AF-B
    across_blue = rectangle(added_min_a, AF, B, 3*B)
    far_scri = np.vstack([xy(-B, B), across_blue[[0, 3]]])
    crossing = np.asarray(front_xy(*traveler["cross"], scales))
    gray_leader = {"arrowstyle":"-", "lw":.8, "color":GRAY}
    for direction, time_sign, cap_label in ((1, "+", "Front cap"), (-1, "-", "Rear cap")):
        corners = direction*added
        shade_axial_diamond(ax, bb, flat_boundaries, (direction*2*AF, direction*2*B), -direction)
        ax.plot(*(direction*np.asarray(xy([-B, -AF], B))), color=GREEN,
                lw=2.6, solid_capstyle="butt", zorder=5)
        ax.plot(*corners[[3, 0]].T, color=BLUE, lw=1.4, ls=HORIZON_STYLE, zorder=5)
        ax.plot(*(direction*np.asarray(xy(-B, [B, 3*B]))), color=BLUE,
                lw=1.4, ls=HORIZON_STYLE, zorder=5)
        ax.plot(*corners[[1, 2, 3]].T, color=GRAY, lw=2.1, solid_capstyle="butt", zorder=5)
        ax.plot(*(direction*far_scri.T), color=GRAY, lw=2.1,
                solid_capstyle="butt", zorder=5)
        ax.plot(*(direction*across_blue[[3, 2]].T), color=GREEN, lw=1.8,
                ls=(0, (1, 2)), zorder=5)
        ax.plot(*(direction*np.asarray(xy([-AF, B], B))), color=GRAY, lw=2.1,
                solid_capstyle="butt", zorder=5)
        ax.scatter(*(direction*np.vstack([added[[1, 2]], xy(-B, B)]).T),
                   s=28, facecolors="white", edgecolors=GRAY,
                   linewidths=1, zorder=11)
        ax.scatter(*(direction*crossing), s=28, color=RED, zorder=10)
        ax.annotate(cap_label, direction*np.asarray(xy(-.97, B)),
                    xytext=direction*np.array([3.54, -.18]), ha="center",
                    fontsize=LABEL_SIZE, color=GREEN,
                    arrowprops={"arrowstyle":"-", "color":GREEN, "lw":.8})
        ax.annotate(rf"Original $\mathscr{{I}}^{time_sign}$", direction*np.asarray(xy(1.17, B)),
                    xytext=direction*np.array([-1.13, 1.65]), ha="center",
                    fontsize=LABEL_SIZE, color=GRAY, arrowprops=gray_leader)
        for edge, label_xy in (([1, 2], [.69, 2.18]), ([2, 3], [3.09, 2.57])):
            ax.annotate(rf"Added $\mathscr{{I}}^{time_sign}$", np.mean(corners[edge], axis=0),
                        xytext=direction*np.asarray(label_xy), ha="center",
                        va="top" if direction < 0 else "baseline",
                        fontsize=LABEL_SIZE, color=GRAY, arrowprops=gray_leader)
        ax.annotate(rf"$i^{time_sign}_{{\mathrm{{add}}}}$", corners[2],
                    xytext=direction*np.array([2.09, 2.87]), ha="center",
                    fontsize=LABEL_SIZE, color=GRAY)
    center_x, center_t = front_xy(*traveler["center"], scales)
    ax.plot(center_x, center_t, color=ORANGE, lw=1.7, ls=CENTER_STYLE, zorder=6)
    ax.annotate("Center rider", (center_x[263], center_t[263]), xytext=(-2.08, .70),
                fontsize=LABEL_SIZE, color=ORANGE, ha="center",
                arrowprops={"arrowstyle":"-", "color":ORANGE, "lw":.7})
    backward = traveler["backward"]
    ax.plot(*backward.T, color=PURPLE, lw=1.8, ls=BACKWARD_STYLE, zorder=7)
    ax.annotate("Backward free fall", backward[len(backward)//2+660],
                xytext=(-1.23, 2.33), ha="center", fontsize=LABEL_SIZE, color=PURPLE,
                arrowprops={"arrowstyle":"-", "color":PURPLE, "lw":.8})
    future = np.vstack([traveler["future"], added[2]])
    path = np.vstack([-future[:0:-1], future])
    ax.plot(*path.T, color=RED, lw=2.4, zorder=8)
    arrow = traveler["collar_index"] + 270
    for start, end in ((-future[arrow], -future[arrow-38]), (future[arrow-38], future[arrow])):
        ax.annotate("", end, xytext=start,
                    arrowprops={"arrowstyle":"-|>", "color":RED, "lw":1.8}, zorder=9)
    ax.annotate("Forward free fall", future[460], xytext=(1.96, -.87), fontsize=LABEL_SIZE, color=RED,
                arrowprops={"arrowstyle":"-", "color":RED, "lw":.8})
    ax.annotate("Rear horizon", xy(-AF, .60), xytext=(-1.60, 1.02),
                fontsize=LABEL_SIZE, color=BLUE, ha="center",
                arrowprops={"arrowstyle":"-", "color":BLUE, "lw":.8})
    ax.set(xlim=(-4.42, 4.42), ylim=(-3.10, 3.08))
    ax.set_title("(a) Axial spacetime and extension", loc="left", fontsize=TITLE_SIZE, pad=7)


def spatial_panel(ax, cap, capped):
    y = np.linspace(-1, 1, 1801)
    xx = np.sqrt(np.maximum(1-(cap.psi(y) if capped else y*y), 0))
    wall = np.column_stack([np.r_[xx, -xx[::-1]], np.r_[y, y[::-1]]])
    ax.add_patch(Polygon(wall, facecolor=PALE_BLUE, edgecolor=BLUE, lw=1.4))
    ax.axhline(0, color="#93999e", lw=.8, ls=(0, (4, 3)), zorder=3)
    ax.plot([-.88, .88], [0, 0], color=GRAY, lw=1.2, zorder=4)
    ax.text(0, -.25, "Axis of travel", ha="center", fontsize=LABEL_SIZE, color=GRAY)
    ax.annotate("", (1.42, -1.03), xytext=(.83, -1.03),
                arrowprops={"arrowstyle":"->", "lw":1, "color":GRAY})
    ax.text(1.12, -1.21, r"$x$", ha="center", fontsize=LABEL_SIZE, color=GRAY)
    if capped:
        ax.plot([1, 1], [-cap.a, cap.a], color=GREEN, lw=3, zorder=5)
        ax.plot([-1, -1], [-cap.a, cap.a], color=GREEN, lw=3, zorder=5)
        ax.annotate("Front cap", (1, .27), xytext=(1.19, .32), color=GREEN, fontsize=LABEL_SIZE,
                    arrowprops={"arrowstyle":"-", "lw":.8, "color":GREEN})
        ax.annotate("Rear cap", (-1, .25), xytext=(-.64, .64), color=GREEN, fontsize=LABEL_SIZE,
                    arrowprops={"arrowstyle":"-", "lw":.8, "color":GREEN})
        title, subtitle, color = "(c) Capped wall", "Smooth 4D extension", GREEN
    else:
        ax.annotate("Curved front", (.98, .20), xytext=(1.12, .52), color=BLUE, fontsize=LABEL_SIZE,
                    arrowprops={"arrowstyle":"-", "lw":.8, "color":BLUE})
        title, subtitle, color = "(b) Spherical wall", r"$C^2$-inextendible in 4D", RED
    ax.text(0, 1.01, title, transform=ax.transAxes, fontsize=TITLE_SIZE, va="bottom")
    ax.text(0, -.04, subtitle, transform=ax.transAxes, color=color, fontsize=LABEL_SIZE, va="top")
    ax.set(xlim=(-1.15, 1.99), ylim=(-1.25, 1.12), aspect="equal")
    ax.axis("off")


def main():
    cap, traveler = verify_comparison()
    plt.rcParams.update({"font.family":"sans-serif", "font.sans-serif":["Arial", "DejaVu Sans"],
                         "mathtext.fontset":"stix", "font.size":12,
                         "pdf.fonttype":42, "ps.fonttype":42})
    fig = plt.figure(figsize=(11.6, 6.6))
    grid = fig.add_gridspec(2, 2, width_ratios=[2.05, 1], hspace=.30, wspace=.10)
    axial_panel(fig.add_subplot(grid[:, 0]), cap, traveler)
    spatial_panel(fig.add_subplot(grid[0, 1]), cap, False)
    spatial_panel(fig.add_subplot(grid[1, 1]), cap, True)
    fig.subplots_adjust(left=.025, right=.985, top=.945, bottom=.08)
    FIGURES.mkdir(parents=True, exist_ok=True)
    for suffix in ["pdf", "png"]:
        target = FIGURES / f"bubble_extension_comparison.{suffix}"
        fig.savefig(target, dpi=230, bbox_inches="tight", facecolor="white")
        print(target)
    plt.close(fig)


if __name__ == "__main__":
    main()
