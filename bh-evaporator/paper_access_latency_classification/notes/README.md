# Notes Map

Date: 2026-06-20

Purpose: keep the access-latency notes usable after the constrained-access
direction was closed as a primary result engine. The folder contains useful
theorem work, conceptual bridges, literature checks, and scratch material, but
the live decision is now in the postmortem.

## Current Status

Read this first:

- `postmortem_2026_06_20.md`
  - Terminal decision note for the constrained-access direction.
  - Records why the apparent result space is largely occupied by quantum
    crypto, Hayden-Preskill recovery, symmetry-recovery bounds,
    Lieb-Robinson/locality, expander fast-scrambling, and decoupling.
  - Preserves the useful residue as a defensive audit toolkit:
    access/export bottlenecks, routed-versus-dressed recovery, and the
    distinction between publicization, de-protection, and coherent export.
  - Adds the start rule for future directions: run a literature pass before
    investing in drafting or proof work.

The rest of this folder should now be read as historical support and reusable
technical scaffolding, not as an active program plan.

## Read Order

For historical reconstruction, read:

1. `postmortem_2026_06_20.md`
2. `long_term_goal_constrained_access.md`
3. `program_status_2026_06_18.md`
4. `private_information_fate_classification.md`
5. `access_geometry_and_export_bottlenecks.md`
6. `level1_local_tightness_benchmark.md`
7. `level2_expander_fast_routing.md`
8. `level2_expander_mixer_theorem.md`
9. `experimental_prediction_routes.md`
10. `paths_forward_2026_06_18.md`

Then use the remaining files as needed.

## Historical Result Stack

These are the notes closest to the theorem draft. They are useful for audit,
reuse, and citation mining, but the postmortem supersedes them as program
guidance.

- `program_status_2026_06_18.md`
  - Program calibration after the black-hole-to-access shift.
  - Separates theorem-grade constrained-access results from the
    conditional black-hole sufficiency application.
  - Locates the gravitational residue in the supplied inputs:
    state count, boundary saturation, thermal-scrambling tie, and local
    geometry.
  - Historically named the next sharp test:
    scrambling diagnostics versus coherent recovery fidelity.

- `self_review_and_external_review_packet.md`
  - Self-review after the observability-gap target adjustment.
  - Lists solid results, conditional/open pieces, weak points, and the
    outside-review packet that was considered before the postmortem.

- `external_review_response_2026_06_18.md`
  - Response to the first external-style review.
  - Records accepted fixes and the revised technical target:
    deterministic observability/export via free probability, design
    theory, operator spreading, or quantum-control observability.

- `paths_forward_2026_06_18.md`
  - Historical result-oriented direction map.
  - Ranks the routes considered after the latency classification, with the
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
  - Former next-result boundary after the moment-gap export
    criterion.
  - Positive route: prove a `t=2` expander moment-Hamiltonian gap and
    convert it to export/recovery.
  - Negative route: construct fast operator growth with abelian/public
    export, showing OTOCs and support growth do not imply private
    recovery.

- `access_geometry_and_export_bottlenecks.md`
  - Synthesis note.
  - Unifies the Level 1 and Level 2 modules as:
    `private recovery latency = access geometry + export/decoupling`.
  - Compares ordinary lattices, directed channels, expanders,
    dressed/nonlocal access, and measurement-cut scale separation.
  - States the then-live result targets without treating horizons and
    measurements as identical.

- `directions_review_2026_06_18.md`
  - Result-direction review before the postmortem.
  - Ranks the branches then under consideration by payoff/risk after the
    expander theorem:
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
  - Former technical gate: replace iid/random baselines with correlated
    ETH/scrambling dynamics.

- `constrained_access_program_plan_review.md`
  - Program review after the expander/moment-gap detour.
  - Re-centers the program on the access-profile triad:
    `publicization != de-protection != coherent export`.
  - Defines the experimental/numerical target quantities:
    `R_public`, `lambda`, and `F_export`.
  - Demotes expander moment-gap work to a witness branch for coherent
    export rather than the program center.

- `experimental_prediction_routes.md`
  - Route map for experimentally or numerically legible
    predictions.
  - Separates framework demonstrations from discriminating measurements.
  - Strongest near-term route: recovery-versus-scrambling phase diagram,
    with locality / interaction-range scaling as the experimental
    access-axis test.
  - Calibration target:
    `same public records, different private quantum fates`.

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
  - Kept the experimental target visible without turning proof work into an
    apparatus-design project.

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
  - Review packet from before this folder was organized.
  - Partly superseded by `private_information_fate_classification.md`.

- `../notes/darwinian_no_hair_split.md`
  - Raw theorem workspace that led to the TeX draft.
  - Superseded for postmortem purposes by `main.tex`,
    `access_latency_stress_test.md`, and
    `private_information_fate_classification.md`.

- `../notes/access_emergence_philosophy.md`
  - Broad exploratory memo on emergence, substrate independence, and geometry above the cut.
  - Still useful for ambition and guardrails, but
    `long_term_goal_constrained_access.md` is the shorter compass.

## Format Rule If This Folder Is Reopened

New notes should be added only if the postmortem stop rule is satisfied. If
that happens, they should declare one of these roles at the top:

```text
Role: result stack / stress test / conceptual bridge / literature / scratch / archive
```

They should also state:

```text
Status: proven / imported / conjectural / exploratory / superseded
```

This prevents diary-style notes from becoming canonical by accident.
