# Connector-Mode Evaporator

## Status In The Larger Program

This is one implementation of the broader relational evaporator principle:

```text
bh-evaporator/notes/relational_evaporator_principle.md
```

The broader principle is:

```text
mass scales with objects;
entropy scales with relations among objects;
evaporation removes one object and decouples many relations.
```

The connector-mode model realizes this with:

```text
objects = sites;
relations = explicit pairwise connector modes.
```

So this note should be read as a test case, not as the whole idea.

## Purpose

This is the clean non-gravitational translation of the matrix-model lesson.

The matrix literature suggests that the useful mechanism is not literal
eigenvalue clumping. It is:

```text
evaporation removes a visible subsystem and also decouples many connector
modes between that subsystem and the remaining core.
```

That gives a natural way for the remaining core to heat:

```text
most energy stays in the core;
the number of active core degrees of freedom drops sharply;
energy per active degree rises.
```

This note asks whether that principle can become a finite quantum evaporator
without importing the full D0-brane / holographic story.

## Basic Picture

Take `N` core sites.

There are two kinds of active degrees of freedom:

```text
site modes:       one per site
connector modes: one per unordered pair of sites
```

So the active mode count is:

```text
q_N = a N + b N(N-1)/2.
```

For large `N`,

```text
q_N ~ (b/2) N^2.
```

When one site evaporates, the core changes:

```text
N -> N-1.
```

But more importantly, the emitted site loses its connectors to the remaining
core:

```text
N-1 connector modes decouple.
```

So active modes drop by:

```text
Delta q_N = q_N - q_(N-1) = a + b(N-1).
```

This is the toy analogue of:

```text
U(N) matrix block -> U(N-1) x U(1)
off-diagonal modes connecting the two blocks decouple.
```

## Why This Can Heat

Let the core have energy:

```text
E_N
```

and active mode count:

```text
q_N.
```

Define a kinetic/equipartition temperature proxy:

```text
T_N = E_N / q_N.
```

After emission:

```text
E_(N-1) = E_N - epsilon_N,
q_(N-1) < q_N.
```

The remaining core heats if:

```text
T_(N-1) > T_N
```

or:

```text
(E_N - epsilon_N) / q_(N-1) > E_N / q_N.
```

Rearranging:

```text
epsilon_N / E_N < 1 - q_(N-1)/q_N.
```

The right-hand side is the fractional loss of active degrees of freedom.

For connector-dominated systems:

```text
q_N ~ N^2,
q_(N-1)/q_N ~ (N-1)^2/N^2,
1 - q_(N-1)/q_N ~ 2/N.
```

So the core heats if the emitted subsystem carries away less than about:

```text
2 E_N / N.
```

This matches the matrix-model intuition:

```text
the emitted object carries O(1) energy while the black-hole block carries
O(N^2) energy, so most energy remains in the block.
```

## Negative Heat Capacity

The heat-capacity sign is not automatic from mode counting alone. It depends on
how total core energy scales with `N`.

If:

```text
E_N ~ e q_N T_N
```

then simply removing modes at fixed temperature is ordinary positive heat
capacity.

Negative heat capacity appears along the evaporation trajectory when:

```text
E_(N-1) < E_N
but
T_(N-1) > T_N.
```

The connector criterion above gives the exact condition.

In words:

```text
the core loses energy but loses active modes faster than it loses energy.
```

That is the transferable content.

## Entropy And State Count

If each active mode is a qubit or finite qudit, then:

```text
dim H_N = d_site^N d_conn^[N(N-1)/2]
S_N = N log d_site + N(N-1)/2 log d_conn.
```

For connector-dominated systems:

```text
S_N ~ N^2.
```

This is much more natural than Track E's imposed area register:

```text
Track E:
  S_n ~ n by using n qubits.

Connector model:
  S_N ~ N^2 because pairwise connector modes are active.
```

If the mass/energy scale grows linearly with `N`,

```text
M_N ~ N,
```

then:

```text
S_N ~ M_N^2.
```

