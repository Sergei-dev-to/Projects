# Detached-Qubit C2 Results

## Purpose

C2 tries to combine:

```text
C1 explicit emitted radiation qubits
```

with:

```text
Track E energy-filtered, probabilistic emission.
```

The intended one-step structure is:

```text
no emission:
  H_n -> H_n tensor |no emission>

emission:
  H_n -> H_(n-1) tensor |detached qubit, energy label>
```

Transition weights use:

```text
Gamma_{f b, i}
  ~ |<n-1,f; b | detach | n,i>|^2 J(omega_{f i})
```

with:

```text
omega_{f i} = E_{n,i} - E_{n-1,f}.
```

## Implementation

Script:

```text
sim/detached_qubit_c2.py
```

Design note:

```text
notes/option_c2_energy_filtered_design.md
```

Data:

```text
sim/data/detached_qubit_c2_summary_n5.csv
sim/data/detached_qubit_c2_summary_n6_compressed.csv
```

Two radiation-label modes:

```text
exact:
  label includes (step, n, i, f, detached qubit, energy bin)

compressed:
  label includes (step, n, detached qubit, energy bin)
```

Full early/late entropies are computed only at selected steps to avoid sparse
density-matrix explosion.

## Results

Small exact/compressed comparison:

```text
n = 4,...,5
steps = 12
operator = boundary
seed = 2468

mode        mass     accel   gamma ratio   epsilon ratio   peak I2(E:L)   branches
----------------------------------------------------------------------------------
exact       sqrt     0.856   0.856         1.000           0.376          12320
exact       linear   0.851   0.851         1.000           0.386          12320
compressed  sqrt     0.844   0.844         1.000           0.521            800
compressed  linear   0.832   0.832         1.000           0.513            872
```

Larger compressed probe:

```text
n = 4,...,6
steps = 16

mode        mass     accel   gamma ratio   epsilon ratio   peak I2(E:L)   branches
----------------------------------------------------------------------------------
compressed  sqrt     0.886   0.873         1.014           1.441          41632
compressed  linear   0.886   0.887         1.000           1.253          53216
```

Exact labels at `n = 4,...,6`, `steps = 16` exceeded the branch cap:

```text
2,781,248 branches > 2,000,000 cap.
```

## Interpretation

This first C2 implementation is not yet successful.

It gives:

```text
explicit radiation bins;
probabilistic emission/no-emission branches;
nonzero early/late radiation structure.
```

But it does not recover the Track E thermodynamic behavior:

```text
power decelerates for both sqrt and linear mass laws;
sqrt and linear are nearly indistinguishable;
epsilon is nearly flat, so the conditional emitted energy does not capture
the intended hotter-as-smaller behavior.
```

The acceleration/deceleration is almost entirely controlled by:

```text
gamma(t)
```

and gamma falls as the state approaches lower sectors / floors.

## Why This Failed

Likely causes:

```text
1. The sector range is too small and floor effects dominate.
2. The global pmax normalization suppresses lower-sector emission instead of
   producing a black-hole-like rate profile.
3. Boundary-detached qubit labels do not preserve enough transition
   distinguishability to maintain Track E's favorable W profile.
4. The passband and initial-state choice are not tuned to keep the trajectory
   in the accelerating window.
```

This is not a fundamental failure of C2, but it shows that the naive version is
not enough.

## Current Verdict

C2 remains the right conceptual route, but the first implementation is a
negative result.

The model currently has:

```text
radiation architecture: yes
probabilistic emission: yes
early/late structure: yes
black-hole-like acceleration: no
sqrt-vs-linear discrimination: weak/no
```

So it is not yet an all-phenomenology evaporator.

## Next Modifications To Consider

The next C2 attempt should not simply scale this version.

Modify the rate model first:

```text
1. sector-normalized pmax:
   normalize emission probabilities separately per n so lower sectors are not
   globally suppressed.

2. BH-inspired target rate:
   rescale each sector so gamma_n ~ 1/sqrt(n), then test whether epsilon_n
   also grows.

3. restore exact Track E W profile:
   choose emission probabilities so that sector-averaged W_n matches the
   successful Track E channel, while radiation labels stay small.

4. larger n with trajectory-only pretest:
   test gamma/epsilon/power before attempting quantum radiation entropies.
```

The cleanest next diagnostic is probably:

```text
C2 rate-profile pretest without radiation entropies.
```

If that cannot recover Track E-like acceleration, there is no point pushing the
quantum radiation side.
