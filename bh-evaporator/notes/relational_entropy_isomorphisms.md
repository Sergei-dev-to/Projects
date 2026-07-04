# Relational Entropy: Isomorphic Routes to S ~ E^2

## Purpose

This note collects systems where the same structural pattern appears in
different language:

```text
energy counts objects;
entropy counts relations.
```

If there are `N` object-like degrees of freedom and `O(N^2)` relation-like
degrees of freedom, then a system with

```text
E ~ N,
S ~ N^2
```

has

```text
S ~ E^2,
T^{-1} = dS/dE ~ E,
C < 0.
```

That is the Schwarzschild thermodynamic scaling. The question is whether this
can be made into a genuine non-gravitational quantum model with physical
states, a Hamiltonian, and a unitary evaporation map.

This is the same branch as:

```text
notes/relational_evaporator_principle.md
notes/relational_objects_literature_map.md
notes/soft_vs_energetic_relations.md
notes/not_giving_up_escape_routes.md
```

The present note is the index and filter.

## Working Verdict

Known results already cover most ingredients:

```text
O(N^2) relation-like thermodynamics in large-N gauge/matrix systems;
long-range/nonadditive energy accounting and Kac scaling;
negative heat capacity from convex microcanonical entropy;
physical gauge-edge sectors;
exponential fusion-space degeneracy;
black-hole puncture counting in gravitational approaches.
```

The useful demarcation is the combined requirement:

```text
S(E) ~ E^2 requires relation-sized state counting with object-sized energy.
Known physics gets this through large-N normalization, soft constrained
sectors, or holography. Ordinary energetic relations fail the energy test.
```

The combined non-gravitational control object has not shown up in the first
literature pass:

```text
a finite Hamiltonian system whose physical soft relation sector gives
S(E) ~ E^2, whose energy grows like object count, and whose unitary shrinking
map exports the lost relation information as radiation.
```

That is the live target.

## The Basic Pattern

A relation-based model has three layers.

```text
objects:
  visible constituents, labels, sites, matrix eigenvalues, defects, punctures

relations:
  pairwise connectors, off-diagonal modes, graph edges, fusion channels,
  gauge-edge sectors, boundary constraints, entanglement bonds

energy:
  controlled mainly by object count, collective size, or a small hard sector
```

The attractive scaling is immediate for pairwise relations:

```text
number of objects       ~ N
number of pair relations ~ N(N-1)/2
energy                  ~ N
entropy                 ~ N^2
```

The hard part is physical legitimacy. Relation labels must be actual physical
states after constraints, and they must carry entropy without carrying
proportional energy.

## Why This Matters for the Demarcation Program

The original Hamiltonian paper treats the Schwarzschild density of states as an
input:

```text
S(E) ~ E^2.
```

The relational route is a candidate microscopic explanation of that input. It
would say that the state count is superextensive in energy because the energy
scale counts object-like degrees while the entropy counts relation-like
degrees.

If the same relation sector also couples efficiently to radiation, it may also
help explain the boundary-accessibility input. That second step is stronger
and remains open.

## Isomorphic Examples

### Pairwise Relation Qudits

The clean finite toy model:

```text
N objects;
one relation qudit on each unordered pair;
dim H_rel ~ d^(N choose 2).
```

This realizes `S ~ N^2` immediately. It becomes a Schwarzschild-like state
count if the energy is tied to the objects rather than to the connectors.

The control failure is also immediate. If each connector is an ordinary
energetic qudit with an `O(1)` gap, an evaporating object releases `O(N)`
connector energy. The remaining system does not heat in the required way.

This toy is useful because it isolates the needed fix:

```text
relations must be soft, constrained, topological, or correlation-like.
```

### Matrix and D0-Brane Models

Matrix models provide the closest mature version of the relation idea.

```text
objects       = diagonal blocks / D0-branes
relations     = off-diagonal matrix elements / open strings
entropy       = active matrix degrees, often O(N^2)
evaporation   = block separation, U(N) -> U(N-1) x U(1)
```

