#!/usr/bin/env python3
"""Unified unitary sector-isometry evaporator.

This script promotes the energy-resolved sector-rate kernel to a finite
state-vector model.  A single evaporation run now has:

    - sector dimensions and mass law;
    - hard emission weights derived from golden-rule transition data;
    - an isometric emission map from B_n to B_{n-1} plus hard/soft records;
    - full radiation entropy and early/late mutual information measured from
      the same state.

The soft record is the Stinespring register that makes the coarse shrinkage
map exactly unitary.  The hard probabilities are not assigned by hand; they
are obtained by binning the sector Hamiltonian transition kernel.
"""
from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_energy_resolved import (
    beta_for_downward_step,
    build_energy_resolved_sectors,
    build_transition_data,
)
from sector_hamiltonian_evaporator import target_x_distribution


StateKey = tuple[int, int, tuple[int, ...], tuple[int, ...]]
State = dict[StateKey, complex]


@dataclass(frozen=True)
class SectorRule:
    n: int
    beta: float
    total_rate: float
    hard_probs: np.ndarray
    hard_mean_omega: np.ndarray
    hard_mean_x: np.ndarray
    core_maps_scrambled: np.ndarray
    core_maps_noscramble: np.ndarray


@dataclass(frozen=True)
class TrajectoryRow:
    mass_law: str
    mapping: str
    seed: int
    step: int
    n_before: int
    n_after: int
    rate: float
    mean_omega: float
    power: float
    mean_x: float
    spectrum_tv_to_thermal_x: float
    s_full_radiation: float
    s_core: float
    s_early: float
    s_late: float
    i_early_late: float
    log_core_support: float
    basis_terms: int


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def normalize_probs(values: np.ndarray) -> np.ndarray:
    total = float(np.sum(values))
    if total <= 0.0:
        raise ValueError("cannot normalize zero probability vector")
    return values / total


