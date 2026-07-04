#!/usr/bin/env python3
"""Tiny autonomous sector-Hamiltonian evaporator.

This is a small direct test of the autonomous Hamiltonian:

    H = H_core + K_scramble + H_rad + H_int.

The Hilbert space keeps sectors n=2,3,4, a small set of radiation modes, and
at most two emitted quanta.  The goal is not a scaling run.  It checks whether
the same ingredients used in the secular sector model can be embedded in one
time-independent Hamiltonian and evolved as exp(-i H t).
"""
from __future__ import annotations

import argparse
import csv
import itertools
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")

from area_register_rate_scan import local_removal_ops, scrambled_removal_ops
from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_energy_resolved import (
    build_energy_resolved_sectors,
    beta_for_downward_step,
)
from sector_hamiltonian_evaporator import target_x_distribution
from sector_hamiltonian_scrambling import expander_adjacency, random_symmetric


@dataclass(frozen=True)
class BasisState:
    n: int
    a: int
    occ: tuple[int, ...]


def radiation_occupations(mode_count: int, max_quanta: int) -> list[tuple[int, ...]]:
    out = []
    for total in range(max_quanta + 1):
        for occupied in itertools.combinations(range(mode_count), total):
            occ = [0] * mode_count
            for idx in occupied:
                occ[idx] = 1
            out.append(tuple(occ))
    return out


def build_basis(sectors, mode_count: int, max_quanta: int, n_initial: int):
    basis: list[BasisState] = []
    for occ in radiation_occupations(mode_count, max_quanta):
        emitted = sum(occ)
        n = n_initial - emitted
        if n not in sectors:
            continue
        for a in range(sectors[n].dim):
            basis.append(BasisState(n=n, a=a, occ=occ))
    index = {state: idx for idx, state in enumerate(basis)}
    return basis, index


def make_radiation_modes(sectors, n_initial: int, mode_x: NDArray[np.float64]) -> NDArray[np.float64]:
    beta = beta_for_downward_step(sectors[n_initial], sectors[n_initial - 1])
    return mode_x / beta


def mixer_block(dim: int, kind: str, seed: int) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    if kind == "none":
        return np.zeros((dim, dim), dtype=float)
    if kind == "dense":
        return random_symmetric(rng, dim)
    if kind == "expander":
        return expander_adjacency(dim)
    raise ValueError(f"unknown mixer kind: {kind}")


def build_hamiltonian(
    *,
    basis: list[BasisState],
    index: dict[BasisState, int],
    sectors,
    q: int,
    operator: str,
    mixer_kind: str,
    k_strength: float,
    g: float,
    rad_omegas: NDArray[np.float64],
    resonance_width_x: float,
    ohmic_power: float,
    seed: int,
) -> sp.csr_matrix:
    rows: list[int] = []
    cols: list[int] = []
    data: list[complex] = []
    dim_total = len(basis)

    # Diagonal H_core + H_rad.
    for idx, state in enumerate(basis):
        energy = sectors[state.n].evals[state.a] + float(np.dot(state.occ, rad_omegas))
        rows.append(idx)
        cols.append(idx)
        data.append(energy)

    # K_scramble acts within fixed sector and fixed radiation occupation.
    mixer_cache: dict[int, NDArray[np.float64]] = {}
    for state in basis:
        if state.n not in mixer_cache:
            mixer_cache[state.n] = k_strength * mixer_block(
                sectors[state.n].dim,
                mixer_kind,
                seed + 17_000 + 101 * state.n,
            )
        block = mixer_cache[state.n]
        if not np.any(block):
            continue
        i = index[state]
        for b in range(sectors[state.n].dim):
            if b == state.a:
                continue
            val = block[b, state.a]
            if abs(val) <= 1e-14:
                continue
            target = BasisState(n=state.n, a=b, occ=state.occ)
            j = index.get(target)
            if j is not None:
                rows.append(j)
                cols.append(i)
                data.append(val)

    # H_int creates or annihilates one radiation quantum while shifting n.
    rng = np.random.default_rng(seed + 100_000)
    op_cache = {}
    for n in sorted(sectors):
        if n - 1 not in sectors:
            continue
        high = sectors[n]
        low = sectors[n - 1]
        if operator == "local":
            ops = local_removal_ops(high, low, q)
        elif operator == "scrambled":
            ops = scrambled_removal_ops(high, low, q, rng)
        else:
            raise ValueError(f"unknown operator: {operator}")
        op_e = np.zeros((low.dim, high.dim), dtype=float)
        for op in ops:
            op_e += np.abs(low.evecs.T @ op @ high.evecs)
        op_cache[n] = op_e / max(float(np.max(op_e)), 1e-300)

    for source in basis:
        if source.n - 1 not in sectors:
            continue
        beta = beta_for_downward_step(sectors[source.n], sectors[source.n - 1])
        op_e = op_cache[source.n]
        i = index[source]
        for mode_idx, omega_rad in enumerate(rad_omegas):
            if source.occ[mode_idx] != 0:
                continue
            occ_new = list(source.occ)
            occ_new[mode_idx] = 1
            occ_new_t = tuple(occ_new)
            for b in range(sectors[source.n - 1].dim):
                target = BasisState(n=source.n - 1, a=b, occ=occ_new_t)
                j = index.get(target)
                if j is None:
                    continue
                omega_core = sectors[source.n].evals[source.a] - sectors[source.n - 1].evals[b]
                detuning_x = beta * (omega_core - omega_rad)
                envelope = np.exp(-0.5 * (detuning_x / resonance_width_x) ** 2)
                val = g * op_e[b, source.a] * (max(omega_rad, 0.0) ** (0.5 * ohmic_power)) * envelope
                if abs(val) <= 1e-14:
                    continue
                rows.append(j)
                cols.append(i)
                data.append(val)
                rows.append(i)
                cols.append(j)
                data.append(val)

    return sp.coo_matrix((data, (rows, cols)), shape=(dim_total, dim_total)).tocsr()


