from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from statistics import mean

from fused_floquet_time_resolved_scan import (
    StateKeyTR,
    build_initial_sparse,
    entropy_from_factors,
    golden_hard_schedule,
    mutual_information_from_factors,
)
from interacting_spin_hamiltonian_page import shell_qubits
from threshold_integrated_statevector_evaporator import (
    normalize_sparse,
    transfer_next_shell,
    transferred_probabilities,
)


@dataclass(frozen=True)
class ThresholdVariantRow:
    mode: str
    threshold: int
    seed: int
    scrambler: str
    micro_emissions: int
    basis_terms: int
    transferred_mean: float
    p_done: float
    s_soft: float
    s_full_radiation: float
    s_core_acc: float
    mi_old_new_full: float
    soft_minus_none: float
    old_new_minus_none: float


@dataclass(frozen=True)
class ThresholdVariantSummary:
    mode: str
    threshold: int
    cases: int
    scrambled_soft_mean: float
    none_soft_mean: float
    soft_gap_mean: float
    scrambled_old_new_mean: float
    none_old_new_mean: float
    old_new_gap_mean: float
    transferred_mean_scrambled: float
    p_done_scrambled: float
    max_basis_terms: int


def emit_with_threshold_mode(
    state: dict[StateKeyTR, complex],
    threshold: int,
    n_bits: int,
    shell_axes_by_stage: tuple[list[int], list[int], list[int]],
    p_one: float,
    mode: str,
) -> dict[StateKeyTR, complex]:
    next_state: dict[StateKeyTR, complex] = {}
    for key, amplitude in state.items():
        core, acc, transferred, soft_labels, hard_bits, bath_bits, soft_history = key
        for hard_bit, energy, probability in (
            (0, 1, 1.0 - p_one),
            (1, 2, p_one),
        ):
            if probability <= 0.0:
                continue
            new_acc = acc + energy
            new_core = core
            new_transferred = transferred
            new_soft = soft_labels
            soft_event = (0, 0)
            if new_acc >= threshold and transferred < 3:
                if mode == "carry":
                    new_acc -= threshold
                elif mode == "reset":
                    new_acc = 0
                else:
                    raise ValueError(f"unknown mode {mode!r}")
                old_transferred = transferred
                new_core, new_transferred, new_soft = transfer_next_shell(
                    new_core,
                    new_transferred,
                    new_soft,
                    n_bits,
                    shell_axes_by_stage,
                )
                soft_event = (old_transferred + 1, new_soft[old_transferred])
            new_key = (
                new_core,
                new_acc,
                new_transferred,
                new_soft,
                (hard_bits << 1) | hard_bit,
                (bath_bits << 1) | hard_bit,
                soft_history + (soft_event,),
            )
            next_state[new_key] = next_state.get(new_key, 0.0j) + amplitude * math.sqrt(
                probability
            )
    return normalize_sparse(next_state)


