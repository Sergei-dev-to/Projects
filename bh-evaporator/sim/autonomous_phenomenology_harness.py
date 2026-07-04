#!/usr/bin/env python3
"""Phenomenology harness for the autonomous droplet Hamiltonian.

This script keeps the autonomous Hamiltonian fixed and measures the black-hole
evaporation diagnostics directly from the evolved state.  The staged Hilbert
space is a direct sum over droplet-size sectors, so the main core/radiation
entropy is computed with the sector label included in the coarse-grained split.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
import scipy.sparse.linalg as spla

import autonomous_integrated_droplet as auto
from scan_bose_hubbard_dos import DATADIR


@dataclass(frozen=True)
class Case:
    name: str
    chain_length: int
    scramble_mode: str
    scramble_strength: float
    erosion_coupling: float
    chain_hop: float
    hard_energy: float | None
    initial_state: str
    seed: int


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


def build_args(base: argparse.Namespace, case: Case) -> argparse.Namespace:
    hard_energy = case.hard_energy
    if hard_energy is None:
        hard_energy = 4.0 * base.sigma
    return argparse.Namespace(
        q=base.q,
        sigma=base.sigma,
        L0=base.L0,
        Lmin=base.Lmin,
        chain_length=case.chain_length,
        max_quanta=base.L0 - base.Lmin,
        hard_energy=hard_energy,
        chain_hop=case.chain_hop,
        scramble_mode=case.scramble_mode,
        scramble_strength=case.scramble_strength,
        scramble_degree=base.scramble_degree,
        erosion_coupling=case.erosion_coupling,
        far_sink_strength=0.0,
        matrix_cutoff=1e-12,
        initial_state=case.initial_state,
        seed=case.seed,
        t_max=base.t_max,
        time_points=base.time_points,
    )


def parse_cases(base: argparse.Namespace) -> list[Case]:
    if base.case == "main":
        return [
            Case(
                name="main_chain14",
                chain_length=14,
                scramble_mode="sparse",
                scramble_strength=0.25,
                erosion_coupling=0.50,
                chain_hop=1.20,
                hard_energy=None,
                initial_state="haar",
                seed=base.seed,
            )
        ]
    if base.case == "suite":
        return [
            Case("main_chain14", 14, "sparse", 0.25, 0.50, 1.20, None, "haar", base.seed),
            Case("short_chain5", 5, "sparse", 0.25, 0.50, 1.20, None, "haar", base.seed),
            Case("no_scramble_chain10", 10, "none", 0.0, 0.50, 1.20, None, "haar", base.seed),
            Case("weak_scramble_chain10", 10, "sparse", 0.05, 0.50, 1.20, None, "haar", base.seed),
            Case("wrong_energy_chain10", 10, "sparse", 0.25, 0.50, 1.20, 2.0 * base.sigma, "haar", base.seed),
        ]
    if base.case == "controls":
        return [
            Case("short_chain5", 5, "sparse", 0.25, 0.50, 1.20, None, "haar", base.seed),
            Case("no_scramble_chain10", 10, "none", 0.0, 0.50, 1.20, None, "haar", base.seed),
            Case("weak_scramble_chain10", 10, "sparse", 0.05, 0.50, 1.20, None, "haar", base.seed),
            Case("wrong_energy_chain10", 10, "sparse", 0.25, 0.50, 1.20, 2.0 * base.sigma, "haar", base.seed),
        ]
    if base.case == "basis_controls":
        return [
            Case("basis_sparse_chain10", 10, "sparse", 0.25, 0.50, 1.20, None, "basis", base.seed),
            Case("basis_no_scramble_chain10", 10, "none", 0.0, 0.50, 1.20, None, "basis", base.seed),
        ]
    raise ValueError(f"unknown case set: {base.case}")


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
    basis: list[auto.BasisState],
    masks: list[int],
) -> tuple[float, float, float, float]:
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
        col = (rad_offsets[state.stage] + rad_label) * len(masks) + mask_index[state.chain_mask]
        coeff[row, col] += amp
    rho_core = coeff @ coeff.conj().T
    eigs = np.linalg.eigvalsh(rho_core).real
    eigs = np.clip(eigs, 0.0, 1.0)
    entropy = entropy_from_eigs(eigs)
    renyi2 = renyi2_from_eigs(eigs)
    purity = float(np.sum(eigs * eigs))
    return entropy, renyi2, purity, float(np.linalg.norm(psi))


def chain_entropy(
    psi: NDArray[np.complex128],
    basis: list[auto.BasisState],
    masks: list[int],
) -> tuple[float, float, str]:
    mask_index = {mask: idx for idx, mask in enumerate(masks)}
    rest_keys: dict[tuple[int, int], int] = {}
    rest_ids = np.empty(len(basis), dtype=np.int64)
    chain_ids = np.empty(len(basis), dtype=np.int64)
    for idx, state in enumerate(basis):
        key = (state.stage, state.droplet_index)
        if key not in rest_keys:
            rest_keys[key] = len(rest_keys)
        rest_ids[idx] = rest_keys[key]
        chain_ids[idx] = mask_index[state.chain_mask]
    coeff = np.zeros((len(masks), len(rest_keys)), dtype=np.complex128)
    for amp, chain_id, rest_id in zip(psi, chain_ids, rest_ids):
        if abs(amp) > 1e-14:
            coeff[chain_id, rest_id] += amp
    rho_chain = coeff @ coeff.conj().T
    eigs = np.linalg.eigvalsh(rho_chain).real
    eigs = np.clip(eigs, 0.0, 1.0)
    probs = np.zeros(len(masks), dtype=float)
    for p, state in zip(np.abs(psi) ** 2, basis):
        probs[mask_index[state.chain_mask]] += p
    number_probs: dict[int, float] = {}
    for mask, p in zip(masks, probs):
        number_probs[auto.popcount(mask)] = number_probs.get(auto.popcount(mask), 0.0) + float(p)
    number_probs_text = ";".join(f"{n}:{number_probs[n]:.8g}" for n in sorted(number_probs))
    return entropy_from_eigs(eigs), renyi2_from_eigs(eigs), number_probs_text


def final_shell_mi(
    psi: NDArray[np.complex128],
    stages: list[auto.Stage],
    basis: list[auto.BasisState],
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
        tensor[core, late, early, mask_index[state.chain_mask]] += amp / np.sqrt(final_prob)
    flat = tensor.reshape(-1)
    dims = [final.core_dim, late_dim, early_dim, len(masks)]
    early_entropy, _ = reduced_entropy_tensor(flat, dims, [2])
    late_entropy, _ = reduced_entropy_tensor(flat, dims, [1])
    both_entropy, _ = reduced_entropy_tensor(flat, dims, [1, 2])
    return final_prob, early_entropy + late_entropy - both_entropy, early_entropy, late_entropy


def thermo_values(mean_L: float, q: int, sigma: float) -> dict[str, float]:
    lval = max(mean_L, 1e-12)
    energy = 4.0 * sigma * lval
    entropy = lval * lval * np.log(q)
    temperature = 2.0 * sigma / (lval * np.log(q))
    heat_capacity = -2.0 * lval * lval * np.log(q)
    power_proxy = 4.0 * lval * temperature**3
    return {
        "core_energy_proxy": float(energy),
        "micro_entropy_proxy": float(entropy),
        "temperature_proxy": float(temperature),
        "heat_capacity_proxy": float(heat_capacity),
        "power_2d_proxy": float(power_proxy),
        "E2_power_proxy": float(energy * energy * power_proxy),
    }


def run_case(base: argparse.Namespace, case: Case) -> tuple[list[dict[str, float | int | str]], dict[str, float | int | str]]:
    args = build_args(base, case)
    stages = auto.build_stages(args.L0, args.Lmin, args.q, args.sigma)
    basis, basis_index, masks = auto.build_basis(stages, args.chain_length, args.max_quanta)

    def index_of_local(_basis, state):
        return basis_index[state]

    auto.index_of = index_of_local  # type: ignore[assignment]
    hmat = auto.build_hamiltonian(args, stages, basis, basis_index, masks)
    psi0 = auto.initial_state(stages, basis, args)
    times = np.linspace(0.0, args.t_max, args.time_points)
    rows: list[dict[str, float | int | str]] = []
    h0 = float(np.vdot(psi0, hmat @ psi0).real)
    for time, psi in zip(
        times,
        spla.expm_multiply((-1j) * hmat, psi0, start=0.0, stop=args.t_max, num=args.time_points),
    ):
        obs = auto.observables(psi, hmat, stages, basis, args)
        cr_entropy, cr_renyi2, cr_purity, norm = core_rad_entropy(psi, stages, basis, masks)
        hard_entropy, hard_renyi2, number_probs = chain_entropy(psi, basis, masks)
        final_prob, shell_mi, shell_early_s, shell_late_s = final_shell_mi(psi, stages, basis, masks, args)
        rows.append(
            {
                "case": case.name,
                "time": float(time),
                "basis_dim": len(basis),
                "chain_length": args.chain_length,
                "scramble_mode": args.scramble_mode,
                "scramble_strength": args.scramble_strength,
                "erosion_coupling": args.erosion_coupling,
                "chain_hop": args.chain_hop,
                "hard_energy_unit": args.hard_energy,
                "initial_state": args.initial_state,
                "state_norm": norm,
                "hamiltonian_energy_drift_from_initial": float(obs["hamiltonian_energy"] - h0),
                "core_radiation_entropy": cr_entropy,
                "core_radiation_renyi2": cr_renyi2,
                "core_radiation_purity": cr_purity,
                "hard_chain_entropy": hard_entropy,
                "hard_chain_renyi2": hard_renyi2,
                "hard_number_probs": number_probs,
                "final_sector_postselected_shell_mi": shell_mi,
                "final_sector_postselected_early_shell_entropy": shell_early_s,
                "final_sector_postselected_late_shell_entropy": shell_late_s,
                "final_sector_postselection_prob": final_prob,
                **obs,
                **thermo_values(float(obs["mean_L"]), args.q, args.sigma),
            }
        )
    summary = summarize_case(rows)
    return rows, summary


def first_time_at(rows: list[dict[str, float | int | str]], key: str, threshold: float) -> float:
    for row in rows:
        if float(row[key]) >= threshold:
            return float(row["time"])
    return float("nan")


def summarize_case(rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str]:
    times = np.asarray([float(row["time"]) for row in rows])
    hard = np.asarray([float(row["hard_energy"]) for row in rows])
    mean_l = np.asarray([float(row["mean_L"]) for row in rows])
    power = np.gradient(hard, times) if len(times) > 1 else np.zeros_like(hard)
    final = rows[-1]
    best_final = max(rows, key=lambda row: float(row["p_final_stage"]))
    best_l = min(rows, key=lambda row: float(row["mean_L"]))
    best_entropy = max(rows, key=lambda row: float(row["core_radiation_entropy"]))
    return {
        "case": final["case"],
        "basis_dim": final["basis_dim"],
        "chain_length": final["chain_length"],
        "scramble_mode": final["scramble_mode"],
        "scramble_strength": final["scramble_strength"],
        "hard_energy_unit": final["hard_energy_unit"],
        "final_mean_L": final["mean_L"],
        "best_mean_L": best_l["mean_L"],
        "final_p_final_stage": final["p_final_stage"],
        "max_p_final_stage": best_final["p_final_stage"],
        "time_to_p_final_0p5": first_time_at(rows, "p_final_stage", 0.5),
        "time_to_p_final_0p75": first_time_at(rows, "p_final_stage", 0.75),
        "final_hard_energy": final["hard_energy"],
        "max_hard_energy": float(np.max(hard)),
        "max_positive_power": float(np.max(power)),
        "min_power": float(np.min(power)),
        "final_core_radiation_entropy": final["core_radiation_entropy"],
        "max_core_radiation_entropy": best_entropy["core_radiation_entropy"],
        "final_core_radiation_renyi2": final["core_radiation_renyi2"],
        "final_hard_chain_entropy": final["hard_chain_entropy"],
        "final_hard_chain_renyi2": final["hard_chain_renyi2"],
        "final_shell_mi": final["final_sector_postselected_shell_mi"],
        "max_shell_mi": max(float(row["final_sector_postselected_shell_mi"]) for row in rows),
        "final_chain_far": final["chain_far"],
        "max_abs_energy_drift": max(abs(float(row["hamiltonian_energy_drift_from_initial"])) for row in rows),
        "hard_number_probs_final": final["hard_number_probs"],
        "mean_L_drop": float(mean_l[0] - mean_l[-1]),
    }


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run autonomous phenomenology harness.")
    parser.add_argument("--case", choices=["main", "suite", "controls", "basis_controls"], default="suite")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--L0", type=int, default=3)
    parser.add_argument("--Lmin", type=int, default=1)
    parser.add_argument("--scramble-degree", type=int, default=4)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--t-max", type=float, default=80.0)
    parser.add_argument("--time-points", type=int, default=41)
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "autonomous_phenomenology_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "autonomous_phenomenology_summary.csv",
    )
    args = parser.parse_args(argv)
    all_rows: list[dict[str, float | int | str]] = []
    summaries: list[dict[str, float | int | str]] = []
    for case in parse_cases(args):
        print(f"[autonomous-harness] running {case.name}")
        rows, summary = run_case(args, case)
        all_rows.extend(rows)
        summaries.append(summary)
        print(
            "[autonomous-harness] {case} dim={basis_dim} final_L={final_mean_L:.3f} "
            "p_final={final_p_final_stage:.3f} hard={final_hard_energy:.3f} "
            "Srad={final_core_radiation_entropy:.3f} MI={final_shell_mi:.3f}".format(**summary)
        )
    write_csv(args.timeseries_csv, all_rows)
    write_csv(args.summary_csv, summaries)
    print(f"[autonomous-harness] wrote {args.timeseries_csv}")
    print(f"[autonomous-harness] wrote {args.summary_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
