# Participation Pigeonhole: the Route-(b) Inequality and Generalized Channel Occupation (Q1b Skeleton Completion)

Date: 2026-07-05; route-2b dependency update 2026-07-08

Role: closes the top formal gap left by
`asymmetry_backreaction_escape_result.md` (route-(b): does O(1) flux
through register-sampling channels force entropy-rank participation?).
Result: yes for the ordinary-sector support count, while total
`N_eff ~ S` follows at exact KMS calibration or at finite accuracy
`eta <~ 1/(n_bar_eq sqrt(S))`; coarser calibration gives the explicit
floor `N_eff ~ min(cS, (eta n_bar_eq)^-2)`.  The result is a two-line
pigeonhole once the per-channel asymmetry statement is put in its
correct general-operator form.  The generalization also resolves the
"formalize channel occupation for general eigenchannel operators" item
of `statistics_rank_link_result.md` §3 and puts leg B on textbook KMS
footing.  One new hypothesis is made explicit (the commutator cap, an
envelope-type assumption) and one blindness of the certificate is
recorded (coupling enhancement).  Verification grading per claim.  Not
paper text.

Successor status: `collective_channel_starvation_result.md` resolves
the live collective-enhancement residue within a thermal Markovian
refill class.  A persistent bright collective channel develops a
LOW-side asymmetry deficit unless its refill rate exceeds the thermal
scale.  Accordingly, E' remains the correct STATIC hypothesis, while
the dynamically completed black-hole statement replaces route 2b's
piece of E' by `Gamma_th <= c_P T`.  The Planckian/QNM input and refill
scope are load-bearing and must remain visible.

## 1. Generalized occupation and per-channel asymmetry [computation]

Let A_i be a Gram eigenchannel operator at the resolved line, A_i,ω
its frequency-ω component.  Golden-rule rates through this channel:

```text
Gamma_em,i  ∝ <A_i,ω^dag A_i,ω>      (normal ordered);
Gamma_abs,i ∝ <A_i,ω A_i,ω^dag>      (anti-normal ordered).
```

Define the generalized channel occupation

```text
K_i  ≡  <A_i,ω^dag A_i,ω> / <[A_i,ω , A_i,ω^dag]>.
```

Then the per-channel asymmetry is exactly

```text
r_i = Gamma_em,i / Gamma_abs,i = K_i / (K_i + 1),
```

reproducing lemma 3b's mode formula with no reference to literal
modes.  [Computation; definition.]  For K_i large, r_i -> 1
(asymmetry-free); for a channel in equilibrium the standard KMS
condition gives <A_ω A_ω^dag> = e^{beta omega} <A_ω^dag A_ω> for ANY
operator, i.e. r_i = e^{-beta omega} — leg B is the textbook KMS
relation applied per channel, which is the strongest verifiability
footing available.  [Standard KMS/fluctuation-dissipation. Anchor
ref identified 2026-07-05: Haag--Hugenholtz--Winnink, "On the
equilibrium states in quantum statistical mechanics," Commun. Math.
Phys. 5, 215--236 (1967). Add textbook backup (e.g.
Bratteli--Robinson) before paper text.]

Edge cases: <[A,A^dag]> <= 0 (population-inverted or Hermitian-like
channels) gives r_i >= 1 — even further from Boltzmann, so such
channels are excluded by the asymmetry observation a fortiori.
[Immediate.]

## 2. Enhancement dichotomy and the certificate's blind spot [statement + computation]

Write the channel intensity as I_i = <A_i^dag A_i> = |c_i|^2 · O(1) ·
K_i, where |c_i|^2 sets the scale of the commutator (the coupling
strength).  Enhanced per-channel flux requires

```text
K_i >> 1   (occupation enhancement),   or
|c_i|^2 enhanced beyond the envelope   (coupling enhancement).
```

The asymmetry leg kills occupation enhancement: K_i >> 1 forces
r_i -> 1, caught by the calibrated line (with the resolved-ladder
clause of the escape note).  The asymmetry leg is provably BLIND to
coupling enhancement: r_i is invariant under c_i rescaling (check:
A = c·a on an equilibrium mode has r = e^{-beta omega} for every c).
At the static level coupling enhancement is excluded only by the
ordinary-envelope hypothesis E' (no anomalously bright exterior
vertex).  Its two failure modes have different closures.  A
non-universal microscopic charge is excluded by gravitational coupling
universality.  A COLLECTIVE enhancement is not forbidden by
universality, but its explicit deployment is starvation-limited:
within thermal Markovian refill, `Gamma_th <= c_P T` makes its LOW-side
asymmetry deficit proportional to its flux fraction.  Thus E' remains
the static condition, while the dynamical certificate derives its
collective half modulo Planckian/QNM relaxation.
So the theorem's two hypotheses are independent and both load-bearing:

```text
static envelope hypothesis -> no coupling enhancement;
asymmetry leg              -> no occupation enhancement;
Planckian refill bound      -> collective coupling cannot remain
                               bright and KMS-exact persistently.
```

