# Model Search Strategy From The Desiderata

## Purpose

Use the reviewer-facing desiderata to decide what kind of model is worth
building next.

Reference standard:

```text
notes/reviewer_acceptable_model_desiderata.md
```

The model should generate as much as possible from one autonomous
non-gravitational Hamiltonian:

```text
H_total fixed;
core/radiation split diagnosed from the state;
area-like entropy from model structure;
emission from matrix elements;
thermodynamics and information flow measured.
```

## What We Know

### Area-sector / area-register models

Strength:

```text
they reproduce S ~ M^2, T ~ 1/M, negative heat capacity, and acceleration.
```

Weakness:

```text
the central entropy law is assigned.
```

Role:

```text
control model only.
```

This route is useful for learning what follows from `S(M)`, but it does not
meet the no-settling standard.

### Variable-N Bose-Hubbard

Strength:

```text
natural shrinking sectors;
physical particle-loss operators;
accelerating evaporation in several windows;
Kraus upgrade with growing core-radiation Renyi-2 entropy.
```

Weakness:

```text
the state count is Bose-Hubbard combinatorics, not area-like.
```

Role:

```text
natural-dynamics benchmark.
```

It tells us that natural shrinking and physical emission operators can work,
but it does not solve the entropy law.

### Connector modes

Strength:

```text
N active sites;
O(N^2) pairwise connector degrees;
M ~ N;
S ~ N^2 ~ M^2 at counting level.
```

Weakness:

```text
dynamics is not established;
site removal is too coarse if treated as one hard emission;
connector softness and flux scaling are open.
```

Role:

```text
best finite-Hilbert-space route to reducing the entropy-input objection.
```

### Matrix clump

Strength:

```text
emergent geometry/separation;
off-diagonal degrees scale like N^2;
eigenvalue escape gives a natural radiation split;
post-emission heating is physically motivated.
```

Weakness:

```text
hard to simulate quantum mechanically;
known successful versions are close to black-hole matrix theory;
finite Page diagnostics are difficult.
```

Role:

```text
best natural-dynamics route to evaporation and radiation emergence.
```

## Strongest Abstract Target

The strongest model class combines connector counting with matrix-clump
dynamics:

```text
relational clump with pairwise active modes.
```

The core object is an active bound cluster of constituents. Its entropy comes
from relations among constituents:

```text
active relations ~ N(N-1)/2.
```

Radiation is diagnosed when one constituent separates and its incident
relations stop participating in the active core.

The minimal abstract Hamiltonian should have:

```text
constituent variables;
pairwise connector/off-diagonal variables;
internal chaotic mixing;
escape/separation directions;
connector gaps or couplings that depend on separation.
```

In matrix language, this is ordinary matrix quantum mechanics:

```text
H = Tr(P^2)/2 + Tr([X_a, X_b]^2)/4 + possible stabilizing terms.
```

In finite connector language, it is an incidence-local model:

```text
H = H_sites + H_connectors + H_incidence + H_escape.
```

The connector version is easier to simulate. The matrix version is more
physically organic.

## The Main Design Constraint

The shell mistake must not be repeated.

A coarse event like

```text
N -> N-1
```

removes order `N` pairwise degrees. That is too large for one microscopic hard
emission.

Therefore the model must support two timescales:

```text
microscopic emissions:
  small energy, small entropy transfer, many events;

coarse separation:
  one constituent leaves after many microscopic changes.
```

The first decisive test is connector/off-diagonal softness:

```text
Do the active relational modes contain many low-energy transitions whose
typical scale decreases like 1/N?
```

If the answer is no, pairwise counting gives the entropy law but not
evaporation.

## Candidate Hamiltonian Families

### Candidate 1: Stripped matrix clump

Hamiltonian:

```text
H = 1/2 sum_a Tr(P_a^2)
  + g^2/4 sum_{a,b} Tr([X_a, X_b]^2)
  + optional weak confinement / stabilization.
```

Core/radiation diagnostic:

```text
core = compact eigenvalue clump;
radiation = separated eigenvalue plus decoupled off-diagonal modes.
```

First kill test:

```text
classical or semiclassical simulation;
check clump persistence, eigenvalue escape, post-escape heating.
```

Pass condition:

```text
after an eigenvalue escapes, the remaining clump has lower energy and higher
temperature proxy over many seeds/initial conditions.
```

Why it is worth testing:

```text
it directly targets emergent split, evaporation, and heating.
```

Main risk:

```text
the stripped model may fail without the full matrix-black-hole structure.
```

### Candidate 2: Finite relational connector clump

Degrees:

```text
N site qudits or rotors;
connector modes c_ij for i < j;
optional position/separation coordinate per site.
```

Hamiltonian skeleton:

```text
H_sites
+ H_connectors
+ H_incidence
+ H_escape.
```

Core/radiation diagnostic:

```text
core = largest active connected component;
radiation = detached sites plus connector modes no longer incident on the core.
```

First kill test:

```text
compute spectrum of connector/off-diagonal modes as a function of N;
measure whether low-energy transition scale goes like 1/N.
```

Second kill test:

```text
run autonomous dynamics and check whether many small connector emissions
precede coarse site separation.
```

Why it is worth testing:

```text
it is finite-dimensional and attacks S ~ M^2 by architecture.
```

Main risk:

```text
connector modes may be counted as entropy without producing the right energy
or emission dynamics.
```

### Candidate 3: Hybrid finite matrix/connector model

This is the practical synthesis:

```text
finite connector system inspired by matrix off-diagonal modes.
```

Degrees:

```text
site variables represent eigenvalue-like constituents;
connector variables represent off-diagonal modes;
connector energy/coupling depends on a separation-like variable.
```

Hamiltonian idea:

```text
H =
  sum_i p_i^2 / 2m
  + V_clump({x_i})
  + sum_{i<j} H_conn(c_ij; |x_i - x_j|)
  + H_mix.
```

Desired behavior:

```text
inside the clump:
  many active connector modes;

as one site separates:
  incident connector modes become heavy, frozen, or weakly coupled;

remaining clump:
  fewer active modes and higher temperature proxy.
```

Why this may be the best search target:

```text
it keeps the finite connector bookkeeping while borrowing the matrix-clump
mechanism for emergence and separation.
```

Main risk:

```text
the separation coordinate may become a particle model with extra connector
labels unless the coupling rule is simple and physically motivated.
```

## Model Search Gates

Any candidate must pass these gates before investing in Page diagnostics.

### Gate 1: Area-like active state count

Measure or derive:

```text
S_active(N) ~ N^2.
```

### Gate 2: Measured mass/energy scaling

Measure:

```text
M_active(N) ~ N
```

or another relation that gives the desired thermodynamics without direct
assignment.

### Gate 3: Soft microscopic emissions

Check:

```text
typical emitted energy ~ 1/N.
```

This should come from the spectrum or matrix elements, not from assigning
`epsilon_N = 1/N`.

### Gate 4: Post-emission heating

Check:

```text
E_core decreases;
T_core increases.
```

### Gate 5: Flux and acceleration

Measure:

```text
outgoing flux spectrum;
emitted power versus core size;
later power > earlier power.
```

### Gate 6: Information flow

Only after Gates 1-5:

```text
core-radiation entropy;
early/late radiation mutual information;
scrambling controls.
```

## Recommended Search Order

### Step 1: Matrix-clump classical kill test

Reason:

```text
fastest way to test natural evaporation/heating.
```

This does not solve the finite quantum information problem, but it tells us
whether the best natural dynamical mechanism survives stripping.

### Step 2: Connector softness test

Reason:

```text
fastest way to test whether pairwise entropy can support Hawking-scale
microscopic emissions.
```

If connector modes are not soft, the connector model is only a counting story.

### Step 3: Hybrid connector-clump Hamiltonian

Reason:

```text
combines the best surviving mechanism from Steps 1 and 2.
```

This is the first serious candidate for the reviewer desiderata.

## Decision Logic

