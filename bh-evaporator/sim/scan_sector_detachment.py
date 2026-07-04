#!/usr/bin/env python3
"""Scan sector-detachment diagnostics over operator structure and bandwidth."""
from __future__ import annotations

import argparse
import csv
import pathlib

from sector_detachment_diagnostics import DATADIR, Params, build_transition, diagnostics


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def run_row(args: argparse.Namespace, operator: str, bandwidth: float, seed: int) -> dict[str, float | int | str]:
    params = Params(
        n=args.n,
        q=args.q,
        alpha=args.alpha,
        bandwidth=bandwidth,
        mass_law=args.mass_law,
        operator=operator,
        seed=seed,
        omega0=args.omega0,
        envelope_width=args.envelope_width,
        ohmic_power=args.ohmic_power,
        min_gap=args.min_gap,
        spectral_bins=args.spectral_bins,
        time_points=args.time_points,
        t_max=args.t_max,
        target_total_width=args.target_total_width,
        doorway_rank=args.doorway_rank,
    )
    d, eval_high, eval_low_tiled, labels = build_transition(params)
    diag = diagnostics(params, d, eval_high, eval_low_tiled, labels)
    return diag


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=8)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--alpha", type=float, default=8.0)
    parser.add_argument("--mass-law", choices=["sqrt", "linear"], default="sqrt")
    parser.add_argument("--operators", default="local,scrambled,aligned,low_rank")
    parser.add_argument("--bandwidths", default="0,0.02,0.05,0.1,0.25,0.5,1.0")
    parser.add_argument("--seeds", default="2468,2469,2470")
    parser.add_argument("--omega0", type=float, default=None)
    parser.add_argument("--envelope-width", type=float, default=0.8)
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument("--min-gap", type=float, default=0.0)
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=400)
    parser.add_argument("--t-max", type=float, default=80.0)
    parser.add_argument("--target-total-width", type=float, default=1.0)
    parser.add_argument("--doorway-rank", type=int, default=4)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "sector_detachment_scan.csv",
    )
    args = parser.parse_args()

    operators = parse_list(args.operators, str)
    bandwidths = parse_list(args.bandwidths, float)
    seeds = parse_list(args.seeds, int)
    rows: list[dict[str, float | int | str]] = []
    total = len(operators) * len(bandwidths) * len(seeds)
    count = 0
    for operator in operators:
        for bandwidth in bandwidths:
            for seed in seeds:
                count += 1
                print(
                    f"[sector-detach-scan] {count}/{total} "
                    f"operator={operator} bandwidth={bandwidth:g} seed={seed}",
                    flush=True,
                )
                try:
                    row = run_row(args, operator, bandwidth, seed)
                except Exception as exc:
                    row = {
                        "operator": operator,
                        "bandwidth": bandwidth,
                        "seed": seed,
                        "error": str(exc),
                    }
                rows.append(row)

    write_csv(args.output_csv, rows)
    print(f"[sector-detach-scan] wrote {args.output_csv}")

    print("operator bandwidth gram_norm record_norm spec_norm c_tail largest")
    grouped = {}
    for row in rows:
        if "error" in row:
            continue
        key = (row["operator"], row["bandwidth"])
        grouped.setdefault(key, []).append(row)
    for key in sorted(grouped, key=lambda item: (str(item[0]), float(item[1]))):
        vals = grouped[key]
        mean = lambda name: sum(float(row[name]) for row in vals) / len(vals)
        print(
            f"{key[0]:9s} {float(key[1]):8.3g} "
            f"{mean('channel_gram_participation_norm'):9.3f} "
            f"{mean('accessible_record_gram_participation_norm'):11.3f} "
            f"{mean('spectral_participation_norm'):9.3f} "
            f"{mean('c_long_mean'):7.4f} "
            f"{mean('largest_channel_width_fraction'):7.4f}"
        )


if __name__ == "__main__":
    main()