This split is the fork closure stated at operator level.  NEW
explicit hypothesis (E'): the envelope caps the commutator scale,
<[A_i,ω , A_i,ω^dag]> <= O(1) · |c_i|^2 with envelope-bounded c_i.
[Statement; E' is the honest new assumption this note adds — it is
the general-operator form of "matrix elements do not hide powers."]

## 3. The pigeonhole [computation; corrected same day after review]

Let Phi_i be the per-eigenchannel line fluxes, Phi_H the Schwarzschild
total, f the enhanced-channel flux fraction (bounded by the asymmetry
leg: f <= eta · n_bar_eq).  Non-enhanced channels are capped at the
envelope flux Phi_env.  This is the per-channel translation of the
Schwarzschild scaling lemma in `paper_boundary_saturation/main.tex`
(checked 2026-07-05): the paper proves
`P ~ N_eff * lambda_bar * T^4` and `N_eff ~ S` when `lambda_bar` has
no hidden power of `E`; it does not name an exact Phi_env constant.
The cap is therefore an ordinary-envelope hypothesis normalized so
that carrying Phi_H through ordinary channels needs ~ c·S of them,
i.e. Phi_H / Phi_env ~ c·S.  Two distinct statements — keep them named
and separate:

(i) ORDINARY-SECTOR SUPPORT COUNT.  Within the non-enhanced sector
the cap gives

```text
N_eff^ord >= (1 - f) · Phi_H / Phi_env  ~  (1 - f) · c · S.
```

[Exact given the cap; pigeonhole over the ordinary sector only.]

(ii) TOTAL PARTICIPATION.  An enhanced channel carrying flux fraction
f contributes f^2 to the participation denominator by itself, so

```text
N_eff = (sum_i Phi_i)^2 / sum_i Phi_i^2
      >= 1 / ( f^2 + (1 - f) · Phi_env / Phi_H )
      =  1 / ( f^2 + (1 - f) / (c S) )
      ~  min( c S , f^{-2} )    up to O(1).
```

Full total-rank saturation (N_eff ~ S) therefore requires
f <~ 1/sqrt(S), i.e. KMS calibration accuracy eta <~ 1/(n_bar_eq
sqrt(S)); at coarser calibration the certificate still yields the
quantitative floor N_eff >= (eta · n_bar_eq)^{-2}.  [Computation.
The first draft of this note claimed N_eff >= (1-f)·c·S for the
TOTAL participation; that is wrong at finite f — the enhanced
channel dominates the denominator.  Caught in review 2026-07-05.]

Route (b) is closed in the corrected sense: register sampling at O(1)
flux fraction forces the entropy-graded ordinary-sector count (i),
and total-participation saturation (ii) is certified in the eta -> 0
limit, with an explicit floor at finite eta.  [The constant c and the
normalization of Phi_env are the per-channel ordinary-envelope
translation of the paper's Schwarzschild scaling lemma; the paper
verifies the scaling, not an exact numerical cap.]

## 4. Assembled theorem, v2 [conditional; full hypothesis list]

Class: microcanonical shell; flux line omega ~ T calibrated by
detailed balance, with the resolution-stability check or
harmonic-line clause (escape note §4); ordinary envelope including
the commutator cap E'; Schwarzschild-scaling per-channel flux cap
Phi_env (the ordinary-envelope translation above).

**Cap dependency, resolved 2026-07-06
(`participation_cap_decomposition_result.md`):** the per-channel cap
Phi_env / F_H ~ 1/(cS) is NOT an independent hypothesis.  It
decomposes into (a) a pure-observable outlier floor N_eff >= 1/f
(exact from Tr(W^2) <= lambda_max Tr W, no envelope), plus (b)
N_eff^ord ~ cS = Lemma 1 on the ORDINARY sector, which is
uncontested (the envelope was only ever disputed for the enhanced
outlier) and is underwritten by the same E' (emission-envelope
condition — charge route by universality, collective route the live
residue) that excludes the coupling-enhanced outlier.  In the
static-only theorem the certificate therefore rests on the asymmetry
observable and E'.  In the dynamically completed version,
`collective_channel_starvation_result.md` replaces route 2b's piece of
E' by the Planckian/QNM relaxation input `Gamma_th <= c_P T`, within
the stated refill class.  The per-channel cap remains downstream, not
an additional independent hypothesis.

Clarification: the exact ordinary-sector decomposition is
`N_eff = 1/(f^2 + (1-f)^2/N_eff^ord)`.  The displayed theorem below
uses the conservative support-count/cap form
`N_eff^ord >= (1-f)cS`, which gives the `(1-f)/(cS)` denominator.

