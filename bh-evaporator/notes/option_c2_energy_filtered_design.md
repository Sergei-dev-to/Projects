# Option C2: Energy-Filtered Detached-Qubit Design

## Purpose

C2 is the intended synthesis of the two successful halves:

```text
Track E:
  thermodynamic emission rates and acceleration diagnostics

C1:
  explicit emitted radiation qubits and early/late radiation cuts
```

The goal is:

```text
an explicit radiation-register evaporator with emission/no-emission branches,
where the emission branch is weighted by energy-lowering matrix elements.
```

## One-Step Structure

At step `t`, the state lives in:

```text
core H_n
existing radiation R_1 ... R_t
```

A fresh radiation bin is added:

```text
B_t = |0> no emission
      plus emitted states.
```

The one-step map has two kinds of branches:

```text
no emission:
  H_n -> H_n tensor |0>_B

emission:
  H_n -> H_(n-1) tensor |emitted>_B
```

## Minimal Radiation Bin

A single emitted qubit is too small to distinguish all transitions, so the
first C2 pilot uses a modest bin:

```text
B_t = no-emission flag
      + emitted detached-qubit value b
      + coarse energy bin e
```

Labels:

```text
0:
  no emission

(1, b, e):
  emission occurred;
  detached boundary qubit value b = 0 or 1;
  emitted energy fell in bin e.
```

This is not fully faithful to all transition labels, but it is less artificial
than recording `(n,i,f)` and more informative than C1.

## Emission Weights

For an instantaneous core eigenstate:

```text
|n,i>
```

boundary detachment gives amplitudes into:

```text
|n-1,f> tensor |b>.
```

Let:

```text
A_{f b, i} = <n-1,f; b | detach | n,i>
omega_{f i} = E_{n,i} - E_{n-1,f}
```

Define unnormalized emission weight:

```text
Gamma_{f b, i}
  = g * |A_{f b, i}|^2 * J(omega_{f i})
```

where:

```text
J(omega) = omega^p if min_gap <= omega <= max_gap
           0 otherwise
```

Then scale `g` so:

```text
max_i sum_{f,b} Gamma_{f b, i} <= pmax.
```

No-emission amplitude:

```text
s_i = sqrt(1 - sum_{f,b} Gamma_{f b, i}).
```

## Coherence Caveat

If multiple `(f,b)` transitions share the same coarse energy-bin radiation
label, amplitudes can interfere.

Therefore this C2 pilot has two possible modes:

```text
exact mode:
  radiation label includes f as well as b and energy bin;
  faithful but larger.

compressed mode:
  radiation label includes only b and energy bin;
  scalable but not guaranteed faithful.
```

The first pilot should run both at small size and compare:

```text
core energy(t)
power(t)
gamma(t)
epsilon(t)
S2(core)
```

If compressed mode changes the thermodynamic diagnostics too much, it cannot
be used for claims.

## Diagnostics

For every run report:

```text
gamma(t):
  emission probability per step

epsilon(t):
  emitted energy conditional on emission

P(t):
  gamma(t) * epsilon(t)

S2(core)
S2(early)
S2(late)
I2(early:late)
```

Controls:

```text
sqrt mass vs linear mass
boundary/local vs scrambled detachment
exact labels vs compressed labels
```

## Success Criteria

C2 is promising if:

```text
1. sqrt mass accelerates and linear does not;
2. acceleration can be decomposed into gamma and epsilon;
3. explicit radiation bins give nonzero early/late structure;
4. compressed labels roughly preserve exact-mode thermodynamics;
5. local/scrambled controls differ in the black-hole-like case.
```

## Failure Criteria

C2 should be downgraded if:

```text
1. it reduces to C1 kinematic detachment;
2. compressed labels change the channel qualitatively;
3. acceleration disappears once emission is probabilistic;
4. radiation structure is identical across all controls;
5. branch growth is as bad as full transition-record radiation.
```

## First Pilot

This pilot has now been run.

Result note:

```text
notes/detached_qubit_c2_results.md
```

Short result:

```text
The first C2 implementation gives probabilistic emission and explicit
radiation bins, but it decelerates for both sqrt and linear mass laws. The
sqrt/linear distinction is weak, and conditional emitted energy is nearly flat.
```

So the naive C2 map is not yet the desired synthesis.

The next attempt should modify the rate profile before scaling the radiation
calculation.

Candidate fixes:

```text
sector-normalized pmax;
BH-inspired gamma_n ~ 1/sqrt(n);
matching the successful Track E W_n profile;
larger-n trajectory pretest before quantum entropy calculation.
```

Original first-pilot target:

```text
n = 4,...,7
steps = 32
seed = 2468
operator = boundary
mass laws = sqrt, linear
label modes = exact, compressed
```

This is small enough to fail cheaply.
