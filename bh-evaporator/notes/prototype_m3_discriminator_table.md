# M3 Discriminator Table: Prototype Branches

Date: 2026-07-05

Status: analytic discriminator note, updated after Q1 and the Q1b
line-asymmetry result.  This is still not a phenomenology claim.

## Inputs Carried Forward

- M1: the strict Dvali memory-burden prototype has entropy-sized
  degeneracy in the assisted memory sector, but its thermal/flux-carrying
  source Gram is rank one: `N_eff = 1`.  The luminosity enhancement is
  carried by the master occupation `n0 ~ S`, not by `S` independent
  source channels.
- M2: in the strict prototype, total memory occupation `N_m` is
  conserved.  A diary deposited into memory load does not reach the
  emitted `b0` record except through coarse diagonal tags such as
  mass/frequency shifts.  HP-style quantum recovery is therefore blocked
  in the strict burden branch.
- Q1: per-resolved-mode counting statistics separates the strict sharp
  master branch from the ETH-Gaussian/thermal branch:

```text
strict sharp master branch:       g2(0) = 1 - 1/S;
ETH-Gaussian entropy-rank branch: g2(0) = 2;
semiclassical Hawking mode:       g2(0) = 2.
```

- Q1b (statistics-rank link, lemma 3b): stimulated
  emission/absorption asymmetry of the calibrated line separates the
  same branches at probe level.  A channel with mean occupation `K` has
  `em/abs = K/(K+1) -> 1` for `K >> 1`; an equilibrium channel
  reproduces the Boltzmann ratio `e^(-omega/T)` exactly.  The strict
  prototype's line has `em/abs = n0/(n0+1) = 1 - 1/S` where the KMS
  line requires `e^(-omega/T)` — an O(1) detailed-balance failure,
  independent of `g2`.

- Literature anchor: the N-portrait memory-burden papers use collective
  master-mode enhancement and assisted gaplessness, while Dvali:2024hsb
  maps burden release to model-dependent post-burden powers
  `tau ~ R S_BH^(1+k)` and a conservative rare-pair-annihilation bound
  `tau >= R S_BH^2`.

Terminology discipline: source-rank saturation and HP-style latency are
independent axes.  The luminosity/source-Gram lemma concerns the former
inside its envelope class.  Log-latency is a separate certificate
supplied only when the usual scrambling/decoupling hypotheses are also
present.

## Branch Table

