# Faithful Purification Program

## Goal

The target result is not a microscopic black-hole model.

The target is:

```text
a non-gravitational quantum evaporator that reproduces the black-hole
phenomenology checklist as a controlled quantum system.
```

The current strongest thermodynamic candidate is Track E:

```text
variable-length local spin chain
H_n = (C^2)^n
S_n = n log 2
M_n ~ sqrt(n)
matrix-element-derived emission
robust acceleration for sqrt mass
linear-mass and scrambled controls
```

The missing foundation is:

```text
faithful purifiable radiation dynamics.
```

## What "Faithful" Means

The reduced Track E channel evolves core density blocks:

```text
rho_n -> rho'_n
```

using transition rates:

```text
Gamma^{(n)}_{f i}
```

for jumps:

```text
|n,i> -> |n-1,f>.
```

A radiation-tracking model is faithful only if tracing the radiation gives the
same reduced core channel:

```text
Tr_R[ U (rho_C \otimes |0><0|_R) U^\dagger ] = E(rho_C).
```

If a compression changes this reduced channel, it is not evidence for the
original evaporator. This is why the naive energy-bin compression failed.

## Exact Stinespring Dilation

For each sector `n`, define no-jump amplitudes:

```text
s_i = sqrt(1 - sum_f Gamma^{(n)}_{f i})
```

and jump amplitudes:

```text
j_{f i} = sqrt(Gamma^{(n)}_{f i}).
```

The isometry maps:

```text
|n,i>|vac>
  ->
  s_i |n,i>|no jump>
  + sum_f j_{f i} |n-1,f>|n,i,f>.
```

Radiation labels:

```text
|no jump>
|n,i,f>
```

are orthogonal.

Tracing radiation gives exactly:

```text
rho'_{n,ij} = s_i s_j rho_{n,ij}
```

for no-jump evolution, and

```text
rho'_{n-1,ff} += sum_i Gamma^{(n)}_{f i} rho_{n,ii}
```

for jumps.

This is exactly the reduced Track E channel currently simulated.

## Why Exact Labels Matter

If two different transitions are assigned the same radiation label, their
amplitudes interfere:

```text
(i -> f) and (i' -> f')
```

are no longer orthogonal radiation records.

That changes the reduced core channel.

Therefore:

```text
coarse labels cannot be merged at the amplitude level
unless the resulting channel is revalidated against the original reduced
channel.
```

## Milestones

### Milestone 1: F2 -> Y

Show the Track E thermodynamic evaporator has a faithful Stinespring
purification.

Deliverables:

```text
1. exact isometry definition;
2. small-system numerical validation;
3. reduced-vs-purified errors for energy, area, emitted power, and core rho;
4. note explaining why this preserves the thermodynamic Track E result.
```

This does not require large full-radiation simulations.

### Milestone 2: Minimal Radiation Structure

Use the faithful exact-label model only as far as feasible.

Compute selected-time:

```text
S2(core)
S2(early)
S2(late)
I2(early : late)
```

The goal is not yet a full Page curve; it is to see whether exact labels can
reach any size where sqrt/linear or local/scrambled cases differ.

### Milestone 3: Scalable Quantum Radiation

If exact labels fail by branch explosion, move to a representation that
preserves faithfulness:

```text
1. tensor-network / MPS radiation history;
2. random-phase Stinespring embedding validated against the reduced channel;
3. collision model with small radiation bins whose channel is fitted to the
   same Gamma rates and validated.
```

The constraint remains:

```text
trace radiation -> original Track E core channel.
```

### Milestone 4: Full Phenomenology

Only after F2 is solid should we aim for:

```text
Page turnover;
early/late radiation correlations;
same model preserving thermodynamic acceleration.
```

## Current Recommendation

Milestone 1 has now been tested.

Validation script:

```text
sim/spin_chain_stinespring_faithfulness.py
```

Data:

```text
sim/data/spin_chain_stinespring_faithfulness_summary_n5.csv
sim/data/spin_chain_stinespring_faithfulness_timeseries_n5.csv
```

Small validation run:

```text
n = 4,...,5
steps = 12
seed = 2468
operators = boundary, scrambled
mass laws = sqrt, linear
```

Result:

```text
case                 max relative rho error   max energy error   max branches
----------------------------------------------------------------------------
boundary sqrt        3.546e-16                3.553e-15          6176
boundary linear      5.127e-16                1.421e-14          6176
scrambled sqrt       7.773e-16                7.105e-15          6176
scrambled linear     4.813e-16                1.421e-14          6176
```

So the exact-label Stinespring construction is faithful.

An earlier incorrect version recorded only jump labels and omitted per-step
no-jump labels. That gave order-one errors because histories with the same
jumps at different times were merged coherently. The corrected construction
records a radiation outcome at every time step:

```text
(step, n, -1, -1)      no jump
(step, n, i, f)        jump i -> f
```

The no-jump label is common across `i` inside a sector so the no-jump Kraus
preserves the correct intra-sector coherence.

## Updated Status

This moves:

```text
F2: unitary or purifiable evaporation
```

to:

```text
Y in construction, validated at small size.
```

It does not solve the radiation-structure problem.

The corrected exact-label construction grows quickly:

```text
n = 4,...,6, steps = 16
```

already exceeded the default branch cap:

```text
2,187,328 branches > 2,000,000 cap
```

So exact labels are a proof and a small diagnostic, not the scalable route to
Page/early-late physics.

## Revised Next Step

The remaining hard cells are:

```text
F8: Page-like radiation entropy in the same model
F9: early/late quantum radiation structure
```

The faithful construction tells us the right constraint for any scalable
method:

```text
it must reproduce the exact-label channel after tracing radiation.
```

The next viable routes are:

```text
1. exact-label selected-time diagnostics, pushing only as far as branch count
   permits;
2. tensor-network representation of the exact-label isometry;
3. a deliberately designed sequential isometry with smaller radiation bins,
   but validated against the same reduced core channel.
```
