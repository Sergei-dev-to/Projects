# Autonomous Repeated-Cycle Results

## Question

Can we stop hand-scheduling separate diagnostics and run a fixed repeated
evaporation rule?

The fixed step is:

```text
bulk-edge mixing
-> energy-aware boundary emission
-> emitted-energy accumulation
-> if emitted energy exceeds Delta M, apply finite-gauge shell update.
```

This targets the central modularity criticism.

## Script

```text
sim/autonomous_repeated_cycle.py
```

Outputs:

```text
sim/data/autonomous_repeated_cycle_exact_L2.csv
sim/data/autonomous_repeated_cycle_schedule.csv
```

## What Is Fixed

The repeated step uses fixed rules:

```text
1. apply bulk mixer;
2. compute local golden-rule hard-bin weights from current mass;
3. run the energy-aware Hamiltonian emission block;
4. subtract emitted energy;
5. if accumulated emitted energy >= Delta M, move the finite-gauge shell factor
   into the shell record.
```

This is a repeated-interaction process with a threshold rule.

It is not yet:

```text
a single time-independent autonomous Hamiltonian.
```

## Exact State-Vector Cycle

The exact state-vector cycle uses the smallest finite-gauge case:

```text
q = 2
L = 2
dim H_L = 16
dim H_(L-1) = 2
dim H_shell = 8
```

Output:

```text
variant    steps  shrunk  D_hard  I(R:hard)  I(R:micro)  I(R:shell)  I(R:allrec)  I(R:core)
none           1      1  0.0000     0.0000     1.3863     2.7726      4.1589     1.3863
local          1      1  0.0000     0.0000     1.3863     2.7726      4.1589     1.3863
scrambled      1      1  0.0000     0.0000     1.3863     2.7726      4.1589     1.3863
```

The small exact cycle works:

```text
hard radiation remains locally thermal;
hard radiation alone carries no reference information;
the microscopic record carries the port-emission information;
the shell record carries the exact finite-gauge shell capacity;
the core retains the smaller H_(L-1) capacity.
```

At `L = 2`, the cycle shrinks after one emission, so local versus scrambled
mixing does not yet matter.

## Large-L Schedule

The same repeated rule was used at the schedule level for larger `L`, without
dense state-vector information tracking.

Representative output:

```text
L= 2 steps=  1 first_omega/T=2.779 emitted/DeltaM=1.002
L= 5 steps=  3 first_omega/T=2.149 emitted/DeltaM=1.011
L=40 steps= 28 first_omega/T=1.981 emitted/DeltaM=1.013
```

This shows the intended large-`L` behavior:

```text
individual emissions have omega = O(T);
many emissions are needed to reach one shell gap;
the threshold rule becomes a coarse update after many microscopic emissions.
```

## Interpretation

This is the first integrated cycle:

```text
emission + energy accumulation + finite-gauge shell shrinkage
```

under one repeated rule.

It is a stronger result than the previous isolated diagnostics because the
update is no longer manually assembled after the fact.

## What It Fixes

It strengthens:

```text
F2:
  one repeated unitary/purifiable cycle rather than separate channel pieces.

F3:
  exact finite-gauge shell shrinkage is triggered by an energy threshold.

F8/F9:
  hard-local/global-record information split survives through the cycle.
```

## What It Does Not Fix

Still missing:

```text
single time-independent Hamiltonian;
large-L dense information-flow simulation;
local gauge Hamiltonian deriving shell update;
Page curve over many shell cycles.
```

Also, the exact state-vector cycle is only:

```text
L = 2.
```

The large-`L` many-small-quanta behavior is visible in the schedule diagnostic,
not in the full reference-information simulation.

## Current Verdict

This is probably the right level to pause and synthesize.

The project now has:

```text
1. derived thermodynamic scalings;
2. microscopic boundary emission mechanism;
3. golden-rule/canonical/typicality support for emission weights;
4. finite Hamiltonian emission block;
5. exact finite-gauge shell shrink factor;
6. repeated-cycle integration.
```

The remaining issue is not another small module.

The remaining issue is whether we demand:

```text
a single autonomous Hamiltonian and large Page curve
```

or whether the repeated-interaction evaporator is already enough for the
intended non-gravitational control result.
