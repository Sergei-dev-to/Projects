# ETH ⇒ second-moment decoupling of the weak-emission channel

**Goal.** Replace the design assumption on the in-shell mixer (paper
`paper_ideal_hamiltonian`, Sec. 2.3 / Sec. 4) by ETH-type spectral assumptions
on a *fixed* shell Hamiltonian, and derive the decoupling bound
(Eq. `eq:decoupling-bound` of the paper) with an explicit error budget.

This file records the full computation behind the paper's Appendix
"An ETH Route to Emission-Channel Decoupling" (Proposition: ETH decoupling).

---

## 1. Setup

One evaporation step maps shell `H_E` (dim `D`, eigenpairs `H_E|ν⟩ = θ_ν|ν⟩`)
to shell `H_{E−ω}` (dim `D_−`, eigenbasis `|ν̄⟩`). Ingredients, all from the
paper's Appendix A (weak-emission Stinespring map):

- **Flat-rate conditioned jumps** `K̂_m : H_E → H_{E−ω}`, record
  `m = (ω, λ, μ)`, normalized so `Σ_m K̂_m† K̂_m = 1_E` (the `J_E = Γ_E 1`
  idealization; the deviation `F_E` is a separate, already-budgeted error).
- **Dwell dephasing** from tracing the waiting-time record:
  `T(ρ)_{νν'} = L_{νν'} ρ_{νν'}`, with the Lorentzian kernel
  `L_{νν'} = Γ_E / (Γ_E + i(θ_ν − θ_ν'))`. Note `L_νν = 1`, `|L| ≤ 1`,
  `L_{ν'ν} = L*_{νν'}`.
- **One conditioned step**: `Λ(ρ) = Σ_m [K̂_m T(ρ) K̂_m†] ⊗ |m⟩⟨m|_R`.

Code subspace `C ⊂ H_E`, `dim C = d_Q = e^k`, projector `P_C`; reference `Q`
maximally entangled with `C`: `Φ_CQ = (1/d_Q) Σ_{ij} |i⟩⟨j|_C ⊗ |i⟩⟨j|_Q`.

After the dwell: `σ = (T ⊗ id_Q)(Φ)`. After the emission, with the radiation
record traced:

```
ρ_QB = Σ_m (K̂_m ⊗ 1_Q) σ (K̂_m† ⊗ 1_Q).
```

## 2. Assumptions

- **(E1) Sectorwise nondegenerate spectrum, bounded near-resonance.** Within
  each symmetry sector, no degeneracies, and
  `#{(ν,ν′) : ν≠ν′, |θ_ν−θ_ν′| ≤ Γ_E} ≲ D · Γ_E ρ_B(E)`
  (`ρ_B` = level density; `Γ_E ρ_B` = levels per linewidth). The `f_deg`
  diagnostic of the Cayley appendix is the finite-size check.
- **(E2) Srednicki-form ETH for the jump operators.**
  `⟨ν̄|K̂_m|ν⟩ = D^{−1/2} f_m(Ē, ω) R^{(m)}_{ν̄ν}`, with `f_m` smooth across
  the shell and `R` zero-mean, unit-variance, O(1) variables.
- **(E3) Fourth-moment factorization (full ETH / freeness).** Joint fourth
  moments of the `R`'s Wick-factorize into pairings; crossing/connected
  corrections suppressed by `e^{−S_micro}` relative to retained pairings.
  Distinct records `m ≠ m′` uncorrelated at second and fourth moment.
  (Free-probability formulation of ETH: Foini–Kurchan PRE 99, 042139 (2019);
  Pappalardi–Foini–Kurchan PRL 129, 170603 (2022).)
- **(E4) Weak-coupling window**: `Γ_E ≪ ΔE` (shell width). Same window as
  the golden rule. Both regimes `Γ_E ρ_B ≷ 1` (overlapping vs isolated
  resonances) are admissible; formulas below interpolate.
- **(E5) Shell-typical code**: `(P_C)_{νν} ≈ d_Q/D` up to O(1) factors, and
  the code is uncorrelated with the `R` fluctuations (the low-complexity
  initial states of Sec. 2.4). Codes fine-tuned in the eigenbasis are
  excluded (and physically should be: they evade dephasing).

Record weights: `q_m ≡ E Tr[K̂_m† K̂_m]/D = D_− |f_m|²/D`, and flat-rate
completeness gives `Σ_m q_m = 1`.

## 3. Mean decoupling (second moments of R only)

