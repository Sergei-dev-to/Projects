#!/usr/bin/env python3
"""Scan candidate natural core Hamiltonians for convex microcanonical windows."""
from __future__ import annotations

import argparse
import csv
import pathlib
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.linalg as la
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = ROOT / "sim" / "data"
DATADIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class SpinOps:
    sx: NDArray[np.float64]
    sz: NDArray[np.float64]
    zz_pairs: list[tuple[int, int, NDArray[np.float64]]]


def pauli() -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=float)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=float)
    return sx, sz


def kron_n(op_list: list[NDArray[np.float64]]) -> NDArray[np.float64]:
    out = op_list[0]
    for op in op_list[1:]:
        out = np.kron(out, op)
    return out


def build_spin_ops(n: int) -> SpinOps:
    sx, sz = pauli()
    sx_sum = np.zeros((2**n, 2**n), dtype=float)
    sz_fields = []
    for i in range(n):
        ops = [np.eye(2)] * n
        ops[i] = sx
        sx_sum += kron_n(ops)

    zz_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            ops = [np.eye(2)] * n
            ops[i] = sz
            ops[j] = sz
            zz_pairs.append((i, j, kron_n(ops)))

    return SpinOps(sx=sx_sum, sz=sz, zz_pairs=zz_pairs)


def build_long_range_ising(
    n: int,
    alpha: float,
    jz: float,
    hx: float,
    hz_dis: float,
    seed: int,
    ops: SpinOps,
) -> NDArray[np.float64]:
    rng = np.random.default_rng(seed)
    dim = 2**n
    h = np.zeros((dim, dim), dtype=float)

    norm = 0.0
    pair_terms = []
    for i, j, zz in ops.zz_pairs:
        dist = min(j - i, n - (j - i))
        weight = 1.0 / (float(dist) ** alpha) if alpha > 0 else 1.0
        norm += weight
        pair_terms.append((weight, zz))
    norm = norm / n if norm > 0 else 1.0

    for weight, zz in pair_terms:
        h += -(jz / max(norm * n, 1e-12)) * weight * zz

    h += -hx * ops.sx

    if hz_dis > 0.0:
        _, sz = pauli()
        fields = hz_dis * rng.uniform(-1.0, 1.0, size=n)
        for i, field in enumerate(fields):
            local = [np.eye(2)] * n
            local[i] = sz
            h += field * kron_n(local)

    return (h + h.T) / 2.0


def smooth(y: NDArray[np.float64], passes: int = 1) -> NDArray[np.float64]:
    out = y.astype(float).copy()
    kernel = np.array([0.25, 0.5, 0.25])
    for _ in range(passes):
        padded = np.pad(out, (1, 1), mode="edge")
        out = np.convolve(padded, kernel, mode="valid")
    return out