This is a real mechanism. When one object separates, many
off-diagonal relation modes decouple.

Literature anchors:

```text
Berkowitz, Hanada, Maltz,
"Chaos in Matrix Models and Black Hole Evaporation",
https://arxiv.org/abs/1602.01473.

Berkowitz, Hanada, Maltz,
"A microscopic description of black hole evaporation via holography",
https://arxiv.org/abs/1603.03055.

Klebanov, Susskind,
"Schwarzschild Black Holes in Various Dimensions from Matrix Theory",
https://arxiv.org/abs/hep-th/9709108.
```

This route is already black-hole/holography-adjacent. It may be close to the
correct physics, while giving less leverage as a demarcating control.

### Large-N Gauge Plasma

Adjoint matrix fields give physical `O(N^2)` thermodynamics in deconfined
sectors.

```text
objects   = color indices
relations = adjoint degrees connecting color indices
entropy   = O(N^2)
```

This is a standard realization of relational entropy. Its missing piece for our
purpose is an evaporation operation that changes the effective rank or active
object count:

```text
N -> N - 1.
```

Large-N gauge theory is therefore a strong reference point, but not by itself a
finite evaporator.

### Quantum Graphity and Dynamical Graphs

Quantum graphity makes relations explicit.

```text
objects   = vertices
relations = quantum edges
geometry  = low-energy pattern of active edges
```

Literature anchors:

```text
Konopka, Markopoulou, Smolin,
"Quantum Graphity: a model of emergent locality",
https://arxiv.org/abs/0801.0861.

Hamma, Markopoulou, Premont-Schwarz, Severini,
"A quantum Bose-Hubbard model with evolving graph as toy model for emergent
spacetime",
https://arxiv.org/abs/0911.5075.
```

This is conceptually close to the desired architecture because the edge Hilbert
space is microscopic. The target in that literature is emergent locality and
geometry; the extra target here is a shrinking thermal object with
Schwarzschild state count, radiation, and negative heat capacity.

### Gauge Edge Modes and Boundary Sectors

Gauge theories show how entropy can live in boundary-compatible relation data
rather than ordinary local particles.

```text
objects   = regions or bulk systems
relations = gluing data across a boundary
entropy   = edge-sector entropy
```

Literature anchors:

```text
Donnelly,
"Decomposition of entanglement entropy in lattice gauge theory",
https://arxiv.org/abs/1109.0036.

Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
https://arxiv.org/abs/1412.1895.

Donnelly, Wall,
"Geometric entropy and edge modes of the electromagnetic field",
https://arxiv.org/abs/1506.05792.
```

This is one of the most relevant precedents because the entropy is physical
after constraints. It supplies a mechanism for soft relation labels; additional
structure is needed to obtain `S ~ E^2`.

### Non-Abelian Fusion Spaces and Topological Defects

Non-Abelian anyons give a physical Hilbert space whose dimension grows
exponentially with the number of defects:

```text
dim H_n ~ d^n.
```

If a droplet of size `R` carries `n_R ~ R^2` soft punctures or defects, then

```text
S_R ~ R^2.
```

The important distinction is between fusion-space entropy and anyon-gas
entropy. If the `R^2` labels are energetic quasiparticles, the energy also
scales as `R^2`. The useful version needs boundary punctures, defects, holes,
or constrained sectors whose fusion labels are nearly degenerate.

Literature anchor:

```text
Nayak, Simon, Stern, Freedman, Das Sarma,
"Non-Abelian Anyons and Topological Quantum Computation",
Rev. Mod. Phys. 80, 1083 (2008),
https://arxiv.org/abs/0707.1889.
```

This may be the cleanest non-gravitational route if the energetic-defect
problem has a natural solution.

### String-Net and Quantum Double Patches

Exactly solvable topological lattice Hamiltonians provide a microscopic source
of fusion rules and constrained edge sectors.

