# Option C: Microscopic Hamiltonian Routes

## Purpose

Review whether we should push beyond the current edge-tension gauge droplet
and look for a more natural microscopic Hamiltonian.

Option C means:

```text
replace the constructed soft residual-entropy sector and erosion channel with
something closer to a standard local many-body model.
```

The target ingredients are:

```text
1. extensive constrained/residual entropy: S ~ area;
2. energy dominated by an interface or boundary: M ~ perimeter;
3. local boundary erosion dynamics;
4. hard radiation channel with energy scale T ~ 1/R;
5. soft record / edge data for purification.
```

## Short Verdict

There is no single obvious Hamiltonian that gives all five ingredients.

The best candidates split by purpose:

```text
ice / six-vertex / frustrated models:
  best for natural residual entropy;

finite-group gauge theory:
  best for exact Hilbert-space counting and edge records;

quantum dimer / RK models:
  best for local constrained dynamics;

quantum spin ice:
  best physical bridge between ice entropy and emergent gauge theory;

fracton / subsystem models:
  interesting but not a clean match for M ~ R.
```

So Option C is not one road. It is a fork.

## Candidate 1: Classical Ice / Six-Vertex Droplet

### What it gives

Ice-rule models impose local constraints, e.g.

```text
two-in / two-out.
```

The allowed configurations grow exponentially with area in 2D. For square ice:

```text
N_states ~ c^(L^2),
c = (4/3)^(3/2).
```

This gives:

```text
S ~ L^2.
```

If the ice-rule phase is embedded in a polarized/trivial phase, the interface
can have line tension:

```text
M ~ L.
```

Then the thermodynamic package follows.

### Why it is attractive

This is the most natural entropy story:

```text
the entropy is ordinary residual entropy of a constrained manifold.
```

No gauge-theory abstraction is needed.

### Weakness

It is too classical unless quantized.

Also, residual entropy is vulnerable to perturbations that lift degeneracy or
select order.

### Best use

Use it as the physical intuition:

```text
black-hole-like thermodynamics from an ice-rule residual-entropy droplet.
```

Not yet the best quantum information model.

## Candidate 2: Finite-Group Gauge Hamiltonian

### What it gives

Kogut-Susskind lattice gauge Hamiltonians provide:

```text
link Hilbert spaces;
Gauss constraints;
electric and magnetic terms;
boundary edge modes under factorization.
```

For finite group `Z_q`, the link Hilbert space is finite, and imposing Gauss
law on a planar patch gives:

```text
dim H_phys = q^(E - V + 1) = q^(plaquettes).
```

### Why it is attractive

This is our cleanest exact counting model.

It also naturally supports:

```text
edge flux records;
moving-boundary shell data;
hard/soft split language.
```

### Weakness

A generic gauge Hamiltonian includes plaquette/magnetic terms. Those lift the
plaquette flux degeneracy.

If we project to the usual topological ground-state sector on a disk:

```text
area entropy disappears.
```

So the model needs a special regime:

```text
Gauss law enforced strongly;
plaquette fluxes soft or weakly split.
```

### Best use

Keep this as the main analytic core unless we find a better one.

It is the best compromise between:

```text
quantum Hilbert space;
exact counting;
edge records;
computability.
```

## Candidate 3: Quantum Dimer / Rokhsar-Kivelson Droplet

### What it gives

Quantum dimer models have local constrained Hilbert spaces:

```text
one dimer touches each site.
```

They also have local dynamics:

```text
plaquette flips / ring exchanges.
```

At RK points, one often gets exact equal-amplitude ground states over many
classical configurations.

### Why it is attractive

This is the best path toward a local erosion channel.

Boundary erosion could be built from:

```text
local plaquette flips near the boundary;
monomer/dimer defects;
edge rearrangements.
```

### Weakness

The RK ground state is commonly unique within a sector. The large constrained
configuration space appears as a basis, not necessarily as thermodynamic
degeneracy.

So it may improve dynamics while weakening the entropy source.

### Best use

Use dimer/RK models if Option B stalls and we need a more local boundary
dynamics model.

## Candidate 4: Quantum Spin Ice

