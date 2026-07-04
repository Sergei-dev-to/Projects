#!/usr/bin/env python3
"""Repeated-record participation for a matrix detachment kernel.

The single-step matrix radial frontend often has low accessible-record
participation.  This script asks whether accessible record sequences become
high-participation after repeated emissions and internal re-scrambling.

For a one-step transition matrix D with row labels m, define record Kraus
operators K_m by keeping only rows with label m.  When dim(P)=dim(Q), iterate

    K_{m_k...m_1} = K_{m_k} U ... K_{m_2} U K_{m_1},

where U is either identity or a fixed random unitary.  The diagnostic is the
Gram participation of the sequence operators under the Hilbert-Schmidt inner
product.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import pathlib

import numpy as np
from numpy.typing import NDArray

from matrix_radial_detachment_diagnostics import Params as RadialParams, build_transition
from sector_detachment_diagnostics import DATADIR, participation


def random_unitary(dim: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = phases / np.maximum(np.abs(phases), 1e-300)
    return q * phases.conj()[None, :]


def record_kraus(
    d: NDArray[np.complex128],
    labels: NDArray[np.int64],
) -> tuple[list[int], list[NDArray[np.complex128]]]:
    record_labels = [int(label) for label in np.unique(labels)]
    kraus = []
    for label in record_labels:
        mask = labels == label
        k = np.zeros_like(d)
        k[mask, :] = d[mask, :]
        kraus.append(k)
    return record_labels, kraus


def normalize_kraus(kraus: list[NDArray[np.complex128]]) -> list[NDArray[np.complex128]]:
    total = sum(k.conj().T @ k for k in kraus)
    scale = float(np.trace(total).real)
    if scale <= 0.0:
        return kraus
    dim = kraus[0].shape[1]
    return [k * np.sqrt(dim / scale) for k in kraus]


def sequence_operators(
    kraus: list[NDArray[np.complex128]],
    depth: int,
    u: NDArray[np.complex128],
) -> list[NDArray[np.complex128]]:
    if depth < 1:
        raise ValueError("depth must be >= 1")
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
        "sequence_gram_participation": participation(eig),
        "sequence_gram_participation_norm": participation(eig) / max(len(ops), 1),
        "sequence_width_participation": participation(widths),
        "sequence_width_participation_norm": participation(widths) / max(len(ops), 1),
        "largest_sequence_width_fraction": float(np.max(widths) / max(np.sum(widths), 1e-300)),
        "operator_rank_bound": min(flat.shape),
    }


def run_depths(args: argparse.Namespace) -> list[dict[str, float | int | str]]:
    params = RadialParams(
        cutoff=args.cutoff,
        mu=args.mu,
        g=args.g,
        p_fraction=args.fraction,
        q_fraction=args.fraction,
        record_bins=args.record_bins,
        spectral_bins=args.spectral_bins,
        time_points=args.time_points,
        t_max=args.t_max,
    )
    d, _e_p, _e_q, labels, meta = build_transition(params)
    if d.shape[0] != d.shape[1]:
        raise ValueError(f"iteration requires square D, got {d.shape}")
    record_labels, kraus = record_kraus(d, labels)
    if args.normalize:
        kraus = normalize_kraus(kraus)
    if args.scrambling == "identity":
        u = np.eye(d.shape[0], dtype=np.complex128)
    elif args.scrambling == "random":
        u = random_unitary(d.shape[0], args.seed)
    else:
        raise ValueError(f"unknown scrambling: {args.scrambling}")

    rows: list[dict[str, float | int | str]] = []
    for depth in range(1, args.max_depth + 1):
        ops = sequence_operators(kraus, depth, u)
        row = {
            "cutoff": args.cutoff,
            "g": args.g,
            "fraction": args.fraction,
            "record_bins": args.record_bins,
            "scrambling": args.scrambling,
            "depth": depth,
            "dim": d.shape[0],
            "record_label_count": len(record_labels),
            "single_step_gamma": float(np.sum(np.abs(d) ** 2)),
            **{f"meta_{key}": value for key, value in meta.items()},
            **sequence_metrics(ops),
        }
        rows.append(row)
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
    parser.add_argument("--cutoff", type=int, default=5)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=1.0)
    parser.add_argument("--fraction", type=float, default=0.30)
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--scrambling", choices=["identity", "random"], default="random")
    parser.add_argument("--seed", type=int, default=8642)
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=300)
    parser.add_argument("--t-max", type=float, default=60.0)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "repeated_record_participation.csv",
    )
    args = parser.parse_args()

    rows = run_depths(args)
    write_csv(args.output_csv, rows)
    print(f"[repeated-record] wrote {args.output_csv}")
    print("depth scrambling seqs gram_norm width_norm largest")
    for row in rows:
        print(
            f"{int(row['depth']):5d} {str(row['scrambling']):10s} "
            f"{int(row['n_sequences']):4d} "
            f"{float(row['sequence_gram_participation_norm']):9.3f} "
            f"{float(row['sequence_width_participation_norm']):10.3f} "
            f"{float(row['largest_sequence_width_fraction']):7.4f}"
        )


if __name__ == "__main__":
    main()
