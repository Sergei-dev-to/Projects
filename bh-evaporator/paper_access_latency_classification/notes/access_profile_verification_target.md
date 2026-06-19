# Access-Profile Verification Target

Date: 2026-06-17

Role: conceptual bridge / future experimental translation

Status: exploratory. This is not the main proof path, but it records the measurable quantities the theory should eventually predict.

## Purpose

Keep the long-term experimental/numerical target visible while the current work continues on deterministic observability and recovery.

The theory should eventually support a protocol that measures not just Born statistics or public decoherence, but the full access profile:

```text
public record formation
private de-protection
private recovery
disturbance under recovery
```

## Core Experimental Question

Can two measurement apparatuses have the same public classical record but different private quantum recovery laws?

In symbols:

```text
same public redundancy curve
different private recovery profile
```

This is the experimentally useful content of the constrained-access classification.

## Quantities To Predict

For a system `S`, apparatus/bath `B`, emitted records `R_i`, and diary `D` entangled with reference `D_ref`, define:

- `m_public`: minimal fragment size or record depth needed to infer the pointer outcome.
- `m_private`: minimal fragment size, record depth, or decoder/control depth needed to recover the diary.
- `lambda`: de-protection rate from the observability algebra, measured through the protected component of diary operators.
- `F_rec`: optimal or implemented diary recovery fidelity from allowed records and side information.
- `D_pub`: disturbance to public records caused by the private recovery operation.

The target separation is:

```text
m_public << m_private
```

with `m_private` varying across dynamics even when `m_public` is held fixed.

## Model Comparisons

The clean comparison set is:

```text
local finite-velocity apparatus:
    public record can form fast;
    private recovery obeys routing / Lieb-Robinson latency.

chaotic or scrambling apparatus:
    public record can form fast;
    private diary de-protects and becomes recoverable after scrambling plus record budget.

fragmented, scarred, MBL, or symmetry-protected apparatus:
    public record can form;
    private sectors remain protected or anomalously slow.

frozen or echoed dynamics:
    public record may remain;
    private recovery fails unless the access channel was already nonlocal/dressed or side information already held the diary.

nonlocal/global encoder:
    private recovery can survive frozen local routing, diagnosing nonlocal or dressed access.
```

## What This Would Test

Existing models often predict one marginal:

```text
decoherence:
    interference suppression

Quantum Darwinism:
    public redundancy of pointer data

scrambling/ETH:
    operator growth or thermalization

Hayden-Preskill:
    diary recovery after randomization and side information
```

The constrained-access prediction is a joint profile:

```text
public redundancy
private de-protection
private recovery
frozen-dynamics response
disturbance cost
```

The key test is whether public objectivity and private recovery separate:

```text
same decoherence / same public redundancy
does not imply same private recovery.
```

## Current Theory Needed Before Full Protocol

Do not turn this into an experiment-design project yet. The immediate theory tasks are:

1. Prove the approximate observability gap for deterministic Heisenberg orbits:

   ```text
   A_n = alg{U^{-i} K U^i}
   Pi_i = conditional expectation onto the one-step commutant
   T_{1:n} = Pi_n ... Pi_1
   ||T_{1:n}(O_D)||_2 <= C e^{-gamma n}
   ```

2. Use the gap to bound the exact protected component:

   ```text
   ||E_n(O_D)||_2 <= C e^{-gamma n}.
   ```

3. Relate observability/de-protection to export/decoupling for emitted records.
4. Compute the access-profile quantities in three model classes:

   ```text
   local finite-velocity
   random/chaotic scrambler
   fragmented or collective pointer
   ```

Only after those calculations are sharp should this become a concrete experimental proposal.

## Collapse/Noise Comparison

Collapse or effective-destruction models can be compared only if the protocol reaches a scale where enlarged coherent access should recover private information under unitary quantum mechanics.

The operational distinction is:

```text
effective forgetting:
    public channel cannot distinguish private information

recoverable hiding:
    enlarged coherent access can recover it

collapse/noise:
    no allowed coherent enlargement recovers it beyond the model's destruction scale
```

This is potentially interesting but secondary. The primary near-term test is the separation between public redundancy and private recovery within ordinary quantum mechanics.
