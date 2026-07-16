# Capacity, Metadata, and Deadline Questions for Evaporation Completions

Date: 2026-07-11

Status: historical conjecture and kill register. Parent framework:
`evaporation_completion_problem_2026_07_11.md`. The distinctions and closure
tests remain part of the technical audit trail, but this file is no longer an
active research queue after the program endpoint recorded in
`program_endpoint_and_standalone_results_2026_07_13.md`.

This version supersedes the thesis role of the earlier channel/code framing.
It contains no new theorem. It records which attractive conjectures survived
stress testing, which failed, and what a valid replacement would require.

## 0. Corrections on Record

The following distinctions are load bearing:

```text
coarse carrier parameters are not a complete quantum channel;
microscopic evaporation dynamics is not an exogenously chosen code;
different information fates require different full accessible processes,
  not merely different dilations of one fixed process;
eventual information destination is not Page-time recoverability;
number of emitted quanta is not quantum capacity;
greybody transmissivity is not automatically diary-to-radiation
  transmissivity;
constraint-forced charge metadata is not arbitrary private payload;
one long nonstationary history is not the same as either one sample or an
  unlimited IID ensemble.
```

Four claims from the first conjecture pass were changed materially:

```text
original C1, greybody antidegradability:
  REPLACED. It applied a carrier-scattering capacity to the wrong input-output
  map and used an exact pure-loss result where thermal-loss capacity is
  generally known only through bounds.

original C2, universal nonzero dressing defect:
  SPLIT. Charge-varying states force metadata; fixed-charge private states can
  remain perturbatively indistinguishable outside their region.

original C3, typicality-free Page-point onset:
  KILLED for a small diary by a delayed-release completion. Dimension/no-
  hiding gives a diary-size capacity cut, not a universal Page deadline.

original C4, all rate properties require ensembles:
  NARROWED. A long trajectory can estimate rates; the live issue is estimation
  under drift, finite stationarity windows, and no repeated preparation.
```

## 1. Common Setup

At evaporation step `j`, let

```text
V_j : B_j -> B_(j+1) tensor R_j tensor P_j              (1.1)
```

be the physical isometry, with `R_j` the candidate exterior record and `P_j`
hidden partner/edge/archive data. Let `D` be a `d_D`-dimensional diary code in
the initial shell, purified by reference `Q`. Let `A_R(K)` be the accessible
algebra on records through step `K`.

Three channels must not be conflated:

```text
carrier-scattering channel:
  exterior incoming mode -> exterior outgoing mode;

one-record diary channel:
  D -> accessible algebra of one emitted record, conditional on its reachable
  history and declared side information;

full diary process:
  D -> A_R(K), including multitime correlations and process memory. (1.2)
```

Greybody factors directly constrain the first. Information export concerns the
second and third.

## C1. Local-to-Temporal Information

### Established finite control

The integrated coded emitter has exactly diary-independent one- and two-record
marginals while three records recover a logical qubit:

```text
I(Q:R_j) = 0,
I(Q:R_j R_k) = 0,
I(Q:R_j R_k R_l) = 2 log 2.                              (C1.1)
```

Thus positive full-process information can reside entirely in multitime
correlations even when every local carrier is thermal and diary blind. This is
an exact model statement, not a black-hole claim.

### Conjecture C1

For a physical black-hole completion, semiclassical local indistinguishability
may coexist with positive coherent information of the full radiation process:

```text
for every resolved one-wavepacket diary channel N_j,
  ||N_j-C_j||_diamond <= epsilon_local;

but for a sufficiently large multitime record,
  the daughter/hidden complement decouples from Q and D is recoverable. (C1.2)
```

The content is not that the process "beats" a fixed memoryless channel. It is
that the memoryless local marginals are incomplete projections of a process
whose correlations carry the payload.

### Test

For a named completion:

```text
fix a diary code and accessible algebra;
bound each one-record diary channel against a constant channel;
compute two- and higher-record conditional mutual/coherent information;
compute direct diary decoupling from the daughter and all hidden outputs;
compare with a blind completion having the same local marginals.       (C1.3)
```

### Kill or weaken

```text
If one-wavepacket diary dependence is order one, the information is not purely
correlation-only; retain a quantitative local/multitime split.

If the full process has no positive coherent information, the completion does
not export the diary despite its Hawking-like local carriers.
```

### Quarantined greybody subproblem

Pure-loss bosonic antidegradability at transmissivity at most one half is a
valid carrier-channel fact. It constrains diary export only after a physical
internal-emission-to-exterior factorization has been derived. Thermal-loss
quantum capacity is generally a bounds problem, and conventions must specify
whether `gamma` is absorption, reflection, or internal-mode escape.

Do not use a greybody lookup alone as a microstate-capacity theorem.

## C2. Constraint Metadata Versus Fixed-Charge Payload

Let the diary algebra decompose into exact asymptotic charge sectors:

```text
A_D = direct_sum_q B(H_q),
Z(A_D) = span{P_q}.                                      (C2.1)
```

This makes the header/payload distinction algebraic rather than metaphorical:

```text
header:
  the commuting center generated by energy, momentum, angular momentum,
  gauge charge, and other declared asymptotic sectors;

payload:
  noncommuting private degrees of freedom inside a fixed sector H_q. (C2.2)
```

### C2a. Charge-header target

If diary alternatives differ in exact total charges, gravitational or gauge
constraints should force corresponding exterior distinguishability. The target
is a quantitative lower bound on accessible information about `q`, not a bound
on arbitrary private-state recovery.

Candidate observables:

```text
Holevo information of the charge ensemble in the asymptotic algebra;
trace/strategy distance between different-charge record processes;
time and precision required to resolve a charge difference;
accumulated Q2 defect relative to a comparison process blind to q.    (C2.3)
```

### C2b. Fixed-charge payload conjecture

Within one exact charge sector, constraints and perturbative dressing alone do
not generically force recovery-grade access to an arbitrary diary:

```text
same q, different private states
  => charge header identical;
  payload access requires additional dynamics or a stronger nonperturbative
     algebraic principle.                                      (C2.4)
```

Perturbative gravitational-splitting constructions support the possibility
that exterior observables depend only on total Poincare charges. The strong
holography-of-information alternative is precisely that this fixed-charge
privacy fails nonperturbatively or in the correct asymptotic algebra.

The two-arm implementation specification is recorded in
`dressed_pump_header_payload_spec.md`. The July 12 literature pass changes its
status: perturbative gravitational splitting already supplies the static core
of the comparison. Different total charges are asymptotically visible, while
fixed-charge private subspaces can remain exterior-indistinguishable at leading
order. A generic pump cannot adjudicate the nonperturbative disagreement with
strong holography-of-information claims because its observable algebra would
encode the answer by construction. The two arms are retained as a test to apply
inside a named gravitational algebra, not as a standalone simulation target.

### Test

The dressed-pump calculation must contain two separate diary encodings:

```text
arm H, header:
  alternatives have different energy/charge and therefore different dressing;

arm P, payload:
  orthogonal diary states are exactly degenerate in all declared charges.
                                                               (C2.5)
```

For both arms compute local distinguishability, cumulative process defect, and
direct recoverability. Their difference isolates forced metadata from private
payload leakage.

### Kill or branch

```text
If arm H is exactly invisible in the correct asymptotic algebra, the dressing
or charge-resolution model is inadequate.

If arm P is recovery-grade without emission-relative mixing, C2b is false and
the stronger nonperturbative access principle becomes the result target.

If arm P is exactly blind, that does not invalidate dressing; it supports the
fixed-charge private-block branch.
```

No `log S` metadata floor is claimed until the distinguishable charge alphabet,
resolution, and observation budget yield it explicitly.

## C3. Capacity Cuts and Information Deadlines

### C3a. Exact capacity cut already established

If the accessible exterior channel through step `K` is exactly constant on a
`d_D`-dimensional diary, the complementary daughter-plus-hidden output must
contain a reversible copy. Hence

```text
d_(B_K) d_(P_hidden,K) >= d_D.                            (C3.1)
```

For a diary equal to the entire initial shell, telescoping this condition gives
the existing archive bound. For a small diary, (C3.1) permits the daughter to
retain it until very late.

### Counterexample to a universal Page deadline

Take

```text
B_0 = D tensor A_1 tensor ... tensor A_n.                 (C3.2)
```

Emit the `A_j` registers sequentially while retaining `D` unchanged in the
daughter, and emit `D` only at the final step. This completion is unitary,
shrinks, and needs no hidden archive. The radiation can cross the usual Page
dimension point while remaining exactly blind to the selected diary.

Therefore:

```text
unitarity + shrinkage + no hidden archive
  does not force Page-time access to every small diary.   (C3.3)
```

### C3b. Approximate capacity cut — closed as a standard lemma

The audit is recorded in
`approximate_capacity_cut_audit.md`. For a full `d_D`-dimensional code and a
pure completion whose complete hidden complement has dimension
`x=d_(B_K)d_(P_hidden,K)`, the Schmidt-rank argument gives, for `x<d_D`,

```text
inf_(C_K diary blind) ||N_K-C_K||_diamond
  >= 2 (1 - sqrt[x/d_D]).                              (C3.4)
```

This is a direct finite-dimensional information--disturbance/capacity cut,
not a new black-hole theorem. It must be stated with the code, complete hidden
complement, and norm. It does not imply a Page-time deadline for small
protected diaries, and it does not apply unchanged to a restricted reachable
state family.

The original target was:

```text
inf_(C_K diary blind) ||N_K-C_K||
  >= F(d_D, d_(B_K), d_(P_hidden,K), error criterion).    (C3.4)
```

### C3c. Uniform-access deadline conjecture

A Page-scale or earlier deadline may become valid only after adding a
uniformity condition such as:

```text
no protected private subsystem of dimension d_D survives in B_K;
the claim is uniform over all d_D-dimensional diary embeddings;
the emission-process algebra acts approximately irreducibly on the shell;
or a declared average over shell-typical diaries replaces worst case. (C3.5)
```

