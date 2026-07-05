# BEC-Crossover Access Invariants: Literature Pass

Date: 2026-07-04

Role: start-rule gate for the crossover idea (access invariants swept
across the attractive-condensate coupling g → 1; horizon access-profile
as strong-coupling endpoint of a smooth crossover). Companion-paper
(corpuscular-stabilization) slot. Pass done by web search + abstract
fetches in one session; full-text checks owed before any ink (marked
below). Verification status: ABSTRACT-LEVEL unless noted.

## Pre-registered scoop criteria

Scooped iff someone computes, across the attractive-condensate coupling
sweep (or equivalent control parameter):
(i) participation/rank of the EXTERIOR coupling algebra (Gram-kernel
N_eff / saturation exponent sigma);
(ii) recovery/decoupling latency in emitted quanta (HP-type, for newly
deposited information — not internal scrambling time, not Page time of
initial data);
(iii) protected-commutant decay rate (lambda-type de-protection);
(iv) the ordinary-reservoir exponent contrast.
Internal scrambling/OTOC/entanglement at criticality does NOT count —
that is an input (Flassig–Pritzel–Wintergerst territory).

## Occupied (adjacent hits, graded)

1. **Internal scrambling at criticality — occupied, expected.**
   Dvali–Flassig–Gomez–Pritzel–Wintergerst 1307.3458: scrambling time
   ~ log N at the critical point of a Bose prototype (quantum break
   time); companion work: entanglement maximal at criticality,
   Lyapunov over-critical. Input, not scoop.
2. **Storage capacity + manipulation-based retrieval — occupied.**
   Dvali–Panchenko 1507.08952, 1601.01329: gapless modes at
   criticality as cheap qubits; retrieval by EXTERNAL MANIPULATION of
   system parameters (gate model), not passive-emission decoding. No
   latency exponent, no reservoir contrast.
3. **Memory burden — the near-miss on latency.** 1810.02336
   (microscopic holography model: gapless-mode count ~ area of
   (d−1)-sphere from momentum-dependent attractive interaction — NB:
   an area-law mode count from attraction, relevant to saturation
   origin), 2006.00011 (stabilization by memory burden; readability
   onset when memory modes acquire frequency). Retrieval-time-adjacent
   claims exist, but tied to system decay/gap opening, not
   HP-decoupling from an emitted record; no exponent classification;
   abstract of 1810.02336 shows no exterior-bath channel analysis.
   FULL-TEXT CHECK OWED on both.
4. **Saturons — the load-bearing prior art.** Dvali et al.:
   2111.03620 (Gross–Neveu saturons), 2112.00551 (How special are
   black holes / saturon correspondence), 2509.08049 (evaporation
   similarities of saturated solitons and BHs, Sept 2025). Claim:
   objects saturating the microstate-degeneracy bound form a BH
   universality class WITHOUT gravity — area-law entropy, thermal
   decay, information retrieval on the Page formula, in solvable
   (large-N Gross–Neveu) models. This occupies the umbrella claim
   "horizon behavior = saturation universality class reachable without
   gravity" — close to access_emergence_philosophy.md §10's
   aspiration. FULL-TEXT CHECK OWED (what exactly is computed about
   retrieval: Page-time of initial data vs HP latency of new deposits;
   any coupling-algebra analysis).
5. HP-in-Hamiltonians (Nakata–Tezuka), HP-in-circuits (Rampp–Claeys):
   already in our refs; not on the condensate crossover.

## Unoccupied residue (per this pass)

Nobody found computing, as CURVES in the control parameter g across
the crossover (all hits work AT the critical/saturated point or study
decay of the saturated object):
- sigma(g): source Gram-kernel participation of the exterior coupling
  algebra;
- latency exponent(g): HP-decoupling latency for newly deposited
  information from emitted records;
- lambda(g): commutant de-protection rate;
- the reservoir-contrast form of any of these.

## The sharpened question (differentiator)

Dvali's saturation = state-count/degeneracy bound (our input 1, level
(b)). Ours = coupling-algebra saturation + latency certificate (input
2, level (c)). Nobody has asked whether degeneracy saturation FORCES
access saturation, or whether the two separate. The BEC/saturon
systems are exactly where they could separate: a saturon might be
state-count-saturated but access-unsaturated (exterior coupling still
surface-like), landing in a §5.7 intermediate class and GRADING the
Dvali universality claim by the operational package. Either outcome is
a taxonomy result; separation would be the stronger one.

## Kill criteria status

- "Retrieval-cost-vs-criticality already computed in memory-burden
  form": NOT triggered at abstract level; full-text check owed
  (2006.00011, 1810.02336, 2509.08049).
- "Exterior coupling of a trapped condensate ill-posed": OPEN — the
  model-design question (what plays the radiation continuum for a
  trapped BEC: depletion channel, RF outcoupling, trap opening) is the
  first technical task if this proceeds.

## Next step if proceeding

