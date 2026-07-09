"""Support numeric for notes/collective_channel_starvation_result.md.

Single bosonic mode b' (the collective channel) with two Lindblad couplings:
  - internal refill bath: rate G_th, thermal occupation nbar_T;
  - radiation drain:      rate G_out, zero incoming occupation.

Verifies, against exact dense-Liouvillian steady states and time evolution:
  1. steady occupation      n* = G_th nbar_T / (G_th + G_out)          [exact]
  2. steady state is thermal/geometric with parameter n* (so the line
     asymmetry is r* = n*/(n*+1)) and the KMS deficit is
         1 - r*/r_KMS = x / (nbar_T + 1 + x),   x = G_out/G_th        [exact]
  3. g2(0) = 2 exactly in the steady state AND along the starving flash
     (G_th = 0, initial thermal occupation draining away): Gaussianity is
     starvation-blind, only the asymmetry moves.

Dense matrices, Fock cutoff; NumPy plus SciPy for time propagation.
"""

import numpy as np

CUT = 30  # Fock cutoff (occupations <= nbar_T ~ 0.58; thermal tail ~ e^{-30} negligible)


def ops(cut=CUT):
    n = np.arange(cut)
    a = np.zeros((cut, cut))
    a[n[:-1], n[:-1] + 1] = np.sqrt(n[1:])
    return a, a.T.copy(), np.diag(n.astype(float))


def liouvillian(G_th, nbar_T, G_out, cut=CUT):
    a, ad, _ = ops(cut)
    idm = np.eye(cut)

    def dissipator(L, rate):
        LdL = L.T.conj() @ L
        return rate * (np.kron(L.conj(), L)
                       - 0.5 * np.kron(idm, LdL)
                       - 0.5 * np.kron(LdL.T, idm))

    # vec(rho) with column stacking: vec(A rho B) = (B^T kron A) vec(rho)
    Lv = np.zeros((cut * cut, cut * cut))
    Lv += dissipator(a, G_th * (nbar_T + 1) + G_out)   # downward
    Lv += dissipator(ad, G_th * nbar_T)                # upward
    return Lv


def steady_state(Lv, cut=CUT):
    w, v = np.linalg.eig(Lv)
    k = np.argmin(np.abs(w))
    rho = v[:, k].reshape(cut, cut, order="F")
    rho = 0.5 * (rho + rho.T.conj())
    return (rho / np.trace(rho)).real


def moments(rho, cut=CUT):
    _, _, nop = ops(cut)
    n1 = np.trace(rho @ nop).real
    n2 = np.trace(rho @ nop @ nop).real
    g2 = (n2 - n1) / n1**2
    return n1, g2


def geometric_fidelity(rho, nstar, cut=CUT):
    p = np.diag(rho).real
    q = (nstar / (1 + nstar)) ** np.arange(cut) / (1 + nstar)
    offdiag = np.abs(rho - np.diag(np.diag(rho))).max()
    return np.abs(p - q).max(), offdiag


def main():
    beta_omega = 1.0
    nbar_T = 1.0 / (np.exp(beta_omega) - 1.0)  # ~0.5820
    r_kms = np.exp(-beta_omega)
    G_th = 1.0
    print(f"nbar_T = {nbar_T:.6f}, r_KMS = {r_kms:.6f}\n")

    print("steady state under drain (starved channel):")
    print(f"{'x=G_out/G_th':>13} {'n* num':>10} {'n* formula':>11} "
          f"{'g2':>8} {'deficit num':>12} {'deficit formula':>16} "
          f"{'max|dP|':>9} {'max offdiag':>12}")
    for x in (0.1, 0.5, 1.0, 3.0):
        Lv = liouvillian(G_th, nbar_T, x * G_th)
        rho = steady_state(Lv)
        n1, g2 = moments(rho)
        n_pred = G_th * nbar_T / (G_th + x * G_th)
        r_star = n1 / (n1 + 1)
        deficit = 1 - r_star / r_kms
        deficit_pred = x / (nbar_T + 1 + x)
        dp, od = geometric_fidelity(rho, n_pred)
        print(f"{x:13.2f} {n1:10.6f} {n_pred:11.6f} {g2:8.5f} "
              f"{deficit:12.6f} {deficit_pred:16.6f} {dp:9.2e} {od:12.2e}")

    print("\nflash (G_th = 0, drain only, initial thermal nbar_T at G_out=1):")
    print("asymmetry drifts down from KMS; g2 pinned at 2 throughout")
    Lv = liouvillian(0.0, nbar_T, 1.0)
    # initial thermal state
    p0 = (nbar_T / (1 + nbar_T)) ** np.arange(CUT) / (1 + nbar_T)
    rho = np.diag(p0)
    dt, steps_per = 0.02, 25
    prop = None
    print(f"{'t':>6} {'n(t)':>10} {'n formula':>10} {'r(t)':>9} "
          f"{'r/r_KMS':>9} {'g2':>8}")
    from scipy.linalg import expm  # noqa: PLC0415
    prop = expm(Lv * dt)
    vec = rho.flatten(order="F")
    for k in range(7):
        t = k * dt * steps_per
        r_mat = vec.reshape(CUT, CUT, order="F").real
        n1, g2 = moments(r_mat)
        n_pred = nbar_T * np.exp(-1.0 * t)
        r_t = n1 / (n1 + 1)
        print(f"{t:6.2f} {n1:10.6f} {n_pred:10.6f} {r_t:9.6f} "
              f"{r_t / r_kms:9.6f} {g2:8.5f}")
        for _ in range(steps_per):
            vec = prop @ vec


if __name__ == "__main__":
    main()
