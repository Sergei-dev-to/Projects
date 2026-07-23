# Decision log — LR-positivity campaign

Running register. Newest entries first. Every gate outcome and every Fable call
is recorded here so state survives session and model boundaries.

## Fable budget ledger

Cap ~$90. Hard stop at ~$70 cumulative; reserve ~$20 for final-candidate
verification. Two triggers only (P3 ansatz-if-stuck; candidate verify).

| Date | Mode | Purpose | Est. cost | Cumulative |
|---|---|---|---|---|
| — | — | (none yet) | — | $0 |

## Entries

### 2026-07-23 — CAMPAIGN STOPPED; narrow result retained, inflated claims retracted (user + integrator)

The LR campaign is closed. No further P2/P3 search, bake-off, held-out-gate
design, Fable consult, or scaling is authorized. The terminal assessment is in
`CLOSURE.md`.

**Defensible endpoint:** `p3/FOUR_ROW_OBSTRUCTION.md` proves that every four-row
hive polytope which is an empty lattice tetrahedron is unimodular. An independent
audit regenerated the 18 primitive rows and all 816 minors (absolute determinant
counts `0:299, 1:468, 2:48, 4:1`) and checked the White-normal argument. A
standalone exact verifier is now retained with the proof.

**Corrections to the two entries immediately below:**

- “150,316/150,316 unimodular” is retracted. The denominator is the complete
  `P(1)=4` pool and includes two-dimensional members. The correct statement is:
  all 150,316 passed the two-value screen, and every **three-dimensional** member
  is unimodular.
- Four-row hive vertex integrality is known: Buch states all corners are integral
  for `n <= 4`, and Coquereaux-Zuber repeat the SU(4) fact. It is no longer listed
  as open.
- The finite positivity paragraph needed a missing justification for `a2 > 0`.
  It is supplied in the corrected obstruction note by clearing denominators and
  applying positivity of the codimension-one coefficient of a lattice polytope.
- The determinant lemma is called elementary, not new; no novelty or
  publishability claim is made without specialist review.
- The original determinant script was not actually present despite the prior
  entry saying it was. The new verifier repairs that provenance gap.
- The screen artifact's embedded `0b7cc315...` is a semantic-payload hash, not
  the file digest. A true file-hash sidecar (`d3f5ad85...`) is now retained.

**Program-level judgment:** this is a useful narrow lemma, not a satisfying
return on the campaign's orchestration. It does not prove four-row positivity,
touch the `P(1) >= 5` channel, or address lengths five through seven. The useful
path was source correction -> bounded screen -> structural conjecture -> proof;
the elaborate P3 gates and bake-off were discarded. The branch is stopped rather
than enlarged to justify sunk effort.

### 2026-07-23 — OUTCOME C DELIVERED: four-row empty-tetrahedron obstruction proved (Fable, in-session)
Model switched to Fable; the Mode-C consult was executed directly instead of
couriered. Result: the unimodularity conjecture is now a **theorem with an exact
proof** (`p3/FOUR_ROW_OBSTRUCTION.md`): no four-row hive polytope, for ANY
boundary (infinite family), is an empty lattice tetrahedron of volume ≥ 2 — so the
Reeve mechanism is structurally impossible through the 4-point channel, explaining
150,316/150,316 unimodular.
**Proof shape:** (i) exact census of the fixed 18-row rhombus matrix: all 816
triple-minors in {0,±1,±2,4}, exactly ONE |det|=4 triple (the three central rhombi);
the matrix is NOT unimodular, so the naive Hoffman–Kruskal route fails — the first
attempted mechanism was wrong and was replaced, not patched. (ii) New lemma via
White's classification: an empty tetrahedron of volume Δ has ALL FOUR primitive
facet-normal triples of determinant ±Δ² (verified by direct expansion for general
p,q). (iii) GL₃(Z)-invariance + divisibility: Δ=2 needs four |det|=4 triples (one
exists), Δ≥3 needs |det|≥9 (none). ∎
**Bonus:** unconditional identity a₁ = (4c₁−c₂−3)/2 + 2a₃ makes the finite screen's
null geometry-free (max c₂=10 < 13 threshold), and gives the cheap c₁≥5 screen
criterion c₂ ≥ 4c₁−2 if ever wanted.
**Open:** c₁≥5 channel; four-row vertex integrality (matrix non-unimodularity means
it is NOT established here — check De Loera–McAllister); lengths 5–7; literature
check vs Coquereaux–Zuber before any novelty claim. No Fable API spend (in-session).

