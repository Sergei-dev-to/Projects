# Prior-art audit: square-lift rigidity for central-configuration curves

**Audit date:** 2026-07-22

**Status:** finite, pre-registered literature audit.  This document records
the corpus and search concepts fixed before the final searches were run.  A
negative search result is not a priority proof; it supports only the wording
"no equivalent result was found in this audit."

## Question being audited

For fixed strictly positive Newtonian masses, suppose a nonconstant
collision-free fixed-inertia family of central configurations has an
irreducible algebraic curve as its full labelled projective squared-distance
image.  Is it already known that the distance radicals split in the curve's
function field, that the normalized squared-distance map factors through
coordinatewise squaring, or that the curve has even projective degree and
degree at least four?

## Fixed primary corpus

1. Albouy--Chenciner (1998), mutual-distance equations.
2. Roberts (1999), signed five-body continuum.
3. Albouy--Kaloshin (2012), five-body finiteness and constant critical
   values on continua.
4. Hachmeister--Little--McGhee--Pelayo--Sasarita (2013), negative-mass
   continua and neutral configurations.
5. Dias (2017), algebraic/mutual-distance finiteness methods.
6. Gasull--Lazaro--Torregrosa (2019), rational parametrization of radical
   equations in celestial mechanics.
7. Jensen--Leykin (2023/2025), tropical generic finiteness.
8. Chang--Chen (2024, 2025), symbolic six-body finiteness program.
9. Moczurad--Zgliczynski (2026), certified exceptional five-body fibers.
10. References and forward citations reached directly from items 1--9 when
    their titles or abstracts use one of the fixed concepts below.

## Fixed search concepts

The searches combine `central configurations` with each of:

- `square class`, `multiquadratic`, `Kummer`, `radical extension`;
- `coordinatewise square`, `distance cover`, `rational distances`;
- `projective degree`, `even degree`, `degree parity`;
- `conic`, `rational curve`, `algebraic curve`, together with mutual or
  squared distances.

No additional mechanism will be added to the audit in response to the search
results.  Adjacent results are recorded, but only an explicit theorem or
proof implication counts as overlap.

## Source matrix

