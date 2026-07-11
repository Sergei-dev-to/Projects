"""Shrinking-shell blind/weak/mixing diary-channel comparison.

The shell dimensions obey d_j = 2**(L-j). Energies are chosen so that
S(E)=a E**2 (up to a fixed residual entropy), and each shell transition has
the exact density-of-states ratio exp(-beta_j omega_j)=1/2.

Every branch emits the same independent thermal Hawking energy qubit. The
logical degeneracy qubit removed by the shrinking shell is routed either to an
inaccessible partner archive (blind), through a flagged erasure channel
(weak), or to the exterior record (mixing). Random shell unitaries scramble a
small diary before each split. The script measures reference--hidden-system
decoupling and reference--radiation mutual information.

NumPy only. This is a finite information-flow control, not an autonomous
Hamiltonian black-hole model.
"""

from __future__ import annotations

import argparse
import itertools

import numpy as np


def random_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r).copy()
    phases /= np.maximum(np.abs(phases), 1e-300)
    return q * phases.conj()[None, :]


def initial_diary_state(shell_qubits: int, diary_qubits: int) -> np.ndarray:
    d_q = 2**diary_qubits
    d_b = 2**shell_qubits
    d_background = d_b // d_q
    state = np.zeros((d_q, d_b), dtype=np.complex128)
    for label in range(d_q):
        state[label, label * d_background] = 1.0 / np.sqrt(d_q)
    return state


