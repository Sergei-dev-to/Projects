# Fixed High-Rank Channel Probe: Results

## Why this test was needed

The re-randomized shell-channel model worked, but was too loose.

The naive Hamiltonian model failed because a one-channel transition

```text
X_m: C^{D_m} -> C^{D_{m+1}}
```

has large dark subspaces when `D_{m+1} < D_m`.

The intermediate question was:

```text
Can a fixed high-rank emission map reproduce the convex/control separation
without redrawing randomness at each step?
```

## What was implemented

Script:

```text
sim/fixed_high_rank_shell_channel.py
```

For each seed, the script pre-generates one fixed Stinespring map per shell and
reuses it throughout the run.

Each shell map has the form:

```text
H_m -> H_m tensor |0>
     + H_{m+1} tensor |1>
     + ...
     + H_{m+1} tensor |M_m>
```

The emitted labels increase the effective rank:

```text
C^{D_m} -> C^{D_{m+1}} tensor C^{M_m}
```

The radiation Renyi-2 entropy is still computed from the emitted time-bin
state. It is not inserted by hand.

## Default rank-adaptive run

Convex run:

```text
dims:      32 14 7 4 2 2 1 1
channels:  3  2 2 2 1 2 1
nominal p_emit: 0.441 -> 0.604
final energy:   3.895
peak S2_rad:    2.745 at step 4
acceleration ratio: 0.987
```

Linear control:

```text
dims:      32 20 12 7 4 3 2 1
channels:  2  2  2 2 2 2 2
nominal p_emit: flat at 0.523
final energy:   3.830
peak S2_rad:    3.076 at step 5
acceleration ratio: 1.001
```

This default case evaporates and gives a Page-like turnover, but it does not
clearly separate convex from linear in the acceleration diagnostic.

## Stronger convexity

With `curvature = 3`, rank-adaptive channels give:

```text
nominal p_emit: 0.364 -> 0.632
final energy:   4.182
peak S2_rad:    2.405 at step 4
acceleration ratio: 1.159
```

With lower overall rate scale:

```text
curvature = 3
rate_scale = 1.0
acceleration ratio: 1.144
```

So stronger convexity produces the expected acceleration signal in fixed maps.

## Fixed-channel confound check

To make sure the effect was not caused by different numbers of emitted labels,
both convex and linear runs were repeated with:

```text
channel-mode = fixed
channels = 3
```

Convex, curvature 3:

```text
nominal p_emit: 0.364 -> 0.632
E(t): 8.000, 7.534, 7.079, 6.580, 6.071, 5.544, 4.994, 4.413, 3.824
P(t): 0.000, 0.466, 0.455, 0.499, 0.509, 0.528, 0.550, 0.582, 0.588
peak S2_rad: 2.360 at step 4
acceleration ratio: 1.112
```

Convex, curvature 2:

```text
nominal p_emit: 0.441 -> 0.604
P(t): 0.000, 0.437, 0.493, 0.503, 0.523, 0.537, 0.562, 0.575, 0.569
peak S2_rad: 2.790 at step 4
acceleration ratio: 1.119
```

Linear control:

```text
nominal p_emit: flat at 0.523
P(t): 0.000, 0.613, 0.525, 0.554, 0.565, 0.572, 0.571, 0.574, 0.559
peak S2_rad: 3.160 at step 4
acceleration ratio: 0.991
```

The fixed-channel comparison is the important result. It shows that the
convex/control separation survives fixed maps when the emission channel is
high-rank enough.

## Interpretation

This probe passes the intermediate test.

It shows:

```text
1. Re-randomization is not essential.
2. High-rank outgoing channel capacity repairs the dark-subspace obstruction.
3. Convex S(E) can control the emission schedule in a fixed channel model.
4. Page-like entropy turnover still comes from the emitted time-bin state.
```

It does not yet show:

```text
a fixed Hamiltonian generates the channel
a natural core Hamiltonian has the required S(E)
a large robust parameter regime exists
```

## Current verdict

The project remains alive.

The failed naive Hamiltonian taught us that a one-channel evaporator is too
rank-limited. The fixed high-rank channel test says the obstruction is not
fatal: if the emitted radiation has enough independent labels, the convex
schedule reappears without redrawing randomness.

The next worthwhile step is therefore:

```text
construct a multi-mode collision Hamiltonian whose short-time Stinespring map
approximates the fixed high-rank channel.
```

That is now a better-defined target than the original naive Hamiltonian.

## Update after density-channel Hamiltonian test

See:

```text
notes/hamiltonian_density_channel_results.md
```

The multi-mode Hamiltonian succeeds in a weak-collision regime:

```text
curvature 3, channels 8, g = 0.5:
  acceleration ratio: 1.138

linear control, channels 8, g = 0.5:
  acceleration ratio: 0.912
```

This supports the fixed-channel interpretation: enough emitted modes plus weak
coupling can realize the convex/control separation in an actual collision
Hamiltonian.
