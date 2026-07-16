# The Evaporation Completion and Identifiability Problem

Date: 2026-07-11

Status: historical intermediate synthesis. This note refined
`program_reassessment_2026_07_10.md` by replacing a strict gravity/QI
demarcation with a common mathematical object and two concrete questions:
forward completion by a microscopic model and inverse identification from
restricted radiation data. Its formalism remains useful, but its proposed work
queue is superseded by the final endpoint in
`program_endpoint_and_standalone_results_2026_07_13.md`.

## 1. Scope and Central Claim

The program's constructive models, conditional recovery arguments, failed
source certificate, temporal-access theorem, and Matrix proposal can be
organized around one object: an energy-graded sequential evaporation
instrument viewed through a specified exterior algebra.

The central issue is:

```text
Semiclassical thermodynamics and Hawking-like observations constrain only
partial data about the evaporation instrument. Which global quantum processes
are compatible with those constraints, how do they route microscopic
information, and which differences can restricted exterior observations
identify?
```

This will be called the **evaporation completion and identifiability problem**.

The word "completion" must be used precisely. The program considers distinct
global processes compatible with the same *partial* Hawking data: shell
dimensions, inclusive transition rates, selected response functions, or local
radiation marginals. It does **not** claim that inequivalent recovery behavior
can arise from different Stinespring dilations of one already fixed complete
radiation channel. Once the full accessible channel or process comb is fixed,
its information-recovery properties are fixed as well; minimal Stinespring
dilations differ only by an environment isometry.

## 2. Common Mathematical Object

Let the microscopic evaporating system have energy/charge-graded shells

```text
H_B = direct_sum_(E,q) H_(E,q),
dim H_(E,q) = exp[S(E,q)].                                (2.1)
```

One emission step is a physical isometry

```text
V_j : H_(E_j,q_j)
      -> direct_sum_m H_(E_j-omega_m,q_j-delta_q_m)
         tensor R_(j,m) tensor P_(j,m),                  (2.2)
```

where:

```text
B_(j+1): daughter shell;
R_j:     candidate accessible radiation record;
P_j:     partners, edge sectors, hidden archive, or other complementary data;
m:       energy, charge, species, angular, time-bin, or detector label.
```

Equivalently, after choosing resolved output bases, (2.2) supplies transition
or Kraus blocks

```text
D_(j,m,p) : H_(E_j,q_j) -> H_(E_j-omega_m,q_j-delta_q_m), (2.3)
```

where `p` labels complementary output data when it is not retained explicitly.
The complete evaporation history is the sequential composition

```text
V_(1:K) = V_K ... V_1,                                   (2.4)
```

with fresh records, changing shell dimensions, shared memory, and accumulated
partners. Operationally this is a quantum instrument or process comb, not a
single memoryless channel.

The exterior theory must also specify an accessible algebra `A_R(K)` on the
accumulated outputs. The induced record channel is

```text
N_K^A(rho)
  = restriction to A_R(K) of
    Tr_(B_K,P_hidden)[V_(1:K) rho V_(1:K)^dag].           (2.5)
```

Changing `A_R(K)` can change recoverability even when the underlying isometry
is unchanged. Gauge constraints, dressing, charge centers, islands, detector
resolution, and allowed side information therefore enter through the algebra
and restriction in (2.5), not merely through a tensor-factor label.

## 3. What the Different Branches Measured

The major project branches studied different data extracted from (2.1)--(2.5).

| branch | object studied |
| --- | --- |
| state count and area register | shell dimensions `dim H_(E,q)` |
| negative heat capacity | variation of shell dimensions with energy |
| golden-rule softness and luminosity | traces/norms of energy-lowering blocks and exterior phase space |
| shrinking-sector models | changing daughter dimensions in (2.2) |
| unified sector isometry | one supplied completion producing thermodynamic and entropy diagnostics |
| ideal Hamiltonian/ETH | conditions making the physical blocks approximately typical/isometric |
| constrained access | growth of `A_R(K)` and routing into its recoverable part |
| source participation | a proposed internal factorization of the blocks in (2.3) |
| source-invariance audit | replacement of noncanonical source lists by channel/process invariants |
| static certificate | inference of internal/process structure from low-order exterior projections |
| temporal-access theorem | distance of `N_K^A` from diary-blind comparison combs |
| no-hiding archive bound | minimum capacity of `B_K tensor P_hidden` under exterior blindness |
| ETH/design sufficiency | moment conditions under which the complement decouples from a diary reference |
| Matrix/BFSS detachment | proposed derivation of (2.2)--(2.5) from a named microscopic Hamiltonian |

