# Interacting Spin Stress-Test Results

## Question

The first interacting-spin test gave a positive small-size F14 result.

Before building on it, we need to check whether it is robust or just a lucky
parameter choice.

The stress test varies:

```text
graph:
  grid, Margulis algebraic expander, complete graph;

couplings:
  random Heisenberg, deterministic label-generated couplings;

Trotter step:
  dt = 0.1, 0.2, 0.4;

timing:
  warmup/cycle = 4/1, 8/2, 12/3.
```

## Script

```text
sim/interacting_spin_stress_test.py
```

Outputs:

```text
sim/data/interacting_spin_stress_rows.csv
sim/data/interacting_spin_stress_summary.csv
```

## Results

All runs use:

```text
L0 = 4
3 seeds per case
```

```text
case                                      mean total deficit   max total deficit   first MI
grid random,       warmup 8, cycle 2          0.168               0.203            3->2
margulis random,   warmup 8, cycle 2          0.147               0.169            3->2
complete random,   warmup 8, cycle 2          0.145               0.156            3->2
margulis determin, warmup 8, cycle 2          0.229               0.368            3->2

margulis random, dt 0.1                       0.149               0.167            3->2
margulis random, dt 0.2                       0.147               0.169            3->2
margulis random, dt 0.4                       0.134               0.142            3->2

margulis random, warmup 4,  cycle 1           0.148               0.167            3->2
margulis random, warmup 12, cycle 3           0.146               0.169            3->2
```

## Interpretation

The positive interacting-spin result is robust at this size.

It is not sensitive to:

```text
moderate Trotter step changes;
moderate timing changes;
random vs deterministic couplings;
graph choice among grid / algebraic expander / complete.
```

The last point is both good and bad.

Good:

```text
the Page-like behavior is not fragile.
```

Bad:

```text
L0 = 4 is too small to demonstrate a clean fast-scrambling advantage for the
algebraic expander graph.
```

At this size, even the local grid can scramble enough before shell removal.

## Current Assessment

This stress test supports the interacting-spin branch but does not prove the
fast-scrambling scaling story.

What it supports:

```text
interacting spin dynamics can produce Page-like shell evaporation.
```

What it does not yet support:

```text
the algebraic expander graph is necessary or visibly faster in Hamiltonian
dynamics.
```

The next diagnostic should therefore target scrambling directly:

```text
entanglement growth or operator spreading under the same Hamiltonian.
```

The Page diagnostic itself is too coarse at `L0 = 4` to distinguish graphs.
