# Boundary Saturation as the Operational Horizon Invariant — working note

Started 2026-06-12, post literature pass (see
`ds_literature_collision_matrix_2026_06_12.md`). The research claim is
conditional on two technical moves: an intrinsic definition of the
accessible source-side channel count that cannot be dismissed as
coupling normalization, and an exterior certificate for that count that
survives the shared-mode bottleneck. The first is the Gram-kernel
participation number below. The second is now the recovery-latency
criterion of Section 5.5.

## 0. The claim and the contrast engine

**Claim.** The operational definition of a horizon is a thermal system
whose entire entropy is coupling-accessible:
$$\sigma \equiv \lim \frac{\log N_{\rm access}}{\log S} = 1,$$
versus $\sigma = (d-1)/d$ (= 2/3 in three dimensions) for any ordinary
local reservoir coupled through a contact surface.

**Why this is not a stretched-horizon slogan — the contrast engine.**
The invariant is the unique survivor of running the same demarcation on
both horizons:

- *Schwarzschild* makes the state-count input exotic: $S(E) \sim E^2$
  is super-Hagedorn, provably unavailable to local systems (the
  holographic entropy mismatch). Constraint structure: pedestrian
  (factorized exterior suffices for the operational package).
- *de Sitter* makes the state-count input ordinary: the reservoir lemma
  (`ds_operational_horizon.md`) shows the SdS horizon entropy deficit
  is generic finite-bath thermodynamics through second order, with
  $C_{\rm eff} = S_0$. Constraint structure: where the dS mystery
  concentrates.
- *Boundary saturation survives both*: $N_{\rm access} \sim S$ is
  forced by the Schwarzschild luminosity law and required of the dS
  horizon register, while every ordinary bath — including the one that
  realizes the dS spectrum — violates it.

So the spectrum input flips (impossible ↔ trivial) between the two
horizons; saturation does not flip. It is also: geometry-free (statable
in a model with no metric), falsifiable by a scaling exponent, and
violated by systems that satisfy every geometric entropy bound. None of
the four ancestors (stretched horizon, membrane paradigm, holographic
bound, fast-scrambler connectivity) has these properties — see §5.

**Updated framing (2026-06-21): useful ancestry, not avoidance.**
The old membrane/complementarity picture says that, for the exterior
observer, the horizon behaves as an entropy-carrying absorbing and
emitting surface. Boundary saturation is the quantitative version of
that intuition: it asks how much of the entropy-counting Hilbert space is
actually exposed to the exterior coupling algebra. The ancestors are
useful rather than threatening: stretched horizon supplies the
absorbing/re-emitting surface picture, membrane paradigm supplies
surface response, holography supplies the area state count, absorption
universality supplies the area-strength exterior coupling, and
Bekenstein-Mayo supplies the compressed one-dimensional flow. The added
move is to combine them into a source-side participation invariant and
compare it with ordinary reservoirs.

## 1. Lemma 1: the participation channel count

**Setup.** A system shell $\mathcal H_E$ couples to an external
continuum through operators $\{O_\mu\}$. The inclusive emission
(absorption) physics at frequency $\omega$ is controlled by the
**channel Gram kernel**
$$W_{\mu\nu}(E,\omega) = \frac{1}{D_E}\,
\mathrm{Tr}\!\left[\Pi_{E-\omega}\,O_\mu\,\Pi_E\,O_\nu^\dagger\right],$$
a positive-semidefinite Hermitian matrix on channel space (the
shell-averaged Hilbert–Schmidt Gram matrix of the jump operators).

**Definition (participation channel count).**
$$N_{\rm eff}(E,\omega) = \frac{(\mathrm{Tr}\,W)^2}{\mathrm{Tr}\,W^2}
= \frac{\big(\sum_a \lambda_a\big)^2}{\sum_a \lambda_a^2},$$
the participation ratio of the eigenvalues $\lambda_a$ of $W$.

**Current proof target after the literature guard (2026-06-20).**
The result worth protecting is not a new formulation of Hayden-Preskill
recovery, fast scrambling, or the membrane paradigm. It is the
source-side separation:

```text
boundary saturation:
    sigma_acc = limsup log N_eff(source Gram kernel) / log S = 1

ordinary local reservoir with contact coupling:
    sigma_acc <= (d-1)/d
```

