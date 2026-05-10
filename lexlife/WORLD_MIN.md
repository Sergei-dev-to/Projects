# World-Min

## Purpose

Define the smallest world that makes lexocytes and their interactions matter over time.

This document sits above:
- `LEXOCYTE_MIN.md`
- `INTERACTION_MIN.md`

Its job is not to define full lexlife.
Its job is to define the weakest persistence criterion that makes:
- prediction consequential
- interaction consequential
- continued existence nontrivial

## Goal

Create a minimal world in which:
- lexocytes can persist or fail
- predictive success matters
- interaction can improve persistence

This is the first layer where "wrongness" should have consequences.

## Minimal World Contract

A `world-min` must provide:
- multiple lexocytes
- repeated ticks
- an interaction layer producing `x_i(t)` from local emissions
- a persistence variable for each lexocyte
- an update rule for that persistence variable

At this layer, the persistence variable can be called:
- viability
- energy
- reserve

The name matters less than the role:
- it determines whether a lexocyte continues to exist

## Why Persistence Is Needed

Without persistence and failure:
- prediction can be wrong forever with no consequence
- signaling can be irrelevant
- time has no selective force

So `world-min` introduces one thing that the lower layers avoid:
- continued existence depends on performance

## Minimal Persistence Rule

Each lexocyte has a scalar persistence value `u_i(t)`.

At each tick:
- the lexocyte pays a baseline maintenance decay
- the local neighborhood provides support or drag depending on its density
- predictive mismatch further erodes persistence

Minimal form:

`u_i(t+1) = u_i(t) - d + S(k_i(t+1)) - M * err_i(t+1)`

Where:
- `d > 0` is a baseline maintenance decay
- `k_i` is local neighbor count
- `S(k)` is neighborhood support
- `err_i` is prediction error
- `M >= 0` is mismatch cost

The important point is temporal alignment:
- a prediction formed after observing `x_t` should be evaluated against a later observation, not the same one
- viability should depend on both predictive coherence and local embedding

## Minimal Failure Rule

A lexocyte ceases to exist if:

`u_i(t) <= 0`

This is the smallest clean notion of failure.

It means:
- prediction is not just descriptive
- predictive failure can remove agents from the world

## Why This Is Enough

This is enough because it creates a direct path:

- emissions affect observations
- observations affect hidden states and predictions
- prediction mismatch affects persistence
- local density affects persistence
- persistence affects whether a lexocyte remains in the interaction network

That is the minimum loop that makes interaction and prediction jointly consequential.

## Minimal Requirement On Interaction

`world-min` should require more than isolated survival.

A good default requirement is:
- a lexocyte should not be able to persist indefinitely in total isolation unless the world explicitly intends solitude to be viable

Reason:
- otherwise communication becomes optional decoration
- isolated self-stable agents can satisfy persistence without needing other lexocytes

This can be enforced in several simple ways, for example:
- low or negative support under isolation
- strongest support at moderate local density
- mismatch cost applied regardless of density

The exact choice is a world design decision.
But `world-min` should state the principle:
- persistence should depend on genuine coupling, not only private self-stability

## Minimal Timing Model

At tick `t`:
1. each lexocyte has state `(h_t, theta)` and the world tracks viability `u_t`
2. the interaction layer provides `x_t`
3. each lexocyte updates to `h_{t+1}`
4. each lexocyte forms `q_{t+1}` and emits `e_{t+1}`
5. when `x_{t+1}` becomes available through the interaction layer, the world updates persistence using baseline decay, neighborhood support, and predictive mismatch
6. lexocytes with nonpositive persistence are removed
7. removed lexocytes do not contribute emissions to subsequent interaction fields

This keeps timing aligned with the lower layers.

The viability rule should be grounded in observations produced through the interaction layer.
In other words, persistence should depend on predictive coupling to other lexocytes and their local aggregate signals, not on unrelated exogenous targets.

## What World-Min Does Not Yet Require

`world-min` does not require:
- reproduction
- heredity
- mutation
- evolution
- resource fields
- strategy
- explicit cooperation
- semantic protocols

Those belong to later layers.

## Boundary Test

A world is too weak to count as `world-min` if:
- prediction has no effect on continued existence
- interaction has no effect on continued existence
- isolated lexocytes can persist trivially without coupling
- removal or failure never happens

The point of `world-min` is to make persistence depend on predictive coupling.

## Immediate Role In This Project

`WORLD_MIN.md` completes the first clean stack:
- `LEXOCYTE_MIN.md`: what a lexocyte is
- `INTERACTION_MIN.md`: how lexocytes affect one another
- `WORLD_MIN.md`: what makes their success or failure matter over time

The next layer can decide whether lexlife requires:
- reproduction
- inheritance of weights or seeds
- mutation and lineages
- richer signaling ecologies
