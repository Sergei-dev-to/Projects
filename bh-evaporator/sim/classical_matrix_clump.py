"""Classical diagnostic for stripped matrix-clump evaporation.

This is a deliberately small testbed, not a faithful BFSS simulation.

Hamiltonian:

    H = 1/2 sum_a Tr(P_a^2)
      + g^2/2 sum_{a<b} ||[X_a, X_b]||_F^2

with real symmetric traceless matrices.  The diagnostic asks whether a compact
matrix clump develops a separated radial eigenvalue and whether the remaining
subspace heats after that separation.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np


@dataclass
class Params:
    n: int = 6
    d: int = 3
    g: float = 1.0
    dt: float = 0.002
    steps: int = 20000
    sample_every: int = 20
    seed: int = 1234
    x_scale: float = 0.55
    p_scale: float = 0.70
    escape_ratio: float = 3.0


def sym_traceless(rng: np.random.Generator, n: int, scale: float) -> np.ndarray:
    a = rng.normal(size=(n, n))
    a = 0.5 * (a + a.T)
    a -= np.eye(n) * np.trace(a) / n
    norm = np.sqrt(np.trace(a @ a))
    if norm > 0:
        a *= scale / norm * np.sqrt(n)
    return a


def initial_state(params: Params) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(params.seed)
    x = np.array(
        [sym_traceless(rng, params.n, params.x_scale) for _ in range(params.d)]
    )
    p = np.array(
        [sym_traceless(rng, params.n, params.p_scale) for _ in range(params.d)]
    )
    return x, p


def comm(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a @ b - b @ a


def force(x: np.ndarray, g: float) -> np.ndarray:
    d = x.shape[0]
    f = np.zeros_like(x)
    for a in range(d):
        acc = np.zeros_like(x[a])
        for b in range(d):
            if a == b:
                continue
            acc += x[b] @ comm(x[a], x[b]) - comm(x[a], x[b]) @ x[b]
        f[a] = g * g * acc
        f[a] = 0.5 * (f[a] + f[a].T)
        f[a] -= np.eye(x.shape[1]) * np.trace(f[a]) / x.shape[1]
    return f


def energies(x: np.ndarray, p: np.ndarray, g: float) -> tuple[float, float, float]:
    kinetic = 0.5 * sum(np.trace(pa @ pa) for pa in p)
    potential = 0.0
    for a in range(x.shape[0]):
        for b in range(a + 1, x.shape[0]):
            c = comm(x[a], x[b])
            potential += 0.5 * g * g * np.sum(c * c)
    return kinetic + potential, kinetic, potential


def radial_basis(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    r2 = np.zeros_like(x[0])
    for xa in x:
        r2 += xa @ xa
    r2 = 0.5 * (r2 + r2.T)
    vals, vecs = np.linalg.eigh(r2)
    vals = np.maximum(vals, 0.0)
    return np.sqrt(vals), vecs


def projected_kinetic(p: np.ndarray, vecs: np.ndarray, keep: np.ndarray) -> float:
    q = vecs[:, keep]
    kinetic = 0.0
    for pa in p:
        block = q.T @ pa @ q
        kinetic += 0.5 * np.trace(block @ block)
    return float(kinetic)


def projected_potential(x: np.ndarray, vecs: np.ndarray, keep: np.ndarray, g: float) -> float:
    q = vecs[:, keep]
    xb = np.array([q.T @ xa @ q for xa in x])
    potential = 0.0
    for a in range(xb.shape[0]):
        for b in range(a + 1, xb.shape[0]):
            c = comm(xb[a], xb[b])
            potential += 0.5 * g * g * np.sum(c * c)
    return float(potential)


def sample(t: float, x: np.ndarray, p: np.ndarray, params: Params) -> dict[str, float]:
    total, kinetic, potential = energies(x, p, params.g)
    radii, vecs = radial_basis(x)
    r_sorted = np.sort(radii)
    r_max = float(r_sorted[-1])
    r_med = float(np.median(r_sorted[:-1])) if len(r_sorted) > 2 else float(np.median(r_sorted))
    ratio = r_max / max(r_med, 1e-12)
    keep = np.arange(params.n - 1)
    k_cl = projected_kinetic(p, vecs, keep)
    v_cl = projected_potential(x, vecs, keep, params.g)
    dof_cl = params.d * (params.n - 1) * params.n / 2
    temp_cl = 2.0 * k_cl / max(dof_cl, 1.0)
    comm_norm = 0.0
    for a in range(params.d):
        for b in range(a + 1, params.d):
            c = comm(x[a], x[b])
            comm_norm += np.sum(c * c)
    return {
        "t": t,
        "E": total,
        "K": kinetic,
        "V": potential,
        "r_max": r_max,
        "r_med": r_med,
        "ratio": ratio,
        "E_cl": k_cl + v_cl,
        "K_cl": k_cl,
        "T_cl": temp_cl,
        "comm": float(np.sqrt(comm_norm)),
    }


def run(params: Params) -> list[dict[str, float]]:
    x, p = initial_state(params)
    f = force(x, params.g)
    rows: list[dict[str, float]] = []
    for step in range(params.steps + 1):
        if step % params.sample_every == 0:
            rows.append(sample(step * params.dt, x, p, params))
        p_half = p + 0.5 * params.dt * f
        x = x + params.dt * p_half
        x = 0.5 * (x + np.swapaxes(x, 1, 2))
        for a in range(params.d):
            x[a] -= np.eye(params.n) * np.trace(x[a]) / params.n
        f_new = force(x, params.g)
        p = p_half + 0.5 * params.dt * f_new
        p = 0.5 * (p + np.swapaxes(p, 1, 2))
        for a in range(params.d):
            p[a] -= np.eye(params.n) * np.trace(p[a]) / params.n
        f = f_new
    return rows


def summarize(rows: list[dict[str, float]], params: Params) -> str:
    e0 = rows[0]["E"]
    e_drift = max(abs(r["E"] - e0) for r in rows) / max(abs(e0), 1e-12)
    ratios = np.array([r["ratio"] for r in rows])
    escape_idxs = np.where(ratios > params.escape_ratio)[0]
    above = ratios > params.escape_ratio
    longest = 0
    current = 0
    for flag in above:
        if flag:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    lines = [
        f"N={params.n} D={params.d} seed={params.seed} steps={params.steps} dt={params.dt}",
        f"energy_drift_rel={e_drift:.3e}",
        f"ratio_start={rows[0]['ratio']:.3f} ratio_max={ratios.max():.3f} ratio_end={rows[-1]['ratio']:.3f}",
        f"Tcl_start={rows[0]['T_cl']:.3f} Tcl_end={rows[-1]['T_cl']:.3f}",
        f"above_threshold_fraction={above.mean():.3f} longest_above_samples={longest}",
    ]
    if len(escape_idxs) == 0:
        lines.append(f"escape_candidate=no threshold={params.escape_ratio:.2f}")
    else:
        i0 = int(escape_idxs[0])
        before = rows[max(i0 - 5, 0)]
        after = rows[min(i0 + 20, len(rows) - 1)]
        lines.append(
            "escape_candidate=yes "
            f"t={rows[i0]['t']:.3f} ratio={rows[i0]['ratio']:.3f}"
        )
        lines.append(
            "post_event_delta "
            f"dEcl={after['E_cl'] - before['E_cl']:.3f} "
            f"dTcl={after['T_cl'] - before['T_cl']:.3f}"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--d", type=int, default=3)
    parser.add_argument("--g", type=float, default=1.0)
    parser.add_argument("--dt", type=float, default=0.002)
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--sample-every", type=int, default=20)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--x-scale", type=float, default=0.55)
    parser.add_argument("--p-scale", type=float, default=0.70)
    parser.add_argument("--escape-ratio", type=float, default=3.0)
    args = parser.parse_args()
    params = Params(
        n=args.n,
        d=args.d,
        g=args.g,
        dt=args.dt,
        steps=args.steps,
        sample_every=args.sample_every,
        seed=args.seed,
        x_scale=args.x_scale,
        p_scale=args.p_scale,
        escape_ratio=args.escape_ratio,
    )
    rows = run(params)
    print(summarize(rows, params))


if __name__ == "__main__":
    main()
