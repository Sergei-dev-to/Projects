# Soft vs Energetic Relations

## Purpose

The relational evaporator needs many relation states:

```text
S_N ~ N^2.
```

But it cannot let the emitted relation cloud carry energy proportional to all
those states. If it does, the remaining core will not heat.

So the key question is:

```text
What kind of relation degrees of freedom can carry entropy without carrying
proportional energy?
```

This note separates the viable and nonviable options.

## Setup

Let:

```text
N = number of visible objects
R_N = number of active relations ~ N(N-1)/2
S_N ~ R_N log d
M_N ~ mu N
```

Evaporation:

```text
N -> N-1
```

removes:

```text
Delta R_N = N-1
```

relations.

Heating condition:

```text
epsilon_N / E_N < 1 - q_(N-1)/q_N ~ 2/N.
```

If:

```text
E_N ~ mu N,
```

then heating requires:

```text
epsilon_N < O(1).
```

So the whole emitted package, including one object and its O(N) incident
relations, must carry only order-one or smaller energy.

## Case A: Ordinary Energetic Relation Qudits

Suppose each relation is an ordinary qudit with an O(1) excitation scale:

```text
H_rel = sum_{i<j} Delta c_ij^\dagger c_ij
Delta ~ O(1).
```

If emitting one object releases `N-1` relation qudits with typical O(1) energy,
then:

```text
epsilon_rel ~ O(N).
```

This violates the heating condition.

Result:

```text
ordinary energetic connectors fail unless most incident connectors are in
their ground states at emission.
```

This is not impossible, but then the entropy cannot come from thermal
occupation of ordinary connector excitations.

## Case B: Soft Degenerate Relation Labels

Suppose each relation has many internal labels but little or no energy splitting:

```text
H_rel |label> = 0 or nearly 0.
```

Then relation states contribute degeneracy:

```text
dim H_rel = d
```

without contributing much energy.

Entropy:

```text
S_N ~ R_N log d ~ N^2.
```

Energy:

```text
E_N ~ mu N + small corrections.
```

This gives:

```text
S ~ M^2
T ~ 1/M
C < 0.
```

This is the cleanest thermodynamic option.

But it raises a legitimacy question:

```text
why are there so many nearly degenerate relation labels?
```

Possible justifications:

```text
1. gauge/edge-mode degeneracy;
2. soft hair / boundary charge sectors;
3. topological or constrained relation states;
4. emergent low-energy sector of a more microscopic Hamiltonian.
```

If we simply declare them degenerate, the model risks becoming an area register
in disguise.

## Case C: Constrained Relation Hilbert Space

Suppose relation variables have a large raw Hilbert space but constraints keep
their energy low.

Example:

```text
relations satisfy gauge-like constraints;
many label configurations are allowed at nearly the same macroscopic energy;
energetic excitations are separate from label states.
```

This is more physical than pure degeneracy.

The entropy comes from:

```text
number of allowed constrained relation sectors.
```

The energy comes from:

```text
object count, collective modes, or a small number of energetic excitations.
```

This is probably the best target for a serious toy.

It mirrors gauge theory:

```text
edge sectors label how regions are glued;
not every edge label is an ordinary local excitation.
```

## Case D: Thermal Soft Modes With N-Dependent Gap

Suppose relation modes are energetic but have gaps:

```text
Delta_N ~ 1/N.
```

Then an emitted cloud of `O(N)` relations carries:

```text
epsilon_rel ~ N Delta_N ~ O(1).
```

This can satisfy the heating condition.

This is attractive because it avoids exact degeneracy.

But it requires a reason for:

```text
Delta_N ~ 1/N.
```

Possible reasons:

```text
1. collective mode gap of an all-to-all system;
2. finite-size Goldstone/soft mode scaling;
3. horizon-size scaling analogue;
4. deliberate N-dependent coupling.
```

If the gap is put in by hand, the model again becomes less natural.

## Case E: Relation Information Carried In Correlations, Not Local Energies

The relation state might not be a tensor product of `N^2` independent qudits.

Instead:

```text
entropy is stored in correlation patterns among objects.
```

Then emission of one object changes many correlations, but the emitted energy
can remain small.

This is conceptually appealing but technically harder:

```text
we need a concrete Hilbert-space factorization and radiation map.
```

Tensor networks and random states often live here, but they are usually
kinematic.

## Heating Comparison

For pairwise relations and `E_N ~ mu N`:

```text
heating requires epsilon_N < about 2 mu.
```

Emitting one object plus its relation cloud:

```text
ordinary energetic connectors:
  epsilon_N ~ N Delta
  fails for Delta ~ O(1)

soft degenerate labels:
  epsilon_N ~ O(1) from visible object only
  can pass

N-dependent soft gap:
  epsilon_N ~ N * (1/N)
  can pass

constrained edge sectors:
  epsilon_N depends on energetic sector, not raw label count
  can pass
```

## Radiation Consequences

If the relation cloud has raw dimension:

```text
d^(N-1)
```

then radiation grows very quickly.

This is acceptable only if one of these is true:

```text
1. those relation labels are genuinely part of the emitted soft radiation;
2. they are highly constrained and not all independently accessible;
3. they form an archive/purifier, not ordinary observable Hawking quanta;
4. only coarse energetic quanta are observed, while soft relation labels carry
   hidden correlations.
```

The last option is closest to black-hole language:

```text
hard radiation quantum + soft memory.
```

But for a toy model, we must state the factorization honestly.

## Best Candidate For Our Purposes

The best finite toy is probably:

```text
object qudits:
  carry the mass/energy scale;

relation qudits:
  carry mostly degenerate labels;

small energetic sector:
  determines emitted energy and rate;

emission:
  removes one object plus its incident relation labels into radiation/archive.
```

Hamiltonian sketch:

```text
H_N = mu N
    + H_mix(relations, objects)
    + H_soft
    + H_emit
```

with:

```text
||H_soft|| per relation << 1
```

or:

```text
gap_rel(N) ~ 1/N.
```

This is not yet fully natural, but it makes the design requirement explicit.

## What Would Count As A Good Result

Minimal positive result:

```text
Show that soft relational degeneracy gives S ~ M^2, T ~ 1/M, C < 0, and
post-emission heating without imposing M ~ sqrt(S).
```

Stronger result:

```text
Construct a finite Hamiltonian/channel where relation labels are soft but not
completely inert, and emission carries them into an explicit radiation/archive
sector.
```

Strongest result:

```text
Derive or numerically observe an effective relation gap Delta_N ~ 1/N or an
edge-sector degeneracy from a less engineered Hamiltonian.
```

## Current Judgment

The ordinary energetic-connector model is probably not viable.

The viable versions are:

```text
1. soft degenerate relation labels;
2. constrained relation sectors;
3. N-dependent collective soft modes;
4. correlation-carried relation entropy.
```

The next model should not use ordinary independent energetic connector qubits.
It should explicitly separate:

```text
relation labels that carry entropy
from
energetic modes that carry emitted energy.
```

