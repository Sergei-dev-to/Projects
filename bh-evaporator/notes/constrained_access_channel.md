# Constrained access channel

Date: 2026-06-13

Purpose: isolate the "access channel" object that keeps reappearing:
black-hole radiation, bath coupling, mining, gauge constraints,
holography of information, Quantum Darwinism, and the Heisenberg cut
are all cases where information exists globally but only selected
algebras/fragments/protocols can access selected parts of it.

Speculative implications note: `notes/access_emergence_philosophy.md`.
Darwinian/no-hair working note: `notes/darwinian_no_hair_split.md`.
External review memo: `notes/constrained_access_review_memo.md`.

Role in the notes:

```text
This file is the taxonomy and diagnostics hub.
`darwinian_no_hair_split.md` contains the public-center/private-block
theorem work.
`access_emergence_philosophy.md` contains the broader emergence and
geometry-above-the-cut speculation.
```

Anchors:

- Ollivier-Poulin-Zurek, "Environment as a Witness":
  https://arxiv.org/abs/quant-ph/0408125
- Zurek, "Quantum Darwinism":
  https://arxiv.org/abs/0903.5082
- Donnelly-Freidel, local subsystems in gauge theory/gravity:
  https://arxiv.org/abs/1601.04744
- Witten, "Gravity and the crossed product":
  https://arxiv.org/abs/2112.12828
- Raju, "Lessons from the information paradox":
  https://arxiv.org/abs/2012.05770

## 1. Definition-level object

A constrained access channel is not just a quantum channel.  It is a
triple

```text
(finite sector H_code, accessible algebra A(t), protocol class P)
```

plus a record map into whatever an observer can actually collect.

The central question is:

```text
Which information about H_code is recoverable/distinguishable from A(t)
under protocols P, at what latency and complexity?
```

This separates three statements that are often blurred:

1. information exists in the global state;
2. information is present in a mathematical complement/algebra;
3. information is operationally accessible to a specified observer,
   with a specified record, time, and complexity budget.

## 2. Diagnostics

Useful quantities:

1. **Distinguishability.**

```text
D_A(t; psi, phi) = sup_{O in A(t), ||O|| <= 1}
                  | <psi|O|psi> - <phi|O|phi> | .
```

This is the right language for constraint/Gauss questions, where
reduced density matrices may not be the natural object.

2. **Recoverability.**

```text
F_A(t; D) = best entanglement fidelity for recovering diary D
           from A(t) and allowed side information.
```

This is the Hayden-Preskill / Page / island language.

3. **Participation.**

```text
N_eff(A) = (Tr W_A)^2 / Tr W_A^2
```

where `W_A` is the Gram kernel of the operators in the coupling/access
algebra in the relevant shell or code subspace.

4. **Redundancy.**

For a record split into fragments `E_i`, define a Darwinism-style
redundancy:

```text
R_delta(X) = number of disjoint fragments carrying (1-delta)
             of the accessible information about observable X.
```

This distinguishes broadcast classical information from cryptographic
quantum information.

5. **Complexity.**

The algebra may contain an operator in principle while the decoder is
computationally inaccessible.  Complexity is not optional in black-hole
applications.

## 3. Access profile template

The useful classification object is an access profile.  For any proposed
horizon, reservoir, measurement environment, or holographic model, ask
the following questions:

```text
finite sector:
    What finite code/entropy sector is being probed?

public algebra:
    Which observables are redundantly accessible from small records?

private residue:
    Which observables remain decoupled from small records?

record geometry:
    What does the passive record resolve, compress, or anonymize?

recovery law:
    When, how fast, and from what enlarged algebra does private
    information become recoverable?

protocol class:
    Is the observer using passive records, active mining, boundary
    access, dressed/Gauss-law observables, or full microscopic access?

record addressability:
    Does the record identify microscopic source cells, only coarse
    sectors, or no source address at all?

source-symmetry:
    Do repeated record statistics remain insensitive to microscopic
    source addresses, or only the elementary record labels?

bandwidth/compression:
    How many resolvable record degrees are available per coherence time?

saturation:
    Does the source-side access algebra participate at order the full
    entropy, or only a boundary/contact subextensive part?

complexity:
    Is the relevant decoder feasible, or only algebraically present?
```

In finite-dimensional algebraic language, the basic model is

