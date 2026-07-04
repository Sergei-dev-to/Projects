# Soft Relation Entropy and Radiation Access

## Target

The boundary we want to probe is:

```text
soft relation entropy + direct radiation access.
```

State count alone and access alone leave too much freedom. The black-hole-like
combination is:

```text
many physical relation/edge states;
small energy per entropy-carrying degree;
coupling of those degrees, or their collective boundary variables, to the
outgoing radiation channel;
unitary export of the information when the object shrinks.
```

This note records what the literature already suggests and what our own model
probes have found.

## Known Mechanisms Near the Boundary

### 1. Long strings

The long-string route is very close to the pressure point. It says that
short-distance horizon degrees have too much energy, and that a long string
lowers the excitation energy per degree of freedom.

Useful anchors:

```text
Verlinde, Visser,
"Black hole entropy and long strings",
https://arxiv.org/abs/2206.03161.

Halyo,
"Universal Counting of Black Hole Entropy by Strings on the Stretched Horizon",
https://arxiv.org/abs/hep-th/0108167.

Mertens, Verschelde, Zakharov,
"The long string at the stretched horizon and the entropy of large
non-extremal black holes",
https://arxiv.org/abs/1505.04025.
```

Demarcation reading:

```text
softness is achieved by reorganizing many short degrees into a long collective
object.
```

This is a direct known answer to "how can many entropy degrees have low energy
per degree?" It is stringy/horizon-adjacent rather than a generic
non-gravitational control.

### 2. Edge modes and soft hair

Gauge and gravitational edge modes give physical boundary labels after
constraints. Soft hair connects horizon labels to radiation and memory.

Useful anchors:

```text
Donnelly, Wall,
"Entanglement entropy of electromagnetic edge modes",
https://arxiv.org/abs/1412.1895.

Ball, Law, Wong,
"Dynamical Edge Modes and Entanglement in Maxwell Theory",
https://arxiv.org/abs/2403.14542.

Hawking, Perry, Strominger,
"Soft Hair on Black Holes",
https://arxiv.org/abs/1601.00921.

Chu, Koyama,
"Soft Hair of Dynamical Black Hole and Hawking Radiation",
https://arxiv.org/abs/1801.03658.

Di Filippo, Ogawa, Mukohyama, Waki,
"Soft hair, dressed coordinates and information loss paradox",
https://arxiv.org/abs/2305.15800.
```

Demarcation reading:

```text
edge/soft labels address physicality and softness, and they sit at the
radiation interface.
```

The unresolved issue is completeness: edge or soft labels by themselves do not
automatically give the full finite thermodynamic state count, scrambling, and
unitary export package.

### 3. Matrix/off-diagonal clumps

Matrix models give the mature relation-entropy mechanism.

```text
diagonal/block variables       object-like sector
off-diagonal matrix entries    relation sector
block separation               relation removal / evaporation
```

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
```

Demarcation reading:

```text
matrix dynamics already combines relation entropy, soft collective behavior,
and an evaporation-like split.
```

The control question is whether the mechanism survives after removing the
holographic/D-brane interpretation.

### 4. Quantum Hall / Chern-Simons / fuzzy-sphere hybrids

Our notes identify this as the most plausible non-gravitational soft-label
source:

```text
fuzzy sphere             finite angular Mat_R algebra;
Landau-level projection  softness / flat-band kinematics;
Chern-Simons constraints edge Hilbert spaces;
quantum Hall droplet     boundary shrinkage intuition.
```

Supporting note:

```text
notes/automatic_edge_label_model_search.md
```

Demarcation reading:

```text
this route tries to get physical soft boundary labels without immediately
using gravity.
```

The missing piece is the black-hole thermodynamic package: `S ~ M^2`,
negative heat capacity, and unitary shrinking/export.

## Our Local Probes

### A. Angular soft shell

Supporting notes:

```text
notes/angular_soft_mode_branch.md
notes/angular_shell_evaporator_path.md
```

Construction:

```text
soft labels:  Y_lm, l <= L
count:        sum_{l=0}^L (2l+1) = (L+1)^2
mass scale:   M ~ L
entropy:      S ~ L^2 ~ M^2
evaporation:  L -> L-1 removes shell l=L with 2L+1 labels
```

What it gives:

```text
clean area count;
natural entropy loss per coarse shrink;
hard quantum plus soft angular memory split.
```

What it assumes:

```text
the angular labels are soft edge/constraint labels, not ordinary spherical
harmonic excitations.
```

Boundary lesson:

```text
angular boundary labels are a clean basis for relation entropy, but softness is
the real input.
```

### B. Boundary soft modes

Supporting note:

```text
notes/boundary_soft_mode_assessment.md
```

Construction:

```text
bulk constrained register supplies S ~ L^2;
boundary tension supplies M ~ L;
boundary soft modes have omega_n ~ n/L;
exterior bath drains energy through the boundary modes.
```

Result:

```text
thermally active boundary quanta have omega ~ T ~ 1/L;
with a 2D bath, the golden-rule power scales as P ~ M^-2.
```

What it gives:

```text
microscopic Hawking-scale quanta;
boundary-local emission;
mass changes gradually rather than by literal shell deletion.
```

What remains:

```text
bulk-to-boundary information flow;
Page-like radiation diagnostics;
one Hamiltonian coupling bulk constrained states, boundary soft modes, and bath.
```

Boundary lesson:

```text
small-energy emission is easier if the entropy register, mass register, and
emission oscillator are distinct but coupled.
```

### C. Critical connector spectra

Supporting notes:

```text
notes/collective_connector_softness_results.md
notes/critical_connector_heating_results.md
```

Result:

```text
complete-graph incidence spectra are too hard;
critical collective connector spectra can have omega ~ T ~ 1/N;
some spectra give a local power proxy near P ~ N^-2;
heating passes only for special low-energy spectral structures.
```

What it gives:

```text
a possible non-geometric route to soft relation degrees.
```

What it assumes:

```text
the relation sector is naturally critical or gapless.
```

Boundary lesson:

```text
softness can be spectral rather than topological, but then criticality becomes
the supplied structure.
```

### D. Stripped matrix clump

Supporting note:

```text
notes/stripped_matrix_clump_program.md
```

Construction:

```text
bosonic matrix quantum mechanics;
eigenvalue clump as emergent object;
off-diagonal modes as relations;
emission as eigenvalue separation;
remaining clump temperature measured dynamically.
```

What it tests:

```text
whether the relation-entropy evaporation mechanism survives without invoking
the full black-zero-brane/holographic interpretation.
```

Boundary lesson:

```text
if stripped matrix dynamics fails to bind and evaporate, the successful
mechanism may depend on the full gravitational/holographic matrix structure.
```

## Emerging Boundary

The search suggests a sharper boundary than "QM versus gravity":

```text
ordinary local QM:
  state count, energy, and access are usually carried by the same local
  degrees.

