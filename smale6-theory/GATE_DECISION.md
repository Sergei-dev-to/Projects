# Binary stopping-gate decision

**Decision date:** 2026-07-22  
**Decision:** **PASS - consolidate and stop this search program**

## Gate fixed before the final review

The theorem-consolidation sprint passes only if all four conditions hold:

1. the positive-radical square-lift proof is complete after one hostile
   review and one revision;
2. the degree-two exclusion, hence the degree-four lower bound, is rigorous;
3. the finite pre-registered literature audit finds no equivalent theorem;
4. the novelty claim is stated conservatively and distinguishes new
   implications from known ingredients.

Any proof gap, equivalent prior theorem, collapse to a routine restatement,
or unresolved review objection counts as failure. There is no
"inconclusive but continue" branch.

## Evidence

| Condition | Evidence | Result |
|---|---|---|
| Complete proof | SQUARE_LIFT_NOTE.md, Sections 2--5 | **Pass** |
| Hostile review resolved | HOSTILE_REVIEW.md; all seven required corrections incorporated in the sole revision | **Pass** |
| Degree-four barrier | Square lift gives even degree; a degree-one lifting bundle reduces degree two to a positive partial-fraction identity whose poles cannot cancel | **Pass** |
| No equivalent in fixed audit | PRIOR_ART_MATRIX.md, nine fixed sources plus the directly reached Ferrario paper and all fixed search concepts | **Pass** |
| Calibrated novelty | Known: mutual-distance framework, constant \(U\), signed continua, case-specific radical rationalization. Apparently new in the audit: positive splitting of the whole distance cover and the induced degree barrier | **Pass** |

## Locked mathematical result

For fixed strictly positive Newtonian masses, let \(C\) be the integral
Zariski closure of a nonconstant collision-free fixed-inertia arc in the
full labelled squared-distance coordinates, and let \(\widetilde C\) be its
normalization. Then every squared-distance function is a square in
\(\mathbb R(\widetilde C)\). The normalization map factors through
coordinatewise squaring, its pulled-back hyperplane bundle is a square, and
\(\deg C\ge4\).

Consequently, any infinite positive-mass fiber in Smale's sixth problem
contains such a degree-at-least-four algebraic distance curve. The
semialgebraic bridge covers both an explicit continuum and a merely
countably infinite hypothetical fiber.

## Novelty and value assessment

The result is structurally original in the audited literature, but its
ingredients are mostly classical. Its non-obvious step is to use positivity
inside the multiquadratic function field: constant potential does not merely
constrain the radicals; it forces every radical class to be trivial. The
coordinatewise square lift and projective degree obstruction then follow
globally on the normalization.

This is credible short-paper mathematics or a strong structural theorem in
a broader paper. It is not a solution of Smale's sixth problem, does not
prove finiteness for a new mass family, and carries no unconditional
priority claim before expert bibliographic review.

## Stop action

This gate closes the current counterexample-search effort. Under this
program there will be:

- no quartic or higher-degree ansatz search;
- no global singular-locus decomposition;
- no extension to \(n=6\);
- no second hostile review or further theorem revision.

Submission preparation, independent expert checking, or a future project
with a separately fixed budget would be new work and must receive a new
go/no-go decision. The present artifacts are therefore frozen as the
program's endpoint.
