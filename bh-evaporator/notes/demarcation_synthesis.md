# Quantum/Gravity Demarcation Synthesis

## Goal

The demarcation question is:

```text
Which assumptions must gravity supply before ordinary quantum mechanics,
statistical mechanics, and quantum information theory explain the black-hole
evaporation information story?
```

This note is the active steering document. The previous Matrix/moment-focused
version has been archived at:

```text
notes/archive/demarcation_synthesis_matrix_moment_archive_2026_06_26.md
```

For the current conceptual endpoint, see:

```text
notes/demarcation_algebra_type_synthesis.md
```

## Short Answer

Once a model supplies a finite black-hole Hilbert space, a radiation algebra or
factor, unitary dynamics, and enough mixing, ordinary quantum mechanics supplies
the familiar information-flow structure:

```text
Page behavior;
Hayden-Preskill recovery;
decoupling;
state-dependent mirror operators;
island-like algebraic bookkeeping.
```

The gravitational work is in supplying and tying together the inputs that make
that quantum-information machinery applicable:

```text
1. the finite state count, S = A/4G;
2. the Schwarzschild density of states, S(E) ~ E^2, and Hawking-scale softness;
3. the radiation/exterior/interior algebra or factorization;
4. unitary chaotic dynamics, including the thermal scrambling scale;
5. the geometric interpretation of the interior and near-horizon locality.
```

The practical boundary is therefore:

```text
QI/stat mech starts after the Hilbert-space size, algebraic split, and dynamics
are specified.

QG is responsible for deriving, constraining, or replacing those specifications.
```

There are two kinds of boundary:

```text
Crossable seams:
  gravity supplies an input that ordinary QI/stat mech can then consume.
  Examples: S=A/4G, S(E)~E^2, Hawking-scale softness, and the chaotic channel
  class needed for recovery.

Structural seams:
  gravity changes the algebraic question itself. The issue is the definition
  and redundancy of subsystems, especially interior/radiation assignments.
```

Rows 1, 2, and 4 below are mostly crossable. Rows 3 and 5 are structural.
This distinction matters because the Matrix/BFSS second-moment test lives on a
crossable seam, while the deepest demarcation question is the structural seam.

## Layer Map

| Layer | What it explains | Status | Demarcation lesson |
| --- | --- | --- | --- |
| Semiclassical geometry | Hawking temperature, greybody factors, emission rates, luminosity and lifetime scalings | Standard QFT in curved spacetime | Classical geometry fixes the thermodynamic radiation data. |
| Conditional finite quantum mechanics, kinematic | Page behavior from finite-dimensional unitarity and typicality | Standard once a finite system and a split are supplied | Page behavior consumes state count and factorization. |
| Conditional finite quantum mechanics, dynamical | Hayden-Preskill recovery, decoupling, abstract mirror/reconstruction structure | Standard once scrambling dynamics and sufficient radiation access are supplied | Recovery consumes the dynamical channel class. |
| State count and softness | Finite entropy, `S=A/4G`, Schwarzschild `S(E)~E^2`, Hawking-scale quanta | Gravitational; derived in special string/holographic regimes, open for generic Schwarzschild | This is the first hard input consumed by the QI story. |
| Algebra/factor definition | What counts as black hole, radiation, exterior, and interior | Subtle in gauge theory and gravity | The radiation subsystem is an assumption in QI and a construction problem in gravity. |
| Algebra/factor redundancy | How interior and radiation descriptions can encode the same information | Central in islands, complementarity, and holographic reconstruction | This is the sharp structural seam. |
| Dynamics and thermal tie | Unitarity, chaos, fast scrambling, relation between mixing and temperature | Assumed in toy models; supported but model-dependent in holographic systems | QI can use scrambling; gravity must explain why the black hole has the right scrambling dynamics. |
| Geometry/interior | Smooth horizon, local near-horizon correlators, infalling experience, complementary geometric descriptions | Irreducibly gravitational in the present program | Abstract recovery does not by itself produce local spacetime. |

## What Is Standard

Treat the following as background tools:

```text
Page behavior from finite-dimensional unitarity and typicality;
decoupling-based recovery;
Hayden-Preskill recovery from a scrambling system after enough radiation is
available;
thermal factors from density-of-states ratios, rho(E-omega)/rho(E);
the fact that probabilities do not determine a quantum channel;
the fact that output rates do not by themselves determine recoverability.
```

