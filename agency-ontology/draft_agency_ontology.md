# Substrate, Structure, and the Possibility of Embedded Agency

**Draft v0.1** — December 2024  
**Authors**: [TBD]

---

## Abstract

We investigate whether the existence of embedded agents—entities that model their environment and act on those models—constrains the nature of the substrate in which they are embedded. Starting from minimal assumptions (the world exists; we are agents within it), we ask: can any arbitrary substrate be "structured" to admit agency, or do only certain substrates permit embedded observers? We present a toy model—sorting random numbers—that suggests structure can be imposed on apparently structureless data to yield regularities. This raises the question of whether the substrate/structure distinction is fundamental or whether agency is always relative to a choice of interpretation. We survey relevant literature and outline candidate approaches for making progress on this question.

---

## 1. Introduction

The question of why the universe admits observers has been approached primarily through the lens of fine-tuning: the physical constants appear calibrated to permit complex chemistry and hence life. This framing presupposes that the universe has a particular structure (specified by those constants) and asks why that structure happens to be hospitable.

We propose a more fundamental framing. Rather than asking "why is the structure hospitable?", we ask: **does the existence of embedded agents constrain the substrate at all?** 

By "substrate" we mean the underlying reality prior to any interpretation or structuring. By "structuring" we mean an organization or interpretation that reveals regularities. By "embedded agent" we mean a pattern within the substrate that:
1. Maintains some form of persistence
2. Contains a model of (part of) the substrate external to itself
3. Acts in ways informed by that model

If any substrate can be structured to admit agents, then our existence provides no evidence about what the substrate is—the constraint (if any) is purely on the structuring. If only some substrates admit agents under any structuring, then our existence is informative.

---

## 2. Useful Local Compression

A key property of our world is that it admits **useful local compression**. A small subsystem (an agent) can contain a model of a much larger system (its environment) that, while lossy, enables effective action.

Consider a bacterium navigating a sugar gradient. The bacterium, using a tiny fraction of the universe's degrees of freedom, maintains a representation (chemical concentrations, receptor states) that lets it predict and exploit local environmental structure. This is remarkable for at least three reasons:

1. **The model fits inside the agent.** The agent is much smaller than what it models.

2. **The model is useful.** Despite being lossy, it supports successful action (finding sugar).

3. **Locality suffices.** The bacterium need not model Alpha Centauri to find lunch. The world factorizes in ways that make local modeling effective.

Not all conceivable worlds would have these properties. A world with no local regularities (pure noise) would defeat any attempt at compression. A world with only global regularities (where prediction requires knowing everything) would defeat any embedded agent. Our world occupies a middle ground: local regularities, hierarchical structure, and conditional independence that permits factorization.

**Question**: Is this property of our world a fact about the substrate, or could any substrate be structured to exhibit it?

---

## 3. A Toy Model: Order from Randomness

To probe this question, we consider a minimal example: a sequence of uniform random numbers, and what happens when we impose structure by sorting.

### 3.1 Setup

Let $S = \{x_1, \ldots, x_n\}$ where each $x_i \sim \text{Uniform}(0,1)$ independently. This is, by construction, as structure-free as possible: no correlations, flat power spectrum, maximal entropy given the support.

Now define a **structuring**: sort $S$ to obtain an ordered sequence $y_1 < y_2 < \cdots < y_n$, and interpret the index $i$ as "time."

### 3.2 Result

After sorting and subtracting the linear trend (since the expected value of the $i$-th order statistic is approximately $i/(n+1)$), the residuals exhibit non-trivial structure: the power spectrum follows a power law approximately $P(f) \propto 1/f^{\beta}$ with $\beta \approx 1.8$–$2.0$, consistent with fractional Brownian motion.

### 3.3 Interpretation

This result admits two readings:

**Reading A (Regularity is revealed):** The relationships $x_i < x_j$ were always present in the data. Sorting doesn't add structure; it makes latent structure visible. The fractal residuals were "there" all along.

**Reading B (Regularity is imposed):** The fractal structure is a property of the operation "sort uniform random numbers," not of any particular realization. We brought a pattern-finding apparatus from outside.

We suggest these readings may not be in tension. The regularities are properties of the *substrate + structuring* pair, not of either alone. This raises the possibility that the substrate/structure distinction is not fundamental.

---

## 4. Implications

### 4.1 Multiple Structurings

A given substrate may admit multiple distinct structurings, each revealing different regularities. For the random sequence $S$, alternatives to sorting include:
- Defining adjacency by proximity in value (yielding a different topology)
- Grouping by ranges (yielding categorical structure)
- Computing pairwise differences (yielding relational structure)

