# Finite Bath Density Emission Results

## Question

The previous finite emission Hamiltonian implemented the golden-rule bin
weights by choosing:

```text
g_h^2 proportional to p_h^golden.
```

That made `U_emit` explicit, but the matrix elements were still tuned by bin.

This test asks whether the same distribution can come from:

```text
equal microscopic couplings
plus
finite bath density of states.
```

This is closer to the usual golden-rule logic:

```text
rate_h ~ |g|^2 * rho_h.
```

## Script

```text
sim/finite_bath_density_emission.py
```

Outputs:

```text
sim/data/finite_bath_density_emission_*.csv
```

## Model

Use one input state:

```text
|in>
```

and a finite bath of emitted microstates:

```text
|h, a>,  a = 1,...,N_h.
```

The Hamiltonian is:

```text
H_emit = g sum_(h,a) ( |h,a><in| + |in><h,a| ).
```

The microscopic coupling `g` is the same for every bath microstate.

Then:

```text
P(h | emit) = N_h / sum_k N_k.
```

The bin degeneracies `N_h` are chosen as integer approximations to the
microcanonical/phase-space density:

```text
N_h / N_bath ~= p_h^golden.
```

So the weight comes from bath degeneracy, not bin-dependent couplings.

## Results

```text
case             bath states     L1 error      max error    shrink injective
L40 2D N512          512         6.775e-03     1.744e-03       True
L40 2D N4096        4096         6.832e-04     2.788e-04       True
L40 3D N4096        4096         5.018e-04     1.169e-04       True
L8  2D N1024        1024         2.422e-03     5.740e-04       True
```

Representative bins:

```text
L40 2D N4096
bin   omega/T   degeneracy   target     actual
0      0.750       2019      0.492907   0.492920
1      2.250       1353      0.330282   0.330322
2      3.750        504      0.123076   0.123047

L40 3D N4096
bin   omega/T   degeneracy   target     actual
0      0.750        802      0.195894   0.195801
1      2.250       1613      0.393788   0.393799
2      3.750       1002      0.244568   0.244629
```

The approximation improves with bath size, as expected from integer
degeneracy rounding.

## Composition with Shrinkage

The emitted finite energy labels are also fed into the reversible shrinkage
automaton.

Result:

```text
shrinkage injective after composition = True
```

So the finite bath emission model still composes cleanly with `U_bookkeep`.

## Interpretation

This improves the naturalness of `U_emit`.

Before:

```text
per-bin matrix elements encoded the golden-rule weights.
```

Now:

```text
one equal microscopic coupling plus finite bath degeneracies encode the
weights.
```

That is closer to:

```text
Fermi golden rule = matrix element squared times density of states.
```

## Remaining Caveat

The bath density itself is still designed to approximate:

```text
omega^(d-1) exp[S(M - omega) - S(M)].
```

So this does not derive the bath spectrum from a microscopic bath Hamiltonian.

But it removes the less natural ingredient:

```text
bin-dependent emission couplings.
```

## F-Status

This strengthens:

```text
F7:
  emission weights now arise from finite bath degeneracy with equal coupling.

F15:
  U_emit is closer to a standard finite weak-coupling Hamiltonian module.
```

The remaining `U_emit` naturalness target is:

```text
derive the bath density of states rather than assigning it.
```
