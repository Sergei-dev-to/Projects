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
i.e. $\sigma \le (d-1)/d$ strictly below saturation. *To do: state the
thermal-window counting carefully; this is the converse half that makes
the criterion nontrivial.*

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

## 6. Open items, in order (revised after §5.5)

1. **Latency lemma, horizon half:** restate the long paper's HP
   recovery in latency form — diary recoverable after O(k + log S)
   quanta, conditional on mixing + thermal tie.
2. **Latency lemma, bath half (the new conditional move):**
   lower bound on the time for bulk-deposited information to become
   available to surface-supported jump operators in a finite-range
   d-dim system. Safe theorem: Lieb–Robinson ballistic, ~S^{1/d};
   physical expectation: diffusive, ~S^{2/d}. Either separates
   power-law from logarithmic, which is all the dichotomy needs.
3. dS leg restated in latency terms (perturbation of the static patch;
   equilibrium version of HP — check dS Hayden–Preskill literature).
4. Reassess what survives of flux-moment measurement as a secondary
   diagnostic (Dicke-vs-incoherent dichotomy is still visible in
   radiation statistics even if N_eff is not).
5. Then assemble with the contrast engine (§0): the two-horizon flip
   of the spectrum input against the invariance of saturation —
   now in latency form — is the argument that this is a law, not a
   slogan.
