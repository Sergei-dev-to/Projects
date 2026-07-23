> **⛔ RETIRED — DO NOT DISPATCH (2026-07-23).** The campaign is closed; no P3
> workflow rewrite or equal-budget benchmark will be run. This file is retained
> only as provenance. See `CLOSURE.md` and `DECISION_LOG.md`.

# Dispatch: Sol Ultra — P3 (reduction-guided hunt) + outcome-C instrumentation (v2)

You are the primary runner, continuing in the repo `ai-open-problem-screen/`.
P1 is accepted; **the current naive B1–B4 exhaustive-P2 route is closed** by the
`P2.NAIVE_BOX_FEASIBILITY` gate (B1 ≈ 2.5M support-compatible; target box ≈
4.9×10¹¹). A cleverer prefilter/redesign is not proven impossible, but it is not on
the table now — we pivot.

Read first: `ORCHESTRATION.md` (Phase P3, roles), and
`run/p3/heldout_gain_prereg.md` **v2** (the preregistered gate — do NOT modify it).

## Setup gate — control plane to finish BEFORE any generator work

The v1 state machine ends at `P2_AWAITING_AUTHORIZATION` and has no P3 path. **Do
not mutate the v1 schema in place.** Create a **versioned v2 state schema** with
explicit P3 states, plus a migration, the transition implementation, validators,
and tests. Add a **setup-only integrator stop**: Sol reaches the setup state, the
integrator adjudicates, and only then may generator construction begin. Also
hash-commit: the **fixed non-adaptive prospective slice sequence** `S_1..S_k`
(per `heldout_gain_prereg.md` v3), an **immutable scale plan**, a **deterministic
cursor** + checkpoint/resume contract, an **artifact manifest**, and a **separate
bounded C-only budget** (`run/env.json`) that applies **even on a FAIL/INCONCLUSIVE
gate** so C-instrumentation cannot become back-door scaling.

## Box specification (exact)

Search domain: partitions with `len(λ), len(μ), len(ν) ≤ 7`; `|λ| ≤ 30` and
`|μ| ≤ 30` **independently**; `|ν| = |λ| + |μ|`. Canonicalize swap-only (matches the
baseline; conjugation is not a valid P-symmetry).

## Objective A — the counterexample (reduction-guided)

Exact vs heuristic (keep separate): "negative stretched LR coefficient = negative
Ehrhart coefficient of the hive polytope" is **exact**; "hive type contains a
Reeve-type substructure" is a **search prior, not forcing** — a bad sub-configuration
does not imply ambient negativity. Only direct dual-oracle evaluation of a
realizable candidate certifies a negative.

### Step 1 — prospective, blinded gate (build, FREEZE, STOP)

Scored on a **fresh prospective slice**, never B0-7 (whose targets are already
published; it is regression-only). Per `heldout_gain_prereg.md` v3:
1. Build the type-guided generator (negative-Ehrhart configuration catalog → hive
   combinatorial types → inverse realizability → integer boundaries).
2. For each frozen slice `S_i`, feed the generator only the **outcome-stripped**
   triple/feature universe (partitions + label-free hive dimension; **no
   coefficients**). Emit a **ranked prefix** of predicted subunit champions of
   length `≤ floor(|E(S_i)|/10)`, where `E(S_i)` = degree-≥2 triples.
3. Freeze and hash the generator (code, config, features, ranking rule, seed) and
   every ranked prefix into `run/p3/gate_report.json` — **before any coefficients
   are computed** — then STOP.
**Do NOT compute the slice coefficients, derive targets, score, or authorize.** The
integrator then computes the `S_i` polynomials, derives the true subunit champions,
scores the frozen prefixes on the first `S_i` with `≥3` targets (INCONCLUSIVE if
none), and issues or withholds a hashed authorization. Every triple the generator
inspects via oracle/proxy/solver counts toward `C_gen` — not just the prefix.

### Step 2 — only after integrator authorization

If the integrator issues a PASS authorization, scale P3 over the immutable scale
plan within the envelope; emit `run/candidates.json` (the runbook path). Any
`min_coeff < 0` candidate → verification below.

## Objective C — structural positivity (bounded, parallel, heuristic)

From every triple evaluated, maintain the **per-`(hive_rows, degree)` stratum**
record of `min_coeff`, `min_interior_coeff`, and the achieving triple. Report the
per-stratum landscape as evidence for/against an Ehrhart-positivity conjecture.
**Framing constraints (mandatory):**
- Compare only **within a fixed `(hive_rows, degree)` stratum across boxes**
  (runbook), never "as degree/rows grow."
- A minimum over an expanding or adaptively targeted sample is nonincreasing by
  construction; **stabilization in a finite sample cannot establish a positive
  floor.** All of this is **partial / heuristic evidence only**. Outcome C requires
  a proof or a structural obstruction — never claim a floor from sampling.
- C-instrumentation runs strictly under the separate bounded C-only budget and
  never bypasses a FAIL "do not scale" result.

## Candidate verification (per `min_coeff < 0` candidate)

Both oracle paths must agree on the **reduced monomial** polynomial (convert any
Normaliz `h*`/rational output first). Additionally: E1 holdout confirmation through
the **ambient bound** `N = 2B + 2` where `B = (n-1)(n-2)/2` (so `N = 32` at length
7) — use the independent ambient dimension, never an observed degree that could
itself be underestimated — and E2's raw **period-one residue check** (fit residue
classes, confirm period 1), not merely finite-difference stability. Build
`run/verify/<id>/`. You only *propose*; certification is adjudicated by tool
agreement plus the integrator third-path, with a Fable run as smoke test only.

## Fable

Do **not** trigger Fable. Fable spend (Mode C structural consult, or Mode B
candidate smoke test) is authorized and couriered by the integrator/user only, and
is a smoke test, never a certificate. Flag when you believe a Fable consult is
warranted; do not initiate it.

## Reporting

Append a dated entry to `DECISION_LOG.md` at each step and gate. Emit the leaner
evidence format (compact per-triple records + hashes; raw oracle transcripts only
for candidates and a small audit sample). Stay in the `run/env.json` envelope;
extending it is an explicit logged decision. Conservative novelty language; real
prior-art checks (KTT positivity; Ehrhart-positivity classes) before any C claim.
