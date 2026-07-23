# Cross-field ranking: open problems susceptible to a powerful model

Status cut: **2026-07-22**.  This report ranks attack targets, not famous
conjectures.  It follows a core screen of 108 scored entries: 31 in algorithms and
optimization, 35 in discrete mathematics, and 42 in algebra, number theory,
topology, and geometry.  Seven intentionally overlapping cross-field entries
(for example Hadamard 668 and Conway's 99-graph) leave **101 distinct attack
targets**.  A separate 12-entry FrontierMath control pass added nine new clean
targets, for **120 scored entries and 110 distinct targets** overall.  Three
current claim/solution cases in that control set were excluded rather than
scored.

> **Post-campaign correction (2026-07-23).** The stretched-LR target ranked here
> was subsequently mistranslated, its representation advantage overstated, and
> its effective score reassessed from 25 to about 19. The bounded campaign is now
> closed with no counterexample and one narrow four-row obstruction. See
> `CLOSURE.md`. The table below is retained as the original dated ranking, not as
> a current recommendation.

## What changed after the first-pass scores

A compact verifier is only an entry ticket.  The final rerank adds four facts
that the raw score does not capture:

1. Does the easy-to-certify side probably exist?
2. Has this precise target already been exposed to frontier-model campaigns?
3. Is there a second representation capable of changing the search geometry?
4. Can failure still produce publishable structural mathematics?

This removes many seductive but poor bets.  A projective plane of order 12,
the missing Moore graph, Conway's 99-graph, a Markoff-uniqueness collision,
MUB(6), and classical Diophantine counterexamples all have beautiful positive
verifiers.  In each case, however, the desired object may simply not exist,
and the opposite side has no comparably compact certificate.

The opportunity bands below are deliberately qualitative.  There is no
calibration set from which defensible numerical probabilities could be
estimated.  They assume **one serious, well-scaffolded campaign**: specialist
literature and software, model-written experiments, exact verification, and
independent review.  “Full” means the named target is resolved; “paper”
includes a new bound, exhaustive subcase, reusable search theorem, or
certified structural obstruction.

## Recommended five-problem portfolio

| Rank | Target | Outcome prior | Full-hit tier | Paper-yield tier | Why a model has unusual leverage |
|---:|---|---|---:|---:|---|
| 1 | Determine exact selection value `V_7(16)` | guaranteed answer | medium | high | Existing forward/backward code and independent checks expose a precise memory frontier. A new poset quotient, admissible bound, or bidirectional metric beyond the classical splice ruled out in the paper can be tested immediately. |
| 2 | Trivialize the four-pentachoron sphere `Q` | favored, but not guaranteed | medium | high | One exact start state, a replayable Pachner-move certificate, public software and hundreds of thousands of nearby triangulations; the missing ingredient is search policy/macros, not an unknown verifier. |
| 3 | Construct a perfect one-factorization of `K_64` | favored | low--medium | medium--high | The output is only 63 perfect matchings and every pair is checked by a Hamilton-cycle test. Starters, quasigroups, Latin squares, switching, and group extensions provide genuinely different searchable languages. |
| 4 | Find a negative coefficient in a stretched Littlewood--Richardson polynomial | live; problem author expects false | low--medium | medium | The final witness is three small partitions. Hive polytopes turn the problem into exact Ehrhart computation; negative-Ehrhart templates can be searched or transferred structurally instead of enumerating tableaux blindly. |
| 5 | Construct a Hadamard matrix of order 668 | strongly favored | low--medium | medium | The sign matrix has a perfect exact verifier, and Legendre pairs, supplementary difference sets, cocycles, block designs, and switching expose multiple construction languages. Existing classical and AI searches make a new representation mandatory. |

The five were selected as a portfolio: selection is an exact optimization
target, `Q` a path-finding target, `K_64` a compact finite design,
Littlewood--Richardson a high-upside counterexample hunt, and Hadamard 668 a
larger construction target with an unusually strong existence prior.

## Why these five

### 1. Exact selection at `V_7(16)`

`V_i(n)` is the optimal worst-case number of comparisons needed to select the
`i`th element among `n`.  The 2025 computation settles all `n <= 15` and
`V_i(16)` for `i <= 6`, leaving `V_7(16)` in the range 28–33.  Upper
certificates are comparison decision DAGs; lower bounds come from exhaustive
adversary/poset computation and were independently recomputed by two search
directions.

Unlike an existence conjecture, an exact answer is guaranteed.  But it is not
a small-certificate problem: the current computation consumed days, hundreds
of gigabytes, and billions of posets.  The opening is to synthesize a stronger
admissible lower bound or quotient of reduced posets.  The paper explains why
a classical meet-in-the-middle splice does not work, so any bidirectional
proposal must improve the information metric rather than merely join the two
existing searches.

**First experiment.** Hold out several known values, require a new bound or
canonical state representation to reduce expanded states by at least 10x
without changing any answer, and only then run `V_7(16)`.  Stop if the held-out
gain does not materialize.

### 2. The hard four-pentachoron sphere `Q`

The current census paper isolates the triangulation with Regina signature
`eAMPcaabcddd+aoa+aAa8aQara`.  It is topologically a 4-sphere, but no
Pachner path to the standard PL sphere is known.  Exhaustive traversal proves
that a path, if it exists, must pass through a triangulation with at least 12
pentachora.  The authors conjecture the relevant 4-ball and the residual
spheres are standard.

This is unusually clean.  A move sequence is a complete certificate; Regina
can replay every local move.  The existing 2/4/6-pentachoron census supplies
easy examples, hard negatives at bounded height, and state pairs for learning
macros.  The model should not merely tune a random walk: it should alternate
among Pachner states, Kirby/handle descriptions, discrete Morse functions,
and the Cappell–Shaneson subcomplex identified in the paper.

**First experiment.** Reproduce the exhaustive Pachner component through ten
pentachora, build a
bidirectional proof-logging search, learn macro moves on solved hard spheres,
and test whether the policy beats the published heuristic by a preregistered
factor on held-out examples.  Stop before scaling if it does not.

### 3. A perfect one-factorization of `K_64`

A perfect one-factorization partitions all edges of `K_64` into 63 perfect
matchings so that the union of any two is one Hamilton cycle.  `K_64` is the
smallest current open order; the former smallest case, `K_56`, required a
bespoke construction.

The certificate is roughly two thousand edges and has a trivial checker.
More importantly, the same object can be represented as matchings, starters,
row-Hamiltonian quasigroups, constrained Latin squares, or group-developed
blocks.  Humans have searched several favored symmetric families, but there
is no global enumeration modulo all equivalences.  A model can propose and
mutate construction grammars, use exact local repair, and then explain a
successful artifact algebraically.

**First experiment.** Reproduce `K_56`, train the grammar search on known and
withheld orders, then search every group of order 63 plus controlled symmetry-
breaking/switching extensions.  Stop if the method cannot rediscover withheld
constructions at competitive cost.

### 4. Negative stretched Littlewood–Richardson coefficient

For partitions `lambda, mu, nu`, the stretched coefficient is a polynomial in
`t`.  The open positivity conjecture says all of its coefficients are
nonnegative.  The concrete target asks for partitions of length at most 7 and
size at most 30 with a negative coefficient.  The problem author assigns the
constrained target a 60–80% chance of having a solution and expects the
conjecture to be false.

This resembles the useful part of the recent counterexample pattern: the
statement has a small exact witness, the search parameters are combinatorial,
and there is no compelling positivity mechanism.  The key representation is
the hive polytope: the stretched coefficient is its Ehrhart polynomial.
Instead of a flat triple-of-partitions scan, search for hive polytopes carrying
local configurations known to create negative Ehrhart coefficients, then
solve the inverse boundary problem.

**First experiment.** Build two independent exact LR/Ehrhart evaluators;
enumerate all lower-length cases to map the true frontier; then run a
counterexample-guided search over hive combinatorial types.  Stop the bounded
pass at the stated length/size limits and publish only if the exhaustive scope
or a new structural obstruction is independently auditable.

### 5. A Hadamard matrix of order 668

A Hadamard matrix is a sign matrix with mutually orthogonal rows.  Order 668
is the smallest unresolved multiple of four, and the current benchmark's
specialist estimate puts existence at 95--99%.  A CSV of signs is sufficient;
integer matrix multiplication verifies the result.

The target is fifth, not first, because it is exposed and computationally
mature.  A March 2026 AI-led campaign exhaustively found over twelve million
compatible 9-compression cases and mapped the bottleneck in the Legendre-pair
route without finding a matrix.  That does not search all Hadamard matrices;
it says another annealing run in the same ansatz has little information value.
A model campaign should synthesize construction grammars across supplementary
difference sets, cocyclic matrices, block substitutions, switching, and
spectral decompositions, with equivalence-aware exact completion.

**First experiment.** Reproduce known constructions at neighboring difficult
orders and withhold entire construction families during training.  Proceed to
668 only if the grammar system rediscovers withheld matrices and produces a
new equivalence class or compression pattern; otherwise stop before a large
heuristic search.

## Closest alternates

| Target | Why it nearly made the five | Why it did not |
|---|---|---|
| 46-pentachoron K3 triangulation | Exact finite construction; improvements from 54 toward 46 are independently publishable. | Certifying PL identity can be harder than generating a face pairing; specialist tooling burden is higher than for `Q`. |
| Polynomial with Galois group `M_23` | Fewer than 100 digits, exact group verification, major significance, and specialists expect existence. | The relevant locus is extremely thin; known rigidity/braid methods fail for structural reasons, and the path from a promising orbit to a polynomial is less bounded. Best moonshot. |
| Large Steiner system with `5 < t < 10`, `v < 200` | No explicit nontrivial Steiner system with `t > 5` is known; a construction would be a solid result with a trivial incidence checker. | Existence below 200 is only plausible, not assured, and the output/search space can be enormous. |
| Non-3-colorable simple great-circle arrangement | First unchecked size is 12; oriented matroids plus DRAT give a clean coupled search. | The conjecture may be true, so the attractive certificate side may not exist. |
| Genus-zero polycube with no grid-edge unfolding | Low saturation and completely discrete geometry; exhaustive cut-tree certificates are possible. | No standard proof-log format exists and the smallest counterexample could be large. |
| Conway 99-graph | Tiny exact graph certificate and several representations. | Existence is genuinely uncertain; a 2026 SAT study found the obvious encodings computationally ineffective. |
| Kaplansky zero divisor | Gardam's neighboring unit-counterexample and the new oriented-product sieve make this conceptually attractive. | Multiplication is easy to check, but proving the presented group torsion-free is a serious hidden certificate burden. |

## Important exclusions

Live 2025–26 resolution claims were not treated as clean open targets.  In
particular, the characteristic-3 del Pezzo “eight singular points” problem has
a March 2026, 236-page claimed seven-point theorem; regardless of its eventual
validity, the next task there is independent proof adjudication.  The same
conservative rule excludes the `Q_2` presentation: Epoch's July 6 update says
Claude Fable 5 and GPT-5.5 Pro produced verifier-accepted candidates that are
likely correct, although complete proofs remain under review.  It also
excluded the Jacobian conjecture, cycle double cover, Barnette, union-closed
sets, moving sofa, and other items with serious current claims.  This prevents
a stale problem list from masquerading as research taste.

## Bottom line

If maximizing the chance of *any* new theorem, start with exact selection.
`Q` is the strongest higher-value path-finding alternative.  If deliberately
seeking another compact counterexample, choose
stretched Littlewood–Richardson positivity—not a famous conjecture whose
counterexample would be easy to check but is probably nonexistent.

The reusable rule is:

> Prefer one exact artifact, a measured frontier, two non-equivalent
> representations, and a publishable failure mode.  Easy verification alone
> is not enough.
