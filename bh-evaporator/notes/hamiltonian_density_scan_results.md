# Hamiltonian Density-Channel Scan Results

## Scan setup

Script:

```text
sim/scan_hamiltonian_density.py
```

Outputs:

```text
sim/data/hamiltonian_density_scan.csv
sim/data/hamiltonian_density_scan.npz
hamiltonian_density_scan.pdf
```

Grid:

```text
curvature = 1, 2, 3
channels = 1, 2, 4, 8
g = 0.3, 0.5, 0.8, 1.2
steps = 48
seeds = 2
```

Diagnostic:

```text
acceleration ratio = mean emitted power in middle third / mean emitted power
in early third.
```

Values above one indicate an accelerating working window.

## Acceleration table

Rows are channel count. Columns are:

```text
g = 0.3, 0.5, 0.8, 1.2
```

### Curvature 1: linear control

```text
channels 1: 0.61 0.36 0.21 0.11
channels 2: 0.76 0.69 0.62 0.43
channels 4: 0.86 0.80 0.70 0.34
channels 8: 0.94 0.93 0.75 0.20
```

No acceleration regime appears.

### Curvature 2

```text
channels 1: 0.49 0.25 0.10 0.03
channels 2: 0.77 0.64 0.56 0.38
channels 4: 0.97 0.97 0.88 0.42
channels 8: 1.03 1.06 0.88 0.30
```

Acceleration appears only at high channel count and weak coupling.

### Curvature 3

```text
channels 1: 0.57 0.29 0.10 0.04
channels 2: 0.89 0.83 0.69 0.41
channels 4: 0.93 0.99 0.95 0.51
channels 8: 1.04 1.17 1.10 0.40
```

This is the clearest regime:

```text
many emitted modes
convex entropy profile
weak to moderate coupling
```

## Points with acceleration ratio above one

```text
curvature 2, channels 8, g 0.3: acceleration 1.033
curvature 2, channels 8, g 0.5: acceleration 1.064
curvature 3, channels 8, g 0.3: acceleration 1.045
curvature 3, channels 8, g 0.5: acceleration 1.172
curvature 3, channels 8, g 0.8: acceleration 1.095
```

## Interpretation

The effect is not a single cherry-picked point, but it is also not broad across
all parameters.

The scan supports a specific regime:

```text
high outgoing channel capacity
convex microcanonical entropy
weak/moderate collision coupling
finite working window
```

The scan also reinforces the failure mode:

```text
one or two emitted channels are rank-limited
strong coupling front-loads emission
linear entropy profiles decelerate
```

## Current verdict

This is enough to justify writing a numerical results section, provided the
claims are scoped carefully:

```text
We do not claim generic Hamiltonian evaporation.
We show an engineered but fixed collision Hamiltonian regime where negative
microcanonical heat capacity controls an accelerating evaporation window while
radiation Renyi-2 entropy is computed from the unitary emission dynamics.
```

Before finalizing figures, rerun the promising points with more seeds:

```text
curvature 2, channels 8, g = 0.3, 0.5
curvature 3, channels 8, g = 0.3, 0.5, 0.8
linear controls at channels 8, g = 0.3, 0.5, 0.8
```
