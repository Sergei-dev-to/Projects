# Candidate Result: Outgoing Phase-Space Acceleration Criterion

## Question

We paused because the project risked becoming a polished story without a hard
result.

The sharper question is:

```text
Can we identify what actually makes the toy evaporator accelerate?
```

The candidate answer is:

```text
emitted power accelerates when the evolving state moves into sectors/states
with larger outgoing weighted phase space.
```

## Diagnostic definition

For a secular evaporator with energy-lowering transitions:

```text
i in sector n  ->  f in sector n-1
```

define:

```text
W_i = sum_f Gamma_{f i} omega_{f i}
```

where:

```text
Gamma_{f i} = one-step transition probability
omega_{f i} = emitted energy
```

Then the instantaneous emitted power is:

```text
P(t) = sum_i p_i(t) W_i
```

So acceleration is not mysterious in the secular models. It happens when the
population distribution `p_i(t)` drifts toward states with larger `W_i`.

This is the more precise version of:

```text
the shrinkage map exposes increasing outgoing weighted phase space.
```

## Implementation

Script:

```text
sim/phase_space_acceleration_diagnostic.py
```

Figure:

```text
phase_space_acceleration_diagnostic.pdf
```

Data:

```text
sim/data/phase_space_acceleration_diagnostic.csv
sim/data/phase_space_area_local_sqrt_seed2468.npz
sim/data/phase_space_area_local_linear_seed2468.npz
sim/data/phase_space_area_scrambled_sqrt_seed2468.npz
sim/data/phase_space_area_scrambled_linear_seed2468.npz
sim/data/phase_space_area_local_sqrt_seed2469.npz
sim/data/phase_space_area_local_linear_seed2469.npz
sim/data/phase_space_area_scrambled_sqrt_seed2469.npz
sim/data/phase_space_area_scrambled_linear_seed2469.npz
sim/data/phase_space_varn_seed2468.npz
sim/data/phase_space_varn_seed2469.npz
```

The diagnostic computes:

```text
state-averaged W_i
jump probability = sum_i p_i sum_f Gamma_{f i}
conditional emitted energy = P(t) / jump_probability
mean sector
```

## Result

The diagnostic separates the successful cases from the controls.

```text
case                         power mid/early   jump mid/early   omega mid/early
--------------------------------------------------------------------------------
area local sqrt seed 2468     1.122             1.043            1.076
area linear seed 2468         0.906             0.907            0.999
area scrambled sqrt 2468      1.122             1.043            1.076
area scrambled linear 2468    0.906             0.907            0.999
variable-N BH seed 2468       1.352             1.096            1.239

area local sqrt seed 2469     1.123             1.045            1.075
area linear seed 2469         0.906             0.907            0.999
area scrambled sqrt 2469      1.123             1.045            1.075
area scrambled linear 2469    0.906             0.907            0.999
variable-N BH seed 2469       1.337             1.094            1.227
```

The split is clean:

```text
sqrt area register:
  outgoing weighted phase space increases;
  acceleration survives.

linear mass control:
  outgoing weighted phase space decreases;
  emission decelerates.

variable-N Bose-Hubbard:
  outgoing weighted phase space increases strongly;
  both jump probability and conditional emitted energy contribute.
```

## Interpretation

This looks like the first genuinely useful result.

It says that the relevant mechanism is not simply:

```text
negative heat capacity
```

or:

```text
shrinking Hilbert space
```

or:

```text
core-radiation entanglement growth
```

by themselves.

The mechanism is:

```text
the state moves through shrinking sectors in such a way that the outgoing
weighted transition volume increases.
```

In formula form:

```text
P(t) = <W>_t,
W_i = sum_f Gamma_{f i} omega_{f i}.
```

Acceleration is:

```text
d<W>_t / dt > 0
```

over the evaporation window.

## Why this matters

This criterion explains several earlier observations:

```text
1. Fixed-N Bose-Hubbard can fail even with a convex DOS:
   the state does not shrink into sectors with larger W_i.

2. Variable-N Bose-Hubbard can succeed:
   particle loss exposes lower-N sectors with larger effective outgoing
   transition weight.

3. Track B succeeds with M ~ sqrt(area):
   shrinking area raises the emitted-energy scale and modestly raises jump
   probability.

4. Track B linear mass control decelerates:
   the conditional emitted energy stays flat while the jump probability drops.

5. Radiation entropy growth is not enough:
   the power law is governed by W_i, not by S2(core) alone.
```

This is closer to a paper-worthy result because it is a checkable criterion
shared across the models.

## Caveats

This is not yet a theorem.

Limitations:

```text
1. The diagnostic is currently secular/rate-level.
2. It does not address coherent recurrences or non-Markovian radiation.
3. It does not derive the transition matrix elements from gravity.
4. It does not give a Page curve or early/late decoding structure.
5. It identifies the mechanism inside the toy models, not a universal law.
```

Still, it is more than a narrative summary:

```text
we can compute W_i from the Hamiltonian/channel data and predict whether the
model accelerates.
```

## Current verdict

This should become the central technical object if the project continues.

Stress-test update:

```text
notes/phase_space_criterion_stress_test.md
```

The criterion was checked across the Track A scan, the Track B scan, and the
engineered shell/control pair. It classified acceleration versus deceleration
in all tested rows.

The paper should not be organized around:

```text
we made a toy black hole
```

but around:

```text
we identify a finite-system acceleration mechanism for geometry-free
evaporators: increasing outgoing weighted phase space along a shrinking
trajectory.
```

Then the three models become evidence for the criterion:

```text
engineered shell:
  designed W_i profile;

variable-N Bose-Hubbard:
  natural shrinking dynamics with increasing W_i;

area register:
  black-hole entropy scaling with increasing W_i for M ~ sqrt(area), but not
  for the linear mass control.
```

This is a better target than chasing a full Page curve right now.
