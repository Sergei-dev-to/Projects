# Prototype Adjudication: Current Roadmap

Date started: 2026-07-04
Updated: 2026-07-05

Status: current handoff.  M0-M3, Q1, the Q1b proof skeleton (with its
line-asymmetry upgrade), and the Q2 operator-overlap bridge theorem
class are now landed at note level.  Use git history and the result
notes for earlier exploratory details.

## Core Result

The memory-burden/N-portrait collision is a fork, not a contradiction.
The luminosity/source-Gram lemma is class-conditional: it applies to the
weak-emission ordinary-envelope class, where the matrix-element envelope
does not hide powers of energy in a single eigenvalue.  The
memory-burden prototype exits that class by coherent Bose enhancement:
the powers sit in the master occupation, not in entropy-sized source
rank.

The useful classification separates three axes:

```text
1. degeneracy saturation;
2. source-rank saturation;
3. HP-style latency certificate.
```

The Dvali memory-burden/N-portrait prototype is the witness for:

```text
degeneracy-saturated,
source-rank-unsaturated,
strict-model HP-latency blocked.
```

Do not frame this as a refutation of the N-portrait.  Frame it as an
operational branch classification.

## Landed Milestones

### M0: Owed Checks

Status: done.

- Kaikov 2210.02312 does not close the axis.  Its "pre-scrambling" is
  Hilbert-space diffusion, not recovery fidelity or decoupling.
- Dvali:2024hsb is resolved as arXiv:2405.13117.  It reinforces the
  slow memory-release branch through model-dependent post-burden
  lifetime estimates `tau ~ R S_BH^(1+k)` and the conservative
  pair-annihilation bound `tau >= R S_BH^2`; it does not
  operationalize source rank or HP recovery.
- The N-portrait/memory-burden corpus does not appear to contain the
  radiation counting statistic needed here.  Q1 computes it for the
  strict prototype.
- Dvali 2509.22540 strengthens the table-top/frozen-routing motivation:
  their cold-boson memory-burden tests and our routing witness point at
  adjacent bench physics.

### M1: Source Gram

Status: done in `prototype_m0_m1_results.md`.

For the strict Dvali memory-burden prototype, the source Gram matrix at
the flux-carrying thermal line has:

```text
N_eff = 1,
sigma = 0,
lambda_0 ~ C0^2 n0 ~ eps0^2.
```

The luminosity powers sit in the master occupation `n0 ~ S`, not in
`S` comparable source eigenvalues.  Dressing does not rotate the master
emission operator into parametrically many memory ladder directions:
the master-memory coupling is number-number, and the exchange graph
containing the radiation mode is `{a0,b0}`.

Attribution datum to keep visible: 1601.01329 itself reduces equal
coupling to `K` memory modes to coupling to one collective mode, with
the other `K-1` modes decoupled.  Our contribution is the invariant
framing, not the bare existence of the collective mode.

### M2: Latency / Frozen Routing

Status: done at countermodel level in
`prototype_m2_frozen_routing_countermodel.md`.

The speculative route

```text
a_k -> a0 -> b0
```

does not exist in the strict Hamiltonian.  Total memory occupation
`N_m` is conserved.  For diaries encoded in fixed diagonal burden
sectors, the emitted master record does not carry diary coherence, so
HP-style recovery is blocked in the strict model.

Generic loads may leak coarse diagonal information through frequency or
mass tags.  That is not HP recovery of an arbitrary new quantum diary.
In the BH mapping, the available memory release route is parametrically
long.  The 2405.13117 branch gives model-dependent powers
`tau ~ R S_BH^(1+k)` with `k > 0`, with the pair-annihilation argument
giving the conservative bound `tau >= R S_BH^2`.

### M3: Discriminator Table

Status: done in `prototype_m3_discriminator_table.md`, with Q1
filling the counting-statistics column and Q1b adding the
line-asymmetry column.

The robust discriminators are:

```text
source rank:       N_eff ~ S versus N_eff = 1;
diary latency:     HP-like recovery versus burden-blocked/long release;
counting class:    per-resolved-mode g2 ~= 1 versus g2 = 2;
line asymmetry:    em/abs = e^(-omega/T) (KMS) versus 1 - 1/S.
```

Do not use "Dicke-like."  The strict-model statement is now concrete:
one sharp collectively enhanced master source gives
`g2(0) = 1 - 1/S` per resolved mode.  An ETH-Gaussian/thermal outgoing
mode gives `g2(0) = 2`.

### D3: Taxonomy Port

Status: done.

The memory-burden row was added to
`horizon_property_separation_program.md`, and the coherent branch was
backported into `paper_boundary_saturation/main.tex` with Dvali
citations.  The boundary-saturation paper now states that its rank
conclusion applies to the weak-emission ordinary-envelope class, not to
the collectively enhanced single-source branch.

### Q1: Passive Coherence / Counting Statistics

Status: answered at note level in `coherence_witness_g2_result.md`.

For the strict prototype, per-resolved-mode counting statistics separate
the coherent single-source branch from the ETH-Gaussian/thermal branch:

```text
strict sharp master branch:       g2(0) = 1 - 1/S;
ETH-Gaussian entropy-rank branch: g2(0) = 2;
semiclassical Hawking mode:       g2(0) = 2.
```

This is an O(1) passive exterior distinction for the strict model.
Semiclassical per-mode thermality therefore disfavors the strict
coherent branch unless dressed `1/N` rescattering, thermalization of
the collective mode, or another mechanism restores chaotic
`g2(0) = 2`.

Important limitations:

```text
1. State "per resolved mode."  Broadband detection of many detuned
   burden-tagged sub-lines can mimic chaotic bunching.
2. Do not say g2 alone witnesses source rank.  A rank-1 thermalized
   quasimode can have g2 = 2.
3. Use "ETH-Gaussian" or "thermal/chaotic" for the g2 = 2 branch; rank
   by itself is not enough.
```

## Current Roadmap

### Q1b: Statistics-Rank Link

**STATUS: proof skeleton landed 2026-07-05 in
`statistics_rank_link_result.md`, upgraded the same day by a second
pass.** Contents: (1) exact composite-source identity
g2 = 2 + Σ f_i²(g2_i − 2) under fourth-moment channel independence +
phase symmetry; (2) dominance corollary f_i ≤ √(ε/(2−g2_i)); (3) the
no-thermal-enhancement variance sketch, now superseded as the primary
leg by (3b) the line-asymmetry lemma [computation, not sketch]: an
enhanced channel with mean occupation K has stimulated em/abs =
K/(K+1) → 1, while the calibrated line requires the Boltzmann ratio
e^{−ω/T}, so asymmetry within η of Boltzmann bounds the
enhanced-channel flux fraction by f ≤ η·n̄_eq(ω) ~ 0.58·η at ω ~ T —
LINEAR in η and needing only golden-rule rates, no fourth-moment ETH
hypothesis; (4) assembled conditional two-leg theorem, v2 form after
the pigeonhole correction (`participation_pigeonhole_result.md` §4):
ordinary-sector support count N_eff^ord ≥ (1−f)·c·S and total
participation N_eff ≥ 1/(f² + (1−f)/(cS)) ~ min(cS, (η·n̄_eq)⁻²),
with leg B alone sufficient only under the harmonic-line/
resolution-stability clause, leg A (g2) as independent passive
corroboration, and total saturation requiring η ≲ 1/(n̄_eq√S); ε = 0
(semiclassical thermality) gives N_eff ≥ c·S within the class.

New strict-prototype finding from the second pass: the prototype's
line has em/abs = n₀/(n₀+1) = 1 − 1/S where the KMS line requires
e^{−ω/T} — an O(1) detailed-balance failure, independent of g2,
arguably the sharpest strict-model vote yet.  The certificate suite is
now a three-rung operational ladder by cost: passive g2, probe line
asymmetry, deposit-and-decode latency.  Q3 consequence: per-mode
thermality + detailed balance force entropy-rank participation within
the class.

