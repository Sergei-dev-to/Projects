"""Falsification scan for Natario's full zero-energy limiting ray system.

Unlike ``natario_ray_scan.py``, this script keeps the azimuthal component of
the ray direction.  Axisymmetry lets us place the initial point in the
``z=0`` meridional half-plane, but the direction is sampled on the complete
circle

    |m| = 1,       X . m = -1.

The evolved Cartesian system is

    x' = X + m,
    m' = -(I-m m^T) (DX)^T m,
    (log p)' = -m^T DX m.

A bounded orbit with positive mean log-momentum growth, other than the known
front separatrix, would be a candidate obstruction to the simplest global
maximality proof.  This is a search tool, not a proof.
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


def shift_and_jacobian(pos, vs: float, sigma: float, r0: float):
    x, y, z = pos
    q2 = y * y + z * z
    r2 = x * x + q2
    if r2 < 1.0e-14:
        zero = ((0.0, 0.0, 0.0),) * 3
        return (0.0, 0.0, 0.0), zero

    r = math.sqrt(r2)
    f, fp, fpp = profile(r, sigma, r0)
    a = 2.0 * vs * f
    ar = 2.0 * vs * fp
    b = vs * r * fp
    br = vs * (fp + r * fpp)
    u = q2 / r2
    c = b * x / r2

    shift = (-a - b * u, c * y, c * z)
    jac = [[0.0] * 3 for _ in range(3)]

    du_dx = -2.0 * x * q2 / (r2 * r2)
    jac[0][0] = -ar * x / r - br * x * u / r - b * du_dx

    dc_dx = br * x * x / (r * r2) + b / r2 - 2.0 * b * x * x / (r2 * r2)
    jac[1][0] = dc_dx * y
    jac[2][0] = dc_dx * z

    for k, q in enumerate((y, z), start=1):
        du_dq = 2.0 * q * x * x / (r2 * r2)
        jac[0][k] = -ar * q / r - br * q * u / r - b * du_dq
        dc_dq = br * x * q / (r * r2) - 2.0 * b * x * q / (r2 * r2)
        jac[1][k] = dc_dq * y + (c if k == 1 else 0.0)
        jac[2][k] = dc_dq * z + (c if k == 2 else 0.0)

    return shift, tuple(tuple(row) for row in jac)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def rhs(state, vs: float, sigma: float, r0: float):
    pos = state[:3]
    m = state[3:6]
    shift, jac = shift_and_jacobian(pos, vs, sigma, r0)
    atm = tuple(sum(jac[j][i] * m[j] for j in range(3)) for i in range(3))
    strain = dot(m, atm)
    mdot = tuple(-atm[i] + strain * m[i] for i in range(3))
    return tuple(shift[i] + m[i] for i in range(3)) + mdot + (-strain,)


def add(a, b, scale):
    return tuple(a[i] + scale * b[i] for i in range(7))


def rk4(state, dt: float, vs: float, sigma: float, r0: float):
    k1 = rhs(state, vs, sigma, r0)
    k2 = rhs(add(state, k1, 0.5 * dt), vs, sigma, r0)
    k3 = rhs(add(state, k2, 0.5 * dt), vs, sigma, r0)
    k4 = rhs(add(state, k3, dt), vs, sigma, r0)
    out = tuple(
        state[i] + dt * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0
        for i in range(7)
    )
    norm = math.sqrt(dot(out[3:6], out[3:6]))
    if norm == 0.0 or not math.isfinite(norm):
        return out
    return out[:3] + tuple(q / norm for q in out[3:6]) + (out[6],)


def constrained_directions(shift, nchi: int):
    s2 = dot(shift, shift)
    if s2 < 1.0:
        return []
    s = math.sqrt(s2)
    e = tuple(q / s for q in shift)

    trial = (0.0, 0.0, 1.0)
    proj = tuple(trial[i] - dot(trial, e) * e[i] for i in range(3))
    pn = math.sqrt(dot(proj, proj))
    if pn < 1.0e-10:
        trial = (0.0, 1.0, 0.0)
        proj = tuple(trial[i] - dot(trial, e) * e[i] for i in range(3))
        pn = math.sqrt(dot(proj, proj))
    u = tuple(q / pn for q in proj)
    v = (
        e[1] * u[2] - e[2] * u[1],
        e[2] * u[0] - e[0] * u[2],
        e[0] * u[1] - e[1] * u[0],
    )
    radius = math.sqrt(max(0.0, 1.0 - 1.0 / s2))
    base = tuple(-q / s for q in e)
    for i in range(nchi):
        chi = 2.0 * math.pi * (i + 0.5) / nchi
        yield tuple(
            base[j] + radius * (math.cos(chi) * u[j] + math.sin(chi) * v[j])
            for j in range(3)
        )


def scan(args):
    survivors = []
    total = 0
    for ir in range(args.nr):
        r = args.rmin + (args.rmax - args.rmin) * (ir + 0.5) / args.nr
        for itheta in range(args.ntheta):
            theta = args.theta_min + (math.pi - 2.0 * args.theta_min) * (
                itheta + 0.5
            ) / args.ntheta
            pos = (r * math.cos(theta), r * math.sin(theta), 0.0)
            shift, _ = shift_and_jacobian(pos, args.vs, args.sigma, args.r0)
            for m in constrained_directions(shift, args.nchi):
                total += 1
                state = pos + m + (0.0,)
                escaped = False
                min_axis = math.hypot(pos[1], pos[2])
                min_front = math.sqrt((pos[0] - args.front) ** 2 + pos[1] ** 2)
                max_r = r
                for _ in range(int(args.time / args.dt)):
                    state = rk4(state, args.dt, args.vs, args.sigma, args.r0)
                    rr = math.sqrt(dot(state[:3], state[:3]))
                    axis = math.hypot(state[1], state[2])
                    front = math.sqrt(
                        (state[0] - args.front) ** 2 + state[1] ** 2 + state[2] ** 2
                    )
                    min_axis = min(min_axis, axis)
                    min_front = min(min_front, front)
                    max_r = max(max_r, rr)
                    if rr > args.escape_radius or not all(math.isfinite(q) for q in state):
                        escaped = True
                        break
                if not escaped:
                    shift1, _ = shift_and_jacobian(
                        state[:3], args.vs, args.sigma, args.r0
                    )
                    constraint = 1.0 + dot(shift1, state[3:6])
                    angular = state[1] * state[5] - state[2] * state[4]
                    survivors.append(
                        (
                            state[6] / args.time,
                            math.sqrt((state[0] - args.front) ** 2 + state[1] ** 2 + state[2] ** 2),
                            min_front,
                            min_axis,
                            max_r,
                            abs(constraint),
                            abs(angular),
                            pos,
                            m,
                            state[:3],
                        )
                    )

    survivors.sort(reverse=True)
    print(f"initial constrained rays: {total}")
    print(f"bounded through t={args.time:g}: {len(survivors)}")
    print(
        "growth final_front min_front min_axis max_r |constraint| "
        "|varrho*m_phi| initial -> final"
    )
    for row in survivors[: args.report]:
        growth, df, mf, ma, mr, con, angular, pos, m, final = row
        print(
            f"{growth:+.6f} {df:.5f} {mf:.5f} {ma:.5f} {mr:.4f} "
            f"{con:.2e} {angular:.2e} ({pos[0]:+.3f},{pos[1]:+.3f}; "
            f"{m[0]:+.3f},{m[1]:+.3f},{m[2]:+.3f}) -> "
            f"({final[0]:+.4f},{final[1]:+.4f},{final[2]:+.4f})"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vs", type=float, default=2.0)
    parser.add_argument("--sigma", type=float, default=3.0)
    parser.add_argument("--r0", type=float, default=1.0)
    parser.add_argument("--front", type=float, default=1.0)
    parser.add_argument("--rmin", type=float, default=0.7)
    parser.add_argument("--rmax", type=float, default=2.0)
    parser.add_argument("--nr", type=int, default=8)
    parser.add_argument("--ntheta", type=int, default=12)
    parser.add_argument("--nchi", type=int, default=12)
    parser.add_argument("--theta-min", type=float, default=0.01)
    parser.add_argument("--time", type=float, default=60.0)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--escape-radius", type=float, default=8.0)
    parser.add_argument("--report", type=int, default=20)
    args = parser.parse_args()
    scan(args)


if __name__ == "__main__":
    main()