Here "source-side" means that the channel labels are the microscopic
operators in the emission Hamiltonian. They are not outgoing radiation
modes. A shared long-wavelength exterior mode may compress the radiation
coherence matrix to O(1) rank while the source Gram kernel still has
N_eff ~ S. This is exactly why the flux/HBT measurement route failed,
and why the theorem must be stated as a coupling-algebra invariant.

The exterior latency theorem remains useful, but it is downstream: it
certifies the obstruction operationally once mixing/export assumptions
are included. It is not the invariant itself.

**Lemma 1 (invariance and dichotomy).**
(i) $N_{\rm eff}$ is invariant under unitary rebasing of the channel
labels and under overall coupling rescaling $W \to \lambda W$: it is a
spectral invariant of the coupling algebra's image in shell operator
space, not a convention.
(ii) Comparable independent channels of rank $N$ give
$N_{\rm eff} \simeq N$; coherent/aligned (Dicke-type) coupling gives
$N_{\rm eff} \simeq 1$ regardless of the microscopic label count. The
comparable-channel caveat of the long paper's Prop 2 is hereby absorbed
into the definition: $N_{\rm eff}$ *is* the effective participation
count.
**Superseded measurement route.** The first attempt was to identify
$\mathrm{Tr}\,W$ with the mean flux and $\mathrm{Tr}\,W^2$ with a
second-order flux/HBT observable, making $N_{\rm eff}$ directly
measurable from emission statistics. Section 5.5 records why that route
fails for horizon emission: shared outgoing modes make flux
correlations measure radiation-mode participation, not source-kernel
participation. Current status: (i) and (ii) stand as the intrinsic
model-side definition; the exterior certificate is recovery latency,
not flux moments.

## 2. Lemma 2 (Schwarzschild leg)

Restate Prop 2 of the long paper invariantly: within the weak-emission
microcanonical class with $p=2$ phase space, the Schwarzschild
luminosity law calibrates $N_{\rm eff}(E) \propto E^2 \propto S(E)$, i.e.
$\sigma = 1$. (The old "comparable channels" hypothesis becomes the
statement that $N_{\rm eff}$, not a label count, is the source-side
participation count entering the inclusive-rate model.)

## 3. Lemma 3 (ordinary-reservoir bound)

For a local finite-range Hamiltonian in $d$ spatial dimensions coupled
to the continuum through a contact surface: the jump operators are
supported on surface sites, so the Gram kernel's rank is bounded by the
dimension of the surface operator space active in a thermal window,
$\mathrm{rank}\,W \lesssim A_{\rm contact}/\lambda_T^{d-1}$, while
$S \sim V/\lambda_T^d$. Hence
$$N_{\rm eff} \lesssim S^{(d-1)/d},$$
i.e. $\sigma \le (d-1)/d$ strictly below saturation. This is the
converse half that makes the criterion nontrivial. The draft now states
it at lattice scale: few-body surface operators span at most
$c_r|\partial\Lambda|$ source directions, participation never exceeds
rank, and the thermal-window restriction can only reduce the count or
tighten constants. The theorem is therefore insensitive to coupling
normalization, source-basis choice, outgoing-mode rank, and later
decoder processing.

## 4. dS leg

The dS horizon register, by input 2 of `ds_operational_horizon.md`, has
$N_{\rm eff} \sim S_0$ — a reservoir whose entire entropy is in its
contact cells — versus $S_0^{2/3}$ for the ordinary bath that mimics
its spectrum (reservoir lemma). The old equilibrium-fluctuation
measurement route is superseded by the shared-mode obstruction of
Section 5.5. The dS leg should be restated in latency form: perturb the
static patch and ask after how many exchanged Gibbons-Hawking quanta the
perturbation is recoverable from the horizon record. *To do: check dS
Hayden-Preskill literature and formulate the equilibrium recovery
protocol.*

## 5. Ancestors (referee-proofing section)

Current stance: use the ancestors constructively. Stretched horizon and
complementarity supply the exterior story; membrane paradigm supplies the
surface-response language; holography supplies the area state count;
absorption universality supplies the area-strength exterior coupling;
Bekenstein-Mayo/Pendry supplies the compressed one-dimensional flow; fast
scrambling supplies the internal mixing input. Boundary saturation combines
these into a source-side participation invariant and compares it with
ordinary reservoirs.

Each adjacent idea differs in kind:
- **Stretched horizon (Susskind–Thorlacius–Uglum):** postulate about
  where entropy *resides*; presupposes the geometry; no measurable
  criterion. Saturation is a measurable exponent, geometry-free.
