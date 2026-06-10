# Sector-Level Phase-Space Profile Results

## Purpose

The previous stress test showed:

```text
P(t) = <W>_t
```

with:

```text
W_i = sum_f Gamma_{f i} omega_{f i}.
```

That classified acceleration versus deceleration across the existing models.
But it is partly tautological, because `W` is built from the same transition
matrix that defines the emitted power.

The stronger question is:

```text
Can acceleration be predicted from coarse sector structure before tracking the
full state distribution?
```

## Diagnostics

Script:

```text
sim/sector_phase_space_profile.py
```

Figure:

```text
sector_phase_space_profile.pdf
```

Data:

```text
sim/data/sector_phase_space_profile.csv
sim/data/sector_phase_space_profile_summary.csv
```

For each sector, compute:

```text
bar W_n = uniform average of W_i in sector n
```

Then compare:

```text
actual:
  <W>_t = sum_i p_i(t) W_i

sector-only:
  W_sector(t) = sum_n p_n(t) bar W_n
```

Also compute the intrasection selection ratio:

```text
selection(t) = <W>_t / W_sector(t).
```

If `selection(t)` grows, the dynamics is preferentially occupying high-`W`
states inside the sectors.

## Summary result

```text
group                    sector sign   sector corr   structural sign   structural corr   recon corr
---------------------------------------------------------------------------------------------------
area register             1.000         0.681         0.857             0.833             0.939
variable-N Bose-Hubbard    0.556         0.311         0.556             0.214             0.267
combined                  0.750         0.377         0.688             0.314             0.561
```

Definitions:

```text
sector sign:
  whether W_sector mid/early correctly predicts acceleration vs deceleration

structural sign:
  whether mean lower-sector W / initial-sector W predicts acceleration

recon corr:
  correlation between <W>_t and W_sector(t) along each trajectory, averaged
  across rows
```

## Interpretation

This gives a useful split.

Track B area register:

```text
mostly sector-level
```

The sector-only reconstruction works well:

```text
mean reconstruction correlation ~ 0.94
sector sign classification = 28/28
```

So in Track B, the acceleration is mainly explained by the coarse shrinking
area-register profile. This matches the earlier observation that local and
scrambled shrinkage behave almost identically.

Track A variable-N Bose-Hubbard:

```text
not sector-level
```

The sector-only reconstruction is poor:

```text
mean reconstruction correlation ~ 0.27
sector sign classification = 20/36
```

In fact, the uniform lower-sector profile usually goes the wrong way:

```text
mean lower-sector W / initial-sector W ~ 0.57
```

Yet many rows still accelerate. Therefore Track A acceleration is not simply
because lower particle-number sectors have larger average outgoing phase
space.

It comes from intrasection selection:

```text
the particle-loss dynamics preferentially moves the state into high-W
subregions inside the lower-N sectors.
```

Representative Track A mismatches:

```text
observed acceleration   sector-only W   selection ratio   parameters
---------------------------------------------------------------------
1.364                   0.861           1.565             mu=6, gap=4, init=[-18.5,-17]
1.229                   0.765           1.559             mu=6, gap=3, init=[-20,-18]
1.324                   0.953           1.385             mu=5, gap=3, init=[-18.5,-17]
```

This is important. It means the natural many-body model contains a genuinely
dynamical selection effect that is absent from the coarse area-register
picture.

## Transition-bias check

A further diagnostic checks whether one jump from a uniform source sector lands
preferentially in high-`W` states of the destination sector.

Script:

```text
sim/transition_bias_diagnostic.py
```

Data:

```text
sim/data/transition_bias_diagnostic.csv
sim/data/transition_bias_diagnostic_summary.csv
```

Result:

```text
group                    mean transition bias   range
------------------------------------------------------
area register             0.937                  0.681-0.999
variable-N Bose-Hubbard    1.265                  1.045-2.236
```

So the variable-N Bose-Hubbard transitions are generally biased toward
above-average future-`W` states. That supports the selection interpretation.

But transition bias alone does not classify acceleration:

```text
correlation with observed acceleration:
  area register          0.796
  variable-N Bose-Hubbard -0.633
```

The reason is that selection bias is necessary but not sufficient. A row can
land in relatively high-`W` states and still decelerate if the sector profile,
jump probability, or passband suppresses the total outgoing weight.

## Current understanding

There are two acceleration mechanisms in the project:

```text
1. Sector-profile acceleration
   lower/shrinking sectors have larger coarse outgoing W.
   This is Track B.

2. Selection-driven acceleration
   lower sectors do not have larger uniform W, but the dynamics selects
   high-W states inside them.
   This is Track A.
```

The engineered shell model is closer to the first mechanism, because the
profile is imposed.

## Why this matters

This result makes the project less tautological.

The earlier statement:

```text
acceleration means <W> increases
```

is almost definitional.

The refined statement is stronger:

```text
In the area-register model, acceleration is predictable from the coarse
shrinking-sector W profile.

In the variable-N Bose-Hubbard model, acceleration is not predictable from
sector dimensions or sector-averaged W. It depends on transition-induced
selection of high-W states inside the shrinking sectors.
```

That is a real distinction between the abstract entropy-correct model and the
natural many-body model.

## Paper implication

The paper should not present one universal explanation at the wrong level.

Better:

```text
Outgoing weighted phase space is the common diagnostic.

Different models make <W> increase in different ways:
  engineered shell: imposed profile;
  area register: coarse sector profile from M ~ sqrt(area);
  variable-N Bose-Hubbard: matrix-element-driven intrasection selection.
```

This is currently the best technical spine of the project.

