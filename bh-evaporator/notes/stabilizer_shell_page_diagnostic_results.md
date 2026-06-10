# Stabilizer Shell Page Diagnostic Results

## Question

The random-isometry argument says that the shell sequence gives a Page curve if
each shrink step is typical enough.

The next question is:

```text
Can an explicit many-qubit dynamics produce that behavior, at least in a
scalable toy setting?
```

This diagnostic uses Clifford/stabilizer circuits so that many-qubit
entanglement can be tracked exactly without dense state vectors.

## Script

```text
sim/stabilizer_shell_page_diagnostic.py
```

Outputs:

```text
sim/data/stabilizer_shell_page_grid_L8_w0_c0.csv
sim/data/stabilizer_shell_page_grid_L8_w16_c0.csv
sim/data/stabilizer_shell_page_grid_L8_w16_c2.csv
sim/data/stabilizer_shell_page_grid_L8_w16_c8.csv
sim/data/stabilizer_shell_page_expander4_L8_w8_c1.csv
sim/data/stabilizer_shell_page_expander4_L8_w8_c2.csv
sim/data/stabilizer_shell_page_expander4_L8_w8_c4.csv
sim/data/stabilizer_shell_page_expander8_L8_w8_c1.csv
sim/data/stabilizer_shell_page_expander8_L8_w8_c2.csv
sim/data/stabilizer_shell_page_complete_L8_w8_c1.csv
sim/data/stabilizer_shell_page_complete_L8_w8_c4.csv
sim/data/stabilizer_shell_page_grid_L12_w24_c12.csv
sim/data/stabilizer_shell_page_expander4_L12_w12_c2.csv
sim/data/stabilizer_shell_page_expander8_L12_w12_c2.csv
sim/data/stabilizer_shell_page_complete_L12_w12_c2.csv
```

## Model

Start with an `L0 x L0` qubit droplet in a pure state.

At each coarse shrink step:

```text
1. apply a random Clifford scrambling circuit on the active L x L droplet;
2. move the outer shell into radiation;
3. continue with the remaining (L-1) x (L-1) droplet.
```

The diagnostic computes exact stabilizer entropies:

```text
S(radiation),
I(old radiation : new shell).
```

The Page-capacity target is:

```text
S_Page ~= min(N_rad, N_remaining)
```

in qubit units.

This is not yet the finite-gauge droplet Hamiltonian. It is a scalable quantum
information test of the shell-isometry assumption.

## Cases

For `L0 = 8`, ten random seeds were run for each case.

The circuit labels are:

```text
grid:
  nearest-neighbor Clifford layers on the 2D droplet.

complete:
  all-to-all Clifford layers on the active droplet.

expander4 / expander8:
  fixed sparse nonlocal graphs, built as degree-4 or degree-8 random-regular-ish
  matchings on the active droplet.

warmup:
  initial scrambling depth before the first shell is removed.

cycle:
  scrambling depth between shell removals.
```

## Results

```text
case                         mean |S-cap|   max |S-cap|   exact seeds
grid, warmup 0,  cycle 0        98.00          98          0/10
grid, warmup 16, cycle 0        24.10          28          0/10
grid, warmup 16, cycle 2        10.20          14          0/10
grid, warmup 16, cycle 8         0.10           1          9/10
expander4, warmup 8, cycle 1     2.40           6          2/10
expander4, warmup 8, cycle 2     1.50           4          3/10
expander4, warmup 8, cycle 4     0.60           2          6/10
expander8, warmup 8, cycle 1     0.10           1          9/10
expander8, warmup 8, cycle 2     0.00           0         10/10
complete, warmup 8, cycle 1      0.40           2          8/10
complete, warmup 8, cycle 4      0.00           0         10/10
```

Here:

```text
|S-cap| = sum over shell steps of |S_rad - min(N_rad, N_remaining)|.
```

So:

```text
no scrambling:
  fails completely;

initial scrambling only:
  helps but does not maintain Page behavior through the sequence;

shallow local scrambling:
  improves but remains imperfect;

local grid scrambling with depth ~ L0:
  essentially saturates the Page curve;

all-to-all scrambling:
  reaches Page behavior with much smaller depth.
```

The larger `L0 = 12` spot check preserves the same hierarchy:

```text
case                          mean |S-cap|   max |S-cap|   exact seeds
grid, warmup 24, cycle 12        0.00           0         10/10
expander4, warmup 12, cycle 2    0.90           9          9/10
expander8, warmup 12, cycle 2    0.00           0         10/10
complete, warmup 12, cycle 2     0.00           0         10/10
```

So the sparse nonlocal expander-like graph gives Page behavior at much smaller
cycle depth than the local grid:

```text
grid:
  depth ~ L in these tests;

degree-8 expander-like graph:
  depth 2 is enough for L0 = 8 and L0 = 12.
```

## Early/Late Correlations

The same runs track:

```text
I(old radiation : new shell).
```

In the successful cases, the first nonzero old/new mutual information appears
near the Page crossing.

For `L0 = 8`, the Page crossing is around:

```text
L ~= 8 / sqrt(2) ~= 5.7.
```

The successful runs show first old/new mutual information around:

```text
L = 6 -> 5
```

which is the expected discrete shell location.

## Interpretation

This is the first direct many-cycle quantum-information diagnostic in the
project.

It shows:

```text
F8:
  explicit circuit dynamics can produce the Page-like radiation entropy curve.

F9:
  old/new radiation correlations turn on near the Page crossing.
```

It also shows the important failure mode:

```text
the shell dimensions alone are not enough.
```

Without enough scrambling between shell removals, the radiation entropy does
not follow the Page-capacity curve.

## Naturalness

This improves the situation but does not close it.

The good part:

```text
nearest-neighbor 2D dynamics can work, and sparse nonlocal expander-like
dynamics works much faster.
```

So F8/F9 do not require arbitrary all-to-all random isometries.

The remaining caveat:

```text
the circuit is a random Clifford circuit, not a Hamiltonian derived from the
finite-gauge droplet.
```

The needed local circuit depth is of order `L` in this small test, not
obviously the fast-scrambling `log N` behavior associated with black holes.
The sparse expander-like graph is more promising: it reaches the Page curve at
constant depth in the sizes tested, though this is not yet a scaling theorem.

That may or may not matter for this project:

```text
if the goal is Page phenomenology:
  local depth ~ L may be enough.

if the goal includes black-hole fast scrambling:
  local grid dynamics is weak, while the expander-like version is the right
  next candidate.
```

## Current Status

This result makes F8/F9 stronger than before:

```text
they are no longer only Page-theorem assumptions;
they have an explicit scalable stabilizer-circuit realization.
```

But they should remain `P`, not `Y`, because the circuit dynamics is still a
proxy for the finite-gauge droplet Hamiltonian.

The next sensible step is to decide whether fast scrambling is part of the
target phenomenology list. If yes, the expander-like droplet interaction is now
the better branch than the local grid.
