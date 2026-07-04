from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

from finite_bath_density_emission import integer_degeneracies
from finite_emission_hamiltonian import check_composed_shrinkage
from interacting_spin_trotter_page import (
    entropy_of_subset,
    evolve_trotter,
    random_product_state,
    shell_qubits,
)
from interacting_spin_hamiltonian_page import active_qubits
from stitched_floquet_evaporator import (
    deterministic_quantile_sample,
    entropy_L,
    golden_rule_bins,
    mass_L,
    temperature_L,
)


@dataclass(frozen=True)
class AuditedCycleRow:
    seed: int
    scrambler: str
    L0: int
    L_before: int
    L_after: int
    M_before: float
    T_before: float
    shell_gap: float
    micro_emissions: int
    emitted_energy: float
    first_omega_over_T: float
    bath_l1_error: float
    bath_max_error: float
    shrinkage_injective: bool
    rad_qubits: int
    shell_qubits: int
    remaining_qubits: int
    page_capacity: float
    s_rad: float
    old_new_mi: float
    entropy_deficit: float


@dataclass(frozen=True)
class AuditedSummary:
    seed: int
    scrambler: str
    L0: int
    q: int
    sigma: float
    bath_dim: int
    bin_count: int
    bath_microstates: int
    warmup_time: float
    cycle_time: float
    dt: float
    total_micro_emissions: int
    total_entropy_deficit: float
    max_bath_l1_error: float
    page_cross_L: int
    first_old_new_mi: str
    lifetime_scaled_capacity_rule: float
    status: str


def grid_id(L0: int, x: int, y: int) -> int:
    return x * L0 + y


def grid_edges(L0: int) -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for x in range(L0):
        for y in range(L0):
            src = grid_id(L0, x, y)
            for dx, dy in ((1, 0), (0, 1)):
                nx = x + dx
                ny = y + dy
                if nx < L0 and ny < L0:
                    dst = grid_id(L0, nx, ny)
                    edges.add((min(src, dst), max(src, dst)))
    return sorted(edges)


def margulis_edges(L0: int) -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for x in range(L0):
        for y in range(L0):
            src = grid_id(L0, x, y)
            targets = [
                ((x + 2 * y) % L0, y),
                ((x - 2 * y) % L0, y),
                ((x + 2 * y + 1) % L0, y),
                ((x - 2 * y - 1) % L0, y),
                (x, (y + 2 * x) % L0),
                (x, (y - 2 * x) % L0),
                (x, (y + 2 * x + 1) % L0),
                (x, (y - 2 * x - 1) % L0),
            ]
            for tx, ty in targets:
                dst = grid_id(L0, tx, ty)
                if src != dst:
                    edges.add((min(src, dst), max(src, dst)))
    return sorted(edges)


def deterministic_parameters(
    L0: int,
    scrambler: str,
) -> tuple[dict[int, tuple[float, float]], dict[tuple[int, int], tuple[float, float, float]]]:
    if scrambler == "none":
        return {}, {}
    if scrambler == "grid":
        edges = grid_edges(L0)
    elif scrambler == "margulis":
        edges = margulis_edges(L0)
    else:
        raise ValueError(f"unknown scrambler: {scrambler}")

    fields: dict[int, tuple[float, float]] = {}
    for qid in range(L0 * L0):
        fields[qid] = (
            0.73 + 0.11 * ((qid % 5) - 2),
            0.37 + 0.07 * ((qid % 7) - 3),
        )

    degree_scale = math.sqrt(max(1.0, 2.0 * len(edges) / (L0 * L0)))
    couplings: dict[tuple[int, int], tuple[float, float, float]] = {}
    for i, j in edges:
        code = ((i + 3) * (j + 5)) % 17
        couplings[(i, j)] = (
            (0.50 + 0.03 * code) / degree_scale,
            (0.43 + 0.02 * ((code + 5) % 17)) / degree_scale,
            (0.61 + 0.025 * ((code + 11) % 17)) / degree_scale,
        )
    return fields, couplings


def bath_density_error(
    L: int,
    q: int,
    sigma: float,
    bath_dim: int,
    bin_count: int,
    bath_microstates: int,
) -> tuple[list[tuple[float, float]], float, float]:
    distribution = golden_rule_bins(
        L=L,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
    )
    targets = [probability for _, probability in distribution]
    degeneracies = integer_degeneracies(targets, bath_microstates)
    actuals = [degeneracy / bath_microstates for degeneracy in degeneracies]
    errors = [abs(actual - target) for actual, target in zip(actuals, targets)]
    return distribution, sum(errors), max(errors) if errors else 0.0


def evolve_scrambler(
    state,
    n_qubits: int,
    active: set[int],
    fields: dict[int, tuple[float, float]],
    couplings: dict[tuple[int, int], tuple[float, float, float]],
    time: float,
    dt: float,
):
    if not fields and not couplings:
        return state
    return evolve_trotter(
        state=state,
        n_qubits=n_qubits,
        active=active,
        fields=fields,
        couplings=couplings,
        time=time,
        dt=dt,
    )