1. Full-text pass on the five owed papers (half day).
2. Model-design note: attractive Bose–Hubbard (existing
   generate_variable_n_bose_hubbard.py infrastructure) + explicit
   outcoupling channel; define the jump operators so N_eff is
   well-posed.
3. First numeric: sigma(g) and decoupling latency(g) on small N,
   sub-critical → critical sweep; reservoir control = same model,
   repulsive/zero coupling.

Sources (this pass): arXiv 1307.3458, 1507.08952, 1601.01329,
1810.02336, 2006.00011, 2111.03620, 2112.00551, 2509.08049,
2307.01454 (non-isometric HP quantum simulation — circuit-based, not
crossover), Nakata–Tezuka 2303.02010, Rampp–Claeys 2312.03838.

## Full-text pass (2026-07-04) — VERIFIED against TeX sources

All five owed papers read in TeX (plus 1601.01329). Verification
status of this section: FULL TEXT.

**What "information retrieval time" means in the saturon corpus
(2111.03620 §"Time-scale of information retrieval", 2112.00551
§§Passive/Proactive retrieval, 2509.08049 §6):** the minimal time for
the START of retrieval of the INITIALLY stored flavor pattern,
t ≳ S·R (Page-time analogue). Passive: detector must resolve 1/N
flavor correlations at detector rate Γ_det ~ (1/R)(1/N²)N_det; must
collect ~N quanta. Active/proactive: probe scattering, same bound;
modified by memory burden. This is NOT HP-decoupling latency for
newly deposited diaries with radiation side information (O(k+log S)
regime) — different question, different exponent, no decoupling
calculus, no decoder fidelity quantities anywhere.

**Memory burden mechanism (2006.00011, full Hamiltonian §):** master
mode a₀ (N_c = S quanta, gap ε₀ = 1/r_g) + K = S memory modes =
spherical harmonics l ≲ √K with free gaps ε_k = √S·ε₀ (Planckian),
made gapless by assisted criticality. Radiation b₀ couples via
a₀†b₀ + h.c. — THROUGH THE MASTER MODE ONLY. Memory-to-radiation
transfer (a_k ↔ b_k) suppressed by level mismatch (C_k ≲ ε₀ vs
splitting √S ε₀): "energy but no information." Numerics: occupation
transfer rates vs model parameters; no recoverability/fidelity, no
participation count, no reservoir contrast.

**Dvali–Panchenko 1601.01329 (§Readout via Couplings to External
Fields):** critical qubits coupled to a SINGLE external oscillator
(cavity prototype); inscription/readout sequences; retrieval time
tied to inverse qubit gap (implicit latency-vs-criticality relation —
the nearest miss to our latency(g) curve). Single channel, gate
framing, no HP/decoupling, no multi-channel participation, no
reservoir contrast.

**Scoop verdict on pre-registered criteria: NOT TRIGGERED.**
(i) N_eff/σ of exterior coupling algebra: computed nowhere.
(ii) HP-decoupling latency for new deposits: computed nowhere.
(iii) λ de-protection: not formalized (memory-burden suppression is a
mechanism that would make λ small — model input, not invariant).
(iv) reservoir exponent contrast: absent everywhere (their contrast is
semiclassical-vs-quantum, not horizon-vs-ordinary-bath).
(v) crossover curves of access invariants: absent; nearest miss is
1601's gap–retrieval-time relation.

**THE COLLISION (new, sharper than the separation question).** The
memory-burden prototype's emission channel is rank-O(1): radiation
couples only through the master mode (Dicke-like/collective), so its
source Gram kernel has N_eff ~ 1, i.e. σ ≈ 0 — maximally
access-UNsaturated — while being degeneracy-saturated. Our Lemma
(Schwarzschild luminosity ⇒ N_eff ~ S within the standard-envelope
class) and the Dvali prototype therefore sit on OPPOSITE branches of
the saturation paper's own caveat ("different models may put the
required powers of E into coherent enhancement"): boundary saturation
(N_eff ~ S, incoherent entropy-rank emission) vs N-portrait
(N_eff ~ 1, coherently enhanced single-channel emission). The
crossover calculation adjudicates: compute σ(g) and the latency
exponent on the Dvali prototype Hamiltonians themselves (better
starting point than bare Bose–Hubbard — the Hamiltonians are explicit
in 2006.00011) and on an incoherent-channel variant; the
Dicke-vs-incoherent flux-statistics diagnostic (saturation note §6
item 4) is exactly the discriminator. Either the prototype fails the
luminosity calibration or our invariant needs the coherent branch
treated seriously — both outcomes are results.

**Asset:** the prototype Hamiltonians (master + memory + graded
radiation sectors, couplings bounded by consistency) are ready-made
witness systems for the §5.7 taxonomy and for the model-design task
(step 2) — the exterior channel is already defined, making N_eff
well-posed. Kill criterion 2 (ill-posed exterior coupling) is hereby
RESOLVED for the prototype route.
