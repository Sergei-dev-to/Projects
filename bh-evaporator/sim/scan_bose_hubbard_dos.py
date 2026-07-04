#!/usr/bin/env python3
"""Scan small Bose-Hubbard cores for convex microcanonical entropy windows."""
from __future__ import annotations

import argparse
import csv
import itertools
import pathlib

import numpy as np
from numpy.typing import NDArray

try:
    import scipy.linalg as la
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required: {exc}")


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = ROOT / "sim" / "data"
DATADIR.mkdir(parents=True, exist_ok=True)


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, parts - 1):
            yield (first,) + rest


def make_edges(sites: int, geometry: str, j_inter: float) -> list[tuple[int, int, float]]:
    if geometry == "ring":
        return [(i, (i + 1) % sites, 1.0) for i in range(sites)]

    if geometry == "open":
        return [(i, i + 1, 1.0) for i in range(sites - 1)]

    if geometry == "dimers":
        edges = []
        for i in range(0, sites - 1, 2):
            edges.append((i, i + 1, 1.0))
        for i in range(1, sites - 2, 2):
            edges.append((i, i + 1, j_inter))
        return edges

    raise ValueError(f"unknown geometry: {geometry}")


def build_bose_hubbard(
    sites: int,
    particles: int,
    geometry: str,
    j: float,
    u: float,
    v_nn: float,
    j_inter: float,
    disorder: float,
    seed: int,
) -> tuple[NDArray[np.float64], list[tuple[int, ...]]]:
    basis = list(compositions(particles, sites))
    index = {state: idx for idx, state in enumerate(basis)}
    dim = len(basis)
    h = np.zeros((dim, dim), dtype=float)
    rng = np.random.default_rng(seed)
    onsite = disorder * rng.uniform(-1.0, 1.0, size=sites)
    edges = make_edges(sites, geometry, j_inter)

    for a, state in enumerate(basis):
        n = np.array(state, dtype=int)
        h[a, a] += 0.5 * u * float(np.sum(n * (n - 1)))
        h[a, a] += float(np.dot(onsite, n))
        if v_nn != 0.0:
            for i, k, edge_scale in edges:
                h[a, a] += v_nn * edge_scale * n[i] * n[k]

        for i, k, edge_scale in edges:
            amp = j * edge_scale
            if n[k] > 0:
                moved = list(state)
                moved[i] += 1
                moved[k] -= 1
                b = index[tuple(moved)]
                h[b, a] += -amp * np.sqrt((n[i] + 1) * n[k])
            if n[i] > 0:
                moved = list(state)
                moved[i] -= 1
                moved[k] += 1
                b = index[tuple(moved)]
                h[b, a] += -amp * np.sqrt(n[i] * (n[k] + 1))

    return (h + h.T) / 2.0, basis


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
    if np.sum(valid) >= 2:
        entropy_filled = np.interp(centers, centers[valid], entropy[valid])
    else:
        entropy_filled = np.nan_to_num(entropy, nan=0.0)
    entropy_smooth = smooth(entropy_filled, smooth_passes)
    beta = np.gradient(entropy_smooth, centers)
    curvature = np.gradient(beta, centers)
    return {
        "centers": centers,
        "hist": hist.astype(float),
        "entropy": entropy,
        "entropy_smooth": entropy_smooth,
        "beta": beta,
        "curvature": curvature,
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan Bose-Hubbard cores for convex DOS windows.")
    parser.add_argument("--sites-list", default="4,6")
    parser.add_argument("--particles-list", default="6,8")
    parser.add_argument("--geometries", default="ring,dimers")
    parser.add_argument("--j-list", default="0.2,0.5,1.0")
    parser.add_argument("--u-list", default="-0.5,-1.0,-2.0,-4.0")
    parser.add_argument("--v-list", default="0.0,-0.2")
    parser.add_argument("--j-inter", type=float, default=0.2)
    parser.add_argument("--disorder", type=float, default=0.02)
    parser.add_argument("--bins-list", default="16,20,24")
    parser.add_argument("--smooth-passes", type=int, default=1)
    parser.add_argument("--min-hist", type=int, default=2)
    parser.add_argument("--seed", type=int, default=2468)
    parser.add_argument(
        "--output-csv",
        type=pathlib.Path,
        default=DATADIR / "natural_core_bose_hubbard_scan.csv",
    )
    parser.add_argument(
        "--output-npz",
        type=pathlib.Path,
        default=DATADIR / "natural_core_bose_hubbard_scan.npz",
    )
    args = parser.parse_args(argv)

    sites_values = parse_list(args.sites_list, int)
    particle_values = parse_list(args.particles_list, int)
    geometries = parse_list(args.geometries, str)
    j_values = parse_list(args.j_list, float)
    u_values = parse_list(args.u_list, float)
    v_values = parse_list(args.v_list, float)
    bins_values = parse_list(args.bins_list, int)

    rows = []
    spectra = {}
    diagnostics = {}
    cases = list(itertools.product(sites_values, particle_values, geometries, j_values, u_values, v_values))

    for count, (sites, particles, geometry, j, u, v_nn) in enumerate(cases, start=1):
        h, basis = build_bose_hubbard(
            sites,
            particles,
            geometry,
            j,
            u,
            v_nn,
            args.j_inter,
            args.disorder,
            args.seed,
        )
        key = (
            f"L{sites}_N{particles}_{geometry}_J{j:g}_U{u:g}_V{v_nn:g}"
            .replace("-", "m")
            .replace(".", "p")
        )
        print(
            f"[bose-hubbard] {count}/{len(cases)}: "
            f"L={sites} N={particles} {geometry} J={j:g} U={u:g} V={v_nn:g} dim={len(basis)}"
        )
        evals = la.eigvalsh(h)
        spectra[key] = evals

        by_bins = []
        for bins in bins_values:
            mc = microcanonical(evals, bins, args.smooth_passes)
            win = longest_convex_window(mc, args.min_hist)
            rows.append(
                {
                    "model": "bose_hubbard",
                    "sites": sites,
                    "particles": particles,
                    "geometry": geometry,
                    "dimension": len(basis),
                    "j": j,
                    "u": u,
                    "v_nn": v_nn,
                    "j_inter": args.j_inter,
                    "disorder": args.disorder,
                    "bins": bins,
                    "smooth_passes": args.smooth_passes,
                    **win,
                }
            )
            by_bins.append((bins, mc, win))

        bins, mc, win = by_bins[len(by_bins) // 2]
        for name, arr in mc.items():
            diagnostics[f"{key}_bins{bins}_{name}"] = arr

    fieldnames = [
        "model",
        "sites",
        "particles",
        "geometry",
        "dimension",
        "j",
        "u",
        "v_nn",
        "j_inter",
        "disorder",
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
    print(f"[bose-hubbard] wrote {args.output_csv}")
    print(f"[bose-hubbard] wrote {args.output_npz}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
