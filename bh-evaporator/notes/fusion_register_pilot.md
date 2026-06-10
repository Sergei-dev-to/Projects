# Track C: Fusion-Register Pilot

## Purpose

The current area-register model has the right black-hole entropy scaling:

```text
dim H_n = q^n
S_n ~ n
M_n ~ sqrt(n)
```

but the microscopic register is abstract. The fusion-register pilot asks:

```text
Can a fusion-constrained horizon-like register do something a generic area
register cannot?
```

The point is not to claim a real quantum-gravity horizon. The point is to test
whether fusion constraints affect the evaporation mechanism:

```text
W_i = sum_f Gamma_{f i} omega_{f i}.
```

If fusion only changes the entropy base, it probably does not help this
project. If it changes the `W` profile or transition-selection behavior, it is
worth pursuing.

## Minimal model

Use Fibonacci anyons:

```text
1 x tau = tau
tau x tau = 1 + tau
```

Represent `H_n` by fusion paths of `n` tau anyons starting from vacuum. Keep
both final total charges:

```text
H_n = span of all allowed fusion paths after n tau anyons.
```

This gives:

```text
dim H_n = F_{n+1}
S_n = log F_{n+1} ~ n log phi
```

Use:

```text
M_n = alpha sqrt(n)
```

so:

```text
S ~ n ~ M^2
T ~ 1/M
C < 0
```

This is the same thermodynamic backbone as the area-register model, but with
fusion-constrained rather than independent local basis states.

## Shrinkage map

Use the natural prefix-removal map:

```text
H_n -> H_{n-1}
```

A length-`n` fusion path maps to its length-`n-1` prefix. The emitted channel
label records the final charge:

```text
final charge = 1
final charge = tau
```

This is analogous to removing the last boundary anyon.

Control:

```text
scrambled prefix removal
```

Orthogonally rotate the domain and codomain while preserving the singular
values/channel capacity of the prefix map. This tests whether the fusion basis
structure matters or whether only the sector dimensions matter.

## Hamiltonian blocks

Use the same minimal Track B construction:

```text
H_n = M_n I + small random symmetric perturbation.
```

This is not a microscopic anyon Hamiltonian. It is a kill test for the
register and shrinkage structure.

## Comparisons

Run:

```text
fusion prefix removal, sqrt mass
scrambled removal, sqrt mass
fusion prefix removal, linear mass
scrambled removal, linear mass
```

Diagnostics:

```text
emitted power
mean area n
Renyi-2 core entropy in the reduced channel
W trajectory
sector-averaged bar W_n
sector-only reconstruction
```

## Kill conditions

Stop if:

```text
1. fusion prefix and scrambled removal behave the same;
2. the result is indistinguishable from the Track B qubit area register;
3. acceleration comes only from M ~ sqrt(n), with no fusion-specific effect.
```

That would mean anyons are not helping the evaporator story at this level.

## Positive signs

Continue if:

```text
1. fusion prefix removal gives a different W profile from scrambled removal;
2. fusion constraints produce different selection behavior;
3. acceleration or failure differs at fixed entropy/mass schedule;
4. the sector-only reconstruction behaves differently from the qubit register.
```

That would mean fusion constraints matter dynamically, not just entropically.

## Current expectation

The likely result is conservative:

```text
fusion constraints will reproduce area-register thermodynamics but may not
change the W mechanism much.
```

That is still worth testing because it directly connects the earlier anyon
thread to the evaporator project.

