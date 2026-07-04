from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from reversible_shrinkage_automaton import transition
from stitched_floquet_evaporator import golden_rule_bins, temperature_L


@dataclass(frozen=True)
class EmissionBinResult:
    L: int
    bin_index: int
    omega: float
    target_probability: float
    hamiltonian_probability: float
    probability_error: float
    omega_over_T: float


@dataclass(frozen=True)
class EmissionSummary:
    L: int
    q: int
    sigma: float
    bath_dim: int
    bin_count: int
    pulse_time: float
    emission_probability: float
    target_total_probability: float
    l1_error_conditional: float
    max_error_conditional: float
    shrinkage_injective_after_composition: bool


def build_star_hamiltonian(target_probs: list[float], emission_probability: float, pulse_time: float) -> np.ndarray:
    """Hamiltonian coupling one input state to emitted-bin states.

    H = sum_h g_h (|h><in| + |in><h|)

    If the coupling vector has norm G and the initial state is |in>, then after
    time t the total emitted probability is sin^2(G t), and the conditional
    distribution over h is g_h^2 / G^2.
    """

    if not 0.0 <= emission_probability <= 1.0:
        raise ValueError("emission_probability must be in [0,1]")
    if pulse_time <= 0.0:
        raise ValueError("pulse_time must be positive")

    total = sum(target_probs)
    if total <= 0.0:
        raise ValueError("target probabilities must have positive total")
    normalized = [prob / total for prob in target_probs]
    coupling_norm = math.asin(math.sqrt(emission_probability)) / pulse_time
    couplings = [coupling_norm * math.sqrt(prob) for prob in normalized]

    dim = 1 + len(target_probs)
    hamiltonian = np.zeros((dim, dim), dtype=np.complex128)
    for idx, coupling in enumerate(couplings, start=1):
        hamiltonian[0, idx] = coupling
        hamiltonian[idx, 0] = coupling
    return hamiltonian


def evolve_emission(hamiltonian: np.ndarray, pulse_time: float) -> np.ndarray:
    initial = np.zeros(hamiltonian.shape[0], dtype=np.complex128)
    initial[0] = 1.0
    return expm(-1j * hamiltonian * pulse_time) @ initial


def check_composed_shrinkage(
    L: int,
    emitted_bins: tuple[int, ...],
    shell_gap: int,
    accumulator_modulus: int,
) -> bool:
    outputs: set[tuple[object, ...]] = set()
    transition_count = 0
    for accumulator in range(accumulator_modulus):
        for shell_label in range(2 ** max(0, 2 * L - 1)):
            for emitted_bin in emitted_bins:
                item = transition(
                    L=L,
                    accumulator=accumulator,
                    shell_label=shell_label,
                    emitted_bin=emitted_bin,
                    shell_gap=shell_gap,
                    accumulator_modulus=accumulator_modulus,
                )
                key = (
                    item.L_after,
                    item.accumulator_after,
                    item.shell_label_after,
                    item.shrink_record,
                    item.radiation_record,
                )
                outputs.add(key)
                transition_count += 1
    return len(outputs) == transition_count


def run_emission_hamiltonian_check(
    L: int = 40,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    bin_count: int = 8,
    emission_probability: float = 0.2,
    pulse_time: float = 1.0,
) -> tuple[list[EmissionBinResult], EmissionSummary]:
    distribution = golden_rule_bins(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
    )
    omegas = [omega for omega, _ in distribution]
    target_probs = [prob for _, prob in distribution]
    hamiltonian = build_star_hamiltonian(target_probs, emission_probability, pulse_time)
    state = evolve_emission(hamiltonian, pulse_time)
    probabilities = np.abs(state[1:]) ** 2
    total_emitted = float(np.sum(probabilities))
    conditional = probabilities / total_emitted if total_emitted > 0.0 else probabilities

    rows: list[EmissionBinResult] = []
    t = temperature_L(L, q, sigma)
    errors: list[float] = []
    for idx, (omega, target, actual) in enumerate(zip(omegas, target_probs, conditional)):
        error = float(actual - target)
        errors.append(abs(error))
        rows.append(
            EmissionBinResult(
                L=L,
                bin_index=idx,
                omega=omega,
                target_probability=target,
                hamiltonian_probability=float(actual),
                probability_error=error,
                omega_over_T=omega / t if t > 0.0 else 0.0,
            )
        )

    # Integer bins for the shrink automaton composition. The exact values are
    # not meant to equal omega; they are finite emitted-energy labels.
    emitted_integer_bins = tuple(range(1, min(bin_count, 4) + 1))
    injective = check_composed_shrinkage(
        L=5,
        emitted_bins=emitted_integer_bins,
        shell_gap=8,
        accumulator_modulus=8,
    )

    summary = EmissionSummary(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
        pulse_time=pulse_time,
        emission_probability=total_emitted,
        target_total_probability=sum(target_probs),
        l1_error_conditional=float(sum(errors)),
        max_error_conditional=float(max(errors) if errors else 0.0),
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
        ("L40_2d", 40, 2),
        ("L40_3d", 40, 3),
        ("L8_2d", 8, 2),
    ]
    for label, L, bath_dim in cases:
        rows, summary = run_emission_hamiltonian_check(L=L, bath_dim=bath_dim)
        write_dataclass_rows(rows, out_dir / f"finite_emission_hamiltonian_{label}.csv")
        write_dataclass_rows(
            [summary], out_dir / f"finite_emission_hamiltonian_{label}_summary.csv"
        )
        print(label)
        print(
            f"  emitted probability={summary.emission_probability:.6f}",
            f"L1 conditional error={summary.l1_error_conditional:.3e}",
            f"max error={summary.max_error_conditional:.3e}",
            f"shrink injective={summary.shrinkage_injective_after_composition}",
        )
        for row in rows[:3]:
            print(
                " ",
                f"bin={row.bin_index}",
                f"omega/T={row.omega_over_T:.3f}",
                f"target={row.target_probability:.6f}",
                f"actual={row.hamiltonian_probability:.6f}",
            )


if __name__ == "__main__":
    main()
