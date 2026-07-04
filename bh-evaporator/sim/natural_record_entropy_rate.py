#!/usr/bin/env python3
"""Entropy-rate test using the matrix proxy's own record bins.

The record-map scan inserted an explicit source-to-record matrix C_{m a}.  This
script removes that ingredient.  It starts from the source-resolved matrix
amplitudes D_a(q, alpha), adds optional daughter memory chi_a, and uses the
existing Q-sector record label of q as the accessible radiation record.

Thus the record balance is whatever the regulated matrix radial proxy gives,
not a hand-designed source-to-record map.
"""
from __future__ import annotations

import argparse
import csv
import math
import pathlib

import numpy as np
from numpy.typing import NDArray

from daughter_memory_participation import daughter_lift, memory_vectors
from matrix_source_participation import Params as SourceParams, build_source_transitions
from recycled_record_map_dynamics import random_isometry, random_unitary, sequence_metrics, sequence_operators
from sector_detachment_diagnostics import DATADIR


def build_natural_record_kraus(args: argparse.Namespace) -> list[NDArray[np.complex128]]:
    params = SourceParams(
        cutoff=args.cutoff,
        mu=args.mu,
        g=args.g,
        p_fraction=args.fraction,
        q_fraction=args.fraction,
        record_bins=args.record_bins,
        source_set=args.source_set,
        spectral_bins=16,
        time_points=100,
        t_max=20.0,
    )
    _names, source_d, _e_p, _e_q_tiled, labels_tiled, meta = build_source_transitions(params)
    n_sources = int(meta["n_sources"])
    dim_q = int(meta["dim_q"])
    q_labels = labels_tiled[:dim_q]
    memory = memory_vectors(n_sources, args.rho)
    d = daughter_lift(source_d, n_sources, dim_q, memory)
    in_dim = d.shape[1]
    recycler = random_isometry(d.shape[0], in_dim, args.seed + 10_000)

    kraus = []
    n_memory = memory.shape[1]
    lifted_labels = np.tile(q_labels, n_memory)
    for m in range(args.record_bins):
        mask_diag = (lifted_labels == m).astype(np.complex128)
        mask = np.diag(mask_diag)
        kraus.append(recycler @ mask @ d)
    if args.normalize:
        total = sum(k.conj().T @ k for k in kraus)
        scale = float(np.trace(total).real)
        if scale > 0.0:
            kraus = [k * np.sqrt(in_dim / scale) for k in kraus]
    return kraus


def run_case(args: argparse.Namespace) -> list[dict[str, float | int | str]]:
    kraus = build_natural_record_kraus(args)
    dim = kraus[0].shape[0]
    if args.scrambling == "identity":
        u = np.eye(dim, dtype=np.complex128)
    else:
        u = random_unitary(dim, args.seed + 20_000)
    log_records = math.log(args.record_bins)
    rows = []
    for depth in range(1, args.max_depth + 1):
        if args.sample_gram and depth >= args.sample_min_depth:
            metrics = sampled_sequence_metrics(kraus, depth, u, args.gram_samples, args.seed + depth)
        elif args.width_only:
            metrics = width_only_sequence_metrics(kraus, depth, u)
        else:
            ops = sequence_operators(kraus, depth, u)
            metrics = sequence_metrics(ops)
        gram_part = max(float(metrics.get("sequence_gram_participation", 1.0)), 1e-300)
        width_part = max(float(metrics["sequence_width_participation"]), 1e-300)
        h_gram = math.log(gram_part) / depth
        h_width = math.log(width_part) / depth
        rows.append(
            {
                "depth": depth,
                "record_map": "natural_q_bins",
                "record_bins": args.record_bins,
                "rho": args.rho,
                "scrambling": args.scrambling,
                "cutoff": args.cutoff,
                "g": args.g,
                "fraction": args.fraction,
                "source_set": args.source_set,
                **metrics,
                "h_gram": h_gram,
                "h_width": h_width,
                "h_gram_fraction": h_gram / log_records if log_records > 0 else 0.0,
                "h_width_fraction": h_width / log_records if log_records > 0 else 0.0,
            }
        )
    return rows


def participation(values: NDArray[np.float64]) -> float:
    vals = np.maximum(np.asarray(values, dtype=np.float64), 0.0)
    total = float(np.sum(vals))
    if total <= 0.0:
        return 0.0
    return total * total / float(np.sum(vals * vals))


def width_only_sequence_metrics(
    kraus: list[NDArray[np.complex128]],
    depth: int,
    u: NDArray[np.complex128],
) -> dict[str, float | int]:
    width_array = collect_sequence_widths(kraus, depth, u)
    width_part = participation(width_array)
    return {
        "n_sequences": int(width_array.size),
        "total_sequence_width": float(np.sum(width_array)),
        "sequence_gram_participation": 1.0,
        "sequence_gram_participation_norm": 1.0 / max(int(width_array.size), 1),
        "sequence_width_participation": width_part,
        "sequence_width_participation_norm": width_part / max(int(width_array.size), 1),
        "largest_sequence_width_fraction": float(
            np.max(width_array) / max(np.sum(width_array), 1e-300)
        ),
    }


