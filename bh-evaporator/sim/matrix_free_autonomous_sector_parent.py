#!/usr/bin/env python3
"""Matrix-free autonomous parent of the successful sector model.

This implements H_total = H_core + K_scramble + H_rad + H_int as a SciPy
LinearOperator.  It uses the energy-resolved sector spectra that already passed
the sector-rate/isometry tests, but evolves the combined core+radiation system
directly under exp(-i H_total t).
"""
from __future__ import annotations

import argparse
import csv
import itertools
import math
import time as walltime
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import scipy.sparse.linalg as spla
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_energy_resolved import (
    beta_for_downward_step,
    build_energy_resolved_sectors,
)
from sector_hamiltonian_evaporator import target_x_distribution


@dataclass(frozen=True)
class BasisState:
    n: int
    a: int
    occ: int


@dataclass(frozen=True)
class Edge:
    src: int
    dst: int
    amp: float
    kind: str
    omega: float = 0.0
    x: float = 0.0


@dataclass(frozen=True)
class SectorParentModel:
    basis: list[BasisState]
    index: dict[BasisState, int]
    energies: NDArray[np.float64]
    sector_of: NDArray[np.int64]
    rad_energy_of: NDArray[np.float64]
    edges: list[Edge]
    emission_edges: list[Edge]
    edge_src: NDArray[np.int64]
    edge_dst: NDArray[np.int64]
    edge_amp: NDArray[np.float64]
    mode_omega: NDArray[np.float64]
    mode_x: NDArray[np.float64]
    trace: float
    n_min: int
    n_max: int
    q: int


def parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def occupations(mode_count: int, max_quanta: int) -> list[int]:
    out = []
    for count in range(max_quanta + 1):
        for modes in itertools.combinations(range(mode_count), count):
            mask = 0
            for mode in modes:
                mask |= 1 << mode
            out.append(mask)
    return out


def popcount(value: int) -> int:
    return int(value.bit_count())


def mode_occupied(mask: int, mode: int) -> bool:
    return bool(mask & (1 << mode))


def add_mode(mask: int, mode: int) -> int:
    return mask | (1 << mode)


def progress(args: argparse.Namespace, message: str) -> None:
    if not getattr(args, "quiet", False):
        print(message, flush=True)


def rad_energy(mask: int, mode_omega: NDArray[np.float64]) -> float:
    total = 0.0
    for mode, omega in enumerate(mode_omega):
        if mode_occupied(mask, mode):
            total += float(omega)
    return total


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


