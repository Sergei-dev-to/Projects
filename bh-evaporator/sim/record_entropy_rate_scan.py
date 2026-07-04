#!/usr/bin/env python3
"""Entropy-rate scan for repeated accessible records.

This wraps recycled_record_map_dynamics.py and reports the effective record
entropy rates

    h(k) = log N_eff(k) / k

for Gram participation and width participation.  The normalized rates divide
by log(number of record labels), so a value near one means record histories are
using the available alphabet efficiently.
"""
from __future__ import annotations

import argparse
import csv
import math
import pathlib
from types import SimpleNamespace

from recycled_record_map_dynamics import run
from sector_detachment_diagnostics import DATADIR


def parse_csv_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def run_case(
    base: argparse.Namespace,
    record_map: str,
    records: int,
    rho: float,
    scrambling: str,
) -> list[dict[str, float | int | str]]:
    args = SimpleNamespace(**vars(base))
    args.record_map = record_map
    args.records = records
    args.rho = rho
    args.scrambling = scrambling
    args.output_csv = DATADIR / "_unused_record_entropy_rate_scan.csv"
    rows = run(args)
    log_records = math.log(records)
    enriched = []
    for row in rows:
        depth = int(row["depth"])
        gram_part = max(float(row["sequence_gram_participation"]), 1e-300)
        width_part = max(float(row["sequence_width_participation"]), 1e-300)
        h_gram = math.log(gram_part) / depth
        h_width = math.log(width_part) / depth
        enriched.append(
            {
                **row,
                "h_gram": h_gram,
                "h_width": h_width,
                "h_gram_fraction": h_gram / log_records if log_records > 0 else 0.0,
                "h_width_fraction": h_width / log_records if log_records > 0 else 0.0,
            }
        )
    return enriched


def summarize(rows: list[dict[str, float | int | str]]) -> dict[str, float | int | str]:
    last = rows[-1]
    return {
        "record_map": last["record_map"],
        "records": last["records"],
        "rho": last["rho"],
        "scrambling": last["scrambling"],
        "cutoff": last["cutoff"],
        "g": last["g"],
        "fraction": last["fraction"],
        "source_set": last["source_set"],
        "depth": last["depth"],
        "n_sequences": last["n_sequences"],
        "sequence_gram_participation": last["sequence_gram_participation"],
        "sequence_gram_participation_norm": last["sequence_gram_participation_norm"],
        "sequence_width_participation": last["sequence_width_participation"],
        "sequence_width_participation_norm": last["sequence_width_participation_norm"],
        "largest_sequence_width_fraction": last["largest_sequence_width_fraction"],
        "h_gram": last["h_gram"],
        "h_width": last["h_width"],
        "h_gram_fraction": last["h_gram_fraction"],
        "h_width_fraction": last["h_width_fraction"],
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
    parser.add_argument("--g", type=float, default=2.0)
    parser.add_argument("--fraction", type=float, default=0.40)
    parser.add_argument("--source-set", choices=["quadratic", "h_terms"], default="h_terms")
    parser.add_argument("--record-maps", default="aligned,round_robin,random_orthogonal,random_dense")
    parser.add_argument("--records-list", default="3,4")
    parser.add_argument("--rhos", default="0,1")
    parser.add_argument("--scramblings", default="identity,random")
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--normalize", action="store_true")
    parser.add_argument("--seed", type=int, default=13579)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "record_entropy_rate_scan.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "record_entropy_rate_summary.csv",
    )
    args = parser.parse_args()

    all_rows: list[dict[str, float | int | str]] = []
    summaries: list[dict[str, float | int | str]] = []
    for record_map in parse_csv_list(args.record_maps, str):
        for records in parse_csv_list(args.records_list, int):
            for rho in parse_csv_list(args.rhos, float):
                for scrambling in parse_csv_list(args.scramblings, str):
                    rows = run_case(args, record_map, records, rho, scrambling)
                    all_rows.extend(rows)
                    summaries.append(summarize(rows))

    write_csv(args.output_csv, all_rows)
    write_csv(args.summary_csv, summaries)
    print(f"[record-entropy-rate] wrote {args.output_csv}")
    print(f"[record-entropy-rate] wrote {args.summary_csv}")
    print("map records rho scr depth gram_part width_part hG/logM hW/logM largest")
    for row in sorted(
        summaries,
        key=lambda r: (float(r["h_width_fraction"]), float(r["h_gram_fraction"])),
        reverse=True,
    ):
        print(
            f"{str(row['record_map']):17s} {int(row['records']):7d} "
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
