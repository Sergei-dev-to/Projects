# bh-evaporator

Status: completed research program. Endpoint recorded 2026-07-13.

"Completed" refers to this control-model and comparative program, not to the
black-hole information problem as a whole.

This project asked whether one ordinary unitary quantum process could reproduce
the exterior package associated with black-hole evaporation: nearly thermal
emission, heating and faster power loss as the system shrinks, a decreasing
internal state capacity, a Page-like entropy turnover, and recoverable quantum
information in the radiation.

The answer is yes. The project's unified control model realizes the
thermodynamic and information behavior in the same evolving state. Independent
work in random-unitary, operator-growth, equilibrium, replica, and
fixed-Hamiltonian models supplies more developed examples in which
state-dependent radiation dynamics leads to reconstruction. The broad
model-level compatibility question is therefore answered.

## Program outcome

The program began by looking for a clean boundary between work done by gravity
and work done by quantum information theory. The comparison showed that no
unique boundary survives changes of description. A more stable result is a
list of obligations that any microscopic account of evaporation must meet:

1. **Thermodynamics:** derive the state count and its dependence on energy and
   charges.
2. **Observable structure:** identify the physical radiation algebra and its
   complement, including constraints and sectors.
3. **Dynamics:** derive the emission process and show how private-state
   differences enter the radiation over time.
4. **Consistency:** maintain unitarity, conservation laws, shrinking capacity,
   and a complete account of partners, remnants, or other hidden systems.

Once those ingredients are supplied, ordinary quantum mechanics explains much
of the remaining architecture: Page behavior, decoupling, encoded
reconstruction, and conditional recovery. A theory of an actual black hole
must explain why the ingredients exist and why they have their particular
gravitational form, including the area law and the interior.

The comparison also separated four questions that were often compressed into
the word *access*:

```text
destination:       where the information finally resides;
dynamical access:  when the emitted record first depends on it;
algebraic access:  whether it is reconstructible from the radiation in
                   principle;
recovery:          whether a specified observer can decode it with controlled
                   error.
```

Hawking, Page, Hayden--Preskill, islands, replica wormholes, and dynamical
bridge models answer different parts of this sequence. The comparison map
records their assumptions and conclusions without treating any one result as
the entire information problem.

## What this project added

The main project-level contributions are:

- a unified geometry-free evaporator in which Schwarzschild-like
  thermodynamics and information diagnostics belong to the same radiation
  history;
- exact controls showing that thermal emission and partner production can be
  diary-blind, while recoverable information can also live entirely in
  multitime correlations;
- a composable bound showing that a radiation history cannot support accurate
  recovery while remaining cumulatively close to a diary-blind process;
- a family of non-identifiability results showing why coarse or static
  radiation measurements generally do not reveal a hidden microscopic source
  decomposition;
- an adjudication of the strict N-portrait/memory-burden prototype, separating
  its entropy-sized memory degeneracy from the source rank and information
  routing of its specified radiation vertex.

These results establish compatibility, dependencies, controls, and limits of
inference. They do not select the microscopic process realized by a real black
hole.

## External-readiness status

The bounded A--D literature-overlap and scope pass is complete. The final
external-use wording is recorded in
`notes/standalone_result_passes_2026_07_16.md` and summarized in the endpoint
note. In particular, Result B's gate is closed: its generic telescoping bound
is standard comb/hybrid continuity, while its diary-blind evaporation
comparison, hybrid-reachable defects, and recovery converse are retained as
application-level content.

For terminology, the older “three gravitational inputs” ledger is historical:
state count, physical radiation algebra/emission instrument, and
channel-relative temporal encoding. The endpoint's current four-obligation
taxonomy supersedes that ledger by separating thermodynamics, observable
structure, dynamics, and consistency. These are two levels of description,
not competing counts.

## Why the program ends here

The original control-model question has been answered, and the comparative
pass found that effective dynamical bridges already exist in the literature.
Continuing now would require choosing a particular quantum-gravity theory and
deriving its physical radiation sector and state-dependent emission dynamics.
That is worthwhile successor research, but it is a different commitment from
refining the present control models.

The principal successor considered here was BFSS Matrix theory. Existing work
provides D0-brane evaporation and an effective Page curve, while a complete
gauge-invariant, state-resolved radiation channel derived from the BFSS
Hamiltonian remains open. The local feasibility audit did not identify a
calculation that would close that gap without beginning a substantially new
Matrix-theory program.

The observation-facing branches remain documented and are deliberately parked.
The signed starvation/asymmetry diagnostics remain conditional results for
declared passive model classes. The frozen-routing witness remains a separate
experimental control proposal. Neither is needed for the program-level
conclusion.

