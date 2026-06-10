# Mirror operators, state dependence, and the AMPS audit in the Hamiltonian model

**Goal.** Extend the operational layer of the paper (Sec. 4: recovery and
complementary reconstruction) to interior (mirror/partner) operators:

1. construct mirror operators for every microstate (finite-dim modular theory),
2. prove a **no-go**: no state-independent operator can be the mirror for all
   smooth microstates (rigorous counting/linearity argument at finite dim),
3. locate the mirror's support: core pre-Page, early radiation post-Page,
   switching at the Page transition with the entanglement wedge,
4. audit the AMPS monogamy argument: name the premise that fails in the model,
5. quantify "how state-dependent": subspace-dependence with the decoupling
   budget; superpositions *within* a code subspace are safe,
6. complexity remark: the radiation-supported mirror is a Petz pullback,
   generically exponentially complex (Harlow–Hayden; Python's lunch).

This file records the full derivation behind the paper's Section
"Interior operators and state dependence" (sec:mirrors).

---

## 1. Setup and smoothness condition

Fresh mode: `𝖻` = record register of the most recent emission step, Hilbert
space `H_b`, dim `d_b`. Purifier side: `P` = remaining core `B` ⊗ earlier
radiation record `R`. Global state pure on `H_b ⊗ H_P`.

**Smoothness (infalling-vacuum analogue).** `|Ψ⟩` is *smooth at the fresh
mode* if `Tr_P |Ψ⟩⟨Ψ| = ρ_β`, the full-rank thermal state of the mode at the
instantaneous temperature. The golden-rule emission channel produces exactly
this marginal (detailed-balance weights `e^{-βω}` across record branches), up
to the `O(Γ_E/ΔE)` and finite-energy corrections already budgeted for the
spectrum. Pure (unentangled) emitted mode = "firewall" in this language.

## 2. Mirror construction (finite-dimensional modular theory)

For `|Ψ⟩` smooth (hence cyclic-separating for the mode algebra on its Schmidt
support), Tomita–Takesaki in finite dimensions = the Schmidt twisted
transpose. For every operator `X` on the mode there is a unique operator
`X̃_Ψ` supported on the Schmidt partner of `𝖻` inside `P`, satisfying

```
(mirror relation)   X̃_Ψ |Ψ⟩ = (ρ_β^{1/2} X† ρ_β^{-1/2} ⊗ 1_P) |Ψ⟩ ,
                    [X̃_Ψ, Y ⊗ 1_P] = 0 for all exterior Y.
```

Explicitly: with Schmidt form `|Ψ⟩ = Σ_n √p_n |n⟩_b |n′⟩_P`
(`p_n` = eigenvalues of `ρ_β`), `X̃_Ψ` acts on span{|n′⟩} as the
`ρ^{1/2}`-twisted transpose of `X`. Equivalently `X̃ = J X J` with `J` the
modular conjugation of `(A_b, |Ψ⟩)`.

Checks:
- mode annihilator `a` at frequency ω, `ρ_β ∝ e^{-βω n̂}`:
  `ρ^{1/2} a† ρ^{-1/2} = e^{-βω/2} a†`, so `ã|Ψ⟩ = e^{-βω/2} a†|Ψ⟩` —
  exactly the Papadodimas–Raju defining relation.
- two-point functions: `⟨Ψ| (Y⊗1) X̃ |Ψ⟩ = Tr[ρ_β Y ρ^{1/2} X† ρ^{-1/2}]
  = Tr[ρ^{1/2} Y ρ^{1/2} X†]` — the half-shifted thermal (KMS / two-sided
  thermofield) correlators of a smooth horizon.

The construction manifestly depends on `|Ψ⟩` through both the Schmidt basis
and weights. The question is whether that dependence is removable.

## 3. No-go: no state-independent mirror

**Lemma (smooth states span).** Fix one smooth `|Ψ₀⟩`. The family
`{(1 ⊗ U)|Ψ₀⟩ : U unitary on H_P}` consists of smooth states (the mode
marginal is unchanged) and spans all of `H_b ⊗ H_P`.
*Proof.* Unitaries span `B(H_P)` linearly. For any operator `B_P`,
`(1⊗B_P)|Ψ₀⟩ = Σ_n √p_n |n⟩ (B_P|n′⟩)`; since `ρ_β` is full rank, `{|n⟩}` is
a basis of `H_b` and `B_P|n′⟩` is arbitrary, so the span is everything. ∎

Physical reading: the spanning family is dynamically legitimate — same fresh
emission, different past (different initial microstates / preparation
unitaries acting on core + early radiation).

**Proposition (no state-independent interior).** Fix a mode operator `X` with
`[ρ_β^{1/2} X† ρ_β^{-1/2}, X] ≠ 0` (any raising/lowering operator). No single
fixed operator `X̃` satisfies the mirror action relation for **all** smooth
states while commuting with the exterior algebra. Any `X̃` satisfying the
action relation on all smooth states equals
`ρ_β^{1/2} X† ρ_β^{-1/2} ⊗ 1_P` — an **exterior** operator — with
commutator `[X̃, X⊗1] = [ρ^{1/2}X†ρ^{-1/2}, X] ⊗ 1` of order one.

*Proof.* The action relation is linear in `|Ψ⟩`; holding on a spanning set
(Lemma) it forces the operator identity `X̃ = ρ^{1/2}X†ρ^{-1/2} ⊗ 1`. For
`X = a`: `[e^{-βω/2}a†, a] = -e^{-βω/2}[a,a†] ≠ 0`. ∎

So: state-independence + linearity + correct partner action on all
microstates ⟹ the "interior" operator is the exterior twisted adjoint in
disguise, and it fails to commute with the exterior algebra — it is not
behind the horizon at all. PR state this in the continuum
(`b̃|Ψ⟩ = e^{-βω/2}b†|Ψ⟩` on all states ⟹ `b̃ = e^{-βω/2}b†`); at finite
dimension it is a theorem with no analytic caveats.

**Approximate version.** Averaging over the Haar family `U`:
`E_U (1⊗U)|Ψ₀⟩⟨Ψ₀|(1⊗U)† = ρ_β ⊗ π_P`, so
`E_U ‖(X̃ - M⊗1)(1⊗U)|Ψ₀⟩‖² = Tr[Δ†Δ (ρ_β ⊗ π_P)]`, `Δ = X̃ - M⊗1`,
`M = ρ^{1/2}X†ρ^{-1/2}`. Hence ε-approximate state-independence on typical
microstates collapses `X̃` onto the exterior operator in the thermally
weighted 2-norm, leaving an O(1) commutator defect (up to O(ε)) on typical
states. The no-go is not an artifact of demanding exactness.

## 4. Where the mirror lives (construction with decoupling errors)

Inputs from the paper:
- Pre-Page (rising branch additive): `I(𝖻 : R_early) = O(ε)` — the fresh
  mode is uncorrelated with the early radiation; its purifier is in the core.
- Post-Page: "a late radiation block is locally close to thermal while its
  purifier is mostly the early radiation": `I(𝖻 : B) = O(ε)`; purifier in
  `R_early`. (Page/Haar check: small `𝖻 ⊂ R`, `d_R ≫ d_B` ⟹
  `S(𝖻B) ≈ S(𝖻)+S(B)`.)
- Two-sided converses of Prop. complementary-recovery.

**Pre-Page.** Purifier of `𝖻` embeds in `B` up to `O(√ε)` (Uhlmann);
conjugating the Schmidt mirror through the embedding gives a core-supported
`X̃_B` satisfying the mirror relations up to `O(√ε)` — on the PR "little
Hilbert space" `A_ext|Ψ⟩` (products of exterior operators acting on the
state), since exact operator-level commutation on the full space is excluded
off the dynamically accessible image. One fixed `X̃_B` serves all states
produced by the emission isometry `V_E` from the shell: the accessible smooth
states span only the `D`-dimensional image `V_E H_E`, not the full space, so
the spanning hypothesis of the no-go is not met — this is exactly why a fixed
choice is possible there. **Converse:** any radiation-supported candidate
fails: a mirror reproducing the relations would purify the mode,
requiring `I(𝖻 : R) ≈ 2S(𝖻)`, but `I(𝖻 : R_early) = O(ε)` pre-Page. Connected
correlators `⟨Y X̃_R⟩_c` are bounded by `‖ρ_{𝖻R} - ρ_𝖻⊗ρ_R‖₁ = O(ε)` while
the mirror value is O(1).