```text
if matrix clump heats after escape:
    prioritize matrix-inspired hybrid;

if connector modes have 1/N softness:
    prioritize finite connector Hamiltonian;

if both work:
    build hybrid relational clump;

if matrix works but connector softness fails:
    stay closer to matrix dynamics;

if connector softness works but matrix clump fails:
    build finite connector evaporator;

if both fail:
    no-settling route needs a new idea.
```

## Current Best Bet

The strongest model to search for is:

```text
a relational clump Hamiltonian with pairwise active modes and dynamical
separation.
```

The immediate work should be kill tests, not another paper draft:

```text
1. stripped matrix clump: escape + heating;
2. connector modes: soft spectrum + emission scale.
```

## Gate-Test Update

The first gate tests have now been run:

```text
notes/no_settling_gate_test_results.md
notes/collective_connector_softness_results.md
notes/critical_connector_heating_results.md
notes/quadratic_connector_band_positioning.md
notes/quadratic_connector_candidate_scale_review.md
notes/quadratic_connector_evaporator_candidate.md
```

Outcome:

```text
stripped matrix clump:
  separation-like events occur in small cases, but robust post-event heating
  does not;

simple connector spectra:
  pairwise counting gives S ~ N^2, but natural incidence-local spectra do not
  produce omega ~ 1/N softness;

collective critical connector spectra:
  do produce omega ~ T ~ 1/N and can give P ~ N^-2 under local spectral-weight
  normalization;

post-emission heating:
  grid-like critical spectra fail;
  one-dimensional quadratic ring spectra mostly pass for larger N;
  one-dimensional linear ring spectra have good softness and power proxy but
  fail the heating robustness check;
  alpha=2 power-law spectra pass robustly but miss the earlier power proxy;
  alpha=1 power-law spectra have the cleanest power proxy but fragile heating.
```

So the naive matrix branch fails its first dynamical gate. The naive connector
branch fails, but the critical connector branch survives the spectral gate.

The updated search target is therefore narrower:

```text
a relational clump with pairwise active modes, separation dynamics, and a
collective/critical mechanism for soft relational excitations.
```

Plain connector counting is not enough. Plain stripped commutator-squared
matrix dynamics is not enough. The viable connector version needs a critical
relational spectrum.

The next candidate must add one of:

```text
1. a critical/gapless connector sector;
2. separation-dependent connector gaps;
3. a stabilizing matrix-clump mechanism that still permits escape;
4. a known long-range/nonadditive quantum model with compatible emission
   operators.
```

The current best bet is now:

```text
quadratic critical connector ring/clump.
```

It keeps:

```text
S ~ N^2 from pairwise relational modes;
M ~ N from active constituent count;
omega ~ 1/N from a one-dimensional quadratic connector band;
mostly positive post-emission heating after N -> N-1;
possibly P ~ 1/N^2 from local spectral-weight normalization, depending on
the spectral density.
```

The next gate is:

```text
find or build a microscopic Hamiltonian whose active connector sector naturally
has a one-dimensional critical spectrum with O(N^2) modes.
```

The central tension is now sharper:

```text
alpha=1-like / linear spectra:
  good power scaling, fragile heating;

alpha=2-like / quadratic spectra:
  robust heating, weaker power scaling;

critical ring:
  only survives the heating gate in its quadratic version; this points toward
  nonrelativistic Goldstone or ferromagnetic-type connector modes rather than
  a standard massless harmonic chain.

power scaling:
  the quadratic band gives P ~ N^-3/2 with naive local spectral weight;
  the target P ~ N^-2 is recovered if |g(omega)|^2 ~ omega^1/2;
  that emission matrix-element scaling now has to come from the Hamiltonian.
```

There is also a scale constraint:

```text
if M ~ N and S ~ N^2, then T ~ 1/N;
one microscopic emitted quantum has energy ~ 1/N;
one coarse N -> N-1 shrink changes M by ~ 1;
therefore one coarse shrink represents O(N) microscopic emissions.
```

So the next non-micro step is to construct a quadratic connector evaporator
with many microscopic emissions per coarse shrink step, then measure all gates
in one run:

```text
state count;
energy scaling;
soft emission spectrum;
post-emission heating;
power scaling;
core/radiation entropy flow.
```