def collect_sequence_widths(
    kraus: list[NDArray[np.complex128]],
    depth: int,
    u: NDArray[np.complex128],
) -> NDArray[np.float64]:
    widths: list[float] = []

    def visit(level: int, op: NDArray[np.complex128]) -> None:
        if level == depth:
            widths.append(float(np.sum(np.abs(op) ** 2)))
            return
        evolved = u @ op
        for k in kraus:
            visit(level + 1, k @ evolved)

    for k in kraus:
        visit(1, k.copy())
    return np.asarray(widths, dtype=np.float64)


def sequence_from_index(index: int, depth: int, base: int) -> list[int]:
    seq = []
    for _ in range(depth):
        seq.append(index % base)
        index //= base
    return seq


def sequence_operator_from_labels(
    kraus: list[NDArray[np.complex128]],
    labels: list[int],
    u: NDArray[np.complex128],
) -> NDArray[np.complex128]:
    op = kraus[labels[0]].copy()
    for label in labels[1:]:
        op = kraus[label] @ (u @ op)
    return op


def sampled_sequence_metrics(
    kraus: list[NDArray[np.complex128]],
    depth: int,
    u: NDArray[np.complex128],
    n_samples: int,
    seed: int,
) -> dict[str, float | int]:
    width_array = collect_sequence_widths(kraus, depth, u)
    width_part = participation(width_array)
    n_sequences = int(width_array.size)
    total_width = float(np.sum(width_array))
    width_metrics = {
        "n_sequences": n_sequences,
        "total_sequence_width": total_width,
        "sequence_width_participation": width_part,
        "sequence_width_participation_norm": width_part / max(n_sequences, 1),
        "largest_sequence_width_fraction": float(
            np.max(width_array) / max(total_width, 1e-300)
        ),
    }
    probs = width_array / max(total_width, 1e-300)
    cdf = np.cumsum(probs)
    rng = np.random.default_rng(seed)
    purity_sum = 0.0
    for _ in range(n_samples):
        i = int(np.searchsorted(cdf, rng.random(), side="right"))
        j = int(np.searchsorted(cdf, rng.random(), side="right"))
        i = min(i, n_sequences - 1)
        j = min(j, n_sequences - 1)
        op_i = sequence_operator_from_labels(kraus, sequence_from_index(i, depth, len(kraus)), u)
        op_j = sequence_operator_from_labels(kraus, sequence_from_index(j, depth, len(kraus)), u)
        overlap = np.vdot(op_j, op_i)
        denom = max(width_array[i] * width_array[j], 1e-300)
        purity_sum += float(np.abs(overlap) ** 2) / denom
    purity_est = purity_sum / max(n_samples, 1)
    gram_part_est = min(1.0 / max(purity_est, 1e-300), float(n_sequences))
    return {
        **width_metrics,
        "sequence_gram_participation": gram_part_est,
        "sequence_gram_participation_norm": gram_part_est / max(n_sequences, 1),
        "gram_samples": n_samples,
    }


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=4)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=2.0)
    parser.add_argument("--fraction", type=float, default=0.40)
    parser.add_argument("--source-set", choices=["quadratic", "h_terms"], default="h_terms")
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument("--rhos", default="0,1")
    parser.add_argument("--scramblings", default="identity,random")
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--width-only", action="store_true")
    parser.add_argument("--sample-gram", action="store_true")
    parser.add_argument("--sample-min-depth", type=int, default=4)
    parser.add_argument("--gram-samples", type=int, default=2000)
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--seed", type=int, default=13579)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "natural_record_entropy_rate.csv",
    )
    args = parser.parse_args()

    rows = []
    for rho in parse_list(args.rhos, float):
        for scrambling in parse_list(args.scramblings, str):
            case_args = argparse.Namespace(**vars(args))
            case_args.rho = rho
            case_args.scrambling = scrambling
            rows.extend(run_case(case_args))
    write_csv(args.output_csv, rows)
    print(f"[natural-record-rate] wrote {args.output_csv}")
    print("rho scr depth gram_part width_part hG/logM hW/logM largest")
    for row in [r for r in rows if int(r["depth"]) == args.max_depth]:
        print(
            f"{float(row['rho']):3.1f} {str(row['scrambling']):8s} "
            f"{int(row['depth']):5d} "
            f"{float(row['sequence_gram_participation']):9.2f} "
            f"{float(row['sequence_width_participation']):10.2f} "
            f"{float(row['h_gram_fraction']):8.3f} "
            f"{float(row['h_width_fraction']):8.3f} "
            f"{float(row['largest_sequence_width_fraction']):7.4f}"
        )


if __name__ == "__main__":
    main()
