# Orchestration run book — LR-positivity campaign

> **CLOSED — DO NOT RESUME (2026-07-23).** This is a provenance record, not an
> active run book. No further P2/P3 search, bake-off, review gate, or model
> dispatch is authorized. See `CLOSURE.md` and the newest `DECISION_LOG.md` entry.

**Architecture:** blackboard on this repo. `ai-open-problem-screen/` is the single
source of truth. All material state lives in files here; chat is ephemeral. State
must survive session and model boundaries, so nothing load-bearing stays in a
conversation.

## Actors and bindings

| Actor | Role | Interface | Cost posture |
|---|---|---|---|
| **Sol Ultra** (Codex) | primary runner, Phases 1–3 | same-repo agent (reads/writes files here) | generous subscription — carries the grind |
| **Fable** (credits) | specialist: P3 ansatz-if-stuck + candidate verify | out-of-band single-shot (user couriers) | ~$90 hard cap; two triggers only |
| **Integrator** (Claude Code session) | P0 setup, ingest, adjudicate gates, register, third verify path | same-repo agent | metered — no grinding |
| **Oracle** (lrcalc + Normaliz + independent M1/M2) | the certificate | tools, not a model | model agreement is a smoke test, never the certificate |

## Shared folder layout

```
ai-open-problem-screen/
  CAMPAIGN_LR_POSITIVITY.md   # the brief (statement, gates, stop rules)
  ORCHESTRATION.md            # this file
  DECISION_LOG.md             # running register — every gate outcome, dated
  dryrun/                     # validated stdlib pipeline + findings (baseline)
  run/
    frontier.json            # P2 output: per-triple min coeff + champions
    candidates.json          # P3 output: negative-coeff candidates
    verify/                  # per-candidate verification bundles
    env.json                 # tool versions, seeds, compute envelope
    logs/                    # raw run logs
  prompts/
    sol_ultra_campaign.md    # dispatch packet for Sol Ultra
    fable_consult.md         # scoped consult/verify prompt for Fable
```

## Result schemas (preregistered — results must arrive in these shapes)

**Canonical polynomial representation** (defines "bit-identical"): exact monomial
coefficients, low→high degree, each `str(Fraction(num, den))` in lowest terms
(`"3"`, `"1/6"`). Normaliz `h*`-vectors / rational-function output MUST be
converted to this reduced monomial form before any comparison.

**Triple result** (an element of `frontier.json` / `candidates.json`) — carries a
**separate record per evaluator**, not one blended method:
```json
{
  "lam": [ints], "mu": [ints], "nu": [ints],
  "canonicalization": "swap-only-order2",   // must match the baseline's
  "degree": int,
  "min_coeff": "p/q",
  "min_nonleading_coeff": "p/q",   // min over a_0..a_{d-1} (includes constant=1)
  "min_interior_coeff": "p/q",     // min over a_1..a_{d-1}; the P3-gate target (deg>=2)
  "evaluators": [
    { "name": "lrcalc-interp",
      "poly": ["p/q", ...],
      "command": "…", "exit": 0,
      "artifact_sha256": "…", "tool_versions": {"lrcalc": "…"} },
    { "name": "normaliz-ehrhart",
      "poly": ["p/q", ...],
      "command": "…", "exit": 0,
      "artifact_sha256": "…", "tool_versions": {"normaliz": "…"} }
  ],
  "agreement": true          // evaluators' canonical polys identical
}
```
A candidate is routed to `verify/` only if `min_coeff < 0` **and** `agreement`.

**Parity (Phase 1) is defined by the canonical triples-payload hash**, not the
hash of the complete JSON file: production must reproduce
`dryrun/frontier_baseline.json`'s `triples` payload so that
`sha256(json.dumps(triples, sort_keys=True, separators=(",",":")))`
equals `b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7`
(scope `length ≤ 5, size ≤ 7`, swap-only canonicalization).

## Phase flow and gates

**Terminal status (2026-07-23):** the campaign is stopped. P0/P1 and the B0-7
pilot completed with no negative coefficient. The target-domain correction voided
the original P2 feasibility conclusion; three P3 gate designs and the proposed
bake-off were subsequently rejected. A lean four-row screen led to the narrow
empty-tetrahedron obstruction in `p3/FOUR_ROW_OBSTRUCTION.md`. That result does not
justify further search. Every dispatch and scaling path below is historical and
unauthorized; `CLOSURE.md` is controlling.