The branches were therefore not independent candidate inputs. They were
kinematic, dynamical, algebraic, complementary-channel, and inferential views
of the same sequential instrument.

## 4. Partial Hawking Data

Different calculations and observations fix different projections of the
instrument.

### 4.1 Thermodynamic shell data

```text
S(E,q) = log dim H_(E,q),
beta = partial_E S,
exp[S(E-omega,q-delta_q)-S(E,q)].                        (4.1)
```

For Schwarzschild, `S(E)~E^2` fixes `T(E)~E^-1` and the density-of-states
bias toward Hawking-soft transitions. It does not fix the physical emission
matrix elements, species, greybody propagation, or information-bearing
orientation of the transition blocks.

### 4.2 Inclusive emission data

Rates and spectra constrain quantities of the form

```text
Gamma_m(E)
  proportional to (1/d_E) Tr[D_m^dag D_m],               (4.2)
```

possibly together with absorption, KMS/detailed-balance ratios, linewidths,
and low-order response functions. These are block norms or averages. They do
not determine the operators `D_m` on the full shell.

### 4.3 Local radiation states

One-wavepacket density matrices and Gaussian correlators constrain reduced
outputs of (2.5). They need not determine correlations among different
emission times or the dependence of those correlations on a private diary.

### 4.4 Full controlled process

The complete family of input-dependent, intervention-dependent multitime
statistics would determine the accessible process up to the usual operational
equivalences. This is much stronger than passive Hawking observation and is
not generally available for a single astrophysical black hole.

## 5. Hawking-Data Equivalence Classes

Let `D` denote a declared set of accessible data: thermodynamic relations,
inclusive rates, selected correlators, interventions, time windows, and error
tolerances. Define

```text
V ~_(D,epsilon) V'
```

when the two evaporation processes agree on every datum in `D` to tolerance
`epsilon`.

As `D` is enlarged, the equivalence classes refine:

```text
shell thermodynamics
  -> inclusive flux and response
  -> local radiation marginals
  -> passive multitime correlations
  -> controlled diary-sensitive process data
  -> full accessible process tomography
  -> independently supplied microscopic Hamiltonian/dilation data. (5.1)
```

The final arrow denotes added model-side information, not an inference from
process tomography. Even a fully reconstructed accessible process generally
does not identify a unique microscopic Hamiltonian or inaccessible dilation.

A proposed property is identifiable from `D` only if it is constant, or
uniformly bounded, throughout the corresponding equivalence class.

This criterion explains the source-rank failure. A preferred decomposition

```text
H_int = sum_mu O_mu tensor B_mu                           (5.2)
```

can change under compensating invertible refactorizations while the physical
interaction remains fixed. Raw source Gram participation is therefore not
constant even before restricting to exterior data. The physical jump map,
its Choi operator, and the complete process are representation-invariant after
the shell metric, exterior basis, and detector band are fixed.

## 6. Exact Separation Examples

The program contains explicit processes occupying the same coarse data class
while differing at a stronger information level.

### 6.1 Finite thermal pump versus diary access

The finite parametric pump emits `O(S)` approximately thermal Hawking/partner
records, obeys finite energy accounting, and has Hawking-like static response,
while its complete radiation process is exactly constant on an arbitrarily
large spectator diary.

Therefore:

```text
finite energy + thermal emission + partner production
  does not imply diary access.                            (6.1)
```

### 6.2 Blind and mixing shrinking-shell completions

The integrated microcanonical construction supplies blind and mixing
processes with the same:

```text
S(E)~E^2 shell trajectory;
event probability and detailed-balance ratio;
one-wavepacket energy state;
one-wavepacket degeneracy state;
event-partner record.                                    (6.2)
```

In the blind process, lost logical dimensions enter a hidden archive. In the
mixing process, a logical diary is encoded in multitime radiation
correlations. Every one- and two-wavepacket reduced state can be diary blind
while three records recover the diary exactly.

Therefore:

```text
identical local Hawking data
  does not determine the global information-routing completion. (6.3)
```

### 6.3 Access without decoupling

A process can become order-one distinguishable from a diary-blind process by
exposing a charge, dephasing a diary, or repeatedly sampling one direction,
yet fail to decouple the diary reference from the daughter.

