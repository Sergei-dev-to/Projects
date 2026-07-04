#!/usr/bin/env python3
"""
Dynamic shell evaporator kill test.

This script implements the first "Avenue 1" model: a shell-resolved finite
core whose emission channel is driven by the ratio of final to initial shell
degeneracies. The full state is evolved as a pure state over

    core shell x emitted binary time bins.

The radiation Renyi-2 entropy is computed from the complementary reduced core
state, not inserted by hand.
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
    emit_probability: NDArray[np.float64]


def build_shell_model(
    shells: int,
    dmax: int,
    dmin: int,
    e_high: float,
    e_low: float,
    rate_scale: float,
    curvature: float,
) -> ShellModel:
    """Build a convex entropy profile and the induced emission schedule."""
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
    # Enforce non-increasing dimensions as the core evaporates.
    for i in range(1, shells):
        dims[i] = min(dims[i], dims[i - 1])

    beta = np.gradient(entropy, energies)
    temperature = np.where(beta > 0, 1.0 / beta, np.inf)

    emit_weight = np.zeros(shells)
    emit_probability = np.zeros(shells)
    for m in range(shells - 1):
        # Density-of-states detailed-balance factor:
        # exp[S(E_next)-S(E_current)] = D_next / D_current in the
        # large-degeneracy approximation. As beta falls, this suppression weakens.
        degeneracy_ratio = float(np.exp(entropy[m + 1] - entropy[m]))
        emit_weight[m] = rate_scale * degeneracy_ratio
        emit_probability[m] = emit_weight[m] / (1.0 + emit_weight[m])

    return ShellModel(
        energies=energies,
        entropy=entropy,
        beta=beta,
        temperature=temperature,
        dims=dims,
        emit_weight=emit_weight,
        emit_probability=emit_probability,
    )


def complex_gaussian(rng: np.random.Generator, shape: tuple[int, int]) -> NDArray[np.complex128]:
    out = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    return out / np.sqrt(2.0)


def inverse_sqrt_hermitian(mat: NDArray[np.complex128], floor: float = 1e-12) -> NDArray[np.complex128]:
    vals, vecs = np.linalg.eigh((mat + mat.conj().T) / 2.0)
    vals = np.maximum(vals.real, floor)
    return (vecs * (1.0 / np.sqrt(vals))) @ vecs.conj().T


def channel_blocks(
    rng: np.random.Generator,
    dims: NDArray[np.int64],
    emit_weight: NDArray[np.float64],
    shell: int,
) -> list[tuple[int, int, NDArray[np.complex128]]]:
    """Return (target_shell, radiation_label, A) blocks satisfying sum A^dag A=I."""
    d_in = int(dims[shell])
    if shell == len(dims) - 1:
        raw = [complex_gaussian(rng, (d_in, d_in)) / np.sqrt(float(d_in))]
        targets = [(shell, 0)]
    else:
        d_next = int(dims[shell + 1])
        raw = [
            complex_gaussian(rng, (d_in, d_in)) / np.sqrt(float(d_in)),
            np.sqrt(float(emit_weight[shell]))
            * complex_gaussian(rng, (d_next, d_in))
            / np.sqrt(float(d_next)),
        ]
        targets = [(shell, 0), (shell + 1, 1)]

    gram = np.zeros((d_in, d_in), dtype=np.complex128)
    for block in raw:
        gram += block.conj().T @ block
    norm = inverse_sqrt_hermitian(gram)
    return [(target, label, block @ norm) for (target, label), block in zip(targets, raw)]


def stack_state(
    state: dict[int, NDArray[np.complex128]],
    dims: NDArray[np.int64],
    rad_dim: int,
) -> NDArray[np.complex128]:
    rows = []
    for shell, dim in enumerate(dims):
        if shell in state:
            rows.append(state[shell])
        else:
            rows.append(np.zeros((int(dim), rad_dim), dtype=np.complex128))
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


def step_state(
    rng: np.random.Generator,
    state: dict[int, NDArray[np.complex128]],
    model: ShellModel,
    rad_dim_old: int,
) -> dict[int, NDArray[np.complex128]]:
    rad_dim_new = 2 * rad_dim_old
    new_state: dict[int, NDArray[np.complex128]] = {
        shell: np.zeros((int(dim), rad_dim_new), dtype=np.complex128)
        for shell, dim in enumerate(model.dims)
    }
    old_cols = np.arange(rad_dim_old)

    for shell, amp in state.items():
        if amp.size == 0 or np.vdot(amp, amp).real < 1e-28:
            continue
        for target, label, block in channel_blocks(rng, model.dims, model.emit_weight, shell):
            out = block @ amp
            new_state[target][:, old_cols * 2 + label] += out

    norm = np.sqrt(sum(float(np.vdot(amp, amp).real) for amp in new_state.values()))
    if norm <= 0:
        raise FloatingPointError("state norm vanished")
    for shell in list(new_state):
        new_state[shell] /= norm
        if np.vdot(new_state[shell], new_state[shell]).real < 1e-26:
            del new_state[shell]
    return new_state


def run_one_seed(model: ShellModel, steps: int, seed: int) -> dict[str, NDArray[np.float64]]:
    rng = np.random.default_rng(seed)
    d0 = int(model.dims[0])
    initial = complex_gaussian(rng, (d0, 1))
    initial /= np.sqrt(np.vdot(initial, initial).real)
    state: dict[int, NDArray[np.complex128]] = {0: initial}

    rad_dim = 1
    shell_probs = []
    mean_energy = []
    mean_shell = []
    s2_rad = []
    purity = []
    log_rad_dim = []
    micro_s_at_mean = []

    for step in range(steps + 1):
        probs = core_probabilities(state, len(model.dims))
        shell_probs.append(probs)
        mean_energy.append(float(probs @ model.energies))
        mean_shell.append(float(probs @ np.arange(len(model.dims))))
        s2, pur = renyi2_from_core_state(state, model.dims, rad_dim)
        s2_rad.append(s2)
        purity.append(pur)
        log_rad_dim.append(float(np.log(rad_dim)))
        micro_s_at_mean.append(float(np.interp(mean_energy[-1], model.energies[::-1], model.entropy[::-1])))

        if step < steps:
            state = step_state(rng, state, model, rad_dim)
            rad_dim *= 2

    mean_energy_arr = np.asarray(mean_energy)
    emitted_power = np.zeros_like(mean_energy_arr)
    emitted_power[1:] = mean_energy_arr[:-1] - mean_energy_arr[1:]

    return {
        "shell_probs": np.asarray(shell_probs),
        "mean_energy": mean_energy_arr,
        "mean_shell": np.asarray(mean_shell),
        "emitted_power": emitted_power,
        "s2_rad": np.asarray(s2_rad),
        "purity": np.asarray(purity),
        "log_rad_dim": np.asarray(log_rad_dim),
        "micro_s_at_mean": np.asarray(micro_s_at_mean),
    }


def summarize(results: list[dict[str, NDArray[np.float64]]], model: ShellModel) -> dict[str, float]:
    mean_energy = np.mean([r["mean_energy"] for r in results], axis=0)
    emitted_power = np.mean([r["emitted_power"] for r in results], axis=0)
    s2_rad = np.mean([r["s2_rad"] for r in results], axis=0)
    micro_s = np.mean([r["micro_s_at_mean"] for r in results], axis=0)
    log_rad = results[0]["log_rad_dim"]

    peak_idx = int(np.argmax(s2_rad))
    crossing_idx = int(np.argmin(np.abs(log_rad - micro_s)))
    active = emitted_power[1:]
    early_window = active[: max(2, len(active) // 3)]
    late_window = active[max(2, len(active) // 3) : max(3, 2 * len(active) // 3)]
    accel_ratio = float(np.mean(late_window) / max(np.mean(early_window), 1e-300))

    shell_emit = model.emit_probability[:-1]
    emit_schedule_ratio = float(shell_emit[-1] / max(shell_emit[0], 1e-300))

    return {
        "initial_energy": float(mean_energy[0]),
        "final_energy": float(mean_energy[-1]),
        "peak_s2": float(s2_rad[peak_idx]),
        "peak_step": float(peak_idx),
        "dimension_crossing_step": float(crossing_idx),
        "accel_ratio_mid_over_early": accel_ratio,
        "emit_probability_ratio_lowE_over_highE": emit_schedule_ratio,
        "initial_emit_probability": float(shell_emit[0]),
        "late_emit_probability": float(shell_emit[-1]),
    }


def save_npz(
    outpath: pathlib.Path,
    model: ShellModel,
    results: list[dict[str, NDArray[np.float64]]],
    summary: dict[str, float],
    args: argparse.Namespace,
) -> None:
    stacked: dict[str, NDArray[np.float64]] = {}
    for key in results[0]:
        stacked[key] = np.asarray([r[key] for r in results])

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
        emit_probability=model.emit_probability,
        steps=np.arange(args.steps + 1),
        seed0=args.seed,
        seeds=args.seeds,
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        rate_scale=args.rate_scale,
        curvature=args.curvature,
        **stacked,
        **mean,
        **std,
        **{f"summary_{key}": value for key, value in summary.items()},
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the dynamic shell evaporator kill test.")
    parser.add_argument("--shells", type=int, default=8)
    parser.add_argument("--dmax", type=int, default=64)
    parser.add_argument("--dmin", type=int, default=1)
    parser.add_argument("--e-high", type=float, default=8.0)
    parser.add_argument("--e-low", type=float, default=1.0)
    parser.add_argument("--rate-scale", type=float, default=1.8)
    parser.add_argument("--curvature", type=float, default=2.0)
    parser.add_argument("--steps", type=int, default=15)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=DATADIR / "dynamic_shell_evaporator.npz",
    )
    args = parser.parse_args(argv)

    model = build_shell_model(
        shells=args.shells,
        dmax=args.dmax,
        dmin=args.dmin,
        e_high=args.e_high,
        e_low=args.e_low,
        rate_scale=args.rate_scale,
        curvature=args.curvature,
    )

    print("[dynamic] shell dimensions:", " ".join(str(int(d)) for d in model.dims))
    print("[dynamic] shell emit probabilities:", " ".join(f"{p:.3f}" for p in model.emit_probability[:-1]))

    results = []
    for i in range(args.seeds):
        seed = args.seed + i
        print(f"[dynamic] seed {seed} ({i + 1}/{args.seeds})")
        results.append(run_one_seed(model, args.steps, seed))

    summary = summarize(results, model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_npz(args.output, model, results, summary, args)
    print(f"[dynamic] wrote {args.output}")
    print("[dynamic] summary")
    for key, value in summary.items():
        print(f"  {key}: {value:.6g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
