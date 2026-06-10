# Integrated Result Claim

## Purpose

State the strongest current result without turning it into a stronger claim
than the work supports.

The project goal was:

```text
Find a finite non-gravitational quantum system that reproduces as much of the
black-hole evaporation phenomenology package as possible.
```

The current candidate is:

```text
Edge-Tension Expander Evaporator
```

## One-Sentence Claim

A finite non-gravitational repeated-interaction evaporator with area-like
constrained entropy, boundary-tension energy, an explicit 2D bath spectrum,
explicit hard/soft radiation registers, reversible multi-shell shrinkage, and
scrambling internal dynamics reproduces the main Schwarzschild evaporation
phenomenology at the thermodynamic and finite-diagnostic level.

## What Is Actually New, If Anything

Not new:

```text
Page curves without gravity;
unitary qubit evaporation;
hard/soft radiation bookkeeping;
microcanonical exp(Delta S) emission;
fast scrambling as a black-hole diagnostic;
collision/repeated-interaction models.
```

Potentially new:

```text
the integrated non-gravitational control model:

area state count
+ boundary energy
+ negative heat capacity
+ M^-2 evaporation power
+ explicit bath-density emission
+ explicit hard+soft radiation
+ Page/old-new diagnostics
+ reversible shrinkage
+ scrambling dependence.
```

The contribution is an architecture and diagnostic package, not a new
fundamental mechanism.

## Model Skeleton

Droplet sectors:

```text
dim B_L = q^(L^2)
S_L = L^2 log q
M_L = 4 sigma L
```

Temperature:

```text
T_L = (dS/dM)^(-1)
    = 2 sigma / (L log q)
    ~ 1/M.
```

Heat capacity:

```text
C = dM/dT < 0.
```

Emission law:

```text
Gamma_L(omega)
  ~ rho_bath(omega) exp[S(M_L - omega) - S(M_L)].
```

For a 2D exterior bath:

```text
P ~ boundary * T^3
  ~ L * L^-3
  ~ L^-2
  ~ M^-2.
```

Lifetime:

```text
tau ~ M0^3.
```

Shrinkage:

```text
B_L ~= B_(L-1) tensor Shell_L,
dim Shell_L = q^(2L - 1).
```

Page crossing:

```text
dim B_L ~= dim R_L
L ~= L0 / sqrt(2).
```

## Evidence Table

```text
Feature                         Status                         Evidence
--------------------------------------------------------------------------------
finite Hilbert space             derived                        finite q sectors
S ~ M^2                          derived                        S~L^2, M~L
T ~ 1/M                          derived                        microcanonical slope
C < 0                            derived                        dM/dT < 0
P ~ M^-2                         derived with d=2 bath           boundary*T^3
tau ~ M0^3                       derived with P law              continuum integral
small-quanta emission            supported                       golden-rule tracker
explicit bath density            supported                       2D-box spectrum
hard radiation quantum register  supported at small size         explicit hard axes
hard-local thermality            supported at small size         D_hard ~ 1e-2
global hard-density check         supported                       trace distance ~1e-3
Page-like entropy                conditional + diagnostic        Page theorem + circuits
old/new correlations             conditional + diagnostic        MI turns on near Page
global reference flow             supported in tiny test           hard 0, soft nonzero
hard/soft entropy accounting      supported                       Page soft, hard monotone
integrated state-vector test      supported at L0=3               hard+soft+bath in one state
threshold state-vector test       supported as record diagnostic   micro emissions trigger shrink
threshold density scaling         supported to 32768 branches       controls + 4/5/6 emissions
final Floquet candidate scan      supported at L0=3                 weighted hard channel
scrambling dependence            supported at small size         no-scrambling fails
fast/expander advantage          partial                         OTOC/entropy growth only
multi-shell shrinkage            supported as finite map         injective enumeration
global register Floquet rule      supported                       state-vector lift
one autonomous Hamiltonian        missing                         not derived
```

## Strongest Individual Results

### Thermodynamic Core

This is the cleanest result.

```text
area entropy + boundary energy
```

directly gives:

```text
S ~ M^2,
T ~ 1/M,
C < 0.
```

This is not fitted.

### Evaporation Scaling

With a 2D bath:

```text
P ~ M^-2,
tau ~ M0^3.
```

The explicit `box2d` bath-Hamiltonian diagnostic gives:

```text
L1 bin-weight error ~ 0.03,
P/target ~ 0.92,
logP/logM slope ~ -2.04.
```

So the bath density can come from a finite spectrum, not only from an assigned
degeneracy table.

### Explicit Hard Radiation

The emitted hard bin is now an explicit quantum register.

For `L0=4`, `d_hard=2`, scrambled runs give:

```text
latest hard trace distance ~ 1e-2,
hard entropy error ~ 1e-3,
old/new MI turn-on at 3->2.
```

No-scrambling fails:

```text
large Page deficit,
large hard trace distance,
no old/new MI.
```

### Reversible Multi-Shell Shrinkage

