#!/usr/bin/env python3
"""Regulated quantum matrix radial-detachment diagnostics.

This is the first matrix-coordinate frontend for the detachment test.  It is
not BFSS.  It quantizes two real symmetric traceless 2x2 matrices,

    X_a = [[x_a, y_a], [y_a, -x_a]],  a=1,2,

with four oscillator coordinates and Hamiltonian

    H = 1/2 sum_i p_i^2 + 1/2 mu^2 sum_i x_i^2
        + g^2 (x_1 y_2 - y_1 x_2)^2.

The clumped sector P and separated sector Q are spectral projectors of the
radial matrix-separation operator R^2=sum_i x_i^2.  The transition matrix is
the actual Feshbach coupling

    D_{c alpha} = <c| Q H P |alpha>,

where |alpha> diagonalizes PHP and |c> diagonalizes QHQ.  Rows are grouped
into coarse radial record bins to implement the accessible-record test.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from dataclasses import asdict, dataclass

import numpy as np
from numpy.typing import NDArray

from sector_detachment_diagnostics import (
    DATADIR,
    correlator_metrics,
    diagnostics,
    strength_histogram,
    write_histogram,
)


@dataclass(frozen=True)
class Params:
    cutoff: int = 5
    mu: float = 1.0
    g: float = 1.0
    p_fraction: float = 0.35
    q_fraction: float = 0.35
    record_bins: int = 3
    spectral_bins: int = 32
    time_points: int = 400
    t_max: float = 80.0
    output_prefix: str = "matrix_radial_detachment"

    @property
    def n_modes(self) -> int:
        return 4

    @property
    def dim(self) -> int:
        return int(self.cutoff**self.n_modes)

    @property
    def n(self) -> int:
        # Compatibility with the shared diagnostics function.
        return self.cutoff

    @property
    def q(self) -> int:
        # Compatibility with the shared diagnostics function.
        return self.record_bins

    @property
    def mass_law(self) -> str:
        return "matrix_radial"

    @property
    def bandwidth(self) -> float:
        return self.g

    @property
    def doorway_rank(self) -> int:
        return 0

    @property
    def seed(self) -> int:
        return 0

    @property
    def operator(self) -> str:
        return "qhp_radial"

    @property
    def dim_high(self) -> int:
        return self.dim

    @property
    def dim_low(self) -> int:
        return self.dim


def oscillator_1d(cutoff: int) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    destroy = np.zeros((cutoff, cutoff), dtype=np.complex128)
    for n in range(1, cutoff):
        destroy[n - 1, n] = np.sqrt(n)
    create = destroy.conj().T
    x = (destroy + create) / np.sqrt(2.0)
    p = -1j * (destroy - create) / np.sqrt(2.0)
    return x, p


def embed(op: NDArray[np.complex128], mode: int, n_modes: int, cutoff: int) -> NDArray[np.complex128]:
    out: NDArray[np.complex128] | None = None
    ident = np.eye(cutoff, dtype=np.complex128)
    for idx in range(n_modes):
        factor = op if idx == mode else ident
        out = factor if out is None else np.kron(out, factor)
    assert out is not None
    return out


def build_operators(params: Params) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    x1, p1 = oscillator_1d(params.cutoff)
    xs = [embed(x1, mode, params.n_modes, params.cutoff) for mode in range(params.n_modes)]
    ps = [embed(p1, mode, params.n_modes, params.cutoff) for mode in range(params.n_modes)]

    r2 = sum(x @ x for x in xs)
    kinetic = 0.5 * sum(p @ p for p in ps)
    harmonic = 0.5 * params.mu * params.mu * r2
    area = xs[0] @ xs[3] - xs[1] @ xs[2]
    commutator_potential = params.g * params.g * (area @ area)
    h = kinetic + harmonic + commutator_potential
    h = 0.5 * (h + h.conj().T)
    r2 = 0.5 * (r2 + r2.conj().T)
    return h, r2


def sector_bases(
    r2: NDArray[np.complex128],
    params: Params,
) -> tuple[NDArray[np.complex128], NDArray[np.complex128], NDArray[np.float64], NDArray[np.float64]]:
    vals, vecs = np.linalg.eigh(r2)
    vals = np.real(vals)
    order = np.argsort(vals)
    vals = vals[order]
    vecs = vecs[:, order]
    n_p = max(1, int(round(params.p_fraction * vals.size)))
    n_q = max(1, int(round(params.q_fraction * vals.size)))
    if n_p + n_q >= vals.size:
        raise ValueError("p_fraction + q_fraction must leave a buffer sector")
    p_basis = vecs[:, :n_p]
    q_basis = vecs[:, -n_q:]
    p_r2 = vals[:n_p]
    q_r2 = vals[-n_q:]
    return p_basis, q_basis, p_r2, q_r2


def record_labels_from_radii(
    q_states: NDArray[np.complex128],
    r2: NDArray[np.complex128],
    params: Params,
) -> NDArray[np.int64]:
    r_expect = np.real(np.sum(q_states.conj() * (r2 @ q_states), axis=0))
    if params.record_bins <= 1:
        return np.zeros(q_states.shape[1], dtype=np.int64)
    edges = np.quantile(r_expect, np.linspace(0.0, 1.0, params.record_bins + 1))
    edges[0] -= 1e-12
    edges[-1] += 1e-12
    labels = np.digitize(r_expect, edges[1:-1], right=False)
    return labels.astype(np.int64)


def build_transition(
    params: Params,
) -> tuple[
    NDArray[np.complex128],
    NDArray[np.float64],
    NDArray[np.float64],
    NDArray[np.int64],
    dict[str, float | int],
]:
    h, r2 = build_operators(params)
    p_basis, q_basis, p_r2, q_r2 = sector_bases(r2, params)

    h_p = p_basis.conj().T @ h @ p_basis
    h_q = q_basis.conj().T @ h @ q_basis
    e_p, u_p = np.linalg.eigh(0.5 * (h_p + h_p.conj().T))
    e_q, u_q = np.linalg.eigh(0.5 * (h_q + h_q.conj().T))
    p_states = p_basis @ u_p
    q_states = q_basis @ u_q
    d = q_states.conj().T @ h @ p_states
    labels = record_labels_from_radii(q_states, r2, params)
    meta = {
        "dim_total": params.dim,
        "dim_p": int(p_states.shape[1]),
        "dim_q": int(q_states.shape[1]),
        "r2_p_max": float(np.max(p_r2)),
        "r2_q_min": float(np.min(q_r2)),
        "r2_gap": float(np.min(q_r2) - np.max(p_r2)),
        "h_trace": float(np.trace(h).real),
        "qhp_frobenius": float(np.sum(np.abs(d) ** 2)),
    }
    return d.astype(np.complex128), np.real(e_p), np.real(e_q), labels, meta


def parse_args() -> Params:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=5)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=1.0)
    parser.add_argument("--p-fraction", type=float, default=0.35)
    parser.add_argument("--q-fraction", type=float, default=0.35)
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=400)
    parser.add_argument("--t-max", type=float, default=80.0)
    parser.add_argument("--output-prefix", default="matrix_radial_detachment")
    return Params(**vars(parser.parse_args()))


def main() -> None:
    params = parse_args()
    d, e_p, e_q, labels, meta = build_transition(params)
    diag = diagnostics(params, d, e_p, e_q, labels)
    hist, edges = strength_histogram(d, e_p, e_q, params.spectral_bins)

    prefix = DATADIR / (
        f"{params.output_prefix}_cut{params.cutoff}_g{str(params.g).replace('.', 'p')}_"
        f"pf{str(params.p_fraction).replace('.', 'p')}_qf{str(params.q_fraction).replace('.', 'p')}"
    )
    prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = prefix.with_suffix(".json")
    hist_path = prefix.with_name(prefix.name + "_strength.csv")
    json_path.write_text(
        json.dumps({"params": asdict(params), "meta": meta, "diagnostics": diag}, indent=2)
    )
    write_histogram(hist_path, hist, edges)

    for key, value in {**meta, **diag}.items():
        if isinstance(value, float):
            print(f"{key}={value:.6g}")
        else:
            print(f"{key}={value}")
    print(f"wrote_json={json_path}")
    print(f"wrote_strength_csv={hist_path}")


if __name__ == "__main__":
    main()
