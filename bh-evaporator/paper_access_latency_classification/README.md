# Access-Latency Classification Draft

Working title:

```text
Horizon Interfaces and the Recovery of Private Quantum Information
```

Purpose:

```text
Make the private-complement access-latency theorem stack reviewable:

finite LR velocity + source-local emission
=> no location-uniform fast recovery of arbitrary private deposits.

location-uniform fast private recovery
=> fast internal routing/scrambling OR nonlocal/dressed access.
```

Canonical local files:

- `main.tex`: theorem statements and proofs.
- `refs.bib`: bibliography for the TeX draft.
- `notes/README.md`: map of the notes folder and recommended read order.
- `notes/self_review_and_external_review_packet.md`: current self-review
  and suggested outside-review packet.
- `notes/access_latency_stress_test.md`: witness systems, countermodels,
  and failed implications.
- `notes/private_complement_unified_frame.md`: conceptual bridge between
  the Heisenberg-cut and horizon-interface directions.
- `notes/wigner_friend_horizon_access_pass.md`: literature pass on
  Wigner-friend, quantum-erasure, and observer-algebra overlap.
- `notes/private_information_experiment_ideas.md`: exploratory
  observational directions for private information behind public records.
- `notes/access_profile_verification_target.md`: measurable access-profile
  targets for eventual numerical or experimental verification.
- `notes/private_information_fate_classification.md`: result-facing
  skeleton for the full private-information fate classification.
- `notes/literature_scratchpad.md`: recent search hits before full
  adjudication into the draft or bibliography.
- `notes/access_rg_and_substrate_screening.md`: conceptual bridge between
  constrained access, RG-as-channel, universality, and substrate screening.
- `notes/long_term_goal_constrained_access.md`: program-level compass for
  constrained access, emergence, horizons, and possible geometry above the cut.

Archived local notes:

- `notes/archive/firm_road_after_g_branch.md`: historical consolidation
  after parking the speculative geometry/`G` branch.
- `notes/archive/cut_sharpness_toy_model.md`: exploratory diagnostic for
  public/private cut sharpness.  Useful background, but not part of the
  access-latency theorem stack.

Parent notes:

- `../notes/constrained_access_review_memo.md`: current program memo.
- `../notes/darwinian_no_hair_split.md`: theorem workspace that led to
  this draft.

Draft scope:

```text
This draft is about private-complement recovery latency.
The exact public-center cut theorem is included for orientation.
Approximate public objectivity is imported from Quantum Darwinism/SBS.
The new claims concern when private information is absent, slow,
scrambled/recoverable, or visible through dressed/nonlocal access.
```

Immediate result-facing path:

```text
1. Treat the private-information fate classification as the organizing
   result target.
2. Use the existing theorem stack for the publicized / protected /
   slow-routed / fast-routed / dressed-access branches.
3. Use the deterministic observability algebra
   `alg{U^{-i} K U^i}` to separate exact visibility from recovery.
4. Use the observability-gap lemma to target physical ETH/scrambling
   dynamics, then add the export/decoupling condition.
```

The static commutant theorem and the finite-velocity latency theorem are
already included in `main.tex`.  A first solvable de-protection model is
also included: independent random Pauli record generators make fixed
private operators lose protected weight exponentially in an
entropy-independent number of independent record units, while worst-case
exact protection collapses only once the sampled algebra spans the
block, at order `log(dim H)` record depth.  For a horizon-sized block
`dim H ~ exp(S)`, that stronger worst-case condition is `O(S)` records;
the HP-relevant quantity is the fixed-diary rate.  The next live
technical target is a more physical ETH/scrambling version of both
baseline calculations: independent Pauli-growth de-protection and
random-coding decodability should be reproduced by correlated
Heisenberg evolution of an actual record coupling.  The deterministic
problem now splits into observability of `alg{U^{-i} K U^i}` and
export/decoupling of the diary into the emitted records.  The new
observability-gap lemma makes the first target quantitative: a gap for
the product of one-step commutant projections implies exponential
fixed-diary de-protection.  The benchmark proposition shows that iid
Pauli records have an order-one average gap, common commutants have zero
gap, and a conditional per-step contraction is enough even for correlated
record sequences.
