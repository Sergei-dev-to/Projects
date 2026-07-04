#!/usr/bin/env python3
"""Integrated boundary-tension droplet evaporator.

One effective model combines:

  * area entropy and perimeter energy;
  * local Hamiltonian-like scrambling on droplet qubits;
  * shell factorization H_L = H_{L-1} tensor H_shell(L);
  * shell-as-radiation output with hard energy bins as a coarse-graining;
  * Page and early/late radiation diagnostics.

The state vector dimension is fixed at q^(L0^2).  For q=2 and L0=4 this is
65536, which is small enough for exact state-vector diagnostics.
"""
from __future__ import annotations

import argparse
import csv
import pathlib

import numpy as np
from numpy.typing import NDArray

from scan_bose_hubbard_dos import DATADIR
from sector_hamiltonian_evaporator import target_x_distribution
from shell_radiation_isometry import (
    entropy_from_probs,
    hard_tv,
    integer_bin_dims,
    page_entropy_approx,
    reduced_entropy,
    shell_bin_probability,
)


def parse_list(value: str, kind):
    return [kind(part.strip()) for part in value.split(",") if part.strip()]


def random_unitary(dim: int, rng: np.random.Generator) -> NDArray[np.complex128]:
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    qmat, rmat = np.linalg.qr(raw)
    phases = np.diag(rmat)
    phases = phases / np.maximum(np.abs(phases), 1e-300)
    return qmat * phases.conj()[None, :]


def apply_two_qubit_gate(
    psi: NDArray[np.complex128],
    dims: list[int],
    axis_a: int,
    axis_b: int,
    gate: NDArray[np.complex128],
) -> NDArray[np.complex128]:
    if dims[axis_a] != 2 or dims[axis_b] != 2:
        raise ValueError("two-qubit gate requires qubit axes")
    if axis_a == axis_b:
        return psi
    axes = [axis_a, axis_b] + [idx for idx in range(len(dims)) if idx not in {axis_a, axis_b}]
    inverse = np.argsort(axes)
    tensor = psi.reshape(dims)
    moved = np.transpose(tensor, axes)
    rest_dim = int(np.prod([dims[idx] for idx in axes[2:]], dtype=np.int64))
    matrix = moved.reshape((4, rest_dim))
    updated = gate @ matrix
    restored = updated.reshape([2, 2] + [dims[idx] for idx in axes[2:]])
    return np.transpose(restored, inverse).reshape(-1)


def grid_pairs(L: int, layer: int) -> list[tuple[int, int]]:
    pairs = []
    for y in range(L):
        offset = (layer + y) % 2
        for x in range(offset, L - 1, 2):
            pairs.append((y * L + x, y * L + x + 1))
    for x in range(L):
        offset = (layer + x) % 2
        for y in range(offset, L - 1, 2):
            pairs.append((y * L + x, (y + 1) * L + x))
    return pairs


def expander_pairs(n_qubits: int, layer: int) -> list[tuple[int, int]]:
    if n_qubits <= 1:
        return []
    used = set()
    pairs = []
    multiplier = 3 + 2 * (layer % 3)
    for i in range(n_qubits):
        if i in used:
            continue
        j = (multiplier * i + 1 + layer) % n_qubits
        if j == i or j in used:
            continue
        used.add(i)
        used.add(j)
        pairs.append((i, j))
    return pairs


def random_pairs(n_qubits: int, rng: np.random.Generator) -> list[tuple[int, int]]:
    order = list(rng.permutation(n_qubits))
    return [(int(order[i]), int(order[i + 1])) for i in range(0, len(order) - 1, 2)]


def scramble_core(
    psi: NDArray[np.complex128],
    dims: list[int],
    core_qubits: int,
    L: int,
    scrambler: str,
    depth: int,
    rng: np.random.Generator,
) -> NDArray[np.complex128]:
    if scrambler == "none" or core_qubits <= 1:
        return psi
    for layer in range(depth):
        if scrambler == "grid":
            pairs = grid_pairs(L, layer)
        elif scrambler == "expander":
            pairs = expander_pairs(core_qubits, layer)
        elif scrambler == "random":
            pairs = random_pairs(core_qubits, rng)
        else:
            raise ValueError(f"unknown scrambler: {scrambler}")
        for a, b in pairs:
            gate = random_unitary(4, rng)
            psi = apply_two_qubit_gate(psi, dims, a, b, gate)
    norm = np.sqrt(float(np.vdot(psi, psi).real))
    return psi / max(norm, 1e-300)


