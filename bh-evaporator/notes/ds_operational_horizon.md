# An Operational de Sitter Horizon: positioning note

Related access-channel language: `notes/constrained_access_channel.md`
defines the distinguishability/recoverability perspective used below
for constraint-dressed observables.

**Goal.** Extend the operational-horizon program to the cosmological
horizon, and use the constrained variant of the model as the explicit
finite foil for holography-of-information and the CLPW algebra story.
The ambition (stated once, then earned): if the operational content of
the dS static patch plus its Gauss-law constraint is realizable in a
finite constrained quantum system, that system *is* a candidate dS
hologram — which is what dS holography would even mean, given that dS
has no asymptotic boundary to anchor an AdS-style dual.

Successor-gate update (2026-07-16): the active route is
`notes/observer_relative_temporal_access_successor_proposal_2026_07_16.md`.
It replaces the earlier `rho_DSSYK(E)^2` control with the correct paired
one-copy spectral measure and treats DSSYK as a bounded test of
observer-relative temporal access, not as evidence that `Lambda` is literally
a UV regulator. WP0 and WP1 are now complete in
`notes/dssyk_wp0_protocol_and_overlap_2026_07_16.md` and
`notes/dssyk_wp1_formal_controls_2026_07_16.md`. Their exact isometric null
parks DSSYK dynamics until a common one-copy/doubled implementation-cost rule
is physically derived; the equal-energy representation and full relational
algebra do not by themselves change recovery capacity. The standalone result
is drafted in `paper_dssyk_observer_access/main.tex`.

Intrinsic-bandwidth update (2026-07-19):
`notes/dssyk_intrinsic_bandwidth_gate_2026_07_19.md` directly tests the older
idea that `Lambda` acts as a dual UV cutoff. The native chord bandwidth does
give a bounded-spectrum speed limit, but in the Narovlansky--Verlinde
dictionary the de Sitter radius cancels and the resulting time is microscopic,
of order $G_N$. Promoting this to an observer cutoff would require a separately
derived bound on the detector interaction or control Hamiltonian. Result B
already implies that accurate recovery requires order-one integrated
diary-sensitive detector action, so the missing ingredient is a physical dS
rule fixing that action, not another generic continuity theorem. That
conditional extension is the only live route; unrestricted DSSYK dynamics
remain parked.

**Why dS is the right target for the Gauss-law question.** In AdS/flat
space the holography-of-information debate leans on an asymptotic
boundary; our model, having no geometry, looks under-equipped. But dS
has no asymptotic boundary either. The static patch is exactly the
model's predicament — finite system, horizon, thermal radiation, no
spatial infinity — so the factorized-vs-constrained comparison is
cleaner here than anywhere else. Neither side gets a boundary.

---

## 1. The sign-flipped input list

Units $G=\hbar=c=k_B=1$, dS radius $\ell = 1/H$.

Gibbons–Hawking: $T_{\rm dS} = H/2\pi$, $S_{\rm dS} = A/4 = \pi\ell^2
\equiv S_0$.

**First law check (Schwarzschild–de Sitter, small $M$):** roots of
$1 - 2M/r - r^2/\ell^2$ give cosmological horizon radius
$r_c \approx \ell - M$, so

$$S_{\rm hor}(M) \approx \pi\ell^2 - 2\pi\ell M = S_0 - \beta M,
\qquad \beta = 2\pi\ell = 1/T_{\rm dS}.$$

**Input 1 (dS state count).** The horizon register has

$$\rho_{\rm hor}(E) \propto e^{S_0 - \beta E},$$

where $E$ is the energy held inside the patch. Total Hilbert space
dimension $e^{S_0}$ — finite (Banks–Fischler finite dS Hilbert space
[find exact refs]). Structural contrasts with Schwarzschild, each
load-bearing:

| | Schwarzschild | de Sitter |
|---|---|---|
| DOS | $e^{cE^2}$ | $e^{S_0-\beta E}$ |
| temperature | $T \sim 1/M$, falls as it grows | constant, set by $\Lambda$ |
| heat capacity | negative → runaway evaporation | stable equilibrium |
| max-entropy state | none (super-Hagedorn) | **empty patch** ($E=0$) |
| trajectory | shrinking shells | equilibrium / fluctuations |

The maximal-entropy empty state is the model shadow of the CLPW Type
II$_1$ tracial state: every excited state has an entropy *deficit*
$\beta E$ relative to empty dS. In the model this is elementary
bookkeeping; in gravity it required the crossed-product construction.
That contrast is itself a demarcation datum.

The detailed-balance consequence is automatic: fluctuations of patch
energy $E$ are suppressed by $e^{-\beta E}$ — the Gibbons–Hawking
thermal weight at constant $T$. So input 1 is measured by the
constant-temperature law, exactly parallel to Prop 1 of the
Schwarzschild paper (trinity discipline transfers).

### The reservoir lemma (2026-06-12)

**Lemma (the dS state-count input is an ordinary reservoir).** Let an
arbitrary finite local system (the reservoir) have smooth microcanonical
entropy $S_R$, with $S_R(E_{\rm tot}) = S_0$, $S_R' = \beta$, and heat
capacity $C$ at the operating point. A patch holding energy $E$ out of
the shared total sees the reservoir DOS

$$\rho(E) \propto \exp\Big[S_0 - \beta E - \frac{E^2}{2T^2C} + \cdots\Big].$$

The exact Schwarzschild–de Sitter cosmological-horizon entropy expands as
($m = M/\ell$, $r_c = \ell(1 - m - \tfrac32 m^2 + \cdots)$):

$$S_{\rm hor}(M) = \pi r_c^2 = S_0 - \beta M - 2\pi M^2 + \cdots,$$

which is precisely the reservoir form with

$$C_{\rm eff} = \frac{1}{4\pi T_{\rm dS}^2} = \pi\ell^2 = S_0.$$

So the SdS entropy deficit has the generic large-finite-reservoir
expansion through second order, with the single identification
$C_{\rm eff} = S_0$ (heat capacity equal to entropy, unremarkable for
ordinary systems at order-one temperature ratios). This statement
concerns the state-count input and does not by itself characterize the
full de Sitter Hilbert space or its constraint structure.

**Consequence — the two horizons are demarcation-complementary.**
Schwarzschild: spectrally exotic (super-Hagedorn, provably non-local by
the entropy gap), constraint structure pedestrian (the factorized
exterior suffices for the whole operational package). de Sitter:
spectrally ordinary at the level of this finite-reservoir expansion, so
the distinctive dS content must enter beyond input 1. Stage B
(constraints) is therefore not one option among several — it is one of
the places where dS specialness can reside.

**The other place: input 2 survives as nontrivial.** For an ordinary
local bath in three dimensions, entropy is volume-law while the contact
surface is area-law, so the number of comparable coupling channels
scales as $N \sim S_0^{2/3}$, not $S_0$. The dS horizon register has
$N \sim S_0$: a reservoir whose *entire* entropy is carried by its
contact cells. That saturation is a holographic statement even for dS.
The old candidate measurement by relaxation/fluctuation spectral weights
is now only a secondary diagnostic, because shared-mode bottlenecks can
hide source-side participation from instantaneous flux observables. The
current exterior certificate should be formulated in latency terms:
perturb the static patch and ask how many exchanged Gibbons-Hawking
quanta are needed before the perturbation is recoverable from the
horizon record.

So the refined design statement: dS gravitational content = (i) the
Gauss-law/observer constraint structure (Stage B), plus (ii) the
boundary saturation $N \sim S_0$ of an otherwise ordinary reservoir.
Input 1 carries none of it.

