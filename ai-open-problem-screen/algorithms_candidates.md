# Algorithms and optimization candidates

Primary index for this pass: Adrian Dumitrescu's researcher-maintained
[AlgOrEsEArch open-problems page](https://algoresearch.org/), accessed
2026-07-22. The page contains publications through 2026 and labels the items
below as open, while warning that linked collections may lag. Any item that
survives to the deep-review stage will be checked against its linked original
paper and the recent literature.

Scores use the fixed rubric in `METHODOLOGY.md`: artifact compactness (A),
verification exactness (V), search compressibility (S), representation
leverage (R), low saturation (L), and bounded-trajectory fit (T).

| # | Target | Likely success artifact | A | V | S | R | L | T | /30 | Initial note |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | Exact sorting comparison count for infinitely many `n` | decision trees plus lower bounds | 1 | 3 | 2 | 3 | 1 | 2 | 12 | Broad asymptotic program, not one compact result. |
| 2 | Selection monotonicity `V_i(n) <= V_{i+1}(n)` below the median | finite counterexample or adversary proof | 2 | 3 | 3 | 3 | 3 | 3 | 17 | Counterexample side is substantially easier to certify. |
| 3 | Determine the exact value of `V_7(16)` (currently `28..33`) | comparison decision DAG plus independently reproducible adversary computation | 3 | 4 | 4 | 4 | 2 | 4 | 21 | The answer is guaranteed and exact, but a full upper/lower certificate is not compact: the 2025 search reached a multi-billion-poset, hundreds-of-GB frontier. |
| 4 | Decide whether `V_6(17)=31` | comparison tree or adversary certificate | 5 | 5 | 5 | 3 | 3 | 5 | 26 | Same attractive shape at a slightly larger state space. |
| 5 | Decide whether `V_4(19)=29` | comparison tree or adversary certificate | 5 | 5 | 5 | 3 | 3 | 5 | 26 | Same attractive shape; exact status needs primary recheck. |
| 6 | Paterson median-comparison asymptotic constant | general algorithm and matching lower bound | 1 | 2 | 2 | 3 | 2 | 2 | 12 | Deep asymptotic proof, poor finite-certificate fit. |
| 7 | The `1/3-2/3` poset conjecture | finite poset counterexample or universal proof | 5 | 5 | 3 | 3 | 2 | 4 | 22 | Perfect verifier, but decades of structural and computational attention. |
| 8 | `X+Y` sorting in `o(n^2 log n)` | algorithm or lower bound | 2 | 3 | 2 | 3 | 3 | 3 | 16 | A new representation may help, but success is not a short witness. |
| 9 | `O(1.1^n)` exact SUBSET-SUM | algorithm and proof | 2 | 4 | 3 | 3 | 1 | 3 | 16 | Exceptionally saturated algorithmic target. |
| 10 | `O(1.99^n)` polynomial-space SUBSET-SUM | algorithm and proof | 2 | 4 | 3 | 3 | 1 | 3 | 16 | Must be checked against the newest time-space tradeoffs. |
| 11 | `O(1.1^n)` exact CLIQUE | algorithm and proof | 2 | 4 | 3 | 3 | 1 | 3 | 16 | Compact algorithm possible, but intense saturation. |
| 12 | Integer factorization in polynomial time | algorithm and proof | 1 | 3 | 1 | 4 | 1 | 1 | 11 | Clear verification does not compensate for enormous conceptual depth. |
| 13 | Strongly subquadratic 3SUM | algorithm or conditional lower-bound breakthrough | 1 | 3 | 2 | 3 | 1 | 2 | 12 | Heavily defended fine-grained-complexity target. |
| 14 | Linear-time test for planar convex position | algorithm or lower bound | 2 | 3 | 3 | 3 | 3 | 3 | 17 | Crisp target, but not a finite counterexample problem. |
| 15 | `1.99` approximation for planar Euclidean `k`-center | algorithm or hardness result | 2 | 3 | 3 | 3 | 2 | 3 | 16 | Exact geometric instances aid experimentation. |
| 16 | `1.49` approximation for metric TSP | algorithm and approximation proof | 2 | 4 | 2 | 3 | 1 | 2 | 14 | Current improvement over `3/2` is tiny; the area is highly saturated. |
| 17 | Constant approximation for TSP/MST with planar convex bodies | algorithm and charging proof | 2 | 3 | 3 | 4 | 4 | 4 | 20 | Less culturally saturated and representation-rich. |
| 18 | APX-hardness of TSP with disks or convex bodies | compact reduction | 2 | 3 | 2 | 3 | 4 | 3 | 17 | A gadget search could be model-friendly. |
| 19 | NP-hardness of Euclidean MAX-TSP, possibly noncrossing | compact reduction with geometric gadgets | 2 | 4 | 3 | 3 | 3 | 3 | 18 | Verifiable reduction, moderate geometric search space. |
| 20 | Complexity of longest noncrossing spanning tree/matching/Hamiltonian path | algorithm or reduction | 2 | 4 | 3 | 4 | 4 | 4 | 21 | Multiple encodings and finite gadget synthesis make this attractive. |
| 21 | Degree-3 plane geometric spanner with bounded stretch | universal construction or finite obstruction family | 4 | 4 | 3 | 4 | 3 | 4 | 22 | Concrete geometry plus exact finite verification. |
| 22 | Polylogarithmic coloring of 3-colorable graphs | algorithm and proof | 1 | 3 | 2 | 3 | 2 | 2 | 13 | Deep approximation frontier, not a compact artifact. |
| 23 | `0.51` approximation for maximum acyclic subgraph | algorithm or hardness reduction | 2 | 3 | 2 | 3 | 2 | 3 | 15 | Clear but saturated approximation target. |
| 24 | Constant-factor approximation for point guards in a simple polygon | algorithm or hardness result | 2 | 3 | 2 | 3 | 2 | 3 | 15 | Long-standing and technically broad. |
| 25 | Asymptotic count of simple pseudoline arrangements | combinatorial encoding and asymptotic proof | 1 | 2 | 2 | 3 | 3 | 2 | 13 | Enumeration experiments may help, but the result is not a small witness. |
| 26 | Maximum complexity of a `k`-level in a line arrangement | improved construction or universal bound | 1 | 2 | 2 | 2 | 1 | 1 | 9 | A notoriously defended incidence-geometry frontier. |
| 27 | `O(n)` maximum-area empty rectangles among `n` planar points | explicit superlinear family or universal charging proof | 3 | 5 | 4 | 4 | 4 | 4 | 24 | Strong finite-experiment loop and plausible overlooked construction. |
| 28 | Quadratic or near-quadratic triangle detection | algorithm and proof | 1 | 3 | 2 | 3 | 1 | 2 | 12 | Entangled with matrix-multiplication and fine-grained barriers. |
| 29 | `K_10` detection in `O(n^7.5)` | algorithm and proof | 2 | 3 | 2 | 3 | 4 | 3 | 17 | Specific target may admit automated tensor/meet-in-the-middle synthesis. |
| 30 | Exact TSP in `O(1.99^n)` | algorithm and proof | 2 | 3 | 2 | 3 | 1 | 2 | 13 | Extremely mature search space. |
| 31 | Polynomial-time minimum convex partition of a planar point set | algorithm or hardness reduction | 2 | 4 | 3 | 4 | 4 | 4 | 21 | Crisp problem with gadget and dynamic-programming avenues. |

## Provisional leaders from this pass

1. Exact selection, led by `V_7(16)`.  The 2025 primary result gives the
   current range `28..33`; older problem-list wording asking specifically
   whether the answer is 30 is not used here.  Larger instances remain a
   later family, not co-equal first targets.
2. The maximum-area empty-rectangle multiplicity conjecture.
3. Degree-3 bounded-stretch plane spanners.
4. Complexity of longest noncrossing spanning structures.
5. Minimum convex partition complexity.

These are susceptibility rankings, not claims of importance.
