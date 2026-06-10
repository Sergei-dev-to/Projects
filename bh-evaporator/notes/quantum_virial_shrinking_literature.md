# Quantum Virial Shrinking Literature Review

## Question

Can we get negative heat capacity more naturally from a quantum version of
adiabatic/virial shrinking, rather than imposing:

```text
S_n = n log 2
M_n ~ sqrt(n)?
```

The standard phrase is not usually "quantum virial shrinking." The relevant
literature is spread across:

```text
1. virial theorem and self-gravitating systems;
2. gravothermal catastrophe / negative specific heat;
3. quantum self-gravitating gases;
4. finite clusters with negative microcanonical heat capacity;
5. D0-brane / matrix-model evaporation.
```

## Mechanism

For a bound attractive system satisfying a virial relation:

```text
2K + U = 0
```

with:

```text
K > 0
U < 0
E = K + U = -K
```

energy loss makes:

```text
E more negative
K larger
T larger
```

So:

```text
losing energy -> contraction -> heating
```

This is the natural route to negative heat capacity in self-bound systems.

In a quantum model, the same logic uses the quantum virial theorem:

```text
2<K> = <r · grad V>
```

or, for homogeneous potentials:

```text
2<K> = p <V>,   V(lambda r) = lambda^p V(r).
```

For Coulomb/gravity-like attraction:

```text
p = -1
2<K> = -<V>
E = -<K>.
```

## Thread 1: Classical Self-Gravitating Systems

This is the cleanest source of the mechanism.

Key references:

```text
Antonov instability / Lynden-Bell and Wood gravothermal catastrophe.

Hachisu and Sugimoto,
"Gravothermal Catastrophe and Negative Specific Heat of Self-Gravitating
Systems",
Progress of Theoretical Physics 60, 123 (1978).

Bjorn Einarsson,
"Conditions for negative specific heat in systems of attracting classical
particles",
Phys. Lett. A 332, 335 (2004), arXiv:gr-qc/0405130.
```

Takeaway:

```text
negative heat capacity is not a black-hole-only phenomenon;
it is generic in isolated self-gravitating/attractive systems under the right
conditions.
```

Important nuance from Einarsson:

```text
negative heat capacity is not caused by long-range forces alone.
The potential exponent and density singularities matter.
For simple virial arguments, the inverse-radius case is special.
```

## Thread 2: Quantum Self-Gravitating Gases

There is a serious literature on quantum statistics plus self-gravity:

```text
self-gravitating Fermi gas;
self-gravitating Bose gas;
boson stars / Bose-Einstein dark matter;
general-relativistic quantum Fermi gases.
```

Key references:

```text
Pierre-Henri Chavanis,
"Statistical mechanics and thermodynamic limit of self-gravitating fermions
in D dimensions",
arXiv:0708.1888.

Pierre-Henri Chavanis,
"Statistical mechanics of self-gravitating systems in general relativity:
I. The quantum Fermi gas",
arXiv:1908.10806.

Schive et al. / fuzzy dark matter literature:
Schrodinger-Poisson systems obey quantum virial/Ehrenfest relations;
solitonic cores are supported by quantum pressure against self-gravity.
```

Takeaway:

```text
quantum mechanics can stabilize or modify self-gravitating collapse through
degeneracy pressure or quantum pressure;
caloric curves and negative specific heat remain central diagnostics.
```

For our project:

```text
this is closer to a real gravitational system than to a non-gravitational toy;
but it shows how a quantum many-body system can have virial shrinking and
negative heat capacity without assigning M_n by hand.
```

## Thread 3: Finite Clusters and Microcanonical Negative Heat Capacity

This is the non-gravitational finite-system analogue.

Key references:

```text
M. Schmidt et al.,
"Negative Heat Capacity for a Cluster of 147 Sodium Atoms",
Phys. Rev. Lett. 86, 1191 (2001).

Haberland/Schmidt cluster calorimetry papers on sodium clusters.

Nuclear multifragmentation literature on negative heat capacity near
liquid-gas transitions.
```

Takeaway:

```text
finite isolated systems can have negative microcanonical heat capacity,
especially around first-order-like transitions / convex intruders in S(E).
```

This is non-gravitational and experimentally grounded.

But the mechanism is not exactly virial shrinking:

```text
it is usually phase coexistence / surface entropy / convex intruder,
not a self-bound inverse-radius virial relation.
```

For our project:

```text
cluster physics supports the "convex intruder as cold bath" route from the
earlier evaporator work;
it does not naturally give black-hole entropy scaling S ~ M^2.
```

## Thread 4: Attractive Quantum Many-Body Systems

Examples:

```text
attractive Bose gas;
self-bound droplets;
long-range attractive spin/boson models;
Schrodinger-Newton / Bose-star models.
```

These can exhibit:

```text
collapse;
self-binding;
breathing modes;
virial relations;
metastability.
```

But ordinary cold-atom attractive models usually do not automatically give a
stable microcanonical negative-heat-capacity evaporator. They often:

```text
collapse;
fragment;
need external trapping;
or are stabilized by quantum pressure / beyond-mean-field terms.
```

For our project:

```text
an attractive Bose-Hubbard or long-range boson model is a plausible sandbox,
but we should not expect black-hole scaling to emerge automatically.
```

## Thread 5: D0-Brane / Matrix-Model Evaporation

This is highly relevant conceptually, though not non-gravitational in the
spirit of our control model because it is holographic/quantum-gravity-adjacent.

Key reference:

```text
"Chaos in Matrix Models and Black Hole Evaporation",
Phys. Rev. D 94, 126009 (2016), arXiv:1602.01473.
```

Takeaway:

```text
matrix quantum mechanics can model a black-zero-brane-like bound object;
flat directions allow emission of D0-branes;
the object heats as it evaporates, showing negative specific heat.
```

This is close to the idea:

```text
self-bound quantum object + evaporation + negative heat capacity.
```

But it is not a simple non-gravitational laboratory analogue; it is part of a
gauge/gravity-duality program.

## Implication For Our Project

There are two natural mechanisms for negative heat capacity:

```text
1. virial/self-binding mechanism:
   energy loss -> contraction -> kinetic heating;

2. microcanonical convex-intruder mechanism:
   finite-system phase coexistence makes S(E) locally convex.
```

Our current Track E uses neither as a microscopic mechanism.

It imposes:

```text
S ~ M^2
```

at the sector level.

If we want a more natural model, the next target should be:

```text
a finite quantum system with an actual microcanonical negative-C window,
measured from its spectrum or dynamics, before imposing black-hole-like
evaporation.
```

## Candidate Next Models

### Candidate A: Attractive Bose-Hubbard / long-range boson model

Question:

```text
Does the microcanonical caloric curve T(E) show dT/dE < 0 in a useful window?
```

Strength:

```text
concrete quantum Hamiltonian;
particle loss already natural.
```

Weakness:

```text
entropy scaling likely not black-hole-like;
collapse/localization may dominate.
```

### Candidate B: finite cluster / convex-intruder model

Question:

```text
Can we build a quantum shell model with a convex S(E) region and derive
evaporation acceleration from it?
```

Strength:

```text
closest to finite-system thermodynamics literature.
```

Weakness:

```text
may be too engineered, similar to the old shell evaporator.
```

### Candidate C: matrix-model-inspired bound object

Question:

```text
Can a small matrix quantum mechanics / all-to-all attractive model produce
evaporation and heating through eigenvalue emission?
```

Strength:

```text
closest to known black-hole-like quantum evaporation mechanisms.
```

Weakness:

```text
technically heavier and closer to gravity/holography.
```

## Current Judgment

The virial route is real and well discussed, but it points away from the spin
chain and toward self-bound attractive quantum systems.

It can make negative heat capacity more natural.

It will not by itself give:

```text
S ~ M^2
Page structure
Hawking-like radiation
```

So it is best treated as a separate subproblem:

```text
Can we replace imposed negative heat capacity with an emergent microcanonical
negative-C window?
```

If yes, then later ask whether it can be coupled to explicit radiation.
