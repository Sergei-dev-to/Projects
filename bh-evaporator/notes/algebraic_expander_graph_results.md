# Algebraic Expander Graph Results

## Question

The global fixed-Floquet test removed two artificial ingredients:

```text
fresh randomness at every layer;
size-dependent dynamics as L shrinks.
```

But it still used a sparse random graph.

This test asks whether the graph itself can be replaced by a deterministic
algebraic rule.

## Script

```text
sim/global_fixed_floquet_page.py
```

The new geometry is:

```text
margulis
```

using a Margulis/Gabber-Galil-style graph on:

```text
Z_L0 x Z_L0.
```

The directed generator maps are:

```text
(x, y) -> (x +/- 2y, y)
(x, y) -> (x +/- (2y + 1), y)
(x, y) -> (x, y +/- 2x)
(x, y) -> (x, y +/- (2x + 1))
```

with coordinates reduced modulo `L0`. The diagnostic uses the underlying
undirected graph.

This is not a Cayley graph in the narrow abelian translation sense, but it is
an explicit algebraic expander-style rule rather than a sampled random graph.

## Results

Ten seeds were run for each case. The remaining randomness is in the fixed
Clifford Floquet period, not in the graph.

```text
case                                      mean |S-cap|   max |S-cap|   exact seeds
margulis L0=8,  width 8,  warmup 4, cycle 1   0.30           2          8/10
margulis L0=8,  width16,  warmup 2, cycle 1   0.00           0         10/10
margulis L0=12, width 8,  warmup 4, cycle 1   0.00           0         10/10
margulis L0=12, width16,  warmup 2, cycle 1   0.10           1          9/10
```

For comparison, the sparse random global expander gave:

```text
global expander L0=8,  degree 8,  width 8, cycle 1   0.00   0   10/10
global expander L0=12, degree12,  width 8, cycle 1   0.00   0   10/10
```

The algebraic graph is therefore competitive with the sampled sparse expander.

The old/new mutual information again turns on near the discrete Page crossing:

```text
L0 = 8:
  L = 6 -> 5.

L0 = 12:
  L = 9 -> 8, with one marginal case at 10 -> 9.
```

## What This Fixes

This substantially improves the graph naturalness issue.

Before:

```text
choose a random sparse graph by hand.
```

Now:

```text
choose an explicit algebraic expander-style connectivity rule.
```

That means the fast-scrambling graph is no longer arbitrary in the same way.
It is a compact deterministic structure.

## What It Does Not Fix

The dynamics is still not fully derived.

Remaining imposed ingredients:

```text
1. the algebraic expander rule is selected as the internal connectivity;
2. the fixed Floquet period still contains random Clifford gates;
3. shell erosion is still an external update rule;
4. no time-independent Hamiltonian has been specified.
```

So this does not give a complete physical derivation.

But it does fix a meaningful weakness:

```text
fast scrambling no longer requires a random graph ensemble.
```

## Status

For F14:

```text
F14 remains P, but stronger.
```

The model now has a deterministic sparse nonlocal graph that supports the Page
curve and old/new mutual information turn-on under a fixed Floquet dynamics.

The next naturalness target is no longer the graph. It is the dynamics on the
graph:

```text
replace random Clifford Floquet gates with a motivated sparse Hamiltonian or a
fixed deterministic gate pattern.
```
