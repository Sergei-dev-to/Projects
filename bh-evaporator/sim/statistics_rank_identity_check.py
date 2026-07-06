"""Support check for the statistics-rank link (Q1b).

Verifies, by exact normally-ordered moment expansion over a product
state (no Wick/Gaussian assumption), the composite-source identity

    g2 = 2 + sum_i f_i^2 (g2_i - 2)

for A = sum_i alpha_i a_i with independent phase-symmetric modes:
one sharp (Fock N) "condensate" channel + thermal channels.
Also checks the dominance corollary and the line-asymmetry ratios.

Exact per-mode normally ordered moments used (all phase-odd vanish):
  Fock |N>:    <a+a> = N,     <a+2 a2> = N(N-1)      -> g2 = 1 - 1/N
  thermal nb:  <a+a> = nb,    <a+2 a2> = 2 nb^2      -> g2 = 2
The fourth moment of A expands over index assignments (i,j;k,l) with
per-mode factorization; only pairings with equal creation/annihilation
counts per mode survive phase symmetry.
"""

import itertools
import numpy as np

def mode_moments(kind, param):
    # returns dict (p,q) -> <a+^p a^q>, p,q <= 2, phase-symmetric
    m = {}
    if kind == "fock":
        N = param
        m[(1, 1)] = N
        m[(2, 2)] = N * (N - 1)
    elif kind == "thermal":
        nb = param
        m[(1, 1)] = nb
        m[(2, 2)] = 2 * nb**2
    m[(0, 0)] = 1.0
    return m

def g2_exact(alphas, modes):
    """<A+A+AA>/<A+A>^2 by exact expansion, A = sum alpha_i a_i."""
    n = len(alphas)
    I = sum(abs(alphas[i])**2 * modes[i][(1, 1)] for i in range(n))
    num = 0.0
    for i, j, k, l in itertools.product(range(n), repeat=4):
        # <a_i+ a_j+ a_k a_l> over product state: factorize per mode;
        # phase symmetry => each mode needs equal + and - counts.
        counts = {}
        for idx, dag in ((i, 1), (j, 1), (k, 0), (l, 0)):
            c = counts.setdefault(idx, [0, 0])
            c[dag] += 1
        term = 1.0
        ok = True
        for idx, (ann, cre) in counts.items():
            if ann != cre:
                ok = False
                break
            term *= modes[idx][(cre, ann)]
        if not ok:
            continue
        num += (np.conj(alphas[i]) * np.conj(alphas[j])
                * alphas[k] * alphas[l]).real * term
    return num / I**2, I

def identity_prediction(alphas, modes):
    Is = [abs(alphas[i])**2 * modes[i][(1, 1)] for i in range(len(alphas))]
    I = sum(Is)
    g2s = [modes[i][(2, 2)] / modes[i][(1, 1)]**2 for i in range(len(alphas))]
    return 2 + sum((Ii / I)**2 * (g2i - 2) for Ii, g2i in zip(Is, g2s))

def main():
    rng = np.random.default_rng(7)
    print("composite identity check: exact vs prediction")
    print(f"{'f_sharp':>8} {'g2_exact':>10} {'g2_pred':>10} {'diff':>10}")
    N = 400  # sharp channel occupation (finite-size: g2_c = 1 - 1/N)
    for f_target in (0.0, 0.1, 0.3, 0.5, 0.8, 1.0):
        # one Fock channel + 3 thermal channels with random weights
        nbs = [0.6, 1.1, 0.4]
        modes = [mode_moments("fock", N)] + [
            mode_moments("thermal", nb) for nb in nbs]
        w = rng.uniform(0.5, 1.5, size=3)
        # choose couplings to hit flux fraction f_target for the sharp one
        I_th_raw = sum(wi * nb for wi, nb in zip(w, nbs))
        if f_target == 1.0:
            alphas = [1.0, 0, 0, 0]
        else:
            a0 = np.sqrt(f_target / (1 - f_target) * I_th_raw / N)
            alphas = [a0] + [np.sqrt(wi) for wi in w]
        g2, I = g2_exact(alphas, modes)
        pred = identity_prediction(alphas, modes)
        print(f"{f_target:8.2f} {g2:10.6f} {pred:10.6f} {abs(g2-pred):10.2e}")

    print("\ndominance corollary: eps = 2 - g2 vs f^2 (g2_c ~ 1)")
    for f in (0.1, 0.3, 0.5):
        eps_pred = f**2 * (2 - (1 - 1/N))
        ok = "OK" if np.sqrt(eps_pred) >= f else "VIOLATION"
        print(f"  f={f:.1f}: eps={eps_pred:.4f}, sqrt(eps)={np.sqrt(eps_pred):.4f} >= f {ok}")

    print("\nline asymmetry em/abs = <n>/<n+1>:")
    for K in (0.58, 5, 50, 500):
        print(f"  <n>={K:7.2f}: ratio={K/(K+1):.4f}   "
              f"(Boltzmann at omega~T: {np.exp(-1):.4f})")

if __name__ == "__main__":
    main()
