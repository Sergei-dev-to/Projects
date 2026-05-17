# Lantern Tide Design Notes

## Goal

Build a playable, low-pressure cozy-game prototype that can collect ASD-relevant behavioral signals without feeling like a modal questionnaire. The player should experience a small village scene first; the assessment layer is secondary and mostly invisible during play.

The working model is:

```text
play situation -> observable choice/route behavior -> evidence-vector update -> profile summary -> optional scalar range
```

The scalar estimate is intentionally secondary. The vector and profile flags matter more than a single number.

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

The current scalar projection weights process dimensions, then subtracts for novelty breadth and pure social drive so that extroversion, completionism, and novelty seeking do not automatically look like ASD alignment.

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
- A play signal range with mean and variance.
- Strongest driver families.
- Morning path observations.
- How the village adapted.
- Concrete festival outcome.
- A note that this is not a diagnosis.

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
- The interaction set is small, so uncertainty should remain visible.
- Results are useful for design feedback, not clinical interpretation.

## Maintenance Notes

- `OBJECTS` in `app.js` defines most playable interactions.
- Choice text, result text, evidence deltas, state deltas, and quest completion live together in each object.
- `auditInteractionCoverage()` catches common content/scoring mistakes.
- `SCENARIOS` plus `scenario_runner.js` should be updated when scoring logic changes.
- Keep `index.html` asset build tags current when public caching hides changes.
