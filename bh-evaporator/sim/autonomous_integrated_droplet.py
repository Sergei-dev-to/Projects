#!/usr/bin/env python3
"""Autonomous integrated droplet evaporator.

This builds a single time-independent Hamiltonian on a staged droplet/radiation
Hilbert space.  The stages are different factorizations of the same original
droplet information:

  stage 0: H_4
  stage 1: H_3 tensor R_4
  stage 2: H_2 tensor R_4 tensor R_3
  stage 3: H_1 tensor R_4 tensor R_3 tensor R_2

The Hamiltonian contains:

  * boundary-tension energy by stage;
  * intra-core scrambling inside each stage;
  * erosion couplings stage k -> k+1;
  * hard-chain hopping so emitted energy propagates away.

This is small enough for L0=3, q=2, a few hard excitations, and a short
chain.
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

from scan_bose_hubbard_dos import DATADIR


@dataclass(frozen=True)
class Stage:
    k: int
    L: int
    core_dim: int
    rad_dim: int
    droplet_dim: int
    energy: float


@dataclass(frozen=True)
class BasisState:
    stage: int
    droplet_index: int
    chain_mask: int


def random_symmetric(rng: np.random.Generator, dim: int) -> NDArray[np.float64]:
    raw = rng.normal(size=(dim, dim))
    mat = (raw + raw.T) / 2.0
    return mat / np.sqrt(float(dim))


def sparse_core_couplings(
    rng: np.random.Generator, dim: int, degree: int, strength: float
) -> list[tuple[int, int, float]]:
    couplings: dict[tuple[int, int], float] = {}
    if dim <= 1 or degree <= 0 or strength <= 0.0:
        return []
    for src in range(dim):
        targets = rng.choice(dim - 1, size=min(degree, dim - 1), replace=False)
        for target_raw in targets:
            dst = int(target_raw)
            if dst >= src:
                dst += 1
            a, b = sorted((src, dst))
            key = (a, b)
            if key not in couplings:
                couplings[key] = strength * rng.normal() / np.sqrt(float(degree))
    return [(a, b, value) for (a, b), value in couplings.items()]


def build_stages(L0: int, Lmin: int, q: int, sigma: float) -> list[Stage]:
    stages = []
    total_dim = q ** (L0 * L0)
    for k, L in enumerate(range(L0, Lmin, -1)):
        core_dim = q ** (L * L)
        rad_dim = total_dim // core_dim
        stages.append(
            Stage(
                k=k,
                L=L,
                core_dim=core_dim,
                rad_dim=rad_dim,
                droplet_dim=total_dim,
                energy=4.0 * sigma * L,
            )
        )
    # Include final stage after removing Lmin+1 shell.
    final_L = Lmin
    final_core = q ** (final_L * final_L)
    stages.append(
        Stage(
            k=len(stages),
            L=final_L,
            core_dim=final_core,
            rad_dim=total_dim // final_core,
            droplet_dim=total_dim,
            energy=4.0 * sigma * final_L,
        )
    )
    return stages


def popcount(value: int) -> int:
    return int(value.bit_count())


def chain_masks(chain_length: int, max_quanta: int) -> list[int]:
    masks = []
    for mask in range(1 << chain_length):
        if popcount(mask) <= max_quanta:
            masks.append(mask)
    return masks


def site_occupied(mask: int, site: int) -> bool:
    return bool(mask & (1 << site))


def move_particle(mask: int, src: int, dst: int) -> int:
    return (mask & ~(1 << src)) | (1 << dst)


def add_particle(mask: int, site: int) -> int:
    return mask | (1 << site)


def build_basis(
    stages: list[Stage], chain_length: int, max_quanta: int
) -> tuple[list[BasisState], dict[BasisState, int], list[int]]:
    masks = chain_masks(chain_length, max_quanta)
    basis = [
        BasisState(stage=stage.k, droplet_index=i, chain_mask=mask)
        for stage in stages
        for i in range(stage.droplet_dim)
        for mask in masks
    ]
    return basis, {state: idx for idx, state in enumerate(basis)}, masks


def chain_energy(mask: int, hard_energy: float) -> float:
    return popcount(mask) * hard_energy


def core_index(stage: Stage, droplet_index: int) -> int:
    return droplet_index // stage.rad_dim


def same_radiation_prefix(prev: Stage, nxt: Stage, i: int, j: int) -> bool:
    # Moving from prev to nxt refactors the same total droplet index. The new
    # radiation prefix should contain the old radiation labels. In this staged
    # basis that is true when the coarse old radiation index agrees.
    if prev.rad_dim == 1:
        return True
    return (i % prev.rad_dim) == (j % prev.rad_dim)


def build_hamiltonian(
    args: argparse.Namespace, stages: list[Stage], basis, index, masks: list[int]
) -> sp.csr_matrix:
    rng = np.random.default_rng(args.seed)
    rows: list[int] = []
    cols: list[int] = []
    data: list[complex] = []
    # Diagonal stage energy plus hard-chain excitation energy.  With the
    # default hard energy, L -> L-1 erosion is resonant with one emitted hard
    # quantum because E_L - E_{L-1} = 4 sigma.
    for idx, state in enumerate(basis):
        stage = stages[state.stage]
        energy = stage.energy + chain_energy(state.chain_mask, args.hard_energy)
        rows.append(idx)
        cols.append(idx)
        data.append(energy)

    # Chain hopping for hard excitations.
    for state in basis:
        i = index[state]
        for site in range(args.chain_length):
            if not site_occupied(state.chain_mask, site):
                continue
            for delta in (-1, 1):
                new_site = site + delta
                if not (0 <= new_site < args.chain_length):
                    continue
                if site_occupied(state.chain_mask, new_site):
                    continue
                target_mask = move_particle(state.chain_mask, site, new_site)
                target = BasisState(state.stage, state.droplet_index, target_mask)
                j = index.get(target)
                if j is None:
                    continue
                rows.append(j)
                cols.append(i)
                data.append(-args.chain_hop)

    # Intra-core scrambling within each stage and fixed radiation/chain label.
    for stage in stages:
        if args.scramble_mode == "none" or args.scramble_strength <= 0.0 or stage.core_dim <= 1:
            continue
        core_rng = np.random.default_rng(args.seed + 1000 + stage.k)
        if args.scramble_mode == "dense":
            k_core = args.scramble_strength * random_symmetric(core_rng, stage.core_dim)
            core_terms = [
                (a, b, float(k_core[b, a]))
                for a in range(stage.core_dim)
                for b in range(stage.core_dim)
                if a != b and abs(k_core[b, a]) > args.matrix_cutoff
            ]
        elif args.scramble_mode == "sparse":
            undirected = sparse_core_couplings(
                core_rng, stage.core_dim, args.scramble_degree, args.scramble_strength
            )
            core_terms = []
            for a, b, value in undirected:
                if abs(value) <= args.matrix_cutoff:
                    continue
                core_terms.append((a, b, value))
                core_terms.append((b, a, value))
        else:
            raise ValueError(f"unknown scramble mode: {args.scramble_mode}")
        for rad_label in range(stage.rad_dim):
            for chain_mask in masks:
                for a, b, val in core_terms:
                    source_idx = a * stage.rad_dim + rad_label
                    target_idx = b * stage.rad_dim + rad_label
                    source = BasisState(stage.k, source_idx, chain_mask)
                    target = BasisState(stage.k, target_idx, chain_mask)
                    rows.append(index[target])
                    cols.append(index[source])
                    data.append(val)

    # Erosion coupling.  It conserves the existing radiation prefix and emits a
    # hard excitation at chain site 0 when that site is empty.
    for prev, nxt in zip(stages[:-1], stages[1:]):
        shell_dim = nxt.rad_dim // prev.rad_dim
        if shell_dim <= 1:
            continue
        rng_block = np.random.default_rng(args.seed + 5000 + prev.k)
        # A rectangular random isometry-like coupling from old core states to
        # new core x new shell states, normalized by shell dimension.
        for old_core in range(prev.core_dim):
            source_base = old_core * prev.rad_dim
            for rad_label in range(prev.rad_dim):
                source_idx = source_base + rad_label
                for source_mask in masks:
                    if site_occupied(source_mask, 0):
                        continue
                    target_mask = add_particle(source_mask, 0)
                    if popcount(target_mask) > args.max_quanta:
                        continue
                    source = BasisState(prev.k, source_idx, source_mask)
                    col = index[source]
                    for new_core in range(nxt.core_dim):
                        for shell_label in range(shell_dim):
                            new_rad_label = shell_label * prev.rad_dim + rad_label
                            target_idx = new_core * nxt.rad_dim + new_rad_label
                            target = BasisState(nxt.k, target_idx, target_mask)
                            amp = rng_block.normal() / np.sqrt(float(nxt.core_dim * shell_dim))
                            val = args.erosion_coupling * amp
                            if abs(val) <= args.matrix_cutoff:
                                continue
                            row = index[target]
                            rows.append(row)
                            cols.append(col)
                            data.append(val)
                            rows.append(col)
                            cols.append(row)
                            data.append(val)

    # A weak outward bias at the far end suppresses immediate finite-chain
    # recurrence without affecting exact Hamiltonian conservation too much on
    # the simulated time window.  It is implemented as a longer hard chain by
    # default; this term is left at zero unless explicitly requested.
    if args.far_sink_strength > 0.0:
        far = args.chain_length - 1
        for state in basis:
            if not site_occupied(state.chain_mask, far):
                continue
            for empty_site in range(args.chain_length):
                if site_occupied(state.chain_mask, empty_site):
                    continue
                target_mask = move_particle(state.chain_mask, far, empty_site)
                target = BasisState(state.stage, state.droplet_index, target_mask)
                row = index.get(target)
                if row is None:
                            continue
                col = index[state]
                val = args.far_sink_strength / np.sqrt(float(args.chain_length))
                rows.append(row)
                cols.append(col)
                data.append(val)
                rows.append(col)
                cols.append(row)
                data.append(val)

    return sp.coo_matrix((data, (rows, cols)), shape=(len(basis), len(basis))).tocsr()


def initial_state(stages: list[Stage], basis, args: argparse.Namespace) -> NDArray[np.complex128]:
    rng = np.random.default_rng(args.seed + 10_000)
    psi = np.zeros(len(basis), dtype=np.complex128)
    top = stages[0]
    vacuum_mask = 0
    if args.initial_state == "basis":
        psi[index_of(basis, BasisState(0, 0, vacuum_mask))] = 1.0
    elif args.initial_state == "haar":
        raw = rng.normal(size=top.core_dim) + 1j * rng.normal(size=top.core_dim)
        raw /= np.sqrt(float(np.vdot(raw, raw).real))
        for i, amp in enumerate(raw):
            psi[index_of(basis, BasisState(0, i, vacuum_mask))] = amp
    elif args.initial_state == "flat":
        amp = 1.0 / np.sqrt(float(top.core_dim))
        for i in range(top.core_dim):
            psi[index_of(basis, BasisState(0, i, vacuum_mask))] = amp
    else:
        raise ValueError(f"unknown initial state: {args.initial_state}")
    return psi


def index_of(basis: list[BasisState], state: BasisState) -> int:
    # Used only during initial-state construction.
    return basis.index(state)


def observables(psi: NDArray[np.complex128], hmat, stages: list[Stage], basis, args: argparse.Namespace):
    probs = np.abs(psi) ** 2
    stage_probs = np.zeros(len(stages), dtype=float)
    chain_probs = np.zeros(args.chain_length, dtype=float)
    mean_L = 0.0
    mean_quanta = 0.0
    rad_shell_entropy_proxy = 0.0
    for p, state in zip(probs, basis):
        stage = stages[state.stage]
        stage_probs[state.stage] += p
        mean_quanta += p * popcount(state.chain_mask)
        for site in range(args.chain_length):
            if site_occupied(state.chain_mask, site):
                chain_probs[site] += p
        mean_L += p * stage.L
        rad_shell_entropy_proxy += p * np.log(max(stage.rad_dim, 1))
    h_expect = complex(np.vdot(psi, hmat @ psi))
    return {
        "mean_L": float(mean_L),
        "mean_quanta": float(mean_quanta),
        "p_initial_stage": float(stage_probs[0]),
        "p_final_stage": float(stage_probs[-1]),
        "chain_near": float(chain_probs[0]),
        "chain_far": float(np.sum(chain_probs[max(1, args.chain_length // 2) :])),
        "hard_energy": float(mean_quanta * args.hard_energy),
        "shell_entropy_proxy": float(rad_shell_entropy_proxy),
        "hamiltonian_energy": float(h_expect.real),
        "hamiltonian_energy_imag": float(h_expect.imag),
        **{f"p_stage_{idx}": float(value) for idx, value in enumerate(stage_probs)},
        **{f"p_chain_{idx}": float(value) for idx, value in enumerate(chain_probs)},
    }


def summarize(rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str]:
    h_vals = [float(row["hamiltonian_energy"]) for row in rows]
    hard = np.asarray([float(row["hard_energy"]) for row in rows], dtype=float)
    near = np.asarray([float(row["chain_near"]) for row in rows], dtype=float)
    far = np.asarray([float(row["chain_far"]) for row in rows], dtype=float)
    final = rows[-1]
    return {
        "initial_state": rows[0]["initial_state"],
        "basis_dim": rows[0]["basis_dim"],
        "final_mean_L": final["mean_L"],
        "final_p_initial_stage": final["p_initial_stage"],
        "final_p_final_stage": final["p_final_stage"],
        "final_mean_quanta": final["mean_quanta"],
        "final_hard_energy": final["hard_energy"],
        "max_hard_energy": float(np.max(hard)),
        "final_chain_near": final["chain_near"],
        "max_chain_near": float(np.max(near)),
        "final_chain_far": final["chain_far"],
        "max_chain_far": float(np.max(far)),
        "final_shell_entropy_proxy": final["shell_entropy_proxy"],
        "hamiltonian_energy_drift": max(h_vals) - min(h_vals),
    }


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def run(args: argparse.Namespace):
    stages = build_stages(args.L0, args.Lmin, args.q, args.sigma)
    basis, basis_index, masks = build_basis(stages, args.chain_length, args.max_quanta)
    # Bind for initial_state without carrying the index through its old helper.
    global index_of

    def index_of_local(_basis, state):
        return basis_index[state]

    index_of = index_of_local  # type: ignore[assignment]
    hmat = build_hamiltonian(args, stages, basis, basis_index, masks)
    psi0 = initial_state(stages, basis, args)
    times = np.linspace(0.0, args.t_max, args.time_points)
    rows = []
    for time, psi in zip(
        times,
        spla.expm_multiply((-1j) * hmat, psi0, start=0.0, stop=args.t_max, num=args.time_points),
    ):
        rows.append(
            {
                "time": float(time),
                "initial_state": args.initial_state,
                "basis_dim": len(basis),
                **observables(psi, hmat, stages, basis, args),
            }
        )
    return rows, summarize(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run autonomous integrated droplet.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--L0", type=int, default=3)
    parser.add_argument("--Lmin", type=int, default=1)
    parser.add_argument("--chain-length", type=int, default=8)
    parser.add_argument("--max-quanta", type=int, default=None)
    parser.add_argument("--hard-energy", type=float, default=None)
    parser.add_argument("--chain-hop", type=float, default=0.8)
    parser.add_argument("--scramble-mode", choices=["none", "sparse", "dense"], default="sparse")
    parser.add_argument("--scramble-strength", type=float, default=0.25)
    parser.add_argument("--scramble-degree", type=int, default=4)
    parser.add_argument("--erosion-coupling", type=float, default=0.08)
    parser.add_argument("--far-sink-strength", type=float, default=0.0)
    parser.add_argument("--matrix-cutoff", type=float, default=1e-12)
    parser.add_argument("--initial-state", choices=["basis", "flat", "haar"], default="haar")
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument("--t-max", type=float, default=120.0)
    parser.add_argument("--time-points", type=int, default=121)
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "autonomous_integrated_droplet_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "autonomous_integrated_droplet_summary.csv",
    )
    args = parser.parse_args(argv)
    if args.max_quanta is None:
        args.max_quanta = args.L0 - args.Lmin
    if args.hard_energy is None:
        args.hard_energy = 4.0 * args.sigma

    rows, summary = run(args)
    write_csv(args.timeseries_csv, rows)
    write_csv(args.summary_csv, [summary])
    print(f"[auto-droplet] wrote {args.timeseries_csv}")
    print(f"[auto-droplet] wrote {args.summary_csv}")
    print(
        "dim={basis_dim} final_L={final_mean_L:.3f} p_final={final_p_final_stage:.3f} "
        "Ehard={final_hard_energy:.3f} far={final_chain_far:.3f} "
        "H_drift={hamiltonian_energy_drift:.2e}".format(**summary)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