The depletion-backreaction escape is EXAMINED (2026-07-05,
`asymmetry_backreaction_escape_result.md`): closed for the strict
class — number-conserving dressing only frequency-tags, it cannot
create final-state multiplicity, so em/abs stays pinned at
<n0>/(<n0>+1); one kinematic sub-case survives (resolved anharmonic
ladder, where the enhancement factor cancels exactly and em/abs =
P(n0+1)/P(n0) can be Boltzmann-sloped at N_eff = 1), clause-covered
twice: leg A catches it (per-sub-line counting is nonchaotic, below
2) and leg B catches it at two calibration bandwidths (the fake is
resolution-dependent; genuine KMS is not).  Net: loophole downgraded
from escape to stated clause; the strict-prototype vote stands.

The route-(b) participation inequality is DONE (2026-07-05,
`participation_pigeonhole_result.md`): generalized channel occupation
K_i = <A†A>/<[A,A†]> gives r_i = K_i/(K_i+1) for arbitrary channel
operators (leg B = textbook KMS per channel); the enhancement
dichotomy splits into occupation enhancement (killed by asymmetry)
and coupling enhancement (killed only by the envelope hypothesis —
the asymmetry leg is provably blind to it); the pigeonhole closes
route (b) with two named bounds: ordinary-sector support count
N_eff^ord >= (1-f)·c·S, and total participation
N_eff >= 1/(f^2 + (1-f)/(cS)) ~ min(cS, f^{-2}) — total saturation
requires calibration eta <~ 1/(n_bar_eq sqrt(S)).  One new explicit
hypothesis (E', commutator cap).
**Q1b SKELETON COMPLETE: every load-bearing step is at computation or
explicit-hypothesis level; nothing in the chain is a sketch.**

Remaining (bookkeeping and support only): resolved-mode filter
input-output formalization (statement written); fourth-moment ETH
hypothesis (statement written); broadband-vs-resolved g2 numeric with
memory superpositions (the composite identity, dominance corollary,
and asymmetry ratios are already verified in
`sim/statistics_rank_identity_check.py`); paper section first pass
landed in `paper_boundary_saturation/main.tex`, with remaining polish
around constants, theorem phrasing, and placement of the finite-eta
floor.  The current top theorem target is the two-leg certificate
above.  The original `g2`-only leg-A target is kept below as provenance
and as the passive-support subproblem.

Historical leg-A target: under explicit ordinary-envelope assumptions,
test whether the static pair

```text
Schwarzschild luminosity
+ per-resolved-mode chaotic statistics, g2(0) = 2
    => N_eff ~ S.
```

The point is not that `g2` directly measures source rank.  It does not.
The point is that `g2 = 2` may close the coherent-enhancement escape
that allowed rank-one luminosity in the strict prototype.  If this leg
works, flux law plus counting statistics partially repairs the section
5.5 compression obstruction; after the Q1b second pass, line asymmetry
is the primary rank-certificate leg and this is independent passive
corroboration.

Open cases:

```text
few coherent modes;
partial condensation, 1 < g2 < 2;
rank-1 thermalized quasimodes;
broadband tag multiplexing versus resolved bins.
```

Immediate leg-A support calculation: compute broadband-vs-resolved
`g2` in the strict prototype with memory-sector superpositions.

### Q2: Operator-Overlap Bridge

Status: lemma plus first theorem-class bridge drafted in
`operator_overlap_latency_lemma.md` and
`q2_operator_overlap_bridge_theorem.md`.  The exact obstruction uses
the full visible algebra generated by the record channel:

```text
A_vis(T) = Alg{ U(t_j)^\dagger A_src U(t_j) : t_j <= T }.
```

If that visible algebra is diary-blind on a fixed sector, emitted
records up to `T` are diamond-close to a diary-independent channel, and
no decoder can recover diary coherence above the no-information
baseline.  The strict memory-burden prototype supplies the zero-overlap
case.

The bridge result should now be stated with the integrated
blind-algebra defect of the coupled record generators:

```text
sum_j |g_j| eps_j,

eps_j = dist( H_j, A_blind tensor B(R_j) ).
```

For bounded-budget source-local records, small integrated defect makes
the emitted record channel diamond-close to a diary-independent
channel.  Therefore HP-fast recovery requires order-one integrated
generator access, nonlocal/constraint-dressed access, or supplied side
information.  The older single-time `G_D(t)` profile is still a useful
routing diagnostic, but replacing the generator-defect theorem by
`G_D(t)` requires a separate norm-duality lemma.  This calibration
avoids the Lie-algebra-generation pitfall.

The strict memory-burden prototype sits at the exact-zero-defect
endpoint for fixed-sector coherences: the persistent visible algebra
contains diagonal burden tags but no memory ladder/coherence operator,
so `Gamma_D^cb(T)=0`.

This also unifies the access-cut language: diagonal burden tags are the
public center, fixed-sector coherences are protected private blocks, and
the master-record algebra is the visible cut.

### Q3: Branch-Forcing Think-Pass

After Q1b, stress-test candidate principles that might force real black
holes onto one branch:

```text
universal gravitational coupling -> entropy-rank participation?
graviton-condensate/N-portrait -> collective single-source branch?
semiclassical per-mode thermality -> exclusion or thermal mimicry?
```

Per-mode thermality is now the live forcing candidate.  Keep this as a
thinking pass unless Q1b produces a sharp theorem.

### Later

D2 crossover curves: run only after the statistics-rank and
theorem/counterexample forks are cleaner.  The question is whether
degeneracy saturation, soft-constituent formation, source-rank
saturation, and the latency certificate co-emerge or split along the
approach from large `S` toward `S ~ O(1)`.

M4 numerics: support role only.  Not needed for M1-M3, but useful for
the broadband-vs-resolved `g2` check if the analytic statement is
challenged.

## Tier Assessment and Maximal Upside

Redone 2026-07-05 after the Q1b second pass.  Each tier carries two
gradings: current state, then the everything-goes-right endpoint.
Every endpoint below is conditional on the stated class
(microcanonical shell; detailed-balance-calibrated line with the
harmonic-line/resolution-stability clause; ordinary envelopes for
non-enhanced channels including the E' commutator cap; the
Schwarzschild scaling lemma translated into a per-channel
ordinary-envelope flux cap); even the maximal case does not derive
gravity, `G`, or the interior.

The chain of conditions for the full upside, in dependency order:
(1) the depletion-backreaction escape closes — DONE 2026-07-05 at
strict-class level with a stated clause
(`asymmetry_backreaction_escape_result.md`); the successor condition
is the route-(b) participation inequality; (2) the resolved-mode
filter and ETH fourth-moment hypothesis are stated cleanly (leg A
support); (3) the Q2 bridge theorem lands in the fresh-ancilla class;
(4) the dressed N-portrait cannot structurally restore KMS asymmetry
— sharpened by the escape exam into three named repair routes
(register sampling = becoming the entropy-rank branch; sloped
resolved ladder = falsifiable via per-sub-line g2 and resolution
stability; exiting the class).

Tier 1 — axis-separated classification.  LANDED and banked: the
memory-burden prototype as a state-count-saturated but
source-rank-poor and latency-blocked witness.  This is a result at any
downstream outcome; the fork-not-refutation framing does not depend on
how the fork resolves.

Tier 2 — static certification of source rank.  Current: Q1b skeleton
COMPLETE — escape closed/clause-covered, pigeonhole landed and
corrected.  Endpoint: theorem — within the class, Schwarzschild flux
law + KMS line asymmetry force N_eff^ord ≥ (1−f)·c·S and total
N_eff ~ min(cS, (η·n̄_eq)⁻²), with full total saturation at
calibration accuracy η ≲ 1/(n̄_eq√S) and unconditionally at η = 0
(semiclassical anchor).  The saturation paper's Lemma upgrades
from class-conditional to certificate-closed, and boundary saturation
becomes statically certifiable by an exterior observer: no
deposit-and-decode protocol required for the rank axis.

Tier 3 — branch forcing (Q3 full answer).  Current: half-answered
within the channel framework.  Endpoint: semiclassical per-mode
thermality plus detailed balance force the entropy-rank branch
outright, and any surviving coherent alternative must predict an O(1)
KMS violation or sub-thermal per-resolved-mode statistics — a
falsifiable signature, not a philosophical fork.  Sharpest admissible
form: Hawking thermality is not branch-neutral; it votes, and the vote
is a theorem within the class.

Tier 4 — certificate ladder completion.  Needs Q2 in addition.
Endpoint: the three-rung ladder (passive `g2`, probe line asymmetry,
deposit-and-decode latency) is theorem-backed end to end — statics
certify source rank, the visible-algebra bridge certifies the latency
structure.  Slogan upgrade: horizons are thermal systems whose full
entropy is exterior-recoverable at logarithmic emitted-record latency
AND whose source rank is exterior-certifiable statically.

Tier 5 — demarcation payoff (the program's stated goal).  Endpoint:
given per-mode thermality — a QFT-in-curved-space fact — source-rank
saturation follows by quantum-information arguments alone, so the
trinity's input 2 is derived rather than assumed.  The gravitational
residue narrows consistently with the algebra-type seam: the value of
`A/4G` and the lived interior.

Tier 6 — external stakes (keep hedged).  Endpoint: the asymmetry rung
is a linear-response measurement, the cheapest branch discriminator
named so far — a candidate for cold-boson memory-burden hardware
(2509.22540) alongside the frozen-routing witness on the latency rung
(proposal drafted).  If burden physics is real for PBHs, burden onset
predicts `g2` drifting up from 1 plus a growing KMS-asymmetry
deviation in late-stage emission, with stakes in the `10^4-10^9 g`
window.  In-principle claims only: analogue experiments probe pair
correlations, not exterior per-mode `g2`; do not overclaim
experimental status.

D2 crossover curves remain optional territory below these tiers:
useful to clarify whether access structure co-emerges with the
degeneracy/softness package, not load-bearing for any tier above.

## Post-Completion Horizon

Recorded 2026-07-05.  Hypothetical: every tier above lands.  Where the
program would stand, and the ranked next directions.  Nothing here is
actionable before the open items close; this section exists so future
sessions inherit the map.

### Position at full success

Any quantum system reproducing the semiclassical exterior facts of a
Schwarzschild horizon — flux law, per-resolved-mode thermal
statistics, KMS line asymmetry — is forced to entropy-rank source
participation by the static certificate.  With Q2's bridge and the
deposit-and-decode rung, the full program also certifies log-latency
access structure.  The semiclassical exterior facts stop being only
modeling inputs and become measurements on a theorem-backed
three-rung ladder.  This is an operational bootstrap of the horizon's
information-theoretic structure from exterior phenomenology, within
the stated class.

Demarcation consequence: everything exterior-operational about
evaporation is QI-forced by QFT-in-curved-space facts.  Combined with
the algebra-type seam (demarcation_algebra_type_synthesis.md), the
gravitational residue narrows to the value of `A/4G` (upstream state
count) and the lived interior (downstream).

N-portrait consequence: fork-not-refutation upgrades to
refutation-conditional-on-class.  The coherent branch's remaining
escape is exiting the class assumptions (e.g. a genuinely
non-equilibrium line); checking whether real N-portrait dynamics does
so becomes that branch's obligation, with a falsifiable O(1) signature
either way.

Referee honesty check: ETH-minded readers may find "thermality forces
entropy rank" expected.  The headline is the adjudicated fork — the
coherent-enhancement escape closed by computation — and the
operational certificates, not the forced branch.

### Ranked next directions

1. Dangerous-case stress tests: near-extremal/JT and dS.  FIRST PASS
   UPDATED 2026-07-05 (`nearextremal_ds_stress_test.md`, pulled
   forward): the framework is diagnostic at think-pass level.  dS and
   zero-line BPS sectors are consistent with the certificate scope:
   certificates track flux-participating rank and go silent when there
   is no emission line.  Near-extremal/JT is sharper than the original
   "blind to S_0" expectation: a semiclassical area-cross-section
   regime may certify S_0-sized participation, while strong-Schwarzian
   scattering may alter the line strength differently.  Two scope
   refinements adopted (leg-B reference value = microcanonical DOS
   ratio, mandatory at the Schwarzian scale; grand-canonical
   calibration for Kerr/RN, superradiance = inverted channels handled
   natively).  Remaining: the VERIFY list there (greybody exponents,
   Schwarzian evaporation, superradiant response factors), then a
   taxonomy row.  Original questions still worth keeping: dS:
   do the static certificates sharpen or collapse the section 0
   contrast engine (reservoir lemma: dS DOS = ordinary bath)?  AdS:
   the equilibrium side has an exact KMS dictionary, so the rank
   certificate applies there too — revising "latency certificates are
   forced, not chosen" into: statics work on both sides of
   Hawking-Page, latency is the evaporating-side-only rung.  Cheap
   relative to what it decides; do this first.

2. The interior via a fourth rung: decoder complexity.  The ladder is
   ordered by cost; arrival-latency vs decoder-complexity are separate
   exponents (already a remark in the saturation paper; Python's
   lunch, Harlow-Hayden).  Picks the parked learning-to-decode
   direction back up; points at the one open demarcation residue.
   Deepest, hardest.

3. Upstream: does degeneracy saturation force access saturation?  D2
   graduates from optional to the natural structural follow-on, with
   theorem-grade axes to track along the crossover; the
   saturon/corpuscular literature does not compute them.  Connects
   the framework to the other residue (why area-sized entropy).

4. Falsifiability to phenomenology: (a) tabletop asymmetry-rung
   protocol on cold-boson burden hardware (linear response, cheaper
   than the frozen-routing witness; bench bridge to 2509.22540);
   (b) PBH late-stage signature note (`g2` drift + growing KMS
   deviation at burden onset, `10^4-10^9 g` window).

5. Consolidation and distribution: trilogy restructure around the
   certificate result as flagship; demarcation answer is essay-shaped.
   Ranks last under results-first priorities; practical constraint
   (own-voice rewrite, no endorsement network) makes journal direct
   submission the realistic route.

Sequencing rationale: 1 before 2 — a framework whose certificates stay
diagnostic in JT and dS is worth pointing at the interior; one that
collapses there tells us where the real seam is, which is itself a
result.  The current program was born from exactly such a stress test
colliding with the memory-burden prototype.

## Discipline

- Keep fork-not-refutation framing.
- Keep source-rank saturation and HP latency separate.
- Do not claim `g2` alone measures rank.
- Always qualify the Q1 result as per-resolved-mode.
- The backreaction escape is closed for the strict class and
  clause-covered in general — say it that way, never bare "closed."
  Bare leg B needs the harmonic-line/unresolved-ladder clause or the
  two-resolution stability supplement; the pair needs no clause.
- Do not claim the positive boundary-ETH branch derives HP latency from
  source rank alone; it also needs scrambling/decoupling assumptions.
- Do not use "Dicke-like" without a computed statistic.
- Treat `S ~ O(1)` / Planck endpoint as diagnostics-only, not a regime
  for exponent-level statements.
- Do not claim to derive gravity, `G`, or Einstein dynamics.

## Read First

```text
prototype_m0_m1_results.md
prototype_m2_frozen_routing_countermodel.md
prototype_m3_discriminator_table.md
coherence_witness_g2_result.md
statistics_rank_link_result.md
asymmetry_backreaction_escape_result.md
participation_pigeonhole_result.md
q1b_static_certificate_theorem.md
nearextremal_ds_stress_test.md
operator_overlap_latency_lemma.md
q2_operator_overlap_bridge_theorem.md
horizon_property_separation_program.md
paper_boundary_saturation/main.tex
```
