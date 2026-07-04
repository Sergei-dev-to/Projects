#!/usr/bin/env python3
"""
Reduced-density simulation of the Hamiltonian shell evaporator.

For a collision unitary U on core x fresh-bin with the bin initialized in |0>,
the core evolves by Kraus operators

    K_a = <a| U |0>.

The global state remains pure, so the radiation Renyi-2 entropy equals the
core Renyi-2 entropy, -log Tr rho_core^2. This avoids explicit storage of the
emitted radiation history and allows longer multi-mode Hamiltonian tests.
"""
from __future__ import annotations

import argparse
import pathlib

import numpy as np
from numpy.typing import NDArray

from hamiltonian_shell_evaporator import (
    DATADIR,
    HamiltonianModel,
    build_hamiltonian_model,
    build_shell_model,
    complex_gaussian,
    shell_slice,
)


def kraus_from_unitary(ham: HamiltonianModel) -> list[NDArray[np.complex128]]:
    d_core = int(np.sum(ham.shell.dims))
    u4 = ham.unitary.reshape((d_core, ham.bin_dim, d_core, ham.bin_dim))
    return [u4[:, label, :, 0].copy() for label in range(ham.bin_dim)]


def core_probabilities(rho: NDArray[np.complex128], ham: HamiltonianModel) -> NDArray[np.float64]:
    probs = np.zeros(len(ham.shell.dims))
    diag = np.real(np.diag(rho))
    for shell in range(len(ham.shell.dims)):
        probs[shell] = float(np.sum(diag[shell_slice(ham.shell, shell)]))
    return probs


def run_one_seed(args: argparse.Namespace, seed: int) -> tuple[HamiltonianModel, dict[str, NDArray[np.float64]]]:
    shell = build_shell_model(
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        e_high=args.e_high,
        e_low=args.e_low,
        curvature=args.curvature,
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

    rng = np.random.default_rng(seed + 20_000)
    d_core = int(np.sum(shell.dims))
    d0 = int(shell.dims[0])
    psi0 = np.zeros((d_core, 1), dtype=np.complex128)
    initial = complex_gaussian(rng, (d0, 1))
    initial /= np.sqrt(float(np.vdot(initial, initial).real))
    psi0[shell_slice(shell, 0), :] = initial
    rho = psi0 @ psi0.conj().T

    shell_probs = []
    mean_energy = []
    emitted_power = []
    s2_core = []
    purity = []
    micro_s_at_mean = []
    emitted_probability = []
    norm_error = []
    previous_energy = None

    for step in range(args.steps + 1):
        probs = core_probabilities(rho, ham)
        energy = float(probs @ shell.energies)
        pur = float(np.einsum("ij,ji->", rho, rho).real)
        pur = max(pur, 1e-300)

        shell_probs.append(probs)
        mean_energy.append(energy)
        emitted_power.append(0.0 if previous_energy is None else previous_energy - energy)
        purity.append(pur)
        s2_core.append(-float(np.log(pur)))
        micro_s_at_mean.append(float(np.interp(energy, shell.energies[::-1], shell.entropy[::-1])))
        norm_error.append(abs(float(np.trace(rho).real) - 1.0))

        if step < args.steps:
            previous_energy = energy
            next_rho = np.zeros_like(rho)
            emitted = 0.0
            for label, k in enumerate(kraus):
                piece = k @ rho @ k.conj().T
                next_rho += piece
                if label > 0:
                    emitted += float(np.trace(piece).real)
            rho = (next_rho + next_rho.conj().T) / 2.0
            tr = float(np.trace(rho).real)
            if tr <= 0.0:
                raise FloatingPointError("density trace vanished")
            rho /= tr
            emitted_probability.append(emitted / tr)

    emitted_probability.append(0.0)
    return ham, {
        "shell_probs": np.asarray(shell_probs),
        "mean_energy": np.asarray(mean_energy),
        "emitted_power": np.asarray(emitted_power),
        "s2_rad": np.asarray(s2_core),
        "purity": np.asarray(purity),
        "micro_s_at_mean": np.asarray(micro_s_at_mean),
        "emitted_probability": np.asarray(emitted_probability),
        "norm_error": np.asarray(norm_error),
    }


def summarize(results: list[dict[str, NDArray[np.float64]]]) -> dict[str, float]:
    mean_energy = np.mean([r["mean_energy"] for r in results], axis=0)
    emitted_power = np.mean([r["emitted_power"] for r in results], axis=0)
    s2_rad = np.mean([r["s2_rad"] for r in results], axis=0)
    p_emit = np.mean([r["emitted_probability"] for r in results], axis=0)
    peak_idx = int(np.argmax(s2_rad))

    active = emitted_power[1:]
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]

    return {
        "initial_energy": float(mean_energy[0]),
        "final_energy": float(mean_energy[-1]),
        "peak_s2": float(s2_rad[peak_idx]),
        "peak_step": float(peak_idx),
        "accel_ratio_mid_over_early": float(np.mean(mid) / max(np.mean(early), 1e-300)),
        "mean_emitted_probability": float(np.mean(p_emit[:-1])),
        "max_norm_error": float(max(np.max(r["norm_error"]) for r in results)),
    }


