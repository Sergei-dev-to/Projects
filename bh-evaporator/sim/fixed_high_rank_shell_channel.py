#!/usr/bin/env python3
"""
Fixed high-rank shell-channel probe.

This sits between the re-randomized shell-channel kill test and the fixed
Hamiltonian collision test. For each seed it pre-generates one Stinespring map
per shell and reuses those maps at every evaporation step. Each shell can emit
into several orthogonal labels, increasing the rank of the effective emission
map.
"""
from __future__ import annotations

import argparse
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


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
    emit_weight: NDArray[np.float64]
    nominal_emit_probability: NDArray[np.float64]


@dataclass(frozen=True)
class FixedMaps:
    bin_dim: int
    channels_per_shell: NDArray[np.int64]
    blocks: list[list[tuple[int, int, NDArray[np.complex128]]]]


def complex_gaussian(rng: np.random.Generator, shape: tuple[int, int]) -> NDArray[np.complex128]:
    out = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    return out / np.sqrt(2.0)


def inverse_sqrt_hermitian(mat: NDArray[np.complex128], floor: float = 1e-12) -> NDArray[np.complex128]:
    vals, vecs = np.linalg.eigh((mat + mat.conj().T) / 2.0)
    vals = np.maximum(vals.real, floor)
    return (vecs * (1.0 / np.sqrt(vals))) @ vecs.conj().T


def build_shell_model(
    shells: int,
    dmax: int,
    dmin: int,
    e_high: float,
    e_low: float,
    rate_scale: float,
    curvature: float,
) -> ShellModel:
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

    emit_weight = np.zeros(shells)
    nominal_emit_probability = np.zeros(shells)
    for m in range(shells - 1):
        ratio = float(np.exp(entropy[m + 1] - entropy[m]))
        emit_weight[m] = rate_scale * ratio
        nominal_emit_probability[m] = emit_weight[m] / (1.0 + emit_weight[m])

    return ShellModel(
        energies=energies,
        entropy=entropy,
        beta=beta,
        temperature=temperature,
        dims=dims,
        emit_weight=emit_weight,
        nominal_emit_probability=nominal_emit_probability,
    )


def choose_channels(
    dims: NDArray[np.int64],
    mode: str,
    fixed_channels: int,
    rank_factor: float,
    max_channels: int,
) -> NDArray[np.int64]:
    channels = np.zeros(len(dims) - 1, dtype=int)
    for m in range(len(dims) - 1):
        if mode == "fixed":
            channels[m] = fixed_channels
        elif mode == "rank":
            channels[m] = int(np.ceil(rank_factor * float(dims[m]) / float(max(dims[m + 1], 1))))
        else:
            raise ValueError(f"unknown channel mode: {mode}")
        channels[m] = max(1, min(max_channels, channels[m]))
    return channels


def build_fixed_maps(
    rng: np.random.Generator,
    model: ShellModel,
    channels_per_shell: NDArray[np.int64],
) -> FixedMaps:
    bin_dim = 1 + int(np.max(channels_per_shell))
    all_blocks: list[list[tuple[int, int, NDArray[np.complex128]]]] = []

    for shell, dim in enumerate(model.dims):
        d_in = int(dim)
        if shell == len(model.dims) - 1:
            raw = [complex_gaussian(rng, (d_in, d_in)) / np.sqrt(float(d_in))]
            targets = [(shell, 0)]
        else:
            m_channels = int(channels_per_shell[shell])
            raw = [complex_gaussian(rng, (d_in, d_in)) / np.sqrt(float(d_in))]
            targets = [(shell, 0)]
            d_next = int(model.dims[shell + 1])
            for label in range(1, m_channels + 1):
                block = (
                    np.sqrt(float(model.emit_weight[shell]) / float(m_channels))
                    * complex_gaussian(rng, (d_next, d_in))
                    / np.sqrt(float(d_next))
                )
                raw.append(block)
                targets.append((shell + 1, label))

        gram = np.zeros((d_in, d_in), dtype=np.complex128)
        for block in raw:
            gram += block.conj().T @ block
        norm = inverse_sqrt_hermitian(gram)
        all_blocks.append([(target, label, block @ norm) for (target, label), block in zip(targets, raw)])

    return FixedMaps(bin_dim=bin_dim, channels_per_shell=channels_per_shell, blocks=all_blocks)


