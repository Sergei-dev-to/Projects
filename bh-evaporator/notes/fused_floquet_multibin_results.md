# Fused Floquet Multi-Bin Hard Spectrum Results

## Purpose

Test whether the fused model depends on the two-bin hard-radiation alphabet.

The review concern was:

```text
hard radiation is locally thermal, but the exact fused diagnostics use a very
compact two-bin hard register.
```

This scan replaces the two-bin hard channel with `d_hard = 3` and `d_hard = 4`
hard bins, using the same microcanonical/golden-rule weighting rule.

## Setup

Script:

```text
sim/fused_floquet_multibin_scan.py
```

Data:

```text
sim/data/fused_floquet_multibin_rows.csv
sim/data/fused_floquet_multibin_summary.csv
```

Parameters:

```text
L0 = 3
rate L0 = 20
threshold = 5
micro emissions = 4
d_hard = 2, 3, 4
seeds = 0, 1
scramblers = margulis, grid, none
```

The run uses only four emissions to keep the exact multi-bin state-vector
calculation manageable.

## Result

```text
d_hard  soft gap  old/new gap  hard error  <shells>  max terms
2         0.766      0.000      2.2e-16     0.076       8192
3         1.678      0.003      8.9e-16     0.110      41472
4         2.099      0.067      4.4e-16     0.087     131072
```

## Interpretation

The hard-local thermality check survives the larger alphabet:

```text
hard entropy error is numerical zero for d_hard = 2, 3, 4.
```

The soft entropy gap also survives and grows with a richer hard channel:

```text
soft gap:
  0.766 -> 1.678 -> 2.099.
```

This means the hard/soft information split is not an artifact of the two-bin
hard alphabet.

The old/new mutual-information gap is weak in this scan because the four-step
trajectory transfers little shell information:

```text
<shells> ~ 0.08 to 0.11.
```

That is a trajectory-length limitation, not a failure of the hard spectrum
test.

## What This Closes

This reduces the hard-alphabet caveat:

```text
the fused hard-thermality and soft-information diagnostics persist for
three- and four-bin hard spectra.
```

## Remaining Limits

```text
short four-emission trajectory;
exact L0 = 3;
two seeds;
old/new correlations not tested strongly in this short run.
```