### 2026-07-23 — FOUR-ROW SCREEN COMPLETE (corrected domain); strong outcome-C signal (integrator)
Ran the lean restart Codex proposed, on the **corrected** domain (all lengths ≤ 4,
`|ν| = |λ|+|μ| ≤ 30`). Artifact `p3/four_row_screen_len4_size30.json`, sha256
`0b7cc315…`, 477 s, stdlib only (no Normaliz needed — see below).
**Method:** empty tetrahedron ⇒ `P(1)=4`, `P(2)=Δ+9`, negative linear coefficient
⟺ `Δ>12` ⟺ `c(2)>21`. Dimension needs no separate computation: dim ≤ 2 with 4
lattice points has `c(2) ≤ 10`, so any hit is necessarily a dim-3 empty tetrahedron.
Capped counting (abort at threshold) → `O(cap)` per triple; capped counter
validated against the uncapped evaluator, 6,380 cases, 0 mismatches.
**Result:** 9,332,014 support-compatible / 4,229,644 nonzero / mechanism pool
`c(1)=4` = **150,316** / **hits = 0**. Decisive detail: **max `c(2)` over the whole
pool = 10**, i.e. `Δ = 1` for *every* dim-3 empty tetrahedron in the slice — all
**unimodular**, a factor of 12 below the `Δ>12` threshold. No near miss anywhere.
Extends the earlier 426/426 panel to **150,316/150,316** over a complete domain.
**Independent verification:** six pool members recomputed uncapped with full exact
Ehrhart interpolation; exactly two rigid all-positive families — dim 2
`P=(1+t)²` (`c(2)=9`) and dim 3 unimodular `P=1+(11/6)t+t²+(1/6)t³` (`c(2)=10`).
**Outcome-C conjecture:** *every empty tetrahedron arising as a four-row hive
polytope is unimodular* — a structural obstruction explaining why Reeve cannot fire
here. Check against Coquereaux–Zuber before any novelty claim.
**Scope limits (recorded, must not be over-read):** screens only the Reeve
mechanism; `c(1) ≥ 5` (164,061 triples) unscreened; lengths 5–7 untouched. Null =
"mechanism absent in this slice", not "positivity holds".
**Derived tool:** complete four-row screening needs only `c(1)`, `c(2)` per triple
via the necessary condition `a₁ < 0 ⟹ c₂ > 4c₁ − 3` (proof in
`p3/FOUR_ROW_SCREEN_RESULT.md`), reserving exact `c(3)` for survivors.

