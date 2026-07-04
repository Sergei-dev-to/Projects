#!/usr/bin/env python3
"""Parameter scan for the reduced-density Hamiltonian evaporator."""
from __future__ import annotations

import argparse
import csv
import pathlib
from types import SimpleNamespace

import numpy as np

from hamiltonian_shell_density_channel import run_one_seed, summarize


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = ROOT / "sim" / "data"
DATADIR.mkdir(parents=True, exist_ok=True)


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def run_combo(base_args: argparse.Namespace, curvature: float, channels: int, g: float) -> dict[str, float]:
    args = SimpleNamespace(**vars(base_args))
    args.curvature = curvature
    args.channels = channels
    args.g = g

    results = []
    first_ham = None
    for i in range(args.seeds):
        ham, result = run_one_seed(args, args.seed + i)
        if first_ham is None:
            first_ham = ham
        results.append(result)

    assert first_ham is not None
    summary = summarize(results)
    summary.update(
        {
            "curvature": float(curvature),
            "channels": int(channels),
            "g": float(g),
            "d_core": int(np.sum(first_ham.shell.dims)),
            "bin_dim": int(first_ham.bin_dim),
            "steps": int(args.steps),
            "seeds": int(args.seeds),
        }
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan Hamiltonian density-channel parameters.")
    parser.add_argument("--curvatures", default="1,2,3")
    parser.add_argument("--channels-list", default="1,2,4,8")
    parser.add_argument("--g-list", default="0.3,0.5,0.8,1.2")
    parser.add_argument("--shells", type=int, default=8)
    parser.add_argument("--dmax", type=int, default=32)
    parser.add_argument("--dmin", type=int, default=1)
    parser.add_argument("--e-high", type=float, default=8.0)
    parser.add_argument("--e-low", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.8)
    parser.add_argument("--chaos", type=float, default=0.0)
    parser.add_argument("--detuning", type=float, default=0.0)
    parser.add_argument("--steps", type=int, default=48)
    parser.add_argument("--seeds", type=int, default=2)
    parser.add_argument("--seed", type=int, default=8642)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_density_scan.csv",
    )
    parser.add_argument(
        "--output-npz",
        type=pathlib.Path,
        default=DATADIR / "hamiltonian_density_scan.npz",
    )
    args = parser.parse_args(argv)

    curvatures = parse_list(args.curvatures, float)
    channels_values = parse_list(args.channels_list, int)
    g_values = parse_list(args.g_list, float)

    rows: list[dict[str, float]] = []
    total = len(curvatures) * len(channels_values) * len(g_values)
    count = 0

    for curvature in curvatures:
        for channels in channels_values:
            for g in g_values:
                count += 1
                print(
                    f"[scan] {count}/{total}: curvature={curvature:g}, "
                    f"channels={channels}, g={g:g}"
                )
                rows.append(run_combo(args, curvature, channels, g))

    fieldnames = [
        "curvature",
        "channels",
        "g",
        "accel_ratio_mid_over_early",
        "peak_s2",
        "peak_step",
        "final_energy",
        "initial_energy",
        "mean_emitted_probability",
        "max_norm_error",
        "d_core",
        "bin_dim",
        "steps",
        "seeds",
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    shape = (len(curvatures), len(channels_values), len(g_values))
    accel = np.full(shape, np.nan)
    peak_s2 = np.full(shape, np.nan)
    peak_step = np.full(shape, np.nan)
    final_energy = np.full(shape, np.nan)
    mean_emit = np.full(shape, np.nan)
    for row in rows:
        i = curvatures.index(float(row["curvature"]))
        j = channels_values.index(int(row["channels"]))
        k = g_values.index(float(row["g"]))
        accel[i, j, k] = row["accel_ratio_mid_over_early"]
        peak_s2[i, j, k] = row["peak_s2"]
        peak_step[i, j, k] = row["peak_step"]
        final_energy[i, j, k] = row["final_energy"]
        mean_emit[i, j, k] = row["mean_emitted_probability"]

    np.savez(
        args.output_npz,
        curvatures=np.asarray(curvatures, dtype=float),
        channels=np.asarray(channels_values, dtype=int),
        g_values=np.asarray(g_values, dtype=float),
        accel_ratio=accel,
        peak_s2=peak_s2,
        peak_step=peak_step,
        final_energy=final_energy,
        mean_emitted_probability=mean_emit,
    )
    print(f"[scan] wrote {args.output_csv}")
    print(f"[scan] wrote {args.output_npz}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
