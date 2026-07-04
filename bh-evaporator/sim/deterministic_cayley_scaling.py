"""Deterministic Cayley-Hamiltonian decoupling: a finite-size scaling study.

This script tests, for a *single deterministic time-independent* Hamiltonian on a
Cayley (circulant) graph, whether the in-shell mixing it generates is enough to
reproduce the Page/island radiation-entropy curve of the evaporation model in
``paper_ideal_hamiltonian``.  It does NOT assume a Haar isometry (that is the
Section 5 check); it evolves the actual Hamiltonian ``exp(-i K t)`` and measures
the antecedent: does this H scramble enough to decouple the radiation?

Because the phenomenology claimed is asymptotic, the control variable is the
system size ``n`` (number of boundary cells / qubits).  For each ``n`` and each
Hamiltonian family we report:

  1. within-momentum-sector level statistics  <r>  (chaos: Poisson 0.386,
     GOE 0.531, GUE 0.600)         -- rules in/out integrability
  2. a spectral degeneracy / gap-commensurability metric
                                    -- tests the non-resonance hypothesis that
                                       the single-Hamiltonian (temporal-ensemble)
                                       decoupling argument relies on
  3. infinite-temperature OTOC saturation at a fixed scrambling time
                                    -- operator scrambling
  4. the Page/decoupling test: emit shells, evolve the shrinking core under
     exp(-i K t), and compare S_vN(radiation) with the island min
     min(S_emitted, S_remaining), plus old/new mutual information.

Three families are compared to map the counterexample landscape:

  * ``free_chain``  : cycle, XX+YY only (Jz=0, no field) -> genuinely Gaussian.
                      Counterexample 1: free dynamics, wrong (non-Page) curve.
  * ``integ_xxz``   : cycle, XXZ (no field) -> interacting but integrable.
                      The cycle-XXZ "warning example" of the paper.
  * ``chaos_expander``: circulant {1, n/2}, anisotropic XYZ + fields ->
                      chaotic candidate.  The positive case.

Exact diagonalization caps n; defaults run n in {6,8,10}, with n=12 opt-in.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import scipy.sparse as sp

# --------------------------------------------------------------------------- #
# Pauli / Hamiltonian construction (qubit 0 = most significant bit).
# --------------------------------------------------------------------------- #

_I2 = sp.identity(2, format="csr", dtype=complex)
_X = sp.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
_Y = sp.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
_Z = sp.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
_PAULI = {"X": _X, "Y": _Y, "Z": _Z}


def _embed(n: int, ops: dict[int, sp.csr_matrix]) -> sp.csr_matrix:
    """Kronecker-embed single-site operators into the n-qubit space."""
    mats = [ops.get(q, _I2) for q in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = sp.kron(out, m, format="csr")
    return out


def cayley_edges(n: int, generators: tuple[int, ...]) -> list[tuple[int, int]]:
    """Undirected edges of the circulant Cayley graph Cay(Z_n, {+-s})."""
    edges: set[frozenset[int]] = set()
    for g in range(n):
        for s in generators:
            h = (g + s) % n
            if h != g:
                edges.add(frozenset((g, h)))
    return [tuple(sorted(e)) for e in edges]


@dataclass(frozen=True)
class Family:
    name: str
    generators: tuple[int, ...]          # positive shifts; n//2 added at build for expander
    couplings: dict[int, tuple[float, float, float]]   # shift -> (Jx,Jy,Jz)
    hx: float
    hz: float
    use_half_generator: bool = False     # append n//2 to generators at build time
    long_coupling: tuple[float, float, float] = (0.9, 1.1, 0.5)  # for the n//2 bond


def family_generators(fam: Family, n: int) -> tuple[int, ...]:
    gens = list(fam.generators)
    if fam.use_half_generator and n % 2 == 0:
        gens.append(n // 2)
    return tuple(sorted(set(gens)))


def build_hamiltonian(n: int, fam: Family) -> np.ndarray:
    """Dense Hermitian Hamiltonian for family ``fam`` on n qubits."""
    gens = family_generators(fam, n)
    dim = 1 << n
    H = sp.csr_matrix((dim, dim), dtype=complex)

    for g in range(n):
        for s in gens:
            h = (g + s) % n
            if h == g:
                continue
            if g > h:  # count each undirected edge once
                continue
            jx, jy, jz = fam.couplings.get(s, fam.long_coupling)
            for J, P in ((jx, "X"), (jy, "Y"), (jz, "Z")):
                if J != 0.0:
                    H = H + J * _embed(n, {g: _PAULI[P], h: _PAULI[P]})

    for g in range(n):
        if fam.hx != 0.0:
            H = H + fam.hx * _embed(n, {g: _X})
        if fam.hz != 0.0:
            H = H + fam.hz * _embed(n, {g: _Z})

    return np.asarray(H.todense())


# --------------------------------------------------------------------------- #
# Symmetry-resolved level statistics (translation / momentum sector).
# --------------------------------------------------------------------------- #

def _cyclic_shift(b: int, n: int) -> int:
    """Shift the n-bit integer b by one site (qubit q -> q+1, MSB convention)."""
    # qubit 0 is the MSB (bit n-1).  A site shift q->q+1 is a rotate of the
    # n-bit word; the specific direction is irrelevant for sector statistics.
    return ((b << 1) & ((1 << n) - 1)) | (b >> (n - 1))


def momentum_sector_spectrum(H: np.ndarray, n: int, m: int) -> np.ndarray:
    """Eigenvalues of H restricted to translation-momentum sector m."""
    dim = 1 << n
    seen = np.zeros(dim, dtype=bool)
    columns: list[np.ndarray] = []
    for b in range(dim):
        if seen[b]:
            continue
        orbit = [b]
        nb = _cyclic_shift(b, n)
        while nb != b:
            orbit.append(nb)
            nb = _cyclic_shift(nb, n)
        d = len(orbit)
        for x in orbit:
            seen[x] = True
        # Bloch state exists in sector m iff exp(-2pi i m d / n) == 1.
        if (m * d) % n != 0:
            continue
        vec = np.zeros(dim, dtype=complex)
        for j, x in enumerate(orbit):
            vec[x] += np.exp(-2j * np.pi * m * j / n)
        vec /= np.linalg.norm(vec)
        columns.append(vec)
    if len(columns) < 4:
        return np.array([])
    B = np.column_stack(columns)
    Hm = B.conj().T @ H @ B
    Hm = 0.5 * (Hm + Hm.conj().T)
    return np.linalg.eigvalsh(Hm)


def r_statistic(evals: np.ndarray) -> float:
    """Mean adjacent-gap ratio <r> = <min(s_i,s_{i+1})/max(...)>."""
    evals = np.sort(evals)
    gaps = np.diff(evals)
    gaps = gaps[gaps > 1e-12]
    if len(gaps) < 3:
        return float("nan")
    r = np.minimum(gaps[:-1], gaps[1:]) / np.maximum(gaps[:-1], gaps[1:])
    return float(np.mean(r))


def degeneracy_and_commensurability(evals: np.ndarray) -> tuple[float, float]:
    """Fraction of near-zero spacings (degeneracy) and a gap-collision score.

    The gap-collision score is the fraction of distinct consecutive spacings
    that fall within tolerance of another spacing -- high for commensurate /
    resonant spectra (which spoil the temporal-ensemble decoupling argument),
    low for a generic chaotic spectrum.
    """
    evals = np.sort(evals)
    gaps = np.diff(evals)
    if len(gaps) < 4:
        return float("nan"), float("nan")
    width = evals[-1] - evals[0]
    tol = 1e-9 * width
    degeneracy = float(np.mean(gaps < tol))
    s = gaps[gaps > tol]
    s = s / np.mean(s)
    # bucket normalized spacings; commensurate spectra pile into few buckets
    buckets = np.round(s / 0.02)
    _, counts = np.unique(buckets, return_counts=True)
    collision = float(1.0 - len(counts) / len(s))
    return degeneracy, collision


# --------------------------------------------------------------------------- #
# Exact propagator, entropies, OTOC.
# --------------------------------------------------------------------------- #

def propagator(H: np.ndarray, t: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    evals, evecs = np.linalg.eigh(H)
    U = (evecs * np.exp(-1j * evals * t)) @ evecs.conj().T
    return U, evals, evecs


def evolve(H: np.ndarray, t: float, M: np.ndarray) -> np.ndarray:
    """Apply exp(-iHt) to the columns of M without materializing the propagator."""
    evals, evecs = np.linalg.eigh(H)
    phase = np.exp(-1j * evals * t)
    return evecs @ (phase[:, None] * (evecs.conj().T @ M))


def subset_entropy(psi: np.ndarray, n: int, keep: list[int]) -> float:
    """von Neumann entropy (nats) of the reduced state on qubit subset ``keep``."""
    if not keep or len(keep) == n:
        return 0.0
    t = psi.reshape([2] * n)
    rest = [q for q in range(n) if q not in keep]
    t = np.transpose(t, keep + rest).reshape(1 << len(keep), 1 << len(rest))
    s = np.linalg.svd(t, compute_uv=False)
    p = s ** 2
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))


def infinite_temp_otoc(evals: np.ndarray, evecs: np.ndarray, n: int,
                       i: int, j: int, t: float) -> float:
    """C(t) = 1 - Re Tr[Z_i(t) Z_j Z_i(t) Z_j] / 2^n  at infinite temperature."""
    dim = 1 << n
    Zi = np.where((np.arange(dim)[:, None] >> (n - 1 - i)) & 1, -1.0, 1.0).ravel()
    Zj = np.where((np.arange(dim) >> (n - 1 - j)) & 1, -1.0, 1.0)
    U = (evecs * np.exp(-1j * evals * t)) @ evecs.conj().T
    Ud = U.conj().T
    # Z_i(t) = U^dag Z_i U  (diagonal Z_i)
    Zit = Ud @ (Zi[:, None] * U)
    M = Zit @ np.diag(Zj) @ Zit @ np.diag(Zj)
    val = np.real(np.trace(M)) / dim
    return float(max(0.0, min(1.0, (1.0 - val) / 2.0)))


# --------------------------------------------------------------------------- #
# Page / decoupling test with exact Hamiltonian dynamics.
# --------------------------------------------------------------------------- #

def apply_core_unitary(psi: np.ndarray, n: int, c: int, U_core: np.ndarray) -> np.ndarray:
    """Apply U_core (acting on leading qubits 0..c-1) to the full state."""
    M = psi.reshape(1 << c, 1 << (n - c))
    return (U_core @ M).ravel()


def page_expectation(d_a: int, d_b: int) -> float:
    """Exact Page-formula expected entanglement entropy (nats) for a Haar
    pure state on d_a x d_b, the analytic island-min reference."""
    a, b = min(d_a, d_b), max(d_a, d_b)
    harmonic = sum(1.0 / k for k in range(b + 1, a * b + 1))
    return harmonic - (a - 1) / (2.0 * b)


@dataclass
class PageStep:
    step: int
    core_before: int
    core_after: int
    rad_qubits: int
    s_rad: float
    page_min: float
    s_rad_minus_pagemin: float
    old_new_mi: float


def page_test(fam: Family, n: int, block: int, t_mix: float, seed: int,
              mode: str = "hamiltonian") -> list[PageStep]:
    """Emit `block` qubits per step, scrambling the shrinking core each step.

    mode: 'hamiltonian' (deterministic exp(-iKt)), 'haar' (Page reference),
          'none' (no scrambling control).
    """
    rng = np.random.default_rng(90000 + seed)
    # Random PRODUCT state: no pre-existing core/radiation entanglement, so any
    # radiation entropy must be generated by the dynamics.  This makes 'none' a
    # genuine control (S_rad stays 0) instead of inheriting Haar entanglement.
    psi = np.array([1.0 + 0j])
    for _ in range(n):
        a = rng.normal(size=2) + 1j * rng.normal(size=2)
        a /= np.linalg.norm(a)
        psi = np.kron(psi, a)

    # warm up the full register once so the initial state is shell-typical
    if mode == "hamiltonian":
        H_full = build_hamiltonian(n, fam)
        psi = evolve(H_full, t_mix, psi[:, None]).ravel()

    steps: list[PageStep] = []
    c = n
    s = 0
    while c - block >= 1:
        if mode == "hamiltonian":
            Hc = build_hamiltonian(c, fam)
            psi = evolve(Hc, t_mix, psi.reshape(1 << c, 1 << (n - c))).ravel()
        elif mode == "haar":
            z = (rng.normal(size=(1 << c, 1 << c))
                 + 1j * rng.normal(size=(1 << c, 1 << c)))
            q, r = np.linalg.qr(z)
            U_core = q * (np.diag(r) / np.abs(np.diag(r)))
            psi = apply_core_unitary(psi, n, c, U_core)
        # mode == "none": identity, leave psi unchanged

        c_after = c - block
        rad = list(range(c_after, n))            # emitted so far
        new = list(range(c_after, c))            # this step's emission
        old = list(range(c, n))                  # previously emitted
        s_rad = subset_entropy(psi, n, rad)
        s_old = subset_entropy(psi, n, old)
        s_new = subset_entropy(psi, n, new)
        mi = s_old + s_new - s_rad
        page_min = min(len(rad), c_after) * math.log(2.0)
        steps.append(PageStep(
            step=s, core_before=c, core_after=c_after, rad_qubits=len(rad),
            s_rad=s_rad, page_min=page_min,
            s_rad_minus_pagemin=s_rad - page_min, old_new_mi=mi,
        ))
        c = c_after
        s += 1
    return steps


# --------------------------------------------------------------------------- #
# Families and driver.
# --------------------------------------------------------------------------- #

FAMILIES = {
    "free_chain": Family(
        name="free_chain", generators=(1,),
        couplings={1: (1.0, 1.0, 0.0)}, hx=0.0, hz=0.0),
    "integ_xxz": Family(
        name="integ_xxz", generators=(1,),
        couplings={1: (1.0, 1.0, 0.8)}, hx=0.0, hz=0.0),
    "chaos_expander": Family(
        name="chaos_expander", generators=(1,), use_half_generator=True,
        couplings={1: (1.0, 0.6, 1.4)}, long_coupling=(0.9, 1.1, 0.5),
        hx=0.55, hz=0.31),
}


@dataclass(frozen=True)
class ScalingRow:
    family: str
    n: int
    sector_m: int
    sector_levels: int
    r_stat: float
    degeneracy: float
    gap_collision: float
    otoc_sat: float
    otoc_time: float
    page_vs_haar: float       # max_step |S_rad(Hamiltonian) - S_rad(Haar)|  -- THE test
    page_final_mi: float
    page_max_mi: float
    haar_vs_min: float        # Haar finite-size Page floor (reference)
    none_vs_min: float        # no-scramble failure scale


def run_family(name: str, n: int, t_otoc: float, t_mix: float,
               otoc_max_n: int) -> ScalingRow:
    fam = FAMILIES[name]

    H = build_hamiltonian(n, fam)

    m = 1 if n > 2 else 0
    spec = momentum_sector_spectrum(H, n, m)
    r = r_statistic(spec) if spec.size else float("nan")
    deg, coll = (degeneracy_and_commensurability(spec)
                 if spec.size else (float("nan"), float("nan")))

    if n <= otoc_max_n:
        evals, evecs = np.linalg.eigh(H)
        otoc = infinite_temp_otoc(evals, evecs, n, 0, n // 2, t_otoc)
    else:
        otoc = float("nan")

    ham = page_test(fam, n, block=2, t_mix=t_mix, seed=0, mode="hamiltonian")
    haar = page_test(fam, n, block=2, t_mix=t_mix, seed=0, mode="haar")
    none = page_test(fam, n, block=2, t_mix=t_mix, seed=0, mode="none")

    def max_dev(steps: list[PageStep]) -> float:
        return max(abs(s.s_rad_minus_pagemin) for s in steps)

    page_vs_haar = max(abs(h.s_rad - g.s_rad) for h, g in zip(ham, haar))

    return ScalingRow(
        family=name, n=n, sector_m=m, sector_levels=spec.size,
        r_stat=r, degeneracy=deg, gap_collision=coll,
        otoc_sat=otoc, otoc_time=t_otoc,
        page_vs_haar=page_vs_haar,
        page_final_mi=ham[-1].old_new_mi,
        page_max_mi=max(s.old_new_mi for s in ham),
        haar_vs_min=max_dev(haar),
        none_vs_min=max_dev(none),
    )


def seed_scan(sizes: tuple[int, ...] = (6, 8, 10),
              seeds: tuple[int, ...] = tuple(range(8)),
              t_mix: float = 5.0) -> None:
    """Seed-averaged convergence of S_rad(Hamiltonian) to the analytic Page
    formula, with the Haar isometry's own deviation as the reference floor."""
    print(f"{'family':16s}{'n':>3s}{'mean|S_ham-Page|':>18s}{'std':>7s}"
          f"{'mean|S_haar-Page|':>19s}")
    print("-" * 63)
    rows = []
    for name in ("free_chain", "integ_xxz", "chaos_expander"):
        fam = FAMILIES[name]
        for n in sizes:
            ham_devs, haar_devs = [], []
            for s in seeds:
                ham = page_test(fam, n, block=2, t_mix=t_mix, seed=s,
                                mode="hamiltonian")
                haar = page_test(fam, n, block=2, t_mix=t_mix, seed=s,
                                 mode="haar")
                mdev = lambda st: max(
                    abs(x.s_rad - page_expectation(1 << x.rad_qubits,
                                                   1 << x.core_after))
                    for x in st)
                ham_devs.append(mdev(ham))
                haar_devs.append(mdev(haar))
            print(f"{name:16s}{n:3d}{np.mean(ham_devs):18.3f}"
                  f"{np.std(ham_devs):7.3f}{np.mean(haar_devs):19.3f}")
            rows.append({"family": name, "n": n,
                         "ham_dev_mean": np.mean(ham_devs),
                         "ham_dev_std": np.std(ham_devs),
                         "haar_dev_mean": np.mean(haar_devs),
                         "seeds": len(seeds)})
        print()
    out = Path(__file__).resolve().parent / "data" / "deterministic_cayley_seed_scan.csv"
    with out.open("w", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {out}")


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    sizes = [6, 8, 10]          # set INCLUDE_12=True for n=12 (slow)
    include_12 = False
    if include_12:
        sizes.append(12)

    t_otoc = 4.0
    t_mix = 5.0
    otoc_max_n = 10

    rows: list[ScalingRow] = []
    header = (f"{'family':16s}{'n':>3s}{'<r>':>8s}{'deg':>7s}{'coll':>7s}"
              f"{'OTOC':>7s}{'ham-Haar':>9s}{'finalMI':>9s}"
              f"{'HaarFloor':>10s}{'noneFail':>9s}")
    print(header)
    print("-" * len(header))
    for name in ("free_chain", "integ_xxz", "chaos_expander"):
        for n in sizes:
            row = run_family(name, n, t_otoc, t_mix, otoc_max_n)
            rows.append(row)
            print(f"{row.family:16s}{row.n:3d}{row.r_stat:8.3f}"
                  f"{row.degeneracy:7.3f}{row.gap_collision:7.3f}"
                  f"{row.otoc_sat:7.3f}{row.page_vs_haar:9.3f}"
                  f"{row.page_final_mi:9.3f}{row.haar_vs_min:10.3f}"
                  f"{row.none_vs_min:9.3f}")
        print()

    out_path = out_dir / "deterministic_cayley_scaling.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ScalingRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    print(f"wrote {out_path}")
    print("\nReference <r>: Poisson 0.386, GOE 0.531, GUE 0.600")
    print("Discriminator: ham-Haar small (<< noneFail) + finalMI>0")
    print("  => the deterministic Hamiltonian decouples like a Haar isometry")
    print("     (reproduces the island min); noneFail = no-scramble failure scale.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "seed":
        seed_scan()
    else:
        main()
