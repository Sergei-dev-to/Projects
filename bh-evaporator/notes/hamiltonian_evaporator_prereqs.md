# Before Constructing the Hamiltonian Evaporator

## Target

The worthwhile version of the project needs an explicit collision Hamiltonian:

```text
H_total = H_core + H_rad + H_int
```

with repeated fresh radiation time bins. The model should produce, from the
same unitary dynamics:

```text
negative microcanonical heat capacity
accelerating evaporation
computed radiation entropy turnover
```

The current shell-channel model is a useful design test, but it is not enough.
The Hamiltonian version is the minimum credible endpoint for a paper.

## What we need to specify before coding

### 1. Core Hilbert space

We need a finite shell core:

```text
H_core = direct_sum_m H_m
dim H_m = D_m
```

with shell energies:

```text
E_0 > E_1 > ... > E_L
```

and dimensions chosen from a convex entropy profile:

```text
D_m approx exp[S(E_m)]
S''(E) > 0
```

Minimum choice:

```text
same shell dimensions as the current dynamic shell test
```

Better choice:

```text
increase D_max modestly and avoid D_m = 1 too early, so late evolution is not
dominated by tiny accidental Hilbert spaces.
```

### 2. Core Hamiltonian inside each shell

We need to decide whether shell interiors are exactly degenerate or weakly
chaotic.

Degenerate version:

```text
H_core = direct_sum_m E_m I_{D_m}
```

Pros:

```text
simple
cheap
clean shell bookkeeping
```

Cons:

```text
no internal scrambling timescale
less defensible as chaotic finite matter
```

Weakly chaotic version:

```text
H_core = direct_sum_m (E_m I_{D_m} + epsilon G_m)
```

where `G_m` is a fixed GOE/GUE random matrix with bandwidth smaller than the
shell spacing.

Pros:

```text
fixed internal scrambling
less artificial
```

Cons:

```text
more parameters
harder to isolate the shell mechanism
```

Recommended first Hamiltonian run:

```text
start degenerate, then add weak intra-shell chaos as a robustness check.
```

### 3. Radiation time-bin Hilbert space

Minimum binary bin:

```text
|0> = no emission
|1> = one emitted quantum
```

Hamiltonian:

```text
H_rad = omega |1><1|
```

But binary bins only support nearest-shell jumps. A stronger version uses:

```text
|0>, |omega_1>, |omega_2>, ...
```

with:

```text
H_rad = sum_k omega_k |omega_k><omega_k|
```

Recommended first Hamiltonian run:

```text
binary bins, nearest-shell transitions.
```

Recommended second run:

```text
qutrit or ququart bins with multiple emission energies.
```

### 4. Interaction Hamiltonian

Minimum nearest-shell interaction:

```text
H_int =
sum_m g_m X_m tensor |1><0| + h.c.
```

where:

```text
X_m: H_m -> H_{m+1}
```

is a fixed random matrix.

The Golden-rule intuition is:

```text
Gamma_m proportional to g_m^2 D_{m+1}
```

If `g_m` is constant or slowly varying, the changing final-state degeneracy
controls the emission schedule. This is the core mechanism.

Important choice:

```text
Do not tune g_m to force the desired evaporation law in the first test.
```

If we need shell-dependent `g_m`, it should be for a clearly stated passband or
coupling normalization, not to hide the density-of-states mechanism.

### 5. Collision protocol

At step `t`, introduce a fresh radiation bin initialized in `|0>`.

Evolve:

```text
U = exp[-i Delta t (H_core + H_rad,t + H_int,t)]
```

Then the bin is never coupled again.

This is not a single autonomous closed Hamiltonian for all times, but it is a
standard collision/time-bin model and gives explicit unitary dynamics.

What must be fixed per seed:

```text
H_core
all X_m
all couplings g_m
Delta t
```

Fresh bins are new degrees of freedom, but the coupling law should be reused.

### 6. Observable diagnostics

The Hamiltonian run must output:

```text
S(E_m), beta(E_m), T(E_m)
mean core energy E(t)
emitted power P(t)
radiation Renyi-2 entropy S2_rad(t)
linear-S(E) control
fixed-coupling vs tuned-coupling comparison
```

Useful additional diagnostics:

```text
shell probability distribution p_m(t)
purity of radiation/core
Page peak step
dimension-crossing estimate
energy conservation error per collision
```

### 7. Numerical constraints

The state lives in:

```text
core dimension x 2^n_bins
```

For brute force, keep:

```text
D_total_core <= about 100 to 300
n_bins <= about 14 to 18
```

The current shell model with:

```text
D = 64 + 24 + 10 + 5 + 3 + 2 + 1 + 1 = 110
```

is a reasonable starting point.

Hamiltonian exponentials should be applied locally to:

```text
core x current bin
```

not to the full core+radiation space.

### 8. The main implementation question

There are two ways to apply the collision unitary.

Option A:

```text
build dense U on core x bin, then apply it to the state tensor
```

With current dimensions:

```text
dim(core x bin) about 220
```

This is feasible.

Option B:

```text
apply expm_multiply using sparse H
```

This is better later, but not necessary for the first Hamiltonian test.

Recommended:

```text
use dense U first for clarity.
```

## What would count as success

The Hamiltonian version succeeds if:

```text
1. With fixed H_core and fixed X_m, E(t) decreases.
2. In the convex S(E) model, emitted power rises over the working window.
3. In the linear-S(E) control, the comparable acceleration is absent or much
   weaker.
4. S2_rad(t) is computed from the evolved pure state and shows a turnover.
5. The result is stable over random seeds for X_m.
```

## What would count as failure

Failure modes:

```text
the system Rabi-oscillates strongly instead of evaporating
emission probability must be shell-tuned by hand to get acceleration
the convex and linear controls are not distinguishable
the Page-like turnover disappears unless randomness is redrawn every step
the model needs parameters so small that evaporation does not happen in
feasible time
```

## Recommended next sequence

1. Modify the current shell-channel script so maps are fixed per seed.
2. Build `sim/hamiltonian_shell_evaporator.py` with dense `U` on core x bin.
3. Start with degenerate shells and binary radiation bins.
4. Compare convex vs linear entropy profiles.
5. Add weak intra-shell chaos only after the degenerate-shell test works.

This keeps the path incremental and makes each failure informative.

## Update after naive Hamiltonian test

See:

```text
notes/hamiltonian_naive_first_results.md
```

The binary-bin Hamiltonian test failed in an informative way. Because the shell
dimensions shrink, a single transition operator

```text
X_m: C^{D_m} -> C^{D_{m+1}}
```

has a large dark subspace. The system emits the bright component and then
becomes partially trapped. Multi-channel bins and weak intra-shell chaos help
but did not yet recover the convex/control separation.

Revised design constraint:

```text
the Hamiltonian evaporator needs enough outgoing channel capacity and/or
internal scrambling to make the effective emission map high-rank.
```
