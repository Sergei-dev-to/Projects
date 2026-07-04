"""Compressed many-cycle tracker for the edge-tension evaporator.

This is not a dense state-vector simulation.  It tracks the full evaporation
trajectory using the analytical finite-gauge state count and the golden-rule
microscopic emission schedule.

For each shell L:

    M_L = 4 sigma L
    S_L = L^2 log q
    Delta M = 4 sigma
    Delta S = (2L - 1) log q

Microscopic emissions are generated from the current mass using the same
golden-rule bin weights as the emission-block diagnostics.  Emissions continue
until the shell gap Delta M has been radiated, then the coarse update

    H_L -> H_(L-1) tensor H_shell

is applied at the capacity-bookkeeping level.

The Page-style entropy estimate is not a proof of scrambling dynamics.  It is
the random/typical capacity estimate:

    S_Page ~ min(S_remaining_internal, S_external_records).
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import numpy as np

from microscopic_boundary_emission import golden_rule_hard_distribution


def shannon_entropy(probs: np.ndarray, tol: float = 1e-15) -> float:
    probs = probs[probs > tol]
    return float(-np.sum(probs * np.log(probs)))


def shell_entropy(L: int, q: int) -> float:
    return L * L * math.log(q)


def shell_mass(L: int, sigma: float) -> float:
    return 4.0 * sigma * L


def shell_temperature(L: int, q: int, sigma: float) -> float:
    beta = shell_mass(L, sigma) * math.log(q) / (8.0 * sigma**2)
    return 1.0 / beta


def normalized_cycle_time(m_start: float, m_end: float, bath_dim: int) -> float:
    """Time for dM/dt = - M^(-bath_dim), in arbitrary units."""
    return (m_start ** (bath_dim + 1) - m_end ** (bath_dim + 1)) / (bath_dim + 1)


def track_many_cycles(
    L0: int,
    q: int,
    sigma: float,
    bath_dim: int,
    x_edges: np.ndarray,
    n_grid: int,
    max_events_per_shell: int,
) -> tuple[list[dict[str, float | int]], dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    S0 = shell_entropy(L0, q)
    cumulative_hard_entropy = 0.0
    cumulative_emissions = 0
    cumulative_time = 0.0
    page_peak_entropy = -1.0
    page_peak_L = L0
    page_cross_L = -1

    for L in range(L0, 1, -1):
        m_start = shell_mass(L, sigma)
        m_target = shell_mass(L - 1, sigma) if L > 1 else 0.0
        delta_m = m_start - m_target
        mass = m_start
        emitted = 0.0
        hard_entropy_this_shell = 0.0
        events = 0
        first_mean_omega = 0.0
        first_temperature = shell_temperature(L, q, sigma)
        first_p_last = 0.0

        while emitted < delta_m and events < max_events_per_shell and mass > 1e-12:
            probs, mean_omega, temp = golden_rule_hard_distribution(
                mass,
                q,
                sigma,
                bath_dim,
                x_edges,
                n_grid,
            )
            if events == 0:
                first_mean_omega = mean_omega
                first_temperature = temp
                first_p_last = float(probs[-1])
            hard_entropy_this_shell += shannon_entropy(probs)
            emitted += mean_omega
            mass = max(0.0, mass - mean_omega)
            events += 1

        cumulative_emissions += events
        cumulative_hard_entropy += hard_entropy_this_shell
        cumulative_time += normalized_cycle_time(m_start, m_target, bath_dim)

        S_before = shell_entropy(L, q)
        S_after = shell_entropy(L - 1, q)
        delta_S = S_before - S_after
        external_capacity = S0 - S_after
        page_estimate = min(S_after, external_capacity)
        if page_estimate > page_peak_entropy:
            page_peak_entropy = page_estimate
            page_peak_L = L - 1
        if page_cross_L < 0 and external_capacity >= S_after:
            page_cross_L = L - 1

        rows.append(
            {
                "cycle": L0 - L + 1,
                "L_before": L,
                "L_after": L - 1,
                "M_start": m_start,
                "M_target": m_target,
                "T_start": shell_temperature(L, q, sigma),
                "S_before": S_before,
                "S_after": S_after,
                "Delta_S_shell": delta_S,
                "Delta_M": delta_m,
                "events_this_shell": events,
                "cumulative_emissions": cumulative_emissions,
                "first_mean_omega": first_mean_omega,
                "first_temperature": first_temperature,
                "first_omega_over_T": first_mean_omega / first_temperature if first_temperature > 0 else 0.0,
                "first_p_last": first_p_last,
                "emitted_energy": emitted,
                "emitted_over_Delta_M": emitted / delta_m if delta_m > 0 else 0.0,
                "hard_entropy_this_shell": hard_entropy_this_shell,
                "cumulative_hard_entropy": cumulative_hard_entropy,
                "external_record_capacity": external_capacity,
                "page_entropy_estimate": page_estimate,
                "normalized_cycle_time": normalized_cycle_time(m_start, m_target, bath_dim),
                "cumulative_time": cumulative_time,
            }
        )

    summary = {
        "L0": L0,
        "q": q,
        "sigma": sigma,
        "bath_dim": bath_dim,
        "S0": S0,
        "M0": shell_mass(L0, sigma),
        "total_emissions": cumulative_emissions,
        "total_hard_entropy": cumulative_hard_entropy,
        "total_normalized_time": cumulative_time,
        "lifetime_over_M0_power": cumulative_time / (shell_mass(L0, sigma) ** (bath_dim + 1)),
        "page_peak_entropy": page_peak_entropy,
        "page_peak_L_after": page_peak_L,
        "page_cross_L_after": page_cross_L,
        "page_cross_fraction_evaporated": (L0 - page_cross_L) / L0 if page_cross_L >= 0 else -1.0,
    }
    return rows, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L0", type=int, default=40)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--x-edges", nargs="+", type=float, default=[0.0, 2.0, 8.0])
    parser.add_argument("--n-grid", type=int, default=1001)
    parser.add_argument("--max-events-per-shell", type=int, default=10000)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/many_cycle_evaporation_tracker.csv"),
    )
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/many_cycle_evaporation_tracker_summary.csv"),
    )
    args = parser.parse_args()

    rows, summary = track_many_cycles(
        args.L0,
        args.q,
        args.sigma,
        args.bath_dim,
        np.array(args.x_edges, dtype=float),
        args.n_grid,
        args.max_events_per_shell,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print(
        f"L0={args.L0}, total emissions={summary['total_emissions']}, "
        f"page cross L={summary['page_cross_L_after']}, "
        f"page fraction evaporated={summary['page_cross_fraction_evaporated']:.3f}"
    )
    print(
        f"normalized lifetime={summary['total_normalized_time']:.3f}, "
        f"lifetime/M0^(d+1)={summary['lifetime_over_M0_power']:.6f}"
    )
    print()
    print("cycle L->L' events T_start first_w/T ext_cap page_est")
    sample_indices = sorted(set([0, 1, 2, len(rows) // 2, len(rows) - 3, len(rows) - 2, len(rows) - 1]))
    for idx in sample_indices:
        row = rows[idx]
        print(
            f"{row['cycle']:5d} "
            f"{row['L_before']:2d}->{row['L_after']:2d} "
            f"{row['events_this_shell']:6d} "
            f"{row['T_start']:8.4f} "
            f"{row['first_omega_over_T']:9.3f} "
            f"{row['external_record_capacity']:8.3f} "
            f"{row['page_entropy_estimate']:8.3f}"
        )


if __name__ == "__main__":
    main()