The useful version would use many punctures, defects, or boundary labels. A
plain topological phase on a simply connected disk has only `O(1)` topological
ground-state degeneracy.

The test is:

```text
Can a local Hamiltonian produce O(R^2) physical soft labels in a region of
linear size R without paying O(R^2) energy?
```

### Tensor Networks and Code Subspaces

Tensor networks store entropy in bonds and constraints:

```text
objects   = tensors
relations = bonds
entropy   = cut or internal bond dimensions
```

This is a useful language for relation counting, especially near holographic
codes and complementary recovery. To become an evaporator it needs a
Hamiltonian, an energy assignment, and an emission map.

### Long Strings, Random Walks, and Branched Polymers

Long strings and random walks show a different but related isomorphism.

```text
entropy ~ length,
size^2  ~ length.
```

So if the observable energy tracks size rather than length, an `S ~ E^2`
relation can appear. The string/black-hole correspondence lives nearby, though
string entropy itself is usually Hagedorn rather than super-Hagedorn in energy.

The lesson is structural:

```text
a large state count can be attached to hidden extension, relation, or path
data while the macroscopic scale grows more slowly.
```

### Spin Glasses and Constraint Satisfaction

Spin glasses and constraint systems have many states organized by relational
constraints. They are useful as analogues for entropy from compatibility data.

The obstacle is the same as for pairwise relation qudits: unless the relation
sector is soft or constrained in a special way, energy and entropy tend to grow
together.

## Viability Filters

A candidate route has to pass these checks.

### 1. Physical State Count

The `N^2` labels must survive constraints as physical states. Raw labels are
not enough.

Failure mode:

```text
matrix or graph variables appear to give N^2 labels, but constraints quotient
most of them away.
```

### 2. Softness

The relation sector must carry entropy without proportional energy.

Viable mechanisms:

```text
near degeneracy;
topological fusion labels;
gauge edge sectors;
constraint sectors;
N-dependent gaps Delta_N ~ 1/N;
correlation patterns rather than local excitations.
```

Failed control:

```text
ordinary O(1)-gap connector qudits.
```

### 3. Shrinking Map

There must be a natural operation analogous to evaporation:

```text
N -> N - 1
```

or

```text
R -> R - 1.
```

The operation should remove `O(N)` relation states while carrying only the
energy expected of the emitted quantum.

### 4. Radiation Accounting

The lost relation information must be purified somewhere:

```text
radiation records;
soft memory;
emitted object plus relation cloud;
archive/environment counted as radiation.
```

If the relation sector simply disappears, the model is not unitary.

### 5. Emission Rate

The state count alone gives

```text
T ~ 1/N.
```

It does not give the Schwarzschild power law. The model still needs a coupling
or channel-count statement that yields

```text
P ~ 1/N^2
```

in four-dimensional Schwarzschild units.

## Literature Guard: What Is Already Proven

The useful lesson from the first literature pass is that most individual
ingredients already have homes. The likely open target is the combined package.

### 1. Relation counting itself is standard

The bare statement

```text
N objects with pairwise relation labels -> O(N^2) relation labels
```

is elementary. It should not be presented as a result.

Large-N gauge theory and matrix models already use this structure physically:
adjoint/off-diagonal degrees carry `O(N^2)` thermodynamics. Matrix black-hole
models also contain the evaporation-like operation in which a block separates
and many off-diagonal connector modes decouple.

Reference points:

```text
large-N deconfined gauge theory:
  physical O(N^2) thermodynamics from adjoint degrees

D0/matrix evaporation:
  off-diagonal modes as connector degrees;
  block separation as relation removal;
  negative heat capacity discussed explicitly
```

The relational route is therefore a translation of a known matrix/gauge
mechanism into demarcation language, unless it produces a cleaner
non-holographic model.

### 2. Negative heat capacity from convex microcanonical entropy is standard

If a microcanonical entropy has positive curvature over an energy window,

```text
d^2 S/dE^2 > 0,
```

