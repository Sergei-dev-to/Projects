# Candidate Result Audit

## Purpose

Make the possible result falsifiable.

The candidate claim is:

```text
A finite non-gravitational repeated-interaction quantum evaporator can
reproduce the black-hole evaporation phenomenology package when it has:

1. area-like constrained entropy,
2. boundary-tension energy,
3. finite bath-density emission,
4. reversible shrinkage bookkeeping,
5. sufficiently scrambling internal dynamics.
```

This note asks which parts are genuinely derived, which are architecture
choices, and which remain assumptions.

## Current Proposition

For droplet sectors

```text
dim B_L = q^(L^2),
M_L = 4 sigma L,
```

with microcanonical emission into a 2D bath and a reversible shrinkage rule,
the model gives:

```text
S ~ M^2;
T ~ 1/M;
C < 0;
P ~ M^-2;
tau ~ M0^3;
shrinking internal Hilbert space;
Page-like radiation entropy under scrambling/typicality;
early/late radiation correlations near the Page crossing;
fast-scrambling proxy from sparse interacting expander dynamics.
```

## Audit Table

```text
Feature                         How obtained                         Status
--------------------------------------------------------------------------------
finite Hilbert space             finite q-state constrained sectors    derived
S ~ M^2                          dim B_L=q^(L^2), M_L~L               derived
T ~ 1/M                          T=(dS/dM)^-1                         derived
C < 0                            dM/dT < 0                            derived
small-quanta emission            microcanonical weights + bath DOS     stronger P
P ~ M^-2                         boundary*T^3 in 2D bath              derived if bath choice accepted
tau ~ M0^3                       integrate dM/dt ~ -M^-2              derived if P law accepted
shrinking capacity               B_L ~= B_(L-1) tensor Shell_L        derived kinematics
shrink trigger                   emitted-energy threshold              architecture choice
multi-shell shrinkage             internal reversible accumulator       stronger P
unitarity/purifiability           global state-vector isometry          stronger P+
finite bath-density weights       explicit 2D-box bath spectrum         stronger P
explicit hard radiation           hard-bin quantum registers             small-size / P+
global hard thermality            hard density from global lift          supported / P+
Page-like entropy                Page theorem + circuit diagnostics     conditional / P+
early/late correlations           Page crossing + old/new MI tests      conditional / P+
global reference flow             ref-shell diagnostic                  tiny test / P+
hard/soft entropy accounting      soft Page vs hard observer entropy     supported / P+
integrated state-vector test      hard+soft+bath in one pure state       tiny test / P+
threshold state-vector test       accumulator-triggered shrinkage        record diagnostic / P+
threshold density scaling         full density + controls + scaling      supported / P+
final Floquet candidate           weighted hard + threshold controls     small-size / Y-
fast scrambling                  expander interacting-spin tests        numerical / P+
one global register rule         bath+emission+shrink Floquet lift      supported / P+
one autonomous H_total            not yet                              missing
```

## What Is Strong

The thermodynamic core is strong:

```text
S ~ M^2,
T ~ 1/M,
C < 0
```

are not tuned after the fact. They follow immediately from:

```text
area state count;
boundary energy.
```

The acceleration law is also strong, once the exterior bath dimension is fixed:

```text
P ~ boundary * T^(d+1).
```

For `d=2`:

```text
P ~ L * (1/L)^3 ~ L^-2 ~ M^-2.
```

This is the cleanest part of the result.

## What Is Medium-Strong

The finite bath-density emission is better than assigning bin probabilities by
hand:

```text
equal microscopic coupling;
bin weights from bath degeneracies.
```

But the bath spectrum / degeneracy table is still chosen to approximate the
target density. So this is:

```text
less imposed than fitted couplings;
not yet derived from an explicit bath Hamiltonian.
```

Update:

```text
The bath-density module has now been upgraded. A concrete one-particle 2D-box
bath spectrum supplies rho_bath(omega), and the core supplies the
microcanonical exp[Delta S] factor. This reproduces the golden-rule bin
weights with L1 error around 0.03 for L=8,...,64 and preserves the
P ~ M^-2 slope.
```

The reversible shrinkage automaton is also real:

```text
the coarse capacity update need not violate unitarity.
```

But it does not yet answer:

```text
why this threshold rule is dynamically selected.
```

## What Is Conditional

The Page and early/late results depend on typicality/scrambling.

Analytically:

```text
dim B_L = q^(L^2),
dim R_L = q^(L0^2 - L^2)
```

gives the Page crossing:

```text
L ~= L0 / sqrt(2).
```

Numerically:

```text
stabilizer and expander diagnostics reproduce Page-like behavior;
interacting spin dynamics gives positive small-size evidence;
OTOC and entanglement-growth tests distinguish expander from local grid.
```

But the large-system claim remains conditional:

```text
if the internal dynamics is sufficiently scrambling, then Page behavior follows.
```

That is acceptable for a control model, but not yet a theorem about the
specified Hamiltonian.

The explicit hard-register diagnostic adds one important improvement:

```text
hard radiation is no longer only a statistical emission log.
```

At `L0=4, d_hard=2`, the emitted hard register is part of the pure state. With
scrambling, the latest hard reduced state is close to the finite-bath target
distribution; without scrambling, both Page behavior and hard-local thermality
fail.

## What Is Still Put In By Hand

The remaining imposed ingredients are:

```text
1. exterior bath dimension d=2;
2. boundary-tension mass law M_L = 4 sigma L;
3. emitted-energy threshold for shell shrinkage;
4. finite bath degeneracy table;
5. modular ordering U_bookkeep U_emit U_edge U_scramble;
6. sufficiently scrambling interacting dynamics.
```

These are not equally bad.

Good architecture choices:

```text
d=2:
  a clear control knob. It makes the bath-dimension dependence explicit.

M_L~boundary:
  physically ordinary for a line-tension droplet, not an arbitrary exponent.

scrambling:
  a standard black-hole phenomenology requirement, and tested by controls.
```

More vulnerable choices:

```text
threshold shrinkage:
  still a designed coarse rule, but now implemented as an internal reversible
  multi-shell accumulator rule.

bath degeneracy table:
  needs a microscopic bath Hamiltonian if we want a stronger result.

modular cycle:
  makes the architecture transparent, but prevents a strong autonomy claim.
```

## Falsification Tests

The claim would weaken sharply if:

```text
1. finite bath-density emission fails for larger L or smoother bins;
2. Page diagnostics fail under deterministic interacting dynamics;
3. local/removal controls show Page behavior is an artifact of register
   bookkeeping;
4. the shrinkage threshold cannot be embedded in a coherent repeated-
   interaction rule without hidden archives;
5. replacing the assigned bath density with an explicit bath Hamiltonian ruins
   P ~ M^-2;
6. the 2D bath choice turns out to be the only reason the model resembles a
   black hole, with no defensible interpretation.
```

## Victory Standard

A modest victory:

```text
Show a coherent finite repeated-interaction system where the thermodynamic
package is analytic and the information-flow package is supported by explicit
finite-size quantum diagnostics.
```

Current status:

```text
achieved at small size by the audited repeated-interaction simulator.
```

A strong victory:

```text
Show one clean Floquet rule, or one finite Hamiltonian plus repeated bath
ancillas, where scrambling, emission, and shrinkage all occur in the same
simulation and reproduce the F-list.
```

Current status:

```text
not yet.
```

A very strong victory:

```text
Show one autonomous time-independent Hamiltonian whose ordinary dynamics
produces the evaporation trajectory, Page curve, and fast-scrambling
diagnostics.
```

Current status:

```text
out of reach for now.
```

## Recommended Next Step

The next best target is not another broad literature review.

It is:

```text
strengthen the autonomy gap without demanding a perfect H_total.
```

Concrete next test:

```text
write the final integrated architecture/claim note:

1. state the strongest current result in one place;
2. classify every component as derived, finite diagnostic, or assumption;
3. list the remaining non-derived pieces;
4. decide whether the current package is enough for the intended conceptual
   result.
```

Goal:

```text
avoid drifting into endless module polishing after the main F-list has been
substantially covered.
```

Current supporting note:

```text
notes/audited_repeated_interaction_results.md
notes/explicit_hard_register_results.md
notes/explicit_bath_hamiltonian_results.md
notes/multishell_shrinkage_floquet_results.md
```

Completed control:

```text
The audited simulator now compares Margulis, grid, and no-scrambling variants.
No scrambling fails badly; grid and Margulis both work at L0=4, so the current
small Page diagnostic proves the need for entangling dynamics but does not
separate local from expander scrambling.
```

Completed explicit-radiation upgrade:

```text
The hard-bin register is now part of the explicit quantum state in a small
L0=4 diagnostic. Scrambled runs give hard-local thermality and old/new MI;
no-scrambling fails both.
```

Completed bath-Hamiltonian upgrade:

```text
A one-particle 2D-box bath spectrum now generates the bath density of states
used in the emission law. It preserves P ~ M^-2 and does not break the
explicit-hard-register diagnostic.
```

Completed multi-shell shrinkage upgrade:

```text
The threshold shrinkage rule has been implemented as a repeated internal
accumulator update over nested shell labels. Exhaustive enumeration gives an
injective map over 165888 finite-register inputs, including sequences with
zero, one, or two shell shrinks.
```

Completed global-register Floquet upgrade:

```text
A single finite-register rule now combines bath microstate input, hard-bin
emission, emitted-energy accumulation, and conditional shell shrinkage.
Exhaustive enumeration over 1048576 inputs is injective when the bath
microstate and shrink record are retained. Erasing either record destroys
injectivity. This strengthens the repeated-update/autonomy claim, but it is
still a register-level Floquet rule rather than one autonomous Hamiltonian.
```

Completed state-vector lift:

```text
The global register rule has been lifted to an explicit state-vector isometry.
A random complex state over the 1048576-dimensional input basis maps to the
output basis with zero norm error and inverse fidelity 0.9999999999999989.
This shows the combined rule can carry amplitudes coherently, not only
classical labels.
```

Completed global hard-density check:

```text
The visible hard record in the global lifted rule has an explicit reduced
density matrix after tracing hidden bath/shrink records. For a three-emission
hard record, S_hard = 2.079437 versus ln(8) = 2.079442, with trace distance
1.137e-03 to the uniform coarse bath target. This supports hard-local
thermality inside the global rule, but not Page/old-new information flow.
```

Completed global reference-flow check:

```text
A tiny L0=2 diagnostic entangles a reference with the shell label and runs the
global rule. Hard radiation carries no reference information,
I(ref:hard)=0, while the soft/shrink record carries the expelled-shell
information when shrinkage occurs, I(ref:soft)=3.639023. The no-shrink branch
leaves the remaining reference information in the core, I(ref:core)=0.519860.
This supports the hard-local/soft-purifying split inside the global rule, but
is not yet a many-cycle Page calculation.
```

Completed hard/soft entropy accounting:

```text
The Page diagnostic has been placed next to the hard-local thermal entropy.
In L0=8 stabilizer shell runs, the soft fine-grained radiation entropy follows
the Page capacity and returns to zero, while the accumulated hard-bin observer
entropy is monotone. For grid and expander8, all five seeds have zero soft
Page deficit; the first old/new soft MI appears at 6->5. This prevents a
misreading: hard thermal entropy is not the Page entropy.
```

Completed integrated state-vector check:

```text
A small L0=3 state-vector simulation now contains core scrambling, soft shell
records, visible hard bins, and hidden bath purifiers in one pure state.
Scrambled margulis/grid runs have soft Page deficits around 0.29-0.34 and
old/new soft MI at 2->1; no-scrambling has deficit 3.466 and no old/new MI.
The hard bins remain exactly locally thermal in all cases. This joins the
hard/soft/bath accounting in one state, but still omits the microscopic
emitted-energy accumulator and threshold-triggered shrinkage.
```

Completed threshold integrated state-vector check:

```text
A sparse L0=3 branch-state diagnostic now includes eight microscopic hard
emissions, an emitted-energy accumulator, and threshold-triggered shell
transfer. The final state has 131072 branch terms, mean transferred shell count
2.63671875, and complete evaporation probability 0.63671875. Scrambled
margulis/grid runs have soft-record entropy around 6.1-6.3, while
no-scrambling gives around 3.3-3.6. This addresses the external-shrink-schedule
weakness, though it uses record entropies rather than full reduced-density
entropies.
```

Completed threshold density scaling:

```text
The thresholded model has now been run with full reduced-density entropies,
scrambling controls, and an emission-count sweep. For L0=3 and 4,5,6
microscopic emissions, hard entropy exactly follows n ln 2 to numerical
precision, while scrambled soft entropy remains much larger than the
no-scrambling control. The largest case has 32768 branch terms. This shows
threshold shrinkage and full density-matrix diagnostics can coexist at small
size.
```

Completed final Floquet candidate scan:

```text
The current best single diagnostic uses threshold=5, six microscopic emissions,
and nonuniform hard weight P(energy 2)=0.35. It gives exact hard entropy
relative to the target hard distribution, nontrivial threshold shell transfer,
and a large scrambled-vs-none soft entropy gap: S_soft=2.636/2.647 for
margulis/grid versus 0.362 for no scrambling. This is the best current support
for marking the non-gravitational Floquet-control version as close to all-Y.
```