**Post-Page.** `I(𝖻 : B) = O(ε)` ⟹ purifier embeds in `R_early` via an
Uhlmann isometry `W`; pull the mirror back: `X̃_R = W X̃ W†` (equivalently the
adjoint/pullback of the Petz recovery channel of Prop. recovery applied to
the partner observables). Errors `O(√ε)`. **Uniform over a code subspace:**
decoupling holds uniformly over each decoupled code subspace `C` (dim `e^k`
within budget), so `W` can be chosen once per subspace; the relations then
hold for every state of `C` *including superpositions* — linearity over the
subspace is restored. Across families exceeding the budget, impossible by the
no-go. **Converse:** no core-supported operator does the job post-Page,
`I(𝖻 : B) = O(ε)`.

**Switch.** The two regimes meet in the same `O(log 1/ε)` window around
`ΔS_rad = S_micro` (Page point, `M_Page = M_0/√2`, `t ≈ 0.65τ`) as
complementary recovery. The mirror's support tracks the entanglement wedge:
pre-Page interior-partner = core (wedge of the black hole), post-Page
interior-partner ⊂ radiation (island in the wedge of the radiation). This is
the algebraic content of `A = R_B` / ER=EPR (Verlinde–Verlinde QEC version;
Maldacena–Susskind), with the island reconstruction realized by the Petz
pullback.

