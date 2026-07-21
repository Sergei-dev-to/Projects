# Observer Process Capacity in Quantum Gravity

Date: 2026-07-20

Status: **new successor-program charter; research proposal, not a completed
result.** This program is larger than the completed DSSYK WP2 gate and does not
reopen it. Results A--D and the standalone DSSYK demarcation paper remain
complete on their stated scopes. The literature map below is a bounded
orientation pass; every external novelty claim requires a dedicated overlap
pass before use.

## Decision in one paragraph

The worthwhile large question is not whether one more DSSYK detector curve can
be computed. It is whether quantum gravity admits an operational capacity law
for a self-contained observer: a bound on how much microscopic information the
observer can distinguish, retain, and recover over time, derived from the same
physics that fixes its clock, detector, memory, causal domain, and gravitational
backreaction. Positive cosmological constant is then tested as a regulator of
*observer process capacity* rather than assumed to be a literal spectral UV
cutoff. The existing program contributes the temporal-access and recovery
converse; the missing bridge is from gravitational resource consumption to a
distance or divergence between the actual observer process and every
diary-blind process.

## 1. The question

The central question is:

> For a self-contained observer in a gravitating causal diamond, what limits
> the amount and rate of microscopic information that can enter a persistent
> record and become recoverable, and how does that limit depend on the
> geometry--in particular on positive `Lambda`, `S_dS`, and the observer's
> allowed energy?

This separates five notions that are often conflated:

1. a cutoff on the spectrum of a dual Hamiltonian;
2. a finite state count or finite generalized entropy;
3. a limit on clock or detector resolution;
4. a limit on record formation and retention;
5. a limit on recoverable information per unit time or over the observer's
   lifetime.

The program targets items 4 and 5. A successful result may explain an
operational sense in which `Lambda` behaves like a cutoff without claiming item
1.

## 2. The common object: a self-contained observer process

Let `D` be a diary or microscopic code, `S` the probed field/system, `C` the
observer clock or reference frame, `Q` the detector, `M_j` retained observer
memory after slot `j`, `R_j` the new record produced at that slot, and `G_j` the
geometric or gravitational state relevant to later slots. A `K`-slot physical
observer process has the schematic form

```text
P_gamma^(K): D S C Q M_0 G_0
               -> R_1 ... R_K M_K G_K,                  (2.1)
```

where `gamma` denotes the physical background and couplings. The observable
record channel is obtained only after the unobserved systems are traced out.
The process must declare:

- the worldline or causal support of every contact;
- clock preparation and readout;
- detector switching, coupling normalization, and final readout;
- post-measurement state update;
- what memory persists and what is reset;
- energy/work exchanged with any battery or bath;
- stress, recoil, metric response, and horizon flux;
- every external reference, ancilla, and compiler used to implement the
  sequence.

An uncounted external clock, fresh memory supply, work reservoir, or coherent
ancilla is a resource leak, not a harmless idealization.

### 2.1 Process selection is class selection

A positive prediction requires an explicit implementable process. A universal
upper bound does not require one unique detector: gravity may instead select an
admissible class

```text
P_phys(gamma) = all observer combs satisfying the declared causal,
                constraint, conservation, and resource conditions. (2.2)
```

The capacity is then optimized over this entire class. This is the useful
larger meaning of *physical process selection*.

### 2.2 The blind comparison

For each physical process, compare against processes with the same public
energy, charge, clock, interfaces, causal support, and observer resources but
whose records are independent of the private diary. Denote this set by
`Blind_K(gamma)`. The matched comparison prevents ordinary timing, energy, or
observer metadata from being counted as microscopic access.

The existing quantities remain distinct:

```text
delta_K       pairwise record distinguishability;
A_K           cumulative distance from diary-blind sequential processes;
F_rec         declared classical or quantum recovery fidelity;
C_obs         largest recoverable diary code under the allowed process class.
                                                               (2.3)
```

Result B already proves that reliable recovery requires order-one cumulative
departure from every blind comparison comb, including processes with shared
memory. The new program must physically bound that departure.

## 3. Resource pricing is a feasible region, not one number

For a declared process `P`, collect the candidate resources as a vector:

```text
r(P) = (
  diary-sensitive interaction action,
  clock/reference asymmetry,
  detector and memory nonequilibrium free energy,
  blank memory and coherence lifetime,
  contact duration and repetition,
  entropy production and exported heat,
  stress-energy, recoil, and metric response,
  generalized-entropy or area expenditure,
  causal duration
).                                                        (3.1)
```

These entries have different units and are not to be added by definition.
*Physical resource pricing* means deriving a feasible region

```text
r(P) in F_gamma(Lambda, E_obs, boundary conditions, ...), (3.2)
```

or a model-specific monotone `B_gamma(P)` from the same dynamics that defines
the process. A valid price must be:

1. **source-derived:** not chosen after seeing the desired access curve;
2. **closed:** every clock, memory, ancilla, bath, and external reference is
   counted;
3. **sequentially composable:** it remains meaningful under adaptive repeated
   use and retained correlations;
4. **operational:** it bounds a process distance, divergence, or capacity;
5. **representation-covariant:** isometric redescription alone cannot change
   the price;
6. **nontrivial at the physical scale:** the resulting bound must improve on
   the unconstrained channel-capacity bound.

The detector-action audit established one negative example: a free-observer
energy cap does not by itself bound the normalization or integrated action of
an otherwise admissible detector contact. That does not rule out a separate
bound on reference-frame asymmetry, memory free energy, or gravitational
disturbance.

## 4. Central conjecture

### Observer-process budget conjecture

For a self-contained observer process in a gravitating causal diamond, there
exists a physically derived process budget `B_gamma` such that the adaptive
distinguishability of the actual diary-record process from the matched blind
class obeys

```text
D_proc(P_gamma^(K) || Blind_K(gamma)) <= B_gamma(P).       (4.1)
```

`D_proc` is to be chosen from an operational one-shot or amortized process
divergence appropriate to adaptive comb discrimination. The exact divergence,
normalization, and smoothing are theorem deliverables, not assumptions hidden
in the notation.

The budget must in turn be bounded by physical observer and geometric data:

```text
B_gamma(P) <= B_obs(
  Delta S_gen available,
  observer free energy and asymmetry,
  causal duration,
  admissible backreaction
  | Lambda, E_obs, ...).                                  (4.2)
```

Equations (4.1)--(4.2) are conjectural. In particular, generalized entropy is
not assumed to equal process capacity, and the listed resources are not
assumed to combine additively.

If a `d`-dimensional diary is recoverable with error `epsilon`, a one-shot
information converse should give a relation of the schematic form

```text
log d <= D_proc + correction(epsilon,d).                  (4.3)
```

Combining the three statements would produce the target observer-capacity law

```text
C_obs(K,epsilon | gamma)
  <= B_obs(Lambda,S_dS,E_obs,T,...) + error terms.         (4.4)
```

For a fixed diary dimension, Result B supplies the trace-distance necessary
side of this chain. Capacity scaling requires the relative-entropy,
hypothesis-testing, or other one-shot divergence upgrade in (4.3).

### Why this is the hard bridge

Existing gravitational entropy results are primarily state or algebra
statements. An observer process is adaptive, multitime, and memoryful. The
load-bearing mathematical problem is therefore to lift a bound on matter plus
geometry to a bound on adaptive record formation:

```text
state relative entropy / generalized entropy / canonical energy
                       |
                       v
       adaptive process divergence from diary blindness
                       |
                       v
            distinguishability and recovery capacity.    (4.5)
```

Data processing can carry a valid joint-state or process bound down to the
record. It cannot manufacture the missing upper bound on the joint process.
Likewise, Pinsker-type inequalities can convert a relative-entropy upper bound
to trace distance, but only after a common state, reference, and adaptive
strategy class have been controlled. Establishing that control is central,
not bookkeeping.

## 5. What a substantial result would look like

The program has a result ladder. It is not committed to a positive theorem at
every level.

### Level I -- universal resource-to-access theorem

Prove that if every admissible slot has a physically bounded diary-visible
process divergence or defect, then the full memoryful observer record and its
recovery capacity obey a composable bound. This extends Result B from a
necessary distance statement to a capacity statement with an explicit physical
resource ledger.

Minimum worthwhile deliverable:

