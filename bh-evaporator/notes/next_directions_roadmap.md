# Next Directions Roadmap

## Current State

The project now has a coherent candidate:

```text
edge-tension finite-gauge droplet
+ algebraic-expander interacting-spin scrambling
+ finite bath-density emission
+ reversible shrinkage automaton
+ stitched repeated-interaction evaporator.
```

The central remaining question is not:

```text
Can the ingredients work?
```

The evidence says mostly yes.

The central remaining question is:

```text
Can the ingredients be organized into a sufficiently natural model?
```

## Direction 1: Clean Model Specification

Goal:

```text
define the candidate model precisely enough that it is auditable.
```

Needed:

```text
state spaces;
registers;
one-cycle update;
parameters;
observable diagnostics;
claim status: analytical / numerical / assumption.
```

Value:

```text
high
```

Difficulty:

```text
low-medium
```

Risk:

```text
low
```

Status:

```text
done in notes/candidate_model_specification.md
```

## Direction 2: Strengthen F15 Autonomy

Goal:

```text
make the stitched repeated-interaction model less modular.
```

Needed:

```text
embed finite bath-density emission into the stitched simulator;
make U_bookkeep explicitly reversible in the simulator;
replace threshold prose with clock/accumulator registers;
possibly build one global Floquet update.
```

Value:

```text
high
```

Difficulty:

```text
medium
```

Risk:

```text
medium
```

This is the main technical continuation.

## Direction 3: Strengthen F14 Scaling

Goal:

```text
support fast scrambling beyond tiny exact Hamiltonian tests.
```

Needed:

```text
better OTOC sampling;
operator spreading with Clifford/Pauli approximations at larger L;
grid vs Margulis vs complete scaling;
possibly tensor-network approximations.
```

Value:

```text
high
```

Difficulty:

```text
medium-high
```

Risk:

```text
medium-high
```

This matters if we want a strong black-hole-like claim.

## Direction 4: Derive Bath Density More Naturally

Goal:

```text
make U_emit less engineered.
```

Needed:

```text
construct a finite 2D oscillator/edge-mode bath;
bin its spectrum;
show the bath density gives omega^(d-1);
combine it with exp[S(M - omega) - S(M)].
```

Value:

```text
medium-high
```

Difficulty:

```text
medium
```

Risk:

```text
medium
```

This targets the remaining U_emit naturalness issue.

## Direction 5: Literature Positioning

Goal:

```text
compare the concrete candidate against existing non-gravitational evaporator
and black-hole-toy-model literature.
```

Needed comparisons:

```text
SYK evaporators;
Page toy models;
moving mirror / analog gravity;
open-system Page curves;
finite quantum automata/channels;
fast scrambling on expanders.
```

Value:

```text
high
```

Difficulty:

```text
medium
```

Risk:

```text
low
```

Best done after the clean model specification.

## Recommended Order

```text
1. Clean model specification.
2. Strengthen F15 autonomy.
3. Literature positioning against the precise model.
4. F14 scaling and bath-density derivations as targeted follow-ups.
```

Reason:

```text
we need a clear object before more tests or literature comparison.
```
