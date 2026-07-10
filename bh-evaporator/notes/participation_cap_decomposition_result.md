# The Per-Channel Flux Cap Is Not an Independent Assumption

Date: 2026-07-06; route-2b dependency update 2026-07-08

Successor correction (2026-07-09): the spectral starvation theorem now
removes the Markov approximation within stationary linear gauge-invariant
Gaussian additive channels.  However, `signed_cancellation_and_gram_tail_result.md`
shows that HIGH- and LOW-side contributions can cancel exactly in one aggregate
line ratio, even with `N_eff <= 2`.  Consequently, the outlier fractions used
below require channel/line-shape resolution or a multi-setting response
protocol; they do not follow separately from one aggregate tolerance.  The same
successor result proves that static response plus `g2` cannot identify an
arbitrary ordinary Gram tail.  E' (or tomography/a microscopic coupling-spectrum
theorem) therefore remains load-bearing for that sector.

Role: shores up the softest formal joint of the Q1b certificate — the
per-channel cap F_H/F_env ~ cS asserted in
`participation_pigeonhole_result.md` and inked in
`paper_boundary_saturation/main.tex`.  Result: the cap is not a third
hypothesis.  It decomposes into (a) a pure-observable outlier bound
that needs no envelope at all, plus (b) an application of Lemma 1 to
the ordinary sector, which is itself underwritten by the same E'
(emission-envelope condition) already identified.  So the whole
static certificate rests on exactly two inputs — the line-asymmetry
observable and E' — and the cap is downstream of them, not alongside.
After `collective_channel_starvation_result.md`, the route-2b part of E'
is derived within the thermal Markovian refill class from the dynamical
input `Gamma_th <= c_P T`; it is no longer a bare vertex assumption.
The static-only bookkeeping below is retained because the Planckian/QNM
bound and refill scope remain explicit qualifiers.  (NB: E' is
the no-anomalously-bright-exterior-vertex condition, not "coupling
universality"; universality closes only its charge-route half — see
`envelope_as_coupling_universality.md` §3.)  All inequalities are
exact; grading per claim.  Not paper text.

## 1. The pigeonhole, restated exactly

Gram eigenvalues lambda_i at the resolved line; total line flux
F_H proportional to Tr W = sum_i lambda_i (fixed by luminosity, an
OBSERVABLE); participation N_eff = (Tr W)^2 / Tr(W^2).  Let the
brightest channel carry flux fraction

```text
f = lambda_max / Tr W.
```

## 2. Pure-observable floor: N_eff >= 1/f  [exact; no envelope]

Since every lambda_i <= lambda_max,

```text
Tr(W^2) = sum_i lambda_i^2 <= lambda_max sum_i lambda_i
        = f (Tr W)^2,
=> N_eff = (Tr W)^2 / Tr(W^2) >= 1/f.
```

Two lines, exact, and it uses ONLY the observable trace and the
largest eigenvalue.  No ordinary-envelope assumption, no Lemma 1, no
per-channel cap.  The entire content is: **if no single channel
dominates the line flux, participation is large.**

The brightest-channel fraction f is bounded observationally against
occupation enhancement: an occupation-enhanced channel has
em/abs -> 1, so a line within eta of its calibrated KMS ratio caps

```text
f <= eta * n_ref        (occupation-enhanced outlier).
```

Hence, against occupation enhancement, N_eff >= 1/(eta n_ref) with
NOTHING but observables.  This is the circular-free core the old cap
statement obscured.  [Computation; the f-bound is lemma 3b of
`statistics_rank_link_result.md`.]

## 3. The two escapes from the floor, and what closes each

N_eff >= 1/f fails to be useful only if some channel achieves large f
(small participation).  A large-f channel is exactly a bright rank-1
source, and by the route split of
`envelope_as_coupling_universality.md` it is one of:

```text
(1) occupation-enhanced:  closed observationally (section 2, f <= eta n_ref);
(2) coupling-enhanced:    in the static statement, closed by E' (no
    anomalously bright exterior vertex).  Its charge-route subcase (2a)
    is excluded by EFT coupling universality.  Its collective-route
    subcase (2b) is statically invisible but, after explicit deployment,
    is starvation-limited: within thermal Markovian refill and
    Gamma_th <= c_P T, its LOW-side asymmetry bounds its flux fraction
    (`collective_channel_starvation_result.md`).
```