## Post-endpoint successor proposal

The 2026-07-16 proposal
`notes/observer_relative_temporal_access_successor_proposal_2026_07_16.md`
opens a separate, bounded question: whether the natural constraint-dressed
observer implementation in doubled DSSYK changes the cost of temporal diary
access relative to an isospectral one-copy control. It gives the original idea
that `Lambda` may act as a dual cutoff an operational formulation in terms of
observer-process capacity. This successor does not reopen the completed A--D
obligations, and
it expressly does not assume that a bounded spectrum, finite entropy, or
Type-II algebra is already an operational cutoff or a recovery result.

WP0 and WP1 are complete. The primary-source pass and finite-shell protocol are
in `notes/dssyk_wp0_protocol_and_overlap_2026_07_16.md`; the exact isometric,
charge, and twirl controls are in
`notes/dssyk_wp1_formal_controls_2026_07_16.md`. Their joint verdict makes WP2
a physical-selection gate:
exactly transported one-copy and doubled protocols have identical record and
recovery capacities, while the explicit kinematical relational construction
uses the full bounded-operator algebra. A DSSYK dynamics probe now requires a
common, pre-registered implementation or complexity budget on both
descriptions.

The standalone external-facing draft is in
`paper_dssyk_observer_access/main.tex`. It presents the result as a DSSYK
demarcation theorem and exact controls, without the internal WP history. The
clock-state/instrument gate of WP2 is complete with a negative verdict; its
scaling-operator/detector branch remains parked pending a physically derived
instrument and interaction resource rather than a chosen operator family.

The follow-on intrinsic-bandwidth gate is complete in
`notes/dssyk_intrinsic_bandwidth_gate_2026_07_19.md`. It tests the original
cutoff question without reopening WP2. In the Narovlansky--Verlinde
normalization, the native DSSYK bandwidth is
$B=4\mathcal J/\lambda=1/(2\pi G_N)$, so the associated full-band quantum
speed limit is microscopic and the de Sitter radius cancels. An observer-level
cutoff remains conditional on a separately derived detector-resource budget.
The same note applies Result B to show that accurate record recovery requires
order-one integrated diary-sensitive detector action; native diary-blind
bandwidth alone does not supply it.

The July anti-scrambling update reopens only a narrower observer-process
completion problem. It is documented in
`notes/dssyk_observer_process_completion_2026_07_19.md`. Two exact controls are
complete there. First, the de Sitter two-point transfer factor
$e^{-\pi R_{\rm dS}|\omega|}$ has a positive Cauchy random-offset completion;
within that chosen completion a two-level phase diary has one-record distance
$e^{-\pi R_{\rm dS}\Delta E}$ and fixed-error record cost scales as
$e^{2\pi R_{\rm dS}\Delta E}$. Fresh-jitter and shared-offset completions have
the same one-bin channel but differ by $(1-e^{-2\pi R_{\rm dS}\Delta E})/2$
on an explicit two-bin input, proving that the low-point filter does not
select a multitime comb. Second, a direct backwards Euclidean segment has
optimal worst-case heralding probability $e^{-2\tau B}$; on the full DSSYK
band and for $\tau=O(R_{\rm dS})$ this is $e^{-O(S_{\rm dS})}$, while a
physically selected narrow shell can differ. These are observer-process
controls, not an exact DSSYK OTOC. The gravitational multitime completion
test is complete in
notes/dssyk_observer_process_wp_a3_2026_07_19.md. It proves that the
anti-scrambling functional is proper 2-OTO while a passive reduced observer
record is 1-OTO. A timefold-to-record compiler is therefore an additional
resource. The exact DSSYK OTOC remains parked.

The WP2 clock-state/instrument gate is complete in
`notes/dssyk_wp2_clock_resource_gate_2026_07_20.md`. Choosing the canonical
covariant time POVM for the CLPW maximum-entropy clock gives an exact Cauchy
one-read density with scale $\pi R_{\rm dS}$ and a general overlap formula
$M_f(\omega)$. The source construction does not select that POVM's
post-measurement instrument. Fresh, persistent, and contact-disturbed
instruments can have identical one-read data and different two-record diary
access. A finite two-contact detector makes this difference operational, and
extending the equal-energy isometry by the identities on clock and memory
reproduces every completed process in one-copy DSSYK. The 3D model-specific
hardest clock scale remains Planckian, with the radius canceled. WP2 is closed
at the current bulk input; reopening requires a bulk-derived clock instrument,
detector contact/backreaction rule, and common implementation budget.

## Read in this order

1. `notes/program_reevaluation_2026_07_12.md` -- accessible account of the
   physical question, the literature, the project models, and the endpoint.
