"""Exact first-stage scalar transmission calculation at a planar cap.

The solved global problem is a massless scalar in 1+1 dimensions with no
reflecting boundary. It is NOT a computation of the four-dimensional RSET.
See notes/cap_scalar_transmission.md for assumptions and limitations.
Run from any directory; results go to output/cap_scalar_transmission/.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from scipy.integrate import quad


def schwarzian(f, x):
    return sp.simplify(sp.diff(f, x, 3) / sp.diff(f, x)
                       - sp.Rational(3, 2) * (sp.diff(f, x, 2) / sp.diff(f, x))**2)


def symbolic_checks():
    q, p, kappa, c, temperature = sp.symbols("q p kappa c T", positive=True)
    w = -sp.log(q) / kappa
    sw = schwarzian(w, q)
    vacuum = sp.simplify(-sw / (24 * sp.pi))
    thermal = sp.simplify(vacuum + sp.pi * temperature**2 / (12 * kappa**2 * q**2))
    assert sp.simplify(sw - 1 / (2 * q**2)) == 0
    assert sp.simplify(vacuum + 1 / (48 * sp.pi * q**2)) == 0
    assert sp.simplify(thermal.subs(temperature, kappa / (2 * sp.pi))) == 0

    # An independent point-splitting check, with Minkowski subtraction.
    eps = sp.symbols("eps", positive=True)
    transformed = sp.diff(w, q) * sp.diff(w, q).subs(q, q + eps)
    transformed /= (w - w.subs(q, q + eps))**2
    finite = sp.simplify(sp.limit(transformed - eps**-2, eps, 0))
    assert sp.simplify(-finite / (4 * sp.pi) - vacuum) == 0

    # For the flat germ, pq=-c*s and C=(1-v^2)/(kappa^2*pq).
    s = sp.symbols("s", real=True)
    v_squared = 1 + 2 * kappa * s
    coefficient = sp.simplify((1 - v_squared) / (-c * kappa**2 * s))
    assert sp.simplify(coefficient - 2 / (c * kappa)) == 0

    # Smooth nonzero transverse modes solve the full local 4D wave equation.
    A, B, y, z, a, b, ky, kz = sp.symbols("A B y z a b ky kz", real=True)
    phi = sp.cos(a*A + b*B + ky*y + kz*z)
    box_phi = -2*sp.diff(phi, A, B) + sp.diff(phi, y, 2) + sp.diff(phi, z, 2)
    assert sp.simplify(box_phi - (2*a*b - ky**2 - kz**2)*phi) == 0

    return {"schwarzian_w_of_q": str(sw), "vacuum_Tqq": str(vacuum),
            "thermal_Tqq": str(thermal), "point_split_finite_part": str(finite),
            "flat_cap_C": str(coefficient), "nonzero_transverse_mode_check": "passed"}


def compact_initial_data_check():
    # The paper's reduced sech profile; v=-1 at +/-acosh(2), kappa=sqrt(3)/2.
    radius = 0.6
    def v(x):
        return 2 / np.cosh(x) - 2
    def h(x):
        return np.exp(-1 / (1 - (x/radius)**2)) if abs(x) < radius else 0.0
    def hx(x):
        return h(x)*(-2*x/radius**2)/(1-(x/radius)**2)**2 if abs(x) < radius else 0.0
    def pi(x):
        return 0.7*h(x)
    def w0(x):
        return quad(lambda s: 1/(1-v(s)), 0, x, epsabs=1e-12)[0]

    errors = []
    for x in np.linspace(-1, 1, 201):
        # F'=df/du, G'=dg/dw reconstructed from arbitrary Cauchy data.
        Gp = (1-v(x))/2*(pi(x)+(v(x)+1)*hx(x))
        Fp = pi(x)-Gp
        errors.extend([abs(Fp+Gp-pi(x)),
                       abs(-Fp/(v(x)+1)-Gp/(v(x)-1)-hx(x))])
    cutoff = w0(radius)
    # At t=0, w0 is a global diffeomorphism. Compact data => G' compact in w.
    for x in [radius+0.1, 2, 8, 30]:
        assert (1-v(x))/2*(pi(x)+(v(x)+1)*hx(x)) == 0
    assert max(errors) < 1e-12
    return {"max_initial_data_reconstruction_error": max(errors),
            "incoming_derivative_support_w": [w0(-radius), cutoff],
            "kappa": np.sqrt(3)/2,
            "q_below_which_incoming_classical_stress_is_exactly_zero":
                float(np.exp(-np.sqrt(3)/2*cutoff))}


def tail_and_state_checks(out):
    # kappa=1. w=-log(q), and Tqq_classical=(G'(w)/(kappa*q))^2.
    w = np.linspace(0, 24, 961)
    slopes = {}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.1))
    for alpha in [0.5, 1, 1.5]:
        stress = np.exp(2*(1-alpha)*w)
        slope = float(np.polyfit(w, np.log(stress), 1)[0])
        assert abs(slope-2*(1-alpha)) < 1e-12
        slopes[str(alpha)] = slope
        axes[0].semilogy(w, stress, label=rf"$\alpha/\kappa={alpha}$")
    compact = np.zeros_like(w)
    inside = abs(w-3) < 2
    compact[inside] = np.exp(-2/(1-((w[inside]-3)/2)**2)+2*w[inside])
    axes[0].semilogy(w, np.maximum(compact, 1e-12), color="black", ls="--",
                     label="compact pulse (zero after cutoff)")
    axes[0].set(xlabel=r"$\kappa w$", ylabel=r"classical $T_{qq}$ (chosen units)",
                title="Incoming classical tail, open passage", ylim=(1e-11, 1e11))
    axes[0].legend(fontsize=8)

    # Plot q^2 Tqq rather than enormous raw stresses; this exposes cancellation.
    temperatures = np.linspace(0, 1.6, 201)  # T/T_H
    coefficient = (temperatures**2-1)/(48*np.pi)
    axes[1].plot(temperatures, coefficient)
    axes[1].axhline(0, color="gray", lw=0.7)
    axes[1].axvline(1, color="gray", lw=0.7, ls="--")
    axes[1].set(xlabel=r"incoming temperature $T/T_H$",
                ylabel=r"$q^2\langle T_{qq}\rangle$",
                title="2D quantum field: stationary incoming states")
    fig.suptitle("Planar-cap calculation: solved reduced sector, not a 4D stability result", fontsize=11)
    fig.tight_layout()
    fig.savefig(out / "transmission_checks.png", dpi=180)
    plt.close(fig)
    return {"classical_log_stress_slopes_kappa_1": slopes,
            "quantum_cancellation_T_over_TH": 1.0,
            "small_temperature_mismatch": "residual coefficient (2*epsilon+epsilon**2)/(48*pi)"}


def main():
    out = Path(__file__).resolve().parents[1] / "output" / "cap_scalar_transmission"
    out.mkdir(parents=True, exist_ok=True)
    result = {"scope": "exact 1+1 massless scalar; local 4D regularity checks only",
              "symbolic": symbolic_checks(),
              "compact_cauchy_data": compact_initial_data_check()}
    result["tails_and_states"] = tail_and_state_checks(out)
    (out / "checks.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
