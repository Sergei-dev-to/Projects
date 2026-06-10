# Quadratic Connector Candidate Scale Review

## Why This Matters

The quadratic connector branch looked promising because it gives:

```text
O(N^2) active relational modes;
omega ~ 1/N soft quanta;
post-shrink heating in the quadratic spectrum gate.
```

But there is a scale issue that has to be kept explicit.

If:

```text
M(N) ~ N
S(N) ~ N^2
```

then:

```text
T(N) = dM/dS ~ 1/N.
```

A microscopic emitted quantum has energy:

```text
epsilon ~ T ~ 1/N.
```

A coarse active-size change:

```text
N -> N - 1
```

changes the mass by:

```text
Delta M ~ 1.
```

So one coarse shrink step corresponds to order `N` microscopic emitted quanta.

## Script

```text
sim/quadratic_connector_scale_consistency.py
```

Run:

```text
python sim/quadratic_connector_scale_consistency.py
```

Result:

```text
T_power = -1.021
quanta_per_shrink_power = 1.021
T_at_N=256 = 5.6576e-03
quanta_per_shrink_at_N=256 = 176.75
```

The finite-difference constants depend on the normalization, but the scaling is
the key result:

```text
T ~ N^-1
number of Hawking-scale quanta per N -> N-1 shrink ~ N.
```

## Consequence For The Earlier Heating Gate

The earlier critical-connector heating gate tested:

```text
emit epsilon ~ T;
change active spectrum N -> N-1;
ask whether T_after > T_before.
```

That is not the physical coarse shrink step if `M ~ N`.

The better interpretation is:

```text
the gate tested whether the N-indexed connector spectra have the right
thermodynamic direction under a small energy loss and a small active-size
change.
```

It is a useful spectral gate, but it is not yet an autonomous evaporation
model.

## What The Full Model Must Do

A viable autonomous model needs three scales:

```text
microscopic emission:
  each emitted quantum has energy ~ 1/N;

slow shrinkage:
  the active core parameter N changes after O(N) microscopic emissions;

continuous heating:
  the effective temperature rises by O(1/N^3) per microscopic quantum and by
  O(1/N^2) per coarse N -> N-1 shrink.
```

So the connector model needs an internal slow variable or collective coordinate
that lets the active core shrink gradually. A hard jump from `N` to `N-1` after
one quantum is the wrong physical picture.

## Candidate Hamiltonian Target

The strongest current candidate should be formulated as:

```text
H_total =
  H_core_rest
+ H_quadratic_connector_band
+ H_core_connector_coupling
+ H_outgoing_radiation
```

with:

```text
H_core_rest:
  gives M ~ N for the active core;

H_quadratic_connector_band:
  gives O(N^2) active relational modes with z=2 dispersion;

H_core_connector_coupling:
  lets connector excitations carry energy out without immediately deleting a
  constituent;

H_outgoing_radiation:
  provides asymptotic modes so emitted quanta do not return.
```

The core/radiation split should be diagnosed dynamically:

```text
core = active bound component plus its active connector band;
radiation = outgoing connector/radiation excitations and eventually detached
constituents.
```

## What We Have Now

We have:

```text
area-like counting from O(N^2) connectors;
standard physical language for z=2 quadratic modes;
spectral evidence for Hawking-scale soft quanta;
spectral evidence that quadratic bands have the right heating direction.
```

We do not yet have:

```text
an autonomous Hamiltonian where N changes after many microscopic emissions;
a derived escape/separation mechanism;
a measured flux spectrum from time evolution;
Page-like information flow in this same model.
```

## Current Status

The branch remains alive, but the corrected target is stricter:

```text
build a quadratic connector evaporator with many microscopic emissions per
coarse shrink step.
```

That is the next real step toward the main goal.
