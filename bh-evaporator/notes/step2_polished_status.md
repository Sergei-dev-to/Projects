# Step 2 Polished Status

## Goal

Step 2 was the minimum worthwhile Hamiltonian target:

```text
fixed collision Hamiltonian
fresh outgoing radiation bins
computed radiation Renyi-2 entropy
negative-C_mu convex/control separation
```

The current implementation is:

```text
sim/hamiltonian_shell_density_channel.py
```

The polished comparison figure is:

```text
step2_hamiltonian_polished.pdf
```

## Best consolidated run

Use:

```text
curvature = 3
channels = 8
g = 0.5
steps = 48
seeds = 12
```

Convex run:

```text
final energy: 5.470
peak S2_rad: 2.360 at step 48
acceleration ratio: 1.115
mean emitted probability: 0.0527
```

Emitted power means:

```text
early third: 0.0475
middle third: 0.0530
late third: 0.0576
```

Linear control:

```text
final energy: 4.210
peak S2_rad: 3.334 at step 35
acceleration ratio: 0.917
mean emitted probability: 0.0790
```

Emitted power means:

```text
early third: 0.0854
middle third: 0.0783
late third: 0.0732
```

This is the cleanest Step 2 result.

## Faster convex variant

Use:

```text
curvature = 3
channels = 8
g = 0.8
steps = 48
seeds = 12
```

Convex run:

```text
final energy: 2.434
peak S2_rad: 2.409 at step 21
acceleration ratio: 1.070
mean emitted probability: 0.1160
```

Emitted power means:

```text
early third: 0.1270
middle third: 0.1359
late third: 0.0850
```

This shows a clearer Page-like turnover but also shows depletion: the power
accelerates in the working window and then falls.

## Marginal cases

Curvature 2, channels 8, `g = 0.5`, seeds 12:

```text
acceleration ratio: 1.020
```

This is basically flat. It should not be used as the headline result.

Curvature 3, channels 8, `g = 0.3`, seeds 12:

```text
acceleration ratio: 1.005
```

This is too slow to be a useful demonstration.

## Interpretation

Step 2 is minimally achieved.

The defensible claim is:

```text
An engineered fixed collision Hamiltonian with sufficiently many outgoing
channels exhibits a weak-coupling working window in which convex
microcanonical entropy drives increasing emitted power, while a linear entropy
control decelerates. The same dynamics gives the radiation Renyi-2 entropy
through the reduced core state.
```

Do not claim:

```text
generic Hamiltonian evaporators accelerate
the model is natural
the full evaporation history is black-hole-like
the effect survives arbitrary coupling
```

## What remains before manuscript use

For the numerical section:

```text
1. Use the 12-seed polished figure.
2. Include the scan heatmap as support.
3. State explicitly that the successful regime is high-channel,
   weak/moderate-coupling, and finite-window.
4. Explain why one-channel Hamiltonians fail: dark subspaces.
5. Keep Step 3, natural core Hamiltonian, as future work.
```

## Verdict

Step 2 is good enough to write around, as long as the paper is framed as:

```text
a minimal geometry-free Hamiltonian control model
```

not:

```text
a natural analogue black hole.
```
