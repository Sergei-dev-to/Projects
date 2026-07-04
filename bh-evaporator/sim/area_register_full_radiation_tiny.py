#!/usr/bin/env python3
"""Tiny full-radiation diagnostic for the Track B area-register evaporator.

This is intentionally small. It keeps a sparse pure-state history with
explicit early and late radiation labels, so we can distinguish total
core-radiation entropy from early/late radiation correlations.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Hashable

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.sparse as sp
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from area_register_rate_scan import (
    AreaSector,
    build_rate_maps,
    build_sectors,
)
from scan_bose_hubbard_dos import DATADIR


History = tuple[tuple[int, int, int], ...]
StateKey = tuple[int, int, History, History]


@dataclass(frozen=True)
class Case:
    seed: int
    operator: str
    mass_law: str
    max_gap: float


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def initial_state(
    sectors: dict[int, AreaSector],
    n_max: int,
    seed: int,
) -> dict[StateKey, complex]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=sectors[n_max].dim) + 1j * rng.normal(size=sectors[n_max].dim)
    raw = raw / np.sqrt(float(np.vdot(raw, raw).real))
    return {
        (n_max, i, (), ()): complex(amp)
        for i, amp in enumerate(raw)
        if abs(amp) > 0.0
    }


def norm_state(state: dict[StateKey, complex]) -> float:
    return sum(float(abs(amp) ** 2) for amp in state.values())


def normalize_state(state: dict[StateKey, complex]) -> None:
    norm = norm_state(state)
    if norm <= 0.0:
        raise FloatingPointError("state norm vanished")
    scale = 1.0 / np.sqrt(norm)
    for key in list(state):
        state[key] *= scale


def evolve_step(
    state: dict[StateKey, complex],
    rates: dict[int, NDArray[np.float64]],
    split_step: int,
    step: int,
    amplitude_cutoff: float,
) -> dict[StateKey, complex]:
    next_state: defaultdict[StateKey, complex] = defaultdict(complex)
    for (n, i, early, late), amp in state.items():
        if n not in rates:
            next_state[(n, i, early, late)] += amp
            continue

        jump = rates[n][:, i]
        total_jump = float(np.sum(jump))
        stay = np.sqrt(max(1.0 - total_jump, 0.0))
        if abs(amp * stay) > amplitude_cutoff:
            next_state[(n, i, early, late)] += amp * stay

        for f, rate in enumerate(jump):
            if rate <= 0.0:
                continue
            jump_amp = amp * np.sqrt(float(rate))
            if abs(jump_amp) <= amplitude_cutoff:
                continue
            label = ((n, i, f),)
            if step < split_step:
                next_state[(n - 1, f, early + label, late)] += jump_amp
            else:
                next_state[(n - 1, f, early, late + label)] += jump_amp

    compact = dict(next_state)
    normalize_state(compact)
    return compact


def reduced_purity(
    state: dict[StateKey, complex],
    a_key: Callable[[StateKey], Hashable],
    b_key: Callable[[StateKey], Hashable],
) -> tuple[float, int]:
    a_index: dict[Hashable, int] = {}
    b_index: dict[Hashable, int] = {}
    rows = []
    cols = []
    data = []

    for key, amp in state.items():
        ak = a_key(key)
        bk = b_key(key)
        if ak not in a_index:
            a_index[ak] = len(a_index)
        if bk not in b_index:
            b_index[bk] = len(b_index)
        rows.append(a_index[ak])
        cols.append(b_index[bk])
        data.append(amp)

    psi = sp.coo_matrix(
        (np.asarray(data, dtype=np.complex128), (rows, cols)),
        shape=(len(a_index), len(b_index)),
    ).tocsr()
    rho = psi @ psi.conjugate().transpose()
    purity = float(np.sum(np.abs(rho.data) ** 2))
    return max(purity, 1e-300), len(a_index)


def renyi2_from_purity(purity: float) -> float:
    return -float(np.log(max(purity, 1e-300)))


def observables(
    sectors: dict[int, AreaSector],
    state: dict[StateKey, complex],
) -> dict[str, float]:
    energy = 0.0
    area = 0.0
    dimension_entropy = 0.0
    effective_dimension = 0.0
    for (n, i, _early, _late), amp in state.items():
        p = float(abs(amp) ** 2)
        energy += p * float(sectors[n].evals[i])
        area += p * float(n)
        dimension_entropy += p * sectors[n].entropy
        effective_dimension += p * sectors[n].dim

    core_purity, core_support = reduced_purity(
        state,
        a_key=lambda key: (key[0], key[1]),
        b_key=lambda key: (key[2], key[3]),
    )
    early_purity, early_support = reduced_purity(
        state,
        a_key=lambda key: key[2],
        b_key=lambda key: (key[0], key[1], key[3]),
    )
    late_purity, late_support = reduced_purity(
        state,
        a_key=lambda key: key[3],
        b_key=lambda key: (key[0], key[1], key[2]),
    )
    radiation_purity, radiation_support = reduced_purity(
        state,
        a_key=lambda key: (key[2], key[3]),
        b_key=lambda key: (key[0], key[1]),
    )

    s2_core = renyi2_from_purity(core_purity)
    s2_early = renyi2_from_purity(early_purity)
    s2_late = renyi2_from_purity(late_purity)
    s2_radiation = renyi2_from_purity(radiation_purity)
    return {
        "energy": energy,
        "area": area,
        "dimension_entropy": dimension_entropy,
        "effective_dimension": effective_dimension,
        "renyi2_core": s2_core,
        "renyi2_early": s2_early,
        "renyi2_late": s2_late,
        "renyi2_radiation": s2_radiation,
        "renyi2_early_late_mutual": s2_early + s2_late - s2_radiation,
        "core_support": float(core_support),
        "early_support": float(early_support),
        "late_support": float(late_support),
        "radiation_support": float(radiation_support),
        "branch_count": float(len(state)),
        "norm": norm_state(state),
    }


def summarize(result: dict[str, NDArray[np.float64]]) -> dict[str, float]:
    power = result["emitted_power"][1:]
    third = max(2, len(power) // 3)
    early = power[:third]
    mid = power[third : max(third + 1, 2 * len(power) // 3)]
    late = power[max(third + 1, 2 * len(power) // 3) :]
    return {
        "initial_energy": float(result["energy"][0]),
        "final_energy": float(result["energy"][-1]),
        "initial_area": float(result["area"][0]),
        "final_area": float(result["area"][-1]),
        "mean_power_early": float(np.mean(early)),
        "mean_power_mid": float(np.mean(mid)),
        "mean_power_late": float(np.mean(late)) if len(late) else float("nan"),
        "accel_ratio_mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "peak_renyi2_early_late_mutual": float(np.max(result["renyi2_early_late_mutual"])),
        "final_renyi2_early_late_mutual": float(result["renyi2_early_late_mutual"][-1]),
        "final_dimension_entropy": float(result["dimension_entropy"][-1]),
        "final_effective_dimension": float(result["effective_dimension"][-1]),
        "max_branch_count": float(np.max(result["branch_count"])),
        "max_norm_error": float(np.max(np.abs(result["norm"] - 1.0))),
    }


def run_case(args: argparse.Namespace, case: Case) -> tuple[dict[str, NDArray[np.float64]], dict[str, float]]:
    sectors = build_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        alpha=args.alpha,
        bandwidth=args.bandwidth,
        mass_law=case.mass_law,
        seed=case.seed,
    )
    rates = build_rate_maps(
        sectors,
        q=args.q,
        operator=case.operator,
        seed=case.seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=case.max_gap,
        ohmic_power=args.ohmic_power,
    )
    state = initial_state(sectors, args.n_max, case.seed + 70_000)

    records: dict[str, list[float]] = defaultdict(list)
    previous_energy = None
    for step in range(args.steps + 1):
        obs = observables(sectors, state)
        for key, value in obs.items():
            records[key].append(value)
        records["emitted_power"].append(
            0.0 if previous_energy is None else previous_energy - obs["energy"]
        )
        if step < args.steps:
            previous_energy = obs["energy"]
            state = evolve_step(
                state,
                rates=rates,
                split_step=args.split_step,
                step=step,
                amplitude_cutoff=args.amplitude_cutoff,
            )

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    summary = summarize(result)
    return result, summary


def save_case(
    path: pathlib.Path,
    args: argparse.Namespace,
    case: Case,
    result: dict[str, NDArray[np.float64]],
    summary: dict[str, float],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        path,
        q=args.q,
        n_min=args.n_min,
        n_max=args.n_max,
        alpha=args.alpha,
        bandwidth=args.bandwidth,
        pmax=args.pmax,
        min_gap=args.min_gap,
        ohmic_power=args.ohmic_power,
        steps=args.steps,
        split_step=args.split_step,
        amplitude_cutoff=args.amplitude_cutoff,
        seed=case.seed,
        operator=case.operator,
        mass_law=case.mass_law,
        max_gap=case.max_gap,
        **result,
        **{f"summary_{key}": value for key, value in summary.items()},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run tiny full-radiation area-register test.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=3)
    parser.add_argument("--n-max", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--operators", default="local,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--sqrt-max-gap", type=float, default=4.0)
    parser.add_argument("--linear-max-gap", type=float, default=12.0)
    parser.add_argument("--pmax", type=float, default=0.08)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=24)
    parser.add_argument("--split-step", type=int, default=12)
    parser.add_argument("--seeds", default="2468")
    parser.add_argument("--amplitude-cutoff", type=float, default=1e-14)
    parser.add_argument("--output-dir", type=pathlib.Path, default=DATADIR)
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "area_register_full_radiation_tiny_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = []
    operators = parse_list(args.operators, str)
    mass_laws = parse_list(args.mass_laws, str)
    seeds = parse_list(args.seeds, int)
    total = len(operators) * len(mass_laws) * len(seeds)
    count = 0
    for seed in seeds:
        for operator in operators:
            for mass_law in mass_laws:
                count += 1
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                case = Case(seed=seed, operator=operator, mass_law=mass_law, max_gap=max_gap)
                print(
                    f"[full-rad] {count}/{total}: seed={seed} "
                    f"operator={operator} mass={mass_law} gap={max_gap:g}",
                    flush=True,
                )
                result, summary = run_case(args, case)
                stem = (
                    f"area_register_full_radiation_tiny_"
                    f"{operator}_{mass_law}_seed{seed}.npz"
                )
                save_case(args.output_dir / stem, args, case, result, summary)
                row = {
                    "seed": seed,
                    "operator": operator,
                    "mass_law": mass_law,
                    "max_gap": max_gap,
                    **summary,
                }
                rows.append(row)

    args.summary_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with args.summary_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[full-rad] wrote {args.summary_csv}")
    for row in rows:
        print(
            "  "
            f"{row['operator']} {row['mass_law']}: "
            f"accel={row['accel_ratio_mid_over_early']:.3f}, "
            f"peak I2(E:L)={row['peak_renyi2_early_late_mutual']:.3g}, "
            f"branches={row['max_branch_count']:.0f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
