# Fixed-Floquet Expander Page Results

## Question

The previous stabilizer diagnostic used fresh random Clifford layers. That is
useful, but it is still close to imposing typicality.

This test asks whether the result survives with a more model-like dynamics:

```text
choose a sparse nonlocal graph once;
choose a fixed Clifford Floquet period once;
repeat the same update between shell removals.
```

This is still not a time-independent Hamiltonian. But it is stricter than
drawing fresh random layers at every step.

## Script

```text
sim/fixed_floquet_expander_page.py
```

Outputs are written to:

```text
sim/data/fixed_floquet_page_*.csv
```

## Model

For each active droplet size `L`, build:

```text
1. a fixed sparse graph on the active L x L qubits;
2. a fixed Clifford Floquet period of width p;
3. repeat that period between shell removals.
```

The radiation update is the same shell erosion step:

```text
active L x L droplet -> active (L-1) x (L-1) droplet + emitted shell.
```

The diagnostic computes exact stabilizer entropies:

```text
S(radiation),
I(old radiation : new shell).
```

## Results

Ten seeds were run for each case.

```text
case                                      mean |S-cap|   max |S-cap|   exact seeds
grid L0=8, width 4, warmup 4, cycle 2       13.80          22          0/10
grid L0=8, width 4, warmup 4, cycle 8       10.90          21          0/10

expander4 L0=8, width 4, warmup 4, cycle 1   1.50           4          4/10
expander4 L0=8, width 4, warmup 4, cycle 2   2.00           4          3/10

expander8 L0=8, width 4, warmup 4, cycle 1   1.50           3          3/10
expander8 L0=8, width 4, warmup 4, cycle 2   1.40           2          3/10
expander8 L0=8, width 8, warmup 4, cycle 1   0.00           0         10/10
expander8 L0=8, width16, warmup 2, cycle 1   0.00           0         10/10

expander8 L0=12, width 4, warmup 4, cycle 1  3.00           9          4/10
expander8 L0=12, width 4, warmup 4, cycle 2  3.00           9          4/10
expander8 L0=12, width 8, warmup 4, cycle 1  0.30           3          9/10
expander12 L0=12, width 8, warmup 4, cycle 1 0.00           0         10/10

complete L0=8, width 4, warmup 4, cycle 1    0.40           2          8/10
```

## Interpretation

The result is mixed but useful.

Bad news:

```text
a narrow fixed Floquet period does not automatically behave like fresh random
scrambling.
```

This is a real naturalness warning. The previous random-layer diagnostic was
partly using fresh randomness as a typicality engine.

Good news:

```text
sparse nonlocal fixed Floquet dynamics can still recover the Page curve.
```

The strongest cases:

```text
L0 = 8:
  degree-8 expander, period width 8, cycle 1 -> exact in 10/10 seeds.

L0 = 12:
  degree-12 expander, period width 8, cycle 1 -> exact in 10/10 seeds.
```

The old/new radiation mutual information also turns on at the expected discrete
Page crossing:

```text
L0 = 8:
  first MI around L = 6 -> 5.

L0 = 12:
  first MI around L = 9 -> 8.
```

## What This Means for F14

The fast-scrambling story is now more plausible than with a local grid:

```text
local grid:
  needs depth of order L and can fail under a narrow fixed period.

sparse expander-like graph:
  reaches Page behavior with low repeated depth in the tested sizes.
```

But F14 remains partial:

```text
the model is still a fixed Clifford Floquet circuit, not a natural Hamiltonian.
```

The better claim is now:

```text
fast scrambling does not require a fully all-to-all Haar random map;
a sparse nonlocal expander-like internal dynamics appears sufficient in these
stabilizer tests.
```

## Next Step

The next step is to decide how much naturalness we require.

Possible directions:

```text
1. Accept fixed sparse Floquet dynamics as the quantum-system core.
2. Replace the Clifford Floquet circuit with a sparse expander Hamiltonian.
3. Look for a constrained gauge/topological mechanism that naturally gives
   expander-like nonlocal mixing among boundary/internal sectors.
```

Option 2 is the most direct next calculation. Option 3 is the more ambitious
naturalness program.
