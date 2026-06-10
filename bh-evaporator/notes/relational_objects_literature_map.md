# Relational Evaporator: Literature Object Map

## Purpose

We want to know what the literature already has that looks like:

```text
objects carry mass;
relations carry entropy;
evaporation removes one object and decouples many relations.
```

The answer is:

```text
many pieces exist, but the full non-gravitational evaporator package does not
seem to be a standard object.
```

## Summary Table

```text
Object class                  Relation degrees            Good for              Weak point
----------------------------------------------------------------------------------------------------
Matrix/D0 models              off-diagonal modes           N^2 entropy, heating  holographic/BH-adjacent
Large-N gauge plasma          adjoint color relations      N^2 thermodynamics    no shrinking object N
Quantum graphity              edge/link Hilbert spaces     explicit relations    not evaporation-focused
Gauge edge modes              boundary/link-crossing modes soft entropy          not finite evaporator
Soft hair                     near-horizon soft charges    low-energy memory     debated completeness
Tensor networks               entanglement bonds           relational entropy    usually kinematic
SYK/all-to-all                all-to-all interactions      chaos/scrambling      entropy ~ N, not N^2
```

## Matrix/D0 Models

References:

```text
Berkowitz, Hanada, Maltz,
"Chaos in Matrix Models and Black Hole Evaporation",
arXiv:1602.01473.

Berkowitz, Hanada, Maltz,
"A microscopic description of black hole evaporation via holography",
arXiv:1603.03055.
```

Mapping:

```text
objects       = D0-branes / matrix blocks
relations     = off-diagonal matrix elements / open strings
entropy       = active noncommuting matrix degrees ~ N^2
evaporation   = U(N) -> U(N-1) x U(1)
heating        = off-diagonal connector modes decouple; energy per active mode rises
```

Why it matters:

```text
This is the closest known mechanism to our relational evaporator.
```

Why it is not enough for us:

```text
It is explicitly black-hole/holography-adjacent. The goal there is matrix
black-hole evaporation, not a clean non-gravitational control model.
```

## Large-N Gauge Theory Plasma

Mapping:

```text
objects       = color indices / matrix rows-columns
relations     = adjoint gluonic degrees
entropy       = deconfined O(N^2) degrees
```

Why it matters:

```text
The idea that relational/matrix degrees give N^2 entropy is standard in
large-N gauge theory.
```

Weakness:

```text
There is usually no evaporation step N -> N-1. The rank N is fixed.
```

This is useful background, but not yet an evaporator.

## Quantum Graphity / Dynamical Graphs

References:

```text
Konopka, Markopoulou, Smolin,
"Quantum Graphity: a model of emergent locality",
arXiv:0801.0861.

Hamma, Markopoulou, Premont-Schwarz, Severini,
"A quantum Bose-Hubbard model with evolving graph as toy model for emergent spacetime",
arXiv:0911.5075.
```

Mapping:

```text
objects       = vertices
relations     = quantum edge/link degrees
entropy       = graph/link Hilbert space
geometry      = emergent from active links
```

Why it matters:

```text
This is the closest non-matrix precedent for explicit relation Hilbert spaces.
```

Weakness:

```text
The target is emergent locality/geometry, not black-hole-like evaporation,
negative heat capacity, or Page-like radiation.
```

## Gauge Edge Modes

References:

```text
Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
arXiv:1412.1895.

"Dynamical Edge Modes and Entanglement in Maxwell Theory",
arXiv:2403.14542.
```

Mapping:

```text
objects       = regions / bulk gauge systems
relations     = boundary-crossing gauge constraints and edge modes
entropy       = boundary/area-localized edge contribution
```

Why it matters:

```text
This gives a principled way for relation-like degrees to contribute entropy at
a boundary without being ordinary bulk particles.
```

Weakness:

```text
It does not by itself give a finite shrinking evaporator with N -> N-1.
```

## Soft Hair

Representative references:

```text
Hawking, Perry, Strominger,
"Soft Hair on Black Holes",
arXiv:1601.00921.

Afshar et al.,
"Soft Heisenberg hair on black holes in three dimensions",
and related near-horizon soft-hair work.

"Membrane Paradigm from Near Horizon Soft Hair",
arXiv:1805.11099.
```

Mapping:

```text
objects       = black-hole background / horizon cells
relations     = soft charges, boundary modes, large-gauge data
entropy       = low-energy or zero-energy labels
```

Why it matters:

```text
This is the best precedent for entropy-rich, low-energy degrees of freedom.
```

Weakness:

```text
Soft hair as a complete account of black-hole entropy/information is not
settled. Also, this is gravitational rather than a non-gravitational control.
```

## Tensor Networks

Mapping:

```text
objects       = tensors / nodes
relations     = bonds / entanglement links
entropy       = cut bonds
```

Why it matters:

```text
Relational entropy is natural: entropy is literally counted by links crossing
cuts.
```

Weakness:

```text
Most tensor-network uses are kinematic. They prescribe a state or ensemble,
not a Hamiltonian evaporator with negative heat capacity and emitted power.
```

## SYK / All-To-All Models

Mapping:

```text
objects       = Majorana fermions
relations     = all-to-all random couplings
```

Why it matters:

```text
SYK is black-hole-adjacent, chaotic, and all-to-all.
```

Weakness:

```text
The couplings are usually quenched parameters, not active relation Hilbert
spaces. Entropy scales as O(N), not O(N^2).
```

So SYK is not the right direct model for the relational entropy mechanism.

## What Seems Missing

The exact object we want would combine:

```text
1. explicit finite Hilbert space;
2. object count N;
3. active relation count ~ N^2;
4. entropy dominated by relations;
5. mass/energy dominated by objects or a collective scale ~ N;
6. evaporation N -> N-1;
7. decoupling of O(N) relations per emission;
8. radiation/archive accounting for the decoupled relation information;
9. rate dynamics strong enough to accelerate.
```

No surveyed literature class obviously contains all nine in a clean
non-gravitational model.

## Current Judgment

The relational evaporator is not an unexplored ingredient.

Its ingredients are well known:

```text
N^2 matrix degrees;
edge/link Hilbert spaces;
soft edge modes;
boundary entropy;
all-to-all relational structures.
```

The possible result is in the synthesis:

```text
use relational entropy dominance to reproduce the black-hole thermodynamic
backbone in a finite non-gravitational evaporator.
```

That is more interesting than another qubit Page model and more structural
than Track E's area-register mass law.