### 2026-07-23 — ROOT CAUSE: the target was mistranslated (integrator)
Codex/Sol found, and I independently confirmed, that the campaign's search domain
was wrong from the start — **my error**, propagated into the brief, run book,
dispatches, and every feasibility conclusion.
**The error:** the official statement bounds *every* partition by length ≤ 7 and
weight ≤ 30. Since `|nu| = |lam|+|mu|`, that forces **`|lam|+|mu| ≤ 30`**. I wrote
independent bounds `|lam|,|mu| ≤ 30`, which admits `|nu|` up to 60.
**Independent verification:** ordered pairs in my domain = 143,137,296; canonical =
`(143,137,296+11,964)/2 = 71,574,630`, matching Codex exactly. Correct canonical
domain = 631,985 pairs (~113× smaller; ~2,840× in pre-Horn triples, 173,486,732).
Decisive: **99.1% of my domain has `|nu| > 30`** — illegal under any reading, so
this is not an interpretive dispute.
**Consequence:** the `P2.NAIVE_BOX_FEASIBILITY` closure and "the target box is
closed" statement were computed on a ~2,840×-inflated domain and are **void** for
the real target. B0/B1 completed work remains in scope (outer weights ≤ 24).
**Process failure (the real lesson):** `METHODOLOGY.md` requires primary-literature
deep review *before* selection; we deferred bounds/prior verification to publication
time. I even wrote a "verify the bounds before publishing" provenance note into the
brief and then treated it as a footnote rather than a gate, building three rounds of
review machinery on unverified bounds. Note also that three hostile-review passes did
**not** catch it — Sol explicitly reinforced the wrong bound. Adversarial review of a
*specification* cannot catch an error in the *problem statement*; only the source can.
**Rescoring accepted:** LR 25 → ~19. Hive→Ehrhart was **not** our recognition — it is
in the official write-up, so the "representation leverage" that made me rank LR first
was the problem author's step, not ours; and representation was mistaken for an
algorithm (no inheritance theorem, no effective inverse realizability).
Artifacts corrected: `CAMPAIGN_LR_POSITIVITY.md`, `ORCHESTRATION.md` (domain +
voided closure).

### 2026-07-23 — arm bake-off rejected pre-compute; frozen empty-Reeve scan completed (integrator)
The proposed equal-budget arm bake-off was hostile-reviewed before any
prospective artifact existed. It was **not a valid efficiency experiment**:
`AffineDim` + four integral vertices + `c(1)=4` + normalized volume already
determine the Ehrhart polynomial, so the “ranker” would have computed the target
before comparison. The arm entry point is disabled. Replacement: a bounded,
non-certifying **direct structural scan** over a frozen 512-case panel, documented
in `p3/REEVE_SCAN.md` and implemented by `p3/reeve_scan.py`.

One first freeze attempt stopped before `panel.json` on a zero-quota stratum
validator bug; it is preserved at `run/p3/empty-reeve-scan/` and never ran
geometry or stretched-polynomial queries. The bookkeeping-only fix was rerun
with the identical seed/selection algorithm in `empty-reeve-scan-v2` (no reroll).

**Completed result:** exact B1-minus-B0 eligible universe = **1,020,764**;
complete `c(1)=4` mechanism pool = **48,019**; frozen panel = **512**. Exact
Normaliz geometry found 86 affine-dimension-2 cases and 426 three-dimensional
empty integral tetrahedra. All **426/426 tetrahedra are unimodular**
(`Delta=1`); none has the Reeve-negative signature `Delta>12`. Therefore no
stretched-polynomial oracle was queried and the preregistered decision is
`BUDGET_STOP_NO_HIT_IN_FROZEN_PANEL` — explicitly not evidence that the mechanism
is absent elsewhere and not evidence for positivity.

Independent completion verification regenerated all 1,074,757 B1 support
records, the eligible-universe and full mechanism-pool stream hashes, and the
same panel; it then revalidated every geometry record, manifest, adjudication,
and summary. `complete=true`. Key hashes: plan `c41e72ad...`, panel
`23463f3f...`, geometry `2a8f5136...`, adjudication `c8cfd575...`, manifest
`edd4bb43...`. Full P3 remains unauthorized. No Fable spend.

### 2026-07-23 — P3 held-out-gate RETIRED; artifacts suspended (integrator)
Sol's third pass rejected v3 on architectural grounds; conceded. **The held-out-
recall gate is retired, not patched a fourth time.** Root cause (mine): I tried to
enforce an information boundary with prose inside one shared, oracle-equipped agent
session. Hashes order artifacts; they do not prove no private oracle query occurred.
Three successive gates were trivially passable — a signal I was specifying metrics
without adversarially simulating how they'd be gamed.
Decisive additional defects: (a) **estimand misaligned** — recovering interior-<1
*positive* polynomials is not finding a negative, and on B0-7 a degree-only ranker
retrieves both targets, so the gate could "pass" with zero geometric advantage;
(b) the eligible denominator is not label-free (208 evaluated / 14,568 structural /
7,301 post-filter); (c) Sol still chose the test distribution and the ≥3-target
slice rule is outcome-dependent; (d) if |H| > L, 100% recall is impossible;
(e) version drift and setup-gate/prefix-commit contradictions across documents.
**Actions:** `prompts/sol_ultra_p3.md` marked SUSPENDED — DO NOT DISPATCH;
`run/p3/heldout_gain_prereg.md` marked SUPERSEDED (provenance only). Replacement
direction: an **equal-budget control benchmark** (geometric prior vs stratified-
random / dimension-only / rows-size rankers at identical budget), which measures the
question we actually care about and is largely self-normalizing — reducing the need
for enforced blinding for an internal go/no-go. Awaiting user decision on how much
machinery P3 warrants; outcome C is under-served and should be rebalanced upward.

