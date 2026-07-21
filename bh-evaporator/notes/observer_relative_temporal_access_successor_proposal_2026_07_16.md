# Observer-Relative Temporal Access in Constrained Quantum Systems

Date: 2026-07-16

Status: corrected successor proposal, with **WP0--WP2 completed** in
`dssyk_wp0_protocol_and_overlap_2026_07_16.md` and
`dssyk_wp1_formal_controls_2026_07_16.md`. This is a new program built from
results A--D, not an unfinished obligation of the completed evaporation
program. It supersedes the `rho_DSSYK(E)^2` kinematics and the
three-dimensional matched null proposed in
`dssyk_comb_and_factorized_null_2026_07_16.md`. The WP2 clock-instrument and
detector-resource gates are complete in
`dssyk_wp2_clock_resource_gate_2026_07_20.md` and
`dssyk_detector_backreaction_resource_audit_2026_07_20.md`. A clock state plus
a chosen covariant POVM fixes one-read statistics, not a multitime instrument.
Narovlansky--Verlinde do supply a constraint-preserving model detector contact,
but the checked bulk constructions supply no law pricing its normalization,
duration, repetition count, or retained memory. Every declared completion
still transports exactly to the isospectral one-copy model. The external-facing
result is extracted in `paper_dssyk_observer_access/main.tex`.

## Decision in one paragraph

The successor proved worthwhile, but its result is a demarcation rather than a
positive identification of the cosmological constant with a UV regulator. The
test held the physical spectrum and diary code fixed and asked whether the
positive-cosmological-constant-inspired constraint selected different
*temporal information access* from an isospectral one-copy description. It did
not: the constraint, relational algebra, scaling-operator family, clock state,
and available correlators do not by themselves select a multitime instrument
and a resource law, while every declared protocol transports isometrically.
DSSYK is therefore a flagship portability test for the observer-access
framework, not the premise or conclusion of a general cutoff claim.

## 1. Reconnecting to the original question

The conversation began with the proposal that a positive cosmological
constant might appear as a UV cutoff in a dual theory. That phrase can mean at
least four different things:

1. a regulator imposed on an otherwise continuum dual field theory;
2. a finite state count or finite-dimensional static-patch Hilbert space;
3. a bounded spectrum, finite radial wall, or finite-cutoff deformation of a
   holographic model;
4. an operational limit on what a finite observer can distinguish, record, or
   recover in a bounded time.

The literature contains versions of the first three, but not a consensus that
`Lambda` is literally a universal UV regulator. Finite-cutoff DSSYK work studies
deformed spectra, thermodynamics, correlators, complexity, entanglement, and
stretched-horizon interpretations. The present program contributes most
cleanly to meaning 4 by identifying what would be needed for the de Sitter
scale to control an observer-relative *process capacity*, rather than inferring
a cutoff from finite entropy or a bounded spectrum alone.

The long-term operational quantity is

```text
C_obs(K, epsilon; P)
  = log of the largest diary code recoverable with error <= epsilon
    by an allowed K-step observer protocol P.             (1.1)
```

Only after this is nontrivial should one ask whether its scaling with
`S_dS`, temperature, and `Lambda` deserves the name "dual UV cutoff."

## 2. How the successor complements the completed results

The completed evaporation program answered a factorized control question and
left four retained results. The successor uses them as instruments:

| completed result | successor role |
| --- | --- |
| A: one ordinary unitary process can realize the thermodynamic and information-return package | Hold spectrum and state count fixed and test the complementary mechanism: a changed observer algebra rather than transported information in a fixed algebra. |
| B: recovery requires cumulative departure from every diary-blind sequential process | Supply the temporal-access metric and recovery converse for a named constrained model. |
| C: static flux, response, and Gaussian correlators do not identify microscopic access | Forbid any conclusion based only on DSSYK entropy or low-point correlators; require a sequential record channel. |
| D: large degeneracy, active source rank, and diary export are independent | Test whether constraint dressing reveals only public metadata, selected diary directions, or a recoverable generic payload. |

