# Finite-Gauge Evaporation Cycle Results

## Question

Can we put the component diagnostics into one finite-gauge shrink cycle?

The cycle is:

```text
1. start in H_L ~= H_(L-1) tensor H_shell;
2. run microscopic energy-aware boundary emissions;
3. accumulate emitted energy until it reaches Delta M = 4 sigma;
4. move the actual finite-gauge shell factor into a shell record;
5. check hard thermality and reference-information bookkeeping.
```

## Script

```text
sim/finite_gauge_evaporation_cycle.py
```

Output examples:

```text
sim/data/finite_gauge_evaporation_cycle_local.csv
sim/data/finite_gauge_evaporation_cycle_scrambled.csv
sim/data/finite_gauge_evaporation_cycle_local_e2.csv
```

The script currently implements the exact qubit case:

```text
q = 2.
```

## Important Fix

This test exposed a finite-size bug in the shared golden-weight helper:

```text
omega > M
```

was allowed inside hard-bin integration for very small `L`.

That is negligible in the large-`L` diagnostics, but wrong for the exact
`L = 2` cycle. The helper now caps:

```text
omega <= M.
```

## Exact Small Cycle

Use:

```text
q = 2
L = 2
dim H_L = 2^4 = 16
dim H_(L-1) = 2^1 = 2
dim H_shell = 2^3 = 8
Delta M = 4 sigma
```

The automatic threshold rule chooses one microscopic emission:

```text
event 1 p1 = 0.6334
<omega> = 4.0087
T = 1.4427
emitted / DeltaM = 1.0022
```

Results:

```text
variant      D_hard   I(R:hard)   I(R:micro)   I(R:shell)   I(R:allrec)   I(R:core)
local        0.0000     0.0000      1.3863       2.7726        4.1589       1.3863
scrambled    0.0000     0.0000      1.3863       2.7726        4.1589       1.3863
```

The one-emission cycle is too short for local versus scrambled dynamics to
matter, but the bookkeeping works:

```text
hard radiation is locally thermal;
hard radiation alone carries no reference information;
microscopic records carry the emitted-port information;
the finite-gauge shell record carries the lost shell capacity;
the smaller core keeps the remaining capacity.
```

## Forced Two-Emission Stress Test

Forcing two emissions gives:

```text
event 1 p1 = 0.6334, <omega> = 4.0087
event 2 p1 = 0.0000, <omega> = 2.5281
emitted / DeltaM = 1.6342
```

For the local branch:

```text
variant      D_hard   I(R:hard)   I(R:micro)   I(R:shell)   I(R:allrec)   I(R:core)
local        0.0000     0.0000      2.2107       1.9482        4.1589       1.3863
```

This is a stress test, not the physical threshold cycle. The second emission is
already in a tiny remnant-like regime, so the high-energy bin is inaccessible.

## Interpretation

This is the first complete finite-gauge cycle:

```text
microscopic emission block
+ energy threshold
+ exact shell factor H_L -> H_(L-1) tensor H_shell
+ reference-information accounting.
```

It strengthens:

```text
F2: unitary/purifiable cycle;
F3: actual finite-gauge shrink factor;
F8/F9: hard-local/global-record information split through a shrink event.
```

## Limitation

The exact dense simulation only reaches `L = 2`.

At `L = 2`, one emitted quantum already crosses the shell gap:

```text
<omega> ~ Delta M.
```

So this exact full-cycle run does not demonstrate the large-`L` many-small-quanta
regime. The large-`L` many-small-quanta regime is supported by the golden-rule
and boundary-mode diagnostics, but not by this dense full-cycle reference
simulation.

That distinction matters.

## What Remains

To turn this into a stronger result, we need one of:

```text
1. a compressed/analytic information diagnostic that can handle larger L;
2. a tensor-network/sampling version of the cycle;
3. a purely dimension-theoretic Page/random-isometry estimate for large L.
```

The exact finite-gauge cycle works at small size. The next challenge is scaling
the information diagnostic into the large-`L` regime where individual emissions
are genuinely small compared with the shell gap.
