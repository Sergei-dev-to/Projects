# Outgoing Phase-Space Criterion Stress Test

## Purpose

The candidate mechanism is:

```text
P(t) = <W>_t
W_i = sum_f Gamma_{f i} omega_{f i}
```

or, for the coherent shell channel:

```text
W = H_core - E_channel^*(H_core)
P(t) = Tr rho(t) W.
```

The useful question is not whether this identity holds inside a secular
channel. It does by construction.

The useful question is:

```text
Does the same W diagnostic classify the successful and failing cases across
the scans?
```

If yes, then the project has a real technical spine:

```text
acceleration is controlled by increasing outgoing weighted phase space along a
shrinking trajectory.
```

## Implementation

Scripts:

```text
sim/phase_space_criterion_stress_test.py
sim/shell_phase_space_diagnostic.py
```

Figure:

```text
phase_space_criterion_stress_test.pdf
```

Data:

```text
sim/data/phase_space_criterion_stress_test.csv
sim/data/phase_space_criterion_stress_summary.csv
sim/data/shell_phase_space_diagnostic.csv
```

The stress test covers:

```text
Track B area-register scan:
  28 corrected wide-passband rows
  sqrt mass cases and linear mass controls
  local and scrambled shrinkage
  seeds 2468 and 2469

Track A variable-N Bose-Hubbard Kraus scan:
  36 rows
  mu in {5,6,7}
  max emitted gap in {3,4,5}
  two initial windows
  seeds 2468 and 2469

Engineered Hamiltonian shell:
  convex shell schedule
  linear shell control
```

## Result: Track A and Track B scans

Across the 64 Track A/B scan rows:

```text
group                    rows   sign match   correlation
---------------------------------------------------------
area register             28    28/28        0.9998
variable-N Bose-Hubbard    36    36/36        0.9994
combined                  64    64/64        0.9995
```

Here "sign match" means:

```text
observed acceleration > 1  iff  W_mid / W_early > 1.
```

Representative cases:

```text
area sqrt:
  observed mid/early power ~ 1.126
  W mid/early              ~ 1.122

area linear control:
  observed mid/early power ~ 0.598-0.906
  W mid/early              ~ 0.604-0.906

variable-N Bose-Hubbard, best:
  observed mid/early power ~ 1.34-1.36
  W mid/early              ~ 1.33-1.35

variable-N Bose-Hubbard, failing:
  observed mid/early power ~ 0.48-0.50
  W mid/early              ~ 0.47-0.49
```

The split is exact at the level of acceleration versus deceleration.

## Result: engineered shell

The Hamiltonian shell channel was checked using the operator form:

```text
W = H_core - E_channel^*(H_core).
```

For a four-seed check:

```text
case      observed power mid/early   W mid/early   peak S2
-----------------------------------------------------------
convex    1.120                      1.125         2.376
linear    0.899                      0.908         3.356
```

So the engineered shell also fits the same classification:

```text
convex shell schedule:
  W increases and emission accelerates.

linear control:
  W decreases and emission decelerates.
```

## What drives W

The stress test also decomposes:

```text
W = jump probability x conditional emitted energy.
```

Patterns:

```text
Track B sqrt area register:
  jump probability increases mildly;
  conditional emitted energy increases mildly.

Track B linear control:
  conditional emitted energy is almost flat;
  jump probability decreases.

Variable-N Bose-Hubbard:
  successful cases often get help from both factors;
  failing cases can have increasing conditional energy but decreasing jump
  probability large enough to dominate.
```

That last point matters. It explains why negative heat capacity or larger
emitted quanta are not sufficient:

```text
if the shrinking map stops coupling efficiently to open channels, power can
still decrease.
```

## Interpretation

This is the strongest result so far.

The paper-grade claim is not:

```text
we built a realistic black hole.
```

It is:

```text
In finite geometry-free evaporators, acceleration is controlled by the
state-averaged outgoing weighted phase space. Negative heat capacity and
shrinking Hilbert space are not sufficient by themselves; they must be paired
with emission matrix elements that make <W> increase along the trajectory.
```

This makes sense of all the failures:

```text
fixed-N Bose-Hubbard:
  no shrinking-sector trajectory into larger W.

tiny exact radiation tracker:
  too close to the floor; W does not increase over the available window.

linear area-register control:
  correct shrinkage but wrong mass/energy schedule; W decreases.

some variable-N parameter rows:
  shrinking exists, but the particle-loss passband/matrix elements do not
  expose enough outgoing weight.
```

## Caveat

Do not oversell the stress test.

In a secular Markov/Kraus model:

```text
P(t) = <W>_t
```

is essentially an identity once `W` is defined from the transition matrix.

The nontrivial content is weaker but still useful:

```text
the same W diagnostic organizes all successes and failures across three model
families, and it identifies which factor fails: jump access or emitted-energy
scale.
```

To strengthen it further, the next step would be to predict the sign of
`W_mid/W_early - 1` from coarse model data before running the full evaporation.

That follow-up has now been run:

```text
notes/sector_phase_space_profile_results.md
```

Result:

```text
Track B is mostly sector-profile acceleration.
Track A is mostly selection-driven acceleration inside shrinking sectors.
```

## Current verdict

This is enough to stop chasing Page curves for now.

The core technical result should be:

```text
geometry-free evaporation accelerates when shrinking dynamics drives the state
into increasing outgoing weighted phase space.
```

The information-theoretic part remains separate:

```text
core-radiation entropy growth follows in the reduced channels;
early/late radiation structure does not come for free.
```
