# Edge Thermal Occupation Results

## Question

The energy-aware emission block still prepares the boundary edge excitation with
golden-rule weights before decay.

Can those weights instead come from an ordinary thermal boundary edge
Hamiltonian at the droplet temperature?

## Script

```text
sim/edge_thermal_occupation.py
```

Outputs:

```text
sim/data/edge_thermal_occupation.csv
sim/data/edge_thermal_occupation_summary.csv
sim/data/edge_thermal_occupation_finite16.csv
sim/data/edge_thermal_occupation_finite16_summary.csv
sim/data/edge_thermal_occupation_3d.csv
sim/data/edge_thermal_occupation_3d_summary.csv
```

## Comparison

For each droplet size `L`, compare two bin distributions.

Exact microcanonical / golden-rule:

```text
p_h^exact ~ int_bin d omega omega^(d-1)
             exp[S(M - omega) - S(M)].
```

Canonical boundary edge occupation:

```text
p_h^can ~ int_bin d omega omega^(d-1) exp[-beta(M) omega].
```

The entropy curvature correction is:

```text
S(M - omega) - S(M)
  = - beta omega + O(omega^2).
```

Since typical emitted quanta have:

```text
omega ~ T ~ 1/L,
```

the correction should scale as:

```text
O(1/L^2).
```

## Baseline Result

For:

```text
q = 2
sigma = 1
2D bath
x bins = [0,2], [2,8]
L = 2 ... 100
```

the output is:

```text
D(exact, canonical) decay slope: -2.0021
mean D(exact, canonical) last10: 1.020813e-04
mean D(exact, finite 64) last10: 1.940767e-03
```

Representative rows:

```text
L   exact_p_last  canon_p_last  D_exact_can  mean_w/T exact  mean_w/T can
  2     0.764998     0.404207   3.607906e-01       4.239285      1.978465
  6     0.431391     0.404207   2.718375e-02       2.091522      1.978465
 96     0.404308     0.404207   1.007462e-04       1.978868      1.978465
100     0.404300     0.404207   9.284625e-05       1.978836      1.978465
```

So the canonical edge distribution converges rapidly to the exact
microcanonical/golden distribution.

## 3D Bath Control

For a 3D bath:

```text
D(exact, canonical) decay slope: -2.0011
mean D(exact, canonical) last10: 1.170232e-04
```

The high-energy bin probability changes because the density of states changes:

```text
2D bath canonical p_last ~ 0.404
3D bath canonical p_last ~ 0.672
```

but the canonical-to-microcanonical convergence remains `O(L^-2)`.

## Interpretation

This improves the naturalness of the edge-aware emission block.

Before:

```text
edge excitation weights were prepared directly from the golden-rule formula.
```

Now:

```text
an ordinary boundary edge Hamiltonian at temperature T_L gives the same weights
asymptotically.
```

The exact microcanonical correction is finite-size entropy curvature. It is not
a different mechanism.

## What This Fixes

The prepared edge occupation is no longer a separate arbitrary distribution.

It can be read as:

```text
the canonical occupation of boundary soft modes at the droplet temperature.
```

This is precisely the boundary-mode intuition:

```text
omega ~ 1/L,
T ~ 1/L,
beta omega = O(1).
```

## What Remains

This still does not make the evaporator autonomous.

Still missing:

```text
a boundary soft-mode Hamiltonian included in the same total system;
a mechanism that thermalizes or typicalizes the edge mode at T_L;
weak coupling to bath modes that produces decay without pulse scheduling;
coarse mass/register update.
```

So the remaining gap has moved again:

```text
not "why these weights?"
but "how does the boundary mode stay thermally populated while the droplet
evaporates?"
```

## F1-F13 Impact

```text
F7:
  stronger P. The edge occupation used by the energy-aware block can be
  supplied by ordinary canonical boundary-mode statistics rather than direct
  preparation from the golden-rule distribution.

F13:
  stronger P. Boundary-local soft modes now have both the right energy scale
  and the right occupation statistics.
```

No clean `Y` upgrade yet, because the thermalization/typicality mechanism is
still not implemented dynamically.

## Next Step

The next meaningful test is:

```text
edge thermalization / typicality.
```

Two possible routes:

```text
1. canonical typicality route:
   show that a typical state of bulk + edge at fixed total energy gives the
   edge canonical distribution.

2. repeated-interaction route:
   couple the edge mode weakly to a small internal reservoir and show it
   relaxes to the canonical distribution before/while emitting.
```

The first route is cleaner and probably sufficient for the current control
model.