| Source | Result relevant to this note | Overlap with proposed theorem | Evidence | Audit verdict |
|---|---|---|---|---|
| [Albouy--Chenciner (1998)](https://doi.org/10.1007/s002220050200) | Intrinsic and mutual-distance formulations of balanced and central configurations; the foundational squared-distance equations. | Supplies the ambient algebraic language. No theorem about positive radical splitting, square lifts of curve normalizations, or parity of curve degree was located. | Full paper inspected, especially the mutual-distance formulation. | **Adjacent framework; not equivalent.** |
| [Roberts (1999)](https://doi.org/10.1016/S0167-2789(98)00315-7) | Constructs the fixed-mass signed \(1+\)rhombus continuum; on \(I=1\), \(U=4\). It also extends the family to homogeneous and logarithmic potentials. | Supplies the sharp signed counterexample. Its linear squared-distance image demonstrates why positivity is essential, but it does not state a positive-mass splitting or degree theorem. | Full source inspected; theorem and concluding remarks. | **Sharpness example; not overlap.** |
| [Albouy--Kaloshin (2012)](https://doi.org/10.4007/annals.2012.176.1.10) | Proves generic planar five-body finiteness. Lemma 2 proves that \(U\) has finitely many values on their algebraic solution set, hence is constant on each continuum; the paper then studies singular sequences and \(zw\)-diagrams. | This is the closest antecedent to the first proof step. The paper does not group the positive terms of \(U=\sum w_e/r_e\) by square class, split the distance cover, or infer a projective-degree restriction. | Full paper inspected; pp. 541--544 and the continuum arguments. | **One key ingredient; proposed implication not found.** |
| [Hachmeister--Little--McGhee--Pelayo--Sasarita (2013)](https://doi.org/10.1007/s10569-013-9471-1) | Reinterprets Roberts and constructs higher even-dimensional continua, each with one negative mass. | Shows that signed cancellation is structural and generalizable. It does not give the claimed positive-mass obstruction or a degree classification of distance curves. | Abstract and author presentation inspected. | **Signed-continuum prior art; not overlap.** |
| [Dias (2017)](https://doi.org/10.1090/proc/13427) | Gives trilinear homogeneous central-configuration equations and places mutual-distance vectors of fixed-dimensional configurations in determinantal algebraic sets; proves a generic finiteness result. | Treats algebraic sets in mutual-distance variables, but not the function field of a positive physical curve and not square classes, a coordinatewise square lift, or degree parity. | Full arXiv text inspected, especially Theorem 2.2 and Proposition 3.5. | **Adjacent algebraic framework; not equivalent.** |
| [Gasull--Lazaro--Torregrosa (2019)](https://doi.org/10.1007/s12346-018-0300-5) | Uses rational parametrizations to turn selected systems involving square roots into polynomial problems, including symmetric celestial-mechanics examples. | This is the closest methodological neighbor to "make radicands squares." It introduces auxiliary covers or genus-zero parametrizations for particular systems; it does not prove that positivity and constant \(U\) force every distance radical to lie in the original curve function field. | Full paper inspected, especially Sections 1, 3, and 4. | **Close technique; logically different.** |
| [Jensen--Leykin (2023)](https://arxiv.org/abs/2301.02305) | Uses tropical geometry and computation to prove generic finiteness through \(n=5\). | Addresses generic fibers and tropical solvability, not fixed exceptional continua or their distance-curve square classes and projective degrees. | Full arXiv text and stated main result inspected. | **Different finiteness method; not overlap.** |
| [Chang--Chen I (2024)](https://doi.org/10.1016/j.jsc.2023.102277); [II (2025)](https://doi.org/10.1137/24M1716070) | Automates \(zw\)-diagram, asymptotic-order, elimination, and mass-relation analysis for the planar six-body problem. | Studies possible singular sequences at infinity. No square-lift or low-degree distance-curve theorem appears in the stated results or searchable full text. | Part I abstract/full preprint and Part II article page inspected. | **Different obstruction program; not overlap.** |
| [Moczurad--Zgliczynski (2026)](https://arxiv.org/abs/2601.01165) | Gives computer-assisted exact counts for several exceptional five-body mass tuples left outside earlier generic finiteness theorems. | Certifies particular zero-dimensional fibers; it does not constrain a hypothetical algebraic continuum by radical splitting or projective degree. | Full local TeX source and arXiv abstract inspected. | **Complementary certification; not overlap.** |
| [Ferrario (2017)](https://arxiv.org/abs/1608.00480) (item 10 search hit) | Reformulates central configurations using mutual differences and cochains. | An invariant mutual-difference formulation, but no function-field radical or curve-degree result. | Abstract and full arXiv text searched through the fixed concepts. | **Adjacent reformulation; not equivalent.** |

## Search log

| Query family | Relevant primary hits | Equivalent theorem found? |
|---|---|---|
| Square classes / multiquadratic / Kummer / radical extension | No fixed-corpus source using these concepts for a central-configuration continuum was returned. Albouy--Kaloshin was the relevant result reached through "continuum," but stops at constancy of \(U\). | **No.** |
| Coordinatewise squaring / distance cover / rational distances | Gasull--Lazaro--Torregrosa rationalize selected radical equations; Ferrario reformulates mutual differences. | **No.** Neither asserts that the full distance cover splits over the normalization of a positive continuum. |
| Projective degree / even degree / degree parity | Searches returned central-configuration papers using polynomial degree, not a theorem about the projective degree of a physical distance curve. | **No.** |
| Conics / rational or algebraic curves in mutual distances | Dias's determinantal distance varieties and Albouy--Kaloshin's algebraic-continuum arguments were relevant; specialized symmetric classifications also appeared. | **No.** No exclusion by degree \(1,2,3\), or coordinatewise-square factorization, was found. |

## Final novelty wording

The audit found the ingredients separately but not their combination.
Constancy of \(U\) on a central-configuration continuum is explicit in
Albouy--Kaloshin; mutual-distance algebraic geometry is standard from
Albouy--Chenciner onward; multiquadratic basis independence and the
line-bundle calculation are standard algebra.  What appears original in this
program is the implication

\[
\text{positive fixed-mass continuum}
\Longrightarrow
\text{all normalized }s_{ij}\text{ are squares in }\mathbb R(\widetilde C)
\Longrightarrow
\text{coordinatewise square lift and }\deg C\ge4.
\]

Gasull--Lazaro--Torregrosa is the closest technique-level neighbor, but its
direction is constructive and case-specific: pass to a rational auxiliary
parametrization to solve equations containing radicals.  The present
direction is a rigidity statement: positivity forces an already existing
physical curve's entire multiquadratic distance cover to split over its own
function field.

The defensible novelty claim is therefore:

> We found no equivalent square-lift or low-degree-barrier theorem in the
> pre-registered primary corpus or in the fixed concept searches.  The proof
> combines known ingredients into an apparently new structural necessary
> condition for an algebraic positive-mass counterexample.

This is not a priority claim.  Before submission it should receive an expert
bibliographic check, especially from researchers working on
mutual-distance equations and algebraic finiteness.  Mathematically, the
result is a self-contained structural theorem; it does not solve Smale's
sixth problem or prove finiteness for a new mass family.
