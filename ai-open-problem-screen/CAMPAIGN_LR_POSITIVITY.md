# Campaign brief — a negative stretched Littlewood–Richardson coefficient

> **CLOSED — ARCHIVE ONLY (2026-07-23).** Do not execute this brief. The campaign
> stopped without a counterexample; its narrow retained theorem and the reasons
> for stopping are recorded in `CLOSURE.md`.

**Target class:** compact counterexample hunt with a trivial exact verifier.
**Selected because:** it is simultaneously compact-verifiable, low-saturation,
high-upside, and a genuine exercise of the cross-domain *recognition/reduction*
edge (hive polytope → Ehrhart). It bridges a certified-frontier screen and a
"hidden-structure" thesis.
**This document is the instruction set for the executing model.** Follow it in
order. Do not improvise past a stop condition.

---

## 0. Role and objective

You are attacking one precise, pre-stated target. You are **not** trying to
prove or survey the Littlewood–Richardson (LR) positivity conjecture. Your job
is to produce **one** of:

- **(A) a counterexample:** an explicit partition triple within the size budget
  whose stretched LR polynomial has a negative coefficient, certified by two
  independent exact methods; **or**
- **(B) a certified frontier:** an exhaustive, machine-checkable proof of
  nonnegativity up to explicit length/size bounds, with the true near-zero
  frontier mapped; **or**
- **(C) a structural obstruction:** a proof or strong structural reason that
  hive polytopes in this range cannot carry a negative Ehrhart coefficient.

All three are potentially publishable, but publishability is not automatic — it
depends on novelty, prior art, auditability, and strength, adjudicated separately;
report each outcome by its taxonomy label (see `ORCHESTRATION.md`), never as a
guaranteed result. A "we ran a big search and found nothing, with no completed box
and no obstruction" is **not** an acceptable terminal state — the preregistered
stops below exist to convert that into a certified box (B) or an obstruction (C).

Every numeric decision in this campaign is made in **exact rational / big-integer
arithmetic**. Floating point may be used only to *propose* candidates, never to
*decide* anything.

---

## 1. Exact statement and acceptance test

For partitions `λ, μ, ν`, let `c^ν_{λμ}` be the Littlewood–Richardson
coefficient (the structure constant `s_λ s_μ = Σ_ν c^ν_{λμ} s_ν`, equivalently
the multiplicity of `V_ν` in `V_λ ⊗ V_μ` for `GL_n`). Necessary support:
`|ν| = |λ| + |μ|` and `λ, μ ⊆ ν`.

Write `Nλ` for the partition with every part multiplied by `N`. It is a theorem
(Derksen–Weyman; Rassart) that

```
P_{λμν}(N) := c^{Nν}_{Nλ, Nμ}
```

is a **polynomial** in `N` with rational coefficients, `P_{λμν}(0) = 1`. The
**KTT positivity conjecture** (King–Tollu–Toumazet) states that every
coefficient of `P_{λμν}` in the monomial basis is `≥ 0`.

**Target (acceptance test for outcome A).** Exhibit partitions `λ, μ, ν` with

```
length(λ), length(μ), length(ν) ≤ 7   and   |ν| = |λ| + |μ| ≤ 30
```

such that `P_{λμν}(t) ∈ ℚ[t]` has at least one **negative** coefficient.
The witness is the triple `(λ, μ, ν)` plus the polynomial; it is accepted iff
two independent exact evaluators (Section 2) return the identical polynomial and
it has a negative coefficient.