This makes the successor the theory-specific implementation of the completed
program's **observable-structure obligation**:

```text
identify the accessible algebra, its sectors and complement,
then derive how private-state differences enter its record over time. (2.1)
```

It does not reopen A--D or make their external readiness conditional on new
DSSYK work.

## 3. Field position and bounded novelty claim

The adjacent fields currently supply separate pieces:

- CLPW and the crossed-product/QRF literature construct observer-relative
  Type-II algebras and entropies.
- Narovlansky--Verlinde construct the doubled equal-energy DSSYK model and
  constraint-preserving dressed correlators.
- Aguilar-Gutierrez derives the relevant symmetry sector and gauge-invariant
  operator algebra in chord space.
- DSSYK observer and finite-cutoff work studies spectral density,
  thermodynamics, correlators, entanglement, complexity, and stretched
  horizons.
- Recent q-Askey DSSYK deformations show explicitly that factor type depends
  on which operators are included, reinforcing the need to separate algebra
  selection from an operational resource rule.
- de Sitter island work studies recovery from collected radiation with
  gravitational backreaction.
- symmetry-constrained Hayden--Preskill work shows that conserved charges can
  delay leakage and leave remnants.
- quantum-reference-frame work studies sequential measurement, retained
  records, and reference backreaction in non-holographic systems.

The completed WP0 bounded scan has not found a work combining all of the
following:

```text
named constrained holographic model
+ natural dressed observer algebra
+ memoryful sequential record channel
+ microscopic diary distinguishability/recovery
+ isospectral control.                                    (3.1)
```

This was the pre-registered niche. The completed gates explain why the
conjunction is absent: a dressed operator family or observer algebra is not yet
a multitime instrument, and an explicit detector contact is not yet a priced
resource class. The resulting contribution is the demarcation itself, not a
claim that constraints, observer dependence, DSSYK algebras, or
symmetry-modified recovery are individually new. Rajgadia--Xu's state-adapted
dressed operators are the closest algebraic near hit located: they restore
access to the purity of a selected KM state, but do not define an equal-energy
shell diary, memoryful record channel, or isospectral recovery control.

## 4. Correct DSSYK kinematics

The doubled Narovlansky--Verlinde model uses two copies with the same disorder
realization. Fix a common symmetry sector with a nondegenerate spectrum.
Physical states obeying `H_L = H_R` are then uniquely paired:

```text
|E_i>_phys = |E_i>_L |E_i>_R,
H_phys |E_i>_phys = E_i |E_i>_phys.                      (4.1)
```

Therefore the physical density of states is the one-copy spectral measure:

```text
rho_phys(E) = rho_DSSYK(E),                              (4.2)
```

up to the declared shell binning. It is not `rho_DSSYK(E)^2`. If an energy has
multiplicity `g_E>1`, the full kernel has multiplicity `g_E^2`; the map below
then selects a declared diagonal paired subspace unless an additional pairing
or gauge fixing is imposed. The one-copy isomorphism is therefore understood
sector by sector or on that declared paired image.

This observation controls the whole project. An unrestricted unitary
identification

```text
W : |E_i> -> |E_i>_L |E_i>_R                            (4.3)
```

preserves unrestricted distinguishability and channel capacity. The
equal-energy constraint cannot create an access difference relative to this
isospectral transported control. Any operational difference must arise from
the *selected protocol class*: which dressed observables,
interventions, memories, and clocks are physically available to the observer.

This yields the formal spine of the program:

> **Isometric no-free-access principle.** Isomorphic physical Hilbert spaces
> with transported states and unrestricted operations have identical recovery
> capacities. A constraint-access advantage is meaningful only relative to a
> physically derived restriction on the observer protocol class.

## 5. The constraint-access trichotomy

For a fixed shell and observer protocol, classify the result as:

1. **Metadata access.** The record reveals only energy, charge, clock, or
   another public label.
2. **Directional access.** Some microscopic diary directions become
   distinguishable, but the channel does not support generic quantum recovery.
