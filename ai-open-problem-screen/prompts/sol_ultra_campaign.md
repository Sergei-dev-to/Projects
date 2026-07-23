# Dispatch: Sol Ultra — primary runner, LR-positivity campaign

> **RETIRED — DO NOT DISPATCH (2026-07-23).** The campaign is closed. Retained
> only as provenance; see `CLOSURE.md`.

You are the primary runner for a research campaign. You are running as an agent
inside the git repo `ai-open-problem-screen/`. Read these first, in order:

1. `CAMPAIGN_LR_POSITIVITY.md` — the target, exact statement, gates, stop rules.
2. `ORCHESTRATION.md` — your role, the phase flow, the result schemas.
3. `dryrun/DRYRUN_FINDINGS.md` and `dryrun/lr_dryrun.py`, `dryrun/scan.py` — a
   validated stdlib pipeline and its results, your parity baseline.

Assume Python is installed with lrcalc, Normaliz (and LattE/polymake if useful).

## Mandate

Attack the target: a partition triple with `length ≤ 7`, `|λ|,|μ| ≤ 30` whose
stretched Littlewood–Richardson polynomial `P(N) = c^{Nν}_{Nλ,Nμ}` has a negative
monomial coefficient — **or** a certified nonnegativity frontier (outcome B), or a
structural obstruction (outcome C). No "searched, found nothing, no writeup" end
state is acceptable.

Everything that determines acceptance is exact rational / big-integer arithmetic.
Floating point may propose, never decide.

## Phase 1 — oracle parity (do this before any search)

Build two independent exact evaluators of the stretched polynomial:
- **E1**: exact LR counts (lrcalc) at `N = 0..D` + exact rational interpolation,
  with the degree-stability self-check (top finite-difference levels must vanish).
  `D ≥ 2·dim + 3`, `dim ≤ (rows−1)(rows−2)/2`.
- **E2**: explicit Knutson–Tao hive polytope + exact Ehrhart (Normaliz).

Reproduce `dryrun/frontier_baseline.json` (scope `length ≤ 5, size ≤ 7`,
**swap-only** canonicalization, serialization per `dryrun/baseline.py`) so that
`sha256(json.dumps(triples, sort_keys=True, separators=(",",":")))` equals
`b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7`. Individual
anchors your pipeline must also reproduce: `c^{(3,2,1)}_{(2,1),(2,1)} = 2`; and
`λ=μ=(4,3,2,1), ν=(6,5,4,3,2)` has
`P = 1 + (13/4)t + (37/8)t² + 4t³ + (9/4)t⁴ + (3/4)t⁵ + (1/8)t⁶`.

Note on the canonicalizer: only the swap `λ↔μ` preserves the stretched
polynomial; simultaneous conjugation does NOT (scaling and transpose don't
commute — see `dryrun/DRYRUN_FINDINGS.md`). Use swap-only, or the honeycomb `S_3`
(order 6) ONLY after implementing and property-testing it per the launch
checklist in `ORCHESTRATION.md`.

**GATE P1:** the baseline hash matches AND E1/E2 agree on the hive fixtures
(launch-checklist item 3), or STOP and reconcile. Write the result to
`DECISION_LOG.md`. Complete every launch-checklist item in `ORCHESTRATION.md`
before P2.

## Phase 2 — exhaustive frontier

Over canonical triples (swap-only dedup matching the baseline; `|λ|,|μ| ≤ S`
independently) sweep the preregistered finite boxes B1–B4 in `ORCHESTRATION.md`,
each in deterministic order, recording per box whether it **completed**. Emit
`run/frontier.json` (per-evaluator records) and `run/boxes.json`. Track the
**per-`(hive_rows, degree)`-stratum** minimum coefficient — raw coefficients across
differing dimension are not comparable, so do not compare them.

Do **not** claim a counterexample lives at any particular degree: negativity is
possible already at degree 3 (Reeve). Do not prune by degree.

**GATE P2:** route any `min_coeff < 0` (with evaluator agreement) to verification;
if a per-stratum minimum trends toward zero, focus Phase 3 there; a **completed**
box with no negatives is a certified-nonnegativity result for that box (outcome B,
subject to novelty review). An interrupted box is a partial frontier, not B.

## Phase 3 — reduction-guided hunt

Do not flat-scan. Catalog the local configurations that force negative Ehrhart
coefficients (Reeve-type substructures and their higher-dim analogues). Identify
hive combinatorial types at `length ≤ 7` that can contain one. Solve the inverse
realizability problem — integer boundaries `(λ,μ,ν)` in budget whose hive polytope
realizes that type — and evaluate only realizable candidates with **both** E1 and
E2. Emit `run/candidates.json`.

**Held-out-gain gate (preregister before scaling):** the type-guided search must
re-find the Phase-2 near-zero champions at materially lower cost than the flat
scan. If it cannot, stop and write up B/C; do not scale a search that cannot even
reproduce the known frontier. If you stall here, say so explicitly in
`DECISION_LOG.md` so a Fable ansatz consult can be issued — do not burn the
compute envelope thrashing.

## Verification (for any candidate)

For each `min_coeff < 0` triple, build `run/verify/<id>/`: the Normaliz Ehrhart
recomputation (independent of the interpolation that found it), the full exact
polynomial, and a short human-readable note. A candidate is only *proposed* by
you; certification is adjudicated separately by tool agreement, not by your own
confidence.

## Reporting

After each gate, append a dated entry to `DECISION_LOG.md`: what ran, the gate
outcome, and the decision. Pin tool versions and seeds in `run/env.json`. Stay
inside the compute envelope recorded there; extending it is an explicit logged
decision, not a default. Label all novelty conservatively and run a real
prior-art check before any priority language.