### 2026-07-23 — P3 preregistration REPAIRED again after 2nd Sol pass (v3) (integrator)
Sol's confirmation pass caught three more soundness holes in v2; conceded and fixed.
Independently verified the baseline composition. Key v3 fixes:
- **Fair baseline:** efficiency cap is over the **eligible universe** (degree-≥2
  triples), not all nonzero. On B0-7 that is 208 (not 9478) with exactly 2 subunit
  champions, so `floor(|E|/10)` is a real bar (~20), not 947.
- **Mandatory prospective blinding:** the gate is scored on a **fresh prospective
  slice**, never B0-7 — whose two target triples I had already published in this log
  (line ~"1/24 champions"), so it can no longer be held out. B0-7 is regression-only.
  Sol gets an **outcome-stripped** universe; coefficients are computed only after the
  ranked prefixes are frozen.
- **Fixed non-adaptive slice sequence:** frozen upfront at the setup gate; score the
  first `S_i` with ≥3 subunit champions; **INCONCLUSIVE** (not adaptive box-hop) if
  none. Removed the circular auto-enlargement clause.
- **Cost:** every triple inspected via oracle/proxy/solver is gate-critical, not
  merely logged.
- **Control plane:** versioned **v2 state schema** + migration + transitions +
  validators + tests (no in-place mutation) with explicit P3 states and a
  setup-only integrator stop before generator construction.
- **Ambient-bound regression restored:** candidate E1 holdout through `N = 2B+2`,
  `B=(n-1)(n-2)/2` (N=32 at length 7), not observed degree.
Prereg re-pinned: `run/p3/heldout_gain_prereg.md` (v3)
sha256 `be7e56415dc3be9c8196cb059976214c2be1b6329ea6f376afa091ab464f8844`.
Cleared in Sol's pass: min_interior repair, exact box def, PASS-vs-authorization,
Outcome-C caveat, Fable boundary. Next: one final Sol confirmation of v3, then the
setup gate.

### 2026-07-23 — P3 preregistration REPAIRED after Sol review (v2) (integrator)
Sol reviewed the P3 dispatch + prereg pre-dispatch; adjudicated as correct
(conceded). Independently confirmed the core bug on baseline data: under v1's
`min_nonleading` (excludes leading only), **100% of 1045 deg≥1 triples tie at
coefficient 1** and there are **0** genuine interior-<1 cases — the recall gate was
vacuous. Fixes (no P3 results existed, so a clean versioned repair):
- **Metric target → interior coefficient** `min{a_j : 1≤j≤d-1}` (exclude constant
  AND leading); H = subunit champions (interior <1), 100% retrieval required;
  degree 0/1 strata omitted; enlarge R until |H|≥8. (`heldout_gain_prereg.md` v2)
- **Blinding enforced by freeze+hash**, not instruction: Sol freezes/hashes
  generator + full ordered candidate prefix and STOPS before any H is derived;
  integrator derives H and scores.
- **Cost = distinct triples in the emitted ordered prefix** (emission counts;
  construction/solver cost charged); off-by-one fixed (`C_gen ≤ 947`, not 948).
- **PASS = eligible, not authorized:** Sol emits hashed gate report + stops;
  integrator recomputes and issues hashed authorization (role separation restored).
