# Constrained access — external review response

Date: 2026-06-13

Reviewer-side response to the constrained-access review packet.

Documents reviewed:

- `notes/constrained_access_review_memo.md` (primary packet)
- `notes/darwinian_no_hair_split.md` (theorem workspace)
- `notes/constrained_access_channel.md` (taxonomy/diagnostics)

## Overall assessment

The core move is sound: recast BH-information statements as an
operator-algebra QEC structure

```text
A_code = direct sum_x B(H_x),   Z(A_code) = direct sum_x C P_x,
```

with the center as the redundantly-broadcast public layer and the blocks
as decoupled-until-Page private residue.  The toy theorem (§10), the
algebraic theorem (§12), and the block-scalar proposition (§17) are all
correct as stated — honest compositions of Chernoff hypothesis-testing +
information-disturbance duality, and the notes say so.

The novelty is the bundling plus two genuinely new objects: the
source-side saturation invariant `N_eff(W)` and the
source-local-vs-dressed alternatives fork.  Those two are where original
proof effort should concentrate; almost everything else is citable.

Net: the framework is more than analogy if and only if the two open
dependencies become theorems and `N_eff` is made invariant.  The taxonomy
and the composition theorems are already solid and honestly scoped.  The
self-named risk ("the analogy becomes poetic") is real precisely at the
`N_eff` and alternatives-theorem items.

## Substantive issues (ranked)

### 1. The load-bearing hypothesis is unnamed: the resolution gap gamma << xi

Every public-center bound has the shape `exp(-m xi) + O(eta_m)`, and
`eta_m` is cumulative within-sector leakage (explicitly `½ n r eta +
O(n² eta²)` in §17).  To kill the Chernoff term you need `m >~ 1/xi`; to
keep leakage controlled you need `m << 1/gamma` where `gamma` is the
per-record leakage rate (`eta_m ~ m gamma`).  A nonempty window exists
iff

```text
gamma (per-record within-sector leakage) << xi (per-record between-sector Chernoff info).
```

