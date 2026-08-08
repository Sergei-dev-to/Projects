#!/usr/bin/env python3
"""Voltage memory and dipole transients in an ultrastatic Ellis wormhole.

This is a scratch calculation, not part of the manuscript build.

Part 1 computes the exact fixed-flux l=0 voltage memory for a spherical
charged shell moved quasistatically in the x>0 end of

    ds^2 = -dt^2 + dx^2 + (x^2+a^2)dOmega^2.

Part 2 evolves the leading radiative l=1 master equation

    psi_tt = psi_xx - 2/(x^2+a^2) psi + S(t,x)

with a compact dipole-like source in the x>0 end.  This shows the causal
transient crossing the throat; it is complementary to the l=0 memory, not the
same mode.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


A = 1.0
Q = 1.0

OUT_MEMORY = Path("fig_ellis_voltage_memory.png")
OUT_TRANSIENT = Path("fig_ellis_dipole_transient.png")


def phi_minus(x_shell: np.ndarray | float, a: float = A, q: float = Q) -> np.ndarray | float:
    """Far-end uniform potential in the fixed zero-through-flux sector."""
    return (q / a) * (0.5 * np.pi - np.arctan(np.asarray(x_shell) / a))


def make_memory_plot() -> None:
    xi = 8.0
    xf = 1.5
    xs = np.linspace(0.4, 10.0, 700)
    phis = phi_minus(xs)
    delta = float(phi_minus(xf) - phi_minus(xi))

    profile_x = np.linspace(-14.0, 14.0, 1401)

    def fixed_flux_phi_profile(x_shell: float) -> np.ndarray:
        """Static potential profile with Phi(+infty)=0 and zero left flux."""
        out = np.empty_like(profile_x)
        left = profile_x <= x_shell
        out[left] = phi_minus(x_shell)
        out[~left] = phi_minus(profile_x[~left])
        return out

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.2), constrained_layout=True)

    ax = axes[0]
    ax.plot(xs, phis, color="#1f77b4", lw=2.0)
    ax.scatter([xi, xf], [phi_minus(xi), phi_minus(xf)], color="#c43c39", zorder=3)
    ax.annotate("initial", (xi, phi_minus(xi)), xytext=(6.5, 0.26),
                arrowprops={"arrowstyle": "->", "lw": 1.0}, fontsize=9)
    ax.annotate("final", (xf, phi_minus(xf)), xytext=(2.5, 0.85),
                arrowprops={"arrowstyle": "->", "lw": 1.0}, fontsize=9)
    ax.set_xlabel(r"shell position $X/a$")
    ax.set_ylabel(r"far-end voltage $\Phi_-$")
    ax.set_title(r"fixed-flux $\ell=0$ memory")
    ax.grid(alpha=0.25)

    ax = axes[1]
    ax.plot(profile_x, fixed_flux_phi_profile(xi), color="#7570b3", lw=1.8,
            label=rf"initial shell at $X={xi:g}a$")
    ax.plot(profile_x, fixed_flux_phi_profile(xf), color="#1f77b4", lw=2.0,
            label=rf"final shell at $X={xf:g}a$")
    ax.axvline(0.0, color="0.2", lw=1.0, alpha=0.55, label="throat")
    ax.axvline(xi, color="#7570b3", lw=1.0, ls="--", alpha=0.8)
    ax.axvline(xf, color="#1f77b4", lw=1.0, ls="--", alpha=0.8)
    ax.annotate(r"$\Delta\Phi_-$", xy=(-9.0, phi_minus(xi)),
                xytext=(-9.0, phi_minus(xf)),
                arrowprops={"arrowstyle": "<->", "lw": 1.2, "color": "#c43c39"},
                color="#c43c39", ha="center", va="center")
    ax.set_xlabel(r"wormhole coordinate $x/a$")
    ax.set_ylabel(r"static potential $\Phi(x)$")
    ax.set_title(rf"same left flux, different far-end voltage: $\Delta\Phi_-={delta:.3f}$")
    ax.grid(alpha=0.25)
    ax.set_xlim(-12.0, 12.0)
    ax.legend(frameon=False, fontsize=8, loc="upper right")

    fig.savefig(OUT_MEMORY, dpi=180)
    print(f"wrote {OUT_MEMORY}")
    print(f"fixed-flux memory: Phi_-(Xi={xi})={float(phi_minus(xi)):.8f}")
    print(f"fixed-flux memory: Phi_-(Xf={xf})={float(phi_minus(xf)):.8f}")
    print(f"fixed-flux memory: Delta Phi={delta:.8f}")


def evolve_dipole_transient() -> None:
    # Domain and stable second-order finite-difference evolution.
    x_max = 90.0
    dx = 0.05
    dt = 0.025
    t_max = 145.0
    x = np.arange(-x_max, x_max + dx, dx)
    n = x.size
    nt = int(t_max / dt)

    potential = 2.0 / (x * x + A * A)

    # Source: localized in the x>0 end and compact-ish in time.
    x0 = 14.0
    sigma_x = 0.35
    t0 = 20.0
    sigma_t = 2.5
    amp = 0.16
    source_x = np.exp(-0.5 * ((x - x0) / sigma_x) ** 2)
    source_x /= np.trapezoid(source_x, x)

    # Sponge layer to reduce reflections from numerical boundaries.
    sponge_start = 70.0
    sponge = np.zeros_like(x)
    mask = np.abs(x) > sponge_start
    sponge[mask] = 0.030 * ((np.abs(x[mask]) - sponge_start) / (x_max - sponge_start)) ** 2

    psi_prev = np.zeros(n)
    psi = np.zeros(n)
    psi_next = np.zeros(n)

    snapshots_at = [35.0, 55.0, 75.0, 95.0, 115.0]
    snapshots: list[tuple[float, np.ndarray]] = []
    obs_left = int(np.argmin(np.abs(x + 45.0)))
    obs_right = int(np.argmin(np.abs(x - 45.0)))
    trace_stride = 4
    trace_t: list[float] = []
    trace_left: list[float] = []
    trace_right: list[float] = []
    energy_t: list[float] = []
    energy_val: list[float] = []

    snap_index = 0
    cfl2 = (dt / dx) ** 2
    for step in range(nt):
        now = step * dt
        source_t = amp * np.exp(-0.5 * ((now - t0) / sigma_t) ** 2)
        source = source_t * source_x

        lap = np.zeros_like(psi)
        lap[1:-1] = psi[2:] - 2.0 * psi[1:-1] + psi[:-2]
        psi_next[1:-1] = (
            2.0 * psi[1:-1]
            - psi_prev[1:-1]
            + cfl2 * lap[1:-1]
            - dt * dt * potential[1:-1] * psi[1:-1]
            + dt * dt * source[1:-1]
        )

        # Simple damping in sponge regions.
        damp = np.exp(-sponge * dt)
        psi_next *= damp
        psi_next[0] = 0.0
        psi_next[-1] = 0.0

        if step % trace_stride == 0:
            trace_t.append(now)
            trace_left.append(float(psi[obs_left]))
            trace_right.append(float(psi[obs_right]))
            pi = (psi - psi_prev) / dt
            grad = np.zeros_like(psi)
            grad[1:-1] = (psi[2:] - psi[:-2]) / (2.0 * dx)
            energy = 0.5 * np.trapezoid(pi * pi + grad * grad + potential * psi * psi, x)
            energy_t.append(now)
            energy_val.append(float(energy))

        if snap_index < len(snapshots_at) and now >= snapshots_at[snap_index]:
            snapshots.append((now, psi.copy()))
            snap_index += 1

        psi_prev, psi, psi_next = psi, psi_next, psi_prev

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 7.4), constrained_layout=True)

    ax = axes[0]
    offsets = np.linspace(0.0, 0.20, len(snapshots))
    for offset, (ts, snap) in zip(offsets, snapshots):
        ax.plot(x, snap + offset, lw=1.3, label=rf"$t={ts:.0f}$")
    ax.axvline(0.0, color="0.2", lw=1.0, alpha=0.6)
    ax.axvline(x0, color="#c43c39", lw=1.0, ls="--", alpha=0.75)
    ax.set_xlim(-65.0, 55.0)
    ax.set_xlabel(r"wormhole coordinate $x/a$")
    ax.set_ylabel(r"$\psi_1$ snapshots, offset")
    ax.set_title(r"dipole transient through $V_1(x)=2/(x^2+a^2)$")
    ax.legend(frameon=False, ncol=5, fontsize=8)
    ax.grid(alpha=0.22)

    ax = axes[1]
    ax.plot(trace_t, trace_right, color="#d95f02", lw=1.2, label=r"source-side observer $x=45a$")
    ax.plot(trace_t, trace_left, color="#1f77b4", lw=1.5, label=r"far-side observer $x=-45a$")
    ax2 = ax.twinx()
    ax2.plot(energy_t, energy_val, color="0.35", lw=1.0, alpha=0.55, label="field energy")
    ax.set_xlabel(r"time $t/a$")
    ax.set_ylabel(r"$\psi_1(t,x_{\rm obs})$")
    ax2.set_ylabel("energy proxy")
    ax.set_title("causal arrival and decay of the radiative sector")
    ax.grid(alpha=0.22)
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines + lines2, labels + labels2, frameon=False, loc="upper right")

    fig.savefig(OUT_TRANSIENT, dpi=180)
    print(f"wrote {OUT_TRANSIENT}")
    print(f"far-side peak |psi|={max(abs(v) for v in trace_left):.8e}")
    print(f"source-side peak |psi|={max(abs(v) for v in trace_right):.8e}")


def main() -> None:
    make_memory_plot()
    evolve_dipole_transient()


if __name__ == "__main__":
    main()
