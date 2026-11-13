"""Geometry checks for a global meridional boundary atlas; deliberately no plot.

The bounded bulk chart below is global, but its naive cube closure is NOT a
Penrose completion. Ordinary scri requires separate (s,u,theta) charts. The
finite-parameter front and the rider's infinite-time end are different pieces.
"""
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/global_2p1"
RF = float(np.arccosh(2.0))
KAPPA = np.sqrt(3.0) / 2


def v0(x):
    return 2 / np.cosh(x) - 2


def v0prime(x):
    return -2 * np.tanh(x) / np.cosh(x)


def flow(t, xi):
    """Complete axial outgoing-null flow and its derivative with respect to xi."""
    if t == 0:
        return xi, 1.0
    sol = solve_ivp(
        lambda _, z: [1 + v0(z[0]), v0prime(z[0])],
        [0, t], [xi, 0.0], method="DOP853", rtol=3e-12, atol=2e-13,
        max_step=.15,
    )
    assert sol.success
    return sol.y[0, -1], np.exp(sol.y[1, -1])


def checks():
    vv = sp.symbols("v", real=True)
    gold = sp.Matrix([[vv**2 - 1, -vv, 0], [-vv, 1, 0], [0, 0, 1]])
    gi = gold.inv()
    for covector in (sp.Matrix([1, 0, -1]), sp.Matrix([1, 0, 1])):
        assert (covector.T * gi * covector)[0] == 0
    ff, hh = sp.symbols("f h", positive=True)
    dtau = sp.Matrix([(ff + hh) / 2, 0, (-ff + hh) / 2])
    assert sp.simplify((dtau.T * gi * dtau)[0] + ff * hh) == 0

    # Exact metric pullback: variables in order A,U,V. J=dx/dA is negative.
    cu, cv, jj, bb, delta = sp.symbols("cu cv J b delta", nonzero=True, real=True)
    dt = sp.Matrix([[0, 1 / (2 * cu**2), 1 / (2 * cv**2)]])
    dy = sp.Matrix([[0, -1 / (2 * cu**2), 1 / (2 * cv**2)]])
    dx = bb * dt + sp.Matrix([[jj, 0, 0]])
    jac = dt.col_join(dx).col_join(dy)
    pulled = sp.simplify(jac.T * gold.subs(vv, bb - 1 + delta) * jac)
    eta = sp.Matrix([[jj, (1 - delta) / (2 * cu**2), (1 - delta) / (2 * cv**2)]])
    exact = -dt.T * dt + eta.T * eta + dy.T * dy
    assert sp.simplify(pulled - exact) == sp.zeros(3)
    scaled = sp.simplify(cu**2 * cv**2 * pulled)
    assert sp.simplify(scaled.det() + jj**2 * cu**2 * cv**2 / 4) == 0

    max_roundtrip = 0.0
    for tt in (-4., -1., 0., 1., 4.):
        for xi in (-3., -RF, -.4, 0., .7, RF, 3.):
            xx, deriv = flow(tt, xi)
            back, _ = flow(-tt, xx)
            max_roundtrip = max(max_roundtrip, abs(back - xi))
            assert deriv > 0 and abs(back - xi) < 2e-8

    # The global bulk chart keeps the crucial axial endpoints distinct.
    aa = np.arctan(.5)
    center_errors = []
    for tt in (6., 12., 20.):
        xi, _ = flow(-tt, 0.)
        center_errors.append(abs(-np.arctan(xi / (2 * RF)) - aa))
    assert center_errors[-1] < 1e-6
    for label in (-.8, -aa, 0., .3):
        assert label < aa
        xx, _ = flow(20., -2 * RF * np.tan(label))
        assert abs(xx - RF) < 3e-5

    # Ordinary null-infinity charts in laboratory polar coordinates.
    # s=1/R, t=u+R (future) or t=w-R (past), X=R cos(theta).
    ss, ct, st, shift = sp.symbols("s ctheta stheta shift", nonzero=True, real=True)
    for sign in (1, -1):
        jlab = sp.Matrix([[1, -sign / ss**2, 0],
                          [0, -ct / ss**2, -st / ss],
                          [0, -st / ss**2, ct / ss]])
        glab = sp.Matrix([[shift**2 - 1, -shift, 0], [-shift, 1, 0], [0, 0, 1]])
        gs = sp.simplify(ss**2 * jlab.T * glab * jlab)
        expected = sp.Matrix([[-ss**2, sign, 0], [sign, 0, 0], [0, 0, 1]])
        flat_error = (gs.subs(shift, 0) - expected).applyfunc(
            lambda z: sp.factor(z).subs(st**2, 1 - ct**2).simplify())
        assert flat_error == sp.zeros(3)
        determinant = sp.factor(gs.det()).subs(st**2, 1 - ct**2).simplify()
        assert determinant == -1

    mp.mp.dps = 65
    scri_errors = []
    for ssval in (mp.mpf('.04'), mp.mpf('.02'), mp.mpf('.01')):
        worst = mp.mpf(0)
        for sign in (1, -1):
            for uu in (-2, 0, 2):
                for theta in (0, mp.pi / 5, mp.pi / 2, mp.pi):
                    tt = uu + sign / ssval
                    xx = mp.cos(theta) / ssval
                    yy = mp.sin(theta) / ssval
                    rb = mp.sqrt((xx - 2 * tt)**2 + yy**2)
                    shiftval = 2 / mp.cosh(rb)
                    dtime = mp.matrix([[1, -sign / ssval**2, 0]])
                    dxx = mp.matrix([[0, -mp.cos(theta) / ssval**2, -mp.sin(theta) / ssval]])
                    correction = ssval**2 * (shiftval**2 * dtime.T * dtime
                                             - shiftval * (dtime.T * dxx + dxx.T * dtime))
                    worst = max(worst, max(abs(z) for z in correction))
        scri_errors.append(float(worst))
    assert scri_errors[-1] < 1e-35

    # A need not extend to regular scri. Same boundary point (u,theta)=(0,0),
    # but theta^2 R=d gives distinct outgoing axial phases, hence distinct A.
    rr = mp.acosh(2)
    cphase = 4 * rr / mp.sqrt(3)
    phase_limits = []
    for dd in (0, 1, 4):
        radius = mp.mpf('1e10')
        theta = mp.sqrt(dd / radius)
        tt = radius
        xx = radius * mp.cos(theta) - 2 * tt
        phase = tt + xx + cphase - 2 / mp.sqrt(3) * mp.log(
            (1 - mp.exp(xx + rr)) / (1 - mp.exp(xx - rr)))
        expected = cphase - mp.mpf(dd) / 2
        assert abs(phase - expected) < mp.mpf('1e-9')
        phase_limits.append(float(expected))

    # Exact transverse Jacobi coefficient along an outgoing axial null ray.
    # x=RF-E*(lambda_*-lambda), dt/dlambda=E/(1+v0).
    rr = mp.acosh(2)
    kk = mp.sqrt(3) / 2
    cc = 1 / (kk * rr)
    jacobi_errors = []
    for eps in (mp.mpf('1e-4'), mp.mpf('1e-8'), mp.mpf('1e-16')):
        xx = rr - eps
        vp = -2 * mp.tanh(xx) / mp.cosh(xx)
        vyy = vp / xx
        coeff = -eps**2 * vyy / (2 / mp.cosh(xx) - 1)**2
        jacobi_errors.append(float(abs(coeff - cc)))
    assert jacobi_errors[-1] < 1e-14
    pplus = (1 + mp.sqrt(1 + 4 * cc)) / 2
    pminus = (1 - mp.sqrt(1 + 4 * cc)) / 2
    assert pplus > 1 and pminus < 0

    lines = [
        "GLOBAL MERIDIONAL ATLAS: CHECKED BULK AND OPEN BOUNDARY CHARTS; NO DRAWING",
        "Exact optical functions t-y and t+y: both null for the full meridional metric.",
        "tau=(atan(t-y)+atan(t+y))/2: norm -cos(U)^2 cos(V)^2 < 0, future oriented.",
        "A=-atan(Phi_{-t}(x)/(2 RF)): smooth global outgoing axial-flow label.",
        "(A,U,V) is a global bulk cube chart; rho>=0 quotient is the wedge U<=V.",
        f"Flow roundtrip maximum error: {max_roundtrip:.4g}.",
        "Exact metric pullback and determinant checked symbolically.",
        "Rescaled bulk determinant = -J^2 cos(U)^2 cos(V)^2/4 < 0.",
        f"Center label tends a=atan(1/2): sampled errors {center_errors}.",
        "Finite axial front ends have U=V=pi/2 and A<a; front generator A=-a.",
        "The cube closure does NOT resolve ordinary scri or its corner junctions.",
        "Separate scri charts: s=1/R, u=t-R or w=t+R, theta; scaled determinant exactly -1.",
        "At s=0 the limits are -s^2 du^2 +/- 2 du ds + dtheta^2; normal ds is null.",
        f"Maximum sampled scri metric errors at s=.04,.02,.01: {scri_errors}.",
        "Warp correction is flat at finite-u/w scri since rb >= (V-1)/s - V*abs(u or w).",
        f"Same regular scri point (u,theta)=(0,0), different axial phase limits: {phase_limits}.",
        "Thus A is a bulk coordinate, not a continuous boundary coordinate at all ordinary scri points.",
        "Front/center bounded-position t->+infinity instead have lab retarded time ->-infinity.",
        f"Rounded front Jacobi c=1/(kappa RF)={mp.nstr(cc, 13)}; coefficient errors {jacobi_errors}.",
        f"Transverse indicial powers p+={mp.nstr(pplus, 13)}, p-={mp.nstr(pminus, 13)}.",
        "These describe linear transverse variations at the axial null ray; they do not classify all nonlinear endpoints.",
        "Planar cap interior: transverse Jacobi equation is Y''=0; finite nonzero endpoint widths are allowed.",
        "Still required: resolve boundary junctions and verify attachment topology before drawing a global completed diagram.",
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "global_boundary_atlas_check.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    checks()