def build_radiation_modes(
    sectors,
    n_values: list[int],
    mode_x: list[float],
    copies: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Use x bins around a representative beta to make fixed radiation modes."""
    rep_n = max(n_values)
    beta = beta_for_downward_step(sectors[rep_n], sectors[rep_n - 1])
    xs = []
    omegas = []
    for x in mode_x:
        for _ in range(copies):
            xs.append(x)
            omegas.append(x / beta)
    return np.asarray(omegas, dtype=float), np.asarray(xs, dtype=float)


def build_basis(sectors, occs: list[int]) -> tuple[list[BasisState], dict[BasisState, int]]:
    basis = [
        BasisState(n, a, occ)
        for n in sorted(sectors)
        for occ in occs
        for a in range(sectors[n].dim)
    ]
    return basis, {state: idx for idx, state in enumerate(basis)}


def build_model(args: argparse.Namespace) -> SectorParentModel:
    progress(
        args,
        f"[build {args.case_name}] sectors n={args.n_min}..{args.n_max} "
        f"q={args.q} k={args.max_quanta} law={args.mass_law}",
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
    n_values = list(range(args.n_min + 1, args.n_max + 1))
    mode_x = parse_float_list(args.mode_x)
    mode_omega, mode_x_arr = build_radiation_modes(
        sectors, n_values, mode_x, args.mode_copies
    )
    occs = occupations(len(mode_omega), args.max_quanta)
    progress(
        args,
        f"[build {args.case_name}] radiation modes={len(mode_omega)} "
        f"occupations={len(occs)}",
    )
    basis, index = build_basis(sectors, occs)
    progress(args, f"[build {args.case_name}] basis_dim={len(basis)}")
    energies = np.zeros(len(basis), dtype=float)
    sector_of = np.zeros(len(basis), dtype=np.int64)
    rad_energy_of = np.zeros(len(basis), dtype=float)
    for idx, state in enumerate(basis):
        re = rad_energy(state.occ, mode_omega)
        energies[idx] = sectors[state.n].evals[state.a] + re
        sector_of[idx] = state.n
        rad_energy_of[idx] = re

    rng = np.random.default_rng(args.seed + 10_000)
    edges: list[Edge] = []

    # Intra-sector scrambling.
    if args.scramble_strength > 0.0 and args.scramble_degree > 0:
        for n, sector in sectors.items():
            local_edges = random_sparse_symmetric_edges(
                sector.dim,
                args.scramble_degree,
                args.scramble_strength,
                np.random.default_rng(args.seed + 20_000 + n),
            )
            for occ in occs:
                for a, b, amp in local_edges:
                    src = index[BasisState(n, a, occ)]
                    dst = index[BasisState(n, b, occ)]
                    edges.append(Edge(src, dst, amp, "scramble"))
        progress(args, f"[build {args.case_name}] scramble_edges={len(edges)}")

    # Energy-filtered shrinkage transitions plus radiation creation/annihilation.
    emission_edges: list[Edge] = []
    for n in range(args.n_min + 1, args.n_max + 1):
        before = len(emission_edges)
        high = sectors[n]
        low = sectors[n - 1]
        beta = beta_for_downward_step(high, low)
        for occ in occs:
            if popcount(occ) >= args.max_quanta:
                continue
            for a in range(high.dim):
                src_state = BasisState(n, a, occ)
                src = index[src_state]
                for mode, omega_rad in enumerate(mode_omega):
                    if mode_occupied(occ, mode):
                        continue
                    occ_new = add_mode(occ, mode)
                    sample_count = min(args.emission_degree, low.dim)
                    targets = rng.choice(low.dim, size=sample_count, replace=False)
                    for b_raw in targets:
                        b = int(b_raw)
                        omega_core = float(high.evals[a] - low.evals[b])
                        detuning_x = beta * (omega_core - omega_rad)
                        envelope = math.exp(-0.5 * (detuning_x / args.detuning_width_x) ** 2)
                        if envelope <= args.matrix_cutoff:
                            continue
                        # Random signs avoid coherent bias while retaining the
                        # golden-rule envelope.  The omega factor gives the
                        # desired radiation phase-space power at rate level.
                        sign = rng.choice([-1.0, 1.0])
                        area_scale = (
                            float(n) / float(args.emission_area_reference)
                        ) ** (0.5 * args.emission_area_power)
                        amp = (
                            args.emission_coupling
                            * sign
                            * area_scale
                            * (max(omega_rad, 0.0) ** (0.5 * args.ohmic_power))
                            * envelope
                            / math.sqrt(float(sample_count))
                        )
                        dst = index.get(BasisState(n - 1, b, occ_new))
                        if dst is None:
                            continue
                        edge = Edge(src, dst, amp, "emission", omega_rad, beta * omega_rad)
                        edges.append(edge)
                        emission_edges.append(edge)
        progress(
            args,
            f"[build {args.case_name}] emission sector {n}->{n - 1}: "
            f"+{len(emission_edges) - before} edges",
        )

    edge_src = np.asarray([edge.src for edge in edges], dtype=np.int64)
    edge_dst = np.asarray([edge.dst for edge in edges], dtype=np.int64)
    edge_amp = np.asarray([edge.amp for edge in edges], dtype=float)
    return SectorParentModel(
        basis=basis,
        index=index,
        energies=energies,
        sector_of=sector_of,
        rad_energy_of=rad_energy_of,
        edges=edges,
        emission_edges=emission_edges,
        edge_src=edge_src,
        edge_dst=edge_dst,
        edge_amp=edge_amp,
        mode_omega=mode_omega,
        mode_x=mode_x_arr,
        trace=float(np.sum(energies)),
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
    )


def h_action(model: SectorParentModel, vector: NDArray[np.complex128]) -> NDArray[np.complex128]:
    vector = np.asarray(vector, dtype=np.complex128).reshape(-1)
    out = model.energies.astype(np.complex128) * vector
    np.add.at(out, model.edge_dst, model.edge_amp * vector[model.edge_src])
    np.add.at(out, model.edge_src, model.edge_amp * vector[model.edge_dst])
    return out


def as_linear_operator(model: SectorParentModel) -> spla.LinearOperator:
    dim = len(model.basis)
    return spla.LinearOperator(
        shape=(dim, dim),
        dtype=np.complex128,
        matvec=lambda vector: h_action(model, vector),
        rmatvec=lambda vector: h_action(model, vector),
    )


def initial_state(model: SectorParentModel, args: argparse.Namespace) -> NDArray[np.complex128]:
    rng = np.random.default_rng(args.seed + 30_000)
    psi = np.zeros(len(model.basis), dtype=np.complex128)
    candidates = [
        idx
        for idx, state in enumerate(model.basis)
        if state.n == args.n_max and state.occ == 0
    ]
    if args.initial_state == "basis":
        psi[candidates[0]] = 1.0
    elif args.initial_state == "haar":
        raw = rng.normal(size=len(candidates)) + 1j * rng.normal(size=len(candidates))
        raw /= np.sqrt(float(np.vdot(raw, raw).real))
        for idx, amp in zip(candidates, raw):
            psi[idx] = amp
    else:
        raise ValueError(f"unknown initial state: {args.initial_state}")
    return psi


def sector_probs(model: SectorParentModel, probs: NDArray[np.float64]) -> dict[int, float]:
    out = {}
    for n in range(model.n_min, model.n_max + 1):
        out[n] = float(np.sum(probs[model.sector_of == n]))
    return out


def flux_spectrum(
    model: SectorParentModel,
    psi: NDArray[np.complex128],
    x_edges: NDArray[np.float64],
    target: NDArray[np.float64],
) -> dict[str, float | str]:
    hist = np.zeros(len(x_edges) - 1, dtype=float)
    flux = 0.0
    power = 0.0
    for edge in model.emission_edges:
        current = 2.0 * edge.amp * float(np.imag(np.conjugate(psi[edge.dst]) * psi[edge.src]))
        # Positive current means source -> emitted state in our convention.
        if current <= 0.0:
            continue
        flux += current
        power += current * edge.omega
        bin_idx = np.searchsorted(x_edges, edge.x, side="right") - 1
        if 0 <= bin_idx < len(hist):
            hist[bin_idx] += current
    if float(np.sum(hist)) > 1e-14:
        probs = hist / float(np.sum(hist))
        tv = 0.5 * float(np.sum(np.abs(probs - target)))
    else:
        probs = np.zeros_like(hist)
        tv = float("nan")
    return {
        "outward_flux": flux,
        "outward_power": power,
        "flux_tv_to_thermal_x": tv,
        "flux_x_probs": ";".join(f"{p:.8g}" for p in probs),
    }


def observables(
    model: SectorParentModel,
    hop: spla.LinearOperator,
    psi: NDArray[np.complex128],
    x_edges: NDArray[np.float64],
    target: NDArray[np.float64],
) -> dict[str, float | str]:
    probs = np.abs(psi) ** 2
    sp = sector_probs(model, probs)
    mean_n = sum(n * p for n, p in sp.items())
    rad_e = float(probs @ model.rad_energy_of)
    core_e = float(probs @ (model.energies - model.rad_energy_of))
    h_expect = complex(np.vdot(psi, hop @ psi))
    row: dict[str, float | str] = {
        "mean_n": float(mean_n),
        "core_energy": core_e,
        "radiation_energy": rad_e,
        "hamiltonian_energy": float(h_expect.real),
        "hamiltonian_energy_imag": float(h_expect.imag),
        **{f"p_sector_{n}": p for n, p in sp.items()},
    }
    row.update(flux_spectrum(model, psi, x_edges, target))
    return row


def write_csv(path: Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def append_csv_row(path: Path, row: dict[str, float | int | str], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def summarize(rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str]:
    times = np.asarray([float(row["time"]) for row in rows], dtype=float)
    rad = np.asarray([float(row["radiation_energy"]) for row in rows], dtype=float)
    mean_n = np.asarray([float(row["mean_n"]) for row in rows], dtype=float)
    flux = np.asarray([float(row["outward_flux"]) for row in rows], dtype=float)
    power = np.asarray([float(row["outward_power"]) for row in rows], dtype=float)
    hvals = np.asarray([float(row["hamiltonian_energy"]) for row in rows], dtype=float)
    finite_tvs = [float(row["flux_tv_to_thermal_x"]) for row in rows if np.isfinite(float(row["flux_tv_to_thermal_x"]))]
    active = np.arange(1, len(rows), dtype=int)
    if len(active) >= 3:
        windows = np.array_split(active, 3)
    else:
        windows = [active, active, active]

    def window_mean(values: NDArray[np.float64], window: NDArray[np.int64]) -> float:
        if len(window) == 0:
            return float("nan")
        return float(np.mean(values[window]))

    def safe_ratio(num: float, den: float) -> float:
        if not np.isfinite(num) or not np.isfinite(den) or abs(den) < 1e-14:
            return float("nan")
        return num / den

    mass_law = str(rows[-1]["mass_law"])
    area_power = float(rows[-1]["emission_area_power"])
    bath_power = float(rows[-1]["ohmic_power"])
    if mass_law == "sqrt":
        predicted_power_exponent_n = area_power - 0.5 * (bath_power + 2.0)
        predicted_power_exponent_m = 2.0 * predicted_power_exponent_n
    elif mass_law == "linear":
        predicted_power_exponent_n = area_power
        predicted_power_exponent_m = area_power
    else:
        predicted_power_exponent_n = float("nan")
        predicted_power_exponent_m = float("nan")

    early_power = window_mean(power, windows[0])
    mid_power = window_mean(power, windows[1])
    late_power = window_mean(power, windows[2])
    early_flux = window_mean(flux, windows[0])
    mid_flux = window_mean(flux, windows[1])
    late_flux = window_mean(flux, windows[2])
    early_tv_values = [
        float(rows[idx]["flux_tv_to_thermal_x"])
        for idx in windows[0]
        if np.isfinite(float(rows[idx]["flux_tv_to_thermal_x"]))
    ]
    mid_tv_values = [
        float(rows[idx]["flux_tv_to_thermal_x"])
        for idx in windows[1]
        if np.isfinite(float(rows[idx]["flux_tv_to_thermal_x"]))
    ]
    late_tv_values = [
        float(rows[idx]["flux_tv_to_thermal_x"])
        for idx in windows[2]
        if np.isfinite(float(rows[idx]["flux_tv_to_thermal_x"]))
    ]
    return {
        "case": rows[-1]["case"],
        "basis_dim": rows[-1]["basis_dim"],
        "edge_count": rows[-1]["edge_count"],
        "emission_edge_count": rows[-1]["emission_edge_count"],
        "mass_law": rows[-1]["mass_law"],
        "alpha": rows[-1]["alpha"],
        "scramble_strength": rows[-1]["scramble_strength"],
        "emission_coupling": rows[-1]["emission_coupling"],
        "emission_area_power": rows[-1]["emission_area_power"],
        "emission_area_reference": rows[-1]["emission_area_reference"],
        "ohmic_power": rows[-1]["ohmic_power"],
        "predicted_power_exponent_n": predicted_power_exponent_n,
        "predicted_power_exponent_m": predicted_power_exponent_m,
        "initial_mean_n": mean_n[0],
        "final_mean_n": mean_n[-1],
        "mean_n_drop": mean_n[0] - mean_n[-1],
        "final_radiation_energy": rad[-1],
        "max_radiation_energy": float(np.max(rad)),
        "max_outward_flux": float(np.max(flux)),
        "max_outward_power": float(np.max(power)),
        "early_outward_flux": early_flux,
        "mid_outward_flux": mid_flux,
        "late_outward_flux": late_flux,
        "flux_mid_over_early": safe_ratio(mid_flux, early_flux),
        "flux_late_over_early": safe_ratio(late_flux, early_flux),
        "early_outward_power": early_power,
        "mid_outward_power": mid_power,
        "late_outward_power": late_power,
        "power_mid_over_early": safe_ratio(mid_power, early_power),
        "power_late_over_early": safe_ratio(late_power, early_power),
        "early_mean_flux_tv_to_thermal_x": float(np.mean(early_tv_values)) if early_tv_values else float("nan"),
        "mid_mean_flux_tv_to_thermal_x": float(np.mean(mid_tv_values)) if mid_tv_values else float("nan"),
        "late_mean_flux_tv_to_thermal_x": float(np.mean(late_tv_values)) if late_tv_values else float("nan"),
        "mean_flux_tv_to_thermal_x": float(np.mean(finite_tvs)) if finite_tvs else float("nan"),
        "min_flux_tv_to_thermal_x": float(np.min(finite_tvs)) if finite_tvs else float("nan"),
        "max_energy_drift": float(np.max(hvals) - np.min(hvals)),
    }


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | int | str]], dict[str, float | int | str]]:
    t0 = walltime.perf_counter()
    model = build_model(args)
    hop = as_linear_operator(model)
    psi0 = initial_state(model, args)
    x_edges = np.asarray(args.x_edges, dtype=float)
    target = target_x_distribution(x_edges, args.ohmic_power)
    progress(
        args,
        f"[run {args.case_name}] model built in {walltime.perf_counter() - t0:.1f}s: "
        f"dim={len(model.basis)} edges={len(model.edges)} "
        f"emit_edges={len(model.emission_edges)}",
    )
    rows: list[dict[str, float | int | str]] = []
    times = np.linspace(0.0, args.t_max, args.time_points)
    psi = psi0
    progress(args, f"[run {args.case_name}] evolution start: {len(times)} time points")
    incremental_path = getattr(args, "timeseries_csv", None)
    incremental_enabled = bool(getattr(args, "incremental_timeseries", False)) and incremental_path is not None
    incremental_fields: list[str] | None = None
    if incremental_enabled:
        incremental_path = Path(incremental_path)
        if incremental_path.exists():
            incremental_path.unlink()
        progress(args, f"[run {args.case_name}] incremental timeseries: {incremental_path}")

    for step_idx, time in enumerate(times):
        step_t0 = walltime.perf_counter()
        rows.append(
            {
                "case": args.case_name,
                "time": float(time),
                "basis_dim": len(model.basis),
                "edge_count": len(model.edges),
                "emission_edge_count": len(model.emission_edges),
                "mass_law": args.mass_law,
                "alpha": args.alpha,
                "scramble_strength": args.scramble_strength,
                "emission_coupling": args.emission_coupling,
                "emission_area_power": args.emission_area_power,
                "emission_area_reference": args.emission_area_reference,
                "ohmic_power": args.ohmic_power,
                **observables(model, hop, psi, x_edges, target),
            }
        )
        row = rows[-1]
        if incremental_enabled:
            if incremental_fields is None:
                incremental_fields = sorted(row)
            append_csv_row(Path(incremental_path), row, incremental_fields)
        progress(
            args,
            f"[run {args.case_name}] point {step_idx + 1}/{len(times)} "
            f"t={float(time):.3g} mean_n={float(row['mean_n']):.3f} "
            f"Erad={float(row['radiation_energy']):.3f} "
            f"Pout={float(row['outward_power']):.3g} "
            f"TV={float(row['flux_tv_to_thermal_x']):.3f} "
            f"dt={walltime.perf_counter() - step_t0:.1f}s",
        )
        if step_idx + 1 < len(times):
            dt = float(times[step_idx + 1] - time)
            evolve_t0 = walltime.perf_counter()
            evolved = spla.expm_multiply(
                (-1j) * hop,
                psi,
                start=0.0,
                stop=dt,
                num=2,
                traceA=(-1j) * model.trace,
            )
            psi = np.asarray(evolved[-1], dtype=np.complex128)
            progress(
                args,
                f"[run {args.case_name}] evolved to next point in "
                f"{walltime.perf_counter() - evolve_t0:.1f}s",
            )
    progress(args, f"[run {args.case_name}] complete in {walltime.perf_counter() - t0:.1f}s")
    return rows, summarize(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run matrix-free autonomous sector parent.")
    parser.add_argument("--case-name", default="matrix_free_parent")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=3)
    parser.add_argument("--n-max", type=int, default=5)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--mass-law", choices=["sqrt", "linear"], default="sqrt")
    parser.add_argument("--dos", default="exponential")
    parser.add_argument("--width-x", type=float, default=4.0)
    parser.add_argument("--mode-x", default="0.5,1.0,1.5,2.0,3.0,5.0")
    parser.add_argument("--mode-copies", type=int, default=2)
    parser.add_argument("--max-quanta", type=int, default=2)
    parser.add_argument("--scramble-strength", type=float, default=1.0)
    parser.add_argument("--scramble-degree", type=int, default=4)
    parser.add_argument("--emission-coupling", type=float, default=0.08)
    parser.add_argument("--emission-degree", type=int, default=6)
    parser.add_argument(
        "--emission-area-power",
        type=float,
        default=1.0,
        help=(
            "Rate-level power of the remaining area variable n in H_emit. "
            "The matrix element is multiplied by "
            "(n / emission_area_reference)^(emission_area_power / 2). "
            "Use 1 for area-sized horizon emission and 0 for an O(1) "
            "emission-strength control."
        ),
    )
    parser.add_argument(
        "--emission-area-reference",
        type=float,
        default=1.0,
        help="Reference n used in the area-emission matrix-element factor.",
    )
    parser.add_argument("--detuning-width-x", type=float, default=0.5)
    parser.add_argument("--ohmic-power", type=float, default=2.0)
    parser.add_argument("--matrix-cutoff", type=float, default=1e-10)
    parser.add_argument("--initial-state", choices=["haar", "basis"], default="haar")
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--t-max", type=float, default=120.0)
    parser.add_argument("--time-points", type=int, default=41)
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument(
        "--incremental-timeseries",
        action="store_true",
        help="Append each saved time point to the timeseries CSV as soon as it is computed.",
    )
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument(
        "--timeseries-csv",
        type=Path,
        default=DATADIR / "matrix_free_parent_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=Path,
        default=DATADIR / "matrix_free_parent_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    if not args.incremental_timeseries:
        write_csv(args.timeseries_csv, rows)
    write_csv(args.summary_csv, [summary])
    print(f"[matrix-free-parent] wrote {args.timeseries_csv}")
    print(f"[matrix-free-parent] wrote {args.summary_csv}")
    print(
        "dim={basis_dim} edges={edge_count} emit_edges={emission_edge_count} "
        "dn={mean_n_drop:.3f} Erad={final_radiation_energy:.3f} "
        "Pmax={max_outward_power:.3g} TVmean={mean_flux_tv_to_thermal_x:.3f} "
        "drift={max_energy_drift:.2e}".format(**summary)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
