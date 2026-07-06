# Coherence Witness: Per-Resolved-Mode g2 Separates the Strict Branches (Q1 Answer)

Date: 2026-07-05

Role: answers Q1 of the results-first ordering (is the
coherent-single-source vs incoherent-entropy-rank fork passively
exterior-visible, and does semiclassical thermality already vote?).
Analytic; specific resolved-vs-broadband numeric support target
identified but not yet run. Verification grading marked per claim.

## Result

Per-resolved-mode photon counting statistics of the emission line
separates the strict sharp-master branch from the ETH-Gaussian/thermal
branch at O(1):

```text
strict coherent prototype (master-mode depletion):
    g2(0) = 1 - 1/S          [exact, see derivation]

incoherent rank-S ETH-Gaussian register (golden-rule limit):
    g2(0) = 2                [textbook: Gaussian/chaotic light]

semiclassical Hawking mode (exterior reduction of squeezed pair):
    g2(0) = 2                [textbook: thermal state per mode]
```

The statistic is compression-proof only in the resolved-mode sense: it
is a property of the one resolved line, not of mode counts, so the
section 5.5 shared-mode obstruction does not apply to that line.  It is
not broadband-proof: tag multiplexing can fake bunching when several
detuned conditional lines are integrated together.  The static exterior
certificate suite was two-legged as first written: g2 distinguishes
coherence class; the latency exponent distinguishes rank within the
incoherent class.  Neither alone does both.  [Superseded same day:
`statistics_rank_link_result.md` (lemma 3b) adds a probe-level third
rung — line asymmetry, em/abs versus the Boltzmann ratio — making the
operational ladder three-runged by cost: passive g2, probe line
asymmetry, deposit-and-decode latency.]

## Derivation (coherent branch)

