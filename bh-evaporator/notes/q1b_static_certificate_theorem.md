# Q1b Static Certificate Theorem: Consolidated Statement

Successor correction (2026-07-09): the theorem below is now a conditional
model-side statement for a fixed canonical source metric and passive channel
class.  The raw source-only Gram participation is not invariant under general
interaction refactorization; an anomalous active Gaussian channel passes the
flux/response/`g2` legs without passive starvation; aggregate `g2` also admits
hot-Gaussian blindness and signed fourth-moment cancellation.  See
`source_gram_invariance_audit.md`, `anomalous_parametric_channel_result.md`, and
`signed_cancellation_and_gram_tail_result.md`.  Do not quote the older theorem
as an exterior-identifiable black-hole source-rank certificate.

Date: 2026-07-05; dependency update 2026-07-08

Role: paper-form staging note for the Q1b result.  This consolidates
`statistics_rank_link_result.md`, `asymmetry_backreaction_escape_result.md`,
`participation_pigeonhole_result.md`, and the route-2b completion in
`collective_channel_starvation_result.md` into one theorem statement.
Not final prose; use this as the source of truth for the certificate
claim.

Dependency update: the STATIC theorem below still names E' when stated
without dynamics.  The route-2b part of E' is no longer a bare vertex
assumption once the collective-channel starvation result is admitted:
within its Markovian thermal-refill scope, it follows from
`Gamma_th <= c_P T`.  Thus there are now two calibrated versions:

```text
static only:        line asymmetry + ordinary-sector envelope
                    + E'                                      => rank bound;
dynamically closed: line asymmetry + ordinary-sector envelope
                    + EFT charge universality
                    + Planckian/QNM relaxation                 => rank bound.
```

The second version is conditional on the relaxation bound and the
starvation theorem's refill scope; it is not assumption-free.

Phase-1/2 correction (2026-07-09):

1. `collective_channel_spectral_starvation_theorem.md` removes the
   time-local Markov assumption for stationary linear, gauge-invariant
   Gaussian channels with additive self-energies.  It gives an exact
   frequency-local flux-versus-LOW-deficit identity in terms of
   `Gamma_int(omega)`; the Planckian/QNM ceiling is only a corollary.
2. `signed_cancellation_and_gram_tail_result.md` proves that one HIGH
   and one LOW channel can have an exactly calibrated aggregate ratio
   with `N_eff <= 2`.  Therefore separate `f_occ` and `f_coll` bounds
   require channel/line-shape resolution or a multi-setting
   drain/time/resolution/tomography protocol.  One net line ratio is not
   sufficient.
3. The paired legs control enhanced sectors, not the full ordinary Gram
   tail.  `N_eff^ord ~ cS` remains the ordinary-sector envelope input
   unless a cumulative tail bound is independently measured or derived.

## Theorem Target

Consider a weak, golden-rule emission model for a resolved exterior
line at frequency `omega` from a microcanonical shell.  Assume:

1. Calibration: the equilibrium emission/absorption ratio for the line
   is the shell DOS ratio

   ```text
   R(E,omega) = rho(E - omega) / rho(E),
   ```

   with `R = exp(-beta omega)` only in the thermodynamic Schwarzschild
   limit.  For rotating/charged horizons, replace this by the
   grand-canonical factor `exp[-beta(omega - m Omega_H - q Phi_H)]`.

2. Resolution: either the line is harmonic/unresolved in the sense of
   `asymmetry_backreaction_escape_result.md`, or the asymmetry is
   stable under the two-resolution check.  The resolved sloped-ladder
   fake is not excluded by bare line asymmetry alone.

3. Ordinary envelope: non-enhanced Gram eigenchannels have no hidden
   powers in their matrix-element envelope.  In per-channel form,
   their resolved-line flux is capped by `Phi_env`, normalized so that
   the Schwarzschild scaling lemma gives

   ```text
   Phi_H / Phi_env ~ c S.
   ```

   This is the per-channel translation of
   `paper_boundary_saturation/main.tex`, Lemma
   "Schwarzschild luminosity and effective rank"; the paper verifies
   the scaling, not an exact numerical cap.  NOT an independent
   assumption (`participation_cap_decomposition_result.md`): it is
   Lemma 1 on the ORDINARY sector only — uncontested, since the
   envelope was only ever disputed for the enhanced outlier — and is
   underwritten by the same E' (assumption 4).  A pure-observable
   floor N_eff >= 1/f survives even if this is rejected (see the
   minimal-statement note below).

