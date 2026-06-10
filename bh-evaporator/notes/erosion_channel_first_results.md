# Erosion Channel First Results

## Purpose

Test whether the hard/soft erosion channel can do more than bookkeeping.

Script:

```text
sim/erosion_channel_diagnostic.py
```

Outputs:

```text
sim/data/erosion_channel_diagnostic.csv
sim/data/erosion_channel_diagnostic_L4.csv
```

## Models Compared

### Level 1 archive

```text
V |a> = sum_h sqrt(p_h) |h>_hard |a,h>_soft
```

Properties:

```text
hard radiation exactly thermal;
soft register stores shell label and hard label;
oversized soft archive.
```

### Level 2 minimal soft

```text
V |psi> = sum_h sqrt(p_h) |h>_hard U_h |psi>_soft
```

where `U_h` are random unitaries.

Properties:

```text
dim H_soft = dim H_shell;
no oversized archive;
hard thermality comes from decoupling/random-unitary suppression of
coherences.
```

## L0 = 4 Result

Command:

```text
python sim/erosion_channel_diagnostic.py --L0 4 --q 2 --d-hard 2 --seed 20260531 --out sim/data/erosion_channel_diagnostic_L4.csv
```

Output summary:

```text
model             L->  S_core  S_hard  S_soft  S_hard_latest  D_hard  I_hh    I_pair
level1_archive     4->3    4.730   0.582   5.312         0.582 4.16e-16   0.000   0.000
level1_archive     3->2    2.771   1.164   3.935         0.582 9.44e-16   0.000   5.417
level1_archive     2->1    0.693   1.747   2.440         0.582 8.33e-16  -0.000   2.681
level2_minimal     4->3    4.730   0.582   4.778         0.582 0.00391   0.000   0.000
level2_minimal     3->2    2.771   1.163   3.929         0.581  0.0279   0.000   5.417
level2_minimal     2->1    0.693   1.742   2.435         0.579  0.0389   0.000   2.681
```

Here:

```text
D_hard = trace distance of the latest hard bin from the target thermal state.
I_hh   = mutual information between first and latest hard bins.
I_pair = mutual information between first and latest hard+soft emitted pairs.
```

## Interpretation

The Level 2 minimal-soft channel behaves as hoped in this small test:

```text
1. latest hard radiation is close to thermal;
2. hard-hard early/late mutual information is essentially zero;
3. hard+soft early/late mutual information is nonzero;
4. global evolution remains a pure isometry;
5. soft capacity is minimal, not enlarged by a hard-label archive.
```

The key qualitative pattern is:

```text
hard radiation alone looks thermal and information-poor;
hard+soft radiation carries the correlations.
```

This is the desired black-hole-like hard/soft split.

## What This Does Not Prove

This is still not local Hamiltonian erosion.

The Level 2 channel uses random unitaries:

```text
U_h : H_shell -> H_soft.
```

So the result proves:

```text
minimal-soft Stinespring channels can realize the desired information split.
```

It does not yet prove:

```text
a local gauge-boundary erosion dynamics naturally produces that channel.
```

## Status Update

The erosion channel now moves:

```text
F9 early/late radiation correlations
```

from:

```text
N
```

to:

```text
P
```

provided we count hard+soft radiation, not hard radiation alone.

This is physically reasonable for the model:

```text
hard radiation = thermal energy carrier;
soft radiation = gauge/edge record needed for purification.
```

## Next Step

The next diagnostic should test robustness:

```text
1. scan seeds;
2. scan L0 = 3,4, maybe 5 if feasible;
3. scan hard dimension d_h;
4. compare random-unitary Level 2 with a structured/local shell map;
5. compute Page-like entropy profiles using several initial states.
```

The most important upgrade is:

```text
replace random U_h with boundary-local gauge moves.
```

