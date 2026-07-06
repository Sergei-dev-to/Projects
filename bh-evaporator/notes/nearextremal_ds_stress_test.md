# Near-Extremal/JT and dS Stress Test of the Static Certificates (First Pass)

Date: 2026-07-05

Role: first pass at item 1 of the roadmap's Post-Completion Horizon,
pulled forward because the Q1b skeleton landed early.  Question: do
the static rank certificates (flux law + KMS asymmetry + g2) survive
their dangerous cases — near-extremal/JT (S_0 versus active entropy)
and dS (ordinary spectrum) — or do they overclaim?  Verdict after the
first verification pass: BPS/extremal zero-line sectors are silent as
expected, but semiclassical near-extremal emission is NOT guaranteed
to be blind to `S_0`.  A Schwarzian-throat scattering anchor reports
area-sized absorption in the weak-Schwarzian regime, so the certificate
may read horizon-area / `S_0` participation there.  This is not a
failure, but it replaces the earlier "active entropy only" expectation
with a sharper question: which line cross-section does the actual
emission channel use?  dS remains ordinary/reservoir-like at this
think-pass level.  All near-extremal exponents below remain
VERIFY-before-external-use.  Not paper text.

## 0. The certificate reading, pinned

Lemma 1 of `paper_boundary_saturation/main.tex` (verified against the
TeX today) is the scaling identity

```text
P(E) ∝ N_eff(E) · lambda_bar(E) · T(E)^{p+2},    p = 2 in 4d,
```

with the envelope hypothesis that lambda_bar carries no hidden powers.
The certificate therefore READS

```text
N_eff ∝ P / ( lambda_bar · T^{p+2} ),
```

and the Schwarzschild conclusion N_eff ~ S_BH is the special case
T ∝ E^{-1}, P ∝ E^{-2}.  Everything below is this identity applied to
other horizons.

## 1. Near-extremal, semiclassical regime (T >> quantum scale) [inference]

Thermodynamics: energy above extremality E_a, T ∝ (E_a/C)^{1/2},
active entropy Delta_S ~ C·T on top of the extremal S_0.

The certificate reads N_eff ∝ P(T)/T^4.  Two anchor cases:

- If the black hole radiates by the geometric-area blackbody law
  (P ~ S_0 l_p^2 T^4), the certificate would read N_eff ~ S_0 —
  tracking the FULL extremal entropy.
- The first source check does NOT support the earlier claim that the
  throat generically forbids this.  Emparan 2501.17470 reports that in
  the weak-Schwarzian semiclassical regime, low-frequency massless
  scalar absorption recovers the universal horizon-area cross-section;
  in the strong-Schwarzian regime the cross-section is enhanced above
  the semiclassical prediction despite suppressed density of states.

So the certificate may genuinely read N_eff ~ S_0 in the semiclassical
near-extremal line, not merely Delta_S.  That is not automatically an
overclaim: the exterior absorption/emission channel may really couple
to area-sized horizon structure even when the thermally changing
entropy is only Delta_S.  The dangerous question is therefore sharper
than the first pass: does the relevant emission line carry area-sized
cross-section, throat-filtered active entropy, or a quantum-Schwarzian
enhancement?  Each answer refines what "flux-participating rank" means
near extremality.  [Corrected after source check 2026-07-05; do not
quote near-extremal powers before checking the detailed greybody /
Schwarzian regime and the emitted species.]

