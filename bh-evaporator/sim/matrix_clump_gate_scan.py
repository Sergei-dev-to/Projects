#!/usr/bin/env python3
"""Gate scan for stripped matrix-clump escape and post-escape heating."""
from __future__ import annotations

import argparse
import csv
import pathlib
import sys

import numpy as np

import classical_matrix_clump as cmc
from scan_bose_hubbard_dos import DATADIR


def escaper_metrics(x: np.ndarray, p: np.ndarray, params: cmc.Params) -> dict[str, float]:
    radii, vecs = cmc.radial_basis(x)
    order = np.argsort(radii)
    esc = int(order[-1])
    keep = order[:-1]
    q = vecs
    xb = np.array([q.T @ xa @ q for xa in x])
    pb = np.array([q.T @ pa @ q for pa in p])
    off_x = 0.0
    off_p = 0.0
    diag_sep = 0.0
    for a in range(params.d):
        row_x = xb[a][esc, keep]
        row_p = pb[a][esc, keep]
        off_x += float(np.sum(row_x * row_x))
        off_p += float(np.sum(row_p * row_p))
        diffs = xb[a][esc, esc] - np.diag(xb[a])[keep]
        diag_sep += float(np.mean(diffs * diffs))
    r_sorted = radii[order]
    r_med = float(np.median(r_sorted[:-1])) if len(r_sorted) > 2 else float(np.median(r_sorted))
    return {
        "ratio": float(r_sorted[-1] / max(r_med, 1e-12)),
        "off_x": float(np.sqrt(off_x)),
        "off_p": float(np.sqrt(off_p)),
        "diag_sep": float(np.sqrt(diag_sep)),
    }


def run_with_gate(params: cmc.Params) -> dict[str, float | int | str]:
    x, p = cmc.initial_state(params)
    f = cmc.force(x, params.g)
    rows: list[dict[str, float]] = []
    for step in range(params.steps + 1):
        if step % params.sample_every == 0:
            row = cmc.sample(step * params.dt, x, p, params)
            row.update(escaper_metrics(x, p, params))
            rows.append(row)
        p_half = p + 0.5 * params.dt * f
        x = x + params.dt * p_half
        x = 0.5 * (x + np.swapaxes(x, 1, 2))
        for a in range(params.d):
            x[a] -= np.eye(params.n) * np.trace(x[a]) / params.n
        f_new = cmc.force(x, params.g)
        p = p_half + 0.5 * params.dt * f_new
        p = 0.5 * (p + np.swapaxes(p, 1, 2))
        for a in range(params.d):
            p[a] -= np.eye(params.n) * np.trace(p[a]) / params.n
        f = f_new

    e0 = rows[0]["E"]
    e_drift = max(abs(r["E"] - e0) for r in rows) / max(abs(e0), 1e-12)
    ratios = np.asarray([r["ratio"] for r in rows])
    off_x = np.asarray([r["off_x"] for r in rows])
    # A candidate escape should be spatially separated and have weak connector
    # amplitude to the clump.  The off-diagonal threshold is relative to the
    # run median so it does not depend on arbitrary normalization.
    off_threshold = max(float(np.median(off_x) * params.offdiag_factor), 1e-12)
    flags = (ratios >= params.escape_ratio) & (off_x <= off_threshold)
    longest = 0
    current = 0
    first_idx = None
    for idx, flag in enumerate(flags):
        if flag:
            if first_idx is None:
                first_idx = idx
            current += 1
            longest = max(longest, current)
        else:
            current = 0

    result: dict[str, float | int | str] = {
        "n": params.n,
        "d": params.d,
        "seed": params.seed,
        "x_scale": params.x_scale,
        "p_scale": params.p_scale,
        "steps": params.steps,
        "dt": params.dt,
        "energy_drift_rel": e_drift,
        "ratio_start": rows[0]["ratio"],
        "ratio_max": float(np.max(ratios)),
        "ratio_end": rows[-1]["ratio"],
        "off_x_median": float(np.median(off_x)),
        "off_x_min": float(np.min(off_x)),
        "escape_flag_fraction": float(np.mean(flags)),
        "longest_escape_samples": longest,
        "Tcl_start": rows[0]["T_cl"],
        "Tcl_end": rows[-1]["T_cl"],
        "Ecl_start": rows[0]["E_cl"],
        "Ecl_end": rows[-1]["E_cl"],
        "gate_pass": "no",
        "event_time": np.nan,
        "event_dEcl": np.nan,
        "event_dTcl": np.nan,
    }
    if first_idx is not None:
        before = rows[max(first_idx - params.before_samples, 0)]
        after = rows[min(first_idx + params.after_samples, len(rows) - 1)]
        d_e = after["E_cl"] - before["E_cl"]
        d_t = after["T_cl"] - before["T_cl"]
        result.update(
            {
                "event_time": rows[first_idx]["t"],
                "event_dEcl": d_e,
                "event_dTcl": d_t,
                "gate_pass": "yes" if d_e < 0.0 and d_t > 0.0 else "mixed",
            }
        )
    return result


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--d", type=int, default=2)
    parser.add_argument("--g", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.001)
    parser.add_argument("--steps", type=int, default=50000)
    parser.add_argument("--sample-every", type=int, default=50)
    parser.add_argument("--seeds", default="400,401,402,403,404,405")
    parser.add_argument("--x-scale", type=float, default=0.55)
    parser.add_argument("--p-scale", type=float, default=2.0)
    parser.add_argument("--escape-ratio", type=float, default=3.0)
    parser.add_argument("--offdiag-factor", type=float, default=0.75)
    parser.add_argument("--before-samples", type=int, default=5)
    parser.add_argument("--after-samples", type=int, default=20)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "matrix_clump_gate_scan.csv",
    )
    args = parser.parse_args(argv)
    seeds = [int(part.strip()) for part in args.seeds.split(",") if part.strip()]
    rows = []
    for seed in seeds:
        params = cmc.Params(
            n=args.n,
            d=args.d,
            g=args.g,
            dt=args.dt,
            steps=args.steps,
            sample_every=args.sample_every,
            seed=seed,
            x_scale=args.x_scale,
            p_scale=args.p_scale,
            escape_ratio=args.escape_ratio,
        )
        params.offdiag_factor = args.offdiag_factor  # type: ignore[attr-defined]
        params.before_samples = args.before_samples  # type: ignore[attr-defined]
        params.after_samples = args.after_samples  # type: ignore[attr-defined]
        row = run_with_gate(params)
        rows.append(row)
        print(
            "seed={seed} pass={gate_pass} ratio_max={ratio_max:.3f} "
            "dE={event_dEcl:.3f} dT={event_dTcl:.3f} drift={energy_drift_rel:.1e}".format(**row)
        )
        sys.stdout.flush()
    write_csv(args.output_csv, rows)
    n_pass = sum(1 for row in rows if row["gate_pass"] == "yes")
    n_mixed = sum(1 for row in rows if row["gate_pass"] == "mixed")
    print(f"[matrix-gate] wrote {args.output_csv}")
    print(f"[matrix-gate] pass={n_pass}/{len(rows)} mixed={n_mixed}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
