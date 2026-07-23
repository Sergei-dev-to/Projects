# Dispatch: Fable — scoped single-shot (self-contained; no repo access)

> **RETIRED — DO NOT DISPATCH (2026-07-23).** The campaign is closed. Retained
> only as provenance; see `CLOSURE.md`.

Fable is a scarce, budget-capped resource (~$90 total). Invoke it for **exactly
two purposes** and nothing else. Each call is one self-contained message; Fable
has no filesystem and no memory of prior calls, so inline everything it needs.
Log every call's purpose and estimated cost in `DECISION_LOG.md`.

---

## MODE A — reduction ansatz (only if Sol Ultra's Phase 3 stalls)

> **Context.** The Littlewood–Richardson coefficient `c^ν_{λμ}` is the structure
> constant `s_λ s_μ = Σ_ν c^ν_{λμ} s_ν`. It is a theorem that the stretched
> coefficient `P(N) = c^{Nν}_{Nλ,Nμ}` is a polynomial in `N` with `P(0)=1`; it
> equals the Ehrhart polynomial of the Knutson–Tao hive polytope with boundary
> `(λ,μ,ν)`. The open KTT conjecture says all its monomial coefficients are ≥ 0.
> A counterexample within `length ≤ 7`, `|λ|,|μ| ≤ 30` is sought.
>
> **Key reduction:** a negative stretched LR coefficient IS a negative Ehrhart
> coefficient of a hive polytope. Ehrhart polynomials of lattice polytopes are not
> always positive (Reeve simplices, etc.).
>
> **Data so far (paste the Phase-2 near-zero champions here):**
> [ ... min non-leading coefficients, the triples achieving them, their
>   polynomials, and how the minimum trends with length/size ... ]
>
> **Task.** Propose specific hive combinatorial types (or families of boundaries
> `(λ,μ,ν)` within the budget) most likely to carry a *negative middle* Ehrhart
> coefficient, with the structural reason for each — which known negative-Ehrhart
> mechanism you expect it to inherit, and what to compute to confirm or kill it
> fastest. Rank your suggestions. Be concrete enough to search directly.

Return: a short ranked list of candidate types/families + the mechanism + the
cheapest discriminating computation for each. No prose padding.

---

## MODE B — candidate verification (independent of the finder)

> **Definitions.** `c^ν_{λμ}` = the Littlewood–Richardson coefficient (multiplicity
> of `s_ν` in `s_λ s_μ`). For partitions scaled by `N` (every part ×N), the
> function `P(N) = c^{Nν}_{Nλ,Nμ}` is a polynomial in `N`.
>
> **Claim to check.** For
> `λ = [...]`, `μ = [...]`, `ν = [...]`,
> it is claimed that `P(N)` has the exact form
> `P(N) = [paste polynomial]`,
> which has a **negative** coefficient at degree [k].
>
> **Task.** Independently, by a method of your own choosing (compute `c^{Nν}_{Nλ,Nμ}`
> for `N = 0,1,…` far enough and interpolate exactly over ℚ, or any other exact
> route), determine `P(N)` and report its exact monomial coefficients. State
> whether a coefficient is negative and at which degree. Show enough of your
> computation to be independently auditable. Do not trust the claimed polynomial;
> recompute from the definition.

Return: your independently computed exact polynomial, agree/disagree with the
claim, and the specific negative coefficient if present. This is a smoke test —
the binding certificate is tool agreement (lrcalc + Normaliz), not your verdict.

---

## MODE C — structural positivity recognition (outcome C)

This is a *recognition* consult — the cross-domain "is this a known structure"
question that is the best use of this budget. One self-contained shot.

> **Context.** For partitions `(λ,μ,ν)`, the stretched Littlewood–Richardson
> coefficient `P(N) = c^{Nν}_{Nλ,Nμ}` is the Ehrhart polynomial of the
> Knutson–Tao hive polytope with boundary `(λ,μ,ν)`. The open KTT conjecture says
> `P` has nonnegative monomial coefficients. Ehrhart polynomials of general lattice
> polytopes are NOT always positive (Reeve simplex, dim 3, negative linear
> coefficient). But an exhaustive dual-oracle scan of thousands of LR hive
> polytopes (all `length ≤ 6`, small size) found **zero** negative coefficients,
> and the minimum non-leading coefficient decreased only mildly (≥1 at degree ≤3
> to 5/12 at degree 4). [Paste the current per-(rows,degree) min-nonleading trend
> from `run/p3/positivity_trend.json` here.]
>
> **Task.** Identify whether LR hive polytopes plausibly belong to a **known
> Ehrhart-positive class**, and what would prove it or predict its failure. Address
> specifically: (i) do hive polytopes have a regular unimodular triangulation / are
> they IDP / compressed / do they admit a Gröbner or shelling structure relevant to
> Ehrhart *coefficient* positivity (not merely nonneg `h*`)? (ii) is there a known
> theorem giving Ehrhart positivity for flow/transportation/Gelfand–Tsetlin-type
> polytopes that hives specialize or relate to? (iii) failing a positivity
> mechanism, what structural feature (which degree, which boundary degeneracy) would
> be the most likely site of a first negative coefficient — i.e. where should the
> counterexample search (P3) concentrate?
>
> Distinguish carefully: nonneg `h*`-vector does NOT imply nonneg Ehrhart
> *coefficients*; do not conflate them.

Return: a ranked assessment — the most plausible known class or theorem hives fall
under (with the precise statement to check), OR the sharpest structural reason to
expect a high-degree failure and where to aim P3. Concrete and auditable; no
padding. This is a recognition prior, not a proof — any positivity claim is
adjudicated by prior-art check and, if pursued, a real proof.
