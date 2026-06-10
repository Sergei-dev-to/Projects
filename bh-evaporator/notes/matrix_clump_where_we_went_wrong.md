# Matrix Clumping: Where We Went Wrong

## Purpose

We tried to strip the matrix-clump idea into a simple classical matrix toy.

After rereading the matrix-evaporation literature, the stripped test was too
naive. It removed several ingredients that are not decorative. They are part of
the evaporation mechanism.

Primary references:

```text
Berkowitz, Hanada, Maltz,
"Chaos in Matrix Models and Black Hole Evaporation",
arXiv:1602.01473.

Berkowitz, Hanada, Maltz,
"A microscopic description of black hole evaporation via holography",
arXiv:1603.03055.

Berenstein, Guan,
"Improved semiclassical model for real time evaporation of Matrix black holes",
arXiv:2105.04577.

Du, Sahakian,
"Emergent geometry from stochastic dynamics, or Hawking evaporation in
M(atrix) theory",
arXiv:1812.05020.
```

## Correct Literature Picture

The successful matrix story is not:

```text
generic eigenvalues form a visible spatial clump;
one radial eigenvalue wanders away;
the remaining clump kinetically heats.
```

It is closer to:

```text
black hole = one fully noncommutative U(N) matrix block;
emission = rare transition to block diagonal U(N-1) x U(1);
escaped D0 = separated U(1) block;
off-diagonal strings between the blocks become heavy and decouple;
remaining block has fewer active degrees of freedom;
energy conservation then raises energy per degree of freedom.
```

So the interior is not primarily an eigenvalue gas. The clean eigenvalue /
position picture appears after separation.

That matters because our diagnostic looked for:

```text
eigenvalue spread inside the whole matrix configuration.
```

But the literature's physical split is:

```text
block structure and decoupling of off-diagonal modes.
```

## Mistake 1: Treating The Black Hole As A Commuting Eigenvalue Clump

In the matrix black-hole picture, a single black hole is described by generic
noncommuting matrices with many active off-diagonal modes.

The commuting/eigenvalue picture is good for sparse D0-brane gas states or for
well-separated blocks.

Our note said:

```text
matrix degrees -> approximate commuting sector -> eigenvalues as positions
-> clump -> escape.
```

That is not the black-hole regime. It is closer to the asymptotic radiation
regime.

Corrected version:

```text
black hole phase:
  noncommuting block, no clean individual D0 positions;

radiation phase:
  approximate block diagonalization, clean separated U(1) degree of freedom.
```

## Mistake 2: Expecting The Bare Classical Bosonic Model To Evaporate

Berenstein and Guan are explicit about this point. In the naive classical
two-matrix model, the flat directions are too thin. Trajectories can make long
excursions, but generically they return.

They add an extra long-distance term interpretable as a fermionic zero-point
energy contribution. That term makes indefinite separation possible in their
classical real-time model.

So our stripped Hamiltonian:

```text
H = kinetic + commutator-squared potential
```

was missing the ingredient that lets an escaping brane keep escaping.

Our result:

```text
mostly no clean escape; occasional ambiguous radial excursions;
mixed post-event heating.
```

is therefore not surprising. It is close to what the literature would lead us
to expect for the bare classical bosonic model.

## Mistake 3: Treating Heating As A Local Virial/Kinetic Event

The heating argument in Berkowitz-Hanada-Maltz is mostly a state-count /
degree-of-freedom argument.

Before emission:

```text
active black-hole degrees of freedom ~ N^2.
```

After one D0-brane emission:

```text
active black-hole degrees of freedom ~ (N-1)^2,
escaped D0 degrees of freedom ~ O(1),
off-diagonal blocks decouple.
```

Most of the energy remains in the black-hole block. Since the black-hole block
has fewer active degrees of freedom, the energy per degree of freedom rises.
That is the temperature increase.

Our diagnostic instead measured:

```text
projected kinetic energy of the remaining radial subspace.
```

That is not the same quantity.

A better stripped diagnostic would compare:

```text
temperature of an N x N noncommuting block
vs
temperature of an (N-1) x (N-1) noncommuting block after one block decouples,
with energy conserved.
```