def scramble_and_split(state: np.ndarray, unitary: np.ndarray) -> np.ndarray:
    """Act on the remaining shell (axis 1), split one qubit, append it."""
    state = np.moveaxis(state, 1, -1)
    state = state @ unitary.T
    state = np.moveaxis(state, -1, 1)
    old_dim = state.shape[1]
    state = state.reshape(state.shape[0], old_dim // 2, 2, *state.shape[2:])
    return np.moveaxis(state, 2, -1)


def entropy_from_probabilities(probabilities: np.ndarray) -> float:
    probabilities = probabilities[probabilities > 1e-14]
    return float(-np.sum(probabilities * np.log(probabilities)))


def trace_norm_hermitian(matrix: np.ndarray) -> float:
    matrix = 0.5 * (matrix + matrix.conj().T)
    return float(np.sum(np.abs(np.linalg.eigvalsh(matrix))))


def partition_metrics(state: np.ndarray, accessible: tuple[bool, ...]) -> tuple[float, float]:
    """Return ||rho_QH-rho_Q tensor rho_H||_1 and I(Q:R)."""
    d_q = state.shape[0]
    emitted_axes = list(range(2, state.ndim))
    hidden_axes = [1] + [axis for axis, keep in zip(emitted_axes, accessible) if not keep]
    record_axes = [axis for axis, keep in zip(emitted_axes, accessible) if keep]
    permutation = [0] + hidden_axes + record_axes
    psi = np.transpose(state, permutation)
    d_h = int(np.prod([state.shape[axis] for axis in hidden_axes], dtype=int))
    d_r = int(np.prod([state.shape[axis] for axis in record_axes], dtype=int))
    matrix_qh_r = psi.reshape(d_q * d_h, d_r)
    rho_qh = matrix_qh_r @ matrix_qh_r.conj().T
    rho4 = rho_qh.reshape(d_q, d_h, d_q, d_h)
    rho_q = np.trace(rho4, axis1=1, axis2=3)
    rho_h = np.trace(rho4, axis1=0, axis2=2)
    decoupling = trace_norm_hermitian(rho_qh - np.kron(rho_q, rho_h))

    schmidt_r = np.linalg.svd(matrix_qh_r, compute_uv=False) ** 2
    s_r = entropy_from_probabilities(schmidt_r)
    psi_h_qr = np.transpose(state, hidden_axes + [0] + record_axes).reshape(
        d_h, d_q * d_r
    )
    schmidt_h = np.linalg.svd(psi_h_qr, compute_uv=False) ** 2
    s_h = entropy_from_probabilities(schmidt_h)
    s_q = entropy_from_probabilities(np.linalg.eigvalsh(rho_q).real)
    mutual_information = s_q + s_r - s_h
    return decoupling, float(mutual_information)


def erasure_average_metrics(state: np.ndarray, access_probability: float) -> tuple[float, float]:
    depth = state.ndim - 2
    decoupling = 0.0
    mutual_information = 0.0
    total_weight = 0.0
    for pattern in itertools.product((False, True), repeat=depth):
        kept = sum(pattern)
        weight = access_probability**kept * (1.0 - access_probability) ** (depth - kept)
        if weight == 0.0:
            continue
        dec, mutual = partition_metrics(state, pattern)
        decoupling += weight * dec
        mutual_information += weight * mutual
        total_weight += weight
    if abs(total_weight - 1.0) > 2e-12:
        raise AssertionError("erasure-pattern probabilities did not normalize")
    return decoupling, mutual_information


def shell_thermodynamics(shell_qubits: int, residual_entropy: float, alpha: float):
    remaining = np.arange(shell_qubits, -1, -1, dtype=float)
    entropy = residual_entropy + remaining * np.log(2.0)
    energy = np.sqrt(entropy / alpha)
    omega = energy[:-1] - energy[1:]
    beta = (entropy[:-1] - entropy[1:]) / omega
    return entropy, energy, beta, omega


def run_seed(
    shell_qubits: int,
    diary_qubits: int,
    access_probabilities: tuple[float, ...],
    seed: int,
):
    rng = np.random.default_rng(seed)
    state = initial_diary_state(shell_qubits, diary_qubits)
    rows = []
    for depth in range(shell_qubits + 1):
        for access_probability in access_probabilities:
            decoupling, mutual = erasure_average_metrics(state, access_probability)
            rows.append((depth, access_probability, decoupling, mutual))
        if depth < shell_qubits:
            state = scramble_and_split(state, random_unitary(state.shape[1], rng))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shell-qubits", type=int, default=6)
    parser.add_argument("--diary-qubits", type=int, default=1)
    parser.add_argument("--seeds", type=int, default=3)
    parser.add_argument("--seed", type=int, default=7319)
    parser.add_argument("--alpha", type=float, default=0.08)
    parser.add_argument(
        "--access",
        type=float,
        nargs="+",
        default=(0.0, 0.25, 0.75, 1.0),
    )
    args = parser.parse_args()
    if not 0 < args.diary_qubits <= args.shell_qubits:
        raise ValueError("diary_qubits must lie between 1 and shell_qubits")
    access_probabilities = tuple(float(value) for value in args.access)
    if any(value < 0.0 or value > 1.0 for value in access_probabilities):
        raise ValueError("access probabilities must lie in [0,1]")

    residual_entropy = np.log(2.0)
    entropy, energy, beta, omega = shell_thermodynamics(
        args.shell_qubits, residual_entropy, args.alpha
    )
    beta_omega = beta * omega
    density_ratio = np.exp(-beta_omega)
    excited_probability = density_ratio / (1.0 + density_ratio)
    curvature_error = np.max(np.abs(entropy - args.alpha * energy**2))

    all_rows = [
        run_seed(
            args.shell_qubits,
            args.diary_qubits,
            access_probabilities,
            args.seed + offset,
        )
        for offset in range(args.seeds)
    ]
    table = {}
    for depth in range(args.shell_qubits + 1):
        for access_probability in access_probabilities:
            selected = [
                row
                for rows in all_rows
                for row in rows
                if row[0] == depth and row[1] == access_probability
            ]
            table[(depth, access_probability)] = (
                float(np.mean([row[2] for row in selected])),
                float(np.std([row[2] for row in selected])),
                float(np.mean([row[3] for row in selected])),
            )

    blind_mutual_max = max(
        abs(table[(depth, 0.0)][2]) for depth in range(args.shell_qubits + 1)
    ) if 0.0 in access_probabilities else 0.0
    full_final_decoupling = table[(args.shell_qubits, 1.0)][0] if 1.0 in access_probabilities else 0.0
    if curvature_error > 2e-14:
        raise AssertionError("S(E)=alpha E^2 shell construction failed")
    if np.max(np.abs(density_ratio - 0.5)) > 2e-14:
        raise AssertionError("density-of-states thermal ratio failed")
    if blind_mutual_max > 2e-12:
        raise AssertionError("blind branch leaked diary information")
    if full_final_decoupling > 2e-12:
        raise AssertionError("fully accessible final radiation did not decouple")

    print("shrinking-shell diary-channel check:")
    print(
        "  shell dimensions:             "
        + " -> ".join(str(2 ** (args.shell_qubits - j)) for j in range(args.shell_qubits + 1))
    )
    print(f"  max S(E)-alpha E^2 error:    {curvature_error:.3e}")
    print(f"  beta_j omega_j range:        [{beta_omega.min():.6f}, {beta_omega.max():.6f}]")
    print(f"  thermal excited probability: {excited_probability[0]:.6f} (all branches/steps)")
    print(f"  blind max I(Q:R):            {blind_mutual_max:.3e}")
    print(f"  full-access final decoupling:{full_final_decoupling:.3e}")
    print("\n  depth access  decoupling(mean+-sd)     I(Q:R) mean")
    for depth in range(args.shell_qubits + 1):
        for access_probability in access_probabilities:
            dec, std, mutual = table[(depth, access_probability)]
            print(
                f"  {depth:5d} {access_probability:6.2f}  "
                f"{dec:10.6f} +- {std:8.6f}    {mutual:10.6f}"
            )


if __name__ == "__main__":
    main()