def initial_state(basis: list[BasisState], sectors, n_initial: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed + 50_000)
    psi = np.zeros(len(basis), dtype=np.complex128)
    vac = tuple(0 for _ in basis[0].occ)
    top_indices = [idx for idx, state in enumerate(basis) if state.n == n_initial and state.occ == vac]
    raw = rng.normal(size=len(top_indices)) + 1j * rng.normal(size=len(top_indices))
    raw /= np.sqrt(float(np.vdot(raw, raw).real))
    for idx, amp in zip(top_indices, raw):
        psi[idx] = amp
    return psi


def observables(
    psi: NDArray[np.complex128],
    hmat: sp.csr_matrix,
    basis: list[BasisState],
    sectors,
    rad_omegas: NDArray[np.float64],
    n_initial: int,
    target_probs: NDArray[np.float64],
    x_edges: NDArray[np.float64],
) -> dict[str, float]:
    probs = np.abs(psi) ** 2
    core_energy = 0.0
    rad_energy = 0.0
    mean_n = 0.0
    rad_count = 0.0
    sector_probs: dict[int, float] = {}
    mode_counts = np.zeros(len(rad_omegas), dtype=float)
    for p, state in zip(probs, basis):
        core_energy += float(p * sectors[state.n].evals[state.a])
        rad_e = float(np.dot(state.occ, rad_omegas))
        rad_energy += float(p * rad_e)
        mean_n += float(p * state.n)
        rad_count += float(p * sum(state.occ))
        sector_probs[state.n] = sector_probs.get(state.n, 0.0) + float(p)
        mode_counts += p * np.asarray(state.occ, dtype=float)

    if float(np.sum(mode_counts)) > 0.0:
        beta0 = beta_for_downward_step(sectors[n_initial], sectors[n_initial - 1])
        xs = beta0 * rad_omegas
        hist = np.histogram(xs, bins=x_edges, weights=mode_counts)[0]
        if np.sum(hist) > 0:
            actual = hist / np.sum(hist)
            spectrum_tv = 0.5 * float(np.sum(np.abs(actual - target_probs)))
        else:
            spectrum_tv = float("nan")
    else:
        spectrum_tv = float("nan")

    h_expect = complex(np.vdot(psi, hmat @ psi))
    return {
        "core_energy": core_energy,
        "rad_energy": rad_energy,
        "bare_core_plus_rad_energy": core_energy + rad_energy,
        "hamiltonian_energy": float(h_expect.real),
        "hamiltonian_energy_imag": float(h_expect.imag),
        "mean_n": mean_n,
        "rad_count": rad_count,
        "p_top_sector": sector_probs.get(n_initial, 0.0),
        "p_lowest_sector": sector_probs.get(min(sectors), 0.0),
        "spectrum_tv_to_thermal_x": spectrum_tv,
    }


