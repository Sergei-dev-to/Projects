# Closure record — stretched Littlewood–Richardson campaign

**Decision date:** 2026-07-23
**Status:** **STOPPED. No further search, bake-off, gate design, or scaling is authorized.**

## Bottom line

The campaign did not solve or materially narrow the stretched
Littlewood–Richardson (LR) coefficient-positivity conjecture. It found no
negative coefficient. Its defensible mathematical output is a narrower
four-row obstruction:

> A four-row hive polytope that is an empty lattice tetrahedron is
> unimodular.

Equivalently, the Reeve empty-tetrahedron mechanism cannot produce a negative
coefficient through the four-lattice-point channel in four rows. This is a
useful lemma and an honest outcome-C result, but it addresses neither
four-row hives with five or more lattice points nor the length-five through
length-seven part of the official target. No novelty claim is made without a
specialist literature review.

The result is too narrow to justify more campaign machinery. The program is
therefore closed as a bounded negative screen, not presented as progress on the
full conjecture.

## What is retained

### 1. Reproducible evaluator work

- A frozen 7,549-record baseline over the small dry-run scope, with no negative
  coefficients and a stable canonical payload hash.
- Independent exact evaluator infrastructure: LR counting plus interpolation,
  and explicit hives plus Normaliz.
- Tests, schemas, resume logic, and compact adjudication artifacts. These are
  retained as reusable engineering, not as evidence that the target was close.

### 2. Bounded empirical results

- The B0-7 pilot processed 18,287 structural triples: 9,478 nonzero, 8,809
  zero, and no evaluator errors or negative coefficients. Its minimum coefficient
  was `1/24` and minimum nonleading coefficient was `5/12`. The retained local
  completion ledger recorded plan hash `d386ebea...`, prefix hash `e7c5236b...`,
  and completion hash `d6f6b968...`; the large raw shards are intentionally not
  part of the source commit.
- The corrected four-row enumeration covered canonical triples with
  `len(lambda), len(mu), len(nu) <= 4` and
  `|nu| = |lambda| + |mu| <= 30`:
  9,332,014 support-compatible triples, 4,229,644 nonzero triples, and
  150,316 cases with `P(1) = 4`. It found no `P(2) > 21` hit and a maximum
  `P(2) = 10` in that pool.

The figure 150,316 is the whole `P(1)=4` pool, including lower-dimensional
polytopes. It must not be described as “150,316 unimodular tetrahedra.” With the
known integrality of hives for `n <= 4`, the correct statement is that every
**three-dimensional** member of the pool is a unimodular tetrahedron.

The complete enumeration is useful internal evidence, but its original run did
not retain every validation sample and machine manifest required for a
publication-grade computational certificate. The code, compact result, and a
new standalone verifier of the theorem's finite determinant census are retained.

### 3. Structural theorem

The proof in `p3/FOUR_ROW_OBSTRUCTION.md` uses the boundary-independent set of
18 four-row hive normals. Of their 816 triples, exactly one has determinant
magnitude four and none has larger magnitude. White's normal form for an empty
lattice tetrahedron of normalized volume `Delta` has four primitive facet-normal
triples, each of determinant magnitude `Delta^2`. This excludes `Delta >= 3`
by magnitude and `Delta = 2` because it would require four determinant-four
triples.

The finite minor census is reproduced by
`p3/verify_four_row_obstruction.py`; the symbolic White-normal calculation is
given in the proof.

## What is not claimed

- No counterexample to stretched-LR positivity was found.
- No certified exhaustive frontier for the official length-seven target was
  completed.
- Four-row positivity was not proved; the `P(1) >= 5` channel remains open.
- Lengths five through seven remain open.
- A negative-Ehrhart substructure was never shown to force negativity of an
  ambient hive polytope.
- The obstruction theorem is not called new or publishable without a fuller
  prior-art check and expert review.

## Why the campaign stopped

The initial selection was based on an overstated recognition advantage: the
hive-to-Ehrhart reduction was already part of the problem's framing. The target
box was then mistranslated, making early feasibility conclusions invalid. Three
successive P3 held-out gates were found to be vacuous or unenforceable, and the
proposed bake-off measured the wrong estimand. The eventual useful result came
from a lean sequence — source correction, small exact screen, structural
conjecture, proof — rather than from the elaborate orchestration.

Continuing would primarily explore crowded or weakly connected heuristic routes
with poor expected return. Sunk effort is not a reason to enlarge the claim or
the budget.

## Reopening rule

This campaign may be reopened only for a concrete mathematical route that would
substantially strengthen the endpoint, such as a credible proof of positivity
for **all** four-row hives or a directly verifiable candidate in the official
box. More ranking experiments, blinded gates, generic scans, or model-review
rounds are not sufficient grounds to reopen it.
