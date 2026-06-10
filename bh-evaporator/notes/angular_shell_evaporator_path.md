# Angular-Shell Evaporator Path

## Purpose

This is the most natural continuation of the relational evaporator idea so far.

Instead of using arbitrary complete-graph connector qudits, use angular
soft/edge labels:

```text
soft modes = Y_lm labels on a two-dimensional boundary
cutoff     = l <= L
```

Evaporation shrinks the cutoff:

```text
L -> L - 1.
```

The removed angular shell:

```text
l = L
```

has:

```text
2L + 1
```

soft labels. These are the relation/edge degrees that decouple during one
emission.

This gives the same `O(N)` relation loss as the connector model, but in a much
cleaner basis.

## Basic Construction

Let the evaporating object be labeled by an integer:

```text
L = angular cutoff / size / mass index.
```

Soft Hilbert space:

```text
H_soft(L) = tensor_{l=0}^L tensor_{m=-l}^l C^d.
```

Number of soft modes:

```text
K_L = sum_{l=0}^L (2l+1) = (L+1)^2.
```

Entropy:

```text
S_L = K_L log d = (L+1)^2 log d.
```

Mass-like scale:

```text
M_L = mu L.
```

Then for large `L`:

```text
S ~ L^2
M ~ L
S ~ M^2
T ~ 1/M.
```

This reproduces the black-hole thermodynamic scaling without imposing:

```text
M ~ sqrt(S).
```

## Evaporation Step

One evaporation step:

```text
H_soft(L) -> H_soft(L-1) tensor H_shell(L)
```

where:

```text
H_shell(L) = tensor_{m=-L}^L C^d.
```

The shell has:

```text
dim H_shell(L) = d^(2L+1).
```

So the entropy removed per step is:

```text
Delta S_L = S_L - S_(L-1) = (2L+1) log d.
```

This is the angular analogue of:

```text
one emitted object decouples O(N) connector modes.
```

## Energy Assignment

The key assumption:

```text
angular shell labels are soft / nearly degenerate.
```

So:

```text
M_L = mu L
```

is not the sum of ordinary mode energies.

The emitted hard quantum has energy:

```text
epsilon_L ~ T_L ~ 1/L.
```

The shell labels carry information/memory but little energy.

This is the crucial distinction from ordinary spherical harmonics.

Ordinary angular excitations have gradient costs:

```text
omega_l^2 ~ l(l+1)/R^2.
```

The angular-shell evaporator instead treats `Y_lm` as a basis for soft edge
labels, not as ordinary bulk waves.

## Heating

The core heats because:

```text
M_L decreases
S_L decreases faster, by Delta S_L ~ L.
```

Microcanonical temperature:

```text
1/T = dS/dM = (dS/dL) / (dM/dL)
    ~ (2 L log d) / mu.
```

So:

```text
T_L ~ mu / (2 L log d).
```

After:

```text
L -> L-1,
```

temperature rises.

## Rate Requirement

The angular-shell count gives:

```text
S ~ M^2
T ~ 1/M
C < 0.
```

It does not automatically give:

```text
P ~ 1/M^2.
```

For Hawking-like acceleration we need:

```text
number flux gamma_L ~ area * T^3
                 ~ L^2 * (1/L)^3
                 ~ 1/L
```

and:

```text
epsilon_L ~ T ~ 1/L.
```

Then:

```text
P_L ~ gamma_L epsilon_L ~ 1/L^2.
```

So the dynamical question becomes:

```text
Can the model produce a T^3-like flux/filter from a finite quantum channel?
```

The thermodynamic state count is solved at the abstract level; the emission
rate is not.

## Radiation Interpretation

One emission produces:

```text
hard radiation quantum: carries energy epsilon_L ~ T_L
soft angular shell:     carries memory labels m=-L,...,L
```

So radiation per step is:

```text
R_L = R_hard(L) tensor H_shell(L).
```

This is better than:

```text
one emitted qubit
```

because the soft shell can purify the entropy loss.

It is also better than:

```text
full transition record
```

because the shell labels are real degrees in the model, not bookkeeping labels.

But it risks making Page behavior too easy, because the soft radiation Hilbert
space grows fast.

The correct interpretation may be:

```text
hard quanta are observable radiation;
soft shell labels are memory/edge/archive degrees that purify the process.
```

## Why This Is More Natural Than Pairwise Connectors

Pairwise connector model:

```text
N objects;
N(N-1)/2 explicit connectors;
emission removes connectors incident on one object.
```

Angular-shell model:

```text
boundary mode cutoff L;
(L+1)^2 angular soft labels;
emission removes the outer shell l=L.
```

Advantages of angular-shell model:

```text
1. Area scaling comes from a 2D mode count.
2. Removed entropy per step is the shell degeneracy 2L+1.
3. Softness has literature precedent via edge modes / soft hair.
4. Radiation split is natural: hard quantum plus soft memory shell.
```

Disadvantages:

```text
1. It introduces boundary geometry.
2. It leans closer to black-hole/horizon language.
3. The soft degeneracy still needs justification.
4. Rate dynamics remains unsolved.
```

## Minimal Model To Test

Start with a purely kinematic but explicit Hilbert-space model:

```text
H_L = H_hard(L) tensor H_soft(L)
```

with:

```text
dim H_soft(L) = d^((L+1)^2)
M_L = mu L
soft labels nearly degenerate
```

Evaporation isometry:

```text
V_L : H_L -> H_(L-1) tensor R_hard(L) tensor H_shell(L).
```

The first test is not Page behavior.

The first test is:

```text
Does this construction cleanly reproduce S ~ M^2, T ~ 1/M, C < 0, and
entropy loss Delta S ~ M per emitted hard quantum?
```

That is already yes at counting level.

The next test is:

```text
Can one choose an energy-filtered channel where epsilon_L ~ T_L and rates
accelerate without using a full transition record?
```

## Natural Next Steps

### Step 1: Formal counting note

Write the angular-shell counting as a compact proposition:

```text
If soft edge labels are truncated at L and M ~ L, then S ~ M^2 and T ~ 1/M.
```

### Step 2: Compare with connector model

Show:

```text
pairwise connectors and angular shells are two bases for relation-dominated
entropy.
```

The angular basis is more horizon-like; the connector basis is more
matrix/graph-like.

### Step 3: Radiation accounting

Decide whether:

```text
H_shell(L)
```

is:

```text
observable soft radiation;
inert archive;
edge memory attached to hard radiation;
or field-like correlation data.
```

### Step 4: Minimal channel

Build:

```text
V_L : H_L -> H_(L-1) tensor R_L
```

where `R_L` contains:

```text
one hard energy bin + soft shell labels.
```

Do not try to make a full Hamiltonian until this channel is coherent.

## Current Judgment

This is the most natural version of the relational evaporator so far.

It keeps the main achievement:

```text
S ~ M^2 from state counting, not from an imposed square-root mass law.
```

It handles the soft-connector issue better:

```text
soft angular edge labels can carry entropy without ordinary excitation energy.
```

The open problem is now precise:

```text
derive or justify the soft angular labels and the emission-rate law.
```

