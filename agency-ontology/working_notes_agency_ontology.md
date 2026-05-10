# Working Notes: Agency, Structure, and the Compressibility of Worlds

**Status**: Exploratory working notes  
**Date started**: December 2024  
**Participants**: Sergei (shmi), Claude

---

## The Core Question

**Can any substrate be structured to admit embedded agency, or does "admitting embedded agents" constrain what the substrate can be?**

If the answer is "any substrate works," then the existence of agency tells us nothing about the underlying reality—agency is purely in the interpretation.

If the answer is "only some substrates work," then our existence as agents is evidence about the nature of the world.

---

## Starting Assumptions and Observations

### The Assumption
The world just *is*—everything else is a (tiny) part of it. This is minimal and relatively uncontroversial for a physicalist. We do not assume:
- 3+1 dimensions
- Time as fundamental
- Determinism
- Any particular physics

### The Observation
We humans exist and are embedded agents in the world. What defines an agent is unclear, but possibilities include:
- Dennett's intentional stance (predictive utility of treating something as having beliefs/goals)
- Any long-lasting pattern that has an internal model and acts to advance emergent goals (like persisting)

---

## Key Concept: Useful Local Compression

The world appears to be **lossily compressible from the inside**. A tiny part (an agent—bacterium, human) can have a model of the world that is:
- Greatly simplified (lossy)
- Fits inside the agent
- Nonetheless useful for the agent's goals

This is remarkable. Not all imaginable worlds would have this property.

### Why this is surprising

Consider extremes:
- **Maximally chaotic world**: No local compression helps because there's no exploitable structure. Past doesn't predict future, nearby doesn't resemble nearby.
- **Holistically structured world**: Structure exists but is only accessible globally—you need to know everything to predict anything.

Our world sits in a middle zone:
- Local regularities (physics is the same here and there)
- Hierarchical structure (chemistry → biology)
- Conditional independence (Alpha Centauri doesn't matter for the bacterium's sugar gradient)

The world seems to **factorize** in ways that make local modeling possible.

---

## The Sorting Experiment (Sergei, 2018)