def step_state(
    state: dict[int, NDArray[np.complex128]],
    model: ShellModel,
    maps: FixedMaps,
    rad_dim_old: int,
) -> tuple[dict[int, NDArray[np.complex128]], float]:
    rad_dim_new = maps.bin_dim * rad_dim_old
    new_state: dict[int, NDArray[np.complex128]] = {
        shell: np.zeros((int(dim), rad_dim_new), dtype=np.complex128)
        for shell, dim in enumerate(model.dims)
    }
    old_cols = np.arange(rad_dim_old)
    emitted_probability = 0.0

    for shell, amp in state.items():
        if amp.size == 0 or np.vdot(amp, amp).real < 1e-28:
            continue
        for target, label, block in maps.blocks[shell]:
            out = block @ amp
            new_state[target][:, old_cols * maps.bin_dim + label] += out
            if label > 0:
                emitted_probability += float(np.vdot(out, out).real)

    norm = np.sqrt(sum(float(np.vdot(amp, amp).real) for amp in new_state.values()))
    if norm <= 0.0:
        raise FloatingPointError("state norm vanished")
    for shell in list(new_state):
        new_state[shell] /= norm
        if np.vdot(new_state[shell], new_state[shell]).real < 1e-26:
            del new_state[shell]
    return new_state, emitted_probability / max(norm * norm, 1e-300)


def stack_state(
    state: dict[int, NDArray[np.complex128]],
    dims: NDArray[np.int64],
    rad_dim: int,
) -> NDArray[np.complex128]:
    rows = []
    for shell, dim in enumerate(dims):
        rows.append(state.get(shell, np.zeros((int(dim), rad_dim), dtype=np.complex128)))
    return np.vstack(rows)


def core_probabilities(state: dict[int, NDArray[np.complex128]], shells: int) -> NDArray[np.float64]:
    probs = np.zeros(shells)
    for shell, amp in state.items():
        probs[shell] = float(np.vdot(amp, amp).real)
    return probs


def renyi2_from_core_state(
    state: dict[int, NDArray[np.complex128]],
    dims: NDArray[np.int64],
    rad_dim: int,
) -> tuple[float, float]:
    psi = stack_state(state, dims, rad_dim)
    rho_core = psi @ psi.conj().T
    purity = float(np.einsum("ij,ji->", rho_core, rho_core).real)
    purity = max(purity, 1e-300)
    return -float(np.log(purity)), purity


def run_one_seed(args: argparse.Namespace, seed: int) -> tuple[ShellModel, FixedMaps, dict[str, NDArray[np.float64]]]:
    rng = np.random.default_rng(seed)
    model = build_shell_model(
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        e_high=args.e_high,
        e_low=args.e_low,
        rate_scale=args.rate_scale,
        curvature=args.curvature,
    )
    channels = choose_channels(
        model.dims,
        mode=args.channel_mode,
        fixed_channels=args.channels,
        rank_factor=args.rank_factor,
        max_channels=args.max_channels,
    )
    maps = build_fixed_maps(rng, model, channels)

    d0 = int(model.dims[0])
    initial = complex_gaussian(rng, (d0, 1))
    initial /= np.sqrt(float(np.vdot(initial, initial).real))
    state: dict[int, NDArray[np.complex128]] = {0: initial}

    rad_dim = 1
    shell_probs = []
    mean_energy = []
    emitted_power = []
    s2_rad = []
    purity = []
    log_rad_dim = []
    micro_s_at_mean = []
    emitted_probability = []
    previous_energy = None

    for step in range(args.steps + 1):
        probs = core_probabilities(state, len(model.dims))
        energy = float(probs @ model.energies)
        s2, pur = renyi2_from_core_state(state, model.dims, rad_dim)

        shell_probs.append(probs)
        mean_energy.append(energy)
        emitted_power.append(0.0 if previous_energy is None else previous_energy - energy)
        s2_rad.append(s2)
        purity.append(pur)
        log_rad_dim.append(float(np.log(rad_dim)))
        micro_s_at_mean.append(float(np.interp(energy, model.energies[::-1], model.entropy[::-1])))

        if step < args.steps:
            previous_energy = energy
            state, p_emit = step_state(state, model, maps, rad_dim)
            emitted_probability.append(p_emit)
            rad_dim *= maps.bin_dim

    emitted_probability.append(0.0)
    return model, maps, {
        "shell_probs": np.asarray(shell_probs),
        "mean_energy": np.asarray(mean_energy),
        "emitted_power": np.asarray(emitted_power),
        "s2_rad": np.asarray(s2_rad),
        "purity": np.asarray(purity),
        "log_rad_dim": np.asarray(log_rad_dim),
        "micro_s_at_mean": np.asarray(micro_s_at_mean),
        "emitted_probability": np.asarray(emitted_probability),
    }


