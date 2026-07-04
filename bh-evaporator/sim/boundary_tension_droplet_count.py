#!/usr/bin/env python3
"""Boundary-tension droplet equation-of-state kill test.

Model:

  * A droplet is a connected set of occupied cells on the square lattice.
  * Energy is boundary tension: E = sigma * perimeter.
  * Each occupied cell carries q soft internal labels.

For all fixed polyominoes up to a chosen area, this script counts shapes by
area and perimeter and computes the microcanonical entropy at fixed perimeter:

    S(P) = log sum_A N_shapes(A,P) q^A.

The target is to see whether S(P) is approximately quadratic in P, since
E proportional to P would then give S(E) proportional to E^2.
"""
from __future__ import annotations

import argparse
import csv
import math
import pathlib
from collections import defaultdict

import numpy as np

from scan_bose_hubbard_dos import DATADIR


Cell = tuple[int, int]
Shape = frozenset[Cell]


def normalize(cells: set[Cell] | Shape) -> Shape:
    min_x = min(x for x, _y in cells)
    min_y = min(y for _x, y in cells)
    return frozenset((x - min_x, y - min_y) for x, y in cells)


def neighbors(cell: Cell) -> tuple[Cell, Cell, Cell, Cell]:
    x, y = cell
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def perimeter(shape: Shape) -> int:
    occupied = set(shape)
    total = 0
    for cell in occupied:
        total += sum(1 for nb in neighbors(cell) if nb not in occupied)
    return total


def enumerate_fixed_polyominoes(max_area: int) -> dict[int, set[Shape]]:
    shapes: dict[int, set[Shape]] = {1: {frozenset({(0, 0)})}}
    for area in range(2, max_area + 1):
        current: set[Shape] = set()
        for shape in shapes[area - 1]:
            boundary = set()
            for cell in shape:
                for nb in neighbors(cell):
                    if nb not in shape:
                        boundary.add(nb)
            for nb in boundary:
                current.add(normalize(set(shape) | {nb}))
        shapes[area] = current
    return shapes


def rectangle_rows(max_side: int, q: int, sigma: float) -> list[dict[str, float | int | str]]:
    rows = []
    best_by_p: dict[int, tuple[int, int, int]] = {}
    for a in range(1, max_side + 1):
        for b in range(1, max_side + 1):
            area = a * b
            p = 2 * (a + b)
            if p not in best_by_p or area > best_by_p[p][0]:
                best_by_p[p] = (area, a, b)
    for p, (area, a, b) in sorted(best_by_p.items()):
        entropy = area * math.log(q) if q > 1 else 0.0
        rows.append(
            {
                "family": "best_rectangle",
                "perimeter": p,
                "energy": sigma * p,
                "area": area,
                "side_a": a,
                "side_b": b,
                "entropy": entropy,
                "entropy_over_p2": entropy / (p * p),
                "entropy_over_e2": entropy / ((sigma * p) ** 2),
            }
        )
    return rows


def summarize_polyominoes(shapes: dict[int, set[Shape]], q: int, sigma: float):
    max_enum_area = max(shapes)
    shape_counts: dict[tuple[int, int], int] = defaultdict(int)
    for area, area_shapes in shapes.items():
        for shape in area_shapes:
            shape_counts[(area, perimeter(shape))] += 1

    by_p: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for (area, p), count in shape_counts.items():
        by_p[p].append((area, count))

    rows = []
    for p, entries in sorted(by_p.items()):
        weights = []
        for area, count in entries:
            if q > 1:
                log_weight = math.log(count) + area * math.log(q)
            else:
                log_weight = math.log(count)
            weights.append((area, count, log_weight))
        max_log = max(logw for _area, _count, logw in weights)
        log_total = max_log + math.log(sum(math.exp(logw - max_log) for _area, _count, logw in weights))
        max_area = max(area for area, _count, _logw in weights)
        dominant_area, dominant_count, dominant_logw = max(weights, key=lambda item: item[2])
        shape_only_entropy = math.log(sum(count for _area, count, _logw in weights))
        rows.append(
            {
                "perimeter": p,
                "energy": sigma * p,
                "entropy": log_total,
                "shape_only_entropy": shape_only_entropy,
                "max_area": max_area,
                "dominant_area": dominant_area,
                "dominant_shape_count": dominant_count,
                "dominant_fraction": math.exp(dominant_logw - log_total),
                "area_bound_square": (p * p) / 16.0,
                "complete_under_max_area": (p * p) / 16.0 <= max_enum_area,
                "entropy_over_p2": log_total / (p * p),
                "entropy_over_e2": log_total / ((sigma * p) ** 2),
                "shape_entropy_over_p2": shape_only_entropy / (p * p),
            }
        )
    return rows, shape_counts


