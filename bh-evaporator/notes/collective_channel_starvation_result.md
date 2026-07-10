# Route 2b Deployed: The Bright-Thermal Collective Channel Is Starvation-Limited

Date: 2026-07-07/08

Role: executes the "dedicated check" named in
`envelope_as_coupling_universality.md` section 6 — the flux fraction and
statistics of the 1601.01329 collective coupling deployed AS an emission
channel — and then works the general question: can any thermalized
bright collective exterior channel (route 2b) persistently carry the
Hawking luminosity?  Result: the static mimicry is exact and trivial,
but the channel is reservoir-starved; sustaining it requires refill at a
super-Planckian rate, and sub-Planckian refill leaves a SIGNED,
O(flux-fraction) sub-thermal line-asymmetry deficit — caught by the
existing asymmetry rung.  The E' residue therefore closes MODULO a
named Planckian-relaxation input, upgrading the certificate's second
input from a vertex assumption to a dynamics bound.  Verification
grading per claim.  Not paper text.

Successor update (2026-07-09):
`collective_channel_spectral_starvation_theorem.md` removes the
time-local Markov assumption for stationary linear, gauge-invariant
Gaussian channels with additive self-energies and derives an exact
frequency-local flux/deficit identity.  Separately,
`signed_cancellation_and_gram_tail_result.md` shows that one aggregate
line ratio can hide exact HIGH/LOW cancellation at `N_eff <= 2`; LOW
and HIGH fractions must be channel-resolved or separated by a
multi-setting protocol.  Exact calibration at two drain strengths
closes that cancellation in the narrow stationary class.  The ordinary
Gram tail remains a separate input-2 joint.

## 1. The deployment: exact structure of the corpus ingredient

Pinned from `1601.01329` `src.tex` l.633-640.  The optical coupling with
K memory species:

```text
H_opt,K = eps sum_j b_j^dag b_j + (delta+eps) c^dag c
          + (g/2) sum_j (c b_j^dag + c^dag b_j),
```

equivalent (exactly, by a linear canonical transformation — the model is
quadratic, so this is operator-level, not state-level) to coupling c to
the single collective mode

```text
b' = (1/sqrt(K)) sum_j b_j,    coupling g' = sqrt(K) g,
```

with the K-1 orthogonal combinations EXACTLY decoupled from c.
"Deployment as an emission channel" = replace the single oscillator c by
a radiation continuum, so b' acquires the enhanced Markovian decay

```text
Gamma' = K Gamma_1,    Gamma_1 = 2 pi g^2 rho(eps)   (per species).
```

[Computation; the sqrt(K) reduction is the paper's own statement, the
continuum step is standard input-output.]

## 2. Static mimicry is exact — the residue was real [computation]

Take the memory sector in a PRODUCT THERMAL state at temperature T
(each species at nbar = nbar_T(eps); genuinely thermalized, no
inter-species coherence).  Then, writing the channel operator
A = g' b':

```text
<b_i^dag b_j> = delta_ij nbar   =>   <b'^dag b'> = nbar = O(1);
K_A = <A^dag A>/<[A,A^dag]> = nbar
  => r = nbar/(nbar+1) = e^{-eps/T}     (exact KMS — asymmetry PASSES);
b' linear in Gaussian modes => Gaussian => g2(0) = 2   (PASSES);
Gram rank of the emission vertex = 1    (single operator, N_eff = 1);
intensity I = g'^2 <b'^dag b'> = K g^2 nbar
            = K x (per-species ordinary intensity).
```

With g at the universal envelope scale and K = S this is the FULL
ordinary-picture flux through ONE channel.  So the route-2b static
mimicry exists in three lines on corpus ingredients: bright, thermal,
KMS, g2 = 2, rank one.  This CONFIRMS by construction that the
certificate's residue was real — no static observable can see it —
and localizes the entire burden of the escape in dynamics.

## 3. The strict deployment fails dynamically: a flash, not a channel [exact]

The drain removes quanta specifically from b'.  But b' holds only
<b'^dag b'> = nbar = O(1) of the total K nbar memory quanta, and the
orthogonal K-1 modes are EXACTLY decoupled from the radiation.  So the
strict model, deployed as an emission channel:

```text
emits  ~ nbar = O(1) quanta in time 1/(K Gamma_1), then goes dark;
integrated flux fraction = nbar / (K nbar) = 1/K -> 0.
```