- **Membrane paradigm:** operational surface transport coefficients; no
  entropy-vs-channel-count statement.
- **Holographic principle:** geometric *bound* $S \le A/4$; saturation
  is a dynamical *equality* about the coupling algebra. An ordinary
  bath satisfies every holographic bound and violates saturation.
- **Fast-scrambler connectivity (Sekino–Susskind, SYK):** internal
  interaction graph (the mixing input); saturation concerns the
  external coupling algebra (the emission input). Distinct inputs in
  the trinity; conflating them is the likeliest referee error —
  preempt explicitly.

## 5.5 Obstruction found in Lemma 1(iii) (2026-06-12) — and the candidate repair

**The flux-statistics route fails.** The plan was: mean flux measures
Tr W, HBT/intensity correlations measure Tr W², ratio gives N_eff. But
HBT acts on the *radiation* coherence matrix, and the collective
bottleneck (the record-capacity result of the long paper) intervenes:
distinct source channels feed the same few outgoing modes
(Schwarzschild: λ ~ 1/T ~ R, so O(1) angular channels — s-wave
dominance, Page 1976). Flux statistics therefore measure the
radiation-mode participation (~O(1) per coherence time), NOT the
source-kernel participation (~S). The Gram-kernel N_eff is still
well-defined and invariant (ETH makes W near-diagonal over emitters in
shell space, so N_eff(source) ~ N regardless of shared outgoing
modes), but it is not exterior-measurable through flux moments.

**Worse, the naive "absorption measures area-many channels" reading is
threatened:** σ_abs ~ A at λ ~ R means σ/λ² ~ O(1) — the horizon is
O(1) outgoing modes at the per-mode unitarity limit, not many weak
ones. The long paper's Prop 2 survives because it is explicitly
within-class (standard per-channel ETH strength); the saturation paper
wanted to do better than within-class, and flux moments don't get
there.

**Candidate repair — the latency invariant.** What *is*
exterior-measurable, normalization-free, and distinguishes the two
scalings is the Hayden–Preskill recovery latency for centrally
deposited information:

- horizon system: a diary deposited anywhere becomes
  radiation-recoverable after t_scr ~ β log S (plus O(k) quanta) —
  polylog(S) latency for ALL of the entropy;
- ordinary d-dim bath: bulk-deposited information must diffuse to the
  contact surface first, τ_diff ~ R²/D ~ S^{2/3}β-ish — power-law
  latency for bulk content.

Latency is a time measured in emitted quanta against the coherence
time β: dimensionless, basis-free, coupling-normalization-free. So the
operational form of boundary saturation becomes:

> **Horizons are thermal systems whose full entropy is
> exterior-recoverable at logarithmic emitted-record latency;**
> ordinary reservoirs have power-law latency exponents set by interior
> transport.

(Locked framing, user 2026-06-12: **boundary saturation is the hidden
model-side condition; recovery latency is its exterior certificate once
mixing is included.** The "once mixing is included" clause is part of
the framing — the certificate tests the conjunction, and a saturated
but slow-mixing system fails it; this absorbs the thermal-tie
conditionality honestly rather than hiding it.)

This (i) keeps the geometry-free, exponent-falsifiable character,
(ii) survives the collective bottleneck (recovery statements live on
records over time, not on instantaneous mode counts), and (iii) ties
input 2 to input 3: the latency invariant is where boundary
accessibility and mixing jointly become exterior-visible — arguably
the deeper reason both inputs appear in the trinity. Cost: it imports
the scrambling/thermal-tie conditionality of Prop 8.

**Status of the definitions:** keep the Gram-kernel N_eff as the
*model-side* (intrinsic) definition — Lemma 1(i)-(ii) stand — and
state its exterior certificate as the latency exponent, not flux
moments. Lemma 1(iii) is replaced by a latency lemma: horizon-class
models give Hayden-Preskill recovery latency $O(k+\log S)$ emitted
quanta for a diary of entropy $k$, conditional on mixing and the
thermal tie. Local-bath models give latency bounded below by interior
transport. The safe theorem is ballistic Lieb-Robinson, $\sim S^{1/d}$
for a bulk deposit at distance of order the system radius; the physical
diffusive expectation is $\sim S^{2/d}$. Either separates power-law
from logarithmic latency, which is all the dichotomy needs.

