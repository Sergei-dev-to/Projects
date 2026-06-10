# Interacting Spin Scrambling Diagnostic Results

## Question

The Page stress test showed that interacting spin dynamics works at `L0 = 4`,
but it did not distinguish graph choice:

```text
grid, Margulis, and complete graph all gave Page-like shell entropy.
```

That could mean:

```text
1. graph choice does not matter;
2. the Page diagnostic is too coarse at L0 = 4.
```

This diagnostic measures scrambling more directly.

## Script

```text
sim/interacting_spin_scrambling_diagnostic.py
```

Output:

```text
sim/data/interacting_spin_scrambling_diagnostic.csv
```

## Model

Use the same Trotterized random Heisenberg Hamiltonian as the interacting-spin
Page test.

Compare:

```text
grid:
  local nearest-neighbor square graph.

margulis:
  deterministic algebraic expander-style graph.

complete:
  all-to-all control.
```

Starting from random product states, track entanglement growth for:

```text
mean single-qubit entropy;
quadrant entropy;
half-system entropy.
```

All entropies are normalized by their maximum possible value.

## Results

Three seeds were run for each graph.

Threshold times:

```text
graph      single >= 0.9   quadrant >= 0.75   half >= 0.5
grid             2                2                2
margulis         1                1                1
complete         1                1                0.5
```

Time series:

```text
grid
t=0      single=0.000   quad=0.000   half=0.000
t=0.25   single=0.324   quad=0.119   half=0.056
t=0.5    single=0.607   quad=0.248   half=0.145
t=1      single=0.827   quad=0.544   half=0.329
t=2      single=0.948   quad=0.846   half=0.610
t=4      single=0.983   quad=0.957   half=0.834
t=8      single=0.994   quad=0.989   half=0.892

margulis
t=0      single=0.000   quad=0.000   half=0.000
t=0.25   single=0.366   quad=0.241   half=0.129
t=0.5    single=0.699   quad=0.494   half=0.330
t=1      single=0.921   quad=0.832   half=0.636
t=2      single=0.992   quad=0.983   half=0.865
t=4      single=0.999   quad=0.998   half=0.907
t=8      single=0.999   quad=0.998   half=0.908

complete
t=0      single=0.000   quad=0.000   half=0.000
t=0.25   single=0.375   quad=0.338   half=0.224
t=0.5    single=0.755   quad=0.690   half=0.501
t=1      single=0.967   quad=0.939   half=0.803
t=2      single=0.996   quad=0.993   half=0.899
t=4      single=0.997   quad=0.995   half=0.904
t=8      single=0.997   quad=0.996   half=0.903
```

## Interpretation

This is the graph distinction the Page diagnostic could not see.

At `L0 = 4`:

```text
grid:
  reaches the main entanglement thresholds around t = 2.

margulis:
  reaches them around t = 1.

complete:
  reaches half-system threshold by t = 0.5 and the others by t = 1.
```

So the deterministic algebraic graph is not just decorative. Under the same
interacting spin dynamics, it scrambles faster than the local grid and closer
to the complete graph.

## Consequence

The F14 branch now has a more coherent story:

```text
1. Clifford/Floquet expander circuits produce Page behavior.
2. Free Majorana Hamiltonians on the same graph fail.
3. Interacting spin Hamiltonian dynamics produces Page-like shell entropy.
4. Direct entanglement-growth diagnostics show Margulis graph scrambles faster
   than the local grid.
```

This still does not prove asymptotic fast scrambling.

But it supports the working claim:

```text
interacting chaotic dynamics on a deterministic sparse nonlocal graph is a
plausible non-gravitational fast-scrambling module.
```

## Remaining Caveats

```text
L0 = 4 is small.
The diagnostic measures entanglement growth, not an OTOC.
The Hamiltonian is Trotterized.
The couplings are random in this run.
```

The next strongest check would be an operator-spreading or OTOC diagnostic on
the same model.