This is the first real improvement over Track E.

Track E imposed:

```text
M_n ~ sqrt(n)
```

where `n` was already the entropy variable.

The connector model instead suggests:

```text
entropy ~ number of connectors ~ N^2,
mass ~ number of sites ~ N.
```

That gives the black-hole entropy scaling by architecture rather than by a
chosen square-root mass law.

## Temperature Scaling

If:

```text
S_N ~ sigma N^2,
M_N ~ mu N,
```

then microcanonically:

```text
1/T = dS/dM ~ (2 sigma / mu) N.
```

So:

```text
T_N ~ 1/N ~ 1/M_N.
```

This is exactly the Schwarzschild-like sign and scaling.

The key is:

```text
site count N behaves like mass;
connector count N^2 behaves like area entropy.
```

That is the cleanest conceptual payoff of this branch.

## Minimal Quantum Hilbert Space

A literal finite model would use:

```text
H_N = H_site(N) tensor H_conn(N)
```

with:

```text
H_site(N) = tensor_i C^d_s
H_conn(N) = tensor_{i<j} C^d_c.
```

The active core at size `N` contains:

```text
N site qudits
N(N-1)/2 connector qudits.
```

Emission of site `N` maps:

```text
H_N -> H_(N-1) tensor R_N
```

where the radiation system contains:

```text
the emitted site qudit
the N-1 connector qudits that used to link it to the core
possibly an energy/time-bin label.
```

This is important. The emitted radiation is not just one qubit.

The radiation quantum carries:

```text
one visible site plus its connector cloud.
```

This may solve the earlier tension:

```text
small one-qubit radiation was too poor to be thermodynamically faithful;
full transition records were too artificial;
connector-cloud radiation has intermediate, physically motivated size.
```

## Minimal Hamiltonian Idea

The simplest block Hamiltonian is:

```text
H_N = H_sites + H_connectors + H_interactions.
```

For a first toy version:

```text
H_sites       = sum_i h_i
H_connectors  = sum_{i<j} h_ij
H_interactions = sum_{i<j} V(i, ij, j)
```

where connector `ij` couples only to the two endpoint sites.

The important locality is not spatial locality. It is incidence locality:

```text
connector ij only talks to sites i and j.
```

Evaporation of site `N` naturally decouples all modes incident on `N`.

## Emission Map

A simple deterministic split would be:

```text
V_N:
  core sites 1..N, connectors among them
  ->
  core sites 1..N-1, connectors among them
  tensor
  radiation containing site N and connectors (i,N).
```

But deterministic splitting alone is C1-like and too kinematic.

For a thermodynamic evaporator, emission should be energy filtered:

```text
Gamma_{f,r;i} ~ |<f,r|V_N|i>|^2 J(E_i - E_f - E_r).
```

Here:

```text
i = initial state in H_N
f = final state in H_(N-1)
r = radiation state in emitted site + connector cloud.
```

This is more natural than a full transition record because `r` is a real
subsystem, not a label invented to distinguish Kraus branches.

## First Counting Diagnostic

Before building the Hamiltonian, test the thermodynamic skeleton.

Assume:

```text
S_N = s N^2
M_N = mu N
epsilon_N = eta T_N
```

Then:

```text
T_N = dM/dS ~ 1/N.
```

Energy emitted per step:

```text
epsilon_N ~ 1/N.
```

If the number flux scales as:

```text
gamma_N ~ area * T^3 ~ N^2 * (1/N)^3 ~ 1/N,
```

then emitted power is:

```text
P_N ~ gamma_N epsilon_N ~ 1/N^2.
```

As `N` decreases, power increases.

So the connector model can reproduce the Schwarzschild rate structure if:

```text
available emission channels scale like connector area ~ N^2;
typical emitted energy scales like T ~ 1/N;
thermal occupation/filtering gives T^3-like suppression.
```

This last line is where a Hamiltonian/radiation-mode model has to do real work.

## Where This Could Fail

The model can still fail in several ways.

### Failure 1: Too much energy leaves with the connector cloud

