# Q1b Static Certificate Theorem: Consolidated Statement

Date: 2026-07-05

Role: paper-form staging note for the Q1b result.  This consolidates
`statistics_rank_link_result.md`, `asymmetry_backreaction_escape_result.md`,
and `participation_pigeonhole_result.md` into one theorem statement.
Not final prose; use this as the source of truth for the certificate
claim.

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

4. Commutator cap `E'`: the ordinary envelope also caps the channel
   commutator scale, so coupling enhancement cannot hide powers of `S`.
   Line asymmetry is blind to pure coupling enhancement; this is a
   hypothesis, not an observed consequence.

5. The observed line asymmetry is within `eta` of the calibrated
   reference.  For a Schwarzschild thermal line with
   `R = exp(-beta omega) < 1`, write

   ```text
   n_ref = R / (1 - R).
   ```

Then occupation-enhanced channels can carry at most flux fraction

```text
f <= eta * n_ref
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
coupling enhancement leaves `r_i` invariant, so it is excluded only by
the ordinary-envelope plus `E'` hypotheses.

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

## Branch Consequence

Within the class, a coherent/N-portrait branch that reproduces the
Schwarzschild flux and calibrated line asymmetry must choose one of
three exits:

1. become entropy-rank participating through register-sampling
   emission;
2. use a resolved sloped ladder, which predicts nonchaotic sub-line
   `g2` and resolution-dependent asymmetry;
3. leave the calibrated equilibrium class.

This is the current strongest fork statement: not a refutation of all
N-portrait dynamics, but a conditional no-go for the strict coherent
branch inside the certificate class.

## Owed Before Paper Text

- Replace all Boltzmann-only phrasing with DOS-ratio calibration, using
  Boltzmann/grand-canonical forms only as limits.
- Add exact KMS references and black-hole stimulated-response
  references to `refs.bib`.
- Verify the near-extremal/JT greybody and Schwarzian claims before
  using them as examples.
- Run the broadband-vs-resolved `g2` multiplexing numeric if the
  sloped-ladder or tag-multiplexing caveat becomes central.
