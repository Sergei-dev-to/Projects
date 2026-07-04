#!/usr/bin/env python3
"""Repeated records for source/daughter channels with recycled daughter dynamics.

The record-map test can produce a non-square transition D from an input shell
to a daughter-memory/output space.  To test temporal accumulation, this script
adds a random recycling map R from the full output space back to the next
input shell and defines square record Kraus operators

    K_m = R P_m D.

This is not a BFSS evolution.  It is a controlled test of the mechanism:
balanced record maps plus internal reprocessing should grow accessible record
sequence participation, while aligned maps should not.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from matrix_source_participation import Params as SourceParams, build_source_transitions
from daughter_memory_participation import memory_vectors
from record_map_participation import build_record_lift, record_map
from sector_detachment_diagnostics import DATADIR, participation


def random_isometry(out_dim: int, in_dim: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(out_dim, in_dim)) + 1j * rng.normal(size=(out_dim, in_dim))
    q, _r = np.linalg.qr(raw)
    return q[:, :in_dim].conj().T


def build_square_record_kraus(args: argparse.Namespace) -> list[NDArray[np.complex128]]:
    params = SourceParams(
        cutoff=args.cutoff,
        mu=args.mu,
        g=args.g,
        p_fraction=args.fraction,
        q_fraction=args.fraction,
        record_bins=args.records,
        source_set=args.source_set,
        spectral_bins=16,
        time_points=100,
        t_max=20.0,
    )
    _names, source_d, _e_p, _e_q_tiled, _labels_tiled, meta = build_source_transitions(params)
    n_sources = int(meta["n_sources"])
    dim_q = int(meta["dim_q"])
    memory = memory_vectors(n_sources, args.rho)
    c_map = record_map(args.record_map, args.records, n_sources, args.seed)
    d = build_record_lift(source_d, n_sources, dim_q, memory, c_map)
    in_dim = d.shape[1]
    recycler = random_isometry(d.shape[0], in_dim, args.seed + 10_000)
    kraus = []
    block = memory.shape[1] * dim_q
    for m in range(args.records):
        mask = np.zeros((d.shape[0], d.shape[0]), dtype=np.complex128)
        lo = m * block
        hi = (m + 1) * block
        mask[lo:hi, lo:hi] = np.eye(block, dtype=np.complex128)
        kraus.append(recycler @ mask @ d)
    if args.normalize:
        total = sum(k.conj().T @ k for k in kraus)
        scale = float(np.trace(total).real)
        if scale > 0.0:
            kraus = [k * np.sqrt(in_dim / scale) for k in kraus]
    return kraus


def random_unitary(dim: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = phases / np.maximum(np.abs(phases), 1e-300)
    return q * phases.conj()[None, :]


def sequence_operators(
    kraus: list[NDArray[np.complex128]],
    depth: int,
    u: NDArray[np.complex128],
) -> list[NDArray[np.complex128]]:
    current = [k.copy() for k in kraus]
    for _ in range(2, depth + 1):
        nxt = []
        for prev in current:
            evolved = u @ prev
            for k in kraus:
                nxt.append(k @ evolved)
        current = nxt
    return current


def sequence_metrics(ops: list[NDArray[np.complex128]]) -> dict[str, float | int]:
    flat = np.asarray([op.reshape(-1) for op in ops], dtype=np.complex128)
    gram = flat @ flat.conj().T
    eig = np.linalg.eigvalsh(0.5 * (gram + gram.conj().T)).real
    widths = np.real(np.diag(gram))
    return {
        "n_sequences": len(ops),
        "total_sequence_width": float(np.sum(widths)),
        "sequence_gram_participation": participation(eig),
        "sequence_gram_participation_norm": participation(eig) / max(len(ops), 1),
        "sequence_width_participation": participation(widths),
        "sequence_width_participation_norm": participation(widths) / max(len(ops), 1),
        "largest_sequence_width_fraction": float(np.max(widths) / max(np.sum(widths), 1e-300)),
    }


def run(args: argparse.Namespace) -> list[dict[str, float | int | str]]:
    kraus = build_square_record_kraus(args)
    dim = kraus[0].shape[0]
    if args.scrambling == "identity":
        u = np.eye(dim, dtype=np.complex128)
    else:
        u = random_unitary(dim, args.seed + 20_000)
    rows = []
    for depth in range(1, args.max_depth + 1):
        ops = sequence_operators(kraus, depth, u)
        rows.append(
            {
                "depth": depth,
                "record_map": args.record_map,
                "records": args.records,
                "rho": args.rho,
                "scrambling": args.scrambling,
                "cutoff": args.cutoff,
                "g": args.g,
                "fraction": args.fraction,
                "source_set": args.source_set,
                **sequence_metrics(ops),
            }
        )
    return rows


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
    parser.add_argument("--records", type=int, default=3)
    parser.add_argument(
        "--record-map",
        choices=["aligned", "round_robin", "random_orthogonal", "random_dense"],
        default="round_robin",
    )
    parser.add_argument("--rho", type=float, default=0.0)
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--scrambling", choices=["identity", "random"], default="random")
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--seed", type=int, default=13579)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "recycled_record_map_dynamics.csv",
    )
    args = parser.parse_args()
    rows = run(args)
    write_csv(args.output_csv, rows)
    print(f"[recycled-record-map] wrote {args.output_csv}")
    print("depth map scrambling seqs gram_norm width_norm largest")
    for row in rows:
        print(
            f"{int(row['depth']):5d} {str(row['record_map']):12s} {str(row['scrambling']):10s} "
            f"{int(row['n_sequences']):4d} "
            f"{float(row['sequence_gram_participation_norm']):9.3f} "
            f"{float(row['sequence_width_participation_norm']):10.3f} "
            f"{float(row['largest_sequence_width_fraction']):7.4f}"
        )


if __name__ == "__main__":
    main()