**Source**: 
- [Physics has laws, the Universe might not](https://www.lesswrong.com/posts/aCuahwMSvbAsToK22/physics-has-laws-the-universe-might-not)
- [Order from Randomness](https://www.lesswrong.com/posts/2FZxTKTAtDs2bnfCh/order-from-randomness-ordering-the-universe-of-random)

### Setup
1. Generate 1024 uniform random numbers in [0,1]
2. Sort them (ascending)
3. Interpret index as "time," value as state
4. Subtract linear trend
5. Examine residuals

### Result
The residuals show **fractal structure** with power spectrum ~1/f^1.86 (close to Brownian motion's 1/f^2).

### Interpretation
Sorting imposes a structure (monotonicity) that reveals regularities not present in the unordered sequence. The regularity (fractal residuals) is a property of **sorting uniform random numbers**, not of the specific realization.

**Key question raised**: Is the regularity "in" the substrate, or in the operation? 

**Possible answer**: Regularity is always a relationship between substrate and structuring, never a property of substrate alone.

---

## The Internal/External Problem

Cellular automata (Game of Life, Rule 110, etc.) have rules imposed from outside. The rules are not encoded in the grid—they're executed by an external entity (the mathematician, the computer).

This is unsatisfying if we want a self-contained world. Our physics isn't "written on a tablet outside the universe"—it's immanent in the structure.

**Question**: What mathematical structures have rules that are *in* the world rather than *over* it?

**Sergei's insight about sorting**: If sorting "reveals" structure that was already implicit in the relationships between numbers (0.237 < 0.891 was always true), maybe the internal/external distinction is less sharp than it seems. The sorted and unsorted sequence are the same object viewed differently.

---

## Multiple Structurings of the Same Substrate

A random set of N numbers admits many structurings:
- Sort by value (monotonicity, fractal residuals)
- Define adjacency by closeness in value (topological structure)
- Group by some property (categorical structure)
- Compute pairwise differences (relational structure)

Each reveals different regularities. An "agent" in one structuring might experience a completely different "world" than an agent in another structuring of the same substrate.

**Implication**: Agents in different structurings might be mutually incommensurable—not invisible to each other in the usual sense, but lacking any common reference frame (time, space, causality).

---

## What Would Agency Require?

Tentative necessary conditions for a structuring to support agency:

1. **Dynamics** (something time-like): A static structure has no "action" or "persistence through change"

2. **Locality of dynamics**: If everything couples to everything, compression is useless—your neighborhood doesn't determine what happens to you

3. **Intermediate complexity of laws**: Too simple (static or fully random) → no exploitable structure. Too complex (incompressible laws) → can't model them.

4. **Asymmetry/gradients**: Agents need "direction"—something to do, somewhere to go

5. **Boundaries**: (Chris Fields) Observers must distinguish self from environment. Not all structures admit useful boundary-drawing.

---

## Literature Survey: What's Relevant

### Directly relevant

**Chris Fields** - "Building the Observer into the System" (2016)
- Observation requires boundaries
- "No-boundary theorem": embedded observer can't have independent access to systems within observable universe
- Observer and observable form closed system from observer's perspective
- Key insight: boundary-drawing is a constraint

**Assembly Theory** (Cronin/Walker)
- Assembly index measures how much history/selection needed to produce something
- High assembly → agency was likely involved
- Approaches from detection angle, not "what permits agency"

**Tegmark's MUH**
- Observers are "self-aware substructures" (SASs) in sufficiently complex mathematical structures
- Claims only Gödel-complete structures exist physically
- Doesn't characterize "complex enough" rigorously

**Autopoiesis** (Maturana/Varela)
- Living systems produce their own components and boundaries
- Operational closure + structural coupling with environment
- Criterion for agency, but doesn't say which substrates support it

### Adjacent but less directly relevant

- Kolmogorov complexity (structure = compressibility, but no connection to embedded agency)
- Gödel/self-reference literature (limits of self-description, but different question)
- Constructor theory (what transformations are possible, not what observers are possible)

### The gap

Nobody seems to have directly addressed: given an arbitrary substrate, under what conditions can it be structured to admit embedded agents?

---

## Candidate Directions for Progress

### Direction 1: Characterize "self-discovering" structurings

Can we define what it means for a structuring to be self-discovering? A pattern within the structure that, when interpreted as an agent, would itself discover the structuring that makes it an agent.

This is circular but maybe necessarily so—the agent as fixed point of interpretation.

**Task**: Construct simplest toy system where this happens.

### Direction 2: Enumerate structurings of simple substrates

For a finite random sequence:
- How many distinct structurings exist?
- What regularities does each yield?
- Which yield enough regularity for modeling?

Computational approach. Might reveal that some substrates admit many agency-compatible structurings, others few/none.

### Direction 3: Formalize boundary requirements

Chris Fields' approach, made precise:
- Structure admits agency iff it permits partition into agent/environment such that agent-part can encode predictive information about environment-part
- Connect to mutual information, conditional independence

### Direction 4: Anthropic testing

If any substrate works → our existence says nothing about substrate
If only some substrates work → our existence is evidence

Testable in toy universes: generate random substrates, exhaustively search for agency-compatible structurings, see if some consistently fail.

---

## Open Questions

1. Is "structuring" well-defined? What counts as a legitimate structuring vs. arbitrary imposition?

2. Can we separate "substrate" from "structuring" at all, or are they always entangled?

3. Does the sorting experiment actually tell us anything, or is it just "you can find patterns in anything if you look hard enough"?

4. What role does dynamics play? Is a static structure ever agency-compatible?

5. Is there a minimum substrate size/complexity below which no structuring yields agency?

6. How does this relate to the measure problem in cosmology? (Weighting over possible structures)

---

## Technical Details to Work Out

### Formalizing the sorting experiment

- **Substrate**: Set S = {x₁, ..., xₙ} where xᵢ ~ Uniform(0,1) i.i.d.
- **Structuring**: Ordering σ such that x_{σ(1)} < x_{σ(2)} < ... < x_{σ(n)}
- **Regularity**: Power spectrum of detrended sequence
- **Agency-compatible**: ???

### Why fractal residuals emerge

When you sort uniform random numbers, gaps between consecutive order statistics are approximately exponentially distributed. Cumulative sum of mean-centered gaps ≈ random walk → Brownian motion in continuous limit → power spectrum ~1/f².

The regularity is in the *operation on the distribution*, not the specific realization.

---

## Next Steps

1. Reproduce the sorting experiment, try variations
2. Try other structurings on same random data
3. Attempt to formalize "agency-compatible structuring"
4. Look more carefully at Fields' boundary formalism
5. Design a toy system where the structuring is "internal"

---

## Random Thoughts / Parking Lot

- Is the universe a random substrate we're structured into, or a structured substrate we're embedded in? Does the distinction matter?

- The Many Worlds interpretation: different branches as different "structurings"?

- What would a truly structure-less substrate even be? Can we define it?

- Relation to constructor theory: maybe the question is about which *transformations* are possible, and agents are transformations that model their own transformation-context?

- If consciousness is the hard part, should we bracket it and focus on agency/modeling first?

