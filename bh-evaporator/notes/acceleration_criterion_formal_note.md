# Track D: Acceleration Criterion Formal Note

## Purpose

The numerical work now points to a common mechanism:

```text
P(t) = <W>_t
```

with:

```text
W_i = sum_f Gamma_{f i} omega_{f i}.
```

This note states the useful criterion without pretending it is deeper than it
is.

## Setup

Consider sectors:

```text
H = direct sum_n H_n
```

with energy-lowering transitions:

```text
H_n -> H_{n-1}.
```

Let:

```text
p_i(t) = population of source state i
Gamma_{f i} = transition probability from i to f
omega_{f i} = emitted energy
```

Define outgoing weighted phase space:

```text
W_i = sum_f Gamma_{f i} omega_{f i}.
```

Then emitted power is:

```text
P(t) = sum_i p_i(t) W_i.
```

So acceleration over a window means:

```text
<W>_late > <W>_early.
```

## Sector decomposition

Let:

```text
p_n(t) = total population in sector n
bar W_n = uniform average of W_i over i in H_n
sigma_n(t) = actual sector average / uniform sector average
```

where:

```text
sigma_n(t) =
  [sum_{i in H_n} p_i(t) W_i / p_n(t)] / bar W_n.
```

Then:

```text
P(t) = sum_n p_n(t) bar W_n sigma_n(t).
```

This separates acceleration into:

```text
1. sector drift:
   p_n(t) moves toward sectors with larger bar W_n;

2. selection drift:
   sigma_n(t) increases because dynamics selects high-W states inside sectors;

3. transition-scale drift:
   W_i itself changes because jump probability or emitted energy changes.
```

## Sufficient condition

A simple sufficient condition over a time window is:

```text
sum_n p_n(t_2) bar W_n sigma_n(t_2)
>
sum_n p_n(t_1) bar W_n sigma_n(t_1).
```

That is almost a restatement. A more useful coarse sufficient condition is:

```text
1. the sector distribution shifts toward lower n;
2. bar W_n increases along the shrinking direction;
3. sigma_n(t) does not decrease enough to offset that increase.
```

In words:

```text
shrinking must expose larger outgoing weighted phase space, and the dynamics
must not avoid it.
```

## Jump-energy decomposition

Also write:

```text
W_i = gamma_i * epsilon_i
```

where:

```text
gamma_i = sum_f Gamma_{f i}
epsilon_i = [sum_f Gamma_{f i} omega_{f i}] / gamma_i.
```

Then acceleration can be driven by:

```text
1. more frequent jumps;
2. larger emitted energy per jump;
3. both.
```

This explains the model differences:

```text
Track B sqrt mass:
  mild increase in both jump access and emitted energy.

Track B linear mass:
  emitted energy stays nearly flat and jump access falls.

Variable-N Bose-Hubbard:
  successful cases often combine improved jump access with higher conditional
  emitted energy, but only after transition-induced selection.
```

## Relation to black holes

For a Schwarzschild black hole, the analogous statement is:

```text
luminosity increases because the shrinking object gets hotter.
```

Roughly:

```text
T ~ 1/M
area ~ M^2
P ~ area * T^4 ~ 1/M^2.
```

In this language, the effective black-hole `W(M)` increases as `M` decreases.

The toy-model question is:

```text
Can a finite quantum system make W increase for comparably structural reasons?
```

Current answer:

```text
yes for engineered and abstract area-register reasons;
yes for variable-N Bose-Hubbard through matrix-element selection;
not yet from a natural microscopic area-law model.
```

## What is not claimed

This is not:

```text
1. a theorem about quantum gravity;
2. a derivation of Hawking radiation;
3. a Page-curve result;
4. a proof that any finite system with negative heat capacity evaporates.
```

It is a finite-system diagnostic:

```text
negative heat capacity is not enough;
shrinking sectors are not enough;
entropy growth is not enough;
the channel must drive <W> upward.
```

## Current use

This criterion should be used as the organizing object for the project.

The models then become examples of different mechanisms for increasing
`<W>`:

```text
Engineered shell:
  imposed sector/channel W profile.

Area register:
  sector-profile W increase from M ~ sqrt(n).

Variable-N Bose-Hubbard:
  selection-driven W increase inside shrinking particle-number sectors.

Fibonacci fusion register:
  area-register-like sector-profile W increase, with no clear fusion-specific
  dynamical advantage in the minimal pilot.
```