```tex
\mathcal A_{\rm code}
=
\bigoplus_x \mathcal B(\mathcal H_x),
\qquad
Z(\mathcal A_{\rm code})
=
\bigoplus_x \mathbb C P_x .
```

The public algebra is the center `Z(A_code)`: the pointer/no-hair labels
`x`.  The private residue is the noncommutative block algebra
`B(H_x)` inside each sector.  The active theorem pass in
`notes/darwinian_no_hair_split.md` states this as: the passive record
broadcasts the center and hides the blocks until the access algebra is
enlarged.

These questions are independent.  A system can have public pointer
records without fast diary recovery, thermal records without a finite
sector, or eventual recovery through a record that is not anonymous.
Horizon-class behavior is the particular profile in which no-hair data
are public, microscopic data are private to small fragments, the passive
record is record-label anonymous and source-symmetry anonymous,
bandwidth is compressed, source-side access is saturated, and the
private residue is recoverable from a delayed/global access algebra at
horizon latency within the relevant complexity regime.

## 3.5 Pre-sharp-turn machinery map

The earlier black-hole/dS program already separates several properties
that should not be bundled.

| access-profile property | earlier source/result | lesson |
| --- | --- | --- |
| finite sector | Schwarzschild/dS state-count inputs | defines the code entropy whose access is at issue |
| source-side saturation | Gram-kernel participation `N_eff`; luminosity lemma; dS horizon-register contrast | source participation is an intrinsic model-side invariant, not an emitted-mode count |
| passive record compression | `TR=O(1)`, Bekenstein-Mayo/Pendry channel-capacity layer | one-wavelength horizons have few resolvable radiation modes per coherence time |
| record addressability/anonymity | collective-jump lemma; `b^\dagger_{\omega\lambda}` carries no `mu`; ETH/randomness for source-symmetry | Hawking labels do not carry microscopic source addresses; statistics require a symmetry/typicality condition |
| flux-measurement obstruction | HBT/flux moments see radiation-mode participation, not source Gram-kernel participation | instantaneous spectra are the wrong exterior certificate for source saturation |
| recovery latency | boundary-saturation latency lemma; HP import; LR bath bound | access to private blocks is temporal/global, logarithmic for horizon-class, power-law for local reservoirs |
| mixing/routing | thermal-tie discussion; forced-mixing correction; anonymity alternatives | compression plus unitarity gives serialization; fast recovery of arbitrary deposits requires routing or nonlocal access |
| complexity | Harlow-Hayden/Python's-lunch layer | algebraic recoverability and feasible decoding must remain separate |
| constraint/dressed access | Raju/HoI and dS Stage B notes | changing the allowed algebra can bypass factorized passive-record conclusions |

This map is the main reason the access profile should keep `anonymous`,
`compressed`, `saturated`, `recoverable`, `low-latency`, and
`low-complexity` distinct.  The pre-turn work found examples where these
properties separate.

## 4. Quantum Darwinism as the prototype

Quantum Darwinism studies a system `S` monitored by an environment `E`.
Observers do not access `S` directly.  They access fragments of `E`.
Only selected pointer observables of `S` are redundantly recorded across
many fragments.  Fine quantum information is generally not available in
small fragments; it remains in global correlations.

Translation:

```text
system          -> finite sector / horizon sector
environment     -> radiation / exterior record
pointer data    -> no-hair observables
global phases   -> microscopic diary/microstate information
fragments       -> finite pieces of the radiation record
redundancy      -> classical objectivity/macroscopic observability
```

The horizon channel is Darwinian for no-hair data and non-Darwinian for
microscopic quantum data:

- mass, charge, angular momentum, temperature are redundantly visible;
- a newly thrown-in diary is recoverable only from sufficiently large
  radiation algebras and a hard decoder;
- small fragments look thermal and carry only coarse records.

Candidate slogan, for internal use:

> Horizons broadcast classical no-hair data but encrypt quantum diary
> data in nonlocal correlations.

This is a property of the access channel, not a claim about collapse.

### Relation to constrained anonymous access

Quantum Darwinism is the prototype for one layer of the access profile:

```text
redundant fragments select a public commuting algebra.
```

Constrained anonymous access is the larger object.  It asks not only
which facts become public, but also which degrees remain private, what
the record reveals about microscopic source addresses, when the private
information becomes recoverable, and what latency and complexity that
recovery requires.

