# Statistics-Rank Link: Proof Skeleton (Q1b)

Date: 2026-07-05; route-2b dependency update 2026-07-08

Successor correction (2026-07-09): the LOW-side starvation result extends
beyond Markovian refill in the stationary linear gauge-invariant Gaussian
additive class.  It does not by itself make one aggregate response ratio a
rank certificate: HIGH and LOW deviations can cancel exactly, and a fully
ordinary thermal Gram tail is invisible to static response and `g2`.
`signed_cancellation_and_gram_tail_result.md` gives the exact counterexamples,
the conditional paired bound, and an exact two-drain separator.  Any use of
separate HIGH/LOW flux tolerances below therefore presumes resolved response or
a multi-setting protocol; the ordinary tail still needs an envelope,
tomography, or a microscopic theorem.

Further correction (2026-07-09): aggregate `g2` is also signed and
conditional.  A hot thermal HIGH channel has `g2=2`, and a superbunched
channel can exactly cancel an antibunched contribution at `N_eff<=2`.
Moreover an active anomalous Gaussian route passes both response and `g2`.
The HIGH L2 bound below therefore requires its stated subthermal-gap and
no-positive-cumulant assumptions, or replacement by separately resolved
response.  The raw source Gram target itself also needs the canonical metric
described in `source_gram_invariance_audit.md`.

Role: Q1b of the current roadmap — close the coherent-enhancement
escape of the luminosity lemma using per-resolved-mode counting
statistics. Status: proof skeleton with one exact identity, one
two-line corollary, one physics lemma at sketch level (the load-bearing
new piece), and an assembled conditional theorem. Verification grading
per claim. Not yet paper text.

Successor status: route 2b is an exact equilibrium static mimic, while
persistent drain creates a LOW-side deficit in the exact spectral class above.
A Planckian/QNM relaxation ceiling is needed only when translating that
identity into a black-hole flux ceiling.  The cancellation and ordinary-tail
qualifiers in the correction above must remain visible.

## 1. Composite-source identity [exact within stated class]

Decompose the resolved line's source amplitude into Gram eigenchannels
A = sum_i A_i, mutually independent, phase-symmetric (<A_i^2> = 0),
with intensities I_i and flux fractions f_i = I_i / sum I. Then

```text
g2(0) = 2 + sum_i f_i^2 ( g2_i - 2 ).
```

Derivation: expand <A+A+AA>; cross-channel fourth moments Wick-pair
into 2*sum_{i≠j} I_i I_j; phase-odd terms vanish; diagonal terms give
g2_i I_i^2. Checks: single sharp channel + thermal rest: g2 = 2 - f^2;
all-thermal: 2; single sharp alone: 1 - 1/S. [Exact given
independence + phase symmetry; independence across eigenchannels at
fourth order is an ETH-type factorization assumption, corrections
O(e^{-S/2}) — state explicitly in any theorem.]

## 2. Dominance corollary [immediate]

If the measured line has g2(0) = 2 - eps, then every sub-thermal
channel obeys

```text
f_i <= sqrt( eps / (2 - g2_i) ).
```

Strongly coherent channels (g2_i ~= 1) are excluded to f <= sqrt(eps).
Intermediate ("broad condensate", occupation spread alpha*S) channels
have g2_i ~= 1 + alpha^2/12 and are excluded with the correspondingly
weaker constant.

## 3. No-thermal-enhancement lemma [sketch — the load-bearing piece]

Claim: within a microcanonical shell whose emission line at omega ~ T
is calibrated by detailed balance (the Prop-1 input of the long
paper), any eigenchannel with per-channel intensity enhanced by a
factor K >> 1 over the ordinary envelope has g2_i <= 2 - delta with
delta = O(1).

Sketch: thermal (geometric) occupation statistics for a gap-omega
channel at line temperature T means n_bar = 1/(e^{omega/T} - 1) = O(1)
at omega ~ T; enhanced occupation n_bar ~ K at that line would require
effective line temperature ~ K*omega >> T, contradicting the
calibrated Hawking temperature. Moving the channel gap to T/K to make
occupation cheap moves its emission out of the flux-carrying window
(and its quanta out of the observed spectrum). Hence macroscopic
occupation at the line exists only out of detailed balance —
condensate-like — with sub-geometric number variance and therefore
sub-thermal g2_i. [Sketch. To tighten: quantitative delta(K);
formalize "channel occupation" for general eigenchannel operators, not
only literal modes; treat channels entangled with the register
(compensation within the shell) — the detailed-balance ratio of shell
DOS is what forbids flat occupation distributions at the line.]

This lemma is what kills the converse counterexample (rank-1
thermalized quasimode, g2 = 2): such a channel is NOT
intensity-enhanced at the line, so it cannot carry Schwarzschild
luminosity alone within ordinary envelopes — that is the original
Lemma 2 — while any channel that IS enhanced enough to carry it
cannot be thermal. The two exits are closed by the two legs.

