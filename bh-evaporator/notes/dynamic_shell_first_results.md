# Dynamic Shell Evaporator: First Results

## What was implemented

Script:

```text
sim/dynamic_shell_evaporator.py
```

Default output:

```text
sim/data/dynamic_shell_evaporator.npz
```

Summary figure:

```text
dynamic_shell_summary.pdf
```

The model is the Avenue 1 shell-channel kill test:

```text
core shells with dimensions D(E)
convex entropy S(E)
emission weights proportional to exp[S(E_next)-S(E_current)]
fresh binary radiation time bin at each step
pure-state evolution by random Stinespring/isometry blocks
radiation Renyi-2 entropy computed from the complementary core state
```

This is not yet a collision Hamiltonian. It is a unitary channel model with an
explicit density-of-states emission engine.

## Default convex run

Command:

```text
python sim/dynamic_shell_evaporator.py
```

Parameters:

```text
shells = 8
D_max = 64
D_min = 1
curvature = 2
steps = 15
seeds = 3
```

Shell dimensions:

```text
64 24 10 5 3 2 1 1
```

Emission probabilities by shell:

```text
0.401 0.433 0.465 0.498 0.531 0.564 0.596
```

Key outputs:

```text
initial energy: 8.000
final energy:   2.687
peak S2_rad:    2.900
S2 peak step:   7
dimension crossing step: 4
mid/early emitted-power ratio: 1.127
low-E/high-E emission-probability ratio: 1.488
```

The radiation Renyi-2 entropy rises and then turns over:

```text
S2_rad =
0.000, 0.610, 1.143, 1.645, 2.110, 2.485, 2.749, 2.900,
2.881, 2.834, 2.751, 2.597, 2.356, 2.085, 1.922, 1.631
```

Mean energy decreases:

```text
E(t) =
8.000, 7.645, 7.332, 7.027, 6.699, 6.354, 6.006, 5.627,
5.255, 4.886, 4.499, 4.148, 3.725, 3.378, 2.989, 2.687
```

## Linear-entropy control

Command:

```text
python sim/dynamic_shell_evaporator.py --curvature 1.0 --output sim/data/dynamic_shell_evaporator_linear_control.npz
```

Emission probabilities:

```text
0.498 0.498 0.498 0.498 0.498 0.498 0.498
```

Key outputs:

```text
initial energy: 8.000
final energy:   2.276
peak S2_rad:    3.312
S2 peak step:   7
dimension crossing step: 4
mid/early emitted-power ratio: 0.984
low-E/high-E emission-probability ratio: 1.000
```

## Interpretation

This is a useful first signal.

The Page-like entropy turnover occurs in both the convex and linear cases,
which is expected: Hilbert-space competition alone generically produces the
turnover.

The evaporative acceleration is different. In the convex run, the
density-of-states factor makes emission less suppressed as the core loses
energy:

```text
exp[S(E_next)-S(E_current)] increases along the evaporation path.
```

That produces a rising shell emission schedule. In the linear control the
schedule is flat, and the emitted-power ratio does not show the same
acceleration.

So the first kill test is not a full success yet, but it passes the basic
separation test:

```text
Page-like turnover comes from unitary Hilbert-space competition.
Acceleration comes from convex S(E), i.e. negative microcanonical heat capacity.
```

## Weaknesses

The model is still engineered:

```text
the entropy profile is chosen by hand
the emission map is a random shell channel
there is no time-independent Hamiltonian
there is only one emitted frequency per step
```

The current default run also does not fully evaporate to the final shell by the
last step. It is enough to show turnover and acceleration, but not enough for a
final paper figure.

## Next technical steps

1. Tune parameters so the convex run cleanly evaporates to the final shell
   while keeping memory modest.
2. Add a multi-frequency radiation bin or a collision-Hamiltonian version.
3. Use the linear-entropy control as the baseline comparison in any figure.
