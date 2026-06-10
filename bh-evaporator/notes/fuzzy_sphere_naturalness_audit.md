# Fuzzy-Sphere Branch Naturalness Audit

## Purpose

Identify which ingredients of the fuzzy-sphere/angular-shell evaporator are
structural and which are still imposed.

The goal is not to make everything natural immediately. The goal is to avoid
confusing:

```text
derived from the model
```

with:

```text
chosen to reproduce black-hole phenomenology.
```

## Current Model

The coherent sector model is:

```text
H_N = tensor_{l=0}^{N-1} tensor_{m=-l}^{l} C^d
S_N = N^2 log d
M_N = mu N
T_N = (dS/dM)^-1 ~ 1/N
V_N : H_N -> H_(N-1) tensor R_hard(N) tensor H_shell(N)
```

with:

```text
H_shell(N) = tensor_{m=-(N-1)}^{N-1} C^d.
```

## Ingredient Audit

### A1: Angular shell count

Status:

```text
structural.
```

Reason:

```text
The fuzzy sphere algebra Mat_N decomposes into angular shells:

  Mat_N = direct sum_{l=0}^{N-1} V_l,
  dim V_l = 2l+1.

Therefore the number of angular labels is N^2.
```

This is not imposed.

### A2: Tensor-product Hilbert space over angular labels

Status:

```text
model choice.
```

Reason:

```text
Mat_N itself is an N^2-dimensional vector space, not a d^(N^2)-dimensional
qudit Hilbert space.
```

To get entropy:

```text
S_N = N^2 log d
```

we choose one label/qudit per angular matrix harmonic.

This is reasonable for a finite soft-mode register, but it is not forced by
the fuzzy sphere alone.

How to improve naturalness:

```text
Interpret each angular harmonic as an independent soft edge sector, analogous
to gauge edge modes or soft horizon charges.
```

Still unresolved:

```text
derive the label Hilbert space from a constrained field/gauge system.
```

### A3: Softness / near degeneracy

Status:

```text
currently imposed.
```

Reason:

```text
The fuzzy-sphere Laplacian gives l(l+1), so ordinary harmonic excitations are
not soft.
```

How to improve naturalness:

Use one of these mechanisms:

```text
1. Gauge edge sectors:
   labels are superselection/boundary data, not bulk excitations.

2. Soft hair:
   angular labels are zero/near-zero-energy memory charges.

3. Topological/deformation labels:
   labels count degenerate boundary sectors protected by constraints.

4. Critical collective modes:
   gaps shrink with system size, e.g. Delta_N ~ 1/N.
```

Best path:

```text
Use gauge-edge/soft-sector language for the first model. Do not treat the
labels as Laplacian excitations.
```

### A4: Mass/size law M_N ~ N

Status:

```text
partly natural, partly imposed.
```

Reason:

For a Schwarzschild black hole:

```text
radius R ~ M.
```

For a fuzzy sphere:

```text
N controls angular cutoff / number of cells per linear direction.
```

If:

```text
N ~ R / ell_0,
```

then:

```text
M ~ R ~ N.
```

This is natural if the fuzzy sphere is an angular discretization of a boundary
whose physical radius is proportional to the mass.

But for an abstract non-gravitational fuzzy sphere:

```text
M_N ~ N
```

is still an assignment.

How to improve naturalness:

```text
Define N as the size/radius sector from the start, not merely matrix size.
The fuzzy sphere then supplies the angular mode count at that size.
```

This is acceptable but should be stated plainly.

### A5: Evaporation step N -> N-1

Status:

```text
model choice.
```

Reason:

The angular shell removal is structurally clean:

```text
N^2 - (N-1)^2 = 2N-1.
```

But a physical process that changes the fuzzy-sphere cutoff:

```text
N -> N-1
```

is not derived.

How to improve naturalness:

Possible mechanisms:

```text
1. Sector-changing channel:
   treat evaporation as an open-system transition between size sectors.

2. Fuzzy-space topology/change literature:
   use matrix-algebra branching/splitting maps.

3. Quantum error/erasure analogy:
   one outer angular shell becomes inaccessible to the core and is transferred
   to radiation/memory.

4. Matrix model block reduction:
   by analogy, shrinking rank reduces active angular algebra.
```

The cleanest first step is a sector-changing isometry. A Hamiltonian derivation
can come later.

### A6: Hard quantum energy epsilon_N ~ T_N ~ 1/N

Status:

```text
thermodynamic assignment.
```

Reason:

Given:

```text
S_N ~ N^2
M_N ~ N,
```

the thermodynamic temperature is:

```text
T_N ~ 1/N.
```

So assigning typical hard emission energy:

```text
epsilon_N ~ T_N
```

is natural in a thermal emission model.

But a microscopic channel producing this scale is not derived.

How to improve naturalness:

```text
Use a radiation spectral function or transition rule satisfying detailed
balance at temperature T_N.
```

This is standard for thermal channels, but still a channel-level input.

### A7: Power law P ~ 1/N^2

Status:

```text
not derived.
```

Reason:

Counting gives:

```text
T ~ 1/N.
```