```text
physical per-slot/resource budget
  => adaptive comb divergence bound
  => one-shot classical and quantum recovery converse.    (5.1)
```

### Level II -- one model derives process and price jointly

Construct a Lorentzian observer model in which one microscopic action fixes:

- the detector instrument or process tensor;
- retained memory and reset dynamics;
- the observer's stress, dissipation, and recoil;
- the induced gravitational response;
- a nontrivial admissibility or lifetime condition.

Then optimize access under the derived condition. A near-saturating process is
part of a strong positive result.

### Level III -- gravitational observer-capacity theorem

Relate the physical process budget to generalized entropy, canonical energy,
area change, or another gravitational monotone in a causal diamond. The result
must constrain a record or recovery quantity, not merely entropy of an
unmeasured state.

An example target, with the form and constants left open, is

```text
recoverable record information accumulated by O
  <= decrease of a derived observer-plus-geometry budget. (5.2)
```

An equally valuable negative result would prove that generalized entropy,
`Lambda`, and observer energy alone cannot upper-bound process capacity without
an additional closure condition on couplings, references, or memory renewal.

### Level IV -- de Sitter process-capacity law

For a static-patch observer, derive rather than assume the dependence on

```text
R_dS,  T_dS,  S_dS,  E_obs,  observation time.           (5.3)
```

Keep separate:

- total lifetime capacity;
- capacity rate or temporal bandwidth;
- minimum resolvable time/energy scale;
- one-shot memory capacity.

A bound of order `S_dS` on total records is not automatically a UV or rate
bound. A genuine operational-cutoff result must state which of these quantities
is limited.

### Level V -- dual realization and DSSYK test

Only after a bulk process class and price are derived should a dual model be
asked to reproduce them. The DSSYK tasks would then be:

1. identify the dual of the full observer instrument, not only its correlator;
2. map the bulk budget to a dual process cost;
3. test the finite-shell diary and disorder variance;
4. apply the exact one-copy/equal-energy isometry;
5. determine whether the dual realizes an absolute observer bound, a genuine
   implementation difference, or only a representation change.

The program does not require a doubled-model advantage. Faithful reproduction
of a bulk absolute capacity law would already be a meaningful dual test.

## 6. Coordinated workstreams

The following are parts of one program, not independent reframings.

| workstream | physical question | principal output | main failure mode |
| --- | --- | --- | --- |
| A. Observer combs | What process is implemented by a localized detector, clock, readout, and memory? | Lorentzian instrument/process tensor with causal composition | correlators are mistaken for records |
| B. Reference and control | What phase, timing, and noncovariant operations can a finite observer implement? | WAY/asymmetry and reference-degradation bounds for sequential records | an external clock or catalytic correlation is left uncounted |
| C. Thermodynamic memory | What does writing, retaining, and resetting records consume? | one-shot/cyclic free-energy and blank-memory ledger | cyclic reset is assumed when only one-shot storage is physical |
| D. Gravity pricing | How do the same contacts change stress, geometry, horizon entropy, or observer lifetime? | process-divergence or access bound from gravitational admissibility | a Euclidean or statewise bound is applied to an unrelated Lorentzian instrument |
| E. de Sitter and duals | How does the derived law scale with `Lambda`, and how is it represented in a dual? | static-patch law plus DSSYK or other dual test | dimensional analysis or abstract spectral data substitute for a dictionary |

The clock/asymmetry branch is therefore not the whole program. It prices one
way of making energy-phase information operational. The detector-action branch
prices contact strength and duration. The memory branch closes repeated-use
loopholes. The gravity branch is what can make the combined restriction a
quantum-gravity result.

## 7. Preferred integrated benchmarks

### 7.1 Lorentzian Gaussian worldline benchmark

The first model should be large enough to contain the whole logical chain but
simple enough to solve:

- a free field in a Rindler or de Sitter static patch;
- a finite or harmonic worldline detector with explicit switching;
- a retained record oscillator or qubit memory;
- an autonomous or fully counted clock/reference;
- linearized gravitational response or a controlled proxy for it.

For Gaussian choices, an influence functional can determine the memory kernel
and multitime process once the coupling and readout are declared. The same
coupling supplies stress and dissipation. The goal is not realism by itself,
but one nontrivial example where process and price come from one action.

