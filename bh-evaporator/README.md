# bh-evaporator

Research program on the boundary between ordinary quantum-information
mechanisms and specifically gravitational input in black-hole evaporation.

## Current thesis

Once a finite state count, radiation algebra, and suitable dynamics are
supplied, ordinary quantum mechanics gives Page behavior, decoupling, and
conditional recovery.  The program asks which supplied structures gravity
must explain and which can be certified from exterior observables.

The operational evaporation ledger is the two-plus-one necessity trinity:
`S(E) ~ E^2`, entropy-many emission access `N_access ~ S`, and
mixing/scrambling sufficient for typical encoding.  The active
boundary-saturation work tests the second input; it has not yet eliminated it.

The active operational result separates two axes:

```text
source participation:
  model-side microscopic source structure versus the invariant physical
  jump/process map;

recovery latency:
  how quickly arbitrary private information reaches the emitted record.
```

The passive source-rank calculation uses calibrated response: occupation
enhancement shifts the ratio HIGH and a drained thermal collective channel
shifts it LOW.  The LOW spectral identity is exact for stationary linear
gauge-invariant Gaussian additive channels, without a Markov or Planckian
assumption.  However, signed sectors can cancel, the ordinary Gaussian tail is
not identifiable from aggregate static or delay-resolved Gaussian data, and
an anomalous parametric Gaussian channel can pass Hawking flux, positive
absorption, calibrated response, and `g2=2` without passive starvation.
Moreover the raw source-only Gram participation needs a canonical coupling
metric to be representation invariant.  The flagship is therefore under
target/class revision; input 2 has not been exterior-certified.

## Read first

Status correction: the Q1b staging theorem and boundary-saturation paper are
under target/channel-class revision after the July 9 source-invariance and
active-Gaussian audits.  The spectral-starvation theorem is exact only for the
passive gauge-invariant additive class.

- `notes/demarcation_synthesis.md` — five-row quantum/gravity map.
- `notes/quantum_gravity_demarcation_ledger.md` — steering ledger.
- `notes/prototype_adjudication_directions.md` — current technical roadmap.
- `notes/certificate_gap_closure_plan_2026_07_09.md` — active closure
  sequence, acceptance gates, and deferred scope.
- `notes/q1b_static_certificate_theorem.md` — source-rank certificate.
- `notes/collective_channel_starvation_result.md` — route-2b completion.
- `notes/collective_channel_spectral_starvation_theorem.md` — exact
  stationary Gaussian non-Markovian extension.
- `notes/signed_cancellation_and_gram_tail_result.md` — aggregate
  cancellation no-go, paired-leg bound, and two-drain separator.
- `notes/q2_operator_overlap_bridge_theorem.md` — latency obstruction.

- `notes/source_gram_invariance_audit.md` — exact representation no-go and
  jump-map/Choi replacement target.
- `notes/anomalous_parametric_channel_result.md` — active Gaussian route 2c.
- `notes/delay_correlation_nonidentifiability_result.md` — full Gaussian
  delay-correlation no-go for hidden source rank.
- `notes/certificate_time_budget_result.md` — precision versus evaporation
  budget.

## Active papers

`paper_boundary_saturation/` is not locked: its passive theorem survives, but
the source metric, active Bogoliubov route, and operational resource claim are
being revised before any black-hole/QNM specialization.

- `paper_boundary_saturation/` — flagship source-participation and
  line-response certificate.
- `paper_access_latency_classification/` — access/routing theorem stack.
- `paper_frozen_routing_witness/` — experimental control-arm proposal.

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
```

Build the flagship paper from its directory with a standard
`pdflatex`/`bibtex` cycle.
