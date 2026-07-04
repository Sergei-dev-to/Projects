"""Counting/rate skeleton for a connector-mode evaporator.

No Hamiltonian is simulated here.  The purpose is to make the thermodynamic
requirements explicit:

  S_N comes from site + connector qudits;
  M_N is proportional to the number of sites;
  T_N = (dS/dM)^-1;
  heating after N -> N-1 depends on how much energy the emitted subsystem
  carries away;
  power acceleration depends on channel-count and thermal-filter exponents.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np


@dataclass
class Params:
    n_min: int = 4
    n_max: int = 64
    d_site: float = 2.0
    d_conn: float = 2.0
    mu: float = 1.0
    eta: float = 1.0
    p_area: float = 2.0
    q_temp: float = 3.0


def q_modes(n: np.ndarray, a: float = 1.0, b: float = 1.0) -> np.ndarray:
    return a * n + b * n * (n - 1) / 2.0


def entropy(n: np.ndarray, d_site: float, d_conn: float) -> np.ndarray:
    return n * np.log(d_site) + n * (n - 1) / 2.0 * np.log(d_conn)


def mass(n: np.ndarray, mu: float) -> np.ndarray:
    return mu * n


def temperature(n: np.ndarray, d_site: float, d_conn: float, mu: float) -> np.ndarray:
    # Treat n as continuous: S = n log ds + n(n-1)/2 log dc.
    dsdn = np.log(d_site) + (n - 0.5) * np.log(d_conn)
    dmdn = mu
    return dmdn / dsdn


def heating_margin(
    n: np.ndarray,
    d_site: float,
    d_conn: float,
    mu: float,
    eta: float,
) -> np.ndarray:
    # Emitted energy epsilon = eta T_N.  Core energy M_N = mu N.
    # Heat if epsilon/M_N < 1 - q_(N-1)/q_N, here q uses log-d weighted entropy.
    s_n = entropy(n, d_site, d_conn)
    s_prev = entropy(n - 1, d_site, d_conn)
    frac_entropy_loss = 1.0 - s_prev / s_n
    eps_frac = eta * temperature(n, d_site, d_conn, mu) / mass(n, mu)
    return frac_entropy_loss - eps_frac


def power(n: np.ndarray, params: Params) -> np.ndarray:
    t = temperature(n, params.d_site, params.d_conn, params.mu)
    gamma = n**params.p_area * t**params.q_temp
    eps = params.eta * t
    return gamma * eps


def summarize(params: Params) -> str:
    n = np.arange(params.n_min, params.n_max + 1, dtype=float)
    s = entropy(n, params.d_site, params.d_conn)
    m = mass(n, params.mu)
    t = temperature(n, params.d_site, params.d_conn, params.mu)
    margin = heating_margin(n, params.d_site, params.d_conn, params.mu, params.eta)
    pwr = power(n, params)

    # Evaporation goes from large N to small N. Acceleration means power rises
    # as N decreases, so P(n_min) > P(n_max).
    accel_ratio = pwr[0] / pwr[-1]
    s_m2_cv = np.std(s / (m * m)) / np.mean(s / (m * m))
    t_m_cv = np.std(t * m) / np.mean(t * m)

    lines = [
        "connector-mode skeleton",
        f"N range: {params.n_min}..{params.n_max}",
        f"d_site={params.d_site:g} d_conn={params.d_conn:g} mu={params.mu:g}",
        f"epsilon=eta*T eta={params.eta:g}",
        f"gamma ~ N^p T^q with p={params.p_area:g} q={params.q_temp:g}",
        "",
        f"S/M^2 relative variation={s_m2_cv:.3e}",
        f"T*M relative variation={t_m_cv:.3e}",
        f"heating_margin min={margin.min():.3e} max={margin.max():.3e}",
        f"heating holds for all N: {bool(np.all(margin > 0))}",
        f"power smallN/largeN={accel_ratio:.3f}",
        f"power accelerates as N shrinks: {bool(accel_ratio > 1.0)}",
        "",
        "sample rows: N S M T margin P",
    ]
    sample_ns = sorted(
        set(
            [
                params.n_min,
                params.n_min + 1,
                (params.n_min + params.n_max) // 2,
                params.n_max - 1,
                params.n_max,
            ]
        )
    )
    for ns in sample_ns:
        idx = int(ns - params.n_min)
        lines.append(
            f"{ns:3d} {s[idx]:9.3f} {m[idx]:7.3f} {t[idx]:9.5f} "
            f"{margin[idx]:9.5f} {pwr[idx]:11.5e}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=64)
    parser.add_argument("--d-site", type=float, default=2.0)
    parser.add_argument("--d-conn", type=float, default=2.0)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument("--p-area", type=float, default=2.0)
    parser.add_argument("--q-temp", type=float, default=3.0)
    args = parser.parse_args()
    params = Params(
        n_min=args.n_min,
        n_max=args.n_max,
        d_site=args.d_site,
        d_conn=args.d_conn,
        mu=args.mu,
        eta=args.eta,
        p_area=args.p_area,
        q_temp=args.q_temp,
    )
    print(summarize(params))


if __name__ == "__main__":
    main()
