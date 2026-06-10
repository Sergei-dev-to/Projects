# Relational Evaporator Principle

## Motivation

The connector model should not be framed as a narrow graph-qudit trick.

The broader idea is:

```text
black-hole-like thermodynamics can arise when entropy is stored primarily in
relations among constituents, while mass/energy scales primarily with the
number of constituents.
```

In that case:

```text
number of objects       ~ N
number of relations     ~ N^2
mass-like scale         ~ N
entropy-like state count ~ N^2
```

Therefore:

```text
S ~ M^2
T ~ dM/dS ~ 1/M.
```

This is the relational evaporator principle.

The connector-mode model is just the simplest finite implementation:

```text
objects = sites
relations = pairwise connector modes
evaporation = one site leaves and its incident relations decouple
```

## Why This Is Different From Track E

Track E used:

```text
entropy variable n;
mass law M ~ sqrt(n).
```

That gave:

```text
S ~ M^2
```

but only because the mass law was chosen.

The relational model uses:

```text
object count N;
relation count ~ N^2.
```

Then:

```text
S ~ M^2
```

comes from architecture:

```text
entropy counts relations;
mass counts objects.
```

This is a real conceptual improvement.

## Why This Is Related To Matrix Models

In D0-brane matrix quantum mechanics:

```text
diagonal / block degrees      -> object-like degrees
off-diagonal matrix elements  -> relation/connector degrees
```

A black-zero-brane is a noncommutative matrix block with many active
off-diagonal modes.

When one D0-brane separates:

```text
U(N) -> U(N-1) x U(1)
```

and the off-diagonal modes connecting the escaping block to the remaining block
decouple.

The remaining black-hole block has fewer active degrees of freedom. If most
energy remains in the block, the energy per active degree rises.

That is negative heat capacity.

The transferable lesson is not:

```text
all matrix Hamiltonians evaporate.
```

It is:

```text
evaporation can remove relations faster than it removes energy.
```

## General Conditions

A relational evaporator needs five ingredients.

### R1: Relational entropy dominance

The number of active entropy-carrying degrees grows faster than the number of
visible constituents:

```text
S_N ~ N^alpha
```

with:

```text
alpha > 1.
```

For pairwise relations:

```text
alpha = 2.
```

### R2: Object-like mass scaling

The mass-like scale grows approximately linearly with constituent count:

```text
M_N ~ N.
```

Then:

```text
S ~ M^alpha.
```

For black-hole-like entropy:

```text
alpha = 2.
```

### R3: Evaporation removes one object and many relations

A single emission changes:

```text
N -> N-1.
```

But the entropy-carrying sector changes by:

```text
Delta S_N = S_N - S_(N-1) ~ alpha N^(alpha-1).
```

For pairwise relations:

```text
Delta S_N ~ N.
```

So one visible emission can remove a parametrically large number of internal
states.

### R4: Emitted energy is subextensive compared with relation loss

Negative heat capacity requires:

```text
M_(N-1) < M_N
T_(N-1) > T_N.
```

Equivalently, for an active-mode/equipartition temperature:

```text
epsilon_N / E_N < 1 - q_(N-1)/q_N.
```

For pairwise relations:

```text
1 - q_(N-1)/q_N ~ 2/N.
```

So the emitted package must carry less than an `O(1/N)` fraction of the core
energy.

This is plausible if relations carry many states but little energy.

### R5: Radiation must carry or purify the lost relational information

The decoupled relations cannot simply disappear.

One of the following must be true:

```text
1. they accompany the emitted object as soft radiation/memory;
2. they remain as an inert archive that purifies the core;
3. they are transferred into field-like radiation modes;
4. the model is explicitly nonunitary/open, in which case it is not a full
   information-flow toy.
```

For our original goal, option 4 is not enough.

## Thermodynamic Consequences

For:

```text
S_N = sigma N^2
M_N = mu N
```

we get:

```text
1/T = dS/dM = (2 sigma / mu) N
```

so:

```text
T_N = mu / (2 sigma N).
```

As evaporation lowers `N`, temperature rises.

The heat capacity is:

```text
C = dM/dT ~ -N^2.
```

So the negative heat capacity is not a separate assumption. It follows from:

```text
entropy is quadratic in object count;
mass is linear in object count.
```

## Emission Rate

The relational principle gives:

```text
S ~ M^2
T ~ 1/M
C < 0.
```

