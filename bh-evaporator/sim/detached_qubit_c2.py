#!/usr/bin/env python3
"""Option C2: energy-filtered detached-qubit radiation pilot."""
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
    import scipy.linalg as la
    import scipy.sparse as sp
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from scan_bose_hubbard_dos import DATADIR
from variable_length_spin_chain_pilot import (
    SpinSector,
    build_sectors,
    random_symmetric,
)


History = tuple[tuple[int, ...], ...]
StateKey = tuple[int, int, History, History]


@dataclass(frozen=True)
class Case:
    seed: int
    mass_law: str
    label_mode: str
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


def boundary_detach_ops(high: SpinSector, low: SpinSector) -> list[NDArray[np.float64]]:
    ops = []
    for b in range(2):
        op = np.zeros((low.dim, high.dim), dtype=float)
        for prefix in range(low.dim):
            op[prefix, prefix * 2 + b] = 1.0
        ops.append(op)
    return ops


def scrambled_detach_ops(
    high: SpinSector,
    low: SpinSector,
    seed: int,
) -> list[NDArray[np.float64]]:
    rng = np.random.default_rng(seed + 404_000 + high.n)
    raw_h = random_symmetric(rng, high.dim)
    raw_l = random_symmetric(rng, low.dim)
    uh = la.eigh(raw_h)[1]
    ul = la.eigh(raw_l)[1]
    return [ul @ op @ uh.T for op in boundary_detach_ops(high, low)]


def build_amplitude_maps(
    sectors: dict[int, SpinSector],
    operator: str,
    seed: int,
    pmax: float,
    min_gap: float,
    max_gap: float,
    ohmic_power: float,
) -> tuple[dict[int, NDArray[np.float64]], dict[int, NDArray[np.float64]]]:
    raw: dict[int, NDArray[np.float64]] = {}
    omegas: dict[int, NDArray[np.float64]] = {}
    for n in sorted(sectors):
        if n - 1 not in sectors:
            continue
        high = sectors[n]
        low = sectors[n - 1]
        if operator == "boundary":
            ops = boundary_detach_ops(high, low)
        elif operator == "scrambled":
            ops = scrambled_detach_ops(high, low, seed)
        else:
            raise ValueError(f"unknown operator: {operator}")

        omega = high.evals[None, None, :] - low.evals[None, :, None]
        mask = (omega >= min_gap) & (omega <= max_gap)
        weights = np.where(mask, np.maximum(omega, 0.0) ** ohmic_power, 0.0)
        rates = np.zeros((2, low.dim, high.dim), dtype=float)
        for b, op in enumerate(ops):
            op_e = low.evecs.T @ op @ high.evecs
            rates[b] = (np.abs(op_e) ** 2) * weights[0]
        raw[n] = rates
        omegas[n] = np.broadcast_to(omega, rates.shape)

    max_col = max(float(np.max(np.sum(rates, axis=(0, 1)))) for rates in raw.values())
    if max_col <= 0.0:
        raise ValueError("all C2 emission rates vanished")
    scaled = {n: rates * (pmax / max_col) for n, rates in raw.items()}
    return scaled, omegas


def norm_state(state: dict[StateKey, complex]) -> float:
    return sum(float(abs(amp) ** 2) for amp in state.values())


def normalize_state(state: dict[StateKey, complex]) -> None:
    norm = norm_state(state)
    if norm <= 0.0:
        raise FloatingPointError("state norm vanished")
    scale = 1.0 / np.sqrt(norm)
    for key in list(state):
        state[key] *= scale


def label_for(
    label_mode: str,
    step: int,
    n: int,
    i: int,
    f: int,
    b: int,
    energy_bin: int,
    no_emit: bool,
) -> tuple[int, ...]:
    if no_emit:
        return (step, 0, n)
    if label_mode == "exact":
        return (step, 1, n, i, f, b, energy_bin)
    if label_mode == "compressed":
        return (step, 1, n, b, energy_bin)
    raise ValueError(f"unknown label mode: {label_mode}")