## 5. AMPS audit

AMPS premises, model language, for an old (post-Page) black hole:

- (P1) Unitarity + Page: fresh mode `𝖻` is (near-)purified by early radiation
  — `I(𝖻 : R_early) ≈ 2S(𝖻)`. **Derived** in the model.
- (P2) Smoothness: `𝖻` is thermally entangled with an interior partner `b̃`
  satisfying the mirror correlators. **Constructed** in the model (Sec. 2).
- (P3) Independence: `b̃` is a tensor factor / operator algebra independent
  of `R_early` (commuting, distinct degrees of freedom).

Monogamy makes (P1)+(P2)+(P3) contradictory. In the model **(P3) is false,
and provably must be false**: post-Page the mirror is supported inside
`R_early` (Sec. 4), so the entanglements of (P1) and (P2) are the same
entanglement counted twice — no monogamy violation. The no-go proposition
upgrades "is false" to "must be false": no state-independent operator
independent of the radiation could do the mirror job. The model therefore
locates the failing premise of the firewall argument and shows the failure is
forced, not optional.

**Quantified state dependence (response to AMPSS / Marolf–Polchinski within
the model).** The objection to state-dependent maps is that quantum mechanics
acts linearly and superpositions of microstates should not change the
observables (Born-rule worries). The model gives the quantitative boundary:
one fixed reconstruction serves an entire decoupled code subspace of
dimension `e^k`, `k ≤ ΔS_rad - S_micro - 2 log(1/ε)` — superpositions within
the subspace are completely safe — while no fixed choice extends to families
spanning the full space (no-go). "State dependence" in the model is precisely
**subspace dependence with the decoupling budget**; Born-rule issues can only
arise across code subspaces larger than the budget.

## 6. Complexity remark

The radiation-supported mirror is a Petz pullback built from
`ρ_R^{±1/2}` of the radiation record — generically exponentially hard to
implement (Harlow–Hayden; quantified geometrically by the Python's lunch).
Existence statements locate the interior in `R`; they do not make it
feasibly accessible. Same status as the recovery channel of Prop. recovery
(open problem item 4 of the paper).

## 7. What is and is not claimed

- Claimed: the algebraic layer — partner operators with smooth-horizon (KMS)
  correlators, their location, their forced state dependence, the failing
  AMPS premise. All conditional on the same decoupling input as the entropy
  results; corollaries, not new assumptions.
- Not claimed: interior geometry, infalling experience, or that gravity
  realizes its interior this way. The statements are the algebraic content
  the gravitational interior must reproduce (open problem item 2).

## 8. Literature anchors

- AMPS: Almheiri–Marolf–Polchinski–Sully, JHEP 02 (2013) 062, 1207.3123.
- AMPSS apologia: Almheiri–Marolf–Polchinski–Stanford–Sully, JHEP 09 (2013)
  018, 1304.6483.
- Mirrors / state dependence: Papadodimas–Raju, JHEP 10 (2013) 212,
  1211.6767; PRD 89 (2014) 086010, 1310.6335.
- A = R_B / QEC: Verlinde–Verlinde, JHEP 10 (2013) 107, 1211.6913.
- ER=EPR: Maldacena–Susskind, Fortsch. Phys. 61 (2013) 781, 1306.0533.
- Born-rule critique: Marolf–Polchinski, CQG 33 (2016) 075003, 1506.01337.
- Complexity: Harlow–Hayden, JHEP 06 (2013) 085, 1301.4504;
  Brown–Gharibyan–Penington–Susskind, JHEP 08 (2020) 121, 1912.00228.
- General review of the QEC/mirror framework: Harlow, Rev. Mod. Phys. 88
  (2016) 015002, 1409.1231.