def summarize(results: list[dict[str, NDArray[np.float64]]]) -> dict[str, float]:
    mean_energy = np.mean([r["mean_energy"] for r in results], axis=0)
    emitted_power = np.mean([r["emitted_power"] for r in results], axis=0)
    s2_rad = np.mean([r["s2_rad"] for r in results], axis=0)
    micro_s = np.mean([r["micro_s_at_mean"] for r in results], axis=0)
    log_rad = results[0]["log_rad_dim"]
    p_emit = np.mean([r["emitted_probability"] for r in results], axis=0)

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
        "mean_emitted_probability": float(np.mean(p_emit[:-1])),
    }


def save_npz(
    outpath: pathlib.Path,
    model: ShellModel,
    maps: FixedMaps,
    results: list[dict[str, NDArray[np.float64]]],
    summary: dict[str, float],
    args: argparse.Namespace,
) -> None:
    stacked = {key: np.asarray([r[key] for r in results]) for key in results[0]}
    mean = {f"{key}_mean": np.mean(value, axis=0) for key, value in stacked.items()}
    std = {f"{key}_std": np.std(value, axis=0) for key, value in stacked.items()}

    np.savez(
        outpath,
        energies=model.energies,
        entropy=model.entropy,
        beta=model.beta,
        temperature=model.temperature,
        dims=model.dims,
        emit_weight=model.emit_weight,
        nominal_emit_probability=model.nominal_emit_probability,
        channels_per_shell=maps.channels_per_shell,
        bin_dim=maps.bin_dim,
        steps=np.arange(args.steps + 1),
        seed0=args.seed,
        seeds=args.seeds,
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        rate_scale=args.rate_scale,
        curvature=args.curvature,
        channel_mode=args.channel_mode,
        rank_factor=args.rank_factor,
        max_channels=args.max_channels,
        **stacked,
        **mean,
        **std,
        **{f"summary_{key}": value for key, value in summary.items()},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the fixed high-rank shell-channel probe.")
    parser.add_argument("--shells", type=int, default=8)
    parser.add_argument("--dmax", type=int, default=32)
    parser.add_argument("--dmin", type=int, default=1)
    parser.add_argument("--e-high", type=float, default=8.0)
    parser.add_argument("--e-low", type=float, default=1.0)
    parser.add_argument("--rate-scale", type=float, default=1.8)
    parser.add_argument("--curvature", type=float, default=2.0)
    parser.add_argument("--steps", type=int, default=8)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--channel-mode", choices=["rank", "fixed"], default="rank")
    parser.add_argument("--channels", type=int, default=2)
    parser.add_argument("--rank-factor", type=float, default=1.0)
    parser.add_argument("--max-channels", type=int, default=3)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "fixed_high_rank_shell_channel.npz",
    )
    args = parser.parse_args(argv)

    results = []
    first_model = None
    first_maps = None
    for i in range(args.seeds):
        seed = args.seed + i
        print(f"[fixed-channel] seed {seed} ({i + 1}/{args.seeds})")
        model, maps, result = run_one_seed(args, seed)
        if first_model is None:
            first_model = model
            first_maps = maps
            print("[fixed-channel] shell dimensions:", " ".join(str(int(d)) for d in model.dims))
            print("[fixed-channel] channels:", " ".join(str(int(c)) for c in maps.channels_per_shell))
            print(f"[fixed-channel] bin dim={maps.bin_dim}")
            print(
                "[fixed-channel] nominal emission probabilities:",
                " ".join(f"{p:.3f}" for p in model.nominal_emit_probability[:-1]),
            )
        results.append(result)

    assert first_model is not None and first_maps is not None
    summary = summarize(results)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_npz(args.output, first_model, first_maps, results, summary, args)
    print(f"[fixed-channel] wrote {args.output}")
    print("[fixed-channel] summary")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
