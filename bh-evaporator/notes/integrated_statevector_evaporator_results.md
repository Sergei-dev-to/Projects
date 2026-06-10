# Integrated State-Vector Evaporator Results

## Purpose

This is the first diagnostic that puts the main information-theoretic pieces
into one pure state-vector simulation:

```text
scrambling core;
soft shell radiation records;
visible hard bins;
hidden bath records.
```

The purpose is to test whether the hard/soft entropy accounting survives when
all these records live in one state, rather than in separate diagnostics.

## Setup

Small system:

```text
L0 = 3
initial core qubits = 9
cycles: L=3->2, 2->1, 1->0
```

Scramblers:

```text
margulis
grid
none
```

Three seeds were run for each.

Each cycle:

```text
1. scramble active core qubits;
2. mark the outgoing shell as soft radiation;
3. append one visible hard bin;
4. append one hidden bath purifier for that hard bin.
```

The hard/bath pair is the minimal coarse version:

```text
(|0>_hard |0>_bath + |1>_hard |1>_bath) / sqrt(2).
```

So the visible hard bin is exactly locally thermal:

```text
rho_hard = I/2.
```

This is smaller than the eight-mode 2D-box bath used in the global-register
tests, but it tests the same hard-visible/hidden-bath split at state-vector
level.

## Summary Results

Scrambled cases:

```text
scrambler   seed  soft Page deficit  peak soft S  final soft S  hard S  first soft MI
margulis      0        0.290             2.487        0.000      2.079      2->1
margulis      1        0.291             2.484        0.000      2.079      2->1
margulis      2        0.337             2.448        0.000      2.079      2->1
grid          0        0.286             2.491        0.000      2.079      2->1
grid          1        0.333             2.445        0.000      2.079      2->1
grid          2        0.314             2.471        0.000      2.079      2->1
```

No-scrambling control:

```text
scrambler   seed  soft Page deficit  peak soft S  final soft S  hard S  first soft MI
none          0        3.466             0.000        0.000      2.079      none
none          1        3.466             0.000        0.000      2.079      none
none          2        3.466             0.000        0.000      2.079      none
```

The final state-vector dimension is:

```text
32768.
```

The maximum trace distance of the latest hard bin from `I/2` is numerical
roundoff:

```text
max D_hard ~ 10^-15.
```

## Representative Trajectory

For `margulis`, seed 0:

```text
L  page cap  S_soft  S_full_rad  S_visible_rad  S_hard  old/new soft MI
3   2.773    2.487     2.487        3.180       0.693       0.000
2   0.693    0.689     0.689        2.075       1.386       3.810
1   0.000    0.000     0.000        2.079       2.079       1.377
```

Here:

```text
S_soft:
  fine entropy of the emitted soft shell records.

S_full_rad:
  entropy of soft + hard + hidden bath records.

S_visible_rad:
  entropy of soft + visible hard records, with hidden bath traced.

S_hard:
  entropy of visible hard bins only.
```

The key relation is:

```text
S_full_rad ~= S_soft
```

because the hard+hidden-bath pairs are pure when included together.

But:

```text
S_visible_rad ~= S_soft + S_hard
```

because tracing hidden bath records makes the hard bins locally thermal.

## Interpretation

This is the first one-state confirmation of the hard/soft split:

```text
soft shell records:
  carry fine-grained Page-like radiation entropy;
  require scrambling;
  turn over and return to zero.

hard bins:
  are locally thermal;
  contribute coarse visible entropy;
  remain monotone.

hidden bath records:
  purify the hard bins.
```

The no-scrambling control is important:

```text
hard bins are still thermal,
but the soft Page diagnostic fails.
```

So local hard thermality alone does not create the Page curve. The Page behavior
comes from scrambled core information entering the soft shell records.

## What This Strengthens

This strengthens the joint F8/F9/F15 claim:

```text
F8:
  Page-like soft radiation entropy appears in the same state-vector model that
  contains hard and bath records.

F9:
  old/new soft mutual information turns on in the scrambled cases.

F15:
  the hard/soft/bath record structure can be represented in one pure
  state-vector evolution.
```

It also strengthens the distinction:

```text
hard thermality is not the Page curve.
```

## Caveats

This is still a small diagnostic.

Limitations:

```text
L0 = 3 only;
one shell emission per cycle;
minimal two-mode hidden bath, not the full eight-mode 2D-box bath;
no microscopic emitted-energy accumulator;
no threshold-triggered shrinkage inside this state-vector run;
scrambling is still a modular pre-emission operation.
```

So this is not the final autonomous evaporator.

The correct claim is:

```text
the integrated hard/soft/bath information accounting works in one explicit
small state-vector simulation.
```

## Files

Script:

```text
sim/integrated_statevector_evaporator.py
```

Data:

```text
sim/data/integrated_statevector_evaporator_summary.csv
sim/data/integrated_statevector_evaporator_margulis_seed0.csv
sim/data/integrated_statevector_evaporator_margulis_seed1.csv
sim/data/integrated_statevector_evaporator_margulis_seed2.csv
sim/data/integrated_statevector_evaporator_grid_seed0.csv
sim/data/integrated_statevector_evaporator_grid_seed1.csv
sim/data/integrated_statevector_evaporator_grid_seed2.csv
sim/data/integrated_statevector_evaporator_none_seed0.csv
sim/data/integrated_statevector_evaporator_none_seed1.csv
sim/data/integrated_statevector_evaporator_none_seed2.csv
```
