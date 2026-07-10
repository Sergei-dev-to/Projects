# Prototype Adjudication: Current Roadmap

Date started: 2026-07-04
Updated: 2026-07-08

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
asymmetry, deposit-and-decode latency.  Q3 consequence, updated after
the route-2b deployment: per-mode thermality + detailed balance force
entropy-rank participation within the class once EFT charge
universality and the Planckian/QNM refill ceiling are supplied.  A
thermal collective channel preserves KMS and g2 = 2 in equilibrium but
develops a LOW-side deficit under persistent drain; only the latency
rung reaches refill dynamics without the Planckian input.

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
requires calibration eta <~ 1/(n_bar_eq sqrt(S)).  The remaining
static input is E' = the emission-envelope condition (no anomalously
bright exterior vertex); universality closes only its charge subroute.
The route-2b deployment below replaces the collective subroute's piece
of E' by the conditional Planckian/QNM refill bound.  The per-channel
cap is downstream of the ordinary-sector envelope plus the asymmetry
observable, not a third independent leg
(`participation_cap_decomposition_result.md`).
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

### Route 2b Deployment Check (2026-07-07/08)

**STATUS: done in `collective_channel_starvation_result.md`.**  The
envelope note's "dedicated check" executed: the 1601.01329 collective
coupling deployed as an emission channel gives EXACT static mimicry
(KMS, g2 = 2, rank one, K-fold bright — the residue was real), but the
strict deployment is reservoir-starved: the K-1 orthogonal modes are
exactly decoupled, so integrated flux fraction = 1/K, a flash not a
channel, with a SIGNED time-resolved signature (asymmetry starts
thermal and drifts sub-thermal; g2 pinned at 2).  General refill bound:
sustaining flux fraction f at KMS accuracy eta requires
rethermalization Gamma_th >~ f T/eta; with the Planckian/QNM cap
Gamma_th <= c_P T this gives f <~ c_P eta — parallel in form to the
route-1 bound f <= eta nbar_eq, but with the deficit on the LOW side
(starved-cold vs hoarded-hot).  Consequence: E' for route 2b is
DERIVED-modulo-Planckian rather than assumed; the collective-outlier
controls become (asymmetry observable, Planckian relaxation), while
the full rank theorem still uses the ordinary-sector envelope and EFT
universality for route 2a.  The latency rung remains the only
assumption-light reach into route 2b without the Planckian input
(backstop role, plus non-Markovian/coherent-refill corners and the
multiplexed bookkeeping, which are the note's open items).

### Active Gap-Closure Plan (2026-07-09)

The execution sequence for those open items is now fixed in
`certificate_gap_closure_plan_2026_07_09.md`.  Immediate priority is a
linewidth-parameterized stationary Gaussian spectral-starvation theorem,
followed by Gram-eigenchannel multiplexing and only then the
operator-specific black-hole/QNM gate.  That sequence supersedes the
broader Post-Completion Horizon ranking for active work until the
flagship certificate is locked.  Q2 remains a separate companion;
JT/Kerr/dS and phenomenology are deferred.

Progress update, same day:

```text
Phase 0: COMPLETE — theorem observables, widths, line/band ranks fixed.
Phase 1: COMPLETE for the stated class — exact stationary linear
         Gaussian spectral-starvation and flux/deficit identities;
         Markov limit recovered numerically.
Phase 2a: LANDED — one aggregate ratio admits exact HIGH/LOW
          cancellation at N_eff <= 2; paired g2 + separately resolved
          LOW flux + ordinary-tail control gives
          N_eff >= 1/(epsilon_g/kappa + c_-^2 + p).  Exact
          calibration at two drain strengths closes cancellation in the
          narrow stationary class by a monotonicity theorem; finite errors
          are bounded when the scan has a bounded starvation-ratio window.
```

The correction is demarcation-relevant: the current work is trying to
remove input 2 of the established necessity trinity (boundary-accessible
rank).  It has not yet done so.  Signed cancellation needs an operational
full spectral multi-setting closure, and the ordinary Gram-tail bound `p ~ 1/S`
remains the residual part of input 2.  Input 1 (`S(E) ~ E^2`) and input
3 (decoupling/typical encoding) remain separate.

### Q3: Branch-Forcing Think-Pass

After Q1b, stress-test candidate principles that might force real black
holes onto one branch:

```text
universal gravitational coupling -> entropy-rank participation?
graviton-condensate/N-portrait -> collective single-source branch?
semiclassical per-mode thermality -> exclusion or thermal mimicry?
```

Per-mode thermality is now the live forcing candidate, and Q1b
produced the sharp statement (`envelope_as_coupling_universality.md`,
framing corrected 2026-07-06): thermality + luminosity force
N_eff ~ S UNLESS the horizon emits through a thermalized bright
COLLECTIVE exterior channel.  The E' hypothesis reads as
"no anomalously bright exterior emission vertex," with two failure
modes: (2a) non-universal microscopic charge — closed by universality
(equivalence principle / Weinberg-Witten) in the EFT regime; (2b) a
sqrt(S)-coupled thermalized collective channel — NOT closed by
universality (it is ordinary Dicke coherence, not non-universal
gravity), and this is the real N-portrait-style escape.  Two
sub-findings: (a) the strict memory-burden prototype is
occupation-enhanced (K_0 = n_0 ~ S, exterior vertex envelope-scale),
so observables alone exclude it — route (2b) is not realized; (b) the
surviving escape is a dynamical question about the emission vertex,
localized and in-principle checkable, NOT a violation of the
equivalence principle.  Promote Q3 from think-pass: this is a
demarcation statement (rank is QI-forced modulo one sharply-posed
gravitational-dynamics question).

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

Tier 2 — line-response certification of source rank.  Current: Q1b
skeleton COMPLETE and route 2b deployed.  The static theorem remains
conditional on E', but the collective half of E' is now replaced,
within thermal Markovian refill, by `Gamma_th <= c_P T`.  Use the total
dangerous fraction `f_bad = f_occ + f_coll`, with occupation-enhanced
HIGH-side bound `f_occ <= η n̄_eq` and starved-collective LOW-side bound
`f_coll <~ m c_P η` for the single/equal-split cases.  Then
`N_eff^ord >= (1−f_bad)cS` and
`N_eff ~ min(cS,f_bad^-2)`.  Full total saturation still requires
`f_bad <~ S^-1/2`; a coarse finite-accuracy measurement gives a floor,
not an entropy-sized measurement.  Exact calibrated response forces
entropy rank only within the weak-emission, ordinary-sector-envelope,
EFT-universality, Planckian-relaxation, and refill-scope conditions.

Tier 3 — branch forcing (Q3 answer, conditional).  Current: the worst
branch has a rate rather than an unnamed vertex.  A thermal bright
collective channel is an exact equilibrium static mimic at rank one,
but persistent drain makes it sub-thermal unless refill is faster than
the horizon's thermal/QNM scale.  The coherent branch must therefore:
become entropy-rank participating; show the occupation-enhanced HIGH
signature; show the starvation LOW signature; exploit signed aggregate
cancellation at one setting; use a non-additive, nonlinear/non-Gaussian, or
nonstationary refill mechanism outside the spectral theorem; exploit
unresolved mixed-frequency multiplexing; or leave the calibrated class.  This is not an
assumption-free refutation of N-portrait dynamics.  The strict prototype
is still excluded more directly because it is route (1) occupation.

Tier 4 — certificate ladder completion.  Needs Q2 in addition.
Endpoint: the three-rung ladder (passive `g2`, probe line asymmetry,
deposit-and-decode latency) is theorem-backed end to end — line
response certifies source-rank floors under the named dynamics, while
the visible-algebra bridge supplies a necessary latency condition.
Do not state that Q2 proves a real black hole achieves HP recovery; it
proves that fast recovery requires order-one generator access,
nonlocal/dressed access, or side information.

Tier 5 — demarcation payoff (the program's stated goal).  Current
endpoint: source-rank saturation follows from exterior response only
after gravity supplies two dynamical facts — ordinary EFT coupling and
a thermal/QNM relaxation ceiling.  Quantum information consumes those
facts; it does not derive them.  The residue is therefore narrower than
the original trinity but larger than `A/4G` plus the lived interior:
the operator-specific thermal tie remains a genuine gravitational
input until the refill bound is derived microscopically.

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
statistics, and calibrated line asymmetry is forced toward
entropy-rank source participation by the response certificate once
ordinary-sector envelopes, EFT coupling universality, and the
Planckian/QNM refill ceiling are supplied.  A thermal bright collective
channel is invisible in an equilibrium snapshot, but persistent drain
makes it LOW-side nonthermal unless it refills super-Planckianly.  Q2's
latency rung remains the assumption-light backstop for refill dynamics
outside that class.  This is an operational bootstrap of the horizon's
information-theoretic structure from exterior phenomenology, but it is
conditional on named gravitational dynamics rather than QI alone.

Demarcation consequence: much of the exterior-operational package is
QI-forced after the state count, algebra, ordinary emission envelope,
and thermal/QNM dynamics are supplied.  Combined with the algebra-type
seam, the remaining gravitational residues are `A/4G`, the
operator-specific thermal tie that underwrites the refill ceiling, the
exact-to-semiclassical algebra transition, and the lived interior.

N-portrait consequence: fork-not-refutation upgrades to a conditional
rate test.  The strict 2006 prototype is route-1 occupation and is
statically caught.  A different N-portrait can build the rank-one
thermal collective vertex, but persistent Hawking-sized output then
requires super-Planckian refill or a mechanism outside the thermal
Markovian class.  Demonstrating that mechanism becomes the branch's
obligation; absent it, starvation predicts a signed LOW-side response
deviation while `g2` remains two.

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
participation_cap_decomposition_result.md
collective_channel_starvation_result.md
collective_channel_spectral_starvation_theorem.md
signed_cancellation_and_gram_tail_result.md
certificate_gap_closure_plan_2026_07_09.md
q1b_static_certificate_theorem.md
envelope_as_coupling_universality.md
nearextremal_ds_stress_test.md
operator_overlap_latency_lemma.md
q2_operator_overlap_bridge_theorem.md
horizon_property_separation_program.md
paper_boundary_saturation/main.tex
```