### P0 — setup (integrator)  — complete
Produce this file, the folder layout, the schemas, and both dispatch prompts.
Define the compute envelope in `run/env.json`. **Exit:** prompts ready.

### P1 — oracle parity (Sol Ultra)  — complete
Install lrcalc + Normaliz. Reproduce the dry-run frontier (`length ≤ 5`) using
the canonical serialization above and compare its triples-payload hash.
**GATE P1:** the payload hash matches and the two production evaluators agree on
the required hive fixtures, or STOP and reconcile. A mismatch is a toolchain bug,
not a discovery. Record both results in `DECISION_LOG.md`.

### P2 — exhaustive frontier (Sol Ultra)
Canonicalize with the **swap-only (order-2)** symmetry that matches the baseline
(the honeycomb `S_3` order-6 canonicalizer may replace it ONLY after it is
implemented and property-tested per the launch checklist). Conjugation is NOT a
valid dedup symmetry — see `dryrun/DRYRUN_FINDINGS.md`.

**⚠ DOMAIN CORRECTED 2026-07-23.** The bound below is **wrong**: the official target
bounds *every* partition by weight ≤ 30, so `|nu| = |lam|+|mu| ≤ 30` — not
independent `|lam|,|mu| ≤ 30`. The old box was ~2,840× too large in pre-Horn
triples and 99.1% illegal, so the `P2.NAIVE_BOX_FEASIBILITY` closure computed on it
**does not apply to the real target**. Boxes B1–B4 must be re-derived.

**Exact finite boxes (preregister; a box is "certified" only if fully completed).**
~~The size bound applies to **both** `|lam| ≤ S` and `|mu| ≤ S` independently
(`|nu| = |lam|+|mu|` follows).~~ Traverse a fixed sequence of boxes, each with a
**deterministic enumeration order** (sort by `(len(nu), nu, lam, mu)`), and record
per box whether it **completed**:
- B1: `length ≤ 6, S ≤ 12`  — estimate canonical count before running.
- B2: `length ≤ 6, S ≤ 20`.
- B3: `length ≤ 7, S ≤ 16`.
- B4: `length ≤ 7, S ≤ 30`  (the target box; may exceed the envelope — expected).
Estimate the canonical triple count of each box first; do not start a box you
cannot finish within the envelope. Emit `frontier.json` (schema above) plus a
`boxes.json` recording, per box, `{completed: bool, count, min_coeff, …}`.

**Interruption / resume.** Checkpoint the deterministic cursor. An interrupted box
yields a **partial frontier**, which is explicitly NOT a certified box and NOT
outcome B. Resuming continues the cursor; only a fully consumed box is certified.

**Trend statistic (preregistered — raw coefficients across differing
dimension/degree are not comparable).** Within each fixed `(hive_rows, degree)`
stratum, track `min_coeff` and `min_nonleading_coeff`. Compare strata like-with-
like across boxes. "Trend toward zero" means the per-stratum minimum decreasing as
the box grows, not a drop in a raw cross-stratum minimum.

**GATE P2 (branch):**
- any `min_coeff < 0` (with evaluator agreement) → Verification gate.
- a per-stratum minimum trending toward 0 → focus P3 on that stratum.
- a **completed** box with coefficients bounded away from 0 → that box is a
  certified-nonnegativity result (a candidate outcome B, subject to the novelty
  caveat below). An interrupted box is not.

### P3 — reduction-guided hunt (Sol Ultra; Fable if stalled)
**Exact fact vs heuristic — keep them separate.** The equivalence "a negative
stretched LR coefficient IS a negative Ehrhart coefficient of the hive polytope"
is *exact* (definitional). The search strategy "look for hive types containing a
Reeve-type substructure" is a **heuristic prior, not a forcing mechanism**: a
negative-Ehrhart sub-configuration does NOT imply the ambient polytope's Ehrhart
polynomial has a negative coefficient (Ehrhart coefficients are global invariants).
P3 must therefore either (a) supply an explicit inheritance argument for the
specific construction it uses, or (b) treat the substructure as a search prior and
rely on direct evaluation of each realizable candidate — never assert negativity
from the substructure alone.

