# Smale 6 counterexample-search retrospective

**Snapshot:** 2026-07-22  
**Scope:** the Roberts positivity-repair and Chen--Hsiao ramification
experiments in `smale6-repair/` and `smale6-ramification/`  
**Purpose:** record the research objective, pivots, accepted and rejected
hypotheses, evidentiary standards, and revisit conditions so that a future
search does not repeat the same attractive but structurally exhausted ideas.

**Closure notice (2026-07-22):** the next-work recommendations in Sections
17--18 are retained as historical decisions but are superseded by
smale6-theory/GATE_DECISION.md. The square-lift theorem-consolidation gate
passed, and the present counterexample-search program is closed.

**Executive conclusion:** no Smale 6 counterexample was found.  We did obtain
two exact exclusions: the fixed-cloud and finite coefficient-wise co-moving
shell repairs of the Roberts signed mechanism are impossible, and the
particularly suspicious positive
Chen--Hsiao degeneracy is an ordinary mass fold rather than a fixed-mass
continuum.  Our present counterexample frontier is a systematic search for
exceptional singularities whose fixed-mass Lyapunov--Schmidt obstructions
vanish for a structural reason.

**Validation status:** the repair propositions are exact arguments recorded
in project notes.  The fold result is a custom computer-assisted certificate
with exact interval decisions, independent implementations of its vulnerable
derivatives, and multi-precision regression checks.  Neither set of results
has yet been peer-reviewed or independently replicated outside this effort.

## 1. What we were actually trying to do

Smale's sixth problem asks whether, for fixed positive masses, the planar
Newtonian \(n\)-body problem has only finitely many central configurations
modulo translations, rotations, and positive scaling.

Our objective was not initially to prove another special case.  It was to
look seriously for a counterexample by finding a positive-dimensional fiber
of the mass projection

\[
\pi:\{(q,m):q\text{ is a normalized central configuration for }m\}
\longrightarrow \{m_i>0\}.
\]

The decisive reduction is that an infinite fixed-mass fiber cannot be merely
a countable collection of isolated configurations.  After gauge fixing and
introducing positive reciprocal distances \(u_{ij}\) with

\[
u_{ij}^2\lVert q_i-q_j\rVert^2=1,
\]

the collision-free central-configuration set is semialgebraic.  A
zero-dimensional semialgebraic set is finite.  Therefore an infinite fiber
has positive dimension and contains a semialgebraic, piecewise analytic arc.

This tells us what a counterexample detector must find: a fixed-mass tangent
that is not merely infinitesimal but survives every nonlinear compatibility
condition.  It also tells us that searching for exotic countably infinite
"dust" is unnecessary.

## 2. The meta-hypothesis borrowed from the Jacobian/Fable episode

We did not have Fable's complete internal search trace available.  What we
borrowed was an inferred workflow, not a historical claim about its exact
sequence of thoughts: negate the conjecture operationally, choose a
low-complexity witness class, search where prevailing methods do not look,
and verify the resulting artifact independently of the search process.

The useful lesson was not "let an AI brute-force formulas."  It was that a
long-believed conjecture can leave systematically bare regions because the
field has optimized for proving the expected answer.  Counterexample search
then becomes a different research program:

1. Identify where generic theorems explicitly stop.
2. Identify configurations that standard algorithms skip because they are
   singular, badly conditioned, or lie on a special stratum.
3. Change representation until the conjectured obstruction becomes a finite
   set of falsifiable compatibility conditions.
4. Use computation to reject many candidates cheaply and reserve exact proof
   machinery for genuine survivors or strategically important boundary cases.

For Smale 6, this pointed toward exceptional mass loci, degenerate positive
configurations, constrained-stratum boundaries, and the signed examples that
show exactly what positivity must prevent.  It did **not** make Smale 6 likely
false; it gave us a principled map of where a false statement would most
plausibly have escaped existing methods.

## 3. The landscape that determined our priorities

The working literature snapshot was:

- The planar four-body problem is finite for all positive masses.
- For five bodies, generic positive masses are covered, while the
  Albouy--Kaloshin analysis leaves a codimension-two exceptional mass set.
  "Exceptional" means the proof does not apply, not that a continuum exists.
- Several particular exceptional five-body mass choices have subsequently
  been handled by certified enumeration, but not the whole exceptional set.
- The six-body problem is much less resolved; attempts to extend the known
  symbolic asymptotic-diagram programs remain incomplete.

This made \(n=5\) the right first falsification laboratory.  It is the first
dimension not already settled for all positive masses, the uncovered
mass set is explicit enough to target, and the full configuration space is
still small enough for exact local and interval calculations.  Beginning at
\(n=6\) would have mixed the counterexample question with a much larger,
still-incomplete classification of asymptotic diagrams.

We distinguished four possible mechanisms:

1. **Repair a known signed continuum.**  Start with Roberts' exact family and
   replace the negative mass by a positive subsystem.
2. **Integrate a known positive degeneracy.**  Find a fixed-mass analytic arc
   through a singular positive central configuration.