2. `notes/program_endpoint_and_standalone_results_2026_07_13.md` -- concise
   wrap-up, retained results, boundaries, parked branches, and successor
   questions.
3. `notes/standalone_result_passes_2026_07_16.md` -- completed external-use
   overlap and scope pass for results A--D.
4. `notes/observer_relative_temporal_access_successor_proposal_2026_07_16.md`
   -- separate DSSYK/observer-access successor proposal and its stop gates.
5. `notes/dssyk_wp0_protocol_and_overlap_2026_07_16.md` and
   `notes/dssyk_wp1_formal_controls_2026_07_16.md` -- completed source,
   protocol, and formal-control gates for the successor.
6. `paper_dssyk_observer_access/main.tex` -- standalone short technical draft
   on isometric equivalence and the missing observer-resource constraint.
7. `notes/dssyk_intrinsic_bandwidth_gate_2026_07_19.md` -- bounded analytic
   test of whether the native DSSYK bandwidth realizes a cosmological
   operational cutoff.
8. `notes/dssyk_observer_process_completion_2026_07_19.md` -- July
   anti-scrambling update, positive Cauchy observer control, direct
   Euclidean-fold cost, and the gated multitime completion test.
9. `notes/dssyk_observer_process_wp_a3_2026_07_19.md` -- completed
   slot, contour-depth, and implementation-resource audit; records the stop
   verdict for an exact DSSYK OTOC.
10. `notes/dssyk_wp2_clock_resource_gate_2026_07_20.md` -- completed negative
    clock-state/instrument gate, general overlap, explicit inequivalent
    two-contact combs, and exact one-copy/doubled null.
11. `notes/evaporation_framework_comparison_map_2026_07_12.md` -- detailed
   assumption-to-result map across the major frameworks.
12. `notes/program_reassessment_2026_07_10.md` -- historical reassessment that
   retired the strict gravity/quantum-information demarcation.

Earlier ledgers, conjecture registers, and steering notes remain in `notes/` as
the audit trail. Their old sequencing instructions are historical wherever
they conflict with the endpoint documents above.

## Technical result index

- `notes/unified_sector_isometry_results.md` -- unified thermodynamic and
  information-return control model.
- `notes/finite_energy_parametric_pump_result.md` -- thermal, partner-producing,
  exactly diary-blind active emitter.
- `notes/microcanonical_coded_pump_construction.md` -- locally thermal coded
  radiation with information in multitime correlations.
- `notes/q2_composable_diary_access_theorem.md` -- cumulative temporal-access
  obstruction.
- `notes/shrinking_shell_diary_access_result.md` -- shrinking-capacity and
  no-hiding controls.
- `notes/static_source_rank_certificate_tombstone.md` -- closure of the general
  static source-certificate route.
- `notes/source_gram_invariance_audit.md` -- representation-invariance limit
  and process-map replacement.
- `notes/signed_cancellation_and_gram_tail_result.md` -- cancellation,
  non-identifiability, and conditional two-drain separator.
- `notes/anomalous_parametric_channel_result.md` -- active Gaussian mimic of
  the static Hawking package.
- `notes/delay_correlation_nonidentifiability_result.md` -- delay-resolved
  Gaussian no-go.
- `notes/certificate_time_budget_result.md` -- precision cost within one
  evaporation history.
- `notes/prototype_m0_m1_results.md`,
  `notes/prototype_m3_discriminator_table.md`, and
  `notes/asymmetry_backreaction_escape_result.md` -- strict memory-burden
  calculation.
- `notes/bfss_evaporation_literature_status_2026_07_12.md` and
  `notes/bfss_detachment_feasibility_2026_07_10.md` -- BFSS overlap and
  feasibility audit.

## Paper and proposal directories

The `paper_*` directories collect possible technical extractions and earlier
model-building stages. None is the program's flagship, and the completion of
the research program does not depend on turning each branch into a paper.

- `paper_boundary_saturation/` -- conditional passive diagnostics and static
  inference limits.
- `paper_access_latency_classification/` -- temporal-access theorem stack.
- `paper_ideal_hamiltonian/` -- conditional Hamiltonian/ETH realization.
- `paper_frozen_routing_witness/` -- separate experimental control proposal.

## Verification

The main numerical checks can be rerun with:

```powershell
python sim/collective_channel_starvation_check.py
python sim/spectral_starvation_check.py
python sim/signed_cancellation_optimizer.py
python sim/active_gaussian_route_check.py
python sim/delay_correlation_rank_no_go.py
python sim/finite_parametric_pump.py
python sim/shrinking_shell_diary_channel.py
python sim/locally_thermal_code_emitter.py
```
