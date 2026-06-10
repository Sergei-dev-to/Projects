# Landau/Fuzzy-Sphere Remaining Issues

## Purpose

Check whether the unresolved assumptions in the fuzzy-sphere/angular-shell
evaporator become natural in the lowest-Landau-level / quantum-Hall version.

The relevant reinterpretation:

```text
ordinary high-l harmonics -> bad, energetic;
LLL/angular orbitals      -> good, degenerate guiding-center labels;
fuzzy sphere Mat_N        -> projected operator algebra of the LLL.
```

## Issue 1: Soft Angular Labels

### Previous status

Softness was imposed.

### Landau-level status

Much better.

In a Landau level, angular/guiding-center labels are degenerate because the
kinetic energy is fixed by the Landau-level index.

On a disk:

```text
higher angular momentum m -> larger radius
but same Landau-level kinetic energy.
```

On a Haldane sphere:

```text
LLL degeneracy = 2Q + 1.
```

So high angular labels can be soft if they are:

```text
guiding-center / flat-band labels,
```

not ordinary Laplacian excitations.

This is the strongest naturalness improvement.

## Issue 2: Finite Angular Cutoff

### Previous status

We imposed:

```text
l <= L.
```

### Landau-level status

Natural.

The cutoff is controlled by flux/degeneracy:

```text
N = 2Q + 1
```

for a spherical LLL.

The number of available orbitals is finite because magnetic flux is finite.

For a droplet with fixed magnetic length:

```text
area ~ number of flux quanta.
```

So a shrinking droplet naturally has fewer available outer orbitals.

## Issue 3: Fuzzy-Sphere Mat_N And N^2 Entropy

### Previous status

The fuzzy sphere gave `Mat_N`, but we had to decide what the Hilbert space was.

### Landau-level status

Better, but still needs interpretation.

The LLL Hilbert space has:

```text
dim H_LLL = N.
```

The projected operator algebra has:

```text
End(H_LLL) = Mat_N,
dim Mat_N = N^2.
```

So `N^2` is natural for:

```text
operator/edge/relation labels,
```

not for a single-particle LLL Hilbert space.

To get entropy:

```text
S ~ N^2,
```

we still need to say that the soft microstates live in something like:

```text
edge/operator/relation sectors of Mat_N,
```

or a tensor register over those operator labels.

This is plausible but not automatic.

## Issue 4: M_N ~ N

### Previous status

Partly imposed.

### Landau-level status

Mixed.

In quantum Hall physics:

```text
area ~ flux ~ N.
```

If `N` is the number of LLL orbitals/flux quanta, then:

```text
area ~ N,
radius ~ sqrt(N).
```

But Schwarzschild wants:

```text
area ~ M^2,
radius ~ M.
```

So there are two possible identifications:

### Identification A: N = area / flux

Then:

```text
S ~ N
M ~ sqrt(N)
```

This is just the old area-register logic.

### Identification B: N = linear cutoff / radius

Then:

```text
S ~ N^2
M ~ N.
```

This matches Schwarzschild.

The fuzzy-sphere `Mat_N` naturally supports identification B because:

```text
number of matrix harmonics ~ N^2.
```

But the simple LLL degeneracy supports identification A:

```text
number of single-particle orbitals ~ N.
```

Therefore:

```text
we should not use single-particle LLL degeneracy as the entropy count.
we should use the fuzzy/operator algebra Mat_N as the relational/edge count.
```

This is important.

## Issue 5: N -> N-1 Evaporation

### Previous status

Model choice.

### Landau-level status

Somewhat natural.

Quantum Hall droplets naturally have outer orbitals. On the disk:

```text
larger m orbitals live farther out.
```

Removing/shrinking the edge removes high-m outer orbitals.

On the fuzzy sphere:

```text
Mat_N -> Mat_(N-1)
```

removes the outer angular shell:

```text
2N-1 labels.
```

So shell removal is natural as a kinematic operation.

But a physical evaporation process that changes:

```text
N -> N-1
```

still needs a channel or Hamiltonian.

## Issue 6: Hard Emission Energy epsilon ~ 1/N

### Previous status

Thermodynamic assignment.

