# Two-Track Strategy

## Synthesis update

The current synthesis is:

```text
notes/project_synthesis_after_tracks.md
```

That note supersedes this as the main project-status document. The two-track
split remains useful, but the paper framing should now center on the broader
decomposition:

```text
entropy law + shrinking Hilbert space + emission matrix elements
```

## Why split the project

The variable-N Bose-Hubbard result is encouraging, but it does not solve every
black-hole-phenomenology requirement.

It gives:

```text
natural many-body core
shrinking particle-number sectors
physical particle-loss emission operators
accelerating evaporation
core-radiation entropy growth under Kraus evolution
```

It does not give:

```text
black-hole entropy scaling S ~ area ~ M^2
```

For fixed site count `L`, the Bose-Hubbard sector dimension is:

```text
dim H_N = binomial(N + L - 1, N)
```

so at large `N`:

```text
S_N ~ (L - 1) log N
```

That is not the Bekenstein-Hawking scaling. The model is a good natural
evaporator, not a natural area-law entropy model.

## Track A: variable-N Bose-Hubbard

Role:

```text
dynamics proof of principle
```

Main lesson:

```text
shrinking Hilbert sectors plus physical particle-loss operators can produce
accelerating evaporation and core-radiation entropy growth without manually
assigning shell dimensions.
```

What Track A supports:

```text
1. Fixed-N relaxation was the wrong analogue.
2. Shrinking sectors matter dynamically.
3. Particle-loss Kraus channels can preserve acceleration.
4. Natural many-body dynamics can realize part of the BH evaporation backbone.
```

What Track A cannot support by itself:

```text
1. S ~ area.
2. S ~ M^2.
3. T ~ 1/M from a natural entropy law.
4. A full Page curve.
5. Early/late radiation mutual information.
```

Track A deliverables already produced:

```text
notes/variable_n_bose_hubbard_results.md
notes/variable_n_kraus_results.md
step3_variable_n_bose_hubbard.pdf
step3_variable_n_kraus.pdf
step3_variable_n_kraus_scan.pdf
```

Current Track A status:

```text
strong enough as a supporting result;
not enough to become the whole black-hole analogue.
```

## Track B: area-register / entropy-correct core

Role:

```text
black-hole scaling model
```

Goal:

```text
restore S ~ area ~ M^2 while keeping shrinking Hilbert-space evaporation.
```

Simplest model:

```text
sector label n = area register size
H_n = (C^q)^{tensor n}
dim H_n = q^n
S_n = n log q
M_n = alpha sqrt(n)
T_n = dM/dS ~ 1/sqrt(n) ~ 1/M
```

Emission:

```text
n -> n - 1
omega_n = M_n - M_{n-1}
```

This restores the black-hole thermodynamic backbone by construction:

```text
entropy decreases with n
mass decreases with n
temperature rises as n decreases
heat capacity is negative
```

The hard question for Track B is dynamical:

```text
Can a reasonable shrinking-register channel produce accelerating emission and
core-radiation entropy growth without simply restating the engineered shell
model?
```

## Relationship between tracks

Track A and Track B answer different objections.

Track A answers:

```text
Can a natural many-body evaporator produce acceleration when the object
actually shrinks?
```

Track B answers:

```text
Can we reproduce the black-hole entropy/temperature scaling with a finite
quantum register?
```

The engineered shell model remains the control model:

```text
it isolates the mechanism cleanly,
but imposes the density of states directly.
```

The emerging paper structure could become:

```text
1. Engineered shell control: all phenomenology, transparent mechanism.
2. Track A: natural dynamics, wrong entropy scaling.
3. Track B: correct entropy scaling, abstract dynamics.
4. Discussion: black-hole phenomenology separates into entropy law,
   shrinking Hilbert space, and emission matrix elements.
```

## Immediate recommendation

Pause Track A except for documentation.

Start Track B with a design/test note:

```text
notes/track_b_area_register.md
```

First Track B test:

```text
build an area-register Kraus evaporator with dim H_n = q^n and M_n = sqrt(n),
then test emitted power, core entropy, and sensitivity to transition structure.
```
