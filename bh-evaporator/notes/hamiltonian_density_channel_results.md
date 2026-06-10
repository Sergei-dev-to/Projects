# Hamiltonian Density-Channel Results

## Why this script was added

The explicit pure-state Hamiltonian simulation stores:

```text
core x emitted-radiation-history
```

so multi-mode runs become expensive quickly.

For a collision unitary with each fresh radiation bin initialized in `|0>`,
the reduced core evolves by Kraus operators:

```text
K_a = <a| U |0>
rho_core -> sum_a K_a rho_core K_a^\dagger
```

Since the global core+radiation state is pure, the radiation Renyi-2 entropy is
equal to the core Renyi-2 entropy:

```text
S2_rad = -log Tr rho_core^2
```

So this reduced-density simulation still computes the relevant entropy exactly,
but avoids storing the full radiation history.

Script:

```text
sim/hamiltonian_shell_density_channel.py
```

## Main result

The many-mode Hamiltonian gives the desired convex/control separation in a
weak-collision regime.

### Convex, curvature 3, channels 8, g = 0.5

```text
final energy: 5.468
peak S2_rad: 2.341 at final simulated step
acceleration ratio: 1.138
mean emitted probability: 0.053
```

Emitted power:

```text
early: 0.046, 0.046, 0.046, 0.046, ...
late:  0.058, 0.058, 0.058, 0.058, ...
```

This is a slow but clean accelerating window.

### Linear control, channels 8, g = 0.5

```text
final energy: 4.190
peak S2_rad: 3.360 at step 35
acceleration ratio: 0.912
mean emitted probability: 0.079
```

Emitted power decays:

```text
early: 0.095, 0.093, 0.092, 0.090, ...
late:  0.073, 0.072, 0.071, 0.069, ...
```

The linear control evaporates, but does not accelerate.

## Stronger coupling

With `g = 0.8`, curvature 3 still shows an accelerating early/mid window:

```text
final energy: 2.394
peak S2_rad: 2.394 at step 22
acceleration ratio: 1.080
```

But the curve later decelerates as the core nears depletion:

```text
early: 0.114, 0.113, 0.113, 0.114, ...
mid:   0.128, 0.131, 0.134, ...
late:  0.073, 0.070, 0.067, 0.064, ...
```

The matching linear control has:

```text
acceleration ratio: 0.738
```

So the convex/control distinction remains, but the successful interpretation is
not "power rises forever." It is:

```text
negative heat capacity produces an accelerating working window before finite
depletion effects take over.
```

## Curvature 2

The weaker convex profile gives a weaker signal.

With `g = 0.5`:

```text
acceleration ratio: 1.056
```

With `g = 0.8`:

```text
acceleration ratio: 0.900
```

So curvature 2 is marginal and coupling-dependent, while curvature 3 is the
cleaner demonstration regime.

## Interpretation

This is the first positive Hamiltonian result.

It shows:

```text
1. A fixed collision Hamiltonian can generate Page-like entropy turnover.
2. With enough emitted modes and weak coupling, convex S(E) produces an
   accelerating evaporation window.
3. Linear controls evaporate but do not show the same acceleration.
4. The naive one-channel failure was indeed a channel-capacity problem.
```

It also shows a limitation:

```text
strong coupling front-loads emission and washes out the negative-C schedule.
```

The correct regime is weak-collision / many-mode / finite working window.

## Current status

This is now close to the minimum worthwhile technical result, but not yet a
paper-ready numerical section.

Before using it in the manuscript, we still need:

```text
parameter scans over g, channel count, and curvature
error bands over more random seeds
a clean figure comparing convex and linear controls
a careful statement that the acceleration is a working-window effect
```

But the project no longer rests only on a Stinespring shell channel. There is
now a fixed Hamiltonian collision model that exhibits the desired separation in
a controlled regime.