> **⚠ CORRECTED 2026-07-23 — the target was mistranslated.** The official statement
> bounds **every** partition by length ≤ 7 and weight ≤ 30. Since |ν| = |λ| + |μ|,
> that forces **|λ| + |μ| ≤ 30**, not independent bounds |λ|,|μ| ≤ 30. The erroneous
> domain was ~113× too large in canonical pairs (71,574,630 vs 631,985) and ~2,840×
> in pre-Horn triples; **99.1% of it admitted |ν| > 30**, illegal under any reading.
> Every feasibility conclusion computed on the old box (including "the target box is
> closed") is void and must be recomputed.
>
> Provenance note: the specific length ≤ 7 / size ≤ 30 constrained target and the
> "≈60–80% chance a counterexample exists, conjecture expected false" prior are
> reported from a secondary source (the screen's ranking doc). **Verify the exact
> bounds and attribution against the primary problem statement before publishing
> any claim about them.** Do not repeat the probability figure as fact.

---

## 2. The oracle — two independent exact evaluators (non-negotiable)

Verification must be **decoupled from search** and performed by **two code paths
that do not share a computational core.** Build both before searching.

**Evaluator E1 — LR-count + exact interpolation.**
1. Let `B=(n−1)(n−2)/2`, the ambient hive-dimension bound. Compute
   `c^{Nν}_{Nλ,Nμ}` with an exact LR-coefficient routine and exact integers.
2. For routine frontier evaluation, fit at `N=0,…,B` and verify the reserved
   point `N=B+1`. Interpolate exactly over `ℚ` (Lagrange/Newton with reduced
   rational arithmetic). The stretching-polynomial theorem and the degree bound
   make these `B+1` fit values sufficient; the holdout is an executable wiring
   and normalization check.
3. For a putative negative candidate, use the stronger conservative policy:
   fit at `N=0,…,B` and verify every additional point through `N=2B+2`. For
   length `≤7`, this checks through `N=32`. Any failed holdout halts adjudication.
4. P1 baseline reproduction may use the preregistered adaptive finite-difference
   mode because acceptance additionally requires bit-identical agreement with
   the frozen independently generated 7,549-record payload. Adaptive mode alone
   is not candidate certification.
5. **Period check.** E1 relies on the stretching-polynomial theorem; it does not
   infer a quasiperiod by fitting residue classes. E2 must request Normaliz's raw
   Ehrhart *quasi*-polynomial and verify that its residue list collapses to one
   canonical polynomial. A nontrivial period or residue disagreement is a
   boundary/lattice-normalization failure and halts the campaign.

**Evaluator E2 — explicit hive polytope + Ehrhart.**
1. Construct the Knutson–Tao hive polytope `H_{λμν}` explicitly: the triangular
   hive array with boundary fixed by `λ, μ, ν` and the rhombus (concavity)
   inequalities as the facets. Its lattice points are the integer hives, counting
   `c^ν_{λμ}`.
2. Compute its Ehrhart polynomial with an independent exact tool (Normaliz,
   LattE, or polymake). Because dilation by `N` sends the boundary to
   `Nλ, Nμ, Nν`, this Ehrhart polynomial equals `P_{λμν}`.
3. Decode the raw Ehrhart quasipolynomial exactly, require period collapse to
   one, and compare its canonical monomial polynomial with E1.

**Cross-check gate.** On a held-out set of triples with known LR polynomials
(from KTT tables or independently recomputed), E1 and E2 must agree **100%**. A
single disagreement halts the campaign until resolved — a mismatch is a bug, not
a discovery. A candidate counterexample is accepted only when E1 and E2 return
the *bit-identical* polynomial.

---

## 3. Two non-equivalent representations (the search geometry)

Naming genuinely different languages for the same object is the point; a
counterexample is expected to be findable in one and invisible in another.

- **R1 — combinatorial (tableaux / puzzles).** `c^ν_{λμ}` as a count of LR skew
  tableaux or Knutson–Tao puzzles; stretching = re-counting at `Nλ,Nμ,Nν`. Search
  here = enumerate/canonicalize triples. This is the *brute* language; use it for
  calibration and verification, not as the primary search.
- **R2 — geometric (hive polytope / Ehrhart).** `P_{λμν}` as the Ehrhart
  polynomial of `H_{λμν}`. Search here = target polytope *combinatorial types*
  that force a negative Ehrhart coefficient, then invert to a boundary. This is
  the primary search language and the source of the model's leverage.
- **R3 — optional (vector partition function / honeycomb).** `c^ν_{λμ}` as a
  Kostant-type vector partition function evaluated in a chamber; negativity of a
  chamber Ehrhart. Use only if R2 stalls; it can expose different degeneracies.

---

## 4. The reduction thesis — why a model has leverage here

The recognition step that a domain specialist may not habitually make:

> **A negative stretched LR coefficient is exactly a negative Ehrhart
> coefficient of a hive polytope.**

Ehrhart polynomials of lattice polytopes are **not** always positive — negative
coefficients are a studied phenomenon (Reeve simplices in dimension 3 already
have a negative linear coefficient; more generally "long/thin" or degenerate
polytopes and certain higher-dimensional families). A symmetric-functions
specialist tends to scan triples of partitions; an Ehrhart specialist rarely
looks at hives. The model's cross-domain access is the whole edge.

**Do not run a flat scan over triples.** Instead:
1. Catalog the *local geometric configurations* known in Ehrhart theory to
   produce negative coefficients (Reeve-type substructures, spiky vertices, faces
   with few interior points at small dilation).
2. Ask which hive-polytope combinatorial types (for length ≤ 7) can contain such
   a configuration.
3. Solve the **inverse realizability problem**: find integer boundaries
   `(λ, μ, ν)` within the length/size budget whose hive polytope realizes that
   type. This is an integer-feasibility problem over the boundary data.
4. Evaluate only the realizable candidates with E1 **and** E2.

The transferable move is: change representation until the obstruction becomes a
finite, checkable realizability question — then let the exact oracle decide.

---

## 5. Preregistered first experiment and stop conditions

Three stages. Each has a falsifiable stop. Fix a compute envelope (wall-clock and
memory) **before** starting and record it.

**Stage 1 — build and validate the oracle.**
- Implement E1 and E2. Pass the 100% cross-check gate on held-out known triples.
- **Stop condition:** if E1 and E2 cannot be made to agree on the held-out set,
  halt and fix — no search until the oracle is trusted.

**Stage 2 — map the true frontier (this alone can yield outcome B).**
- Exhaustively compute `P_{λμν}` over the preregistered finite boxes B1–B4 in
  `ORCHESTRATION.md`, with `|λ|` and `|μ|` bounded independently. A box counts as
  complete only when every canonical triple in it has a recorded exact result.
- Record: the minimum coefficient observed, which triples come closest to zero,
  and whether nonnegativity holds throughout (reproducing KTT's tested range as a
  control). Use the validated canonicalization rule in Section 6.
- **Deliverable if the campaign stops here:** a certified nonnegativity frontier
  for each completed box, plus the near-zero landscape. Describe interrupted
  boxes as partial evidence, not certified frontiers; make no automatic
  publishability claim without novelty and prior-art review.
- **Stop / branch condition:** if the frontier shows coefficients *trending
  toward zero* as length/size grow, follow that trend (it points at the
  counterexample region). If coefficients are uniformly bounded away from zero
  with no trend, that is evidence for a structural obstruction — pivot to
  outcome C.

**Stage 3 — reduction-guided search (outcome A).**
- Execute the Section 4 procedure: negative-Ehrhart configuration catalog →
  admissible hive types at length ≤ 7 → inverse realizability → exact evaluation.
- Preregister a **held-out-gain gate** before scaling: the reduction-guided
  search must rediscover the Stage-2 near-zero champions (and any known
  small-coefficient cases) at materially lower cost than the flat scan. If it
  cannot even reproduce the known frontier efficiently, it will not find a rarer
  negative case — **stop and write up B or C.**
- **Terminal stop:** on exhausting the length ≤ 7 / size ≤ 30 realizable-type
  budget within the compute envelope with no negative coefficient, stop. Do not
  extend the envelope silently; extending is a new decision with its own recorded
  rationale.

---

## 6. Search discipline

- **Canonicalize triples by swapping `λ ↔ μ` only** (order 2), matching the
  checksummed dry-run baseline. This symmetry provably preserves the stretched
  polynomial. Simultaneous conjugation preserves the unstretched LR coefficient
  but does **not** preserve the stretched polynomial because scaling and
  transposition do not commute; never use it for deduplication. The honeycomb
  `S_3` (order 6) may replace swap-only only after every generator has passed
  stretched-polynomial property tests against the oracle as required by the
  `ORCHESTRATION.md` launch checklist. Untested symmetry pruning is forbidden.
- Log every evaluated triple, its polynomial, and its provenance
  (search stage, which representation surfaced it). The search must be replayable.
- Keep exact arithmetic end to end. `lrcalc`/big-int counts can be large
  (size up to `30·N` at `N ≈ 30`); ensure no silent overflow.
- Budget is finite and stated. No open-ended grind — that is the failure mode the
  stop conditions exist to prevent.

---

## 7. Hostile review and the correlated-blind-spot rule

Before any result is called final:

- **Do not certify a candidate with the code path that found it.** A
  counterexample surfaced in R2 must be confirmed in R1's independent evaluator,
  and ideally re-checked a third way (exact-rational recomputation or a proof
  assistant on the finite arithmetic).
- **A model reviewing its own reduction is not an independent check.** Models
  share blind spots; a self-hostile-review pass catches slips but not shared
  systematic errors. Where possible, route the final witness to a *different*
  system or a human for verification with no knowledge of how it was found — the
  witness is three small partitions and a polynomial, so this costs minutes.
  (Prior lesson from an adjacent program: a single agent that drafted,
  hostile-reviewed, and revised its own theorem produced a plausible result whose
  independent verification was still correctly gated as new work. Inherit that
  discipline.)
- Adversarially attack the reduction itself: is the hive polytope constructed
  with the *correct* boundary and *correct* rhombus inequalities? An off-by-one in
  the boundary silently computes a different coefficient. E2's raw-quasipolynomial
  period check (Section 2) is one guard; explicit small-case agreement with hand
  computation is
  another.

---

## 8. Deliverables

- **If A:** the triple `(λ, μ, ν)`; `P_{λμν}(t)` with the negative coefficient
  highlighted; both evaluators' outputs showing agreement; a third independent
  re-verification; reproducible code; a short note stating the result, the
  reduction that found it, and the exact bounds/attribution verified against
  primary sources.
- **If B:** the exhaustive nonnegativity certificate with explicit length/size
  bounds; the near-zero frontier map; the canonicalization and its validation;
  reproducible code.
- **If C:** the structural statement and its proof or the strong evidence for it,
  framed as necessary-condition mathematics, not a resolution of the conjecture.

Label all novelty conservatively. Run a real prior-art check (KTT and successors,
Ehrhart-negativity literature) before any priority language; "apparently new in
the checked corpus" is the ceiling absent expert bibliographic review.

---

## 9. Literature anchors (from memory — verify each against the primary source)

- A. Knutson, T. Tao, *The honeycomb model of GL_n tensor products I: proof of
  the saturation conjecture*, J. Amer. Math. Soc. 12 (1999). Hives/honeycombs,
  the saturation property.
- H. Derksen, J. Weyman — polynomiality of stretched LR coefficients (via
  semi-invariants of quivers). Cross-check the exact statement and year.
- E. Rassart, *A polynomiality property for Littlewood–Richardson coefficients*,
  J. Combin. Theory Ser. A 107 (2004) — polynomiality and structure of the
  stretched polynomial.
- R. King, C. Tollu, F. Toumazet — stretched LR/Kostka coefficients and the
  **positivity conjecture** (the target). Verify which paper states it and its
  exact form (there are related factorization / Newton-polytope claims).
- Ehrhart negativity: Beck, De Loera, Develin, Pfeifle, Stanley, *Coefficients
  and roots of Ehrhart polynomials* (2005), and the Reeve-simplex examples — the
  source of the negative-coefficient configurations for R2.
- Tools: `lrcalc` (A. S. Buch); SageMath symmetric functions; Normaliz / LattE /
  polymake for exact Ehrhart.

These are recollection-level pointers to locate the primary sources, not verified
citations. Confirm authors, titles, and the precise conjecture statement before
relying on any of them.

---

## 10. Known traps

- **Degree underestimate** in E1 → wrong polynomial. Guard with the theorem-backed
  ambient hive bound and reserved/conservative holdouts (Section 2).
- **Quasi-polynomial period > 1** appearing → boundary/normalization bug, not a
  new phenomenon; the theorem guarantees period 1.
- **Unsound equivalence pruning** → silently skipped polynomials and an invalid
  frontier. Use swap-only unless every generator of a larger canonicalization
  group has passed stretched-polynomial property tests against the oracle.
- **Floating point anywhere in a decision** → invalid. Rationals/big-ints only for
  anything that determines acceptance.
- **Self-certification** → a counterexample confirmed only by its finding code is
  not accepted. Two independent evaluators, minimum.
- **Silent envelope creep** → treat any budget extension as a new, recorded
  decision, not a default continuation.
