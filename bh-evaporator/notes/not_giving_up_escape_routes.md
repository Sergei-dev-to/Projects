# Not Giving Up: Routes To Natural Physical R^2 Entropy

## Question

The matrix Chern-Simons / quantum Hall review gave a useful warning:

```text
raw matrix labels are not physical entropy after constraints.
```

But that does not mean the program is dead.

The sharper target is now:

```text
find a non-gravitational quantum system where the physical constrained Hilbert
space already contains area-scaling soft/topological entropy.
```

Then add evaporation dynamics.

## What We Need

The model should provide, as naturally as possible:

```text
1. physical Hilbert spaces H_R, not just label sets;
2. log dim H_R ~ R^2;
3. soft or topological degeneracy, not ordinary high-energy modes;
4. a natural shell relation H_R -> H_(R-1) + emitted sector;
5. hard radiation energy scale epsilon_R ~ 1/R;
6. enough information structure to test Page-like diagnostics.
```

The hard part is not just `R^2` counting. It is:

```text
R^2 physical states at low energy, after constraints.
```

## Candidate A: Non-Abelian Anyon / Fusion Droplet

This is the best escape route.

Basic idea:

```text
Use a 2D topologically ordered system with non-Abelian anyons or defects.
The physical Hilbert space is the fusion space.
For many non-Abelian anyons, dim H grows exponentially with anyon number:

dim H_n ~ d^n.
```

If a droplet of linear size R carries:

```text
n_R ~ R^2
```

topological defects, punctures, plaquettes, or boundary anyon labels, then:

```text
S_R ~ n_R log d ~ R^2.
```

This is not raw matrix counting. It is physical fusion-space counting.

### Why this helps

It directly solves the matrix-CS failure:

```text
The entropy is not N^2 unconstrained matrix entries.
The entropy is the dimension of a constrained topological fusion space.
```

It also naturally explains why the entropy is soft:

```text
fusion channels are topological / protected / nearly degenerate.
```

This is much closer to the horizon intuition than ordinary qubits.

### Main issue

If the anyons are actual bulk quasiparticle excitations, then putting:

```text
n_R ~ R^2
```

anyons into the droplet costs:

```text
energy ~ R^2 * gap.
```

That would kill the desired:

```text
M_R ~ R.
```

So the anyons cannot be ordinary energetic bulk quasiparticles.

Viable versions need one of:

```text
1. boundary punctures/defects with soft fusion degeneracy;
2. holes/defects/domain walls whose fusion channels are nearly degenerate;
3. a topological code/subspace where the labels are constraints, not
   independently excited particles;
4. a Chern-Simons/conformal-block Hilbert space assigned to punctures with
   energy supplied by a separate hard sector.
```

This is not a minor point. It decides whether the anyon model is genuinely
black-hole-like or just an expensive gas of anyons.

### Evaporation picture

The natural evaporation step would be:

```text
remove a boundary layer of O(R) punctures/defects/edge labels.
```

Then:

```text
Delta S_R = S_R - S_(R-1) ~ R.
```

If the hard energy emitted per step is:

```text
epsilon_R ~ 1/R,
```

then:

```text
T_R ~ epsilon_R ~ 1/R
```

is compatible with:

```text
dS/dM ~ R.
```

The fusion space supplies entropy; the hard emitted quantum supplies energy.

### Status

Promising, but the model must avoid treating `R^2` anyons as energetic
quasiparticles.

The right slogan:

```text
topological fusion-space entropy, not anyon gas entropy.
```

## Candidate B: String-Net / Levin-Wen / Quantum Double Patch

This is the Hamiltonian version of Candidate A.

Basic idea:

```text
Use an exactly solvable 2D lattice Hamiltonian with topological order.
The local Hilbert space and constraints are microscopic.
Boundary defects, punctures, or anyonic excitations define physical fusion
spaces.
```

Why it helps:

```text
The Hilbert space is not invented after the fact.
It comes from a local spin Hamiltonian.
The anyons/fusion rules are emergent.
```

Main issue:

Ordinary topological order on a simply connected disk has only O(1)
topological ground-state degeneracy. Area-law entanglement exists, but that is
not the same as a thermodynamic number of internal microstates.

To get:

```text
S ~ R^2,
```

we need many punctures/defects/boundary labels or an extensive topological
defect structure.

That may be acceptable if the black-hole analogue is:

```text
a horizon densely populated by soft topological boundary labels.
```

But it is not automatic from the bare topological phase on a disk.

### Status

Best route if we insist on a concrete local Hamiltonian.

But it probably needs engineered punctures/defects, so it is less clean than
the abstract fusion-droplet picture.

## Candidate C: Large-N Gauge / Matrix Quantum Mechanics

This route should not be discarded too quickly.

Matrix CS failed to give physical `N^2` entropy because it is highly
constrained/topological and equivalent to a Calogero model.

But ordinary large-N gauge/matrix systems can have physical:

```text
S ~ N^2
```

in deconfined/highly excited sectors.

This is not raw bookkeeping. It is standard large-N thermodynamics.

Why it helps:

```text
adjoint degrees of freedom are relational;
O(N^2) entropy is physical;
rank-changing / block-emission processes exist in matrix models;
the D0-brane/black-zero-brane story already uses this mechanism.
```