**Input 2 (boundary accessibility).** Horizon-area-many source
operators coupling the patch interior to the horizon register,
$N \sim S_0 \sim A$. The equilibrium analogue of the luminosity law is
not a direct mode count: absorption/emission balance and fluctuation
spectra calibrate inclusive strength, while the current exterior
certificate of full access is latency. Open design question: formulate
the static-patch recovery protocol and compare its $S_0$ scaling to an
ordinary finite reservoir coupled through a contact surface.

**Input 3 (decoupling/mixing of the horizon register).** Same as
Schwarzschild. Measured by: recovery — Hayden–Preskill for an object
thrown across the cosmological horizon, recoverable from later
Gibbons–Hawking quanta? (Check literature for dS Hayden–Preskill.)

**Design question #1 — what is "R"?** dS has no asymptotic radiation
register. Options:
(a) the observer's collection apparatus inside the patch (collected
GH quanta);
(b) the antipodal patch — the global dS vacuum restricted to one
static patch is thermal, purified by the antipode, i.e. the two-patch
structure is a TFD, and mirror operators live on the antipode (cleanest
formal choice, directly parallels the Schwarzschild mirror section);
(c) interior-as-R, horizon-register-as-B.
The choice is itself part of the demarcation: which is operationally
meaningful for a patch observer.

---

## 2. The two-stage constraint program (the Gauss-law foil)

**Stage 0 — factorized benchmark.** The unconstrained model above:
patch interior ⊗ horizon register ⊗ record. Split states exist;
information sits where it sits until moved. This is the bookkeeping
that holography-of-information says gravity does not honor.

**Stage A — constrain a non-Hamiltonian charge.** Project onto an
eigenspace of a global conserved $Q$ (number, parity). Expectation:
only the value of $Q$ delocalizes; local reduced states otherwise keep
their factorized ignorance. This is Raju's own control case ("ordinary
gauge theory: the Gauss law at infinity reveals the total charge and
nothing more"). The model should reproduce it exactly, and it
calibrates the method.

**Stage B — constrain the Hamiltonian itself.** Fix total energy,
include an internal clock, work with relational (Page–Wootters)
states. Now the constrained charge *generates dynamics* — precisely
the feature Raju identifies as what makes gravity different from EM,
and precisely the structure CLPW dress with an observer to get the
crossed product. Finite-dimensional questions, all analytical:

1. How much global-state information appears in small subsystems'
   reduced states once states are relational? (The QM shadow of
   "information available everywhere.")
2. Does the Page curve for relational radiation entropy flatten,
   deform, or survive? (Page curve meets Page–Wootters.)
3. Does the constrained model reproduce the CLPW phenomenology —
   observer-relative entropies, maximal-entropy state, generalized
   second law — without gravity? Which parts fail?
4. Error scaling: constraint-induced correlations should be
   $O(e^{-S})$-ish for generic states (clock variance arguments);
   holography of information claims *exact* availability. Is the
   distinction exact-vs-exponentially-small, and is that the entire
   content of the gravitational claim at finite $S_0$?

**Deliverable:** a stage table — for each holography-of-information /
CLPW signature, whether it appears at Stage A, Stage B, or neither
(genuinely gravitational residue). Same demarcation discipline as the
horizon papers.

