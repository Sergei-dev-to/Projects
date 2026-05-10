# Reproduction-Min

## Motivation

The guiding image here is not a clever individual machine that can do everything on its own.

The guiding image is closer to the insect-like micromachines in Lem's *The Invincible*:
- individually weak
- locally reactive
- interesting mainly in the aggregate
- replication/evolution present in the background, but swarm behavior in the foreground

That suggests a design principle:

Reproduction should not be treated as a required capability of a single lexocyte at the `world-min` stage.

## Principle

`world-min` should make single lexocytes weak and swarm-dependent.

If reproduction is introduced later, it should be a property of the larger substrate:
- a colony
- a local swarm configuration
- a developmental or environmental process

not necessarily a property of one isolated lexocyte acting as a complete self-factory.

## What This Means

At the current stage:
- a lone lexocyte does not need to reproduce
- a pair of lexocytes does not need to reproduce
- even a stable local group does not yet need reproduction

The first task is:
- make collective persistence real
- make density and local coupling matter
- make swarm-level organization possible

Only then should reproduction be added.

## Minimal Reproduction Idea

When the project is ready for reproduction, the cleanest first version is probably not:
- "one lexocyte copies itself"

but rather:
- a sufficiently coherent local swarm can seed a new occupied site or local patch

That would fit the motivation better because:
- reproduction is emergent and contextual
- no single unit has to be individually competent in every way
- lineage can still exist without making the atom too powerful

## Candidate Rule Shapes

Possible future reproduction triggers:

1. Local coherence trigger
   A small neighborhood with enough viable, mutually predictive lexocytes can seed a new site.

2. Density window trigger
   Reproduction happens only when local density is in a productive range.

3. Collective seed trigger
   Multiple nearby lexocytes contribute to a shared seed state that initializes a new lexocyte.

4. Environmental trigger
   The swarm modifies the local medium enough that a new lexocyte can emerge there.

These are all more faithful to the motivation than isolated self-copying.

## Why This Matters

If we give an isolated lexocyte:
- prediction
- emission
- persistence
- reproduction

too early, we risk making the atom too complete.

That would pull the project away from:
- swarm emergence

and toward:
- tiny self-contained agents with optional group behavior

The original motivation points the other way.

## Current Project Decision

Right now:
- keep reproduction out of the active simulator
- continue strengthening `world-min`
- only add a reproduction layer after the non-reproductive swarm already shows nontrivial collective persistence

At present, the active simulator contains no reproduction code path.

## Immediate Role In This Project

`REPRODUCTION_MIN.md` is not active yet.

It exists to prevent premature design drift.

The current order should be:
1. `LEXOCYTE_MIN.md`
2. `INTERACTION_MIN.md`
3. `WORLD_MIN.md`
4. only then `REPRODUCTION_MIN.md`