`E[K̂_m X K̂_m†]_{μ̄ν̄} = (|f_m|²/D) Σ_{νμ} E[R_{μ̄ν} R*_{ν̄μ}] X_{νμ}
= (|f_m|²/D) δ_{μ̄ν̄} Tr X`.

So `E ρ_QB = (Σ_m q_m) π_{B} ⊗ Tr_C σ = π_B ⊗ π_Q` exactly (T is
trace-preserving on C, so `Tr_C σ = π_Q`). **The mean is exactly decoupled**;
all content is at the level of fluctuations (purity).

## 4. Second moment: the two contractions

Want `P ≡ E Tr ρ_QB² = Σ_{mm'} E Tr[A_m A_{m'}]`,
`A_m = (K̂_m ⊗ 1) σ (K̂_m† ⊗ 1)`.

Matrix elements (B-side index ᾱ, Q-side index i):

```
⟨ᾱ i|A_m|β̄ j⟩ = (|f_m|²/D)^{...}  —  explicitly:
Tr[A_m A_{m'}] = (|f_m|²|f_{m'}|²/D²) Σ R^{(m)}_{ᾱν} σ_{νi,ν'j} R^{(m)*}_{β̄ν'}
                                        R^{(m')}_{β̄μ} σ_{μj,μ'i} R^{(m')*}_{ᾱμ'} .
```

