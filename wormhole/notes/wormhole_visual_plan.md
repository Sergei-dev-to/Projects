# Wormhole Visual Plan

## Recommendation

Build our own animation first, then extract 4--6 paper snapshots from it.

Reason:
- I did not find a clearly suitable existing video that explains the exact point we need:
  per-end asymptotic charge stays fixed, finite Gaussian enclosed charge can change, and the harmonic sector rebookkeeps during transit.
- A custom animation guarantees that the visuals track the paper's invariants instead of generic wormhole imagery.
- If the animation is built well, snapshots for the paper become obvious rather than ad hoc.

## What The Visuals Must Teach

The visuals should separate three things that readers currently mix up:

1. Asymptotic end charges `Q_+`, `Q_-`
2. Finite Gaussian enclosed charges near each mouth
3. Harmonic/source-free bookkeeping `Q_wh`

The animation should make it impossible to confuse:
- `fixed asymptotic end charge`
with
- `changing finite enclosed charge`
or
- `changing local apparent mouth charge`

## Core Animation Sequence

### Sequence A: Approach Without Transit

Source starts far on side `+` and moves toward the throat.

Show:
- field lines / equipotentials on both sides
- one large Gaussian surface at each asymptotic end
- one smaller Gaussian surface around each mouth
- readout:
  - `Q_+ = const`
  - `Q_- = const`
  - `Q_wh = const`

Visual message:
- opposite side develops a dipolar response
- no varying opposite-end monopole appears
- mouth-local enclosed charge can vary

### Sequence B: Transit

Source crosses the throat.

Show:
- source worldline crossing the throat
- the finite Gaussian surfaces near the mouths
- the asymptotic Gaussian surfaces fixed in place
- readout:
  - `Q_+ = const`
  - `Q_- = const`
  - `Q_wh -> Q_wh ± q`

Visual message:
- transit changes the decomposition
- not the asymptotic charges

### Sequence C: Post-Transit Separation

Source emerges on side `-` and moves away from the mouth.

Show:
- exit mouth and particle both looking locally monopolar
- side `-` far field still matching the same asymptotic charge as before
- readout:
  - finite enclosed charge around mouth changes
  - finite enclosed charge around particle changes
  - asymptotic end charges still unchanged

Visual message:
- local apparent charges can rearrange
- asymptotic monopole does not

### Sequence D: Long-Throat Attenuation

Repeat Sequence A for a long thin throat.

Show:
- opposite-side dipole visibly weaker
- readout of the first few multipoles:
  - `B_0 = const`
  - `B_1`, `B_2` suppressed

Visual message:
- the allowed channels are higher multipoles
- those channels are evanescent in a long thin throat

## Paper Figures To Extract

### Figure 1: Approach Sequence

4 panels:
- far away
- intermediate
- near mouth
- just before transit

Each panel should show:
- source position
- field lines or equipotentials
- side `-` asymptotic fit label: `B_0 = 0` or `Q_- = const`

Purpose:
- show growing dipole without monopole induction

### Figure 2: Transit Bookkeeping

4 panels:
- pre-transit
- crossing
- just emerged
- well separated after emergence

Each panel should show:
- asymptotic Gaussian surfaces at both ends
- finite Gaussian surfaces around mouths
- numeric or symbolic labels for:
  - `Q_+`
  - `Q_-`
  - `Q_wh`

Purpose:
- show exactly what changes and what does not

### Figure 3: Multipoles / Attenuation

Two options:
- current multipole plot, improved with clearer labels
- or side-by-side short-throat / long-throat snapshots

Purpose:
- show that the surviving channels are higher multipoles and are attenuated

## Suggested Caption Language

Use:
- `asymptotic end charge`
- `finite Gaussian enclosed charge`
- `harmonic flux label`
- `local apparent mouth charge`

Avoid:
- `the end gains charge`
- `the wormhole acquires charge`

unless immediately qualified as:
- `in a finite-surface or local bookkeeping sense, not as an asymptotic end charge`

## Recommendation On Workflow

Best path:

1. Make one clean custom animation.
2. Export snapshots for the paper.
3. Optionally host the full video externally or as ancillary material.

Do not start from paper snapshots alone unless absolutely necessary.

Reason:
- the argument is dynamical
- the bookkeeping becomes obvious only when watched continuously
- snapshots are easier to choose once the animation exists

## External Material Search Result

Quick search did not surface a suitable existing animation for:
- Gaussian surfaces at each asymptotic end
- fixed end charges during transit
- changing finite enclosed charges near mouths
- harmonic-sector bookkeeping

So the default should be:
- build our own
- use outside material only as aesthetic inspiration