def initial_state(kind: str, dim: int, rng: np.random.Generator) -> NDArray[np.complex128]:
    if kind == "basis":
        psi = np.zeros(dim, dtype=np.complex128)
        psi[0] = 1.0
        return psi
    if kind == "flat":
        psi = np.ones(dim, dtype=np.complex128)
        return psi / np.sqrt(float(dim))
    if kind == "haar":
        raw = rng.normal(size=dim) + 1j * rng.normal(size=dim)
        return raw / np.sqrt(float(np.vdot(raw, raw).real))
    raise ValueError(f"unknown initial state: {kind}")


def erode_shell(
    psi: NDArray[np.complex128],
    dims: list[int],
    core_qubits: int,
    L: int,
) -> tuple[NDArray[np.complex128], list[int], int]:
    inner_qubits = (L - 1) * (L - 1)
    shell_qubits = core_qubits - inner_qubits
    if shell_qubits != 2 * L - 1:
        raise ValueError("unexpected shell qubit count")
    tensor = psi.reshape(dims)
    shell_dim = 2**shell_qubits
    new_shape = [2] * inner_qubits + [shell_dim] + dims[core_qubits:]
    tensor = tensor.reshape(new_shape)
    axes = list(range(inner_qubits)) + list(range(inner_qubits + 1, tensor.ndim)) + [inner_qubits]
    tensor = np.transpose(tensor, axes)
    new_dims = [2] * inner_qubits + dims[core_qubits:] + [shell_dim]
    return tensor.reshape(-1), new_dims, shell_dim


def thermodynamic_row(L: int, q: int, sigma: float) -> dict[str, float | int]:
    area = L * L
    perimeter = 4 * L
    energy = sigma * perimeter
    entropy = area * np.log(q)
    temp = 2.0 * sigma / (L * np.log(q))
    heat = -2.0 * area * np.log(q)
    power = perimeter * temp**3
    return {
        "L": L,
        "area": area,
        "perimeter": perimeter,
        "energy": energy,
        "entropy": float(entropy),
        "temperature": float(temp),
        "heat_capacity": float(heat),
        "power_2d_proxy": float(power),
        "E2_power_proxy": float((energy**2) * power),
    }


def latest_shell_hard_probs(
    psi: NDArray[np.complex128],
    dims: list[int],
    latest_axis: int,
    bin_dims: list[int],
) -> NDArray[np.float64]:
    return shell_bin_probability(psi, dims, latest_axis, bin_dims)


def run_case(args: argparse.Namespace, state_kind: str, scrambler: str, seed: int):
    if args.q != 2:
        raise ValueError("integrated scrambling circuit currently supports q=2")
    rng = np.random.default_rng(seed)
    total_qubits = args.L0 * args.L0
    psi = initial_state(state_kind, 2**total_qubits, rng)
    dims = [2] * total_qubits
    core_qubits = total_qubits
    target_probs = target_x_distribution(np.asarray(args.x_edges, dtype=float), args.ohmic_power)
    rows = []
    thermo_rows = []

    for step, L in enumerate(range(args.L0, args.Lmin, -1), start=1):
        thermo_rows.append({"state": state_kind, "scrambler": scrambler, "seed": seed, **thermodynamic_row(L, args.q, args.sigma)})
        psi = scramble_core(psi, dims, core_qubits, L, scrambler, args.depth, rng)
        psi, dims, shell_dim = erode_shell(psi, dims, core_qubits, L)
        core_qubits = (L - 1) * (L - 1)
        latest_axis = len(dims) - 1
        bin_dims = integer_bin_dims(target_probs, shell_dim)
        actual_hard = latest_shell_hard_probs(psi, dims, latest_axis, bin_dims)
        rad_axes = list(range(core_qubits, len(dims)))
        early_axes = rad_axes[:-1]
        late_axes = [latest_axis]
        core_axes = list(range(core_qubits))

        core_dim = 2**core_qubits
        rad_dim = int(np.prod([dims[idx] for idx in rad_axes], dtype=np.int64))
        core_entropy = reduced_entropy(psi, dims, core_axes)
        rad_entropy = reduced_entropy(psi, dims, rad_axes)
        early_entropy = reduced_entropy(psi, dims, early_axes)
        late_entropy = reduced_entropy(psi, dims, late_axes)
        early_late_entropy = reduced_entropy(psi, dims, early_axes + late_axes)
        rows.append(
            {
                "state": state_kind,
                "scrambler": scrambler,
                "seed": seed,
                "depth": args.depth,
                "step": step,
                "L_removed": L,
                "core_qubits": core_qubits,
                "core_dim": core_dim,
                "latest_shell_dim": shell_dim,
                "radiation_dim": rad_dim,
                "log_core_dim": float(np.log(core_dim)) if core_dim > 0 else 0.0,
                "log_radiation_dim": float(np.log(rad_dim)) if rad_dim > 0 else 0.0,
                "core_entropy": core_entropy,
                "radiation_entropy": rad_entropy,
                "page_entropy_estimate": page_entropy_approx(core_dim, rad_dim),
                "latest_hard_tv": hard_tv(actual_hard, target_probs),
                "early_entropy": early_entropy,
                "late_entropy": late_entropy,
                "early_late_entropy": early_late_entropy,
                "early_late_mutual_information": early_entropy + late_entropy - early_late_entropy,
                "actual_latest_hard_probs": ";".join(f"{p:.8g}" for p in actual_hard),
                "latest_bin_dims": ";".join(str(dim) for dim in bin_dims),
            }
        )
    return rows, thermo_rows


