#!/usr/bin/env python3
"""Phase scan for natural accessible-record entropy rates.

This scans the regulated matrix proxy without an inserted source-to-record map.
The accessible record is the natural Q-sector radial/energy bin.  The broad
scan uses width entropy rate, which can be pushed deeper than the full Gram
diagnostic.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

from natural_record_entropy_rate import run_case
from sector_detachment_diagnostics import DATADIR


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
    parser.add_argument("--g-list", default="0.25,0.5,1,2")
    parser.add_argument("--fractions", default="0.25,0.30,0.35,0.40")
    parser.add_argument("--source-sets", default="h_terms")
    parser.add_argument("--record-bins-list", default="3,6")
    parser.add_argument("--rhos", default="0,1")
    parser.add_argument("--scrambling", choices=["identity", "random"], default="identity")
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--seed", type=int, default=13579)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "natural_record_phase_scan.csv",
    )
    args = parser.parse_args()

    rows = []
    for source_set in parse_list(args.source_sets, str):
        for g in parse_list(args.g_list, float):
            for fraction in parse_list(args.fractions, float):
                for record_bins in parse_list(args.record_bins_list, int):
                    for rho in parse_list(args.rhos, float):
                        case_args = argparse.Namespace(
                            cutoff=args.cutoff,
                            mu=args.mu,
                            g=g,
                            fraction=fraction,
                            source_set=source_set,
                            record_bins=record_bins,
                            rhos=str(rho),
                            rho=rho,
                            scramblings=args.scrambling,
                            scrambling=args.scrambling,
                            max_depth=args.max_depth,
                            width_only=True,
                            sample_gram=False,
                            sample_min_depth=args.max_depth + 1,
                            gram_samples=0,
                            normalize=args.normalize,
                            seed=args.seed,
                            output_csv=DATADIR / "_unused_natural_phase_scan.csv",
                        )
                        case_rows = run_case(case_args)
                        final = case_rows[-1]
                        first = case_rows[0]
                        final["one_step_total_width"] = first["total_sequence_width"]
                        final["one_step_width_participation"] = first[
                            "sequence_width_participation"
                        ]
                        final["one_step_largest_width_fraction"] = first[
                            "largest_sequence_width_fraction"
                        ]
                        rows.append(final)
                        print(
                            "g={:.3g} f={:.2f} bins={} rho={:.1f} "
                            "gamma1={:.3g} hW/logM={:.3f} partW={:.2f} largest={:.4f}".format(
                                g,
                                fraction,
                                record_bins,
                                rho,
                                float(final["one_step_total_width"]),
                                float(final["h_width_fraction"]),
                                float(final["sequence_width_participation"]),
                                float(final["largest_sequence_width_fraction"]),
                            ),
                            flush=True,
                        )
    write_csv(args.output_csv, rows)
    print(f"[natural-phase-scan] wrote {args.output_csv}")
    print("top by width entropy rate:")
    for row in sorted(rows, key=lambda r: float(r["h_width_fraction"]), reverse=True)[:12]:
        print(
            "g={:.3g} f={:.2f} bins={} rho={:.1f} source={} "
            "gamma1={:.3g} hW/logM={:.3f} width_part={:.2f} largest={:.4f}".format(
                float(row["g"]),
                float(row["fraction"]),
                int(row["record_bins"]),
                float(row["rho"]),
                str(row["source_set"]),
                float(row["one_step_total_width"]),
                float(row["h_width_fraction"]),
                float(row["sequence_width_participation"]),
                float(row["largest_sequence_width_fraction"]),
            )
        )


if __name__ == "__main__":
    main()
