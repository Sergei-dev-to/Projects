# Structured Erosion Channel Results

## Purpose

Test F13:

```text
local/structured erosion vs scrambled erosion controls.
```

The previous Level 2 channel used Haar-random shell unitaries:

```text
V |psi> = sum_h sqrt(p_h) |h>_hard U_h |psi>_soft.
```

That showed the hard/soft information split, but random `U_h` could have been
doing too much work.

This diagnostic replaces random `U_h` with structured shell-flux maps.

## Script

```text
sim/structured_erosion_channel.py
```

Outputs:

```text
sim/data/structured_erosion_channel.csv
sim/data/structured_erosion_channel_summary.csv
```

## Models

### random_minimal

Baseline Level 2:

```text
U_h = Haar-random unitary on H_shell.
```

### shift_minimal

Structured shell map:

```text
U_h = cyclic shift by h on shell flux labels.
```

### clock_minimal

Structured shell map:

```text
U_h = diagonal clock phase exp(2 pi i h a / D_shell).
```

### flux_partition

Deterministic shell readout:

```text
|a>_shell -> |h = f(a)>_hard |a>_soft,
```

with partition sizes chosen to approximate the target thermal hard
distribution.

All models use minimal soft capacity:

```text
dim H_soft = dim H_shell.
```

## Scan

Command:

```text
python sim/structured_erosion_channel.py --seeds 8
```

Configurations:

```text
L0 = 3, d_hard = 2,3
L0 = 4, d_hard = 2
q = 2
8 seeds each
```

## Summary

```text
model            L0 d_h maxD    I_hh    I_pair  S_latest/thermal
clock_minimal     3   2  0.025  0.0009   3.856   0.581/0.582
clock_minimal     3   3  0.028  0.0024   3.856   0.831/0.832
clock_minimal     4   2  0.002  0.0000   2.679   0.582/0.582
flux_partition    3   2  0.033  0.0008   3.856   0.562/0.582
flux_partition    3   3  0.047  0.0035   3.856   0.890/0.832
flux_partition    4   2  0.020  0.0000   2.679   0.562/0.582
random_minimal    3   2  0.041  0.0007   3.856   0.578/0.582
random_minimal    3   3  0.060  0.0020   3.856   0.821/0.832
random_minimal    4   2  0.050  0.0000   2.679   0.575/0.582
shift_minimal     3   2  0.025  0.0007   3.856   0.582/0.582
shift_minimal     3   3  0.029  0.0022   3.856   0.831/0.832
shift_minimal     4   2  0.002  0.0000   2.679   0.582/0.582
```

Definitions:

```text
maxD:
  maximum trace distance between latest hard bin and target thermal marginal.

I_hh:
  final mutual information between first and latest hard bins.

I_pair:
  final mutual information between first and latest hard+soft emitted pairs.
```

## Interpretation

The structured maps reproduce the desired hard/soft pattern.

Most important:

```text
1. shift_minimal and clock_minimal keep hard bins as close to thermal as the
   random baseline, often closer;
2. hard-hard early/late mutual information remains near zero;
3. hard+soft early/late mutual information remains clearly nonzero;
4. minimal soft capacity is still enough.
```

This means:

```text
the hard/soft information split is not purely an artifact of Haar-random
scrambling.
```

Simple shell-flux operations can produce the same qualitative behavior.

## Why Shift/Clock Work

For a typical state of the full droplet, the shell subsystem is close enough to
locally mixed that nontrivial shell unitaries have small overlaps in the hard
off-diagonal terms:

```text
rho_hh' ~ sqrt(p_h p_h') Tr(rho_shell U_h^dagger U_h').
```

For shift/clock operations:

```text
Tr(U_h^dagger U_h') = 0
```

when `h != h'` in the ideal shell space.

So the hard marginal becomes close to diagonal/thermal without needing random
unitaries.

## Flux Partition Result

The deterministic flux partition is more literal:

```text
hard bin = coarse shell-flux observable.
```

It also keeps hard-hard mutual information near zero and hard+soft pair
correlations nonzero, but its latest hard entropy can deviate more from the
thermal target because the hard distribution depends on the actual shell state
and finite partition sizes.

This is expected.

## What This Improves

F13 can move from:

```text
N
```

to:

```text
P
```

because we now have structured-vs-random erosion controls.

It is not `Y` yet because:

```text
1. shift/clock maps are structured shell maps, not derived local Hamiltonian
   boundary erosion;
2. there is no explicit link/vertex update with Gauss matching yet;
3. hard probabilities are still chosen, not derived from boundary matrix
   elements and a bath.
```

## Current Status

The model no longer depends on fully random shell scrambling for the hard/soft
information split.

The next natural target is:

```text
boundary-local plaquette/link erosion with Gauss matching.
```

But the structured control already shows:

```text
simple gauge-flux shell operations can reproduce the same hard/soft behavior
as the random minimal-soft channel.
```

