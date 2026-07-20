# DSSYK Constraint-Access Gate

Date: 2026-07-16

Status: superseded as the active successor gate by
`observer_relative_temporal_access_successor_proposal_2026_07_16.md`; retained
for the audit trail. No DSSYK computation was performed under this version.

The earlier comb and matched-control derivation in
`notes/dssyk_comb_and_factorized_null_2026_07_16.md` is also superseded. The
corrected proposal uses the one-copy physical spectral density, an explicit
shell diary encoder, an isospectral one-copy control, and the natural dressed
observer protocol.

This gate tests whether the equal-energy constraint in doubled DSSYK produces
an operational information-access effect beyond a matched ordinary finite
reservoir. It is not a generic DSSYK/dS-holography project and it does not
assume that the cosmological constant is literally a UV cutoff.

## Start rule: literature overlap remains mandatory

The triviality stop condition and the literature-overlap condition are
independent. The project must complete the following bounded pass before any
external novelty claim:

1. **Attribution.** The primary source for the doubled infinite-temperature
   construction coupled by an equal-energy condition `H_L = H_R` is
   Narovlansky--Verlinde, arXiv:2310.16994. The earlier Rahman and Susskind
   papers are primary sources for the DSSYK-infinity/dS-JT conjectural line:
   arXiv:2209.09997 and arXiv:2209.09999. Rahman--Susskind's response to the
   Narovlansky--Verlinde interpretation is arXiv:2312.04097, with the
   temperature clarification in arXiv:2401.08555. These roles must remain
   distinct in later writing.
2. **Recovery-grade overlap.** Search the doubled equal-energy model for a
   recovery fidelity, decoupling error, diary dependence, channel/comb
   distinguishability, process tensor, or observer-record quantity. Entropies,
   static correlators, pole-skipping, complexity, scrambling, and algebra type
   alone do not satisfy this check.

The pass is a gate even if the eventual computation is nontrivial. A prior
recovery-grade result would change the project from a proposed calculation to
an overlap/reframing decision.

### Initial bounded scan

The abstract-level scan found the following near-misses, none of which is yet
the target quantity:

- Narovlansky--Verlinde compute constraint-preserving dressed two-point
  functions in the doubled equal-energy model, not a recovery fidelity or a
  sequential record channel.
- Rahman--Susskind analyze the DSSYK-infinity/dS-JT interpretation, including
  temperature distinctions and disagreements over entropy/energy scaling, not
  dynamical diary access.
- Tietto--Verlinde introduce a dS model with an observer and match entropy to
  the DSSYK spectral density, but do not define a recovery protocol.
- Xu derives the Type II_1 DSSYK algebra and its modular structure; this is
  algebraic access structure, not a comb-level recovery quantity.
- Rajgadia--Xu study microscopic purity in DSSYK: generic probes lose access
  to KM-state purity while state-adapted dressed operators restore it. This is
  the closest access-related near-hit, but it is an observable-algebra
  comparison rather than a recovery-grade temporal-access calculation.
- Cao--Gao analyze a single-sided DSSYK/EOW-brane model, commutants, and a
  no-man's-island interpretation. It is not the doubled equal-energy model
  with a diary/observer comb.
- Narovlansky's later microscopic dS-dynamics proposal studies gauge-invariant
  correlators and OTOCs, not a diary-blind comparison process.

Provisional result: no direct recovery-grade calculation was found in the
abstract-level scan. This is **not** the final overlap verdict. The primary
texts must still be read for hidden uses of fidelity, decoupling, conditional
mutual information, state discrimination, or an equivalent channel quantity.

### Primary-text checkpoint (2026-07-16)

The full-text checks completed so far strengthen, but do not broaden, that
provisional result. Rahman--Susskind's response (arXiv:2312.04097) and their
temperature paper (arXiv:2401.08555) contain the DSSYK/dS dictionary,
entropy/energy/temperature comparisons, and the relevant construction history;
searches for recovery, diary, and information-decoupling language did not
locate a recovery-grade comb or channel quantity. The latter paper's
"tomperature" discussion concerns freezing/removing a qubit to define a
temperature, not extracting a diary.

The current closest hits remain algebraic or state-structural: Rajgadia--Xu
(arXiv:2604.14387) compare generic and state-adapted probes of microscopic
purity, while Cao--Gao (arXiv:2511.01978) study commutants and reconstruction in
a single-sided EOW model. Neither computes the present sequential,
diary-blind process defect in the doubled equal-energy model. Accordingly the
literature gate is recorded as **no direct overlap found in the bounded scan;
near-hit distinction documented**, rather than as a novelty claim.

## Definition gate: the comb is the first technical deliverable

Before calculating a DSSYK number, define a finite time-binned observer comb.
For bins `j = 1,...,K`, specify:

- the constrained system and its microcanonical shell;
- the observer memory and clock registers;
- the sequential measurement/interaction channel
  `Phi_j: M_{j-1} -> M_j tensor R_j`, where `R_j` is the record bin;
- the class of allowed clock settings and observer interventions;
- the hybrid-reachable state set used to evaluate the defect;
- the diary-blind comparison comb `Psi_j` on the same spaces, with the same
  measurement schedule and shell marginal but with the diary label scrambled
  or removed from the interaction.