### 7.2 Backreacting de Sitter benchmark

The second benchmark should introduce a genuine horizon or area budget. JT de
Sitter with an information-collecting observer is a natural near hit because
recovery and backreacted geometry coexist. Its current role is not to supply a
ready-made detector comb, but to test whether the collector's record process can
be inserted without divorcing information gain from the geometry that pays for
it.

### 7.3 DSSYK benchmark

DSSYK remains a later dual laboratory. It already supplies the exact isometric
control, a constraint-preserving model detector contact, relational dressing,
clock/correlator data, and a sharp demonstration of what is not selected. It
does not currently supply the joint Lorentzian process budget required for the
first two benchmarks.

## 8. Work packages

### QG0 -- charter and full overlap map

Status: this charter is complete; the full overlap map is not.

Deliverables:

1. line-by-line map from adjacent theorems to (4.1)--(4.4);
2. precise distinction between state entropy, channel capacity, process
   divergence, detector response, and recoverable records;
3. identification of any prior adaptive gravitational capacity theorem;
4. one primary source set for each workstream.

### QG1 -- abstract observer-capacity theorem

Define the self-contained observer comb, matched blind class, adaptive process
divergence, and one-shot capacity. Prove the abstract implication

```text
derived process budget <= B
  => classical/quantum observer capacity <= F(B,epsilon). (8.1)
```

This work package uses Result B but must not claim novelty for standard
strategy-divergence or channel-capacity inequalities without a full comparison.

### QG2 -- joint instrument/backreaction model

Build the Lorentzian Gaussian worldline benchmark and derive from one action:

1. the two-slot process first, then arbitrary `K` if controlled;
2. diary-conditioned records;
3. retained detector/reference state;
4. energy, work, noise, and stress response;
5. a model-internal admissibility region;
6. the optimized access-versus-disturbance curve.

QG1 and QG2 can proceed in parallel and must meet at a common process
divergence.

### QG3 -- generalized-entropy/process bridge

Test whether relative entropy, canonical energy, quantum Bousso/GSL data, or a
crossed-product entropy law can upper-bound the divergence of the observer
process from its blind comparison. The theorem must include the observer's
record algebra and retained memory. If no such implication holds, extract the
counterexample and state the missing physical assumption.

### QG4 -- de Sitter scaling and interpretation

Insert a controlled static-patch geometry and determine whether the bound is on
total capacity, rate, resolution, or lifetime. Derive the `Lambda` dependence
from the model. Compare the result with `S_dS`, generalized heat capacity, and
Bekenstein-type channel bounds without identifying them by name alone.

### QG5 -- dual test

Conditional on QG2--QG4. Translate the complete process and budget into DSSYK
or another explicit dual, retain the one-copy isometric control, and compute a
recovery-grade quantity. No dual dynamics calculation is authorized merely by
completion of QG1.

## 9. Program gates

### Continue if

- one resource derived from the same action as the instrument gives a
  nontrivial process-divergence bound;
- the bound survives persistent memory, adaptive strategies, and counted
  references;
- a gravity relation constrains that resource without importing a separate
  incompatible observer model;
- the physical scaling distinguishes total capacity, rate, and resolution;
- the result adds a multitime/recovery statement not already contained in
  state-entropy or ordinary channel-capacity literature.

### Stop or reframe if

- generalized entropy enters only as an assumed memory dimension;
- an energy cap is again used to price an unrelated interaction;
- the result requires unpriced resets, clocks, baths, compilers, or fresh
  ancillas;
- the adaptive process bound collapses to a known theorem with no gravitational
  or recovery content;
- the `Lambda` scaling is dimensional analysis rather than dynamics;
- the bound is trivial at the relevant de Sitter scales;
- the claimed dual difference disappears under exact isometric transport and
  no independent implementation datum remains.

The final condition does not kill an absolute bulk observer-capacity result. It
kills only a claim that the doubled constraint itself created the advantage.

## 10. Strong positive and negative endpoints

### Strong positive endpoint

A publishable positive endpoint would contain all of:

1. a self-contained Lorentzian observer process;
2. a source-derived resource or backreaction law;
3. a composable process-distance or divergence theorem;
4. a recovery/capacity converse;
5. a nontrivial `Lambda` or causal-diamond scaling;
6. a protocol saturating or parametrically approaching the bound;
7. a matched dual or nongravitational control.

### Strong negative endpoint

A publishable negative endpoint would prove a general nonimplication such as:

> generalized entropy, observer energy, and an accessible algebra do not bound
> adaptive observer process capacity unless the physical construction also
> closes coupling normalization, external references, and memory renewal.

This would generalize the DSSYK energy-cap/action-budget nonimplication from one
contact model to a theory-level limit on static-to-operational inference.

## 11. Relationship to the completed work

The completed program contributes:

- **Result A:** a control showing that thermodynamic realism and information
  diagnostics can coexist in one state;
- **Result B:** the temporal hybrid/recovery converse used after a physical
  process budget is obtained;
- **Result C:** the prohibition on inferring microscopic access from static
  thermodynamics or low-point response alone;
- **Result D:** the separation of degeneracy, active rank, and diary export;
- **DSSYK WP0--WP2:** the exact isometric null, clock-state/instrument
  nonidentifiability, contour-typing obstruction, explicit detector contact,
  and energy-cap/action-budget nonimplication.

None of these is reopened. The new program begins one level above them: it asks
for the physical law that turns observer and gravitational resources into a
process-capacity bound.

The standalone DSSYK paper should not absorb this conjectural program. It may
later be cited as the demarcation that motivated the larger question.

## 12. Bounded field map

The following adjacent literatures currently provide separate components.
Their conjunction and novelty relative to (4.1)--(4.4) remain to be audited.

### Local measurement and multitime processes