def summarize(rows: list[dict[str, float | int | str]]) -> list[dict[str, float | int | str]]:
    grouped: dict[tuple[str, str, int], list[dict[str, float | int | str]]] = {}
    for row in rows:
        grouped.setdefault((str(row["state"]), str(row["scrambler"]), int(row["seed"])), []).append(row)
    out = []
    for (state, scrambler, seed), group in sorted(grouped.items()):
        final = max(group, key=lambda row: int(row["step"]))
        out.append(
            {
                "state": state,
                "scrambler": scrambler,
                "seed": seed,
                "steps": len(group),
                "depth": int(final["depth"]),
                "final_core_entropy": float(final["core_entropy"]),
                "final_radiation_entropy": float(final["radiation_entropy"]),
                "final_page_entropy_estimate": float(final["page_entropy_estimate"]),
                "mean_hard_tv": float(np.mean([float(row["latest_hard_tv"]) for row in group])),
                "max_early_late_mutual_information": float(
                    max(float(row["early_late_mutual_information"]) for row in group)
                ),
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
    parser = argparse.ArgumentParser(description="Run integrated droplet evaporator.")
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--L0", type=int, default=4)
    parser.add_argument("--Lmin", type=int, default=1)
    parser.add_argument("--states", default="basis,flat,haar")
    parser.add_argument("--scramblers", default="none,grid,expander,random")
    parser.add_argument("--depth", type=int, default=4)
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
        default=DATADIR / "integrated_droplet_evaporator_timeseries.csv",
    )
    parser.add_argument(
        "--thermo-csv",
        type=pathlib.Path,
        default=DATADIR / "integrated_droplet_evaporator_thermo.csv",
    )
    parser.add_argument(
        "--summary-csv",
        type=pathlib.Path,
        default=DATADIR / "integrated_droplet_evaporator_summary.csv",
    )
    args = parser.parse_args(argv)

    states = parse_list(args.states, str)
    scramblers = parse_list(args.scramblers, str)
    seeds = parse_list(args.seeds, int)
    all_rows = []
    all_thermo = []
    for seed in seeds:
        for state in states:
            for scrambler in scramblers:
                print(f"[integrated-droplet] seed={seed} state={state} scrambler={scrambler}", flush=True)
                rows, thermo = run_case(args, state, scrambler, seed)
                all_rows.extend(rows)
                all_thermo.extend(thermo)
    summary = summarize(all_rows)
    write_csv(args.timeseries_csv, all_rows)
    write_csv(args.thermo_csv, all_thermo)
    write_csv(args.summary_csv, summary)
    print(f"[integrated-droplet] wrote {args.timeseries_csv}")
    print(f"[integrated-droplet] wrote {args.thermo_csv}")
    print(f"[integrated-droplet] wrote {args.summary_csv}")
    print("state  scrambler  seed  Srad_final  Page_est  hardTV  max I(E:L)")
    for row in summary:
        print(
            f"{str(row['state']):6s} "
            f"{str(row['scrambler']):9s} "
            f"{int(row['seed']):4d} "
            f"{float(row['final_radiation_entropy']):10.3f} "
            f"{float(row['final_page_entropy_estimate']):8.3f} "
            f"{float(row['mean_hard_tv']):7.3f} "
            f"{float(row['max_early_late_mutual_information']):10.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