It does not by itself give the Hawking power law.

To get:

```text
P ~ 1/M^2,
```

we need something like:

```text
number flux gamma ~ area * T^3
energy per emission epsilon ~ T.
```

In relational variables:

```text
area-like channel count ~ N^2
T ~ 1/N
gamma ~ N^2 T^3 ~ 1/N
epsilon ~ T ~ 1/N
P ~ 1/N^2.
```

So acceleration requires a rate mechanism with enough temperature dependence.

This remains a real dynamical problem.

## Physical Interpretations Of Relations

The same abstract relation slot can be realized in several ways.

### Matrix model

```text
relations = off-diagonal matrix/open-string modes
```

Strong precedent. But holographic/black-hole adjacent.

### Graph/link model

```text
relations = edge/link Hilbert spaces
```

Close to quantum graphity. Good for background independence and emergent
locality. Not automatically good for evaporation.

### Gauge/edge-mode model

```text
relations = boundary/edge/soft modes
```

Good for low-energy information-rich modes. Needs care because soft hair is
not a settled complete account of black-hole entropy.

### Tensor/network model

```text
relations = entanglement bonds or tensor legs
```

Good for Page/island-like information structure. Usually kinematic unless a
Hamiltonian is added.

### Incidence-local qudit model

```text
relations = explicit connector qudits on complete-graph edges
```

Best finite toy for us. Most engineered, but transparent.

## The Softness Problem

The key difficulty is not producing many relations. That is easy.

The key difficulty is:

```text
relations must carry lots of entropy without carrying proportional energy.
```

If each relation is an ordinary energetic qudit, then emitting one object plus
its `O(N)` relations may remove too much energy. The remaining core may cool or
stay at the same temperature.

So the model needs one of:

```text
1. soft/near-degenerate relation modes;
2. constraints that make relation states numerous but low-energy;
3. a separation between information-carrying relation labels and energetic
   excitations;
4. collective dynamics where relation modes count entropy but not additive
   emitted energy.
```

This is the main design challenge.

## The Radiation Problem

If one emitted object carries all `O(N)` incident relations as radiation, then
the radiation subsystem per step is large.

That helps unitarity:

```text
the lost relational information has somewhere to go.
```

But it risks trivializing Page behavior:

```text
radiation Hilbert space grows very fast.
```

Possible ways out:

```text
1. visible radiation is small, connector cloud is soft memory;
2. connector cloud is highly constrained, so its effective dimension is smaller
   than the raw qudit count;
3. only a coarse subset of relations is released, while the rest becomes inert
   archive degrees;
4. use field-like modes where relation information is encoded in correlations,
   not in a simple tensor product of emitted qudits.
```

This is the information-flow challenge.

## What Would Be New Or Interesting

Not new by itself:

```text
edge/link degrees of freedom;
matrix off-diagonal modes;
soft hair;
all-to-all relational systems.
```

Potentially interesting:

```text
a finite non-gravitational evaporator where black-hole-like thermodynamics
follows from relational entropy dominance:

  objects carry mass;
  relations carry entropy;
  evaporation removes objects and decouples relations.
```

The clean result would be:

```text
S ~ M^2 and T ~ 1/M are not imposed by a mass law but follow from relational
state counting.
```

The stronger result would add:

```text
an explicit Hamiltonian/channel with radiation that preserves this mechanism.
```

## Immediate Program

Do not start with a complicated Hamiltonian.

Proceed in layers:

```text
Layer 1: counting theorem
  If S_N ~ N^2 and M_N ~ N, then T ~ 1/M and C < 0.

Layer 2: heating criterion
  If relation loss outpaces energy loss, the remaining core heats.

Layer 3: rate criterion
  Find what rate scalings are needed for accelerating power.

Layer 4: finite connector toy
  Sites + relation qudits; test soft vs energetic connectors.

Layer 5: radiation/information toy
  Decide where decoupled relation information lives.
```

The connector-mode notes currently cover Layers 1-3.

The next real work is Layer 4:

```text
soft connector vs energetic connector.
```

## Current Judgment

The relational evaporator principle is worth pursuing.

It is broader than the connector implementation and more interesting than an
area-register model.

It does not yet solve the full problem. The unresolved issues are:

```text
softness of relational entropy;
dynamical emission rates;
radiation/information accounting.
```

But it gives the best current route to a non-gravitational model where
black-hole-like thermodynamics is structural rather than imposed.