Catalog candidate hive types; solve the inverse realizability problem for integer
boundaries within a box; evaluate every realizable candidate with **both** oracle
paths.
**Fable trigger #1:** if the type-guided search cannot re-find the P2 near-zero
champions at materially lower cost than the flat scan (the quantitative held-out-
gain metric, fixed in the launch checklist BEFORE observing P3 results), issue one
scoped Fable consult (`prompts/fable_consult.md`). Log the spend.
**Exit:** `candidates.json`, or exhaustion of the realizable-type budget → STOP at
the floor result.

### Verification gate (per candidate — the real certificate)
For each `min_coeff < 0` candidate, build `run/verify/<id>/`:
1. Normaliz Ehrhart on the explicit hive polytope (path independent of the
   interpolation that found it).
2. Integrator's independent M1/M2 recomputation at small `N` (third code path).
3. **Fable trigger #2:** cross-check by a different model (smoke test only).
Certify **iff** the two tool paths return the bit-identical polynomial with a
negative coefficient. Model agreement alone never certifies.

### Adjudication (integrator)
After each gate, score against the brief's preregistered stop conditions, write
the outcome to `DECISION_LOG.md`, and decide continue / stop / escalate. On a
certified counterexample: freeze artifacts, run the real prior-art check, route
the three-partition witness to a human / Lean for final independent verification.

## Launch checklist (pre-P2 — required before spending serious compute)

From the review. Do not scale a search until all are done:

1. **Symmetry:** either use the provably valid swap-only canonicalizer (matches the
   baseline) or implement the honeycomb `S_3` (order-6) canonicalizer with a
   per-generator property test (each generator leaves the stretched polynomial
   invariant on a sample, checked against the oracle). Do NOT reintroduce
   conjugation as a dedup symmetry.
2. **Baseline:** reproduce the canonical `triples` payload of
   `dryrun/frontier_baseline.json` to the exact payload hash specified above
   (Phase-1 gate; this is not the hash of the complete JSON file).
3. **Hive fixtures:** a fixed set of hand-checked hive polytopes covering boundary
   orientation and every rhombus inequality; require lrcalc-interp and
   normaliz-ehrhart to agree on these fixtures before running the full frontier.
   Explicit hive construction is the highest-risk silent-convention source.
4. **P2 boxes:** finalize the box list with estimated canonical counts and confirm
   each intended box fits the envelope.
5. **Resume semantics:** implement and test the deterministic cursor + checkpoint.
6. **Trend statistic:** fix the per-stratum metric before observing P2 output.
7. **Held-out-gain metric:** fix the quantitative P3 efficiency threshold before
   observing P3 output.
8. **Outcome taxonomy:** wire the three distinct outcomes (below) into reporting.

## Outcome taxonomy (do not inflate a stop into a result)

- **A — counterexample:** certified per the verification gate.
- **B — certified nonnegativity of a completed box:** a *fully consumed* finite box
  with zero negatives. A partial/interrupted frontier is NOT B.
- **C — structural obstruction:** a proof or strong structural reason.
- **partial / heuristic evidence:** an interrupted scan or a suggestive trend.

Publishability is not automatic for any of these — it depends on novelty, prior
art, auditability, and strength, adjudicated separately. Report the outcome by its
taxonomy label; never advertise a stop condition as a guaranteed publishable result.

## Determinism / seed

P1 and P2 scientific results are **deterministic and seed-independent**
(exhaustive enumeration). The `seed` in `run/env.json` governs heuristic sampling
inside P3, if any. A non-certifying planning artifact may also reuse it solely to
make a cost-estimation sample reproducible (as B4 in `run/box_estimates.json`
does); such a sample is never frontier evidence or a completeness certificate.
Every use must state its scope explicitly.

## Budget governance (Fable)

- Two triggers only: P3 ansatz-if-stuck, candidate verification.
- Each call: bounded single-shot, token cap, logged in `DECISION_LOG.md` with
  purpose and estimated cost.
- Hard stop at ~$70 cumulative; reserve ~$20 for final-candidate verification.
- Never Fable for enumeration or grind.

## Circuit breakers

- Sol Ultra runs inside the `run/env.json` compute envelope; extending it is an
  explicit logged decision.
- P1 parity failure halts everything until reconciled.
- No "searched hard, found nothing, no writeup" terminal state: P2/P3 exhaustion
  converts to the floor result (B) or a structural obstruction (C).
- Correlated-searcher rule: Sol Ultra, Fable, and the integrator share reasoning
  blind spots; the mechanical oracle is the only certificate.
```
