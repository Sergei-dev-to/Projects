# bh-evaporator

Research program on the boundary between ordinary quantum-information
mechanisms and specifically gravitational input in black-hole evaporation.

## Current thesis

Once a finite state count, radiation algebra, and suitable dynamics are
supplied, ordinary quantum mechanics gives Page behavior, decoupling, and
conditional recovery.  The program asks which supplied structures gravity
must explain and which can be certified from exterior observables.

The active operational result separates two axes:

```text
source participation:
  how many independent source-Gram directions carry the Hawking line;

recovery latency:
  how quickly arbitrary private information reaches the emitted record.
```

The current source-rank certificate uses a calibrated two-sided line
response.  Occupation enhancement shifts the emission/absorption ratio
above its thermal reference.  A drained thermal collective channel shifts
it below the reference when its refill rate is bounded by the thermal/QNM
scale.  The latter statement is conditional on the stated Markovian refill
and Planckian/QNM input; mixed-frequency multiplexing remains open.

## Read first

- `notes/demarcation_synthesis.md` — five-row quantum/gravity map.
- `notes/quantum_gravity_demarcation_ledger.md` — steering ledger.
- `notes/prototype_adjudication_directions.md` — current technical roadmap.
- `notes/certificate_gap_closure_plan_2026_07_09.md` — active closure
  sequence, acceptance gates, and deferred scope.
- `notes/q1b_static_certificate_theorem.md` — source-rank certificate.
- `notes/collective_channel_starvation_result.md` — route-2b completion.
- `notes/q2_operator_overlap_bridge_theorem.md` — latency obstruction.

## Active papers

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
```

Build the flagship paper from its directory with a standard
`pdflatex`/`bibtex` cycle.
