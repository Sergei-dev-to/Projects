# Fixed Floquet Scrambling Before Erosion

## Purpose

Replace the fresh-random local circuit with a fixed local Floquet circuit.

The question:

```text
Did the previous local-scrambling result require redrawing random gates at every
layer, or can one fixed local dynamics mix the shell enough before erosion?
```

## Script

```text
sim/fixed_floquet_before_erosion.py
```

Outputs:

```text
sim/data/fixed_floquet_before_erosion.csv
sim/data/fixed_floquet_before_erosion_summary.csv
sim/data/fixed_floquet_before_erosion_L4check.csv
sim/data/fixed_floquet_before_erosion_L4check_summary.csv
```

Main run:

```text
python sim/fixed_floquet_before_erosion.py --seeds 4
```

`L0 = 4` spot check:

```text
python sim/fixed_floquet_before_erosion.py --seeds 1 --include-L4 \
  --out sim/data/fixed_floquet_before_erosion_L4check.csv \
  --summary-out sim/data/fixed_floquet_before_erosion_L4check_summary.csv
```

## Models Tested

Initial states:

```text
basis_all
uniform_all
factor_haar
```

Floquet layouts:

```text
edge_fixed:
  each neighboring plaquette pair gets one fixed gate, reused every layer.

uniform_fixed:
  the same fixed gate is reused on every neighboring plaquette pair.
```

Gate types:

```text
generic:
  one fixed two-qdit unitary.

flux_conserving:
  one fixed two-qdit unitary block diagonal in total flux mod q.
```

Erosion channels:

```text
shift_minimal
clock_minimal
```

Depths:

```text
D = 0, 1, 2, 4, 8, 16.
```

## Main Result

The fixed-Floquet scrambler works.

The formerly failing product states are repaired by repeated fixed local gates.
This is true for:

```text
edge_fixed generic;
edge_fixed flux_conserving;
uniform_fixed generic;
uniform_fixed flux_conserving.
```

The stricter flux-conserving cases work too, which is the important naturalness
check.

## Representative `L0 = 3`, `d_hard = 2` Results

Previously failing `basis_all + clock`:

```text
floquet       gate            D   maxD   I_pair  S_h/thermal
edge_fixed    flux_conserving 0   0.443   0.000  0.000/0.582
edge_fixed    flux_conserving 1   0.114   2.884  0.578/0.582
edge_fixed    flux_conserving 4   0.040   3.819  0.581/0.582

uniform_fixed flux_conserving 0   0.443   0.000  0.000/0.582
uniform_fixed flux_conserving 1   0.083   2.909  0.573/0.582
uniform_fixed flux_conserving 4   0.062   3.814  0.578/0.582
```

Previously failing `uniform_all + shift`:

```text
floquet       gate            D   maxD   I_pair  S_h/thermal
edge_fixed    flux_conserving 0   0.443   0.000 -0.000/0.582
edge_fixed    flux_conserving 1   0.090   2.235  0.564/0.582
edge_fixed    flux_conserving 4   0.022   3.817  0.581/0.582

uniform_fixed flux_conserving 0   0.443   0.000 -0.000/0.582
uniform_fixed flux_conserving 1   0.139   2.256  0.548/0.582
uniform_fixed flux_conserving 4   0.057   3.664  0.580/0.582
```

For `d_hard = 3`, the same qualitative pattern holds. Depth 4 is generally
enough to bring the hard entropy close to the thermal target and produce
nonzero hard+soft early/late mutual information.

## `L0 = 4` Spot Check

The `L0 = 4`, one-seed check is also positive.

Examples:

```text
initial      floquet       gate            channel  D   maxD   I_pair  S_h/thermal
basis_all    edge_fixed    flux_conserving clock    0   0.443   0.000  0.000/0.582
basis_all    edge_fixed    flux_conserving clock    4   0.013   2.662  0.582/0.582

uniform_all  edge_fixed    flux_conserving shift    0   0.443  -0.000  0.000/0.582
uniform_all  edge_fixed    flux_conserving shift    4   0.006   2.660  0.582/0.582

factor_haar  edge_fixed    generic          clock    0   0.342  -0.000  0.297/0.582
factor_haar  edge_fixed    generic          clock    4   0.003   2.667  0.582/0.582
```

At `L0 = 4`, depth 4 is enough to drive the shell close to locally mixed:

```text
mean shell entropy ~ 3.4
mean shell purity  ~ 0.056.
```

## Interpretation

The previous local-scrambling result was not merely an artifact of redrawing new
random gates at every layer.

One fixed local Floquet circuit can mix the shell enough for the same
structured hard/soft erosion channel to work.

This narrows the assumption again:

```text
old assumption:
  the droplet is Haar-scrambled or random-local-circuit scrambled.

new assumption:
  the droplet has one fixed local chaotic constrained dynamics that locally
  mixes shell variables before erosion.
```

## Naturalness Assessment

This is a real improvement.

What is now less imposed:

```text
the scrambler is fixed rather than redrawn;
it is local on the plaquette grid;
it works with flux-conserving two-site gates;
it repairs the exact product states that previously failed.
```

What remains imposed:

```text
the Floquet gates are still generated randomly;
there is no time-independent Hamiltonian yet;
energy conservation during scrambling is not modeled;
the flux-conserving rule is a toy proxy, not full link-variable gauge dynamics.
```

So the right status is:

```text
fixed local constrained Floquet scrambling is sufficient in small exact tests.
```

Not yet:

```text
a natural Hamiltonian droplet dynamically scrambles and evaporates.
```

## Consequence For The Program

This strengthens the edge-tension droplet story.

The hard/soft radiation result now depends on a much less artificial
scrambling assumption:

```text
local fixed constrained dynamics before erosion.
```

The next naturalness test is no longer "fixed circuit versus random circuit."
That has been passed.

The next test is:

```text
fixed Floquet circuit versus fixed Hamiltonian.
```

Minimum next Hamiltonian target:

```text
H_mix = sum_<ij> h_ij
```

where `h_ij` is a local flux-conserving two-plaquette term. Evolve by:

```text
U(t) = exp(-i H_mix t)
```

before each erosion step, and repeat the same diagnostics.