## 3b. Line-asymmetry lemma [computation — supersedes the sketch as
the primary leg, 2026-07-05 second pass]

The detailed-balance exclusion is sharper stated through
emission/absorption asymmetry than through occupation variance, and it
becomes a computation:

Any channel with mean occupation K at the line has stimulated rates in
ratio em/abs = K/(K+1) → 1 for K ≫ 1 (enhanced channels are
asymmetry-free). An equilibrium channel at gap ω has
n̄ = 1/(e^{ω/T}−1), reproducing em/abs = e^{−ω/T} exactly (numeric:
n̄ = 0.58 at ω = T gives 0.3671 vs e^{−1} = 0.3679). If the observed
line asymmetry matches the calibrated Boltzmann factor to accuracy η,
the enhanced-channel flux fraction obeys

```text
f  <=  eta * n_bar_eq(omega)   ~   0.58 * eta   at omega ~ T.
```

LINEAR in η (vs √ε for the statistics leg), and requires only
golden-rule rates (second moments) — no fourth-moment ETH
factorization hypothesis. The two legs are complementary and
independent: the "geometric with mean K" state (thermal-enhanced)
escapes the g2 leg (g2 = 2) but is caught by asymmetry (ratio → 1);
the sharp condensate is caught by both. The kinematic escape route of
§3's variance argument is thereby closed by computation.

**Strict-prototype finding (new discriminator):** the memory-burden
prototype's line has em/abs = n₀/(n₀+1) = 1 − 1/S, where the
Hartle-Hawking/KMS line requires e^{−ω/T} ≈ 1/e — an O(1) failure of
detailed-balance calibration, independent of g2, arguably the sharpest
strict-model vote yet. Same fork-not-refutation framing: dressed
versions may repair it; O(1) asymmetry cannot come from 1/N
corrections, so the repair must be structural. [Computation on the
strict Hamiltonian; the "depletion-backreaction" escape — asymmetry
supplied by backreaction on n₀ rather than by occupation statistics —
EXAMINED 2026-07-05 in `asymmetry_backreaction_escape_result.md`:
closed for the strict class (number-conserving dressing only
frequency-tags, cannot create final-state multiplicity); one kinematic
sub-case survives (resolved anharmonic ladder, em/abs =
P(n₀+1)/P(n₀) with the enhancement factor cancelling exactly), caught
by leg A (per-sub-line g2 ≈ 1) and by a two-resolution stability
check within leg B.]

**Operational ladder (record):** the certificate suite now has three
rungs by cost — g2 (passive: watch the light), line asymmetry (probe:
linear-response absorption measurement), latency (deposit-and-decode).

## 4. Assembled theorem [SUPERSEDED — do not quote this block]

**SUPERSEDED 2026-07-05 by theorem v2 in
`participation_pigeonhole_result.md` §4.**  Two defects of the block
below: (a) the `(1 - min(...))^2 · c · S` conclusion overstates TOTAL
participation at finite eps/eta — an enhanced channel at flux
fraction f floors total N_eff at ~ f^{-2}; the corrected statement
separates the ordinary-sector support count (linear in (1-f)) from
total participation (min(cS, f^{-2})); (b) "leg B alone suffices"
needs the harmonic-line/resolution-stability clause (escape note).
Kept for provenance only.

Class: microcanonical shell; flux line omega ~ T calibrated by
detailed balance; Gram eigenchannels independent to fourth order (ETH
factorization); phase symmetry; ordinary envelope for non-enhanced
channels.

```text
Schwarzschild luminosity
+ line asymmetry within eta of Boltzmann     [leg B, linear, rates only]
+ per-resolved-mode g2(0) >= 2 - eps         [leg A, independent witness]
  =>
enhanced-channel flux fraction <= min( eta * n_bar_eq , sqrt(eps/delta) )
  =>
N_eff >= (1 - min(...))^2 * c * S.
```

Leg B alone suffices for the theorem and needs fewer assumptions (no
fourth-moment factorization) WITHIN the harmonic-line/unresolved-ladder
class, or when supplemented by a two-resolution stability check on the
asymmetry (see `asymmetry_backreaction_escape_result.md` §4: a resolved
anharmonic ladder with Boltzmann-sloped P(n₀) fakes bare leg B at
N_eff = 1); leg A remains as the passive witness and independent
corroboration, and the PAIR needs no clause — the legs provably cover
each other's blind spots.

