#!/usr/bin/env python3
"""Shell-to-radiation isometry diagnostic.

This implements the cleaner erosion model:

    H_L = H_{L-1} tensor H_shell(L)
    H_shell(L) -> R_out(L)

There is no separate soft register.  The outgoing shell radiation has energy
bins as a coarse-graining; the fine-grained state within and across those bins
carries the purification information.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_evaporator import target_x_distribution


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def integer_bin_dims(probabilities: NDArray[np.float64], total_dim: int) -> list[int]:
    if total_dim < len(probabilities):
        raise ValueError("radiation dimension must be at least the number of hard bins")
    raw = probabilities * total_dim
    dims = [max(1, int(np.floor(value))) for value in raw]
    while sum(dims) > total_dim:
        candidates = [idx for idx, value in enumerate(dims) if value > 1]
        idx = min(candidates, key=lambda i: raw[i] - np.floor(raw[i]))
        dims[idx] -= 1
    while sum(dims) < total_dim:
        idx = max(range(len(dims)), key=lambda i: raw[i] - np.floor(raw[i]))
        dims[idx] += 1
    return dims


def random_state(dim: int, rng: np.random.Generator) -> NDArray[np.complex128]:
    raw = rng.normal(size=dim) + 1j * rng.normal(size=dim)
    return raw.astype(np.complex128) / np.sqrt(float(np.vdot(raw, raw).real))


def initial_state(kind: str, dim: int, rng: np.random.Generator) -> NDArray[np.complex128]:
    if kind == "haar":
        return random_state(dim, rng)
    if kind == "basis":
        psi = np.zeros(dim, dtype=np.complex128)
        psi[0] = 1.0
        return psi
    if kind == "flat_product":
        psi = np.ones(dim, dtype=np.complex128)
        return psi / np.sqrt(float(dim))
    raise ValueError(f"unknown initial state: {kind}")


def entropy_from_probs(vals: NDArray[np.float64]) -> float:
    vals = vals[vals > 1e-14]
    if len(vals) == 0:
        return 0.0
    return -float(np.sum(vals * np.log(vals)))


def reduced_entropy(psi: NDArray[np.complex128], dims: list[int], keep_axes: list[int]) -> float:
    if not keep_axes:
        return 0.0
    keep = list(keep_axes)
    trace = [idx for idx in range(len(dims)) if idx not in keep]
    tensor = psi.reshape(dims)
    permuted = np.transpose(tensor, keep + trace)
    keep_dim = int(np.prod([dims[idx] for idx in keep], dtype=np.int64))
    trace_dim = int(np.prod([dims[idx] for idx in trace], dtype=np.int64))
    matrix = permuted.reshape((keep_dim, trace_dim))
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    probs = np.maximum(singular_values.real, 0.0) ** 2
    total = float(np.sum(probs))
    if total > 0.0:
        probs /= total
    return entropy_from_probs(probs)


def shell_bin_probability(
    psi: NDArray[np.complex128],
    dims: list[int],
    shell_axis: int,
    bin_dims: list[int],
) -> NDArray[np.float64]:
    tensor = psi.reshape(dims)
    probs = np.sum(np.abs(tensor) ** 2, axis=tuple(idx for idx in range(len(dims)) if idx != shell_axis))
    out = []
    start = 0
    for width in bin_dims:
        out.append(float(np.sum(probs[start : start + width])))
        start += width
    return np.asarray(out, dtype=float)


def hard_tv(actual: NDArray[np.float64], target: NDArray[np.float64]) -> float:
    if float(np.sum(actual)) <= 0.0:
        return float("nan")
    actual = actual / float(np.sum(actual))
    return 0.5 * float(np.sum(np.abs(actual - target)))


def erode_one_shell(
    psi: NDArray[np.complex128],
    dims: list[int],
    current_L: int,
    q: int,
) -> tuple[NDArray[np.complex128], list[int]]:
    old_core_dim = dims[0]
    new_core_dim = q ** ((current_L - 1) * (current_L - 1))
    shell_dim = q ** (2 * current_L - 1)
    if old_core_dim != new_core_dim * shell_dim:
        raise ValueError("core dimension does not factor into inner core times shell")
    tensor = psi.reshape([old_core_dim] + dims[1:])
    tensor = tensor.reshape([new_core_dim, shell_dim] + dims[1:])
    tensor = np.transpose(tensor, [0] + list(range(2, tensor.ndim)) + [1])
    return tensor.reshape(-1), [new_core_dim] + dims[1:] + [shell_dim]


def page_entropy_approx(d_a: int, d_b: int) -> float:
    # Large-dimension Page estimate for the smaller side.
    d_min = min(d_a, d_b)
    d_max = max(d_a, d_b)
    if d_min <= 1:
        return 0.0
    return float(np.log(d_min) - d_min / (2.0 * d_max))


def run_case(args: argparse.Namespace, state_kind: str, seed: int):
    rng = np.random.default_rng(seed)
    target_probs = target_x_distribution(np.asarray(args.x_edges, dtype=float), args.ohmic_power)
    initial_dim = args.q ** (args.L0 * args.L0)
    psi = initial_state(state_kind, initial_dim, rng)
    dims = [initial_dim]
    emitted_shells: list[dict[str, object]] = []
    rows = []

    for step, current_L in enumerate(range(args.L0, args.Lmin, -1), start=1):
        psi, dims = erode_one_shell(psi, dims, current_L, args.q)
        shell_dim = dims[-1]
        bin_dims = integer_bin_dims(target_probs, shell_dim)
        emitted_shells.append({"L": current_L, "dim": shell_dim, "bin_dims": bin_dims})

        core_axis = [0]
        rad_axes = list(range(1, len(dims)))
        latest_axis = len(dims) - 1
        early_axes = rad_axes[:-1]
        late_axes = [latest_axis]
        all_rad_entropy = reduced_entropy(psi, dims, rad_axes)
        core_entropy = reduced_entropy(psi, dims, core_axis)
        early_entropy = reduced_entropy(psi, dims, early_axes)
        late_entropy = reduced_entropy(psi, dims, late_axes)
        early_late_entropy = reduced_entropy(psi, dims, early_axes + late_axes)
        early_late_mi = early_entropy + late_entropy - early_late_entropy
        actual_hard = shell_bin_probability(psi, dims, latest_axis, bin_dims)
        tv = hard_tv(actual_hard, target_probs)

        core_dim = dims[0]
        rad_dim = int(np.prod(rad_axes and [dims[idx] for idx in rad_axes] or [1], dtype=np.int64))
        rows.append(
            {
                "state": state_kind,
                "seed": seed,
                "step": step,
                "L_removed": current_L,
                "core_dim": core_dim,
                "latest_shell_dim": shell_dim,
                "radiation_dim": rad_dim,
                "log_core_dim": float(np.log(core_dim)),
                "log_radiation_dim": float(np.log(rad_dim)),
                "core_entropy": core_entropy,
                "radiation_entropy": all_rad_entropy,
                "page_entropy_estimate": page_entropy_approx(core_dim, rad_dim),
                "latest_hard_tv": tv,
                "early_entropy": early_entropy,
                "late_entropy": late_entropy,
                "early_late_entropy": early_late_entropy,
                "early_late_mutual_information": early_late_mi,
                "target_probs": ";".join(f"{p:.8g}" for p in target_probs),
                "actual_latest_hard_probs": ";".join(f"{p:.8g}" for p in actual_hard),
                "latest_bin_dims": ";".join(str(dim) for dim in bin_dims),
            }
        )
    return rows


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | int | str]]:
    out = []
    grouped: dict[tuple[str, int], list[dict[str, float | int | str]]] = {}
    for row in rows:
        grouped.setdefault((str(row["state"]), int(row["seed"])), []).append(row)
    for (state, seed), group in sorted(grouped.items()):
        final = max(group, key=lambda row: int(row["step"]))
        max_mi = max(float(row["early_late_mutual_information"]) for row in group)
        mean_tv = float(np.mean([float(row["latest_hard_tv"]) for row in group]))
        out.append(
            {
                "state": state,
                "seed": seed,
                "steps": len(group),
                "final_core_dim": int(final["core_dim"]),
                "final_radiation_dim": int(final["radiation_dim"]),
                "final_core_entropy": float(final["core_entropy"]),
                "final_radiation_entropy": float(final["radiation_entropy"]),
                "final_page_entropy_estimate": float(final["page_entropy_estimate"]),
                "mean_latest_hard_tv": mean_tv,
                "max_early_late_mutual_information": max_mi,
                "final_early_late_mutual_information": float(final["early_late_mutual_information"]),
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
    parser = argparse.ArgumentParser(description="Run shell-to-radiation isometry diagnostic.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--L0", type=int, default=4)
    parser.add_argument("--Lmin", type=int, default=1)
    parser.add_argument("--states", default="haar,basis,flat_product")
    parser.add_argument("--seeds", default="2468,2469")
    parser.add_argument("--ohmic-power", type=float, default=1.0)
    parser.add_argument(
        "--x-edges",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, float("inf")],
    )
    parser.add_argument(
        "--timeseries-csv",
        type=pathlib.Path,
        default=DATADIR / "shell_radiation_isometry_timeseries.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "shell_radiation_isometry_summary.csv",
    )
    args = parser.parse_args(argv)

    states = parse_list(args.states, str)
    seeds = parse_list(args.seeds, int)
    rows = []
    for seed in seeds:
        for state in states:
            print(f"[shell-rad] state={state} seed={seed}", flush=True)
            rows.extend(run_case(args, state, seed))
    summary = summarize(rows)
    write_csv(args.timeseries_csv, rows)
    write_csv(args.summary_csv, summary)
    print(f"[shell-rad] wrote {args.timeseries_csv}")
    print(f"[shell-rad] wrote {args.summary_csv}")
    print("state         seed  Srad_final  Page_est  hardTV  max I(E:L)")
    for row in summary:
        print(
            f"{str(row['state']):12s} "
            f"{int(row['seed']):4d} "
            f"{float(row['final_radiation_entropy']):10.3f} "
            f"{float(row['final_page_entropy_estimate']):8.3f} "
            f"{float(row['mean_latest_hard_tv']):7.3f} "
            f"{float(row['max_early_late_mutual_information']):10.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
