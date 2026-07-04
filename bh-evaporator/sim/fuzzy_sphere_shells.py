"""Verify fuzzy-sphere angular shell structure.

For spin j=(N-1)/2, Mat_N decomposes under the adjoint SU(2) action as

    Mat_N = direct sum_{l=0}^{N-1} V_l,
    dim V_l = 2l + 1.

The fuzzy-sphere Laplacian is

    Delta(A) = sum_i [J_i, [J_i, A]]

and has eigenvalues l(l+1) with those degeneracies.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np


@dataclass
class Params:
    n: int = 6
    tol: float = 1e-8
    d_label: float = 2.0
    mu: float = 1.0


def spin_matrices(n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    j = (n - 1) / 2.0
    m_vals = np.arange(j, -j - 1, -1)
    jp = np.zeros((n, n), dtype=complex)
    for col, m in enumerate(m_vals):
        mp = m + 1
        if mp > j:
            continue
        row = int(round(j - mp))
        jp[row, col] = np.sqrt(j * (j + 1) - m * (m + 1))
    jm = jp.conj().T
    jx = 0.5 * (jp + jm)
    jy = (jp - jm) / (2j)
    jz = np.diag(m_vals).astype(complex)
    return jx, jy, jz


def commutator_super(jmat: np.ndarray) -> np.ndarray:
    n = jmat.shape[0]
    ident = np.eye(n, dtype=complex)
    # vec(J A - A J), column-major vec convention.
    return np.kron(ident, jmat) - np.kron(jmat.T, ident)


def laplacian_super(n: int) -> np.ndarray:
    js = spin_matrices(n)
    dim = n * n
    lap = np.zeros((dim, dim), dtype=complex)
    for jmat in js:
        c = commutator_super(jmat)
        lap += c @ c
    return 0.5 * (lap + lap.conj().T)


def group_eigs(vals: np.ndarray, tol: float) -> list[tuple[float, int]]:
    vals = np.sort(np.real(vals))
    groups: list[tuple[float, int]] = []
    current = [vals[0]]
    for v in vals[1:]:
        if abs(v - np.mean(current)) < tol:
            current.append(v)
        else:
            groups.append((float(np.mean(current)), len(current)))
            current = [v]
    groups.append((float(np.mean(current)), len(current)))
    return groups


def thermodynamic_rows(n_max: int, d_label: float, mu: float) -> list[str]:
    rows = ["N  Lmax  modes  shell  S         M      T_cont"]
    for n in range(2, n_max + 1):
        modes = n * n
        shell = 2 * n - 1
        entropy = modes * np.log(d_label)
        mass = mu * n
        # S_N = N^2 log d, M_N = mu N -> T = mu/(2N log d)
        temp = mu / (2.0 * n * np.log(d_label))
        rows.append(
            f"{n:2d} {n-1:5d} {modes:6d} {shell:6d} "
            f"{entropy:8.3f} {mass:7.3f} {temp:9.5f}"
        )
    return rows


def summarize(params: Params) -> str:
    lap = laplacian_super(params.n)
    vals = np.linalg.eigvalsh(lap)
    groups = group_eigs(vals, params.tol)

    lines = [
        f"fuzzy sphere shell check N={params.n}",
        "eigenvalue  degeneracy  expected_l  expected_eval  expected_deg  ok",
    ]
    ok_all = True
    for l, (eig, deg) in enumerate(groups):
        expected_eval = l * (l + 1)
        expected_deg = 2 * l + 1
        ok = abs(eig - expected_eval) < 1e-7 and deg == expected_deg
        ok_all = ok_all and ok
        lines.append(
            f"{eig:9.6f} {deg:10d} {l:11d} "
            f"{expected_eval:14.6f} {expected_deg:13d} {ok}"
        )
    lines.extend(
        [
            f"all_shells_ok={ok_all}",
            "",
            "thermodynamic shell skeleton",
            *thermodynamic_rows(params.n, params.d_label, params.mu),
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--tol", type=float, default=1e-8)
    parser.add_argument("--d-label", type=float, default=2.0)
    parser.add_argument("--mu", type=float, default=1.0)
    args = parser.parse_args()
    params = Params(n=args.n, tol=args.tol, d_label=args.d_label, mu=args.mu)
    print(summarize(params))


if __name__ == "__main__":
    main()