To get Hawking power:

```text
P ~ N^2 T^4 ~ 1/N^2,
```

we need a blackbody-like flux mechanism:

```text
number flux ~ area * T^3.
```

The fuzzy-shell model does not automatically produce this.

How to improve naturalness:

Options:

```text
1. Couple hard radiation to a 3+1-dimensional bath:
   blackbody phase space gives T^3 number flux.

2. Add field-like radiation modes with density of states rho(omega) ~ omega^2.

3. Keep rate law phenomenological but isolate it as the only remaining input.
```

Most natural:

```text
field-like hard radiation bath with rho(omega) ~ omega^2.
```

That gives the T^3 factor without arbitrary tuning.

### A8: Radiation purification by shell labels

Status:

```text
structurally consistent, physically interpretive.
```

Reason:

The dimension balance works:

```text
dim H_N = dim H_(N-1) * dim H_shell(N)
```

if:

```text
H_N = tensor over angular labels.
```

So the shell can purify exactly the entropy lost by the core.

But physical interpretation is open:

```text
is H_shell observable soft radiation,
edge memory,
or an archive sector?
```

How to improve naturalness:

Use the hard/soft split:

```text
hard radiation:
  carries energy and ordinary observable quanta;

soft shell:
  carries memory/edge labels at little energy.
```

This matches soft-hair-inspired models better than treating all shell labels
as ordinary radiation.

## Naturalness Ranking

```text
Most structural:
  angular shell count;
  entropy scaling from N^2 labels;
  temperature scaling once M~N is accepted;
  shell dimension balance.

Moderately natural:
  M~N if N is physical radius/size;
  hard emission energy ~ T;
  hard/soft radiation split.

Still imposed:
  softness of angular labels;
  N -> N-1 dynamics;
  detailed rate law;
  tensor-product soft Hilbert space per harmonic.
```

## What We Can Fix Now

### Fix 1: Replace arbitrary rate law with radiation phase space

Use a hard radiation bath with:

```text
rho(omega) ~ omega^2.
```

Thermal emission at:

```text
T_N ~ 1/N
```

then naturally gives:

```text
number flux ~ area * T^3,
power ~ area * T^4.
```

This makes the acceleration less imposed.

### Fix 2: Treat shell labels as edge sectors, not excitations

State explicitly:

```text
The soft shell is a memory/edge Hilbert space.
It is not governed by the fuzzy Laplacian energy.
```

This prevents the high-l energy objection.

### Fix 3: Use N as radius/size sector

Do not say:

```text
matrix size magically equals mass.
```

Say:

```text
N labels the size sector; fuzzy-sphere Mat_N is the angular edge algebra
available at that size.
```

Then:

```text
M~N
```

is a definition of the size-sector model, not a hidden fuzzy-sphere theorem.

### Fix 4: Make the first channel explicitly isometric

Define:

```text
H_N = H_(N-1) tensor H_shell(N)
```

by construction, using the tensor product over modes.

Then:

```text
V_N : H_N -> H_(N-1) tensor H_shell(N) tensor R_hard(N)
```

can be made unitary/isometric without transition-record labels.

This fixes the direct-sum/tensor problem.

## What We Cannot Fix Yet

### Unfixed 1: Deriving soft edge sectors

We can motivate from gauge edge modes/soft hair, but not derive from a simple
non-gravitational Hamiltonian yet.

### Unfixed 2: Deriving N -> N-1 from Hamiltonian dynamics

The first coherent model will be a sector-changing channel, not a closed
Hamiltonian.

### Unfixed 3: Nontrivial Page/early-late structure

The shell purification may make information recovery too easy unless we add
scrambling and delayed release.

## Proposed More Natural Model

Use the following as the next formal target:

```text
Size sector:
  N = R / ell_0.

Core Hilbert space:
  H_N = tensor_{l=0}^{N-1} tensor_{m=-l}^{l} C^d_edge.

Energy:
  E_N = mu N + energetic excitations,
  edge labels are degenerate or nearly degenerate.

Temperature:
  T_N = (dS/dE)^-1 = mu / (2N log d_edge).

Hard radiation:
  field-like modes with rho(omega) ~ omega^2.

Soft radiation/memory:
  H_shell(N) = tensor_{m=-(N-1)}^{N-1} C^d_edge.

Evaporation channel:
  N -> N-1,
  hard quantum sampled thermally at T_N,
  soft shell transferred to memory/radiation.
```

This fixes the biggest naturalness issue around rates by using field phase
space, and fixes the tensor issue by construction.

It still leaves softness and sector-changing dynamics as explicit assumptions.

## Current Judgment

The fuzzy-sphere branch can be made more natural, but not fully derived.

The best honest claim would be:

```text
Given a soft angular edge Hilbert space with size cutoff N, the black-hole
thermodynamic backbone follows structurally. Coupling the hard sector to a
3D radiation bath supplies the Hawking-like rate scaling. The remaining
nontrivial assumptions are the origin of the soft edge sectors and the
sector-changing evaporation channel.
```

That is cleaner than Track E and more natural than arbitrary connectors.