- Fewster and Verch,
  [*Quantum Fields and Local Measurements*](https://arxiv.org/abs/1810.06512),
  derive localized system--probe measurement maps and instruments.
- Polo-Gomez, Garay, and Martin-Martinez,
  [*A Detector-Based Measurement Theory for Quantum Field Theory*](https://arxiv.org/abs/2108.02793),
  derive field POVMs and state updates from declared detector couplings and
  readouts.
- Jorgensen and Pollock,
  [*Exploiting the Causal Tensor Network Structure of Quantum Processes to Efficiently Simulate Non-Markovian Path Integrals*](https://arxiv.org/abs/1902.00315),
  connect influence functionals to multitime process tensors.

These works show how a specified interaction becomes an instrument. They do
not by themselves select or gravitationally price the interaction.

### Conservation, clocks, and reference resources

- Ahmadi, Jennings, and Rudolph,
  [*The WAY theorem and the quantum resource theory of asymmetry*](https://arxiv.org/abs/1209.0921),
  formulate conservation-limited measurement as an asymmetry resource problem.
- Katsube, Ozawa, and Hotta,
  [*Limitations of Quantum Measurements and Operations of Scattering Type under the Energy Conservation Law*](https://arxiv.org/abs/2211.13433),
  give quantitative energy-conservation limits for scattering measurements
  and operations.
- Marvian and Spekkens,
  [*A no-broadcasting theorem for quantum asymmetry and coherence and a trade-off relation for approximate broadcasting*](https://arxiv.org/abs/1812.08766),
  establish degradation constraints for bounded quantum reference frames.
- Erker et al.,
  [*Autonomous quantum clocks: does thermodynamics limit our ability to measure time?*](https://arxiv.org/abs/1609.06704),
  relate clock performance to heat and entropy production in an autonomous
  model.

These are candidates for the reference branch, not a pre-existing gravity
price. Their assumptions about additive conservation, external symmetry
frames, finite size, and repeated correlations must be checked in each
gravitating model.

### Thermodynamic and operational process costs

- Faist and Renner,
  [*Fundamental work cost of quantum processes*](https://arxiv.org/abs/1709.00506),
  derive a general information-theoretic lower limit on process work cost.
- Shirokov,
  [*Energy-constrained diamond norms and their use in quantum information theory*](https://arxiv.org/abs/1706.00361),
  supplies continuity tools for infinite-dimensional energy-constrained
  channels and capacities.
- Hayden and Wang,
  [*What exactly does Bekenstein bound?*](https://arxiv.org/abs/2309.07436),
  test Bekenstein bounds directly on communication capacities and show the
  importance of restricting both encoder and decoder.

The Hayden--Wang result is a close operational anchor. The new question is
memoryful observer record formation and recovery with the observer and its
backreaction included inside the process.

### Gravitational entropy and relative entropy

- Casini,
  [*Relative entropy and the Bekenstein bound*](https://arxiv.org/abs/0804.2182),
  formulates the flat-space bound through relative-entropy positivity.
- Wall,
  [*A proof of the generalized second law for rapidly changing fields and arbitrary horizon slices*](https://arxiv.org/abs/1105.3445),
  proves a semiclassical GSL for causal horizons under stated algebraic
  assumptions.
- Bousso, Casini, Fisher, and Maldacena,
  [*Proof of a Quantum Bousso Bound*](https://arxiv.org/abs/1404.5635),
  bound vacuum-subtracted entropy on a light-sheet by area decrease for free
  fields with weak backreaction.
- Lashkari and Van Raamsdonk,
  [*Canonical Energy is Quantum Fisher Information*](https://arxiv.org/abs/1508.00897),
  identify a holographic relative-entropy metric with bulk canonical energy in
  an AdS setting.
- Jafferis, Lewkowycz, Maldacena, and Suh,
  [*Relative entropy equals bulk relative entropy*](https://arxiv.org/abs/1512.06431),
  relate nearby-state boundary and bulk relative entropy in entanglement
  wedges.
- Faulkner and Speranza,
  [*Gravitational algebras and the generalized second law*](https://arxiv.org/abs/2405.00847),
  connect crossed-product entropy, generalized entropy, and GSL monotonicity
  for Killing horizons in a semiclassical regime.

These are state, wedge, algebra, or horizon-cut results. The proposed process
bridge must not cite them as adaptive observer-capacity theorems before that
bridge is proved.

### de Sitter observer and backreaction anchors

- Chandrasekaran, Longo, Penington, and Witten,
  [*An Algebra of Observables for de Sitter Space*](https://arxiv.org/abs/2206.10780),
  construct a worldline-dressed Type-II observer algebra and generalized
  entropy.
- De Vuyst, Eccles, Hoehn, and Kirklin,
  [*Gravitational entropy is observer-dependent*](https://arxiv.org/abs/2405.00114),
  sharpen the quantum-reference-frame dependence of the observer algebra and
  entropy.
- Aalsma and Sybesma,
  [*The Price of Curiosity: Information Recovery in de Sitter Space*](https://arxiv.org/abs/2104.00006),
  place radiation recovery and collecting-observer backreaction in one JT de
  Sitter geometry.
- Banks and Draper,
  [*Generalized Entanglement Capacity of de Sitter Space*](https://arxiv.org/abs/2404.13684),
  propose a generalized heat/entanglement capacity for the static patch. This
  use of “capacity” is thermodynamic and must be distinguished from operational
  process capacity.
- Tietto and Verlinde,
  [*A Microscopic Model of de Sitter Spacetime with an Observer*](https://arxiv.org/abs/2502.03869),
  supply observer thermodynamics and a model-specific energy partition/cap.
- Narovlansky and Verlinde,
  [*Double-scaled SYK and de Sitter Holography*](https://arxiv.org/abs/2310.16994),
  supply the doubled equal-energy model, constraint-preserving operators, and
  a model detector contact.

The completed DSSYK audits explain why these ingredients cannot presently be
composed into (4.1)--(4.4) by citation alone.

## 13. Immediate program move

The first move should preserve the large objective while producing two
independent pieces that can meet:

1. **QG1 theorem skeleton:** define the adaptive blind-process divergence and
   prove the exact information/recovery consequence of a hypothetical budget
   `B`.
2. **QG2 model skeleton:** write one Lorentzian detector--field--memory action
   and derive both its two-slot record process and its disturbance/resource
   ledger.

Do not begin with DSSYK numerics, a chosen complexity measure, or an assumed
`S_dS` memory dimension. The first integration gate is whether the model's
derived ledger controls the same process divergence used by the theorem.

That is the first falsifiable calculation inside a large program, not the
definition of the program's ambition.
