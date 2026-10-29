# Geometric extension and curvature prior art

Research checked on 29 October 2026 against the current `paper/main.tex`. This is a positioning review, not an independent verification of the manuscript's global proof. Primary full texts were inspected where available; the 1992 Racz--Wald paper was available as a publisher abstract and through the authors' own explicit 1996 recap. No manuscript files were changed.

## Does the planar-cap criterion follow from existing Killing-horizon extension theory?

### Takeaway

The regular constant-inaffinity horizon continuation is established Racz--Wald theory, and transverse variation of surface gravity was already known to produce a pp curvature obstruction on an actual Killing horizon. The proposed contribution is materially different: prove that *any* extension of the specified scalar-shift spacetime forces an open planar Killing-horizon patch, even though the original rounded stationary-limit wall is generally not a null horizon.

### Cited Findings

- **Racz and Wald (1992), CQG 9, 2643--2656, DOI 10.1088/0264-9381/9/12/008.** They assume a Killing-horizon hypersurface, Killing orbits diffeomorphic to the real line, and a smooth cross-section intersecting each orbit once. Nonzero surface gravity makes a generator incomplete. A nonzero surface-gravity gradient on it yields pp curvature singularity; constant nonzero surface gravity permits extension of a horizon neighborhood to a regular bifurcate horizon. These are already explicit in the primary publisher abstract. [Publisher](https://doi.org/10.1088/0264-9381/9/12/008)
- **Racz and Wald (1996), CQG 13, 539--553, arXiv:gr-qc/9507055.** Section 1 directly recapitulates both 1992 results. Its Example 1 shows global hyperbolicity plus local regular extendibility does not alone ensure a global bifurcate extension. Section 2's final assumptions include a smooth globally hyperbolic stationary spacetime, a single controlled asymptotically flat end, no white-hole region, and an appropriate Killing event horizon with compact cross-section. Theorem 4.2 then obtains a global extension; Lemma 4.1 supplies the gluing mechanism. Theorems do not require Einstein's equations. [Full text, sections 1--4](https://arxiv.org/html/gr-qc/9507055)
- **Cropp, Liberati and Visser (2013), CQG 30, 125001, arXiv:1302.2383.** Sections 2--3 distinguish peeling from inaffinity; section 4.5 treats acoustic horizons. Equations (51)--(52) define peeling and its exponential law; section 4.5.3 explains why a null candidate field need not initially be geodesic. Equations (103) and the following paragraph summarize which surface-gravity notions agree and which generically differ. This is background for careful terminology, not a warp-drive extension classification. [Full text](https://arxiv.org/html/1302.2383)
- The proposed manuscript's `eq:not-whole-sphere` and `eq:wall-normal-norm` show why ordinary rounded walls do not satisfy the starting hypothesis of Racz--Wald: their wall worldvolume is generally timelike, and the stationary null orbit is pregeodesic only on the locus G. The cap proposition explicitly constructs a known regular Killing-horizon branch. [Current manuscript](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex)

### Inferences

- **Do not advertise the local Kruskal construction or constant-kappa condition, by themselves, as the new theorem.** Attribute the regular-horizon mechanism to Racz--Wald, then explain the specialized Hausdorff attachment.
- **Strongest potentially distinctive claim:** the capture plus fixed transverse observer-disk argument forces an open planar constant-inaffinity patch from the existence of *any* Hausdorff C2 extension, without assuming beforehand that the stationary-limit wall is a Killing horizon. This is a necessity theorem about the original full spacetime, not freedom to choose a new metric on a far side. [Manuscript theorem and Appendix B](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex)
- A variable-kappa obstruction *after a genuine Killing horizon has been assumed* substantially overlaps Racz--Wald. The rounded-wall transverse Hessian obstruction, radial global inextendibility, and forced existence of a whole cap patch address hypotheses not supplied by that result. [Racz--Wald recap](https://arxiv.org/html/gr-qc/9507055); [manuscript](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex)
- Add the **1996 Racz--Wald paper** to the bibliography and discuss its local/global distinction. It is currently absent from `references.bib`; only 1992 is cited. The existing explicit closed-graph argument is useful because the 1996 black-hole hypotheses do not directly cover a finite open aperture. [Bibliography](C:/Users/serge/Projects/alcubierre-penrose/paper/references.bib)

### Gaps

- The complete original 1992 PDF was not retrieved. The relevant hypotheses and conclusions were checked against its publisher abstract and the authors' full 1996 account; do not assign an unverified 1992 theorem number.
- No claim of absolute priority follows from this bounded search. The global criterion's validity and originality still depend on the capture and transverse-neighborhood proof, which needs mathematical review independently of literature positioning.

## What do curvature-invariant papers establish, and what does an endpoint pp result add?

### Takeaway

Scalar regularity at finite spacetime points is compatible with the proposed finite-affine endpoint singularity at infinite stationary time. The paper should neither imply that the earlier scalar computations are incorrect nor infer that bounded invariants establish extendibility. There is a concrete overinterpretation in Mattingly et al.'s conclusion that the manuscript can address carefully.

### Cited Findings

- **Mattingly et al. (2021), Universe 7, 21, arXiv:2010.13693.** Section 4 plots Alcubierre invariants versus bubble parameters; Appendix A specifies a null tetrad, not a demonstration that it is parallel along the incomplete generator. Section 6 says its invariant functions contain no curvature singularities, then infers from invariant characterization that horizons would be detected by curvature singularities and suggests a coordinate transformation might remove the known causal discontinuity. Those extrapolations exceed the finite-point scalar plots. [Full text, sections 4 and 6, Appendix A](https://arxiv.org/html/2010.13693)
- **Rodal, GRG 55, article 134 (2023), DOI 10.1007/s10714-023-03182-9.** The publisher confirms publication on 18 November 2023. The same title was posted to arXiv on 23 December 2025; the bibliography's 2023 journal date with 2512.20738 is therefore not intrinsically an error. The article examines scalar invariants and criticizes graphical truncation in Mattingly et al. Section 3 distinguishes the radial shape of the wall from spherical symmetry of the full metric and rejects a class-B warped-product characterization. It does not supply a C2 endpoint-extension theorem. [Publisher metadata](https://link.springer.com/article/10.1007/s10714-023-03182-9); [arXiv full text](https://arxiv.org/html/2512.20738)
- **Racz (2010), Space-time extensions II, CQG 27, 155007, arXiv:0803.0648.** Theorem 4.2 assumes control of curvature and derivatives over a synchronized geodesic neighborhood, rather than a lone curve, and gives local C(k-minus) extension. Section 5 treats global attachment. This is relevant general context for the manuscript's emphasis on transverse neighborhoods. [Full text, Theorem 4.2 and section 5](https://arxiv.org/html/0803.0648)

### Inferences

- Use wording such as: **"Earlier invariant studies characterize the smooth finite-coordinate geometry. They do not decide whether an incomplete generator has a regular endpoint in an extension. We compute parallelly propagated tidal curvature at that endpoint and then address global inextendibility."** This leaves the earlier scalar calculations intact. [Manuscript](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex); [Mattingly](https://arxiv.org/html/2010.13693)
- If discussing Mattingly's stronger conclusion, target the scalar-regularity-to-horizon/extension inference specifically. Do not say that Mattingly numerically missed an infinite value at a finite coordinate point: the proposed endpoint is at t tending to infinity, and the divergence is in a parallel frame. [Manuscript local endpoint analysis](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex)
- The **flat-rim example** is a strong specialized illustration: its generator's pp components remain bounded, but every fixed transverse neighborhood contains divergent transported curvature. General extension theory already demands neighborhood control; the potential novelty is the explicit compact warp wall and invariant obstruction, not the abstract observation that one-ray boundedness is insufficient. [Rim proposition in manuscript](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex); [Racz](https://arxiv.org/html/0803.0648)
- Rodal's warning about symmetry supports identifying the plotted 1+1 geometry as an axial restriction. Avoid suggesting that spherical wall shape makes a full spherically symmetric quotient available. [Rodal section 3](https://arxiv.org/html/2512.20738)

### Gaps

- Narrow searches for "Alcubierre parallel-propagated", "Alcubierre non-scalar singularity", and "Alcubierre geodesic incompleteness" did not locate another independent full four-dimensional global cap-classification theorem. This is a search result, not proof of absence.
- I did not independently audit Mattingly's invariant algebra or Rodal's Petrov classification; neither is necessary to establish the endpoint-versus-finite-point distinction.

## Which optional additions are applications of established theory rather than the central novelty?

### Takeaway

Finite-duration completeness and local exact matter pulses are useful applications, but they are closely connected to established general theorems and solution families. They should not dilute the global necessity theorem. A finite-body cap-crossing proposition is more directly relevant as an operational corollary of the sharpness example.

### Cited Findings

- **Choquet-Bruhat and Cotsakis (2002), Global Hyperbolicity and Completeness, JGP 43, 345--350, arXiv:gr-qc/0201057.** Theorem 2.1 gives global hyperbolicity under controlled slicing assumptions. Theorem 3.2 gives future timelike and null completeness when lapse-gradient and extrinsic-curvature norms have integrable time bounds, with uniform lapse, shift, and spatial-metric control. In the unit-lapse flat-slice shift ansatz, an integrable uniform spatial-shift derivative bound controls the extrinsic curvature. [Full text](https://arxiv.org/html/gr-qc/0201057)
- **Galloway, Ling and Sbierski (2018), CMP 359, 937--949, arXiv:1704.00353.** Theorem 1 states that timelike completeness plus global hyperbolicity implies C0-inextendibility. Theorem 2 supplies an endpoint-reaching timelike geodesic if a smooth globally hyperbolic spacetime admits a C0 extension. These are already cited in the manuscript and are the general tools underlying its reduction to captured exits and the optional finite-duration corollary. [Full text, Theorems 1--2](https://arxiv.org/html/1704.00353v4)
- **Podolsky and Ortaggio (2003), CQG 20, 1685--1701, arXiv:gr-qc/0212073.** Sections 3--4 describe exact Kundt waves of arbitrary profile on backgrounds including Minkowski and Plebanski--Hacyan products, with cosmological constant, electromagnetic fields and radiation; section 4.4 considers test particles. The proposed pp/Kundt local cap pulse uses this established family. [Full text](https://arxiv.org/html/gr-qc/0212073)
- **Krtous, Podolsky, Zelnikov and Kadlecova (2012), PRD 86, 044039, arXiv:1201.2813.** Sections IV--VI develop exact radiation/gyraton solutions on direct-product Einstein--Maxwell backgrounds, with transverse field equations. This is supporting prior art for the curved-cap pulse construction rather than a new warp-extension theorem. [Full text](https://arxiv.org/html/1201.2813)
- The project's matter notes distinguish test-body crossings, local exact null-matter examples, and the uncompleted coupled compact-wall/massive-body evolution problem. These are correct scope boundaries to preserve. [Flat-cap crossing notes](C:/Users/serge/Projects/alcubierre-penrose/notes/flat_cap_matter_crossing.md); [source-family notes](C:/Users/serge/Projects/alcubierre-penrose/notes/stationary_cap_matter_families.md)

### Inferences

- Rank the paper's potential contribution as: (1) global necessary-and-sufficient scalar-shift extension criterion; (2) rounded radial endpoint/global inextendibility result; (3) compact sharpness example with invariant rim obstruction and, optionally, finite test-body accessibility. The known regular Killing-horizon construction supplies the sufficiency mechanism. [Current manuscript](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex)
- Finite-duration completeness is a short specialized application of existing slicing theorems plus the C0-inextendibility theorem, not the best principal novelty claim. [Choquet-Bruhat--Cotsakis](https://arxiv.org/html/gr-qc/0201057); [Galloway--Ling--Sbierski](https://arxiv.org/html/1704.00353v4)
- Exact local matter transit is mathematically useful but should be described as an application of known pp/Kundt solutions, not a new exact-solution family or a proof of generic stability/global self-gravitating portal engineering. [Podolsky--Ortaggio](https://arxiv.org/html/gr-qc/0212073); [matter notes](C:/Users/serge/Projects/alcubierre-penrose/notes/flat_cap_matter_crossing.md)
- Suggested narrowly defensible positioning: **"We determine which reduced continuations survive restoration of the transverse directions. In a specified stationary scalar-shift class, any C2 extension forces an open planar constant-inaffinity Killing-horizon patch. Standard regular-horizon continuation realizes precisely that exceptional branch; rounded radial walls are globally inextendible."** This is a proposed contribution statement, conditional on the manuscript proof surviving independent scrutiny, not an absolute priority assertion. [Manuscript](C:/Users/serge/Projects/alcubierre-penrose/paper/main.tex)

### Gaps

- No independent peer review of the proposed theorem has been performed here. Literature comparison cannot certify its proof.
- Optional massive self-gravitating transit needs constraint-satisfying coupled wall/passenger data; the cited local evolution theory alone does not create that data. [Source-family notes, section 7](C:/Users/serge/Projects/alcubierre-penrose/notes/stationary_cap_matter_families.md)
- This task did not classify all possible maximal cap completions, cyclic quotients, M--H properties, or new asymptotic ends. They are not needed for the proposed positioning.
