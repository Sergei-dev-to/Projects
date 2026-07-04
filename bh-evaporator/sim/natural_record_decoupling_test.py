#!/usr/bin/env python3
r"""Direct decoupling validation for natural record histories.

Given natural-record Kraus operators K_m, form record-history Kraus operators
and test whether the complementary system B decouples from a small diary
reference.  This is Test 5 for the proxy diagnostics.

The record-history channel is normalized to a trace-preserving channel on the
input shell by whitening T = sum_s K_s^\dagger K_s.  The total one-step width
is therefore not tested here; it remains a separate gate.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from natural_record_entropy_rate import build_natural_record_kraus
from recycled_record_map_dynamics import sequence_operators
from sector_detachment_diagnostics import DATADIR


def random_unitary(dim: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r)
    phases = phases / np.maximum(np.abs(phases), 1e-300)
    return q * phases.conj()[None, :]


def random_code(input_dim: int, code_dim: int, seed: int) -> NDArray[np.complex128]:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(input_dim, code_dim)) + 1j * rng.normal(size=(input_dim, code_dim))
    q, _r = np.linalg.qr(raw)
    return q[:, :code_dim]


def whiten_kraus(
    kraus: list[NDArray[np.complex128]],
    cutoff: float = 1e-12,
) -> tuple[list[NDArray[np.complex128]], int]:
    total = sum(k.conj().T @ k for k in kraus)
    eig, vec = np.linalg.eigh(0.5 * (total + total.conj().T))
    keep = eig > cutoff * max(float(np.max(eig)), 1.0)
    support = vec[:, keep] @ np.diag(1.0 / np.sqrt(eig[keep]))
    return [k @ support for k in kraus], int(np.sum(keep))


def rb_state(kraus: list[NDArray[np.complex128]], code: NDArray[np.complex128]) -> NDArray[np.complex128]:
    code_dim = code.shape[1]
    out_dim = kraus[0].shape[0]
    rho = np.zeros((code_dim * out_dim, code_dim * out_dim), dtype=np.complex128)
    blocks = [[None for _ in range(code_dim)] for _ in range(code_dim)]
    for i in range(code_dim):
        vi = code[:, i : i + 1]
        for j in range(code_dim):
            vj = code[:, j : j + 1]
            block = sum(k @ vi @ (vj.conj().T @ k.conj().T) for k in kraus)
            blocks[i][j] = block / code_dim
    for i in range(code_dim):
        for j in range(code_dim):
            rho[i * out_dim : (i + 1) * out_dim, j * out_dim : (j + 1) * out_dim] = blocks[i][j]
    return 0.5 * (rho + rho.conj().T)


def partial_trace_reference(rho_rb: NDArray[np.complex128], code_dim: int, out_dim: int) -> NDArray[np.complex128]:
    rho_b = np.zeros((out_dim, out_dim), dtype=np.complex128)
    for i in range(code_dim):
        rho_b += rho_rb[i * out_dim : (i + 1) * out_dim, i * out_dim : (i + 1) * out_dim]
    return 0.5 * (rho_b + rho_b.conj().T)


def trace_norm(mat: NDArray[np.complex128]) -> float:
    return float(np.sum(np.linalg.svd(mat, compute_uv=False)))


def decoupling_error(kraus: list[NDArray[np.complex128]], code: NDArray[np.complex128]) -> float:
    code_dim = code.shape[1]
    out_dim = kraus[0].shape[0]
    rho_rb = rb_state(kraus, code)
    rho_b = partial_trace_reference(rho_rb, code_dim, out_dim)
    rho_r = np.eye(code_dim, dtype=np.complex128) / code_dim
    product = np.kron(rho_r, rho_b)
    return trace_norm(rho_rb - product)


def run(args: argparse.Namespace) -> list[dict[str, float | int | str]]:
    one_step = build_natural_record_kraus(args)
    dim = one_step[0].shape[0]
    if args.scrambling == "identity":
        u = np.eye(dim, dtype=np.complex128)
    else:
        u = random_unitary(dim, args.seed + 20_000)
    rows = []
    for depth in range(1, args.max_depth + 1):
        histories = sequence_operators(one_step, depth, u)
        tp_histories, support_dim = whiten_kraus(histories)
        if support_dim < args.code_dim:
            rows.append(
                {
                    "depth": depth,
                    "n_sequences": len(histories),
                    "support_dim": support_dim,
                    "decoupling_trace_norm": float("nan"),
                    "tp_trace_norm_error": float("nan"),
                    "code_dim": args.code_dim,
                    "cutoff": args.cutoff,
                    "g": args.g,
                    "fraction": args.fraction,
                    "source_set": args.source_set,
                    "record_bins": args.record_bins,
                    "rho": args.rho,
                    "scrambling": args.scrambling,
                }
            )
            continue
        code = random_code(support_dim, args.code_dim, args.seed + 30_000 + depth)
        error = decoupling_error(tp_histories, code)
        total = sum(k.conj().T @ k for k in tp_histories)
        tp_error = trace_norm(total - np.eye(support_dim, dtype=np.complex128))
        rows.append(
            {
                "depth": depth,
                "n_sequences": len(histories),
                "support_dim": support_dim,
                "decoupling_trace_norm": error,
                "tp_trace_norm_error": tp_error,
                "code_dim": args.code_dim,
                "cutoff": args.cutoff,
                "g": args.g,
                "fraction": args.fraction,
                "source_set": args.source_set,
                "record_bins": args.record_bins,
                "rho": args.rho,
                "scrambling": args.scrambling,
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
    parser.add_argument("--g", type=float, default=0.5)
    parser.add_argument("--fraction", type=float, default=0.40)
    parser.add_argument("--source-set", choices=["quadratic", "h_terms"], default="h_terms")
    parser.add_argument("--record-bins", type=int, default=6)
    parser.add_argument("--rho", type=float, default=0.0)
    parser.add_argument("--scrambling", choices=["identity", "random"], default="identity")
    parser.add_argument("--code-dim", type=int, default=2)
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--seed", type=int, default=13579)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "natural_record_decoupling_test.csv",
    )
    args = parser.parse_args()
    rows = run(args)
    write_csv(args.output_csv, rows)
    print(f"[natural-decoupling] wrote {args.output_csv}")
    print("depth seqs support decoupling_error tp_error")
    for row in rows:
        print(
            f"{int(row['depth']):5d} {int(row['n_sequences']):5d} "
            f"{int(row['support_dim']):7d} "
            f"{float(row['decoupling_trace_norm']):16.6g} "
            f"{float(row['tp_trace_norm_error']):9.3g}"
        )


if __name__ == "__main__":
    main()