def run_case(
    mode: str,
    threshold: int,
    seed: int,
    scrambler: str,
    L0: int = 3,
    rate_L0: float = 20.0,
    micro_emissions: int = 6,
) -> ThresholdVariantRow:
    n_bits = L0 * L0
    split_step = micro_emissions // 2
    shell_axes_by_stage = (
        sorted(shell_qubits(L0, 3)),
        sorted(shell_qubits(L0, 2)),
        sorted(shell_qubits(L0, 1)),
    )
    hard_probs, _means, _temps = golden_hard_schedule(
        L0=rate_L0,
        micro_emissions=micro_emissions,
        q=2,
        sigma=1.0,
        bath_dim=2,
        x_edges=__import__("numpy").array((0.0, 2.0, 8.0), dtype=float),
        n_grid=1001,
    )
    state = build_initial_sparse(L0, 8.0, 0.2, seed, scrambler)
    for p_one in hard_probs:
        state = emit_with_threshold_mode(
            state, threshold, n_bits, shell_axes_by_stage, p_one, mode
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
    return ThresholdVariantRow(
        mode=mode,
        threshold=threshold,
        seed=seed,
        scrambler=scrambler,
        micro_emissions=micro_emissions,
        basis_terms=len(state),
        transferred_mean=transferred_mean,
        p_done=probs[3],
        s_soft=entropy_from_factors(state, ("soft",), micro_emissions, split_step),
        s_full_radiation=entropy_from_factors(
            state, ("full_radiation",), micro_emissions, split_step
        ),
        s_core_acc=entropy_from_factors(state, ("core_acc",), micro_emissions, split_step),
        mi_old_new_full=mutual_information_from_factors(
            state, ("full_old",), ("full_new",), micro_emissions, split_step
        ),
        soft_minus_none=0.0,
        old_new_minus_none=0.0,
    )


def summarize(rows: list[ThresholdVariantRow]) -> list[ThresholdVariantSummary]:
    out: list[ThresholdVariantSummary] = []
    for mode in sorted({row.mode for row in rows}):
        for threshold in sorted({row.threshold for row in rows if row.mode == mode}):
            group = [row for row in rows if row.mode == mode and row.threshold == threshold]
            scrambled = [row for row in group if row.scrambler in {"margulis", "grid"}]
            none = [row for row in group if row.scrambler == "none"]
            none_soft = {row.seed: row.s_soft for row in none}
            none_old = {row.seed: row.mi_old_new_full for row in none}
            soft_gaps = [
                row.s_soft - none_soft[row.seed]
                for row in scrambled
                if row.seed in none_soft
            ]
            old_gaps = [
                row.mi_old_new_full - none_old[row.seed]
                for row in scrambled
                if row.seed in none_old
            ]
            out.append(
                ThresholdVariantSummary(
                    mode=mode,
                    threshold=threshold,
                    cases=len(group),
                    scrambled_soft_mean=mean(row.s_soft for row in scrambled),
                    none_soft_mean=mean(row.s_soft for row in none),
                    soft_gap_mean=mean(soft_gaps),
                    scrambled_old_new_mean=mean(row.mi_old_new_full for row in scrambled),
                    none_old_new_mean=mean(row.mi_old_new_full for row in none),
                    old_new_gap_mean=mean(old_gaps),
                    transferred_mean_scrambled=mean(row.transferred_mean for row in scrambled),
                    p_done_scrambled=mean(row.p_done for row in scrambled),
                    max_basis_terms=max(row.basis_terms for row in group),
                )
            )
    return out


def write_dataclass_rows(rows: list[object], path: Path) -> None:
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
    rows: list[ThresholdVariantRow] = []
    for mode in ("carry", "reset"):
        for threshold in (4, 5):
            for scrambler in ("margulis", "grid", "none"):
                for seed in (0, 1):
                    rows.append(run_case(mode, threshold, seed, scrambler))
    none_soft = {
        (row.mode, row.threshold, row.seed): row.s_soft
        for row in rows
        if row.scrambler == "none"
    }
    none_old = {
        (row.mode, row.threshold, row.seed): row.mi_old_new_full
        for row in rows
        if row.scrambler == "none"
    }
    rows = [
        ThresholdVariantRow(
            **{
                **row.__dict__,
                "soft_minus_none": row.s_soft
                - none_soft.get((row.mode, row.threshold, row.seed), row.s_soft),
                "old_new_minus_none": row.mi_old_new_full
                - none_old.get(
                    (row.mode, row.threshold, row.seed), row.mi_old_new_full
                ),
            }
        )
        for row in rows
    ]
    summary = summarize(rows)
    out_dir = Path(__file__).resolve().parent / "data"
    write_dataclass_rows(rows, out_dir / "fused_floquet_threshold_variant_rows.csv")
    write_dataclass_rows(
        summary, out_dir / "fused_floquet_threshold_variant_summary.csv"
    )
    print("mode   threshold soft_gap old_new_gap <shells> p_done")
    for row in summary:
        print(
            f"{row.mode:6s} "
            f"{row.threshold:9d} "
            f"{row.soft_gap_mean:8.3f} "
            f"{row.old_new_gap_mean:11.3f} "
            f"{row.transferred_mean_scrambled:8.3f} "
            f"{row.p_done_scrambled:6.3f}"
        )


if __name__ == "__main__":
    main()
