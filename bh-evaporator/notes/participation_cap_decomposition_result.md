# The Per-Channel Flux Cap Is Not an Independent Assumption

Date: 2026-07-06

Role: shores up the softest formal joint of the Q1b certificate — the
per-channel cap F_H/F_env ~ cS asserted in
`participation_pigeonhole_result.md` and inked in
`paper_boundary_saturation/main.tex`.  Result: the cap is not a third
hypothesis.  It decomposes into (a) a pure-observable outlier bound
that needs no envelope at all, plus (b) an application of Lemma 1 to
the ordinary sector, which is itself underwritten by the same
coupling-universality principle (E') already identified.  So the whole
certificate rests on exactly two inputs — the line-asymmetry observable
and coupling universality — and the cap is downstream of them, not
alongside.  All inequalities are exact; grading per claim.  Not paper
text.

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
(2) coupling-enhanced:    closed by E' = coupling universality.
```

So the brightest-channel fraction is bounded — f <= eta n_ref — under
the two inputs (asymmetry observable + universality).  No separate cap
is invoked to bound lambda_max; the route analysis already did it.

## 4. Saturation upgrade: from N_eff >= 1/f to N_eff ~ cS

The stronger statement separates the outlier explicitly.  Write
Tr W_ord = (1-f) Tr W for the ordinary sector (outlier removed).  Then

```text
Tr(W^2) = lambda_max^2 + Tr(W^2)_ord
        = f^2 (Tr W)^2 + (Tr W_ord)^2 / N_eff^ord,
=> N_eff = 1 / ( f^2 + (1-f)^2 / N_eff^ord ).
```

With N_eff^ord ~ cS this is the corrected pigeonhole bound
N_eff ~ min(cS, f^{-2}) (superseding the linear form; consistent with
`participation_pigeonhole_result.md`).  The ONLY new ingredient beyond
section 2 is

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
disputed outlier; once sections 2-3 remove it (observably + by
universality), Lemma 1 applies to what remains WITHOUT the contested
step.

Moreover the same E' = coupling universality does double duty:

```text
E' (universality) =>
   (a) no coupling-enhanced outlier            [section 3, route 2];
   (b) ordinary emission operators are ETH-enveloped
       => Lemma 1 holds on the ordinary sector => N_eff^ord ~ cS.
```

Step (b) is the SAME argument as section 3 of
`envelope_as_coupling_universality.md` (universal minimal coupling =>
e^{-S/2} ETH envelope), now used for the residual sector rather than
against the outlier.  So the per-channel cap needs no input that was
not already on the table.

## 6. Consequences

The certificate's dependency structure, fully reduced:

```text
INPUT I  (observable):  line asymmetry within eta of calibrated KMS.
INPUT II (principle):   gravitational coupling universality (= E').

I         => no occupation-enhanced outlier (f <= eta n_ref).
II        => no coupling-enhanced outlier, AND ordinary sector
             ETH-enveloped (Lemma 1 => N_eff^ord ~ cS).
I + II    => N_eff ~ min(cS, (eta n_ref)^{-2}) ~ cS for eta small.
I alone   => N_eff >= 1/(eta n_ref), the pure-observable floor,
             valid against occupation enhancement with NO envelope.
```

The "per-channel flux cap F_H/F_env ~ cS" is therefore not a third
assumption.  It is the section-4 identity plus N_eff^ord ~ cS, and the
latter is Lemma 1 on the uncontested sector, underwritten by II.  The
soft joint dissolves into the two inputs already named.

Bonus, worth keeping: the pure-observable floor N_eff >= 1/(eta n_ref)
is a genuinely assumption-light result.  Even a reader who rejects
coupling universality and every envelope statement must accept that a
Schwarzschild line calibrated to KMS within eta has participation at
least 1/(eta n_ref) against occupation enhancement.  That is the
minimal defensible certificate, and it survives with nothing but the
KMS identity and the observed asymmetry.

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
- `envelope_as_coupling_universality.md`: section 3's universality
  argument now does double duty (outlier exclusion + ordinary-sector
  envelope); cross-reference.
- Paper: the certificate section can state the floor first
  (unconditional) and the saturation form second (adds universality on
  the ordinary sector), which is a cleaner and more honest logical
  order than the single capped bound now inked.
