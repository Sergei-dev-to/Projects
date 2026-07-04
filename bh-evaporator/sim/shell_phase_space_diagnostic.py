#!/usr/bin/env python3
"""Operator-W diagnostic for the Hamiltonian shell evaporator."""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from hamiltonian_shell_density_channel import kraus_from_unitary
from hamiltonian_shell_evaporator import (
    DATADIR,
    build_hamiltonian_model,
    build_shell_model,
    complex_gaussian,
    shell_slice,
)
from variable_n_bose_hubbard_evaporation import summarize


def summarize_series(values: NDArray[np.float64]) -> dict[str, float]:
    active = values[1:]
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]
    late = active[max(third + 1, 2 * len(active) // 3) :]
    return {
        "early": float(np.mean(early)),
        "mid": float(np.mean(mid)),
        "late": float(np.mean(late)) if len(late) else float("nan"),
        "mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
    }


def normalize_rho(rho: NDArray[np.complex128]) -> NDArray[np.complex128]:
    rho = (rho + rho.conj().T) / 2.0
    tr = float(np.trace(rho).real)
    if tr <= 0.0:
        raise FloatingPointError("density trace vanished")
    return rho / tr


def run_one(args: argparse.Namespace, curvature: float, seed: int) -> dict[str, NDArray[np.float64]]:
    shell = build_shell_model(
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        e_high=args.e_high,
        e_low=args.e_low,
        curvature=curvature,
    )
    ham = build_hamiltonian_model(
        shell=shell,
        seed=seed,
        g=args.g,
        dt=args.dt,
        chaos=args.chaos,
        detuning=args.detuning,
        channels=args.channels,
    )
    kraus = kraus_from_unitary(ham)
    d_core = int(np.sum(shell.dims))
    h_diag = shell.energies[shell.shell_of_core_index]
    h_core = np.diag(h_diag).astype(np.complex128)
    channel_h = np.zeros_like(h_core)
    for k in kraus:
        channel_h += k.conj().T @ h_core @ k
    w_op = h_core - channel_h

    rng = np.random.default_rng(seed + 20_000)
    psi = np.zeros((d_core, 1), dtype=np.complex128)
    initial = complex_gaussian(rng, (int(shell.dims[0]), 1))
    initial /= np.sqrt(float(np.vdot(initial, initial).real))
    psi[shell_slice(shell, 0), :] = initial
    rho = psi @ psi.conj().T

    records = {
        "energy": [],
        "emitted_power": [],
        "w_expectation": [],
        "emitted_probability": [],
        "s2_core": [],
    }
    previous_energy = None
    for step in range(args.steps + 1):
        energy = float(np.trace(rho @ h_core).real)
        w_expectation = float(np.trace(rho @ w_op).real)
        purity = max(float(np.trace(rho @ rho).real), 1e-300)
        records["energy"].append(energy)
        records["emitted_power"].append(0.0 if previous_energy is None else previous_energy - energy)
        records["w_expectation"].append(w_expectation)
        records["s2_core"].append(-float(np.log(purity)))

        if step < args.steps:
            previous_energy = energy
            next_rho = np.zeros_like(rho)
            emitted = 0.0
            for label, k in enumerate(kraus):
                piece = k @ rho @ k.conj().T
                next_rho += piece
                if label > 0:
                    emitted += float(np.trace(piece).real)
            records["emitted_probability"].append(emitted)
            rho = normalize_rho(next_rho)
    records["emitted_probability"].append(0.0)
    return {key: np.asarray(value, dtype=float) for key, value in records.items()}


def run_group(args: argparse.Namespace, label: str, curvature: float) -> dict[str, float | str]:
    runs = [run_one(args, curvature, args.seed + offset) for offset in range(args.seeds)]
    mean = {key: np.mean([run[key] for run in runs], axis=0) for key in runs[0]}
    power_summary = summarize_series(mean["emitted_power"])
    w_summary = summarize_series(mean["w_expectation"])
    return {
        "case": label,
        "curvature": curvature,
        "power_mid_over_early": power_summary["mid_over_early"],
        "w_mid_over_early": w_summary["mid_over_early"],
        "power_early": power_summary["early"],
        "power_mid": power_summary["mid"],
        "w_early": w_summary["early"],
        "w_mid": w_summary["mid"],
        "peak_s2_core": float(np.max(mean["s2_core"])),
        "final_energy": float(mean["energy"][-1]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run shell W diagnostic.")
    parser.add_argument("--shells", type=int, default=8)
    parser.add_argument("--dmax", type=int, default=32)
    parser.add_argument("--dmin", type=int, default=1)
    parser.add_argument("--e-high", type=float, default=8.0)
    parser.add_argument("--e-low", type=float, default=1.0)
    parser.add_argument("--convex-curvature", type=float, default=3.0)
    parser.add_argument("--linear-curvature", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=0.5)
    parser.add_argument("--dt", type=float, default=0.8)
    parser.add_argument("--chaos", type=float, default=0.0)
    parser.add_argument("--detuning", type=float, default=0.0)
    parser.add_argument("--channels", type=int, default=8)
    parser.add_argument("--steps", type=int, default=48)
    parser.add_argument("--seeds", type=int, default=4)
    parser.add_argument("--seed", type=int, default=8642)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "shell_phase_space_diagnostic.csv",
    )
    args = parser.parse_args(argv)

    rows = [
        run_group(args, "convex", args.convex_curvature),
        run_group(args, "linear", args.linear_curvature),
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[shell-W] wrote {args.output_csv}")
    for row in rows:
        print(
            f"  {row['case']}: power={row['power_mid_over_early']:.3f}, "
            f"W={row['w_mid_over_early']:.3f}, peakS2={row['peak_s2_core']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