Useful separation:

```text
Quantum Darwinism:
    public pointer algebra from redundant records.

Constrained anonymous access:
    public pointer algebra
    + private block residue
    + record-label and source-symmetry anonymous compressed records
    + source-side participation/saturation
    + delayed or enlarged-algebra recovery
    + latency and complexity budgets.
```

Thus the right question is not whether a horizon is "just Quantum
Darwinism."  The right question is which extra access-profile
properties must be added to Darwinian public records to obtain
horizon-class behavior.

## 5. Heisenberg cut version

The ordinary Heisenberg cut separates "system" from "apparatus/record."
In standard measurement theory the placement of the cut is partly a
modeling convention: include more apparatus quantum-mechanically and
the cut moves.

A horizon is a physically constrained cut:

```text
observer algebra outside / complementary quantum sector inside.
```

The cut can still move, but only by changing the access algebra:

- collect old radiation: Page/Hayden-Preskill cut shift;
- include an island: algebraic reconstruction cut shift;
- lower mining apparatus: active access cut shift;
- use boundary CFT: holographic access cut;
- include Gauss-law dressings: nonfactorizing access cut.

This may be the right conceptual equivalence:

> A finite horizon is a thermodynamic Heisenberg cut whose pointer
> observables are no-hair data and whose quantum residue is accessible
> only through large, delayed, or nonlocal exterior algebras.

Again: not collapse.  The cut is an access distinction.

## 6. Gauge constraints and gravity

Gauge theories already show that access is algebraic, not tensor-factor
naive.  Gauss constraints tie regions through boundary fluxes.  To make
subsystems one chooses centers, edge modes, dressings, or extended
Hilbert spaces.  Gravity intensifies this: diffeomorphism-invariant
operators require relational or asymptotic dressing.

In the constrained-access language:

```text
Gauss law changes A(t), not just the state.
```

This is the clean relationship to Raju/holography of information:

- factorized Hayden-Preskill branch: interior information reaches the
  exterior record after scrambling/emission;
- constraint access branch: the exterior algebra already contains
  dressed nonlocal information about the would-be interior.

The right comparison is not "is the reduced density matrix outside
different?"  It is:

```text
sup over allowed dressed observables of distinguishability,
with latency and complexity budgets.
```

This matches the `ds_operational_horizon.md` Stage B direction.

## 7. Horizons as constrained access channels

For a passive nonextremal no-hair horizon, the access profile is:

```text
finite sector:
    Bekenstein-Hawking / microcanonical horizon sector.

public algebra:
    no-hair, thermodynamic, and conserved labels:
    mass/temperature bins, charge, angular momentum.

private residue:
    diary information and microscopic degeneracy inside a fixed
    no-hair sector.

record geometry:
    collective, compressed Hawking record; records carry
    frequency/channel/time-bin data but no microscopic source address,
    with source-symmetry anonymity supplied by ETH/randomness or
    symmetry of the source-to-mode map.

recovery law:
    Page/HP recovery from a sufficiently large delayed radiation
    algebra plus side information; horizon-class when the source-side
    access is saturated and the emitted-record latency is logarithmic.
```

This is stronger than saying "there is a horizon."  It is a statement
about which observables become public records, which remain hidden in
global correlations, and what it costs to recover them.

## 8. Witness profiles

The template separates systems that otherwise sound similar.  The
detailed theorem stress test lives in `darwinian_no_hair_split.md`; this
table is only the taxonomy-level version.  The canonical review matrix
is in `notes/constrained_access_review_memo.md`.

| system | finite sector | public algebra | private residue | record geometry | recovery law |
| --- | --- | --- | --- | --- | --- |
| ordinary Darwinian environment | yes, for the monitored system | pointer observable redundantly recorded | generic quantum information remains in global correlations | fragments can be many and local to the environment | no generic Page/HP diary recovery |
| ordinary local reservoir with surface contact | yes | surface/contact observables | bulk information away from contact | record resolves the contact, not the whole volume | transport-limited; power-law latency |
| Rindler wedge | no finite unregulated horizon sector | modular/thermal observables for wedge algebra | no finite Page-style diary sector | local thermal-cell record, regulator dependent | no finite Page/HP recovery law without extra structure |
| tape emitter | yes | time/address record can reveal readout order | not private once its turn arrives | serial but source-addressed by time bin | eventual recovery; no fast anonymous access |
| horizon-class channel | yes | no-hair/thermodynamic labels | diary/microstate data inside fixed no-hair sector | collective, compressed, anonymous passive record | delayed/global Page/HP recovery; logarithmic latency when saturated and mixed |
| constraint-dressed gravity access | yes, model dependent | asymptotic charges and dressed observables | depends on allowed dressed algebra and complexity | record/algebra is nonfactorizing rather than source-local | distinguished by dressed-observable distinguishability with latency/complexity budgets |

