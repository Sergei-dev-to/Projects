#!/usr/bin/env python3
"""Heating gate for critical connector clumps.

The collective softness search showed that critical connector spectra can have
thermal quanta with omega ~ T ~ 1/N.  This script asks the next question:

  If the core loses energy of order T and its active connector sector changes
  from N to N-1, does the remaining core heat?

This is a thermodynamic gate, not an autonomous dynamics simulation.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np

import collective_connector_softness_search as soft
from scan_bose_hubbard_dos import DATADIR


def bose_energy(eigs: np.ndarray, temperature: float) -> float:
    vals = soft.normalize_positive(eigs)
    if vals.size == 0:
        return 0.0
    x = vals / max(temperature, 1e-300)
    occ = np.zeros_like(x)
    mask = x < 700.0
    occ[mask] = 1.0 / np.expm1(x[mask])
    return float(np.sum(vals * occ))


def classical_energy(eigs: np.ndarray, temperature: float, cutoff_multiple: float) -> float:
    vals = soft.normalize_positive(eigs)
    active = vals <= cutoff_multiple * temperature
    return float(np.sum(active) * temperature)


def solve_temperature(
    eigs: np.ndarray,
    target_energy: float,
    mode: str,
    cutoff_multiple: float,
) -> float:
    if target_energy <= 0.0:
        return 0.0
    lo = 1e-12
    hi = 1.0
    def energy(t: float) -> float:
        if mode == "bose":
            return bose_energy(eigs, t)
        if mode == "classical_cutoff":
            return classical_energy(eigs, t, cutoff_multiple)
        raise ValueError(mode)
    while energy(hi) < target_energy and hi < 1e6:
        hi *= 2.0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if energy(mid) < target_energy:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def connector_spectrum(model: str, n: int) -> np.ndarray:
    spectra = soft.spectra_for_n(n)
    if model not in spectra:
        raise ValueError(f"unknown model {model}; choices {sorted(spectra)}")
    return spectra[model]


def run(args: argparse.Namespace) -> tuple[list[dict[str, float | str]], list[dict[str, float | str]]]:
    rows: list[dict[str, float | str]] = []
    default_models = [
        "connector_grid_NxN_crit",
        "connector_rect_exactish_crit",
        "connector_ring_crit",
        "powerlaw_alpha1",
        "powerlaw_alpha2",
    ]
    model_text = getattr(args, "models", None)
    models = default_models if not model_text else [part.strip() for part in model_text.split(",") if part.strip()]
    for model in models:
        for n in range(args.n_min, args.n_max + 1):
            t0 = args.eta / n
            eig_n = connector_spectrum(model, n)
            eig_prev = connector_spectrum(model, n - 1)
            if args.energy_mode == "bose":
                e0 = bose_energy(eig_n, t0)
            else:
                e0 = classical_energy(eig_n, t0, args.cutoff_multiple)
            eps = args.emit_kappa * t0
            e_after = max(e0 - eps, 0.0)
            t_after = solve_temperature(eig_prev, e_after, args.energy_mode, args.cutoff_multiple)
            rows.append(
                {
                    "model": model,
                    "N": n,
                    "T_before": t0,
                    "T_after": t_after,
                    "heats": "yes" if t_after > t0 else "no",
                    "temperature_ratio": t_after / max(t0, 1e-300),
                    "E_before": e0,
                    "E_after": e_after,
                    "emitted_energy": eps,
                    "emitted_fraction": eps / max(e0, 1e-300),
                    "n_modes_before": len(soft.normalize_positive(eig_n)),
                    "n_modes_after": len(soft.normalize_positive(eig_prev)),
                }
            )
    summary: list[dict[str, float | str]] = []
    for model in models:
        sub = [r for r in rows if r["model"] == model]
        ratios = np.asarray([float(r["temperature_ratio"]) for r in sub])
        nmax = sub[-1]
        summary.append(
            {
                "model": model,
                "energy_mode": args.energy_mode,
                "emit_kappa": args.emit_kappa,
                "heating_fraction": float(np.mean(ratios > 1.0)),
                "min_temperature_ratio": float(np.min(ratios)),
                "median_temperature_ratio": float(np.median(ratios)),
                "ratio_at_nmax": float(nmax["temperature_ratio"]),
                "emitted_fraction_at_nmax": float(nmax["emitted_fraction"]),
                "passes_heating_gate": "yes" if np.all(ratios > 1.0) else "no",
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
    parser.add_argument("--n-min", type=int, default=8)
    parser.add_argument("--n-max", type=int, default=128)
    parser.add_argument("--eta", type=float, default=1.0)
    parser.add_argument("--emit-kappa", type=float, default=1.0)
    parser.add_argument("--energy-mode", choices=["bose", "classical_cutoff"], default="bose")
    parser.add_argument("--cutoff-multiple", type=float, default=3.0)
    parser.add_argument("--models", default="")
    parser.add_argument(
        "--rows-csv",
        type=pathlib.Path,
        default=DATADIR / "critical_connector_heating_rows.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "critical_connector_heating_summary.csv",
    )
    args = parser.parse_args(argv)
    rows, summary = run(args)
    write_csv(args.rows_csv, rows)
    write_csv(args.summary_csv, summary)
    print(f"[critical-heating] wrote {args.rows_csv}")
    print(f"[critical-heating] wrote {args.summary_csv}")
    for row in summary:
        print(
            "{model}: pass={passes_heating_gate} heatfrac={heating_fraction:.2f} "
            "ratio_nmax={ratio_at_nmax:.4f} emitfrac_nmax={emitted_fraction_at_nmax:.3e}".format(**row)
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
