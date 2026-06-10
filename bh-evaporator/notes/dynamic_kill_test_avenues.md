# Dynamic Kill Test: Possible Avenues

## Question

Can we build a small explicit model in which the same structure produces:

```text
negative microcanonical heat capacity
accelerating evaporation
computed radiation entropy
Page-like turnover
```

The key requirement is that the Page-like entropy curve must not be attached
after the fact. It has to come from the emitted time-bin degrees of freedom.

## Avenues

### Avenue 1: shell channel with dimension-driven emission

This is the recommended first kill test.

Define shells:

```text
E_0 > E_1 > ... > E_L
D_m = round(exp[S(E_m)])
```

Choose `S(E)` with a convex window, for example:

```text
S(E) = S_floor + a E^2
```

over the working range. Then:

```text
beta(E) = dS/dE = 2 a E
T(E) = 1 / beta(E)
```

If evaporation lowers `E`, then `beta` decreases and `T` increases. This is
the negative-heat-capacity schedule.

At each step, couple shell `m` to lower shells `m+k` and a fresh radiation bin:

```text
H_m -> H_{m+k} tensor |omega_k>
```

with transition weights proportional to:

```text
Gamma_{m -> m+k} proportional to |g_k|^2 D_{m+k} rho_rad(omega_k)
```

or, for a minimal discrete passband:

```text
p_{m,k} = normalize[ |g_k|^2 D_{m+k} f(omega_k) ]
```

where `omega_k = E_m - E_{m+k}`.

Then draw a Haar-random isometry with block weights `p_{m,k}`:

```text
V_m: C^{D_m} -> direct_sum_k (C^{D_{m+k}} tensor |omega_k>)
```

The full state evolves by applying the appropriate shell map and appending the
new time bin. Radiation entropy is computed directly from the resulting pure
state.

#### Why it is useful

This is the smallest model that binds:

```text
D(E) -> beta(E) -> transition weights -> E(t) -> S_rad(t)
```

It is not a Hamiltonian exponentiation yet, but it is a unitary Stinespring
evaporation map with an explicit density-of-states engine.

#### What would count as success

```text
1. beta(E) decreases as the core loses energy.
2. Mean emitted power increases during the working window.
3. Radiation Renyi-2 entropy rises and later turns over.
4. The Page time roughly tracks log dim(rad) ~ log dim(core).
5. Changing the convexity of S(E) changes the evaporation acceleration while
   leaving generic Page competition intact.
```

#### Main weakness

The transition weights are still engineered. This is acceptable for the kill
test, but the paper must call it a minimal control model rather than a natural
Hamiltonian.

### Avenue 2: collision Hamiltonian generating the same channel

This upgrades Avenue 1 by replacing direct isometries with short-time
Hamiltonian evolution.

For each shell window, define:

```text
H_core = direct_sum_m (E_m I_m + epsilon H_m^GUE)
H_rad = sum_k omega_k |omega_k><omega_k|
H_int = sum_{m,k} g_k X_{m,k} tensor |omega_k><0| + h.c.
```

Then evolve:

```text
U = exp[-i Delta t (H_core + H_rad + H_int)]
```

with a fresh radiation bin at each step.

The Golden-rule rate into shell `m+k` is controlled by:

```text
|g_k|^2 D_{m+k} rho_rad(omega_k)
```

so the negative-C schedule still enters through the density of final states.

#### Why it is useful

This is more defensible as an explicit microscopic model:

```text
finite Hamiltonian
unitary evolution
fresh outgoing time bins
computed radiation entropy
```

#### Main weakness

It is more expensive and easier to get bogged down in numerical details before
we know whether the idea works.

### Avenue 3: stochastic trajectory plus purified radiation

This is a cheaper semi-quantum diagnostic.

Use the same transition probabilities `p_{m,k}`, but sample many evaporation
histories:

```text
m_0 -> m_1 -> ... -> m_t
```

Attach a radiation basis string to each history and purify the ensemble by
assigning amplitudes:

```text
sqrt(P(history)) times random phase / random core vector
```

Then compute radiation entropies from the resulting history state.

#### Why it is useful

It tests the thermodynamic schedule quickly and makes plots easy.

#### Main weakness

It is too close to a constructed Page ansatz. Useful for debugging, but not
enough for the paper unless followed by Avenue 1 or 2.

### Avenue 4: natural finite-system core

Try to find a physically standard Hamiltonian with a convex intruder:

```text
finite attractive Bose-Hubbard cluster
long-range spin system
finite droplet / phase-coexistence model
```

Then couple it to outgoing time bins.

#### Why it is useful

This would make the model much more physically compelling.

#### Main weakness

This is too hard as the next step. It should come only after Avenue 1 shows
that the information-flow story works at all.

## Recommended path

Do Avenue 1 first.

Implementation target:

```text
bh-evaporator/sim/dynamic_shell_evaporator.py
```

Outputs:

```text
bh-evaporator/sim/data/dynamic_shell_evaporator.npz
```

Minimum plots:

```text
S(E), beta(E), T(E)
mean core energy vs step
emitted power vs step
radiation S2 vs step
log dim remaining core vs log dim radiation
```

Parameter scale:

```text
L = 8 to 12 shells
D_max = 32 to 128
rad_dim = 3 or 4
number of random seeds = 10 to 50
```

Use Renyi-2 entropy first:

```text
S2(rad) = -log Tr rho_rad^2
```

It is cheaper and stable enough for the kill test.

## Decision rule

Continue toward the paper only if Avenue 1 shows:

```text
negative-C_mu schedule controls emission acceleration
and
the same unitary map gives a Page-like radiation entropy turnover.
```

If it only gives a Page curve because the isometry dimensions force one, while
the negative-C schedule is irrelevant to the dynamics, the idea is not strong
enough.

## First implementation

Implemented:

```text
sim/dynamic_shell_evaporator.py
```

First-result note:

```text
notes/dynamic_shell_first_results.md
```

Initial assessment:

```text
The Page-like turnover appears in both convex and linear-entropy runs, as
expected from Hilbert-space competition. The acceleration diagnostic differs:
the convex run has a rising emission schedule and a mid/early emitted-power
ratio above one, while the linear control has a flat emission schedule and no
comparable acceleration.
```

This is enough to keep going to plotting and parameter tuning, but not yet
enough for a final manuscript claim.