black-hole-like systems:
  state count, energy, and access can be carried by different sectors, with
  dynamics tying them into one evaporating object.
```

In the model language:

```text
state count:      bulk/relations/edge labels
energy:           object size, boundary tension, or collective coordinate
emission access:  boundary soft modes or off-diagonal connectors
export:           radiation plus soft memory/archive
```

This sector split is the object to study. It is also where the known successful
routes cluster:

```text
long strings;
edge modes / soft hair;
matrix off-diagonal dynamics;
holographic boundary descriptions.
```

## Most Promising Next Probe

### Literature guard result

This direction is not empty territory. There are explicit soft-hair
information-flow models, including Page-curve constructions.

Useful anchors:

```text
Cheng, An,
"Soft black hole information paradox: Page curve from Maxwell soft hair of a
black hole",
https://arxiv.org/abs/2012.14864.

Hotta, Nambu, Yamaguchi,
"Soft-Hair-Enhanced Entanglement Beyond Page Curves in a Black-hole
Evaporation Qubit Model",
https://arxiv.org/abs/1706.07520.

Chiang, Kung, Chen,
"Modification to the Hawking temperature of a dynamical black hole by a
flow-induced supertranslation",
https://arxiv.org/abs/2004.05045.

Cheng,
"Evaporating black holes and late-stage loss of soft hair",
https://arxiv.org/abs/2108.10177.
```

What this changes:

```text
the open question is not "can soft hair be used in Page-curve stories?";
that has been explored.

the useful control question is whether soft boundary modes that fix the
frequency/rate problem also transmit generic bulk entropy information, or
whether an additional scrambling/bulk-boundary coupling is required.
```

The most targeted next local probe is the boundary-soft-mode information-flow
test:

```text
bulk constrained register -> boundary soft mode -> exterior bath quantum.
```

Vary three regimes:

```text
1. no bulk-boundary scrambling;
2. local boundary coupling only;
3. scrambled bulk-to-boundary coupling.
```

Measure:

```text
hard-radiation thermality;
hard-only early/late mutual information;
hard+soft purification;
coarse Page-like behavior;
latency from deposited bulk information to exterior recovery.
```

Pass/fail reading:

```text
If regime 3 gives hard-radiation thermality, full hard+soft purification, and
a Page-like transfer while regimes 1-2 fail recovery, then the probe separates
energy-scale access from information access.

If all regimes fail, boundary soft modes only solve the frequency/rate problem.

If regimes 1-2 already succeed, the model is leaking information through the
chosen coupling rather than testing scrambling-mediated access.
```

Why this is the right next poke:

```text
the power law already works in the boundary-soft-mode model;
the missing boundary question is whether entropy information reaches the
emission channel.
```

This directly tests the overlap of state count and emission access.

## Second Probe

### Literature guard result

The stripped matrix-clump direction is also close to known work. Matrix
black-hole evaporation already uses eigenvalue escape, off-diagonal mode
decoupling, flat directions, negative specific heat, and classical/semi-classical
diagnostics.

Useful anchors:

```text
Berkowitz, Hanada, Maltz,
"Chaos in Matrix Models and Black Hole Evaporation",
https://arxiv.org/abs/1602.01473.

Berenstein, Guan,
"Improved semiclassical model for real time evaporation of Matrix black holes",
https://arxiv.org/abs/2105.04577.
```

What this changes:

```text
the stripped matrix probe should not be framed as a new evaporation mechanism;
it is a control test for which pieces of the known matrix mechanism survive
when the holographic/D-brane interpretation is stripped away.
```

The second probe is stripped matrix clump dynamics:

```text
does eigenvalue escape heat the remaining clump?
```

This is higher risk but higher value. A success would give a dynamical
relation-entropy mechanism. A failure would identify which ingredients of the
mature matrix mechanism were doing the binding and evaporation work.
