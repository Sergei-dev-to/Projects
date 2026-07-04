#!/usr/bin/env python3
"""
Naive Hamiltonian shell evaporator.

This is the first collision-Hamiltonian version of the dynamic shell test.
It uses a fixed finite core Hamiltonian, a fresh binary radiation bin at each
step, and a fixed interaction that couples shell m with an empty bin to shell
m+1 with an occupied bin.
"""
from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.linalg as la
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required for Hamiltonian evolution: {exc}")


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = ROOT / "sim" / "data"
DATADIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class ShellModel:
    energies: NDArray[np.float64]
    entropy: NDArray[np.float64]
    beta: NDArray[np.float64]
    temperature: NDArray[np.float64]
    dims: NDArray[np.int64]
    offsets: NDArray[np.int64]
    shell_of_core_index: NDArray[np.int64]


@dataclass(frozen=True)
class HamiltonianModel:
    shell: ShellModel
    h_core: NDArray[np.complex128]
    h_bin: NDArray[np.complex128]
    h_int: NDArray[np.complex128]
    h_collision: NDArray[np.complex128]
    unitary: NDArray[np.complex128]
    x_norms: NDArray[np.float64]
    gap: float
    g: float
    dt: float
    bin_dim: int


def complex_gaussian(rng: np.random.Generator, shape: tuple[int, int]) -> NDArray[np.complex128]:
    out = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    return out / np.sqrt(2.0)


def random_hermitian(rng: np.random.Generator, dim: int) -> NDArray[np.complex128]:
    raw = complex_gaussian(rng, (dim, dim))
    herm = (raw + raw.conj().T) / 2.0
    scale = np.sqrt(max(dim, 1))
    return herm / scale


def build_shell_model(
    shells: int,
    dmax: int,
    dmin: int,
    e_high: float,
    e_low: float,
    curvature: float,
) -> ShellModel:
    if shells < 3:
        raise ValueError("shells must be at least 3")
    if dmax <= dmin:
        raise ValueError("dmax must be larger than dmin")
    if e_high <= e_low:
        raise ValueError("e_high must be larger than e_low")

    energies = np.linspace(e_high, e_low, shells)
    raw = energies**curvature
    raw = (raw - raw[-1]) / (raw[0] - raw[-1])
    entropy = np.log(float(dmin)) + raw * (np.log(float(dmax)) - np.log(float(dmin)))
    dims = np.maximum(dmin, np.rint(np.exp(entropy)).astype(int))
    dims[0] = dmax
    dims[-1] = dmin
    for i in range(1, shells):
        dims[i] = min(dims[i], dims[i - 1])

    beta = np.gradient(entropy, energies)
    temperature = np.where(beta > 0, 1.0 / beta, np.inf)
    offsets = np.concatenate(([0], np.cumsum(dims)[:-1])).astype(int)
    shell_of_core_index = np.concatenate(
        [np.full(int(dim), shell, dtype=int) for shell, dim in enumerate(dims)]
    )
    return ShellModel(
        energies=energies,
        entropy=entropy,
        beta=beta,
        temperature=temperature,
        dims=dims,
        offsets=offsets,
        shell_of_core_index=shell_of_core_index,
    )


def shell_slice(model: ShellModel, shell: int) -> slice:
    start = int(model.offsets[shell])
    return slice(start, start + int(model.dims[shell]))