3. **Payload access.** A declared diary code becomes recoverable with
   controlled error.

This trichotomy is the main demarcation. Type-II algebra, nonlocal dressing,
nonzero correlators, and nonzero process defect do not by themselves imply
payload access.

## 6. Operational objects

### 6.1 Diary code

For each disorder realization `omega`, choose a microcanonical bin
`I = [E-Delta E/2,E+Delta E/2]` containing many paired eigenstates. Define a
shell-preserving encoder

```text
V_omega : H_D -> span{|E_i,E_i> : E_i in I}.             (6.1)
```

The pre-registered first calculation would have used the binary classical
phase diary fixed in WP0. It was not authorized past the completed WP2 resource
gate, but the code definition remains the correct target for any future
reopening. Its two states have identical energy probabilities and are defined
by energy rank before later observer outcomes. A fixed energy eigenvalue is
generically nondegenerate and cannot carry the code by itself; a multi-level
finite shell is load-bearing. A logical-qubit extension would require a
stronger fixed-header code condition.

### 6.2 Observer protocol

Begin with the explicit NV constraint-preserving scaling-operator contact, not
an arbitrarily chosen element of the full relational matrix algebra. A finite
record model may complete that contact by coupling a record ancilla at time
`tau_j`, while retaining any separately declared observer memory:

```text
U_j = exp[-i g_j O_phys(tau_j) tensor X_(R_j)],
N_K^P : diary code -> R_1 ... R_K.                       (6.2)
```

Equation (6.2) is a candidate instrument completion, not something derived by
NV. The switching profile, coupling normalization `g_j`, probe preparation,
readout, state update, contact schedule, and retained-memory rule remain extra
operational inputs. Standard detector measurement theory can construct the
resulting instrument once those inputs are supplied; it does not select or
price them.

The native physical evolution is generated by `(H_L+H_R)/2`; one DSSYK copy
also supplies the relational-time interpretation. Any additional clock
register must be identified explicitly as detector timing memory rather than
silently adding a second Page--Wootters clock.

### 6.3 Access witnesses

For two code states, begin with record distinguishability:

```text
delta_K(P,omega)
  = (1/2) ||N_K^P(rho_0)-N_K^P(rho_1)||_1.              (6.3)
```

For every diary-blind record channel `C_K`, the triangle inequality gives,
using the full code-restricted diamond norm in `[0,2]`,

```text
||N_K^P-C_K||_(code,diamond) >= delta_K(P,omega).        (6.4)
```

Thus `delta_K` is a lower-bound witness against *all* diary-blind channels and
does not depend on selecting one convenient scrambled comparison.

The full necessary access quantity remains

```text
A_K(P,omega)
  = inf_(C_K diary blind) sum_(j<=K) eta_j,              (6.5)
```

with hybrid-reachable step defects from Result B. Actual recovery is a third,
stronger object: entanglement fidelity or the complementary-system decoupling
error. Use distinct notation for these three quantities.

### 6.4 Disorder

The first route is per realization. Report the mean and variance of
`delta_K(P,omega)` or the recovery quantity. The program's existing
self-averaging note is only a methodological precedent: its Renyi-purity
concentration result does not automatically control a trace-norm supremum,
comb distance, or recovery fidelity. A new concentration argument is required
before replacing per-realization results by an averaged-channel claim.

## 7. Controls

### Primary control: isospectral one-copy DSSYK

Transport the same shell, diary code, and every observer step through the
isometry (4.3). The complete one-copy and doubled record channels are then
exactly equal, as proved in the WP1 no-free-access theorem. This control
preserves the exact physical spectrum and shows that representation and the
constraint alone cannot generate access. A nontrivial comparison requires a
common, independently motivated implementation-cost restriction under which
the one-copy and dressed-simple protocol classes are not exact transports.

### Blind control: same-shell diary twirl

Apply a code twirl before the same observer instrument:

```text
T_D(rho) = average over diary-code unitaries,
C_K^twirl = N_K^P o T_D.                                (7.1)
```

