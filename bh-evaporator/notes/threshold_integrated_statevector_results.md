# Threshold Integrated State-Vector Results

## Purpose

This test makes the larger integration jump:

```text
microscopic hard emissions
+ emitted-energy accumulator
+ threshold-triggered shell transfer
+ soft records
+ visible hard records
+ hidden bath records
```

The specific question is:

```text
Can shell shrinkage be triggered by emitted microscopic quanta inside the
state-vector branch structure, rather than imposed as one shell per cycle?
```

## Setup

Small sparse state-vector diagnostic:

```text
L0 = 3
initial core basis dimension = 2^9 = 512
micro emissions = 8
threshold = 4 emitted-energy units
hard energies = 1 or 2
```

Each microscopic emission appends:

```text
hard bit h in {0,1}
bath purifier bit b = h
energy = 1 + h
```

An accumulator is updated after each emission. Whenever:

```text
accumulator >= threshold
```

the next available shell is transferred from the core register to a soft/shrink
record, and the accumulator is reduced by the threshold.

The shell order is:

```text
L=3 shell -> L=2 shell -> L=1 shell.
```

Scramblers:

```text
margulis
grid
none
```

Three seeds were run for each.

## Important Caveat

This diagnostic computes record entropies of orthogonal branch records, not
full reduced-density entropies.

The earlier integrated state-vector test computed density-matrix entropies at
smaller branch count. This threshold test uses record entropies so that the
branch-dependent accumulator and shell-transfer process can be followed across
`131072` final branches.

So this is a threshold/shrinkage integration test, not a replacement for the
density-matrix Page diagnostics.

## Result

All runs have the same threshold statistics:

```text
final basis terms                  = 131072
mean transferred shells            = 2.63671875
complete evaporation probability   = 0.63671875
```

The threshold distribution at the final emission is:

```text
P(0 shells transferred) = 0
P(1 shell transferred)  = 0
P(2 shells transferred) = 0.36328125
P(3 shells transferred) = 0.63671875
```

Final record entropies:

```text
scrambler   seed   S_soft   S_hard   S_full_rad   S_visible_rad
margulis      0    6.259    5.545     11.149        11.149
margulis      1    6.149    5.545     11.039        11.039
margulis      2    6.241    5.545     11.131        11.131
grid          0    6.258    5.545     11.147        11.147
grid          1    6.117    5.545     11.007        11.007
grid          2    6.176    5.545     11.066        11.066
none          0    3.641    5.545      8.531         8.531
none          1    3.346    5.545      8.236         8.236
none          2    3.381    5.545      8.271         8.271
```

The hard entropy is:

```text
S_hard = 8 ln 2 = 5.545177...
```

because there are eight fair microscopic hard emissions.

Representative `margulis`, seed 0 trajectory:

```text
step  <shells>  P0     P1     P2     P3     S_soft  S_hard
1     0.000     1.000  0      0      0      0.000   0.693
2     0.250     0.750  0.250  0      0      1.417   1.386
3     0.875     0.125  0.875  0      0      3.369   2.079
4     1.063     0      0.938  0.063  0      3.769   2.773
5     1.500     0      0.500  0.500  0      5.043   3.466
6     1.906     0      0.109  0.875  0.016  5.509   4.159
7     2.219     0      0.008  0.766  0.227  5.960   4.852
8     2.637     0      0      0.363  0.637  6.259   5.545
```

## Interpretation

This is the first run where microscopic emitted quanta drive shrinkage through
an accumulator inside the state-vector branch structure.

The important positive result is:

```text
threshold-triggered shell transfer works coherently at the branch level.
```

The scrambling comparison is also meaningful:

```text
margulis/grid:
  higher soft record entropy, around 6.1-6.3.

none:
  lower soft record entropy, around 3.3-3.6.
```

The threshold statistics are independent of scrambler because the emission
energies are independent fair hard bits in this diagnostic. The soft entropy
does depend on scrambling because the shell labels being transferred are
scrambled or unscrambled core data.

## What This Strengthens

This strengthens F15 in the specific place that was still weak:

```text
shrinkage is no longer just scheduled one shell at a time;
it is triggered by accumulated microscopic emissions.
```

It also supports:

```text
F2:
  the update is branch-wise coherent and record-preserving.

F3:
  shells are actually transferred out of the core when the threshold is met.

F7:
  hard microscopic quanta now drive the shrinkage update.
```

## What This Still Does Not Do

This is not yet the final model.

Limitations:

```text
record entropies, not full reduced-density entropies;
hard energies are fair bits, not drawn from the full 2D-box bath spectrum;
only initial scrambling, not branch-dependent scrambling after each shrink;
small L0=3;
no large-L Page curve in this thresholded state-vector run.
```

So the correct claim is:

```text
the microscopic-emission accumulator and threshold shell-transfer mechanism
can be embedded in the integrated finite state-vector architecture.
```

The next stronger test would combine:

```text
threshold accumulator
+ branch-dependent scrambling after shrinkage
+ density-matrix Page diagnostics
```

but that is substantially more expensive.

## Files

Script:

```text
sim/threshold_integrated_statevector_evaporator.py
```

Data:

```text
sim/data/threshold_integrated_statevector_summary.csv
sim/data/threshold_integrated_statevector_margulis_seed0.csv
sim/data/threshold_integrated_statevector_margulis_seed1.csv
sim/data/threshold_integrated_statevector_margulis_seed2.csv
sim/data/threshold_integrated_statevector_grid_seed0.csv
sim/data/threshold_integrated_statevector_grid_seed1.csv
sim/data/threshold_integrated_statevector_grid_seed2.csv
sim/data/threshold_integrated_statevector_none_seed0.csv
sim/data/threshold_integrated_statevector_none_seed1.csv
sim/data/threshold_integrated_statevector_none_seed2.csv
```
