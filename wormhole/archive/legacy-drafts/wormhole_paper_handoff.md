# Wormhole Paper Handoff

## Project identity

Working title ideas:
- Charge Without Charge Revisited
- Monopole Rigidity in Traversable Wormholes
- Topological Rigidity of Asymptotic Charges in Wormhole Geometries
- Why Ordinary Charge Transport Does Not Create a Wormhole Monopole

Short description:
This project aims to make a precise, explicit, and hard-to-misread statement that asymptotic monopole charges at each wormhole end are topological sector data and cannot be changed by transporting ordinary charge through the throat. Claims or intuitions that a wormhole end acquires a new effective monopole charge when a charged particle moves through the throat are to be diagnosed as either sector confusion, gauge-choice confusion, or misreading of field-line behavior. The paper should combine a bulletproof technical statement, an explicit field calculation or visual example, and one or two intuition pumps.

## Current status

This is the current flagship gravity paper candidate.

Reason for prioritization:
- cleaner and sharper than the broad black-hole conceptual projects
- likely to support a real theorem/no-go/clarification rather than just a viewpoint
- likely publishable if written carefully
- lower novelty-risk than several other projects
- easier to know when it is actually done

Assessment:
- novelty: moderate to good
- effort: medium
- risk: low to medium
- arXiv-worthiness: yes
- likely outcome: solid technical clarification paper

## Core thesis

The main claim should be something like:

> In a two-ended wormhole spacetime, the asymptotic monopole charge measured at each end is fixed by the global topological sector (equivalently by flux data/cohomology class) and cannot be altered by local transport of ordinary charge through the throat. Interior dynamics can rearrange higher multipoles and field-line geometry, but not the asymptotic monopole data of either end.

The paper should not overclaim. It does not need to say that every discussion in the literature is wrong. It only needs to say:
- the asymptotic monopole data are rigid
- ordinary charge motion through the throat does not change those monopole data
- apparent contrary intuitions come from confusing field-line deformation with sector change

## Strongest likely result shape

Ideal result structure:

1. A precise proposition/no-go statement
   - for Maxwell (or electrostatic sector first)
   - in a two-ended wormhole background with suitable asymptotic conditions
   - showing that the asymptotic flux integral at each end is invariant under interior transport of ordinary charge, unless one changes the global topological sector / threads additional flux / changes boundary data

2. An explicit worked example
   - point charge approaching and passing through a wormhole throat on axis
   - compute the field on a symmetry-reduced slice or using an image-charge / Green-function construction if available
   - show snapshots of field lines
   - show that field lines bend/reconnect in intuitive ways but asymptotic monopole moments remain fixed

3. A conceptual explanation
   - cohomology / homotopy / Gauss-law sector viewpoint
   - distinguish local charge sources from harmonic flux sectors
   - explain why “charge without charge” means nontrivial flux sector, not charge transport generating a new monopole from nothing

4. Optional phenomenology corollary
   - higher multipoles can be induced across the wormhole, but are attenuated
   - asymptotic monopole claims used in observational papers are suspect if they rely on the wrong intuition

## What is likely actually novel

Likely novelty is not “wormhole charges exist” or “Gauss law exists.” The novelty is more likely to be one or more of:
- a particularly clean statement that asymptotic monopoles are rigid sector data
- an explicit demonstration that moving a charge through the throat does not create a new asymptotic monopole at an end
- a clear separation between sector-changing operations and ordinary interior dynamics
- a worked field-line calculation/figure that makes the correct intuition visually obvious
- a correction to a recurring mistaken interpretation in the literature

This should be framed as a technical clarification with explicit consequences, not as a grand overturning of all wormhole phenomenology.

## Likely mathematical language to use

Use whichever of these is cleanest:
- Gauss law on nontrivial topology
- asymptotic flux integrals at each end
- de Rham cohomology / nontrivial H^2 or dual statement depending on setup
- harmonic forms / flux sectors
- topological sectors not continuously connected under local dynamics
- distinction between exact and harmonic contributions to the field
- superselection-like language if useful, but only if it helps rather than obscures

Potential slogan:
- local dynamics can move sources, but cannot continuously change topological flux data

## Key intuitive picture

The reader’s wrong intuition to target is something like:
- “If I push a charge through the throat, the mouth it emerged from should look charged, so a wormhole end can acquire monopole charge dynamically.”

The paper should replace that with:
- field lines can thread the throat and then reconfigure
- the asymptotic flux at an end is not determined by naive local bookkeeping of where the particle currently is
- if the asymptotic monopole charge differs, that means you are in a different global sector, not that ordinary transport created it

## What Codex should do first

1. Search project folders for any prior drafts, notes, figures, or calculations related to:
   - wormholes
   - charge without charge
   - monopole
   - field lines
   - Krasnikov
   - Stojkovic
   - Visser
   - cohomology
   - Gauss law
   - asymptotic charge

2. Identify whether there is already:
   - a partial LaTeX draft
   - a Mathematica / Python / notebook calculation
   - a figure of field lines on a wormhole slice
   - literature notes or quotations from papers to engage

3. Build a project inventory:
   - existing files
   - what they contain
   - what is salvageable
   - what is missing

4. Then help produce:
   - a formal statement of the main proposition
   - a proof outline
   - a list of candidate explicit calculations
   - a target introduction

## Minimal success condition

A successful first phase is:
- we know exactly what files already exist
- we have one precise main proposition
- we know the easiest explicit example to compute
- we have identified the literature target(s)
- we have a realistic path to a first draft