This is an exact same-model diary-blind comparison and supplies a computable
reference for (6.3). It is not an ordinary reservoir.

### Charge control

Use a finite non-Hamiltonian constraint (parity or number) to verify the
metadata-access branch: the public charge can be exposed while generic fixed-
charge payload remains hidden. This is the calibration between an ordinary
symmetry restriction and the Hamiltonian/relational constraint.

### Ordinary local reservoir: secondary interpretation

A three-dimensional finite-range reservoir introduces locality and transport
in addition to factorization. It is therefore not the primary matched null.
Use its Lieb--Robinson or diffusion latency only after the isospectral
constraint comparison yields a nontrivial signal. Exact realization of an
arbitrary DSSYK spectral density by a local reservoir must not be assumed.

## 8. Work packages and gates

### WP0 -- corrected overlap and definitions

Completed in `dssyk_wp0_protocol_and_overlap_2026_07_16.md`:

1. The primary TeX pass fixes NV as the source of the doubled equal-energy
   construction and the Rahman--Susskind line as an independent/competing
   DSSYK--de Sitter scale program.
2. No checked DSSYK work computes a diary-dependent record channel, recovery
   fidelity, process distance, or equivalent quantity.
3. A fixed-rank shell, energy-matched binary phase diary, candidate NV-simple
   detector family, native time, and per-realization disorder rule are
   specified.
4. The protocol gate is conditional because Aguilar-Gutierrez's chord-space
   kinematical relational algebra uses all `B(H_0^S)`, rather than deriving a
   restricted observer instrument.

Deliverable: a self-contained protocol and overlap specification. No dynamics
calculation before it is complete.

### WP1 -- formal and finite controls

Completed in `dssyk_wp1_formal_controls_2026_07_16.md`:

1. Exact isometric transport preserves the full record channel, `delta_K`,
   `A_K`, recovery fidelity, and `C_obs`.
2. The charge control has perfect cross-sector metadata access and exactly
   zero fixed-sector payload access.
3. The same-shell twirled control has `delta_K=0`; for the binary classical
   diary, the actual-to-twirl full diamond norm equals the actual pairwise
   `delta_K`.
4. `sim/dssyk_wp1_controls.py` verifies the finite identities.

Deliverable: a control table showing spectrum, protocol algebra, public
labels, private code, and access witness.

### WP2 -- clock-instrument and detector-resource gates (complete negative verdict)

The clock audit corrects the earlier physical-selection claim. CLPW supply a
lower-bounded clock Hamiltonian and clock states, but no time POVM,
post-measurement instrument, or repeated detector contacts. If one additionally
chooses the canonical covariant time POVM, the one-read overlap is

```text
M_f(omega) = integral dq f(q+omega) f(q)*,                 (8.1)
```

and the maximum-entropy clock state gives the Cauchy completion
`M_f(omega)=exp(-pi R_dS |omega|)`. That kernel matches a tracial two-point
filter; it is not yet a bulk-derived record channel. Fresh/reset, persistent
Naimark-memory, and contact-disturbed instruments can have the same one-read
density and different two-record access. A finite two-contact parity-memory
detector makes the nonuniqueness explicit:

```text
delta_2,persistent = 1,
delta_2,fresh      = |M_f(Delta E)|^2,
delta_2,kicked     = |cos(kappa Delta E)|.                 (8.2)
```

Extending the equal-energy isometry by the identities on clock and detector
memory makes every completed comb exactly identical in one-copy and doubled
DSSYK. The proof, controls, and correction of the earlier common-memory wording
are in `dssyk_wp2_clock_resource_gate_2026_07_20.md`.

The detector follow-up closes the remaining resource-selection question at the
current input. Narovlansky--Verlinde write the constraint-preserving model
contact

```text
S_int = integral d tau [X^+ O^-_phys + X^- O^+_phys].      (8.3)
```

Standard measurement and influence-functional machinery can turn a fully
specified version of this contact into an instrument or process tensor. The
model does not, however, fix its normalization, switching, readout, retained
memory, duration, or repetition count. The Tietto--Verlinde observer-energy cap
alone does not bound the diary-sensitive accumulated action

