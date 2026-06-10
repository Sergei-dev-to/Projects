# Fusion-Register Pilot Results

## Purpose

The fusion-register pilot tests whether a horizon-like constrained Hilbert
space changes the evaporation mechanism, or merely replaces the qubit
area-register dimension by Fibonacci growth.

Question:

```text
Can fusion constraints do dynamical work in the W mechanism?
```

where:

```text
W_i = sum_f Gamma_{f i} omega_{f i}.
```

## Implementation

Design note:

```text
notes/fusion_register_pilot.md
```

Script:

```text
sim/fusion_register_pilot.py
```

Figure:

```text
fusion_register_pilot.pdf
```

Data:

```text
sim/data/fusion_register_pilot.csv
sim/data/fusion_register_fusion_sqrt_seed2468.npz
sim/data/fusion_register_fusion_linear_seed2468.npz
sim/data/fusion_register_scrambled_sqrt_seed2468.npz
sim/data/fusion_register_scrambled_linear_seed2468.npz
sim/data/fusion_register_fusion_sqrt_seed2469.npz
sim/data/fusion_register_fusion_linear_seed2469.npz
sim/data/fusion_register_scrambled_sqrt_seed2469.npz
sim/data/fusion_register_scrambled_linear_seed2469.npz
```

Model:

```text
Fibonacci anyon fusion paths
1 x tau = tau
tau x tau = 1 + tau
```

Sector:

```text
H_n = all allowed length-n fusion paths from vacuum
dim H_n = F_{n+1}
```

Mass law:

```text
sqrt control:   M_n = alpha sqrt(n)
linear control: M_n = alpha n
```

Shrinkage maps:

```text
fusion prefix removal:
  remove the final tau anyon and keep the prefix path;
  emitted label records final charge 1 or tau.

scrambled removal:
  orthogonally rotated version preserving channel capacity.
```

## Result

The result is conservative.

```text
case                    mean accel   mean W ratio   mean sector-W ratio
-----------------------------------------------------------------------
fusion, sqrt mass        1.060       1.062          1.095
scrambled, sqrt mass     1.063       1.065          1.097
fusion, linear mass      0.999       0.999          0.999
scrambled, linear mass   0.999       0.999          0.999
```

The square-root mass law gives mild acceleration.

The linear mass law is essentially flat:

```text
mid/early power ~ 0.999
```

The fusion-prefix and scrambled maps are almost indistinguishable.

## Mechanism

For the sqrt-mass cases:

```text
sector-W mid/early ~ 1.096
actual W mid/early ~ 1.064
selection mid/early ~ 0.970
```

So the mechanism is sector-profile acceleration:

```text
the coarse lower-sector W profile rises,
while intrasection selection slightly suppresses it.
```

This is qualitatively the same mechanism as the Track B qubit area register.

## Interpretation

The pilot did not show a fusion-specific dynamical advantage.

It showed:

```text
1. Fibonacci fusion sectors reproduce the area-register thermodynamic pattern.
2. M ~ sqrt(n) gives mild acceleration.
3. M ~ n does not.
4. The W diagnostic tracks the acceleration.
5. Fusion-prefix removal behaves almost the same as scrambled removal.
```

Therefore, at this minimal level:

```text
fusion constraints matter entropically but not dynamically.
```

They provide a less arbitrary route to exponential-in-area Hilbert-space growth,
but they do not yet improve the evaporator mechanism relative to a generic
area register.

## What this means for anyons

This does not kill all anyon/fusion approaches.

It only says the simplest fusion-path register with random Hamiltonian blocks
and prefix removal does not add much beyond Track B.

Anyons might matter if we add:

```text
1. a genuine fusion Hamiltonian, not random blocks;
2. fixed total topological charge sectors;
3. local F-move/braid-generated dynamics;
4. emission constrained by topological charge conservation with an exterior
   anyon;
5. nontrivial radiation labels carrying topological charge.
```

But those are substantially more specific models.

## Current verdict

Track C is useful as a negative/conservative result.

It suggests:

```text
Do not pivot the evaporator project to anyons unless we are willing to model
topological charge dynamics more seriously.
```

For the present project, the fusion pilot supports a narrower conclusion:

```text
area-law Hilbert-space growth is not enough;
the relevant question is still how the shrinkage map makes <W> increase.
```