Heating requires:

```text
epsilon_N / E_N < 1 - q_(N-1)/q_N.
```

If the emitted site plus connector cloud carries away energy proportional to
the modes it removes, then temperature may stay constant or decrease.

So the connector cloud must carry information/decoupled degrees of freedom
without carrying proportional energy.

This mirrors black holes:

```text
entropy loss per emitted quantum is large compared with the emitted energy.
```

### Failure 2: Radiation becomes too large

The emitted radiation subsystem has size:

```text
1 site + (N-1) connectors.
```

That is much larger than one Hawking quantum.

Possible interpretation:

```text
the connector cloud is soft/hair-like memory accompanying the visible emitted
quantum.
```

But this must be handled carefully. If each emission releases O(N) qudits of
radiation, Page-like behavior may become trivial.

### Failure 3: Hamiltonian is arbitrary

A complete graph of qudits with connector qudits is an engineered incidence
system.

It is less arbitrary than Track E's mass law, but still not a standard
condensed-matter Hamiltonian.

The question is whether the mechanism is clear enough to justify the toy:

```text
area entropy from connectors;
mass from sites;
heating from connector decoupling.
```

### Failure 4: Dynamics does not select the right energy scale

The counting gives:

```text
T ~ 1/N
```

but the Hamiltonian spectrum may not produce typical emitted energies of order
`1/N`.

This likely requires either:

```text
1. explicit N-dependent coupling scale;
2. collective low-energy modes whose gaps shrink like 1/N;
3. a bath/radiation spectral function that filters energies thermally.
```

This is the next hard question.

## Relation To Prior Tracks

### Compared with Track E

Track E:

```text
H_n = n qubits
S_n ~ n
M_n ~ sqrt(n)
```

Connector model:

```text
H_N = N sites + O(N^2) connectors
S_N ~ N^2
M_N ~ N
```

So the connector model moves the square from the mass law into the state count.

That is more natural.

### Compared with C1 detached qubits

C1 emits:

```text
one qubit per step.
```

Connector model emits:

```text
one site plus its connector cloud.
```

So the emitted subsystem is not too small to carry the thermodynamic
consequences of shrinkage.

### Compared with exact transition records

Exact records emit:

```text
transition labels.
```

Connector model emits:

```text
real degrees of freedom that used to participate in the Hamiltonian.
```

That is less artificial.

## Minimal Next Test

The first useful test is not a full Hamiltonian simulation.

It is a counting/rate skeleton:

```text
N sites;
S_N = log dim H_N from site+connector qudits;
M_N = mu N;
T_N = (dS/dM)^-1;
gamma_N = c N^p T_N^q;
epsilon_N = k T_N;
P_N = gamma_N epsilon_N.
```

Scan `p,q` and ask:

```text
which channel-count/spectral-filter exponents give accelerating power?
```

Then we know what a Hamiltonian has to reproduce.

For Schwarzschild-like behavior:

```text
p = 2
q = 3
```

because:

```text
area ~ N^2,
thermal flux in 3+1 dimensions ~ T^3,
energy per quantum ~ T.
```

But for a generic finite quantum toy, other exponents are possible.

## Decision Point

This branch is worth pursuing if we can make one of these two statements true:

```text
1. Connector counting alone naturally gives S ~ M^2 and T ~ 1/M, improving
   Track E's imposed mass law.

2. A simple incidence-local Hamiltonian plus energy-filtered emission gives
   accelerating power and nontrivial radiation without transition records.
```

Statement 1 is already true at the counting level.

Statement 2 remains open.

## Current Judgment

The connector-mode evaporator is the best conceptual bridge found so far.

It preserves the useful matrix-model lesson:

```text
evaporation dynamically decouples many connector modes.
```

It improves Track E:

```text
S ~ M^2 comes from pairwise active modes rather than an imposed square-root
mass law.
```

The main unresolved issue is dynamics:

```text
can a reasonable Hamiltonian make the emitted energy and rate scale correctly,
without imposing the evaporation schedule?
```