```text
G_D(T) = integral_0^T dt ||H(t)-H^(0)(t)||,                (8.4)
```

because the cap imposes no contact-normalization condition: in any class that
remains admissible under positive rescaling, the rescaling leaves the free
observer-energy cap unchanged while rescaling `G_D`. The Espindola--Ali
Euclidean metric-susceptibility bound is a useful near hit, but it supplies
neither a Lorentzian CP instrument nor a map to (8.4). This conditional analytic
energy-cap/action-budget nonimplication and the bounded source audit are in
`dssyk_detector_backreaction_resource_audit_2026_07_20.md`.

WP2 deliverable: the clock-state/instrument nonidentifiability proposition,
three exact two-slot controls, the explicit NV contact audit, and the
energy-cap/action-budget nonimplication. Scaling-operator numerics and exact
DSSYK OTOCs are not authorized by the present inputs: they would evaluate a
chosen, unpriced protocol rather than test a constraint-selected resource law.

### WP3 -- conditional scaling and recovery

Status: **not authorized at the current bulk input.** Reopen only if a future
construction supplies a Lorentzian instrument, a retained-memory/backreaction
rule, and a common one-copy/doubled interaction-action, contact, or
implementation-cost bound. If those inputs produce a disorder-stable
microscopic signal not reducible to public labels:

1. extend to larger `K` and diary dimension;
2. estimate `A_K` or bound distance to the full blind-comb class;
3. compute a decoupling/recovery quantity;
4. compare latency to the secondary local-reservoir control;
5. ask whether `C_obs(K,epsilon)` has a meaningful `S_dS` or `Lambda` scaling.

## 9. Stop conditions

Stop or reframe if any of the following occurs:

- the full literature pass finds the same diary-record or recovery quantity;
- the natural DSSYK observer protocol cannot be specified independently of the
  desired answer;
- the diary cannot be encoded without changing the energy/no-hair data being
  compared;
- the result is only a known entropy, correlator, algebra type, or complexity;
- `delta_K` vanishes after public energy/clock labels are matched;
- a signal exists only after unrestricted full-matrix operations are allowed;
- disorder averaging erases the code and no per-realization concentration is
  available;
- the isospectral one-copy control reproduces the same access profile.

The final condition fired exactly in WP1. WP2 further showed that neither the
clock data nor the currently available contact and backreaction inputs define a
non-transportable restricted process class. These are scientifically useful
endpoints: the equal-energy description changes representation, while every
declared operational completion has the same access.

## 10. Claims allowed and prohibited

Allowed from the completed gates:

```text
The equal-energy constraint does not create temporal diary access: every
declared observer protocol and resource rule transports exactly to an
isospectral one-copy description. Current DSSYK and de Sitter observer inputs
do not yet select the Lorentzian multitime instrument and implementation budget
needed to make a stronger operational cutoff claim.
```

Potential later interpretation:

```text
The de Sitter scale bounds an observer-relative process capacity or access
bandwidth in this model.
```

Prohibited without substantially more work:

```text
Lambda is literally the UV cutoff of the fundamental dual theory;
DSSYK proves de Sitter holography;
a Type-II algebra implies diary recovery;
a bounded spectrum or finite entropy implies an operational cutoff;
nonzero dressed correlators imply payload access;
the result solves the cosmological constant problem.
```

## 11. Go/no-go recommendation

**WP0--WP2 are complete; close the successor at the current bulk input.** Do
not open a general DSSYK or de Sitter-holography calculation. Exact transported
protocols are a null; the clock state does not select a multitime instrument;
and the explicit NV detector contact remains unpriced. Neither the
Tietto--Verlinde observer-energy cap nor the available Euclidean and Lorentzian
backreaction results supplies the missing action, duration, contact-count, or
memory law. Reopen only if a bulk construction jointly derives a Lorentzian
instrument, retained-memory/backreaction rule, and a common one-copy/doubled
implementation budget. Until then, the WP1 no-free-access theorem, the
clock-state/instrument nonidentifiability result, and the
energy-cap/action-budget nonimplication are the endpoint.