then

```text
C = - (dS/dE)^2 / (d^2 S/dE^2) < 0.
```

This is standard in finite systems, first-order phase coexistence, clusters,
and gravitating systems. A relational model with `S ~ E^2` is one instance of
that general fact.

Useful anchor:

```text
Gross,
"Negative heat capacity at phase-separation in macroscopic systems",
https://arxiv.org/abs/cond-mat/0508455.
```

### 3. The energetic-connector failure is model bookkeeping

The statement

```text
emitting one object releases O(N) ordinary connectors;
ordinary connectors with O(1) gaps carry O(N) energy;
this is too much for Schwarzschild-like heating
```

is likely too elementary to have a named theorem. It is an energy accounting
lemma. We can state it as a sanity check, but it should be framed as the
failure of the naive relation-qudit toy, not as a new physics result.

The surrounding literature is substantial, under the language of long-range
and nonadditive systems. Fully connected or slowly decaying pair interactions
generically have energy scaling faster than `N`. The standard way to recover
an extensive thermodynamic limit is a system-size-dependent weakening of the
pair potential, often called the Kac prescription. In our language:

```text
ordinary pair relations:
  O(N^2) active pairs with O(1) strength -> O(N^2) energy

Kac-scaled pair relations:
  O(N^2) active pairs with O(1/N) strength -> O(N) energy
```

That is exactly the energetic pressure point. A Schwarzschild-like relational
model needs the relation sector to be soft, constrained, topological,
correlation-like, or effectively Kac-scaled by dynamics.

Reference points:

```text
Dauxois, Ruffo, Arimondo, Wilkens,
"Dynamics and Thermodynamics of Systems with Long Range Interactions: an
Introduction",
https://arxiv.org/abs/cond-mat/0208455.

Campa, Dauxois, Ruffo,
"Statistical mechanics and dynamics of solvable models with long-range
interactions",
https://arxiv.org/abs/0907.0323.

Mori,
"Phase transitions in systems with non-additive long-range interactions",
https://arxiv.org/abs/1310.3458.

Kastner,
"Long-range systems, (non)extensivity, and the rescaling of energies",
https://arxiv.org/abs/2506.22296.
```

So the elementary no-go should probably be described as an application of
standard nonadditive thermodynamics to relation entropy, rather than as a new
standalone theorem.

### 4. Fusion-space entropy is established

Non-Abelian anyons and defects provide physical Hilbert spaces whose dimension
grows exponentially with the number of quasiparticles or defects. That part is
well known in topological quantum computation.

Reference point:

```text
Nayak, Simon, Stern, Freedman, Das Sarma,
"Non-Abelian Anyons and Topological Quantum Computation",
https://arxiv.org/abs/0707.1889.
```

What is not supplied automatically:

```text
O(R^2) soft defects in a droplet of size R;
energy growing only like R;
a shrinking evaporation map;
radiation carrying the lost fusion information.
```

If the defects are ordinary gapped quasiparticles, `O(R^2)` defects cost
`O(R^2)` energy. The topological route needs soft punctures, boundary labels,
holes, domain walls, or constraint sectors.

### 5. Plain topological order does not give area-sized thermodynamic entropy

Exactly solvable string-net and quantum-double models are important because
they give microscopic Hamiltonians and physical constrained Hilbert spaces.
But a simply connected disk in a topological phase does not have an
area-sized ground-state degeneracy. In Levin-Wen models, the ground-state
degeneracy depends on spatial topology; on a sphere it is nondegenerate.

Reference point:

```text
Hu, Stirling, Wu,
"Ground State Degeneracy in the Levin-Wen Model for Topological Phases",
https://arxiv.org/abs/1105.5771.
```

So the topological route requires many punctures, defects, boundaries, or
labels. A bare topological phase is not enough.

### 6. Gauge-edge entropy is established, but not the finite evaporator