def build_hamiltonian_model(
    shell: ShellModel,
    seed: int,
    g: float,
    dt: float,
    chaos: float,
    detuning: float,
    channels: int,
) -> HamiltonianModel:
    rng = np.random.default_rng(seed)
    d_core = int(np.sum(shell.dims))
    gap = float(shell.energies[0] - shell.energies[1])

    h_core = np.zeros((d_core, d_core), dtype=np.complex128)
    for m, energy in enumerate(shell.energies):
        sl = shell_slice(shell, m)
        h_core[sl, sl] += energy * np.eye(int(shell.dims[m]))
        if chaos > 0.0 and shell.dims[m] > 1:
            h_core[sl, sl] += chaos * random_hermitian(rng, int(shell.dims[m]))

    if channels < 1:
        raise ValueError("channels must be at least 1")
    bin_dim = 1 + int(channels)
    h_bin = np.diag([0.0] + [gap + detuning] * channels).astype(np.complex128)
    h_int = np.zeros((bin_dim * d_core, bin_dim * d_core), dtype=np.complex128)
    x_norms = np.zeros(len(shell.dims) - 1)

    for m in range(len(shell.dims) - 1):
        d_in = int(shell.dims[m])
        d_out = int(shell.dims[m + 1])
        x_norm_accum = 0.0
        in0 = shell_slice(shell, m)
        out1 = shell_slice(shell, m + 1)
        for channel in range(1, bin_dim):
            # This normalization makes the expected transition strength from a
            # typical vector scale as D_out / D_in per emitted channel, so
            # convex S(E) changes the emission schedule without shell-tuning g_m.
            x = complex_gaussian(rng, (d_out, d_in)) / np.sqrt(float(d_in))
            x_norm_accum += float(np.trace(x.conj().T @ x).real / d_in)
            for local_out, core_out in enumerate(range(out1.start, out1.stop)):
                row = bin_dim * core_out + channel
                for local_in, core_in in enumerate(range(in0.start, in0.stop)):
                    col = bin_dim * core_in + 0
                    val = g * x[local_out, local_in] / np.sqrt(float(channels))
                    h_int[row, col] += val
                    h_int[col, row] += np.conj(val)
        x_norms[m] = x_norm_accum / float(channels)

    h_collision = np.kron(h_core, np.eye(bin_dim, dtype=np.complex128)) + np.kron(
        np.eye(d_core, dtype=np.complex128), h_bin
    ) + h_int
    h_collision = (h_collision + h_collision.conj().T) / 2.0
    unitary = la.expm(-1j * dt * h_collision)

    return HamiltonianModel(
        shell=shell,
        h_core=h_core,
        h_bin=h_bin,
        h_int=h_int,
        h_collision=h_collision,
        unitary=unitary,
        x_norms=x_norms,
        gap=gap,
        g=g,
        dt=dt,
        bin_dim=bin_dim,
    )


def apply_collision(
    psi: NDArray[np.complex128],
    unitary: NDArray[np.complex128],
    bin_dim: int,
) -> NDArray[np.complex128]:
    d_core, old_rad_dim = psi.shape
    with_bin = np.zeros((d_core, bin_dim, old_rad_dim), dtype=np.complex128)
    with_bin[:, 0, :] = psi
    flat = with_bin.reshape((bin_dim * d_core, old_rad_dim))
    evolved = (unitary @ flat).reshape((d_core, bin_dim, old_rad_dim))

    out = np.zeros((d_core, bin_dim * old_rad_dim), dtype=np.complex128)
    for label in range(bin_dim):
        out[:, label::bin_dim] = evolved[:, label, :]
    norm = np.sqrt(float(np.vdot(out, out).real))
    if norm <= 0.0:
        raise FloatingPointError("state norm vanished")
    return out / norm


def core_probabilities(psi: NDArray[np.complex128], shell: ShellModel) -> NDArray[np.float64]:
    core_probs = np.sum(np.abs(psi) ** 2, axis=1)
    probs = np.zeros(len(shell.dims))
    for m in range(len(shell.dims)):
        probs[m] = float(np.sum(core_probs[shell_slice(shell, m)]))
    return probs


def renyi2_from_core(psi: NDArray[np.complex128]) -> tuple[float, float]:
    rho_core = psi @ psi.conj().T
    purity = float(np.einsum("ij,ji->", rho_core, rho_core).real)
    purity = max(purity, 1e-300)
    return -float(np.log(purity)), purity


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

    rng = np.random.default_rng(seed + 10_000)
    d0 = int(shell.dims[0])
    d_core = int(np.sum(shell.dims))
    psi = np.zeros((d_core, 1), dtype=np.complex128)
    initial = complex_gaussian(rng, (d0, 1))
    initial /= np.sqrt(float(np.vdot(initial, initial).real))
    psi[shell_slice(shell, 0), :] = initial

    shell_probs = []
    mean_energy = []
    emitted_power = []
    s2_rad = []
    purity = []
    log_rad_dim = []
    micro_s_at_mean = []
    bin1_probability = []
    norm_error = []

    previous_energy = None
    for step in range(args.steps + 1):
        probs = core_probabilities(psi, shell)
        energy = float(probs @ shell.energies)
        s2, pur = renyi2_from_core(psi)

        shell_probs.append(probs)
        mean_energy.append(energy)
        emitted_power.append(0.0 if previous_energy is None else previous_energy - energy)
        s2_rad.append(s2)
        purity.append(pur)
        log_rad_dim.append(float(np.log(psi.shape[1])))
        micro_s_at_mean.append(float(np.interp(energy, shell.energies[::-1], shell.entropy[::-1])))
        norm_error.append(abs(float(np.vdot(psi, psi).real) - 1.0))

        if step < args.steps:
            old_rad_dim = psi.shape[1]
            psi_next = apply_collision(psi, ham.unitary, ham.bin_dim)
            # Probability that the newly appended bin is occupied by any
            # emitted-channel label.
            emitted = 0.0
            for label in range(1, ham.bin_dim):
                emitted += float(np.sum(np.abs(psi_next[:, label::ham.bin_dim]) ** 2))
            bin1_probability.append(emitted)
            previous_energy = energy
            psi = psi_next

    bin1_probability.append(0.0)
    return ham, {
        "shell_probs": np.asarray(shell_probs),
        "mean_energy": np.asarray(mean_energy),
        "emitted_power": np.asarray(emitted_power),
        "s2_rad": np.asarray(s2_rad),
        "purity": np.asarray(purity),
        "log_rad_dim": np.asarray(log_rad_dim),
        "micro_s_at_mean": np.asarray(micro_s_at_mean),
        "bin1_probability": np.asarray(bin1_probability),
        "norm_error": np.asarray(norm_error),
    }