Thus the static statement still reads "asymmetry observable + E'."
The dynamically completed black-hole statement replaces route 2b's
piece of E' by Planckian/QNM relaxation.  If `f_occ` is the
occupation-enhanced fraction and `f_coll` is the fraction in `m`
collective channels at `omega ~ T`, then parametrically

```text
f_occ  <= eta n_ref,
f_coll <~ m c_P eta,
f_bad  =  f_occ + f_coll.
```

The `m`-channel expression is established for the single/equal-split
cases; mixed-frequency unequal multiplexing remains open bookkeeping.
No separate cap is invoked to bound lambda_max; the route analysis
already does it.

## 4. Saturation upgrade: from N_eff >= 1/f to N_eff ~ cS

The stronger statement separates the outlier explicitly.  Write
Tr W_ord = (1-f) Tr W for the ordinary sector (outlier removed).  Then

```text
Tr(W^2) = lambda_max^2 + Tr(W^2)_ord
        = f^2 (Tr W)^2 + (Tr W_ord)^2 / N_eff^ord,
=> N_eff = 1 / ( f^2 + (1-f)^2 / N_eff^ord ).
```

There are two useful versions of the upgrade.

If Lemma 1 is taken to give normalized ordinary-sector participation,
`N_eff^ord ~ cS`, then the exact identity gives

```text
N_eff = 1 / ( f^2 + (1-f)^2 / (cS) )
      ~ min(cS, f^{-2}).
```

The more conservative support-count version used in
`participation_pigeonhole_result.md` follows from the same identity plus
the weaker count `N_eff^ord >= (1-f)cS`, equivalently from the
per-channel ordinary cap:

```text
N_eff >= 1 / ( f^2 + (1-f)/(cS) ).
```

The two forms differ only at finite `f`; both give the same parametric
floor `min(cS, f^{-2})`.  The ONLY new ingredient beyond section 2 is

```text
N_eff^ord ~ cS       (participation of the ordinary sector).
```

## 5. Why N_eff^ord ~ cS is not circular — the key point

N_eff^ord ~ cS is Lemma 1 (`paper_boundary_saturation`,
Lemma "Schwarzschild luminosity and effective rank") applied to the
ordinary sector.  Lemma 1 assumes the ordinary envelope
(lambda-bar carries no hidden power of E).  The worry was that
re-importing Lemma 1 makes the certificate circular, since the
certificate was supposed to REPLACE the envelope assumption.

It is not circular, for a sharp reason.  The envelope assumption was
only ever contested for ONE channel — the coherently enhanced source
that carries the luminosity at rank one (the memory-burden escape, the
"hidden power in a single eigenvalue" of Lemma 1's own caveat).  For
the ORDINARY sector — every channel except the candidate outlier — the
envelope is the standard ETH statement for simple operators and was
never in dispute.  The certificate's job was exactly to remove the
disputed outlier; once sections 2-3 remove it (observably + by E', the
no-bright-collective-channel condition — of which universality closes
only the charge subroute in the static formulation, while the
starvation theorem supplies the collective closure modulo the refill
bound), Lemma 1 applies to what remains WITHOUT the contested step.

Moreover the same E' does double duty:

```text
E' =>
   (a) no coupling-enhanced outlier            [section 3, route 2];
   (b) ordinary emission operators are ETH-enveloped
       => Lemma 1 holds on the ordinary sector => N_eff^ord ~ cS.
```

Caveat on what E' is (corrected 2026-07-06,
`envelope_as_coupling_universality.md` §3): E' is NOT "coupling
universality."  Universality (equivalence principle / Weinberg-Witten)
closes only the non-universal-CHARGE failure; the static residue is
COLLECTIVE coupling enhancement (a sqrt(S)-coupled thermalized
collective channel), which universality does not forbid.  So static E' =
"no anomalously bright exterior emission vertex," and step (a) above is
underwritten by charge-route universality PLUS the
no-bright-collective-channel condition.  Dynamically, the latter is
replaced by the starvation theorem plus `Gamma_th <= c_P T` within its
refill scope.  Step (b) still follows from
the ordinary-sector envelope.  The point that survives verbatim: the
per-channel cap needs no input beyond E' and the observable — but E'
itself is the emission-envelope condition, not universality alone.

