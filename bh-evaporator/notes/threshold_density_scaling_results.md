# Threshold Density Scaling Results

## Purpose

This run collapses the next three planned steps into one diagnostic:

```text
1. full reduced-density threshold test;
2. scrambling controls;
3. scale one parameter: number of microscopic emissions.
```

It directly asks whether the thresholded accumulator model can still support
the hard/soft entropy split when full reduced-density entropies are computed,
not only record entropies.

## Setup

Small thresholded state-vector model:

```text
L0 = 3
threshold = 4 emitted-energy units
warmup_time = 8
dt = 0.2
```

Microscopic emission counts:

```text
4, 5, 6
```

Scrambling controls:

```text
margulis
grid
none
```

Seeds:

```text
0, 1
```

The largest case has:

```text
32768 branch terms.
```

Unlike the previous threshold diagnostic, this computes exact reduced-density
entropies by grouping the sparse state and using the smaller side of each
bipartition.

## Main Result

Hard radiation remains exactly locally thermal:

```text
emissions  S_hard target  max hard entropy error
4          4 ln 2         ~1e-15
5          5 ln 2         ~2e-15
6          6 ln 2         ~1e-15
```

Scrambled soft entropy is much larger than no-scrambling soft entropy:

```text
emissions  margulis S_soft     grid S_soft        none S_soft
4          2.612, 2.580       2.580, 2.557       0.234, 0.234
5          2.282, 2.265       2.265, 2.249       0.693, 0.693
6          1.297, 1.293       1.293, 1.284       0.424, 0.424
```

The scrambled-minus-none soft-entropy gap persists through the scale sweep:

```text
emissions  gap range
4          ~2.32-2.38
5          ~1.56-1.59
6          ~0.86-0.87
```

The thresholded shrinkage statistics evolve as expected:

```text
emissions  mean transferred shells  P(done)
4          1.0625                   0
5          1.5000                   0
6          1.90625                  0.015625
```

## Interpretation

This is the strongest integrated quantum diagnostic so far.

It has, in one full reduced-density calculation:

```text
microscopic hard emissions;
hidden bath purifiers;
energy accumulation;
threshold-triggered shell transfer;
scrambling controls;
hard-local thermality;
soft-record information sensitivity to scrambling.
```

The no-scrambling control is again important:

```text
hard radiation stays thermal even without scrambling;
soft radiation entropy does not.
```

So the model keeps the intended distinction:

```text
hard thermality:
  local bath/purifier effect.

soft Page-like information:
  requires scrambled core information entering shell records.
```

## What This Achieves

This gets through the planned sequence:

```text
Step 2:
  smallest full-density threshold test.

Step 3:
  scrambling controls: margulis, grid, none.

Step 4:
  emission-count scaling: 4 -> 5 -> 6 emissions.
```

The expensive version was feasible up to 32768 branch terms.

## What It Does Not Yet Show

This is still not a large Page curve.

Limitations:

```text
L0 = 3 only;
only up to 6 microscopic emissions in the full-density sweep;
hard energies are fair 1/2 branches, not full 2D-box weights;
scrambling occurs before emission, not branch-dependently after each shrink;
the soft entropy begins turning down as completion branches appear, but this is
not a clean multi-cycle Page curve.
```

The correct claim is:

```text
the full reduced-density thresholded model survives the first scaling and
control tests.
```

## Strategic Meaning

The remaining gap is now narrower.

We no longer need to ask:

```text
Can threshold shrinkage and full density-matrix diagnostics coexist?
```

They can, at small size.

The next question is:

```text
Can we turn this into a cleaner Page-curve threshold run, probably by choosing
emission/threshold parameters that produce a longer controlled trajectory
before complete evaporation dominates?
```

## Files

Script:

```text
sim/threshold_density_scaling.py
```

Data:

```text
sim/data/threshold_density_scaling_rows.csv
sim/data/threshold_density_scaling_summary.csv
```