## 5.6 The compression pivot (2026-06-12, locked architecture)

**Compression is a horizon signature, not an obstacle.** It is
equivalent to the spectral input: $T R = O(1)$ (one-wavelength system)
⟺ the radiation field has $O(1)$ modes per coherence time. Both
horizons satisfy it; ordinary bodies ($\lambda_T \ll R$) do not.

**Critically provisioned channel.** $O(1)$ nats per $\beta$ over
$\tau/\beta \sim S$ steps — total exactly $S$, no slack. Literature
anchor (verified): Bekenstein–Mayo 2001, "Black holes are
one-dimensional" — black holes behave as one-dimensional
entropy/information channels; Pendry's information-flux bound behind
it. Cite both.

**Forced-mixing lemma: STRONG VERSION FALSE.** The claimed implication
(inputs 1+2 + unitarity + compression ⟹ mixing) fails to a
countermodel: a serial tape-readout purifies $S$ bits through one mode
over $O(S)$ emissions using *time-bin orthogonality* — no fast
scrambling, records orthogonal in time through the same mode.
Compression + unitarity force **serialization only**.

**Corrected theorem target (the sharp version):**
> compressed channel + state-independent evaporation +
> Hayden–Preskill latency $O(k+\log S)$ for *arbitrarily deposited* diaries
> ⟹ fast routing/mixing.
Eventual purification needs only tape reading; *rapid recoverability
of a newly deposited qubit* requires the deposited information to
reach the few coupling directions within $O(k+\log S)$ emitted records —
which ordinary local baths cannot do, and horizons do only if
accessibility and mixing act together.

**The locked six-point architecture:**
1. $TR = O(1)$ gives a compressed exterior channel.
2. The channel is critically provisioned: $O(1)$ nats per $\beta$ over
   $\tau/\beta \sim S$ steps.
3. Therefore horizon information flow is temporal/serial, not
   instantaneous/spectral.
4. Boundary saturation is not directly seen in flux moments.
5. The exterior certificate is Hayden–Preskill latency.
6. Fast mixing is not forced by unitarity alone; it is forced by
   logarithmic recovery latency for arbitrary deposited information.

The trinity does not reduce to two inputs + unitarity; it becomes more
integrated: **compression explains why accessibility and mixing are
exterior-visible only as a joint temporal exponent.**

## 5.7 Stress-test program and taxonomy (Codex discussion + AdS check, 2026-06-13)

See also `notes/horizon_property_separation_program.md` for the
standalone separation-program version: predicates, witness systems,
theorem candidates, and the novelty audit.

**Where the road leads (endpoint articulation, Codex):** an operational
theory/taxonomy of horizons — ordinary reservoirs (power-law latency) /
fast scramblers without saturation / saturated-but-slow systems /
horizons (saturation + log latency) / gravitational horizons (the above
+ geometric completion + constraint dressing). The short paper has the
theorem; this program identifies the invariant behind it. The taxonomy
is the saturation paper's discussion section.