## 6. Consequences

The certificate's dependency structure, fully reduced.  Keep the static
and dynamically completed versions separate:

```text
INPUT I  (observable):  line asymmetry within eta of calibrated KMS.
STATIC INPUT II (E' = emission-envelope condition): no anomalously
             bright exterior emission vertex.

DYNAMIC REPLACEMENT FOR II's outlier half:
             (2a) no non-universal charge — EFT/equivalence-principle
                  universality;
             (2b) no hidden persistent bright collective channel —
                  starvation bound plus Gamma_th <= c_P T, within the
                  thermal Markovian refill scope.

I         => no occupation-enhanced outlier (f <= eta n_ref).
II        => ordinary sector ETH-enveloped
             (Lemma 1 => N_eff^ord ~ cS).
I + static II, or I + dynamic replacement + ordinary-sector envelope
          => N_eff ~ min(cS, f_bad^{-2}) ~ cS for sufficiently small
             eta, where f_bad = f_occ + f_coll.
I alone   => exact floor N_eff >= 1/f; if the dangerous outlier is
             occupation-enhanced, f <= eta n_ref, so
             N_eff >= 1/(eta n_ref).  This does NOT exclude a
             coupling-enhanced thermal outlier; that is II's job.
```

The "per-channel flux cap F_H/F_env ~ cS" is therefore not a third
assumption.  It is the section-4 identity plus N_eff^ord ~ cS, and the
latter is Lemma 1 on the uncontested ordinary sector.  The soft joint
dissolves into the observable, the ordinary-sector envelope, and a
named control of the two possible bright outliers.  For route 2b that
control is now dynamical rather than an unexplained commutator cap.

Bonus, worth keeping: the pure-observable floor is genuinely
assumption-light.  Even a reader who rejects coupling universality and
every envelope statement must accept `N_eff >= 1/f` exactly, and must
also accept that any occupation-enhanced bright channel is limited by
`f <= eta n_ref`.  Thus the stronger floor
`N_eff >= 1/(eta n_ref)` is earned whenever the dangerous outlier is
occupation-enhanced.  It does not rule out a coupling-enhanced thermal
outlier — the thermalized bright collective channel.  That outlier is
statically invisible; the starvation result reaches it only after the
Planckian/QNM relaxation and refill-scope assumptions are supplied.

## Discipline

- State the floor (N_eff >= 1/f, pure observable) and the saturation
  form (N_eff ~ min(cS, f^{-2}), needs N_eff^ord ~ cS) as SEPARATE
  claims with different dependency lists.  Do not quote saturation
  where only the floor is earned.
- N_eff^ord ~ cS is Lemma 1 on the ORDINARY sector; say "ordinary
  sector," because Lemma 1 on the full source is exactly what the
  outlier escapes.
- Keep the static E' formulation distinct from the dynamical
  starvation completion.  Do not silently turn QNM lore or generic
  Planckian dissipation into a theorem about every collective refill
  operator.
- The floor is the fallback for a reader who rejects universality; do
  not let the saturation headline hide that a weaker unconditional
  statement exists.

## Feeds

- `participation_pigeonhole_result.md`: the cap hypothesis E' entry is
  refined — the cap is derived here from I + II, not assumed; the
  pure-observable floor N_eff >= 1/f is new and belongs in the scope
  discussion.
- `q1b_static_certificate_theorem.md`: hypothesis list can drop "the
  per-channel cap" as a standalone item and cite this decomposition;
  add the floor as the minimal unconditional statement.
- `envelope_as_coupling_universality.md`: section 3's E'
  (emission-envelope condition) does double duty (outlier exclusion +
  ordinary-sector envelope); the outlier-exclusion half is
  charge-route universality PLUS the no-bright-collective-channel
  condition, not universality alone.  Cross-reference.
- `collective_channel_starvation_result.md`: route 2b is now bounded
  modulo Planckian/QNM relaxation; propagate that replacement whenever
  the static E' dependency is summarized.
- Paper: the certificate section can state the floor first
  (unconditional) and the saturation form second (adds E' / the
  emission-envelope condition on the ordinary sector), which is a
  cleaner and more honest logical order than the single capped bound
  now inked.
