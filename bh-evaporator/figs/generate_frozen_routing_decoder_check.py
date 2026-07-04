"""Direct two-copy Yoshida-Kitaev decoder simulation for the frozen-routing
witness instance (L=6, m=4, T=24, emissions at 14/17/20/23).

Closes limitation (v) of paper_frozen_routing_witness: replaces the
optimal-decoder achievability proxy with the protocol's own number.

Registers (22 qubits):
  0        A       reference, EPR with diary at copy-1 site 1
  1-6      copy 1  chain, evolves U (brickwork CZ + Haar 1q)
  7-12     copy 2  chain, evolves U* (conjugate gates, same schedule)
  13       D'      decoder's fresh EPR partner (teleportation target),
                   EPR with copy-2 site 1
  14-17    R       copy-1 records (swapped out of site 6)
  18-21    R'      copy-2 records (same schedule)

Initial entanglement: copy-1 sites 2-6 EPR with copy-2 sites 2-6
(the "old black hole" resource).  Decoder: project each (R_i, R'_i)
pair onto Phi+; post-selection probability P = squared norm; recovered
diary fidelity F_YK = <Phi+| rho_{A,D'} |Phi+>.
"""

import numpy as np

L, M, T = 6, 4, 24
REC_AT = (14, 17, 20, 23)
N_SEEDS = 12

A = 0
C1 = list(range(1, 7))
C2 = list(range(7, 13))
DP = 13
R1 = list(range(14, 18))
R2 = list(range(18, 22))
NQ = 22

ODD = [(i, i + 1) for i in (1, 3, 5)]
EVEN = [(i, i + 1) for i in (2, 4)]

H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
PHI = np.array([1, 0, 0, 1]).reshape(2, 2) / np.sqrt(2)


def haar_su2(rng):
    z = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(z)
    return q * (np.diagonal(r) / np.abs(np.diagonal(r)))


def apply_1q(psi, u, q):
    psi = np.tensordot(u, psi, axes=([1], [q]))
    return np.moveaxis(psi, 0, q)


def apply_cz(psi, q1, q2):
    idx = [slice(None)] * psi.ndim
    idx[q1] = 1
    idx[q2] = 1
    psi = psi.copy()
    psi[tuple(idx)] *= -1.0
    return psi


def cnot(psi, a, b):
    psi = apply_1q(psi, H, b)
    psi = apply_cz(psi, a, b)
    return apply_1q(psi, H, b)


def initial_state():
    psi = np.zeros((2,) * NQ, dtype=complex)
    psi[(0,) * NQ] = 1.0
    pairs = [(A, C1[0])] + [(C1[i], C2[i]) for i in range(1, 6)] + [(DP, C2[0])]
    for a, b in pairs:
        psi = apply_1q(psi, H, a)
        psi = cnot(psi, a, b)
    return psi


def run(seed, frozen):
    rng = np.random.default_rng(seed)
    psi = initial_state()
    n_em = 0
    for t in range(1, T + 1):
        for i in range(6):
            u = haar_su2(rng)
            psi = apply_1q(psi, u, C1[i])
            psi = apply_1q(psi, u.conj(), C2[i])
        # edges are chain positions 1..6, mapped to both copies
        if not frozen:
            for a, b in ODD if t % 2 else EVEN:
                psi = apply_cz(psi, C1[a - 1], C1[b - 1])
                psi = apply_cz(psi, C2[a - 1], C2[b - 1])  # CZ real: conj = CZ
        if t in REC_AT and n_em < M:
            psi = np.swapaxes(psi, C1[5], R1[n_em])
            psi = np.swapaxes(psi, C2[5], R2[n_em])
            n_em += 1

    # decoder: project (R_i, R'_i) onto Phi+, tracking axis shifts
    labels = list(range(NQ))
    for i in range(M):
        a1, a2 = labels.index(R1[i]), labels.index(R2[i])
        psi = np.tensordot(PHI.conj(), psi, axes=([0, 1], [a1, a2]))
        labels.pop(max(a1, a2))
        labels.pop(min(a1, a2))
    p_success = float(np.real(np.vdot(psi, psi)))
    psi = psi / np.sqrt(p_success)

    keep = [labels.index(A), labels.index(DP)]
    traced = [i for i in range(psi.ndim) if i not in keep]
    m = np.transpose(psi, keep + traced).reshape(4, -1)
    rho = m @ m.conj().T
    phi4 = PHI.reshape(4)
    f_yk = float(np.real(phi4.conj() @ rho @ phi4))
    return f_yk, p_success


if __name__ == "__main__":
    for frozen in (False, True):
        fs, ps = zip(*[run(1000 + s, frozen) for s in range(N_SEEDS)])
        arm = "frozen" if frozen else "normal"
        print(
            f"{arm:7s}  F_YK = {np.mean(fs):.3f} +/- {np.std(fs):.3f}   "
            f"P_success = {np.mean(ps):.3f} +/- {np.std(ps):.3f}"
        )
