# bh-evaporator

Research program on the boundary between ordinary quantum-information
mechanisms and specifically gravitational input in black-hole evaporation.

Program-framing notice (2026-07-10):
`notes/program_reassessment_2026_07_10.md` finds that a strict, unique
gravity/QI demarcation is not presently defensible. The proposed successor is
an assumption audit and conditional-closure program for exterior recovery.
The five-row ledger remains the operational map pending an explicit framing
decision; it should not be read as a unique ontology of gravitational inputs.

## Current thesis

Once a finite state count, radiation algebra, active emission instrument, and
suitable diary-mixing dynamics are supplied, ordinary quantum mechanics gives
Page behavior, decoupling, and conditional recovery. The program asks which
supplied structures gravity must explain and which can be certified from
exterior observables.

The current ledger has three gravitational inputs: (1) the Schwarzschild state
count and softness, `S(E) ~ E^2`; (2) the physical radiation algebra and active
emission instrument; and (3) channel-relative temporal encoding of private
information. The last two meet in the temporal/Krylov orbit of the physical
emission process. They are not compressed by assuming an entropy-sized static
interface.

The active operational result separates two axes:

```text
source participation:
  model-side microscopic source structure versus the invariant physical
  jump/process map;

recovery latency:
  how quickly arbitrary private information reaches the emitted record.
```

The closed static source-rank branch used calibrated response: occupation
enhancement shifts the ratio HIGH and a drained thermal collective channel
shifts it LOW.  The LOW spectral identity is exact for stationary linear
gauge-invariant Gaussian additive channels, without a Markov or Planckian
assumption.  However, signed sectors can cancel, the ordinary Gaussian tail is
not identifiable from aggregate static or delay-resolved Gaussian data, and
an anomalous parametric Gaussian channel can pass Hawking flux, positive
absorption, calibrated response, and `g2=2` without passive starvation.
Moreover the raw source-only Gram participation needs a canonical coupling
metric to be representation invariant. These are closure results: microscopic
source participation is supplied model data, not a generally exterior-derived
observable. A finite-energy parametric pump can nevertheless emit `O(S)`
thermal Hawking/partner records while remaining exactly diary-blind. The live
question is therefore Q2: when and why does the active emission process acquire
a diary-visible temporal orbit? The long-time necessary theorem is now exact:
full-record distance from a diary-blind comparison process grows at most as the
linear sum of hybrid-reachable step defects, with no exponential blind-budget
penalty.

The current microscopic evaluation target is the physical, gauge-invariant
Matrix/BFSS D0-detachment process. A July 10 feasibility audit gives a
conditional go only for a design-stage small-`N` bosonic/BMN pilot; a full BFSS
information-export calculation is not presently a local project.

## Read first

- `notes/program_reassessment_2026_07_10.md` — candid audit of whether the
  demarcation umbrella survives and the proposed conditional-closure reframe.

Status correction: the static source-rank certificate is closed as a route to
a general exterior derivation. The spectral-starvation and two-drain results
survive as conditional passive-class phenomenology. The finite-pump result is
the control and launch point for the Q2 temporal-access program.

- `notes/static_source_rank_certificate_tombstone.md` — closure verdict,
  retained results, and reopening conditions.
- `notes/finite_energy_parametric_pump_result.md` — persistent thermal,
  partner-producing, exactly diary-blind active emitter.
- `notes/q2_composable_diary_access_theorem.md` — long-time shared-memory
  access obstruction and recovery converse.
- `notes/shrinking_shell_diary_access_result.md` — no-hiding archive bound and
  blind/weak/mixing `S(E)~E^2` shell comparison.
- `notes/microcanonical_coded_pump_construction.md` — integrated finite-shell
  collision with thermal event odds and locally identical coded radiation.
- `notes/temporal_access_necessary_sufficient_synthesis.md` — closed
  conditional access/decoupling bracket and the remaining gravity target.
- `notes/demarcation_scoop_audit_2026_07_10.md` — novelty and priority audit.
- `notes/demarcation_synthesis.md` — five-row quantum/gravity map.
- `notes/quantum_gravity_demarcation_ledger.md` — authoritative five-row
  program plan and execution gates.
- `notes/bfss_detachment_feasibility_2026_07_10.md` — Matrix/BFSS go/no-go
  dossier and smallest faithful pilot.
- `notes/prototype_adjudication_directions.md` — superseded prototype roadmap
  retained as a historical audit trail.
- `notes/certificate_gap_closure_plan_2026_07_09.md` — superseded closure
  plan retained as an audit trail.
- `notes/q1b_static_certificate_theorem.md` — source-rank certificate.
- `notes/collective_channel_starvation_result.md` — route-2b completion.
- `notes/collective_channel_spectral_starvation_theorem.md` — exact
  stationary Gaussian non-Markovian extension.
- `notes/signed_cancellation_and_gram_tail_result.md` — aggregate
  cancellation no-go, paired-leg bound, and two-drain separator.
- `notes/q2_operator_overlap_bridge_theorem.md` — superseded first
  generator-level latency formulation.

- `notes/source_gram_invariance_audit.md` — exact representation no-go and
  jump-map/Choi replacement target.
- `notes/anomalous_parametric_channel_result.md` — active Gaussian route 2c.
- `notes/delay_correlation_nonidentifiability_result.md` — full Gaussian
  delay-correlation no-go for hidden source rank.
- `notes/certificate_time_budget_result.md` — precision versus evaporation
  budget.

## Active papers

`paper_boundary_saturation/` is now a conditional technical paper rather than
the program's flagship. Its passive theorem survives, but its no-go results and
active counterexample close the attempted general static inference. Q2 and the
algebra/temporal-access synthesis are the primary program line.

- `paper_boundary_saturation/` — conditional passive source-participation,
  line-response, and no-go paper.
- `paper_access_latency_classification/` — access/routing theorem stack.
- `paper_ideal_hamiltonian/` — conditional Hamiltonian/ETH realization.

The primary demarcation synthesis has not yet been consolidated into its own
paper directory. `paper_frozen_routing_witness/` is a useful control-arm
proposal but is not on the current core publication path.

The other `paper_*` directories record earlier model-building stages and
controls.  They should not all be treated as simultaneous submission targets.

## Verification

Run the collective-channel support calculation with:

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

Build the boundary-saturation paper from its directory with a standard
`pdflatex`/`bibtex` cycle.
