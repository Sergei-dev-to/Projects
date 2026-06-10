# Global Fixed-Floquet Page Results

## Question

The fixed-Floquet expander diagnostic still picked a separate fixed period for
each active droplet size `L`.

That is a naturalness weakness:

```text
the dynamics changes when the droplet shrinks.
```

This test is stricter:

```text
choose one global sparse graph on the original L0 x L0 droplet;
choose one global fixed Clifford Floquet period;
after shrinkage, apply the same rule restricted to the remaining active qubits.
```

So the model is closer to a single fixed dynamics.

## Script

```text
sim/global_fixed_floquet_page.py
```

Outputs:

```text
sim/data/global_fixed_floquet_page_*.csv
```

## Results

Ten seeds were run for each case.

```text
case                                             mean |S-cap|   max |S-cap|   exact seeds
grid L0=8, width 8,  warmup 4, cycle 4              1.70           6          6/10
grid L0=8, width16,  warmup 2, cycle 2              0.00           0         10/10

global expander L0=8, degree 8,  width 8, cycle 1   0.00           0         10/10
global expander L0=8, degree16,  width 8, cycle 1   0.00           0         10/10
global expander L0=8, degree16, width16, cycle 1    0.00           0         10/10

global expander L0=12, degree12, width 8, cycle 1   0.00           0         10/10
global expander L0=12, degree24, width 8, cycle 1   0.00           0         10/10
global expander L0=12, degree24, width16, cycle 1   0.00           0         10/10
```

The old/new mutual information turns on at the expected discrete Page crossing:

```text
L0 = 8:
  L = 6 -> 5.

L0 = 12:
  L = 9 -> 8.
```

## Interpretation

This fixes an important naturalness worry.

The previous expander Floquet diagnostic could be criticized as using
size-dependent dynamics:

```text
one period for L0;
another period for L0 - 1;
another period for L0 - 2;
...
```

The global fixed-Floquet test removes that particular issue. One graph and one
period are chosen at the beginning, then reused throughout the evaporation
history.

The result remains strong:

```text
global sparse expander-like dynamics gives exact Page behavior in every tested
seed for L0 = 8 and L0 = 12.
```

The local grid can also work, but it needs more total depth. For example:

```text
grid:
  width 16, cycle 2 -> 32 elementary layers per shell.

global expander:
  width 8, cycle 1 -> 8 elementary layers per shell.
```

So the expander branch remains the better fast-scrambling proxy.

## What Is Still Missing

This is still not a Hamiltonian derivation.

The remaining imposed ingredients are:

```text
1. a sparse nonlocal graph is chosen by hand;
2. the Floquet gates are Clifford/random;
3. the shell erosion rule is still external to the unitary scrambling dynamics.
```

But this is a cleaner position than before:

```text
we no longer need fresh randomness per layer;
we no longer need size-dependent periods;
we no longer need fully all-to-all coupling.
```

## Status

This strengthens F14 from a weak proxy to a fairly concrete circuit-level
fast-scrambling proxy.

It should still remain:

```text
F14 = P
```

until a Hamiltonian or more physically motivated sparse expander mechanism is
specified.
