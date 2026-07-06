# Depletion-Backreaction Escape: Closed for the Strict Class; One Kinematic Sub-Case, Caught by the Pair (Q1b Loophole Exam)

Date: 2026-07-05

Role: examines the main open loophole of the line-asymmetry leg
(`statistics_rank_link_result.md`, lemma 3b): can a rank-1 dressed
condensate generate O(1) Boltzmann line asymmetry via backreaction on
`n0` rather than via occupation statistics?  Verdict: no, within the
strict class (computation); the general escape routes are enumerated
and each is either rank growth or caught by the `g2` leg; one genuine
kinematic sub-case (resolved anharmonic ladder) fakes leg B alone and
is caught by leg A — and by a two-resolution consistency check within
leg B itself.  Verification grading per claim.  Not paper text.

## 1. Where line asymmetry can come from [bookkeeping]

Golden-rule rates at a resolved probe frequency `omega`, emission
operator `A`:

```text
Gamma_em(omega)  ∝ sum_f |<f|A|i>|^2      at E_f = E_i - omega;
Gamma_abs(omega) ∝ sum_f |<f|A^dag|i>|^2  at E_f = E_i + omega.
```

Within golden-rule/linear response there are three and only three
sources of em/abs asymmetry:

```text
(a) occupation statistics of the emitting channel;
(b) final-state multiplicity (entropy grading of accessible
    states at E - omega versus E + omega);
(c) energy dependence of the matrix-element envelope (in ETH
    form: the e^{-S(E_bar)/2} normalization + smoothness of
    f(E_bar, omega)).
```

Equilibrium KMS: (b) + (c) jointly produce `e^{-beta omega}` in an
ETH shell; in a factorized mode description the same fact appears as
(a) with geometric occupation.  [Standard ETH/fluctuation-dissipation
bookkeeping.  Scope: golden rule; non-Markovian/strong-probe
corrections not covered.]

## 2. Strict class: escape closed [computation]

Class: single collective emission vertex `C0 (a0^dag b0 + h.c.)`;
harmonic `a0`; number-number master-memory coupling; `[H, N_m] = 0`.
This includes the strict prototype and every dressing that preserves
these properties.

Per resolved line = fixed burden-tag value.  Emission maps
`|n0, m> -> |n0 - 1, m>` and absorption maps `|n0, m> -> |n0 + 1, m>`
with the memory configuration `m` unchanged (number-number coupling +
`N_m` conservation).  If several configurations share a tag, the map
is block diagonal with the same set of `m` on both sides, so the
multiplicity cancels in the ratio.  For any ladder distribution
`P(n0)` the harmonic (frequency-degenerate) ladder gives exactly

```text
em/abs = sum_n P(n) n / sum_n P(n) (n+1) = <n0> / (<n0> + 1),
```

which is `1 - 1/S` at `<n0> ~ S` (binomial during strict decay:
consistent with the coherence-witness derivation).

Backreaction on `n0` enters exclusively as the c-number shift of line
frequencies through `dE_mem/dn0` — the M1/M2 frequency tags.  It
relocates lines; it cannot create or reweight final-state
multiplicity.  Secular depletion drifts rates and tags on the
evaporation timescale but leaves the instantaneous ratio at a
resolved line untouched.  Within this class the escape is CLOSED: the
O(1) KMS failure of the strict prototype survives all
number-conserving dressing.  [Computation on the strict Hamiltonian
class.]

## 3. What Boltzmann asymmetry at a resolved line requires [route enumeration]

Route (a) — occupation: geometric-type statistics with
`n_bar = O(1)` at the line.  Not enhanced; cannot carry Schwarzschild
flux alone within ordinary envelopes (the original Lemma 2 leg).

Route (b) — register sampling: an emission vertex that changes the
register configuration, with `e^S`-graded final-state multiplicity
supplying the DOS ratio of (b)/(c).  The emission operator then has
weight on entropy-many shell directions at the line — Gram
participation.  A LOW-rank register-changing vertex (coupling to a
second collective direction, a few modes, etc.) gives a few discrete
final states, not entropy grading; its asymmetry reverts to
occupation-type factors of those few modes, i.e. back to route (a).
So route (b) at O(1) line-flux fraction is entropy-rank
participation.  Target inequality (open): flux fraction `f_X` through
register-sampling channels + ETH envelope flatness implies
`N_eff >= c(f_X) S`.  [Sketch; the participation-versus-weight-skew
inequality is the remaining formal gap of the whole Q1b program.]

Route (c) — resolved anharmonic ladder: the genuine kinematic
sub-case.  Section 4.

## 4. Resolved-ladder sub-case [computation + open dynamics]

If the collective gap is `n0`-dependent (anharmonic condensate), the
transitions `(n0+1 <-> n0)` occur at distinct frequencies, offset
`delta_omega = d omega / d n0` per step.

Unresolved regime (`delta_omega` below calibration bandwidth): the
degenerate-sum formula of section 2 applies; `em/abs -> 1`; the
section 2 verdict stands.

Resolved regime: at a fixed sub-line frequency, emission and
absorption connect the SAME level pair, and the enhancement factor
cancels exactly:

```text
Gamma_em / Gamma_abs = P(n0+1)(n0+1) / [ P(n0)(n0+1) ]
                     = P(n0+1) / P(n0).
```

