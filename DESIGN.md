# Lantern Tide Design Notes

## Goal

Build a playable, low-pressure cozy-game prototype that can collect ASD-relevant behavioral signals without feeling like a modal questionnaire. The player should experience a small village scene first; the assessment layer is secondary and mostly invisible during play.

The working model is:

```text
play situation -> observable choice/route behavior -> evidence-vector update -> profile summary -> optional scalar range
```

The scalar estimate is intentionally secondary. The vector and profile flags matter more than a single number.

Current measurement target: a play-based reflection of adult-women autism-trait domains. It is meant to help players notice patterns and decide whether more formal self-assessment or clinical evaluation might be worth exploring. It is not meant to classify, diagnose, or reproduce the source questionnaire total.

## Product Boundary

Lantern Tide is:

- GQ-ASC-inspired.
- A static frontend prototype.
- A design and measurement exploration.
- A short playable demo for feedback.

Lantern Tide is not:

- A diagnostic instrument.
- A validated GQ-ASC score.
- A replacement for clinical evaluation.
- A claim that one game route can identify autism.

Any player-facing or developer-facing language should preserve that boundary.

## Source Alignment

The current source reference is [GQ_ASC_ADULT_WOMEN_REFERENCE.md](GQ_ASC_ADULT_WOMEN_REFERENCE.md), based on the modified adult-women GQ-ASC PDF and Brown et al. (2020).

The source instrument uses a 4-point agree/disagree questionnaire, five components, reverse scoring for specified items, and a total-score cutoff. Lantern Tide does not implement that scoring. It instead translates some construct families into behavioral game situations and a hand-tuned evidence vector.

Current alignment is partial:

- Camouflaging, sensory sensitivities, socializing, interests, and imagination/play are represented indirectly.
- Imagination/play is sampled through story cards, the story lantern, and symbolic object play, but it is still lighter than the source component.
- Validated questionnaire scoring is not implemented.

Do not describe the app as scoring the GQ-ASC unless an explicit licensed questionnaire mode is added and kept separate from the behavioral game profile.

## Current Game Loop

The player starts in Harborwake on the morning of Lantern Tide. The scene has four areas:

- Market Square: social load, lanterns, bells, Mira, Saff.
- Quiet Garden: recovery, fountain, cedar, smooth shell.
- Beach Path: shells, tide pool, Lio, Nia.
- Tide-Glass Workshop: sorting, display, thread basket, Oren.

Core preparations:

- Mira needs the lantern oil card.
- Lio needs help with the shell path.
- Oren needs help with the tide-glass display.

Side interactions are not filler. They provide contrast and additional evidence around sensory regulation, social monitoring, novelty sampling, and pattern-focused behavior.

Newer assessment-specific side interactions:

- Notice board: distinguishes direct helping, social monitoring, and concrete role/schedule structure.
- Story cards and story lantern: sample explicit imagination/play separately from novelty.
- Glass loom: samples systemizing, repeat-tuning, context-switch friction, and novelty sampling.

## Evidence Vector

`app.js` tracks these dimensions:

| Dimension | Intended role |
|---|---|
| `social_prediction_uncertainty` | Pausing, watching, or needing more context before social action. |
| `social_monitoring_cost` | Active effort spent tracking or managing social interaction. |
| `masking_adaptation` | Self-adjustment, guided entry, repair, or norm-following behavior. |
| `sensory_accumulation` | Load from sound, crowding, brightness, or simultaneous stimulation. |
| `regulation_dependency` | Use of recovery places, comfort objects, pacing, or quiet returns. |
| `context_switch_friction` | Difficulty leaving, switching tasks, or stopping a focused thread. |
| `focused_loop_depth` | Repeated or deep engagement with a narrow system. |
| `systemizing_structure` | Sorting, ordering, pattern-building, rule extraction. |
| `ambiguity_avoidance` | Preference for clearer roles, timing, schedules, or concrete affordances. |
| `novelty_breadth` | Broad sampling and curiosity; treated mainly as a confound guard. |
| `social_drive` | Desire to approach socially; context, not ASD evidence by itself. |
| `imagination_play` | Story, pretend play, symbolic making; used for source-domain coverage, not the scalar ASD-axis projection. |

The current scalar projection weights process dimensions, then subtracts for novelty breadth and pure social drive so that extroversion, completionism, and novelty seeking do not automatically look like ASD alignment.

## Construct Coverage Matrix

`SOURCE_DOMAIN_MODEL` in `app.js` is the canonical construct map. Each source domain has:

- weighted evidence dimensions,
- a sampling threshold,
- player-facing notes,
- explicit confounds to guard against.

Current source domains:

| Source domain | Main evidence dimensions | Main confounds |
|---|---|---|
| Imagination and play | `imagination_play` | Novelty without story, art preference, playful mood. |
| Camouflaging | `masking_adaptation`, `social_monitoring_cost`, `social_prediction_uncertainty` | Ordinary politeness, shyness, new-place caution. |
| Sensory sensitivities | `sensory_accumulation`, `regulation_dependency` | Fatigue, headache, preference for quiet. |
| Socializing | `social_drive`, social-monitoring dimensions, sensory load | Extroversion, introversion, task urgency. |
| Interests | `focused_loop_depth`, `systemizing_structure`, `context_switch_friction`, `novelty_breadth` | Completionism, puzzle preference, novelty seeking. |

## Confound Guards

Important false positives to avoid:

- Introversion alone.
- Direct social approach alone.
- Completionist broad sampling.
- Sensory-only preference without broader pattern.
- Novelty seeking mistaken for focused interest.
- A single domain spike treated as a global profile.

Important false negatives to avoid:

- Extroverted autistic routes where social approach coexists with monitoring, load, recovery, or masking.
- Quiet regulation routes where the relevant signal is recovery-after-load, not simple avoidance.
- Focused/systemizing routes that are narrow and repeated rather than broad completionism.

## Summary Output

The end summary should be satisfying to a player who wants reflection, but it should not overclaim.

Current summary layers:

- A route style name such as `Pattern-Maker`, `Quiet Regulator`, or `Careful Connector`.
- Source-domain coverage for the five adult-women GQ-ASC components.
- A credibility/read label based on route length, domain breadth, single-domain spikes, thin evidence, and confound flags.
- A play signal range with mean and variance.
- Strongest driver families.
- Morning path observations.
- How the village adapted.
- Concrete festival outcome.
- A note that this is not a diagnosis.

## Calibration Path

The prototype now exposes an `assessmentRecord()` shape in `app.js` and lets the ending reflection copy/download that record. The same ending screen has a collapsed pilot export panel for pairing the route with comparator/context fields. A useful validation dataset would collect:

- the game route record,
- source-domain vector values,
- summary score/range,
- a separately administered validated questionnaire or clinician-reviewed comparator,
- optional context variables such as age range, diagnosis status, and replay/role-play intent.

The current weights are hand-tuned. `calibration_runner.js` can fit ridge-regression weights from paired game/comparator records and report error against a mean-only baseline, leave-one-out error, and source-domain correlations. Those outputs are tuning diagnostics, not validation by themselves. A calibration study should fit or revise the weights against external outcomes, then retest confound routes and order-stability routes before making stronger claims.

## Public Data Prior

`public_data_prior.js` maps the public UCI Adult Autism Screening AQ-10 dataset into the game's source domains and generates `calibration_prior.public.json`. This gives a weak adult-screening anchor and female-subset statistics.

The prior is not allowed to replace the female-oriented design target. AQ-10 does not adequately cover camouflaging, gendered social scripts, subtle adaptation, or internalized sensory load. Those constructs stay intentionally oversampled in the game even when public data is used for broad sanity checks.

## Reliability Checks

`scenario_runner.js` now includes:

- scenario checks for core scoring expectations,
- scripted playthroughs covering broad and narrow source-domain routes,
- simulated player archetypes,
- reliability pairs that replay same-intent routes in different orders and compare domain profiles.

Passing these checks is not validation. It only prevents obvious regressions in the prototype logic.

## UI Principles

The game should feel approachable for players who may be ASD, including ASD girls or women who may have learned masking strategies.

Guidelines:

- Prefer direct, concrete choices over abstract self-rating.
- Do not prompt the player how they are supposed to feel.
- Keep tasks discoverable without turning the game into a checklist.
- Avoid modal-questionnaire feel where possible.
- Keep phone interactions usable: tap to walk, sideways drag to look, vertical scroll outside the map.
- Make dialogue choices readable and visually distinct.
- Keep the developer/scoring layer hidden from ordinary play.

## Current Limitations

- The map is still symbolic canvas art, not a full Palia-like world.
- Movement is click/tap-to-walk, not physics-heavy exploration.
- The evidence model is hand-tuned and unvalidated.
- The app does not administer or score the original GQ-ASC questionnaire.
- Imagination/play is now explicitly sampled, but still needs more situations before it should be treated as robust.
- The interaction set is small, so uncertainty should remain visible.
- No real play/comparator calibration dataset has been collected yet, though export, pilot collection, public proxy-data, and offline fitting tools now exist.
- Results are useful for design feedback, not clinical interpretation.

## Maintenance Notes

- `OBJECTS` in `app.js` defines most playable interactions.
- Choice text, result text, evidence deltas, state deltas, and quest completion live together in each object.
- `auditInteractionCoverage()` catches common content/scoring mistakes.
- `SCENARIOS` plus `scenario_runner.js` should be updated when scoring logic changes.
- The public page should use clean asset URLs; use the no-cache local server for development when browser caching hides changes.