Under one explicit condition, ask when all private directions must acquire
order-one cumulative access. This is a completion-selection conjecture, not a
typicality-free consequence of dimension counting.

### Kill

Any completion satisfying the declared uniformity condition while retaining a
diary-blind protected direction past the proposed deadline kills that version.
Do not move the condition after seeing the counterexample.

## C4. Nonstationary Single-History Identification

A single evaporation history contains many emission events and can estimate
some rates. The obstruction is not "one codeword implies no rates." It is that
the process drifts while the observer accumulates the samples needed for a
specified precision.

### Conjecture C4

For a declared completion property `theta`, observation protocol, and local
stationarity window, there is a minimax tradeoff

```text
estimation error(theta)
  >= G(number of usable events,
       parameter drift,
       backreaction budget,
       detector access,
       model class).                                     (C4.1)
```

For entropy-sensitive full-rank properties, the required event count may drive
an order-one mass change before the target precision is reached. The existing
time-budget result is one class-specific instance, not yet a universal theorem.

### Test

```text
specify the observable distribution and parameter class;
derive a two-point or packing lower bound for estimation;
include the changing mass/temperature in the likelihood;
compare adaptive local-window estimation with a naive stationary estimator;
identify which properties remain estimable from O(S) events.          (C4.2)
```

### Ensemble branch

Black-hole populations can improve estimation of coarse class-relative
parameters only after accounting for heterogeneity in mass, spin, environment,
initial state, selection, and detector response. They are not automatically IID
copies of one microscopic completion and do not by themselves identify private
routing.

## 5. Completion-Selection Mechanisms

Keep necessary classifiers separate from sufficient selectors.

```text
necessary constraints and obstructions:
  shell shrinkage/no-hiding capacity cuts;
  gauge/gravitational charge metadata;
  locality and routing bounds;
  anonymity/permutation-covariance alternatives;
  conservation-law protected sectors;

sufficient export mechanisms:
  emission-relative irreducibility plus quantitative mixing;
  physical jump-process ETH/design moments;
  direct complementary-channel decoupling;
  a model-specific theorem implying one of the above;

model calculations:
  gauge-invariant transition/process data in Matrix/BFSS or another named
  microscopic emitter.                                   (5.1)
```

Anonymity can classify routing versus nonlocal/dressed access. It does not by
itself replace ETH/design or prove decoupling: a permutation-symmetric
collective-charge channel can retain large private blocks forever.

## 6. Task Order

```text
1. C3b approximate capacity-cut audit: CLOSED.
   The full-code diamond-norm lemma is recorded separately; do not present it
   as a new black-hole theorem or silently extend it to restricted families.

2. C2 two-arm dressed-pump: LITERATURE-LOCATED; GENERIC SIMULATION PAUSED.
   Perturbative dressing forces the charge header but not arbitrary
   fixed-charge payload access. Reopen only inside a derived gravitational
   algebra with actual emission dynamics; see
   `evaporation_framework_comparison_map_2026_07_12.md`.

3. C1 local-to-temporal observable package: DESIGNED.
   The exact control and physical-emitter observables are consolidated in
   `local_to_temporal_observable_package.md`.

4. C4 minimax formulation:
   proceed only for a live certificate and declared nonstationary model class.

5. Model application:
   return to BFSS or another emitter only after one target above is both
   nontrivial and independently computable without full process tomography.
```

## 7. Literature and Ownership Gates

Before external use, audit:

```text
quantum memory channels and correlation-only capacity;
approximate privacy/correctability dimension bounds;
gravitational splitting and fixed-charge dressed observables;
nonstationary quantum-process estimation;
black-hole capacity claims using greybody channels;
finite-blocklength evaporation or Page-onset bounds without typicality.
```

Known primary anchors already identified:

- Wolf--Perez-Garcia--Giedke, quantum capacities of pure-loss bosonic
  channels: <https://arxiv.org/abs/quant-ph/0606132>.
- Rosati--Mari--Giovannetti, bounds for thermal attenuator capacity:
  <https://arxiv.org/abs/1801.04731>.
- Bradler--Adami, capacities of specified particle/horizon black-hole
  channels: <https://arxiv.org/abs/1310.7914>.
- Donnelly--Giddings and Giddings, perturbative gravitational splitting and
  charge-only asymptotic distinguishability:
  <https://arxiv.org/abs/1805.11095>,
  <https://arxiv.org/abs/1903.06160>.

These anchors do not establish C1--C4. They delimit what must not be claimed as
new and which conjectures are physically coherent.

## 8. Discipline

- Every statement is relative to a diary code, accessible algebra, completion
  family, data class, and error criterion.
- Never infer diary capacity directly from a greybody coefficient.
- Always compare charge-varying and fixed-charge diary codes in a dressing
  argument.
- Never claim a Page-time deadline from dimension counting alone.
- Treat one-history limits as nonstationary estimation problems, not slogans
  about one codeword.
- Distinguish necessary access, sufficient decoupling, and final recovery.
- Kill a conjecture when its preregistered counterexample appears; do not rescue
  it by silently strengthening the assumptions.
