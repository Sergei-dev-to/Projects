#!/usr/bin/env python3
"""Power scaling for connector spectra with spectral coupling weights.

For a local emission operator spread over connector modes, the earlier proxy was

  P ~ (1/L) sum_k exp(-omega_k/T) omega_k.

This script generalizes it to a matrix-element weight

  |g(omega)|^2 ~ omega^a

and fits the N-scaling of

  P_a ~ (1/L) sum_k exp(-omega_k/T) omega_k^(1+a).
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np

import collective_connector_softness_search as soft
from scan_bose_hubbard_dos import DATADIR


def parse_floats(text: str) -> list[float]:
    return [float(part.strip()) for part in text.split(",") if part.strip()]


def fit_power(ns: np.ndarray, values: np.ndarray) -> float:
    mask = np.isfinite(values) & (values > 0)
    if np.sum(mask) < 2:
        return np.nan
    return float(np.polyfit(np.log(ns[mask]), np.log(values[mask]), 1)[0])


def power_proxy(eigs: np.ndarray, temperature: float, coupling_power: float) -> float:
    vals = soft.normalize_positive(eigs)
    if vals.size == 0:
        return 0.0
    weights = np.exp(-vals / max(temperature, 1e-300))
    return float(np.sum(weights * np.power(vals, 1.0 + coupling_power)) / vals.size)


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    models = [part.strip() for part in args.models.split(",") if part.strip()]
    coupling_powers = parse_floats(args.coupling_powers)
    rows: list[dict[str, float | str]] = []
    for n in range(args.n_min, args.n_max + 1):
        temp = args.eta / n
        spectra = soft.spectra_for_n(n)
        for model in models:
            eigs = spectra[model]
            for a in coupling_powers:
                rows.append(
                    {
                        "N": n,
                        "T": temp,
                        "model": model,
                        "coupling_power_a": a,
                        "power_proxy": power_proxy(eigs, temp, a),
                    }
                )

    summary: list[dict[str, float | str]] = []
    for model in models:
        for a in coupling_powers:
            sub = [r for r in rows if r["model"] == model and float(r["coupling_power_a"]) == a]
            ns = np.asarray([float(r["N"]) for r in sub])
            powers = np.asarray([float(r["power_proxy"]) for r in sub])
            exponent = fit_power(ns, powers)
            summary.append(
                {
                    "model": model,
                    "coupling_power_a": a,
                    "power_exponent": exponent,
                    "power_at_nmax": float(powers[-1]),
                    "target_distance": abs(exponent + 2.0),
                    "near_bh_power": "yes" if -2.2 <= exponent <= -1.8 else "no",
                }
            )
    return rows, summary


def write_csv(path: pathlib.Path, rows: list[dict[str, float | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-min", type=int, default=16)
    parser.add_argument("--n-max", type=int, default=256)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument(
        "--models",
        default="connector_ring_crit,connector_ring_linear_crit,powerlaw_alpha1,powerlaw_alpha2",
    )
    parser.add_argument("--coupling-powers", default="0,0.25,0.5,0.75,1.0")
    parser.add_argument(
        "--rows-csv",
        type=pathlib.Path,
        default=DATADIR / "connector_power_coupling_rows.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "connector_power_coupling_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    write_csv(args.rows_csv, rows)
    write_csv(args.summary_csv, summary)
    print(f"[connector-power-coupling] wrote {args.rows_csv}")
    print(f"[connector-power-coupling] wrote {args.summary_csv}")
    for row in summary:
        if row["near_bh_power"] == "yes":
            print(
                "{model}: a={coupling_power_a:.2f} exponent={power_exponent:.3f}".format(
                    **row
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
