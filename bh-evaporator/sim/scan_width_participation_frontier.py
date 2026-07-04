#!/usr/bin/env python3
"""Scan the width-versus-participation frontier for daughter-memory lifts."""
from __future__ import annotations

import argparse
import csv
import pathlib

from daughter_memory_participation import run_row
from sector_detachment_diagnostics import DATADIR


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def write_csv(path: pathlib.Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoffs", default="4,5")
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--g-values", default="0.5,1,2")
    parser.add_argument("--fractions", default="0.2,0.25,0.3,0.35,0.4")
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument("--source-sets", default="quadratic,h_terms")
    parser.add_argument("--rhos", default="0,0.5,1")
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=200)
    parser.add_argument("--t-max", type=float, default=40.0)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "width_participation_frontier.csv",
    )
    args = parser.parse_args()

    rows = []
    cutoffs = parse_list(args.cutoffs, int)
    gs = parse_list(args.g_values, float)
    fractions = parse_list(args.fractions, float)
    source_sets = parse_list(args.source_sets, str)
    rhos = parse_list(args.rhos, float)
    total = len(cutoffs) * len(gs) * len(fractions) * len(source_sets) * len(rhos)
    count = 0
    for cutoff in cutoffs:
        for g in gs:
            for fraction in fractions:
                for source_set in source_sets:
                    for rho in rhos:
                        count += 1
                        print(
                            f"[frontier] {count}/{total} cutoff={cutoff} g={g:g} "
                            f"fraction={fraction:g} source={source_set} rho={rho:g}",
                            flush=True,
                        )
                        row_args = argparse.Namespace(
                            cutoff=cutoff,
                            mu=args.mu,
                            g=g,
                            fraction=fraction,
                            record_bins=args.record_bins,
                            source_set=source_set,
                            spectral_bins=args.spectral_bins,
                            time_points=args.time_points,
                            t_max=args.t_max,
                        )
                        try:
                            row = run_row(row_args, rho)
                        except Exception as exc:
                            row = {
                                "cutoff": cutoff,
                                "g": g,
                                "fraction": fraction,
                                "source_set": source_set,
                                "rho": rho,
                                "error": str(exc),
                            }
                        rows.append(row)
    write_csv(args.output_csv, rows)
    print(f"[frontier] wrote {args.output_csv}")

    valid = [row for row in rows if "error" not in row]
    valid.sort(
        key=lambda row: (
            float(row.get("gamma_total", 0.0))
            * float(row.get("channel_gram_participation_norm", 0.0))
            * float(row.get("accessible_record_gram_participation_norm", 0.0))
        ),
        reverse=True,
    )
    print("top width*full*record")
    print("cut g frac source rho gamma full record largest score")
    for row in valid[:12]:
        score = (
            float(row["gamma_total"])
            * float(row["channel_gram_participation_norm"])
            * float(row["accessible_record_gram_participation_norm"])
        )
        print(
            f"{int(row['cutoff']):3d} {float(row['g']):3.1f} "
            f"{float(row['fraction']):4.2f} {str(row['source_set']):9s} "
            f"{float(row['rho']):3.1f} {float(row['gamma_total']):9.3g} "
            f"{float(row['channel_gram_participation_norm']):6.3f} "
            f"{float(row['accessible_record_gram_participation_norm']):6.3f} "
            f"{float(row['largest_channel_width_fraction']):7.3f} "
            f"{score:9.3g}"
        )


if __name__ == "__main__":
    main()
