#!/usr/bin/env python3
"""Generate Step 3 natural-core diagnostic figure."""
from __future__ import annotations

import argparse
import csv
import pathlib
from collections import defaultdict

import numpy as np


PROJECT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = PROJECT / "sim" / "data"


def read_rows(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open() as fh:
        return list(csv.DictReader(fh))


def bh_key(row: dict[str, str]) -> tuple:
    return (
        int(float(row["sites"])),
        int(float(row["particles"])),
        row["geometry"],
        float(row["j"]),
        float(row["u"]),
        float(row["v_nn"]),
    )


def bh_label(key: tuple) -> str:
    sites, particles, geometry, j, u, v_nn = key
    return f"L={sites}, N={particles}, {geometry}\nJ={j:g}, U={u:g}, V={v_nn:g}"


def summarize_bh_focus(path: pathlib.Path) -> list[tuple[int, float, tuple]]:
    rows = read_rows(path)
    grouped = defaultdict(list)
    for row in rows:
        grouped[bh_key(row)].append(row)

    out = []
    for key, vals in grouped.items():
        pass_count = sum(float(row["convex_bins"]) >= 3 for row in vals)
        mean_bins = float(np.mean([float(row["convex_bins"]) for row in vals]))
        out.append((pass_count, mean_bins, key))
    return sorted(out, reverse=True)


def convex_mask(z: np.lib.npyio.NpzFile, key: str, bins: int, min_hist: int) -> tuple[np.ndarray, ...]:
    prefix = f"{key}_bins{bins}"
    centers = z[f"{prefix}_centers"]
    hist = z[f"{prefix}_hist"]
    entropy = z[f"{prefix}_entropy"]
    entropy_smooth = z[f"{prefix}_entropy_smooth"]
    beta = z[f"{prefix}_beta"]
    curvature = z[f"{prefix}_curvature"]
    mask = (hist >= min_hist) & np.isfinite(beta) & (beta > 0) & np.isfinite(curvature) & (curvature > 0)
    return centers, hist, entropy, entropy_smooth, beta, curvature, mask


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bose-focus",
        type=pathlib.Path,
        default=DATADIR / "natural_core_bose_hubbard_focus_seed2468.csv",
    )
    parser.add_argument(
        "--bose-npz",
        type=pathlib.Path,
        default=DATADIR / "natural_core_bose_hubbard_focus_seed2468.npz",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=PROJECT / "step3_natural_core_probe.pdf",
    )
    args = parser.parse_args(argv)

    try:
        import matplotlib
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover
        raise SystemExit(f"matplotlib is required for plotting: {exc}")

    matplotlib.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.grid": True,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    z = np.load(args.bose_npz)
    key = "L6_N8_ring_J0p5_Um1_Vm0p2"
    centers, hist, entropy, entropy_smooth, beta, curvature, mask = convex_mask(z, key, bins=22, min_hist=2)

    fig, axes = plt.subplots(1, 3, figsize=(9.2, 3.0))

    ax = axes[0]
    ax.plot(centers, entropy_smooth, color="C0", label="smoothed")
    ax.scatter(centers, entropy, s=18, color="0.25", label="log bin count")
    ax.fill_between(
        centers,
        np.nanmin(entropy_smooth) - 0.15,
        np.nanmax(entropy_smooth) + 0.15,
        where=mask,
        color="C3",
        alpha=0.16,
        label="convex window",
    )
    ax.set_xlabel("energy")
    ax.set_ylabel("S(E)")
    ax.set_title("Attractive Bose-Hubbard DOS")
    ax.legend(frameon=False, fontsize=8)

    ax = axes[1]
    ax.plot(centers, beta, color="C1", label="beta")
    ax.plot(centers, curvature, color="C2", label="S''(E)")
    ax.axhline(0.0, color="0.3", linewidth=0.8)
    ax.fill_between(centers, ax.get_ylim()[0], ax.get_ylim()[1], where=mask, color="C3", alpha=0.12)
    ax.set_xlabel("energy")
    ax.set_title("Positive beta and convexity")
    ax.legend(frameon=False, fontsize=8)

    focus = summarize_bh_focus(args.bose_focus)[:6]
    labels = [bh_label(item[2]) for item in focus][::-1]
    pass_counts = [item[0] for item in focus][::-1]
    mean_bins = [item[1] for item in focus][::-1]

    ax = axes[2]
    y = np.arange(len(labels))
    ax.barh(y, pass_counts, color="C0", alpha=0.75, label="bin choices passed")
    ax.plot(mean_bins, y, "o", color="C3", label="mean convex bins")
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlim(0, 8)
    ax.set_xlabel("count out of 8")
    ax.set_title("Focused robustness scan")
    ax.legend(frameon=False, fontsize=8, loc="lower right")

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
