from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

from finite_emission_hamiltonian import check_composed_shrinkage
from stitched_floquet_evaporator import golden_rule_bins, temperature_L


@dataclass(frozen=True)
class BathBinResult:
    L: int
    bin_index: int
    omega: float
    target_probability: float
    bath_degeneracy: int
    bath_probability: float
    probability_error: float
    omega_over_T: float


@dataclass(frozen=True)
class BathEmissionSummary:
    L: int
    q: int
    sigma: float
    bath_dim: int
    bin_count: int
    bath_microstates: int
    microscopic_coupling: float
    pulse_time: float
    emission_probability: float
    l1_error_conditional: float
    max_error_conditional: float
    shrinkage_injective_after_composition: bool


def integer_degeneracies(probabilities: list[float], total_states: int) -> list[int]:
    if total_states < len(probabilities):
        raise ValueError("total_states must be at least the number of bins")

    raw = [prob * total_states for prob in probabilities]
    floors = [max(1, math.floor(value)) for value in raw]
    excess = sum(floors) - total_states
    if excess > 0:
        order = sorted(range(len(floors)), key=lambda idx: raw[idx] - floors[idx])
        for idx in order:
            if excess == 0:
                break
            if floors[idx] > 1:
                floors[idx] -= 1
                excess -= 1

    deficit = total_states - sum(floors)
    if deficit > 0:
        order = sorted(
            range(len(floors)),
            key=lambda idx: raw[idx] - math.floor(raw[idx]),
            reverse=True,
        )
        for offset in range(deficit):
            floors[order[offset % len(order)]] += 1

    return floors


def run_finite_bath_density_check(
    L: int = 40,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    bin_count: int = 8,
    bath_microstates: int = 4096,
    emission_probability: float = 0.2,
    pulse_time: float = 1.0,
) -> tuple[list[BathBinResult], BathEmissionSummary]:
    distribution = golden_rule_bins(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
    )
    omegas = [omega for omega, _ in distribution]
    targets = [prob for _, prob in distribution]
    degeneracies = integer_degeneracies(targets, bath_microstates)
    actuals = [degeneracy / bath_microstates for degeneracy in degeneracies]

    # Equal microscopic coupling to every bath microstate. The aggregate
    # coupling norm is g * sqrt(N_bath).
    aggregate_coupling = math.asin(math.sqrt(emission_probability)) / pulse_time
    microscopic_coupling = aggregate_coupling / math.sqrt(bath_microstates)

    t = temperature_L(L, q, sigma)
    rows: list[BathBinResult] = []
    errors: list[float] = []
    for idx, (omega, target, degeneracy, actual) in enumerate(
        zip(omegas, targets, degeneracies, actuals)
    ):
        error = actual - target
        errors.append(abs(error))
        rows.append(
            BathBinResult(
                L=L,
                bin_index=idx,
                omega=omega,
                target_probability=target,
                bath_degeneracy=degeneracy,
                bath_probability=actual,
                probability_error=error,
                omega_over_T=omega / t if t > 0.0 else 0.0,
            )
        )

    injective = check_composed_shrinkage(
        L=5,
        emitted_bins=tuple(range(1, min(bin_count, 4) + 1)),
        shell_gap=8,
        accumulator_modulus=8,
    )
    summary = BathEmissionSummary(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
        bath_microstates=bath_microstates,
        microscopic_coupling=microscopic_coupling,
        pulse_time=pulse_time,
        emission_probability=emission_probability,
        l1_error_conditional=sum(errors),
        max_error_conditional=max(errors) if errors else 0.0,
        shrinkage_injective_after_composition=injective,
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
        ("L40_2d_N512", 40, 2, 512),
        ("L40_2d_N4096", 40, 2, 4096),
        ("L40_3d_N4096", 40, 3, 4096),
        ("L8_2d_N1024", 8, 2, 1024),
    ]
    for label, L, bath_dim, bath_microstates in cases:
        rows, summary = run_finite_bath_density_check(
            L=L,
            bath_dim=bath_dim,
            bath_microstates=bath_microstates,
        )
        write_dataclass_rows(rows, out_dir / f"finite_bath_density_emission_{label}.csv")
        write_dataclass_rows(
            [summary], out_dir / f"finite_bath_density_emission_{label}_summary.csv"
        )
        print(label)
        print(
            f"  bath states={summary.bath_microstates}",
            f"g={summary.microscopic_coupling:.6e}",
            f"L1 error={summary.l1_error_conditional:.3e}",
            f"max error={summary.max_error_conditional:.3e}",
            f"shrink injective={summary.shrinkage_injective_after_composition}",
        )
        for row in rows[:3]:
            print(
                " ",
                f"bin={row.bin_index}",
                f"omega/T={row.omega_over_T:.3f}",
                f"deg={row.bath_degeneracy}",
                f"target={row.target_probability:.6f}",
                f"actual={row.bath_probability:.6f}",
            )


if __name__ == "__main__":
    main()
