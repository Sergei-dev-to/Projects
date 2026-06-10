# Global Floquet Reference-Flow Results

## Purpose

The global hard-density diagnostic checked local hard thermality.

This test asks a different question:

```text
Where does information about the evaporated shell go?
```

The diagnostic entangles a reference system with the initial shell label, runs
the global finite-register rule, and measures mutual information between the
reference and:

```text
hard radiation;
soft/shrink record;
hard+soft radiation;
remaining core.
```

## Setup

This is a deliberately tiny information-flow test:

```text
L0 = 2
q = 2
reference dimension = dim Shell_2 = q^3 = 8
shell_gap = 4
sequence length = 3
2D-box bath modes = 8
```

The initial state is:

```text
sum_s |s>_ref |s>_shell
```

with a uniform bath-sequence superposition.

The threshold is lowered to `shell_gap = 4` so shrinkage occurs in most, but
not all, branches. This makes the diagnostic easy to interpret:

```text
shrink branches:
  shell label should move to soft/shrink record.

no-shrink branches:
  shell label should remain in the core.
```

The hard record is only the coarse hard-bin sequence.

## Result

```text
basis terms                 = 4096
shrink probability           = 0.875
S_ref                        = 2.079442

I(ref : hard)                = 0.000000
I(ref : soft)                = 3.639023
I(ref : hard+soft radiation) = 3.639023
I(ref : core)                = 0.519860
I(hard : soft)               = 0.376770
```

The numbers have a simple interpretation.

The reference entropy is:

```text
S_ref = ln(8).
```

For a perfectly entangled reference/record pair, the quantum mutual
information would be:

```text
2 ln(8) = 4.158883...
```

Since shrinkage occurs with probability `7/8`, most of that reference
information is transferred into the soft/shrink record:

```text
I(ref : soft) ~= 3.639.
```

The no-shrink branch has probability `1/8`, and the remaining reference
information stays in the core:

```text
I(ref : core) ~= 0.520.
```

## Interpretation

This is the first global-rule diagnostic that checks information location.

It supports the intended split:

```text
hard radiation:
  locally thermal coarse emission record;
  carries no shell-label reference information in this test.

soft/shrink radiation:
  carries the expelled shell information when shrinkage occurs.

core:
  retains shell information on branches where shrinkage has not occurred.
```

This is exactly the separation the model needs if hard radiation is to look
thermal locally while the full radiation record remains purifying.

## What This Strengthens

This strengthens:

```text
F2  purifiable evaporation
F3  shrinking internal state space
F8  radiation entropy / information bookkeeping
F9  nontrivial radiation correlations, in a minimal reference-flow sense
F15 one repeated update rule
```

It does not by itself prove a Page curve.

## What This Does Not Yet Do

This is not:

```text
a many-cycle Page curve;
an old/new radiation mutual-information calculation;
a fast-scrambling diagnostic;
a natural Hamiltonian derivation.
```

It is a targeted sanity check:

```text
the global update can keep hard radiation locally thermal while moving
evaporated-shell information into soft/shrink records.
```

The next missing step is to combine this reference-flow structure with
nontrivial scrambling and many-cycle Page diagnostics.

## Files

Script:

```text
sim/global_floquet_reference_flow.py
```

Data:

```text
sim/data/global_floquet_reference_flow_summary.csv
```