The step defect is the Result-B quantity

```text
eta_j = sup over hybrid-reachable states sigma
        || [(Phi_j - Psi_j) tensor id_(A R_<j)](sigma) ||_1,
```

with the appropriate code restriction and energy constraint. The record-level
distance is then bounded by `D_K <= sum_j eta_j`. If this comb cannot be
defined without silently choosing the answer through the record algebra, the
gate stops at definition rather than proceeding to correlator calculations.

## Ensemble gate: preserve the diary label

DSSYK calculations commonly use an ensemble average. That average is part of
the definition and cannot be postponed until after the access calculation.
Choose one of two admissible routes:

1. **Label-preserving average.** Define the diary insertion and the
   constraint-preserving observer channels so that averaging over disorder
   leaves a well-defined diary label and a nontrivial averaged comb.
2. **Per-realization route.** Define `D_K(omega)` for each disorder
   realization and report both its mean and variance (or a rigorous
   concentration bound). The variance must be propagated to the recovery or
   distinguishability quantity.

An averaged channel in which the diary label disappears is not evidence for
diary blindness; it is an undefined averaging order for this question. The
project's `self_averaging_variance.md` is the required technology for the
per-realization/concentration branch.

## Null gate: pre-register the matched control curve

The factorized control is computed first. It must be matched to the DSSYK
constraint surface microcanonically:

- same shell density of states, not merely the same `S_0` and temperature;
- same total energy shell and allowed energy bins;
- same observer clock, record bins, interventions, and measurement schedule;
- same marginal record statistics after the diary is removed.

Define the null curve before evaluating DSSYK:

```text
D_null(K) = sum_{j=1}^K eta_j^contact,
```

where `eta_j^contact` is derived from the matched factorized reservoir and
its declared contact/transport channel. If the benchmark is chosen to be
strictly diary-blind by construction, its special limiting curve is
`D_null(K) = 0`; that exact-zero benchmark must not be confused with the more
physical ordinary-contact benchmark, whose transport curve must be derived
from the reservoir lemma and its contact assumptions.

The DSSYK result is relevant only if it exceeds the pre-registered null in a
declared sense—scaling, integrated defect, or recovery error—and not merely if
it is nonzero. No DSSYK curve may be interpreted before `D_null(K)` is written
down.

## DSSYK calculation and stop conditions

Only after the three gates above are closed:

1. construct a constraint-preserving diary insertion on the doubled
   equal-energy model;
2. build the observer comb and its diary-blind comparison;
3. compute the label-preserving or per-realization defect curve;
4. compare it to `D_null(K)` under the same microcanonical data.

Stop or reframe if:

- the literature already contains the recovery-grade quantity;
- the disorder average erases the diary and the variance is uncontrolled;
- the factorized control cannot be matched on the same shell;
- the observer record cannot be defined as a sequential channel with memory;
- the DSSYK curve only reproduces known entropy, correlator, algebra,
  scrambling, or complexity bookkeeping; or
- the constrained curve does not beat the pre-registered ordinary-reservoir
  curve.

## Scope and intended payoff

The payoff is a constraint/access comparison, not a proof of DSSYK/dS
duality and not a solution of the cosmological constant problem. A positive
result would show that the equal-energy/observer constraint changes an
operational temporal-access invariant relative to a microcanonically matched
factorized reservoir. A null result would be useful too: it would support the
view that the dS signatures under study are ordinary finite-reservoir or
bookkeeping effects rather than a distinct information-access mechanism.

## Historical decision under this superseded gate (2026-07-16)

This was the decision before the one-copy spectral correction and is retained
only for provenance. It proposed a finite-shell observer-comb comparison
against the frozen ordinary contact envelope. The active proposal instead
uses the isospectral one-copy control and parks dynamics at the resource gate;
none of the actions below this historical decision remain queued.

## Primary references for the attribution pass

- Rahman, [dS JT Gravity and Double-Scaled SYK](https://arxiv.org/abs/2209.09997).
- Susskind, [De Sitter Space, Double-Scaled SYK, and the Separation of Scales](https://arxiv.org/abs/2209.09999).
- Narovlansky and Verlinde, [Double-scaled SYK and de Sitter Holography](https://arxiv.org/abs/2310.16994).
- Rahman and Susskind, [Comments on a Paper by Narovlansky and Verlinde](https://arxiv.org/abs/2312.04097).
- Rahman and Susskind, [Infinite Temperature is Not So Infinite](https://arxiv.org/abs/2401.08555).
- Tietto and Verlinde, [A microscopic model of de Sitter spacetime with an observer](https://arxiv.org/abs/2502.03869).
- Xu, [Von Neumann Algebras in Double-Scaled SYK](https://arxiv.org/abs/2403.09021).
- Rajgadia and Xu, [Emergent States and Algebras from the Double-Scaling limit of Pure States in SYK](https://arxiv.org/abs/2604.14387).
- Cao and Gao, [Single-Sided Black Holes in Double-Scaled SYK Model and No Man's Island](https://arxiv.org/abs/2511.01978).
- Narovlansky, [Towards a microscopic description of de Sitter dynamics](https://arxiv.org/abs/2506.02109).
- [Self-averaging variance technology](self_averaging_variance.md).
