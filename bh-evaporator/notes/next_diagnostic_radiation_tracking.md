# Next Diagnostic: Minimal Radiation Tracking

## Purpose

The current models already show:

```text
decreasing energy
shrinking internal Hilbert space
negative-heat-capacity thermodynamics
accelerating emission
growth of core-radiation Renyi-2 entropy
```

But the radiation has only been tracked in a reduced or transition-labelled
way. We know that the core becomes mixed, so a purification would assign the
same Renyi-2 entropy to all emitted radiation together. We do not yet know how
the radiation is organized internally.

The next diagnostic should answer:

```text
Does the toy evaporator produce nontrivial correlations between early and late
radiation, or only core-radiation entropy growth?
```

This matters because the black-hole information puzzle is not just about
whether the remaining object becomes entangled with radiation. That part is
generic. The sharper issue is how information is distributed among early
radiation, late radiation, and the shrinking interior.

## Why this is the right next test

The project has reached a useful split:

```text
Track A: variable-N Bose-Hubbard
  natural particle-loss dynamics
  wrong black-hole entropy scaling

Track B: area register
  correct S ~ M^2 scaling
  abstract microscopic origin
```

Both tracks now pass the same basic reduced-density test:

```text
acceleration survives;
core-radiation S2 grows;
the accessible internal dimension shrinks.
```

The remaining question is whether the radiation channel has any information
structure beyond that.

## Minimal setup

Start with Track B, not Track A.

Reason:

```text
Track B has much smaller sector structure and the correct entropy law.
```

Use a deliberately tiny area register:

```text
n = 3,...,7
q = 2
H_n = n qubits
M_n = alpha sqrt(n)
```

Use the existing shrinkage maps:

```text
local removal
scrambled removal
```

but now keep explicit radiation bins for a short run:

```text
core C
early radiation R_E
late radiation R_L
```

Each emission appends a small radiation label. The label does not need to be a
real field mode at first. It only has to record enough information to purify
the Kraus transition:

```text
no emission
emission energy bin
transition label, or compressed transition label
```

Then compute:

```text
S2(C)
S2(R_E)
S2(R_L)
S2(R_E union R_L)
I2(R_E : R_L)
```

The central new diagnostic is early-late mutual information.

## What would count as success

A useful positive result would be:

```text
1. emitted power still accelerates;
2. core dimension still shrinks;
3. S2(C) grows initially;
4. early-late radiation correlations become nonzero;
5. the result differs between local and scrambled shrinkage, or between
   square-root and linear mass laws.
```

The last point is important. If every version gives the same early-late
structure, then the diagnostic is probably too coarse.

## What would count as failure

The test would still be informative if it fails.

Possible failures:

```text
1. Full radiation tracking is too expensive even at tiny n.
2. Early-late mutual information is numerically zero.
3. The result is dominated by the arbitrary transition-label choice.
4. Local and scrambled shrinkage remain indistinguishable.
5. The square-root and linear mass laws differ only in power, not in
   information structure.
```

Failure modes 2-5 would mean that our current models reproduce thermodynamic
evaporation more strongly than information-theoretic evaporation.

That would sharpen the paper rather than kill it:

```text
black-hole-like thermodynamics is easy to reproduce without gravity;
black-hole-like radiation structure is the harder target.
```

## Avoid overinterpreting the test

This diagnostic will not produce a real Page curve unless the model is large
enough and the evaporation nearly completes.

It also will not test islands, replica wormholes, or gravitational encoding.

The correct interpretation is narrower:

```text
we are checking whether the finite evaporator has any internal radiation
correlation structure beyond total core-radiation entanglement.
```

## Recommended next implementation

Build one script:

```text
sim/area_register_full_radiation_tiny.py
```

with:

```text
small n range
few time steps
two mass laws: sqrt and linear
two shrinkage maps: local and scrambled
one fixed seed pair
```

Outputs:

```text
sim/data/area_register_full_radiation_tiny_*.npz
track_b_full_radiation_tiny.pdf
```

The plot should show:

```text
mean emitted power
mean area n
S2(core)
S2(early radiation)
S2(late radiation)
I2(early : late)
```

## Current verdict

This is the right next diagnostic before broadening scans.

It is small enough to fail cheaply, and it tests the main remaining weakness in
the current evidence:

```text
we have thermodynamic evaporation;
we do not yet have radiation-structure evaporation.
```

## First result

The tiny exact diagnostic has now been run.

Result note:

```text
notes/track_b_full_radiation_tiny_results.md
```

Short verdict:

```text
explicit early/late radiation tracking is feasible at n=3,...,5;
the tiny model shows nonzero early/late Renyi-2 structure;
the signal is not discriminating across sqrt/linear or local/scrambled cases;
the tiny model loses the acceleration seen in the larger reduced Kraus run.
```

So this is not yet a positive radiation-structure result. It is a useful
failure mode.