These are tools and background. They become relevant to black holes only after
gravity or a microscopic model supplies the state count, algebra, and dynamics.

## What Remains Demarcation-Relevant

### 1. State Count

Question:

```text
What microscopic structures realize S(E) ~ E^2 over a Schwarzschild window?
```

Current position:

```text
ordinary local finite-density systems do not naturally give this scaling;
long strings, fractionation, large-N matrix sectors, edge/constraint sectors,
and holographic constructions are the known routes.
```

Demarcation value:

```text
This is where the evaporation story first consumes a gravitational or
holographic input.
```

### 2. Softness

Question:

```text
Why are the active carriers Hawking-soft rather than ordinary high-energy
microscopic excitations?
```

Current position:

```text
Matrix/string fractionation and long-string mechanisms are the strongest local
literature anchors. They suggest how many degrees of freedom can share energy
so that the energy per active carrier is of order T.
```

Demarcation value:

```text
The density of states and the emission scale should be traced to the same
substrate.
```

### 3. Radiation Algebra and Factorization

Question:

```text
What is the radiation subsystem or algebra in gravity?
```

Current position:

```text
factorized toy models assume H = H_BH tensor H_rad;
gauge constraints and gravitational dressing make this split nontrivial;
islands and complementary recovery show that the interior/exterior assignment
is algebraic and state-dependent in gravitational settings.
```

The directly adjacent literature is target-space and matrix entanglement in
gauged matrix models. This literature already asks how to define subregions or
subsystems in matrix quantum mechanics while respecting gauge invariance. The
June 2026 audit sharpened the status:

```text
The conceptual construction is substantially occupied at toy/mechanism level:
target-space/matrix entanglement, emergent factorization, accessible algebras,
islands/Page behavior, and matrix-model von Neumann algebras are all active
literature. The remaining openings are rigor, realism, and dynamics, with strong
incumbents already working on rigor and realism.
```

Demarcation value:

```text
The factorization is the sharpest boundary between supplied QI structure and
quantum-gravity structure.
```

This row has two subproblems:

```text
3a. Factor definition:
    How does gravity define an exterior radiation algebra when constraints,
    dressing, and edge modes obstruct naive tensor factorization?

3b. Factor redundancy:
    How can the same information have an interior description and a radiation
    description, as in islands, complementarity, and entanglement-wedge
    reconstruction?
```

The first subproblem is already present in gauge theories and gravitational
constraint systems. The second is the structural seam: the issue is not only
which factor exists, but why two geometric assignments can represent the same
quantum information.

Relevant anchors:

```text
Mazenc--Ranard:
  target-space entanglement via subalgebras of observables;

Das--Kaushal--Mandal--Trivedi and Das--Kaushal--Liu--Mandal--Trivedi:
  target-space entanglement in D-brane holography and gauge-invariant
  target-space subalgebras;

Hampapura--Harper--Lawrence:
  target-space entanglement in gauged multi-matrix models;

Sugishita:
  algebraic target-space entanglement in fermion and matrix quantum mechanics;

Gautam--Hanada--Jevicki--Peng:
  matrix entanglement and its application to evaporating small black holes.
```

### 4. Dynamics and Information Export

Question:

```text
Does a microscopic gravity model actually produce the chaotic radiation channel
that QI assumes?
```

Current position:

```text
Once a generic shrinking channel is supplied, recovery follows from standard
decoupling. The remaining model-specific question is whether the microscopic
emission process supplies such a channel.
```

For Matrix/BFSS evaporation, the current concrete test is:

```text
Compute or bound the radiation-resolved second moments of the D0-detachment
operator.
```

Equivalently:

```text
Given amplitudes A_{i -> f,m}, where i is the initial black-hole microstate,
f is the unobserved daughter black-hole state, and m is the emitted D0/radiation
record, study

  K_{ij}^{mn} = sum_f A_{i -> f,m} A^*_{j -> f,n}.
```

This is a consistency test for a specific microscopic model:

```text
Does Matrix evaporation hand QI the kind of radiation channel that
Page/Hayden-Preskill recovery requires?
```

This row matters for dynamical recovery. Page behavior consumes less: finite
dimension, global purity, and a split. Hayden-Preskill recovery additionally
consumes scrambling, access to the emitted radiation, and the relevant
decoupling estimates.

July 2026 operational update:

```text
The source-rank question now has a conditional exterior certificate.
Occupation-enhanced rank-one emission gives a HIGH-side calibrated-response
deviation. A thermal bright collective channel is an exact equilibrium mimic,
but persistent drain makes it reservoir-starved; with
Gamma_th <= c_P T it gives a LOW-side deviation proportional to its flux.
Thus source-rank saturation follows within the weak-emission/refill class only
after gravity supplies ordinary EFT coupling and an operator-specific
thermal/QNM relaxation ceiling.
```

The companion latency theorem is one-way: small integrated access to the
diary-visible generator algebra forbids fast recovery. It does not prove that
a real horizon has the sufficient decoupling/export dynamics.

### 5. Geometry and Interior

Question:

```text
Which horizon features are absent from the exterior channel description?
```

Current position:

```text
exterior entropy flow and recovery can be modeled algebraically;
local near-horizon correlators, infalling experience, causal structure, and
the geometric meaning of complementary descriptions require more than a
factorized radiation channel.
```

Demarcation value:

```text
This is where operational information flow stops being an adequate substitute
for spacetime geometry.
```

## Matrix/BFSS Status

The Matrix track is one useful stress test of rows 1, 2, 3, and 4.

What the literature appears to supply:

```text
state count and softness:
  BFKS/KS, matrix strings, long-string/fractionated sectors;

first-moment Hawking-like emission:
  BFK/BFKS/Liu--Tseytlin and real-time BFSS black-zero-brane evaporation work;

asymptotic factorization:
  block separation into a daughter clump plus escaping D0/short-string sector.
```

What remains open:

```text
the dynamical-consistency check: once a radiation algebra is supplied by the
matrix-entanglement / emergent-factorization framework, does the actual
real-time detachment dynamics populate it generically enough for recovery?
```

This track can answer:

```text
Does this candidate microscopic gravity model supply the QI inputs it needs?
```

The broader rows remain:

```text
What is the general quantum-gravity origin of factorization, interior geometry,
or S=A/4G?
```

## Relation To Existing Drafts

```text
paper_ideal_hamiltonian:
  demonstrates how much exterior phenomenology follows after the state count,
  emission access, and mixing are supplied. It belongs to the conditional
  finite-quantum-mechanics layer.

paper_operational_horizon:
  packages the same conditional lesson around exterior horizon signatures. It
  should be read as an operational model with the gravitational inputs made
  explicit.

paper_boundary_saturation:
  addresses emission access: which entropy degrees participate in the coupling
  to radiation. It is demarcation-relevant if framed as an input gravity must
  supply or a microscopic model must derive.

paper_access_latency_classification:
  studies consequences of locality and access once an algebra and dynamics are
  specified. It is useful background, but much of the constrained-access
  machinery overlaps known QI/crypto/scrambling literature.

detachment_operator_test_spec:
  gives the concrete Matrix/BFSS consistency test for row 4.
```

## Rules For Future Work

Every proposed calculation, note, or draft should identify which row it tests:

```text
1. state count;
2. softness;
3. algebra/factorization;
4. chaotic dynamics and information export;
5. geometric/interior completion.
```

Then ask:

```text
Is this already standard QI/stat mech once the input is supplied?
Does it derive one of the inputs?
Does it show that a concrete microscopic model supplies one of the inputs?
Does it clarify why the input is specifically gravitational or holographic?
```

If the answer to all four questions is no, it is probably off the demarcation
path.

## Current Best Next Moves

1. Consolidate the two-sided source-rank certificate in
   `paper_boundary_saturation/main.tex`, retaining the Planckian/QNM,
   Markovian-refill, finite-accuracy, and multiplexing qualifiers.

2. Treat `notes/demarcation_algebra_type_synthesis.md` as the conceptual
   endpoint: Type I exact/QI, Type III_1 QFT, Type II crossed-product
   semiclassical gravity, with finite `e^{A/4G}` state count and lived interior
   as residues.

3. Reassess the drafts against the algebra-type synthesis and label standard QI
   consequences as standard QI consequences.

4. If continuing the Matrix direction, position it as a dynamical-consistency
   check on an algebra supplied by the matrix-entanglement literature, ideally
   in contact with that community.

5. Avoid new taxonomy or toy numerics unless they answer one of the residues:
   state count/equation of state, exact-to-semiclassical algebra transition, or
   lived interior, or close a named certificate loophole.
