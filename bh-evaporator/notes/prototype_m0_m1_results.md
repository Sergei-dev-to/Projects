# M0 + M1 Results: Prototype Adjudication (D1)

Date: 2026-07-04. Continues `prototype_adjudication_directions.md`.
Verification status: FULL TEXT against TeX sources unless noted.

## M0 — owed checks: COMPLETE, kill criterion NOT triggered

**(a) Dvali:2024hsb resolved and read = arXiv:2405.13117** (Dvali,
Valbuena-Bermudez, Zantedeschi, "Memory burden effect in black holes
and solitons: Implications for PBH", PRD 110, 056029). TeX now at
`.codex_tmp/arxiv_src/2405.13117/`. Content: memory-burden regime
classification (Type-I: m_j ~ m_phi; Type-II: m_j >> m_phi — black
holes are Type-II with m_j ~ M_P, m_phi ~ 1/R), soliton/BH
correspondence, PBH mass-spread prediction (stabilized mass depends on
N_G, statistically distributed => model-independent remnant-mass
spread), memory-burden vs classical-extremality comparison. NO
recovery fidelity, NO decoupling calculus, NO channel-rank or
participation quantity anywhere (grep verified: no fidelity/decoupling
hits; all g^2 hits are coupling constants). Kill criterion not
triggered. Useful additions: (i) memory de-excitation goes only via
rare pairwise annihilation of near-matched Y_lm pairs, rate
Gamma ~ omega_j^5/M_P^4 (their eq. around l.1704). The paper states
model-dependent post-burden powers tau ~ R S_BH^(1+k), with the
pair-annihilation argument giving the conservative bound
tau >= R S_BH^2; this reinforces M2 expectation; (ii) the pattern
imprints on radiation only
through its ENERGY (the mass-spread hair) — consistent with our
frequency-tag finding in M1 below.

**(b) N-portrait radiation-statistics search: axis UNOCCUPIED.**
Web pass (2026-07-04): the corpus has 1/N non-thermal deviations
carrying hair (1112.3359 orbit) but no second-order coherence / g2 /
Dicke-vs-thermal photon-statistics computation of N-portrait or
memory-burden radiation. "Dicke superradiance" hits in the BH
literature are rotational superradiance (Zel'dovich/Press-Teukolsky)
or analogue black-hole lasers — different phenomena. Nearest miss
(FULL TEXT, 1601.01329 src.tex l.617-643): luminosity FLUCTUATIONS of
a single external mode reveal internal qubit state ("quantum hair") —
mean occupancy, not statistics. The Dicke-vs-incoherent flux-statistics
discriminator (M3) is therefore ours to define.

**KEY ATTRIBUTION DATUM for M1 (same passage, 1601.01329 l.638-640,
verified):** for the optical coupling of one external mode c to K
memory species b_j at equal coupling g, the corpus itself proves the
system is equivalent to c coupling to the single collective mode
b' = (1/sqrt K) Sum b_j with g' = sqrt(K) g, "all the other K-1 modes
decoupled." The rank-1/collective-channel structure is thus explicit
in their own corpus — but never framed as channel rank, participation,
or an access invariant, and never connected to luminosity scaling.
Cite this when writing up; the fork-operationalization remains ours.

**(c) 2509.22540 skimmed (Sudden_MB_3.tex).** Swift memory burden:
information load affects CLASSICAL response to perturbations (merger
ringdown/spectroscopy); memory-burden parameter
mu = m_alpha N / (p E_p) as a new macroscopic quantum characteristic;
table-top proposal = attractive bosons on a ring (Kanamoto-Carr type,
master mode a_0, Bogoliubov b_{+-1} memory modes, p = 1/2 gap
exponent), measuring stabilization/depletion-slowdown and
trajectory selection, NOT access invariants. No recovery/rank/latency
quantities. Kill criterion not triggered. Their bench and our
frozen-routing witness protocol are the same hardware, different
measurements — strengthens Tier-3 framing.

## M1 — source Gram kernel of the 2006.00011 prototype: N_eff = 1, VERIFIED (analytic)

Setup verified against `burden_arxiv_final2.tex`: full Hamiltonian
(l.493-503), parameters (l.662-672): eps_0 = 1/r_g, N_c = K = S,
N_m = S/2, eps_k = sqrt(S) eps_0; bounds C_0 <~ eps_0/sqrt(S) (l.733),
C_k <~ eps_0 (l.707), C_{k,k'} ~ C~ <~ eps_0/S (l.671).

Exterior-coupled operators (our W, eq. (gram) of saturation paper):
O_0 = C_0 a_0 (to b_0, gap eps_0); O_k = C_k a_k (to b_k, gap
sqrt(S) eps_0, from H_higher); same for second sector.

**Structure results:**

1. **W is block-diagonal in channel space** on the microcanonical
   shell: off-diagonals W_{0k} vanish identically (a_0 and a_k† move
   different conserved sectors; trace picks no cross terms).

2. **At the flux-carrying (thermal) frequency omega ~ eps_0:
   W has the single nonzero eigenvalue lambda_0 = C_0^2 n_0 ~ eps_0^2.
   N_eff(E, omega~T) = 1.** sigma = 0. The memory channels have
   spectral support only at omega <~ eps_0/sqrt(S) (dressed memory
   bandwidth; random hopping C~ <~ eps_0/S over K = S modes gives
   semicircle radius ~ eps_0/sqrt(S), consistent with the paper's own
   gaplessness-preservation constraint) — no support at the thermal
   line, and their exterior partners b_k sit at sqrt(S) eps_0 with no
   states at low omega => golden-rule flux through memory channels is
   ZERO (no energy-conserving final states), not merely suppressed.
   The (C_k/eps_k)^2 = 1/S factor is virtual occupation, not flux.

3. **Where the E-powers sit: occupancy, not rank.** Tr W at the
   thermal line = C_0^2 n_0 = (eps_0^2/S)(S) = eps_0^2 — the required
   powers of E sit inside the SINGLE Gram eigenvalue as the Bose
   factor n_0 = S, i.e. lambda-bar carries a hidden power of E. This
   violates precisely the standard-envelope hypothesis of the
   luminosity Lemma ("no hidden power-law dependence of lambda-bar on
   E"), so the prototype exits the lemma's class exactly through the
   named caveat (coherent enhancement). Fork confirmed; NOT a
   contradiction. Branch table entry: prototype = degeneracy-saturated
   (S patterns), source-rank-unsaturated (N_eff = 1, sigma = 0).

4. **Kill criterion (dressing spreads a_0 over ~S shell directions):
   NOT triggered — algebraic reason.** The master-memory coupling is
   pure number-number: (1 - n_hat_0/N_c) Sum eps_k n_hat_k. It
   exchanges ENERGY but never quanta. The particle-exchange graph
   component containing the radiation mode b_0 is {a_0, b_0} alone;
   no term at any order of dressing rotates a_0 into memory-mode
   ladder directions. Dressing produces a_0 x f(n_hat_k,...) —
   pattern-DIAGONAL fragmentation only: the emission line splits by
   pattern energy E_p (frequency tag). With equal memory gaps, E_p
   depends only on N_m and the sector split => the tag reveals
   O(log S) classical bits over the whole history (this is exactly
   2405.13117's mass-spread hair), never the S-bit pattern. At each
   fixed omega, W remains rank ~1 (N_eff = 1 + O(1) fine-structure
   from shell-width E_p variation, not parametric in S).

5. **Bonus pre-result for M2 (makes M2 nearly immediate):** the
   prototype conserves total memory occupation N_m EXACTLY (paper's
   own statement, l.520-524; Kaikov's variant states the same). So
   within the strict model, information deposited in memory modes
   NEVER reaches radiation: recovery fidelity from emitted records is
   zero for all times — latency = infinity, not Page-scale. NOTE: the
   directions note's M2 sketch posited "perturbative routing
   a_k -> a_0 -> b_0"; that channel DOES NOT EXIST in the Hamiltonian
   (C_{k,k'} routes a_k -> a'_{k'}, memory-to-memory only). The only
   exit is H_higher's a_k <-> b_k, detuned by sqrt(S) eps_0 with
   C_k <~ eps_0: zero golden-rule rate into the toy's b_k; in a real
   BH the pair-annihilation channel of 2405.13117 gives the
   conservative bound tau >= R S_BH^2, inside a broader
   model-dependent post-burden law tau ~ R S_BH^(1+k). Input-3
   certificate fails maximally on this
   prototype. M2 residue: check whether the (1 - n_0/N_c)-modulated
   gaps let radiation carry pattern-dependence beyond E_p (expect no:
   modulation is again N_m-only for equal gaps).

6. **Matched incoherent ETH-register contrast (D1(b), sketch):** same
   DOS and same Tr W (fixed by luminosity), but weight spread over
   ~S surface operators: lambda-bar ~ eps_0^2/S, N_eff ~ S. The two
   branches are now both computed:
   boundary-saturation: N_eff ~ S, lambda-bar ~ eps_0^2/S;
   N-portrait/burden: N_eff = 1, lambda-bar ~ eps_0^2 (n_0-enhanced).
   Same luminosity, opposite participation — the discriminator table
   (M3) row is fixed.

Kaikov 2210.02312 variant (eqn_model, verified 2022_10_20_pre_scr.tex):
identical structure — number-number master-memory coupling, single
a<->b exchange channel C_b, N_m conserved (stated). All M1 conclusions
carry over verbatim to the M1/M2 workhorse.

## D3 — taxonomy paragraph (draft, for saturation paper Discussion / horizon_property_separation_program)

Degeneracy saturation does not imply source-rank saturation, and
source-rank saturation does not by itself imply HP latency. The
memory-burden prototype of Dvali–Eisemann–Emond–Zell (2006.00011)
saturates the microstate-degeneracy bound by construction (K = S
assisted-gapless memory modes), yet its exterior coupling algebra is
maximally unsaturated: radiation couples only through the master mode,
the source Gram matrix at the flux-carrying frequency has a single
eigenvalue λ₀ = C₀²n₀, and N_eff = 1 (σ = 0). The luminosity's powers
of E sit in the Bose occupancy of one coherently enhanced channel
rather than in channel rank — the escape branch our Lemma's envelope
hypothesis names. The prototype therefore occupies the
"degeneracy-saturated, source-rank-unsaturated" cell of the classification,
with our boundary-ETH register occupying the doubly saturated cell and
ordinary baths / analogue horizons the rest. The two branches are
exteriorly distinguishable: participation certificate (N_eff ~ S vs 1),
new-deposit latency (log S only under the additional HP/decoupling
certificate vs blocked), and a controlled coherence statistic once
specified (incoherent entropy-rank vs collectively enhanced
single-source). The rank-1 collective structure is already implicit in
the Dvali corpus itself: 1601.01329 reduces equal coupling to K memory
modes to coupling to one collective mode with the other K-1 modes
decoupled. Our novelty is the invariant framing and operational fork,
not the bare observation that the collective mode exists.

Table row: | memory-burden prototype (2006.00011) | DOS: saturated
(K=S) | N_eff = 1, σ=0 | new-deposit latency: ∞ (strict model; BH
mapping has model-dependent post-burden powers and conservative
pair-annihilation bound tau >= R S_BH^2) | radiation/coherence diagnostic:
collectively enhanced single-source; visibility/g2 pending explicit
calculation |

## M2 — latency statement (near-final)

In the strict prototype, total memory occupation N_m is an exact
conserved quantity, and the particle-exchange graph connects memory
modes only to each other (C_{k,k'}, C̃) and to the Planck-gapped b_k
(detuned by √S ε₀, zero golden-rule flux). A diary deposited in the
memory sector therefore never appears in emitted records: recovery
fidelity is identically zero at all times — the input-3 certificate
(HP latency O(k + log S)) fails not marginally but maximally. In the
BH mapping, the fastest available exit is the paired Y_lm annihilation
of 2405.13117, rate ω⁵/M_P⁴. The paper states model-dependent
post-burden powers tau ~ R S_BH^(1+k), with conservative bound
tau >= R S_BH^2 from the pair-annihilation argument; this is beyond
Page scale and parametrically incompatible with HP. Kill check (fast
second-order
master-mediated routing): closed — no Hamiltonian term converts memory
quanta into master quanta, so the routing a_k → a₀ → b₀ does not exist
at any order. Residue: burden-modulated gaps let the b₀ line encode
E_p(t); with equal memory gaps this is a function of (N_m, sector
split) only — O(log S) classical bits, no pattern recovery. Verdict:
the burden branch provably fails the log-latency certificate within
its own model class; this is the countermodel arm of the T2
alternatives theorem (frozen routing realized physically).

## Status after this session

- M0: DONE (all three checks; nothing closes our axes).
- M1: DONE analytically; N_eff = 1 confirmed; E-powers in occupancy;
  collision = fork, as calibrated. D3 paragraph now UNBLOCKED
  (attribution discipline satisfied).
- M2: DONE at note level (latency statement above); kill check closed.
- D3: paragraph + table row DRAFTED above; needs porting into
  saturation-paper Discussion / horizon_property_separation_program
  with citations formatted (2006.00011, 2405.13117, 1601.01329
  collective-mode passage).
- Next: M3 discriminator table (one row per branch: N_eff certificate,
  latency exponent, controlled coherence statistic), then decide
  D2/M4. Radiation-statistics diagnostic is unoccupied territory (M0b).
