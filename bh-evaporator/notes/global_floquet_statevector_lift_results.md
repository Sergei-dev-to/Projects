# Global Floquet State-Vector Lift Results

## Purpose

The previous global-register test showed that the combined bath/emission/
shrinkage rule is injective on computational-basis records.

This test asks the next question:

```text
Can that register rule be promoted to a quantum state-vector map?
```

The answer, for this finite diagnostic, is yes: the injective register rule
lifts to an isometry on arbitrary complex amplitudes over the enumerated input
basis.

## Setup

Same register rule as:

```text
notes/global_floquet_register_rule_results.md
```

Parameters:

```text
L0 = 3
q = 2
shell_gap = 8
accumulator modulus = 8
sequence length = 3
2D-box bath modes with max momentum = 1
```

The input basis includes:

```text
accumulator state
shell labels
bath microstate sequence
```

The output basis includes:

```text
final L
final accumulator
final shell labels
bath microstate sequence
hard-bin sequence
emitted-unit sequence
shrink records
```

A random normalized complex state is sampled over all input basis states and
mapped through the finite-register rule.

## Result

```text
input dimension       = 1048576
output dimension      = 1048576
full map injective    = True
norm error            = 0.0
inverse fidelity      = 0.9999999999999989

hard visible rank     = 8
hard visible entropy  = 2.079438
hard visible purity   = 0.125001

no-bath collisions    = 1032192
no-shrink collisions  = 571392
```

The hard visible entropy is essentially:

```text
ln(8) = 2.079441...
```

which is expected because the visible hard record consists of three emissions,
each with two coarse hard bins.

## Interpretation

This is a useful upgrade over pure register injectivity.

The map does not merely preserve labels. It preserves arbitrary amplitudes on
the finite basis:

```text
|psi_in> -> |psi_out>
```

with exact norm preservation and exact reconstruction on the image.

The erasure checks again show why the hidden records matter. If the bath
microstate or shrink record is omitted, many distinct input amplitudes collapse
onto the same coarse record. A unitary model cannot do that. Those records must
remain somewhere in the full radiation/environment state.

## What This Strengthens

This strengthens:

```text
F2  unitary or purifiable evaporation
F3  shrinking internal state space
F15 autonomy / one repeated update rule
```

The correct statement is now:

```text
the combined bath/emission/shrinkage register rule has an explicit
state-vector isometric lift at finite size.
```

## What This Still Does Not Do

This is not yet:

```text
a time-independent Hamiltonian;
a dynamically derived shrink trigger;
a scrambling simulation;
a full hard/soft density-matrix evaporation history;
a proof of large-L behavior.
```

It is a finite isometry diagnostic. Its value is that it removes one possible
failure mode:

```text
the global rule is not merely classically reversible; it can carry quantum
amplitudes coherently.
```

## Files

Script:

```text
sim/global_floquet_statevector_lift.py
```

Data:

```text
sim/data/global_floquet_statevector_lift_summary.csv
```
