# Swarm Goal

## Purpose

Recenter the project around the original motivation:
- many weak units
- local interaction only
- qualitatively new collective behavior at scale

This document exists to prevent drift toward:
- overly competent individual agents
- local optimization for its own sake
- reproduction before swarm behavior is interesting

## Source Motivation

The relevant image is closer to the micromachine cloud in Lem's *The Invincible* than to a colony of miniature chat models.

Key features of that image:
- a single unit is weak and nearly uninteresting
- collective capability appears only in the aggregate
- the swarm can temporarily form a higher-order functional system
- redundancy and replaceability matter more than individual sophistication

However, the project is not trying to reproduce every mechanistic detail of Lem's story.
The book is a source of pressure on the design, not a literal engineering blueprint.

## Goal

Build the smallest system in which a large population of weak lexocytes can exhibit collective modes that do not exist at the level of one or two units.

The project should prioritize:
- scale dependence
- collective organization
- temporary higher-order assembly
- distributed rather than centralized competence

The distinctive ambition is still to keep some minimal "LLM-like" character in the atom.
So the target is not a generic swarm particle.
The target is:
- a weak predictive communicative unit
- participating in a swarm whose collective behavior becomes qualitatively new at scale

This is the synthesis of the original goal and the lesson taken from the book.

## What Success Looks Like

Success is not:
- a stable pair
- a tiny conversation
- a clever single lexocyte
- survival by isolated units

Success is:
- clustering
- collective memory
- robustness and repair
- wave-like propagation
- quorum effects
- temporary spatial or functional differentiation
- robustness through redundancy

At least one such behavior should appear more reliably at higher density than at low density.

## Working Principle

The swarm should be more important than the atom.

This means:
- a lone lexocyte should be weak, possibly nonviable
- small groups should not already solve the full problem
- large populations should unlock new regimes

If one lexocyte can already do too much, the atom is overdesigned.

But if the lexocyte becomes too simple to count as a predictive communicative unit at all, the project loses its original identity.
So the design pressure is two-sided:
- the atom must stay weak
- the atom must still remain minimally model-based

## Role Of Prediction

Prediction remains useful, but it should not be treated as a private optimization target.

Prediction should contribute to swarm phenomena such as:
- local alignment
- synchronization
- threat response
- assembly cueing
- maintaining transient collective structure

If prediction only produces tidy local attractors, it is not serving the main goal.

Prediction should therefore be understood less as "tiny next-token game playing" and more as:
- local anticipation
- alignment cueing
- transient coordination support

## Role Of The World

The world should be evaluated by whether it supports swarm dependence, not merely persistence.

Important questions:
- Do larger populations produce different qualitative behavior?
- Are there density thresholds?
- Can local signals coordinate assembly or dispersal?
- Does the swarm remain functional under local loss or noise?

## Current Project Interpretation

The current simulator is acceptable only insofar as it helps probe swarm-supporting regimes.

It should not become an end in itself.

In particular:
- `world-min` is a scaffold for swarm emergence, not the final target
- `reproduction-min` remains deferred
- richer swarm metrics matter more than survival alone
- local signaling may need to be more cue-like than conversational
- the lexocyte may need to be simplified if it is doing too much individually

## Immediate Experimental Target

The next explicit targets should be:
- collective memory
- robustness and repair

Secondary signal:
- role differentiation

This is a stronger test than simple long-run coexistence because it asks whether the swarm can retain structure, recover from damage, and divide function without relying on a highly competent atom.

## First Concrete Experiment

The first concrete swarm experiment should be:
- transient disturbance, persistent trace, and partial repair

Minimal form:
1. start with a population distributed across the field
2. introduce a local disturbance in one region
3. remove or let the disturbance decay
4. test whether the swarm retains a trace of that event in its later configuration or response
5. damage part of the resulting organized structure
6. test whether the swarm partially repairs, reroutes, or restores that structure

The disturbance does not need to be semantically rich.
It only needs to create a local temporary change in conditions under which a collective response can arise.
For example, it may alter:
- local viability conditions
- the local observation channel
- the local signaling environment

## Success Criteria For The First Experiment

The experiment is successful if, relative to baseline:
- a transient event leaves a measurable later trace in the swarm
- the trace is not reducible to one or two surviving units
- partial damage does not simply erase the organized pattern
- the swarm shows some recovery, rerouting, or partial restoration after damage
- the effect is stronger at higher density than at low density

Role differentiation is an additional positive sign if different local regions settle into visibly different modes during or after recovery.

## Minimum Observables

The current simulator should eventually report enough structure to test:
- largest connected component over time
- number of connected components over time
- local density near the disturbance region over time
- population or occupancy change inside versus outside the disturbed region
- whether post-disturbance structure differs from pre-disturbance structure in spatial clustering, component structure, or token-mode distribution
- whether post-damage structure recovers toward the pre-damage configuration

Optional but useful:
- token-field change near the trigger
- recovery after local removals or noise
- differentiation of interior versus boundary or core versus fringe regions

## What Will Count As Failure

The experiment fails if:
- nothing persists from the disturbance once it is removed
- the whole field just dies
- the whole field freezes uniformly
- only a trivial pair or tiny fixed cluster survives
- local damage simply destroys all higher-order structure with no recovery
- the response does not differ meaningfully between low and high density

This failure definition is important because the current simulator can already produce stable persistence without clearly producing swarm behavior.

## Consequence For Design

Near-term design choices should favor:
- weak individual units
- density-dependent collective modes
- local reconfiguration
- measurement of cluster and field structure
- cue-like local signaling
- preserving a minimal predictive internal model

Near-term design choices should disfavor:
- rich isolated-unit competence
- early reproduction
- treating the current viability law as the main objective
- drifting all the way into generic non-predictive swarm particles

## Current Order

The intended order is now:
1. `SWARM_GOAL.md`
2. `LEXOCYTE_MIN.md`
3. `INTERACTION_MIN.md`
4. `WORLD_MIN.md`
5. only later `REPRODUCTION_MIN.md`