- **Outcome-C framing corrected:** per-fixed-stratum only; sample minima are
  nonincreasing so cannot prove a floor; heuristic evidence, C needs proof;
  bounded **C-only budget** (`env.json`, 12h) applies even on FAIL so Step 3 can't
  bypass "do not scale."
- **Operational contract:** P3 states, immutable scale plan, deterministic cursor,
  resume, manifest required before P3 (Sol to implement in its schema).
- Box spec exact (`|λ|,|μ|≤30` independent, `|ν|=|λ|+|μ|`, all lengths ≤7);
  candidate verification adds E1 holdout to `2·deg+2` and E2 raw period-one residue
  check; candidates path reconciled to `run/candidates.json`; "naive B1–B4 route is
  closed" (not "no redesign possible"); Fable is smoke-only, integrator/user
  authorizes+couriers, Sol must not trigger it.
Schema gained `min_interior_coeff`. Artifacts updated: `run/p3/heldout_gain_prereg.md`,
`prompts/sol_ultra_p3.md`, `ORCHESTRATION.md`, `run/env.json`.

### 2026-07-23 — PIVOT to P3 + outcome C; artifacts issued (integrator)
Exhaustive P2 closed (feasibility gate). New direction and dispatch artifacts:
- `run/p3/heldout_gain_prereg.md` — **preregistered** held-out-gain metric (fixed
  before any P3 results): reference box R = pinned B0-7 nonzero records
  (completion sha `d6f6b968…`); held-out set H = per-(rows,degree) min-nonleading
  champions (≤5/stratum); PASS = recall(H) ≥ 0.80 AND `C_gen ≤ C_flat/10` (948).
- `prompts/sol_ultra_p3.md` — P3 dispatch: reduction-guided hunt (Objective A) +
  outcome-C instrumentation (Objective C) from the same computation; exact-vs-
  heuristic split enforced; leaner evidence format; extend the per-stratum
  min-nonleading trend to higher degree to decide A-vs-C weighting.
- `prompts/fable_consult.md` Mode C — structural-positivity recognition consult
  (are LR hives a known Ehrhart-positive class? / where would a high-degree
  negative first appear?). This is the first authorized Fable spend (log cost when
  dispatched).
Weighting: P3 primary (its search generates the high-degree data C needs), C in
parallel. Decisive signal to watch: per-stratum min_nonleading → 0 (favors A) vs
positive floor (favors C). Current: 1 (deg≤3) → 5/12 (deg 4), mild downward.

### 2026-07-23 — INTEGRATOR ADJUDICATION of Sol Ultra P1 + pilot (this session, Fable)
Reviewed the artifacts, not the prose. **P1 ACCEPTED:** `run/p1/gate_report.json`
32/32 checks pass; a fully independent toolchain (lrcalc 2.1 + Normaliz 3.10.2 on
WSL) reproduced the baseline triples-payload hash byte-for-byte
(`b345773c…`, 7549 triples), with 6/6 E2 fixture agreements — the strongest parity
result available. **B0-7 pilot VERIFIED:** honestly labeled not-outcome-B
(partial extension); 18,287 processed, 9,478 nonzero, 0 errors, 0 negatives;
min coeff 1/24 (leading, = 4-dim volume term), min nonleading 5/12. **Independent
third-path check:** recomputed both min-coeff champions
(`λ=μ=(3,2,1,1)`, `ν=(4,3,3,2,1,1)` and `(5,3,2,2,1,1)`) with the stdlib pipeline —
`P = 1 + 25/12 t + 35/24 t² + 5/12 t³ + 1/24 t⁴`, exact rational match to Sol.
Model + tool agreement AND an independent path agree. **P2 hold endorsed:** B1 =
1,074,757 nonzero candidates at N=1; naive exhaustive P2 is infeasible and not the
right path to a counterexample. Recommendation recorded in this session's summary:
treat the exhaustive frontier as done (calibration + modest floor); pivot to P3
(reduction-guided) as the counterexample vehicle; pursue outcome C (structural
positivity of LR hive Ehrhart) in parallel given the uniform positivity of 9,478
nonzero records. Preregister the P3 held-out-gain metric before P3.

