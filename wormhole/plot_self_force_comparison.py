#!/usr/bin/env python3
"""Plot fixed-zero-flux self-force for Ellis and test wormhole profiles."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import scan_fixed_flux_self_force as scan


OUT = "fig_self_force_comparison.png"
OUT_PDF = "fig_self_force_comparison.pdf"


def mass_drop_profile(a: float = 1.0, length: float = 0.6, power: float = 2.0) -> scan.Profile:
    xmax = scan.L_DOMAIN
    x = np.linspace(0.0, xmax, 9001)

    def mass(xx: float) -> float:
        return 0.5 * a * np.exp(-((xx / length) ** power))

    def ode(xx: float, y: np.ndarray) -> list[float]:
        value = max(0.0, 1.0 - 2.0 * mass(xx) / y[0])
        return [np.sqrt(value)]

    sol = solve_ivp(ode, (0.0, xmax), [a], t_eval=x, rtol=1e-10, atol=1e-12)
    r = sol.y[0]

    def radius(l: np.ndarray) -> np.ndarray:
        return np.interp(np.abs(l), x, r)

    return scan.Profile(r"mass-drop $R^{(3)}\leq0$", radius)


def scan_forces(profile: scan.Profile, positions: np.ndarray) -> np.ndarray:
    rows = scan.scan_profile(profile, [float(x) for x in positions])
    return np.array([row[1] for row in rows])


def main() -> None:
    # Keep this modest; each point solves all radial modes.
    positions = np.array(
        [0.35, 0.45, 0.55, 0.68, 0.80, 0.95, 1.10, 1.30,
         1.60, 2.00, 2.40, 3.00, 3.50, 4.30, 5.20, 6.20]
    )

    ellis_exact = np.array([scan.ellis_exact_fixed_force(float(x)) for x in positions])
    profiles = [
        (scan.ellis(), "#1f77b4", "Ellis numerical"),
        (scan.fat_throat(amp=1.25, width=2.8), "#d95f02", "fat-flare test"),
        (mass_drop_profile(length=0.6, power=2.0), "#7570b3", r"mass-drop $R^{(3)}\leq0$"),
    ]

    results = []
    for profile, color, label in profiles:
        forces = scan_forces(profile, positions)
        results.append((forces, color, label))
        print(label)
        for x, force in zip(positions, forces):
            print(f"  l0/a={x:5.2f}  F={force:+.6e}")

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.6), constrained_layout=True)

    for ax in axes:
        ax.axhline(0.0, color="0.15", lw=1.0)
        ax.set_xlabel(r"charge position $l_0/a$")
        ax.grid(alpha=0.25)

    ax = axes[0]
    for forces, color, label in results:
        ax.plot(positions, forces, "o-", lw=1.7, ms=4.2, color=color, label=label)
    ax.plot(positions, ellis_exact, "--", lw=1.5, color="#1f77b4", alpha=0.7, label="Ellis exact")
    ax.set_ylabel(r"fixed-flux self-force $F a^2/e^2$")
    ax.set_title("linear scale")
    ax.set_xlim(0.25, 6.35)
    ax.set_ylim(-0.095, 0.285)
    ax.legend(frameon=False, fontsize=9)

    ax = axes[1]
    for forces, color, label in results:
        ax.plot(positions, forces, "o-", lw=1.7, ms=4.2, color=color, label=label)
    ax.plot(positions, ellis_exact, "--", lw=1.5, color="#1f77b4", alpha=0.7)
    ax.set_yscale("symlog", linthresh=1.0e-3, linscale=0.8)
    ax.set_ylabel(r"fixed-flux self-force $F a^2/e^2$ (symlog)")
    ax.set_title("symmetric-log force scale")
    ax.set_xlim(0.25, 6.35)

    fig.suptitle("Fixed-zero-flux self-force: Ellis versus test profiles", fontsize=13)
    fig.savefig(OUT, dpi=220)
    fig.savefig(OUT_PDF)
    print(f"wrote {OUT}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
