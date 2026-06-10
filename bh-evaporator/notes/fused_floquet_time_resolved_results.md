# Fused Floquet Time-Resolved Results

## Purpose

This diagnostic starts fusing the previously separate ingredients into one
final-candidate run.

It uses the same selected finite Floquet evaporator parameters as the earlier
final scan, but adds time-resolved radiation records. Each microscopic emission
step now carries:

```text
hard bit;
hidden bath purifier bit;
soft shell-transfer record, if a threshold crossing occurs at that step.
```

This makes the early/late radiation split meaningful inside the final model.
The hard-emission probabilities are generated from the microcanonical
golden-rule weights, rather than chosen as a fixed hand-set probability.

## Setup

Script:

```text
sim/fused_floquet_time_resolved_scan.py
```

Data:

```text
sim/data/fused_floquet_time_resolved_rows.csv
sim/data/fused_floquet_time_resolved_summary.csv
```

Parameters:

```text
L0 = 3
rate L0 = 20
threshold = 5
micro emissions = 6
scramblers = margulis, grid, none
seed = 0
split step = 3 early emissions + 3 late emissions
```

`L0` is the exact state-vector register size. `rate L0` is the larger
microcanonical scale used to generate hard-emission weights. This separation is
forced by tractability: using the continuum rate formula directly at `L0 = 3`
is too deep in the finite-size regime and drains the mass in a few events.

The run is deliberately narrow. It checks whether the same candidate
architecture can support golden-rule hard weights and time-resolved early/late
diagnostics.

## Result

Corrected run:

```text
cases=3
best_threshold=5
best_emissions=6
p1=0.407->0.407
mean_omega_total=1.737
soft_gap=2.152
old_new_gap=0.631
p_done=0.000
max_terms=32768
```

Detailed rows:

```text
scrambler   <shells>  S_soft  S_hard  I(old:new full rad)  soft-none gap  old-new gap
margulis     1.188    3.515   4.054          2.615             2.147         0.627
grid         1.188    3.525   4.054          2.624             2.157         0.636
none         1.188    1.368   4.054          1.988             0             0
```

Here `old` means the first three emission steps and `new` means the last three
emission steps.

The full-radiation split includes hard bits, hidden bath purifier bits, and
time-resolved soft shell-transfer records.

The hard probability schedule comes from:

```text
Gamma(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

For this six-emission run:

```text
P(hard bit = 1): 0.4065 -> 0.4066
<omega>/T:       1.9878 -> 1.9882
```

## Interpretation

This is the first fused diagnostic where the same finite model contains:

```text
microcanonical/golden-rule weighted hard emissions;
hidden bath purifiers;
energy accumulation;
threshold-triggered shrinkage;
time-resolved soft records;
hard-local thermality;
scrambling comparison;
old/new full-radiation mutual information.
```

The old/new mutual information is present even without scrambling because the
threshold accumulator correlates early and late emissions. Scrambling still
does real work: it increases the full-radiation old/new mutual information by
about `0.63` nats and increases soft record entropy by about `2.15` nats.

This is therefore a useful fused result, but still a small finite diagnostic.

## Weighted-Power Schedule

The same script also writes:

```text
sim/data/fused_floquet_weighted_power_schedule.csv
```

This computes the weighted-power diagnostic:

```text
W_L = boundary * integral d omega
                  omega^d exp[S(M - omega) - S(M)]
```

for `d = 2`, using the same edge-tension entropy curve. Representative values:

```text
L    M^2 W_L       exact/Boltzmann power ratio
3    5414.661      1.7855
8    3232.647      1.0660
20   3062.824      1.0100
40   3040.064      1.0025
```

Thus the large-`L` weighted power approaches:

```text
M^2 W_L = constant,
```

which is the discrete diagnostic form of:

```text
P ~ M^-2.
```

## Caveats

The run is not yet a robust final demonstration:

```text
L0 = 3;
one seed;
six microscopic emissions;
compact two-bin hard spectrum in the exact state-vector run;
rate generation evaluated at a larger representative `rate L0 = 20`;
no complete evaporation in the selected trajectory;
driven/stroboscopic cycle rather than simple time-independent Hamiltonian.
```

The result closes two concrete gaps under the Floquet toy-model standard:

```text
early/late radiation correlations are computed in the same final-candidate
model;

hard weights and the power law are tied to the microcanonical state-count
ratio rather than a fixed hand-set thermal probability.
```

## Next Fusion Step

The remaining useful fusion target is a larger version of this same diagnostic:

```text
more seeds;
longer trajectories;
larger hard alphabet;
closer alignment between the state-vector register size and the rate-generation
scale.
```