The asymmetry equals the ladder population ratio, independent of
occupation size.  A condensate whose `n0` exchanges with any
entropy-graded environment carries `d ln P / d n0 = -beta omega`
(from `rho_env(E - n0 omega)` grading), giving exact KMS asymmetry at
`<n0> ~ S` with O(1)-width `P(n0)`.  The emission operator is still
the single collective `a0`, so `N_eff = 1`: leg B alone is faked,
kinematically.  [Ratio: computation.  The sloped-`P` configuration is
kinematic; whether burden-sector dynamics realizes
`beta_env = beta_Hawking` is model-dependent and OPEN — do not claim
either way.]

Two catches:

**Leg A catches it.**  Within one resolved sub-line the source is the
restricted level pair: sub-thermal/nonchaotic counting, `g2` well
below 2 (the precise value depends on the replenishment model — a
single resolved level-pair transition can even be antibunched; the
claim needed here is only "not 2").  Semiclassical thermality demands
`g2 = 2` at every resolution.  The joint observation (KMS asymmetry
AND resolved `g2 = 2`) excludes the fake.

**Leg B catches it at two resolutions.**  Genuine equilibrium is
resolution-independent: for geometric `P`, both the per-pair ratio
`P(n+1)/P(n)` and the degenerate sum `<n>/(<n>+1)` equal
`e^{-beta omega}` — coarse and fine calibration agree, as KMS must.
The sloped-ladder fake is resolution-DEPENDENT: `e^{-beta omega}`
when resolved, `-> 1` when coarse.  So leg B supplemented by a
resolution-stability check (measure the asymmetry at two calibration
bandwidths) is again standalone-sufficient.  [Computation; follows
from the two formulas above.]

Scale note (BH mapping): `delta_omega / omega ~ 1/S` fractional
offset; resolving it needs integration time `~ S R` — the same
resolution scale as burden tags.  An observer who cannot resolve the
ladder sees the fake fail KMS in the opposite direction
(`em/abs -> 1`).  [Inference.]

Symmetry of the certificate (record): the two legs provably cover
each other's blind spots.  The geometric mean-K state fakes leg A
(`g2 = 2`) and is caught by leg B (`em/abs -> 1`); the sloped-ladder
state fakes leg B (KMS asymmetry) and is caught by leg A
(`g2 ~= 1`).  Neither bare leg is standalone-sufficient; the PAIR is
the certificate, and each leg is individually repairable by a stated
supplement (leg B: resolution stability; leg A: the luminosity
pairing already in Lemma 2).

## 5. Consequences

1. Theorem statement update: "leg B alone suffices" acquires a
   clause — leg B alone suffices within the harmonic-line /
   unresolved-ladder class, OR when supplemented by the
   two-resolution stability check; the bare pair statement needs no
   clause.
2. The strict-prototype vote (`em/abs = 1 - 1/S`) is unaffected: the
   bilinear master is harmonic and number-conserving dressing cannot
   repair it (section 2).
3. The dressed N-portrait's structural repair routes are now
   enumerated: (i) register-sampling emission = becoming the
   entropy-rank branch; (ii) sloped resolved ladder = predicts
   nonchaotic per-sub-line `g2` (below 2) and resolution-dependent
   asymmetry, both falsifiable against semiclassical thermality;
   (iii) exit the class
   (non-equilibrium line, no KMS calibration input).
4. Loophole status: CLOSED at strict-class level; downgraded overall
   from "escape" to "clause" — the resolved-ladder configuration is a
   stated exception covered twice over, not an unexamined hole.
5. Remaining formal gaps, new order: ~~route-(b) participation
   inequality~~ DISCHARGED same day in
   `participation_pigeonhole_result.md` (with a finite-eta
   correction: ordinary-sector count is linear in (1-f); TOTAL
   participation is floored at ~f^{-2}, so full saturation needs
   eta <~ 1/(n_bar_eq sqrt(S))); resolved-mode filter formalization
   (leg A; statement written); ETH fourth-moment hypothesis statement
   (leg A; statement written); broadband-vs-resolved multiplexing
   numeric.

## Discipline

- Say "closed for the strict class; clause-covered in general," never
  bare "closed."
- The sloped-ladder fake is kinematic; do not claim burden dynamics
  realizes it, and do not claim it cannot.
- The route-(b) participation inequality is discharged in
  `participation_pigeonhole_result.md`; quote it in the corrected
  two-quantity form (ordinary-sector count versus total
  participation), never the uncorrected linear total.
- Route enumeration in section 3 is exhaustive only within
  golden-rule/linear response; say so if quoted.
- Keep the pair framing: the certificate is the two legs jointly,
  with stated single-leg supplements.

## Feeds

- `statistics_rank_link_result.md`: 3b caveat resolved (pointer
  here); section 4 leg-B-alone remark gets the harmonicity/
  resolution-stability clause; open item 2 done, replaced by the
  route-(b) inequality.
- Roadmap Q1b: remaining-gaps reorder (this note; participation
  inequality promoted to top).
- M3 table: strict-branch asymmetry cell — "unexamined" resolved,
  point here.
- Q3: the enumerated repair routes sharpen the branch-forcing
  trilemma into named, falsifiable alternatives.
