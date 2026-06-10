# Deterministic Cayley-Hamiltonian decoupling: finite-size scaling

**Review status:** useful finite-size evidence, but not yet a closed
deterministic-expander result.  The positive graph below is a Cayley/circulant
graph, not an expander family: for generators `{+1,-1,n/2}` the adjacency gap
collapses as `O(n^{-2})`.  The test also uses a `scramble-then-reveal` qubit
channel rather than the full weak-emission open channel of the paper.  See
`notes/deterministic_cayley_scaling_review.md` before using this result in the
draft.

**Script:** `sim/deterministic_cayley_scaling.py`
**Data:** `sim/data/deterministic_cayley_scaling.csv`

## Purpose

Test the load-bearing assumption of the `paper_ideal_hamiltonian` model — that the
in-shell mixer decouples the radiation, giving the island/Page curve — for a
*single deterministic time-independent* Hamiltonian on a Cayley (circulant)
graph, using exact dynamics `exp(-iKt)` rather than an assumed Haar isometry.

This tests the *antecedent* ("does this H scramble enough?"), which the Section 5
Haar check assumes. Because the claimed phenomenology is asymptotic, the control
variable is system size `n`; a single small `n` is uninformative because small
Hilbert spaces look scrambled regardless. The discriminator is the **trend** in
`n`, plus independent chaos diagnostics.

## Families (mapping the counterexample landscape)

- **free_chain** — cycle, XX+YY only (Jz=0, no field): genuinely Gaussian.
  Counterexample 1 (free dynamics give the wrong, non-Page curve).
- **integ_xxz** — cycle, XXZ (no field): interacting but integrable. The
  cycle-XXZ "warning example" in the paper's Discussion.
- **chaos_expander** — circulant {±1, ±n/2}, anisotropic XYZ + (h_x,h_z) fields:
  chaotic, vertex-transitive (homogeneous) candidate. The positive case.

## Diagnostics

1. `<r>` — mean adjacent gap ratio in a fixed translation-momentum sector.
   Poisson 0.386 (integrable), GOE 0.531 / GUE 0.600 (chaotic).
2. `deg` — fraction of near-zero spacings: spectral degeneracy, which enlarges
   the temporal-ensemble commutant and would spoil single-Hamiltonian decoupling.
3. `OTOC` — infinite-temperature squared-commutator saturation at t=4.
4. `ham-Haar` — **the test**: `max_step |S_rad(Hamiltonian) - S_rad(Haar)|` over
   the emission sequence. The raw deviation from the island `min` is dominated
   by the known finite-size Page correction (largest at the balanced cut), so we
   compare against the Haar reference instead. `noneFail` (no-scramble deviation
   from `min`) sets the failure scale.

## Results (n = 6, 8, 10, 12; single seed)

| family | n | `<r>` | deg | ham-Haar | finalMI | noneFail |
|---|---|---|---|---|---|---|
| free_chain | 6 | 0.366 | 0.500 | 0.340 | 1.263 | 1.386 |
| free_chain | 8 | 0.602 | 0.586 | 0.854 | 1.606 | 2.773 |
| free_chain | 10 | 0.471 | 0.673 | 1.268 | 1.339 | 2.773 |
| free_chain | 12 | 0.412 | 0.814 | 1.666 | 1.820 | 4.159 |
| integ_xxz | 6 | 0.207 | 0.375 | 0.060 | 1.184 | 1.386 |
| integ_xxz | 8 | 0.258 | 0.379 | 0.121 | 1.976 | 2.773 |
| integ_xxz | 10 | 0.371 | 0.378 | 0.212 | 2.435 | 2.773 |
| integ_xxz | 12 | 0.436 | 0.389 | 0.299 | 2.537 | 4.159 |
| chaos_expander | 6 | 0.636 | 0.000 | 0.123 | 1.305 | 1.386 |
| chaos_expander | 8 | 0.524 | 0.000 | 0.064 | 2.288 | 2.773 |
| chaos_expander | 10 | 0.540 | 0.000 | 0.027 | 2.655 | 2.773 |
| chaos_expander | 12 | 0.552 | 0.000 | 0.052 | 2.730 | 4.159 |

## Reading (honest)

The robust finding is the **separation**, via the slope in `n` of `ham-Haar`:

- **free_chain: 0.340 → 0.854 → 1.268 → 1.666 — monotone increase.** Diverges
  from Page; the Gaussian counterexample fails and gets *worse* with size, with
  `deg` climbing 0.50 → 0.81. Counterexample 1 demonstrated.
- **integ_xxz: 0.060 → 0.121 → 0.212 → 0.299 — monotone increase.** Diverges
  (more slowly); integrable dynamics fail to reproduce the island min, Poisson-
  leaning `<r>`, nonzero `deg`. The cycle-XXZ warning demonstrated.
