# Planck-Mass Emergent-Gravity Access Pass

Date: 2026-07-05

Role: independent pass after `bec_crossover_access_litpass.md` and
`prototype_adjudication_directions.md`, focused on whether the
Planck-mass/Planck-length regime gives a useful route into emergent
gravity for the access-invariant program.

## Corpus status

I read the two Claude notes. I did not find the Dvali/BEC TeX sources
named there under `C:\Users\serge\Projects` or inside
`bh-evaporator`. The only directly relevant local arXiv source I found
was `bh-evaporator/.codex_tmp/arxiv_src/2206.03161/main.tex`
(`Black hole entropy and long strings`). The Dvali papers are cited in
the notes and current refs, but their TeX source folders do not appear
to be present locally.

This matters for attribution: the rank-one/memory-burden reading in the
Claude notes is plausible, but M1 should be done against the actual
2006.00011/2210.02312 Hamiltonians before drafting anything.

## Bottom line

The Planck mass is not a controlled asymptotic regime for our current
exponents. For a Schwarzschild black hole,

```text
S ~ N ~ (M/M_P)^2 ~ (R/l_P)^2 .
```

At `M ~ M_P`, `S ~ O(1)`, so `sigma = log N_eff / log S`,
Page/HP latency exponents, and large-N condensate arguments stop being
sharp. The safer framing is:

```text
Planck mass = endpoint where the operational-horizon large-S package
              loses parametric control,
not
Planck mass = the place where a clean exponent-level emergence theorem
              should be formulated.
```

The useful variable is the approach to that endpoint from `S >> 1`.
The question becomes whether degeneracy saturation, soft constituent
formation, and exterior access saturation co-emerge along that approach,
or whether they split into branches.

## Literature calibration

### N-portrait / critical condensate

Dvali-Gomez's N-portrait gives the cleanest Planck-mass scaling:
a black hole is a condensate of `N` soft gravitons with wavelength
`sqrt(N) l_P`, coupling `1/N`, and `N` equal to the entropy. The paper
itself says semiclassical black-hole physics is large-N quantum
physics. Thus `M ~ M_P` corresponds to `N ~ 1`, where the condensate
picture is no longer a semiclassical expansion. This supports using the
Planck point as a breakdown endpoint, not as a controlled derivation
point.

Sources: arXiv:1112.3359, arXiv:1207.4059, arXiv:1307.3458.

### Long-string / Planck-cell energy problem

Verlinde-Visser 2206.03161 is directly relevant to the phrase
"around Planck mass." If black-hole entropy is assigned to independent
Planck cells near the horizon, the energy is too large by `R/l_P`.
Their long-string/matrix-quantum-mechanics mechanism lowers both
excitation energy and effective degrees of freedom by the same factor.
This is a good entropy/energy motivation for emergent long degrees of
freedom, but it does not compute source-rank, HP latency, or an exterior
coupling algebra.

Source: local TeX at `.codex_tmp/arxiv_src/2206.03161/main.tex`;
arXiv:2206.03161.

### Saturon / retrieval corpus

The saturon line strongly occupies "black-hole-like thermodynamics
without gravity." It gives degeneracy saturation, inverse-size emission
energy, and Page-time-like retrieval. It still appears not to compute
our operational package: source Gram participation, newly deposited
diary HP latency, or commutant de-protection.

Sources: arXiv:2107.10616, arXiv:2112.00551, arXiv:2509.08049.

### Fast pre-scramblers

Kaikov 2210.02312 does not close our HP-latency axis. It defines
pre-scrambling as wavefunction diffusion over the Hilbert-space basis,
and tests the enhanced-memory-capacity prototype. It does not formulate
decoupling, recovery fidelity, exterior radiation side information, or
source-channel rank. It does, however, give a ready-made Hamiltonian
variant with master mode, memory sectors `K, K'`, and bounded couplings
that should be used in M1/M2.

Source: arXiv:2210.02312.

### Newer memory-burden direction

Dvali 2509.22540 is newer than the Claude notes and should be added to
M0. It extends memory burden from slow evaporation to swift response
under perturbations and explicitly advertises cold-boson table-top
tests. For us, this strengthens the case that memory burden is an
independent operational axis, not just a lifetime correction. It also
pushes against any casual claim that critical memory systems automatically
give HP-style rapid recovery of newly deposited information.

Source: arXiv:2509.22540.

## Claim discipline

Strong claim to pursue:

```text
Degeneracy saturation does not by itself imply access saturation.
The N-portrait/memory-burden and boundary-ETH pictures are distinct
operational branches that can be graded by source-rank, latency, and
radiation-coherence diagnostics.
```

Claims to avoid:

```text
The Dvali program is contradicted by our luminosity lemma.
```

The luminosity lemma is class-conditional. Coherent enhancement is
already an admitted escape branch. The result is a classification, not
a refutation.

Also avoid:

```text
Emergent gravity is born at exactly the Planck mass.
```

For this program, the controlled statement is that semiclassical
gravity-like operational behavior is a large-S package whose endpoint
is Planckian.

## Next work

1. Locate or redownload the missing TeX sources for arXiv:2006.00011,
   2210.02312, 2509.08049, and 2509.22540.
2. M1: compute the source Gram kernel for the memory-burden prototype.
   Bare reading: radiation couples through the master `a <-> b` channel,
   so `N_eff ~ 1`; check whether dressed/diagonalized jump operators
   generate a parametrically large effective rank.
3. M2: estimate newly deposited diary latency. Deposit into memory
   modes, route through the allowed `C_m` and `C_b` couplings, and
   compare the earliest recoverability from emitted records to
   `O(k + log S)`.
4. M3: build the matched incoherent-channel variant at the same density
   of states. Compare `N_eff`, HP latency, and a secondary
   Dicke/coherent-vs-incoherent radiation statistic.
5. Treat the Planck endpoint as finite-N diagnostics only. Run curves
   from moderate `N` down to `N ~ 1`, but do not interpret `N ~ 1`
   slopes as asymptotic exponents.

## Working thesis

The Planck-mass question is best reframed as a crossover question:
trans-Planckian attempts self-complete into soft many-body states;
large `S` gives thermodynamic and potentially operational horizon
behavior; the Planck point is where the large-N description ends. The
novel contribution available to this project is to test whether the
access package follows the degeneracy/softness package, or separates
from it.
