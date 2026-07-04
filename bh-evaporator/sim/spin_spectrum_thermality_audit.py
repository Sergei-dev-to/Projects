#!/usr/bin/env python3
"""Thermality audit for the autonomous spin-spectrum evaporator.

This script compares three different notions of the emitted hard spectrum:

1. final radiation-chain occupation;
2. time-integrated outward erosion current;
3. time-integrated golden-rule tendency from the actual erosion matrix.

It also compares these spectra against pure Boltzmann, phase-space corrected
Boltzmann, and first-step spin-spectrum transition weights.
"""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
import scipy.sparse.linalg as spla
from numpy.typing import NDArray

import autonomous_spin_spectrum_multiband as base
from scan_bose_hubbard_dos import DATADIR


@dataclass(frozen=True)
class ErosionEdge:
    src: int
    dst: int
    band: int
    omega: float
    value: float
    detuning: float
    overlap: float
    stage: int


def normalize(weights: NDArray[np.float64]) -> NDArray[np.float64]:
    total = float(np.sum(weights))
    if total <= 1e-14:
        return np.ones_like(weights) / len(weights)
    return weights / total


def tv(p: NDArray[np.float64], q: NDArray[np.float64]) -> float:
    return float(0.5 * np.sum(np.abs(p - q)))


def boltzmann_target(bands: list[float], temperature: float, phase_power: float) -> NDArray[np.float64]:
    omega = np.asarray(bands, dtype=float)
    weights = np.power(omega, phase_power) * np.exp(-omega / max(temperature, 1e-12))
    return normalize(weights)


def build_erosion_edges(
    args: argparse.Namespace,
    stages: list[base.Stage],
    basis_index: dict[base.BasisState, int],
    masks: list[int],
    bands: list[float],
) -> list[ErosionEdge]:
    edges: list[ErosionEdge] = []
    overlaps = {
        prev.k: base.shell_overlap_terms(prev, nxt, args)
        for prev, nxt in zip(stages[:-1], stages[1:])
    }
    for prev, nxt in zip(stages[:-1], stages[1:]):
        shell_dim = nxt.rad_dim // prev.rad_dim
        for old_eig in range(prev.core_dim):
            source_base_energy = prev.energy + prev.eigvals[old_eig]
            for rad in range(prev.rad_dim):
                for mask in masks:
                    if base.popcount(mask) >= args.max_quanta:
                        continue
                    source = base.BasisState(prev.k, old_eig, rad, mask)
                    src = basis_index[source]
                    for band, omega in enumerate(bands):
                        local_mode = base.mode_index(band, 0, args.chain_length)
                        if base.occupied(mask, local_mode):
                            continue
                        target_mask = base.add_mode(mask, local_mode)
                        for new_eig, shell, overlap in overlaps[prev.k][old_eig]:
                            new_rad = shell * prev.rad_dim + rad
                            if new_rad >= nxt.rad_dim or shell >= shell_dim:
                                continue
                            target_energy = nxt.energy + nxt.eigvals[new_eig] + omega
                            detuning = source_base_energy - target_energy
                            envelope = np.exp(-0.5 * (detuning / args.detuning_width) ** 2)
                            val = args.erosion_coupling * overlap * envelope
                            if abs(val) <= args.matrix_cutoff:
                                continue
                            target = base.BasisState(nxt.k, new_eig, new_rad, target_mask)
                            dst = basis_index[target]
                            edges.append(
                                ErosionEdge(
                                    src=src,
                                    dst=dst,
                                    band=band,
                                    omega=omega,
                                    value=float(val),
                                    detuning=float(detuning),
                                    overlap=float(overlap),
                                    stage=prev.k,
                                )
                            )
    return edges


