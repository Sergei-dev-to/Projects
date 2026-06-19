# Notes Map

Date: 2026-06-16

Purpose: keep the access-latency notes usable. The folder now contains result notes, conceptual bridge notes, literature notes, and scratch material. This file says what to read first and what each note is for.

## Read Order

For a cold start, read:

1. `long_term_goal_constrained_access.md`
2. `private_information_fate_classification.md`
3. `constrained_access_program_plan_review.md`
4. `access_geometry_and_export_bottlenecks.md`
5. `directions_review_2026_06_18.md`
6. `paths_forward_2026_06_18.md`
7. `level1_local_tightness_benchmark.md`
8. `level2_expander_fast_routing.md`
9. `level2_expander_mixer_theorem.md`
10. `moment_gap_two_way_attempt.md`
11. `access_latency_stress_test.md`
12. `external_review_response_2026_06_18.md`
13. `private_complement_unified_frame.md`

Then use the remaining files as needed.

## Canonical Result Stack

These are the notes closest to the current theorem draft.

- `self_review_and_external_review_packet.md`
  - Current self-review after the observability-gap target adjustment.
  - Lists solid results, conditional/open pieces, weak points, and the recommended outside-review packet.

- `external_review_response_2026_06_18.md`
  - Response to the first external-style review.
  - Records accepted fixes and the revised technical target:
    deterministic observability/export via free probability, design
    theory, operator spreading, or quantum-control observability.

- `paths_forward_2026_06_18.md`
  - Current result-oriented direction map.
  - Ranks the live routes after the latency classification, with the
    corrected split between de-protection and export:
    deterministic de-protection plus export, local tightness,
    expander/log-diameter fast routing, failure classification, dressed
    access, measurement-cut separation, and experimental/numerical
    access profiles.

- `level1_local_tightness_benchmark.md`
  - Conditional Level 1 theorem module.
  - States the local tightness benchmark:
    LR lower bound before light-cone arrival, and recovery after arrival
    under an explicit boundary export/decoupling condition.
  - Includes the conditional proof, conveyor/shift witness,
    directed-drift-scrambler witness, design-circuit upper bound route,
    log-diameter transfer, and isolates the remaining chaotic-circuit
    export task.

- `level2_expander_fast_routing.md`
  - Conditional Level 2 theorem module.
  - Replaces lattice diameter by bounded-degree expander access radius.
  - Shows that logarithmic collection plus decoupling export gives
    `O(log S + k + log(1/epsilon))` recovery latency.
  - Separates theorem-backed mixers from the harder deterministic
    expander-Hamiltonian export problem, and records the access-capacity
    caveat.

- `level2_expander_mixer_theorem.md`
  - Concrete Level 2 theorem-backed mixer module.
  - States the expander mixer theorem end to end and instantiates the
    export primitive with TPE/approximate-design decoupling and
    Brown-Fawzi random-circuit decoupling.
  - Separates logarithmic/polylog theorem-backed existence from the
    still-open deterministic expander Hamiltonian version.

- `moment_gap_two_way_attempt.md`
  - Immediate next result boundary after the moment-gap export
    criterion.
  - Positive route: prove a `t=2` expander moment-Hamiltonian gap and
    convert it to export/recovery.
  - Negative route: construct fast operator growth with abelian/public
    export, showing OTOCs and support growth do not imply private
    recovery.

- `access_geometry_and_export_bottlenecks.md`
  - Current synthesis note.
  - Unifies the Level 1 and Level 2 modules as:
    `private recovery latency = access geometry + export/decoupling`.
  - Compares ordinary lattices, directed channels, expanders,
    dressed/nonlocal access, and measurement-cut scale separation.
  - States the next result targets without treating horizons and
    measurements as identical.

- `directions_review_2026_06_18.md`
  - Current result-direction review.
  - Ranks the live branches by payoff/risk after the expander theorem:
    theorem-backed expander mixer, deterministic expander export, local
    tightness/dual-unitary cuts, failure classification, dressed access,
    export-capacity bounds, measurement-cut export, and experimental
    access profiles.

- `private_information_fate_classification.md`
  - Main organizing note.
  - Defines the static compartments:
    - public center,
    - recorded-but-deep block,
    - protected commutant.
  - Defines recovery mechanisms:
    - slow routed,
    - fast routed/scrambled,
    - dressed/nonlocal accessible.
  - Tracks what is proven, what is imported, and what remains open.
  - Current technical gate: replace iid/random baselines with correlated ETH/scrambling dynamics.

