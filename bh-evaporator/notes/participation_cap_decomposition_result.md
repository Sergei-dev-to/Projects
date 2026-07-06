# The Per-Channel Flux Cap Is Not an Independent Assumption

Date: 2026-07-06

Role: shores up the softest formal joint of the Q1b certificate — the
per-channel cap F_H/F_env ~ cS asserted in
`participation_pigeonhole_result.md` and inked in
`paper_boundary_saturation/main.tex`.  Result: the cap is not a third
hypothesis.  It decomposes into (a) a pure-observable outlier bound
that needs no envelope at all, plus (b) an application of Lemma 1 to
the ordinary sector, which is itself underwritten by the same E'
(emission-envelope condition) already identified.  So the whole
certificate rests on exactly two inputs — the line-asymmetry observable
and E' — and the cap is downstream of them, not alongside.  (NB: E' is
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
(2) coupling-enhanced:    closed by E' (no anomalously bright exterior
    vertex): its charge-route subcase (2a) by coupling universality,
    its collective-route subcase (2b) only as a dynamical residue —
    universality does NOT forbid a sqrt(S) collective vertex
    (`envelope_as_coupling_universality.md` §3).
```

So the brightest-channel fraction is bounded — f <= eta n_ref — under
the two inputs (asymmetry observable + E'), where the coupling half of
E' is closed by universality only for the charge subroute; the
collective subroute is the open dynamical question.  No separate cap
is invoked to bound lambda_max; the route analysis already did it.

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
only the charge subroute), Lemma 1 applies to what remains WITHOUT the
contested step.

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
closes only the non-universal-CHARGE failure; the live residue is
COLLECTIVE coupling enhancement (a sqrt(S)-coupled thermalized
collective channel), which universality does not forbid.  So E' =
"no anomalously bright exterior emission vertex," and step (a) above is
underwritten by charge-route universality PLUS the
no-bright-collective-channel condition.  Step (b) still follows from
the ordinary-sector envelope.  The point that survives verbatim: the
per-channel cap needs no input beyond E' and the observable — but E'
itself is the emission-envelope condition, not universality alone.

## 6. Consequences

The certificate's dependency structure, fully reduced:

```text
INPUT I  (observable):  line asymmetry within eta of calibrated KMS.
INPUT II (E' = emission-envelope condition):  no anomalously bright
             exterior emission vertex.  Two parts: (2a) no
             non-universal charge — closed by universality/Weinberg-
             Witten in the EFT regime; (2b) no thermalized bright
             COLLECTIVE channel — the live dynamical residue, NOT
             closed by universality.

I         => no occupation-enhanced outlier (f <= eta n_ref).
II        => no coupling-enhanced outlier (via 2a + 2b), AND ordinary
             sector ETH-enveloped (Lemma 1 => N_eff^ord ~ cS).
I + II    => N_eff ~ min(cS, (eta n_ref)^{-2}) ~ cS for eta small.
I alone   => exact floor N_eff >= 1/f; if the dangerous outlier is
             occupation-enhanced, f <= eta n_ref, so
             N_eff >= 1/(eta n_ref).  This does NOT exclude a
             coupling-enhanced thermal outlier; that is II's job.
```

The "per-channel flux cap F_H/F_env ~ cS" is therefore not a third
assumption.  It is the section-4 identity plus N_eff^ord ~ cS, and the
latter is Lemma 1 on the uncontested sector, underwritten by II (E',
the emission-envelope condition — charge route by universality,
collective route as the live residue).  The
soft joint dissolves into the two inputs already named.

Bonus, worth keeping: the pure-observable floor is genuinely
assumption-light.  Even a reader who rejects coupling universality and
every envelope statement must accept `N_eff >= 1/f` exactly, and must
also accept that any occupation-enhanced bright channel is limited by
`f <= eta n_ref`.  Thus the stronger floor
`N_eff >= 1/(eta n_ref)` is earned whenever the dangerous outlier is
occupation-enhanced.  It does not rule out a coupling-enhanced thermal
outlier — the thermalized bright collective channel — which is
precisely the E' / collective-channel residue (NOT a universality
residue: universality does not bear on it).

## Discipline

- State the floor (N_eff >= 1/f, pure observable) and the saturation
  form (N_eff ~ min(cS, f^{-2}), needs N_eff^ord ~ cS) as SEPARATE
  claims with different dependency lists.  Do not quote saturation
  where only the floor is earned.
- N_eff^ord ~ cS is Lemma 1 on the ORDINARY sector; say "ordinary
  sector," because Lemma 1 on the full source is exactly what the
  outlier escapes.
- The double-duty of E' (excludes outlier + envelopes the residual)
  is the load-bearing observation; keep both halves explicit.
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
- Paper: the certificate section can state the floor first
  (unconditional) and the saturation form second (adds E' / the
  emission-envelope condition on the ordinary sector), which is a
  cleaner and more honest logical order than the single capped bound
  now inked.
