"""Support figures for paper_frozen_routing_witness.

Figure 1 (fig_arms.pdf):      protocol schedule schematic, normal vs frozen arm.
Figure 2 (fig_signature.pdf): predicted witness signature from an exact
                              statevector simulation of the L=6 instance
                              (ideal gates; hardware envelopes enter the
                              paper's budget, not this figure).

Simulation model (single copy + purifications, information-theoretic):
  qubit 0        reference A, maximally entangled with the diary
  qubits 1..6    routing chain; diary enters at site 1, access at site 6
  records        fresh ancillas swapped out of site 6 at scheduled depths
  qubits (E)     partners purifying chain sites 2..6 ("old" resource)

Dynamics: brickwork of CZ on alternating bulk edges + Haar-random
single-qubit gates each layer.  Frozen arm: identical schedule and
identical single-qubit gates, CZ layers replaced by identity.

Reported quantities (both rigorous):
  achievable:  F(rho_AC, rho_A x rho_C)^2  -- decoupling/Uhlmann
               achievability of recovery from records+E
  upper bound: 1/4 + ||rho_ARE - rho_A x rho_RE||_1 / 2
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "paper_frozen_routing_witness"

# ----------------------------------------------------------------- gates


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


def apply_swap(psi, q1, q2):
    return np.swapaxes(psi, q1, q2)


# ------------------------------------------------------- reduced states


def rho_keep(psi, keep):
    n = psi.ndim
    traced = [q for q in range(n) if q not in keep]
    order = list(keep) + traced
    a = np.transpose(psi, order).reshape(2 ** len(keep), 2 ** len(traced))
    return a @ a.conj().T


def trace_distance(r, s):
    ev = np.linalg.eigvalsh(r - s)
    return np.sum(np.abs(ev))


def fidelity(r, s):
    er, vr = np.linalg.eigh(r)
    er = np.clip(er, 0, None)
    sq = (vr * np.sqrt(er)) @ vr.conj().T
    ev = np.linalg.eigvalsh(sq @ s @ sq)
    return np.sum(np.sqrt(np.clip(ev, 0, None))) ** 2


# ------------------------------------------------------------ protocol

L = 6
M_REC = 4
T = 24
REC_AT = (14, 17, 20, 23)
N_SEEDS = 12

A = 0
CHAIN = list(range(1, L + 1))
REC = list(range(L + 1, L + 1 + M_REC))
ENV = list(range(L + 1 + M_REC, L + 1 + M_REC + (L - 1)))
NQ = 1 + L + M_REC + (L - 1)

ODD_EDGES = [(CHAIN[i], CHAIN[i + 1]) for i in range(0, L - 1, 2)]
EVEN_EDGES = [(CHAIN[i], CHAIN[i + 1]) for i in range(1, L - 1, 2)]


def initial_state():
    psi = np.zeros((2,) * NQ, dtype=complex)
    psi[(0,) * NQ] = 1.0
    h = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    cx_pairs = [(A, CHAIN[0])] + list(zip(CHAIN[1:], ENV))
    for a, b in cx_pairs:
        psi = apply_1q(psi, h, a)
        # CNOT a->b via H_b CZ H_b
        psi = apply_1q(psi, h, b)
        psi = apply_cz(psi, a, b)
        psi = apply_1q(psi, h, b)
    return psi


def run_arm(seed, frozen):
    rng = np.random.default_rng(seed)
    psi = initial_state()
    n_emitted = 0
    ach, up = [], []
    for t in range(1, T + 1):
        for q in CHAIN:
            psi = apply_1q(psi, haar_su2(rng), q)
        if not frozen:
            for q1, q2 in ODD_EDGES if t % 2 else EVEN_EDGES:
                psi = apply_cz(psi, q1, q2)
        else:
            # draw and discard so both arms share the 1q randomness stream
            _ = [haar_su2(rng) for _ in (ODD_EDGES if t % 2 else EVEN_EDGES)]
        if t in REC_AT and n_emitted < M_REC:
            psi = apply_swap(psi, CHAIN[-1], REC[n_emitted])
            n_emitted += 1

        rac = rho_keep(psi, [A] + CHAIN)
        ra = rho_keep(psi, [A])
        rc = rho_keep(psi, CHAIN)
        ach.append(fidelity(rac, np.kron(ra, rc)) ** 2)

        rare = rho_keep(psi, [A] + REC + ENV)
        rre = rho_keep(psi, REC + ENV)
        up.append(min(1.0, 0.25 + 0.5 * trace_distance(rare, np.kron(ra, rre))))
    return np.array(ach), np.array(up)


def simulate():
    cache = OUT / "signature_data.npz"
    if cache.exists():
        z = np.load(cache)
        if z["T"] == T and z["m"] == M_REC and z["seeds"] == N_SEEDS:
            print("loaded cached simulation data")
            return {
                "normal": (z["na"], z["nu"]),
                "frozen": (z["fa"], z["fu"]),
            }
    res = {}
    for arm in ("normal", "frozen"):
        a = np.zeros((N_SEEDS, T))
        u = np.zeros((N_SEEDS, T))
        for s in range(N_SEEDS):
            a[s], u[s] = run_arm(1000 + s, frozen=(arm == "frozen"))
        res[arm] = (a, u)
        print(
            f"{arm:7s}  achievable(final) = {a[:, -1].mean():.3f} "
            f"+/- {a[:, -1].std():.3f}   upper(final) = {u[:, -1].mean():.3f}"
        )
    np.savez(
        cache,
        T=T, m=M_REC, seeds=N_SEEDS,
        na=res["normal"][0], nu=res["normal"][1],
        fa=res["frozen"][0], fu=res["frozen"][1],
    )
    return res


# ------------------------------------------------------------- figures

BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e6e5e1"


def style_ax(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK2)
    ax.tick_params(colors=INK2, labelsize=8)
    ax.yaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)


def fig_signature(res):
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    t = np.arange(1, T + 1)

    for arm, color in (("normal", BLUE), ("frozen", ORANGE)):
        a, u = res[arm]
        if arm == "normal":
            # optimal recovery >= max(decoupling bound, trivial 1/4):
            # floor at the baseline attained by discard-and-reprepare
            af = np.maximum(a, 0.25)
            ax.plot(t, af.mean(0), color=color, lw=1.8, label="normal: achievable")
            ax.fill_between(
                t,
                np.maximum(a.mean(0) - a.std(0), 0.25),
                np.maximum(a.mean(0) + a.std(0), 0.25),
                color=color, alpha=0.15, lw=0,
            )
        ax.plot(
            t,
            u.mean(0),
            color=color,
            lw=1.6,
            ls="--",
            label=f"{arm}: upper bound",
        )
        ax.fill_between(
            t, u.mean(0) - u.std(0), u.mean(0) + u.std(0), color=color, alpha=0.12, lw=0
        )

    ax.axhline(0.25, color=INK2, lw=1.0, ls=":")
    ax.text(T + 0.15, 0.25, "trivial\nbaseline 1/4", fontsize=7.5, color=INK2, va="center")
    for d in REC_AT:
        ax.axvline(d, color=GRID, lw=0.8)
    ax.text(REC_AT[0], 1.035, "record emissions", fontsize=7.5, color=INK2, ha="left")

    ax.set_xlabel("circuit depth $t$ (brickwork layers)", fontsize=9, color=INK)
    ax.set_ylabel(r"recovery fidelity $F^{e}_{\mathrm{rec}}$", fontsize=9, color=INK)
    ax.set_xlim(1, T)
    ax.set_ylim(0, 1.05)
    style_ax(ax)
    ax.legend(frameon=False, fontsize=8, loc="center left")
    fig.tight_layout()
    fig.savefig(OUT / "fig_signature.pdf")
    plt.close(fig)


def fig_arms():
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.2), sharey=True)
    rows = {}
    labels = []
    y = 0
    for name in (
        ["$A$ (reference)"]
        + [f"site {i}" for i in range(1, L + 1)]
        + [f"$R_{i}$" for i in range(1, M_REC + 1)]
    ):
        rows[name] = y
        labels.append(name)
        y += 1
    site_row = lambda i: rows[f"site {i}"]

    for ax, frozen in zip(axes, (False, True)):
        ax.set_title("frozen arm" if frozen else "normal arm", fontsize=9.5, color=INK)
        # wires
        for name, ry in rows.items():
            ax.plot([0, T + 1], [ry, ry], color=GRID, lw=0.8, zorder=0)
        # stage 0: diary entanglement marker
        ax.plot([0.3, 0.3], [rows["$A$ (reference)"], site_row(1)], color=INK2, lw=1.2)
        ax.scatter([0.3, 0.3], [rows["$A$ (reference)"], site_row(1)], s=8, color=INK2)
        n_emitted = 0
        for t in range(1, T + 1):
            for i in range(1, L + 1):  # 1q gates
                ax.add_patch(
                    plt.Rectangle(
                        (t - 0.18, site_row(i) - 0.18), 0.36, 0.36,
                        facecolor="#c3c2b7", edgecolor="none", zorder=2,
                    )
                )
            edges = ODD_EDGES if t % 2 else EVEN_EDGES
            for q1, q2 in edges:
                i1, i2 = CHAIN.index(q1) + 1, CHAIN.index(q2) + 1
                if frozen:
                    ax.plot(
                        [t, t], [site_row(i1), site_row(i2)],
                        color=ORANGE, lw=1.4, ls=(0, (1.5, 1.5)), zorder=1,
                    )
                else:
                    ax.plot([t, t], [site_row(i1), site_row(i2)], color=BLUE, lw=1.8, zorder=3)
                    ax.scatter(
                        [t, t], [site_row(i1), site_row(i2)], s=7, color=BLUE, zorder=3
                    )
            if t in REC_AT and n_emitted < M_REC:
                ry = rows[f"$R_{n_emitted + 1}$"]
                ax.plot([t, t], [site_row(L), ry], color="#008300", lw=1.8, zorder=3)
                ax.scatter([t], [ry], s=16, color="#008300", marker="x", zorder=3)
                n_emitted += 1
        ax.set_xlim(-0.4, T + 1.2)
        ax.set_ylim(-0.8, len(rows) - 0.2)
        ax.invert_yaxis()
        ax.set_xlabel("layer", fontsize=8.5, color=INK2)
        ax.set_xticks([1, 5, 10, 15])
        ax.tick_params(colors=INK2, labelsize=8)
        for s in ax.spines.values():
            s.set_visible(False)
    axes[0].set_yticks(range(len(labels)))
    axes[0].set_yticklabels(labels, fontsize=8, color=INK)
    axes[1].text(
        T * 0.45, len(rows) - 0.55,
        "dotted = skipped (couplers parked)",
        fontsize=7.5, color=ORANGE, ha="center",
    )
    axes[0].text(
        T * 0.45, len(rows) - 0.55,
        "record coupling identical in both arms",
        fontsize=7.5, color="#008300", ha="center",
    )
    fig.tight_layout()
    fig.savefig(OUT / "fig_arms.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig_arms()
    res = simulate()
    fig_signature(res)
    print("wrote", OUT / "fig_arms.pdf", "and", OUT / "fig_signature.pdf")