4. Coupling-enhancement control.  In the static-only statement this is
   the commutator/vertex cap `E'`: the ordinary envelope also caps the
   channel commutator scale, so coupling enhancement cannot hide powers
   of `S`.  In the dynamically completed statement E' decomposes into:

   ```text
   (2a) no channel-selective microscopic gravitational charge
        [standard EFT/equivalence-principle input];
   (2b) no persistently bright thermal collective channel
        [derived within the starvation model from Gamma_th <= c_P T].
   ```

   Line asymmetry is statically blind to pure coupling enhancement, but
   a drained collective channel with Planckian-limited refill develops a
   LOW-side asymmetry deficit.  Strongly non-Markovian refill and the
   fully multiplexed mixed-frequency case remain outside the completed
   statement.

5. The channel-resolved or multi-setting-separated line asymmetry is
   within `eta_+`/`eta_-` of the calibrated reference.  A single
   aggregate tolerance cannot be used as both bounds because HIGH and
   LOW defects can cancel.  For a Schwarzschild thermal line with
   `R = exp(-beta omega) < 1`, write

   ```text
   n_ref = R / (1 - R).
   ```

Then a separately bounded occupation-enhanced channel can carry at most
flux fraction

```text
f <= eta_+ * n_ref
```

up to the convention used for the asymmetry error.  Therefore:

```text
ordinary-sector support count:
N_eff^ord >= (1 - f) * c * S;

total source participation:
N_eff >= 1 / ( f^2 + (1 - f)/(c S) )
      ~ min(c S, f^-2).
```

This displayed total bound is the conservative support-count form.  The
exact decomposition is

```text
N_eff = 1 / ( f^2 + (1 - f)^2 / N_eff^ord ).
```

If the ordinary sector itself has normalized participation
`N_eff^ord ~ cS`, this becomes
`1/(f^2 + (1-f)^2/(cS))`.  If one uses only the weaker per-channel
ordinary cap, `N_eff^ord >= (1-f)cS`, it reduces to the conservative
displayed bound above.  Both have the same parametric floor
`min(cS, f^-2)`.

In particular, exact calibration (`eta = 0`) gives
`N_eff >= c S` within the class.  At finite calibration accuracy,
full total-participation saturation requires

```text
eta <~ 1 / (n_ref sqrt(S)).
```

At coarser accuracy, the theorem still gives the explicit floor
`N_eff ~ min(cS, (eta n_ref)^-2)`.

For the dynamically completed version, let `f_coll` be the total flux
fraction carried by `m` thermal collective channels in the scope of
`collective_channel_starvation_result.md`.  The starvation bound gives,
at `omega ~ T` and up to greybody and occupation constants,

```text
f_coll <~ m c_P eta_-.
```

Use the total dangerous fraction

```text
f_bad = f_occ + f_coll,
f_occ <= eta_+ n_ref,
```

in the participation formulas above.  Exact calibrated asymmetry with
finite `c_P` sets both fractions to zero in this scope.  For finite
accuracy the theorem certifies the corresponding explicit floor; it
does not turn a coarse measurement into full entropy-rank saturation.
These formulas are invalid if `eta_+` and `eta_-` are inferred from one
net aggregate ratio rather than separately resolved/protocol-bounded.

## Minimal Statement (assumption-light floor)

Independently of assumptions 3 and 4, a weaker statement holds on
observables alone
(`participation_cap_decomposition_result.md` §2).  From
`Tr(W^2) <= lambda_max Tr W` (exact) and the observable trace,

```text
N_eff >= 1/f,
```

and against occupation enhancement the asymmetry bounds
`f <= eta n_ref`, so

```text
N_eff >= 1 / (eta n_ref)
    [pure observable against occupation enhancement; no envelope, no E'].
```

A reader who rejects coupling universality and every envelope
statement must still accept the exact floor `N_eff >= 1/f`, and must
also accept that an occupation-enhanced bright channel is bounded by
`f <= eta n_ref`.  The stronger displayed floor follows if the
dangerous outlier is occupation-enhanced.  It does not exclude a
coupling-enhanced thermal outlier; that is exactly what assumption 4
does.  The saturation form above is the upgrade that adds assumptions
3-4; quote whichever matches the assumptions in play.

## Proof Skeleton

For any channel operator `A_i,omega`,

```text
Gamma_em,i  proportional to <A_i^dag A_i>,
Gamma_abs,i proportional to <A_i A_i^dag>.
```

Define generalized occupation

```text
K_i = <A_i^dag A_i> / <[A_i, A_i^dag]>.
```

Then

