# Spin-Chain Trajectory Radiation Diagnostic

## Purpose

This is the first intermediate radiation-structure test for Track E.

The exact full-radiation Hilbert-space calculation was too expensive beyond
tiny area-register sizes. This diagnostic therefore samples quantum-jump
trajectories of the variable-length spin-chain evaporator and records coarse
early/late radiation histories.

This is not a full quantum Page-curve calculation.

It answers a cheaper question:

```text
Do the emitted radiation records contain early/late correlations in the same
parameter regime where the thermodynamic evaporator accelerates?
```

## Implementation

Script:

```text
sim/spin_chain_trajectory_radiation.py
```

Data:

```text
sim/data/spin_chain_trajectory_radiation_summary_seed2468.csv
sim/data/spin_chain_trajectory_radiation_summary_seed2469.csv
```

Model:

```text
Track E variable-length spin chain
n = 4,...,10
H_n = (C^2)^n
S_n = n log 2
M_n = alpha sqrt(n) or alpha n
```

The script samples the jump unraveling of the existing reduced channel:

```text
(n, i) -> (n - 1, f)
```

with probabilities taken from the same rate maps used in the Track E
robustness scan.

Each trajectory records:

```text
early emission count
early emitted-energy bin
late emission count
late emitted-energy bin
```

The diagnostic computes the classical mutual information:

```text
I(record_early : record_late)
```

between these coarse early and late radiation records.

## Parameters

```text
seeds = 2468, 2469
trajectories = 10000 per case
steps = 80
early/late split = 40
operators = boundary, bulk, scrambled
mass laws = sqrt, linear
energy bin width = 1.0
```

## Results

```text
seed  operator   mass     accel mid/early   MI(E:L)   normalized MI   final n
--------------------------------------------------------------------------------
2468  boundary   sqrt     1.157             0.589     0.308           5.737
2468  boundary   linear   0.892             0.719     0.318           4.806
2468  bulk       sqrt     1.152             0.567     0.287           5.694
2468  bulk       linear   0.883             0.728     0.322           4.794
2468  scrambled  sqrt     1.078             0.238     0.118           6.806
2468  scrambled  linear   0.937             0.593     0.260           5.089

2469  boundary   sqrt     1.145             0.576     0.303           5.732
2469  boundary   linear   0.907             0.725     0.319           4.793
2469  bulk       sqrt     1.150             0.558     0.280           5.688
2469  bulk       linear   0.906             0.737     0.324           4.787
2469  scrambled  sqrt     1.094             0.245     0.121           6.773
2469  scrambled  linear   0.922             0.596     0.260           5.076
```

## Interpretation

The thermodynamic signal survives in the trajectory sampler:

```text
sqrt mass accelerates;
linear mass decelerates.
```

This agrees with the reduced-density Track E scan.

The early/late radiation records are correlated:

```text
I(record_early : record_late) > 0
```

but this is not yet a black-hole-specific information result. The linear
controls often have larger classical early/late record mutual information than
the sqrt cases, mostly because they evaporate farther and produce broader
coarse trajectory records.

The more meaningful distinction is local versus scrambled removal:

```text
sqrt local boundary/bulk:
  normalized MI ~ 0.28-0.31

sqrt scrambled:
  normalized MI ~ 0.12
```

So local removal carries more early/late trajectory structure in the
black-hole-like sqrt-mass cases. This is consistent with the earlier Track E
result that local removal preserves a stronger favorable W profile than
scrambled removal.

## What This Does Not Show

This does not show:

```text
1. quantum early/late radiation entanglement;
2. Page turnover of the full radiation state;
3. purification of early radiation by late radiation;
4. islands, wormholes, or a microscopic black-hole encoding.
```

It is a classical record diagnostic of the jump process.

## Current Verdict

This route is useful but insufficient.

It gives a scalable way to test emitted-record correlations while preserving
the thermodynamic acceleration signal. However, it does not close the main
radiation-structure gap.

The status is now:

```text
thermodynamic backbone:
  yes, robust in Track E

classical radiation-record correlations:
  yes, measurable and local/scrambled-sensitive

quantum Page/early-late radiation structure:
  still not achieved
```

## Next Step

The next useful step was tested: a compressed exact radiation calculation for
Track E.

Instead of exact transition labels, keep only:

```text
emission/no-emission;
emitted energy bin;
possibly removed spin label.
```

This would retain a quantum radiation Hilbert space while reducing the branch
explosion. It is the next attempt at closing the real gap:

```text
Page-like quantum radiation structure in the same model that has the
thermodynamic backbone.
```

## Compressed Exact Radiation Attempt

Script:

```text
sim/spin_chain_compressed_radiation.py
```

First small run:

```text
n = 4,...,7
steps = 32
pmax = 0.04
seed = 2468
operators = boundary, scrambled
mass laws = sqrt, linear
```

Result:

```text
case                accel mid/early   peak I2(E:L)   max branches
------------------------------------------------------------------
boundary sqrt       0.169             1.721          1839
boundary linear     0.176             1.859          2506
scrambled sqrt      0.111             1.797          1839
scrambled linear    0.071             1.914          2506
```

Probe:

```text
n = 4,...,8
steps = 16
pmax = 0.08
operator = boundary
```

Compressed exact result:

```text
boundary sqrt       accel = 0.749
boundary linear     accel = 0.903
```

But the corresponding reduced Track E channel gives:

```text
boundary sqrt       accel = 1.047
boundary linear     accel = 0.999
```

So the compression is not dynamically faithful.

Reason:

```text
Energy-bin compression does not merely compress the radiation Hilbert space.
It merges different Kraus labels coherently. Distinct microscopic transitions
that should be orthogonal radiation records can now interfere if they land in
the same energy bin.
```

That changes the reduced core dynamics and destroys the acceleration signal.

Verdict:

```text
Naive compressed exact radiation is not acceptable as evidence.
```

To make this route valid, the compressed labels must preserve enough Kraus
distinguishability to reproduce the reduced core channel. That likely means
one of:

```text
1. keep exact transition labels and use tensor-network compression;
2. group labels only after tracing radiation, not at the amplitude level;
3. use random-phase / typical-channel embeddings and verify the reduced core
   dynamics against the original channel;
4. abandon exact pure-state tracking and use trajectory diagnostics for now.
```