Corollary (semiclassical anchor, eps = 0): exact per-mode thermality
implies zero SHARP-channel flux (g2_i near 1), hence N_eff ~ S GIVEN
static E' — the emission-envelope / no-bright-collective-channel condition.
The qualifier is essential: the §1 identity with a single thermal
COLLECTIVE channel (f = 1, g2_i = 2) gives g2 = 2 at N_eff = 1, so
g2 = 2 alone does NOT force rank; it forces rank only once a
thermalized bright collective channel (route 2b of
`envelope_as_coupling_universality.md`) is excluded by E'.  The static
certificate pair (flux law + counting statistics) certifies
source-rank saturation modulo that condition; the coherent-enhancement
escape it closes is the SHARP-channel (occupation) one, not the
collective one.  Dynamically, the starvation result replaces the
collective half of E' by the conditional refill-rate bound.

Q3 consequence: equilibrium per-mode thermality + detailed balance
force entropy-rank participation within the static class unless the
horizon emits through a thermalized bright collective channel.  Under
persistent drain, that remaining route is starvation-limited modulo
`Gamma_th <= c_P T`.  A surviving N-portrait branch has exactly the
options: (a) predict g2 != 2 per resolved mode (falsifiable against
semiclassical thermality); (b) generate thermal statistics from
genuinely many independent amplitudes (= becoming the boundary-ETH
branch); (c) rely on broadband tag multiplexing (killed per resolved
mode); or (d) emit through a thermalized bright COLLECTIVE channel —
g2 = 2 and KMS-preserving at rank one in equilibrium, but LOW-side
asymmetry under Planckian-limited persistent drain.  It survives through
super-Planckian/non-Markovian refill, unresolved multiplexing, or exit
from the class; the latency rung remains the assumption-light backstop.

## 5. Open items, in order (updated after second pass)

1. ~~Tighten Lemma 3~~ DONE via restructuring: the asymmetry leg (§3b)
   replaces the variance sketch with a computation; the variance
   argument survives as commentary only.
2. ~~Depletion-backreaction escape~~ DONE 2026-07-05 in
   `asymmetry_backreaction_escape_result.md`: closed for the strict
   class (backreaction = frequency tags, no final-state multiplicity);
   resolved-ladder sub-case clause-covered by leg A and by
   two-resolution stability within leg B.
2b. ~~Route-(b) participation inequality~~ DONE 2026-07-05 in
   `participation_pigeonhole_result.md` (corrected same day in
   review): ordinary-sector support count N_eff^ord ≥ (1−f)·c·S;
   total participation N_eff ≥ 1/(f² + (1−f)/(cS)) ~ min(cS, f⁻²),
   given the Schwarzschild scaling lemma translated into a per-channel
   ordinary-envelope cap + the NEW explicit commutator-cap hypothesis
   E' (the general-operator envelope form).  Total
   saturation requires η ≲ 1/(n̄_eq√S).  Same note: generalized channel
   occupation K_i ≡ ⟨A†A⟩/⟨[A,A†]⟩ resolves §3's "formalize channel
   occupation" item and puts leg B on textbook KMS footing; recorded
   blindness — asymmetry cannot see COUPLING enhancement (r invariant
   under c-rescaling), only the envelope hypothesis excludes it.
   Assembled theorem v2 (linear (1−f), full hypothesis list) is §4
   there and supersedes §4 below on the leg-B side.
3. Formalize the resolved-mode filter at operator level (output wave
   packets; needed for leg A only).  Statement now written
   (pigeonhole note §5); remaining work is input-output bookkeeping.
4. Fourth-moment ETH factorization hypothesis with e^{-S/2} budget
   (leg A only; the sharp channel is exempt from Gaussianity — the §1
   identity does not Wick-factorize it).
5. Support numeric: PARTIALLY DONE 2026-07-05 —
   `sim/statistics_rank_identity_check.py` verifies the composite
   identity exactly (1e-16 across mixtures incl. pure-Fock endpoint
   1 − 1/N), the dominance corollary, and the asymmetry ratios
   (equilibrium channel reproduces Boltzmann to 3 decimals; enhanced
   channels ratio → 1). Remaining numeric: broadband-vs-resolved g2
   with memory superpositions (multiplexing demo).
6. Only after 2-4: paper form (new section of
   paper_boundary_saturation — Lemma upgrade: class-conditional →
   certificate-closed, with the two-leg certificate and the
   three-rung operational ladder).

## Discipline

- The theorem is conditional on the class; say so every time.
- g2 alone does not witness rank (converse false).  The primary
  certificate after the second pass is luminosity + ordinary envelope
  + KMS line asymmetry; luminosity + g2 is leg-A passive corroboration,
  not the whole theorem.
- Per-resolved-mode qualifier is mandatory (multiplexing loophole).
- Semiclassical Hawking g2 = 2 per mode: standard, but VERIFY refs
  before ink (thermal reduction of squeezed pair; Bekenstein-Meisels,
  Panangaden-Wald for stimulated response).
