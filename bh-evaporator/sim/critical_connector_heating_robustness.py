#!/usr/bin/env python3
"""Robustness scan for the critical connector heating gate."""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np

import critical_connector_heating_gate as gate
from scan_bose_hubbard_dos import DATADIR


def parse_floats(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    rows: list[dict[str, float | str]] = []
    etas = parse_floats(args.etas)
    kappas = parse_floats(args.emit_kappas)
    modes = [part.strip() for part in args.energy_modes.split(",") if part.strip()]
    for mode in modes:
        for eta in etas:
            for kappa in kappas:
                ns = argparse.Namespace(
                    n_min=args.n_min,
                    n_max=args.n_max,
                    eta=eta,
                    emit_kappa=kappa,
                    energy_mode=mode,
                    cutoff_multiple=args.cutoff_multiple,
                    models=args.models,
                )
                _, summary = gate.run(ns)
                for row in summary:
                    rows.append(
                        {
                            **row,
                            "eta": eta,
                            "cutoff_multiple": args.cutoff_multiple,
                        }
                    )

    models = sorted({str(row["model"]) for row in rows})
    aggregate: list[dict[str, float | str]] = []
    for model in models:
        sub = [row for row in rows if row["model"] == model]
        pass_flags = np.asarray([str(row["passes_heating_gate"]) == "yes" for row in sub])
        heat_frac = np.asarray([float(row["heating_fraction"]) for row in sub])
        ratio_nmax = np.asarray([float(row["ratio_at_nmax"]) for row in sub])
        aggregate.append(
            {
                "model": model,
                "settings_tested": len(sub),
                "strict_pass_fraction": float(np.mean(pass_flags)),
                "mean_heating_fraction": float(np.mean(heat_frac)),
                "min_heating_fraction": float(np.min(heat_frac)),
                "mean_ratio_at_nmax": float(np.mean(ratio_nmax)),
                "min_ratio_at_nmax": float(np.min(ratio_nmax)),
                "robust_status": (
                    "robust"
                    if np.all(pass_flags)
                    else "mostly"
                    if np.mean(heat_frac) >= args.mostly_threshold and np.min(ratio_nmax) > 1.0
                    else "fragile"
                    if np.mean(heat_frac) >= 0.5
                    else "fails"
                ),
            }
        )
    return rows, aggregate


def write_csv(path: pathlib.Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-min", type=int, default=8)
    parser.add_argument("--n-max", type=int, default=128)
    parser.add_argument("--etas", default="0.5,1.0,2.0")
    parser.add_argument("--emit-kappas", default="0.25,0.5,1.0,2.0")
    parser.add_argument("--energy-modes", default="bose,classical_cutoff")
    parser.add_argument("--models", default="")
    parser.add_argument("--cutoff-multiple", type=float, default=3.0)
    parser.add_argument("--mostly-threshold", type=float, default=0.95)
    parser.add_argument(
        "--rows-csv",
        type=pathlib.Path,
        default=DATADIR / "critical_connector_heating_robustness_rows.csv",
    )
    parser.add_argument(
        "--aggregate-csv",
        type=pathlib.Path,
        default=DATADIR / "critical_connector_heating_robustness_aggregate.csv",
    )
    args = parser.parse_args(argv)
    rows, aggregate = run(args)
    write_csv(args.rows_csv, rows)
    write_csv(args.aggregate_csv, aggregate)
    print(f"[critical-heating-robustness] wrote {args.rows_csv}")
    print(f"[critical-heating-robustness] wrote {args.aggregate_csv}")
    for row in aggregate:
        print(
            "{model}: status={robust_status} strict={strict_pass_fraction:.2f} "
            "mean_heat={mean_heating_fraction:.2f} min_ratio={min_ratio_at_nmax:.4f}".format(**row)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
