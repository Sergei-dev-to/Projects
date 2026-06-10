# Fused Floquet Rate-Scale Results

## Purpose

Test whether the fused diagnostic depends sensitively on the separation between:

```text
exact register size:
  L0 = 3;

rate-generation scale:
  rate L0 used in the microcanonical golden-rule hard weights.
```

This targets the main finite-size caveat in the fused model.

## Setup

Script:

```text
sim/fused_floquet_rate_scale_scan.py
```

Data:

```text
sim/data/fused_floquet_rate_scale_rows.csv
sim/data/fused_floquet_rate_scale_summary.csv
```

Fixed:

```text
L0 = 3
threshold = 5
micro emissions = 6
seeds = 0, 1
scramblers = margulis, grid, none
```

Scanned:

```text
rate L0 = 8, 12, 20, 40
```

## Result

```text
rate L0   p1 first   soft gap   old/new gap   hard error   <shells>
8          0.419       2.076       0.684       8.9e-16      1.210
12         0.411       2.103       0.637       8.9e-16      1.195
20         0.407       2.114       0.616       0            1.188
40         0.405       2.119       0.608       8.9e-16      1.186
```

The hard probability approaches its large-`L` value as expected. The fused
information diagnostics remain stable:

```text
soft gap:
  about 2.08 to 2.12 nats;

old/new full-radiation mutual-information gap:
  about 0.61 to 0.68 nats;

mean transferred shells:
  about 1.19 to 1.21.
```

## Interpretation

The exact state-vector run still uses a small register, but the fused behavior
does not appear to be an artifact of the chosen `rate L0 = 20`.

The remaining caveat is narrower:

```text
rate L0 and exact L0 are still separated for tractability,
but varying rate L0 over a factor of five leaves the diagnostics stable.
```

This improves the status of the rate-scale issue from an untested caveat to a
characterized finite-size limitation.

## Remaining Limits

This does not solve the scale problem completely:

```text
exact register size is still L0 = 3;
hard alphabet is still two bins;
only two seeds were used;
long Page-curve behavior is not tested here.
```

The next scale improvement would need either a compressed entropy diagnostic or
a larger exact state-vector run.