Gauge theories already show that boundary/edge sectors are physical after the
right Hilbert-space extension or algebraic treatment. This is exactly the kind
of "relation after constraints" mechanism we need.

Reference points:

```text
Donnelly,
"Decomposition of entanglement entropy in lattice gauge theory",
https://arxiv.org/abs/1109.0036.

Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
https://arxiv.org/abs/1412.1895.

Ball, Law, Wong,
"Dynamical Edge Modes and Entanglement in Maxwell Theory",
https://arxiv.org/abs/2403.14542.
```

The open combined question is whether such edge sectors can be made into a
finite thermodynamic state count with a Schwarzschild mass law and a unitary
shrinking/emission process.

### 7. Gravitational puncture versions exist

Loop quantum gravity and isolated-horizon calculations already use punctures
or boundary degrees to count black-hole entropy. This is close in spirit to
the soft-relational route, but it is gravitational.

Reference points:

```text
Donnelly,
"Entanglement Entropy in Loop Quantum Gravity",
https://arxiv.org/abs/0802.0880.

Ghosh, Noui, Perez,
"Statistics, holography, and black hole entropy in loop quantum gravity",
https://arxiv.org/abs/1309.4563.
```

These results should be treated as existing gravitational implementations of
the boundary/puncture idea, not as non-gravitational controls.

### Interim Literature Verdict

Already established:

```text
O(N^2) matrix/gauge relation thermodynamics;
block/off-diagonal decoupling in matrix evaporation;
negative heat capacity from convex microcanonical entropy;
physical gauge-edge entropy;
exponential fusion-space degeneracy;
topological degeneracy with punctures/defects/topology;
black-hole puncture counting in gravitational approaches.
```

Still not found as a standard non-gravitational object:

```text
a finite Hamiltonian system whose physical soft relation sector gives
S(E) ~ E^2, whose energy grows like object count, and whose unitary shrinking
map exports the lost relation information as radiation.
```

That combined object is the real target. The individual ingredients should be
cited, not reproven.

## Clean Demarcation Using Existing Results

The literature supports the following demarcation.

```text
ordinary local finite-density matter:
  entropy and energy both scale with the number of active local degrees;
  no natural S(E) ~ E^2 window at Schwarzschild scale.

ordinary pair-relation matter:
  relation count can scale as N^2;
  ordinary O(1)-energy pair relations also tend to give O(N^2) energy.

Kac/mean-field pair systems:
  pair count scales as N^2;
  pair strength is scaled as 1/N to keep energy O(N);
  this realizes the scaling algebraically, with the scaling rule supplied
  externally or by a large-N normalization.

large-N matrix/gauge systems:
  O(N^2) relation-like degrees are physical;
  large-N normalization can make collective dynamics controlled;
  this is the mature route, already close to holography.

gauge-edge/topological/fusion sectors:
  physical relation labels can be soft or protected;
  area-sized entropy needs many boundaries, punctures, defects, or edge labels;
  the remaining work is energy assignment and evaporation/export dynamics.

gravitational/holographic systems:
  the full package is naturally realized;
  this is the phenomenon the demarcation is trying to isolate.
```

In one sentence:

```text
S(E) ~ E^2 requires relation-sized state counting with object-sized energy.
Known physics gets this by large-N normalization, soft constrained sectors, or
holography; ordinary energetic relations do not.
```

## Investigable Question

The live question is:

```text
Can relation entropy remain O(N^2) while relation energy remains O(N),
without simply postulating pair strength 1/N?
```

Known mechanisms that could make this happen:

### 1. Dynamical Kac scaling

The effective relation strength could scale as `1/N` because of collective
normalization, gauge constraints, large-N saddle structure, or criticality.

This is common in large-N and mean-field theory. The question is whether the
scaling is derived from a microscopic Hamiltonian with fixed local rules, or
inserted as the definition of the model family.

### 2. Topological or fusion degeneracy

Relation labels can be nearly degenerate because they are topological sectors
or fusion channels. Energy then need not track the number of relation labels.