- `constrained_access_program_plan_review.md`
  - Current program review after the expander/moment-gap detour.
  - Re-centers the program on the access-profile triad:
    `publicization != de-protection != coherent export`.
  - Defines the experimental/numerical target quantities:
    `R_public`, `lambda`, and `F_export`.
  - Demotes expander moment-gap work to a witness branch for coherent
    export rather than the program center.

- `access_latency_stress_test.md`
  - Witness and countermodel companion.
  - Tests the theorem stack against ordinary reservoirs, saturated slow routers, collective charge pointers, HP/fast scramblers, nonlocal encoders, HoI/Gauss-law access, AdS, Rindler, and BTZ.
  - Use this when checking whether a proposed claim survives standard examples.

## Program Compass

- `long_term_goal_constrained_access.md`
  - Program-level destination.
  - States the broader aspiration:

    ```text
    constrained access -> public/deep/private structure
    -> effective classical or horizon-like structure above the cut
    ```

  - Also records what not to claim yet: no derived gravity, no derived geometry, no claim that horizons are literally Wigner-friend cuts.

## Conceptual Bridge Notes

These are useful for positioning but should not be imported into the theorem draft unless they produce precise claims.

- `private_complement_unified_frame.md`
  - Bridge between Heisenberg-cut and horizon-interface directions.
  - Establishes the three-compartment language.
  - Separates fixed-cut recovery from moving-the-cut operations.
  - Separates de-protection from decodability.

- `access_rg_and_substrate_screening.md`
  - Bridge to RG, information geometry, substrate screening, and access equivalence.
  - Main correction: access filtration is not automatically RG flow.
  - Useful distinction:

    ```text
    effective forgetting vs recoverable hiding
    ```

- `wigner_friend_horizon_access_pass.md`
  - Targeted literature pass on Wigner-friend/black-hole analogies, quantum erasure, and observer algebras.
  - Main lesson: the Wigner-friend/black-hole analogy is prior art; the opening is the access-algebra/private-complement/rate structure.

- `private_information_experiment_ideas.md`
  - Experimental/observational directions.
  - Main proposed signature:

    ```text
    public redundancy scale << private recovery scale
    ```

  - Includes the frozen-dynamics diagnostic as a possible lab analogue of routing versus dressed access.

- `access_profile_verification_target.md`
  - Lightweight bridge from the theorem stack to eventual numerical or experimental verification.
  - Records measurable quantities: `m_public`, `m_private`, `lambda`, `F_rec`, and disturbance to public records.
  - Keeps the experimental target visible without turning the current proof work into an apparatus-design project.

## Literature and Scratch

- `literature_scratchpad.md`
  - Search hits and rough relevance notes.
  - Not an endorsed bibliography.
  - Sources should be promoted from here into `refs.bib` or a focused literature note only after closer reading.

## Archive

- `archive/firm_road_after_g_branch.md`
  - Historical consolidation after parking the speculative geometry/`G` branch.
  - Superseded by `long_term_goal_constrained_access.md` and `private_information_fate_classification.md`.

- `archive/cut_sharpness_toy_model.md`
  - Earlier toy-model diagnostic for public/private cut sharpness.
  - Superseded by the commutant theorem, Pauli-growth theorem, and random-coding baseline in `main.tex`.

## Parent Notes

These parent-folder notes are useful history but are no longer the clean entry point.

- `../notes/constrained_access_review_memo.md`
  - Review packet from before the current folder was organized.
  - Partly superseded by `private_information_fate_classification.md`.

- `../notes/darwinian_no_hair_split.md`
  - Raw theorem workspace that led to the current TeX draft.
  - Superseded for current purposes by `main.tex`, `access_latency_stress_test.md`, and `private_information_fate_classification.md`.

- `../notes/access_emergence_philosophy.md`
  - Broad exploratory memo on emergence, substrate independence, and geometry above the cut.
  - Still useful for ambition and guardrails, but `long_term_goal_constrained_access.md` is the shorter current compass.

## Format Rule Going Forward

New notes should declare one of these roles at the top:

```text
Role: result stack / stress test / conceptual bridge / literature / scratch / archive
```

They should also state:

```text
Status: proven / imported / conjectural / exploratory / superseded
```

This prevents diary-style notes from becoming canonical by accident.
