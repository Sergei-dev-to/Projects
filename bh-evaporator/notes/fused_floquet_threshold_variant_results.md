# Fused Floquet Threshold Variant Results

## Purpose

Test whether the fused behavior depends on the exact accumulator bookkeeping.

The current rule is:

```text
carry mode:
  if A >= Delta, transfer a shell and set A -> A - Delta.
```

The comparison rule is:

```text
reset mode:
  if A >= Delta, transfer a shell and set A -> 0.
```

Both are simple coarse-grained ways to represent many small hard emissions
triggering one shell-transfer event.

## Setup

Script:

```text
sim/fused_floquet_threshold_variant_scan.py
```

Data:

```text
sim/data/fused_floquet_threshold_variant_rows.csv
sim/data/fused_floquet_threshold_variant_summary.csv
```

Parameters:

```text
L0 = 3
rate L0 = 20
micro emissions = 6
thresholds = 4, 5
modes = carry, reset
seeds = 0, 1
scramblers = margulis, grid, none
hard weights = microcanonical/golden-rule schedule
```

## Result

```text
mode    threshold  soft gap  old/new gap  <shells>  P(done)
carry       4        1.076      2.678      1.781    0.005
carry       5        2.114      0.616      1.188    0
reset       4        1.221      2.522      1.699    0.005
reset       5        2.216      0.488      1.131    0
```

## Interpretation

The fused behavior is not tied to the carry-over accumulator rule.

Both accumulator variants preserve:

```text
scrambling-enhanced soft entropy;
old/new radiation mutual-information enhancement when enough shrinkage occurs;
threshold-dependent tradeoff between soft entropy gap and old/new correlation.
```

The reset rule slightly reduces the transferred shell count and old/new gap,
as expected, because overshoot energy is discarded instead of carried forward.
But it does not remove the fused behavior.

## What This Closes

This narrows the threshold-rule caveat.

Before:

```text
the shrink trigger might be a fragile artifact of one accumulator update.
```

After:

```text
the qualitative result survives two natural threshold update conventions.
```

The threshold rule is still a model ingredient, not derived from an autonomous
Hamiltonian. But it is now stress-tested at the level relevant to the current
Floquet toy-model standard.