def fit_quadratic(
    rows: list[dict[str, float | int | bool | str]],
    min_p: int,
    require_complete: bool = False,
) -> dict[str, float]:
    valid = [
        row
        for row in rows
        if int(row["perimeter"]) >= min_p
        and float(row["entropy"]) > 0.0
        and (not require_complete or bool(row.get("complete_under_max_area", True)))
    ]
    x = np.asarray([float(row["perimeter"]) ** 2 for row in valid], dtype=float)
    y = np.asarray([float(row["entropy"]) for row in valid], dtype=float)
    if len(x) < 2:
        return {
            "fit_min_perimeter": min_p,
            "require_complete": float(require_complete),
            "rows": float(len(x)),
            "slope_S_vs_P2": float("nan"),
            "intercept": float("nan"),
            "r2": float("nan"),
        }
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    r2 = 1.0 - ss_res / max(ss_tot, 1e-300)
    return {
        "fit_min_perimeter": min_p,
        "require_complete": float(require_complete),
        "rows": float(len(x)),
        "slope_S_vs_P2": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
    }


def thermodynamic_rows(rows: list[dict[str, float | int]], sigma: float):
    ordered = sorted(rows, key=lambda row: int(row["perimeter"]))
    out = []
    for idx, row in enumerate(ordered):
        p = int(row["perimeter"])
        energy = sigma * p
        entropy = float(row["entropy"])
        if idx == 0:
            temp = float("nan")
            heat = float("nan")
        else:
            prev = ordered[idx - 1]
            d_e = energy - float(prev["energy"])
            d_s = entropy - float(prev["entropy"])
            temp = d_e / d_s if d_s > 0.0 else float("nan")
            if idx >= 2:
                prev_temp = out[-1]["temperature"]
                d_t = temp - float(prev_temp)
                heat = d_e / d_t if abs(d_t) > 1e-300 else float("inf")
            else:
                heat = float("nan")
        out.append(
            {
                **row,
                "temperature": temp,
                "heat_capacity": heat,
                "power_2d_proxy": p * temp**3 if np.isfinite(temp) else float("nan"),
                "E2_power_proxy": (energy**2) * p * temp**3 if np.isfinite(temp) else float("nan"),
            }
        )
    return out


