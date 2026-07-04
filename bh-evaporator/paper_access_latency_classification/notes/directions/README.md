# Direction Plans

Date: 2026-07-02

Three research directions spun out of the access-profile synthesis
(`../qi_access_inequality_note.md`) and its review.  Each plan states a
target claim, the routes to it, blocking prior-art checks, milestones,
and kill criteria.

```text
1. learning_to_decode_lower_bound.md   (theory; new)
       query/sample lower bound for HP decoding without a U-oracle;
       makes the latency-complexity coupling a theorem.

2. frozen_routing_platform_proposal.md (experiment design; upgrades Route 2)
       platform-concrete protocol for the frozen-routing test with an
       error budget and confound controls.
       M1-M3 executed 2026-07-02: frozen_routing_m1_m3_working_note.md
       (tunable couplers, circuit-level freezing, two-copy YK at ~20
       qubits, viability gate passes on paper; [pin] items open).
       M4-M5 executed same day (pinning, budgets, public layer,
       sweep); PROMOTED to paper draft:
       ../../paper_frozen_routing_witness/main.tex.

3. verified_recovery_collapse_witness.md (foundations; upgrades Route 6)
       recovery as a one-sided positive witness against objective
       collapse; record redundancy as a macroscopicity axis.
```

Shared dependency: apply the three technical fixes to
`qi_access_inequality_note.md` (sample-complexity exponent,
Yoshida-Kitaev cost phrasing, one-directional hiding condition) before
any of these goes external.  The exponent fix matters most for
direction 1.