def microcanonical(evals: NDArray[np.float64], bins: int, smooth_passes: int) -> dict[str, NDArray[np.float64]]:
    hist, edges = np.histogram(evals, bins=bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    valid = hist > 0
    entropy = np.full_like(centers, np.nan, dtype=float)
    entropy[valid] = np.log(hist[valid].astype(float))
    # Fill empty bins by interpolation only for derivative diagnostics.
    if np.sum(valid) >= 2:
        entropy_filled = np.interp(centers, centers[valid], entropy[valid])
    else:
        entropy_filled = np.nan_to_num(entropy, nan=0.0)
    entropy_smooth = smooth(entropy_filled, smooth_passes)
    beta = np.gradient(entropy_smooth, centers)
    curvature = np.gradient(beta, centers)
    temp = np.where(beta > 0, 1.0 / beta, np.nan)
    heat_capacity = np.where(curvature > 0, -(beta**2) / curvature, np.nan)
    return {
        "centers": centers,
        "hist": hist.astype(float),
        "entropy": entropy,
        "entropy_smooth": entropy_smooth,
        "beta": beta,
        "curvature": curvature,
        "temperature": temp,
        "heat_capacity": heat_capacity,
    }


def longest_convex_window(mc: dict[str, NDArray[np.float64]], min_hist: int) -> dict[str, float]:
    hist = mc["hist"]
    beta = mc["beta"]
    curv = mc["curvature"]
    centers = mc["centers"]
    mask = (hist >= min_hist) & np.isfinite(beta) & (beta > 0) & np.isfinite(curv) & (curv > 0)

    best_start = -1
    best_len = 0
    start = None
    for idx, ok in enumerate(mask):
        if ok and start is None:
            start = idx
        if (not ok or idx == len(mask) - 1) and start is not None:
            end = idx if not ok else idx + 1
            length = end - start
            if length > best_len:
                best_len = length
                best_start = start
            start = None

    if best_len == 0:
        return {
            "convex_bins": 0,
            "convex_width": 0.0,
            "convex_e_min": np.nan,
            "convex_e_max": np.nan,
            "max_curvature": float(np.nanmax(curv)),
        }

    end = best_start + best_len
    return {
        "convex_bins": int(best_len),
        "convex_width": float(centers[end - 1] - centers[best_start]),
        "convex_e_min": float(centers[best_start]),
        "convex_e_max": float(centers[end - 1]),
        "max_curvature": float(np.nanmax(curv[best_start:end])),
    }


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan long-range spin cores for convex DOS windows.")
    parser.add_argument("--N", type=int, default=10)
    parser.add_argument("--alphas", default="0,0.5,1,2")
    parser.add_argument("--jz-list", default="0.5,1,2")
    parser.add_argument("--hx-list", default="0.2,0.5,1")
    parser.add_argument("--hz-dis", type=float, default=0.05)
    parser.add_argument("--bins-list", default="16,20,24")
    parser.add_argument("--smooth-passes", type=int, default=1)
    parser.add_argument("--min-hist", type=int, default=2)
    parser.add_argument("--seed", type=int, default=1357)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "natural_core_spin_scan.csv",
    )
    parser.add_argument(
        "--output-npz",
        type=pathlib.Path,
        default=DATADIR / "natural_core_spin_scan.npz",
    )
    args = parser.parse_args(argv)

    alphas = parse_list(args.alphas, float)
    jz_values = parse_list(args.jz_list, float)
    hx_values = parse_list(args.hx_list, float)
    bins_values = parse_list(args.bins_list, int)

    print(f"[natural-core] precomputing spin operators N={args.N}")
    ops = build_spin_ops(args.N)
    rows = []
    spectra = {}
    diagnostics = {}

    total = len(alphas) * len(jz_values) * len(hx_values)
    count = 0
    for alpha in alphas:
        for jz in jz_values:
            for hx in hx_values:
                count += 1
                key = f"alpha{alpha:g}_jz{jz:g}_hx{hx:g}".replace(".", "p")
                print(f"[natural-core] {count}/{total}: alpha={alpha:g}, jz={jz:g}, hx={hx:g}")
                h = build_long_range_ising(args.N, alpha, jz, hx, args.hz_dis, args.seed, ops)
                evals = la.eigvalsh(h)
                spectra[key] = evals

                by_bins = []
                for bins in bins_values:
                    mc = microcanonical(evals, bins, args.smooth_passes)
                    win = longest_convex_window(mc, args.min_hist)
                    row = {
                        "model": "long_range_ising",
                        "N": args.N,
                        "alpha": alpha,
                        "jz": jz,
                        "hx": hx,
                        "hz_dis": args.hz_dis,
                        "bins": bins,
                        "smooth_passes": args.smooth_passes,
                        **win,
                    }
                    rows.append(row)
                    by_bins.append((bins, mc, win))

                # Store the middle bin diagnostic for plotting.
                bins, mc, win = by_bins[len(by_bins) // 2]
                for name, arr in mc.items():
                    diagnostics[f"{key}_bins{bins}_{name}"] = arr

    fieldnames = [
        "model",
        "N",
        "alpha",
        "jz",
        "hx",
        "hz_dis",
        "bins",
        "smooth_passes",
        "convex_bins",
        "convex_width",
        "convex_e_min",
        "convex_e_max",
        "max_curvature",
    ]
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    np.savez(args.output_npz, **spectra, **diagnostics)
    print(f"[natural-core] wrote {args.output_csv}")
    print(f"[natural-core] wrote {args.output_npz}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