**Peripheral hypothesis for Stage B framing (2026-06-13, from the
anonymity/alternatives work — keep alive, do not build a theorem on it
yet):** the alternatives theorem of the saturation program
(`boundary_saturation_invariant.md` §5.8) forks unitary information
release under a compressed anonymous channel into
(a) fast internal routing/mixing, or
(b) an emission map already nonlocal on the source algebra.
The fork may align with the factorized-vs-Gauss-law split:
branch (a) = the factorized Hamiltonian scrambling model (Stage 0);
branch (b) = gravitational/Gauss-law/holography-of-information access
(Stage B's constrained model). If it holds up, Stage B is the study of
the encoder branch — a framing the QRF literature has not used, and a
partial answer to the crowding problem. Status: suggestive
observation, not an argument; discussion-level only until the
alternatives theorem is proven.

---

## 3. Candidate operational package for the static patch

- Constant-$T$ detailed balance of patch fluctuations ⟸ input 1.
- Maximal-entropy empty state; deficits $S_0 - \beta E$ ⟸ input 1.
- TFD/antipodal mirror structure with smooth-horizon two-point
  functions ⟸ purification + smoothness condition (transfers from the
  Schwarzschild mirror section).
- Area-law absorption / relaxation ⟸ input 2 (measurement leg open,
  see above).
- HP-type recovery across the horizon ⟸ input 3.
- Observer-relative entropies, II$_1$-like trace structure ⟸ Stage B
  constraint, **not** the unconstrained model — this is the predicted
  split, and confirming it is the paper's punchline if it holds.
- Not operational (geometric residue): global dS geometry, inflating
  exterior, dS quasinormal modes, the observer's local frame.

---

## 4. Required reading / overlap map (do before any ink)

Confident references:
- Raju, "Lessons from the information paradox," Phys. Rep. 943 (2022),
  arXiv:2012.05770 — already cited in both papers.
- Chandrasekaran–Longo–Penington–Witten, "An algebra of observables
  for de Sitter space," arXiv:2206.10780.
- Witten, "Gravity and the crossed product," arXiv:2112.12828;
  Chandrasekaran–Penington–Witten, "Large N algebras and generalized
  entropy," arXiv:2209.10454.
- Chakraborty–Chakravarty–Godet–Paul–Raju, "The Hilbert space of de
  Sitter quantum gravity" and "Holography of information in de Sitter
  space," arXiv:2303.16315 and 2303.16316 [verify numbers].
- Gibbons–Hawking, PRD 15, 2738 (1977).
- Page–Wootters, PRD 27, 2885 (1983).

To scan (overlap risk — this is the crowded part):
- Höhn et al. quantum-reference-frame / crossed-product line, incl.
  finite-dimensional crossed-product analogues and observer-dependent
  gravitational entropy (De Vuyst–Höhn–Kirklin et al., 2024–25) —
  **highest overlap risk for Stage B**; our differentiator is the
  operational-horizon package + trinity discipline, not the algebra
  construction itself.
- DSSYK / static-patch holography (Susskind line; Narovlansky–Verlinde)
  — background; if Stage B works, the relation of the constrained
  finite model to DSSYK is the obvious referee question.
- Banks, Fischler on finite dS Hilbert space dimension.
- Islands/Page curves in dS (several 2020–22 papers) — for design
  question #1, option (a).

## 5. First calculations (analytical, in order)

1. Trinity leg 1, dS version: prove $\rho \propto e^{S_0-\beta E}$ ⟺
   constant-$T$ detailed balance within the model class (should be a
   three-line Prop 1 analogue).  The realizability half is done — see
   the reservoir lemma above ($C_{\rm eff}=S_0$ match through second
   order); remaining: state the equivalence direction and the validity
   window of the expansion.
2. Settle the input-2 exterior-certificate question.  The old
   relaxation/fluctuation-rate route is secondary after the
   shared-mode obstruction; the primary target is a static-patch
   latency protocol. Compare horizon-register recovery to an ordinary
   finite reservoir with contact-surface coupling, where interior
   transport gives a power-law lower bound.
3. Stage A in a toy: total-parity constraint on (interior ⊗ horizon ⊗
   record), show only the charge delocalizes. Calibration exercise.
4. Stage B core computation: energy constraint + clock, relational
   reduced state of a small probe; quantify global-state dependence
   and its $S_0$-scaling. This is the decisive calculation — its
   outcome (exact vs exponentially small availability) determines
   whether the paper's conclusion is "HoI is constraint bookkeeping"
   or "HoI has genuinely gravitational content the model cannot see."