The multi-shell accumulator map is injective:

```text
inputs         = 165888
unique outputs = 165888
injective      = True
max shrinks    = 2 in a length-4 sequence
```

This means repeated threshold shrinkage can be represented as a reversible
finite-register update.

It is still designed, but it is not an irreversible collapse.

### Global Register Floquet Rule

The bath microstate, hard-bin emission, emitted-energy accumulator, and
conditional shrinkage update can be combined into one repeated finite-register
rule.

The current exhaustive check gives:

```text
inputs              = 1048576
full map injective  = True
```

The control erasures fail:

```text
erase bath microstate -> not injective
erase shrink record   -> not injective
```

This is useful because it identifies which records a unitary dilation must
retain. The expelled shell data is not optional; it must be carried by a soft,
shrink, or radiation record.

The same rule now has an explicit state-vector lift. A random complex state on
the 1048576-dimensional input basis maps coherently to the output basis with:

```text
norm error       = 0.0
inverse fidelity = 0.9999999999999989
```

So the current F15 evidence is not only classical injectivity; it is a finite
isometry diagnostic.

The visible hard record in this global state-vector rule also has a direct
reduced-density diagnostic:

```text
hard dimension           = 8
hard entropy             = 2.079437
target entropy           = ln(8) = 2.079442
trace distance to target = 1.137e-03
```

This supports hard-local thermality inside the global rule, while still not
testing Page behavior or early/late correlations.

The same global rule now has a minimal reference-flow diagnostic. For a tiny
`L0=2` test with a reference entangled with the emitted shell label:

```text
shrink probability           = 0.875
I(ref : hard)                = 0.000000
I(ref : soft)                = 3.639023
I(ref : hard+soft radiation) = 3.639023
I(ref : core)                = 0.519860
```

This checks the intended information split: the hard record is locally thermal
and uninformative about the shell label, while the soft/shrink record carries
the expelled shell information.

A hard/soft accounting diagnostic now puts this next to the Page curve. In an
`L0=8` stabilizer shell run with three coarse hard emissions per shell:

```text
soft Page deficit        = 0 for grid and expander8 in 5/5 seeds
peak soft entropy        = 28 qubits
final soft entropy       = 0
first old/new soft MI    = 6->5
final hard coarse entropy = 16.635532
```

This makes the entropy distinction explicit:

```text
soft fine-grained entropy:
  Page-like and returns to zero.

hard coarse observer entropy:
  locally thermal and monotone.
```

Finally, a small integrated state-vector diagnostic now puts this accounting in
one pure state. For `L0=3`, the state contains scrambling core qubits, soft
shell records, visible hard bins, and hidden bath purifiers. Scrambled
`margulis/grid` runs have small soft Page deficits, old/new soft MI at `2->1`,
and hard bins thermal to numerical precision. The no-scrambling control keeps
hard bins thermal but fails the soft Page diagnostic:

```text
margulis soft Page deficit ~ 0.29-0.34
grid soft Page deficit     ~ 0.29-0.33
none soft Page deficit     ~ 3.466
final hard entropy         = 3 ln 2 = 2.079442
max latest hard trace distance ~ 10^-15
```

This is the first one-state check joining F8/F9/F15, though still at tiny size.

A thresholded sparse state-vector diagnostic now adds the missing accumulator
piece. Eight microscopic hard emissions with energies `1` or `2` update an
emitted-energy accumulator; whenever the accumulator reaches threshold `4`,
the next shell is transferred to a soft/shrink record. The final branch
statistics are:

```text
final basis terms                = 131072
mean transferred shells          = 2.63671875
P(complete evaporation)          = 0.63671875
S_hard                           = 8 ln 2 = 5.545177
```

Scrambled runs have much larger soft-record entropy than no-scrambling:

```text
margulis/grid S_soft ~ 6.1-6.3
none S_soft          ~ 3.3-3.6
```

This is a record-entropy diagnostic rather than a full reduced-density Page
calculation, but it shows that microscopic emissions can trigger shell
shrinkage inside the integrated branch structure.

The full reduced-density threshold version has now been run through a small
scaling sweep:

```text
L0 = 3
micro emissions = 4, 5, 6
scramblers = margulis, grid, none
seeds = 0, 1
max branch terms = 32768
```

Hard radiation remains exactly thermal:

```text
S_hard = n ln 2
hard entropy error ~ 10^-15
```

Scrambled soft entropy stays well above the no-scrambling control:

```text
emissions  scrambled S_soft   none S_soft
4          ~2.56-2.61        ~0.234
5          ~2.25-2.28        ~0.693
6          ~1.28-1.30        ~0.424
```

This gets through the full-density threshold test, scrambling controls, and
one emission-count scaling check in a single diagnostic.

The final Floquet candidate scan adds nonuniform hard weights and a small
trajectory search. The best readable case is:

```text
threshold = 5
micro emissions = 6
P(hard energy 2) = 0.35
```

It gives:

```text
mean transferred shells = 1.117
P(done)                 = 0
S_hard                  = S_hard,target = 3.885
S_soft(margulis/grid)   = 2.636, 2.647
S_soft(none)            = 0.362
scrambled-none gap      = 2.27-2.29
```

This is currently the cleanest single finite Floquet diagnostic of the mapped
evaporation package.

## What Is Still Designed

These are still model choices:

```text
1. choose a 2D exterior bath;
2. choose boundary-tension energy M_L = 4 sigma L;
3. choose the repeated-interaction ordering;
4. choose the accumulator threshold Delta M;
5. choose a scrambling Hamiltonian/Floquet module;
6. choose the hard/soft shell emission map.
```

Some are acceptable architecture:

```text
2D bath:
  explicit control knob; determines the power law.

boundary tension:
  ordinary non-gravitational energy law.

scrambling:
  standard black-hole phenomenology requirement, and tested by controls.
```

The most vulnerable remaining choices are:

```text
hard/soft emission map;
threshold shrinkage rule;
modular repeated-interaction ordering.
```

## What We Should Not Claim

Do not claim:

```text
we derived black-hole evaporation from a natural Hamiltonian;
we solved the information paradox;
we found a unique mechanism;
Page curves require our model;
fast scrambling has been proven asymptotically for the candidate Hamiltonian;
gravity is irrelevant to actual black holes.
```

Also do not claim:

```text
this reproduces islands or wormholes.
```

The model is useful precisely because it does not contain those mechanisms.

## What We Can Claim

Defensible:

```text
The usual black-hole evaporation phenomenology package is not uniquely
gravitational. A finite non-gravitational repeated-interaction quantum system
can reproduce the package at the level of thermodynamic scaling and explicit
small-system information diagnostics.
```

More precise:

```text
Area-like constrained entropy plus boundary-tension energy are sufficient to
produce S~M^2, T~1/M, and negative heat capacity. Coupling this system to a
2D bath with an explicit finite spectrum gives P~M^-2 and tau~M0^3. With
scrambling and reversible shrinkage, explicit hard+soft radiation registers
show Page-like entropy behavior and old/new correlations at small size.
```

## Why This Matters

The model separates two issues:

```text
generic finite quantum/statistical mechanics:
  Page behavior,
  global purification,
  local thermality,
  negative heat capacity from convex/area-vs-boundary state count,
  accelerated evaporation.

genuinely gravitational mechanisms:
  why horizons have the required state count,
  why the relevant bath is effectively what it is,
  how semiclassical Hawking emission is encoded,
  how islands/wormholes reproduce the purification channel,
  how locality/causality constrain the information flow.
```

So the conceptual message is:

```text
Much of the black-hole information-puzzle phenomenology is not diagnostic of
gravity by itself.
```

The remaining gravitational problem is not the Page curve as a curve. It is
the mechanism selecting and realizing the purification channel in a spacetime
with horizons.

## Current F-Status

```text
F1  finite explicit quantum system                 Y
F2  unitary or purifiable evaporation              P+
F3  shrinking internal state space                 P+
F4  S ~ M^2                                        Y
F5  T ~ 1/M / negative heat capacity               Y
F6  accelerating evaporation                       Y
F7  emission rates from dynamics/matrix elements   P+
F8  Page-like radiation entropy                    P+
F9  early/late radiation correlations              P+
F10 separates generic from gravitational           Y
F11 outgoing phase-space diagnostic                P
F12 mass-law controls                              P
F13 local-vs-scrambled removal controls            P
F14 fast scrambling                                P+
F15 autonomy / one update rule or Hamiltonian       P+
```

`P+` here means:

```text
substantial architecture plus diagnostics, but not a final derivation.
```

## Remaining Gaps Worth Working On

If continuing, the highest-value gaps are:

```text
1. less modular hard/soft emission map;
2. combine the state-vector lift with scrambling and explicit hard/soft
   density-matrix diagnostics;
3. larger scrambling diagnostics that separate grid from expander;
4. explicit hard registers with more spectral resolution;
5. asymptotic or analytic statement for the scrambling requirement.
```

The lowest-value next move would be:

```text
another tiny exact simulation that only rechecks the same Page crossing.
```

## Decision

This is now enough to count as a real candidate result, not just a vague
program.

It is not yet a finished paper-level theorem. But it is a coherent result:

```text
all major black-hole evaporation phenomenology except genuine gravitational
selection mechanisms has a finite non-gravitational control realization.
```

The next phase should be either:

```text
1. turn this into a concise manuscript/note with explicit caveats; or
2. attack one remaining strong gap, especially combining the state-vector
   global rule with scrambling and explicit hard/soft density matrices.
```

Update:

```text
The final Floquet-control checkpoint is now:

notes/final_floquet_toy_model_result.md
```

Under the Floquet toy-model standard, the central non-gravitational F-list is
now mostly `Y` or `Y-`. The remaining caveat is not coherence of the control
model, but naturalness and scale.