**Compression scope check (new, ours):** large AdS black holes have
$TR \sim r_+^2/L^2 \gg 1$ — NOT compressed; small AdS / flat
Schwarzschild / dS have $TR \sim 1$. The dividing line is Hawking–Page:
**compression ⟺ the negative-heat-capacity (evaporating) regime.**
Resolution of the apparent tension: the universal invariant is
saturation of the *source* algebra (Planck cells, $N \sim S$) +
latency certificate; the *bandwidth* $B \sim A/\lambda_T^{d-1}$ nats
per $\beta$ distinguishes serial horizons ($B \sim O(1)$: flat
Schwarzschild, dS, small AdS — critically provisioned over lifetime)
from parallel horizons ($B \gg 1$ but still $\ll S$: large AdS, planar
Rindler — Codex's one-channel-per-thermal-cell density form). In all
cases radiation channels $\ll$ source channels, so the certificate is
temporal universally. Falsifiable internal prediction: for parallel
horizons some channel structure returns to spectral visibility (flux
statistics partially work for large AdS BHs).

**Stress-test ranking:**
1. *Near-extremal / JT* — the dangerous one: at $T \to 0$, does
   latency certify all of $S_0$ or only the thermally active sector
   $\Delta S(T)$? Connects to the near-extremal spectrum literature
   (Iliesiu–Turiaci line). Outcomes: invariant refines to
   "dynamically active entropy," OR near-extremal fails the
   certificate ⇒ the invariant characterizes *evaporating* horizons.
   Must be addressed in the paper's discussion before a referee does.
2. *BTZ / large AdS* — tests compression scope (see check above);
   holographic dictionary: saturation/latency as CFT operator-growth
   statements.
3. *Causal diamonds* — bridge to observer horizons; saturation for
   finite observer-accessible regions without event horizons.
4. *Rindler* — local lemma factory only: exact thermality
   (Bisognano–Wichmann), channel density $A_\perp/\beta^{d-1}$, no
   finite entropy/lifetime/record without regulation; clarifies that
   Schwarzschild's global seriality = "the whole horizon is one
   thermal cell" ($\beta \sim R$).
5. *Analogue horizons* — negative control for the paper: pass
   (kinematic) thermality, fail saturation/latency; proves thermality
   alone was never the horizon content. Cheap, add to "what saturation
   is not."

## 5.8 The anonymity hypothesis (user's intuition, 2026-06-13)

**Source intuition:** the horizon is a great anonymizer — infalling
matter smears into "indescript red-shifted goo" over the whole horizon
(no well-defined entry point), and radiation "coalesces from everywhere
and nowhere in particular" (no traceable emitter).

**Mapping to existing structures:** infall anonymization = classical
face of fast scrambling (charge-spreading on the stretched horizon, the
origin of Sekino–Susskind); emission anonymity = the collective-jump
lemma in words ($b^\dagger$ carries no $\mu$); $\lambda \sim R$ = the
one-pixel camera: a Schwarzschild black hole is a macroscopic thermal
system whose own quanta have wavelength of order the system size, so
its radiation cannot image microscopic source location. Ordinary bodies
with $\lambda_T \ll R$ are self-imaging; parallel horizons are imageable
at thermal-cell, never source-cell, resolution.
Anonymity = no-hair, operationalized (only conserved charges survive;
ringdown leaks O(1) multipole bits).

**Definition (anonymous emission channel, locked wording):**

> An anonymous emission channel is one whose emitted record is
> covariant under permutations of microscopic source cells, so no
> resolvable record variable — source label, outgoing mode, frequency,
> or timing — identifies which cell supplied the information, beyond
> conserved charges and coarse no-hair data.

Clean, formalizable, aligned with the collective-jump result; the
model already satisfies it (vertex-transitive mixer, collective jump).

**Load-bearing consequence — the alternatives theorem (corrected;
"anonymity ⟹ mixing" was too fast):** the tape-readout countermodel
of §5.6 is a non-anonymous channel — the time-stamp is a return
address — so anonymity closes that loophole. But it does not by itself
derive mixing: a highly nonlocal anonymous *encoder* could read global
collective functions of the state over time, preserving anonymity and
unitarity while hiding the mixing inside the emission operator. The
defensible theorem target is a no-free-lunch / routing statement:

> **(Locked theorem statement, Codex 2026-06-13.)** Given compression,
> anonymity, and restricted source-local emission access, unitary
> release of arbitrary microscopic information requires either
> sufficient internal routing/mixing or an emission map whose action
> is already nonlocal on the source algebra.

Anonymity does not derive mixing; it forces the information-routing
burden *somewhere*. Horizons appear to discharge it via fast
scrambling / no-hair dynamics. The demarcation reading of the two
branches — internal routing = factorized scrambling model;
nonlocal encoder = Gauss-law/holography-of-information access —
stays **peripheral, discussion-only**: the theorem itself remains
operational and finite-dimensional.

**One-pixel camera, softened (locked wording):** a Schwarzschild black
hole is a macroscopic thermal system whose own quanta have wavelength
of order the system size, so its radiation cannot image microscopic
source location. (Small cold objects can also be one-wavelength
emitters; they lack the entropy/capacity structure.)

**Where it goes:** long paper — already present technically
(collective jumps, resolvable records), no change; operational note —
at most one discussion sentence; boundary-saturation paper — yes,
refines the latency theorem target.

**Third face of the merged question:** a condensate of identical
bosons in one soft mode is structurally anonymous (which-constituent
is meaningless by permutation symmetry). So: saturation origin /
corpuscular stabilization / anonymity are plausibly one microscopic
question — why is gravity's bound state a permutation-symmetric,
mode-degenerate condensate: an anonymous channel operating at
capacity.

## 5.9 T2 literature positioning + proof spec (Codex pass, 2026-06-13)

**Verdict:** the exact alternatives theorem is not a standard named
result; the ingredients are known. Do NOT pitch as "horizons anonymize
information" (too close to no-hair / stretched-horizon / scrambling
folklore). The new value is the **trichotomy collapse**: compressed
anonymous emission cannot be simultaneously source-local, slow-routing,
and fast-recovering — one of locality or slow routing has to go.

