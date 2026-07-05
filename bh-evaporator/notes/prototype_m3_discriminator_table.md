# M3 Discriminator Table: Prototype Branches

Date: 2026-07-05

Status: analytic discriminator note. This is not yet a phenomenology claim.

## Inputs carried forward

- M1: the strict Dvali memory-burden prototype has entropy-sized degeneracy in the assisted memory sector, but its thermal/flux-carrying source Gram is rank one: `N_eff = 1`. The luminosity enhancement is carried by the master occupation `n0 ~ S`, not by `S` independent source channels.
- M2: in the strict prototype, total memory occupation `N_m` is conserved. A diary deposited into memory load does not reach the emitted `b0` record except through coarse diagonal tags such as mass/frequency shifts. Hayden-Preskill-style quantum recovery is therefore blocked in the strict burden branch.
- Literature anchor: the N-portrait memory-burden papers use collective master-mode enhancement and assisted gaplessness, while Dvali:2024hsb maps burden release to model-dependent post-burden powers `tau ~ R S_BH^(1+k)` and a conservative rare-pair-annihilation bound `tau >= R S_BH^2`.

Terminology discipline: source-rank saturation and HP-style latency are independent axes. The luminosity/source-Gram lemma concerns the former inside its envelope class. Log-latency is a separate certificate supplied only when the usual scrambling/decoupling hypotheses are also present.

## Branch Table

| branch | degeneracy / DOS | source Gram at flux frequency | luminosity carrier | new-deposit latency | radiation/coherence diagnostic | current verdict |
|---|---:|---:|---|---|---|---|
| Boundary-ETH / incoherent entropy-rank | saturated or matched to BH entropy | `N_eff ~ S`, `sigma = 1`, `lambda_bar ~ eps0^2 / S`, `Tr W ~ eps0^2` | many weak incoherent channels | HP-like `O(k + log S)` emitted quanta, conditional on fast mixing and a real thermal tie | source phases average incoherently; phase-sensitive visibility should vanish or scale down with source rank | access-saturated branch |
| N-portrait / strict memory-burden | saturated by `K ~ S` assisted gapless memory modes | `N_eff = 1`, `sigma = 0`, `lambda_bar ~ eps0^2` from `C0^2 n0`, same `Tr W` scale | one collectively enhanced master source | infinite in the strict toy for fixed-energy memory diaries; BH mapping gives model-dependent post-burden powers, with conservative bound `tau >= R S_BH^2` in Dvali:2024hsb | collectively enhanced single-source branch; statistics are model-dependent until computed | degeneracy-saturated but source-rank-unsaturated |
| Ordinary local reservoir | may be large but not BH-saturated | bounded by contact/surface access, not volume entropy | local transport/contact channels | ballistic lower bound `~ S^{1/d}` if mapped to a `d`-dimensional bulk reservoir; diffusive expectation longer | statistics alone not decisive | local reservoir, not horizon-like saturation |
| Fast scrambler without saturation | mixing may be fast, but DOS/source access not entropy-saturated | can have low or intermediate `N_eff` | model-dependent | can be logarithmic internally | not enough without DOS/source-rank saturation | fast mixing alone is insufficient |

## Statistic S1: Collective Visibility

The clean radiation-side discriminator is not raw flux. Flux can be identical in the entropy-rank and collective branches because both can realize the same `Tr W`.

For a controlled analogue or frozen-routing witness, split the source into two controllable blocks feeding the same outgoing coarse mode:

```text
Gamma(phi) = |sqrt(Gamma_L) + e^{i phi} sqrt(Gamma_R)|^2
V = (Gamma_max - Gamma_min) / (Gamma_max + Gamma_min)
```

Expected scaling:

- Rank-one collective/coherent branch: `V = O(1)` when the relative phase is controllable.
- Incoherent entropy-rank branch: the cross term averages away; `V -> 0`, or at most scales like `N_eff^{-1/2}` under finite random-source sampling.

This is a tabletop/control-protocol statistic. It is not a claim that an exterior Schwarzschild observer can infer source `N_eff` from ordinary Hawking flux.

## Statistic S2: Intensity Cumulant Is Supporting Only

A possible secondary diagnostic is the normally ordered zero-delay intensity ratio for a fixed coarse outgoing mode:

```text
g2(0) = <A^\dagger A^\dagger A A> / <A^\dagger A>^2
```

This should not be used as the primary M3 claim yet. In an incoherent chaotic single temporal mode one expects bunching, while a coherent bosonic source can be closer to Poissonian, but the actual value depends on source state, time/frequency resolution, depletion, continuum coupling, and detector mode count. For M3, `g2` is a target calculation, not an adjudicated branch label.

## M3 Verdict

The robust discriminator is two-dimensional:

```text
axis 1: source-rank saturation, N_eff ~ S versus N_eff = 1
axis 2: diary latency, HP-like logarithmic recovery versus burden-blocked/power-long release
secondary axis: controlled coherence visibility, not ordinary flux
```

Thus the Dvali memory-burden/N-portrait branch should be recorded as:

```text
degeneracy-saturated,
source-rank-unsaturated,
strict-model HP-latency blocked,
collectively enhanced single-source statistics pending explicit calculation.
```

Avoid the shorthand "Dicke-like" unless a concrete `g2` or visibility calculation is attached. The safer label is "collectively enhanced single-source branch."
