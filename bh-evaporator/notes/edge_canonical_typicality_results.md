# Edge Canonical Typicality Results

## Question

Can the boundary edge occupation arise from typicality of a large droplet
reservoir, rather than from explicit thermal preparation?

The previous result showed:

```text
canonical edge weights at T_L match exact microcanonical/golden weights up to
O(L^-2) corrections.
```

This note checks the stronger typicality statement:

```text
a Haar-typical pure state in the microcanonical shell of reservoir + edge has
an edge reduced state close to the microcanonical edge distribution.
```

## Script

```text
sim/edge_canonical_typicality.py
```

Outputs:

```text
sim/data/edge_canonical_typicality.csv
sim/data/edge_canonical_typicality_summary.csv
sim/data/edge_canonical_typicality_dim1024.csv
sim/data/edge_canonical_typicality_dim1024_summary.csv
sim/data/edge_canonical_typicality_dim16384.csv
sim/data/edge_canonical_typicality_dim16384_summary.csv
```

## Model

For edge energy bins `omega_h`, use a reservoir degeneracy:

```text
dim H_res(h) ~ exp[S(M - omega_h)].
```

The total microcanonical shell is:

```text
H_shell = direct_sum_h |h>_edge tensor H_res(h).
```

The exact reduced edge distribution is:

```text
p_h^micro = dim H_res(h) / sum_k dim H_res(k).
```

For large `L`, this approaches:

```text
p_h^can ~ exp[-beta(M) omega_h]
```

with the appropriate bath/bin degeneracy factors.

A Haar-typical state in `H_shell` has sector weights distributed as a Dirichlet
random variable with parameters:

```text
dim H_res(h).
```

So typical fluctuations should shrink as reservoir dimensions grow.

## Baseline Result

For:

```text
q = 2
sigma = 1
2D bath
x bins = [0,2], [2,8]
total finite shell dimension = 4096
samples = 512
L = 2 ... 100
```

the summary is:

```text
D(exact, canonical) decay slope: -2.0039
mean D(exact, canonical) last10: 1.685426e-04
mean D(sample, finite shell) last10: 4.674509e-03
mean D(sample, canonical) last10: 4.675270e-03
```

Representative rows:

```text
L   exact_p_last  sample_p_last  D_samp_fin  D_samp_can  min/max counts
  2     0.751849      0.751718   5.295282e-03 5.778724e-01 1016/3080
  6     0.220588      0.220725   5.255222e-03 4.687945e-02  904/3192
 96     0.174012      0.174090   4.736107e-03 4.741296e-03  713/3383
100     0.173999      0.173906   4.577409e-03 4.570494e-03  713/3383
```

The typical sampled edge state is close to the finite microcanonical edge
distribution. At large `L`, the finite microcanonical distribution is also very
close to canonical.

## Reservoir-Dimension Control

Changing the finite shell dimension changes typical-state fluctuations:

```text
total_dim   mean D(sample, finite shell) last10
1024        9.341644e-03
4096        4.674509e-03
16384       2.337777e-03
```

This is the expected concentration behavior:

```text
larger reservoir dimensions -> smaller typical fluctuations.
```

## Interpretation

This removes another artificial preparation step.

Before:

```text
edge occupation was prepared with golden-rule weights.
```

Then:

```text
golden-rule weights were shown to match canonical edge occupation at T_L.
```

Now:

```text
canonical/microcanonical edge occupation follows from typicality of a large
droplet reservoir.
```

So the edge mode does not need an external thermostat. It can be typicalized by
the droplet reservoir itself, provided bulk-edge mixing is strong enough.

## What Remains

This is still statistical, not dynamical.

It shows:

```text
if the bulk + edge state is typical in an energy shell, the edge occupation is
correct.
```

It does not yet show:

```text
the Hamiltonian dynamically produces and maintains that typicality during
evaporation.
```

The remaining assumption is therefore:

```text
bulk-edge mixing/scrambling is sufficient to keep the boundary edge typical
between emissions.
```

That is a much more standard assumption than direct preparation of the edge
probabilities.

## F1-F13 Impact

```text
F7:
  stronger P. Edge occupation can now be justified by canonical typicality of
  the droplet reservoir, not just inserted.

F13:
  stronger P. Boundary-local emission is compatible with reservoir typicality;
  the missing piece is dynamical bulk-edge mixing.
```

Still no clean `Y` upgrade:

```text
the autonomous Hamiltonian maintaining typicality and updating L is not built.
```

## Next Step

The next meaningful direction is a small dynamical typicalization test:

```text
bulk reservoir + edge mode
fixed total energy shell
local/scrambled bulk-edge Hamiltonian
measure relaxation of edge populations toward microcanonical weights.
```

If that works, the only major remaining modular piece is the coarse `L` update.