**Anchor list (for the T2 session's related-work section):**
- Hayden–Preskill 0708.4025 — proves fast recovery *assuming* the
  scrambling encoder; T2 asks what makes that assumption possible
  under a compressed anonymous channel.
- Sekino–Susskind 0808.2096 — motivates the routing scale; T2 makes
  fast scrambling a forced branch, not a benchmark.
- Susskind–Thorlacius–Uglum hep-th/9306069 — anonymizer intuition is
  old; cite, don't claim.
- Braunstein–Pati no-hiding gr-qc/0603046 — related background (info
  absent from one subsystem is in the complement); lacks locality,
  source addresses, compression, latency.
- Bekenstein–Mayo gr-qc/0105055 — the compression premise; T2's
  novelty is coupling compression to anonymity + HP latency.
- HP-in-Hamiltonians, arXiv 2303.02010 — HP recovery is a stronger
  diagnostic than local OTOC growth; supports latency-over-spectral.
- Raju 2012.05770 — the nonlocal-encoder branch's home: gravity makes
  interior info available through constraints; in T2 it is the second
  alternative (the exterior algebra was never source-local).

**Framing map (use verbatim-ish):** HP proves fast recovery assuming
scrambling; fast-scrambler lore motivates the required routing scale;
LR bounds (Theorem 1) show ordinary local reservoirs fail it; Raju/HoI
supplies the nonlocal alternative; the anonymity theorem identifies why
those are the two branches once the exterior channel has no source
return address.

**No-smuggling proof spec (the hypotheses must be independently
checkable so "nonlocal encoder" is not defined as "whatever else"):**
1. *Source-local access* = property of the jump operators alone:
   supports of $O_\mu$ are $O(1)$-local patches of the source algebra
   (checkable before any dynamics).
2. *Fast routing* = property of the internal dynamics alone: evolved
   deposit operators develop overlap with the coupling algebra within
   the latency window (operator-growth statement, quantifiable via the
   Gram overlap of $V(t)$ against the emission algebra).
3. *Theorem obligation:* with (1) source-local access and NOT-(2), show
   latency fails — structurally Theorem 1's argument with the geometric
   light cone replaced by the operator-growth cone of the actual
   internal dynamics.

**Candidate proof path (new, from the tape-readout autopsy):** latency
≥ routing time, because information must reach the coupling directions
before it can enter the record (data-processing). The tape readout
evaded this because each cell was *pre-aligned* with a future record
direction (its own time-bin) — zero routing needed. Anonymity =
permutation covariance = **no cell is preferentially aligned with any
record direction**, so the deposit must be rotated into the collective
coupling directions before emission can carry it: routing is
unavoidable, and the only question is who performs the rotation — the
internal dynamics (branch 1) or the emission map itself (branch 2,
which then cannot be source-local). This turns the dichotomy from a
disjunction-by-exhaustion into a conservation statement about where
the rotation happens.

## 5.10 Temporal-certificate forcing argument + decoder-complexity axis (2026-07-03, in paper)

Two additions to `paper_boundary_saturation/main.tex` from the
hyperbolic/elliptic locality discussion (Carroll–Singh mad-dog thread).

**(a) Why the certificate is temporal — forcing argument, Discussion
section.** Upgrades §5.5's "flux moments failed" to "they had to fail":
stationary horizons (Rindler, eternal, large AdS) admit an equilibrium
dictionary — exact KMS state, Euclidean saddle, Bisognano–Wichmann /
Israel TFD — that ties stationary response/fluctuation spectra to
interior state structure, so state-side structure has a *spectral*
exterior representation there. Schwarzschild evaporation is on the
other side of the Hawking–Page divide: negative heat capacity ⇒ no
canonical ensemble, no stationary KMS state to refer long-time spectral
data to. Combined with compression (O(1) modes per coherence time), the
only exterior-visible face of entropy-sized structure is the time
ordering of the emitted record ⇒ latency certificates are forced, not
chosen. Independently corroborates the §5.7 compression/Hawking–Page
divide. New refs: BisognanoWichmann1976, Israel1976,
GibbonsHawkingAction1977.

**(b) Two-exponent remark, end of Dynamical Counterpart section.**
Recovery separates into arrival (decoupling latency; our axis) and
extraction (decoder complexity; Yoshida–Kitaev efficient with known
dynamics, Harlow–Hayden hardness, Python's-lunch geometric criterion).
The exponents can diverge — log-arrival with exponential extraction is
a possible class — and the paper now states explicitly that its
classification is by arrival latency, insensitive to decoder resources.
Connects to the access-profile note's decoder-complexity axis
(`paper_access_latency_classification`); taxonomy row for §5.7 if the
taxonomy section is ever written out.

## 6. Open items, in order (revised after §5.5)

1. **Latency lemma, horizon half: DONE 2026-06-13** — Lemma
   "Horizon half: logarithmic latency" in the Schwarzschild-leg
   section, proof by import (decoupling budget k + 2log(1/ε) nats at
   O(1) nats/quantum, plus O(log S) re-scrambling quanta conditional
   on the thermal tie; HP regime removes the Page-time wait). Also
   closed same day: Schwarzschild luminosity lemma proof via the exact
   identity Tr W = N_eff·λ̄ with λ̄ ≡ Tr W²/Tr W (the class hypothesis
   "λ̄ = standard ETH envelope" is the invariant form of comparable
   channels); contact-scaling lemma proof (few-body surface operators
   ⇒ rank W ≤ c_r|∂Λ| ~ S^{(d-1)/d}, participation ≤ rank,
   lattice-scale counting suffices for the exponent); deposit-symmetry
   remark (fourth remark after Theorem 1); validity clause
   k + log(|B|/ε) = o(S^{1/d}) added to Theorem 1; abstract advertises
   state-independence.
2. **Latency lemma, bath half (the new conditional move): DONE
   2026-06-12** — Theorem 1 (+ exterior-light-cone lemma + no-bulk-
   fraction corollary) in `paper_boundary_saturation/main.tex`,
   ordinary-reservoir section. Proof architecture: exterior (field +
   apparatus + ancillas, arbitrary time-dependent H_E = adaptive
   protocols via Stinespring) attached as a single auxiliary vertex to
   the interaction graph; arbitrary on-site H_E removed by interaction
   picture, so LR holds with constants set by (J, g, r, d) only; every
   path exterior→bulk traverses the bulk, distance ≥ L/a. Twirl over
   the deposit region converts the LR commutator into Q–E decoupling
   ‖ρ_QE − π⊗ρ_E‖₁ ≤ e^{2k} c₀|B||∂Λ| e^{−(L−vt)/ξ}; the no-recovery
   converse is the long paper's overlap argument. Latency
   t ≥ (L − ξ[2k + log(c₀|B||∂Λ|/ε)])/v — k, log|B|,
   log|∂Λ|, log(1/ε) enter *additively* against a power-law budget
   (mirrors the O(k + log S) horizon structure). Key referee-proofing:
   the bound is operator-norm,
   state-independent ⟹ survives arbitrary decoder pre-shared
   entanglement — the "old-bath HP" objection dies; locality, not
   entanglement budget, separates the classes (BHV no-signaling).
   Corollary kills surface-deposit objections: fraction of entropy
   recoverable at latency τ ≲ τ·S^{−1/d}, so any fixed fraction costs
   τ ≳ S^{1/d}. Diffusive S^{2/d} kept as stated expectation, not
   theorem. New refs: Lieb–Robinson 1972, Hastings–Koma 2006,
   Bravyi–Hastings–Verstraete 2006, Nachtergaele–Sims 2010 (review;
   covers harmonic/unbounded-coupling extensions for the regulator
   remark).
3. dS leg: DRAFTED 2026-06-13 in latency form (equilibrium HP
   protocol: decoder holds prior exchanged-quanta record; horizon
   register O(k + log S_0) by import; the reservoir-lemma bath fails
   by a power of S_0 via Theorem 1). Remaining: position against dS
   Hayden–Preskill literature (user's check) before finalizing.
4. Reassess what survives of flux-moment measurement as a secondary
   diagnostic (Dicke-vs-incoherent dichotomy is still visible in
   radiation statistics even if N_eff is not).
5. Then assemble with the contrast engine (§0): the two-horizon flip
   of the spectrum input against the invariance of saturation —
   now in latency form — is the argument that this is a law, not a
   slogan.