Therefore:

```text
nonzero or order-one process access
  does not by itself imply recoverable export.            (6.4)
```

These are not different dilations of one fixed full radiation channel. They
are different full channels/processes that coincide only on the deliberately
restricted data in (6.1)--(6.3).

## 7. Information Destination, Access, and Recovery

The completion framework separates three logically distinct statements.

### 7.1 Destination

For a globally isometric shrinking process, exact exterior blindness implies
that the complementary daughter-plus-hidden system retains a reversible copy
of the input. Across blind shrinking steps, the required hidden logical
capacity is at least

```text
dim archive >= d_initial/d_final.                         (7.1)
```

Thus complete evaporation without an entropy-sized hidden archive forces
information to leave the shrinking system eventually.

### 7.2 Access

Let `A_K` be the minimum cumulative hybrid-reachable process defect from every
diary-blind comparison comb. The composable theorem gives

```text
A_K=o(1)
  => no order-one diary recovery from the record by step K. (7.2)
```

Order-one separation from blindness is necessary.

### 7.3 Recovery

Recovery requires the stronger complementary-channel condition

```text
||rho_(Q B_K P_hidden)-rho_Q tensor rho_(B_K P_hidden)||_1 << 1, (7.3)
```

or an equivalent correctability statement for the chosen radiation algebra.
ETH/design moment conditions are sufficient routes to (7.3), but remain
model-side dynamical hypotheses until verified for a physical emitter.

The distinction is:

```text
shrinking/no archive fixes eventual destination;
process distance diagnoses necessary access;
decoupling establishes recoverable export.               (7.4)
```

## 8. Scrambling Reinterpreted

Generic chaos or scrambling is not an independent guarantee of export. Its
relevant role is to rotate private shell directions relative to the physical
emission blocks so that the accessible process becomes diary-visible and
eventually decoupling.

The meaningful dynamical condition is therefore

```text
emission-relative mixing of the physical instrument,     (8.1)
```

not scrambling diagnosed only by level statistics, OTOCs, or an internal
mixer detached from the emission operator.

The failed source-participation input and the former scrambling input meet at
this point: both were proxies for how broadly the physical emission process
acts on private directions. The invariant target is the process itself.

## 9. Forward and Inverse Problems

### 9.1 Forward completion

Given a microscopic Hamiltonian, constraints, state preparation, and exterior
algebra:

```text
derive or calculate V_(1:K) or its controlled invariants;
verify thermodynamic and gauge/charge sectors;
determine information destination, access, and decoupling;
test scaling with energy, size, cutoff, and regulator.    (9.1)
```

Matrix/BFSS detachment is one candidate forward problem. A small bosonic
matrix pilot can validate definitions and methods; it cannot by itself
establish the large-`N` BFSS completion.

### 9.2 Inverse identification

Given an allowed exterior dataset `D`:

```text
determine which completion properties are identifiable;
construct indistinguishable adversarial completions when they are not;
find the least costly additional interventions that separate the target
classes;
state sample, energy, time, and control complexity.       (9.2)
```

The static source-certificate branch is principally an inverse result. Its
failure motivates class-relative process property testing rather than a
universal scalar certificate.

## 10. Relation to the Channel/Code Separation

A related channel/code proposal gives a communication-theory description of
the same structure:

```text
coarse carrier/channel data:
  temperature, greybody response, energy/charge budget, forced metadata;

code/routing data:
  how microscopic private information is embedded into the emitted records.
```

This is useful if "channel" is understood as the coarse carrier specification,
not the complete CPTP map from the microscopic shell to all accessible
radiation. In standard quantum-information language, once that complete map
and its input code are fixed, recovery is no longer an independent hidden
choice. The apparent channel/code ambiguity exists because Hawking data fix
only a restricted projection of the physical process.

The completion language therefore supplies the precision behind the analogy:

```text
carrier-level Hawking data
  = the declared partial dataset D;

code/routing choice
  = the unresolved action of compatible completions on private directions;

decoding experiment
  = a stronger process-level datum that refines the equivalence class.
```

Two conclusions are already supported:

```text
static carrier data do not determine private routing;
shrinking capacity with no hidden archive imposes an eventual transmission
obligation.
```

Stronger statements in the channel/code note remain research targets rather
than consequences of the present synthesis:

```text
that black holes are uniquely or exactly self-provisioned channels;
that gravitational constraints force a quantitative header but not payload;
that a Page-time access deadline follows without a mixing/typicality input;
that the algebra-type transition is the shadow of timing metadata.
```

These proposals should be tested inside the completion formalism, where the
accessible algebra, hidden capacity, channel uses, coherent capacity, and
error criterion must all be explicit.

## 11. Revised Validation Hierarchy

The earlier validation ladder is now interpreted as progressively richer
projections of the evaporation completion:

| level | established data | does not by itself establish |
| --- | --- | --- |
| 0 | shell state count and thermodynamics | physical emission |
| 1 | inclusive spectrum, power, lifetime | diary sensitivity |
| 2 | local response and radiation statistics | multitime information routing |
| 3 | specified sequential physical instrument | recovery from a chosen algebra |
| 4 | order-one diary access | isotropic decoupling |
| 5 | recovery/decoupling | gravitational geometry or smooth interior |
| 6 | algebraic/geometric interpretation | microscopic origin of all preceding data |

Claims about an evaporator or simulator should state which level is actually
verified. Matching a lower projection is not evidence for an unspecified
higher completion property.

## 12. Relation to Gravity

This framework does not identify a unique boundary between gravity and QI.
Instead it distinguishes logical roles.

```text
microscopic/gravitational theory may supply:
  the shell spectrum and state count;
  the constrained physical instrument;
  the exterior algebra and partner disposition;
  the dynamics selecting an information-routing completion;
  the geometric/interior interpretation;

statistical mechanics and QI supply:
  consequences of density-of-states ratios;
  channel and complementary-channel identities;
  no-hiding, decoupling, capacity, and recovery theorems;
  limits on inference from restricted data.              (11.1)
```

Under duality, the same completion may have geometric and many-body
descriptions. The invariant distinction is between facts established by the
concrete theory and consequences following from abstract quantum structure.

## 13. What the Framework Does Not Solve

The completion language represents but does not derive:

```text
the microscopic origin of S=A/4G or generic Schwarzschild S(E)~E^2;
the physical exterior algebra in a nonperturbative gravitational theory;
a large-N microscopic evaporation instrument;
smooth infalling experience or local interior geometry;
the compatibility of information export with semiclassical near-horizon EFT.
```

Those are not defects in the definition. They are upstream or downstream
physical constraints that a successful completion must satisfy.

## 14. Novelty Calibration

Quantum instruments, Stinespring dilation, process tensors/combs,
complementary-channel recovery, Page decoupling, and the broad fact that
thermal marginals do not determine global information are standard.

The potentially distinctive project output is narrower:

```text
an explicit hierarchy of black-hole-like partial data;
exact blind/mixing completions sharing that data;
the source-representation no-go and static identifiability map;
a composable long-time access obstruction for changing-shell emitters;
the destination/access/recovery separation;
a model-facing invariant transition/process interface.   (13.1)
```

Each item requires an independent literature and theorem audit before a
priority claim. The framework is valuable only if it sharpens one or more of
those technical results; naming the common object is not itself a discovery.

## 15. Proposed Program Consequences at This Stage

The primary question becomes:

> Given black-hole thermodynamic and semiclassical emission constraints, what
> additional physical principles select the information-routing completion,
> and what restricted data can distinguish the resulting classes?

The near-term work proposed at this stage was:

```text
1. Consolidate the exact equivalence/separation examples into one canonical
   completion matrix.

2. Audit the composable access theorem against quantum-comb continuity and
   strategy-distance literature.

3. Audit the static no-go package against quantum system identification,
   hidden-realization, and channel property-testing literature.

4. Identify a class-relative low-cost witness of diary access or decoupling;
   stop if every witness requires full process tomography.

5. Treat Matrix/BFSS as a forward application only after a gauge-invariant
   instrument and accessible algebra pass the design gate.

6. Keep state-count origin and geometric/interior completion visible as
   separate physical boundaries rather than pretending the instrument
   language derives them.
```

## 16. Concise Program Statement

> Black-hole thermodynamics and Hawking-like observations constrain only
> partial projections of a sequential, energy-graded evaporation instrument.
> Distinct global processes can share those projections while routing private
> information into accessible multitime radiation, a hidden archive, or a
> protected daughter sector. The program classifies these completions,
> determines which properties restricted radiation data can identify, and
> asks microscopic models to calculate the physical completion. Recovery is a
> property of the complete accessible process, not of thermality, source rank,
> or generic scrambling taken separately.
