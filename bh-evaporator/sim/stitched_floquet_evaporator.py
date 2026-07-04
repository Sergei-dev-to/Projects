from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StitchedCycleRow:
    cycle: int
    L_before: int
    L_after: int
    emissions_this_shell: int
    emitted_energy_this_shell: float
    shell_gap: float
    M_before: float
    T_before: float
    first_omega_over_T: float
    internal_entropy_after: float
    external_capacity_after: float
    page_estimate_after: float
    normalized_time_after: float
    f14_module: str


@dataclass(frozen=True)
class StitchedSummary:
    L0: int
    q: int
    sigma: float
    bath_dim: int
    total_shell_cycles: int
    total_micro_emissions: int
    final_external_capacity: float
    page_cross_L: int
    page_fraction_evaporated: float
    normalized_lifetime: float
    lifetime_scaled: float
    f15_status: str


def entropy_L(L: int, q: int) -> float:
    return L * L * math.log(q)


def mass_L(L: int, sigma: float) -> float:
    return 4.0 * sigma * L


def temperature_L(L: int, q: int, sigma: float) -> float:
    return 2.0 * sigma / (L * math.log(q))


def golden_rule_bins(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    bin_count: int = 64,
) -> list[tuple[float, float]]:
    m = mass_L(L, sigma)
    t = temperature_L(L, q, sigma)
    max_omega = min(m, 12.0 * t)
    if max_omega <= 0.0:
        return [(0.0, 1.0)]

    weights: list[tuple[float, float]] = []
    for idx in range(bin_count):
        omega = max_omega * (idx + 0.5) / bin_count
        m_after = max(0.0, m - omega)
        l_after = m_after / (4.0 * sigma)
        delta_s = (l_after * l_after - L * L) * math.log(q)
        phase_space = omega ** max(0, bath_dim - 1)
        weights.append((omega, phase_space * math.exp(delta_s)))

    total = sum(weight for _, weight in weights)
    if total == 0.0:
        return [(max_omega / 2.0, 1.0)]
    return [(omega, weight / total) for omega, weight in weights]


def deterministic_quantile_sample(distribution: list[tuple[float, float]], index: int) -> float:
    """Low-discrepancy deterministic sample from a discrete distribution."""

    q = (index * 0.6180339887498949) % 1.0
    total = 0.0
    for omega, prob in distribution:
        total += prob
        if q <= total:
            return omega
    return distribution[-1][0]


def run_stitched_evaporator(
    L0: int = 40,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
) -> tuple[list[StitchedCycleRow], StitchedSummary]:
    rows: list[StitchedCycleRow] = []
    external_capacity = 0.0
    normalized_time = 0.0
    total_micro_emissions = 0
    total_entropy = entropy_L(L0, q)
    page_cross_L = -1

    for cycle, L in enumerate(range(L0, 1, -1), start=1):
        shell_gap = mass_L(L, sigma) - mass_L(L - 1, sigma)
        distribution = golden_rule_bins(L, q, sigma, bath_dim)
        emitted = 0.0
        emissions = 0
        first_omega = None

        while emitted < shell_gap:
            omega = deterministic_quantile_sample(distribution, total_micro_emissions + 1)
            if first_omega is None:
                first_omega = omega
            emitted += omega
            emissions += 1
            total_micro_emissions += 1

        shell_capacity = entropy_L(L, q) - entropy_L(L - 1, q)
        external_capacity += shell_capacity
        internal_after = entropy_L(L - 1, q)
        page_estimate = min(internal_after, external_capacity)
        rad_fraction = external_capacity / total_entropy
        if page_cross_L < 0 and external_capacity >= internal_after:
            page_cross_L = L - 1

        m_before = mass_L(L, sigma)
        # Normalized continuum time from dM/dt = -M^-bath_dim.
        normalized_time += (
            mass_L(L, sigma) ** (bath_dim + 1)
            - mass_L(L - 1, sigma) ** (bath_dim + 1)
        ) / (bath_dim + 1)

        rows.append(
            StitchedCycleRow(
                cycle=cycle,
                L_before=L,
                L_after=L - 1,
                emissions_this_shell=emissions,
                emitted_energy_this_shell=emitted,
                shell_gap=shell_gap,
                M_before=m_before,
                T_before=temperature_L(L, q, sigma),
                first_omega_over_T=(first_omega or 0.0) / temperature_L(L, q, sigma),
                internal_entropy_after=internal_after,
                external_capacity_after=external_capacity,
                page_estimate_after=page_estimate,
                normalized_time_after=normalized_time,
                f14_module="algebraic-expander interacting-spin scrambling",
            )
        )

    if page_cross_L < 0:
        page_cross_L = 0
    page_fraction = (total_entropy - entropy_L(page_cross_L, q)) / total_entropy
    scale_power = bath_dim + 1
    lifetime_scaled = normalized_time / (mass_L(L0, sigma) ** scale_power)
    summary = StitchedSummary(
        L0=L0,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        total_shell_cycles=len(rows),
        total_micro_emissions=total_micro_emissions,
        final_external_capacity=external_capacity,
        page_cross_L=page_cross_L,
        page_fraction_evaporated=page_fraction,
        normalized_lifetime=normalized_time,
        lifetime_scaled=lifetime_scaled,
        f15_status="P+: one explicit repeated-interaction architecture, not one H_total",
    )
    return rows, summary


def write_dataclass_rows(rows: list[object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].__dataclass_fields__))  # type: ignore[attr-defined]
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("L40_2d", 40, 2, 1.0, 2),
        ("L80_2d", 80, 2, 1.0, 2),
        ("L40_3d", 40, 2, 1.0, 3),
    ]
    for label, L0, q, sigma, bath_dim in cases:
        rows, summary = run_stitched_evaporator(
            L0=L0,
            q=q,
            sigma=sigma,
            bath_dim=bath_dim,
        )
        write_dataclass_rows(rows, out_dir / f"stitched_floquet_evaporator_{label}.csv")
        write_dataclass_rows(
            [summary], out_dir / f"stitched_floquet_evaporator_{label}_summary.csv"
        )
        print(label)
        print(
            f"  shell cycles={summary.total_shell_cycles}",
            f"micro emissions={summary.total_micro_emissions}",
            f"page L={summary.page_cross_L}",
            f"page fraction={summary.page_fraction_evaporated:.3f}",
            f"lifetime scaled={summary.lifetime_scaled:.6f}",
        )
        for row in rows[:3] + rows[-3:]:
            print(
                " ",
                f"{row.L_before}->{row.L_after}",
                f"events={row.emissions_this_shell}",
                f"first omega/T={row.first_omega_over_T:.3f}",
                f"Page={row.page_estimate_after:.3f}",
            )


if __name__ == "__main__":
    main()
