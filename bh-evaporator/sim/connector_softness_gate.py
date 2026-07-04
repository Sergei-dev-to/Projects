#!/usr/bin/env python3
"""Softness gate for connector-mode evaporator candidates.

This does not simulate evaporation.  It asks whether simple connector
Hamiltonians naturally produce microscopic gaps scaling like 1/N, as required
for Hawking-scale emissions when S ~ N^2 and M ~ N.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np

from scan_bose_hubbard_dos import DATADIR


def line_graph_complete_spectrum(n: int, scale_power: float) -> np.ndarray:
    """Spectrum of shifted line-graph hopping on connectors of K_n.

    Connector modes are edges of K_n.  Two connector modes hop if they share a
    site.  The line graph L(K_n) has adjacency eigenvalues:

      2(n-2)       multiplicity 1
      n-4          multiplicity n-1
      -2           multiplicity n(n-3)/2

    We use H = [lambda_max I - A] / n^scale_power so the ground is zero.
    """
    lam0 = 2.0 * (n - 2)
    eigs = [0.0]
    eigs.extend([(lam0 - (n - 4)) / (n**scale_power)] * (n - 1))
    eigs.extend([(lam0 - (-2.0)) / (n**scale_power)] * (n * (n - 3) // 2))
    return np.asarray(eigs, dtype=float)


def independent_connector_spectrum(n: int, epsilon: float) -> np.ndarray:
    n_conn = n * (n - 1) // 2
    return np.concatenate(([0.0], np.full(n_conn, epsilon)))


def site_complete_graph_spectrum(n: int, scale_power: float) -> np.ndarray:
    """Collective site spectrum for comparison, shifted complete-graph hopping."""
    # Complete graph adjacency has n-1 and -1. Shifted gap is n / n^scale.
    return np.asarray([0.0] + [n / (n**scale_power)] * (n - 1), dtype=float)


def summarize_spectrum(eigs: np.ndarray, target: float) -> dict[str, float]:
    positive = np.sort(eigs[eigs > 1e-12])
    if positive.size == 0:
        return {
            "gap_min": np.nan,
            "gap_median": np.nan,
            "gap_p10": np.nan,
            "soft_fraction": 0.0,
        }
    return {
        "gap_min": float(positive[0]),
        "gap_median": float(np.median(positive)),
        "gap_p10": float(np.quantile(positive, 0.1)),
        "soft_fraction": float(np.mean(positive <= target)),
    }


def fit_power(ns: np.ndarray, values: np.ndarray) -> float:
    mask = np.isfinite(values) & (values > 0)
    if np.sum(mask) < 2:
        return np.nan
    coeff = np.polyfit(np.log(ns[mask]), np.log(values[mask]), 1)
    return float(coeff[0])


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    ns = np.arange(args.n_min, args.n_max + 1, dtype=int)
    rows: list[dict[str, float | str]] = []
    models: list[tuple[str, callable]] = [
        ("independent_fixed_gap", lambda n: independent_connector_spectrum(n, args.epsilon)),
        ("line_graph_unscaled", lambda n: line_graph_complete_spectrum(n, 0.0)),
        ("line_graph_kac_1_over_N", lambda n: line_graph_complete_spectrum(n, 1.0)),
        ("line_graph_soft_by_hand_1_over_N2", lambda n: line_graph_complete_spectrum(n, 2.0)),
        ("site_complete_kac_1_over_N", lambda n: site_complete_graph_spectrum(n, 1.0)),
    ]
    for model, builder in models:
        for n in ns:
            target = args.target_eta / n
            eigs = builder(int(n))
            summary = summarize_spectrum(eigs, target)
            rows.append(
                {
                    "model": model,
                    "N": int(n),
                    "target_1_over_N": target,
                    "n_modes": len(eigs),
                    **summary,
                }
            )
    aggregate: list[dict[str, float | str]] = []
    for model, _builder in models:
        sub = [row for row in rows if row["model"] == model]
        nvals = np.asarray([float(row["N"]) for row in sub])
        gaps = np.asarray([float(row["gap_min"]) for row in sub])
        med = np.asarray([float(row["gap_median"]) for row in sub])
        soft = np.asarray([float(row["soft_fraction"]) for row in sub])
        aggregate.append(
            {
                "model": model,
                "gap_min_power": fit_power(nvals, gaps),
                "gap_median_power": fit_power(nvals, med),
                "soft_fraction_at_nmax": float(soft[-1]),
                "gap_min_at_nmax": float(gaps[-1]),
                "gap_median_at_nmax": float(med[-1]),
                "target_at_nmax": args.target_eta / float(ns[-1]),
                "passes_softness_gate": "yes"
                if fit_power(nvals, gaps) <= -0.85 and float(soft[-1]) > 0.1
                else "no",
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
    parser.add_argument("--epsilon", type=float, default=1.0)
    parser.add_argument("--target-eta", type=float, default=1.0)
    parser.add_argument(
        "--rows-csv",
        type=pathlib.Path,
        default=DATADIR / "connector_softness_gate_rows.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "connector_softness_gate_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    write_csv(args.rows_csv, rows)
    write_csv(args.summary_csv, summary)
    print(f"[connector-softness] wrote {args.rows_csv}")
    print(f"[connector-softness] wrote {args.summary_csv}")
    for row in summary:
        print(
            "{model}: pass={passes_softness_gate} gap_power={gap_min_power:.3f} "
            "gap_nmax={gap_min_at_nmax:.4g} target={target_at_nmax:.4g} "
            "soft_frac={soft_fraction_at_nmax:.3f}".format(**row)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
