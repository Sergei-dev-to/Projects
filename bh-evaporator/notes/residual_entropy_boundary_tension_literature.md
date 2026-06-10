# Residual Entropy + Boundary Tension: Literature Review

## Purpose

The finite-group gauge droplet leaves one main non-naturalness:

```text
Why should the bulk have area-extensive soft entropy while the energy is
mostly boundary/interface energy?
```

This note reviews nearby known systems.

## Short Verdict

There is no perfect off-the-shelf model, but the pattern is not exotic.

Known ingredients:

```text
1. ice-rule / frustrated systems:
   extensive residual entropy from local constraints;

2. lattice gauge theories:
   physical constrained Hilbert spaces and boundary edge modes;

3. quantum dimer / RK-type models:
   constrained configuration spaces and exactly solvable equal-amplitude
   states;

4. fracton / subsystem gauge models:
   unusual constrained degeneracy, sometimes scaling with L^2.
```

The closest natural physical picture is:

```text
a frustrated/ice-rule or gauge-constrained droplet with residual entropy,
embedded in a trivial phase with an interface tension.
```

That is less artificial than an abstract area register, but it is not a
standard stable topological ground-state entropy.

## Candidate 1: Ice-Rule / Spin-Ice / Six-Vertex Manifolds

### What the literature gives

Ice-rule systems have local constraints such as:

```text
two-in / two-out at each vertex or tetrahedron.
```

The number of allowed configurations grows exponentially with system area or
volume.

For square ice / six-vertex models:

```text
number of states on an n x n grid ~ c^(n^2),
```

with Lieb's square-ice constant:

```text
c = (4/3)^(3/2) = 8 sqrt(3) / 9.
```

Spin ice is the three-dimensional magnetic analogue. Its low-energy physics is
well described by an emergent gauge-field / Coulomb phase, with magnetic
monopole-like excitations.

### Why it helps

This is almost exactly the kind of bulk we want:

```text
local microscopic constraints;
many equal-energy or nearly equal-energy configurations;
extensive residual entropy;
emergent gauge language.
```

A droplet of such a phase inside a trivial/polarized phase can have:

```text
bulk residual entropy ~ area or volume;
interface energy ~ boundary.
```

For our 2D evaporator:

```text
2D ice droplet:
  S ~ area ~ R^2
  M ~ interface length ~ R
```

This is the most physically intuitive realization of the edge-tension droplet.

### What it does not solve

The entropy is mostly classical residual entropy unless we quantize the
manifold.

Also, generic perturbations can lift the degeneracy or select ordered states.
So the model needs either:

```text
robust frustration,
weak splitting compared with evaporation scale,
or an explicitly quantum constrained Hamiltonian.
```

### Status

Best physical intuition for the soft bulk.

Probably the simplest story:

```text
black-hole-like thermodynamics from an ice-rule droplet with line tension.
```

## Candidate 2: Finite-Group Lattice Gauge Theory

### What the literature gives

Lattice gauge theory naturally has:

```text
link Hilbert spaces;
Gauss constraints;
boundary edge modes under spatial factorization.
```

Donnelly's lattice-gauge entropy decomposition makes the edge-mode point
explicit: gauge-theory regions require edge states transforming under boundary
gauge transformations, and entropy decomposes into boundary-representation and
correlation terms.

Our own finite `Z_q` counting found:

```text
dim H_phys(D) = q^(E - V + 1).
```

For a planar disk:

```text
E - V + 1 = number of plaquettes.
```

So:

```text
S ~ area.
```

### Why it helps

This gives the cleanest exact Hilbert-space count.

It is quantum from the start:

```text
physical Hilbert space = gauge-invariant link states.
```

The soft shell record also has a natural gauge-theory interpretation.

### What it does not solve

The usual fully gapped topological gauge ground state on a disk does not have
area-extensive degeneracy. If we impose a magnetic flatness term and select the
topological ground sector, the entropy collapses.

So the finite-group gauge droplet must live in a very soft constrained sector:

```text
Gauss law imposed;
plaquette fluxes not energetically lifted, or only weakly lifted.
```

This is closer to:

```text
zero-coupling / flat-band / frustrated gauge matter
```

than to ordinary topological order.

### Status

Best exact counting model.

Needs a physical reason for the plaquette-flux degeneracy to remain soft.

## Candidate 3: Quantum Dimer / Rokhsar-Kivelson Models

### What the literature gives

Quantum dimer models have constrained Hilbert spaces:

```text
one dimer touches each site,
or maximal dimer/monomer constraints.
```

At Rokhsar-Kivelson-type points, the exact ground state is often an
equal-amplitude superposition over an exponentially large classical
configuration space.

Recent monomer-dimer variants explicitly map to `Z_2` gauge theories with
matter.

### Why it helps

They are concrete quantum Hamiltonians whose low-energy Hilbert space is a
constraint manifold.

They are useful for building an explicit unitary erosion model:

```text
local flips / ring exchanges;
constrained boundary dynamics;
emergent gauge description.
```

### What it does not solve

The RK ground state itself is often unique within a sector, not exponentially
degenerate.

So quantum dimer models do not automatically give thermodynamic residual
entropy as ground-state degeneracy. They give:

```text
an exponentially large constrained basis,
but a coherent ground-state superposition over it.
```

For our evaporator, that may still be useful if the microcanonical window
contains many constrained states, but it is not as direct as the gauge-counting
or ice-rule residual entropy picture.

### Status

Good route to a microscopic Hamiltonian and dynamics.

Less direct as the entropy source.

## Candidate 4: Fracton / Subsystem Gauge Models

### What the literature gives

Fracton and subsystem-symmetry gauge models have constrained Hilbert spaces and
unusual degeneracy. Some models have ground-state degeneracy whose logarithm
scales subextensively, and some subsystem-gauge models have leading degeneracy
that grows like the square of the linear system size.

### Why it helps

This is relevant because black-hole entropy also scales like an area, not a
volume.

In principle:

```text
3D fracton-like system:
  log GSD ~ R^2
```

could provide an area-like physical degeneracy without assigning it by hand.

### What it does not solve

For a 3D droplet, ordinary interface energy would scale as:

```text
M ~ surface area ~ R^2,
```

not:

```text
M ~ R.
```

So fracton degeneracy helps the entropy side but not the mass/energy side.

Also, many fracton degeneracies are boundary-condition-sensitive or not fully
topologically protected in the same way as ordinary topological order.

### Status

Interesting backup route.

Not the cleanest match to the edge-tension droplet.

## Candidate 5: Subsystem Codes / Gauge Codes

Subsystem codes can have many gauge degrees of freedom and constrained
Hilbert spaces.

They are useful for:

```text
hard/soft information bookkeeping;
explicit unitary circuits;
Page diagnostics;
erasure/erosion channels.
```

But they are dangerous as entropy sources:

```text
gauge qubits may be redundancy, not physical entropy.
```

### Status

Good technology for the information-flow channel.

Weak as the primary thermodynamic model unless the extensive sector is
physical.

## Comparative Table

```text
Model family          area entropy  soft bulk  quantum H  edge/interface  main issue
------------------------------------------------------------------------------------
ice / spin ice        Y             Y          P          P/Y             classical / degeneracy lifting
finite gauge droplet  Y             Y          Y          Y               too soft; fluxes must stay degenerate
quantum dimer / RK    P             Y          Y          P               ground state often unique
fracton/subsystem     P/Y           Y          Y          P               energy scaling mismatch
subsystem codes       P             Y          Y          P               gauge vs physical entropy
```

Legend:

```text
Y = strong match
P = partial / construction-dependent
```

## What This Means For Non-Naturalness

The main non-naturalness has shifted.

Earlier weak point:

```text
M ~ sqrt(S) was imposed.
```

Now:

```text
S ~ R^2 and M ~ R follow from area residual entropy plus boundary tension.
```

Remaining weak point:

```text
Why is the constrained bulk so soft?
```

The literature says this is not absurd. Extensive residual entropy occurs in
ice-rule and frustrated systems, and constrained gauge Hilbert spaces are
standard.

But it also says this is not generic stable topological order. It is closer to:

```text
frustrated residual entropy;
zero-coupling gauge sectors;
flat-band constrained manifolds;
RK-like fine-tuned points;
subsystem constrained phases.
```

## Best Next Model

The next version should probably be phrased as:

```text
an ice-rule / finite-gauge constrained droplet with boundary tension.
```

Not:

```text
a topological ground-state droplet.
```

The reason:

```text
topological ground-state degeneracy is usually too small on a disk;
residual constrained entropy is the actual source of S ~ R^2.
```

## Immediate Technical Next Step

Define a shell-eroding channel for the finite-gauge or ice-rule droplet:

```text
H_L -> H_(L-1) tensor H_shell(L),
dim H_shell(L) = q^(2L - 1)
```

Then split:

```text
H_shell(L) -> hard energy bin tensor soft record.
```

The key diagnostic:

```text
hard radiation alone thermal-ish;
hard + soft record unitary;
Page turnover from shrinking H_L versus growing exterior record.
```

This is now the real missing piece.

## Sources

Relevant sources checked:

```text
Ferreyra and Grigera,
"Boundary conditions and the residual entropy of ice systems",
Phys. Rev. E 98, 042146 (2018).

Lieb,
"Residual entropy of square ice",
Phys. Rev. 162, 162 (1967).

Castelnovo, Moessner, and Sondhi,
"Spin Ice, Fractionalization and Topological Order",
Annual Review of Condensed Matter Physics 3, 35-55 (2012);
arXiv:1112.3793.

Donnelly,
"Decomposition of entanglement entropy in lattice gauge theory",
Phys. Rev. D85, 085004 (2012);
arXiv:1109.0036.

Andrews, De Sterck, Inglis, and Melko,
"Monte Carlo study of degenerate groundstates and residual entropy in a
frustrated honeycomb lattice Ising model",
arXiv:0812.3330.

Vijay, Haah, and Fu,
"Fracton Topological Order, Generalized Lattice Gauge Theory and Duality",
arXiv:1603.04442.

Williamson, Bi, and Cheng,
"Fracton-like phases from subsystem symmetries",
arXiv:1908.07601.
```

