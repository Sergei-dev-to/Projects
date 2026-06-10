# Design Tension: No-Compromise Review

## Purpose

We should not keep modifying the model just to fill table cells.

The original target was:

```text
a non-gravitational quantum system that reproduces the known black-hole
evaporation phenomenology, without claiming to be a microscopic black hole.
```

The desired package is:

```text
1. S ~ M^2;
2. T ~ 1/M;
3. negative heat capacity;
4. shrinking internal Hilbert space;
5. evaporation into radiation;
6. accelerating emitted power;
7. explicit unitary/purifiable radiation;
8. Page-like radiation entropy;
9. early/late radiation structure.
```

The recent work clarified that we can get pieces of this package, but not yet
in one satisfying model.

## What We Have

### Track E

Track E has the strongest thermodynamic backbone.

```text
core = n-spin chain
dim H_n = 2^n
S_n = n log 2
M_n ~ sqrt(n)
emission = H_n -> H_(n-1)
rates from matrix elements and energy gaps
```

Strength:

```text
negative heat capacity;
accelerating power for sqrt mass;
linear-mass controls;
local-vs-scrambled controls;
W diagnostic.
```

Weakness:

```text
radiation is not natural unless we keep large transition records.
```

### Exact Transition-Record Radiation

This purifies Track E exactly.

Radiation label:

```text
(step, n, i, f)
```

Strength:

```text
faithful;
tracing radiation reproduces Track E.
```

Weakness:

```text
huge;
artificial;
not a natural emitted radiation subsystem;
not scalable to Page/early-late diagnostics.
```

### C1 Detached-Qubit Radiation

C1 emits one qubit per step.

Strength:

```text
explicit radiation qubit chain;
Page-like core/radiation entropy;
early/late radiation mutual information.
```

Weakness:

```text
deterministic one-qubit-per-step schedule;
thermodynamics is mostly mass-gap bookkeeping;
radiation structure identical for sqrt and linear mass laws.
```

### C2 Energy-Filtered Detached-Qubit Radiation

C2 attempted to combine detached qubits with energy-filtered rates.

Strength:

```text
probabilistic emission;
explicit radiation bins;
nonzero early/late structure.
```

Weakness:

```text
naive implementation decelerates for both sqrt and linear mass laws;
sqrt/linear distinction weak;
does not recover Track E thermodynamics.
```

## The Core Tension

The problem is not just numerical.

It is structural:

```text
Page/early-late radiation wants small, reusable emitted subsystems:
  qubits, qudits, time bins.

Thermodynamic transition-rate faithfulness wants distinguishable transition
channels:
  enough labels to distinguish which core transition occurred.
```

If the radiation label is too small, distinct transitions interfere or become
coarse-grained in a way that changes the reduced channel.

If the radiation label is fully faithful, the radiation becomes a giant
transition record rather than a natural emitted quantum.

This is the actual design obstruction.

## No-Compromise Standard

We should not accept a model that gets the checklist only by splitting the
burden between unrelated mechanisms.

Not acceptable:

```text
1. C1-style deterministic Page model plus separately assigned mass gaps.
2. Exact transition-record radiation treated as if it were a natural field.
3. Rate tuning that forces acceleration without a clear mechanism.
4. Radiation compression that changes the reduced thermodynamic channel.
5. A model where Page structure is identical across all thermodynamic controls.
```

A good result must have a single coherent evaporation mechanism that produces:

```text
1. shrinking state space;
2. thermodynamic heating / negative heat capacity;
3. accelerating power;
4. explicit radiation degrees of freedom;
5. nontrivial information flow in that radiation.
```

The mechanism may be artificial in the sense of being a toy model, but it
cannot be a glued-together checklist.

## What This Means

Track E and C1 are both useful diagnostics, but neither is the final answer.

Track E says:

```text
Here is how to get the thermodynamic evaporation engine.
```

C1 says:

```text
Here is how to get the radiation-register Page structure.
```

The missing model must explain why these are the same process.

## Consequence For Further Work

Do not run more C2 variants just to see if one works.

Before more numerics, we need a principled one-step process where:

```text
the emitted subsystem is small enough to be radiation-like,
but rich enough to carry the information required by the emission channel.
```

This likely means one of two serious directions:

### Direction 1: Sequential Isometry From The Start

Build a model directly as:

```text
V_n : H_n -> H_(n-1) tensor R_t
```

where `R_t` has fixed modest dimension, and impose thermodynamic constraints at
the level of the isometry.

This abandons exact Track E faithfulness.

The test becomes:

```text
does the isometry itself produce the thermodynamic and information backbone?
```

### Direction 2: Field-Like Radiation Instead Of Qubit Labels

Use a radiation subsystem with genuine mode structure:

```text
energy bins;
occupation states;
possibly bosonic modes;
time bins.
```

Then emission channels can be distinguishable by energy/mode without storing
the full transition `(i,f)`.

This is closer to Hawking radiation, but it is a larger model.

## Current Judgment

The all-phenomenology target is still interesting, but our current spin-chain
Track E plus detached-qubit patches do not yet reach it.

The best honest result so far is:

```text
The thermodynamic backbone and the Page/radiation backbone can each be
reproduced without gravity, but combining them in one faithful finite quantum
model exposes a nontrivial tension between thermodynamic transition
distinguishability and natural small radiation subsystems.
```

That is not a failure. It is a useful design constraint.

## Next Decision

Choose one of:

```text
1. Stop here and treat the result as a design-obstruction note.
2. Start a new model based on a fixed-dimension sequential isometry.
3. Start a new model with field-like radiation modes.
```

Do not continue by incremental patching of C2 unless we can state the new
principle before coding it.