That is more like a microcanonical block-count calculation than a simple
trajectory-temperature measurement.

## Mistake 4: Treating Emission As A Typical Short-Time Event

The literature presents D0 emission as entropically suppressed at large N but
eventually realized through chaotic/ergodic dynamics.

This is not the same as:

```text
run one random initial condition for moderate time and wait for evaporation.
```

The relevant story is rare-event dynamics:

```text
generic noncommuting block;
rare fluctuation toward a block-diagonal configuration;
off-diagonal modes decouple;
separated block moves along a flat direction.
```

Our scans were not set up as rare-event sampling, transition-state analysis, or
microcanonical entropy comparison.

## Mistake 5: Forgetting The Gauge/Block Structure

We used real symmetric traceless matrices and radial eigenvectors of:

```text
R^2 = sum_a X_a^2.
```

That is a rough shape diagnostic, not the physical splitting used in the
papers.

The relevant splitting is closer to:

```text
U(N) -> U(N-1) x U(1)
```

with off-diagonal strings becoming heavy.

So the better observable is not simply:

```text
largest eigenvalue of R^2.
```

It is:

```text
can the matrices be approximately block diagonalized into a large block plus a
small block, and are the off-diagonal blocks dynamically heavy/adiabatic?
```

## Mistake 6: Confusing A Holographic Mechanism With A Generic Matrix Toy

The known mechanism is deeply tied to:

```text
D0-brane matrix quantum mechanics;
off-diagonal open-string modes;
fermionic/supersymmetric cancellations or corrections;
large-N entropy counting;
holographic black-zero-brane thermodynamics.
```

Du-Sahakian go even further: their model uses stochastic coarse-graining and
known black-hole scales to construct a mean-field evaporation picture.

So the matrix literature does not straightforwardly give:

```text
all BH phenomenology, none of gravity.
```

It gives:

```text
all BH phenomenology, but in a matrix-theory/holographic setting where the
black-hole interpretation is doing real work.
```

## Corrected Lesson

The useful lesson is not:

```text
bare commutator-squared matrices naturally evaporate like black holes.
```

The useful lesson is:

```text
negative heat capacity can arise naturally when evaporation dynamically removes
many internal coupling degrees of freedom while most energy remains in the
surviving bound subsystem.
```

That is the transferable mechanism.

In matrix language:

```text
emitting one D0 removes O(N) off-diagonal connections to the black-hole block;
the block has fewer active degrees of freedom;
energy per active degree rises.
```

This is closer to our original Track E bookkeeping than it first looked, but
with a better physical interpretation:

```text
shrinking Hilbert space = decoupling of off-diagonal connector modes.
```

## What To Do With This

There are two honest paths.

### Path 1: Follow The Matrix Literature Faithfully

Use a model closer to Berenstein-Guan:

```text
two-matrix SU(2) reduction;
explicit radial/angle variables;
fermionic zero-point / long-distance correction;
adiabatic invariant for off-diagonal modes.
```

This is worthwhile if the question is:

```text
how matrix black holes evaporate.
```

But it is not our clean non-gravitational control system.

### Path 2: Extract The Degree-Of-Freedom Decoupling Principle

Forget literal eigenvalue clump dynamics for now.

Build a non-gravitational finite quantum model where evaporation:

```text
1. removes one visible subsystem;
2. also decouples many connector degrees of freedom;
3. leaves most energy in the remaining core;
4. therefore raises energy per active degree of freedom.
```

This preserves the transferable lesson without pretending that the stripped
matrix Hamiltonian already works.

## Current Judgment

We went wrong by over-stripping the matrix mechanism.

The literature does not support the claim that a bare bosonic
commutator-squared matrix toy should robustly evaporate and heat.

It supports a subtler claim:

```text
matrix black-hole evaporation works because block separation dynamically
reduces the number of active off-diagonal degrees of freedom, while quantum /
fermionic ingredients allow the separated block to escape.
```

For our project, the more promising transferable idea is not "matrix clump" by
itself.

It is:

```text
evaporation as connector-mode decoupling.
```

