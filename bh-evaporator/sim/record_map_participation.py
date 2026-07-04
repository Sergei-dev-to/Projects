#!/usr/bin/env python3
"""Accessible-record maps for source/daughter detachment amplitudes.

This script tests whether source and daughter-memory participation can be made
visible to a balanced radiation record.  Starting from source-resolved matrix
blocks D_a and daughter-memory vectors chi_a, introduce a source-to-record map
C_{m a}.  The lifted amplitudes are

    D_{m,ell,q; alpha} = sum_a C_{m a} chi_a(ell) D_a(q,alpha).

The accessible label is m.  This isolates a failure mode found in the radial
proxy: full-channel participation can coexist with highly biased record
weights.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from daughter_memory_participation import memory_vectors
from matrix_source_participation import Params as SourceParams, build_source_transitions
from sector_detachment_diagnostics import DATADIR, participation


def record_map(mode: str, n_records: int, n_sources: int, seed: int) -> NDArray[np.complex128]:
    if n_records < 1:
        raise ValueError("n_records must be positive")
    if mode == "aligned":
        c = np.zeros((n_records, n_sources), dtype=np.complex128)
        c[0, :] = 1.0 / np.sqrt(n_sources)
        return c
    if mode == "round_robin":
        c = np.zeros((n_records, n_sources), dtype=np.complex128)
        for a in range(n_sources):
            c[a % n_records, a] = 1.0
        row_norms = np.sqrt(np.sum(np.abs(c) ** 2, axis=1))
        row_norms[row_norms == 0.0] = 1.0
        return c / row_norms[:, None]
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(n_records, n_sources)) + 1j * rng.normal(size=(n_records, n_sources))
    if mode == "random_dense":
        raw /= np.sqrt(np.sum(np.abs(raw) ** 2, axis=1, keepdims=True))
        return raw
    if mode == "random_orthogonal":
        # Orthonormalize rows when possible; otherwise orthonormalize columns and
        # use the first n_records rows as the closest small test.
        q, _r = np.linalg.qr(raw.T)
        return q[:, :n_records].T
    raise ValueError(f"unknown record map mode: {mode}")


def build_record_lift(
    source_d: NDArray[np.complex128],
    n_sources: int,
    dim_q: int,
    memory: NDArray[np.complex128],
    c_map: NDArray[np.complex128],
) -> NDArray[np.complex128]:
    blocks = source_d.reshape(n_sources, dim_q, source_d.shape[1])
    n_records = c_map.shape[0]
    n_memory = memory.shape[1]
    lifted = np.zeros((n_records, n_memory, dim_q, source_d.shape[1]), dtype=np.complex128)
    for a in range(n_sources):
        lifted += c_map[:, a, None, None, None] * memory[a, None, :, None, None] * blocks[a][
            None, None, :, :
        ]
    return lifted.reshape(n_records * n_memory * dim_q, source_d.shape[1])


def fast_record_diagnostics(
    params: SourceParams,
    d: NDArray[np.complex128],
    labels: NDArray[np.int64],
) -> dict[str, float | int | str]:
    gram_i = d.conj().T @ d
    eig_i = np.linalg.eigvalsh(0.5 * (gram_i + gram_i.conj().T)).real
    record_labels = np.unique(labels)
    record_widths = np.zeros(record_labels.size, dtype=np.float64)
    record_gram = np.zeros((record_labels.size, record_labels.size), dtype=np.complex128)
    for i, li in enumerate(record_labels):
        rows_i = labels == li
        d_i = d[rows_i, :]
        record_widths[i] = float(np.sum(np.abs(d_i) ** 2))
        for j, lj in enumerate(record_labels):
            rows_j = labels == lj
            d_j = d[rows_j, :]
            record_gram[i, j] = np.vdot(d_j, d_i)
    eig_record = np.linalg.eigvalsh(0.5 * (record_gram + record_gram.conj().T)).real
    gamma = float(np.sum(np.abs(d) ** 2))
    rank_bound = min(d.shape)
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
        "gamma_total": gamma,
        "channel_gram_participation": participation(eig_i),
        "channel_gram_participation_norm": participation(eig_i) / max(rank_bound, 1),
        "initial_gram_participation": participation(eig_i),
        "initial_gram_participation_norm": participation(eig_i) / max(rank_bound, 1),
        "largest_channel_width_fraction": float(np.max(eig_i) / max(np.sum(eig_i), 1e-300)),
        "accessible_record_count": int(record_labels.size),
        "accessible_record_gram_participation": participation(eig_record),
        "accessible_record_gram_participation_norm": participation(eig_record)
        / max(record_labels.size, 1),
        "accessible_record_width_participation": participation(record_widths),
        "accessible_record_width_participation_norm": participation(record_widths)
        / max(record_labels.size, 1),
        "largest_accessible_record_width_fraction": float(
            np.max(record_widths) / max(np.sum(record_widths), 1e-300)
        ),
    }


def run_row(args: argparse.Namespace, mode: str, n_records: int, rho: float) -> dict[str, float | int | str]:
    params = SourceParams(
        cutoff=args.cutoff,
        mu=args.mu,
        g=args.g,
        p_fraction=args.fraction,
        q_fraction=args.fraction,
        record_bins=n_records,
        source_set=args.source_set,
        spectral_bins=args.spectral_bins,
        time_points=args.time_points,
        t_max=args.t_max,
    )
    names, source_d, e_p, e_q_tiled, labels_tiled, meta = build_source_transitions(params)
    n_sources = int(meta["n_sources"])
    dim_q = int(meta["dim_q"])
    e_q = e_q_tiled[:dim_q]
    memory = memory_vectors(n_sources, rho)
    c_map = record_map(mode, n_records, n_sources, args.seed)
    d = build_record_lift(source_d, n_sources, dim_q, memory, c_map)
    labels = np.repeat(np.arange(n_records, dtype=np.int64), memory.shape[1] * dim_q)
    diag = fast_record_diagnostics(params, d, labels)
    return {
        "mode": mode,
        "n_records": n_records,
        "rho": rho,
        "n_sources": n_sources,
        "n_memory": int(memory.shape[1]),
        "source_set": args.source_set,
        "cutoff": args.cutoff,
        "g": args.g,
        "fraction": args.fraction,
        "source_names": ",".join(names),
        **meta,
        **diag,
    }


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=4)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=2.0)
    parser.add_argument("--fraction", type=float, default=0.40)
    parser.add_argument("--source-set", choices=["quadratic", "h_terms"], default="h_terms")
    parser.add_argument("--modes", default="aligned,round_robin,random_orthogonal,random_dense")
    parser.add_argument("--records", default="2,3,4,6")
    parser.add_argument("--rhos", default="0,1")
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=200)
    parser.add_argument("--t-max", type=float, default=40.0)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "record_map_participation.csv",
    )
    args = parser.parse_args()

    rows = []
    for mode in parse_list(args.modes, str):
        for n_records in parse_list(args.records, int):
            for rho in parse_list(args.rhos, float):
                row = run_row(args, mode, n_records, rho)
                rows.append(row)
    write_csv(args.output_csv, rows)
    print(f"[record-map] wrote {args.output_csv}")
    print("mode records rho gamma full record width largest score")
    for row in sorted(
        rows,
        key=lambda r: float(r["accessible_record_gram_participation_norm"])
        * float(r["channel_gram_participation_norm"])
        * float(r["gamma_total"]),
        reverse=True,
    ):
        score = (
            float(row["gamma_total"])
            * float(row["channel_gram_participation_norm"])
            * float(row["accessible_record_gram_participation_norm"])
        )
        print(
            f"{str(row['mode']):17s} {int(row['n_records']):7d} {float(row['rho']):3.1f} "
            f"{float(row['gamma_total']):8.3g} "
            f"{float(row['channel_gram_participation_norm']):6.3f} "
            f"{float(row['accessible_record_gram_participation_norm']):6.3f} "
            f"{float(row['accessible_record_width_participation_norm']):6.3f} "
            f"{float(row['largest_accessible_record_width_fraction']):7.3f} "
            f"{score:8.3g}"
        )


if __name__ == "__main__":
    main()