### 2026-07-23 — B0-7 scientific partial extension completed; P2 held (integrator)

Completed the post-P1 `B0-7` plan (`length ≤ 6`, inner sizes `≤ 7`) under the
checkpointed dual-oracle runner. This is deliberately classified
**partial-extension / not-outcome-B** because it is not one of the preregistered
B1–B4 boxes.

- Consumed all 18,287 structural triples: 14,302 frozen P1-prefix records plus
  3,985 new length-6 records.
- Exact support totals matched preregistration: 9,478 nonzero and 8,809 zero.
  The new suffix contains 1,929 nonzero and 2,056 zero records.
- Every new nonzero has separate bounded E1 evidence (`N=0..B`, reserved
  `N=B+1` holdout) and explicit-hive Normaliz Ehrhart evidence. All 1,929 agree;
  evaluator errors/disagreements = 0.
- Negative coefficients = 0. Overall minimum coefficient = `1/24`; minimum
  nonleading coefficient = `5/12`. The two minimum champions independently
  recompute to
  `1 + 25/12 t + 35/24 t^2 + 5/12 t^3 + 1/24 t^4` for
  `λ=μ=(3,2,1,1)` and respectively `ν=(4,3,3,2,1,1)` and
  `ν=(5,3,2,2,1,1)`.
- Full independent acceptance rechecked the plan, all 126 chunks, every one of
  the 1,929 new dual-evaluator records, both champions, and the completion
  sidecar. Completion core SHA-256 is `d6f6b968…`; completion-file SHA-256 is
  `ff327cb4…`.

Planning counts now make a naive P2 launch indefensible without a separate
feasibility case. B1 has 2,501,976 support-compatible pre-Horn triples and an
**exact** 1,074,757 nonzero canonical support count at `N=1`. B2/B3 exact
pre-Horn upper bounds are 736,249,709 / 103,018,487; B4's explicitly sampled
planning estimate is about 492.9 billion. The executable readiness audit passes
every check it currently evaluates and blocks on `P2.NAIVE_BOX_FEASIBILITY`.
The launch checklist's quantitative P3 held-out-gain threshold also remains to
be preregistered before any reduction-guided P3 scaling.

**Decision:** do not start B1/P2 automatically. Next work must be a bounded B1
throughput/storage sample, a leaner artifact design or proved prefilter/box
redesign, followed by explicit integrator authorization. No outcome A/B/C is
claimed from B0.

### 2026-07-23 — P1 accepted; executable orchestration validated (integrator)

The WSL environment is confirmed rather than reinstalled: Python 3.12.3,
`lrcalc 2.1`, Normaliz 3.10.2 and PyNormaliz 2.19.

- E1 independently persisted all 7,549 recomputed records; the controller hashes
  their bytes directly and obtains the frozen payload `b345773c…` with zero
  missing/extra/polynomial mismatches. The old self-report-only gap is closed.
- E2 regenerated six pinned fixtures with exact-integer input validation,
  hand-audited boundary/rhombus coverage, raw quasipolynomial decoding,
  `P(1)` checks, and exact lrcalc↔Normaliz agreement. Fixture-definition SHA-256
  is `3437ad9b…`; E2 summary payload is `dfa8b0b3…`.
- Hardened evidence manifest contains 34 verified artifacts (manifest id
  `6b46ac58…`). P1 passes the exact required 32/32 checks with zero failures;
  an independent read-only reviewer reproduced the stored gate result.
- Campaign oracle language is reconciled: bounded E1 plus a reserved holdout is
  routine scientific mode, verification candidates check through `2B+2`, P1
  adaptive mode is accepted only through exact frozen-payload equality, and the
  period guard is Normaliz's raw quasipolynomial collapse rather than an
  unimplemented E1 residue fit.
- Final repository-wide WSL discovery passes 60/60 tests.

