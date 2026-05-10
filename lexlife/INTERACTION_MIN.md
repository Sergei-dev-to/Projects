# Interaction-Min

## Purpose

Define the smallest possible interaction scheme between lexocytes while staying below full ecology.

This document answers:
- how one lexocyte's output becomes another lexocyte's input
- what counts as token exchange
- what the minimal shared medium looks like

This document does not yet define:
- death
- reproduction
- energy
- selection
- large-scale colony dynamics

## Goal

Create the thinnest interaction layer that still allows lexocytes to matter to one another as predictive communicators.

The interaction layer should be:
- local
- token-based
- inspectable
- simple enough to simulate directly

## Minimal Interaction Contract

Each lexocyte does two externally visible things:
- emits a token `e_{t+1} in V`
- receives an encoded observation `x_t in V`

Interaction requires a shared mapping:

`x_i(t) = E({e_j(t) : j in N(i)})`

This means:
- one or more lexocytes emit tokens into a local medium
- the medium encodes those local emissions into an observation token for each receiving lexocyte

So lexocytes do not necessarily read one another's raw emissions directly.
They read an encoded local observation derived from nearby emissions.

By default:
- `N(i)` is the local neighborhood of lexocyte `i`
- `i` is not in `N(i)`
- `E` is local and memoryless unless a later world spec says otherwise

## Minimal Shared Medium

The medium can be represented abstractly as a local encoder.

At each tick:
1. every lexocyte emits a token
2. for each lexocyte, the medium gathers a local set of nearby emissions
3. the medium compresses that local set into one observation token
4. that observation token becomes the next lexocyte input

This keeps the interface simple:
- lexocyte outputs one token
- lexocyte inputs one token

## Recommended First Encoder

For the smallest interaction model, use:
- local neighborhood of nearby lexocytes
- one emitted token per lexocyte
- one encoded observation token per lexocyte

Recommended first encoding:
- `x_i(t) = mode({e_j(t) : j in N(i)})`

If no neighbor token is present:
- use a designated null or silence token, typically `0`

This is intentionally lossy.
The point is not richness yet. The point is to establish a clean signaling loop.

The encoder should be simple enough that it does not perform hidden cognition on behalf of the lexocytes.
It should summarize local emissions, not interpret them semantically.

## Why This Counts As Interaction

This is real interaction if:
- a lexocyte's emitted token changes what another lexocyte observes
- that changed observation can alter the other lexocyte's hidden state, prediction, or future emission

That is the minimum causal chain.

If emitted tokens do not affect any other lexocyte's future computation, there is no meaningful interaction.

## Minimal Timing Model

Interaction should use a synchronous tick model for the first version.

At tick `t`:
1. each lexocyte has hidden state `h_t`
2. each lexocyte receives observation `x_t`
3. each lexocyte updates to `h_{t+1}`
4. each lexocyte forms `q_{t+1}` and emits `e_{t+1}`
5. the medium collects all emitted tokens `e_{t+1}`
6. the medium encodes them into observations `x_{t+1}`

This aligns interaction with `LEXOCYTE_MIN.md`.

## Minimal Structural Assumptions

`interaction-min` assumes only:
- multiple lexocytes exist
- they share a finite vocabulary `V`
- each emits one token per tick
- each receives one encoded token per tick
- a local, memoryless encoder maps emissions to observations

It does not assume:
- a grid specifically
- a graph specifically
- any particular spatial geometry

The only requirement is locality: not every lexocyte should affect every other lexocyte equally.

## Recommended First Topology

For the first concrete implementation:
- use a 2D square grid
- one lexocyte per occupied site
- Moore neighborhood

But this is an implementation convenience, not part of the minimal ontology.

## What Interaction Must Preserve

The interaction layer must preserve:
- local causality
- token exchange
- distinguishability between emission and observation

In particular:
- `e_i(t)` is what a lexocyte says
- `x_i(t)` is what a lexocyte receives after environmental encoding

They should not be conflated.
Also, by default, a lexocyte does not receive its own emitted token through the encoder.

## Boundary Test

An interaction model is too weak if:
- emitted tokens never affect other lexocytes
- every lexocyte only receives its own previous token
- the encoder performs most of the meaningful computation instead of the lexocytes
- the environment fully determines behavior and tokens are irrelevant
- interaction can be removed without changing the system qualitatively

The point of `interaction-min` is to make token exchange causally real.

## Immediate Role In This Project

`INTERACTION_MIN.md` sits between:
- `LEXOCYTE_MIN.md`, which defines the organism
- later world specs, which may define persistence, viability, reproduction, or evolution

The next layer should decide:
- whether predictive performance affects persistence
- whether interaction remains purely observational or becomes strategic
- whether offspring inherit weights or a more compressed seed
