# Direction Plan: Verified Recovery as a One-Sided Collapse Witness

Date: 2026-07-02

Role: research direction plan (foundations track)

Status: planning; upgrades Route 6 of
`../experimental_prediction_routes.md` and the Collapse/Noise section of
`../access_profile_verification_target.md`.

## One-Line Goal

Formalize verified diary recovery after redundant record formation as a
one-sided positive witness against objective-collapse models, and map
verified-recovery experiments onto collapse parameter space with record
redundancy as the macroscopicity variable.

## The Core Asymmetry

Existing collapse tests (matter-wave interferometry, spontaneous
radiation, optomechanical noise) hunt for anomalous *decoherence* — a
negative signal confounded by ordinary environmental decoherence.  The
access framework supplies the opposite polarity:

```text
failed recovery:      uninformative (environment produces it too).
verified recovery:    falsifies any collapse event in the window;
                      no environmental confound can fake success.
```

In discrimination-table language (qi access note): collapse models
predict the irreversible-erasure row; unitary QM predicts the
later-recoverable row; only the erasure row is refutable by a single
positive outcome.

Scope guard, stated up front in any draft: this has no power against
Bohmian mechanics or any interpretation reproducing unitary channel
statistics.  Targets are dynamical-collapse models only (GRW, CSL,
Diosi-Penrose), which are different theories.

## Claims To Establish

```text
C1 (witness lemma):
    in a collapse model with effective collapse rate Gamma acting
    during the record-formation window tau, post-record recovery obeys
    F_rec^e <= F_triv + O(exp(-Gamma tau))-type bound derived from the
    collapse master equation.  Verified F_rec^e >= 1 - delta then
    upper-bounds Gamma for the realized (mass, geometry, redundancy).

C2 (one-sidedness lemma):
    formalize the asymmetry: recovery success probability under
    unitary QM + noise never exceeds the noiseless value, so observed
    success is monotone evidence; make the statistical statement clean
    (a bound, not a likelihood-ratio hand-wave).

C3 (redundancy axis):
    compute, for CSL specifically, the collapse rate of a pointer
    recorded in N redundant fragments of mass m each, versus one
    record of mass Nm, versus no record.  Question: does redundancy
    per se buy collapse-model sensitivity, or is it fully absorbed
    into total displaced mass?  This is the calculation the direction
    lives or dies on, and it is analytic.

C4 (translation claim):
    interferometric visibility is recovery of one off-diagonal;
    entanglement-fidelity recovery of a diary is the complete version.
    Make precise in what sense verified recovery is a strictly
    stronger witness than fringe visibility at matched mass scale,
    or show it is not.
```

## Honest Reach Assessment (goes in the paper, not just the plan)

Current verified-recovery experiments live at a few qubits — many
orders of magnitude inside the unexcluded CSL region.  The paper's
claim is therefore not "we can rule out collapse now" but:

```text
1. here is the operational quantity collapse models deny;
2. here is a protocol whose positive outcome excludes them
   model-independently within the realized window;
3. here is the redundancy/mass/coherence frontier at which the
   protocol starts cutting unexcluded parameter space.
```

Item 3 requires locating the crossover platform.  Candidate: levitated
optomechanics where the particle's position is redundantly recorded in
scattered photons (a natural Darwinism setting) and recoherence is
attempted.  If C3 says redundancy buys nothing beyond mass, item 3
reduces to known recoherence frontiers and the paper shrinks
accordingly.

## Blocking Prior-Art Checks

```text
1. recoherence-based collapse bounds: has anyone derived CSL/GRW
   exclusions from demonstrated recoherence or coherence revival
   rather than from sustained coherence?  (Bassi et al. reviews;
   levitated-optomechanics proposals.)
2. collapse models vs quantum error correction / information recovery:
   any existing statement that verified QEC recovery bounds collapse
   rates (the witness lemma may exist in QEC clothing).
3. Darwinism-meets-collapse literature: whether record redundancy has
   been used as a collapse-model variable anywhere.
4. the Touil/Zurek Darwinism-scrambling line (already flagged in the
   qi-note review) for overlap with C4.
```

## Milestones

```text
M1  prior-art pass (checks above).
M2  C1 + C2: witness and one-sidedness lemmas from the CSL master
    equation.  Short, self-contained; also directly usable by the
    Heisenberg-cut essay.
M3  C3: the redundancy calculation.  Decision point for the paper's
    size.
M4  C4: relation to interferometric visibility.
M5  reach map: protocol parameters vs CSL (lambda, r_C) exclusion
    frontier; identify the crossover platform.
M6  draft.
```

## Kill Criteria

```text
- M1 check 2 finds the witness lemma already published => downgrade to
  citation inside the Heisenberg-cut essay; stop the standalone paper.
- M3 shows redundancy is fully absorbed into displaced mass AND M1
  check 1 shows recoherence bounds are established practice => nothing
  new remains beyond packaging; fold into the essay.
- C2 cannot be made statistically clean (success probability bound
  leaks) => the "one-sided" framing is overclaimed; do not publish it.
```

## Deliverable and Venue

Foundations-adjacent paper: Foundations of Physics, Quantum Studies, or
quant-ph arXiv note; this is also the falsifiable payload that the
Heisenberg-cut essay needs, so M2's lemmas should be written to be
liftable.  All content analytic; no numerics.

## Dependencies

- Discrimination-table rows quoted from the qi access note after its
  fixes are applied.
- Independent of directions 1 and 2, but shares the verified-recovery
  protocol machinery with the frozen-routing proposal; if both proceed,
  keep protocol definitions in one place (suggest: a shared
  definitions note, created when the second draft starts).
