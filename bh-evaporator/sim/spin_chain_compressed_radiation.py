#!/usr/bin/env python3
"""Compressed exact radiation diagnostic for the variable-length spin chain.

This keeps a sparse pure state over core states and early/late radiation
histories, but compresses each emitted quantum to an energy-bin label rather
than an exact transition label. It is a deliberate compromise between the tiny
exact full-radiation calculation and the purely classical trajectory sampler.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Hashable

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.sparse as sp
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from scan_bose_hubbard_dos import DATADIR
from variable_length_spin_chain_pilot import (
    SpinSector,
    build_rate_maps,
    build_sectors,
)


History = tuple[int, ...]
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
    sectors: dict[int, SpinSector],
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
    omegas: dict[int, NDArray[np.float64]],
    step: int,
    split_step: int,
    energy_bin_width: float,
    amplitude_cutoff: float,
    max_branches: int,
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

        nz = np.nonzero(jump > 0.0)[0]
        for f in nz:
            jump_amp = amp * np.sqrt(float(jump[f]))
            if abs(jump_amp) <= amplitude_cutoff:
                continue
            omega = float(max(omegas[n][f, i], 0.0))
            label = int(np.floor(omega / energy_bin_width + 1e-12))
            if step < split_step:
                next_state[(n - 1, f, early + (label,), late)] += jump_amp
            else:
                next_state[(n - 1, f, early, late + (label,))] += jump_amp

    compact = dict(next_state)
    if len(compact) > max_branches:
        raise MemoryError(f"branch cap exceeded: {len(compact)} > {max_branches}")
    normalize_state(compact)
    return compact


def reduced_purity(
    state: dict[StateKey, complex],
    a_key,
    b_key,
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


def renyi2(purity: float) -> float:
    return -float(np.log(max(purity, 1e-300)))


def observables(
    sectors: dict[int, SpinSector],
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

    s2_core = renyi2(core_purity)
    s2_early = renyi2(early_purity)
    s2_late = renyi2(late_purity)
    s2_radiation = renyi2(radiation_purity)
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
        "max_radiation_support": float(np.max(result["radiation_support"])),
        "max_norm_error": float(np.max(np.abs(result["norm"] - 1.0))),
    }


def run_case(args: argparse.Namespace, case: Case) -> tuple[dict[str, NDArray[np.float64]], dict[str, float]]:
    sectors = build_sectors(args, case.mass_law, case.seed)
    rates, omegas = build_rate_maps(
        sectors,
        operator=case.operator,
        seed=case.seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=case.max_gap,
        ohmic_power=args.ohmic_power,
    )
    state = initial_state(sectors, args.n_max, case.seed + 90_000)

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
                omegas=omegas,
                step=step,
                split_step=args.split_step,
                energy_bin_width=args.energy_bin_width,
                amplitude_cutoff=args.amplitude_cutoff,
                max_branches=args.max_branches,
            )

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    summary = {
        "seed": case.seed,
        "operator": case.operator,
        "mass_law": case.mass_law,
        "max_gap": case.max_gap,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "steps": args.steps,
        "energy_bin_width": args.energy_bin_width,
        **summarize(result),
    }
    return result, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run compressed exact spin-chain radiation test.")
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=7)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--block-model", choices=["local", "random"], default="local")
    parser.add_argument("--jx", type=float, default=0.8)
    parser.add_argument("--jz", type=float, default=0.6)
    parser.add_argument("--hx", type=float, default=0.7)
    parser.add_argument("--hz-disorder", type=float, default=0.25)
    parser.add_argument("--operators", default="boundary,scrambled")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--sqrt-max-gap", type=float, default=4.0)
    parser.add_argument("--linear-max-gap", type=float, default=12.0)
    parser.add_argument("--pmax", type=float, default=0.04)
    parser.add_argument("--min-gap", type=float, default=0.01)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--split-step", type=int, default=16)
    parser.add_argument("--seeds", default="2468")
    parser.add_argument("--energy-bin-width", type=float, default=1.0)
    parser.add_argument("--amplitude-cutoff", type=float, default=1e-12)
    parser.add_argument("--max-branches", type=int, default=2_000_000)
    parser.add_argument("--output-dir", type=pathlib.Path, default=DATADIR)
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "spin_chain_compressed_radiation_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = []
    total = len(parse_list(args.seeds, int)) * len(parse_list(args.operators, str)) * len(parse_list(args.mass_laws, str))
    count = 0
    for seed in parse_list(args.seeds, int):
        for operator in parse_list(args.operators, str):
            for mass_law in parse_list(args.mass_laws, str):
                count += 1
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                case = Case(seed=seed, operator=operator, mass_law=mass_law, max_gap=max_gap)
                print(
                    f"[compressed-rad] {count}/{total}: seed={seed} "
                    f"operator={operator} mass={mass_law}",
                    flush=True,
                )
                result, summary = run_case(args, case)
                stem = (
                    "spin_chain_compressed_radiation_"
                    f"{operator}_{mass_law}_seed{seed}.npz"
                )
                args.output_dir.mkdir(parents=True, exist_ok=True)
                np.savez(
                    args.output_dir / stem,
                    **result,
                    **{f"summary_{key}": value for key, value in summary.items()},
                )
                rows.append(summary)

    args.summary_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with args.summary_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[compressed-rad] wrote {args.summary_csv}")
    for row in rows:
        print(
            f"  {row['operator']} {row['mass_law']} seed={row['seed']}: "
            f"accel={row['accel_ratio_mid_over_early']:.3f}, "
            f"peak I2={row['peak_renyi2_early_late_mutual']:.3f}, "
            f"branches={row['max_branch_count']:.0f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