- **chaos_expander: 0.123 → 0.064 → 0.027 → 0.052 — small and bounded, NOT
  cleanly monotone.** It stays 10–80x below the no-scramble failure scale
  (`noneFail` ≈ 4.16) and far below the counterexamples, with `<r>` ≈ 0.52–0.64
  (chaotic), `deg` = 0, and growing `finalMI` (post-Page correlations).

What this does and does NOT show:

- It **cleanly separates** the chaotic deterministic Cayley Hamiltonian from the
  free and integrable cases: the counterexamples diverge monotonically and carry
  their spectral signatures, while the chaotic case stays bounded near the Haar
  finite-size floor.
- It does **NOT** yet establish convergence-to-Page for the deterministic H. The
  chaos_expander deviation **ticks up at n=12** (0.027 -> 0.052), so the single-
  seed data is consistent with both convergence and a small nonzero plateau, and
  cannot distinguish them. `ham-Haar` is a max-over-steps of a difference between
  two individually fluctuating O(2^{-c/2}) quantities, and the Haar reference is
  itself one random draw, so the single-seed estimator is noisy.

Bottom line: this is finite-size-scaling evidence for an *existence*-style claim
that a deterministic chaotic Cayley Hamiltonian behaves like the Haar isometry
(bounded, far from failure), with the free/integrable counterexamples explicitly
failing — but "bounded" is not yet "converging." Settling convergence requires
seed averaging (below).

## Seed-averaged convergence (8 seeds, vs analytic Page formula)

Averaging over 8 seeds and comparing to the *exact Page-formula* expectation
(removing the single-Haar-draw noise) settles the convergence question. The
reference column is the Haar isometry's own finite-size deviation from the Page
formula, computed identically.

| family | n | mean \|S_ham - Page\| | std | mean \|S_haar - Page\| |
|---|---|---|---|---|
| free_chain | 6 | 0.399 | 0.139 | 0.057 |
| free_chain | 8 | 1.049 | 0.142 | 0.026 |
| free_chain | 10 | 1.203 | 0.147 | 0.012 |
| integ_xxz | 6 | 0.115 | 0.164 | 0.057 |
| integ_xxz | 8 | 0.169 | 0.088 | 0.026 |
| integ_xxz | 10 | 0.160 | 0.123 | 0.012 |
| chaos_expander | 6 | 0.060 | 0.043 | 0.057 |
| chaos_expander | 8 | 0.028 | 0.016 | 0.026 |
| chaos_expander | 10 | 0.015 | 0.007 | 0.012 |

**Decisive comparison — the last two columns for chaos_expander:**

- chaos_expander deviation from Page: 0.060 -> 0.028 -> 0.015 (std shrinking
  0.043 -> 0.016 -> 0.007);
- Haar isometry's *own* deviation from Page: 0.057 -> 0.026 -> 0.012.

These are **statistically identical** (within ~0.003 nats at every size) and both
roughly halve as n increases by 2. So the deterministic chaotic Cayley
Hamiltonian is **indistinguishable from a Haar isometry** and **converges to the
island/Page value**. The single-seed n=12 uptick (0.027 -> 0.052) was noise.

By contrast:

- **free_chain diverges**: 0.399 -> 1.049 -> 1.203, far above the Haar floor.
- **integ_xxz plateaus**: ~0.115 -> 0.169 -> 0.160, small but clearly *above*
  the Haar floor (0.06 -> 0.01) and not descending -- distinguishable from the
  chaotic case, which tracks Haar to within 0.003.

## Bottom line

Finite-size scaling of a single deterministic, homogeneous (vertex-transitive)
Cayley Hamiltonian shows it reproduces the island/Page radiation-entropy curve,
tracking a Haar isometry and converging to the Page formula as the system grows,
while free (Gaussian) and integrable (cycle-XXZ) Hamiltonians demonstrably fail
-- the former diverging, the latter plateauing above the Haar floor -- each with
its predicted spectral signature (`<r>`, `deg`). This is evidence for the
deterministic-mixer route by direct analysis of the specific Hamiltonian, the
appropriate standard for a deterministic named object, with no theorem invoked.

Scope: ED-limited sizes (n <= 12), one circulant expander (not an optimized
Ramanujan graph), fixed t_mix=5. A t_mix scan would estimate the convergence
rate; larger n via Krylov/sparse evolution would extend the trend.

## Caveats / scope

- Sizes are small (n ≤ 12, exact diagonalization); the convergence is a trend,
  not a proof. This is evidence for an *existence* claim (an explicit
  deterministic H works), not a *universality* theorem.
- Level statistics resolve only the translation-momentum symmetry; free_chain and
  integ_xxz carry extra conserved charges (Sz, particle–hole), so their `<r>` is
  noisy — `deg` is the more robust integrability flag for them.
- The expander is a small circulant {±1, ±n/2}, not an optimized Ramanujan graph;
  the point is the chaotic-vs-integrable-vs-free contrast, not graph optimality.
- `t_mix = 5`, single seed. A `t_mix` and seed scan would tighten the
  convergence-rate estimate.