def write_csv(path: pathlib.Path, rows: list[dict[str, float | int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count boundary-tension lattice droplets.")
    parser.add_argument("--max-area", type=int, default=12)
    parser.add_argument("--q-list", default="1,2,4")
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--fit-min-perimeter", type=int, default=14)
    parser.add_argument("--complete-fit-min-perimeter", type=int, default=8)
    parser.add_argument("--rectangle-max-side", type=int, default=40)
    parser.add_argument(
        "--polyomino-csv",
        type=pathlib.Path,
        default=DATADIR / "boundary_tension_polyomino_entropy.csv",
    )
    parser.add_argument(
        "--thermo-csv",
        type=pathlib.Path,
        default=DATADIR / "boundary_tension_polyomino_thermo.csv",
    )
    parser.add_argument(
        "--rectangle-csv",
        type=pathlib.Path,
        default=DATADIR / "boundary_tension_rectangle_entropy.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "boundary_tension_droplet_summary.csv",
    )
    args = parser.parse_args(argv)

    q_values = [int(part.strip()) for part in args.q_list.split(",") if part.strip()]
    print(f"[droplet] enumerating fixed polyominoes up to area {args.max_area}", flush=True)
    shapes = enumerate_fixed_polyominoes(args.max_area)
    for area in sorted(shapes):
        print(f"[droplet] area={area} shapes={len(shapes[area])}", flush=True)

    all_entropy_rows = []
    all_thermo_rows = []
    all_rectangle_rows = []
    summary_rows = []
    total_shapes = sum(len(v) for v in shapes.values())
    for q in q_values:
        entropy_rows, _shape_counts = summarize_polyominoes(shapes, q, args.sigma)
        thermo_rows = thermodynamic_rows(entropy_rows, args.sigma)
        rectangle = rectangle_rows(args.rectangle_max_side, q, args.sigma)
        fit = fit_quadratic(entropy_rows, args.fit_min_perimeter)
        complete_fit = fit_quadratic(
            entropy_rows,
            args.complete_fit_min_perimeter,
            require_complete=True,
        )
        rect_fit = fit_quadratic(rectangle, min_p=2 * args.fit_min_perimeter)
        for row in entropy_rows:
            all_entropy_rows.append({"q": q, **row})
        for row in thermo_rows:
            all_thermo_rows.append({"q": q, **row})
        for row in rectangle:
            all_rectangle_rows.append({"q": q, **row})

        large = [row for row in entropy_rows if int(row["perimeter"]) >= args.fit_min_perimeter]
        mean_entropy_over_p2 = float(np.mean([float(row["entropy_over_p2"]) for row in large]))
        mean_shape_over_p2 = float(np.mean([float(row["shape_entropy_over_p2"]) for row in large]))
        expected_compact_coeff = math.log(q) / 16.0 if q > 1 else 0.0
        summary_rows.append(
            {
                "q": q,
                "max_area": args.max_area,
                "total_shapes": total_shapes,
                "fit_min_perimeter": args.fit_min_perimeter,
                "polyomino_slope_S_vs_P2": fit["slope_S_vs_P2"],
                "polyomino_r2": fit["r2"],
                "complete_polyomino_rows": complete_fit["rows"],
                "complete_polyomino_slope_S_vs_P2": complete_fit["slope_S_vs_P2"],
                "complete_polyomino_r2": complete_fit["r2"],
                "rectangle_slope_S_vs_P2": rect_fit["slope_S_vs_P2"],
                "rectangle_r2": rect_fit["r2"],
                "expected_compact_logq_over_16": expected_compact_coeff,
                "mean_entropy_over_p2_large": mean_entropy_over_p2,
                "mean_shape_entropy_over_p2_large": mean_shape_over_p2,
                "mean_dominant_fraction_large": float(np.mean([float(row["dominant_fraction"]) for row in large])),
                "mean_dominant_area_over_bound_large": float(
                    np.mean([float(row["dominant_area"]) / float(row["area_bound_square"]) for row in large])
                ),
            }
        )

    write_csv(args.polyomino_csv, all_entropy_rows)
    write_csv(args.thermo_csv, all_thermo_rows)
    write_csv(args.rectangle_csv, all_rectangle_rows)
    write_csv(args.summary_csv, summary_rows)
    print(f"[droplet] wrote {args.polyomino_csv}")
    print(f"[droplet] wrote {args.thermo_csv}")
    print(f"[droplet] wrote {args.rectangle_csv}")
    print(f"[droplet] wrote {args.summary_csv}")
    print("q  slope(all)  slope(complete)  rows  slope(rect)  expected  dom_frac  area/bound")
    for row in summary_rows:
        print(
            f"{row['q']:1d} "
            f"{row['polyomino_slope_S_vs_P2']:10.4f} "
            f"{row['complete_polyomino_slope_S_vs_P2']:15.4f} "
            f"{row['complete_polyomino_rows']:4.0f} "
            f"{row['rectangle_slope_S_vs_P2']:11.4f} "
            f"{row['expected_compact_logq_over_16']:9.4f} "
            f"{row['mean_dominant_fraction_large']:9.3f} "
            f"{row['mean_dominant_area_over_bound_large']:10.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
