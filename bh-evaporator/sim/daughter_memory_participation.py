#!/usr/bin/env python3
"""Daughter-memory lift of source-resolved matrix detachment amplitudes.

The source/tether test showed that source operators can have participation,
while collective summation can erase it.  This script inserts a controlled
daughter memory between those extremes.

Starting from source blocks

    D_a = <q| Q O_a P |alpha>,

we assign each source a daughter-memory vector |chi_a>.  The emitted channel
with accessible daughter memory has amplitudes

    D_(ell,q),alpha = sum_a <ell|chi_a> D_a(q,alpha).

The memory overlap matrix is

    <chi_b|chi_a> = (1-rho) delta_ab + rho,

so rho=0 gives orthogonal daughter memories and rho=1 gives identical memory,
equivalent to full collective source erasure.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from matrix_source_participation import Params as SourceParams, build_source_transitions
from sector_detachment_diagnostics import DATADIR, diagnostics


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def memory_vectors(n_sources: int, rho: float) -> NDArray[np.complex128]:
    if not (0.0 <= rho <= 1.0):
        raise ValueError("rho must lie in [0,1]")
    gram = (1.0 - rho) * np.eye(n_sources) + rho * np.ones((n_sources, n_sources))
    eigvals, eigvecs = np.linalg.eigh(gram)
    eigvals = np.maximum(eigvals, 0.0)
    # Rows are source labels a, columns are orthonormal memory basis ell.
    return (eigvecs @ np.diag(np.sqrt(eigvals))).astype(np.complex128)


def daughter_lift(
    source_d: NDArray[np.complex128],
    n_sources: int,
    dim_q: int,
    memory: NDArray[np.complex128],
) -> NDArray[np.complex128]:
    blocks = source_d.reshape(n_sources, dim_q, source_d.shape[1])
    n_mem = memory.shape[1]
    lifted = np.zeros((n_mem, dim_q, source_d.shape[1]), dtype=np.complex128)
    for a in range(n_sources):
        lifted += memory[a, :, None, None] * blocks[a][None, :, :]
    return lifted.reshape(n_mem * dim_q, source_d.shape[1])


def daughter_labels(labels: NDArray[np.int64], n_memory: int) -> NDArray[np.int64]:
    return np.tile(labels, n_memory)


def run_row(args: argparse.Namespace, rho: float) -> dict[str, float | int | str]:
    params = SourceParams(
        cutoff=args.cutoff,
        mu=args.mu,
        g=args.g,
        p_fraction=args.fraction,
        q_fraction=args.fraction,
        record_bins=args.record_bins,
        source_set=args.source_set,
        spectral_bins=args.spectral_bins,
        time_points=args.time_points,
        t_max=args.t_max,
    )
    names, source_d, e_p, e_q_tiled, labels_tiled, meta = build_source_transitions(params)
    n_sources = int(meta["n_sources"])
    dim_q = int(meta["dim_q"])
    # The source transition repeats Q energies/labels once per source.
    e_q = e_q_tiled[:dim_q]
    labels = labels_tiled[:dim_q]
    mem = memory_vectors(n_sources, rho)
    d = daughter_lift(source_d, n_sources, dim_q, mem)
    lifted_labels = daughter_labels(labels, mem.shape[1])
    diag = diagnostics(params, d, e_p, np.tile(e_q, mem.shape[1]), lifted_labels)
    return {
        "rho": rho,
        "n_memory": int(mem.shape[1]),
        "n_sources": n_sources,
        "source_set": args.source_set,
        "cutoff": args.cutoff,
        "g": args.g,
        "fraction": args.fraction,
        "record_bins": args.record_bins,
        "source_names": ",".join(names),
        **meta,
        **diag,
    }


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
    parser.add_argument("--g", type=float, default=1.0)
    parser.add_argument("--fraction", type=float, default=0.35)
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument(
        "--source-set",
        choices=["linear", "quadratic", "linear_quadratic", "commutator", "h_terms"],
        default="quadratic",
    )
    parser.add_argument("--rhos", default="0,0.1,0.25,0.5,0.75,0.9,1")
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=300)
    parser.add_argument("--t-max", type=float, default=60.0)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "daughter_memory_participation.csv",
    )
    args = parser.parse_args()

    rows = [run_row(args, rho) for rho in parse_list(args.rhos, float)]
    write_csv(args.output_csv, rows)
    print(f"[daughter-memory] wrote {args.output_csv}")
    print("rho fullGram absFull recordGram widthPart largest gamma")
    for row in rows:
        print(
            f"{float(row['rho']):4.2f} "
            f"{float(row['channel_gram_participation_norm']):8.3f} "
            f"{float(row['channel_gram_participation']):7.2f} "
            f"{float(row['accessible_record_gram_participation_norm']):10.3f} "
            f"{float(row['accessible_record_width_participation_norm']):9.3f} "
            f"{float(row['largest_channel_width_fraction']):7.3f} "
            f"{float(row['gamma_total']):9.3g}"
        )


if __name__ == "__main__":
    main()
