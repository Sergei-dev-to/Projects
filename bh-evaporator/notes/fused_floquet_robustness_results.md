# Fused Floquet Robustness Results

## Purpose

Stress-test the fused Floquet diagnostic across threshold choices and seeds.

This addresses two review gaps:

```text
small one-seed fused diagnostic;
threshold-triggered shrinkage chosen too narrowly.
```

## Setup

Script:

```text
sim/fused_floquet_robustness_scan.py
```

Data:

```text
sim/data/fused_floquet_robustness_rows.csv
sim/data/fused_floquet_robustness_scan_summary.csv
sim/data/fused_floquet_robustness_by_threshold.csv
```

Parameters:

```text
L0 = 3
rate L0 = 20
micro emissions = 6
thresholds = 4, 5, 6
seeds = 0, 1
scramblers = margulis, grid, none
hard weights = microcanonical/golden-rule schedule
```

## Result

Summary by threshold:

```text
threshold  soft gap  old/new gap  hard error  <shells>  P(done)
4            1.076      2.678      0          1.781     0.005
5            2.114      0.616      0          1.188     0
6            2.438      0.022      0          1.005     0
```

Here:

```text
soft gap =
  mean scrambled S_soft minus no-scrambling S_soft;

old/new gap =
  mean scrambled I(old:new full radiation) minus no-scrambling value;

<shells> =
  mean transferred shell count in the scrambled cases.
```

## Interpretation

The fused behavior is not a one-threshold accident.

All thresholds tested preserve:

```text
exact hard entropy relative to the golden-rule hard schedule;
nonzero threshold-triggered shrinkage;
larger soft radiation entropy with scrambling than without scrambling.
```

The threshold controls which part of the information-flow behavior is most
visible:

```text
threshold = 4:
  more shell transfer, strongest old/new radiation correlation gap;

threshold = 5:
  balanced case, nontrivial soft gap and old/new gap;

threshold = 6:
  weakest shrinkage, strongest soft entropy gap, almost no old/new enhancement.
```

This is physically reasonable for the toy model. If the threshold is too high,
the run has not yet transferred enough shell information to build strong
late/early correlations. If the threshold is lower, more shrinkage occurs and
old/new correlations become easier to see.

## What This Closes

This improves the status of:

```text
model robustness:
  no longer a single threshold and single seed;

shrink-trigger stress test:
  threshold choices change the balance of diagnostics but do not destroy the
  fused behavior;

scrambling comparison:
  the soft entropy gap persists across all thresholds tested.
```

## Remaining Limits

This is still a small exact diagnostic:

```text
L0 = 3;
two seeds;
six microscopic emissions;
two-bin hard alphabet;
rate L0 separated from exact register L0;
driven/stroboscopic cycle.
```

The result should be read as a finite robustness check, not an asymptotic
claim.

