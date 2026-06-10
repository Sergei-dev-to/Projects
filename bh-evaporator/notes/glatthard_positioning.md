# Glatthard Positioning

## Papers checked

### 2024

```text
Jonas Glatthard,
"Page-curve-like entanglement dynamics in open quantum systems",
arXiv:2401.06042, Phys. Rev. D 109, L081901 (2024).
```

Core point:

```text
Page-curve-like entropy dynamics should occur generally in weakly coupled,
low-temperature system-plus-bath models when the system starts pure and far
from equilibrium.
```

Mechanism:

```text
interaction with bath generates entanglement entropy
eventual relaxation toward a near-ground-state mean-force Gibbs state lowers it
```

Examples:

```text
harmonic quantum Brownian motion
spin-boson model
```

Notable result:

```text
for an initially excited impurity, Page time occurs when the excitation has
half decayed.
```

### 2025

```text
Jonas Glatthard,
"Thermodynamics of the Page curve in Markovian open quantum systems",
arXiv:2501.09082.
```

Core point:

```text
Page-like subsystem entropy decrease can be studied in Lindbladian/Markovian
open quantum systems.
```

Thermodynamic interpretation:

```text
entropy decrease is linked to Landauer's principle and must be accompanied by
heat flow out of the system.
```

Examples:

```text
decaying two-level excitation
localized oscillator equilibration
```

Notable result:

```text
in both examples, Page time occurs when half the initial energy has left.
```

## Impact on our project

Glatthard makes the "Page curve without gravity" point quite directly.

Therefore our paper should not be framed as:

```text
we show Page-like dynamics can occur outside gravity
```

That is already done more generally and cleanly in open quantum systems.

Our possible differentiator is:

```text
we combine Page-like unitary information flow with a negative-heat-capacity
evaporation engine.
```

Specifically, Glatthard's systems are ordinary cooling/relaxing systems:

```text
excited system weakly coupled to cold reservoir
energy leaves
entropy rises then falls
Page time near half energy loss
```

Our target is black-hole-like evaporative thermodynamics:

```text
system loses energy but gets hotter
emission accelerates
microcanonical C_mu < 0 from convex entropy
P(E) can scale like E^{-2}
```

So the paper must emphasize:

```text
Page-like entanglement dynamics is not the novelty.
The novelty, if any, is coupling it to a negative-C_mu thermodynamic engine.
```

## Consequence for Step 2

Glatthard also lowers the value of a generic collision/Page model.

Step 2 is interesting only if the collision model contains the negative-heat
capacity schedule dynamically:

```text
emission rates depend on the core density of states / microcanonical slope
the effective temperature rises as energy decreases
the Page-like entropy curve is correlated with accelerated evaporation
```

A plain excited-system collision model would be too close to Glatthard.

## How to cite/position

Suggested text:

```text
Recent work by Glatthard shows that Page-curve-like entropy dynamics is
expected quite generally in weakly coupled open quantum systems relaxing
toward low-temperature states, and relates the entropy decrease to ordinary
thermodynamic heat flow. Our construction targets a complementary regime:
a finite evaporating core with negative microcanonical heat capacity, so that
the system heats up rather than cools as it loses energy. The aim is therefore
not to obtain a Page-like curve in isolation, but to bind Page-like information
flow to black-hole-like evaporative thermodynamics.
```

## Current assessment

Glatthard makes our project more constrained but not dead.

The viable niche is:

```text
Page-like dynamics + negative heat capacity + accelerating evaporation
```

not:

```text
Page-like dynamics in non-gravitational systems
```

## Update after broader prior-art check

I did not find a paper that already builds the exact object we now seem to
need:

```text
an explicit non-gravitational unitary evaporator whose emission schedule is
driven by a negative microcanonical heat-capacity window, and whose radiation
entropy is computed from the emitted quantum degrees of freedom.
```

The surrounding literature covers the pieces separately:

```text
Glatthard:
  Page-like open-system thermodynamics without gravity.

Hotta-Sugita:
  black-hole negative heat capacity matters for Page-typicality reasoning.

Finite-system thermodynamics:
  convex intruders and negative heat capacity in microcanonical systems.

Many-body / random / open-system Page-curve models:
  Page-like entanglement dynamics in non-gravitational quantum systems.
```

So the remaining possible contribution is not conceptual slogan, but a specific
construction:

```text
negative-C_mu thermodynamic engine
plus
unitary time-bin radiation dynamics
plus
computed Page-like entropy / distinguishability diagnostics.
```

This is the point at which the project either becomes technically interesting
or should be put aside.

## Decision

Proceed, but only to the minimum dynamic test.

The next stage should not be a broad rewrite or more positioning work. It
should be a small simulation that answers one question:

```text
Can the same shell model generate both the black-hole-like evaporation schedule
and the Page-like radiation entropy curve?
```

If yes, the project has a defensible niche:

```text
a geometry-free negative-heat-capacity quantum evaporator as a control model
for black-hole evaporation phenomenology.
```

If no, or if the Page curve has to be imposed independently of the evaporation
schedule, then the paper loses its main differentiator and should probably stay
as notes.