def run_audited_evaporator(
    L0: int = 4,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    bin_count: int = 8,
    bath_microstates: int = 2048,
    warmup_time: float = 8.0,
    cycle_time: float = 2.0,
    dt: float = 0.2,
    seed: int = 0,
    scrambler: str = "margulis",
) -> tuple[list[AuditedCycleRow], AuditedSummary]:
    n_qubits = L0 * L0
    fields, couplings = deterministic_parameters(L0, scrambler)
    state = random_product_state(n_qubits, seed + 10_000)
    radiation: set[int] = set()
    rows: list[AuditedCycleRow] = []
    total_micro_emissions = 0
    normalized_time = 0.0
    page_cross_L = -1
    first_old_new_mi = ""

    state = evolve_scrambler(
        state=state,
        n_qubits=n_qubits,
        active=set(active_qubits(L0, L0)),
        fields=fields,
        couplings=couplings,
        time=warmup_time,
        dt=dt,
    )

    for L in range(L0, 0, -1):
        state = evolve_scrambler(
            state=state,
            n_qubits=n_qubits,
            active=set(active_qubits(L0, L)),
            fields=fields,
            couplings=couplings,
            time=cycle_time,
            dt=dt,
        )

        distribution, bath_l1, bath_max = bath_density_error(
            L=L,
            q=q,
            sigma=sigma,
            bath_dim=bath_dim,
            bin_count=bin_count,
            bath_microstates=bath_microstates,
        )
        shell_gap = mass_L(L, sigma) - mass_L(max(0, L - 1), sigma)
        emitted = 0.0
        emissions = 0
        first_omega = None

        while emitted < shell_gap and L > 0:
            omega = deterministic_quantile_sample(
                distribution, total_micro_emissions + emissions + 1
            )
            if first_omega is None:
                first_omega = omega
            emitted += omega
            emissions += 1

        total_micro_emissions += emissions
        shrinkage_injective = check_composed_shrinkage(
            L=max(2, L),
            emitted_bins=tuple(range(1, min(bin_count, 4) + 1)),
            shell_gap=8,
            accumulator_modulus=8,
        )

        old_radiation = set(radiation)
        shell = shell_qubits(L0, L)
        radiation |= shell
        remaining = max(0, (L - 1) * (L - 1))
        capacity = min(len(radiation), remaining) * math.log(2.0)
        s_old = entropy_of_subset(state, n_qubits, old_radiation)
        s_new = entropy_of_subset(state, n_qubits, shell)
        s_rad = entropy_of_subset(state, n_qubits, radiation)
        old_new_mi = max(0.0, s_old + s_new - s_rad)
        if not first_old_new_mi and old_new_mi > 1e-6:
            first_old_new_mi = f"{L}->{L - 1}"
        if page_cross_L < 0 and len(radiation) >= remaining:
            page_cross_L = L - 1

        normalized_time += (
            mass_L(L, sigma) ** (bath_dim + 1)
            - mass_L(max(0, L - 1), sigma) ** (bath_dim + 1)
        ) / (bath_dim + 1)

        t = temperature_L(L, q, sigma)
        rows.append(
            AuditedCycleRow(
                seed=seed,
                scrambler=scrambler,
                L0=L0,
                L_before=L,
                L_after=L - 1,
                M_before=mass_L(L, sigma),
                T_before=t,
                shell_gap=shell_gap,
                micro_emissions=emissions,
                emitted_energy=emitted,
                first_omega_over_T=(first_omega or 0.0) / t,
                bath_l1_error=bath_l1,
                bath_max_error=bath_max,
                shrinkage_injective=shrinkage_injective,
                rad_qubits=len(radiation),
                shell_qubits=len(shell),
                remaining_qubits=remaining,
                page_capacity=capacity,
                s_rad=s_rad,
                old_new_mi=old_new_mi,
                entropy_deficit=capacity - s_rad,
            )
        )

    if page_cross_L < 0:
        page_cross_L = 0
    summary = AuditedSummary(
        seed=seed,
        scrambler=scrambler,
        L0=L0,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        bin_count=bin_count,
        bath_microstates=bath_microstates,
        warmup_time=warmup_time,
        cycle_time=cycle_time,
        dt=dt,
        total_micro_emissions=total_micro_emissions,
        total_entropy_deficit=sum(max(0.0, row.entropy_deficit) for row in rows),
        max_bath_l1_error=max(row.bath_l1_error for row in rows),
        page_cross_L=page_cross_L,
        first_old_new_mi=first_old_new_mi or "none",
        lifetime_scaled_capacity_rule=normalized_time
        / (mass_L(L0, sigma) ** (bath_dim + 1)),
        status=(
            "single audited repeated-interaction update; deterministic "
            "scrambling, finite bath-density emission, reversible shrinkage"
        ),
    )
    return rows, summary


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
    all_summaries: list[AuditedSummary] = []
    for scrambler in ("margulis", "grid", "none"):
        for seed in range(5):
            rows, summary = run_audited_evaporator(seed=seed, scrambler=scrambler)
            write_dataclass_rows(
                rows,
                out_dir
                / f"audited_repeated_interaction_evaporator_{scrambler}_seed{seed}.csv",
            )
            all_summaries.append(summary)
            print(
                f"scrambler={scrambler}",
                f"seed={seed}",
                f"emissions={summary.total_micro_emissions}",
                f"deficit={summary.total_entropy_deficit:.3f}",
                f"max bath L1={summary.max_bath_l1_error:.3e}",
                f"page L={summary.page_cross_L}",
                f"first MI={summary.first_old_new_mi}",
                f"lifetime scale={summary.lifetime_scaled_capacity_rule:.6f}",
            )

    write_dataclass_rows(
        all_summaries,
        out_dir / "audited_repeated_interaction_evaporator_summary.csv",
    )


if __name__ == "__main__":
    main()
