# Track B Tiny Full-Radiation Diagnostic

## Purpose

This test upgrades the Track B area-register model from a reduced core
density-matrix channel to a tiny explicit radiation-history calculation.

The question was:

```text
Does the area-register evaporator produce early/late radiation structure, or
only total core-radiation entropy growth?
```

## Implementation

Script:

```text
sim/area_register_full_radiation_tiny.py
```

Figure:

```text
track_b_full_radiation_tiny.pdf
```

Data:

```text
sim/data/area_register_full_radiation_tiny_summary.csv
sim/data/area_register_full_radiation_tiny_local_sqrt_seed2468.npz
sim/data/area_register_full_radiation_tiny_local_linear_seed2468.npz
sim/data/area_register_full_radiation_tiny_scrambled_sqrt_seed2468.npz
sim/data/area_register_full_radiation_tiny_scrambled_linear_seed2468.npz
```

The model uses a sparse pure-state Stinespring history.

Each basis state is labelled by:

```text
(core sector n, core eigenstate i, early radiation history, late radiation history)
```

Each jump appends an exact transition label:

```text
(n, initial core eigenstate i, final core eigenstate f)
```

to either the early or late radiation history, depending on the time step.

This is more explicit than the reduced Kraus calculation, but it is much more
expensive.

## Parameters

Default tiny run:

```text
n = 3,...,5
q = 2
steps = 24
early/late split = step 12
seed = 2468
pmax = 0.08
sqrt mass gap = 4
linear mass gap = 12
```

Cases:

```text
local removal, sqrt mass
local removal, linear mass
scrambled removal, sqrt mass
scrambled removal, linear mass
```

## Result

The diagnostic did not preserve the Track B acceleration.

```text
case                       mid/early power   peak I2(E:L)   peak S2(core)
------------------------------------------------------------------------------
local, sqrt mass           0.332             3.158          3.006
local, linear mass         0.280             3.172          3.021
scrambled, sqrt mass       0.340             3.155          3.006
scrambled, linear mass     0.281             3.173          3.022
```

The exact tiny model does show nonzero early/late radiation structure under the
Renyi-2 proxy:

```text
I2(E:L) = S2(E) + S2(L) - S2(E union L)
```

but the value is almost the same across local/scrambled shrinkage and
sqrt/linear mass laws.

That means the early/late diagnostic is not yet distinguishing the
black-hole-like thermodynamic setup from the control.

## Interpretation

This is not a refutation of the area-register Kraus result.

The earlier Track B Kraus run used:

```text
n = 4,...,10
steps = 80
```

and found modest acceleration around:

```text
mid / early power ~ 1.12
```

The tiny full-radiation run uses:

```text
n = 3,...,5
```

so the register has very little room to evaporate before reaching the bottom
sector. The final mean area is already close to the floor:

```text
final mean n ~ 3.07-3.09
```

The deceleration is therefore likely a finite-floor effect, or at least cannot
be separated from one in this run.

## Scaling obstruction

A slightly larger exact run was attempted:

```text
n = 3,...,6
steps = 18
```

The sparse reduced-density multiplication for early/late entropy became too
large and attempted an allocation of roughly:

```text
64.5 GiB
```

So exact full-history tracking becomes expensive almost immediately.

This is the first clear technical sign that a serious radiation-structure test
will need either:

```text
1. a compressed radiation label;
2. trajectory sampling;
3. tensor-network/MPS history representation;
4. or a narrower diagnostic than full early/late Renyi-2 entropy.
```

## Verdict

The tiny full-radiation diagnostic is useful, but not yet a positive result.

It says:

```text
1. explicit radiation tracking is feasible only at very small sizes;
2. the tiny exact model shows early/late correlations;
3. those correlations are not discriminating;
4. the tiny model loses the acceleration seen in the larger reduced Kraus run.
```

The current project status should therefore be:

```text
thermodynamic evaporation: yes
radiation-structure evaporation: not yet
```

## Recommended next move

Do not keep pushing exact full-history evolution naively.

The next radiation-structure attempt should use one of two routes:

```text
Route 1: trajectory diagnostic
  sample many quantum-jump histories;
  measure classical early/late correlations of emitted energy/time records.

Route 2: compressed exact diagnostic
  keep only emission-time and emission-energy bins as radiation labels;
  test whether this preserves enough structure to compare sqrt and linear mass
  laws without exploding the Hilbert space.
```

Route 1 is cheaper and probably the better next diagnostic.