This closes the DSSYK mechanism tested here, not the larger question of finite
observer capacity in quantum gravity. A separate successor charter is in
`observer_process_capacity_quantum_gravity_charter_2026_07_20.md`. It seeks a
process-capacity law derived jointly from a self-contained observer instrument,
memory, and gravitational resource budget, and returns to DSSYK only after that
bulk law exists.

## Primary literature map

- Susskind, [De Sitter Space, Double-Scaled SYK, and the Separation of Scales](https://arxiv.org/abs/2209.09999).
- Narovlansky and Verlinde, [Double-scaled SYK and de Sitter Holography](https://arxiv.org/abs/2310.16994).
- Aguilar-Gutierrez, [Symmetry Sectors in Chord Space and Relational Holography in the DSSYK](https://arxiv.org/abs/2506.21447).
- Chandrasekaran, Longo, Penington, and Witten, [An Algebra of Observables for de Sitter Space](https://arxiv.org/abs/2206.10780).
- De Vuyst, Eccles, Hoehn, and Kirklin, [Gravitational entropy is observer-dependent](https://arxiv.org/abs/2405.00114).
- Tietto and Verlinde, [A microscopic model of de Sitter spacetime with an observer](https://arxiv.org/abs/2502.03869).
- Aalsma and Sybesma, [The Price of Curiosity: Information Recovery in de Sitter Space](https://arxiv.org/abs/2104.00006).
- Nakata, Wakakuwa, and Koashi, [Black holes as clouded mirrors](https://arxiv.org/abs/2007.00895).
- Ahmadi, Jennings, and Rudolph, [Dynamics of a quantum reference frame undergoing selective measurements and coherent interactions](https://arxiv.org/abs/1005.0798).
- Aguilar-Gutierrez, [T-squared deformations in DSSYK: stretched-horizon thermodynamics](https://arxiv.org/abs/2410.18303).
- Aguilar-Gutierrez, [Deforming DSSYK and Reaching the Stretched Horizon From Finite Cutoff Holography](https://arxiv.org/abs/2602.06113).
- Aguilar-Gutierrez, Kukolj, and Seitz, [q-Askey Deformations of Double-Scaled SYK](https://arxiv.org/abs/2605.13956).
- Rahman and Susskind, [Comments on a Paper by Narovlansky and Verlinde](https://arxiv.org/abs/2312.04097).
- Rajgadia and Xu, [Emergent States and Algebras from the Double-Scaling Limit of Pure States in SYK](https://arxiv.org/abs/2604.14387).
- Fewster and Verch, [Quantum Fields and Local Measurements](https://arxiv.org/abs/1810.06512).
- Polo-Gomez, Garay, and Martin-Martinez, [A Detector-Based Measurement Theory for Quantum Field Theory](https://arxiv.org/abs/2108.02793).
- Jorgensen and Pollock, [Exploiting the Causal Tensor Network Structure of Quantum Processes to Efficiently Simulate Non-Markovian Path Integrals](https://arxiv.org/abs/1902.00315).
- Raval, Hu, and Anglin, [Stochastic Theory of Accelerated Detectors in a Quantum Field](https://arxiv.org/abs/gr-qc/9510002).
- Lin and Hu, [Backreaction and Unruh Effect: New Insights from Exact Solutions of Uniformly Accelerated Detectors](https://arxiv.org/abs/gr-qc/0611062).
- Espindola and Ali, [Spectral Admissibility of Real Observers in Euclidean de Sitter Gravity](https://arxiv.org/abs/2605.30423).
- Cui and Kolchmeyer, [A de Sitter Anti-Scrambling Algebra](https://arxiv.org/abs/2607.13665).
- Chen, Stanford, Tang, and Yang, [Negative Shocks versus Static Patch Holography](https://arxiv.org/abs/2607.14042).
