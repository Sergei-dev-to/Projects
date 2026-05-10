#!/usr/bin/env python3
"""
Generate reproducible thermodynamic and spectral data for figures.

Model: fully-connected XXZ with weak disorder on N spins, edge operator X.
Computes spectrum, microcanonical S(E), T_mu(E), C_mu(E), and the typical
transition frequency omega_star(E) from a coarse-grained edge spectral function.

Outputs NPZ files into sim/data/ for plotting by figs/generate.py.
"""
from __future__ import annotations

import argparse
import pathlib
import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass

try:
    import scipy.linalg as la
    import scipy.sparse as sp
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"SciPy is required for data generation: {exc}")


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATADIR = ROOT / "sim" / "data"
DATADIR.mkdir(parents=True, exist_ok=True)


def pauli() -> tuple[NDArray, NDArray, NDArray, NDArray]:
    sx = np.array([[0.0, 1.0], [1.0, 0.0]], float)
    sy = np.array([[0.0, -1.0j], [1.0j, 0.0]], complex)
    sz = np.array([[1.0, 0.0], [0.0, -1.0]], float)
    sm = np.array([[0.0, 0.0], [1.0, 0.0]], complex)  # sigma^-
    return sx, sy, sz, sm


def kron_n(op_list: list[NDArray]) -> NDArray:
    out = op_list[0]
    for op in op_list[1:]:
        out = np.kron(out, op)
    return out


def build_xxz_hamiltonian(N: int, jxy: float, jz: float, h_dis: float, seed: int) -> NDArray:
    rng = np.random.default_rng(seed)
    sx, sy, sz, _ = pauli()
    H = np.zeros((2**N, 2**N), complex)
    # Fully connected (mean-field strength 1/N)
    for i in range(N):
        for j in range(i + 1, N):
            opsx = [np.eye(2)] * N
            opsy = [np.eye(2)] * N
            opsz = [np.eye(2)] * N
            opsx[i] = sx; opsx[j] = sx
            opsy[i] = sy; opsy[j] = sy
            opsz[i] = sz; opsz[j] = sz
            H += (jxy / N) * (kron_n(opsx) + kron_n(opsy)) + (jz / N) * kron_n(opsz)
    # Weak disordered field in z
    fields = h_dis * rng.uniform(-1.0, 1.0, size=N)
    for i, h in enumerate(fields):
        ops = [np.eye(2)] * N
        ops[i] = sz
        H += h * kron_n(ops)
    # Hermitian float matrix
    H = (H + H.conj().T) / 2.0
    return H.real


def edge_operator(N: int) -> NDArray:
    _, _, _, sm = pauli()
    Xs = []
    for i in range(N):
        ops = [np.eye(2, dtype=complex)] * N
        ops[i] = sm
        Xs.append(kron_n(ops))
    X = sum(Xs) / np.sqrt(N)
    return X


def microcanonical_from_spectrum(E: NDArray, bins: int) -> dict:
    E = np.asarray(E)
    hist, edges = np.histogram(E, bins=bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    # Entropy up to a constant: S(E) ~ log DOS
    # Avoid log(0): add a small floor
    dos = hist.astype(float) + 1e-12
    S = np.log(dos)
    # Smooth derivatives with simple finite differences
    dE = np.diff(edges)
    # Uniform bins assumed by numpy.histogram with int bins
    dS = np.gradient(S, centers)
    Tmu = 1.0 / np.maximum(1e-12, dS)
    d2S = np.gradient(dS, centers)
    Cmu = -Tmu**2 / np.maximum(1e-12, d2S)
    return {"E_centers": centers, "hist_E": hist, "S": S, "T_mu": Tmu, "C_mu": Cmu}


def spectral_omega_star(H: NDArray, X: NDArray, E: NDArray, bins: int, width: float = 0.2) -> tuple[NDArray, NDArray]:
    """Compute a coarse ω*(E) by binning eigenstates and finding peak transitions.
    Uses a naive Gaussian broadening of transitions from states in each bin.
    """
    evals, evecs = E, None
    # For dense H, get eigenvectors once to reuse
    w, V = la.eigh(H)
    evals = w
    evecs = V
    centers = microcanonical_from_spectrum(evals, bins)["E_centers"]
    omega_star = np.zeros_like(centers)
    for b, Ec in enumerate(centers):
        mask = (evals >= Ec - 0.5 * (centers[1] - centers[0])) & (evals < Ec + 0.5 * (centers[1] - centers[0]))
        idx = np.where(mask)[0]
        if idx.size < 2:
            omega_star[b] = np.nan
            continue
        # Build transitions from bin states to all others with weights |<i|X|j>|^2
        Vi = evecs[:, idx]
        XVi = X @ Vi
        # Matrix elements to all j: <j|X|i> = (V^† X Vi)_j,i
        M = V.conj().T @ XVi
        weights = np.abs(M) ** 2
        # Transition frequencies ω = E_j - E_i
        Ei = evals[idx]
        Ej = evals[:, None]
        Omega = Ej - Ei[None, :]
        # Consider ω>0 and accumulate a broadened spectrum
        pos = Omega > 0
        omega = Omega[pos].ravel()
        wght = weights[pos].ravel().real
        if omega.size == 0:
            omega_star[b] = np.nan
            continue
        # Histogram with Gaussian broadening
        o_min, o_max = np.percentile(omega, 1), np.percentile(omega, 99)
        grid = np.linspace(max(1e-3, o_min), o_max, 200)
        spec = np.zeros_like(grid)
        sig = width
        for om, wt in zip(omega, wght):
            spec += wt * np.exp(-0.5 * ((grid - om) / sig) ** 2)
        omega_star[b] = grid[np.argmax(spec)]
    return centers, omega_star


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=12, help="Number of spins (default 12)")
    ap.add_argument("--jxy", type=float, default=1.0)
    ap.add_argument("--jz", type=float, default=1.0)
    ap.add_argument("--hdis", type=float, default=0.2, help="Disorder strength in z")
    ap.add_argument("--bins", type=int, default=20)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args(argv)

    N = args.N
    print(f"[sim] building H (N={N}) …")
    H = build_xxz_hamiltonian(N, args.jxy, args.jz, args.hdis, args.seed)
    print("[sim] diagonalizing …")
    w, V = la.eigh(H)
    print("[sim] spectrum computed: ", w.shape[0], "levels")

    print("[sim] microcanonical quantities …")
    mc = microcanonical_from_spectrum(w, bins=args.bins)
    np.savez(DATADIR / "thermo.npz", **mc)
    print("[sim] wrote sim/data/thermo.npz")

    print("[sim] spectral function summary …")
    X = edge_operator(N)
    centers, wstar = spectral_omega_star(H, X, w, bins=args.bins)
    np.savez(DATADIR / "spectral.npz", E_centers=centers, omega_star=wstar)
    print("[sim] wrote sim/data/spectral.npz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

