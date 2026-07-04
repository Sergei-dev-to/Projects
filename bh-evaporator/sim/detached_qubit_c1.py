#!/usr/bin/env python3
"""Option C1: deterministic detached-qubit radiation pilot.

The n-spin core loses one boundary qubit at each evaporation step. The detached
qubits are kept as explicit radiation time bins. This is a changing-bipartition
model, not the Track E transition-rate channel.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.linalg as la
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from scan_bose_hubbard_dos import DATADIR
from variable_length_spin_chain_pilot import (
    SpinSector,
    build_sectors,
)


@dataclass(frozen=True)
class Case:
    seed: int
    mass_law: str


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def random_initial_state(dim: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    return raw / np.sqrt(float(np.vdot(raw, raw).real))


def reorder_boundary_to_radiation(
    psi: NDArray[np.complex128],
    core_n: int,
    rad_n: int,
) -> NDArray[np.complex128]:
    """Move the last core qubit to the end of the radiation register.

    Input order is:

        core qubits, then existing radiation qubits

    Output order is:

        remaining core qubits, existing radiation qubits, emitted qubit
    """
    tensor = psi.reshape((2,) * (core_n + rad_n))
    axes = list(range(core_n - 1)) + list(range(core_n, core_n + rad_n)) + [core_n - 1]
    return np.transpose(tensor, axes).reshape(-1)


def reduced_purity_from_state(
    psi: NDArray[np.complex128],
    keep_axes: list[int],
    total_qubits: int,
) -> tuple[float, int]:
    keep_axes = list(keep_axes)
    trace_axes = [axis for axis in range(total_qubits) if axis not in keep_axes]
    tensor = psi.reshape((2,) * total_qubits)
    permuted = np.transpose(tensor, keep_axes + trace_axes)
    keep_dim = 2 ** len(keep_axes)
    trace_dim = 2 ** len(trace_axes)
    mat = permuted.reshape(keep_dim, trace_dim)
    rho = mat @ mat.conjugate().T
    purity = float(np.sum(np.abs(rho) ** 2))
    return max(purity, 1e-300), keep_dim


def renyi2(purity: float) -> float:
    return -float(np.log(max(purity, 1e-300)))


def core_energy(
    psi: NDArray[np.complex128],
    sector: SpinSector,
    core_n: int,
    rad_n: int,
) -> float:
    core_dim = 2**core_n
    rad_dim = 2**rad_n
    mat = psi.reshape(core_dim, rad_dim)
    rho_core = mat @ mat.conjugate().T
    h = sector.evecs @ np.diag(sector.evals) @ sector.evecs.T
    return float(np.trace(rho_core @ h).real)


def observables(
    psi: NDArray[np.complex128],
    sectors: dict[int, SpinSector],
    core_n: int,
    rad_n: int,
    split_rad: int,
) -> dict[str, float]:
    total = core_n + rad_n
    core_axes = list(range(core_n))
    early_axes = list(range(core_n, core_n + min(rad_n, split_rad)))
    late_axes = list(range(core_n + min(rad_n, split_rad), total))
    rad_axes = early_axes + late_axes

    core_purity, _ = reduced_purity_from_state(psi, core_axes, total)
    rad_purity, _ = reduced_purity_from_state(psi, rad_axes, total) if rad_axes else (1.0, 1)
    early_purity, _ = (
        reduced_purity_from_state(psi, early_axes, total) if early_axes else (1.0, 1)
    )
    late_purity, _ = (
        reduced_purity_from_state(psi, late_axes, total) if late_axes else (1.0, 1)
    )

    s2_core = renyi2(core_purity)
    s2_rad = renyi2(rad_purity)
    s2_early = renyi2(early_purity)
    s2_late = renyi2(late_purity)
    energy = core_energy(psi, sectors[core_n], core_n, rad_n)
    return {
        "core_n": float(core_n),
        "rad_n": float(rad_n),
        "energy": energy,
        "dimension_entropy": float(core_n * np.log(2.0)),
        "renyi2_core": s2_core,
        "renyi2_radiation": s2_rad,
        "renyi2_early": s2_early,
        "renyi2_late": s2_late,
        "renyi2_early_late_mutual": s2_early + s2_late - s2_rad,
        "norm": float(np.vdot(psi, psi).real),
    }


def summarize(result: dict[str, NDArray[np.float64]]) -> dict[str, float]:
    power = result["emitted_power"][1:]
    third = max(1, len(power) // 3)
    early = power[:third]
    mid = power[third : max(third + 1, 2 * len(power) // 3)]
    late = power[max(third + 1, 2 * len(power) // 3) :]
    return {
        "initial_energy": float(result["energy"][0]),
        "final_energy": float(result["energy"][-1]),
        "initial_core_n": float(result["core_n"][0]),
        "final_core_n": float(result["core_n"][-1]),
        "mean_power_early": float(np.mean(early)),
        "mean_power_mid": float(np.mean(mid)),
        "mean_power_late": float(np.mean(late)) if len(late) else float("nan"),
        "accel_ratio_mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
        "peak_renyi2_core": float(np.max(result["renyi2_core"])),
        "peak_renyi2_radiation": float(np.max(result["renyi2_radiation"])),
        "peak_renyi2_early_late_mutual": float(np.max(result["renyi2_early_late_mutual"])),
        "final_renyi2_early_late_mutual": float(result["renyi2_early_late_mutual"][-1]),
        "max_norm_error": float(np.max(np.abs(result["norm"] - 1.0))),
    }


def run_case(args: argparse.Namespace, case: Case) -> tuple[dict[str, NDArray[np.float64]], dict[str, float]]:
    sectors = build_sectors(args, case.mass_law, case.seed)
    psi = random_initial_state(sectors[args.n_max].dim, case.seed + 310_000)
    core_n = args.n_max
    rad_n = 0
    split_rad = args.steps // 2

    records: dict[str, list[float]] = {
        "core_n": [],
        "rad_n": [],
        "energy": [],
        "dimension_entropy": [],
        "renyi2_core": [],
        "renyi2_radiation": [],
        "renyi2_early": [],
        "renyi2_late": [],
        "renyi2_early_late_mutual": [],
        "norm": [],
        "emitted_power": [],
    }
    previous_energy = None

    for step in range(args.steps + 1):
        obs = observables(psi, sectors, core_n, rad_n, split_rad)
        for key in records:
            if key == "emitted_power":
                records[key].append(
                    0.0 if previous_energy is None else previous_energy - obs["energy"]
                )
            else:
                records[key].append(obs[key])

        if step < args.steps:
            if core_n <= args.n_min:
                previous_energy = obs["energy"]
                continue
            previous_energy = obs["energy"]
            psi = reorder_boundary_to_radiation(psi, core_n=core_n, rad_n=rad_n)
            core_n -= 1
            rad_n += 1

    result = {key: np.asarray(value, dtype=float) for key, value in records.items()}
    summary = {
        "seed": case.seed,
        "mass_law": case.mass_law,
        "n_min": args.n_min,
        "n_max": args.n_max,
        "steps": args.steps,
        **summarize(result),
    }
    return result, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run detached-qubit C1 pilot.")
    parser.add_argument("--n-min", type=int, default=2)
    parser.add_argument("--n-max", type=int, default=10)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--block-model", choices=["local", "random"], default="local")
    parser.add_argument("--jx", type=float, default=0.8)
    parser.add_argument("--jz", type=float, default=0.6)
    parser.add_argument("--hx", type=float, default=0.7)
    parser.add_argument("--hz-disorder", type=float, default=0.25)
    parser.add_argument("--mass-laws", default="sqrt,linear")
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--output-dir", type=pathlib.Path, default=DATADIR)
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "detached_qubit_c1_summary.csv",
    )
    args = parser.parse_args(argv)

    rows = []
    for seed in parse_list(args.seeds, int):
        for mass_law in parse_list(args.mass_laws, str):
            case = Case(seed=seed, mass_law=mass_law)
            print(f"[c1] seed={seed} mass={mass_law}", flush=True)
            result, summary = run_case(args, case)
            args.output_dir.mkdir(parents=True, exist_ok=True)
            stem = f"detached_qubit_c1_{mass_law}_seed{seed}.npz"
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

    print(f"[c1] wrote {args.summary_csv}")
    for row in rows:
        print(
            f"  {row['mass_law']} seed={row['seed']}: "
            f"accel={row['accel_ratio_mid_over_early']:.3f}, "
            f"peak S2core={row['peak_renyi2_core']:.3f}, "
            f"peak I2EL={row['peak_renyi2_early_late_mutual']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