Strict-decay variant of the prototype (the F-species footnote of
2006.00011): a0 with initial Fock occupation N = n0 = S, bilinear
coupling to a continuum. Amplitude damping of a Fock state gives at
transmitted fraction eta a binomial mixture Binom(N, eta') in the
source and the emitted beam inherits normally-ordered source
statistics (input-output). For a binomial,

```text
<m(m-1)> / <m>^2 = 1 - 1/N,   independent of eta.
```

Hence g2(0) = 1 - 1/S throughout the unburdened decay stage. [Exact
combinatorics; input-output step is standard quantum optics —
VERIFY textbook citation (Loudon / Walls-Milburn) before ink.]

Dephasing robustness: the master-memory coupling is number-number;
pure phase/frequency tagging does not change photon-number statistics
at zero delay. [Standard.]

Burdened-stage caveat: with the memory sector in a mixture, the
burden-dependent detuning makes the emission RATE sector-dependent; a
classical mixture of Poissonian beams has g2 > 1 (bounded by the rate
spread). So burden onset drifts g2 upward — itself an exterior-visible
signature — but by rate-mixture bunching, mechanistically distinct
from chaotic g2 = 2. [Inference; quantify only if needed.]

## Derivation (incoherent branch)

Rank-S source: the line amplitude is a sum of ~S independent weak
ETH-random channels; central limit ⇒ Gaussian field ⇒ chaotic light,
g2(0) = 2 by the Gaussian moment theorem. [Textbook.]

## Semiclassical anchor

Each exterior Hawking mode is the partial trace of a two-mode squeezed
vacuum = exactly thermal ⇒ chaotic per-mode statistics, g2(0) = 2.
Stimulated-emission response thermal (Bekenstein-Meisels 1977,
Panangaden-Wald 1977). [Anchor refs identified 2026-07-05:
Bekenstein--Meisels, "Einstein A and B coefficients for a black
hole," Phys. Rev. D 15, 2775; Panangaden--Wald, "Probability
distribution for radiation from a black hole in the presence of
incoming radiation," Phys. Rev. D 16, 929.  Verify any formula-level
quote before paper text. Note analogue-gravity experiments probe pair
correlations, not directly exterior g2 — do not overclaim
experimental status.]

## Conclusions

1. Q1 answer: YES — the fork is passively exterior-visible via g2.
2. The semiclassical vote: per-mode Hawking thermality (g2 = 2) is
   inconsistent with the STRICT coherent prototype (g2 ≈ 1) at O(1),
   not Planck-suppressed.
3. Calibrated statement (fork-not-refutation discipline): this is OUR
   inference from THEIR strict Hamiltonian. The dressed N-portrait
   invokes 1/N rescattering for the thermal SPECTRUM; the corpus
   contains no statistics (g2) computation (M0 search). Whether
   rescattering restores g2 = 2 is open and is that branch's
   obligation. Possible outcomes: (a) it does — then the coherent
   branch mimics chaotic statistics and the static certificate loses
   power (latency remains); (b) it does not — the coherent branch
   predicts laser-like Hawking light, falsifiable in principle.
4. For the taxonomy: add g2 as the third discriminator column,
   replacing the unclaimed "Dicke-like" label with computed values
   (strict prototype: 1 - 1/S; ETH register: 2; semiclassical BH: 2).
   The M3 prohibition ("no Dicke claims without a computed statistic")
   is hereby satisfied for the strict model.

## Optional numeric support (not run)

Exact small-N check of both claims: (a) two-mode/F-species Fock
depletion, verify g2 = 1 - 1/N along the decay; (b) small ETH register
(random matrix elements) feeding one line, verify g2 → 2. Cheap; run
only if the analytic steps are challenged or before external use.

## Reevaluation (same day, red-team pass)

Three amendments; the headline survives in refined form.

**1. Robustness upgrade — vertex-independence.** g2 ≈ 1 does not
depend on the bilinear coupling (which 2006.00011's own footnote calls
a modeling convenience). Any emission operator that is a fixed
function of the single sharply-occupied collective mode gives output
moments that factorize to 1 + O(1/S). g2 measures source-amplitude
multiplicity and coherence, not vertex structure. [Inference; exact
for polynomial vertices on sharp-occupation states.]

**2. Loophole found — tag multiplexing.** Burden frequency tags
entangle quanta with memory sectors; a BROADBAND detector integrating
many detuned conditionally-Poissonian sub-lines sees beat-note
bunching (pseudothermal light, g2 → 2 — the standard lab synthesis of
chaotic light from a laser). The discriminator therefore requires a
resolution qualifier: PER-RESOLVED-MODE statistics. Within one
resolved bin: one tag value ⇒ one conditional amplitude ⇒ Poissonian.
Semiclassical Hawking is chaotic at every resolution. Outcome (a) of
the Conclusions now has a named mechanism (multiplexed mimicry) and a
named counter-test (resolve the sub-lines).

**3. Naive converse false; repaired version is the new theorem
target.** A single register-thermalized quasimode emits g2 = 2 through
a rank-1 coupling (canonical typicality), so g2 alone does NOT witness
rank. But a rank-1 thermalized mode has no S-enhancement and cannot
carry the Schwarzschild luminosity within ordinary envelopes (the
original Lemma); the only rank-1 route to the luminosity is
macroscopic coherent enhancement, which per-resolved-mode g2 = 2
excludes. Original leg-A chain (passive-support target, no longer the
primary Q1b theorem after the line-asymmetry upgrade):

```text
Schwarzschild luminosity
+ ordinary envelope
+ per-resolved-mode chaotic statistics (g2 = 2)
  ⇒  N_eff ~ S.
```

If this leg works, flux law plus counting statistics helps eliminate
the coherent-enhancement loophole rather than measuring rank directly.
The Q1b second pass promotes KMS line asymmetry to the primary static
rank-certificate leg; this `g2` chain remains independent passive
corroboration.  Open for leg A: intermediate cases (few coherent
modes, partial condensation, 1 < g2 < 2), and the multiplexing loophole
handled by the resolution clause. [Target, not result.]

**Numeric, promoted from optional to specific:** strict prototype with
memory-sector superpositions; compute broadband vs resolved g2 to
exhibit multiplexed mimicry and its failure under resolution.

## Feeds

- Q3 (branch forcing): semiclassical thermality is now a live
  candidate for a principle that forces the incoherent branch (or
  forces the coherent branch to a dressed version that mimics it).
- Discriminator table (prototype_m3): add the g2 column.
- Saturation paper: the coherent-branch paragraph can eventually cite
  this as the static discriminator; NOT yet — verify textbook/anchor
  refs first.
