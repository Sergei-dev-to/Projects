#!/usr/bin/env python3
"""Scan the regulated matrix radial-detachment frontend."""
from __future__ import annotations

import argparse
import csv
import pathlib

from matrix_radial_detachment_diagnostics import Params, build_transition
from sector_detachment_diagnostics import DATADIR, diagnostics


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def run_row(cutoff: int, g: float, p_fraction: float, q_fraction: float, args: argparse.Namespace):
    params = Params(
        cutoff=cutoff,
        mu=args.mu,
        g=g,
        p_fraction=p_fraction,
        q_fraction=q_fraction,
        record_bins=args.record_bins,
        spectral_bins=args.spectral_bins,
        time_points=args.time_points,
        t_max=args.t_max,
    )
    d, e_p, e_q, labels, meta = build_transition(params)
    row = diagnostics(params, d, e_p, e_q, labels)
    row.update(meta)
    return row


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
    parser.add_argument("--g-values", default="0,0.5,1,2")
    parser.add_argument("--fractions", default="0.25,0.3,0.35")
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=300)
    parser.add_argument("--t-max", type=float, default=60.0)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "matrix_radial_detachment_scan.csv",
    )
    args = parser.parse_args()

    cutoffs = parse_list(args.cutoffs, int)
    g_values = parse_list(args.g_values, float)
    fractions = parse_list(args.fractions, float)
    rows = []
    total = len(cutoffs) * len(g_values) * len(fractions)
    count = 0
    for cutoff in cutoffs:
        for g in g_values:
            for fraction in fractions:
                count += 1
                print(
                    f"[matrix-radial-scan] {count}/{total} "
                    f"cutoff={cutoff} g={g:g} fraction={fraction:g}",
                    flush=True,
                )
                try:
                    row = run_row(cutoff, g, fraction, fraction, args)
                except Exception as exc:
                    row = {
                        "cutoff": cutoff,
                        "g": g,
                        "p_fraction": fraction,
                        "q_fraction": fraction,
                        "error": str(exc),
                    }
                rows.append(row)
    write_csv(args.output_csv, rows)
    print(f"[matrix-radial-scan] wrote {args.output_csv}")
    print("cut g frac gamma fullGram recordGram widthPart cTail decay largest")
    for row in rows:
        if "error" in row:
            print(f"{row['cutoff']:3d} {row['g']:4g} {row['p_fraction']:4g} ERROR {row['error']}")
            continue
        print(
            f"{int(row['n']):3d} {float(row['bandwidth']):4.1f} "
            f"{float(row['dim_p']) / float(row['dim_total']):4.2f} "
            f"{float(row['gamma_total']):7.3g} "
            f"{float(row['channel_gram_participation_norm']):8.3f} "
            f"{float(row['accessible_record_gram_participation_norm']):10.3f} "
            f"{float(row['accessible_record_width_participation_norm']):9.3f} "
            f"{float(row['c_long_mean']):7.4f} "
            f"{float(row['decay_time']):6.3f} "
            f"{float(row['largest_channel_width_fraction']):7.3f}"
        )


if __name__ == "__main__":
    main()