The first live orchestration-only resume exercise found a lifecycle bug beyond
the prior review: state had hashed mutable `checkpoint.json`, whose bytes change
on resume. That attempt is preserved, not deleted, under
`run/archive/mutable-checkpoint-attempt-20260723T180555Z/`. The controller now
emits immutable checkpoint snapshots and proves their historical prefix after
completion. The canonical replay reaches `PILOT_COMPLETE`, revision 7; its
cursor-3 snapshot remains valid and historical after all ten toy records finish.
This toy exercise is explicitly not scientific evidence and cannot authorize P2.

### 2026-07-23 — review adjudicated + blockers fixed (integrator)
Sol Ultra pre-launch review received; adjudicated as largely correct (conceded).
Fixes applied:
- **Symmetry (deeper than flagged):** the old canonicalizer used swap + conjugation.
  Testing showed **conjugation does NOT preserve the stretched polynomial**
  (counterexample `λ=μ=(4,2), ν=(6,4,2)`: `P=1+2t` vs conjugate `1+3/2 t+1/2 t²`).
  So the order-4 dedup was *unsound*, not merely mislabeled "order-12". Fixed to
  **swap-only (order 2)**, provably valid (0 violations / 2355 triples). Honeycomb
  `S_3` (order 6) with property tests is a pre-P2 task.
- **Baseline artifact:** generated `dryrun/frontier_baseline.json` +
  `.sha256` = `b345773c40f2c340808ec20c424b1d33cba59e68bf45796842f1550d742b42d7`
  (len≤5,size≤7, 7549 triples, 0 negatives, deterministic across runs). Phase-1
  parity is now a hash, not prose.
- **Degree-6 "dimensional exclusion" claim withdrawn:** negativity is possible at
  degree 3 (Reeve). Scans establish only that no negative occurs among the scanned
  hive polytopes; no degree-based pruning.
- **Docs corrected:** two-evaluator result schema, canonical polynomial rep,
  exact finite P2 boxes B1–B4 with completion/resume semantics, per-stratum trend
  statistic, P3 exact-vs-heuristic split (substructure ≠ forcing), outcome taxonomy
  (A / B-completed-box / C / partial), seed only in P3, launch checklist.
- **Two code bugs fixed:** `scale(p,0)` normalization; `scan.py` test counter.
Also updated: `ORCHESTRATION.md`, `prompts/sol_ultra_campaign.md`,
`CAMPAIGN_LR_POSITIVITY.md`, `run/env.json`, `dryrun/DRYRUN_FINDINGS.md`.
**Status:** launch checklist defined; not yet all executed (needs lrcalc/Normaliz
env). Ready to re-issue to Sol Ultra.

### 2026-07-23 — P0 setup complete (integrator)
Orchestration designed (blackboard-on-repo). Written: `ORCHESTRATION.md`, result
schemas, `prompts/sol_ultra_campaign.md`, `prompts/fable_consult.md`,
`run/env.json`. **Next:** dispatch `prompts/sol_ultra_campaign.md` to Sol Ultra
for Phase 1 (oracle parity). Campaign is ready to launch.

### 2026-07-23 — dry run validated (baseline)
Stdlib pipeline (`dryrun/`) validated the design: two independent evaluators
(LR-tableau count vs Jacobi–Trudi/Schur) agree with 0 mismatches. The originally
reported counts—4,891 at `length ≤ 4, size ≤ 9` and 794 at `length ≤ 5, size ≤ 7`—
used the subsequently disproved conjugation dedup and are **superseded**, not
canonical frontier counts. The corrected swap-only `length ≤ 5, size ≤ 7`
baseline has 7,549 records (entry above). Both old scans found zero negatives.
Degree (= hive dim) confirmed to climb
with length AND size; first genuine middle coefficients appear at degree 6
(`λ=μ=(4,3,2,1), ν=(6,5,4,3,2)`), all positive. Counterexample region, if any, is
degree ≳ 6 → length ≥ 6, size in the teens–30. Stdlib counter dies there; real run
needs lrcalc + Normaliz. See `dryrun/DRYRUN_FINDINGS.md`.