The hard check:

```text
Do the O(N^2) labels require O(N^2) energetic defects?
```

If yes, the route reduces to an expensive gas. If no, it may provide the clean
non-gravitational control model.

### 3. Gauge-edge sectors

Gauge constraints can create physical boundary or gluing labels whose entropy
is not ordinary bulk particle entropy.

The hard check:

```text
Can edge-sector entropy be made into a finite thermodynamic state count,
rather than an entanglement contribution associated with a chosen cut?
```

### 4. Matrix/off-diagonal dynamics

Matrix models naturally contain object-like diagonal/block degrees and
relation-like off-diagonal degrees. Block separation removes many relations.

The hard check:

```text
Can one extract the relation-entropy mechanism in a model that is useful as a
control, or is the mechanism inseparable from the holographic black-hole
setting?
```

### 5. Correlation-only relation entropy

The relation information may live in correlations among objects rather than in
independent connector qudits. Then changing one object can affect many
relations without releasing a cloud of energetic pair excitations.

The hard check:

```text
Can this be represented as a physical Hilbert space with a Hamiltonian and
unitary radiation map?
```

## Practical Next Dig

The fastest useful dig is a triage of the three soft relation mechanisms:

```text
fusion/topological defects:
  look for area-many protected labels without area-many quasiparticle energy.

gauge-edge sectors:
  look for finite thermodynamic entropy from physical edge sectors.

matrix/off-diagonal models:
  isolate which scaling facts rely only on relation bookkeeping and which rely
  on holography/gravity.
```

The expected outcome is a demarcation table:

```text
route                         gives S~E^2?  gives soft energy?  gives export?
ordinary pair qudits          yes by count   no                 easy but wrong energy
Kac-scaled pairs              yes            by scaling          model-dependent
topological fusion sectors    maybe          maybe              open
gauge-edge sectors            maybe          plausible           open
matrix/off-diagonal systems   yes            yes in known cases  black-hole adjacent
holography/gravity            yes            yes                 yes
```

## Crowding Assessment by Route

### Matrix/off-diagonal route: heavily explored

This is the most developed direction. The relation picture is almost explicit:

```text
diagonal/block variables       object-like sector
off-diagonal matrix entries    relation/connector sector
block separation               relation removal
```

The literature already studies evaporation, negative heat capacity, thermal
emission, and off-diagonal mode decoupling in matrix black holes.

Useful anchors:

```text
Berkowitz, Hanada, Maltz,
"Chaos in Matrix Models and Black Hole Evaporation",
https://arxiv.org/abs/1602.01473.

Berkowitz, Hanada, Maltz,
"A microscopic description of black hole evaporation via holography",
https://arxiv.org/abs/1603.03055.

Berenstein, Guan,
"Improved semiclassical model for real time evaporation of Matrix black holes",
https://arxiv.org/abs/2105.04577.

Du, Sahakian,
"Emergent geometry from stochastic dynamics, or Hawking evaporation in
M(atrix) theory",
https://arxiv.org/abs/1812.05020.
```

Assessment:

```text
best source of known mechanisms;
poor source of a clean non-gravitational control;
use it as the mature comparison class.
```

### Gauge-edge route: active and close to the desired language

This direction is crowded in the good sense. Edge modes, boundary symplectic
structure, thermal edge partition functions, and horizon-localized degrees of
freedom are active topics.

Useful anchors:

```text
Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
https://arxiv.org/abs/1412.1895.

Geiller, Jai-akson,
"Extended actions, dynamics of edge modes, and entanglement entropy",
https://arxiv.org/abs/1912.06025.

Ball, Law, Wong,
"Dynamical Edge Modes and Entanglement in Maxwell Theory",
https://arxiv.org/abs/2403.14542.

Dabholkar, Harris, Moitra,
"Edge Modes on Stringy Horizons",
https://arxiv.org/abs/2601.13131.

Klinger, Kudler-Flam, Satishchandran,
"Generalized Entropy is von Neumann Entropy II: The complete symmetry group
and edge modes",
https://arxiv.org/abs/2601.07910.
```

