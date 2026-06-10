# Edge Dynamical Typicalization Results

## Question

Can a finite Hamiltonian dynamically drive a boundary edge mode toward the
microcanonical/canonical weights, instead of assuming the edge is already
typical?

The previous result showed:

```text
typical states of edge + reservoir have the right edge distribution.
```

This diagnostic asks whether Hamiltonian mixing inside the fixed energy shell
can produce that typicality from a non-typical initial edge state.

## Script

```text
sim/edge_dynamical_typicalization.py
```

Outputs:

```text
sim/data/edge_dynamical_typicalization.csv
sim/data/edge_dynamical_typicalization_summary.csv
sim/data/edge_dynamical_typicalization_b4.csv
sim/data/edge_dynamical_typicalization_b4_summary.csv
sim/data/edge_dynamical_typicalization_b24.csv
sim/data/edge_dynamical_typicalization_b24_summary.csv
sim/data/edge_dynamical_typicalization_dim512.csv
sim/data/edge_dynamical_typicalization_dim512_summary.csv
```

## Model

Use the same finite microcanonical shell:

```text
H_shell = direct_sum_h |h>_edge tensor C^(d_h),
```

where:

```text
d_h ~ exp[S(M - omega_h)]
```

with bin-density factors included.

The target edge distribution is:

```text
p_h = d_h / sum_k d_k.
```

Start from a non-typical state entirely in one edge sector, then evolve under a
Hamiltonian acting within the total energy shell.

Two Hamiltonian variants were tested:

```text
full_random:
  random Hermitian matrix on the full shell.

banded:
  random Hermitian matrix with finite bandwidth in the sector-grouped basis.
```

This is not a local lattice Hamiltonian yet. It is a minimal ETH/scrambling
test.

## Baseline

Parameters:

```text
L = 40
q = 2
sigma = 1
2D bath
total_dim = 256
seeds = 8
t_max = 30
```

Target weights:

```text
0.8242, 0.1758
```

Counts:

```text
211, 45
```

Result:

```text
variant      D(t=0)   D(final)  D(best)   t_best
full_random    0.1758    0.0187   0.0075   18.500
banded         0.1758    0.0765   0.0765   30.000
```

The full random Hamiltonian typicalizes the edge well. The banded Hamiltonian
improves the edge population but does not fully typicalize on this timescale.

## Controls

Banded bandwidth:

```text
bandwidth   D(final)   D(best)
4           0.1499     0.1488
12          0.0765     0.0765
24          0.0427     0.0403
```

So the result depends on mixing strength, as expected.

Larger reservoir, full random Hamiltonian:

```text
total_dim = 512
seeds = 4

D(t=0) = 0.1758
D(final) = 0.0138
D(best) = 0.0032
```

Larger reservoir dimension improves the typicalized result.

## Interpretation

This supports the canonical-typicality route dynamically, with a caveat.

What works:

```text
strong mixing inside the edge+reservoir energy shell drives edge populations
toward the microcanonical target.
```

What does not automatically work:

```text
weak/banded mixing may be too slow or incomplete.
```

So the assumption we need is not mysterious:

```text
bulk-edge dynamics must be sufficiently scrambling/ergodic on the emission
timescale.
```

That is physically reasonable for a black-hole-like control model, but it is
still an assumption.

## What This Fixes

The edge occupation story is now:

```text
microcanonical reservoir state counts determine the target edge distribution;
canonical edge occupation is the large-L approximation;
typical pure states reproduce the distribution;
strong Hamiltonian mixing dynamically approaches it from non-typical states.
```

This is much better than direct edge preparation.

## What Remains

Still missing:

```text
a geometrically local bulk-edge Hamiltonian that typicalizes efficiently;
simultaneous typicalization and emission in one continuous dynamics;
coarse mass/register update L -> L-1;
large Page-curve simulation.
```

The important new failure mode is:

```text
if bulk-edge mixing is too local or too weak, edge thermalization is too slow.
```

That is exactly the kind of meaningful condition we wanted to identify.

## F1-F13 Impact

```text
F7:
  stronger P. Edge occupation is now dynamically approachable under strong
  Hamiltonian mixing.

F13:
  sharper P. Boundary-local emission needs sufficiently strong bulk-edge
  scrambling; weak banded mixing is not enough in the tested window.
```

Still no clean `Y`:

```text
the full local autonomous evaporator has not been built.
```

## Next Step

At this point the next bottleneck is no longer the emission block. It is the
coarse shrinkage/update:

```text
many microscopic emissions drain energy;
the effective bulk register capacity must shrink from q^(L^2) to q^((L-1)^2);
the lost information must already be in radiation/soft records.
```

The next diagnostic should test a coarse update after many energy-aware
microscopic emissions.
