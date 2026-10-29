"""Scan Natario's projectivized high-momentum null-ray system.

This is a falsification tool for global maximality, not a proof.  In the
meridional plane the limiting system is

    x' = X(x) + m,
    m' = -(I-mm^T) (DX)^T m,
    (log rho)' = -m^T DX m,

with |m|=1 and the zero-energy constraint X.m=-1.  A bounded recurrent orbit
with positive mean log-rho growth away from the axial generator would defeat
the simplest Natario global argument.
"""

from __future__ import annotations

import argparse
import math


def profile(r: float, sigma: float, r0: float):
    u = sigma * (r - r0)
    th = math.tanh(u)
    sech2 = 1.0 - th * th
    f = 0.25 * (1.0 + th)
    fp = 0.25 * sigma * sech2
    fpp = -0.5 * sigma * sigma * sech2 * th
    return f, fp, fpp


def shift_and_jacobian(x: float, y: float, vs: float, sigma: float, r0: float):
    r2 = x * x + y * y
    if r2 < 1.0e-14:
        return 0.0, 0.0, ((0.0, 0.0), (0.0, 0.0))
    r = math.sqrt(r2)
    f, fp, fpp = profile(r, sigma, r0)
    a = 2.0 * vs * f
    b = vs * r * fp
    ar = 2.0 * vs * fp
    br = vs * (fp + r * fpp)
    u = y * y / r2
    w = x * y / r2

    xx = -a - b * u
    xy = b * w

    ux = -2.0 * x * y * y / (r2 * r2)
    uy = 2.0 * y * x * x / (r2 * r2)
    wx = y * (y * y - x * x) / (r2 * r2)
    wy = x * (x * x - y * y) / (r2 * r2)

    dxx_dx = -ar * x / r - br * x * u / r - b * ux
    dxx_dy = -ar * y / r - br * y * u / r - b * uy
    dxy_dx = br * x * w / r + b * wx
    dxy_dy = br * y * w / r + b * wy
    return xx, xy, ((dxx_dx, dxx_dy), (dxy_dx, dxy_dy))


def rhs(state, vs: float, sigma: float, r0: float):
    x, y, psi, ell = state
    mx, my = math.cos(psi), math.sin(psi)
    nx, ny = -my, mx
    xx, xy, jac = shift_and_jacobian(x, y, vs, sigma, r0)
    an_x = jac[0][0] * nx + jac[0][1] * ny
    an_y = jac[1][0] * nx + jac[1][1] * ny
    am_x = jac[0][0] * mx + jac[0][1] * my
    am_y = jac[1][0] * mx + jac[1][1] * my
    psi_dot = -(mx * an_x + my * an_y)
    ell_dot = -(mx * am_x + my * am_y)
    return xx + mx, xy + my, psi_dot, ell_dot


def add(a, b, scale):
    return tuple(a[i] + scale * b[i] for i in range(4))


def rk4(state, dt: float, vs: float, sigma: float, r0: float):
    k1 = rhs(state, vs, sigma, r0)
    k2 = rhs(add(state, k1, 0.5 * dt), vs, sigma, r0)
    k3 = rhs(add(state, k2, 0.5 * dt), vs, sigma, r0)
    k4 = rhs(add(state, k3, dt), vs, sigma, r0)
    return tuple(
        state[i] + dt * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
        for i in range(4)
    )


def constrained_directions(xx: float, xy: float):
    s2 = xx * xx + xy * xy
    if s2 < 1.0:
        return []
    s = math.sqrt(s2)
    root = math.sqrt(max(0.0, 1.0 - 1.0 / s2))
    px, py = -xy / s, xx / s
    base_x, base_y = -xx / s2, -xy / s2
    return [
        (base_x + sign * root * px, base_y + sign * root * py)
        for sign in (-1.0, 1.0)
    ]


def norm_and_radial_derivative(r, theta, vs, sigma, r0):
    f, fp, fpp = profile(r, sigma, r0)
    a = 2.0 * vs * f
    ap = 2.0 * vs * fp
    b = vs * r * fp
    bp = vs * (fp + r * fpp)
    d = 2.0 * a * b + b * b
    dp = 2.0 * (ap * b + (a + b) * bp)
    u = math.sin(theta) ** 2
    return a * a + d * u, 2.0 * a * ap + dp * u


