# Discrete-mathematics candidate screen

Status cut: **2026-07-22**.  This is a deliberately skeptical screen of 35
targets in graph theory, combinatorics, finite geometry, design theory, Ramsey
theory, and discrete geometry.  The unit being scored is the most concrete
attack target attached to a problem, not the prestige of its parent
conjecture.

Every retained item has a recent primary paper, a researcher-maintained
survey/database, or an official problem-list entry that still treats it as
open.  I separately searched for recent solution and counterexample claims.
Items with a live full-resolution claim were withheld even when the claim is
unrefereed; see the exclusion log at the end.  “Open” below therefore means
“open on this status cut under this audit,” not a permanent guarantee.

## Scoring and interpretation

The six scores are each 0--5, in this order:

- **F — finite certificate:** success can be a compact graph, matrix, array,
  coloring, or proof object;
- **V — exact verification:** the decisive check is exact arithmetic,
  SAT/DRAT, exhaustive enumeration, or short hand verification;
- **B — bounded/searchable class:** the target has a fixed size, strong normal
  form, or compressible parameter space;
- **R — representation gap:** there is plausible unused leverage from a new
  encoding, duality, transfer, or invariant;
- **L — low saturation:** 5 means little modern targeted search, 0 means the
  relevant class has already been exhausted heavily;
- **M — manageable trajectory:** a model can plausibly load the needed
  background, operate tools, and criticize candidates in a bounded campaign.

The unweighted total is out of 30.  Easy verification is not the same thing as
easy discovery, and a high score is not a probability of success.

## Inventory at a glance

| # | Target | Area | F/V/B/R/L/M | Total |
|---:|---|---|---|---:|
| 1 | Hadamard matrix of order 668 | design theory | 5/5/4/5/4/4 | **27** |
| 2 | Three MOLS of order 10 | design theory | 5/5/5/4/1/4 | **24** |
| 3 | Conway 99-graph | algebraic graph theory | 5/5/5/4/2/4 | **25** |
| 4 | Projective plane of order 12 | finite geometry | 5/5/4/4/1/3 | **22** |
| 5 | Maximal determinant in order 23 | design theory / matrices | 4/3/5/4/2/3 | **21** |
| 6 | Moore graph of degree 57 | algebraic graph theory | 5/5/3/4/1/2 | **20** |
| 7 | Erdős--Gyárfás power-of-two cycle | graph theory | 5/5/3/4/3/4 | **24** |
| 8 | Tree independence-polynomial unimodality | enumerative graph theory | 5/5/4/3/0/4 | **21** |
| 9 | Gallai path decomposition | graph decomposition | 4/4/3/4/3/4 | **22** |
| 10 | Tuza triangle packing/covering | extremal graph theory | 5/4/3/4/2/4 | **22** |
| 11 | Erdős--Lovász Tihany | chromatic graph theory | 4/3/2/3/3/2 | **17** |
| 12 | Caccetta--Häggkvist | directed graphs | 5/5/3/4/2/4 | **23** |
| 13 | Graceful Tree Conjecture | graph labeling | 5/4/3/3/1/5 | **21** |
| 14 | Perfect 1-factorisation of `K_64` | graph designs | 5/5/5/4/3/4 | **26** |
| 15 | Ryser odd Latin-square transversal | Latin squares | 5/4/3/4/2/4 | **22** |
| 16 | Stein one-sided rainbow matching | rainbow matchings | 5/4/3/5/5/4 | **26** |
| 17 | Brouwer matching conjecture for STS | design theory | 5/4/3/4/4/4 | **24** |
| 18 | Ryser hypergraph covering | hypergraph theory | 5/4/3/4/3/3 | **22** |
| 19 | Exact `R(5,5)` | Ramsey theory | 5/4/5/3/0/3 | **20** |
| 20 | Exact `R(4,6)` | Ramsey theory | 5/4/5/3/0/2 | **19** |
| 21 | Exact Schur number `S(6)` | Ramsey/additive combinatorics | 5/5/5/3/1/4 | **23** |
| 22 | Exact van der Waerden number `W(2,7)` | Ramsey theory | 5/5/4/4/2/2 | **22** |
| 23 | Kissing number in dimension 5 | discrete geometry | 4/3/3/4/2/2 | **18** |
| 24 | No-three-in-line, `2n` question | grid geometry | 4/3/4/3/2/4 | **20** |
| 25 | Chromatic number of the plane | geometric graph theory | 3/3/3/4/1/2 | **16** |
| 26 | Planar `k`-set problem | computational geometry | 2/2/1/4/3/1 | **13** |
| 27 | Erdős--Rado sunflower conjecture | extremal set theory | 2/3/2/4/2/2 | **15** |
| 28 | Sidorenko's conjecture | extremal graph theory | 3/3/2/4/3/1 | **16** |
| 29 | Turán's `(3,4)` conjecture | extremal hypergraphs | 3/3/2/4/1/2 | **15** |
| 30 | Conway thrackle conjecture | topological graph drawing | 4/3/3/4/3/2 | **19** |
| 31 | List Edge-Coloring Conjecture | graph coloring | 5/4/3/4/3/3 | **22** |
| 32 | Total Coloring Conjecture | graph coloring | 5/4/3/3/2/3 | **20** |
| 33 | Hadwiger's conjecture, first open case | graph minors | 5/4/2/3/1/1 | **16** |
| 34 | Berge--Fulkerson conjecture | cubic graphs / matchings | 5/4/3/4/2/4 | **22** |
| 35 | Tutte 5-flow conjecture | graph flows | 5/4/3/4/2/4 | **22** |