def hard_bin_stats(
    rates: np.ndarray,
    omegas: np.ndarray,
    beta: float,
    x_edges: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    """Average transition kernel over an equilibrated incoming sector."""
    x_values = beta * omegas
    hard_weights = np.zeros(len(x_edges) - 1, dtype=float)
    hard_omega = np.zeros_like(hard_weights)
    hard_x = np.zeros_like(hard_weights)
    for h in range(len(hard_weights)):
        mask = (x_values >= x_edges[h]) & (x_values < x_edges[h + 1])
        weighted = np.where(mask, rates, 0.0)
        weight = float(np.sum(weighted))
        hard_weights[h] = weight
        if weight > 0.0:
            hard_omega[h] = float(np.sum(weighted * omegas) / weight)
            hard_x[h] = float(np.sum(weighted * x_values) / weight)
    total_rate = float(np.sum(rates) / rates.shape[1])
    hard_probs = normalize_probs(hard_weights)
    # Empty bins can happen at the edges.  Use bin centers for harmless labels.
    centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    finite_centers = np.where(np.isfinite(centers), centers, x_edges[:-1] + 1.0)
    hard_x = np.where(hard_weights > 0.0, hard_x, finite_centers)
    hard_omega = np.where(hard_weights > 0.0, hard_omega, hard_x / beta)
    return hard_probs, hard_omega, hard_x, total_rate


def build_sector_rules(
    *,
    mass_law: str,
    mapping_seed: int,
    q: int,
    n_min: int,
    n_max: int,
    alpha: float,
    width_x: float,
    dos: str,
    operator: str,
    pmax: float,
    x_min: float,
    x_max: float,
    ohmic_power: float,
    x_edges: np.ndarray,
) -> dict[int, SectorRule]:
    sectors = build_energy_resolved_sectors(
        n_min=n_min,
        n_max=n_max,
        q=q,
        alpha=alpha,
        mass_law=mass_law,
        width_x=width_x,
        dos=dos,
        seed=mapping_seed,
    )
    transitions = build_transition_data(
        sectors=sectors,
        q=q,
        operator=operator,
        seed=mapping_seed,
        pmax=pmax,
        x_min=x_min,
        x_max=x_max,
        ohmic_power=ohmic_power,
    )
    rng = np.random.default_rng(mapping_seed + 900_000)
    rules: dict[int, SectorRule] = {}
    for n in range(n_min + 1, n_max + 1):
        high = sectors[n]
        low = sectors[n - 1]
        beta = beta_for_downward_step(high, low)
        hard_probs, hard_omega, hard_x, total_rate = hard_bin_stats(
            transitions.rates[n],
            transitions.omegas[n],
            beta,
            x_edges,
        )
        hdim = len(hard_probs)
        scrambled = rng.integers(0, low.dim, size=(high.dim, hdim), endpoint=False)
        noscramble = np.zeros((high.dim, hdim), dtype=int)
        for a in range(high.dim):
            for h in range(hdim):
                noscramble[a, h] = (a + h) % low.dim
        rules[n] = SectorRule(
            n=n,
            beta=beta,
            total_rate=total_rate,
            hard_probs=hard_probs,
            hard_mean_omega=hard_omega,
            hard_mean_x=hard_x,
            core_maps_scrambled=scrambled,
            core_maps_noscramble=noscramble,
        )
    return rules


def initial_state(n_max: int, q: int, seed: int) -> State:
    rng = np.random.default_rng(seed)
    dim = q**n_max
    raw = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    raw = raw / np.linalg.norm(raw)
    return {(n_max, a, (), ()): complex(raw[a]) for a in range(dim)}


def apply_emission(state: State, rule: SectorRule, mapping: str) -> State:
    maps = (
        rule.core_maps_scrambled
        if mapping == "scrambled"
        else rule.core_maps_noscramble
    )
    out: State = {}
    amplitudes = np.sqrt(rule.hard_probs)
    for (n, core, hard, soft), amp in state.items():
        if n != rule.n:
            raise ValueError(f"state contains sector {n}, expected {rule.n}")
        for h, branch_amp in enumerate(amplitudes):
            new_core = int(maps[core, h])
            # The soft label records the incoming core state and hard branch.
            # It is the minimal explicit register used here to keep columns
            # orthogonal after coarse-graining B_n -> B_{n-1}.
            soft_label = core * len(amplitudes) + h
            key = (n - 1, new_core, hard + (h,), soft + (soft_label,))
            out[key] = out.get(key, 0.0j) + amp * branch_amp
    norm = math.sqrt(sum(abs(amp) ** 2 for amp in out.values()))
    if norm <= 0.0:
        raise ValueError("state norm vanished")
    return {key: amp / norm for key, amp in out.items()}


def probabilities_by_hard(state: State, step_index: int, hdim: int) -> np.ndarray:
    probs = np.zeros(hdim, dtype=float)
    for (_n, _core, hard, _soft), amp in state.items():
        probs[hard[step_index]] += abs(amp) ** 2
    return normalize_probs(probs)


def entropy_from_probs(probs: Iterable[float]) -> float:
    vals = np.asarray([p for p in probs if p > 1e-15], dtype=float)
    if len(vals) == 0:
        return 0.0
    return float(-np.sum(vals * np.log(vals)))


def partition_label(
    key: StateKey,
    part: str,
    split: int,
) -> object:
    n, core, hard, soft = key
    if part == "core":
        return (n, core)
    if part == "full_radiation":
        return (hard, soft)
    if part == "early":
        return (hard[:split], soft[:split])
    if part == "late":
        return (hard[split:], soft[split:])
    if part == "core_late":
        return ((n, core), hard[split:], soft[split:])
    if part == "core_early":
        return ((n, core), hard[:split], soft[:split])
    raise ValueError(f"unknown partition: {part}")


def entropy_of_part(state: State, part: str, split: int) -> float:
    row_ids: dict[object, int] = {}
    col_ids: dict[object, int] = {}
    entries: list[tuple[int, int, complex]] = []
    complement = {
        "core": "full_radiation",
        "full_radiation": "core",
        "early": "core_late",
        "late": "core_early",
    }[part]
    for key, amp in state.items():
        row_label = partition_label(key, part, split)
        col_label = partition_label(key, complement, split)
        row = row_ids.setdefault(row_label, len(row_ids))
        col = col_ids.setdefault(col_label, len(col_ids))
        entries.append((row, col, amp))

    # Build the reduced Gram matrix on the smaller side when possible.
    if len(row_ids) <= len(col_ids):
        rho = np.zeros((len(row_ids), len(row_ids)), dtype=np.complex128)
        by_col: dict[int, list[tuple[int, complex]]] = {}
        for row, col, amp in entries:
            by_col.setdefault(col, []).append((row, amp))
        for col_entries in by_col.values():
            for row_i, amp_i in col_entries:
                for row_j, amp_j in col_entries:
                    rho[row_i, row_j] += amp_i * np.conjugate(amp_j)
    else:
        rho = np.zeros((len(col_ids), len(col_ids)), dtype=np.complex128)
        by_row: dict[int, list[tuple[int, complex]]] = {}
        for row, col, amp in entries:
            by_row.setdefault(row, []).append((col, amp))
        for row_entries in by_row.values():
            for col_i, amp_i in row_entries:
                for col_j, amp_j in row_entries:
                    rho[col_i, col_j] += np.conjugate(amp_i) * amp_j
    evals = np.linalg.eigvalsh(rho)
    evals = np.clip(np.real(evals), 0.0, 1.0)
    return entropy_from_probs(evals)


def log_core_support(state: State) -> float:
    support = {(n, core) for (n, core, _hard, _soft), amp in state.items() if abs(amp) > 1e-14}
    return math.log(len(support)) if support else 0.0


def run_case(args: argparse.Namespace, mass_law: str, mapping: str, seed: int) -> list[TrajectoryRow]:
    x_edges = np.asarray(args.x_edges, dtype=float)
    rules = build_sector_rules(
        mass_law=mass_law,
        mapping_seed=seed,
        q=args.q,
        n_min=args.n_min,
        n_max=args.n_max,
        alpha=args.alpha,
        width_x=args.width_x,
        dos=args.dos,
        operator=args.operator,
        pmax=args.pmax,
        x_min=args.x_min,
        x_max=args.x_max,
        ohmic_power=args.ohmic_power,
        x_edges=x_edges,
    )
    target_probs = target_x_distribution(x_edges, args.ohmic_power)
    state = initial_state(args.n_max, args.q, seed + 17)
    rows: list[TrajectoryRow] = []
    for step, n in enumerate(range(args.n_max, args.n_min, -1), start=1):
        rule = rules[n]
        state = apply_emission(state, rule, mapping)
        h_probs = probabilities_by_hard(state, step - 1, len(rule.hard_probs))
        mean_omega = float(np.sum(h_probs * rule.hard_mean_omega))
        mean_x = float(np.sum(h_probs * rule.hard_mean_x))
        tv = 0.5 * float(np.sum(np.abs(h_probs - target_probs)))
        split = step // 2
        s_full = entropy_of_part(state, "full_radiation", split)
        s_core = entropy_of_part(state, "core", split)
        s_early = entropy_of_part(state, "early", split)
        s_late = entropy_of_part(state, "late", split)
        rows.append(
            TrajectoryRow(
                mass_law=mass_law,
                mapping=mapping,
                seed=seed,
                step=step,
                n_before=n,
                n_after=n - 1,
                rate=rule.total_rate,
                mean_omega=mean_omega,
                power=rule.total_rate * mean_omega,
                mean_x=mean_x,
                spectrum_tv_to_thermal_x=tv,
                s_full_radiation=s_full,
                s_core=s_core,
                s_early=s_early,
                s_late=s_late,
                i_early_late=s_early + s_late - s_full,
                log_core_support=log_core_support(state),
                basis_terms=len(state),
            )
        )
    return rows


def write_rows(rows: list[TrajectoryRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(TrajectoryRow.__dataclass_fields__),  # type: ignore[attr-defined]
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def summarize(rows: list[TrajectoryRow]) -> list[dict[str, object]]:
    out = []
    groups = sorted({(row.mass_law, row.mapping, row.seed) for row in rows})
    for mass_law, mapping, seed in groups:
        group = [row for row in rows if row.mass_law == mass_law and row.mapping == mapping and row.seed == seed]
        first = group[0]
        mid = group[len(group) // 2]
        last = group[-1]
        out.append(
            {
                "mass_law": mass_law,
                "mapping": mapping,
                "seed": seed,
                "power_last_over_first": last.power / first.power,
                "power_mid_over_first": mid.power / first.power,
                "omega_last_over_first": last.mean_omega / first.mean_omega,
                "mean_tv": float(np.mean([row.spectrum_tv_to_thermal_x for row in group])),
                "max_s_full_radiation": max(row.s_full_radiation for row in group),
                "final_s_full_radiation": last.s_full_radiation,
                "final_i_early_late": last.i_early_late,
                "final_log_core_support": last.log_core_support,
                "final_basis_terms": last.basis_terms,
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run unified sector-isometry evaporator.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=2)
    parser.add_argument("--n-max", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--operator", default="scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--mappings", default="scrambled,noscramble")
    parser.add_argument("--dos", default="exponential")
    parser.add_argument("--width-x", type=float, default=4.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--x-min", type=float, default=0.0)
    parser.add_argument("--x-max", type=float, default=8.0)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--seeds", default="2468")
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument(
        "--trajectory-csv",
        type=Path,
        default=DATADIR / "unified_sector_isometry_trajectory.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=DATADIR / "unified_sector_isometry_summary.csv",
    )
    args = parser.parse_args(argv)

    mass_laws = parse_list(args.mass_laws, str)
    mappings = parse_list(args.mappings, str)
    seeds = parse_list(args.seeds, int)
    rows: list[TrajectoryRow] = []
    for mass_law in mass_laws:
        for mapping in mappings:
            for seed in seeds:
                print(f"[unified] {mass_law} mapping={mapping} seed={seed}", flush=True)
                rows.extend(run_case(args, mass_law, mapping, seed))

    write_rows(rows, args.trajectory_csv)
    summary_rows = summarize(rows)
    args.summary_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.summary_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"[unified] wrote {args.trajectory_csv}")
    print(f"[unified] wrote {args.summary_csv}")
    print("mass mapping      seed  P_last/P_first  TV    Srad_max Srad_final Iearlylate")
    for row in summary_rows:
        print(
            f"{row['mass_law']:6s} {row['mapping']:11s} {int(row['seed']):4d} "
            f"{float(row['power_last_over_first']):14.3f} "
            f"{float(row['mean_tv']):5.3f} "
            f"{float(row['max_s_full_radiation']):8.3f} "
            f"{float(row['final_s_full_radiation']):10.3f} "
            f"{float(row['final_i_early_late']):10.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
