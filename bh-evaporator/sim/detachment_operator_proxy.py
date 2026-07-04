#!/usr/bin/env python3
"""Synthetic detachment-operator diagnostics.

This is a calibration harness for the Matrix detachment program.  It does not
simulate BFSS.  It implements the exact objects the BFSS calculation must
eventually produce:

    D[c, alpha] = <c|O_detach|alpha>
    A(omega)    = sum |D[c, alpha]|^2 delta(E_c - E_alpha - omega)
    G[c, c']    = sum_alpha D[c, alpha] conj(D[c', alpha])

The model choices generate controlled pass/fail cases for the two gates:
transition-operator spreading and channel-doorway Gram participation.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
from dataclasses import asdict, dataclass

import numpy as np
from numpy.typing import NDArray

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = ROOT / "sim" / "data"


@dataclass(frozen=True)
class Params:
    dim_initial: int = 96
    n_records: int = 4
    dim_daughter: int = 24
    dim_escape: int = 2
    model: str = "isotropic"
    seed: int = 1234
    omega0: float = 1.0
    envelope_width: float = 0.45
    spectral_bins: int = 32
    time_points: int = 400
    t_max: float = 80.0
    target_total_width: float = 1.0
    doorway_rank: int = 4
    scar_fraction: float = 0.08
    output_prefix: str = "detachment_proxy"

    @property
    def n_channels(self) -> int:
        return self.n_records * self.dim_daughter * self.dim_escape


def normalize_total_width(d: NDArray[np.complex128], target: float) -> NDArray[np.complex128]:
    total = float(np.sum(np.abs(d) ** 2))
    if total == 0.0:
        return d
    return d * np.sqrt(target / total)


def participation(vals: NDArray[np.float64], tol: float = 1e-14) -> float:
    vals = np.asarray(vals, dtype=float)
    vals = vals[vals > tol]
    if vals.size == 0:
        return 0.0
    return float((np.sum(vals) ** 2) / np.sum(vals * vals))


def make_energies(params: Params, rng: np.random.Generator) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.int64]]:
    e_initial = np.sort(rng.normal(loc=0.0, scale=1.0, size=params.dim_initial))

    record_energies = params.omega0 + 0.18 * np.arange(params.n_records)
    daughter_base = np.sort(rng.normal(loc=-0.15, scale=0.9, size=params.dim_daughter))
    escape_offsets = 0.04 * np.arange(params.dim_escape)

    e_channels = []
    record_labels = []
    for m, rec_e in enumerate(record_energies):
        for beta_e in daughter_base:
            for esc_e in escape_offsets:
                e_channels.append(beta_e + rec_e + esc_e + 0.03 * rng.normal())
                record_labels.append(m)
    return e_initial, np.asarray(e_channels), np.asarray(record_labels, dtype=np.int64)


def energy_envelope(e_initial: NDArray[np.float64], e_channels: NDArray[np.float64], params: Params) -> NDArray[np.float64]:
    omega = e_channels[:, None] - e_initial[None, :]
    return np.exp(-0.5 * ((omega - params.omega0) / params.envelope_width) ** 2)


def complex_normal(rng: np.random.Generator, shape: tuple[int, ...]) -> NDArray[np.complex128]:
    return (rng.normal(size=shape) + 1j * rng.normal(size=shape)) / np.sqrt(2.0)


def transition_matrix(
    params: Params,
    rng: np.random.Generator,
    e_initial: NDArray[np.float64],
    e_channels: NDArray[np.float64],
) -> NDArray[np.complex128]:
    n_c = params.n_channels
    n_i = params.dim_initial
    env = energy_envelope(e_initial, e_channels, params)

    if params.model == "isotropic":
        d = complex_normal(rng, (n_c, n_i)) * np.sqrt(env / max(n_i, 1))

    elif params.model == "aligned":
        # Common-doorway counterexample: all channels share the same alpha
        # vector.  The separable envelope keeps a smooth strength function while
        # preserving rank one in channel space.
        u = complex_normal(rng, (n_c,))
        v = complex_normal(rng, (n_i,))
        channel_weight = np.sqrt(np.mean(env, axis=1))
        initial_weight = np.sqrt(np.mean(env, axis=0))
        d = (u * channel_weight)[:, None] * (v * initial_weight)[None, :]

    elif params.model == "doorway_rank":
        rank = max(1, min(params.doorway_rank, n_c, n_i))
        u = complex_normal(rng, (n_c, rank))
        v = complex_normal(rng, (rank, n_i))
        d = (u @ v) * np.sqrt(env / max(rank * n_i, 1))

    elif params.model == "scarred":
        d = complex_normal(rng, (n_c, n_i)) * np.sqrt(env / max(n_i, 1))
        keep = max(1, int(round(params.scar_fraction * n_i)))
        mask = np.zeros(n_i, dtype=bool)
        mask[rng.choice(n_i, size=keep, replace=False)] = True
        d[:, ~mask] *= 0.02

    elif params.model == "record_blocked":
        # Channels from each emitted-record bin see a different block of initial
        # states.  This can have high total participation but fails if a diary
        # crosses those protected blocks.
        d = np.zeros((n_c, n_i), dtype=np.complex128)
        labels = np.repeat(np.arange(params.n_records), params.dim_daughter * params.dim_escape)
        block_edges = np.linspace(0, n_i, params.n_records + 1, dtype=int)
        for m in range(params.n_records):
            cols = slice(block_edges[m], block_edges[m + 1])
            rows = labels == m
            d[np.ix_(rows, np.arange(n_i)[cols])] = complex_normal(
                rng, (int(np.sum(rows)), block_edges[m + 1] - block_edges[m])
            )
        d *= np.sqrt(env / max(n_i, 1))

    else:
        raise ValueError(f"unknown model: {params.model}")

    return normalize_total_width(d, params.target_total_width)


def strength_histogram(
    d: NDArray[np.complex128],
    e_initial: NDArray[np.float64],
    e_channels: NDArray[np.float64],
    bins: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    omega = (e_channels[:, None] - e_initial[None, :]).ravel()
    weights = (np.abs(d) ** 2).ravel()
    lo, hi = np.quantile(omega, [0.01, 0.99])
    if hi <= lo:
        lo, hi = float(np.min(omega)), float(np.max(omega))
    hist, edges = np.histogram(omega, bins=bins, range=(float(lo), float(hi)), weights=weights)
    return hist.astype(float), edges.astype(float)


def correlator_metrics(
    d: NDArray[np.complex128],
    e_initial: NDArray[np.float64],
    e_channels: NDArray[np.float64],
    params: Params,
) -> dict[str, float]:
    omega = (e_channels[:, None] - e_initial[None, :]).ravel()
    weights = (np.abs(d) ** 2).ravel()
    total = float(np.sum(weights))
    if total <= 0.0:
        return {"c_long_mean": float("nan"), "c_min": float("nan"), "decay_time": float("nan")}
    weights = weights / total
    times = np.linspace(0.0, params.t_max, params.time_points)
    cvals = np.abs(np.exp(-1j * times[:, None] * omega[None, :]) @ weights)
    below = np.where(cvals < np.exp(-1.0))[0]
    decay_time = float(times[int(below[0])]) if below.size else float("nan")
    tail = cvals[len(cvals) // 2 :]
    return {
        "c_long_mean": float(np.mean(tail)),
        "c_min": float(np.min(cvals)),
        "decay_time": decay_time,
    }


def diagnostics(
    params: Params,
    d: NDArray[np.complex128],
    e_initial: NDArray[np.float64],
    e_channels: NDArray[np.float64],
) -> dict[str, float | str | int]:
    gamma_total = float(np.sum(np.abs(d) ** 2))
    hist, _edges = strength_histogram(d, e_initial, e_channels, params.spectral_bins)
    spectral_part = participation(hist)
    spectral_part_norm = spectral_part / max(np.count_nonzero(hist), 1)

    gram_channel = d @ d.conj().T
    gram_initial = d.conj().T @ d
    eig_c = np.linalg.eigvalsh(0.5 * (gram_channel + gram_channel.conj().T)).real
    eig_i = np.linalg.eigvalsh(0.5 * (gram_initial + gram_initial.conj().T)).real
    chan_part = participation(eig_c)
    init_part = participation(eig_i)

    corr = correlator_metrics(d, e_initial, e_channels, params)
    effective_rank_bound = min(params.n_channels, params.dim_initial)

    return {
        "model": params.model,
        "seed": params.seed,
        "dim_initial": params.dim_initial,
        "n_channels": params.n_channels,
        "gamma_total": gamma_total,
        "spectral_participation": spectral_part,
        "spectral_participation_norm": spectral_part_norm,
        "channel_gram_participation": chan_part,
        "channel_gram_participation_norm": chan_part / max(effective_rank_bound, 1),
        "initial_gram_participation": init_part,
        "initial_gram_participation_norm": init_part / max(effective_rank_bound, 1),
        "largest_channel_width_fraction": float(np.max(eig_c) / max(np.sum(eig_c), 1e-300)),
        **corr,
    }


def write_histogram(path: pathlib.Path, hist: NDArray[np.float64], edges: NDArray[np.float64]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["omega_lo", "omega_hi", "weight"])
        writer.writeheader()
        for lo, hi, weight in zip(edges[:-1], edges[1:], hist):
            writer.writerow({"omega_lo": lo, "omega_hi": hi, "weight": weight})


def parse_args() -> Params:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dim-initial", type=int, default=96)
    parser.add_argument("--n-records", type=int, default=4)
    parser.add_argument("--dim-daughter", type=int, default=24)
    parser.add_argument("--dim-escape", type=int, default=2)
    parser.add_argument(
        "--model",
        choices=["isotropic", "aligned", "doorway_rank", "scarred", "record_blocked"],
        default="isotropic",
    )
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--omega0", type=float, default=1.0)
    parser.add_argument("--envelope-width", type=float, default=0.45)
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=400)
    parser.add_argument("--t-max", type=float, default=80.0)
    parser.add_argument("--target-total-width", type=float, default=1.0)
    parser.add_argument("--doorway-rank", type=int, default=4)
    parser.add_argument("--scar-fraction", type=float, default=0.08)
    parser.add_argument("--output-prefix", default="detachment_proxy")
    args = parser.parse_args()
    return Params(**vars(args))


def main() -> None:
    params = parse_args()
    rng = np.random.default_rng(params.seed)
    e_initial, e_channels, _record_labels = make_energies(params, rng)
    d = transition_matrix(params, rng, e_initial, e_channels)
    diag = diagnostics(params, d, e_initial, e_channels)
    hist, edges = strength_histogram(d, e_initial, e_channels, params.spectral_bins)

    prefix = DATADIR / f"{params.output_prefix}_{params.model}_seed{params.seed}"
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix(".json")
    hist_path = prefix.with_name(prefix.name + "_strength.csv")
    json_path.write_text(json.dumps({"params": asdict(params), "diagnostics": diag}, indent=2))
    write_histogram(hist_path, hist, edges)

    for key, value in diag.items():
        if isinstance(value, float):
            print(f"{key}={value:.6g}")
        else:
            print(f"{key}={value}")
    print(f"wrote_json={json_path}")
    print(f"wrote_strength_csv={hist_path}")


if __name__ == "__main__":
    main()
