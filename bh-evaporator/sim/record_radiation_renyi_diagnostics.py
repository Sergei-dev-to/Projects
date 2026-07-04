#!/usr/bin/env python3
"""Record-carrying autonomous parent with second Renyi diagnostics.

The matrix-free sector parent measures shrinkage, energy conservation, and the
instantaneous radiation spectrum.  This variant adds two ingredients needed for
information-flow diagnostics:

1. radiation is stored on a short outgoing chain, so different spatial regions
   can be treated as early/late radiation records;
2. the initial core is purified by an inert reference system, so we can measure
   where information about the initial state goes.

The Hamiltonian remains time independent.  Emission couples the core to the
first radiation site, radiation hops along the chain, and scrambling acts
inside each fixed-n core sector.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import time as walltime
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import scipy.sparse.linalg as spla
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_energy_resolved import (
    beta_for_downward_step,
    build_energy_resolved_sectors,
)


@dataclass(frozen=True)
class BasisState:
    n: int
    a: int
    rad: int


@dataclass(frozen=True)
class ChainModel:
    basis: list[BasisState]
    index: dict[BasisState, int]
    energies: NDArray[np.float64]
    sector_of: NDArray[np.int64]
    rad_energy_of: NDArray[np.float64]
    rad_tuple_of: list[tuple[int, ...]]
    edge_src: NDArray[np.int64]
    edge_dst: NDArray[np.int64]
    edge_amp: NDArray[np.float64]
    mode_omega: NDArray[np.float64]
    mode_x: NDArray[np.float64]
    trace: float
    n_min: int
    n_max: int
    q: int
    slot_count: int
    mode_count: int


def parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def progress(args: argparse.Namespace, message: str) -> None:
    if not args.quiet:
        print(message, flush=True)


def encode_rad(values: tuple[int, ...], base: int) -> int:
    code = 0
    factor = 1
    for value in values:
        code += int(value) * factor
        factor *= base
    return code


def decode_rad(code: int, slot_count: int, base: int) -> tuple[int, ...]:
    values = []
    raw = int(code)
    for _ in range(slot_count):
        values.append(raw % base)
        raw //= base
    return tuple(values)


def rad_popcount(values: tuple[int, ...]) -> int:
    return sum(1 for value in values if value != 0)


def rad_energy(values: tuple[int, ...], mode_omega: NDArray[np.float64]) -> float:
    total = 0.0
    for value in values:
        if value:
            total += float(mode_omega[value - 1])
    return total


def radiation_codes(slot_count: int, mode_count: int, max_quanta: int) -> list[int]:
    base = mode_count + 1
    out = []
    for values in itertools.product(range(base), repeat=slot_count):
        if rad_popcount(values) <= max_quanta:
            out.append(encode_rad(values, base))
    return out


def build_radiation_modes(
    sectors: dict[int, Any],
    n_max: int,
    mode_x: list[float],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    beta = beta_for_downward_step(sectors[n_max], sectors[n_max - 1])
    xs = np.asarray(mode_x, dtype=float)
    return xs / beta, xs


def random_sparse_symmetric_edges(
    dim: int,
    degree: int,
    strength: float,
    rng: np.random.Generator,
) -> list[tuple[int, int, float]]:
    if dim <= 1 or degree <= 0 or strength <= 0.0:
        return []
    edges: dict[tuple[int, int], float] = {}
    for src in range(dim):
        targets = rng.choice(dim - 1, size=min(degree, dim - 1), replace=False)
        for raw in targets:
            dst = int(raw)
            if dst >= src:
                dst += 1
            a, b = sorted((src, dst))
            if (a, b) not in edges:
                edges[(a, b)] = strength * rng.normal() / math.sqrt(float(degree))
    return [(a, b, amp) for (a, b), amp in edges.items()]


def build_model(args: argparse.Namespace) -> ChainModel:
    progress(
        args,
        f"[build {args.case_name}] sectors n={args.n_min}..{args.n_max} "
        f"q={args.q} slots={args.slot_count} max_quanta={args.max_quanta}",
    )
    sectors = build_energy_resolved_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        alpha=args.alpha,
        mass_law=args.mass_law,
        width_x=args.width_x,
        dos=args.dos,
        seed=args.seed,
    )
    mode_x = parse_float_list(args.mode_x)
    mode_omega, mode_x_arr = build_radiation_modes(sectors, args.n_max, mode_x)
    mode_count = len(mode_omega)
    base = mode_count + 1
    rad_codes = radiation_codes(args.slot_count, mode_count, args.max_quanta)
    rad_tuples = {code: decode_rad(code, args.slot_count, base) for code in rad_codes}
    progress(
        args,
        f"[build {args.case_name}] modes={mode_count} rad_configs={len(rad_codes)}",
    )

    basis = [
        BasisState(n, a, rad)
        for n in range(args.n_min, args.n_max + 1)
        for rad in rad_codes
        for a in range(sectors[n].dim)
    ]
    index = {state: idx for idx, state in enumerate(basis)}
    progress(args, f"[build {args.case_name}] basis_dim={len(basis)}")

    energies = np.zeros(len(basis), dtype=float)
    sector_of = np.zeros(len(basis), dtype=np.int64)
    rad_energy_of = np.zeros(len(basis), dtype=float)
    rad_tuple_of: list[tuple[int, ...]] = []
    for idx, state in enumerate(basis):
        values = rad_tuples[state.rad]
        re = rad_energy(values, mode_omega)
        energies[idx] = sectors[state.n].evals[state.a] + re
        sector_of[idx] = state.n
        rad_energy_of[idx] = re
        rad_tuple_of.append(values)

    edges: list[tuple[int, int, float]] = []

    if args.scramble_strength > 0.0 and args.scramble_degree > 0:
        before = len(edges)
        for n in range(args.n_min, args.n_max + 1):
            local = random_sparse_symmetric_edges(
                sectors[n].dim,
                args.scramble_degree,
                args.scramble_strength,
                np.random.default_rng(args.seed + 20_000 + n),
            )
            for rad in rad_codes:
                for a, b, amp in local:
                    edges.append(
                        (
                            index[BasisState(n, a, rad)],
                            index[BasisState(n, b, rad)],
                            amp,
                        )
                    )
        progress(args, f"[build {args.case_name}] scramble_edges={len(edges) - before}")

    if args.hop_strength > 0.0:
        before = len(edges)
        for state in basis:
            values = rad_tuples[state.rad]
            for site in range(args.slot_count - 1):
                if values[site] == 0 or values[site + 1] != 0:
                    continue
                moved = list(values)
                moved[site + 1] = moved[site]
                moved[site] = 0
                dst = index.get(BasisState(state.n, state.a, encode_rad(tuple(moved), base)))
                if dst is not None:
                    edges.append((index[state], dst, args.hop_strength))
        progress(args, f"[build {args.case_name}] hop_edges={len(edges) - before}")

    rng = np.random.default_rng(args.seed + 10_000)
    for n in range(args.n_min + 1, args.n_max + 1):
        before = len(edges)
        high = sectors[n]
        low = sectors[n - 1]
        beta = beta_for_downward_step(high, low)
        for rad in rad_codes:
            values = rad_tuples[rad]
            if values[0] != 0 or rad_popcount(values) >= args.max_quanta:
                continue
            for a in range(high.dim):
                src = index[BasisState(n, a, rad)]
                for mode, omega_rad in enumerate(mode_omega, start=1):
                    emitted = list(values)
                    emitted[0] = mode
                    rad_new = encode_rad(tuple(emitted), base)
                    sample_count = min(args.emission_degree, low.dim)
                    targets = rng.choice(low.dim, size=sample_count, replace=False)
                    for raw in targets:
                        b = int(raw)
                        omega_core = float(high.evals[a] - low.evals[b])
                        detuning_x = beta * (omega_core - float(omega_rad))
                        envelope = math.exp(-0.5 * (detuning_x / args.detuning_width_x) ** 2)
                        if envelope <= args.matrix_cutoff:
                            continue
                        sign = rng.choice([-1.0, 1.0])
                        amp = (
                            args.emission_coupling
                            * sign
                            * (max(float(omega_rad), 0.0) ** (0.5 * args.ohmic_power))
                            * envelope
                            / math.sqrt(float(sample_count))
                        )
                        dst = index.get(BasisState(n - 1, b, rad_new))
                        if dst is not None:
                            edges.append((src, dst, amp))
        progress(args, f"[build {args.case_name}] emission {n}->{n - 1}: +{len(edges) - before} edges")

    edge_src = np.asarray([edge[0] for edge in edges], dtype=np.int64)
    edge_dst = np.asarray([edge[1] for edge in edges], dtype=np.int64)
    edge_amp = np.asarray([edge[2] for edge in edges], dtype=float)
    return ChainModel(
        basis=basis,
        index=index,
        energies=energies,
        sector_of=sector_of,
        rad_energy_of=rad_energy_of,
        rad_tuple_of=rad_tuple_of,
        edge_src=edge_src,
        edge_dst=edge_dst,
        edge_amp=edge_amp,
        mode_omega=mode_omega,
        mode_x=mode_x_arr,
        trace=float(np.sum(energies)),
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        slot_count=args.slot_count,
        mode_count=mode_count,
    )


def h_action(model: ChainModel, vector: NDArray[np.complex128]) -> NDArray[np.complex128]:
    vector = np.asarray(vector, dtype=np.complex128)
    if vector.ndim == 1:
        out = model.energies.astype(np.complex128) * vector
        np.add.at(out, model.edge_dst, model.edge_amp * vector[model.edge_src])
        np.add.at(out, model.edge_src, model.edge_amp * vector[model.edge_dst])
        return out
    out = model.energies[:, None].astype(np.complex128) * vector
    np.add.at(out, model.edge_dst, model.edge_amp[:, None] * vector[model.edge_src, :])
    np.add.at(out, model.edge_src, model.edge_amp[:, None] * vector[model.edge_dst, :])
    return out


def as_linear_operator(model: ChainModel) -> spla.LinearOperator:
    dim = len(model.basis)
    return spla.LinearOperator(
        shape=(dim, dim),
        dtype=np.complex128,
        matvec=lambda vector: h_action(model, vector),
        matmat=lambda matrix: h_action(model, matrix),
        rmatvec=lambda vector: h_action(model, vector),
    )


def purified_initial_state(
    model: ChainModel,
    args: argparse.Namespace,
) -> tuple[NDArray[np.complex128], int]:
    empty_rad = 0
    candidates = [
        model.index[BasisState(args.n_max, a, empty_rad)]
        for a in range(args.q ** args.n_max)
    ]
    d_ref = len(candidates)
    psi = np.zeros((len(model.basis), d_ref), dtype=np.complex128)
    norm = 1.0 / math.sqrt(float(d_ref))
    for ref, sys_idx in enumerate(candidates):
        psi[sys_idx, ref] = norm
    return psi, d_ref


def label_for(
    component: str,
    ref: int,
    state: BasisState,
    rad_values: tuple[int, ...],
    early_sites: tuple[int, ...],
    late_sites: tuple[int, ...],
) -> Any:
    if component == "Q":
        return ref
    if component == "C":
        return (state.n, state.a)
    if component == "N":
        return state.n
    if component == "R":
        return rad_values
    if component == "E":
        return tuple(rad_values[idx] for idx in early_sites)
    if component == "L":
        return tuple(rad_values[idx] for idx in late_sites)
    raise ValueError(f"unknown component: {component}")


def combined_label(parts: tuple[str, ...], *args: Any) -> tuple[Any, ...]:
    return tuple(label_for(part, *args) for part in parts)


def second_renyi(
    psi: NDArray[np.complex128],
    model: ChainModel,
    keep: tuple[str, ...],
    *,
    early_sites: tuple[int, ...],
    late_sites: tuple[int, ...],
    threshold: float,
) -> float:
    all_parts = ("Q", "C", "R")
    trace = tuple(part for part in all_parts if part not in keep)
    keep_map: dict[tuple[Any, ...], int] = {}
    trace_map: dict[tuple[Any, ...], int] = {}
    entries: list[tuple[int, int, complex]] = []

    for sys_idx, state in enumerate(model.basis):
        rad_values = model.rad_tuple_of[sys_idx]
        for ref in range(psi.shape[1]):
            amp = psi[sys_idx, ref]
            if abs(amp) <= threshold:
                continue
            args = (ref, state, rad_values, early_sites, late_sites)
            keep_label = combined_label(keep, *args)
            trace_label = combined_label(trace, *args)
            if keep_label not in keep_map:
                keep_map[keep_label] = len(keep_map)
            if trace_label not in trace_map:
                trace_map[trace_label] = len(trace_map)
            entries.append((keep_map[keep_label], trace_map[trace_label], amp))

    if not entries:
        return float("nan")
    mat = np.zeros((len(keep_map), len(trace_map)), dtype=np.complex128)
    for row, col, amp in entries:
        mat[row, col] += amp
    if mat.shape[0] <= mat.shape[1]:
        rho = mat @ mat.conj().T
    else:
        rho = mat.conj().T @ mat
    purity = float(np.sum(np.abs(rho) ** 2).real)
    return -math.log(max(purity, 1e-300))


def diagnostics(
    model: ChainModel,
    hop: spla.LinearOperator,
    psi: NDArray[np.complex128],
    d_ref: int,
    args: argparse.Namespace,
) -> dict[str, float]:
    probs_sys = np.sum(np.abs(psi) ** 2, axis=1)
    mean_n = float(probs_sys @ model.sector_of)
    rad_energy_total = float(probs_sys @ model.rad_energy_of)
    h_expect = np.trace(psi.conj().T @ (hop @ psi))

    split = args.early_late_split
    early_sites = tuple(range(split, args.slot_count))
    late_sites = tuple(range(0, split))
    entropy: dict[str, float] = {}
    for name, keep in {
        "Q": ("Q",),
        "C": ("C",),
        "R": ("R",),
        "E": ("E",),
        "L": ("L",),
        "QC": ("Q", "C"),
        "QR": ("Q", "R"),
        "QE": ("Q", "E"),
        "QL": ("Q", "L"),
        "EL": ("E", "L"),
    }.items():
        entropy[f"s2_{name.lower()}"] = second_renyi(
            psi,
            model,
            keep,
            early_sites=early_sites,
            late_sites=late_sites,
            threshold=args.entropy_threshold,
        )

    s2_q = entropy["s2_q"]
    s2_c = entropy["s2_c"]
    s2_r = entropy["s2_r"]
    s2_e = entropy["s2_e"]
    s2_l = entropy["s2_l"]
    row = {
        "mean_n": mean_n,
        "radiation_energy": rad_energy_total,
        "hamiltonian_energy": float(np.real(h_expect)),
        "hamiltonian_energy_imag": float(np.imag(h_expect)),
        "reference_dimension": float(d_ref),
        **entropy,
        "i2_qc": s2_q + s2_c - entropy["s2_qc"],
        "i2_qr": s2_q + s2_r - entropy["s2_qr"],
        "i2_qe": s2_q + s2_e - entropy["s2_qe"],
        "i2_ql": s2_q + s2_l - entropy["s2_ql"],
        "i2_el": s2_e + s2_l - entropy["s2_el"],
    }
    return row


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str]:
    h = np.asarray([float(row["hamiltonian_energy"]) for row in rows], dtype=float)
    return {
        "case": rows[-1]["case"],
        "basis_dim": rows[-1]["basis_dim"],
        "edge_count": rows[-1]["edge_count"],
        "reference_dimension": rows[-1]["reference_dimension"],
        "initial_mean_n": rows[0]["mean_n"],
        "final_mean_n": rows[-1]["mean_n"],
        "mean_n_drop": float(rows[0]["mean_n"]) - float(rows[-1]["mean_n"]),
        "initial_i2_qc": rows[0]["i2_qc"],
        "final_i2_qc": rows[-1]["i2_qc"],
        "initial_i2_qr": rows[0]["i2_qr"],
        "final_i2_qr": rows[-1]["i2_qr"],
        "max_i2_qr": max(float(row["i2_qr"]) for row in rows),
        "initial_i2_el": rows[0]["i2_el"],
        "final_i2_el": rows[-1]["i2_el"],
        "max_i2_el": max(float(row["i2_el"]) for row in rows),
        "final_s2_r": rows[-1]["s2_r"],
        "max_energy_drift": float(np.max(h) - np.min(h)),
    }


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | int | str]], dict[str, float | int | str]]:
    t0 = walltime.perf_counter()
    model = build_model(args)
    hop = as_linear_operator(model)
    psi, d_ref = purified_initial_state(model, args)
    progress(
        args,
        f"[run {args.case_name}] model built in {walltime.perf_counter() - t0:.1f}s: "
        f"dim={len(model.basis)} ref={d_ref} edges={len(model.edge_src)}",
    )

    rows: list[dict[str, float | int | str]] = []
    times = np.linspace(0.0, args.t_max, args.time_points)
    for step_idx, time in enumerate(times):
        step_t0 = walltime.perf_counter()
        obs = diagnostics(model, hop, psi, d_ref, args)
        rows.append(
            {
                "case": args.case_name,
                "time": float(time),
                "basis_dim": len(model.basis),
                "edge_count": len(model.edge_src),
                "mass_law": args.mass_law,
                "scramble_strength": args.scramble_strength,
                "hop_strength": args.hop_strength,
                "emission_coupling": args.emission_coupling,
                **obs,
            }
        )
        row = rows[-1]
        progress(
            args,
            f"[run {args.case_name}] point {step_idx + 1}/{len(times)} "
            f"t={float(time):.3g} mean_n={float(row['mean_n']):.3f} "
            f"Erad={float(row['radiation_energy']):.3f} "
            f"I2_QC={float(row['i2_qc']):.3f} "
            f"I2_QR={float(row['i2_qr']):.3f} "
            f"I2_EL={float(row['i2_el']):.3f} "
            f"dt={walltime.perf_counter() - step_t0:.1f}s",
        )
        if step_idx + 1 < len(times):
            dt = float(times[step_idx + 1] - time)
            evolved = spla.expm_multiply(
                (-1j) * hop,
                psi,
                start=0.0,
                stop=dt,
                num=2,
                traceA=(-1j) * model.trace,
            )
            psi = np.asarray(evolved[-1], dtype=np.complex128)
    summary = summarize(rows)
    progress(
        args,
        f"[run {args.case_name}] complete in {walltime.perf_counter() - t0:.1f}s: "
        f"dn={float(summary['mean_n_drop']):.3f} "
        f"I2_QR {float(summary['initial_i2_qr']):.3f}->{float(summary['final_i2_qr']):.3f} "
        f"I2_EL {float(summary['initial_i2_el']):.3f}->{float(summary['final_i2_el']):.3f}",
    )
    return rows, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record-radiation Renyi diagnostics for the autonomous parent.")
    parser.add_argument("--case-name", default="record_renyi")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=3)
    parser.add_argument("--n-max", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--mass-law", choices=["sqrt", "linear"], default="sqrt")
    parser.add_argument("--dos", default="exponential")
    parser.add_argument("--width-x", type=float, default=4.0)
    parser.add_argument("--mode-x", default="0.8,1.5,3.0")
    parser.add_argument("--slot-count", type=int, default=4)
    parser.add_argument("--early-late-split", type=int, default=2)
    parser.add_argument("--max-quanta", type=int, default=3)
    parser.add_argument("--scramble-strength", type=float, default=1.0)
    parser.add_argument("--scramble-degree", type=int, default=4)
    parser.add_argument("--hop-strength", type=float, default=0.4)
    parser.add_argument("--emission-coupling", type=float, default=0.05)
    parser.add_argument("--emission-degree", type=int, default=6)
    parser.add_argument("--detuning-width-x", type=float, default=0.5)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--matrix-cutoff", type=float, default=1e-10)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--t-max", type=float, default=40.0)
    parser.add_argument("--time-points", type=int, default=9)
    parser.add_argument("--entropy-threshold", type=float, default=1e-13)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--timeseries-csv",
        type=Path,
        default=DATADIR / "record_radiation_renyi_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=DATADIR / "record_radiation_renyi_summary.csv",
    )
    args = parser.parse_args(argv)
    if args.early_late_split <= 0 or args.early_late_split >= args.slot_count:
        raise ValueError("--early-late-split must be between 0 and slot-count")
    rows, summary = run(args)
    write_csv(args.timeseries_csv, rows)
    write_csv(args.summary_csv, [summary])
    print(f"[record-renyi] wrote {args.timeseries_csv}")
    print(f"[record-renyi] wrote {args.summary_csv}")
    print(
        "dim={basis_dim} ref={reference_dimension} edges={edge_count} "
        "dn={mean_n_drop:.3f} I2_QR={initial_i2_qr:.3f}->{final_i2_qr:.3f} "
        "I2_QC={initial_i2_qc:.3f}->{final_i2_qc:.3f} "
        "I2_EL={initial_i2_el:.3f}->{final_i2_el:.3f} drift={max_energy_drift:.2e}".format(
            **summary
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
