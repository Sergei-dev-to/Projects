# Stitched Floquet Evaporator Results

## Question

Can the current modules be expressed as one repeated-interaction architecture
rather than as disconnected diagnostics?

The stitched Floquet specification defines one repeated cycle:

```text
U_cycle(L) = U_bookkeep U_emit U_edge U_scramble(L).
```

This result runs the corresponding coarse simulator.

## Scripts and Spec

Specification:

```text
notes/stitched_floquet_evaporator_spec.md
```

Simulator:

```text
sim/stitched_floquet_evaporator.py
```

Outputs:

```text
sim/data/stitched_floquet_evaporator_L40_2d.csv
sim/data/stitched_floquet_evaporator_L40_2d_summary.csv
sim/data/stitched_floquet_evaporator_L80_2d.csv
sim/data/stitched_floquet_evaporator_L80_2d_summary.csv
sim/data/stitched_floquet_evaporator_L40_3d.csv
sim/data/stitched_floquet_evaporator_L40_3d_summary.csv
```

## Model

Each microscopic cycle contains:

```text
1. internal scrambling:
   algebraic-expander interacting-spin module;

2. edge/boundary thermalization:
   microcanonical/canonical edge weights;

3. emission:
   golden-rule small-quanta emission into a bath;

4. bookkeeping:
   emitted-energy accumulator;

5. threshold shrinkage:
   apply L -> L - 1 when emitted energy crosses Delta M.
```

The simulator is coarse:

```text
it tracks trajectory and capacity, not the full state vector.
```

## Results

```text
case      shell cycles   micro emissions   page L   page fraction   scaled lifetime
L40 2D        39              592            28        0.510          0.333328
L80 2D        79             2309            56        0.510          0.333333
L40 3D        39              396            28        0.510          0.250000
```

For the 2D bath:

```text
tau / M0^3 ~= 1/3.
```

For the 3D bath control:

```text
tau / M0^4 ~= 1/4.
```

The Page crossing remains:

```text
L ~= L0 / sqrt(2).
```

Examples:

```text
L0 = 40:
  L0 / sqrt(2) = 28.3
  observed page L = 28

L0 = 80:
  L0 / sqrt(2) = 56.6
  observed page L = 56
```

## Microscopic Emissions Per Shell

For `L0 = 40`, early shells have many microscopic emissions:

```text
40 -> 39:
  29 emissions

39 -> 38:
  27 emissions

38 -> 37:
  28 emissions
```

For `L0 = 80`:

```text
80 -> 79:
  55 emissions

79 -> 78:
  57 emissions

78 -> 77:
  53 emissions
```

So the stitched cycle preserves the intended separation:

```text
microscopic radiation quanta are small;
coarse shell shrinkage happens after many emissions.
```

## Interpretation

This is not new physics beyond the modules. Its value is architectural.

Before:

```text
scrambling, emission, shell shrinkage, and Page tracking were separate tests.
```

Now:

```text
they are organized as one repeated-interaction evaporator.
```

This strengthens F15:

```text
F15 moves from weak P to P+.
```

But it does not make F15 a clean `Y`.

## Remaining F15 Gap

The stitched model is still not one time-independent Hamiltonian:

```text
U_scramble:
  Hamiltonian-like internal module;

U_emit:
  emission block/channel;

U_bookkeep:
  threshold accumulator and coarse shrinkage update.
```

The coarse shell update is still explicit.

So the current status is:

```text
one explicit repeated-interaction architecture:
  yes;

one autonomous H_total:
  no.
```

## Current Assessment

The stitched architecture is good enough to serve as the current candidate
model specification.

The remaining naturalness question is sharper:

```text
Can U_emit and U_bookkeep be embedded into a less artificial autonomous
Hamiltonian/Floquet rule?
```

That is now the main F15 problem.