3. **Find a different component at an exceptional mass.**  A known singular
   point may be harmless while another configuration at the same masses lies
   on a positive-dimensional component.
4. **Move to a broader exceptional locus or higher \(n\).**  Search
   systematically only after the \(n=5\) candidate and rejection machinery is
   working.

The first two mechanisms were tested.  The third and fourth remain open.

## 4. Phase I: trying to repair the Roberts continuum

### Why we accepted the direction

Roberts gives an exact one-parameter family

\[
(\pm a,0),(0,\pm b),(0,0),\qquad a^2+b^2=1,
\]

with masses \((1,1,1,1,-1/4)\).  It is the cleanest available model of the
phenomenon we wanted, missing the positive-mass hypothesis by one sign.  The
initial idea was that a finite positive cluster or shell might reproduce the
effective force of the negative central mass while retaining the same shear.

This was attractive for three reasons: the target family was exact, the
symmetry reduced the equations drastically, and signed or otherwise
"unphysical" constructions are precisely the sort of discarded neighboring
space from which a valid counterexample might sometimes be recovered.

### What we tried

- a fixed positive auxiliary cloud;
- concentric homothetic rhombi and rectangles;
- finite coefficient-wise co-moving shells;
- affine motion in normalized squared-distance space;
- direct local emulation of the missing outward force.

### What was accepted

The experiment produced exact reusable obstructions, recorded in
`smale6-repair/RESULT.md`:

- A finite positive cluster cannot be gravitationally neutral in the needed
  sense: its internal accelerations cannot all equal one common vector.
- A nontrivial positive-mass central-configuration curve cannot be affine in
  normalized squared-distance space; it must have a strictly positive
  weighted curvature component.
- A fixed positive cloud cannot accompany an open interval of the Roberts
  shear.
- Neither can any finite coefficient-wise co-moving shell, including nested
  homothetic rhombi or rectangles.

The calculation also found a useful near miss: outer positive pairs can
exactly replace one missing force component, but unavoidable cross-coupling
makes the \(x\)- and \(y\)-multipliers disagree except at the isolated square.

### What was rejected

The hypothesis that the negative mass is a local defect replaceable by a
finite positive module was rejected for all the classes above.  Adding more
shells or more parameters within the same coefficient-wise mechanism would
not address the proof; it would only enlarge an already excluded ansatz.

This was also less unexplored than it initially appeared.  Roberts himself
noted the natural replacement of the negative center by symmetric positive
bodies.  Our contribution was to turn broad versions of that temptation into
exact no-go statements, not to discover an untouched construction paradigm.

### What was parked rather than rejected

A nonlinear, compact, collision-free positive continuation that turns or
branches before the Roberts collision endpoints is not excluded.  Nor is a
topology-changing construction unrelated to finite neutral-cluster
emulation.  These may be revisited only if a new mechanism explains how they
evade both the curvature and collision-cluster obstructions.

### Stop decision

We archived the Roberts-specific branch.  The workflow lesson is:

> Once an exact argument eliminates the mechanism, do not continue by adding
> decorative parameters to the same mechanism.  Require a sentence stating
> which hypothesis of the no-go theorem the new proposal violates.

## 5. The pivot: from constructing a family to auditing ramification

The repair failure changed the search question.  Instead of starting with a
beautiful one-parameter ansatz and trying to force positivity, we began with
the mass projection itself.