The brightness bought by sqrt(K) concentration is paid for by reservoir
starvation.  Time-resolved signature of the flash (verified numerically,
section 7): the line asymmetry STARTS exactly thermal and drifts DOWN,

```text
r(t) = n(t)/(n(t)+1),  n(t) = nbar e^{-Gamma' t}   ->   r < e^{-eps/T},
```

while g2(0) stays pinned at 2 throughout (the state remains Gaussian;
Gaussianity is starvation-blind).  So the corpus ingredients CANNOT be
assembled into a persistent bright thermal channel: the un-built model
of the envelope note's section 6 residue is un-built for a structural
reason, not by accident.  [Exact within H_opt,K + continuum; the K-1
decoupling makes the 1/K flux fraction rigorous, not an estimate.]

## 4. The general refill bound: brightness is rate-limited by rethermalization [computation]

To sustain the flux, internal dynamics must refill b'.  Model the refill
as a coupling of b' to the internal sector at rate Gamma_th with thermal
occupation nbar_T (Markovian; scope remark in section 6).  Exact steady
state of the drained mode (drain Gamma', incoming radiation empty):

```text
n* = Gamma_th nbar_T / (Gamma_th + Gamma'),
```

the state is exactly thermal/geometric with parameter n*, and the
measured line asymmetry r* = n*/(n*+1) sits BELOW the KMS value:

```text
1 - r*/r_KMS = x / (nbar_T + 1 + x),      x = Gamma'/Gamma_th.
```

(Both formulas verified numerically, section 7.)  So the KMS deficit is

```text
eta ~ Gamma' / (Gamma_th (nbar_T + 1))     for x << 1.
```

Now pin Gamma' by the flux the channel must carry.  A rank-one channel
at frequency omega ~ T carrying fraction f of the Hawking photon flux
(N_dot ~ a T, a = O(1) greybody; one quantum per light-crossing time,
standard) needs

```text
Gamma' = f N_dot / n*  ~  f a T / nbar_T,
```

so with any internal relaxation cap Gamma_th <= c_P T:

```text
eta  >~  f a / (c_P nbar_T (nbar_T + 1))  ~  f / c_P     at omega ~ T.
```

**Starvation bound: the flux fraction of any rank-one collective
channel is bounded by the measured line-asymmetry accuracy,
f <~ c_P eta, in exact parallel to the occupation-enhancement bound
f <= eta nbar_eq of the pigeonhole note.**  Exact KMS (eta = 0, the
semiclassical statement to all orders) requires Gamma_th/Gamma' ->
infinity: super-Planckian rethermalization.

The deviation is SIGNED and two-sided across routes:

```text
route (1)  occupation enhancement: r -> 1,        asymmetry HIGH;
route (2b) starved collective:     r* < e^{-w/T}, asymmetry LOW.
```

A drained channel is colder than its bath; a hoarding channel is hotter
than KMS.  The asymmetry rung is a two-sided instrument.

## 5. Corners checked

- **Low-frequency hiding.**  At omega << T the deficit is suppressed
  (nbar(nbar+1) ~ (T/omega)^2), but a LUMINOSITY-carrying channel there
  has width Gamma' = F b T^2/(omega nbar) ~ F b T > omega once
  F > omega/T: overdamped, not a resolvable line at omega.  So a sub-T
  line can carry at most luminosity fraction ~ omega/T.  Closed for
  single channels; the multiplexed version is bookkeeping (below).
- **High frequency.**  nbar exponentially small => Gamma' exponentially
  large.  Worse, closed.
- **m collective channels.**  Splitting the flux over m rank-one
  channels gives per-channel deficit ~ f_i/c_P ~ 1/(m c_P): hiding
  below accuracy eta needs m >~ 1/(c_P eta), i.e. a participation floor
  N_eff >~ 1/(c_P eta), parallel in form to the pigeonhole's
  pure-observable floor N_eff >= 1/f.  Full multiplexed bookkeeping
  (channels at mixed frequencies, partial fractions) NOT done — open
  item, mirrors the existing pigeonhole structure.
- **Causality tightening FAILED — correction on record.**  First guess:
  b' is horizon-delocalized, so refill needs horizon-wide signaling,
  giving Gamma_th <= T from causality alone.  WRONG: the drain leaves a
  coherent "hole" (off-diagonal anticorrelations) in the symmetric
  mode, and PARALLEL LOCAL dephasing at each constituent destroys those
  anticorrelations and restores <b'^dag b'> -> nbar at the LOCAL rate,
  no horizon-wide transport required.  So the binding input really is
  the local relaxation/dephasing rate cap, not causality.  Do not quote
  the causality version.
- **Channel capacity is NOT the obstruction.**  Pendry's single-channel
  bound Q <= pi k_B^2 T^2 / (3 hbar) [verified: J. Phys. A 16, 2161
  (1983); formula confirmed at abstract/secondary level] and the
  Bekenstein-Mayo "black holes are one-dimensional" observation (in
  program lore, compression pivot) mean the Hawking luminosity ~ T^2 is
  only O(1) single-channel capacities.  A rank-one carrier is NOT
  parametrically forbidden on bandwidth/power grounds — the BH is
  critically provisioned — which is exactly WHY the no-go lives in
  statistics precision (eta) rather than raw power, and why route 2b
  was invisible to the static legs at O(1).

## 6. The Planckian input, graded

The bound needs Gamma_th <= c_P T with c_P = O(1).  Status:

- For black holes semiclassically: the horizon's own relaxation rate is
  the quasinormal rate, Im omega_QNM ~ T up to O(1) (lowest QNMs of
  Schwarzschild).  [Standard lore, numerics-supported across the QNM
  literature; primary-source check owed (Berti-Cardoso-Starinets
  review) before external use.]
- Generic many-body: "Planckian dissipation" tau >= hbar/(k_B T) is a
  CONJECTURE (Hartnoll-Mackenzie review), proven only in special
  settings.  The adjacent rigorous anchor is the MSS chaos bound
  lambda_L <= 2 pi T [proven under stated assumptions,
  Maldacena-Shenker-Stanford 1503.01409], which bounds the chaos
  exponent, not relaxation rates — supporting, not equivalent.
- Scope remark: the refill treatment is Markovian.  At Gamma_th ~ T the
  refill bath's correlation time ~ 1/T is comparable to the relaxation
  time — Markovianity is MARGINAL, corrections O(1), not obviously
  sign-changing.  Strongly non-Markovian refill is an open corner.
- A COHERENT (drive-like) refill instead of a thermal one imprints
  phase coherence on the mode and moves g2 off 2 / breaks
  stationarity — it exits the mimicry class by construction.
  [Argument, not theorem: general non-Gaussian coherent refills not
  classified.]

## 7. Support numeric [computation, verified]

`sim/collective_channel_starvation_check.py` (dense Liouvillian,
Fock cutoff 30, numpy/scipy only), beta omega = 1, run 2026-07-08:

- steady state under drain: n* matches Gamma_th nbar_T/(Gamma_th +
  Gamma') to machine precision and the state is exactly geometric with
  parameter n* (diagonal deviation <= 9e-15, off-diagonals <= 4e-15)
  for x = Gamma'/Gamma_th in {0.1, 0.5, 1, 3};
- KMS deficit matches 1 - r*/r_KMS = x/(nbar_T + 1 + x) to machine
  precision (e.g. 0.240156 at x = 0.5, 0.654739 at x = 3);
- g2(0) = 2.00000 in all starved steady states AND along the flash
  (Gamma_th = 0, n(t) = nbar e^{-Gamma' t} confirmed): the asymmetry
  drifts from 1.00 down to 0.08 of KMS while g2 never moves.

## 8. Statement of the result

**Collective-channel starvation bound (conditional).**  Within the
certificate class, any exterior emission channel structure of rank m
carrying luminosity fraction F of a temperature-T Schwarzschild flux,
with internal rethermalization capped at Gamma_th <= c_P T, shows a
sub-thermal line-asymmetry deficit

```text
eta >~ F a / (m c_P nbar (nbar+1))    at its line frequency,
```

so exact semiclassical KMS excludes sub-Planckian-refilled bright
collective channels entirely, and measured KMS accuracy eta bounds
their flux fraction by F <~ m c_P eta.  Combined with the existing
occupation bound (route 1) and the pigeonhole, the two outlier-control
inputs become:

```text
(I)  the line-asymmetry observable            (unchanged);
(II) Planckian relaxation, Gamma_th <= c_P T  (replacing the E'
     vertex assumption for route 2b; route 2a stays closed by
     EFT universality as before).
```

The route-2b part of E' is thereby DERIVED-modulo-Planckian rather than
assumed: the no-bright-collective-channel condition follows from
reservoir starvation plus a dynamics bound with independent physical
standing (QNM relaxation semiclassically; Planckian dissipation
generically).  The full rank theorem still separately uses the
ordinary-sector smooth envelope and EFT universality for route 2a; this
result replaces only the collective-outlier part of E'.

What this does NOT do: it does not close the residue
assumption-free — the latency rung (Q2) remains the only
certificate leg that reaches route 2b without the Planckian input.
Its load-bearing role is reduced (backstop, and non-Markovian/coherent
refill corners), not eliminated.

## 9. Lab dichotomy and positioning

- The bound binds systems whose ONLY scale is T.  An ENGINEERED system
  can rethermalize a mode at rates set by couplings unrelated to its
  effective temperature (Gamma_th >> T_eff), so a bright-thermal
  rank-one channel — perfectly Hawking-looking light from a rank-one
  source — is CONSTRUCTIBLE on a bench.  The demarcation-flavored
  landing: what forbids the mimic for black holes is precisely that a
  horizon has no scale faster than its own temperature.  This also
  sharpens what the tabletop asymmetry measurement measures: the
  drain-to-refill ratio Gamma'/Gamma_th, i.e. starvation, not rank
  directly.
- Superradiant-laser literature (adjacent, not overlapping):
  Meiser-Holland, PRA 81, 063827 (2010) [abstract-verified 2026-07-07]
  find steady-state collective emission is bunched below threshold,
  ~COHERENT (g2 ~ 1) in the superradiant regime, chaotic above the
  second threshold — the known bright-collective steady states are
  NOT thermal mimics, consistent with the starvation picture (their
  bright regime is atomic-phase-locked, a coherent refill, which
  exits the mimicry class; the bath-dominated regime that would mimic
  is exactly the one starvation forbids at full flux).  No statement
  of a starvation/asymmetry-deficit bound found in the searches run
  [inference from searches, not exhaustive].

## Discipline

- Say "starvation-limited," not "impossible": the no-go is conditional
  on the Planckian input (conjecture-grade generically,
  QNM-lore-grade for BHs) and on the Markovian-refill scope.
- The deficit is SIGNED: route 2b starves COLD (r below KMS), route 1
  hoards HOT (r above).  Quote the two-sidedness; do not collapse it
  to "asymmetry deviation."
- Do not quote the causality version of the refill bound (section 5) —
  it is wrong; local parallel dephasing refills without transport.
- Do not claim the multiplexed (m-channel, mixed-frequency) bookkeeping
  is done.  Single-channel and equal-split cases only.
- Pendry/Bekenstein-Mayo honesty: no parametric power obstruction; the
  result lives in eta.  Do not oversell "the flux doesn't fit."
- g2 stays 2 under starvation (Gaussian).  The starvation signature is
  in the ASYMMETRY only (plus time dependence).  Consistent with
  program lore: g2 reads coherence class, asymmetry is the probe.
- The latency rung stays in the certificate: it is the only
  assumption-free reach into route 2b.

## Feeds

- `participation_cap_decomposition_result.md`: the outlier controls
  update to (asymmetry observable, EFT universality, Planckian
  relaxation); route 2b's part of E' is derived-modulo-Planckian, while
  the ordinary-sector envelope remains a separate rank-saturation input.
- `envelope_as_coupling_universality.md` section 6: the residue's
  "dedicated check" is now DONE — flux fraction 1/K (exact),
  statistics computed; the un-built escape is un-buildable from corpus
  ingredients without super-Planckian refill.
- Roadmap Q3 / Tier 3: branch-forcing endpoint upgrades to "thermality
  + luminosity + KMS asymmetry force entropy-rank UNLESS the horizon
  rethermalizes a collective mode super-Planckianly" — the escape now
  has a rate, not just a name.  Tier 6: the tabletop measurement reads
  Gamma'/Gamma_th; the PBH burden-onset prediction gains a signed
  discriminator (sub-thermal drift of the line during any
  collective/burden stall).
- `prototype_m3_discriminator_table.md`: add the starved-collective
  column (r below KMS, g2 = 2, N_eff = 1, flux fraction 1/K strict).
- Q2 bridge: still owed for the assumption-free version; the bright
  collective emitter is now a concrete candidate to test the bridge
  hypotheses against (it sits OUTSIDE the fresh-ancilla class —
  same flag as the persistent-b0 prototype).
