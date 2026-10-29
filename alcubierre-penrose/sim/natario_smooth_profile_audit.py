"""Numerical audit of the explicit globally smooth Natario profile.

The proof is analytic; this script checks a concrete normalization
R_F=W=1 on a dense quadrature table and samples the complete inner S=1 wall.
"""

from __future__ import annotations

import bisect
import math


RF = 1.0
WIDTH = 1.0
RMIN = RF - WIDTH / 2.0
N = 200_001


def bump(s: float) -> float:
    if s <= 0.0 or s >= 1.0:
        return 0.0
    return math.exp(-1.0 / (s * (1.0 - s)))


grid = [i / (N - 1) for i in range(N)]
weights = [bump(s) for s in grid]
ds = 1.0 / (N - 1)
cumulative = [0.0] * N
for i in range(1, N):
    cumulative[i] = cumulative[i - 1] + 0.5 * ds * (
        weights[i - 1] + weights[i]
    )
integral = cumulative[-1]


def interpolate(values, s: float) -> float:
    if s <= 0.0:
        return values[0]
    if s >= 1.0:
        return values[-1]
    i = bisect.bisect_right(grid, s) - 1
    q = (s - grid[i]) / ds
    return (1.0 - q) * values[i] + q * values[i + 1]


def eta(s: float) -> float:
    if s <= 0.0:
        return 0.0
    if s >= 1.0:
        return 1.0
    return interpolate(cumulative, s) / integral


def eta_prime(s: float) -> float:
    return bump(s) / integral


def eta_second(s: float) -> float:
    if s <= 0.0 or s >= 1.0:
        return 0.0
    return (
        bump(s)
        / integral
        * (1.0 - 2.0 * s)
        / (s * s * (1.0 - s) ** 2)
    )


def data(r: float):
    s = (r - RMIN) / WIDTH
    a = 2.0 * eta(s)
    ap = 2.0 * eta_prime(s) / WIDTH
    app = 2.0 * eta_second(s) / (WIDTH * WIDTH)
    b = 0.5 * r * ap
    bp = 0.5 * (ap + r * app)
    return a, ap, b, bp


def norm2_and_derivative(r: float, theta: float):
    a, ap, b, bp = data(r)
    u = math.sin(theta) ** 2
    d = 2.0 * a * b + b * b
    norm2 = a * a + d * u
    derivative = 2.0 * a * ap + 2.0 * (
        ap * b + (a + b) * bp
    ) * u
    return norm2, derivative


wall = []
for i in range(501):
    theta = math.pi * i / 500.0
    lo, hi = RMIN, RF
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        value, _ = norm2_and_derivative(mid, theta)
        if value < 1.0:
            lo = mid
        else:
            hi = mid
    root = 0.5 * (lo + hi)
    value, derivative = norm2_and_derivative(root, theta)
    wall.append((derivative, root, theta, value))

minimum = min(wall)
maximum_root = max(row[1] for row in wall)
minimum_root = min(row[1] for row in wall)
kappa = 2.0 * eta_prime(0.5) / WIDTH

print(f"quadrature I = {integral:.18f}")
print(f"eta(1/2) = {eta(0.5):.18f}")
print(f"kappa = {kappa:.15f}")
print(f"wall root range = [{minimum_root:.12f}, {maximum_root:.12f}]")
print(
    "minimum d_r |X|^2 on sampled wall = "
    f"{minimum[0]:.12f} at r={minimum[1]:.12f}, "
    f"theta={minimum[2]:.12f}"
)
print(f"maximum wall residual = {max(abs(row[3] - 1.0) for row in wall):.3e}")

assert abs(eta(0.5) - 0.5) < 2.0e-12
assert minimum_root > RMIN
assert maximum_root <= RF + 1.0e-12
assert minimum[0] > 0.0