| branch | degeneracy / DOS | source Gram at flux frequency | luminosity carrier | new-deposit latency | per-resolved-mode counting | line asymmetry (em/abs) | current verdict |
|---|---:|---:|---|---|---|---|---|
| Boundary-ETH / incoherent ETH-Gaussian entropy-rank | saturated or matched to BH entropy | `N_eff ~ S`, `sigma = 1`, `lambda_bar ~ eps0^2 / S`, `Tr W ~ eps0^2` | many weak incoherent channels | HP-like `O(k + log S)` emitted quanta, conditional on fast mixing and a real thermal tie | thermal/chaotic `g2(0)=2`; source phases average incoherently | Boltzmann `e^(-omega/T)` (KMS-calibrated equilibrium channels) | access-saturated branch |
| N-portrait / strict memory-burden | saturated by `K ~ S` assisted gapless memory modes | `N_eff = 1`, `sigma = 0`, `lambda_bar ~ eps0^2` from `C0^2 n0`, same `Tr W` scale | one collectively enhanced sharp master source | infinite in the strict toy for fixed-energy memory diaries; BH mapping gives model-dependent post-burden powers, with conservative bound `tau >= R S_BH^2` in Dvali:2024hsb | resolved-mode `g2(0)=1-1/S`; broadband tag-multiplexing can increase apparent bunching | `n0/(n0+1) = 1 - 1/S`; O(1) KMS failure (backreaction escape closed for the strict class; resolved-ladder sub-case clause-covered — see `asymmetry_backreaction_escape_result.md`) | degeneracy-saturated but source-rank-unsaturated |
| Starved bright collective channel (route 2b deployed; `collective_channel_starvation_result.md`) | saturated memory sector behind the channel | `N_eff = 1` by construction (single collective operator `b'`, coupling `sqrt(K) g`) | one thermalized collective mode at `O(1)` occupation | not addressed by statics; the only assumption-free reach is the latency rung | `g2(0) = 2` exactly (Gaussian; starvation-blind) | starts at KMS, drifts BELOW: `r* = n*/(n*+1) < e^(-omega/T)` with deficit `x/(nbar+1+x)`, `x = Gamma'/Gamma_th`; strict deployment carries integrated flux fraction `1/K` only | static mimicry exact but starvation-limited; sustaining full flux needs super-Planckian refill |
| Semiclassical Hawking mode | BH entropy assumed | not a source-Gram model by itself | thermal reduction of two-mode squeezed pair | HP latency only with extra Page/decoupling setup | thermal/chaotic `g2(0)=2` per exterior mode | Boltzmann `e^(-omega/T)` exactly (thermal stimulated response) | votes against the strict sharp coherent branch |
| Ordinary local reservoir | may be large but not BH-saturated | bounded by contact/surface access, not volume entropy | local transport/contact channels | ballistic lower bound `~ S^{1/d}` if mapped to a `d`-dimensional bulk reservoir; diffusive expectation longer | statistics alone not decisive | Boltzmann at reservoir temperature; not decisive by itself | local reservoir, not horizon-like saturation |
| Fast scrambler without saturation | mixing may be fast, but DOS/source access not entropy-saturated | can have low or intermediate `N_eff` | model-dependent | can be logarithmic internally | not enough without DOS/source-rank saturation | model-dependent; not decisive | fast mixing alone is insufficient |

Adjacent taxonomy note: the near-extremal/BPS stress test is a
different off-diagonal cell, not a relabeling of the memory-burden
branch.  At T = 0 the BPS sector can be degeneracy-saturated while the
line-rank certificate is silent/undefined because no emission line is
present.  At small nonzero T, the emitted line may read S_0-sized,
active-entropy-sized, or quantum-Schwarzian-enhanced participation
depending on the verified cross-section.  The strict memory-burden
prototype instead has an active sharp line whose source rank is
unsaturated.

## Statistic S1: Controlled Visibility

The clean controlled source-side discriminator is not raw flux.  Flux
can be identical in the entropy-rank and collective branches because
both can realize the same `Tr W`.

For a controlled analogue or frozen-routing witness, split the source
into two controllable blocks feeding the same outgoing coarse mode:

```text
Gamma(phi) = |sqrt(Gamma_L) + e^{i phi} sqrt(Gamma_R)|^2
V = (Gamma_max - Gamma_min) / (Gamma_max + Gamma_min)
```

Expected scaling:

- Rank-one collective/coherent branch: `V = O(1)` when the relative
  phase is controllable.
- Incoherent entropy-rank branch: the cross term averages away;
  `V -> 0`, or at most scales like `N_eff^(-1/2)` under finite
  random-source sampling.

This is a tabletop/control-protocol statistic.  It is not a claim that
an exterior Schwarzschild observer can infer source `N_eff` from
ordinary Hawking flux.

## Statistic S2: Intensity Cumulant / Q1 Result

The passive exterior statistic is the normally ordered zero-delay
intensity ratio for a fixed resolved outgoing mode:

```text
g2(0) = <A^\dagger A^\dagger A A> / <A^\dagger A>^2
      = <n(n-1)> / <n>^2.
```

Matched-flux result:

```text
strict sharp master source:       g2(0) = 1 - 1/S;
ETH-Gaussian entropy-rank source: g2(0) = 2;
semiclassical Hawking mode:       g2(0) = 2.
```

