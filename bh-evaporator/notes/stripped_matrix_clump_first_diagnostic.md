# Stripped Matrix-Clump First Diagnostic

## What Was Added

Script:

```text
bh-evaporator/sim/classical_matrix_clump.py
```

This is a classical diagnostic for the stripped bosonic matrix Hamiltonian:

```text
H = 1/2 sum_a Tr(P_a^2)
  + g^2/2 sum_{a<b} ||[X_a, X_b]||_F^2.
```

The matrices are real symmetric and traceless. This is not BFSS. It is a cheap
test of whether the clump/escape/heating mechanism survives in a stripped
ordinary matrix system.

## Diagnostics

The code tracks:

```text
energy drift;
radial eigenvalue spread;
largest-radius / median-radius ratio;
candidate escape events;
approximate clump energy after excluding the largest radial direction;
approximate clump kinetic temperature.
```

Escape candidate:

```text
r_max / r_median > threshold
```

Default threshold:

```text
3.0
```

This is only a crude detector. It is good enough to decide whether the branch is
alive, not good enough for a final claim.

## First Runs

Mild compact initial data:

```text
N=6, D=3, p_scale=0.70, steps=10000, dt=0.001
```

Representative results:

```text
seed 100: ratio_max=2.313, no escape
seed 101: ratio_max=2.545, no escape
seed 102: ratio_max=2.378, no escape
```

More energetic compact data:

```text
N=6, D=3, p_scale=1.40, seeds 200..215
```

Result:

```text
no threshold-crossing escape events;
largest observed ratio was about 2.98.
```

Hotter data:

```text
N=6, D=3, p_scale=3.0, seeds 300..307
```

Result:

```text
no threshold-crossing escape events;
clump temperature mostly decreased over the run.
```

Small lower-dimensional runs:

```text
N=4, D=2, p_scale=2.0, steps=50000, dt=0.001
```

Two representative seeds:

```text
seed 400:
  energy_drift_rel = 1.0e-4
  ratio_max = 5.012
  above_threshold_fraction = 0.058
  longest_above_samples = 14
  post_event dE_cl = -0.656
  post_event dT_cl = +0.061

seed 401:
  energy_drift_rel = 1.6e-5
  ratio_max = 3.791
  above_threshold_fraction = 0.080
  longest_above_samples = 10
  post_event dE_cl = -0.537
  post_event dT_cl = -0.282
```

## Interpretation

The first result is not a clean success.

What we see:

```text
1. The integrator is stable enough for exploratory work.
2. Generic N=6, D=3 compact clumps do not obviously evaporate on these times.
3. Smaller N=4, D=2 cases can produce separated radial eigenvalue events.
4. The heating signature is mixed: one candidate heats after energy loss, one
   cools after energy loss.
```

So the stripped matrix model has not yet shown the desired robust mechanism:

```text
energy loss -> smaller clump -> hotter clump.
```

But it has also not failed decisively. The crude clump split and escape
detector may be too naive.

## Important Caveat

The diagnostic uses radial eigenvectors of:

```text
R^2 = sum_a X_a^2
```

to define an approximate escaper and clump. That is not the same as a clean
joint-eigenvalue decomposition.

For a real matrix-clump claim, we need a better separation diagnostic:

```text
1. approximate simultaneous diagonalization;
2. off-diagonal mass/connectivity to the candidate escaper;
3. persistence of separation, not just threshold crossing.
```

The current diagnostic may confuse internal shape fluctuations with genuine
eigenvalue escape.

## Current Judgment

This branch is alive but unproven.

The encouraging part:

```text
matrix dynamics gives a non-imposed notion of size/separation.
```

The warning:

```text
the stripped commutator-squared model does not immediately reproduce robust
evaporation plus heating.
```

The next useful step is not to run many more random seeds. It is to improve the
definition of "one eigenvalue has escaped" using approximate joint
diagonalization or off-diagonal-mode diagnostics.