def surface_audit(args):
    samples = []
    for it in range(101):
        theta = math.pi * it / 100.0
        lo = 1.0e-8
        slo, _ = norm_and_radial_derivative(
            lo, theta, args.vs, args.sigma, args.r0
        )
        hi = max(args.rmax, 2.0 * args.r0)
        shi, _ = norm_and_radial_derivative(
            hi, theta, args.vs, args.sigma, args.r0
        )
        if slo >= 1.0 or shi <= 1.0:
            continue
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            smid, _ = norm_and_radial_derivative(
                mid, theta, args.vs, args.sigma, args.r0
            )
            if smid < 1.0:
                lo = mid
            else:
                hi = mid
        root = 0.5 * (lo + hi)
        _, radial = norm_and_radial_derivative(
            root, theta, args.vs, args.sigma, args.r0
        )
        samples.append((radial, root, theta))
    if samples:
        radial, root, theta = min(samples)
        print(
            "inner |X|=1 surface: "
            f"min radial derivative {radial:+.8f} at "
            f"r={root:.6f}, theta={theta:.6f}"
        )


def scan(args):
    survivors = []
    total = 0
    for ir in range(args.nr):
        r = args.rmin + (args.rmax - args.rmin) * (ir + 0.5) / args.nr
        for it in range(args.ntheta):
            theta = args.theta_min + (math.pi - 2.0 * args.theta_min) * (
                it + 0.5
            ) / args.ntheta
            x, y = r * math.cos(theta), r * math.sin(theta)
            xx, xy, _ = shift_and_jacobian(x, y, args.vs, args.sigma, args.r0)
            for mx, my in constrained_directions(xx, xy):
                total += 1
                state = (x, y, math.atan2(my, mx), 0.0)
                max_r = r
                min_front = math.hypot(x - args.r0, y)
                escaped = False
                steps = int(args.time / args.dt)
                for _ in range(steps):
                    state = rk4(state, args.dt, args.vs, args.sigma, args.r0)
                    rr = math.hypot(state[0], state[1])
                    max_r = max(max_r, rr)
                    min_front = min(min_front, math.hypot(state[0] - args.r0, state[1]))
                    if rr > args.escape_radius or not all(math.isfinite(q) for q in state):
                        escaped = True
                        break
                if not escaped:
                    xx1, xy1, _ = shift_and_jacobian(
                        state[0], state[1], args.vs, args.sigma, args.r0
                    )
                    mx1, my1 = math.cos(state[2]), math.sin(state[2])
                    constraint = 1.0 + xx1 * mx1 + xy1 * my1
                    survivors.append(
                        (
                            state[3] / args.time,
                            math.hypot(state[0] - args.r0, state[1]),
                            min_front,
                            max_r,
                            abs(constraint),
                            x,
                            y,
                            mx,
                            my,
                            state[0],
                            state[1],
                        )
                    )
    survivors.sort(reverse=True)
    print(f"initial constrained rays: {total}")
    print(f"bounded through t={args.time:g}: {len(survivors)}")
    print("growth  final_front  min_front  max_r  |constraint|  initial -> final")
    for row in survivors[: args.report]:
        growth, df, mf, mr, con, x, y, mx, my, xf, yf = row
        print(
            f"{growth:+.6f}  {df:.5f}  {mf:.5f}  {mr:.4f}  {con:.2e}  "
            f"({x:+.3f},{y:+.3f}; {mx:+.3f},{my:+.3f}) -> "
            f"({xf:+.4f},{yf:+.4f})"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vs", type=float, default=2.0)
    parser.add_argument("--sigma", type=float, default=3.0)
    parser.add_argument("--r0", type=float, default=1.0)
    parser.add_argument("--rmin", type=float, default=0.15)
    parser.add_argument("--rmax", type=float, default=2.5)
    parser.add_argument("--nr", type=int, default=12)
    parser.add_argument("--ntheta", type=int, default=18)
    parser.add_argument("--theta-min", type=float, default=0.015)
    parser.add_argument("--time", type=float, default=60.0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--escape-radius", type=float, default=8.0)
    parser.add_argument("--report", type=int, default=20)
    args = parser.parse_args()
    surface_audit(args)
    scan(args)


if __name__ == "__main__":
    main()