### What it gives

Quantum spin ice starts from the classical ice manifold and adds quantum
dynamics, often described by ring-exchange terms within the constrained
manifold.

It naturally connects:

```text
residual entropy;
emergent gauge theory;
monopole-like defects;
quantum dynamics.
```

### Why it is attractive

It is the best physical bridge between:

```text
ice-rule entropy
```

and:

```text
gauge-theory language.
```

### Weakness

Most spin-ice literature is 3D. A 3D droplet has:

```text
entropy ~ volume ~ R^3
interface energy ~ area ~ R^2,
```

which does not directly give Schwarzschild-like:

```text
S ~ R^2, M ~ R.
```

There are 2D artificial spin-ice / six-vertex analogues, but then the quantum
coherent Hamiltonian story is less mature.

### Best use

Use as physical support for constrained residual entropy and emergent gauge
language, not as the immediate model.

## Candidate 5: Fracton / Subsystem Gauge Models

### What it gives

Some fracton/subsystem models have degeneracy scaling with non-volume powers
of system size.

That sounds attractive because black holes have area entropy.

### Weakness

For a 3D subsystem/fracton droplet:

```text
interface energy ~ R^2
```

not:

```text
M ~ R.
```

Also, the degeneracy often depends sensitively on boundary conditions and
subsystem symmetries.

### Best use

Keep as a backup idea if we abandon the 2D droplet picture.

Not the next practical route.

## Candidate 6: Subsystem Codes / Gauge Codes

### What it gives

Subsystem/gauge codes are good for:

```text
explicit Hilbert-space constraints;
edge records;
erasure channels;
hard/soft information diagnostics.
```

### Weakness

Gauge qubits may be redundancy rather than physical entropy.

If the entropy source is not physical, it does not solve our main problem.

### Best use

Use for channel design and diagnostics, not as the thermodynamic core.

## Ranking By Goal

### Best entropy source

```text
1. ice / six-vertex residual entropy
2. finite-group gauge droplet
3. quantum spin ice
4. dimer/RK constrained basis
5. fracton/subsystem
```

### Best exact quantum counting

```text
1. finite-group gauge droplet
2. subsystem/gauge code
3. dimer/RK model
4. string-net/fusion variant
5. ice model
```

### Best local dynamics

```text
1. quantum dimer/RK model
2. quantum spin ice
3. finite-group gauge Hamiltonian with weak plaquette terms
4. subsystem code circuit
5. classical ice
```

### Best fit to our current result

```text
1. finite-group gauge droplet
2. ice/six-vertex droplet
3. quantum dimer/RK erosion model
```

## Recommendation

Do not switch wholesale to Option C yet.

The current finite-gauge droplet is still the best core because it has exact
counting and already produced the thermodynamic scalings.

But we should use Option C to guide the next refinement:

```text
1. Keep finite-group gauge counting as the core.
2. Borrow local plaquette/ring-exchange moves from gauge/dimer/RK models.
3. Treat ice/six-vertex residual entropy as the physical interpretation.
4. Try to replace random U_h in the Level 2 erosion channel with structured
   boundary-local moves.
```

In other words:

```text
Option B now, informed by Option C.
```

The next concrete target should be:

```text
a structured boundary erosion channel built from plaquette-flux operations,
compared against the random Level 2 channel.
```

## Sources Checked

Relevant sources:

```text
Lieb,
"Residual entropy of square ice",
Phys. Rev. 162, 162 (1967).

Castelnovo, Moessner, and Sondhi,
"Spin Ice, Fractionalization, and Topological Order",
Annual Review of Condensed Matter Physics 3, 35-55 (2012);
arXiv:1112.3793.

Kogut and Susskind,
"Hamiltonian formulation of Wilson's lattice gauge theories",
Phys. Rev. D 11, 395 (1975).

Donnelly,
"Decomposition of entanglement entropy in lattice gauge theory",
arXiv:1109.0036.

Rokhsar and Kivelson quantum dimer model literature.

Vijay, Haah, and Fu,
"Fracton Topological Order, Generalized Lattice Gauge Theory and Duality",
arXiv:1603.04442.
```

