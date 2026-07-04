r"""Microcanonical collision Hamiltonian for shell erosion.

This script converts the structured shell erosion channel into an explicit
collision Hamiltonian:

    H = g (V + V^\dagger),

where V maps the shell Hilbert space into hard radiation plus a minimal soft
record. The hard-bin weights are not chosen thermally; they are computed from
the microcanonical entropy ratio and 2D bath phase space.

For one complete collision pulse, theta = pi/2, the input shell is fully
transferred to hard+soft radiation. At short time, the same Hamiltonian gives
branch probabilities proportional to the microcanonical weights.
"""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from statistics import mean, pstdev

import numpy as np
from scipy.linalg import expm

from erosion_channel_diagnostic import haar_state, reduced_density, trace_distance_to_diag


def entropy_of_mass(mass: float, q: int, sigma: float) -> float:
    if mass <= 0:
        return 0.0
    return (mass / (4.0 * sigma)) ** 2 * math.log(q)


def beta_continuum(L: int, q: int, sigma: float) -> float:
    mass = 4.0 * sigma * L
    return mass * math.log(q) / (8.0 * sigma**2)


def microcanonical_hard_distribution(
    L: int,
    q: int,
    sigma: float,
    d_hard: int,
    bath_dim: int,
    bin_width: float,
    n_grid: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return hard-bin probabilities and mean x=beta*omega in each bin."""
    mass = 4.0 * sigma * L
    beta = beta_continuum(L, q, sigma)
    s0 = entropy_of_mass(mass, q, sigma)
    weights: list[float] = []
    mean_x: list[float] = []
    for h in range(d_hard):
        x0 = h * bin_width
        x1 = (h + 1) * bin_width
        x = np.linspace(x0, x1, n_grid)
        omega = x / beta
        entropy_weight = np.array([math.exp(entropy_of_mass(mass - w, q, sigma) - s0) for w in omega])
        density_weight = x**bath_dim
        integrand = density_weight * entropy_weight
        weight = float(np.trapezoid(integrand, x))
        first = float(np.trapezoid(x * integrand, x))
        weights.append(weight)
        mean_x.append(first / weight if weight > 0 else 0.0)
    probs = np.array(weights, dtype=float)
    probs = probs / probs.sum()
    return probs, np.array(mean_x, dtype=float)


def entropy_subsystem(state: np.ndarray, dims: list[int], keep: list[int]) -> float:
    keep = list(keep)
    trace = [i for i in range(len(dims)) if i not in keep]
    d_keep = int(np.prod([dims[i] for i in keep], dtype=np.int64))
    d_trace = int(np.prod([dims[i] for i in trace], dtype=np.int64))
    if d_trace < d_keep:
        keep, trace = trace, keep
        d_keep, d_trace = d_trace, d_keep
    perm = keep + trace
    psi = np.transpose(state.reshape(dims), perm).reshape(d_keep, d_trace)
    rho = psi @ psi.conj().T
    vals = np.linalg.eigvalsh(rho)
    vals = vals[vals > 1e-14]
    return float(-np.sum(vals * np.log(vals)))


def mutual_information(state: np.ndarray, dims: list[int], axes_a: list[int], axes_b: list[int]) -> float:
    return (
        entropy_subsystem(state, dims, axes_a)
        + entropy_subsystem(state, dims, axes_b)
        - entropy_subsystem(state, dims, axes_a + axes_b)
    )


def shell_dims_for_L0(L0: int, q: int) -> list[int]:
    return [q] + [q ** (2 * L - 1) for L in range(2, L0 + 1)]


def collision_output_flat(flat: np.ndarray, probs: np.ndarray, model: str) -> np.ndarray:
    d_shell = flat.shape[1]
    d_hard = len(probs)
    out = np.zeros((flat.shape[0], d_hard, d_shell), dtype=complex)
    if model == "shift":
        for h, p in enumerate(probs):
            out[:, h, :] = math.sqrt(float(p)) * np.roll(flat, shift=h, axis=1)
    elif model == "clock":
        labels = np.arange(d_shell)
        for h, p in enumerate(probs):
            phases = np.exp(2j * np.pi * h * labels / d_shell)
            out[:, h, :] = math.sqrt(float(p)) * flat * phases
    else:
        raise ValueError(model)
    return out


def apply_full_collision_pulse(
    state: np.ndarray,
    dims: list[int],
    shell_axis: int,
    probs: np.ndarray,
    model: str,
) -> tuple[np.ndarray, list[int], int, int]:
    """Apply theta=pi/2 evolution under H=g(V+V^dagger), dropping input shell."""
    d_shell = dims[shell_axis]
    tensor = np.moveaxis(state.reshape(dims), shell_axis, -1)
    rest_shape = tensor.shape[:-1]
    flat = tensor.reshape(-1, d_shell)
    out = -1j * collision_output_flat(flat, probs, model)
    out = out.reshape(rest_shape + (len(probs), d_shell))
    new_dims = dims[:shell_axis] + dims[shell_axis + 1 :] + [len(probs), d_shell]
    return out.reshape(-1), new_dims, len(new_dims) - 2, len(new_dims) - 1


def verify_collision_hamiltonian(probs: np.ndarray, d_shell: int, model: str, theta: float) -> float:
    """Build a tiny explicit H and compare exp(-i theta H) with formula."""
    d_hard = len(probs)
    d_in = d_shell
    d_out = d_hard * d_shell
    dim = d_in + d_out
    v = np.zeros((d_out, d_in), dtype=complex)
    basis = np.eye(d_shell, dtype=complex)
    out = collision_output_flat(basis, probs, model)
    for a in range(d_shell):
        v[:, a] = out[a].reshape(-1)
    h = np.zeros((dim, dim), dtype=complex)
    h[d_in:, :d_in] = v
    h[:d_in, d_in:] = v.conj().T
    u = expm(-1j * theta * h)
    psi = haar_state(d_in, np.random.default_rng(1234))
    initial = np.zeros(dim, dtype=complex)
    initial[:d_in] = psi
    evolved = u @ initial
    expected = np.zeros(dim, dtype=complex)
    expected[:d_in] = math.cos(theta) * psi
    expected[d_in:] = -1j * math.sin(theta) * (v @ psi)
    return float(np.linalg.norm(evolved - expected))


def run_model(
    L0: int,
    q: int,
    sigma: float,
    d_hard: int,
    bath_dim: int,
    bin_width: float,
    model: str,
    seed: int,
) -> list[dict[str, float | int | str]]:
    rng = np.random.default_rng(seed)
    dims = shell_dims_for_L0(L0, q)
    state = haar_state(int(np.prod(dims, dtype=np.int64)), rng)
    hard_axes: list[int] = []
    soft_axes: list[int] = []
    rows: list[dict[str, float | int | str]] = []

    for L in range(L0, 1, -1):
        shell_axis = L - 1
        probs, mean_x = microcanonical_hard_distribution(
            L, q, sigma, d_hard, bath_dim, bin_width, n_grid=801
        )
        state, dims, hard_axis, soft_axis = apply_full_collision_pulse(state, dims, shell_axis, probs, model)
        hard_axes = [axis - 1 if axis > shell_axis else axis for axis in hard_axes]
        soft_axes = [axis - 1 if axis > shell_axis else axis for axis in soft_axes]
        hard_axes.append(hard_axis)
        soft_axes.append(soft_axis)

        latest_hard_rho = reduced_density(state, dims, [hard_axis])
        hard_trace_dist = trace_distance_to_diag(latest_hard_rho, probs)
        core_axes = list(range(0, L - 1))
        row: dict[str, float | int | str] = {
            "L0": L0,
            "q": q,
            "sigma": sigma,
            "d_hard": d_hard,
            "bath_dim": bath_dim,
            "bin_width": bin_width,
            "model": model,
            "seed": seed,
            "after_erosion_L": L,
            "remaining_core_L": L - 1,
            "beta": beta_continuum(L, q, sigma),
            "hard_probs": ";".join(f"{p:.8g}" for p in probs),
            "mean_x": ";".join(f"{x:.8g}" for x in mean_x),
            "core_entropy": entropy_subsystem(state, dims, core_axes),
            "hard_entropy": entropy_subsystem(state, dims, hard_axes),
            "soft_entropy": entropy_subsystem(state, dims, soft_axes),
            "latest_hard_entropy": entropy_subsystem(state, dims, [hard_axis]),
            "target_hard_entropy": float(-np.sum(probs * np.log(probs + 1e-300))),
            "latest_hard_trace_distance": hard_trace_dist,
        }
        if len(hard_axes) >= 2:
            row["I_first_hard_last_hard"] = mutual_information(state, dims, [hard_axes[0]], [hard_axes[-1]])
            row["I_first_pair_last_pair"] = mutual_information(
                state, dims, [hard_axes[0], soft_axes[0]], [hard_axes[-1], soft_axes[-1]]
            )
        else:
            row["I_first_hard_last_hard"] = 0.0
            row["I_first_pair_last_pair"] = 0.0
        rows.append(row)
    return rows


def summarize(vals: list[float]) -> tuple[float, float]:
    return mean(vals), pstdev(vals)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L0", type=int, default=4)
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--sigma", type=float, default=1.0)
    parser.add_argument("--d-hard", type=int, default=4)
    parser.add_argument("--bath-dim", type=int, default=2)
    parser.add_argument("--bin-width", type=float, default=1.0)
    parser.add_argument("--seeds", type=int, default=8)
    parser.add_argument("--seed0", type=int, default=20260602)
    parser.add_argument("--out", type=Path, default=Path("sim/data/microcanonical_collision_hamiltonian.csv"))
    parser.add_argument(
        "--summary-out",
        type=Path,
        default=Path("sim/data/microcanonical_collision_hamiltonian_summary.csv"),
    )
    args = parser.parse_args()

    rows: list[dict[str, float | int | str]] = []
    for model in ["shift", "clock"]:
        for offset in range(args.seeds):
            rows.extend(
                run_model(
                    args.L0,
                    args.q,
                    args.sigma,
                    args.d_hard,
                    args.bath_dim,
                    args.bin_width,
                    model,
                    args.seed0 + offset,
                )
            )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    groups: dict[tuple[str, int], list[dict[str, float | int | str]]] = {}
    for row in rows:
        groups.setdefault((str(row["model"]), int(row["after_erosion_L"])), []).append(row)

    summary_rows: list[dict[str, float | int | str]] = []
    for (model, L), group in sorted(groups.items()):
        summary: dict[str, float | int | str] = {
            "model": model,
            "after_erosion_L": L,
            "n": len(group),
            "hard_probs": group[0]["hard_probs"],
            "mean_x": group[0]["mean_x"],
        }
        for key in [
            "latest_hard_trace_distance",
            "latest_hard_entropy",
            "target_hard_entropy",
            "I_first_hard_last_hard",
            "I_first_pair_last_pair",
        ]:
            vals = [float(row[key]) for row in group]
            m, s = summarize(vals)
            summary[f"{key}_mean"] = m
            summary[f"{key}_std"] = s
        summary_rows.append(summary)

    with args.summary_out.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    probs, _ = microcanonical_hard_distribution(
        args.L0, args.q, args.sigma, args.d_hard, args.bath_dim, args.bin_width, n_grid=801
    )
    ham_error = verify_collision_hamiltonian(probs, d_shell=args.q ** (2 * args.L0 - 1), model="shift", theta=0.37)

    print(f"wrote {args.out}")
    print(f"wrote {args.summary_out}")
    print(f"single-shell Hamiltonian formula error: {ham_error:.3e}")
    print("model L probs                         D_hard  S_h/target  I_hh    I_pair")
    for row in summary_rows:
        print(
            f"{row['model']:<5} {row['after_erosion_L']:>1} "
            f"{str(row['hard_probs'])[:29]:<29} "
            f"{row['latest_hard_trace_distance_mean']:7.4f} "
            f"{row['latest_hard_entropy_mean']:6.3f}/"
            f"{row['target_hard_entropy_mean']:.3f} "
            f"{row['I_first_hard_last_hard_mean']:7.4f} "
            f"{row['I_first_pair_last_pair_mean']:7.3f}"
        )


if __name__ == "__main__":
    main()