def evolve_step(
    state: dict[StateKey, complex],
    rates: dict[int, NDArray[np.float64]],
    omegas: dict[int, NDArray[np.float64]],
    step: int,
    split_step: int,
    label_mode: str,
    energy_bin_width: float,
    amplitude_cutoff: float,
    max_branches: int,
) -> tuple[dict[StateKey, complex], float, float]:
    next_state: defaultdict[StateKey, complex] = defaultdict(complex)
    emitted_probability = 0.0
    emitted_power = 0.0

    for (n, i, early, late), amp in state.items():
        if n not in rates:
            label = label_for(label_mode, step, n, i, i, 0, 0, no_emit=True)
            if step < split_step:
                next_state[(n, i, early + (label,), late)] += amp
            else:
                next_state[(n, i, early, late + (label,))] += amp
            continue

        jump = rates[n][:, :, i]
        total_jump = float(np.sum(jump))
        p_source = float(abs(amp) ** 2)
        emitted_probability += p_source * total_jump
        emitted_power += p_source * float(np.sum(jump * omegas[n][:, :, i]))

        stay = np.sqrt(max(1.0 - total_jump, 0.0))
        no_label = label_for(label_mode, step, n, i, i, 0, 0, no_emit=True)
        if abs(amp * stay) > amplitude_cutoff:
            if step < split_step:
                next_state[(n, i, early + (no_label,), late)] += amp * stay
            else:
                next_state[(n, i, early, late + (no_label,))] += amp * stay

        nz = np.argwhere(jump > 0.0)
        for b, f in nz:
            rate = float(jump[b, f])
            jump_amp = amp * np.sqrt(rate)
            if abs(jump_amp) <= amplitude_cutoff:
                continue
            omega = float(max(omegas[n][b, f, i], 0.0))
            energy_bin = int(np.floor(omega / energy_bin_width + 1e-12))
            em_label = label_for(
                label_mode,
                step,
                n,
                i,
                int(f),
                int(b),
                energy_bin,
                no_emit=False,
            )
            if step < split_step:
                next_state[(n - 1, int(f), early + (em_label,), late)] += jump_amp
            else:
                next_state[(n - 1, int(f), early, late + (em_label,))] += jump_amp

    compact = dict(next_state)
    if len(compact) > max_branches:
        raise MemoryError(f"branch cap exceeded: {len(compact)} > {max_branches}")
    normalize_state(compact)
    return compact, emitted_probability, emitted_power


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
    return max(float(np.sum(np.abs(rho.data) ** 2)), 1e-300), len(a_index)


def renyi2(purity: float) -> float:
    return -float(np.log(max(purity, 1e-300)))