Axis-splitting payoff: a BPS/extremal sector with genuine e^{S_0}
degeneracy at T = 0 emits nothing; the flux-anchored certificates are
silent there while the degeneracy axis is saturated.  This is a
DISTINCT taxonomy cell from the memory-burden prototype, and the
distinction matters: the prototype has an ACTIVE sharp line that is
source-rank-unsaturated (N_eff = 1 on real emission, which is what
lets g2 and asymmetry vote), whereas the BPS sector is line-rank
SILENT/UNDEFINED — no emission line exists to certify or to fake KMS.
"Degeneracy-saturated with unsaturated active-line rank" (prototype)
and "degeneracy-saturated with no active line" (BPS at T = 0) are two
different cells, both off the Schwarzschild diagonal.  What they share
is only that degeneracy saturation does not imply flux-rank
saturation; the axis separation is thus not a toy-model artifact, and
gravity exhibits it at extremality — but do not merge the two cells.
[Inference; source anchors identified 2026-07-05: Iliesiu--Turiaci
2003.02860 for the non-supersymmetric near-extremal RN/JT continuum,
and Heydeman--Iliesiu--Turiaci--Zhao 2011.01953 for near-BPS gap plus
large extremal degeneracy.  Still verify applicability to the specific
charged/rotating family before external use.]

## 2. Rotating/charged calibration and superradiance [computation-level]

For Kerr/RN the calibrated line asymmetry is grand-canonical:

```text
em/abs = e^{ -beta (omega - m Omega_H - q Phi_H) }.
```

Superradiant modes (omega < m Omega_H + q Phi_H) have em/abs > 1 —
amplification.  The generalized-occupation formalism of the
pigeonhole note handles this without modification: r = K/(K+1) > 1
corresponds to K < 0 (inverted channels), and the KMS reference
value itself exceeds 1 for those modes, so calibration is still
well-posed.  Discipline: leg B for rotating/charged horizons MUST be
calibrated at the co-rotating Boltzmann factor; naive e^{-omega/T}
calibration would misread every Kerr line as an O(1) KMS violation
and fake a memory-burden-like vote.  [Computation-level given
standard superradiance; check factors before ink.]

## 3. Schwarzian/quantum regime (T at or below the gap scale) [inference; the real danger found]

Below the quantum scale (E_a ~ 1/C), the near-extremal DOS is the
Schwarzian form rho(E) ~ sinh(2 pi sqrt(2 C E)) and semiclassical
thermodynamics fails.  Consequence for leg B: the CANONICAL
calibration e^{-beta omega} is wrong at O(1) when omega ~ E_a,
because the microcanonical ratio rho(E - omega)/rho(E) deviates from
any Boltzmann factor there.  This is the one place the stress test
found genuine breakage — of the canonical PHRASING, not of the
framework: the notes' own microcanonical formulation (asymmetry
calibrated by the shell DOS ratio, escape note §1) remains correct
and computable.  Refinement adopted: state leg B's reference value as
the DOS ratio always; e^{-beta omega} is its thermodynamic-limit
form.  Falsifiable wrinkle worth recording: quantum near-extremal
lines are predicted to be calibrated-non-Boltzmann in a way fixed by
the Schwarzian DOS — a real gravitational system whose line
asymmetry deviates from naive KMS while remaining fully calibrated.
[Inference; thermodynamic anchor identified as Iliesiu--Turiaci
2003.02860.  Evaporation/cross-section side anchored separately by
Emparan 2501.17470 and candidate charged-evaporation follow-up
2411.03447.  Still verify emitted species and ensemble conventions
before any external claim.]

## 4. dS static patch [inference]

The certificate identity is not even posed: there is no asymptotic
flux channel, and P(E) has no meaning for an observer inside the
horizon.  What replaces it is the June reservoir lemma: the static
patch DOS is an ordinary finite bath (C_eff = S_0), so any
probe-level line the observer calibrates reads ORDINARY rank at
T_dS — no saturation signal in statics.  This quantitatively
reproduces, rather than collapses, the section-0 contrast engine of
the saturation paper: Schwarzschild spectrum exotic (statics certify
rank), dS spectrum ordinary (saturation content lives in the
constraint structure only).  The static certificates are powerful
exactly where the flux law is exotic, and mute where it is not — as
they should be.  [Inference from the reservoir lemma; no new
computation.]

## 5. Verdict

