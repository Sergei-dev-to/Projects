# Global Floquet Hard-Density Results

## Purpose

The global state-vector lift showed that the combined register rule can carry
quantum amplitudes coherently.

This test asks whether the same lifted rule gives a sensible reduced density
matrix for the visible hard radiation record.

The diagnostic factors the output basis as:

```text
visible hard-bin sequence
tensor
hidden records
```

and traces over the hidden records.

## Setup

Same finite global rule as:

```text
notes/global_floquet_register_rule_results.md
notes/global_floquet_statevector_lift_results.md
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

The visible hard record has:

```text
hard dimension = 2^3 = 8
```

The hidden records include:

```text
final L
final accumulator
final shell labels
bath microstate sequence
emitted-unit sequence
shrink records
```

Because the bath has four axis modes and four diagonal modes, the target
coarse hard distribution is uniform over the two hard bins at each emission.
For three emissions, the target hard entropy is:

```text
ln(8) = 2.079441...
```

## Result

```text
input dimension              = 1048576
hard dimension               = 8
hidden dimension             = 1048576

S_hard                       = 2.079437
S_target                     = 2.079442
trace distance to target     = 1.137e-03
offdiag Frobenius norm       = 0.000e+00
purity                       = 0.125001
max probability error        = 8.12e-04
```

The individual hard-sequence probabilities are all close to:

```text
1/8 = 0.125.
```

## Interpretation

This supports hard-local thermality inside the global lifted rule.

The hard radiation record is locally close to the expected coarse thermal
distribution after tracing hidden bath/shrink records.

The zero off-diagonal norm is not a deep thermalization result. It occurs
because the hidden bath microstate sequence remains in the environment and
records which microscopic mode produced the hard bin. Tracing that record
decoheres the visible hard bins.

So the correct interpretation is:

```text
the global state-vector rule gives locally thermal hard radiation,
provided hidden bath records are traced.
```

It is not:

```text
a Page-curve calculation;
an early/late mutual-information calculation;
a scrambling diagnostic.
```

## What This Strengthens

This strengthens the merger between:

```text
F2  purifiable evaporation
F7  bath-density emission
F15 one repeated update rule
```

It also gives a small direct check of:

```text
hard-local thermality
```

inside the global rule.

## Remaining Gap

The next missing piece is not local hard thermality. The next missing piece is:

```text
combine the global state-vector rule with nontrivial core scrambling and
hard+soft radiation records, then compute Page/old-new diagnostics.
```

That is where F8/F9 and F14 must meet F15.

## Files

Script:

```text
sim/global_floquet_hard_density.py
```

Data:

```text
sim/data/global_floquet_hard_density_rows.csv
sim/data/global_floquet_hard_density_summary.csv
```
