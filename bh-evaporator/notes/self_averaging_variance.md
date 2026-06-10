# Self-averaging of the Page curve: variance of the Rényi-2 purity under full ETH

**Goal (open problem item 3, QM half).** Show that for a *fixed* shell
Hamiltonian satisfying ETH-type assumptions, the radiation purity
`P = Tr ρ_R²` concentrates: instance = two-contraction mean up to
exponentially small fluctuations. Consequence: the ensemble language of the
replica-wormhole derivation is redundant on the quantum-mechanics side — a
single Hamiltonian self-averages — and the factorization puzzle has no QM
half in the model. This extends App F by one Wick order.

## 1. Assumption (E3′)

(E3) of App F extended to **eighth moments**: joint moments of the ETH
variables `R^(m)` Wick-factorize into pairings through eighth order, with
crossing/connected corrections suppressed by `e^{-S_micro}` relative to
retained pairings; distinct records uncorrelated. Same free-probability-ETH
status as (E3) (Foini–Kurchan; Pappalardi–Foini–Kurchan) — one more order of
the same hypothesis, not a new kind of assumption.

## 2. Permutation calculus for the second moment of the purity

`P² = (Tr ρ_R²)²` contains eight matrix-element factors (4 R, 4 R*). Wick ⇒
sum over the 4! = 24 pairings = permutations π ∈ S₄ of the four replicas.
With σ = (12)(34) the double-swap, the Gaussian-proxy weights are

```
E[P²] = (d_B d_R)^{-4} Σ_{π∈S₄} d_B^{c(π)} d_R^{c(σπ)} ,
```

`c(·)` = number of cycles, `d_B = e^{S_micro}`, `d_R = e^{ΔS_rad}`.

**Disconnected block (4 terms, π ∈ S₂×S₂):**
- e:        d_B⁴ d_R²  → 1/d_R²
- (12):     d_B³ d_R³  → 1/(d_B d_R)
- (34):     d_B³ d_R³  → 1/(d_B d_R)
- (12)(34): d_B² d_R⁴  → 1/d_B²

Sum = (1/d_R + 1/d_B)² = (E P)² exactly. ✓ Variance = the remaining 20
connected permutations.

**Connected terms, by class (computed: c(π), c(σπ)):**
- cross transpositions (13),(14),(23),(24): c=3, c(σπ)=1 → 4/(d_B d_R³);
  and the σ-dual class → 4/(d_B³ d_R).
- 3-cycles (8 of them): give 1/(d_B² d_R²)-type terms.
- 4-cycles etc.: ≤ 1/(d_B² d_R²).

**Norm-fluctuation subtlety.** The largest connected class,
`4/(d_B d_R³) + 4/(d_B³ d_R)`, relative size `4/(d_B d_R) = 4 e^{-(S_micro+ΔS_rad)}`,
is the norm-fluctuation contribution of the unconstrained Gaussian proxy
(`Tr Ψ` fluctuates). The physical channel is trace-preserving — the
flat-rate normalization `Σ_m K̂_m†K̂_m = 1` holds exactly (deviations F_E
budgeted separately in App A) — so this class is absent. (Even if retained
it is ≤ e^{-S₀}, so the headline below is unaffected.)

**Calibration by the exact Haar result.** For normalized Haar states
(Giraud, J. Phys. A 40, 2793 (2007)):
`Var[Tr ρ_A²] ≈ 2/(d_A d_B)²`, mean ≈ 1/d_min, hence

```
Var[P]/(E P)² ≈ 2 e^{-2 max(ΔS_rad, S_micro)} .
```

This matches the surviving connected classes (1/(d_B²d_R²)-type and the
smaller dual-transposition class) with their exact multiplicities and
cancellations. ETH corrections multiply by [1 + O(e^{-S_micro})] (crossings,
E3′) and the dwell/envelope factors O(Γ_E/ΔE) as in App F.

## 3. Result

```
SD[Tr ρ_R²]/E[Tr ρ_R²] = O(e^{-max(ΔS_rad(E), S_micro(E))}) ≤ O(e^{-S₀/2})
```

uniformly along the trajectory away from the endpoint, using
`ΔS_rad + S_micro ≳ S₀` (record refinement only raises ΔS_rad). Worst case
exactly at the Page transition, where both exponents equal S₀/2. The
Rényi-2 entropy fluctuation is δS₂ ≈ δP/P = O(e^{-S₀/2}).

The variance can be read over any of: (i) the fictitious ETH ensemble,
(ii) microcanonical shell windows, (iii) shell-typical codes / low-complexity
initial states (E5) — the leading connected diagrams are identical;
Chebyshev then gives concentration over codes/seeds for fixed H.

**Factorization corollary.** Multi-shell products:
`E[P(E) P(E′)] − E[P(E)] E[P(E′)]` consists of the same connected classes ⇒
products of purities factorize up to `e^{-S₀}`-type corrections. For a fixed
Hamiltonian there is nothing for half-wormholes to restore at this order:
the connected pairings *are* the model's half-wormhole analogues
(Saad–Shenker–Stanford–Yao, "wormholes without averaging"), explicitly
listed and exponentially small.

## 4. Empirical check (App E data, already in the paper)

Table tab:cayley-scaling std column (8 seeds, chaotic circulant family):

| n | seed std |
|---|---|
| 6 | 0.043 |
| 8 | 0.016 |
| 10 | 0.007 |

Ratios 2.7, 2.3 per Δn = 2. Prediction: δS ~ e^{-S₀/2} = 2^{-n/2} → factor 2
per Δn = 2. Consistent (8 seeds ⇒ ±~40% noise on a std estimate). The
chaotic family's scatter also matches the Haar reference's own finite-size
deviations — concentration at the Haar rate, as self-averaging requires.
Caveats: the measured metric is max-over-steps |S_vN − Page| over seeds
(initial states), not the per-shell Rényi-2 SD; scaling check only.

## 5. What this settles and what it doesn't

- Settles (conditional on E1–E5 + E3′): the exterior entropy package of a
  single fixed Hamiltonian equals the ensemble answer to e^{-S₀/2}; the
  ensemble is redundant; no factorization puzzle arises in the model.
- Remaining (gravity side, open problem 3): why the gravitational path
  integral computes an ensemble *mean* at all — the model now bounds the
  question entirely on the gravity side.
- Not covered: higher Rényi/von Neumann fluctuation constants (same method,
  more replicas), endpoint regime, fluctuations of finer observables than
  shell purities.

## 6. Literature anchors

- Exact Haar purity variance: O. Giraud, J. Phys. A 40, 2793 (2007),
  quant-ph/0611285.
- Ensemble behavior of replica wormholes / factorization:
  Penington–Shenker–Stanford–Yang; Marolf–Maxfield (both already in refs).
- Wormholes without averaging / half-wormholes: Saad, Shenker, Stanford,
  Yao, arXiv:2103.16754.
- Free-probability ETH at higher moments: Pappalardi–Foini–Kurchan (in refs).
