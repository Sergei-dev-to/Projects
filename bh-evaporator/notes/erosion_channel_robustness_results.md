# Erosion Channel Robustness Results

## Purpose

Stress-test the current Level 2 minimal-soft erosion channel for the F8/F9
questions:

```text
F8: radiation entropy / Page-like behavior
F9: early/late radiation correlations
```

The question is whether the first positive result was seed-specific or robust.

## Script

```text
sim/scan_erosion_channel_robustness.py
```

Outputs:

```text
sim/data/erosion_channel_robustness.csv
sim/data/erosion_channel_robustness_summary.csv
```

The scan uses the Level 2 minimal-soft channel:

```text
V |psi> = sum_h sqrt(p_h) |h>_hard U_h |psi>_soft,
dim H_soft = dim H_shell.
```

So the soft record is not enlarged by a hard-label archive.

## Scan

Command:

```text
python sim/scan_erosion_channel_robustness.py --seeds 8
```

Configurations:

```text
L0 = 3, d_hard = 2,3,4
L0 = 4, d_hard = 2
q = 2
8 seeds each
```

`L0 = 4, d_hard > 2` is expensive for exact dense state-vector/SVD
diagnostics, so it is not included in the default scan.

## Summary

```text
L0 d_h n  maxD(mean)  I_hh(mean)  I_pair(mean)  S_hard_latest/thermal
 3   2  8     0.0411      0.0007       3.8559   0.5779/0.5822
 3   3  8     0.0601      0.0020       3.8559   0.8206/0.8324
 3   4  8     0.0639      0.0035       3.8559   0.9343/0.9475
 4   2  8     0.0498      0.0000       2.6791   0.5751/0.5822
```

Definitions:

```text
maxD:
  maximum trace distance, over erosion steps, between latest hard bin and
  target thermal marginal.

I_hh:
  final mutual information between first and latest hard bins.

I_pair:
  final mutual information between first and latest hard+soft emitted pairs.
```

## Interpretation

The pattern is robust in these small exact simulations:

```text
1. hard-only early/late mutual information is near zero;
2. hard+soft early/late mutual information is clearly nonzero;
3. latest hard bins remain close to the target thermal marginal;
4. minimal-soft capacity is enough; no oversized archive is needed.
```

So the hard/soft distinction is doing real information-flow work:

```text
hard radiation:
  thermal-looking and almost uncorrelated across early/late bins;

hard+soft radiation:
  carries the correlations needed for purification.
```

## What This Improves

This makes F8/F9 more credible.

Before:

```text
F8 = P, F9 = P but based on one small run.
```

After:

```text
F8 = P with robust hard/soft entropy bookkeeping in exact channel runs.
F9 = P with robust early/late hard+soft correlations and nearzero hard-only
     early/late correlations.
```

It still does not justify `Y`, because:

```text
1. the channel is random-unitary, not boundary-local;
2. Page turnover has not been studied at large enough size;
3. hard thermality is still chosen through p_h, not derived from a bath
   Hamiltonian.
```

## Current Status

The Level 2 erosion channel is no longer just a one-off plausibility argument.

It is a robust small-system diagnostic:

```text
minimal soft record + random shell scrambling
is enough to produce thermal-looking hard radiation while preserving
early/late information in hard+soft correlations.
```

The next step is not another random-channel scan.

The next step is:

```text
replace random U_h with structured boundary-local gauge/plaquette moves.
```

