"""Finite regression checks for the DSSYK WP1 formal controls.

The script verifies isometric invariance of a two-step memoryful record
channel, the charge metadata/fixed-sector payload split, and the binary
classical twirl identity. It uses random finite matrices and is not a DSSYK
dynamics calculation.
"""

from __future__ import annotations

import argparse

import numpy as np


def random_unitary(dim: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    q, r = np.linalg.qr(raw)
    phases = np.diag(r).copy()
    phases /= np.maximum(np.abs(phases), 1e-300)
    return q * phases.conj()[None, :]


def random_density(dim: int, rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    rho = raw @ raw.conj().T
    return rho / np.trace(rho)


def trace_norm_hermitian(matrix: np.ndarray) -> float:
    hermitian = 0.5 * (matrix + matrix.conj().T)
    return float(np.sum(np.abs(np.linalg.eigvalsh(hermitian))))


def partial_trace_system(rho: np.ndarray, d_system: int, d_record: int) -> np.ndarray:
    reshaped = rho.reshape(d_system, d_record, d_system, d_record)
    return np.trace(reshaped, axis1=0, axis2=2)


def append_record_and_interact(
    rho_system_record: np.ndarray,
    unitary_system_new: np.ndarray,
    d_system: int,
    d_old_record: int,
) -> np.ndarray:
    """Append |0><0| and apply a system--new-record unitary."""
    zero = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)
    rho = np.kron(rho_system_record, zero).reshape(
        d_system, d_old_record, 2, d_system, d_old_record, 2
    )
    rho = np.transpose(rho, (0, 2, 1, 3, 5, 4)).reshape(
        2 * d_system * d_old_record, 2 * d_system * d_old_record
    )
    lifted = np.kron(unitary_system_new, np.eye(d_old_record))
    rho = lifted @ rho @ lifted.conj().T
    return rho.reshape(d_system, 2, d_old_record, d_system, 2, d_old_record).transpose(
        0, 2, 1, 3, 5, 4
    ).reshape(2 * d_system * d_old_record, 2 * d_system * d_old_record)


def two_step_record(
    rho_system: np.ndarray, unitaries: tuple[np.ndarray, np.ndarray]
) -> np.ndarray:
    d_system = rho_system.shape[0]
    state = rho_system
    old_record = 1
    for unitary in unitaries:
        state = append_record_and_interact(state, unitary, d_system, old_record)
        old_record *= 2
    return partial_trace_system(state, d_system, old_record)


def transport_interaction(
    unitary: np.ndarray, isometry: np.ndarray, d_system: int, d_large: int
) -> np.ndarray:
    """Extend W U W^dagger by identity off the physical image."""
    w_record = np.kron(isometry, np.eye(2))
    projector = isometry @ isometry.conj().T
    physical = w_record @ unitary @ w_record.conj().T
    complement = np.kron(np.eye(d_large) - projector, np.eye(2))
    return physical + complement


def isometry_check(rng: np.random.Generator) -> float:
    d_system = 3
    d_large = 5
    raw = rng.normal(size=(d_large, d_system)) + 1j * rng.normal(
        size=(d_large, d_system)
    )
    isometry, _ = np.linalg.qr(raw)
    isometry = isometry[:, :d_system]
    unitaries = (random_unitary(2 * d_system, rng), random_unitary(2 * d_system, rng))
    transported = tuple(
        transport_interaction(unitary, isometry, d_system, d_large)
        for unitary in unitaries
    )
    rho = random_density(d_system, rng)
    rho_large = isometry @ rho @ isometry.conj().T
    record = two_step_record(rho, unitaries)
    record_large = two_step_record(rho_large, transported)
    return trace_norm_hermitian(record - record_large)


def charge_record_channel(rho: np.ndarray, sector_dims: tuple[int, ...]) -> np.ndarray:
    """Measure only the direct-sum sector label and retain no payload data."""
    if rho.shape != (sum(sector_dims), sum(sector_dims)):
        raise ValueError("rho does not match the declared charge sectors")
    probabilities = []
    offset = 0
    for dim in sector_dims:
        block = rho[offset : offset + dim, offset : offset + dim]
        probabilities.append(float(np.trace(block).real))
        offset += dim
    return np.diag(probabilities).astype(np.complex128)


def basis_density(dim: int, index: int) -> np.ndarray:
    state = np.zeros(dim, dtype=np.complex128)
    state[index] = 1.0
    return np.outer(state, state.conj())


def charge_control_check() -> tuple[float, float]:
    # Two charge sectors, each with a two-dimensional private payload.
    sector_dims = (2, 2)
    total_dim = sum(sector_dims)
    charge_zero = charge_record_channel(basis_density(total_dim, 0), sector_dims)
    charge_one = charge_record_channel(basis_density(total_dim, 2), sector_dims)
    header_delta = 0.5 * trace_norm_hermitian(charge_zero - charge_one)

    payload_zero = charge_record_channel(basis_density(total_dim, 0), sector_dims)
    payload_one = charge_record_channel(basis_density(total_dim, 1), sector_dims)
    payload_delta = 0.5 * trace_norm_hermitian(payload_zero - payload_one)
    return header_delta, payload_delta


def twirl_check(rng: np.random.Generator) -> tuple[float, float]:
    sigma_zero = random_density(4, rng)
    sigma_one = random_density(4, rng)
    delta = 0.5 * trace_norm_hermitian(sigma_zero - sigma_one)
    average = 0.5 * (sigma_zero + sigma_one)
    cq_diamond = max(
        trace_norm_hermitian(sigma_zero - average),
        trace_norm_hermitian(sigma_one - average),
    )
    return delta, cq_diamond


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1701)
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)

    isometry_error = isometry_check(rng)
    header_delta, payload_delta = charge_control_check()
    twirl_delta, twirl_diamond = twirl_check(rng)

    if isometry_error > 2e-12:
        raise AssertionError("isometric transport changed the record channel")
    if abs(header_delta - 1.0) > 2e-12 or payload_delta > 2e-12:
        raise AssertionError("charge metadata/payload split failed")
    if abs(twirl_delta - twirl_diamond) > 2e-12:
        raise AssertionError("binary cq twirl identity failed")

    print("DSSYK WP1 finite controls:")
    print(f"  two-step isometry record error: {isometry_error:.3e}")
    print(f"  charge-header delta:            {header_delta:.6f}")
    print(f"  fixed-charge payload delta:     {payload_delta:.3e}")
    print(f"  actual binary delta:            {twirl_delta:.6f}")
    print(f"  actual-to-twirl diamond norm:   {twirl_diamond:.6f}")


if __name__ == "__main__":
    main()