def observables(
    sectors: dict[int, SpinSector],
    state: dict[StateKey, complex],
    full_entropy: bool,
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
    s2_core = renyi2(core_purity)
    if full_entropy:
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

        s2_early = renyi2(early_purity)
        s2_late = renyi2(late_purity)
        s2_radiation = renyi2(radiation_purity)
        s2_mutual = s2_early + s2_late - s2_radiation
    else:
        early_support = late_support = radiation_support = 0
        s2_early = s2_late = s2_radiation = s2_mutual = float("nan")
    return {
        "energy": energy,
        "area": area,
        "dimension_entropy": dimension_entropy,
        "effective_dimension": effective_dimension,
        "renyi2_core": s2_core,
        "renyi2_early": s2_early,
        "renyi2_late": s2_late,
        "renyi2_radiation": s2_radiation,
        "renyi2_early_late_mutual": s2_mutual,
        "core_support": float(core_support),
        "early_support": float(early_support),
        "late_support": float(late_support),
        "radiation_support": float(radiation_support),
        "branch_count": float(len(state)),
        "norm": norm_state(state),
    }


def summarize(result: dict[str, NDArray[np.float64]]) -> dict[str, float]:
    power = result["emitted_power"][1:]
    gamma = result["emitted_probability"][1:]
    epsilon = result["conditional_energy"][1:]
    third = max(2, len(power) // 3)
    early = slice(0, third)
    mid = slice(third, max(third + 1, 2 * len(power) // 3))
    late = slice(max(third + 1, 2 * len(power) // 3), None)
    return {
        "initial_energy": float(result["energy"][0]),
        "final_energy": float(result["energy"][-1]),
        "initial_area": float(result["area"][0]),
        "final_area": float(result["area"][-1]),
        "mean_power_early": float(np.mean(power[early])),
        "mean_power_mid": float(np.mean(power[mid])),
        "mean_power_late": float(np.mean(power[late])) if len(power[late]) else float("nan"),
        "accel_ratio_mid_over_early": float(np.mean(power[mid]) / max(np.mean(power[early]), 1e-300)),
        "gamma_mid_over_early": float(np.mean(gamma[mid]) / max(np.mean(gamma[early]), 1e-300)),
        "epsilon_mid_over_early": float(np.mean(epsilon[mid]) / max(np.mean(epsilon[early]), 1e-300)),
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "peak_renyi2_early_late_mutual": float(np.nanmax(result["renyi2_early_late_mutual"])),
        "final_renyi2_early_late_mutual": float(result["renyi2_early_late_mutual"][-1]),
        "max_branch_count": float(np.max(result["branch_count"])),
        "max_norm_error": float(np.max(np.abs(result["norm"] - 1.0))),
    }


def run_case(args: argparse.Namespace, case: Case) -> tuple[dict[str, NDArray[np.float64]], dict[str, float]]:
    sectors = build_sectors(args, case.mass_law, case.seed)
    rates, omegas = build_amplitude_maps(
        sectors,
        operator=args.operator,
        seed=case.seed,
        pmax=args.pmax,
        min_gap=args.min_gap,
        max_gap=case.max_gap,
        ohmic_power=args.ohmic_power,
    )
    state = initial_state(sectors, args.n_max, case.seed + 510_000)

    records: dict[str, list[float]] = defaultdict(list)
    entropy_steps = {int(part) for part in args.entropy_steps.split(",") if part.strip()}
    entropy_steps.update({0, args.steps})
    for step in range(args.steps + 1):
        obs = observables(sectors, state, full_entropy=step in entropy_steps)
        for key, value in obs.items():
            records[key].append(value)
        if step == 0:
            records["emitted_probability"].append(0.0)
            records["emitted_power"].append(0.0)
            records["conditional_energy"].append(0.0)
        if step < args.steps:
            state, gamma, power = evolve_step(
                state,
                rates=rates,
                omegas=omegas,
                step=step,
                split_step=args.split_step,
                label_mode=case.label_mode,
                energy_bin_width=args.energy_bin_width,
                amplitude_cutoff=args.amplitude_cutoff,
                max_branches=args.max_branches,
            )
            records["emitted_probability"].append(gamma)
            records["emitted_power"].append(power)
            records["conditional_energy"].append(power / max(gamma, 1e-300))

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    summary = {
        "seed": case.seed,
        "operator": args.operator,
        "mass_law": case.mass_law,
        "label_mode": case.label_mode,
        "max_gap": case.max_gap,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "steps": args.steps,
        **summarize(result),
    }
    return result, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run C2 energy-filtered detached-qubit pilot.")
    parser.add_argument("--n-min", type=int, default=4)
    parser.add_argument("--n-max", type=int, default=7)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--block-model", choices=["local", "random"], default="local")
    parser.add_argument("--jx", type=float, default=0.8)
    parser.add_argument("--jz", type=float, default=0.6)
    parser.add_argument("--hx", type=float, default=0.7)
    parser.add_argument("--hz-disorder", type=float, default=0.25)
    parser.add_argument("--operator", choices=["boundary", "scrambled"], default="boundary")
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--label-modes", default="exact,compressed")
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
    parser.add_argument("--entropy-steps", default="")
    parser.add_argument("--output-dir", type=pathlib.Path, default=DATADIR)
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "detached_qubit_c2_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = []
    for seed in parse_list(args.seeds, int):
        for label_mode in parse_list(args.label_modes, str):
            for mass_law in parse_list(args.mass_laws, str):
                max_gap = args.sqrt_max_gap if mass_law == "sqrt" else args.linear_max_gap
                case = Case(seed=seed, mass_law=mass_law, label_mode=label_mode, max_gap=max_gap)
                print(
                    f"[c2] seed={seed} label={label_mode} mass={mass_law} op={args.operator}",
                    flush=True,
                )
                result, summary = run_case(args, case)
                args.output_dir.mkdir(parents=True, exist_ok=True)
                stem = f"detached_qubit_c2_{args.operator}_{label_mode}_{mass_law}_seed{seed}.npz"
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

    print(f"[c2] wrote {args.summary_csv}")
    for row in rows:
        print(
            f"  {row['label_mode']} {row['mass_law']}: "
            f"accel={row['accel_ratio_mid_over_early']:.3f}, "
            f"gamma={row['gamma_mid_over_early']:.3f}, "
            f"eps={row['epsilon_mid_over_early']:.3f}, "
            f"I2={row['peak_renyi2_early_late_mutual']:.3f}, "
            f"branches={row['max_branch_count']:.0f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