def save_npz(
    outpath: pathlib.Path,
    ham: HamiltonianModel,
    results: list[dict[str, NDArray[np.float64]]],
    summary: dict[str, float],
    args: argparse.Namespace,
) -> None:
    stacked = {key: np.asarray([r[key] for r in results]) for key in results[0]}
    mean = {f"{key}_mean": np.mean(value, axis=0) for key, value in stacked.items()}
    std = {f"{key}_std": np.std(value, axis=0) for key, value in stacked.items()}
    np.savez(
        outpath,
        energies=ham.shell.energies,
        entropy=ham.shell.entropy,
        beta=ham.shell.beta,
        temperature=ham.shell.temperature,
        dims=ham.shell.dims,
        x_norms=ham.x_norms,
        gap=ham.gap,
        g=ham.g,
        dt=ham.dt,
        bin_dim=ham.bin_dim,
        steps=np.arange(args.steps + 1),
        seed0=args.seed,
        seeds=args.seeds,
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        curvature=args.curvature,
        channels=args.channels,
        chaos=args.chaos,
        detuning=args.detuning,
        **stacked,
        **mean,
        **std,
        **{f"summary_{key}": value for key, value in summary.items()},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run reduced-density Hamiltonian shell evaporator.")
    parser.add_argument("--shells", type=int, default=8)
    parser.add_argument("--dmax", type=int, default=32)
    parser.add_argument("--dmin", type=int, default=1)
    parser.add_argument("--e-high", type=float, default=8.0)
    parser.add_argument("--e-low", type=float, default=1.0)
    parser.add_argument("--curvature", type=float, default=3.0)
    parser.add_argument("--g", type=float, default=1.5)
    parser.add_argument("--dt", type=float, default=0.8)
    parser.add_argument("--chaos", type=float, default=0.0)
    parser.add_argument("--detuning", type=float, default=0.0)
    parser.add_argument("--channels", type=int, default=3)
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=8642)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_shell_density_channel.npz",
    )
    args = parser.parse_args(argv)

    results = []
    first_ham = None
    for i in range(args.seeds):
        seed = args.seed + i
        print(f"[ham-density] seed {seed} ({i + 1}/{args.seeds})")
        ham, result = run_one_seed(args, seed)
        if first_ham is None:
            first_ham = ham
            print("[ham-density] shell dimensions:", " ".join(str(int(d)) for d in ham.shell.dims))
            print("[ham-density] X norm schedule:", " ".join(f"{x:.3f}" for x in ham.x_norms))
            print(f"[ham-density] core dim={int(np.sum(ham.shell.dims))}, bin dim={ham.bin_dim}")
        results.append(result)

    assert first_ham is not None
    summary = summarize(results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_npz(args.output, first_ham, results, summary, args)
    print(f"[ham-density] wrote {args.output}")
    print("[ham-density] summary")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
