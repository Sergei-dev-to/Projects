# ArXiv Polishing Antipatterns

Purpose: keep the arXiv pass focused on the actual result and avoid habits that have repeatedly pulled the project off course.

## Working Standard

The paper should state a precise gravity-free Hamiltonian result, identify its assumptions, derive the black-hole evaporation phenomenology that follows from them, and mark only the real remaining limitation: the assumptions are not derived from simpler non-gravitational microscopic degrees of freedom.

Polishing should make that result easier to evaluate. It should not dilute the claim, add historical narrative, or replace missing reasoning with prose.

## Antipatterns to Avoid

### Premature wrap-up

Bad pattern: declare the draft nearly done while a core assumption, consequence, symbol, or reference is still unclear.

Correction: before calling a section ready, check whether a skeptical reader can identify the input, the derivation, the output, and the limitation without reconstructing our discussion history.

### Microstepping

Bad pattern: propose small isolated fixes when the user is asking for a result-sized move.

Correction: work in passes with a clear endpoint: claims audit, assumptions/consequences audit, notation/reference audit, or final source hygiene.

### Paper-first drift

Bad pattern: optimize title, prose, section order, or review posture before the result is actually supported.

Correction: let the result control the writing. If a section does not support the result, clarify, move, or remove it.

### Invented terminology

Bad pattern: introduce phrases such as "autonomous parent", "audit test", "control value", or other labels that are not standard and are not genuinely needed.

Correction: use standard terms from the literature wherever possible: Hamiltonian, density of states, continuum modes, weak coupling, Fermi's golden rule, microcanonical shell, Haar-random isometry, Stinespring isometry, Page curve, Page's formula, scrambling time.

### LLM prose tics

Bad pattern: use slogan headings or contrastive filler such as "not X, but Y", "clean and defensible", "framework", "seam", "rate generation, not rate assignment", and repetitive "result/resulting" phrasing.

Correction: write directly. Name the claim, input, calculation, and consequence.

### Mixing phenomenology with mechanism

Bad pattern: put implementation details, diagnostics, or assumptions into the list of target black-hole phenomenology.

Correction: keep three lists separate:
- target phenomenology: thermality, finite-energy corrections, negative heat capacity, Hawking flux scalings, lifetime scaling, Page curve, early/late correlations;
- model assumptions: density of states, emission coupling, area strength, rapid mixing, typical isometries;
- diagnostics or finite checks: small model tables, energy-bin probabilities, radiation entropies.

### Underchecking literature

Bad pattern: rely on memory or invented wording for standard physics.

Correction: when wording or notation is standard, check cited papers or textbooks and align with them. The reader's effort should go into our assembly of the pieces, not decoding nonstandard notation for standard ingredients.

### Defensive framing

Bad pattern: write as if responding to a reviewer objection.

Correction: strengthen the claim or state the limitation directly. The paper should read as a self-contained result, not a resubmission.

### Hidden assumptions

Bad pattern: let an output appear to be derived when it is actually an input.

Correction: every claimed consequence must trace to a displayed assumption or derivation. Density of states, area-proportional inclusive strength, rapid mixing, and Haar-random isometries must be labeled honestly.

### Numerical-section confusion

Bad pattern: present tables before explaining what they test, use undefined symbols, include excessive significant figures, or leave zero entries unexplained.

Correction: state the expected analytic value, the computed value, the diagnostic meaning, and the takeaway. Use only meaningful precision.

### Notation sloppiness

Bad pattern: use a symbol before defining it, reuse a symbol for unrelated objects, or introduce notation that fights standard conventions.

Correction: every symbol should be standard or defined at first use. Avoid local shortcuts that save one line but cost the reader mental effort.

### Overcautious downshifting

Bad pattern: weaken "conditional Hamiltonian result" into "toy illustration" when the assumptions support more.

Correction: claim accurately. The result is conditional, but the consequences are real consequences of the stated Hamiltonian class.

### Version confusion

Bad pattern: edit the wrong draft or overwrite a prior version without making the file target explicit.

Correction: before large edits, identify the active file. Current active paper is `bh-evaporator/paper_ideal_hamiltonian/main.tex` unless the user says otherwise.

### Status inflation

Bad pattern: say "done" when the remaining work has merely changed form.

Correction: report status by remaining blockers: conceptual, derivational, numerical, reference, or prose/source hygiene.

### Losing the holy grail

Bad pattern: drift into making a publishable-looking paper rather than pursuing the project goal.

Correction: keep the goal visible: determine how much of black-hole evaporation phenomenology can be reproduced by a gravity-free quantum Hamiltonian. The current draft aims to show that the full phenomenology follows from a specified non-gravitational Hamiltonian class, while a more microscopic derivation of that class remains open.

## ArXiv Pass Checklist

Before declaring the draft arXiv-ready:

1. The title and abstract must say what the result is without hiding behind process language.
2. The introduction must separate target phenomenology, model assumptions, and consequences.
3. The main Hamiltonian must be stated before discretization or finite checks.
4. Standard ingredients must use standard terminology and cite appropriate references.
5. Each claimed evaporation feature must have a visible derivation path from the assumptions.
6. The finite-dimensional section must be clearly optional support, not the basis of the main claim.
7. The discussion must state the real limitation without hedging or apologizing.
8. The source must compile cleanly, with stable references and no stale project-history artifacts.