**Case m ≠ m′** (independent R's, second moments only):
`E[R^{(m)}_{ᾱν} R^{(m)*}_{β̄ν'}] = δ_{ᾱβ̄} δ_{νν'}` and likewise for m′.
Sum: `(|f_m|²|f_{m'}|²/D²) · D_− · Σ_{ν,i,j} σ_{νi,νj} Σ_μ σ_{μj,μi}`
`= (q_m q_{m'}/D_−) Tr[(Tr_C σ)²] = q_m q_{m'}/(D_− d_Q)`.

**Case m = m′**, Gaussian pairing A (same δ-pattern as above): contributes
`q_m²/(D_− d_Q)`.

Together, pairing A summed over all (m, m′):
```
Σ_{mm'} q_m q_{m'} / (D_− d_Q) = 1/(D_− d_Q) = e^{−[S_micro(E−ω) + k]}.
```
**This is the island/swap contraction** — the post-Page branch.

**Case m = m′**, Gaussian pairing B
(`E[R_{ᾱν}R*_{ᾱμ'}] E[R*_{β̄ν'}R_{β̄μ}]`-type: ᾱ, β̄ free, ν=μ′, ν′=μ):
`(|f_m|⁴/D²) · D_−² · Σ_{νν',ij} σ_{νi,ν'j} σ_{ν'j,νi} = q_m² Tr σ²`.

Summed: `(Σ_m q_m²) · Tr σ²` — **the record/Hawking (identity) contraction**.

**Crossing / connected terms**: suppressed by `e^{−S_micro}` relative, by (E3).

So:
```
P = (Σ_m q_m²) Tr σ²  +  e^{−[S_micro(E−ω)+k]} [1 + O(e^{−S_micro})] + crossings.
```

## 5. The dephased-code purity (Lorentzian kernel)

```
Tr σ² = (1/d_Q²) Σ_{νν'} |L_{νν'}|² (P_C)_{νν} (P_C)_{ν'ν'}.
```

Checks: `T = id` (`L ≡ 1`) gives `Tr σ² = 1` (pure, no time record). Full
dephasing (`L = δ`) gives `Σ_ν (P_C)_{νν}²/d_Q²`.

For a shell-typical code, `(P_C)_{νν} ≈ d_Q/D`:
- diagonal: `≈ 1/D` (diagonal-ensemble value);
- off-diagonal: `Σ_{ν'≠ν} |L_{νν'}|² ≈ Γ_E ρ_B` levels per linewidth, giving
  `O(Γ_E ρ_B)/D`.

```
Tr σ² = (1/D) [1 + O(Γ_E ρ_B(E))],   and  Γ_E ρ_B / D = Γ_E/ΔE  ≪ 1 by (E4).
```

Interpretation: `(Σ_m q_m²) Tr σ² = e^{−S₂^rec}` where `S₂^rec` is the
Rényi-2 entropy of the **full realized record** — channels, frequencies, and
arrival times. The arrival-time factor is the kernel above: the waiting-time
record resolves the shell down to width `Γ_E` (capacity between
`log(ΔE/Γ_E)` and `log D` depending on `Γ_E ρ_B ≷ 1`). The surviving
coherences (pairs within `Γ_E`) are exactly the `O(Γ_E/ΔE)` correction — the
same near-resonant coherent weight flagged in the paper's App. A remark.

Important sanity points:
- Arrival-time refinement *raises* `S₂^rec` ⇒ it can only *help* decoupling
  (the record side gains dimensions). For a conservative bound, lower-bound
  `S₂^rec` by the binned thermodynamic record entropy of Sec. 5 of the paper.
- The entropy bookkeeping of the rising Page branch refers to the *binned*
  records of the regulated model (App. C explicitly includes time bins in
  histories), so no inconsistency is introduced — same status as App. A.

## 6. Result (one step) and composition

One-step second moments match the Haar isometry's:

```
E Tr ρ_QB² = e^{−S₂^rec} + e^{−[S_micro(E−ω)+k]}
             × [1 + O(Γ_E/ΔE) + O(e^{−S_micro(E−ω)})].
```

These are exactly the two contractions of the paper's App. C, derived for a
fixed Hamiltonian instead of assumed via 2-designs.

**2-norm → 1-norm**: `E‖ρ_QB − π_Q⊗π_B‖₂² = P − 1/(d_Q D_−)`, and
`‖X‖₁ ≤ √(d_Q D_−) ‖X‖₂`, giving

```
E‖ρ_QB − π_Q ⊗ π_B‖₁ ≲ exp{ −(1/2)[S₂^rec − S_micro(E−ω) − k] } + ε_step,
ε_step = O(√(Γ_E/ΔE)) × (leading exponent) + O(e^{−S_micro/2}-type crossings).
```

**Composition**: hybrid/triangle argument — replace one step at a time by its
Haar counterpart; each replacement costs ε_step at the level of second
moments; errors add: `Σ_j ε_j`, dominated by the late, small shells, exactly
like the `ε_Page` term already budgeted in Sec. 4 of the paper. (Same
structure as the standard approximate-design hybrid arguments,
Szehr–Dupuis–Tomamichel–Renner; Harrow–Low.)

## 7. Error budget (the punchline)

| error source | size | status |
|---|---|---|
| surviving dwell coherences | `O(Γ_E/ΔE)` | same parameter as the golden rule / Markov window — **no new small parameter** |
| ETH crossing terms | `O(e^{−S_micro})` rel. | full-ETH hypothesis (E3) |
| envelope variation of `f_m` over shell | smoothness of ETH envelope | same smoothness already used in the rate calculation |
| flat-rate deviation `F_E` | per App. A | already budgeted |
| code fine-tuning | excluded by (E5) | physical: eigenbasis-aligned codes evade dephasing |

## 8. Failure modes (consistency with the Cayley scaling study)

- **free chain**: violates (E1) — `f_deg` grows to 0.81; Gaussian dynamics
  also violate (E2)/(E3). Observed: diverges from Page.
- **cycle XXZ**: violates (E3) (Bethe structure; Poisson-leaning ⟨r⟩).
  Observed: plateaus above the Haar floor.
- **chaotic circulant**: satisfies the diagnostics (f_deg = 0, GOE ⟨r⟩).
  Observed: indistinguishable from Haar, converges to Page.

The failures predicted by the assumptions are the failures observed — the
assumptions are doing real work, and they are the checkable ones.

## 9. Literature anchors

- ETH ansatz with `f(Ē,ω) R_{ab}`: Srednicki, J. Phys. A 32, 1163 (1999).
- Full ETH / freeness (4-point factorization): Foini & Kurchan, PRE 99,
  042139 (2019); Pappalardi, Foini, Kurchan, PRL 129, 170603 (2022).
- Emergent state designs from chaotic dynamics (deep thermalization):
  Ho & Choi, PRL 128, 060601 (2022); Cotler, Mark, Huang, Hernández, Choi,
  Shaw, Endres, Choi, PRX Quantum 4, 010311 (2023). Our statement is the
  *channel* analogue: the radiation record is the projecting register.
- Temporal averaging / diagonal-ensemble equilibration: Linden, Popescu,
  Short, Winter, PRE 79, 061103 (2009).

## 10. What remains for full rigor

1. (E3) is a hypothesis: exact for RMT ensembles, numerically supported for
   chaotic local Hamiltonians, formalized but not proven by free-probability
   ETH. A proof for any named Hamiltonian family is open (as expected — this
   is the same status as ETH itself).
2. Uniformity of (E1)–(E5) along the entire evaporation trajectory is
   assumed (constants uniform in shell index).
3. Exact symmetries: apply sectorwise with charges recorded in the
   radiation (as in the paper's App. B).
4. The 1-norm conversion uses the crude `√(dim)` bound; smoothed one-shot
   versions (Dupuis et al.) would tighten constants but not exponents.