def summarize_series(values: NDArray[np.float64]) -> dict[str, float]:
    if len(values) < 5:
        return {"early": float("nan"), "late": float("nan"), "late_over_early": float("nan")}
    deriv = np.diff(values)
    early = np.mean(deriv[1 : max(3, len(deriv) // 3)])
    late = np.mean(deriv[max(3, 2 * len(deriv) // 3) :])
    return {
        "early": float(early),
        "late": float(late),
        "late_over_early": float(late / max(early, 1e-300)),
    }


def run_case(args: argparse.Namespace, mixer_kind: str, seed: int):
    sectors = build_energy_resolved_sectors(
        n_min=args.n_min,
        n_max=args.n_max,
        q=args.q,
        alpha=args.alpha,
        mass_law=args.mass_law,
        width_x=args.width_x,
        dos=args.dos,
        seed=seed,
    )
    mode_x = np.asarray(args.mode_x, dtype=float)
    rad_omegas = make_radiation_modes(sectors, args.n_max, mode_x)
    basis, index = build_basis(sectors, len(rad_omegas), args.max_quanta, args.n_max)
    hmat = build_hamiltonian(
        basis=basis,
        index=index,
        sectors=sectors,
        q=args.q,
        operator=args.operator,
        mixer_kind=mixer_kind,
        k_strength=args.k_strength,
        g=args.g,
        rad_omegas=rad_omegas,
        resonance_width_x=args.resonance_width_x,
        ohmic_power=args.ohmic_power,
        seed=seed,
    )
    psi0 = initial_state(basis, sectors, args.n_max, seed)
    times = np.linspace(0.0, args.t_max, args.time_points)
    x_edges = np.asarray(args.x_edges, dtype=float)
    target_probs = target_x_distribution(x_edges, args.ohmic_power)
    rows = []
    for time, psi in zip(times, spla.expm_multiply((-1j) * hmat, psi0, start=0.0, stop=args.t_max, num=args.time_points)):
        rows.append(
            {
                "time": float(time),
                "mixer": mixer_kind,
                "seed": seed,
                "hilbert_dim": len(basis),
                **observables(psi, hmat, basis, sectors, rad_omegas, args.n_max, target_probs, x_edges),
            }
        )
    rad_energy = np.asarray([row["rad_energy"] for row in rows], dtype=float)
    rad_count = np.asarray([row["rad_count"] for row in rows], dtype=float)
    energy_slope = summarize_series(rad_energy)
    count_slope = summarize_series(rad_count)
    final = rows[-1]
    summary = {
        "mixer": mixer_kind,
        "seed": seed,
        "hilbert_dim": len(basis),
        "final_rad_energy": final["rad_energy"],
        "final_rad_count": final["rad_count"],
        "final_mean_n": final["mean_n"],
        "final_p_top_sector": final["p_top_sector"],
        "final_p_lowest_sector": final["p_lowest_sector"],
        "final_spectrum_tv_to_thermal_x": final["spectrum_tv_to_thermal_x"],
        "rad_energy_late_over_early": energy_slope["late_over_early"],
        "rad_count_late_over_early": count_slope["late_over_early"],
        "hamiltonian_energy_drift": max(row["hamiltonian_energy"] for row in rows)
        - min(row["hamiltonian_energy"] for row in rows),
        "bare_energy_drift": max(row["bare_core_plus_rad_energy"] for row in rows)
        - min(row["bare_core_plus_rad_energy"] for row in rows),
    }
    return rows, summary


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run tiny autonomous sector evaporator.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--n-min", type=int, default=2)
    parser.add_argument("--n-max", type=int, default=4)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--mass-law", default="sqrt")
    parser.add_argument("--dos", default="exponential")
    parser.add_argument("--width-x", type=float, default=4.0)
    parser.add_argument("--operator", choices=["local", "scrambled"], default="scrambled")
    parser.add_argument("--mixers", default="none,dense,expander")
    parser.add_argument("--k-strength", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=0.08)
    parser.add_argument("--resonance-width-x", type=float, default=0.45)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--max-quanta", type=int, default=2)
    parser.add_argument("--mode-x", type=float, nargs="+", default=[0.5, 1.0, 1.5, 2.0, 3.0, 5.0])
    parser.add_argument("--x-edges", type=float, nargs="+", default=[0.0, 1.0, 2.0, 3.0, 5.0, float("inf")])
    parser.add_argument("--t-max", type=float, default=180.0)
    parser.add_argument("--time-points", type=int, default=121)
    parser.add_argument("--seeds", default="2468")
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "tiny_autonomous_sector_evaporator_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "tiny_autonomous_sector_evaporator_summary.csv",
    )
    args = parser.parse_args(argv)

    mixers = [part.strip() for part in args.mixers.split(",") if part.strip()]
    seeds = [int(part.strip()) for part in args.seeds.split(",") if part.strip()]
    all_rows = []
    summaries = []
    for seed in seeds:
        for mixer in mixers:
            print(f"[tiny-auto] seed={seed} mixer={mixer}", flush=True)
            rows, summary = run_case(args, mixer, seed)
            all_rows.extend(rows)
            summaries.append(summary)

    write_csv(args.timeseries_csv, all_rows)
    write_csv(args.summary_csv, summaries)
    print(f"[tiny-auto] wrote {args.timeseries_csv}")
    print(f"[tiny-auto] wrote {args.summary_csv}")
    print("mixer      dim  Erad    Nrad   <n>    TV     dE late/early  drift")
    for row in summaries:
        print(
            f"{str(row['mixer']):9s} "
            f"{int(row['hilbert_dim']):4d} "
            f"{float(row['final_rad_energy']):6.3f} "
            f"{float(row['final_rad_count']):6.3f} "
            f"{float(row['final_mean_n']):6.3f} "
            f"{float(row['final_spectrum_tv_to_thermal_x']):6.3f} "
            f"{float(row['rad_energy_late_over_early']):13.3f} "
            f"{float(row['hamiltonian_energy_drift']):8.2e}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