```text
Schwarzschild luminosity
+ KMS line asymmetry within eta of Boltzmann
  =>
enhanced-channel flux fraction f <= eta * n_bar_eq(omega)
  =>
N_eff^ord >= (1 - f) * c * S                (ordinary-sector count);
N_eff     >= 1 / ( f^2 + (1 - f)/(c S) )
          ~  min( c S , (eta * n_bar_eq)^{-2} )   (total participation).
```

If the ordinary sector is asserted to have normalized participation
`N_eff^ord ~ cS`, the exact identity gives the slightly sharper finite
`f` form `N_eff = 1/(f^2 + (1-f)^2/(cS))`.  For the certificate's
scaling use, both forms give the same `min(cS, f^{-2})` floor.

Semiclassical anchor (eta = 0): exact KMS asymmetry gives
N_eff >= c·S within the static class and modulo E'.  A rank-one
thermal COLLECTIVE channel has r = e^{-beta omega} (KMS-exact) and
g2 = 2 at an instant, so the equilibrium static legs cannot see it.
The starvation theorem adds time and drain: with finite
`Gamma_th <= c_P T`, persistent nonzero collective flux produces a
LOW-side deficit, so exact calibration excludes it in that dynamical
scope.  At finite eta, use the combined dangerous fraction
`f_bad = f_occ + f_coll`, with `f_occ <= eta n_bar_eq` and, for the
single/equal-split collective cases at omega ~ T,
`f_coll <~ m c_P eta`.  The total-participation statement is then a
floor, and the full
saturation claim requires eta <~ 1/(n_bar_eq sqrt(S)) — state which of
the two quantities is meant every time.  Leg A (g2) remains independent
passive corroboration and covers the sloped-ladder clause.  All
load-bearing steps are now at computation or explicit-hypothesis
level; nothing in the chain is a sketch.

## 5. Leg-A hypothesis statements (owed items, statement only)

Fourth-moment ETH factorization (for the §1 composite identity of the
statistics note): for distinct Gram eigenchannels at the resolved
line, connected cross-channel fourth moments are suppressed,

```text
<A_i^dag A_j^dag A_k A_l>_connected = O(e^{-S/2}) * (Wick scale),
        for index patterns not matched in pairs,
```

with the sharp/enhanced channel EXEMPT from internal Gaussianity (the
identity never Wick-factorizes a channel against itself).  [Statement;
hypothesis to assume explicitly in the theorem, standard ETH-typicality
grounds.]

Resolved-mode filter: an output wave-packet mode
b_w = ∫ dt w(t) e^{i omega t} b_out(t) with bandwidth Delta_omega
smaller than the burden-tag spacing and than the anharmonic ladder
offset when the ladder clause is invoked; per-resolved-mode statements
quantify over such w.  All g2 and asymmetry claims are claims about
b_w.  [Statement; formalization is bookkeeping over input-output
theory, no new physics expected.]

## Discipline

- E' (commutator cap) is a real hypothesis in the static-only theorem.
  In the dynamical completion, explicitly replace only its route-2b
  outlier half by the Planckian/QNM refill bound; do not present either
  form as hypothesis-free.
- The asymmetry leg cannot see coupling enhancement; never claim leg
  B at equilibrium alone excludes it.  The collective closure uses
  time-dependent drain plus a refill-rate bound.
- The constant c and Phi_env are not exact constants quoted from the
  paper; they are the per-channel ordinary-envelope normalization of
  the paper's Schwarzschild scaling lemma.  Quote them as scaling data,
  not as an already-proven numerical cap.
- Sloped-ladder clause carries over verbatim from the escape note.
- N_eff here is participation over the Gram eigenbasis at the
  resolved line; do not quote it as basis-independent without the
  Gram construction.
- Always name which quantity a bound concerns: ordinary-sector
  support count N_eff^ord (linear in (1-f)) versus total
  participation N_eff (floored by f^{-2}).  Total saturation ~ S
  requires eta <~ 1/(n_bar_eq sqrt(S)); do not quote the saturation
  conclusion at O(1) eta.
- Distinguish the conservative support-count formula
  `f^2 + (1-f)/(cS)` from the exact normalized ordinary-sector formula
  `f^2 + (1-f)^2/N_eff^ord`.  They are parametrically equivalent for
  the scaling claim but not identical finite-`f` statements.

## Feeds

- `statistics_rank_link_result.md`: open item 2b (route-(b)
  inequality) DONE; item 3 (filter) and item 4 (fourth-moment) have
  explicit statements here, remaining work is bookkeeping; assembled
  theorem superseded by v2 above (linear (1-f), full hypothesis
  list).
- Roadmap Q1b: skeleton COMPLETE — all load-bearing steps at
  computation or explicit-hypothesis level; remaining: formalization
  bookkeeping, multiplexing numeric, then paper form.
- Escape note: its route-(b) "target inequality" is discharged here.
- Paper form (when written): the certificate section's hypothesis
  list is §4 of this note.
- Route 2b paper form: use `collective_channel_starvation_result.md` and
  retain its Markovian, Planckian/QNM, and multiplexing qualifiers.
