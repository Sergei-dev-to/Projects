> **⛔ SUPERSEDED — DO NOT USE AS A GATE (2026-07-23).** The held-out-recall design
> is being retired, not patched again. Fatal issues: the estimand is misaligned
> (recovering interior-<1 *positive* polynomials ≠ finding a negative, and on B0-7 a
> degree-only ranker retrieves both targets, demonstrating no geometric advantage);
> the eligible-universe denominator is not cleanly label-free (208 evaluated vs
> 14,568 structural vs 7,301 post-filter); and blinding is unenforceable inside one
> shared agent session with oracle access. Retained for provenance only.

# P3 held-out-gain metric — PREREGISTERED (v3, 2026-07-23)

**v3 supersedes v2.** v2 was still unsound: (a) the efficiency baseline was all
9,478 nonzero B0-7 records, but only 208 are degree ≥ 2 and exactly 2 are
subunit champions — a generator emitting all 208 passes `208 ≤ 947` with no
intelligent ranking; (b) B0-7 can no longer be blinded (its two target triples are
published in `DECISION_LOG.md`); (c) the auto-enlargement clause was
unexecutable and circular. v3 fixes all three plus the ambient-bound regression.

Purpose unchanged: prove the reduction-guided generator is an informative prior
before scaling. Nothing here may change after any P3 output is observed.

## Prospective, unlabeled slice (mandatory — B0-7 is regression only)

The gate is scored on a **fresh prospective slice**, never on B0-7. B0-7 is retained
only as a **known-target regression test**, not as held-out evidence.

Blinding is prospective, enforced by information flow:
1. At the **setup gate** (before any generator work), Sol proposes a **fixed,
   finite, non-adaptive sequence** of prospective sub-boxes `S_1,…,S_k` of the
   target domain, each disjoint from the already-evaluated triple manifest and each
   fully evaluable within the C-only budget. The integrator freezes and hashes this
   sequence. Selection is by **label-free features only** (partitions and hive
   *dimension*, which is combinatorial — computable without the stretched
   polynomial). No coefficients are computed or revealed at this stage.
2. Sol's generator is given only the **outcome-stripped triple/feature universe** of
   each `S_i` and emits, per `S_i`, a **ranked prefix** of predicted subunit
   champions. Sol freezes and hashes the generator (code, config, features, ranking
   rule, seed) and every ranked prefix — **before any coefficients exist** — then
   STOPS.
3. Only then does the integrator compute the actual polynomials of the `S_i`,
   derive the true subunit champions, and score the frozen prefixes.

## Eligible universe, target set, and cost

For a slice `S`:
- **Eligible universe** `E(S)` = triples in `S` with hive dimension (degree) ≥ 2
  (label-free). This — not the nonzero count — is the baseline.
- **Target set** `H(S)` = triples in `S` with `min_interior(P) < 1` (subunit
  champions; `min_interior = min{a_j : 1 ≤ j ≤ d-1}`, excluding constant and
  leading). Computed only after freezing.
- **Ranked prefix length cap** `L(S) = floor(|E(S)| / 10)`.
- **Cost** `C_gen(S)` = number of distinct triples the generator commits to in its
  ranked prefix **plus every triple it inspected via any oracle, proxy, or
  feasibility solve** — all gate-critical, not merely logged. (A purely
  combinatorial ranker's `C_gen` is its prefix length; a ranker that peeks via the
  oracle is charged for every peek.)

## Scored slice and outcomes

Scored on the **first `S_i` in the frozen sequence with `|H(S_i)| ≥ 3`** (a
preregistered, non-adaptive selection rule; the rule is fixed even though which
`S_i` qualifies is revealed only on evaluation). If no `S_i` has `≥ 3` subunit
champions → **INCONCLUSIVE** (do not adaptively pick another box; fall back to
outcome C).

**PASS (eligibility, not authorization)** on the scored `S_i`, both required:
1. **Recall:** the frozen ranked prefix contains **100%** of `H(S_i)`.
2. **Efficiency:** `C_gen(S_i) ≤ L(S_i) = floor(|E(S_i)| / 10)`.

PASS → Sol emits a hashed gate report and STOPS; the **integrator** independently
recomputes and issues a hashed scaling authorization. FAIL or INCONCLUSIVE → do
not scale P3; record it; reallocate to outcome C and to certifying the largest
feasible box under the separate bounded C-only budget.

## Setup gate (control-plane, before generator work)

Requires a **versioned state machine**: do not mutate the v1 schema in place —
create a v2 schema, migration, transition implementation, validators, and tests
with explicit P3 states, plus a **setup-only integrator stop** before generator
construction. The frozen slice sequence and prefixes are committed here.

## Notes

- Validates the prior, not the existence of a counterexample. PASS ≠ a negative
  exists; FAIL/INCONCLUSIVE ≠ none does.
- Re-pin this file's SHA-256 on acceptance; run one final confirmation before
  generator work.
