"""Bounded numerical falsification pass for the scalar-shift capture proof.

This is not part of the proof and is not used by the paper.  It integrates the
exact geodesic equations with Killing time as parameter for several compact
walls, including a cubic-degenerate radial wall.  The aim is to catch sign,
normalization, and limiting-flow mistakes in Proposition 2 of paper/main.tex.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from numpy.polynomial import Polynomial
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


def transition_polynomial(degenerate: bool = False, endpoint_order: int = 5):
    """Return F,F' on [0,1], with F(0)=0 and F(1)=1.

    In the degenerate case F'(1/2)=F''(1/2)=0 and symmetry gives
    F(1/2)=1/2.  Extending F constantly outside [0,1] is C^endpoint_order.
    """

    u = Polynomial([0.0, 1.0])
    density = u**endpoint_order * (1.0 - u) ** endpoint_order
    if degenerate:
        density *= (u - 0.5) ** 2
    primitive = density.integ()
    normalization = primitive(1.0) - primitive(0.0)

    def fraction(value):
        value = np.asarray(value, dtype=float)
        clipped = np.clip(value, 0.0, 1.0)
        result = (primitive(clipped) - primitive(0.0)) / normalization
        return np.where(value <= 0.0, 0.0, np.where(value >= 1.0, 1.0, result))

    def derivative(value):
        value = np.asarray(value, dtype=float)
        result = density(np.clip(value, 0.0, 1.0)) / normalization
        return np.where((value <= 0.0) | (value >= 1.0), 0.0, result)

    return fraction, derivative


@dataclass(frozen=True)
class EllipsoidalWall:
    v_s: float = 2.0
    inner: float = 0.5
    outer: float = 1.5
    axes: tuple[float, float, float] = (1.0, 1.0, 1.0)
    center: tuple[float, float, float] = (0.0, 0.0, 0.0)
    degenerate: bool = False

    def __post_init__(self):
        fraction, derivative = transition_polynomial(self.degenerate)
        object.__setattr__(self, "_fraction", fraction)
        object.__setattr__(self, "_derivative", derivative)
        if self.degenerate and abs(self.v_s - 2.0) > 1.0e-12:
            raise ValueError("The cubic-degenerate test fixes v_s=2 so the wall is at u=1/2.")

    @property
    def width(self):
        return self.outer - self.inner

    def rho_and_gradient(self, point):
        point = np.asarray(point, dtype=float)
        center = np.asarray(self.center)
        axes = np.asarray(self.axes)
        scaled = (point - center) / axes
        rho = float(np.linalg.norm(scaled))
        if rho == 0.0:
            return rho, np.zeros(3)
        gradient = (point - center) / (axes**2 * rho)
        return rho, gradient

    def fraction_and_gradient(self, point):
        rho, grad_rho = self.rho_and_gradient(point)
        u = (rho - self.inner) / self.width
        fraction = float(self._fraction(u))
        grad_fraction = float(self._derivative(u)) * grad_rho / self.width
        return fraction, grad_fraction

    def value_gradient(self, point):
        fraction, grad_fraction = self.fraction_and_gradient(point)
        return -self.v_s * fraction, -self.v_s * grad_fraction

    def wall_u(self):
        target = 1.0 / self.v_s
        if self.degenerate:
            return 0.5
        return brentq(lambda u: float(self._fraction(u)) - target, 0.0, 1.0)

    def generator_points(self):
        rho_wall = self.inner + self.width * self.wall_u()
        center = np.asarray(self.center)
        x_offset = self.axes[0] * rho_wall
        return [center + np.array([x_offset, 0.0, 0.0]),
                center - np.array([x_offset, 0.0, 0.0])]


@dataclass(frozen=True)
class MultiWall:
    """Two or more disjoint bubble interiors with one constant exterior."""

    components: tuple[EllipsoidalWall, ...]
    v_s: float = 2.0

    def value_gradient(self, point):
        fractions = []
        gradients = []
        for component in self.components:
            fraction, gradient = component.fraction_and_gradient(point)
            fractions.append(fraction)
            gradients.append(gradient)
        product = float(np.prod(fractions))
        gradient_product = np.zeros(3)
        for index, gradient in enumerate(gradients):
            other = float(np.prod([f for j, f in enumerate(fractions) if j != index]))
            gradient_product += other * gradient
        return -self.v_s * product, -self.v_s * gradient_product

    def generator_points(self):
        points = []
        for component in self.components:
            points.extend(component.generator_points())
        return points


@dataclass(frozen=True)
class MirroredX:
    profile: object

    def value_gradient(self, point):
        reflected = np.array([-point[0], point[1], point[2]])
        value, gradient = self.profile.value_gradient(reflected)
        return value, np.array([-gradient[0], gradient[1], gradient[2]])

    def generator_points(self):
        return [np.array([-p[0], p[1], p[2]]) for p in self.profile.generator_points()]


def positive_momentum(v, c_y=0.0, c_z=0.0, energy=1.0):
    """Positive solution of E=sqrt(P^2+Q^2+1)+vP with Q_A=c_A P."""

    c2 = c_y * c_y + c_z * c_z
    a = 1.0 + c2 - v * v
    b = 2.0 * energy * v
    c = 1.0 - energy * energy
    discriminant = b * b - 4.0 * a * c
    roots = [(-b + sign * np.sqrt(discriminant)) / (2.0 * a) for sign in (-1.0, 1.0)]
    positive = [root for root in roots if root > 1.0e-12]
    if not positive:
        raise ValueError(f"No positive momentum for v={v}, c2={c2}, E={energy}")
    return max(positive)


def stable_energy(log_p, c_y, c_z, v):
    """Evaluate P(sqrt(1+c^2+P^-2)+v) without subtracting near-equals."""

    eps = np.exp(-log_p)
    root = np.sqrt(1.0 + c_y * c_y + c_z * c_z + eps * eps)
    numerator = np.exp(log_p) * (1.0 + c_y * c_y + c_z * c_z - v * v) + eps
    return numerator / (root - v)


def integrate_positive(profile, point, c=(0.0, 0.0), energy=1.0, end_time=40.0):
    value, _ = profile.value_gradient(point)
    p_x = positive_momentum(value, c[0], c[1], energy)
    initial = np.array([*point, np.log(p_x), c[0], c[1], 0.0], dtype=float)

    def rhs(_time, state):
        position = state[:3]
        log_p, c_y, c_z = state[3:6]
        value, gradient = profile.value_gradient(position)
        eps = np.exp(-log_p)
        denominator = np.sqrt(1.0 + c_y * c_y + c_z * c_z + eps * eps)
        velocity = np.array([value + 1.0 / denominator, c_y / denominator, c_z / denominator])
        return np.array([
            *velocity,
            -gradient[0],
            -gradient[1] + gradient[0] * c_y,
            -gradient[2] + gradient[0] * c_z,
            eps / denominator,
        ])

    def resolved_boost(_time, state):
        return 18.0 - state[3]

    resolved_boost.terminal = True
    resolved_boost.direction = -1

    solution = solve_ivp(
        rhs,
        (0.0, end_time),
        initial,
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=max(0.02, end_time / 3000.0),
        dense_output=True,
        events=resolved_boost,
    )
    if not solution.success:
        raise RuntimeError(solution.message)

    actual_end = float(solution.t[-1])
    sample_times = np.unique(np.concatenate((
        np.linspace(0.0, min(actual_end, 30.0), 301),
        np.geomspace(max(1.0e-3, min(actual_end, 30.0)), actual_end, 500),
    )))
    sample_times = sample_times[sample_times <= actual_end]
    states = solution.sol(sample_times)
    values = np.array([profile.value_gradient(states[:3, i])[0] for i in range(states.shape[1])])
    energies = np.array([
        stable_energy(states[3, i], states[4, i], states[5, i], values[i])
        for i in range(states.shape[1])
    ])
    final = states[:, -1]
    final_value, _ = profile.value_gradient(final[:3])
    eps = np.exp(-final[3])
    direction = np.array([1.0, final[4], final[5]]) / np.sqrt(
        1.0 + final[4] ** 2 + final[5] ** 2 + eps**2
    )
    generators = profile.generator_points()
    distance = min(float(np.linalg.norm(final[:3] - generator)) for generator in generators)
    halfway_tau = float(solution.sol(actual_end / 2.0)[6])
    return {
        "success": solution.success,
        "v+1": final_value + 1.0,
        "dir_error": float(np.linalg.norm(direction - np.array([1.0, 0.0, 0.0]))),
        "distance_G": distance,
        "logP": float(final[3]),
        "tau": float(final[6]),
        "tau_second_half": float(final[6] - halfway_tau),
        "energy_rel_drift": float(np.max(np.abs(energies - energy)) / max(1.0, abs(energy))),
        "spatial_radius_max": float(np.max(np.linalg.norm(states[:3, :], axis=0))),
        "final_position": final[:3],
        "killing_time": actual_end,
    }


def integrate_nonpositive(profile, point, p_x, q=(0.0, 0.0), end_time=100.0):
    value, _ = profile.value_gradient(point)
    energy = np.sqrt(p_x * p_x + q[0] * q[0] + q[1] * q[1] + 1.0) + value * p_x
    initial = np.array([*point, p_x, q[0], q[1], 0.0], dtype=float)

    def rhs(_time, state):
        position = state[:3]
        p, q_y, q_z = state[3:6]
        value, gradient = profile.value_gradient(position)
        dot_t = energy - value * p
        return np.array([
            value + p / dot_t,
            q_y / dot_t,
            q_z / dot_t,
            -gradient[0] * p,
            -gradient[1] * p,
            -gradient[2] * p,
            1.0 / dot_t,
        ])

    solution = solve_ivp(
        rhs,
        (0.0, end_time),
        initial,
        method="DOP853",
        rtol=2.0e-10,
        atol=2.0e-12,
        max_step=0.1,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    states = solution.y
    residuals = []
    for i in range(states.shape[1]):
        value_i, _ = profile.value_gradient(states[:3, i])
        dot_t = energy - value_i * states[3, i]
        residuals.append(dot_t * dot_t - np.dot(states[3:6, i], states[3:6, i]) - 1.0)
    return {
        "success": solution.success,
        "P_sign_preserved": bool(np.all(states[3] <= 1.0e-12)),
        "tau": float(states[6, -1]),
        "mass_shell_abs": float(np.max(np.abs(residuals))),
        "spatial_radius_max": float(np.max(np.linalg.norm(states[:3, :], axis=0))),
        "final_position": states[:3, -1],
    }


def inside_point(profile, generator_index=0, inward=0.04, transverse=(0.0, 0.0)):
    generator = np.asarray(profile.generator_points()[generator_index], dtype=float)
    sign = 1.0 if generator[0] >= np.mean([p[0] for p in profile.generator_points()]) else -1.0
    return generator + np.array([-sign * inward, transverse[0], transverse[1]])


def stable_transverse_seed(profile, generator_index=0, offset=(0.01, -0.008)):
    """Linear stable-manifold slope for each transverse mode at a generator."""

    generator = np.asarray(profile.generator_points()[generator_index], dtype=float)
    _, gradient = profile.value_gradient(generator)
    kappa = -gradient[0]
    step = 2.0e-5
    slopes = []
    for axis, displacement in zip((1, 2), offset):
        plus = generator.copy()
        minus = generator.copy()
        plus[axis] += step
        minus[axis] -= step
        _, grad_plus = profile.value_gradient(plus)
        _, grad_minus = profile.value_gradient(minus)
        hessian_aa = (grad_plus[axis] - grad_minus[axis]) / (2.0 * step)
        eigenvalue = (-kappa - np.sqrt(kappa * kappa - 4.0 * hessian_aa)) / 2.0
        slopes.append(eigenvalue * displacement)
    return tuple(slopes)


def print_result(name, result, keys: Iterable[str]):
    fields = []
    for key in keys:
        value = result[key]
        if isinstance(value, (float, np.floating)):
            fields.append(f"{key}={value:.3e}")
        else:
            fields.append(f"{key}={value}")
    print(f"{name:31s} " + "  ".join(fields))


def main():
    regular = EllipsoidalWall()
    degenerate = EllipsoidalWall(degenerate=True)
    close_to_one = EllipsoidalWall(v_s=1.05)
    ellipsoid = EllipsoidalWall(
        axes=(1.25, 0.80, 1.10), center=(0.15, 0.10, -0.05)
    )
    mirror = MirroredX(ellipsoid)
    multi = MultiWall((
        EllipsoidalWall(axes=(0.65, 0.55, 0.60), center=(0.0, 1.8, 0.0)),
        EllipsoidalWall(axes=(0.70, 0.60, 0.65), center=(0.0, -1.8, 0.0)),
    ))

    radial_offset = (0.01, -0.008)
    ellipsoid_offset = (0.001, -0.0008)

    capture_cases = [
        ("radial regular, E=1", regular, inside_point(regular, inward=0.08), (0.0, 0.0), 1.0, 25.0),
        ("radial regular, E=2", regular, inside_point(regular, inward=0.08), (0.0, 0.0), 2.0, 25.0),
        ("radial transverse stable", regular,
         inside_point(regular, inward=0.025, transverse=radial_offset),
         stable_transverse_seed(regular, offset=radial_offset), 1.0, 30.0),
        ("radial cubic-degenerate", degenerate, inside_point(degenerate, inward=0.18), (0.0, 0.0), 1.0, 20000.0),
        ("v_s close to one", close_to_one, inside_point(close_to_one, inward=0.03), (0.0, 0.0), 1.0, 100.0),
        ("ellipsoid axial", ellipsoid, inside_point(ellipsoid, inward=0.08), (0.0, 0.0), 1.0, 35.0),
        ("ellipsoid transverse stable", ellipsoid,
         inside_point(ellipsoid, inward=0.02, transverse=ellipsoid_offset),
         stable_transverse_seed(ellipsoid, offset=ellipsoid_offset), 1.0, 40.0),
        ("past via reflected shift", mirror, inside_point(mirror, generator_index=1, inward=0.08), (0.0, 0.0), 1.0, 35.0),
        ("disconnected wall component", multi, inside_point(multi, generator_index=0, inward=0.05), (0.0, 0.0), 1.0, 30.0),
    ]

    print("CAPTURE CANDIDATES")
    capture_results = []
    for case in capture_cases:
        name, profile, point, c, energy, end_time = case
        result = integrate_positive(profile, point, c, energy, end_time)
        capture_results.append((name, result))
        print_result(name, result, (
            "v+1", "dir_error", "distance_G", "logP", "tau_second_half", "energy_rel_drift"
        ))

    print("\nNONCAPTURE SIGN CHECKS")
    sign_cases = [
        ("P=0 with transverse Q", regular, np.array([0.0, 0.1, 0.0]), 0.0, (0.3, -0.2)),
        ("P<0 from bubble interior", regular, np.array([0.0, 0.0, 0.0]), -1.0, (0.0, 0.0)),
        ("P<0 near front wall", regular, inside_point(regular, inward=0.08), -8.0, (1.0, -0.5)),
    ]
    sign_results = []
    for name, profile, point, p_x, q in sign_cases:
        result = integrate_nonpositive(profile, point, p_x, q)
        sign_results.append((name, result))
        print_result(name, result, ("P_sign_preserved", "tau", "mass_shell_abs", "spatial_radius_max"))

    # This is deliberately a coarse falsification threshold, not a theorem test.
    failures = []
    for name, result in capture_results:
        if result["energy_rel_drift"] > 5.0e-5:
            failures.append(f"{name}: energy drift")
        if "degenerate" not in name and (
            abs(result["v+1"]) > 2.0e-4 or result["dir_error"] > 2.0e-3
        ):
            failures.append(f"{name}: did not approach the capture limits")
    degenerate_result = dict(capture_results)["radial cubic-degenerate"]
    if abs(degenerate_result["v+1"]) > 2.0e-3 or degenerate_result["dir_error"] > 2.0e-3:
        failures.append("radial cubic-degenerate: did not approach the capture limits")
    for name, result in sign_results:
        if not result["P_sign_preserved"] or result["tau"] < 5.0:
            failures.append(f"{name}: nonpositive-P branch behaved like a finite-time exit")

    if failures:
        print("\nFALSIFICATION FLAGS")
        for failure in failures:
            print(" -", failure)
        raise SystemExit(1)
    print("\nNo contradiction was found in this bounded test matrix.")


if __name__ == "__main__":
    main()
