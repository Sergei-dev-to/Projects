# LR-positivity campaign — Stage 1–2 dry run (revised after review)

**Date:** 2026-07-23. **Environment:** stock Python 3.13, standard library only.
Exact arithmetic via `fractions`. **Code:** `lr_dryrun.py` (two coefficient
counters + interpolation), `scan.py` (frontier), `baseline.py` (checksummed
artifact). **Baseline artifact:** `frontier_baseline.json` +
`frontier_baseline.sha256`.

This revision corrects three claims in the first draft that a review correctly
flagged, plus a soundness bug the review did not catch but the baseline work
surfaced. Corrections are marked **[CORRECTED]**.

## Stage 1 — coefficient oracle validated

Two independent exact evaluators of the (unstretched) LR coefficient
`c^nu_{lam mu}`:

- **M1** counts LR skew tableaux (ballot backtracking) — combinatorial.
- **M2** expands `s_{nu/lam}` in the Schur basis via the Jacobi–Trudi
  `h`-determinant and Pieri rule — algebraic. Shares no core with M1.

They agree with **0 mismatches** on every triple cross-checked. Known spot values
reproduced.

**[CORRECTED] What the two methods are.** M1 and M2 are two independent
*coefficient counters*. They are **not** two independent *stretched-polynomial
evaluators*: both feed the same finite-difference interpolation, and the frontier
scan computes stretched values through M1 only, cross-checked against M2 at the
coefficient level (`N ≤ 1`). The genuinely independent stretched-polynomial
evaluator (E2 = explicit hive polytope + Normaliz Ehrhart) is **not implemented
in this stdlib dry run**; standing it up is Phase 1 of the real campaign.

**[CORRECTED] Period claim softened.** `poly_from_values` fits one polynomial and
checks that the top finite-difference levels vanish (stability). This is
*consistent with* Ehrhart quasi-polynomial period 1 but is **not** an independent
residue-class test; the first draft overstated it as a period check. A real
residue test is deferred.

**Bugs found and fixed during the dry run** (evidence the harness works):
- `scale(p, 0)` produced `(0,…,0)` rather than the empty partition; M1 and M2
  handle unnormalized zeros differently, so they disagreed at `N = 0`. Fixed by
  normalizing `scale`.
- `scan.py` incremented its test counter per `(lam,mu)` rather than per triple
  (miscount only; mismatch detection was correct). Fixed.
- **The canonicalizer was unsound (see below). Fixed.**

## [CORRECTED] Symmetry / deduplication — the important fix

The first draft claimed the frontier was deduplicated under the "order-12 LR
symmetry." That was wrong twice over:

1. Only **swap `lam <-> mu`** (order 2) preserves the *stretched* polynomial
   `P(N) = c^{Nnu}_{Nlam,Nmu}`. Verified: **0 swap-violations** over 2,355 triples.
2. **Simultaneous conjugation does NOT preserve `P`.** It is a symmetry of the
   unstretched coefficient only, because scaling and transpose do not commute
   (`(N·lam)' != N·(lam')`). Explicit counterexample the code found:
   `lam = mu = (4,2), nu = (6,4,2)` gives `P = 1 + 2t`, while the conjugate triple
   gives `1 + (3/2)t + (1/2)t^2` — different polynomial, different degree.

The first draft's canonicalizer used swap **and conjugation** (an order-4 quotient),
so it could merge two triples with different polynomials and keep only one —
**potentially skipping a polynomial, including a hypothetical negative one.** The
frontier is now deduplicated by **swap only (order 2)**, which is provably valid.
The largest valid group is the honeycomb `S_3` (order 6, Ehrhart-preserving);
implementing it needs rectangle-complement transforms and per-generator property
tests, and is a **pre-P2 task**. Swap-only over-counts honeycomb duplicates but
never drops a case, so exhaustiveness is preserved.

## Stage 2 — frontier baseline (corrected, checksummed)

Regenerated with swap-only dedup. `frontier_baseline.json`:

| Scope | Canonical triples (swap-only, all nonzero) | Negative coeffs | SHA-256 (triples payload) |
|---|---:|---:|---|
| `length ≤ 5, size ≤ 7` | **7,549** | **0** | `b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7` |

Deterministic: identical hash across repeated runs. This file, and the exact
serialization convention documented in `baseline.py`, is the **Phase-1 parity
artifact**. The production pipeline must reproduce the canonical `triples`
payload hash shown above; this is deliberately distinct from the hash of the
complete JSON file. (The first draft's counts of 4,891 / 794 were under the
unsound order-4 dedup and are withdrawn.)

**KTT positivity holds throughout this box** — zero negative coefficients.

## [CORRECTED] On where a counterexample can live

The first draft claimed negativity is "dimensionally excluded below degree 6" and
that a counterexample "lives at degree ≳ 6." **Both are withdrawn as unsupported.**
Negative Ehrhart coefficients occur already in **dimension 3**: the Reeve
tetrahedron has Ehrhart polynomial `(h/6)t^3 + t^2 + (2 - h/6)t + 1`, whose linear
coefficient is negative for `h > 12`. So degree 3 already admits a negative middle
coefficient in principle.

What the scans actually establish is narrower and correct: **no negative
coefficient occurs among the hive polytopes arising from LR triples in the scanned
box, and their smallest non-leading coefficient stays ≥ 1.** That is empirical
evidence that the *hive* polytopes in this range are well-behaved — a genuine
(and interesting) observation — but it is **not** a dimensional exclusion and must
**not** drive pruning or a stopping rule. Whether hive polytopes resist
low-degree negativity for a structural reason is an open question (a possible
outcome-C result), not an established fact.

## Degree vs size (individual-triple probe — unaffected by the above)

Degree (= hive-polytope dimension) climbs with length **and** size. At length 5,
`lam = mu`, increasing `|lam|`:

| `|lam|` | degree | polynomial | min coeff |
|---:|---:|---|---|
| 5 | 1 | `1 + t` | 1 |
| 7 | 3 | `1 + (11/6)t + t^2 + (1/6)t^3` | 1/6 |
| 10 | 6 | `1 + (13/4)t + (37/8)t^2 + 4t^3 + (9/4)t^4 + (3/4)t^5 + (1/8)t^6` | 1/8 |

Genuine middle coefficients first appear around degree 6 here, all positive
(smallest 3/4). This locates where the *search* gets interesting; it is **not** a
claim that lower degrees are safe. A single degree-6 triple already costs ~8 s in
stdlib because the counter's cost scales with the coefficient value — the tooling
wall the real campaign clears with lrcalc + Normaliz.

## Net assessment (revised)

The verification core is validated and now **sound**: two independent coefficient
counters agree; the canonicalizer is corrected to a provably valid symmetry; the
frontier is a deterministic, checksummed artifact. Within the certified box
(`length ≤ 5, size ≤ 7`) the conjecture holds with zero negatives. No claim is made
about where a counterexample must live beyond "not in this box." Promoting to the
real attempt is a tooling step (lrcalc + Normaliz) plus the pre-P2 tasks in the
launch checklist (`../ORCHESTRATION.md`).