### Landau-level status

Still not automatic.

Quantum Hall edge modes typically have energies controlled by:

```text
edge velocity / circumference ~ v/R.
```

If:

```text
R ~ N,
```

then:

```text
edge spacing ~ 1/N.
```

This is encouraging.

But if:

```text
area ~ N,
R ~ sqrt(N),
```

then edge spacing scales like:

```text
1/sqrt(N).
```

So again we need the linear-size identification:

```text
N ~ R.
```

Possible natural route:

```text
hard radiation energy comes from edge/circumference scale ~ 1/R.
```

Then if:

```text
R ~ M ~ N,
```

we get:

```text
epsilon ~ 1/N.
```

## Issue 7: Hawking-Like Rate P ~ 1/N^2

### Previous status

Not derived.

### Landau-level status

Still not derived.

Quantum Hall edge physics gives chiral edge modes and tunneling/emission
channels, but it does not naturally give Schwarzschild blackbody scaling:

```text
P ~ area * T^4.
```

To get that, we probably still need:

```text
hard radiation coupled to a 3D bath with rho(omega) ~ omega^2.
```

Then:

```text
number flux ~ area * T^3,
power ~ area * T^4.
```

The quantum-Hall/fuzzy part supplies the soft degeneracy and edge labels, not
the 3D radiation phase space.

## Issue 8: Information Flow

### Previous status

Open.

### Landau-level status

Potentially better.

Quantum Hall systems naturally separate:

```text
bulk topological/flat-band degrees;
edge modes;
quasiparticles;
topological/anyon data.
```

This gives a plausible hard/soft split:

```text
hard radiation:
  energetic edge/quasiparticle emission;

soft memory:
  changed edge/LLL/fuzzy labels.
```

But Page-like dynamics still requires an explicit unitary channel.

## Naturalness Table

```text
Assumption                         Landau/fuzzy status
----------------------------------------------------------------
high angular labels are soft        natural via LLL degeneracy
finite cutoff                       natural via flux / finite matrix size
N^2 shell count                     natural for Mat_N/operator algebra
M ~ N                               natural only if N is linear size, not flux count
N -> N-1                            kinematically natural, dynamically open
epsilon ~ 1/N                       plausible from edge scale 1/R if R~N
P ~ 1/N^2                           still needs 3D radiation phase space
unitary information flow            still needs explicit channel
```

## Best Version So Far

The most natural version is:

```text
1. N labels linear size / radius sector.
2. At size N, the boundary has a fuzzy-sphere/LLL-like projected algebra Mat_N.
3. Soft microstates live in relational/edge/operator labels of Mat_N.
4. Their count scales as N^2.
5. Hard edge/radiation energy is set by circumference scale, epsilon ~ 1/N.
6. Evaporation N -> N-1 removes the outer matrix-angular shell.
7. Soft shell labels purify the entropy loss.
8. Hard quanta couple to a 3D bath to get Hawking-like flux scaling.
```

This is not fully derived, but it is less arbitrary than:

```text
area register with M ~ sqrt(n).
```

## Main Remaining Tension

The quantum Hall intuition most naturally gives:

```text
degeneracy ~ area / magnetic length^2.
```

Black-hole scaling wants:

```text
entropy ~ area ~ radius^2.
```

That is fine if:

```text
N ~ radius
Mat_N count ~ N^2.
```

But if someone reads `N` as the LLL orbital count/flux count, then:

```text
N already means area.
```

We must avoid this ambiguity.

Use notation carefully:

```text
R = size/radius sector
K_R ~ R^2 = number of soft labels
Mat_R = fuzzy/angular operator algebra with dimension R^2
```

Do not let `N` simultaneously mean radius and flux degeneracy.

## Current Judgment

The Landau/fuzzy approach naturalizes the soft angular labels.

It does not by itself naturalize everything.

The remaining irreducible inputs are:

```text
1. identify matrix size/cutoff with linear radius;
2. provide a sector-changing evaporation channel;
3. use 3D hard radiation phase space for the rate;
4. track information in hard+soft radiation.
```

That is probably good enough to proceed to a minimal channel model, as long as
we state those inputs explicitly.

