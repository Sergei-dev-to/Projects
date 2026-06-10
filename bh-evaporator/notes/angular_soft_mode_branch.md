# Angular Soft-Mode Branch

## Prompt

An earlier abandoned idea was:

```text
excitation modes are like spherical harmonics;
energy differences go down for higher l,m.
```

This note revisits the idea in light of the relational evaporator.

## Immediate Correction

For ordinary fields on a sphere, angular gradients cost energy.

The Laplacian eigenvalues are:

```text
l(l+1)/R^2
```

so higher `l` modes are usually more energetic, not softer.

Therefore this is probably wrong as a model of ordinary propagating
excitations:

```text
higher l,m -> lower energy.
```

But the idea can be useful if the `l,m` modes are not ordinary excitations.

## Better Interpretation

Treat the spherical harmonic labels as:

```text
soft boundary / edge / relation labels
```

rather than ordinary bulk waves.

Then the model becomes:

```text
large object of radius R;
boundary supports angular soft modes Y_lm;
modes are cut off at l_max ~ R / ell_0;
number of angular labels ~ l_max^2 ~ R^2 / ell_0^2;
mass-like scale M ~ R;
entropy-like count S ~ R^2 ~ M^2.
```

That is exactly the relational scaling.

In this reading:

```text
the modes are not soft because high l has low gradient energy;
they are soft because they are edge/label/gauge/near-degenerate sectors.
```

## Count

Number of spherical harmonic modes up to cutoff `L`:

```text
sum_{l=0}^L (2l+1) = (L+1)^2.
```

If:

```text
L ~ R / ell_0,
```

then:

```text
number of modes ~ R^2 / ell_0^2.
```

If:

```text
M ~ R,
```

then:

```text
S ~ number of angular soft labels ~ M^2.
```

Temperature:

```text
T^{-1} = dS/dM ~ M
```

so:

```text
T ~ 1/M.
```

This is the same object/relation logic in boundary language:

```text
linear size/mass counts objects;
angular labels count area-like relations.
```

## Why This May Be Relevant

This branch addresses the soft-connector problem.

Instead of assigning one independent connector qudit to every pair of objects,
we use:

```text
soft angular boundary labels
```

with a natural area count.

Possible advantages:

```text
1. S ~ M^2 comes from a 2D mode count.
2. Softness is less ad hoc if modes are edge/gauge labels.
3. Radiation can be "hard quantum + soft angular memory."
4. It connects to known black-hole soft hair and edge-mode language.
```

Possible disadvantages:

```text
1. It reintroduces geometry: a sphere and angular harmonics.
2. Soft hair / edge modes are gravitational or gauge-theoretic, not generic.
3. Need a physical cutoff L ~ R/ell_0.
4. Need to explain dynamics and evaporation rates.
```

## Literature Connections

### Soft hair

Black-hole soft hair is often described using horizon supertranslation or gauge
parameters expanded in spherical harmonics.

Relevant idea:

```text
soft charges / memory labels can be low-energy or zero-energy while carrying
information.
```

Representative references:

```text
Hawking, Perry, Strominger,
"Soft Hair on Black Holes",
arXiv:1601.00921.

Compere, Long,
"Classical static final state of collapse with supertranslation memory",
and related supertranslation hair work.
```

### Gauge edge modes

Gauge-theory entanglement across a boundary requires edge sectors. These edge
modes can contribute boundary/area entropy.

Representative references:

```text
Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
arXiv:1412.1895.

"Dynamical Edge Modes and Entanglement in Maxwell Theory",
arXiv:2403.14542.
```

### Stretched horizon / angular modes

Brick-wall and stretched-horizon calculations often count near-horizon modes
with angular quantum numbers and a UV cutoff. The area scaling comes from the
number of modes available near the boundary.

This is relevant but dangerous:

```text
ordinary near-horizon field modes are energetic after regularization;
the entropy can be UV-divergent and cutoff-dependent.
```

Our branch should not simply copy brick-wall counting unless the cutoff and
softness are explicit.

## Relation To Connector Model

Connector model:

```text
relations = pairwise links among N objects
count ~ N^2
```

Angular soft-mode model:

```text
relations = boundary angular labels up to L
count ~ L^2
```

If:

```text
N ~ L ~ R,
```

then the two are equivalent at the scaling level:

```text
relation count ~ N^2 ~ R^2.
```

The angular model may be more natural for area scaling.

The connector model may be better for finite Hilbert-space bookkeeping.

## Energy Scaling Options

### Bad option: ordinary angular excitations

If energy grows like:

```text
omega_l ~ sqrt(l(l+1))/R
```

then high-l modes are not soft.

This does not solve the soft-connector problem.

### Viable option: edge-label degeneracy

If angular labels are nearly degenerate sectors:

```text
omega_l ~ 0
```

or small compared with the hard emission energy, then they can carry entropy
without proportional energy.

### Viable option: collective soft gap

If:

```text
omega_l ~ 1/R
```

for many modes, then a single hard quantum can have energy:

```text
epsilon ~ T ~ 1/R
```

while soft labels encode extra information.

But if all emitted soft labels are independently excited, the energy can again
be too large.

## What This Branch Would Try To Build

Minimal abstract model:

```text
radius/mass register: R_N ~ N
angular soft-label Hilbert space: modes (l,m), l <= N
dimension: d^[(N+1)^2]
energy: M_N ~ N + small soft splittings
emission: N -> N-1 plus one hard quantum and soft angular memory
```

This is basically:

```text
area register with a mode basis and a softness interpretation.
```

It is better than a naked area register if we can justify:

```text
1. why the modes are angular/boundary-like;
2. why they are soft/near-degenerate;
3. how their cutoff changes as N shrinks;
4. how the lost modes are purified by radiation/memory.
```

## Current Judgment

The old idea should stay abandoned in its original form:

```text
ordinary higher-l excitations getting lower in energy.
```

But it is worth reviving as:

```text
angular soft/edge labels with an area-law mode count.
```

This may be the cleanest version of the "soft relational entropy" requirement.

It sits between:

```text
connector graph model:
  relation count is explicit but engineered;

soft hair / edge modes:
  softness is motivated but gravitational/gauge-theoretic;

area register:
  scaling works but microscopic interpretation is thin.
```

The next useful diagnostic would compare:

```text
pairwise connector entropy ~ N^2
vs
angular soft-mode entropy ~ (L+1)^2
```

and ask which gives a cleaner radiation/information split.