## A. Fixed finite designs and graphs

| # | Statement and current status evidence | Witness / proof type and exact verifier | Smallest plausible artifact | Prior computational saturation | Structural opening |
|---:|---|---|---|---|---|
| **1** | **Hadamard 668.** Construct a `668 x 668` sign matrix `H` with `HH^T = 668 I`.  [Epoch's live problem page](https://epoch.ai/frontiermath/open-problems/hadamard) says 668 is the smallest unknown order, records only 5--10 serious attempts, and was accessed on this status cut. | Pure construction.  **Verifier available:** yes; parse `+1/-1` entries and multiply exactly over the integers. | A CSV containing 446,224 signs.  No explanatory proof is needed for correctness, though a construction principle would make the result publishable. | Low for this exact order despite a large Hadamard literature; the maintained survey estimates only 5--10 serious attempts. | Search over construction grammars rather than entries: block-circulant, supplementary-difference-set, cocyclic, spectral, and hybrid templates; use equivalence-aware canonicalization and exact completion. |
| **2** | **Three mutually orthogonal Latin squares of order 10.**  [Bright--Keita--Stevens (EJC 2026)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i1p30) says existence remains open and audits Myrvold's restricted cases with SAT. | Pure construction.  **Verifier available:** yes; check each square is Latin and that every ordered pair of symbols occurs once for each pair of squares. | Three `10 x 10` arrays, 300 entries total. | Very high historically.  The 2026 SAT work closes 20 restricted pair types and finds pairs in eight remaining types, but does not globally encode the third square. | The paper itself exposes the gap: pair-first search is inadequate.  Joint three-square encodings, transversal-composition duality, orbit-aware exact cover, and learned symmetry breaking are still plausible. |
| **3** | **Conway 99-graph.** Decide whether a strongly regular graph with parameters `(99,14,1,2)` exists.  [Cesarz--Woldar, Algebraic Combinatorics 2025](https://alco.centre-mersenne.org/articles/10.5802/alco.418/) explicitly calls existence an elusive open problem and sharpens automorphism restrictions. | Construction or nonexistence proof.  **Positive verifier available:** yes; check a 99-vertex adjacency matrix has degree 14, one common neighbor for adjacent pairs, and two for nonadjacent pairs.  Negative certificates would require exhaustive SAT/association-scheme proof. | A 99-by-99 zero-one adjacency matrix (or 693-edge list). | Decades of algebraic restrictions and symmetry-specific searches; not a complete search because a putative graph may have tiny or trivial automorphism group. | Stop assuming useful automorphisms.  Encode local neighborhoods, coherent configurations, eigenspaces, and canonical augmentation simultaneously; search the asymmetric residue rather than another group-action case. |
| **4** | **Projective plane of order 12.** Decide whether a projective plane of non-prime-power order 12 exists.  A 2025 primary paper on cyclic planes states that [order 12 is the smallest unknown case](https://arxiv.org/abs/2510.19804); recent finite-geometry notes continue to list it as open. | Construction or certified exhaustive nonexistence.  **Positive verifier available:** yes; check a `157 x 157` incidence matrix has row/column sum 13 and every pair of rows and columns intersects once.  Negative verification is much harder. | A 157-point/157-line incidence list, 2,041 incidences. | Very high conceptually, but nothing close to the complete order-10-style enumeration at order 12.  Many arithmetic and subgroup cases are excluded. | Combine incidence coding, ternary-ring identities, code constraints, and isomorph-free SAT; learned partial-plane completion may expose a small forbidden core or an unexpected non-Desarguesian template. |
| **5** | **Maximal determinant, order 23.** Determine the maximum absolute determinant of a `23 x 23` sign matrix.  The researcher-maintained [OEIS entry A003433](https://oeis.org/A003433) was updated in July 2026; order 23 remains the smallest order with unknown exact maximum. | Optimization: a better matrix gives a lower bound; exact resolution also needs an upper certificate.  **Verifier available:** determinant is exact, but a global upper certificate is not standardized. | A 23-by-23 sign matrix plus either a rational Gram-matrix exclusion or a complete canonical enumeration proving optimality. | High: switching, Gram-matrix, and equivalence-class methods resolved every smaller order.  Order 23 has resisted them. | Search in the much smaller space of feasible integral Gram matrices, then decompose; combine lattice/Hasse invariants, SDP bounds converted to rationals, and certified canonical augmentation. |
| **6** | **Missing Moore graph.** Decide existence of a degree-57, diameter-2 Moore graph, equivalently an SRG with parameters `(3250,57,0,1)`.  [Ishida, June 2026](https://arxiv.org/abs/2606.29183) explicitly says existence remains open and rules out involutions. | Construction or nonexistence proof.  **Positive verifier available:** yes; check 3,250 vertices, degree 57, no triangles or 4-cycles, and every nonadjacent pair has one common neighbor. | A 92,625-edge list. | Extremely high theoretical saturation and several failed/nonaccepted nonexistence claims; direct heuristic optimization has remained very far from zero deficit. | A construction would probably need algebraic compression: permutation systems, modules, association schemes, or a lift/cover.  Blind edge search is not credible at this scale. |

## B. Graph, Latin-square, and hypergraph counterexample targets

| # | Statement and current status evidence | Witness / proof type and exact verifier | Smallest plausible artifact | Prior computational saturation | Structural opening |
|---:|---|---|---|---|---|
| **7** | **Erdős--Gyárfás.** Every graph of minimum degree at least 3 contains a cycle whose length is a power of two.  The live [Erdős problem #64 status](https://demath.org/problems/erdos-gyarfas-cycles) is open; Liu--Montgomery settled sufficiently large minimum degree, leaving degree 3. | A counterexample is a finite graph.  **Verifier available:** yes; check minimum degree and enumerate simple cycles, rejecting lengths `2^k`. | A preferably cubic graph, adjacency list, and independently reproduced cycle inventory. | Moderate.  Small and structured graph families have been searched, but there is no bounded theorem reducing the conjecture to a completed range. | Treat allowed cycle lengths as a semigroup/covering constraint; generate lifts, voltage graphs, substitutions, or products whose cycle spectra are controlled symbolically rather than screening random cubic graphs. |
| **8** | **Tree independence polynomial unimodality.** Is the independence polynomial of every tree unimodal?  The March 2026 [artifact and paper](https://zenodo.org/records/19100781) states the conjecture remains open and checks all 8,691,747,673 trees on at most 29 vertices. | Counterexample tree.  **Verifier available:** yes; tree DP computes the exact coefficient sequence and a single descent-then-rise disproves unimodality. | A tree on at least 30 vertices plus its exact independence-polynomial coefficients. | **Maximal for naive size search:** every tree through 29 is exhausted, with structural reductions and spider-family analysis. | Search grammar space rather than tree space: recursively compose rooted-tree independence pairs and optimize coefficient-shape invariants; use adversarial dynamic programming to target two separated modes. |
| **9** | **Gallai path decomposition.** Every connected `n`-vertex graph has an edge decomposition into at most `ceil(n/2)` paths.  A [February 2026 paper](https://www.sciencedirect.com/science/article/pii/S0012365X25004388) still states the conjecture and proves another Eulerian special case. | Counterexample graph plus nondecomposability certificate, or a proof.  **Verifier available:** SAT/ILP can encode path partitions; DRAT or exhaustive canonical certificates are possible but not off-the-shelf. | A connected graph and a checkable UNSAT proof for every partition into `ceil(n/2)` paths. | Many graph classes are settled; direct isomorph-free global census appears much less saturated than the theorem literature. | Encode a path decomposition as endpoint parity plus trail connectivity, separating the easy linear constraints from subtour cuts; mine minimal UNSAT cores for structural lemmas. |
| **10** | **Tuza.** For every graph, the minimum number `tau` of edges meeting all triangles is at most twice the maximum number `nu` of edge-disjoint triangles.  [Bennett et al., June 2026](https://arxiv.org/abs/2606.09736) proves a random-geometric case; the general conjecture remains open. | Counterexample graph with `tau > 2 nu`.  **Verifier available:** yes in principle; independent ILP/SAT certificates establish both optima. | A graph plus a maximum-packing certificate, a minimum-cover lower certificate, and exact inequality. | Considerable LP/packing theory and many graph classes; no exhaustive census of reduced critical graphs at meaningful orders. | Work on the triangle hypergraph, enforcing graph-realizability while searching integrality-gap extremizers; symmetry-free critical-core generation may find configurations missed by family-based proofs. |
| **11** | **Erdős--Lovász Tihany.** If `chi(G)=k>omega(G)` and `a,b>=2`, `a+b=k+1`, must `G` contain disjoint subgraphs of chromatic number at least `a` and `b`?  [Erdős #628](https://www.erdosproblems.com/forum/thread/628?order=newest) was last edited December 2025 and reports no full claim. | Counterexample graph plus chromatic and non-splitting certificates.  **Verifier available:** partly; coloring/UNSAT certificates are exact, but quantifying all vertex bipartitions is expensive. | A graph, chosen `(a,b)`, proof of `chi>omega`, and one DRAT certificate for the combined split encoding. | Deep special-case literature, but relatively little direct global computation. | Encode the entire split existential in one SAT instance and search critical graphs under modular decomposition; complement/induced-subgraph views may reveal a smaller obstruction language. |
| **12** | **Caccetta--Häggkvist.** Every `n`-vertex digraph with minimum outdegree at least `n/r` contains a directed cycle of length at most `r`.  AIM's [problem workshop notes](https://aimath.org/WWN/caccetta/caccetta.pdf) and 2026 papers continue to treat it as open. | A counterexample is a finite digraph for some `r`.  **Verifier available:** yes; check outdegrees and directed girth exactly. | A loopless digraph adjacency list with `delta^+ >= ceil(n/r)` and directed girth greater than `r`. | One of the most studied directed-extremal problems; many parameters and dense regimes are settled.  Exhaustive search is limited by unbounded `n,r`. | Use Cayley/voltage digraphs, additive-set encodings, or blow-ups with an exact cycle-language constraint; search symbolic families rather than isolated adjacency matrices. |
| **13** | **Graceful Tree Conjecture.** Every tree with `m` edges labels its vertices injectively by `0,...,m` so that edge differences are exactly `1,...,m`.  A [2026 graph-labeling article](https://actamath.savbb.sk/pdf/aumb28.pdf) still calls the general problem wide open; the exhaustive [tree computation](https://arxiv.org/abs/1003.3045) reaches 35 vertices. | Counterexample tree plus proof of no graceful labeling.  **Verifier available:** SAT/CP with a DRAT-like proof or exhaustive backtracking certificate. | A tree on at least 36 vertices and an UNSAT certificate for the all-different difference constraints. | Very high naive saturation through 35 vertices and vast family-specific theory. | Search recursively for obstruction gadgets in the difference constraint graph; learn nogoods transferable across rooted-tree compositions instead of enumerating the 36-vertex frontier flatly. |
| **14** | **Perfect 1-factorisation of `K_64`.** Partition the edges of `K_64` into 63 perfect matchings such that every pair forms a Hamilton cycle.  [Glock--Sgueglia](https://borowiecki.dev/pdf/2510.01949) identifies 64 as the current smallest open order; a July 2026 paper says the general conjecture remains far from solved. | Pure construction.  **Verifier available:** yes; check edge partition, matching property, and 1-cycle union for all 1,953 matching pairs. | Sixty-three lists of 32 disjoint edges. | Moderate.  `K_56`, the former smallest case, required a bespoke construction; `K_64` is current and has not been exhaustively searched modulo all equivalences. | Translate to row-Hamiltonian quasigroups/Latin squares; search algebraic operations, starters, group extensions, and switched near-factorisations, with exact local-repair scoring. |
| **15** | **Ryser's odd-order transversal conjecture.** Every odd-order Latin square has a full transversal.  Montgomery's [researcher survey](https://rhmontgomery.warwick.ac.uk/papers/37transversalssurvey.pdf) says the odd case remains beyond the methods that prove the large-even near-transversal result. | Counterexample odd Latin square plus proof of no transversal.  **Verifier available:** exact-cover SAT and DRAT. | An odd `n x n` Latin square and an UNSAT proof for a rainbow perfect matching in `K_{n,n}`. | Latin squares are enumerated only at small orders; theory is intense, but the counterexample search beyond group tables is not globally exhausted. | Jointly synthesize the square and a compact obstruction to every rainbow matching; exploit trades, parity signatures, and hypergraph dual certificates rather than sample random Latin squares. |
| **16** | **Stein's surviving one-sided rainbow-matching conjecture.** Every edge-coloring of `K_{n,n-1}` that is proper at each vertex in the larger part has a rainbow matching of size `n-1`.  Montgomery's [survey, Section 6.4](https://rhmontgomery.warwick.ac.uk/papers/37transversalssurvey.pdf) explicitly says this formulation remains widely open. | Counterexample coloring plus no-rainbow-matching certificate.  **Verifier available:** SAT/DRAT or exact matching-with-colors ILP. | A colored complete bipartite graph, probably at modest `n`, together with a short UNSAT certificate. | Low.  Stein's stronger equi-`n` conjectures drew the counterexamples; this one-sided survivor has far less systematic computation. | This is a representation-gap target: switch among arrays, colored bipartite graphs, 3-partite hypergraphs, and matroid intersection; co-synthesize a coloring and a Hall-type dual obstruction. |
| **17** | **Brouwer's Steiner-triple-system matching conjecture.** Every Steiner triple system of order `n` has a matching of at least `(n-4)/3` triples (integer-rounded as necessary).  Montgomery's [current survey, Conjecture 6.1](https://rhmontgomery.warwick.ac.uk/papers/37transversalssurvey.pdf) lists it open and tight for infinite families. | Counterexample STS plus matching-number certificate.  **Verifier available:** check every pair occurs once; certify maximum 3-set packing by ILP/SAT. | A block list for an STS and a DRAT/ILP certificate that its matching number is below the bound. | Small STSs are heavily classified, but there is no modern global search targeted at extremal matching deficiency across construction grammars. | Search Wilson/fundamental constructions with matching deficiency as a composable invariant; dual fractional covers and absorber failures may guide exact counterexample synthesis. |
| **18** | **Ryser hypergraph covering.** Every `r`-partite `r`-uniform hypergraph satisfies `tau <= (r-1) nu`.  [Clow--Haxell--Mohar 2025](https://arxiv.org/abs/2505.05339) disproves a stronger Lovász conjecture while stating Ryser remains open for all `r>=4`. | Counterexample hypergraph plus exact matching and cover optima.  **Verifier available:** ILP/SAT with dual/cutting-plane certificates. | A small `r`-partite incidence list, most plausibly `r=4`, with `tau>(r-1)nu`. | Strong theory, many intersecting/equality cases, but limited exhaustive generation outside highly symmetric examples. | Repurpose the failed stronger-conjecture counterexample mechanism; search line hypergraphs and products of distance-regular graphs while optimizing the cover/matching gap directly. |

## C. Exact Ramsey-type constants

| # | Statement and current status evidence | Witness / proof type and exact verifier | Smallest plausible artifact | Prior computational saturation | Structural opening |
|---:|---|---|---|---|---|
| **19** | **Determine `R(5,5)`.** The April 24, 2026 edition of Radziszowski's [Small Ramsey Numbers](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1) records `43 <= R(5,5) <= 46`; the current upper bound has a separate [computational proof](https://arxiv.org/abs/2409.15709). | Lower bound: a graph avoiding a 5-clique and a 5-independent set.  Upper bound: exhaustive SAT/canonical proof.  **Verifier available:** yes for a graph; DRAT plus independently checked enumeration for an upper bound. | A Ramsey graph on 43, 44, or 45 vertices to improve the lower bound, or a complete proof certificate at the first forced order. | Extreme.  This is a flagship computational Ramsey target with decades of optimized generation and a recent independent upper-bound implementation. | A genuinely new quotient is needed: degree-sequence gluing, neighborhood type algebras, or proof-producing symmetry handling.  More local search is unlikely to matter. |
| **20** | **Determine `R(4,6)`.** The same April 2026 [dynamic survey](https://www.combinatorics.org/ojs/index.php/eljc/article/view/DS1) records `36 <= R(4,6) <= 41`. | Lower graph or upper exhaustive proof.  **Verifier available:** direct clique/independent-set checking for a lower witness; DRAT/canonical certificates for an upper result. | A `(4,6)`-Ramsey graph at a new order, or a complete nonexistence certificate between 36 and 41. | Extreme.  Extensive handcrafted and SAT searches already target precisely these small orders. | Cross-order gluing and reusable proof certificates for neighborhood subproblems are more promising than another monolithic encoding. |
| **21** | **Determine `S(6)`.** The six-color Schur number is not known exactly.  A July 16, 2026 [template paper](https://arxiv.org/abs/2607.15034) uses the current lower bound `S(6)>=536`; the best published general upper bound remains far larger (see [Heule 2020](https://arxiv.org/abs/2006.01502)). | Lower bound: color an initial interval with six sum-free color classes.  Upper bound: SAT/DRAT proof that all longer colorings fail.  **Verifier available:** yes. | A 6-color string extending the 536 construction, ideally with a short generative template; exact settlement needs an upper certificate too. | High but not exhausted.  The July 2026 shifted-template improvement was itself discovered in an AI conversation, showing the representation space is still live. | Search over composable templates, affine shifts, substitutions, and automata rather than raw color strings; require exact expansion and a tiny checker. |
| **22** | **Determine `W(2,7)`.** The maintained [Leaps in Bounds entry](https://leapsinbounds.org/constants/van-der-waerden-2-7/) gives the best explicit lower bound `3704` and no matching practical upper bound; the exact value is open. | Lower bound: a binary string with no monochromatic 7-term AP.  Upper bound: exhaustive proof.  **Verifier available:** yes for a coloring; SAT/DRAT for a finite upper range. | A length-3704-or-longer binary coloring, preferably generated by a cyclic/zipper rule. | Moderate-high, but the listed lower record dates to 2012, much less active than small Ramsey graphs. | Treat colorings as cyclic words, morphic sequences, or codewords and synthesize the generator; exploit AP orbits and spectral constraints before SAT completion. |

## D. Discrete and computational geometry

| # | Statement and current status evidence | Witness / proof type and exact verifier | Smallest plausible artifact | Prior computational saturation | Structural opening |
|---:|---|---|---|---|---|
| **23** | **Kissing number in dimension 5.** Determine the maximum number of unit spheres touching one unit sphere in five dimensions.  A July 2026 [Discrete & Computational Geometry paper](https://link.springer.com/article/10.1007/s00454-026-00841-x) gives the current interval `40 <= tau_5 <= 44`. | A larger spherical code improves the lower bound; an exact semidefinite/geometric proof gives an upper bound.  **Verifier available:** exact for rational/algebraic coordinates, less simple for numerical coordinates and global upper bounds. | Forty-one or more vectors in `R^5` with pairwise inner products at most `1/2`, with exact coordinates and interval-checked inequalities. | High: strong SDP, lattice, and spherical-code searches; the four-value gap remains. | Symmetry breaking may be the wrong prior.  Search low-degree algebraic Gram matrices and contact graphs jointly, then reconstruct exact coordinates from high precision. |
| **24** | **No-three-in-line `2n` problem.** Can every `n x n` grid contain `2n` points with no three collinear?  The live [OEIS record A272651](https://oeis.org/A272651) was updated July 2026 and reports `2n` through all exhaustively settled small orders (through 66) plus constructions at additional larger orders. | A construction settles a new `n`; a negative answer needs a proof that the maximum is below `2n`.  **Verifier available:** exact collinearity check for constructions; SAT/ILP proof for nonexistence. | A list of `2n` integer lattice points for the first currently untreated `n`, or a DRAT certificate proving a first failure. | High at small orders, including exhaustive computation through 66; not saturated for structured infinite construction rules. | Synthesize modular permutations, Costas-like arrays, and unions of graphs of functions over residue rings; prove no-three-collinear by determinant identities rather than check each `n` separately. |
| **25** | **Chromatic number of the plane.** Determine which of 5, 6, or 7 equals `chi(R^2)`.  [Erdős problem #508](https://www.erdosproblems.com/508) was edited January 2026 with bounds 5--7; June 2026 work still develops finite unit-distance obstructions. | A finite 6-chromatic unit-distance graph raises the lower bound; an explicit 5- or 6-coloring of the whole plane lowers the upper bound.  **Verifier available:** graph coloring is certifiable, but exact unit-distance realization and whole-plane coverage require care. | A finite graph with exact algebraic planar coordinates and a DRAT proof of chromatic number at least 6. | Very high after the 2018 jump to five, including SAT, neural, and geometric search. | Search graph and realization simultaneously through distance-constraint algebra, rather than first finding an abstract graph; certify coordinates by minimal polynomials and intervals. |
| **26** | **Planar `k`-set problem.** Determine the correct asymptotic maximum number of `k`-sets of `n` planar points.  The maintained [Open Problems Project entry](https://topp.openproblem.net/p7) still records a large gap between upper and lower bounds. | Usually an asymptotic construction or proof, not a one-shot artifact.  **Verifier available:** finite configurations can be checked, but they do not settle the asymptotic problem. | A parametrized point construction with a symbolic count, or a new incidence inequality with a checkable recurrence. | Extremely deep geometric-combinatorial literature; the main gap is theoretical, not an unattended finite search. | Oriented matroids and allowable sequences can move geometry into discrete word systems, but this representation is already known; novelty would require a new transfer invariant. |

## E. Structural conjectures with finite counterexample modes

| # | Statement and current status evidence | Witness / proof type and exact verifier | Smallest plausible artifact | Prior computational saturation | Structural opening |
|---:|---|---|---|---|---|
| **27** | **Erdős--Rado sunflower.** For each fixed petal count `r`, is every sufficiently large `k`-uniform family forced to contain an `r`-sunflower with a bound `C_r^k`?  Rao's 2026 [JLMS survey/article](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/jlms.70380) says the original conjecture remains open. | Proof or an infinite lower-bound construction; a single finite family cannot refute the existence of a constant.  **Verifier available:** exact for finite instances, not for the asymptotic leap. | A compact recursive family with superexponential size and a proof of sunflower avoidance, or a new robust-sunflower inequality. | Very high after the 2019--2021 breakthroughs; specialists have explored entropy, random restrictions, and robust sunflowers intensely. | Mechanize the search for stronger intermediate structures and entropy potentials, but expect theory rather than a Fable-like finite witness. |
| **28** | **Sidorenko.** Every bipartite graph `H` has homomorphism density at least the random-graph benchmark in every graphon.  A 2025 [Forum of Mathematics, Sigma paper](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/local-aspects-of-the-sidorenko-property-for-linear-equations/9A01CA2ED3DCD4E742D205B1A17ED88F) explicitly says the graph conjecture remains open. | Proof, or a bipartite `H` and graphon violating the inequality.  **Verifier available:** a rational step graphon would give an exact finite polynomial inequality; global proof is not turnkey. | A small bipartite graph and rational weighted adjacency matrix whose exactly computed densities violate Sidorenko. | Active and sophisticated; many graph classes and flag/entropy methods are known, but no counterexample for ordinary graphs. | Exhaustively search rational step graphons jointly with previously unresolved `H`, then use real algebraic optimization to turn numerical gaps into exact inequalities. |
| **29** | **Turán's `(3,4)` conjecture.** Determine the extremal density of a 3-uniform hypergraph with no tetrahedron `K_4^3`; Turán's construction predicts `5/9`.  A 2025 [Advances in Mathematics paper](https://pikhurko.github.io/E/Pikhurko25am.pdf) continues to list the original tetrahedron problem among the central open cases. | Proof or an asymptotic construction beating the conjectured density.  **Verifier available:** a finite blow-up template can be checked exactly; an upper proof may use rational flag-algebra certificates. | A small weighted 3-graph template whose blow-ups are tetrahedron-free and exceed `5/9`, with rational weights. | Extreme: 85 years of extremal theory and extensive flag-algebra SDP. | Search nonhomogeneous iterated blow-ups and algebraic substitution systems, asking for an exact identity; ordinary finite 3-graph optimization is saturated. |
| **30** | **Conway thrackle.** A planar thrackle on `n` vertices has at most `n` edges.  [Hernández-Vélez--Kynčl--Salazar 2025](https://arxiv.org/abs/2506.11808) explicitly says the planar conjecture remains open and records the best linear upper bound. | Counterexample graph plus a valid topological drawing, or proof.  **Verifier available:** possible with a combinatorial rotation/crossing-order certificate, but no universally standard checker. | A graph with more edges than vertices and a pseudosegment crossing word certifying every edge pair meets exactly once. | Moderate.  There was a computational approach, but the continuous-looking drawing space has not been exhaustively discretized. | Make realizability combinatorial: oriented matroids, wiring diagrams, and SAT over crossing orders; the key is a complete equivalence between the certificate and a planar thrackle drawing. |
| **31** | **List Edge-Coloring Conjecture.** Every loopless multigraph has list chromatic index equal to chromatic index.  A 2025 [Acta Mathematica Sinica paper](https://doi.org/10.1007/s10114-025-2761-1) still calls the general conjecture open while settling more planar cases. | Counterexample graph and adversarial lists.  **Verifier available:** show ordinary edge-coloring at `k`, then give `k`-element lists and a DRAT proof that no list edge-coloring exists. | A simple or low-multiplicity graph, a list assignment, one ordinary coloring, and one UNSAT certificate. | Many classes and small maximum degrees are proved; direct co-search over graph plus list assignment is comparatively unsaturated. | Co-synthesize the graph and bad lists, quotienting color renamings; mine Hall-type obstructions in the line graph rather than test arbitrary list instances. |
| **32** | **Total Coloring Conjecture.** Every simple graph has a total coloring with at most `Delta+2` colors.  [Glock--Kühn--Lo--Osthus 2025](https://arxiv.org/abs/2507.05548) proves dense cases; the general conjecture remains open. | Counterexample graph needing `Delta+3` colors.  **Verifier available:** SAT/DRAT for total-coloring nonexistence. | A graph plus an UNSAT certificate for `Delta+2` colors and a coloring with `Delta+3`. | Very high theoretical saturation; many degree ranges and classes are known.  Less complete is a canonical census of critical graphs at moderate order. | Search total-color-critical graphs directly using line-graph-square constraints and minimal-UNSAT cores; transfer obstructions from list coloring. |
| **33** | **Hadwiger, first open case.** Every graph with chromatic number at least 7 contains a `K_7` minor.  A 2025 [JCTB paper](https://www.sciencedirect.com/science/article/abs/pii/S0095895625000619) says Hadwiger remains wide open for every `t>=7`. | Counterexample graph plus certificates of 7-chromaticity and no `K_7` minor.  **Verifier available:** coloring proof is routine; a compact no-minor certificate may require tree decompositions or exhaustive branch-set search. | A 7-chromatic graph, DRAT proof of no 6-coloring, and independently checkable no-`K_7`-minor certificate. | Among the most saturated and structurally defended problems in graph theory. | Any viable hunt should target a tightly defined graph grammar where minor exclusion is structural, not brute-force arbitrary graphs. |
| **34** | **Berge--Fulkerson.** Every bridgeless cubic graph has six perfect matchings such that every edge lies in exactly two.  A 2025 [Discrete Applied Mathematics paper](https://www.sciencedirect.com/science/article/pii/S0166218X25000599) continues to state the conjecture while proving more snark families. | Counterexample cubic graph plus nonexistence certificate.  **Verifier available:** enumerate perfect matchings and solve a small exact-cover/SAT instance; DRAT certifies failure. | A cyclically highly connected snark and a DRAT proof that no required six-matchings multiset exists. | High: snarks and perfect-matching cover indices have been enumerated to meaningful sizes, and many products are known. | Generate snarks adversarially against the matching-incidence polytope, using cuts/faces as learned constraints; search graph grammar and dual obstruction together. |
| **35** | **Tutte 5-flow.** Every bridgeless graph has a nowhere-zero 5-flow.  [Li--Su 2025](https://www.ort.shu.edu.cn/EN/10.15960/j.cnki.issn.1007-6093.2025.03.006) says it remains unresolved and proves Euler-genus at most 20. | Counterexample graph plus proof no 5-flow.  **Verifier available:** modular-flow existence is a finite CSP; DRAT/SMT can certify nonexistence. | A highly connected snark and an UNSAT certificate for all nowhere-zero `Z_5` flows. | High.  Reductions to snarks and computational work on circular flow number are mature; snarks through at least 36 vertices have been classified for relevant flow behavior. | Search signed/gadget substitutions that force incompatible boundary-flow signatures.  Compose exact signature tables so a large obstruction can be verified locally. |

## Top six for an AI-led campaign

These are not the six most famous problems.  They are the six for which the
shape of a successful result most resembles the recent AI-assisted pattern:
a constrained but non-obvious search space, a compact artifact, a tiny exact
checker, and a credible representation gap.

### 1. Hadamard 668 — best one-shot artifact target

Why it ranks first: it is fixed, constructive, overwhelmingly believed to have
a solution, and the checker is integer matrix multiplication.  The unusually
low number of serious attacks on this exact order matters more than the age of
the general Hadamard conjecture.  A model can search *languages of
constructions*—difference families, block arrays, cocycles, and hybrid
completions—while independent agents verify every candidate.

The pre-registered first experiment should reproduce the known order-428
construction from the same grammar, then search a finite catalogue of
equivalence-reduced templates at 668.  Stop that branch if it cannot recover
428 or if every predeclared template class is exhausted; do not silently widen
to random `668^2` bit search.

### 2. Perfect 1-factorisation of `K_64` — best compact graph-design target

The answer, if positive, is only 63 matchings and every condition is local and
exact.  More importantly, 64 is the *current first hole*, so a result has a
clean publication story without proving Kotzig's whole conjecture.  The
row-Hamiltonian Latin-square/quasigroup encoding supplies several genuinely
different search geometries.

A bounded experiment is to enumerate algebraic starter and extension
templates, with switching repair, after validating the pipeline on `K_56`.
Stop after the declared template families are either exhausted or shown to be
isomorphic to known failed families.

### 3. Stein one-sided rainbow matching — best underexplored counterexample bet

This survived after several stronger Stein conjectures were disproved, but it
has not inherited their computational attention.  A counterexample is a small
colored complete bipartite graph plus a DRAT certificate.  Four equivalent
languages—array, colored graph, 3-partite hypergraph, and constrained matroid
intersection—create exactly the sort of representation gap an agent can sift.

The first experiment should perform an isomorph-free census for a declared
range of `n`, co-synthesizing both the coloring and a dual obstruction.  Even a
negative census with new reducibility lemmas is publishable structural
mathematics.  Stop at the predeclared `n` once completeness and certificate
checking are independently reproduced.

### 4. Conway 99-graph — best fixed algebraic-graph target

The positive artifact is tiny and perfectly checkable, while the literature's
casework has concentrated on possible automorphisms.  The opening is precisely
the asymmetric residue: a global local-neighborhood/coherent-configuration
encoding that does not assume a useful group action.

This ranks below the first three because 99 vertices already produce a hard
SRG completion problem and decades of specialist constraints defend it.  A
bounded first experiment should measure whether known spectral and local
constraints propagate substantially in an automorphism-free SAT model.  Stop
if the model cannot solve reconstructed smaller SRG controls or leaves the
99-case essentially unconstrained.

### 5. Three MOLS of order 10 — best mature SAT target with a named gap

The 2026 paper gives a particularly sharp opening: the remaining Myrvold cases
cannot be eliminated by considering only an orthogonal pair; the third square
has to enter jointly.  The artifact is 300 symbols and the verifier is trivial.
This is much better specified than a generic “try SAT again” proposal.

It ranks fifth because the problem has enormous prior saturation.  The bounded
experiment is a joint triple encoding of the eight surviving restricted cases,
with composition/transversal duality and proof logging.  Stop when those eight
cases are either solved or certified resistant under the fixed encoding; do
not claim that failure covers unrestricted triples.

### 6. Erdős--Gyárfás — best graph counterexample-mechanism target

A single finite graph would end the conjecture and checking it is elementary.
The high-leverage move is not to enumerate cubic graphs one order at a time,
but to synthesize voltage lifts, substitutions, or products with a *symbolic
cycle spectrum*.  That mirrors the lesson from recent counterexamples: search
for an identity or fibration that manufactures the artifact, not for a lucky
adjacency matrix.

The bounded experiment should specify a finite lift/base-graph grammar and
derive all possible cycle lengths algebraically before graph generation.  Stop
after that grammar is exhausted.  Brouwer's STS matching conjecture is the
closest alternate at the same score if this cycle-spectrum grammar shows no
compression.

## Near misses and why they did not make the top six

- **Brouwer STS matching (24/30)** is genuinely undercomputed and has excellent
  certificates.  It narrowly loses to Erdős--Gyárfás because its smallest
  plausible counterexample scale is less clear, but it is the first reserve.
- **Projective plane 12 (22/30)** and **Moore 57 (20/30)** have perfect positive
  verifiers but likely artifacts are enormous and are defended by decades of
  arithmetic/algebraic restrictions.
- **Schur `S(6)` (23/30)** has a live template representation, but finding a
  better lower coloring is not the same as determining the exact number; the
  upper side remains much harder.
- **Tree independence unimodality (21/30)** is a beautiful counterexample
  shape, but 8.69 billion trees through 29 have already been exhausted.  Only
  a compositional coefficient-space search justifies another campaign.
- **Famous mega-problems** such as Hadwiger, Turán `(3,4)`, sunflower, and the
  planar `k`-set problem score poorly because even a finite computation is
  unlikely to bridge the asymptotic or structural gap.

## Conservative exclusion and claim log

The following were encountered during status checking and are **not** among
the 35 scored candidates:

- **Cycle Double Cover Conjecture:** full OpenAI proof announced July 2026;
  excluded while that claim is audited rather than treating it as open.
- **1--2--3 Conjecture:** resolved affirmatively by Keusch; the later paper
  [“A solution to the 1-2-3 conjecture”](https://www.sciencedirect.com/science/article/pii/S0095895624000030)
  is not merely a variant result.
- **Barnette's conjecture:** a March 2026 Zenodo/Synapse manuscript explicitly
  claims a proof.  The claim is not established here, but the conservative
  gate removes the item instead of scoring it as unambiguously open.
- **Union-closed sets conjecture:** current authoritative surveys still call it
  open, but a June 2026 manuscript claims a full proof.  Withheld under the
  same claim gate.
- **Lonely Runner Conjecture:** current primary work verifies cases through 13
  runners and still treats the general problem as open, but a March 2026
  manuscript titled “A Complete Proof” is live.  Withheld rather than
  adjudicating that manuscript in this screen.
- **The 1/3--2/3 poset conjecture:** a March 2026 full-proof claim was found;
  withheld.
- **Circulant Hadamard conjecture** and **Alon--Tarsi Latin-square conjecture:**
  arXiv manuscripts claim full proofs; withheld under the same rule.
- **Stein's equi-`n`-square `n-1` conjecture:** not open—it was disproved by
  Pokrovskiy--Sudakov.  Item 16 is a different, explicitly surviving Stein
  conjecture.
- **Erdős's near-linear planar unit-distance conjecture:** disproved in May
  2026; the still-open true growth-rate problem is too nonspecific for this
  certificate screen.
- **Graph reconstruction and Erdős--Hajnal:** current literature/search pages
  produced conflicting or easily misread 2026 status signals.  Neither was
  needed to reach 35, so both were withheld pending a dedicated claim audit.

## Bottom line

The strongest cluster is not “famous graph conjectures.”  It is **fixed finite
design holes with exact positive verifiers**, followed by **underexplored
counterexample formulations whose nonexistence side can be proof-logged**.
The screen therefore favors Hadamard 668, `K_64` perfect 1-factorisation, and
Stein's one-sided rainbow matching over much more prestigious asymptotic
problems.  That ranking is exactly what the six-factor rubric is supposed to
do.