def summarize(results: list[dict[str, NDArray[np.float64]]]) -> dict[str, float]:
    mean_energy = np.mean([r["mean_energy"] for r in results], axis=0)
    emitted_power = np.mean([r["emitted_power"] for r in results], axis=0)
    s2_rad = np.mean([r["s2_rad"] for r in results], axis=0)
    micro_s = np.mean([r["micro_s_at_mean"] for r in results], axis=0)
    log_rad = results[0]["log_rad_dim"]
    bin1 = np.mean([r["bin1_probability"] for r in results], axis=0)

    peak_idx = int(np.argmax(s2_rad))
    crossing_idx = int(np.argmin(np.abs(log_rad - micro_s)))
    active = emitted_power[1:]
    third = max(2, len(active) // 3)
    early = active[:third]
    mid = active[third : max(third + 1, 2 * len(active) // 3)]
    accel_ratio = float(np.mean(mid) / max(np.mean(early), 1e-300))

    return {
        "initial_energy": float(mean_energy[0]),
        "final_energy": float(mean_energy[-1]),
        "peak_s2": float(s2_rad[peak_idx]),
        "peak_step": float(peak_idx),
        "dimension_crossing_step": float(crossing_idx),
        "accel_ratio_mid_over_early": accel_ratio,
        "mean_bin1_probability": float(np.mean(bin1[:-1])),
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
        chaos=args.chaos,
        detuning=args.detuning,
        channels=args.channels,
        **stacked,
        **mean,
        **std,
        **{f"summary_{key}": value for key, value in summary.items()},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the naive Hamiltonian shell evaporator.")
    parser.add_argument("--shells", type=int, default=8)
    parser.add_argument("--dmax", type=int, default=64)
    parser.add_argument("--dmin", type=int, default=1)
    parser.add_argument("--e-high", type=float, default=8.0)
    parser.add_argument("--e-low", type=float, default=1.0)
    parser.add_argument("--curvature", type=float, default=2.0)
    parser.add_argument("--g", type=float, default=0.9)
    parser.add_argument("--dt", type=float, default=0.8)
    parser.add_argument("--chaos", type=float, default=0.0)
    parser.add_argument("--detuning", type=float, default=0.0)
    parser.add_argument("--channels", type=int, default=1, help="Number of emitted labels besides |0>")
    parser.add_argument("--steps", type=int, default=15)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=4321)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_shell_evaporator.npz",
    )
    args = parser.parse_args(argv)

    results = []
    first_ham: HamiltonianModel | None = None
    for i in range(args.seeds):
        seed = args.seed + i
        print(f"[ham] seed {seed} ({i + 1}/{args.seeds})")
        ham, result = run_one_seed(args, seed)
        if first_ham is None:
            first_ham = ham
            print("[ham] shell dimensions:", " ".join(str(int(d)) for d in ham.shell.dims))
            print("[ham] X norm schedule:", " ".join(f"{x:.3f}" for x in ham.x_norms))
            print(
                f"[ham] core dim={int(np.sum(ham.shell.dims))}, "
                f"bin dim={ham.bin_dim}, collision dim={ham.unitary.shape[0]}"
            )
        results.append(result)

    assert first_ham is not None
    summary = summarize(results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_npz(args.output, first_ham, results, summary, args)
    print(f"[ham] wrote {args.output}")
    print("[ham] summary")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
