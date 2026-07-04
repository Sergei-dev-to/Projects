from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from stitched_floquet_evaporator import golden_rule_bins, mass_L, temperature_L


@dataclass(frozen=True)
class BathSpectrumBin:
    spectrum: str
    L: int
    bin_index: int
    omega: float
    target_probability: float
    bath_count: int
    bath_probability: float
    probability_error: float
    omega_over_T: float


@dataclass(frozen=True)
class BathSpectrumSummary:
    spectrum: str
    L: int
    q: int
    sigma: float
    bath_dim: int
    bin_count: int
    oscillator_count: int
    mode_spacing: float
    max_quanta: int
    state_count: int
    l1_error: float
    max_error: float
    mean_omega: float
    target_mean_omega: float
    power_proxy: float
    target_power_proxy: float


def weak_compositions(total: int, parts: int) -> list[tuple[int, ...]]:
    if parts == 1:
        return [(total,)]
    out: list[tuple[int, ...]] = []
    for first in range(total + 1):
        for rest in weak_compositions(total - first, parts - 1):
            out.append((first,) + rest)
    return out


def oscillator_bath_energies(
    oscillator_count: int,
    mode_spacing: float,
    max_quanta: int,
    spectrum: str,
) -> list[float]:
    if spectrum == "linear":
        mode_energies = [mode_spacing * (idx + 1) for idx in range(oscillator_count)]
    elif spectrum == "quadratic":
        mode_energies = [
            mode_spacing * (idx + 1) ** 2 for idx in range(oscillator_count)
        ]
    elif spectrum == "box2d":
        energies: list[float] = []
        for nx in range(-max_quanta, max_quanta + 1):
            for ny in range(-max_quanta, max_quanta + 1):
                if nx == 0 and ny == 0:
                    continue
                energies.append(mode_spacing * math.sqrt(nx * nx + ny * ny))
        return sorted(energies)
    else:
        raise ValueError(f"unknown spectrum: {spectrum}")

    energies: list[float] = []
    for total_quanta in range(max_quanta + 1):
        for occupations in weak_compositions(total_quanta, oscillator_count):
            energies.append(
                sum(n * energy for n, energy in zip(occupations, mode_energies))
            )
    return sorted(energies)


def bin_edges_from_centers(centers: list[float]) -> list[float]:
    if len(centers) == 1:
        return [0.0, max(centers[0] * 2.0, 1.0)]
    edges = [0.0]
    for left, right in zip(centers[:-1], centers[1:]):
        edges.append(0.5 * (left + right))
    edges.append(centers[-1] + 0.5 * (centers[-1] - centers[-2]))
    return edges


def counts_in_bins(energies: list[float], centers: list[float]) -> list[int]:
    edges = bin_edges_from_centers(centers)
    counts = [0 for _ in centers]
    for energy in energies:
        for idx in range(len(centers)):
            if edges[idx] <= energy < edges[idx + 1]:
                counts[idx] += 1
                break
    return counts


def bath_probabilities_from_counts(counts: list[int]) -> list[float]:
    regularized = [max(1, count) for count in counts]
    total = sum(regularized)
    return [count / total for count in regularized]


def entropy_ratio_weight(L: int, omega: float, q: int, sigma: float) -> float:
    mass = mass_L(L, sigma)
    l_after = max(0.0, (mass - omega) / (4.0 * sigma))
    delta_s = (l_after * l_after - L * L) * math.log(q)
    return math.exp(delta_s)


def run_bath_spectrum_check(
    spectrum: str,
    L: int,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    bin_count: int = 8,
    oscillator_count: int = 6,
    max_quanta: int = 9,
    mode_spacing_factor: float = 0.35,
) -> tuple[list[BathSpectrumBin], BathSpectrumSummary]:
    distribution = golden_rule_bins(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
    )
    centers = [omega for omega, _ in distribution]
    targets = [prob for _, prob in distribution]
    t = temperature_L(L, q, sigma)
    mode_spacing = mode_spacing_factor * t
    energies = oscillator_bath_energies(
        oscillator_count=oscillator_count,
        mode_spacing=mode_spacing,
        max_quanta=max_quanta,
        spectrum=spectrum,
    )
    counts = counts_in_bins(energies, centers)
    # The bath Hamiltonian supplies the density-of-states factor. The core
    # still supplies the microcanonical entropy-ratio factor.
    raw_actuals = [
        max(1, count) * entropy_ratio_weight(L, omega, q, sigma)
        for count, omega in zip(counts, centers)
    ]
    total_actual = sum(raw_actuals)
    actuals = [weight / total_actual for weight in raw_actuals]

    rows: list[BathSpectrumBin] = []
    errors = [abs(actual - target) for actual, target in zip(actuals, targets)]
    for idx, (omega, target, count, actual) in enumerate(
        zip(centers, targets, counts, actuals)
    ):
        rows.append(
            BathSpectrumBin(
                spectrum=spectrum,
                L=L,
                bin_index=idx,
                omega=omega,
                target_probability=target,
                bath_count=count,
                bath_probability=actual,
                probability_error=actual - target,
                omega_over_T=omega / t,
            )
        )

    mean_omega = sum(omega * prob for omega, prob in zip(centers, actuals))
    target_mean_omega = sum(omega * prob for omega, prob in zip(centers, targets))
    summary = BathSpectrumSummary(
        spectrum=spectrum,
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
        oscillator_count=oscillator_count,
        mode_spacing=mode_spacing,
        max_quanta=max_quanta,
        state_count=len(energies),
        l1_error=sum(errors),
        max_error=max(errors),
        mean_omega=mean_omega,
        target_mean_omega=target_mean_omega,
        power_proxy=4.0 * L * mean_omega ** (bath_dim + 1),
        target_power_proxy=4.0 * L * target_mean_omega ** (bath_dim + 1),
    )
    return rows, summary


def power_law_slope(summaries: list[BathSpectrumSummary]) -> float:
    xs = np.array([math.log(mass_L(item.L, item.sigma)) for item in summaries])
    ys = np.array([math.log(max(item.power_proxy, 1e-300)) for item in summaries])
    slope, _intercept = np.polyfit(xs, ys, deg=1)
    return float(slope)


def write_dataclass_rows(rows: list[object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].__dataclass_fields__)  # type: ignore[attr-defined]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    all_rows: list[BathSpectrumBin] = []
    summaries: list[BathSpectrumSummary] = []
    for spectrum in ("linear", "quadratic", "box2d"):
        spectrum_summaries: list[BathSpectrumSummary] = []
        for L in (8, 16, 32, 64):
            rows, summary = run_bath_spectrum_check(
                spectrum=spectrum,
                L=L,
                max_quanta=20 if spectrum == "box2d" else 9,
            )
            all_rows.extend(rows)
            summaries.append(summary)
            spectrum_summaries.append(summary)
            print(
                f"spectrum={spectrum}",
                f"L={L}",
                f"states={summary.state_count}",
                f"L1={summary.l1_error:.3f}",
                f"max={summary.max_error:.3f}",
                f"mean/target={summary.mean_omega/summary.target_mean_omega:.3f}",
                f"P/target={summary.power_proxy/summary.target_power_proxy:.3f}",
            )
        print(
            f"spectrum={spectrum}",
            f"logP/logM slope={power_law_slope(spectrum_summaries):.3f}",
        )

    write_dataclass_rows(all_rows, out_dir / "explicit_bath_hamiltonian_bins.csv")
    write_dataclass_rows(summaries, out_dir / "explicit_bath_hamiltonian_summary.csv")


if __name__ == "__main__":
    main()
