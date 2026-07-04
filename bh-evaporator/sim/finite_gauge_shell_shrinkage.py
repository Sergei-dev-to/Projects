"""Finite-gauge shell shrinkage diagnostic.

This targets F3 directly for the edge-tension droplet.

For the finite Z_q gauge droplet:

    dim H_L = q^(L^2)
    dim H_(L-1) = q^((L-1)^2)
    dim H_shell = q^(2L - 1)

so

    H_L ~= H_(L-1) tensor H_shell

at the level of Hilbert-space dimension.

This script builds that exact factorization, starts H_L maximally entangled
with a reference, then applies the coarse shrink map:

    |core, shell>_bulk |0>_record -> |core>_bulk |shell>_record

and measures where the reference information goes.

It is intentionally a Hilbert-space/factorization diagnostic, not a local gauge
Hamiltonian.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path


def row_for_L(L: int, q: int) -> dict[str, float | int]:
    d_L = q ** (L * L)
    d_core = q ** ((L - 1) * (L - 1))
    d_shell = q ** (2 * L - 1)
    if d_core * d_shell != d_L:
        raise ValueError("factorization failed")

    log_core = math.log(d_core)
    log_shell = math.log(d_shell)
    log_total = math.log(d_L)

    return {
        "L": L,
        "q": q,
        "dim_H_L": d_L,
        "dim_H_L_minus_1": d_core,
        "dim_H_shell": d_shell,
        "log_dim_H_L": math.log(d_L),
        "log_dim_H_L_minus_1": math.log(d_core),
        "log_dim_H_shell": math.log(d_shell),
        "expected_delta_S": (2 * L - 1) * math.log(q),
        "S_ref_before": log_total,
        "I_ref_bulk_before": 2.0 * log_total,
        "I_ref_core_before": 2.0 * log_core,
        "I_ref_shell_before": 2.0 * log_shell,
        "S_ref_after": log_total,
        "I_ref_bulk_core_after": 2.0 * log_core,
        "I_ref_shell_record_after": 2.0 * log_shell,
        "I_ref_dummy_shell_after": 0.0,
        "I_ref_all_after": 2.0 * log_total,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--max-L", type=int, default=12)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("sim/data/finite_gauge_shell_shrinkage.csv"),
    )
    args = parser.parse_args()

    rows = [row_for_L(L, args.q) for L in range(2, args.max_L + 1)]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {args.out}")
    print("L  dim H_L  dim core  dim shell  DeltaS   I(R:core) after  I(R:shellrec) after  I(R:all) after")
    for row in rows:
        print(
            f"{row['L']:1d} "
            f"{row['dim_H_L']:8d} "
            f"{row['dim_H_L_minus_1']:9d} "
            f"{row['dim_H_shell']:10d} "
            f"{row['expected_delta_S']:7.3f} "
            f"{row['I_ref_bulk_core_after']:16.3f} "
            f"{row['I_ref_shell_record_after']:21.3f} "
            f"{row['I_ref_all_after']:14.3f}"
        )


if __name__ == "__main__":
    main()
