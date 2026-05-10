#!/usr/bin/env python3
"""Compare Ellis and deformed spherical wormhole profiles."""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import scan_fixed_flux_self_force as scan


OUT = "fig_profile_comparison.png"
OUT_PDF = "fig_profile_comparison.pdf"
OUT_MASS = "fig_profile_comparison_massdrop.png"
OUT_MASS_PDF = "fig_profile_comparison_massdrop.pdf"


def diagnostics(profile: scan.Profile, l: np.ndarray) -> tuple[np.ndarray, ...]:
    r = profile.radius(l)
    h = l[1] - l[0]
    rp = np.gradient(r, h, edge_order=2)
    rpp = np.gradient(rp, h, edge_order=2)
    theta = 2.0 * rp / r
    scalar_r = -4.0 * rpp / r + 2.0 * (1.0 - rp * rp) / (r * r)
    hawking_m = 0.5 * r * (1.0 - rp * rp)
    return r, theta, scalar_r, hawking_m


def mass_drop_profile(a: float = 1.0, length: float = 0.6, power: float = 2.0) -> scan.Profile:
    """Build r(l) from a monotone decreasing Hawking mass.

    m(l)=a/2 exp[-(l/length)^power] gives R^(3)<=0 for l>0 where r'>0.
    The throat has r(0)=a and r'(0)=0.
    """
    xmax = 45.0
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


def make_plot(profile: scan.Profile, out_png: str, out_pdf: str, title: str) -> None:
    ellis = scan.ellis()
    l = np.linspace(-7.0, 7.0, 1801)

    er, etheta, ecurv, emass = diagnostics(ellis, l)
    fr, ftheta, fcurv, fmass = diagnostics(profile, l)

    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.2), constrained_layout=True)

    ax = axes[0, 0]
    ax.plot(l, er, lw=2.2, label="Ellis")
    ax.plot(l, fr, lw=2.2, label=profile.name)
    ax.set_ylabel(r"areal radius $r(l)$")
    ax.set_xlabel(r"proper radial coordinate $l/a$")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25)

    ax = axes[0, 1]
    ax.plot(l, fr - er, lw=2.2, color="#b45309")
    ax.axhline(0.0, color="0.25", lw=0.9)
    ax.set_ylabel(r"$r_{\rm test}(l)-r_{\rm Ellis}(l)$")
    ax.set_xlabel(r"$l/a$")
    ax.grid(alpha=0.25)

    ax = axes[1, 0]
    ax.plot(l, etheta, lw=2.2, label="Ellis")
    ax.plot(l, ftheta, lw=2.2, label=profile.name)
    ax.axhline(0.0, color="0.25", lw=0.9)
    ax.set_ylabel(r"area expansion $\Theta=2r'/r$")
    ax.set_xlabel(r"$l/a$")
    ax.grid(alpha=0.25)

    ax = axes[1, 1]
    ax.plot(l, ecurv, lw=2.2, label="Ellis")
    ax.plot(l, fcurv, lw=2.2, label=profile.name)
    ax.axhline(0.0, color="0.25", lw=0.9)
    ax.set_ylabel(r"spatial scalar curvature ${}^{(3)}R$")
    ax.set_xlabel(r"$l/a$")
    ax.grid(alpha=0.25)

    fig.suptitle(title, fontsize=13)
    fig.savefig(out_png, dpi=220)
    fig.savefig(out_pdf)
    print(f"wrote {out_png}")
    print(f"wrote {out_pdf}")


def main() -> None:
    make_plot(
        scan.fat_throat(amp=1.25, width=2.8),
        OUT,
        OUT_PDF,
        "Ellis profile versus a fixed-flux attractive fat-flare profile",
    )
    make_plot(
        mass_drop_profile(length=0.6, power=2.0),
        OUT_MASS,
        OUT_MASS_PDF,
        r"Ellis profile versus a fixed-flux attractive $R^{(3)}\leq0$ profile",
    )


if __name__ == "__main__":
    main()
