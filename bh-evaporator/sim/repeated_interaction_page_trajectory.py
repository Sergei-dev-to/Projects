from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from fused_floquet_time_resolved_scan import (
    build_initial_sparse,
    emit_weighted_quantum_time_resolved,
    entropy_from_factors,
    factors_from_key,
    golden_hard_schedule,
)
from interacting_spin_hamiltonian_page import shell_qubits
from threshold_integrated_statevector_evaporator import transferred_probabilities


@dataclass(frozen=True)
class PageTrajectoryRow:
    scrambler: str
    seed: int
    step: int
    threshold: int
    L_init: int
    L_sched: float
    basis_terms: int
    transferred_mean: float
    p_done: float
    s_full_radiation: float
    s_core_acc: float
    log_core_acc_support: float
    mean_active_core_capacity: float


def core_acc_support_log(state, step: int) -> float:
    factors = [factors_from_key(key, step, step // 2)["core_acc"] for key in state]
    return math.log(len(set(factors))) if factors else 0.0


def mean_active_core_capacity(
    state,
    L_init: int,
    q: int,
) -> float:
    old_style_state = {
        (core, acc, transferred, soft_labels, hard_bits, bath_bits): amplitude
        for (
            core,
            acc,
            transferred,
            soft_labels,
            hard_bits,
            bath_bits,
            _soft_history,
        ), amplitude in state.items()
    }
    probs = transferred_probabilities(old_style_state)
    return sum(
        prob * max(L_init - transferred, 0) ** 2 * math.log(q)
        for transferred, prob in probs.items()
    )


def run_page_trajectory(
    L_init: int = 3,
    L_sched: float = 20.0,
    threshold: int = 4,
    micro_emissions: int = 8,
    scramblers: tuple[str, ...] = ("margulis", "none"),
    seed: int = 0,
    q: int = 2,
    sigma: float = 1.0,
    bath_dim: int = 2,
    x_edges: tuple[float, ...] = (0.0, 2.0, 8.0),
    n_grid: int = 1001,
    warmup_time: float = 8.0,
    dt: float = 0.2,
) -> list[PageTrajectoryRow]:
    hard_probs, _mean_omegas, _temperatures = golden_hard_schedule(
        L0=L_sched,
        micro_emissions=micro_emissions,
        q=q,
        sigma=sigma,
        bath_dim=bath_dim,
        x_edges=np.array(x_edges, dtype=float),
        n_grid=n_grid,
    )
    n_bits = L_init * L_init
    shell_axes_by_stage = (
        sorted(shell_qubits(L_init, 3)),
        sorted(shell_qubits(L_init, 2)),
        sorted(shell_qubits(L_init, 1)),
    )
    rows: list[PageTrajectoryRow] = []
    for scrambler in scramblers:
        state = build_initial_sparse(
            L0=L_init,
            warmup_time=warmup_time,
            dt=dt,
            seed=seed,
            scrambler=scrambler,
        )
        for step, p_one in enumerate(hard_probs, start=1):
            state = emit_weighted_quantum_time_resolved(
                state=state,
                threshold=threshold,
                n_bits=n_bits,
                shell_axes_by_stage=shell_axes_by_stage,
                p_one=p_one,
            )
            old_style_state = {
                (core, acc, transferred, soft_labels, hard_bits, bath_bits): amplitude
                for (
                    core,
                    acc,
                    transferred,
                    soft_labels,
                    hard_bits,
                    bath_bits,
                    _soft_history,
                ), amplitude in state.items()
            }
            probs = transferred_probabilities(old_style_state)
            transferred_mean = sum(count * prob for count, prob in probs.items())
            rows.append(
                PageTrajectoryRow(
                    scrambler=scrambler,
                    seed=seed,
                    step=step,
                    threshold=threshold,
                    L_init=L_init,
                    L_sched=L_sched,
                    basis_terms=len(state),
                    transferred_mean=transferred_mean,
                    p_done=probs[3],
                    s_full_radiation=entropy_from_factors(
                        state, ("full_radiation",), step, step // 2
                    ),
                    s_core_acc=entropy_from_factors(
                        state, ("core_acc",), step, step // 2
                    ),
                    log_core_acc_support=core_acc_support_log(state, step),
                    mean_active_core_capacity=mean_active_core_capacity(
                        state, L_init, q
                    ),
                )
            )
    return rows


def write_rows(rows: list[PageTrajectoryRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0].__dataclass_fields__),  # type: ignore[attr-defined]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out = (
        Path(__file__).resolve().parent
        / "data"
        / "repeated_interaction_page_trajectory.csv"
    )
    rows = run_page_trajectory()
    write_rows(rows, out)
    print(f"wrote {out}")
    print(
        "scrambler step S_rad S_core log_support mean_capacity <shells> p_done terms"
    )
    for row in rows:
        if row.step in {2, 4, 6, 8}:
            print(
                f"{row.scrambler:9s} {row.step:4d} "
                f"{row.s_full_radiation:6.3f} {row.s_core_acc:6.3f} "
                f"{row.log_core_acc_support:10.3f} "
                f"{row.mean_active_core_capacity:13.3f} "
                f"{row.transferred_mean:8.3f} {row.p_done:6.3f} "
                f"{row.basis_terms:6d}"
            )


if __name__ == "__main__":
    main()