Assessment:

```text
strongest language for physical soft relation labels;
already gravitational/horizon-adjacent;
open control question is finite thermodynamic state count plus evaporation
map outside the gravitational setting.
```

### Fusion/topological-defect route: explored, but the control model is less visible

Fusion-space entropy is standard. Black-hole entropy from Chern-Simons
punctures is also a developed gravitational route. There are also recent
anyon-shell or anyon-condensate black-hole proposals.

Useful anchors:

```text
Nayak, Simon, Stern, Freedman, Das Sarma,
"Non-Abelian Anyons and Topological Quantum Computation",
https://arxiv.org/abs/0707.1889.

Engle, Noui, Perez,
"Black hole entropy and SU(2) Chern-Simons theory",
https://arxiv.org/abs/0905.3168.

Roman,
"Black Holes as Non-Abelian Anyon Condensates",
https://arxiv.org/abs/2507.23457.
```

Assessment:

```text
fusion degeneracy is established;
gravitational puncture counting is established;
the clean non-gravitational finite evaporator is still not obvious.
```

The key pressure point remains:

```text
Can one get area-many protected/fusion labels without paying area-many
quasiparticle energy?
```

### Quantum graphity/dynamical graph route: explored for emergent locality

Quantum graphity and related dynamical graph models explicitly use vertex and
edge Hilbert spaces. This is structurally close to relation entropy.

Useful anchor:

```text
Konopka, Markopoulou, Severini,
"Quantum Graphity: a model of emergent locality",
https://arxiv.org/abs/0801.0861.
```

Assessment:

```text
good source of relation-Hilbert-space architecture;
main target is emergent locality/geometry, not Schwarzschild evaporation;
worth consulting for model-building, less likely to already contain the full
thermodynamic package.
```

### Overall

The promising directions have been explored substantially, but in different
communities and with different goals.

```text
matrix route:
  full black-hole-like dynamics, already holographic.

edge route:
  physical soft boundary labels, currently active, horizon-adjacent.

fusion route:
  physical protected Hilbert spaces, gravitational puncture versions mature,
  non-gravitational evaporator less visible.

graph route:
  relation Hilbert spaces and emergent locality, weaker thermodynamic target.
```

The least crowded useful target is therefore not "relation entropy" in general.
It is:

```text
a non-gravitational finite control model where soft/topological relation
entropy supplies S(E) ~ E^2 and a unitary shrinking map exports the relation
information.
```

Concrete checks:

1. Search the combined target directly.

```text
"finite Hamiltonian" + relation entropy + negative heat capacity;
topological defects + evaporation + negative heat capacity;
gauge edge modes + finite reservoir + unitary evaporation;
matrix evaporation + non-holographic control.
```

2. Keep the minimal pairwise-relation lemma as an orientation check.

```text
If E_N ~ N and log dim H_rel(N) ~ N^2, then S(E) ~ E^2 and C < 0.
If relation qudits have O(1) energy density, heating fails.
```

This separates the good counting from the bad energetics.

3. Work out the topological-defect route.

```text
Can a known non-Abelian fusion-space model provide O(R^2) soft physical labels
without O(R^2) quasiparticle energy?
```

4. Work out the gauge-edge route.

```text
Can edge-sector entropy be made thermodynamic and finite, rather than only an
entanglement contribution across a chosen cut?
```

5. Compare against matrix evaporation.

```text
Which part of the D0/matrix evaporation mechanism is purely relational, and
which part is already gravitational/holographic?
```

6. Decide whether this supplies a microscopic origin for input 1 only, or for
inputs 1 and 2 together.

```text
state count:       S(E) ~ E^2
emission access:   O(S) entropy degrees participate in radiation coupling
```

The second point is the harder one. Relation entropy that cannot couple to
radiation is not enough for the operational horizon package.