If \(F(x;m)=0\) is a gauge-fixed central-configuration system, choose a
regular point and a parameterization of a nonconstant fixed-mass arc with
\(x'(0)\ne0\).  Then

\[
D_xF(x_0;m)x'(0)=0.
\]

Thus every nontrivial arc passes through fixed-mass degeneracy.  But
degeneracy is only a necessary first-order condition.  Expanding

\[
x(t)=x_0+t v+t^2x_2+\cdots
\]

produces successive range-compatibility conditions.  A nonzero projection
onto the left kernel at any finite order rejects that tangent as the germ of
a fixed-mass arc.

This led to the jet sieve in `smale6-ramification/jet_sieve.js`.  Its controls
were deliberately opposite:

- Roberts' genuine signed continuum survives through every implemented
  order.
- The positive Palmore triangle-center degeneracy fails the numerical
  order-two sweep, as an ordinary bifurcation should.  It is retained as a
  calibration, not claimed here as a new exact result.

The important methodological shift was from **searching over hand-designed
shapes** to **searching over singular fibers and their integrability**.

## 6. Why Chen--Hsiao was accepted as the first live target

The Chen--Hsiao point was not chosen merely because a determinant vanished.
It combined five independent reasons for attention:

1. all five masses are positive;
2. it is a genuine Hessian/shape degeneracy, not a rotational or scaling
   artifact;
3. its masses lie on Albouy--Kaloshin exceptional relations;
4. the later theorem on the special three-collinear trapezoid family studied
   the constrained stratum, not necessarily transverse full-planar motion;
5. the 2026 certified-enumeration paper explicitly says its program would
   fail to establish finiteness at this degenerate value.

This was exactly the kind of seam the meta-program sought: a known positive
singularity sitting between a geometric classification and an interval
pipeline, with neither work resolving the full fixed-mass transverse germ.

The initial calculation found that the one-dimensional kernel leaves the
three-collinear stratum immediately.  That observation justified examining
the full configuration space rather than simply invoking the constrained
family result.

## 7. What the Chen--Hsiao calculation accepted and rejected

### Cheap discovery-stage result

The full numerical jet calculation found a large nonzero order-two
obstruction.  This rejected the candidate as a fixed-mass continuum long
before the interval proof was built.

This is the generic outcome that we should expect in future searches:

> A degenerate central configuration is usually a fold or another finite
> bifurcation, not evidence of an infinite fiber.

### Why we nevertheless certified it

Certification was justified here because the point occupied an explicit gap
in the literature and because the resulting machinery would be reusable.  We
needed to eliminate several ways the numerical rejection could have been
misleading:

- a determinant bracket did not prove an exact singular point;
- a numerical SVD did not prove corank one;
- the symmetric slice could have missed an odd, symmetry-breaking kernel;
- the tangent to the published mass-and-shape family is tangent to the
  discriminant and therefore is not a transverse fold parameter;
- a floating-point quadratic projection was not a proof of fixed-mass
  isolation.

The final polynomial Moore--Spence/Krawczyk certificate established an exact
root, full-planar corank one, a nonzero fixed-mass quadratic coefficient, and
nonzero transversality when \(\nu\) varies with \(\mu\) fixed.  The local
normal form is

\[
\nu(c)=\nu_*-\kappa c^2+O(c^3),\qquad \kappa>0.
\]

The full result and verifier are in
`smale6-ramification/CERTIFIED_FOLD.md`.

### Precise rejected claim

The Chen--Hsiao configuration is not on a fixed-mass continuum.  In a local
neighborhood of this configuration and its exact masses, the branch is an
ordinary fold with locally zero, one, or two solutions in a fixed nearby
fiber.

### What this did not reject

- another component elsewhere in the fiber at the same exact masses;
- another singular point on the two-equal-pairs mass family;
- other Albouy--Kaloshin exceptional components;
- a positive continuum for a different \(n\).

The word "area" is therefore safe only in a local joint
configuration--mass sense.  Analytic fold theory clears a neighborhood of
this branch qualitatively, but the certificate does not give a global region
of mass space or an explicit uniform neighborhood radius.

## 8. Decision register

| Candidate or claim | Decision | Evidence | Revisit condition |
|---|---|---|---|
| Roberts signed continuum | Accepted as a control, invalid as a counterexample | Exact family with one negative mass | Never treat it as positive evidence without changing the sign mechanism |
| Finite positive neutral replacement | Rejected exactly | Positive-cluster virial identity | Only if the proposed subsystem is not finite, positive, and internally Newtonian |
| Fixed positive cloud along Roberts shear | Rejected exactly | Analytic continuation plus collision-cluster contradiction | Only if the original shear or fixed-cloud hypothesis is abandoned |
| Finite coefficient-wise co-moving shells | Rejected exactly | Endpoint collision and direct outer-body force obstruction | Only with genuinely nonlinear motion or pre-endpoint branching |
| Affine normalized squared-distance lift | Rejected exactly | Strict convexity of the positive potential | Only if the distance path bends with the required positive curvature |
| Line or conic in the full projective squared-distance image | Rejected exactly for fixed positive masses | Constant potential, square-class separation, and a pole argument | Only at projective degree greater than two, with varying/signed masses, or outside the full-distance hypothesis |
| More nested rhombi/rectangles | Archived blind alley | Covered by the co-moving-shell theorem | Do not revisit by increasing shell count |
| Nonlinear compact Roberts-inspired lift | Parked | Not covered by current no-go theorems | Require an explicit mechanism evading both no-go arguments before computing |
| Roberts invariant geometrization | Accepted as explanatory prior art, not reopened as a search track | Roberts's constant-potential identity; later neutral-configuration/orthogonal-doubling formulation | Revisit only with a mechanism that survives the positive-cluster virial obstruction |
| Potential-exponent transfer of the Roberts family | Archived as a signed regression family | Exact central mass is negative throughout the logarithmic-to-Newtonian family | Revisit only after locating a distinct fixed-positive-mass continuum at another exponent |
| Palmore positive degeneracy | Retained as a numerical nonintegrable calibration | Order-two sweep, consistent with the known/expected cubic behavior | Reuse to test implementations; no new exact claim is made here |
| Chen--Hsiao constrained family alone | Rejected as sufficient analysis | Kernel leaves the three-collinear stratum | Full-planar calculation is mandatory |
| Chen--Hsiao fixed-mass germ | Rejected and certified | Exact Krawczyk root, full corank one, nonzero quadratic coefficient | Closed locally |
| Other configurations at the Chen--Hsiao masses | Open | Not searched globally | Global certified cover of the normalized fiber |
| Whole \((1,1,\mu,\mu,\nu)\) exceptional family | Open; strongest falsification target identified in this program | Only one singular point classified by this effort | Systematic discriminant and higher-order ramification census |
| Other five-body exceptional mass components | Open | Generic theorem does not cover them | Prioritize components with explicit algorithmic or stratum gaps |
| Six-body unresolved diagrams | Deferred | Search space and literature classification are much larger | Revisit after the singularity-census pipeline works at \(n=5\) |

## 9. Accepted and rejected inferences

The following distinctions should be treated as hard rules.

### Accepted

- Infinite fixed-mass fiber \(\Rightarrow\) positive-dimensional
  semialgebraic component \(\Rightarrow\) analytic arc somewhere.
- Fixed-mass arc \(\Rightarrow\) nontrivial kernel of the full reduced
  Jacobian.
- Nonzero finite-order Lyapunov--Schmidt obstruction \(\Rightarrow\) that tangent does
  not integrate to an arc.
- Corank one plus nonzero quadratic projection \(\Rightarrow\) local isolation at fixed
  mass.
- Adding a nonzero mass-direction projection \(\Rightarrow\) ordinary fold in that mass
  direction.
- Finite isotropy can forbid particular low-order equivariant jets, but each
  actually allowed coefficient must still be computed.  In the variational
  fixed-mass reduction, the cubic map
  \(u\mapsto\lVert u\rVert^2u\) is always symmetry-allowed.

### Rejected

- "The Jacobian determinant vanishes, therefore a continuum may be nearby."
- "A large numerical null vector proves exact degeneracy."
- "The symmetric or geometrically constrained stratum is the full problem."
- "Finite survival of a jet proves a curve."  It is only a discovery signal.
- "Local isolation proves the entire mass fiber finite."
- "Exceptional mass" means "likely counterexample."  It often means only
  that a generic proof or chosen reduced system loses rank.
- "A more elaborate version of an excluded ansatz is a new direction."
- "A finite symmetry group can by itself force all Lyapunov--Schmidt orders
  to vanish."  It is a low-order filter, not an all-orders identity.
- "An irreducible representation occurring in a symmetric power proves that
  the corresponding obstruction is nonzero or has an isolated zero."

## 10. What appears original, and what does not

No priority claim is made without a broader literature audit.

Already known were the Roberts signed continuum, Roberts' suggestion of
positive symmetric replacement bodies, the Chen--Hsiao family and its
degenerate point, the exceptional mass relations, and the general
Lyapunov--Schmidt, Moore--Spence, and Krawczyk methods.

The potentially new mathematical outputs are narrower:

- the exact affine-distance, fixed-cloud, and finite co-moving-shell
  exclusions tailored to Roberts repair;
- the exact projective-conic exclusion for the full normalized
  squared-distance image;
- identification of the Chen--Hsiao kernel as transverse to the
  three-collinear stratum;
- the fixed-mass quadratic obstruction at that point;
- the exact full-planar fold certificate and its direction in mass space.

The search strategy itself is a non-obvious synthesis rather than a new
mathematical technique: use gaps left by generic finiteness theorems and
certification failures to generate candidates, then use formal integrability
as an aggressive rejection filter.

## 11. Stop/go protocol for future candidates

Every candidate should pass these gates in order.

### Gate 0: capability

State how the proposal could produce a positive-dimensional **fixed-mass**
fiber.  A family whose masses vary is not a candidate until a fixed-mass
tangent is identified.

### Gate 1: literature gap

Name the exact uncovered cell: mass locus, geometric stratum, local versus
global question, and which theorem or program stops there.  Search the
original source for whether the "natural" ansatz was already attempted.

### Gate 2: cheap geometry

Check positivity, collision freedom, gauge validity, compact normalized
closure, and any virial/convexity obstruction before fitting parameters.

### Gate 3: full first-order rank

Compute the kernel only after quotienting translations, rotation, and scale.
If symmetry is used, split the full tangent space and inspect every odd block.
A determinant alone is insufficient.

### Gate 4: formal integrability

Project the quadratic term onto the left kernel immediately.  For higher
corank, test the full quadratic obstruction on the kernel sphere.  Continue
to higher jets only if the lower obstruction vanishes.

**Stop rule:** at corank one, a robust nonzero projected obstruction rejects
the candidate as a continuum source.  At higher corank, a nonzero value for
one sampled tangent rejects only that tangent; archive the point only after
proving that the obstruction map has no zero on projective kernel space (or
after an equivalent rigorous exhaustion).  Do not build a bespoke interval
proof for every rejected point.  Escalate only if the point fills an explicit
literature gap, supplies a reusable benchmark, or the numerical separation
is questionable.

### Gate 5: exact local dimension

A jet survivor must be converted to a polynomial or rational system and
checked by exact algebraic dimension, interval Newton/Krawczyk, or a validated
Lyapunov--Schmidt reduction.  Finite-order survival is never the final result.

### Gate 6: local/global accounting

Before announcing progress on Smale 6, write one sentence each for:

- the local germ that was classified;
- the part of the fixed-mass fiber actually covered;
- other masses and components left untouched.

If only the first sentence is nonempty, the result is a local calibration,
not a substantial clearing of the conjecture.

## 12. Where the program should go next

Stepping back changes the ranking slightly from the immediate conclusion of
`CERTIFIED_FOLD.md`.

### Counterexample-discovery track: first priority

Perform a **systematic higher-order ramification census** on the
two-equal-pairs family

\[
(1,1,\mu,\mu,\nu).
\]

Instead of selecting another attractive known determinant zero, solve for
the singular set of the full reduced equations and evaluate the
Lyapunov--Schmidt quadratic coefficient across it.  Ordinary folds are to be
discarded automatically.  The genuine targets are:

- corank-one points where the quadratic projection also vanishes;
- corank-two or higher points;
- components on which several fixed-mass jet obstructions vanish
  identically;
- transitions where a full-space mode is missed by a constrained stratum or
  reduced-system choice.

A merely small quadratic coefficient is not enough.  A high-priority
candidate should offer an exact symmetry, factorization, conservation
identity, or other mechanism that could force the quadratic and later
reduced coefficients to vanish.

This is the closest analogue of the Fable lesson: change the search object
from human-selected configurations to an automatically generated
discriminant-with-integrability map.  The Chen--Hsiao certificate supplies a
calibrated ordinary-fold case that this pipeline must reject.

### Closure track: second priority

Perform a certified global enumeration at the exact Chen--Hsiao masses,
using the fold certificate as a dedicated singular chart and ordinary
interval boxes elsewhere.  This could close the entire fiber and might find
another component, but absent such a discovery it is a proof-oriented closure
project rather than the highest-yield counterexample search.

The exact pair \((\mu_*,\nu_*)\) is implicitly and jointly defined by the
certified augmented root.  Its two displayed intervals are not independent
mass parameters.  A global proof must preserve that correlation through the
augmented defining equations or prove a uniform result over the entire
rectangular enclosure; simply substituting the two interval boxes would not
by itself prove finiteness at the exact pair.

### Expansion track: after the pipeline works

Apply the census to other Albouy--Kaloshin exceptional components, prioritizing
those where current interval methods report undecided boxes or where geometric
results live in a proper stratum.  Move to unresolved six-body asymptotic
diagrams only when the \(n=5\) machinery can generate and reject candidates
without bespoke coordinate work at each point.

## 13. Bottom line

We did clear real territory, but the main value of the sequence is a sharper
search discipline.

- The Roberts branch taught us that positivity cannot be repaired as a local
  force-sign substitution by fixed clouds or finite coefficient-wise
  co-moving shells along the Roberts shear.
- The Chen--Hsiao branch taught us that a conspicuous positive degeneracy is
  usually just a fold and that constrained-family or determinant analyses are
  not enough.
- The certificate closed one strategically important local germ and produced
  a trustworthy calibration case.
- The original counterexample objective now calls for a broad discriminant
  and integrability census, not another hand-picked singularity and not an
  immediate retreat into proving finiteness at one mass.

The next experiment should therefore begin with a candidate generator and
the stop/go gates above.  If it begins with another elegant geometric ansatz,
the burden is to explain what structural mechanism makes it different from
the two archived blind alleys.

## 14. Artifact map

The technical result files should remain result-centered.  This document is
the cross-project decision record.

| Artifact | Role and status |
|---|---|
| `smale6-repair/RESULT.md` | Exact Roberts-repair exclusions and their scope; authoritative for Phase I |
| `smale6-repair/nested_rhombi.js` | Discovery and held-out residual calculations; not itself the proof of the no-go theorems |
| `smale6-ramification/RESULT.md` | Double-precision Chen--Hsiao discovery calculation, controls, and literature seam |
| `smale6-ramification/jet_sieve.js` | Reusable finite-order candidate triage; survival is not a proof |
| `smale6-ramification/ch_fold_certificate_design.js` | Numerical design notebook for the later certificate; superseded as evidence by the exact verifier |
| `smale6-ramification/CERTIFIED_FOLD.md` | Authoritative local theorem, proof chain, and limitations |
| `smale6-ramification/fold_certificate.js` | Polynomial augmented system and numerical seed generation |
| `smale6-ramification/fixed_interval.js` | Exact fixed-decimal BigInt interval kernel |
| `smale6-ramification/fold_interval_certificate.js` | Krawczyk existence, uniqueness, and contraction certificate |
| `smale6-ramification/fold_invariants_certificate.js` | Rank, quadratic obstruction, and mass-transversality intervals |
| `smale6-ramification/full_planar_certificate.js` | Primary symmetry-breaking odd-block certificate |
| `smale6-ramification/fold_full_planar_certificate.js` | Independently organized odd-block cross-check |
| `smale6-ramification/fold_hessian_crosscheck.js` | Independent Taylor-jet check of the second directional derivative |
| `smale6-ramification/certificate_self_test.js` | Compact exact regression; passes at 70, 90, and 130 decimal digits |
| `smale6-ramification/census.js` | Pilot singular-route continuation with exact mass-derivative series; candidate generator, not a complete component census |
| `smale6-ramification/census_corank2.js` | Kernel-circle quadratic/cubic sampler at the square negative control |
| `smale6-ramification/CENSUS.md` | Audited pilot results, limitations, literature status, and decision register |

The literature snapshot used in the second phase is cached under
`smale6-ramification/literature/`.  In particular,
`mz2601/difficult-masses.tex` records that the enumeration program would fail
to establish finiteness at the Chen--Hsiao degeneracy, while the original
Chen--Hsiao paper and Roberts source are retained alongside the experiments.

## 15. Literature anchors for the working snapshot

- M. Hampton and R. Moeckel, *Finiteness of relative equilibria of the
  four-body problem*, Inventiones Mathematicae 163, 289--312.
- A. Albouy and V. Kaloshin, *Finiteness of central configurations of five
  bodies in the plane*, Annals of Mathematics 176 (2012), 535--588.
- A. Albouy and A. Chenciner, *Le problème des n corps et les distances
  mutuelles*, Inventiones Mathematicae 131 (1998), 151--184,
  [DOI 10.1007/s002220050200](https://doi.org/10.1007/s002220050200).
- G. E. Roberts, *A Continuum of Relative Equilibria in the 5-Body Problem*,
  Physica D 127 (1999), 141--145, DOI
  `10.1016/S0167-2789(98)00315-7`; source cached as `roberts98.tex`.
- K.-C. Chen and J.-S. Hsiao, *Convex central configurations of the n-body
  problem which are not strictly convex*, Journal of Dynamics and
  Differential Equations 24 (2012), 119--128, DOI
  `10.1007/s10884-011-9233-2`.
- Y. Liu and S. Zhang, *A characterization of a special planar 5-body central
  configuration with a trapezoidal convex hull*, Journal of Geometry and
  Physics 213 (2025), 105494; arXiv:2305.01376.
- M. Moczurad and P. Zgliczyński, *Central Configurations with Unequal
  Masses: Finiteness in Several Exceptional Cases of Five Bodies*,
  arXiv:2601.01165 (2026); source cached under
  `smale6-ramification/literature/mz2601/`.
- K. R. Meyer and D. S. Schmidt, *Bifurcations of relative equilibria in
  the 4- and 5-body problem*, Ergodic Theory and Dynamical Systems 8 (1988),
  215--225, [DOI 10.1017/S0143385700009433](https://doi.org/10.1017/S0143385700009433).
- J. Hachmeister, J. Little, J. McGhee, J. Pelayo, and A. Sasarita,
  *Continua of central configurations with a negative mass in the n-body
  problem*, Celestial Mechanics and Dynamical Astronomy 115 (2013),
  427--438, [DOI 10.1007/s10569-013-9471-1](https://doi.org/10.1007/s10569-013-9471-1).
- X. Yu and S. Zhu, *Finiteness of stationary configurations of the planar
  five-vortex problem*, [arXiv:2103.11975](https://arxiv.org/abs/2103.11975).
- T. Zhou and Z. Xia, *On the Degeneracy of the Central Configuration
  Formed by a Regular n-Gon with a Central Mass*,
  [arXiv:2604.04610](https://arxiv.org/abs/2604.04610) (2026).

These references anchor the status claims used to choose targets.  They do
not establish a priority claim for the new project deductions listed in
Section 10.

## 16. Addendum (2026-07-22): the census pilot was executed and audited

The first-priority track of Section 12 has now had a successful **pilot**;
audited results and scope limits are in smale6-ramification/CENSUS.md.  One
pseudo-arclength route seeded at the Chen--Hsiao fold detected two corank-one
points whose quadratic obstruction vanishes but whose cubic obstruction is
nonzero (36.8 and 0.111), plus the corank-two square with a central body at

\[
\mu=1,\qquad \nu_*=(13+11\sqrt2)/12.
\]

At the square, \(D_4\) symmetry forces the quadratic obstruction to vanish
and the reconstructed cubic remains numerically separated from zero.  This
is exactly the structural mechanism the pilot was intended to detect.
However, it is a classical negative control: Meyer--Schmidt (1988) already
gave the exact critical mass, nullity-two Lyapunov--Schmidt reduction, cubic
normal form, local fixed-mass isolation, and all nearby kite and trapezoid
branches.

The pilot did **not** complete a discriminant-component census.  Its event
logic detects only sampled sign changes of \(Q\); tangential or paired
sub-step zeros can be missed.  At corank two, the augmented normalized-kernel
system has an \(S^1\) fiber and one continuation path cannot enumerate every
attached physical branch.  The large-mass end stops at the step budget, and
the mass-origin region becomes ill-conditioned rather than being resolved.
Thus the supported conclusion is only: three exceptional events were
detected on one numerical route, all rejected as fixed-mass continuum germs,
and no counterexample was observed on that route.

## 17. Decision after the audit

### Accepted

- The augmented equations, gauge, exact Taylor differentiation, and
  Chen--Hsiao calibration are internally sound and reproducible.
- The two corank-one quadratic-zero events are valid discovery candidates
  and are numerically rejected at cubic order as fixed-mass tangents.
- The square is a strong end-to-end control: the code independently
  rediscovers the symmetry-forced quadratic vanishing and known cubic
  rejection.
- The broader meta-direction remains promising: search the discriminant
  together with integrability obstructions instead of selecting only
  attractive geometric ansätze.

### Rejected or downgraded

- “Exactly three non-fold points,” “the whole component was traced,” and
  “the component was cleared” are not supported.
- The two corank-one points should be called quadratic-zero or cusp-like
  until the unfolding-rank conditions for an ordinary cusp are checked.
- The square calculation has no novelty claim beyond its value as an
  independent computational control.
- The near-origin region is open; the observed return is not an independent
  replication and may reflect branch switching in the augmented system.
- A global singular solve is premature if it reuses the current event
  detector unchanged.

### Required repair before global expansion

1. Replace sign-change-only detection by adaptive searches for extrema and
   near-zeros of \(Q\), with stepwise error or interval bounds.
2. Replace normal-equations eigenanalysis by a robust SVD or rank-revealing
   QR near small singular values.
3. Deflate or branch-switch explicitly at corank-two points instead of
   following one arbitrary point on the kernel circle.
4. Resolve the small-mass boundary in a rescaled blow-up chart.
5. Only then perform a global solve for other discriminant components.

This is not a blind alley: the pilot validated the candidate-generating
idea and exposed exactly which numerical shortcuts prevent it from becoming
a census.  The next work item is therefore **repair and branch completion**,
not certification of the classical square and not an immediate black-box
global solve.

## 18. Addendum (2026-07-22): audit of the proposed Jacobian-to-Smale transfer

The six-part transfer map proposed after the census contained one useful
operational correction, two rediscoveries, one exact new exclusion, and one
sound but prematurely ordered computational direction.  The distinctions
matter because the program was created precisely to avoid turning an
appealing analogy into another bespoke blind alley.

### 18.1 What is and is not known about Fable's discovery process

The public technical discussions give compact verification and later
geometric explanations of the Jacobian counterexample.  In particular, Will
Sawin's construction geometrizes the map using a marked linear factor of a
cubic and Terry Tao explicitly describes the geometry as retroactive.  They
do not supply Fable's complete prompt, candidate log, or internal search
trace.  Therefore the claim that the system *demonstrably* performed a
particular mechanism-constrained haystack search is not evidence-backed.

The transferable lesson must be taken from the artifact, not from an
imagined transcript: search in a representation where exact identities or
factorizations are cheap to recognize, retain exact verifiability, and use
computation to cover a mechanism-defined class.  The
[technical dissection](https://sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/)
and [Tao's digestion](https://terrytao.wordpress.com/2026/07/21/a-digestion-of-the-jacobian-conjecture-counterexample/)
support the structural and retroactive-geometrization statements, not a
specific account of the hidden search process.

### 18.2 Finite symmetry: retain the filter, reject the theorem as stated

At the square-plus-center point, \(D_4\) symmetry really does forbid the
quadratic reduced map, and the computed cubic rejects the candidate.  The
correct general rule is narrower than "a finite symmetry can never force a
continuum."  On the kernel \(K\) of a variational fixed-mass reduction, a
finite isotropy group always allows the equivariant gradient cubic

\[
u\longmapsto \lVert u\rVert^2u
=\nabla\left(\frac14\lVert u\rVert^4\right),
\]

which has an isolated real zero.  Thus finite isotropy alone cannot force the
entire reduced germ to vanish to all orders.  But an allowed term need not
have a nonzero coefficient in the actual \(N\)-body equations, and occurrence
of an irrep in a symmetric power says nothing by itself about the zero set.
Outside the self-adjoint gradient setting, finite symmetry can even force
positive-dimensional zeros for particular source and target
representations.  The decision rule is consequently:

> Use finite isotropy to predict forbidden low-order jets.  Compute the first
> allowed jet; do not assume it is present.  If it vanishes or has projective
> zeros, look for an identity, factorization, syzygy, continuous symmetry, or
> special coefficient relation.

This corrects the justification while preserving the useful operational
message.

### 18.3 Roberts was already geometrized

For the rhombus with central mass \(M\), Roberts's own inertia-normalized
potential is

\[
U=4+2\left(M+\frac14\right)\left(\frac1a+\frac1b\right),
\qquad a^2+b^2=1,
\]

and the reduced equation factors as

\[
\left(M+\frac14\right)(a^{-3}-b^{-3})=0.
\]

The incidence variety is the union of the vertical signed component
\(M=-1/4\) and the square section \(a=b\).  Hachmeister et al. subsequently
gave the invariant neutral-configuration and orthogonal-doubling
generalization.  The program's positive-cluster virial identity blocks a
finite all-positive neutral seed.  Recasting the same facts as a vertical
mass-projection component and as cancellation between square-root classes is
useful packaging, but the underlying mechanism is prior art rather than a
new high-ceiling direction.

### 18.4 Exponent deformation does not transfer toward positivity

Roberts already states that the family persists for the homogeneous
potentials

\[
U_d=\sum_{i<j}\frac{m_im_j}{r_{ij}^d},\qquad d>0,
\]

and in the logarithmic point-vortex limit, with central mass

\[
M(d)=-2^{-d-1}.
\]

It therefore moves from \(M(0)=-1/2\) in the logarithmic case to
\(M(1)=-1/4\) in the Newtonian case without ever entering the positive
orthant.  If the vortex mass/circulation tuple is held fixed instead, the
non-square continuum disappears immediately away from its matching exponent.
Varying the exponent and the mass together is a signed regression test, not
a fixed-positive-mass transfer.  Moreover, a variable real exponent replaces
polynomial equations by exponential/logarithmic dependence, so the present
witness-set/Gröbner machinery does not carry over unchanged.  This track is
archived unless an independently found fixed-positive-mass continuum at a
different exponent supplies a new starting point.

### 18.5 The conic proposal is now an exact no-go

The proposed conic ansatz did not merely fail numerically.  Proposition 1A
of `smale6-repair/RESULT.md` proves:

> For fixed positive masses and fixed inertia, a collision-free central-
> configuration arc whose full labelled squared-distance image lies in a
> projective line or conic is constant in shape.

The proof combines constancy of \(U\), separation of square-root classes in a
multiquadratic function field, positivity, and pole cancellation.  It is a
new exact result of this program.  A targeted search of the primary
mutual-distance, finiteness, and signed-continuum literature found no
equivalent theorem, but unpublished folklore remains possible and no
priority claim is made.  The closest antecedents supply separate ingredients:
Albouy--Kaloshin use constancy of \(U\) on continua, while Albouy--Chenciner
develop the mutual-distance algebraic framework.  The new combination is the
degree-two normalization, square-class separation, positivity, and pole
cancellation.  It also reveals why Roberts works: its affine
distance line uses negative coefficients to cancel the nonconstant
square-root classes.

A structurally admissible exact successor begins only after this degree-two
barrier.  One possible parked design parametrizes distances by binary
quadratics,

\[
r_e=\frac{p_e}{p_0},\qquad s_e=\frac{p_e^2}{p_0^2},
\]

so the squared-distance image has projective degree at most four and inverse
cubes remain rational.  It would have to impose fixed inertia, constant
potential, planar Euclidean-distance-matrix rank, the full
Albouy--Chenciner equations, collision/nonconstant saturations, and finally
real positivity.  This is a legitimate mechanism-defined class, but not an
obviously cheap Gröbner calculation and not the immediate priority.

### 18.6 Correct order of work

The global numerical-algebraic decomposition remains the right mechanical
expansion, but only after the repairs in Section 17.  The current normalized-
kernel augmented system contains an \(S^1\) fiber at corank two, sign-change
event detection misses tangential zeros, and the small-mass chart is
unresolved.  A witness-set or monodromy calculation must additionally use a
determinantal/deflated critical-locus formulation, saturate collision and
denominator components, cover gauge charts, and filter for real positive
solutions.  Numerical component discovery is not itself an exact finiteness
or continuum proof.

The revised priority order is therefore:

1. preserve Proposition 1A and the Roberts factorization as exact project
   results, while retaining the explicit no-priority caveat;
2. repair tangential-event detection, rank computation, corank-two branch
   handling, and the small-mass boundary chart;
3. then decompose the global singular locus for
   \((1,1,\mu,\mu,\nu)\) and apply the jet sieve component by component;
4. retain the degree-four rational-distance ansatz as a bounded parallel
   experiment only after its much larger symbolic system is scoped;
5. move to \(n=6\) only after the \(n=5\) engine is reusable.

The \(n=5\)-to-\(n=6\) dimension analogy remains a sensible workflow heuristic,
not evidence that either dimension contains a counterexample.

## 19. Final closure: square-lift theorem and stopping gate

The terminal experiment was changed from global decomposition of the
\((1,1,\mu,\mu,\nu)\) singular locus to consolidation of the exact
square-lift obstruction discovered while strengthening the conic no-go. The
result, proof review, fixed prior-art audit, and binary decision are archived
in smale6-theory/.

The endpoint theorem says that any infinite fixed-positive-mass fiber
contains an algebraic full squared-distance curve whose normalization
factors through coordinatewise squaring and whose projective degree is at
least four. The internal theorem gate passed after one hostile review and
one revision. This is an internally checked candidate structural theorem,
not a peer-reviewed result or a priority claim.

The gate cancels the repair census, global singular-locus decomposition,
quartic ansatz search, and automatic move to \(n=6\) under this program.
Independent proof verification or an expert bibliographic review belongs to
a separately authorized submission-preparation effort. The controlling
record is smale6-theory/GATE_DECISION.md.
