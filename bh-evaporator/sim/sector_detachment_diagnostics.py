#!/usr/bin/env python3
"""Hamiltonian-derived detachment diagnostics for a sector model.

This is the first non-synthetic execution of the detachment test.  It uses
explicit finite-dimensional sector Hamiltonians H_n and H_{n-1}, then builds

    D[c, alpha] = <beta, label|O_detach|alpha>

from concrete shrinkage/removal operators between the sectors.

It is not BFSS.  Its purpose is to test the diagnostics on transition
amplitudes derived from Hamiltonians and operators, with a real sector
transition matrix D.
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
    n: int = 8
    q: int = 2
    alpha: float = 8.0
    bandwidth: float = 0.25
    mass_law: str = "sqrt"
    operator: str = "local"
    seed: int = 2468
    omega0: float | None = None
    envelope_width: float = 0.8
    ohmic_power: float = 1.0
    min_gap: float = 0.0
    spectral_bins: int = 32
    time_points: int = 400
    t_max: float = 80.0
    target_total_width: float = 1.0
    doorway_rank: int = 4
    output_prefix: str = "sector_detachment"

    @property
    def dim_high(self) -> int:
        return int(self.q**self.n)

    @property
    def dim_low(self) -> int:
        return int(self.q ** (self.n - 1))


def mass(n: int, alpha: float, mass_law: str) -> float:
    if mass_law == "sqrt":
        return alpha * np.sqrt(float(n))
    if mass_law == "linear":
        return alpha * float(n)
    raise ValueError(f"unknown mass law: {mass_law}")


def random_symmetric(rng: np.random.Generator, dim: int) -> NDArray[np.float64]:
    raw = rng.normal(size=(dim, dim))
    mat = (raw + raw.T) / 2.0
    return mat / np.sqrt(float(dim))


def sector_hamiltonian(n: int, params: Params, rng: np.random.Generator) -> NDArray[np.float64]:
    dim = int(params.q**n)
    h = mass(n, params.alpha, params.mass_law) * np.eye(dim)
    if params.bandwidth > 0.0:
        h += params.bandwidth * random_symmetric(rng, dim)
    return 0.5 * (h + h.T)


def local_removal_ops(dim_high: int, dim_low: int, q: int) -> list[NDArray[np.float64]]:
    ops = []
    for label in range(q):
        op = np.zeros((dim_low, dim_high), dtype=float)
        for prefix in range(dim_low):
            col = prefix * q + label
            op[prefix, col] = 1.0
        ops.append(op)
    return ops


def scrambled_removal_ops(
    dim_high: int,
    dim_low: int,
    q: int,
    rng: np.random.Generator,
) -> list[NDArray[np.float64]]:
    ops = local_removal_ops(dim_high, dim_low, q)
    raw_h = rng.normal(size=(dim_high, dim_high))
    uh, _ = np.linalg.qr(raw_h)
    raw_l = rng.normal(size=(dim_low, dim_low))
    ul, _ = np.linalg.qr(raw_l)
    return [ul @ op @ uh.T for op in ops]


def aligned_removal_ops(
    dim_high: int,
    dim_low: int,
    q: int,
    rng: np.random.Generator,
) -> list[NDArray[np.float64]]:
    # Maximal common-doorway structure: all record labels couple through the
    # same rank-one transition direction.
    u = rng.normal(size=(dim_low,))
    v = rng.normal(size=(dim_high,))
    u /= max(float(np.linalg.norm(u)), 1e-300)
    v /= max(float(np.linalg.norm(v)), 1e-300)
    base = np.outer(u, v)
    return [base / np.sqrt(q) for _ in range(q)]


def low_rank_removal_ops(
    dim_high: int,
    dim_low: int,
    q: int,
    rank: int,
    rng: np.random.Generator,
) -> list[NDArray[np.float64]]:
    # Shared low-rank doorway subspace with record-dependent coefficients.
    rank = max(1, min(rank, dim_low, dim_high))
    u_raw = rng.normal(size=(dim_low, rank))
    v_raw = rng.normal(size=(dim_high, rank))
    u, _ = np.linalg.qr(u_raw)
    v, _ = np.linalg.qr(v_raw)
    ops = []
    for _label in range(q):
        coeff = rng.normal(size=rank)
        op = u @ np.diag(coeff) @ v.T
        op /= max(float(np.linalg.norm(op)), 1e-300)
        ops.append(op / np.sqrt(q))
    return ops


def normalize_total_width(d: NDArray[np.complex128], target: float) -> NDArray[np.complex128]:
    total = float(np.sum(np.abs(d) ** 2))
    if total == 0.0:
        return d
    return d * np.sqrt(target / total)


def participation(vals: NDArray[np.float64], tol: float = 1e-14, rtol: float = 1e-12) -> float:
    vals = np.asarray(vals, dtype=float)
    scale = float(np.max(np.abs(vals))) if vals.size else 0.0
    cutoff = rtol * scale if scale > 0.0 else tol
    vals = vals[vals > cutoff]
    if vals.size == 0:
        return 0.0
    return float((np.sum(vals) ** 2) / np.sum(vals * vals))


def build_transition(params: Params) -> tuple[NDArray[np.complex128], NDArray[np.float64], NDArray[np.float64], NDArray[np.int64]]:
    rng = np.random.default_rng(params.seed)
    h_high = sector_hamiltonian(params.n, params, rng)
    h_low = sector_hamiltonian(params.n - 1, params, rng)
    eval_high, evec_high = np.linalg.eigh(h_high)
    eval_low, evec_low = np.linalg.eigh(h_low)

    op_rng = np.random.default_rng(params.seed + 100_000)
    if params.operator == "local":
        ops = local_removal_ops(params.dim_high, params.dim_low, params.q)
    elif params.operator == "scrambled":
        ops = scrambled_removal_ops(params.dim_high, params.dim_low, params.q, op_rng)
    elif params.operator == "aligned":
        ops = aligned_removal_ops(params.dim_high, params.dim_low, params.q, op_rng)
    elif params.operator == "low_rank":
        ops = low_rank_removal_ops(
            params.dim_high,
            params.dim_low,
            params.q,
            params.doorway_rank,
            op_rng,
        )
    else:
        raise ValueError(f"unknown operator: {params.operator}")

    omega0 = params.omega0
    if omega0 is None:
        omega0 = mass(params.n, params.alpha, params.mass_law) - mass(params.n - 1, params.alpha, params.mass_law)

    rows = []
    channel_labels = []
    omega_all = []
    for label, op in enumerate(ops):
        op_e = evec_low.T @ op @ evec_high
        omega = eval_high[None, :] - eval_low[:, None]
        gap_mask = omega >= params.min_gap
        envelope = np.exp(-0.5 * ((omega - omega0) / params.envelope_width) ** 2)
        bath = np.where(gap_mask, np.maximum(omega, 0.0) ** params.ohmic_power, 0.0)
        weighted = op_e * np.sqrt(envelope * bath)
        rows.append(weighted)
        channel_labels.extend([label] * params.dim_low)
        omega_all.append(omega)

    d = np.vstack(rows).astype(np.complex128)
    d = normalize_total_width(d, params.target_total_width)
    return d, eval_high, np.tile(eval_low, params.q), np.asarray(channel_labels, dtype=np.int64)


def strength_histogram(
    d: NDArray[np.complex128],
    eval_high: NDArray[np.float64],
    eval_low_tiled: NDArray[np.float64],
    bins: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    omega = (eval_high[None, :] - eval_low_tiled[:, None]).ravel()
    weights = (np.abs(d) ** 2).ravel()
    active = weights > 0.0
    if not np.any(active):
        return np.zeros(bins), np.linspace(0.0, 1.0, bins + 1)
    lo, hi = np.quantile(omega[active], [0.01, 0.99])
    if hi <= lo:
        lo, hi = float(np.min(omega[active])), float(np.max(omega[active]))
    hist, edges = np.histogram(omega, bins=bins, range=(float(lo), float(hi)), weights=weights)
    return hist.astype(float), edges.astype(float)


def correlator_metrics(
    d: NDArray[np.complex128],
    eval_high: NDArray[np.float64],
    eval_low_tiled: NDArray[np.float64],
    params: Params,
) -> dict[str, float]:
    omega = (eval_high[None, :] - eval_low_tiled[:, None]).ravel()
    weights = (np.abs(d) ** 2).ravel()
    total = float(np.sum(weights))
    if total <= 0.0:
        return {"c_long_mean": float("nan"), "c_min": float("nan"), "decay_time": float("nan")}
    weights = weights / total
    times = np.linspace(0.0, params.t_max, params.time_points)
    cvals = np.abs(np.exp(-1j * times[:, None] * omega[None, :]) @ weights)
    below = np.where(cvals < np.exp(-1.0))[0]
    decay_time = float(times[int(below[0])]) if below.size else float("nan")
    return {
        "c_long_mean": float(np.mean(cvals[len(cvals) // 2 :])),
        "c_min": float(np.min(cvals)),
        "decay_time": decay_time,
    }


def diagnostics(
    params: Params,
    d: NDArray[np.complex128],
    eval_high: NDArray[np.float64],
    eval_low_tiled: NDArray[np.float64],
    channel_labels: NDArray[np.int64],
) -> dict[str, float | str | int]:
    hist, _edges = strength_histogram(d, eval_high, eval_low_tiled, params.spectral_bins)
    gram_c = d @ d.conj().T
    gram_i = d.conj().T @ d
    eig_c = np.linalg.eigvalsh(0.5 * (gram_c + gram_c.conj().T)).real
    eig_i = np.linalg.eigvalsh(0.5 * (gram_i + gram_i.conj().T)).real
    rank_bound = min(d.shape)
    record_labels = np.unique(channel_labels)
    record_map = np.zeros((record_labels.size, d.shape[0]), dtype=np.complex128)
    record_widths = np.zeros(record_labels.size, dtype=np.float64)
    for idx, label in enumerate(record_labels):
        rows = channel_labels == label
        record_map[idx, rows] = 1.0
        record_widths[idx] = float(np.trace(gram_c[np.ix_(rows, rows)]).real)
    record_gram = record_map @ gram_c @ record_map.conj().T
    eig_record = np.linalg.eigvalsh(0.5 * (record_gram + record_gram.conj().T)).real
    return {
        "n": params.n,
        "q": params.q,
        "operator": params.operator,
        "mass_law": params.mass_law,
        "bandwidth": params.bandwidth,
        "doorway_rank": params.doorway_rank,
        "seed": params.seed,
        "dim_high": params.dim_high,
        "dim_low": params.dim_low,
        "n_channels": int(d.shape[0]),
        "gamma_total": float(np.sum(np.abs(d) ** 2)),
        "spectral_participation": participation(hist),
        "spectral_participation_norm": participation(hist) / max(np.count_nonzero(hist), 1),
        "channel_gram_participation": participation(eig_c),
        "channel_gram_participation_norm": participation(eig_c) / max(rank_bound, 1),
        "initial_gram_participation": participation(eig_i),
        "initial_gram_participation_norm": participation(eig_i) / max(rank_bound, 1),
        "largest_channel_width_fraction": float(np.max(eig_c) / max(np.sum(eig_c), 1e-300)),
        "accessible_record_count": int(record_labels.size),
        "accessible_record_gram_participation": participation(eig_record),
        "accessible_record_gram_participation_norm": participation(eig_record) / max(record_labels.size, 1),
        "accessible_record_width_participation": participation(record_widths),
        "accessible_record_width_participation_norm": participation(record_widths) / max(record_labels.size, 1),
        "largest_accessible_record_width_fraction": float(
            np.max(record_widths) / max(np.sum(record_widths), 1e-300)
        ),
        **correlator_metrics(d, eval_high, eval_low_tiled, params),
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
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--bandwidth", type=float, default=0.25)
    parser.add_argument("--mass-law", choices=["sqrt", "linear"], default="sqrt")
    parser.add_argument(
        "--operator",
        choices=["local", "scrambled", "aligned", "low_rank"],
        default="local",
    )
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--omega0", type=float, default=None)
    parser.add_argument("--envelope-width", type=float, default=0.8)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--min-gap", type=float, default=0.0)
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=400)
    parser.add_argument("--t-max", type=float, default=80.0)
    parser.add_argument("--target-total-width", type=float, default=1.0)
    parser.add_argument("--doorway-rank", type=int, default=4)
    parser.add_argument("--output-prefix", default="sector_detachment")
    args = parser.parse_args()
    return Params(**vars(args))


def main() -> None:
    params = parse_args()
    d, eval_high, eval_low_tiled, labels = build_transition(params)
    diag = diagnostics(params, d, eval_high, eval_low_tiled, labels)
    hist, edges = strength_histogram(d, eval_high, eval_low_tiled, params.spectral_bins)

    bw_token = str(params.bandwidth).replace("-", "m").replace(".", "p")
    prefix = DATADIR / (
        f"{params.output_prefix}_{params.operator}_bw{bw_token}_"
        f"n{params.n}_seed{params.seed}"
    )
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
