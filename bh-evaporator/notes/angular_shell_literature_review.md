# Angular-Shell Evaporator: Literature Review

## Question

Before building the angular-shell evaporator, check whether the same idea is
already present in the literature.

The proposed branch:

```text
soft angular labels Y_lm with l <= L;
mode count (L+1)^2;
mass/size M ~ L;
evaporation L -> L-1;
removed shell l=L carries soft memory.
```

## Short Answer

Several close ingredients exist.

The exact package does not appear to be standard:

```text
finite non-gravitational angular-shell evaporator
with shrinking cutoff L -> L-1,
hard radiation plus soft shell memory,
and S ~ M^2 from angular soft labels.
```

But the angular-mode part is not isolated from the literature. It has strong
nearby precedents.

## 1. Stretched-Horizon Normal Modes

Reference:

```text
Chethan Krishnan, Pradipta S. Pathak,
"Normal Modes of the Stretched Horizon: A Bulk Mechanism for Black Hole
Microstate Level Spacing",
arXiv:2312.14109.
```

Main relevance:

```text
They explicitly compute stretched-horizon normal modes and argue that
quasi-degeneracy in angular quantum numbers is responsible for the area
scaling of entropy.
```

This is the closest literature match to our angular-shell count.

Our proposed count:

```text
sum_{l=0}^L (2l+1) = (L+1)^2.
```

Their abstract-level message:

```text
angular quantum-number quasi-degeneracy distinguishes area scaling from
ordinary volume-scaling black-body counting.
```

Difference:

```text
Their setting is a black-hole stretched horizon / brick-wall style normal-mode
calculation.

Our target is a finite evaporator toy with an explicit shrinking cutoff and
radiation/memory channel.
```

Assessment:

```text
Very relevant. It strongly supports the intuition that angular degeneracy is
the right basis for area entropy. But it does not give our non-gravitational
evaporator.
```

## 2. Brick-Wall / Stretched-Horizon Mode Counting

Reference class:

```text
't Hooft brick-wall model and later stretched-horizon mode counts.
```

Core idea:

```text
near-horizon field modes, including angular modes, are counted with a cutoff;
the resulting entropy scales like horizon area.
```

Relevance:

```text
This is the older ancestor of angular-shell counting.
```

Danger:

```text
ordinary field modes are not soft memory labels;
the entropy is cutoff-sensitive;
the setup is explicitly gravitational.
```

Assessment:

```text
Good precedent for angular/area counting, weak precedent for a clean
information-preserving evaporator.
```

## 3. Soft Hair / Horizon Supertranslations

References:

```text
Hawking, Perry, Strominger,
"Soft Hair on Black Holes",
arXiv:1601.00921.

Averin, Dvali, Gomez, Lust,
"Gravitational Black Hole Hair from Event Horizon Supertranslations",
arXiv:1601.03725.
```

Relevance:

```text
Horizon soft hair is naturally expanded in angular functions on the sphere.
The modes are intended as soft/gapless or low-energy labels, not ordinary bulk
excitations.
```

This is close to our required interpretation:

```text
Y_lm labels as soft edge/memory sectors.
```

Important support:

```text
Averin-Dvali-Gomez-Lust explicitly discuss infinitely many gapless horizon
excitations, then argue that quantum effects make the information-carrier
count finite and compatible with Bekenstein entropy.
```

Difference:

```text
This is gravitational soft hair, not a non-gravitational finite toy.
It also does not by itself provide a clean evaporation map L -> L-1.
```

Assessment:

```text
Strong motivation for the "soft angular labels" interpretation, but not a
complete evaporator.
```

## 4. Soft-Hair Qubit Evaporation Models

Reference:

```text
Hotta, Nambu, Yamaguchi,
"Soft-Hair-Enhanced Entanglement Beyond Page Curves in a Black-hole
Evaporation Qubit Model",
arXiv:1706.07520.
```

Relevance:

```text
This model includes both Hawking-particle emission and zero-energy soft-hair
evaporation, while reproducing thermal properties of 4D Schwarzschild black
holes.
```

This overlaps with our proposed radiation split:

```text
hard radiation + soft memory.
```

Difference:

```text
Their model is a qubit evaporation model, not an angular shell mode-counting
model. It does not appear to derive S ~ M^2 from an angular cutoff
(L+1)^2.
```

Assessment:

```text
Important overlap warning for soft-hair-assisted evaporation, but not a direct
duplicate of the angular-shell branch.
```

## 5. Gauge Edge Modes On Spherical Boundaries

References:

```text
Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
arXiv:1412.1895.

Mukherjee,
"Entanglement entropy and the boundary action of edge modes",
arXiv:2310.14690.

Ball, Law, Wong,
"Dynamical Edge Modes and Entanglement in Maxwell Theory",
arXiv:2403.14542.
```

Relevance:

```text
Gauge theories require edge sectors at boundaries/entangling surfaces.
These edge sectors can be described by boundary fields or harmonic
decompositions on the sphere.
```

This supports:

```text
soft angular boundary labels can be real degrees of freedom, not arbitrary
bookkeeping.
```

Especially relevant:

```text
Mukherjee decomposes gauge fields in tensor harmonics and identifies
superselection sectors labeled by the normal field component on a spherical
entangling surface.

Ball-Law-Wong identify dynamical edge degrees on a stretched horizon and find a
bulk-edge split of the symplectic form and Hamiltonian.
```

Difference:

```text
These works are about entanglement/edge-mode entropy, not an evaporating
shrinking Hilbert-space model.
```

Assessment:

```text
Good support for the soft-edge-label part. Does not solve evaporation.
```

## 6. Quantum N-Portrait / Critical Soft Modes

References:

```text
Dvali, Gomez, et al.,
"Black Holes as Critical Point of Quantum Phase Transition",
arXiv:1207.4059.

Dvali, Gomez, Lust,
"Classical Limit of Black Hole Quantum N-Portrait and BMS Symmetry",
arXiv:1509.02114.
```

Relevance:

```text
Black holes are modeled as critical condensates with nearly gapless
Bogoliubov/Goldstone modes that carry information.
```

This is relevant to the softness problem:

```text
many information carriers with gaps that shrink with system size.
```

Difference:

```text
The entropy variable is usually the occupation number N of soft gravitons, not
our angular cutoff L with (L+1)^2 labels. It is also explicitly gravitational /
black-hole portrait language.
```

Assessment:

```text
Useful precedent for size-dependent soft gaps, less direct for angular-shell
counting.
```

## What Seems New In Our Branch

The pieces that are known:

```text
angular mode degeneracy can give area scaling;
stretched-horizon/brick-wall modes count area entropy;
horizon soft hair is angular and low-energy;
gauge edge modes live on boundaries and can be harmonic-decomposed;
soft-hair qubit evaporation models exist;
critical soft modes can carry information with small gaps.
```

The combination that still looks distinct:

```text
1. abstract finite Hilbert spaces H_L labeled by angular cutoff L;
2. S_L = (L+1)^2 log d;
3. M_L ~ L, hence T ~ 1/L;
4. evaporation as L -> L-1;
5. hard quantum carries energy ~ T;
6. removed soft shell l=L carries/purifies the entropy loss;
7. use this as a non-gravitational control model for BH-like phenomenology.
```

## Main Risk

This branch may become too close to actual black-hole horizon physics.

If we lean on:

```text
stretched horizons;
soft hair;
edge modes;
spherical boundary geometry;
```

then the model may lose the original "none of gravity" control value.

The way to preserve control value is to phrase it as:

```text
a finite angular-boundary evaporator inspired by edge-mode counting,
not a microscopic black hole model.
```

But the more we justify softness from real soft hair, the less independent of
gravity it becomes.

## Current Judgment

The angular-shell branch is worth pursuing, but with eyes open.

It is not completely novel as a counting idea. The stretched-horizon normal
mode paper is especially close on angular quasi-degeneracy and area entropy.

What may remain interesting is the stripped evaporator use:

```text
turn angular area-counting into a finite shrinking Hilbert-space model with
explicit hard radiation plus soft shell memory.
```

That is the next test.

