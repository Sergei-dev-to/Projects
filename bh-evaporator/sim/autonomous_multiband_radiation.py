#!/usr/bin/env python3
"""Autonomous droplet evaporator with multiband hard radiation.

This is the spectral-emission extension of ``autonomous_integrated_droplet``.
The hard radiation sector has several energy bands, each with a short
waveguide.  The erosion coupling creates a hard quantum in a band and is
weighted only by energy detuning, not by a pre-imposed thermal spectrum.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from numpy.typing import NDArray

import autonomous_integrated_droplet as auto
from scan_bose_hubbard_dos import DATADIR


@dataclass(frozen=True)
class BasisState:
    stage: int
    droplet_index: int
    hard_mask: int


def parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]


def mode_index(band: int, pos: int, chain_length: int) -> int:
    return band * chain_length + pos


def mode_band(mode: int, chain_length: int) -> int:
    return mode // chain_length


def mode_pos(mode: int, chain_length: int) -> int:
    return mode % chain_length


def popcount(value: int) -> int:
    return int(value.bit_count())


def occupied(mask: int, mode: int) -> bool:
    return bool(mask & (1 << mode))


def add_mode(mask: int, mode: int) -> int:
    return mask | (1 << mode)


def move_mode(mask: int, src: int, dst: int) -> int:
    return (mask & ~(1 << src)) | (1 << dst)


def hard_masks(n_modes: int, max_quanta: int) -> list[int]:
    return [mask for mask in range(1 << n_modes) if popcount(mask) <= max_quanta]


def hard_energy(mask: int, bands: list[float], chain_length: int) -> float:
    total = 0.0
    for mode in range(len(bands) * chain_length):
        if occupied(mask, mode):
            total += bands[mode_band(mode, chain_length)]
    return total


def internal_energy(stage: auto.Stage, droplet_index: int, levels: int, spacing: float) -> float:
    core = auto.core_index(stage, droplet_index)
    centered = (core % levels) - 0.5 * (levels - 1)
    return spacing * centered


def build_basis(
    stages: list[auto.Stage], masks: list[int]
) -> tuple[list[BasisState], dict[BasisState, int]]:
    basis = [
        BasisState(stage.k, droplet_index, mask)
        for stage in stages
        for droplet_index in range(stage.droplet_dim)
        for mask in masks
    ]
    return basis, {state: idx for idx, state in enumerate(basis)}


def sparse_core_terms(
    rng: np.random.Generator, dim: int, degree: int, strength: float
) -> list[tuple[int, int, float]]:
    if dim <= 1 or degree <= 0 or strength <= 0:
        return []
    terms: dict[tuple[int, int], float] = {}
    for src in range(dim):
        targets = rng.choice(dim - 1, size=min(degree, dim - 1), replace=False)
        for raw in targets:
            dst = int(raw)
            if dst >= src:
                dst += 1
            a, b = sorted((src, dst))
            if (a, b) not in terms:
                terms[(a, b)] = strength * rng.normal() / np.sqrt(float(degree))
    out = []
    for (a, b), value in terms.items():
        out.append((a, b, value))
        out.append((b, a, value))
    return out


def thermal_target(bands: list[float], temperature: float) -> NDArray[np.float64]:
    weights = np.exp(-np.asarray(bands, dtype=float) / max(temperature, 1e-12))
    return weights / np.sum(weights)


def band_coupling_weight(profile: str, omega: float) -> float:
    if profile == "flat":
        return 1.0
    if profile == "inverse_omega":
        return 1.0 / max(omega, 1e-12)
    if profile == "inverse_sqrt_omega":
        return 1.0 / np.sqrt(max(omega, 1e-12))
    if profile == "sqrt_omega":
        return np.sqrt(max(omega, 1e-12))
    raise ValueError(f"unknown band coupling profile: {profile}")


def total_variation(p: NDArray[np.float64], q: NDArray[np.float64]) -> float:
    return float(0.5 * np.sum(np.abs(p - q)))


def entropy_from_eigs(eigs: NDArray[np.float64]) -> float:
    vals = eigs[eigs > 1e-14]
    if vals.size == 0:
        return 0.0
    return float(-np.sum(vals * np.log(vals)))


def renyi2_from_eigs(eigs: NDArray[np.float64]) -> float:
    purity = float(np.sum(eigs * eigs))
    return float(-np.log(max(purity, 1e-300)))


def reduced_entropy_tensor(
    psi: NDArray[np.complex128], dims: list[int], keep_axes: list[int]
) -> tuple[float, float]:
    if not keep_axes:
        return 0.0, 0.0
    keep_axes = sorted(keep_axes)
    trace_axes = [idx for idx in range(len(dims)) if idx not in keep_axes]
    perm = keep_axes + trace_axes
    tensor = np.transpose(psi.reshape(dims), perm)
    keep_dim = int(np.prod([dims[idx] for idx in keep_axes], dtype=np.int64))
    trace_dim = int(np.prod([dims[idx] for idx in trace_axes], dtype=np.int64))
    matrix = tensor.reshape((keep_dim, trace_dim))
    rho = matrix @ matrix.conj().T
    eigs = np.linalg.eigvalsh(rho).real
    eigs = np.clip(eigs, 0.0, 1.0)
    return entropy_from_eigs(eigs), renyi2_from_eigs(eigs)


def stage_offsets(stages: list[auto.Stage]) -> tuple[list[int], list[int]]:
    core_offsets = []
    rad_offsets = []
    core_total = 0
    rad_total = 0
    for stage in stages:
        core_offsets.append(core_total)
        rad_offsets.append(rad_total)
        core_total += stage.core_dim
        rad_total += stage.rad_dim
    return core_offsets, rad_offsets


def core_rad_entropy(
    psi: NDArray[np.complex128],
    stages: list[auto.Stage],
    basis: list[BasisState],
    masks: list[int],
) -> tuple[float, float, float]:
    mask_index = {mask: idx for idx, mask in enumerate(masks)}
    core_offsets, rad_offsets = stage_offsets(stages)
    core_dim = sum(stage.core_dim for stage in stages)
    rad_dim = sum(stage.rad_dim for stage in stages) * len(masks)
    coeff = np.zeros((core_dim, rad_dim), dtype=np.complex128)
    for amp, state in zip(psi, basis):
        if abs(amp) <= 1e-14:
            continue
        stage = stages[state.stage]
        core = auto.core_index(stage, state.droplet_index)
        rad_label = state.droplet_index % stage.rad_dim
        row = core_offsets[state.stage] + core
        col = (rad_offsets[state.stage] + rad_label) * len(masks) + mask_index[state.hard_mask]
        coeff[row, col] += amp
    rho_core = coeff @ coeff.conj().T
    eigs = np.linalg.eigvalsh(rho_core).real
    eigs = np.clip(eigs, 0.0, 1.0)
    return entropy_from_eigs(eigs), renyi2_from_eigs(eigs), float(np.sum(eigs * eigs))


def hard_entropy(
    psi: NDArray[np.complex128],
    basis: list[BasisState],
    masks: list[int],
) -> tuple[float, float, str]:
    mask_index = {mask: idx for idx, mask in enumerate(masks)}
    rest_keys: dict[tuple[int, int], int] = {}
    coeff = np.zeros((len(masks), len(basis)), dtype=np.complex128)
    rest_count = 0
    entries: list[tuple[int, int, complex]] = []
    for amp, state in zip(psi, basis):
        if abs(amp) <= 1e-14:
            continue
        rest = (state.stage, state.droplet_index)
        if rest not in rest_keys:
            rest_keys[rest] = rest_count
            rest_count += 1
        entries.append((mask_index[state.hard_mask], rest_keys[rest], amp))
    coeff = coeff[:, :rest_count]
    for hard_id, rest_id, amp in entries:
        coeff[hard_id, rest_id] += amp
    rho_hard = coeff @ coeff.conj().T
    eigs = np.linalg.eigvalsh(rho_hard).real
    eigs = np.clip(eigs, 0.0, 1.0)
    probs = np.zeros(len(masks), dtype=float)
    for p, state in zip(np.abs(psi) ** 2, basis):
        probs[mask_index[state.hard_mask]] += p
    number_probs: dict[int, float] = {}
    for mask, p in zip(masks, probs):
        number_probs[popcount(mask)] = number_probs.get(popcount(mask), 0.0) + float(p)
    number_probs_text = ";".join(f"{n}:{number_probs[n]:.8g}" for n in sorted(number_probs))
    return entropy_from_eigs(eigs), renyi2_from_eigs(eigs), number_probs_text


def final_shell_mi(
    psi: NDArray[np.complex128],
    stages: list[auto.Stage],
    basis: list[BasisState],
    masks: list[int],
    args: argparse.Namespace,
) -> tuple[float, float, float, float]:
    final = stages[-1]
    final_prob = 0.0
    for amp, state in zip(psi, basis):
        if state.stage == final.k:
            final_prob += float(abs(amp) ** 2)
    if final_prob <= 1e-12 or len(stages) < 3:
        return final_prob, 0.0, 0.0, 0.0

    early_dim = args.q ** (2 * args.L0 - 1)
    late_dim = final.rad_dim // early_dim
    if early_dim * late_dim != final.rad_dim:
        return final_prob, 0.0, 0.0, 0.0

    mask_index = {mask: idx for idx, mask in enumerate(masks)}
    tensor = np.zeros((final.core_dim, late_dim, early_dim, len(masks)), dtype=np.complex128)
    for amp, state in zip(psi, basis):
        if state.stage != final.k:
            continue
        core = auto.core_index(final, state.droplet_index)
        rad_label = state.droplet_index % final.rad_dim
        early = rad_label % early_dim
        late = rad_label // early_dim
        tensor[core, late, early, mask_index[state.hard_mask]] += amp / np.sqrt(final_prob)
    flat = tensor.reshape(-1)
    dims = [final.core_dim, late_dim, early_dim, len(masks)]
    early_entropy, _ = reduced_entropy_tensor(flat, dims, [2])
    late_entropy, _ = reduced_entropy_tensor(flat, dims, [1])
    both_entropy, _ = reduced_entropy_tensor(flat, dims, [1, 2])
    return final_prob, early_entropy + late_entropy - both_entropy, early_entropy, late_entropy


def build_hamiltonian(
    args: argparse.Namespace,
    stages: list[auto.Stage],
    basis: list[BasisState],
    index: dict[BasisState, int],
    masks: list[int],
    bands: list[float],
) -> sp.csr_matrix:
    rows: list[int] = []
    cols: list[int] = []
    data: list[complex] = []
    n_bands = len(bands)
    n_modes = n_bands * args.chain_length

    for idx, state in enumerate(basis):
        stage = stages[state.stage]
        energy = (
            stage.energy
            + internal_energy(stage, state.droplet_index, args.internal_levels, args.internal_spacing)
            + hard_energy(state.hard_mask, bands, args.chain_length)
        )
        rows.append(idx)
        cols.append(idx)
        data.append(energy)

    # Band-preserving propagation.
    for state in basis:
        col = index[state]
        for mode in range(n_modes):
            if not occupied(state.hard_mask, mode):
                continue
            band = mode_band(mode, args.chain_length)
            pos = mode_pos(mode, args.chain_length)
            for delta in (-1, 1):
                new_pos = pos + delta
                if not (0 <= new_pos < args.chain_length):
                    continue
                target_mode = mode_index(band, new_pos, args.chain_length)
                if occupied(state.hard_mask, target_mode):
                    continue
                target = BasisState(state.stage, state.droplet_index, move_mode(state.hard_mask, mode, target_mode))
                row = index.get(target)
                if row is None:
                    continue
                rows.append(row)
                cols.append(col)
                data.append(-args.chain_hop)

    # Sparse intra-core scrambling.
    if args.scramble_strength > 0 and args.scramble_degree > 0:
        for stage in stages:
            terms = sparse_core_terms(
                np.random.default_rng(args.seed + 1000 + stage.k),
                stage.core_dim,
                args.scramble_degree,
                args.scramble_strength,
            )
            for rad_label in range(stage.rad_dim):
                for mask in masks:
                    for a, b, val in terms:
                        source = BasisState(stage.k, a * stage.rad_dim + rad_label, mask)
                        target = BasisState(stage.k, b * stage.rad_dim + rad_label, mask)
                        rows.append(index[target])
                        cols.append(index[source])
                        data.append(val)

    # Energy-filtered erosion.  For each source and band, sample a sparse set of
    # next-sector shell/core targets.  The detuning filter enforces approximate
    # energy conservation without selecting a thermal spectrum by hand.
    for prev, nxt in zip(stages[:-1], stages[1:]):
        shell_dim = nxt.rad_dim // prev.rad_dim
        rng = np.random.default_rng(args.seed + 5000 + prev.k)
        for old_core in range(prev.core_dim):
            for rad_label in range(prev.rad_dim):
                source_idx = old_core * prev.rad_dim + rad_label
                source_e = prev.energy + internal_energy(prev, source_idx, args.internal_levels, args.internal_spacing)
                for mask in masks:
                    if popcount(mask) >= args.max_quanta:
                        continue
                    source = BasisState(prev.k, source_idx, mask)
                    col = index[source]
                    for band, omega in enumerate(bands):
                        local_mode = mode_index(band, 0, args.chain_length)
                        if occupied(mask, local_mode):
                            continue
                        target_mask = add_mode(mask, local_mode)
                        for _ in range(args.erosion_degree):
                            new_core = int(rng.integers(nxt.core_dim))
                            shell_label = int(rng.integers(shell_dim))
                            new_rad_label = shell_label * prev.rad_dim + rad_label
                            target_idx = new_core * nxt.rad_dim + new_rad_label
                            target_e = (
                                nxt.energy
                                + internal_energy(nxt, target_idx, args.internal_levels, args.internal_spacing)
                                + omega
                            )
                            detuning = source_e - target_e
                            envelope = np.exp(-0.5 * (detuning / args.detuning_width) ** 2)
                            if envelope <= args.matrix_cutoff:
                                continue
                            amp = (
                                args.erosion_coupling
                                * band_coupling_weight(args.band_coupling_profile, omega)
                                * envelope
                                * rng.normal()
                                / np.sqrt(float(args.erosion_degree))
                            )
                            target = BasisState(nxt.k, target_idx, target_mask)
                            row = index[target]
                            rows.append(row)
                            cols.append(col)
                            data.append(amp)
                            rows.append(col)
                            cols.append(row)
                            data.append(amp)

    return sp.coo_matrix((data, (rows, cols)), shape=(len(basis), len(basis))).tocsr()


def initial_state(
    args: argparse.Namespace,
    stages: list[auto.Stage],
    basis: list[BasisState],
    index: dict[BasisState, int],
) -> NDArray[np.complex128]:
    rng = np.random.default_rng(args.seed + 10_000)
    psi = np.zeros(len(basis), dtype=np.complex128)
    top = stages[0]
    candidates = []
    for core in range(top.core_dim):
        droplet_index = core * top.rad_dim
        eps = internal_energy(top, droplet_index, args.internal_levels, args.internal_spacing)
        if args.initial_energy_window < 0 or abs(eps - args.initial_internal_energy) <= args.initial_energy_window:
            candidates.append(droplet_index)
    if not candidates:
        candidates = list(range(top.core_dim))
    if args.initial_state == "basis":
        psi[index[BasisState(0, candidates[0], 0)]] = 1.0
    elif args.initial_state == "haar":
        raw = rng.normal(size=len(candidates)) + 1j * rng.normal(size=len(candidates))
        raw /= np.sqrt(float(np.vdot(raw, raw).real))
        for droplet_index, amp in zip(candidates, raw):
            psi[index[BasisState(0, droplet_index, 0)]] = amp
    else:
        raise ValueError(f"unknown initial state: {args.initial_state}")
    return psi


def observables(
    psi: NDArray[np.complex128],
    hmat: sp.csr_matrix,
    stages: list[auto.Stage],
    basis: list[BasisState],
    masks: list[int],
    bands: list[float],
    args: argparse.Namespace,
) -> dict[str, float | str]:
    probs = np.abs(psi) ** 2
    stage_probs = np.zeros(len(stages), dtype=float)
    band_counts = np.zeros(len(bands), dtype=float)
    pos_counts = np.zeros(args.chain_length, dtype=float)
    mean_l = 0.0
    mean_quanta = 0.0
    hard_e = 0.0
    for p, state in zip(probs, basis):
        stage = stages[state.stage]
        stage_probs[state.stage] += p
        mean_l += p * stage.L
        for mode in range(len(bands) * args.chain_length):
            if occupied(state.hard_mask, mode):
                band = mode_band(mode, args.chain_length)
                pos = mode_pos(mode, args.chain_length)
                band_counts[band] += p
                pos_counts[pos] += p
                mean_quanta += p
                hard_e += p * bands[band]
    if mean_quanta > 1e-12:
        band_probs = band_counts / mean_quanta
    else:
        band_probs = np.ones(len(bands), dtype=float) / len(bands)
    temp = 2.0 * args.sigma / (max(mean_l, 1e-12) * np.log(args.q))
    target = thermal_target(bands, temp)
    h_expect = complex(np.vdot(psi, hmat @ psi))
    cr_entropy, cr_renyi2, cr_purity = core_rad_entropy(psi, stages, basis, masks)
    hard_s, hard_s2, number_probs = hard_entropy(psi, basis, masks)
    final_prob, shell_mi, shell_early_s, shell_late_s = final_shell_mi(
        psi, stages, basis, masks, args
    )
    return {
        "mean_L": float(mean_l),
        "mean_quanta": float(mean_quanta),
        "hard_energy": float(hard_e),
        "temperature_proxy": float(temp),
        "core_radiation_entropy": cr_entropy,
        "core_radiation_renyi2": cr_renyi2,
        "core_radiation_purity": cr_purity,
        "hard_entropy": hard_s,
        "hard_renyi2": hard_s2,
        "hard_number_probs": number_probs,
        "final_sector_postselection_prob": final_prob,
        "final_sector_postselected_shell_mi": shell_mi,
        "final_sector_postselected_early_shell_entropy": shell_early_s,
        "final_sector_postselected_late_shell_entropy": shell_late_s,
        "band_tv_to_thermal": total_variation(band_probs, target),
        "band_probs": ";".join(f"{p:.8g}" for p in band_probs),
        "thermal_band_target": ";".join(f"{p:.8g}" for p in target),
        "chain_far": float(np.sum(pos_counts[max(1, args.chain_length // 2) :])),
        "hamiltonian_energy": float(h_expect.real),
        "hamiltonian_energy_imag": float(h_expect.imag),
        **{f"p_stage_{idx}": float(val) for idx, val in enumerate(stage_probs)},
        **{f"band_count_{idx}": float(val) for idx, val in enumerate(band_counts)},
    }


def summarize(rows: list[dict[str, float | str]]) -> dict[str, float | str]:
    final = rows[-1]
    best_final = max(rows, key=lambda row: float(row.get("p_stage_2", 0.0)))
    best_entropy = max(rows, key=lambda row: float(row["core_radiation_entropy"]))
    hvals = [float(row["hamiltonian_energy"]) for row in rows]
    hard = [float(row["hard_energy"]) for row in rows]
    return {
        "case": final["case"],
        "basis_dim": final["basis_dim"],
        "bands": final["bands"],
        "chain_length": final["chain_length"],
        "final_mean_L": final["mean_L"],
        "final_hard_energy": final["hard_energy"],
        "max_hard_energy": max(hard),
        "final_p_final_stage": final.get("p_stage_2", 0.0),
        "max_p_final_stage": best_final.get("p_stage_2", 0.0),
        "final_band_tv_to_thermal": final["band_tv_to_thermal"],
        "min_band_tv_to_thermal": min(float(row["band_tv_to_thermal"]) for row in rows),
        "max_core_radiation_entropy": best_entropy["core_radiation_entropy"],
        "final_core_radiation_entropy": final["core_radiation_entropy"],
        "final_core_radiation_renyi2": final["core_radiation_renyi2"],
        "final_hard_entropy": final["hard_entropy"],
        "final_hard_renyi2": final["hard_renyi2"],
        "final_shell_mi": final["final_sector_postselected_shell_mi"],
        "max_shell_mi": max(float(row["final_sector_postselected_shell_mi"]) for row in rows),
        "hard_number_probs_final": final["hard_number_probs"],
        "final_band_probs": final["band_probs"],
        "final_thermal_target": final["thermal_band_target"],
        "final_chain_far": final["chain_far"],
        "max_energy_drift": max(hvals) - min(hvals),
    }


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | str]], dict[str, float | str]]:
    bands = parse_float_list(args.bands)
    stages = auto.build_stages(args.L0, args.Lmin, args.q, args.sigma)
    masks = hard_masks(len(bands) * args.chain_length, args.max_quanta)
    basis, index = build_basis(stages, masks)
    hmat = build_hamiltonian(args, stages, basis, index, masks, bands)
    psi0 = initial_state(args, stages, basis, index)
    times = np.linspace(0.0, args.t_max, args.time_points)
    rows: list[dict[str, float | str]] = []
    for time, psi in zip(
        times,
        spla.expm_multiply((-1j) * hmat, psi0, start=0.0, stop=args.t_max, num=args.time_points),
    ):
        rows.append(
            {
                "case": args.case_name,
                "time": float(time),
                "basis_dim": len(basis),
                "bands": args.bands,
                "chain_length": args.chain_length,
                **observables(psi, hmat, stages, basis, masks, bands, args),
            }
        )
    return rows, summarize(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run autonomous multiband radiation model.")
    parser.add_argument("--case-name", default="multiband_main")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--L0", type=int, default=3)
    parser.add_argument("--Lmin", type=int, default=1)
    parser.add_argument("--bands", default="2,3,4,5,6")
    parser.add_argument("--chain-length", type=int, default=3)
    parser.add_argument("--max-quanta", type=int, default=2)
    parser.add_argument("--chain-hop", type=float, default=1.0)
    parser.add_argument("--scramble-strength", type=float, default=0.20)
    parser.add_argument("--scramble-degree", type=int, default=4)
    parser.add_argument("--erosion-coupling", type=float, default=0.35)
    parser.add_argument(
        "--band-coupling-profile",
        choices=["flat", "inverse_omega", "inverse_sqrt_omega", "sqrt_omega"],
        default="flat",
    )
    parser.add_argument("--erosion-degree", type=int, default=6)
    parser.add_argument("--detuning-width", type=float, default=0.75)
    parser.add_argument("--internal-levels", type=int, default=7)
    parser.add_argument("--internal-spacing", type=float, default=1.0)
    parser.add_argument("--initial-internal-energy", type=float, default=1.0)
    parser.add_argument("--initial-energy-window", type=float, default=-1.0)
    parser.add_argument("--matrix-cutoff", type=float, default=1e-12)
    parser.add_argument("--initial-state", choices=["basis", "haar"], default="haar")
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--t-max", type=float, default=60.0)
    parser.add_argument("--time-points", type=int, default=31)
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "autonomous_multiband_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "autonomous_multiband_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    write_csv(args.timeseries_csv, rows)
    write_csv(args.summary_csv, [summary])
    print(f"[multiband] wrote {args.timeseries_csv}")
    print(f"[multiband] wrote {args.summary_csv}")
    print(
        "dim={basis_dim} final_L={final_mean_L:.3f} p_final={final_p_final_stage:.3f} "
        "Ehard={final_hard_energy:.3f} TV={final_band_tv_to_thermal:.3f} "
        "drift={max_energy_drift:.2e}".format(**summary)
    )
    print(f"bands={summary['final_band_probs']} thermal={summary['final_thermal_target']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