```text
r_i = Gamma_em,i / Gamma_abs,i = K_i / (K_i + 1).
```

Large occupation enhancement gives `r_i -> 1`, so a calibrated
Schwarzschild line excludes it except for flux fraction `f`.  Pure
coupling enhancement leaves the instantaneous equilibrium `r_i`
invariant.  The static theorem therefore excludes it only through the
ordinary-envelope plus `E'` hypotheses.  The dynamical completion treats
the collective subcase separately: radiative drain competes with refill,
and `Gamma_th <= c_P T` turns a persistent bright collective channel into
a LOW-side KMS deficit bounded in proportion to its flux fraction.

The remaining flux must pass through ordinary channels with per-channel
flux cap `Phi_env`.  Pigeonhole:

```text
N_eff^ord >= (1 - f) Phi_H / Phi_env.
```

For total participation, an enhanced channel with flux fraction `f`
contributes `f^2` to the normalized second moment, giving

```text
N_eff >= 1 / (f^2 + (1 - f) Phi_env/Phi_H).
```

This is the conservative support-count/cap version.  The exact
ordinary-sector decomposition is
`N_eff = 1/(f^2 + (1-f)^2/N_eff^ord)`.

## Role Of g2

The `g2` leg is passive corroboration, not a direct rank meter.
It is still essential for two jobs:

- It catches the resolved sloped-ladder fake: bare asymmetry can look
  KMS while per-sub-line counting stays nonchaotic/subthermal.
- It passively distinguishes the strict sharp collective branch
  (`g2 = 1 - 1/S` per resolved mode) from ETH-Gaussian/Hawking
  thermality (`g2 = 2`).

It also prevents arbitrary HIGH/LOW cancellation from being treated as
a response-only success.  If HIGH channels satisfy
`g2_i <= 2-kappa` and the observed composite statistic obeys
`g2_tot >= 2-epsilon_g`, then

```text
Q_H = sum_{i in H} f_i^2 <= epsilon_g/kappa.
```

If a separate spectral protocol bounds LOW total flux by `F_C <= c_-`
and the ordinary tail obeys `Q_O <= p`, then

```text
N_eff >= 1/[epsilon_g/kappa + c_-^2 + p].
```

This is the cancellation-safe paired-leg form.  Entropy-sized rank
still requires `p ~ 1/S`; the response legs do not derive that ordinary
tail bound by themselves.

## Branch Consequence

Within the class, a coherent/N-portrait branch that reproduces the
Schwarzschild flux and calibrated line asymmetry must choose one of
four exits:

1. become entropy-rank participating through register-sampling
   emission;
2. use a resolved sloped ladder, which predicts nonchaotic sub-line
   `g2` and resolution-dependent asymmetry;
3. leave the calibrated equilibrium class;
4. emit through a thermalized bright COLLECTIVE exterior channel —
   `g2 = 2` and instantaneously KMS-preserving at rank one (route 2b of
   `envelope_as_coupling_universality.md`).  This exit is invisible to
   equilibrium static legs, but its explicit deployment is
   reservoir-starved.  Within the thermal Markovian refill model,
   `Gamma_th <= c_P T` forces a LOW-side asymmetry deficit proportional
   to its flux fraction.  It survives only by super-Planckian refill,
   by leaving that refill class, or in an unresolved multiplexed corner.
   The latency rung remains the assumption-light backstop.

The strict 2006 prototype takes exit 1's complement — it is route (1)
occupation, caught by asymmetry, so it does not reach any of these
exits.  This is the current strongest fork statement: not a refutation
of all N-portrait dynamics, but a conditional no-go for the strict
coherent branch.  Exit 4 is now a rate-bounded residue rather than an
unnamed vertex assumption, but its Planckian and refill-scope qualifiers
remain load-bearing.

## Owed Before Paper Text

- Replace all Boltzmann-only phrasing with DOS-ratio calibration, using
  Boltzmann/grand-canonical forms only as limits.
- Add exact KMS references and black-hole stimulated-response
  references to `refs.bib`.
- Verify the near-extremal/JT greybody and Schwarzian claims before
  using them as examples.
- Run the broadband-vs-resolved `g2` multiplexing numeric if the
  sloped-ladder or tag-multiplexing caveat becomes central.
- Promote the collective-starvation bound from the single/equal-split
  calculation to mixed frequencies and unequal flux fractions before
  quoting the `m`-channel form as a full theorem.
- Replace generic "Planckian" rhetoric by the strongest operator-specific
  QNM/relaxation statement that the black-hole literature actually
  supports; generic many-body Planckian dissipation is only conjectural.