The framework is diagnostic in its dangerous cases at think-pass
level.  BPS/extremal zero-line sectors still do the clean axis split:
the certificates measure flux-participating rank and go silent for
non-radiating degeneracy.  Near-extremal/JT emission, however, cannot
be summarized as "blind to S_0" after the first source check: in the
semiclassical area-cross-section regime it may certify S_0-sized
participation, while the strong-Schwarzian regime may modify the line
strength in a different direction.  That is not a failure of the
certificate; it is the stress test doing useful work by asking which
cross-section the actual channel uses.  Two scope refinements adopted
as results: (i) leg B's reference value is the microcanonical DOS
ratio (canonical Boltzmann only in the thermodynamic limit — mandatory
at the Schwarzian scale); (ii) rotating/charged calibration is
grand-canonical, and the formalism accommodates superradiant
(inverted) channels natively.  The residual risk is concentrated in
the VERIFY list, not in the structure.

VERIFY before any external use:

```text
1. Near-extremal greybody luminosity exponents (Page; Maldacena-
   Strominger; throat transmission powers).  Anchor identified:
   Maldacena--Strominger, "Black Hole Greybody Factors and D-Brane
   Spectroscopy," arXiv:hep-th/9609026 / Phys. Rev. D 55, 861.
2. Schwarzian DOS and its evaporation corrections; SUSY gap + BPS
   degeneracy versus non-SUSY lifting.  Anchors identified:
   Iliesiu--Turiaci, "The statistical mechanics of near-extremal black
   holes," arXiv:2003.02860 / JHEP 05 (2021) 145;
   Heydeman--Iliesiu--Turiaci--Zhao, "The statistical mechanics of
   near-BPS black holes," arXiv:2011.01953; and, for the
   cross-section side, Emparan, "Quantum Cross-section of
   Near-extremal Black Holes," arXiv:2501.17470 / JHEP 04 (2025) 122.
   Candidate charged-evaporation follow-up: arXiv:2411.03447.
3. Superradiant stimulated-response factors.  Bekenstein--Meisels is
   the anchor and includes superradiant modes, but Kerr/RN sign and
   normalization conventions still need a pre-ink check.
4. Lemma-1 phase-space power p for the near-extremal throat (the
   effective p is modified by the greybody energy dependence; the
   certificate reading must use the corrected power).
```

## Discipline

- Say "diagnostic at think-pass level," never "JT confirms" or
  "near-extremal emission is blind to S_0."
- No near-extremal exponent from this note may be quoted before the
  VERIFY list is cleared.
- The BPS axis-splitting claim is an inference about zero-flux
  sectors; do not extend it to near-BPS emission without the greybody
  check.  Keep the BPS cell (no active line) distinct from the
  memory-burden cell (active but source-rank-unsaturated line); they
  are not the same taxonomy entry.
- The dS statement imports the reservoir lemma; it is only as strong
  as that lemma's stated class.

## Feeds

- Roadmap Post-Completion Horizon item 1: first pass UPDATED after
  source check.  dS and zero-line BPS remain consistent with the
  certificate scope; semiclassical near-extremal emission may certify
  S_0-sized rank rather than active entropy only.  Remaining work is
  the VERIFY list (greybody/Schwarzian literature session) and then a
  taxonomy row.
- M3 table / horizon program: candidate new row "near-extremal/BPS
  black hole" — degeneracy-saturated (S_0), line-rank
  SILENT/UNDEFINED at T = 0, and near-extremal line-rank possibly
  S_0-sized, active-entropy-sized, or quantum-enhanced depending on
  the verified line cross-section.  This is a standard-gravity witness
  for the degeneracy/rank split, but a DIFFERENT cell from the
  memory-burden prototype (which has an active source-rank-unsaturated
  line); do not label it as occupying the same cell.
- Pigeonhole note: leg B reference value generalized (DOS ratio;
  grand-canonical factor) — fold into theorem v2's class statement
  when the paper section is written.