def first_step_targets(
    args: argparse.Namespace,
    stages: list[base.Stage],
    bands: list[float],
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Return DOS-only and matrix-element first-step spectral weights.

    The source ensemble is the same initial energy window used by the run.
    DOS-only keeps only the energy-conservation envelope.  Matrix-element
    weights also include the site-basis shell-removal overlap.
    """
    top = stages[0]
    nxt = stages[1]
    overlaps = base.shell_overlap_terms(top, nxt, args)
    candidates = [
        eig for eig, value in enumerate(top.eigvals)
        if abs(float(value) - args.initial_internal_energy) <= args.initial_energy_window
    ]
    if not candidates:
        candidates = list(range(top.core_dim))

    dos = np.zeros(len(bands), dtype=float)
    matrix = np.zeros(len(bands), dtype=float)
    for old_eig in candidates:
        source_base_energy = top.energy + top.eigvals[old_eig]
        for band, omega in enumerate(bands):
            for new_eig, _shell, overlap in overlaps[old_eig]:
                target_energy = nxt.energy + nxt.eigvals[new_eig] + omega
                detuning = source_base_energy - target_energy
                envelope2 = np.exp(-((detuning / args.detuning_width) ** 2))
                dos[band] += envelope2
                matrix[band] += (overlap * overlap) * envelope2
    return normalize(dos), normalize(matrix)


def final_occupation_distribution(
    psi: NDArray[np.complex128],
    basis: list[base.BasisState],
    bands: list[float],
    args: argparse.Namespace,
) -> NDArray[np.float64]:
    probs = np.abs(psi) ** 2
    counts = np.zeros(len(bands), dtype=float)
    for p, state in zip(probs, basis):
        if p <= 1e-14:
            continue
        for mode in range(len(bands) * args.chain_length):
            if base.occupied(state.hard_mask, mode):
                counts[base.mode_band(mode, args.chain_length)] += p
    return normalize(counts)


def audit(args: argparse.Namespace) -> dict[str, str | float]:
    bands = base.parse_float_list(args.bands)
    stages = base.build_stages(args)
    masks = base.hard_masks(len(bands) * args.chain_length, args.max_quanta)
    basis, index = base.build_basis(stages, masks)
    hmat = base.build_hamiltonian(args, stages, basis, index, masks, bands)
    psi0 = base.initial_state(args, stages, index)
    edges = build_erosion_edges(args, stages, index, masks, bands)

    src = np.asarray([edge.src for edge in edges], dtype=np.int64)
    dst = np.asarray([edge.dst for edge in edges], dtype=np.int64)
    edge_band = np.asarray([edge.band for edge in edges], dtype=np.int64)
    val = np.asarray([edge.value for edge in edges], dtype=float)

    times = np.linspace(0.0, args.t_max, args.time_points)
    signed = np.zeros((len(times), len(bands)), dtype=float)
    outward = np.zeros_like(signed)
    inward = np.zeros_like(signed)
    tendency = np.zeros_like(signed)
    final_psi: NDArray[np.complex128] | None = None

    for ti, psi in enumerate(
        spla.expm_multiply((-1j) * hmat, psi0, start=0.0, stop=args.t_max, num=args.time_points)
    ):
        final_psi = psi
        currents = 2.0 * np.imag(val * psi[src] * np.conj(psi[dst]))
        strengths = (np.abs(psi[src]) ** 2) * (val * val)
        for band in range(len(bands)):
            mask = edge_band == band
            band_currents = currents[mask]
            signed[ti, band] = np.sum(band_currents)
            outward[ti, band] = np.sum(np.maximum(band_currents, 0.0))
            inward[ti, band] = np.sum(np.maximum(-band_currents, 0.0))
            tendency[ti, band] = np.sum(strengths[mask])

    assert final_psi is not None
    signed_int = np.trapezoid(signed, times, axis=0)
    outward_int = np.trapezoid(outward, times, axis=0)
    inward_int = np.trapezoid(inward, times, axis=0)
    tendency_int = np.trapezoid(tendency, times, axis=0)

    final_occ = final_occupation_distribution(final_psi, basis, bands, args)
    signed_dist = normalize(np.maximum(signed_int, 0.0))
    outward_dist = normalize(outward_int)
    tendency_dist = normalize(tendency_int)
    dos_target, matrix_target = first_step_targets(args, stages, bands)

    temp_l0 = 2.0 * args.sigma / (args.L0 * np.log(args.q))
    boltz0 = boltzmann_target(bands, temp_l0, 0.0)
    boltz1 = boltzmann_target(bands, temp_l0, 1.0)
    boltz2 = boltzmann_target(bands, temp_l0, 2.0)

    def fmt(vec: NDArray[np.float64]) -> str:
        return ";".join(f"{x:.8g}" for x in vec)

    return {
        "case": args.case_name,
        "basis_dim": len(basis),
        "edge_count": len(edges),
        "bands": args.bands,
        "chain_length": args.chain_length,
        "overlap_degree": args.overlap_degree,
        "detuning_width": args.detuning_width,
        "internal_std": args.internal_std,
        "final_occ": fmt(final_occ),
        "signed_flux": fmt(signed_dist),
        "outward_flux": fmt(outward_dist),
        "inward_flux": fmt(normalize(inward_int)),
        "matrix_tendency": fmt(tendency_dist),
        "target_boltz_p0": fmt(boltz0),
        "target_phase_p1": fmt(boltz1),
        "target_phase_p2": fmt(boltz2),
        "target_dos_first": fmt(dos_target),
        "target_matrix_first": fmt(matrix_target),
        "tv_final_boltz_p0": tv(final_occ, boltz0),
        "tv_final_phase_p1": tv(final_occ, boltz1),
        "tv_final_phase_p2": tv(final_occ, boltz2),
        "tv_final_dos_first": tv(final_occ, dos_target),
        "tv_final_matrix_first": tv(final_occ, matrix_target),
        "tv_outward_boltz_p0": tv(outward_dist, boltz0),
        "tv_outward_phase_p1": tv(outward_dist, boltz1),
        "tv_outward_phase_p2": tv(outward_dist, boltz2),
        "tv_outward_dos_first": tv(outward_dist, dos_target),
        "tv_outward_matrix_first": tv(outward_dist, matrix_target),
        "tv_tendency_boltz_p0": tv(tendency_dist, boltz0),
        "tv_tendency_phase_p1": tv(tendency_dist, boltz1),
        "tv_tendency_phase_p2": tv(tendency_dist, boltz2),
        "tv_tendency_dos_first": tv(tendency_dist, dos_target),
        "tv_tendency_matrix_first": tv(tendency_dist, matrix_target),
        "net_flux_total": float(np.sum(signed_int)),
        "outward_flux_total": float(np.sum(outward_int)),
        "inward_flux_total": float(np.sum(inward_int)),
        "tendency_total": float(np.sum(tendency_int)),
    }


def write_csv(path: pathlib.Path, rows: list[dict[str, str | float]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Audit hard thermality in the spin-spectrum evaporator.")
    p.add_argument("--case-name", default="thermality_audit")
    p.add_argument("--q", type=int, default=2)
    p.add_argument("--sigma", type=float, default=1.0)
    p.add_argument("--L0", type=int, default=3)
    p.add_argument("--Lmin", type=int, default=1)
    p.add_argument("--bands", default="2,3,4,5,6")
    p.add_argument("--chain-length", type=int, default=3)
    p.add_argument("--max-quanta", type=int, default=2)
    p.add_argument("--chain-hop", type=float, default=1.0)
    p.add_argument("--erosion-coupling", type=float, default=0.55)
    p.add_argument("--detuning-width", type=float, default=0.75)
    p.add_argument("--overlap-degree", type=int, default=16)
    p.add_argument("--overlap-cutoff", type=float, default=1e-10)
    p.add_argument("--h-field", type=float, default=0.25)
    p.add_argument("--j-zz", type=float, default=0.20)
    p.add_argument("--lambda-x", type=float, default=0.75)
    p.add_argument("--random-field", type=float, default=0.07)
    p.add_argument("--internal-std", type=float, default=2.0)
    p.add_argument("--initial-internal-energy", type=float, default=-1.0)
    p.add_argument("--initial-energy-window", type=float, default=0.75)
    p.add_argument("--matrix-cutoff", type=float, default=1e-12)
    p.add_argument("--initial-state", choices=["basis", "haar"], default="haar")
    p.add_argument("--seed", type=int, default=2468)
    p.add_argument("--t-max", type=float, default=60.0)
    p.add_argument("--time-points", type=int, default=31)
    p.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "spin_spectrum_thermality_audit.csv",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    row = audit(args)
    write_csv(args.summary_csv, [row])
    print(f"[audit] wrote {args.summary_csv}")
    print(
        "dim={basis_dim} edges={edge_count} finalTV={tv_final_boltz_p0:.3f} "
        "outTV={tv_outward_boltz_p0:.3f} tendTV={tv_tendency_boltz_p0:.3f}".format(**row)
    )
    print(f"final={row['final_occ']}")
    print(f"outward={row['outward_flux']}")
    print(f"tendency={row['matrix_tendency']}")
    print(f"matrix_target={row['target_matrix_first']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