Main issue:

This is very close to holographic black-hole physics.

It may violate our desired control condition:

```text
all phenomenology, no gravity.
```

Still, a non-holographic large-N matrix model could be useful as a comparison.

### Status

Technically strong, conceptually less clean.

It may be the mature version of the relational entropy idea, but not the
cleanest non-gravitational control.

## Candidate D: Chern-Simons Edge/WZW Hilbert Space

Chern-Simons theory with boundaries has physical edge Hilbert spaces.

This solves:

```text
why edge modes exist;
why they are soft/topological;
why factorization requires extra boundary structure.
```

But ordinary edge CFT counting is energy dependent. It does not automatically
give:

```text
dim H_R ~ exp(R^2)
```

at fixed low energy.

To get black-hole-like entropy, one would need scaling input such as:

```text
many punctures;
large level;
large boundary charge;
many boundary components;
or a Cardy regime with energy/central charge scaling appropriately.
```

### Status

Good support machinery.

Not by itself the missing model.

## Candidate E: Quantum Error-Correcting / Stabilizer-Code Patch

Another possible route is a code patch with many stabilizer-compatible states:

```text
physical Hilbert space = constrained code subspace;
soft labels = logical or gauge degrees;
shrinking = code deformation / boundary movement.
```

This gives a concrete Hamiltonian-like system and explicit information-flow
language.

Main issue:

Standard topological codes have:

```text
logical degeneracy = O(1) or boundary-count dependent,
not exp(area).
```

Subsystem codes can have extensive gauge degrees, but then we must be careful:

```text
are those physical states or gauge redundancy?
```

### Status

Potentially useful for Page/information diagnostics.

Probably weak for thermodynamic area entropy unless heavily designed.

## Ranking

```text
1. Non-Abelian fusion droplet / punctured topological boundary
   Best chance at physical soft R^2 entropy.

2. String-net / local Hamiltonian with many defects or punctures
   Best chance at microscopic concreteness.

3. Large-N gauge/matrix quantum mechanics
   Best chance at natural physical N^2 entropy, but too close to holography.

4. Chern-Simons edge/WZW Hilbert spaces
   Best support for edge-mode legitimacy, not enough alone.

5. Stabilizer/topological code patch
   Best for information-flow diagnostics, weak for entropy unless modified.
```

## Key Reframing

The search should no longer be:

```text
Can Mat_R itself be the entropy Hilbert space?
```

It should be:

```text
Can Mat_R or a 2D boundary label set index a physical fusion/topological
Hilbert space whose dimension grows like exp(R^2)?
```

This puts the anyon/fusion branch back into play.

The earlier fusion-register pilot did not kill this. It only showed:

```text
a simple Fibonacci path register with random sector Hamiltonians does not
produce special dynamics beyond the imposed entropy law.
```

That is different from the current question:

```text
Can a fusion/topological system naturalize the area-entropy Hilbert space?
```

## Most Promising Concrete Model

The cleanest next model is:

```text
finite 2D topological boundary patch with n_R ~ R^2 soft puncture/defect
labels, plus a hard boundary radiation channel.
```

Hilbert spaces:

```text
H_core(R) = V_fusion(n_R, total charge = vacuum) tensor H_hard_core(R)

n_R = alpha R^2
```

Evaporation step:

```text
V_fusion(n_R)
  -> V_fusion(n_(R-1)) tensor V_shell(R) tensor hard quantum
```

where:

```text
dim V_fusion(n_R) ~ d^(n_R)
dim V_shell(R) ~ d^(n_R - n_(R-1)) ~ d^(O(R))
epsilon_R ~ 1/R
```

The hard quantum can be ordinary radiation. The soft shell carries the
topological/fusion information released by losing a boundary layer.

This keeps:

```text
entropy source    = physical fusion space
energy source     = separate hard boundary mode
shrinking source  = loss of boundary layer
```

separate, which is what black holes appear to do phenomenologically.

## What Would Count As A Real Win

A real result would be:

```text
There exists a non-gravitational topological quantum system with physical
fusion-space entropy S ~ R^2, a shrinking sector map R -> R-1, and a hard
radiation channel with epsilon ~ 1/R. Under these ingredients, the system
reproduces negative heat capacity, accelerating evaporation, and Page-like
purification without gravity.
```

This would not solve the black-hole information problem.

It would say something sharper:

```text
Much of the black-hole evaporation package follows from a soft topological
area register plus a hard radiation channel, not from gravity alone.
```

Then the genuinely gravitational question becomes:

```text
Why does gravity supply exactly such a topological/edge/fusion Hilbert space,
and how do islands/wormholes compute the same information flow?
```

## Immediate Next Checks

Do these before more numerics:

```text
1. Review non-Abelian anyon fusion-space dimension formulas in a fixed total
   charge sector.

2. Check whether local Hamiltonian realizations can give many soft boundary
   defects without energy ~ R^2.

3. Check whether punctures/holes/twist defects in topological codes give
   extensive fusion degeneracy with controllable energy cost.

4. Decide whether the emitted soft shell should be:
   a. actual anyons leaving the droplet;
   b. a detached boundary code/fusion sector;
   c. a record in an exterior topological memory.

5. Only then build a minimal channel model.
```