Each structuring defines a different "world" with different emergent laws. An agent embedded in one structuring would experience regularities invisible to an agent in another structuring of the same substrate.

### 4.2 Incommensurable Observers

If agents in different structurings of the same substrate cannot perceive each other—lacking any common reference frame—then the substrate may "contain" multiple mutually invisible worlds. This is reminiscent of, but distinct from, many-worlds interpretations of quantum mechanics.

### 4.3 The Internal/External Problem

In the sorting example, the structuring was imposed from outside. The sorter was not part of the sequence. For a fully self-contained account, we would need a structuring that is *internal*: a pattern within the substrate that discovers or generates the very organization that makes it an agent.

This circularity may be unavoidable. The agent would be a kind of fixed point: the interpretation that validates itself.

---

## 5. Requirements for Agency

What properties must a substrate + structuring have to support embedded agency?

### 5.1 Tentative Necessary Conditions

1. **Dynamics**: Something time-like is needed for "action" and "persistence." A purely static structure may not support agency (though it might contain agency as a spatial pattern—this is unclear).

2. **Locality**: The dynamics must be local enough that compression is useful. Fully non-local dynamics (everything depends on everything) would make modeling impossible.

3. **Intermediate complexity**: The laws must be simple enough to model but rich enough to support complex behavior.

4. **Boundaries**: Following Fields (2016), an observer must be able to distinguish self from environment. This requires a structure that admits useful partitions.

### 5.2 Open Question

Are these conditions jointly sufficient? Can we characterize the class of substrate + structuring pairs that satisfy them?

---

## 6. Relation to Existing Work

### 6.1 Mathematical Universe Hypothesis (Tegmark)

Tegmark proposes that all mathematical structures exist physically, and observers are "self-aware substructures" (SASs) in sufficiently complex structures. He suggests only Gödel-complete structures exist, but does not rigorously characterize which structures admit SASs.

Our question is more specific: given a structure, what determines whether it admits embedded agents?

### 6.2 Assembly Theory (Cronin, Walker)

Assembly theory asks how to detect the signature of selection/agency in molecular complexity. The assembly index measures the minimal steps to construct an object. This approaches agency from the detection side rather than asking what substrates permit it.

### 6.3 Autopoiesis (Maturana, Varela)

Autopoietic systems are self-producing and self-bounding. This provides criteria for recognizing agency but does not characterize which substrates can support autopoietic organization.

### 6.4 Observer Physics (Fields)

Fields argues that observation requires boundary-drawing, and proves that embedded observers face fundamental limits on what they can access. His work addresses constraints on observation but not on which structures admit observers.

---

## 7. Directions for Progress

### 7.1 Formalizing Self-Discovering Structurings

Define rigorously what it means for a structuring to be "self-discovering": a pattern P within the substrate such that, when P is interpreted as an agent with a model, the model implies the structuring that makes P an agent.

### 7.2 Enumeration

For simple finite substrates (e.g., sequences of random numbers), enumerate possible structurings and characterize which yield agency-compatible regularities. Look for substrates that resist all structurings.

### 7.3 Information-Theoretic Characterization

Formalize agency-compatibility in terms of information: a structure admits agency iff it permits a partition into agent/environment with sufficient mutual information for prediction.

### 7.4 Toy Universes

Construct computational toy universes (cellular automata, random graphs with dynamics) and search for emergent agents. Compare substrates that succeed versus fail.

---

## 8. Conclusion

We have raised, but not answered, a fundamental question: does the existence of embedded agency constrain the substrate of reality? The sorting experiment suggests that structure can be imposed on apparently structureless data, but the "agent" in that case was external. A complete answer requires understanding when structuring can be internal—when the structure contains its own interpreter.

This question appears underexplored. The literature on observers in physics, origins of life, and foundations of mathematics circles nearby but does not directly address it. Progress may require synthesis across these fields.

---

## References

- Cronin, L., Walker, S. I., et al. (2023). Assembly theory explains and quantifies selection and evolution. *Nature*.

- Fields, C. (2016). Building the observer into the system: Toward a realistic description of human interaction with the world. *Systems*, 4(4), 32.

- Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. D. Reidel.

- Tegmark, M. (2008). The mathematical universe. *Foundations of Physics*, 38(2), 101–150.

- [LessWrong posts by shmi on order from randomness, 2018]

---

## Appendix A: Technical Details of the Sorting Experiment

[To be filled in with precise statistical analysis, code, reproducibility details]

## Appendix B: Formal Definitions

[To be filled in as concepts are made precise]