This separates the strict coherent-single-source branch from the
ETH-Gaussian/thermal branch at O(1), but only per resolved mode.
Broadband detection over many detuned burden-tagged sub-lines can mimic
chaotic bunching.  Conversely, `g2 = 2` alone does not prove source rank:
a rank-one thermalized quasimode can also have thermal counting
statistics.

The original leg-A target for the statistics-rank link was:

```text
Schwarzschild luminosity
+ ordinary envelope
+ per-resolved-mode chaotic statistics, g2(0)=2
    => N_eff ~ S.
```

That target uses `g2` to close the coherent-enhancement loophole; it
does not treat `g2` as a direct rank meter.  After the Q1b second pass
this is passive corroboration, not the primary certificate.  The
sharper primary leg is line asymmetry; see S3.

## Statistic S3: Line Asymmetry / Q1b Result

The probe-level statistic is the stimulated emission/absorption ratio
of the calibrated line (`statistics_rank_link_result.md`, lemma 3b).
A channel with mean occupation `K` at the line has
`em/abs = K/(K+1) -> 1` for `K >> 1`; an equilibrium channel at gap
`omega` reproduces the Boltzmann ratio `e^(-omega/T)` exactly.

Matched-flux result:

```text
strict sharp master source:       em/abs = n0/(n0+1) = 1 - 1/S;
ETH-Gaussian entropy-rank source: em/abs = e^(-omega/T) (KMS);
semiclassical Hawking mode:       em/abs = e^(-omega/T) (KMS).
```

For the strict prototype this is an O(1) failure of detailed-balance
calibration, independent of `g2`.  If the observed asymmetry matches
Boltzmann to accuracy `eta`, the enhanced-channel flux fraction obeys
`f <= eta * n_bar_eq(omega) ~ 0.58 eta` at `omega ~ T` — linear in
`eta` (versus `sqrt(eps)` for the `g2` leg) and needing only
golden-rule rates, no fourth-moment ETH factorization.

Cost ordering of the certificate suite (operational ladder): `g2` is
passive (watch the light), line asymmetry is a probe (linear-response
absorption measurement), latency is deposit-and-decode.

Escape status (2026-07-05, `asymmetry_backreaction_escape_result.md`):
the depletion-backreaction escape is closed for the strict class —
number-conserving dressing only frequency-tags and cannot create
final-state multiplicity.  One kinematic sub-case (resolved anharmonic
ladder) fakes bare asymmetry at `N_eff = 1`; it is clause-covered by
the `g2` leg (per-sub-line counting is nonchaotic, not 2) and by a
two-resolution stability check within the asymmetry leg itself.

## M3 Verdict

The robust discriminator suite is now four-dimensional:

```text
axis 1: source-rank saturation, N_eff ~ S versus N_eff = 1;
axis 2: diary latency, HP-like logarithmic recovery versus blocked/long release;
axis 3: per-resolved-mode counting, g2 ~= 1 versus g2 = 2;
axis 4: line asymmetry, em/abs = e^(-omega/T) (KMS) versus 1 - 1/S.
```

Axis 4 is TWO-SIDED after the route-2b deployment check
(`collective_channel_starvation_result.md`): occupation-enhanced
channels fail HIGH (em/abs -> 1), starved collective channels fail LOW
(em/abs below Boltzmann by `Gamma'/(Gamma_th (nbar+1))`).  KMS is the
narrow middle; both deviations are signed predictions.

Thus the Dvali memory-burden/N-portrait strict branch should be recorded
as:

```text
degeneracy-saturated,
source-rank-unsaturated,
strict-model HP-latency blocked,
sharp-master resolved-mode g2(0)=1-1/S,
KMS-asymmetry failed at O(1): em/abs = 1 - 1/S.
```

Avoid the shorthand "Dicke-like."  The safer label remains
"collectively enhanced single-source branch," now with the computed Q1
counting statistic attached.