The table is a diagnostic, not a taxonomy of spacetimes.  Changing the
allowed protocol class changes the row: passive Hawking collection,
active mining, boundary-CFT access, and Gauss-law dressed access are
different access profiles.

## 8.5 Definition audit: split horizon-profile properties

The pre-sharp-turn work shows that several horizon-flavored words hide
independent properties.  Use the following definitions before claiming a
system is horizon-class.

```text
source-anonymous:
    record-label anonymity means passive labels do not identify
    microscopic source cells.  Source-symmetry anonymity further means
    repeated record statistics do not reconstruct those addresses.
    Records may still identify coarse/no-hair sectors.

bandwidth-compressed:
    resolvable record degrees per coherence time are parametrically
    smaller than the source-side participation.

source-saturated:
    the physically normalized source-side Gram-kernel participation
    N_eff scales like the full finite entropy of the sector.

block-recoverable:
    an enlarged/delayed access algebra can reconstruct the
    noncommutative block information.

low-latency:
    arbitrary k-sized deposits become recoverable in O(k + log S)
    emitted records, or the appropriate horizon-class analogue.

complexity-disciplined:
    recoverability is tagged by decoder complexity: feasible,
    high-complexity, or conditional on Harlow-Hayden/Python's-lunch
    assumptions.

protocol-qualified:
    the access profile states whether the observer uses passive records,
    active mining, boundary access, dressed/Gauss-law observables, or
    full microscopic access.
```

These properties are logically independent enough that the table should
not merge them into a single "record geometry" or "recovery" column.

Expanded witness table:

| system/profile | public center | private blocks | passive? | source-anonymous | compressed | saturated | block recovery | low latency | complexity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ordinary Darwinian environment | yes | usually for nonpointer data | yes | no generic source notion | no generic | no generic | no generic | no | usually easy pointer readout |
| erasure/QEC code | optional | yes below threshold | protocol-dependent | no generic | no generic | no generic | yes from authorized regions | code-dependent | decoder-dependent |
| tape emitter | optional/addressed | no once slot is read | yes | no, timing is address | yes, serial | can be extensive over cycle | eventual | no for arbitrary deposits | easy if schedule known |
| local reservoir with surface contact | surface/macroscopic | bulk private until transport | yes | contact-local, not anonymous | no/thermal-cell dependent | no, N_eff ~ S^{(d-1)/d} | eventual | power-law | protocol-dependent |
| saturated slow-router | optional | yes for remote deposits | yes | possible | possible | yes, N_eff ~ S | eventual | no | can be easy after wait |
| nonlocal anonymous encoder | optional | not necessarily | yes/passive map | yes | possible | possible | possible | possible | hidden in nonlocal map |
| Rindler wedge | thermal/modular | no finite block story | yes | not source-cell based | local thermal-cell density | no finite S | no Page/HP law | no finite law | regulator-dependent |
| horizon-class passive channel | no-hair center | yes inside fixed no-hair sector | yes | yes | serial or thermal-cell compressed | yes | yes by Page/HP/enlarged algebra | yes, if mixed/saturated | HH/Python conditional |
| constraint-dressed gravity access | charges/dressed center | depends on dressed algebra | no, algebra changed | bypasses source-local notion | not passive-record limited | model-dependent | possible | complexity-budgeted | central diagnostic |

The key separation lessons:

```text
public center != horizon
block recovery != horizon
compression != mixing
saturation != low latency
anonymity != source locality
passive access != dressed/Gauss-law access
algebraic recoverability != feasible decoding
```

## 9. Relation to the previous notes

Boundary saturation becomes:

```text
the passive access algebra has participation of order the finite entropy.
```

Flux compression becomes:

```text
instantaneous radiation fragments see Gamma = C W C^\dagger,
not the full access kernel W.
```

Latency becomes:

```text
the time/record count for the access algebra to recover arbitrary new
diaries.
```

Anonymity alternatives become:

```text
compressed anonymous access with fast recovery requires either
internal routing or a nonlocal/constraint-dressed access algebra.
```

Quantum Darwinism adds:

```text
coarse no-hair observables can be redundantly broadcast even while
fine quantum information is hidden in nonlocal correlations.
```

This is the first place the Heisenberg-cut analogy becomes technically
useful: a cut is defined by access, and a horizon is a constrained,
thermodynamic, observer-dependent cut.

## 10. Potential results

1. **Darwinian/no-hair split.**

Formalize a channel where conserved/no-hair observables have high
fragment redundancy while generic diary observables have near-zero
fragment accessibility below the HP threshold.  Current working note:
`notes/darwinian_no_hair_split.md`.  Active theorem pass: use
record-signature leakage for the public no-hair layer, sectorwise
decoupling for the private diary layer, and boundary-saturation latency
to distinguish the horizon-class channel from ordinary Darwinian
decoherence.

2. **Access-cut movement.**

Show how Page recovery, islands, mining, and Gauss-law dressing are all
operations that enlarge or change `A(t)`, and therefore move the
operational cut.

3. **Constraint-vs-scrambling fork.**

Make the alternatives theorem algebraic:

```text
fast access = fast operator growth into A(t)
              OR A(t) was nonlocal/constraint-dressed already.
```

4. **Quantum Darwinism contrast.**

Prove that ordinary Darwinian environments broadcast pointer data
redundantly but do not generically provide low-latency quantum diary
recovery.  Black-hole horizons combine Darwinian no-hair broadcasting
with cryptographic fine-grained recovery.

Sharper form:

```text
Quantum Darwinism gives the public-center layer.
Horizon-class constrained access adds:
    private-block decoupling,
    anonymous compressed passive records,
    source-side saturation,
    enlarged-algebra recovery,
    latency and complexity discipline.
```

The associated theorem target is an upgrade/separation result: identify
which added properties are needed to pass from redundant public records
to the horizon-class profile, and give witnesses showing that the
properties separate.

5. **Access algebra taxonomy.**

Classify passive Hawking radiation, specified bath coupling, active
mining, boundary CFT access, and Gauss-law access by the same
distinguishability/recoverability functions.

## 11. Where this could lead

The larger conceptual statement is:

> The black-hole information problem is a constrained-access problem:
> which observer algebra has access to which finite-sector information,
> how redundantly, how fast, and at what complexity?

This is broader than boundary saturation and more concrete than
"holography is QEC."  It adds the measurement-theory split:

```text
public classical records = redundant no-hair data,
private quantum residue = globally encoded microscopic information,
cut movement = change of access algebra.
```

The risk is that the analogy becomes poetic.  The antidote is to keep
the diagnostics explicit: distinguishability, recoverability,
participation, redundancy, latency, and complexity.

## 12. First access-locality diagnostic

If locality is to emerge above the cut, the first object is not a
metric.  It is an access relation among public centers.

Let the public algebra decompose into center labels or records
`X_i`, with projectors or classical observables in
`Z(A_code)`.  For fragments/protocols available to an observer, define
several relations:

```text
redundancy overlap O(i,j):
    how many record fragments redundantly carry both X_i and X_j;

predictability P(i,j):
    how well records of X_i predict records of X_j;

directed latency T(i -> j):
    minimum record depth/time/protocol cost before information injected
    near X_i is distinguishable or recoverable near X_j;

recovery reach R_k(i -> j):
    whether a k-sized diary associated with i becomes recoverable from
    the access algebra associated with j within a specified budget.
```

An access distance, if it exists, should be derived from these:

```text
d_access(i,j) = monotone function of latency, redundancy decay,
                or recovery cost.
```

The diagnostic must be tested before geometry language is trusted:

1. Does `d_access` separate nearby and far records in an ordinary local
   reservoir?
2. Does it fail or become regulator-dependent for Rindler without a
   finite sector?
3. Does it distinguish a tape emitter from a scrambler with the same
   final unitary release?
4. Does it give a compressed/anonymous relation for horizon-class
   passive radiation?
5. Does it remain stable under changes of observer fragments and
   low-complexity decoding?

Only if these tests behave sensibly should one ask whether the access
relation has metric properties, effective dimension, or causal cones.