This inequality is what separates a real two-layer channel from a smeared
one-layer channel, and it is currently implicit (buried in the
`n r eta << 1` vs `n xi >> 1` tension in §17; gestured at as "the leakage
scale" in the memo's theorem stack).

Recommendation: promote it to a named standalone hypothesis (*resolution
gap* / *signal-dominates-leakage*) and state every public-center theorem
as valid in the window `1/xi <~ m <~ 1/gamma`.  For the horizon
specialization this is a checkable physical claim: per-record
ETH/record-signature variation must be parametrically below the
per-record thermal/greybody Chernoff information for the chosen bins.

### 2. Block-smoothness and decoupling are partly redundant and inconsistently stated

§12 condition 2 is stated for every state `rho_x` in `H_x`
(`||rho_F^{x,rho_x} - sigma_x^{(m)}||_1 <= eta_m`).  That strong form
already implies near-decoupling from any purifier, so condition 3
(`eps_dec`) is nearly derivable — the hypotheses overlap.  But in §10/§11
smoothness is the weaker diagonal/record-signature version
(`a_{mm'}(nu)`, basis/code states), which does not imply decoupling of
superpositions, so there `eps_dec` is genuinely independent.

So "smoothness" is used in two inequivalent senses across sections.  This
answers review question 2 (redundant columns): block-private and
block-smoothness coincide in the §12 strong form and are distinct in the
§10 weak form.

Recommendation: keep the weak (diagonal) smoothness + separate decoupling
convention — it is the physically honest one (early fragments can be
diagonal-flat while coherences still leak) and it keeps §11.3
("microscopic privacy has two ingredients") consistent.  Restate §12 with
weak smoothness, not "every state".

### 3. Source-anonymity is a symmetry hypothesis, not a consequence of collective jumps

Anonymity is attributed to the collective jump `K_m^coll = sum_mu
K_{m mu}` (memo §5; theorem §9.2/§11).  But a collective jump still
carries which-`mu` information in relative amplitudes/coherences unless
the `K_{m mu}` enter permutation-symmetrically — exactly the structure
imposed by hand in Witness B (§18B).  "Rates add while aligned Dicke
amplitudes fail" establishes that rates add, not that the `mu`-label is
erased.

Recommendation: state anonymity as a permutation/symmetry hypothesis on
the source->mode map and show the collective-jump lemma supplies it,
rather than implying anonymity falls out automatically.  This also
cleanly connects to Witness B (same structure, different regime).

### 4. N_eff(W) is only an invariant relative to a privileged, normalized operator set

`N_eff = (Tr W)² / Tr W²` is basis-/normalization-dependent: rescale or
rotate the source operators and it can be made almost anything.  The
"comparable-channel strength condition" carries the entire load.  Review
question 3: it can be the right invariant, but only once the privileged
set is fixed (the actual Lindblad jump operators, normalized by physical
channel strength) and the invariance class is stated (invariant under
strength-preserving unitary mixing; not invariant under reweighting).

The companion claim — that `N_eff(W)` is not visible in instantaneous
flux/HBT moments because the emitted coherence matrix is `Gamma = C W C†`
with `C` compressing — is the actually-novel, defensible part.  Lead with
that and make `N_eff` rigorous enough to support it.

### 5. The alternatives theorem is the prize and is still a slogan

`compressed anonymous access + source-local emission + fast recovery of
arbitrary deposits => fast internal routing` (§18, §19, memo §7) is the
most original potential result.  The two witnesses (slow-router via
Lieb-Robinson, nonlocal encoder) are the right pair, and Witness A's LR
argument is sound in spirit.  But the forward implication needs a
quantitative engine: bounded operator growth => recovery-latency lower
bound.  That engine exists (operator-growth/LR bounds on recoverable
mutual information); cite it and state the contrapositive as the theorem.
Until then this is a conjecture with two examples and should be labeled as
such, not listed among theorem targets on equal footing with §10/§12.

### 6. Watch the circularity in "no-hair = center"

The center of `A_code` is a fixed algebraic object, but which observables
are redundantly recorded is a property of the emission channel, not the
algebra.  So "no-hair data are the center" is a dynamical claim (the
Hawking channel is block-scalar in the no-hair decomposition) dressed as
an algebraic identification.  §18 (Direction 1b, "records select the
effective center") is the escape hatch, but it is also the weakest-proven
step (the approximate no-broadcasting stability theorem, open dependency
#1).  If §1b is left open, the rest reads as: define the center to be
no-hair, then prove no-hair is public.

Recommendation: state plainly that no-hair = center is contingent on the
block-scalar property, and that §1b is what discharges the circularity.

## Answers to the six review questions

1. **Already standard?**  Largely yes, and the notes say so — the
   algebra/center/block-recovery layer is operator-algebra QEC
   (correctable algebras with classical center); center selection is
   QD/SBS; recovery is HP/decoupling.  The genuinely non-standard objects
   are `N_eff` saturation and the alternatives fork.  Also engage the
   existing "is BH radiation Darwinian?" literature — arguments that BH
   radiation has low redundancy for fine data actually support the
   private-block claim.

2. **Witness matrix clean?**  Mostly, but block-private/block-smoothness
   is redundant under the §12 convention (see issue 2).  There are four
   witness matrices across the three notes (memo §6; theorem §13, §19;
   channel §8, §8.5).  Consolidate to one canonical matrix and reference
   it; divergence risk is real.

3. **N_eff the right invariant?**  Conditionally — fix the privileged
   operator set + normalization and state the invariance class (issue 4).
   The flux-compression obstruction is the strong, keep-able part.

4. **Source-local vs dressed the right fork?**  Yes, the right axis and
   the most valuable framing.  But it is a conjecture until the
   operator-growth engine is invoked (issue 5).

5. **Extra horizon assumption?**  Yes — beyond binned no-hair
   distinguishability + within-sector smoothness + Page/HP decoupling +
   collective anonymity + latency/mixing, you also need the resolution
   gap (`gamma << xi`, issue 1) and the permutation symmetry that actually
   delivers anonymity (issue 3).  Those are the two currently-hidden
   assumptions.

6. **Sharper center-selection theorem?**  Likely citable rather than
   open: the strong-Quantum-Darwinism / SBS stability results and the
   approximate-no-broadcasting literature are where "many approximate
   redundant records => approximately commuting algebra" should live.
   Treat open-dependency #1 as a citation-retrieval task with constants,
   not a fresh proof.

## Minor proof points

- §12 public-center bound: testing against `|X|-1` sectors, the
  perturbation contributions add over the union, so the additive term is
  `O(|X| eta_m)`, not `O(eta_m)`.  Cosmetic but state it.
- §10 fidelity step: `F_rec <= 1/d_D + O(eps_dec)` — the trace-distance
  -> fidelity constant is convention-dependent and may be
  `O(sqrt(eps_dec))`.  Pin the inequality used.
- §17 is the cleanest proof in the set (sector non-demolition makes `E_m`
  genuinely block-diagonal, killing off-diagonal `Delta`; the TV
  chain-rule is careful).  No issue beyond surfacing `gamma << xi`.

## Was the memo helpful as a review packet?

Yes — the most useful of the three for actually conducting the review,
which is its purpose.

Worked:

- §3 (predicates) and §4 (theorem stack) gave the claim surface to attack
  without reverse-engineering from proofs.
- §5 (Provenance) made the review tractable: the
  imported/program-specific/open three-way split lets a referee skip
  re-litigating Chernoff and focus on the composition.
- §8 (review questions) is disciplined — 4 of 6 substantive points landed
  on pre-registered questions (Q2, Q3, Q4, Q6).
- §7 ranked the three theorem targets, which set effort priority.

Under-served:

- The predicate list and theorem stack state bounds as
  `exp(-m xi) + O(eta_m)` but never surface that `eta_m` is cumulative and
  fights `xi`.  So the most load-bearing hypothesis (issue 1) is invisible
  at the packet level.  A packet should name every hypothesis that can be
  empty-windowed.
- The §6 witness matrix is the fourth copy; the packet should own the
  canonical matrix and have the others reference it.

Packet scope: memo + `darwinian_no_hair_split.md` is the effective review
set (memo for the claim surface, theorem note for the proofs actually
checked).  `constrained_access_channel.md` was least load-bearing for the
review — taxonomy at lower resolution.

## Recommended next steps (priority order)

1. Name and elevate the resolution gap `gamma << xi` (issue 1) — free and
   load-bearing.
2. Fix the smoothness/decoupling convention (issue 2) and collapse the
   four witness matrices to one.
3. Make `N_eff` rigorous (privileged set + invariance class, issue 4) —
   one of the two real novelties.
4. Turn the alternatives theorem into a real statement via an
   operator-growth latency bound (issue 5) — the other real novelty.
5. Retrieve the SBS-stability citation to close open-dependency #1 (Q6);
   do not reprove it.
