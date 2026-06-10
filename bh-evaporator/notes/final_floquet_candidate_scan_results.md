# Final Floquet Candidate Scan Results

## Purpose

This scan tests the current final Floquet toy-model target directly:

```text
weighted hard emissions;
hidden bath purifiers;
energy accumulation;
threshold-triggered shell transfer;
full reduced-density entropies;
scrambling comparisons;
small parameter sweep for a readable trajectory.
```

The goal is to see whether the remaining non-gravitational `P/Y-` entries can
be made `Y` for the Floquet toy-model standard, without adding more intermediate
modules.

## Setup

Fixed:

```text
L0 = 3
threshold = 5
scramblers = margulis, grid, none
seed = 0
```

Scanned:

```text
micro emissions = 6, 7
P(hard energy 2) = 0.35, 0.50
```

The visible hard bit has distribution:

```text
P(h=1) = p
P(h=0) = 1-p
```

and the bath purifier records the hard bit. The target hard entropy is:

```text
S_hard,target = n[-p log p - (1-p) log(1-p)].
```

The best readable case was selected by a trajectory score that favors:

```text
large scrambled-vs-none soft entropy gap;
nontrivial but incomplete evaporation;
hard entropy close to the target.
```

This score is only a scan heuristic, not a physical observable.

## Best Case

Best parameters:

```text
threshold = 5
micro emissions = 6
P(hard energy 2) = 0.35
```

Summary:

```text
mean transferred shells = 1.117
P(complete evaporation) = 0
max basis terms         = 32768
```

Reduced-density results:

```text
scrambler   S_soft   S_hard  S_hard target  hard error   soft-none gap
margulis    2.636    3.885      3.885        8.9e-16       2.274
grid        2.647    3.885      3.885        4.4e-16       2.286
none        0.362    3.885      3.885        4.4e-16       0
```

The hard/bath mutual information is large in all cases:

```text
I(hard : bath) = 6.209
```

which is expected because the hidden bath purifies the visible hard bits.

## Other Scanned Cases

The other cases also preserve hard thermality, but have less readable
trajectories:

```text
threshold  emissions  p     scrambled S_soft   none S_soft   gap
5          6          0.50  ~2.51-2.52        0.643        ~1.87
5          7          0.35  ~2.34             0.691        ~1.65
5          7          0.50  ~1.63             0.535        ~1.10
```

The best case is therefore not a cherry-picked zero-measure point. The
scrambling/no-scrambling separation persists across the small scan.

## Interpretation

This is the cleanest final-candidate diagnostic so far.

It shows, in one finite Floquet toy-model calculation:

```text
1. microscopic hard emissions with nonuniform weights;
2. exact hard-local thermality relative to the chosen hard distribution;
3. hidden bath purification of hard radiation;
4. emitted-energy accumulation;
5. threshold-triggered shell transfer;
6. full reduced-density entropy calculations;
7. scrambling comparisons;
8. soft radiation entropy strongly enhanced by scrambling.
```

The no-scrambling comparison is again decisive:

```text
hard thermality alone does not create soft radiation entropy.
```

This supports the intended model decomposition:

```text
hard radiation:
  locally thermal observer channel.

hidden bath:
  purifier of hard channel.

soft/shrink records:
  carrier of evaporated core information.

scrambling:
  mechanism that makes transferred shell records information-rich.
```

## What This Means For The Requirements

For the non-gravitational Floquet toy-model standard, this pushes the remaining
integrated requirements close to `Y`:

```text
purifiable evaporation              Y-
shrinking internal capacity          Y-
emission weights/dynamics            Y- in finite weighted channel
radiation entropy                    Y- at small size
information-flow diagnostics         Y- at small size
single update architecture           Y- as Hamiltonian-realizable cycle
```

The thermodynamic requirements were already analytic:

```text
S ~ M^2
T ~ 1/M, C < 0
P ~ M^-2 with 2D bath
```

## Remaining Caveats

This is still not the simple time-independent autonomous-Hamiltonian holy
grail.

Limitations:

```text
L0 = 3;
one seed in the final scan;
small finite hard alphabet;
Floquet/repeated-interaction architecture;
not a large clean Page curve;
not a simple time-independent autonomous Hamiltonian.
```

For the finite toy-model target, the result is now coherent:

```text
the non-gravitational Floquet evaporator can realize the mapped BH
phenomenology package in one finite quantum diagnostic, with explicit
comparisons and caveats.
```

## Files

Script:

```text
sim/final_floquet_candidate_scan.py
```

Data:

```text
sim/data/final_floquet_candidate_scan_rows.csv
sim/data/final_floquet_candidate_scan_summary.csv
```
