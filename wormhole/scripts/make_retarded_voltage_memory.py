#!/usr/bin/env python3
"""Causal toy model for propagation of the fixed-flux voltage memory.

The exact static Ellis-shell result gives the far-end voltage

    Phi_-(X) = q/a [pi/2 - arctan(X/a)].

Here we impose a prescribed inward shell motion X(t) and let the throat voltage
launch a retarded one-dimensional signal into the opposite end,

    Phi(t,x<0) = Phi_th(t + x)       with c=1.

This is not a transverse radiative Maxwell mode.  It is a visualization of the
causal voltage update/memory: a finite observer sees an electric transient, and
the time-integrated transient equals the late-time voltage shift.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


A = 1.0
Q = 1.0
XI = 8.0
XF = 1.5
T0 = 30.0
TAU = 26.0

OUT_PNG = Path("fig_retarded_voltage_memory.png")
OUT_PDF = Path("fig_retarded_voltage_memory.pdf")


def phi_minus(x_shell: np.ndarray | float) -> np.ndarray | float:
    return (Q / A) * (0.5 * np.pi - np.arctan(np.asarray(x_shell) / A))


def smoothstep(u: np.ndarray | float) -> np.ndarray | float:
    uu = np.clip(np.asarray(u), 0.0, 1.0)
    return uu * uu * (3.0 - 2.0 * uu)


def shell_position(t: np.ndarray | float) -> np.ndarray | float:
    s = smoothstep((np.asarray(t) - T0) / TAU)
    return XI + (XF - XI) * s


def throat_voltage(t: np.ndarray | float) -> np.ndarray | float:
    return phi_minus(shell_position(t))


def far_voltage(t: np.ndarray | float, x: np.ndarray | float) -> np.ndarray | float:
    """Retarded voltage in the opposite end, x <= 0."""
    return throat_voltage(np.asarray(t) + np.asarray(x))


def main() -> None:
    x = np.linspace(-80.0, 0.0, 1200)
    t = np.linspace(0.0, 130.0, 1600)
    tt, xx = np.meshgrid(t, x)
    phi = far_voltage(tt, xx)
    phi_i = float(phi_minus(XI))
    phi_f = float(phi_minus(XF))
    delta_phi = phi_f - phi_i

    obs_points = [-10.0, -30.0, -60.0]
    obs_colors = ["#6f5fb8", "#2b83ba", "#b33333"]
    obs_styles = ["-", "--", "-."]

    fig, axes = plt.subplots(2, 2, figsize=(11.7, 7.5), constrained_layout=True)

    ax = axes[0, 0]
    # Use a slightly wider display range than the actual memory step so the
    # final state is dark gray rather than saturated black.
    display_max = phi_f + 0.28
    levels = np.linspace(phi_i, display_max, 22)
    im = ax.contourf(t, x, phi, levels=levels, cmap="Greys", extend="both")
    ax.contour(
        t,
        x,
        phi,
        levels=np.linspace(phi_i, phi_f, 7),
        colors="0.25",
        linewidths=0.55,
    )
    for xobs, style in zip(obs_points, obs_styles):
        ax.axhline(xobs, color="0.1", lw=0.8, ls=style, alpha=0.65)
        ax.text(3.0, xobs + 1.5, rf"$x={xobs:g}a$", fontsize=8, color="0.15")
    ax.plot([T0, T0 - x[-1]], [0, x[-1]], color="0.1", lw=0.8, alpha=0.0)
    ax.set_xlabel(r"time $t/a$")
    ax.set_ylabel(r"opposite-end coordinate $x/a$")
    ax.set_title(r"retarded voltage update, $t+x={\rm const.}$")
    cbar = fig.colorbar(im, ax=ax, shrink=0.92)
    cbar.set_label(r"$\Phi(t,x)$")
    cbar.set_ticks([phi_i, 0.25, 0.40, phi_f])
    cbar.set_ticklabels(
        [rf"$\Phi_i={phi_i:.3f}$", "0.250", "0.400", rf"$\Phi_f={phi_f:.3f}$"]
    )

    ax = axes[0, 1]
    ax.plot(t, shell_position(t), color="0.15", lw=1.8)
    ax2 = ax.twinx()
    ax2.plot(t, throat_voltage(t), color="#c43c39", lw=1.8)
    ax.set_xlabel(r"time $t/a$")
    ax.set_ylabel(r"shell position $X(t)/a$", color="0.15")
    ax2.set_ylabel(r"$\Phi_-(X(t))$", color="#c43c39")
    ax.set_title("prescribed inward shell motion")
    ax.grid(alpha=0.22)

    ax = axes[1, 0]
    for xobs, color, style in zip(obs_points, obs_colors, obs_styles):
        ax.plot(
            t,
            far_voltage(t, xobs),
            color=color,
            lw=1.9,
            ls=style,
            label=rf"$x={xobs:g}a$",
        )
    ax.axhline(phi_i, color="0.35", lw=0.9, ls=":")
    ax.axhline(phi_f, color="0.35", lw=0.9, ls=":")
    ax.annotate(
        "",
        xy=(124.0, phi_i),
        xytext=(124.0, phi_f),
        arrowprops={"arrowstyle": "<->", "lw": 1.1, "color": "0.15"},
    )
    ax.text(
        118.0,
        0.36,
        rf"$\Delta\Phi={delta_phi:.3f}$",
        ha="center",
        va="center",
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.75, "edgecolor": "none", "pad": 2},
    )
    ax.set_xlabel(r"time $t/a$")
    ax.set_ylabel(r"observed voltage $\Phi(t,x_{\rm obs})$")
    ax.set_title("finite observers see delayed memory")
    ax.text(4.0, phi_i + 0.008, "initial", fontsize=8, color="0.25")
    ax.text(4.0, phi_f - 0.018, "final", fontsize=8, color="0.25")
    ax.legend(frameon=False, fontsize=8, loc="center left")
    ax.grid(alpha=0.22)

    ax = axes[1, 1]
    # E_x = -dPhi/dx = -dPhi_th/dt_ret in this retarded model, so -E_x
    # has positive area equal to the voltage memory Delta Phi.
    dphi_dt = np.gradient(throat_voltage(t), t)
    for xobs, color, style in zip(obs_points, obs_colors, obs_styles):
        minus_e_obs = np.interp(t + xobs, t, dphi_dt, left=0.0, right=0.0)
        ax.plot(t, minus_e_obs, color=color, lw=1.9, ls=style, label=rf"$x={xobs:g}a$")
    ax.set_xlabel(r"time $t/a$")
    ax.set_ylabel("voltage-update pulse")
    ax.set_title(r"pulse area gives $\Delta\Phi$")
    ax.text(
        0.04,
        0.90,
        r"$\int (-E_x)\,dt=\Delta\Phi$",
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "alpha": 0.8, "edgecolor": "none", "pad": 3},
    )
    ax.grid(alpha=0.22)

    fig.suptitle(
        r"Ellis shell memory as a causal voltage update: "
        + rf"$\Phi_i={phi_i:.3f}$, $\Phi_f={phi_f:.3f}$",
        fontsize=12,
    )
    fig.savefig(OUT_PNG, dpi=210)
    fig.savefig(OUT_PDF)

    print(f"Phi_i={phi_i:.8f}")
    print(f"Phi_f={phi_f:.8f}")
    print(f"Delta Phi={delta_phi:.8f}")
    print(f"wrote {OUT_PNG}")
    print(f"wrote {OUT_PDF}")


if __name__ == "__main__":
    main()
