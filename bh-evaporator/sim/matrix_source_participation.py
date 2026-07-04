#!/usr/bin/env python3
r"""Source-resolved participation in the regulated matrix radial model.

This tests the prediction that a high-participation detachment channel needs
many inequivalent source/tether operators, not just radial block separation.

The Hamiltonian and P/Q sectors are imported from
matrix_radial_detachment_diagnostics.py.  Source operators are simple
matrix-coordinate monomials projected between the same sectors:

    D_a = <c| Q O_a P |alpha>.

The script compares:

    source Gram:        S_ab = Tr D_a D_b^\dagger
    stacked channel:    rows (a,c)
    collective channel: sum_a D_a

The stacked channel asks whether source labels create independent doorway
directions.  The collective channel asks how much survives if the radiation
record does not resolve the source label.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass

import numpy as np
from numpy.typing import NDArray

from matrix_radial_detachment_diagnostics import (
    DATADIR,
    Params as RadialParams,
    build_operators,
    record_labels_from_radii,
    sector_bases,
)
from sector_detachment_diagnostics import diagnostics, participation


@dataclass(frozen=True)
class Params:
    cutoff: int = 5
    mu: float = 1.0
    g: float = 1.0
    p_fraction: float = 0.30
    q_fraction: float = 0.30
    record_bins: int = 3
    source_set: str = "quadratic"
    spectral_bins: int = 32
    time_points: int = 300
    t_max: float = 60.0
    output_prefix: str = "matrix_source_participation"

    @property
    def n(self) -> int:
        return self.cutoff

    @property
    def q(self) -> int:
        return self.record_bins

    @property
    def mass_law(self) -> str:
        return "matrix_source"

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
        return f"sources_{self.source_set}"

    @property
    def dim_high(self) -> int:
        return int(self.cutoff**4)

    @property
    def dim_low(self) -> int:
        return int(self.cutoff**4)


def oscillator_1d(cutoff: int) -> tuple[NDArray[np.complex128], NDArray[np.complex128]]:
    destroy = np.zeros((cutoff, cutoff), dtype=np.complex128)
    for n in range(1, cutoff):
        destroy[n - 1, n] = np.sqrt(n)
    x = (destroy + destroy.conj().T) / np.sqrt(2.0)
    p = -1j * (destroy - destroy.conj().T) / np.sqrt(2.0)
    return x, p


def embed(op: NDArray[np.complex128], mode: int, n_modes: int, cutoff: int) -> NDArray[np.complex128]:
    out: NDArray[np.complex128] | None = None
    ident = np.eye(cutoff, dtype=np.complex128)
    for idx in range(n_modes):
        factor = op if idx == mode else ident
        out = factor if out is None else np.kron(out, factor)
    assert out is not None
    return out


def source_operators(params: Params) -> list[tuple[str, NDArray[np.complex128]]]:
    x1, p1 = oscillator_1d(params.cutoff)
    xs = [embed(x1, mode, 4, params.cutoff) for mode in range(4)]
    ps = [embed(p1, mode, 4, params.cutoff) for mode in range(4)]
    ops: list[tuple[str, NDArray[np.complex128]]] = []
    if params.source_set in {"linear", "linear_quadratic", "quadratic"}:
        if params.source_set in {"linear", "linear_quadratic"}:
            for idx, x in enumerate(xs):
                ops.append((f"x{idx}", x))
        if params.source_set in {"linear_quadratic", "quadratic"}:
            for idx, x in enumerate(xs):
                ops.append((f"x{idx}2", x @ x))
            for i in range(len(xs)):
                for j in range(i + 1, len(xs)):
                    ops.append((f"x{i}x{j}", 0.5 * (xs[i] @ xs[j] + xs[j] @ xs[i])))
    elif params.source_set == "commutator":
        area = xs[0] @ xs[3] - xs[1] @ xs[2]
        ops.append(("area", area))
        ops.append(("area2", area @ area))
        for idx, x in enumerate(xs):
            ops.append((f"area_x{idx}", 0.5 * (area @ x + x @ area)))
    elif params.source_set == "h_terms":
        for idx, p in enumerate(ps):
            ops.append((f"kin{idx}", 0.5 * (p @ p)))
        for idx, x in enumerate(xs):
            ops.append((f"harm{idx}", 0.5 * params.mu * params.mu * (x @ x)))
        ops.append(("quartic_03", params.g * params.g * (xs[0] @ xs[0] @ xs[3] @ xs[3])))
        ops.append(("quartic_12", params.g * params.g * (xs[1] @ xs[1] @ xs[2] @ xs[2])))
        ops.append((
            "quartic_cross",
            -2.0 * params.g * params.g * (xs[0] @ xs[1] @ xs[2] @ xs[3]),
        ))
    else:
        raise ValueError(f"unknown source set: {params.source_set}")
    return [(name, 0.5 * (op + op.conj().T)) for name, op in ops]


def radial_params(params: Params) -> RadialParams:
    return RadialParams(
        cutoff=params.cutoff,
        mu=params.mu,
        g=params.g,
        p_fraction=params.p_fraction,
        q_fraction=params.q_fraction,
        record_bins=params.record_bins,
        spectral_bins=params.spectral_bins,
        time_points=params.time_points,
        t_max=params.t_max,
    )


def build_source_transitions(
    params: Params,
) -> tuple[list[str], NDArray[np.complex128], NDArray[np.float64], NDArray[np.float64], NDArray[np.int64], dict]:
    rparams = radial_params(params)
    h, r2 = build_operators(rparams)
    p_basis, q_basis, p_r2, q_r2 = sector_bases(r2, rparams)
    h_p = p_basis.conj().T @ h @ p_basis
    h_q = q_basis.conj().T @ h @ q_basis
    e_p, u_p = np.linalg.eigh(0.5 * (h_p + h_p.conj().T))
    e_q, u_q = np.linalg.eigh(0.5 * (h_q + h_q.conj().T))
    p_states = p_basis @ u_p
    q_states = q_basis @ u_q
    labels = record_labels_from_radii(q_states, r2, rparams)

    rows = []
    names = []
    ops = source_operators(params)
    for name, op in ops:
        names.append(name)
        rows.append(q_states.conj().T @ op @ p_states)
    stacked = np.vstack(rows)
    stacked_labels = np.tile(labels, len(rows))
    meta = {
        "dim_total": int(h.shape[0]),
        "dim_p": int(p_states.shape[1]),
        "dim_q": int(q_states.shape[1]),
        "n_sources": len(rows),
        "r2_p_max": float(np.max(p_r2)),
        "r2_q_min": float(np.min(q_r2)),
        "r2_gap": float(np.min(q_r2) - np.max(p_r2)),
        "stacked_frobenius": float(np.sum(np.abs(stacked) ** 2)),
    }
    return names, stacked.astype(np.complex128), np.real(e_p), np.tile(np.real(e_q), len(rows)), stacked_labels, meta


def source_metrics(d: NDArray[np.complex128], n_sources: int, dim_q: int) -> dict[str, float]:
    blocks = d.reshape(n_sources, dim_q, d.shape[1])
    source_gram = np.zeros((n_sources, n_sources), dtype=np.complex128)
    for a in range(n_sources):
        for b in range(n_sources):
            source_gram[a, b] = np.vdot(blocks[b], blocks[a])
    eig = np.linalg.eigvalsh(0.5 * (source_gram + source_gram.conj().T)).real
    collective = np.sum(blocks, axis=0)
    full_eig = np.linalg.eigvalsh(collective @ collective.conj().T).real
    return {
        "source_gram_participation": participation(eig),
        "source_gram_participation_norm": participation(eig) / max(n_sources, 1),
        "largest_source_width_fraction": float(np.max(eig) / max(np.sum(eig), 1e-300)),
        "collective_channel_gram_participation": participation(full_eig),
        "collective_channel_gram_participation_norm": participation(full_eig) / max(
            min(collective.shape), 1
        ),
        "collective_largest_width_fraction": float(
            np.max(full_eig) / max(np.sum(full_eig), 1e-300)
        ),
    }


def parse_args() -> Params:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cutoff", type=int, default=5)
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--g", type=float, default=1.0)
    parser.add_argument("--p-fraction", type=float, default=0.30)
    parser.add_argument("--q-fraction", type=float, default=0.30)
    parser.add_argument("--record-bins", type=int, default=3)
    parser.add_argument(
        "--source-set",
        choices=["linear", "quadratic", "linear_quadratic", "commutator", "h_terms"],
        default="quadratic",
    )
    parser.add_argument("--spectral-bins", type=int, default=32)
    parser.add_argument("--time-points", type=int, default=300)
    parser.add_argument("--t-max", type=float, default=60.0)
    parser.add_argument("--output-prefix", default="matrix_source_participation")
    return Params(**vars(parser.parse_args()))


def main() -> None:
    params = parse_args()
    names, d, e_p, e_q, labels, meta = build_source_transitions(params)
    diag = diagnostics(params, d, e_p, e_q, labels)
    sm = source_metrics(d, int(meta["n_sources"]), int(meta["dim_q"]))
    result = {
        "params": asdict(params),
        "source_names": names,
        "meta": meta,
        "diagnostics": diag,
        "source_metrics": sm,
    }
    prefix = DATADIR / (
        f"{params.output_prefix}_cut{params.cutoff}_g{str(params.g).replace('.', 'p')}_"
        f"{params.source_set}_pf{str(params.p_fraction).replace('.', 'p')}"
    )
    prefix.parent.mkdir(parents=True, exist_ok=True)
    path = prefix.with_suffix(".json")
    path.write_text(json.dumps(result, indent=2))
    for key, value in {**meta, **diag, **sm}.items():
        if isinstance(value, float):
            print(f"{key}={value:.6g}")
        else:
            print(f"{key}={value}")
    print(f"source_names={','.join(names)}")
    print(f"wrote_json={path}")


if __name__ == "__main__":
    main()
