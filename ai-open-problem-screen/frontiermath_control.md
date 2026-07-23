# FrontierMath Open Problems control pass

Status cut: **2026-07-22**.  This pass was added as an external control because
Epoch's collection was independently designed around publishability and
programmatic verification.  It is not treated as an unbiased source: OpenAI
has verifier access, the targets have been shown to frontier systems, and the
site stopped displaying failed attempts in June 2026.  Exposure therefore
lowers low-saturation scores.

> **Post-campaign correction (2026-07-23).** The stretched-LR entry was later
> rescored to about 19 after checking the primary statement and attempting the
> campaign. Its row below is retained as historical input; `CLOSURE.md` records
> the terminal assessment.

Scores use the common order A/V/S/R/L/T.  Twelve clean targets are scored.
Three additional entries are excluded because of a solved status or a live
resolution claim.

| Target | Status/artifact | A/V/S/R/L/T | /30 | Audit note |
|---|---|---|---:|---|
| Hadamard matrix of order 668 | sign matrix; exact integer verifier | 5/5/3/5/2/4 | 24 | Strong existence prior, but classical searches and a 2026 AI-led Legendre-pair campaign lower `L`. |
| Ramsey numbers for book graphs | explicit graph family plus exact Ramsey check | 3/4/3/4/3/3 | 20 | A general construction, not one isolated graph, is needed for the tight bound. |
| Infinitely many solutions to specified small Diophantine equations | parametric family and proof | 3/3/4/4/4/3 | 21 | Bounded equations, but infinitude is not a one-object certificate. |
| Arithmetic Kakeya construction | explicit combinatorial objects improving a bound | 4/5/4/4/3/4 | 24 | Strong construction loop; exposed to frontier models. |
| Degree versus sensitivity | explicit Boolean-function family and proof | 4/5/4/4/3/4 | 24 | Exact truth tables at finite sizes help, but the exponent requires a family. |
| Large Steiner system (`5<t<10`, `v<200`) | incidence block list; trivial exact checker | 5/5/3/5/3/3 | 24 | No nontrivial system with `t>5` is known; existence below 200 is uncertain. |
| Polynomial with Galois group `M_23` | degree-23 polynomial; exact algebra/group computation | 5/4/3/5/3/2 | 22 | Major upside and strong existence prior, but the desired locus is extremely thin. |
| Negative stretched Littlewood--Richardson coefficient | three partitions; exact LR/Ehrhart computation | 5/5/4/5/2/4 | 25 | Problem author expects false; current model exposure is the main penalty. |
| Symplectic ball packing | explicit embeddings plus inequalities | 4/3/3/5/3/3 | 21 | Constructive, but exact symplectic verification carries hidden analytic geometry. |
| Apery-style irrationality proof | recurrences/integrals plus full proof | 2/3/2/5/2/2 | 16 | High conceptual burden and no guaranteed small artifact. |
| Faster prime factorization | algorithm and complexity proof | 1/3/1/4/1/1 | 11 | Exceptionally saturated; included as a negative control. |
| Algorithm deciding unknotting number one | general algorithm and proof | 1/3/2/4/3/2 | 15 | Verification of examples is not verification of the universal algorithm. |

## Excluded after current-status audit

- **Ramsey-style hypergraph construction:** marked solved by AI on the live
  benchmark.
- **Characteristic-3 KLT del Pezzo surface with eight singularities:** a
  March 2026 manuscript claims a full seven-point upper theorem.  The clean
  next task is proof adjudication, not construction search.
- **Absolute Galois group of `Q_2`:** Epoch's 2026-07-06 update reports
  verifier-accepted presentations from Claude Fable 5 and GPT-5.5 Pro and
  says they are likely correct, with full proofs still being checked.  This
  is a live-claim case under the common gate, not an open attack target.
