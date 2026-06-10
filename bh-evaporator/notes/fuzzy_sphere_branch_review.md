# Fuzzy-Sphere Branch Review

## Purpose

Review the fuzzy-sphere/angular-shell branch and identify what we may have
overlooked before building a channel.

## What Looks Solid

### 1. Angular shell count

The algebraic fact is solid:

```text
Mat_N = direct sum_{l=0}^{N-1} V_l
dim V_l = 2l + 1
dim Mat_N = N^2.
```

The script:

```text
sim/fuzzy_sphere_shells.py
```

verifies that the fuzzy-sphere Laplacian has eigenvalues:

```text
l(l+1)
```

with degeneracies:

```text
2l+1.
```

### 2. Shrinking count

The step:

```text
N -> N-1
```

removes:

```text
N^2 - (N-1)^2 = 2N - 1
```

states in the angular-mode basis, exactly the outer shell:

```text
l = N-1.
```

### 3. Thermodynamic scaling

If:

```text
S_N = N^2 log d
M_N = mu N
```

then:

```text
S ~ M^2
T ~ 1/M
C < 0.
```

This improves over Track E because the square comes from angular state
counting, not from choosing `M ~ sqrt(n)`.

## Main Overlooked Issue: Direct Sum Is Not Tensor Factorization

We have been writing:

```text
Mat_N -> Mat_(N-1) + shell.
```

Algebraically, this is a direct-sum/vector-space decomposition:

```text
Mat_N = Mat_(N-1) ⊕ V_{N-1}
```

at the level of dimensions/representations.

But radiation purification wants something closer to:

```text
H_N -> H_(N-1) tensor R_N.
```

Those are not the same.

Dimension comparison:

```text
dim Mat_N = N^2
dim Mat_(N-1) + dim shell = (N-1)^2 + (2N-1) = N^2
```

but:

```text
dim H_N = d^(N^2)
dim H_(N-1) tensor H_shell = d^((N-1)^2) * d^(2N-1) = d^(N^2).
```

So the tensor factorization works only after we interpret each matrix harmonic
mode as carrying a qudit/label:

```text
H_N = tensor_{l=0}^{N-1} tensor_{m=-l}^l C^d.
```

That is not simply `Mat_N` as a Hilbert space. It is a Fock/qudit Hilbert space
whose mode labels are supplied by the fuzzy sphere.

Corrected statement:

```text
The fuzzy sphere supplies the finite angular mode index set.
The evaporator Hilbert space is a tensor product over those mode labels.
```

This distinction matters.

## Issue 2: Softness Is Still Assumed

The fuzzy-sphere Laplacian gives:

```text
lambda_l = l(l+1).
```

So ordinary excitations of the outer shell are high angular momentum
excitations.

To use these labels as black-hole-like entropy, they must be:

```text
edge labels;
memory labels;
gauge/constraint sectors;
near-degenerate internal labels;
or collective soft modes.
```

The fuzzy sphere does not derive softness.

It only gives:

```text
a finite angular index set with area-like count.
```

## Issue 3: Why M_N ~ N?

The model assumes:

```text
M_N = mu N.
```

This is natural if:

```text
N is a radius/size/mass index.
```

But fuzzy-sphere matrix size `N` is not automatically mass. It is:

```text
representation dimension / angular cutoff.
```

We need a convention or mechanism:

```text
larger angular cutoff corresponds to larger object size,
and mass is proportional to that size.
```

This is black-hole-like for Schwarzschild:

```text
radius ~ mass.
```

But it is not generic for arbitrary fuzzy spheres.

## Issue 4: The Energy Gap Is A Sector Gap, Not A Laplacian Gap

The emission energy should be:

```text
epsilon_N ~ T_N ~ 1/N.
```

This is not:

```text
energy of shell l=N-1 under the fuzzy Laplacian.
```

It is a transition energy between macroscopic sectors:

```text
N -> N-1.
```

Correct interpretation:

```text
N-sector labels the size/mass sector.
Mat_N labels the internal soft degeneracy of that sector.
The hard quantum energy is controlled by the thermodynamic derivative, not by
the angular Laplacian.
```

If we forget this, the model collapses back into ordinary high-l excitations.

## Issue 5: Rate Law Is Not Solved

The counting gives:

```text
T ~ 1/N.
```

It does not give:

```text
P ~ 1/N^2.
```

To get that we still need something like:

```text
gamma_N ~ N^2 T^3 ~ 1/N
epsilon_N ~ T ~ 1/N.
```

In a sector model, this will likely be an imposed spectral/rate rule unless we
build more dynamics.

That is acceptable as a diagnostic layer, but it should not be hidden.

## Issue 6: Radiation May Be Too Large

The emitted shell has dimension:

```text
d^(2N-1).
```

This exactly purifies the lost entropy if the core shrinks from:

```text
d^(N^2)
```

to:

```text
d^((N-1)^2).
```

But it means the soft radiation/archive grows very fast.

This is acceptable only if we distinguish:

```text
hard observable radiation:
  small energy-carrying subsystem;

soft shell memory:
  large entropy-carrying, low-energy purifier.
```

If we call the whole shell ordinary radiation, Page behavior may become
kinematic/trivial.

## Issue 7: Relation To Existing Literature

We should not overclaim novelty of:

```text
angular degeneracy gives area scaling.
```

The literature already has nearby versions:

```text
brick-wall / stretched-horizon angular mode counting;
Krishnan-Pathak normal modes;
soft hair angular charges;
gauge edge modes on spherical entangling surfaces;
fuzzy-sphere matrix harmonics.
```

What remains potentially interesting is:

```text
using the angular-shell count as a finite shrinking Hilbert-space evaporator
with an explicit hard/soft radiation split.
```

## Cleaned-Up Model Statement

The coherent model is:

```text
Sector label:
  N = size/mass index.

Mode labels:
  fuzzy-sphere harmonics (l,m), 0 <= l <= N-1.

Hilbert space:
  H_N = tensor_{l=0}^{N-1} tensor_{m=-l}^l C^d.

Entropy:
  S_N = log dim H_N = N^2 log d.

Mass:
  M_N = mu N.

Temperature:
  T_N = mu / (2 N log d).

Evaporation:
  V_N : H_N -> H_(N-1) tensor R_hard(N) tensor H_shell(N),
  H_shell(N) = tensor_{m=-(N-1)}^{N-1} C^d.

Hard quantum:
  carries energy epsilon_N ~ T_N.

Soft shell:
  carries/purifies entropy Delta S_N = (2N-1) log d.
```

This is consistent at the counting/channel level.

It is not yet a Hamiltonian model.

## What Might Work

The promising route is:

```text
1. Treat fuzzy-sphere harmonics as mode labels for a soft edge Hilbert space.
2. Use N as a sector/size label, not as a dynamical matrix eigenvalue.
3. Define evaporation as an isometry that removes the outer shell.
4. Keep hard radiation and soft shell memory separate.
5. Later ask whether a Hamiltonian or random circuit can realize this channel.
```

This avoids the fixed-sphere high-l energy problem.

## What Might Not Work

The model becomes weak if:

```text
1. softness is simply declared with no analogy or constraint;
2. M_N ~ N is just as arbitrary as Track E's M ~ sqrt(n);
3. the shell memory makes information recovery trivial;
4. rate laws are imposed rather than derived;
5. the model is too close to actual horizon soft hair to count as
   non-gravitational.
```

## Current Judgment

The fuzzy-sphere branch is coherent if we treat it as a sector/channel model
with soft edge labels.

It is not coherent if we treat outer-shell harmonics as ordinary energetic
Laplacian excitations.

The next useful step is to build the minimal channel skeleton and check:

```text
dimension balance;
entropy loss;
hard/soft radiation split;
Page-like dimension bounds;
comparison to Track E.
```

