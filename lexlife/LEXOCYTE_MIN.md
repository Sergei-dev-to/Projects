# Lexocyte-Min

## Purpose

Define the smallest unit that deserves to be called a lexocyte before specifying any ecology, reproduction, or collective dynamics.

This document is about the organism-level primitive, not the world it lives in.

## Core Idea

A lexocyte is a tiny predictive token-processing agent.

It is not just:
- a finite-state CA cell
- a lookup table
- a reactive rule node

It must have enough internal structure to:
- receive a token
- update internal state
- predict a next token
- emit a token

## Minimal Specification

At time `t`, a lexocyte has:
- `theta`: persistent parameters / weights
- `h_t`: hidden state

It receives:
- `x_t in V`: an encoded input token from a finite vocabulary `V`

It computes:
- `h_{t+1} = f_theta(h_t, x_t)`
- `q_{t+1} = p_theta(h_{t+1})`
- `e_{t+1} = g_theta(h_{t+1})`

Where:
- `f_theta` is a weighted state update
- `p_theta` is a next-token prediction head producing a distribution or ranked preference over future inputs
- `g_theta` is an emission head

Timing is:
1. receive encoded observation `x_t`
2. update hidden state to `h_{t+1}`
3. form a prediction `q_{t+1}` about the next input
4. emit `e_{t+1}`

That is the minimal loop.

Prediction is not an ornamental side output. It must be behaviorally consequential, either because:
- it directly influences later internal updates or emissions, or
- the world evaluates the lexocyte partly by predictive performance

If prediction can be removed without changing the lexocyte's role, the unit is too weak.

## Irreducible Components

The irreducible parts of a lexocyte are:

1. Token vocabulary
   A finite symbol set `V`.

2. Input channel
   The lexocyte must receive a token-like input.

3. Hidden state
   The lexocyte must retain contextual information across time.

4. Weights
   The lexocyte must contain compressed regularities in persistent parameters, not only in explicit rules.

5. Predictive head
   The lexocyte must generate a prediction about future input, not only react to current input.

6. Emission head
   The lexocyte must produce an output token that can affect other units or the environment.

If one of these is missing, the unit is probably too weak to count as lexocyte-like.

The intended status of `theta` is not "some persistent numbers happen to exist." The parameters should encode predictive bias through inheritance, learning, evolution, or selection.

## Recommended Minimal Architecture

Use a tiny recurrent agent, not attention, for the first version.

Suggested default:
- vocabulary size: `4`
- embedding size: `4`
- hidden size: `8`
- one recurrent update
- one prediction head
- one emission head

Example form:

- `h_{t+1} = tanh(W_h h_t + W_x emb(x_t) + b_h)`
- `logits_pred = W_p h_{t+1} + b_p`
- `logits_emit = W_e h_{t+1} + b_e`

Outputs:
- `q_{t+1} = argmax(logits_pred)` or sample from `softmax(logits_pred)`
- `e_{t+1} = argmax(logits_emit)` or sample from `softmax(logits_emit)`

## Design Decisions

### Recurrence Over Attention

For `lexocyte-min`, recurrence is enough.

Reason:
- simpler
- cheaper
- easier to inspect
- still supports contextual prediction

Attention can come later if recurrence proves too weak.

### Separate Prediction And Emission

Prediction and emission should be separate heads.

Reason:
- a lexocyte should distinguish between what it expects and what it says
- collapsing them too early makes the unit less expressive

### Persistent Weights

Weights are part of the lexocyte definition.

Reason:
- this is where compressed regularities live
- without weights, behavior collapses back toward rule tables and state machines
- random persistent weights are not the point; the weights should be capable of carrying inherited or learned predictive bias

## Non-Requirements

`lexocyte-min` does not require:
- transformers
- long context windows
- gradient descent during lifetime
- natural language
- human semantics
- reproduction
- death
- energy
- space or a grid

Those belong to the world model, not to the lexocyte definition.

## Interface Boundary

`x_t` is an encoded observation supplied to the lexocyte.

It may later come from:
- another lexocyte
- a neighborhood summary
- an environmental encoder

But `lexocyte-min` does not assume a particular source. It only assumes a token-like input interface.

## Boundary Test

A unit is too weak to be a lexocyte if:
- it can be replaced by a small explicit transition table without losing the essential idea
- prediction can be removed without changing behavior
- hidden state can be collapsed to a trivial finite label without losing the essential computation

The point of `lexocyte-min` is to preserve:
- weighted computation
- hidden context
- prediction
- emission

## Immediate Role In This Project

`LEXOCYTE_MIN.md` is the base ontology.

The next layer should define:
- how multiple lexocytes interact
- what constitutes the input token in a shared environment
- only after that, whether persistence, reproduction, or death belong in the world
