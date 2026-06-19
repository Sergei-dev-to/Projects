# External Review Response

Date: 2026-06-18

Role: review packet

Status: current

## Verdict

The external review reads the theorem stack correctly. The core result is
not the iid/random baseline. The core result is the latency dichotomy:

```text
source-local emission + finite Lieb-Robinson velocity
=> no location-uniform fast recovery of arbitrary remote private deposits
```

Equivalently:

```text
location-uniform fast recovery
=> fast routing/scrambling or nonlocal/dressed access
```

This is an information-theoretic obstruction. It does not depend on
decoder complexity.

## Changes Made

The review led to four concrete draft changes.

1. The abstract and introduction now state that the latency obstruction
   is information-theoretic, independent of decoding complexity.

2. The reduced-record LR proof now spells out the
   controlled-`U_Y`/spectator-reference argument, making the
   diamond-norm statement visibly stable under diary-reference
   entanglement.

3. The record-generating algebra is now explicitly relative to the
   specified access family. Enlarging the allowed instruments or adding
   dressed observables enlarges `A_rec` and can shrink the protected
   commutant.

4. The observability-gap section now treats the product of one-step
   commutant projections as a sufficient certificate, not the primary
   physical definition. Conditional/windowed contraction is foregrounded
   as the deterministic target.

## What Remains Open

The missing positive theorem is deterministic:

```text
P_i = U^{-i} K U^i
```

For a concrete chaotic or scrambling family, prove that the correlated
Heisenberg record sequence has a positive observability/de-protection
rate on a fixed diary algebra, and separately prove the export/decoupling
condition that makes emitted records reconstructive.

The random baselines close only the idealized model:

```text
independent randomization
=> fixed-diary de-protection
=> fixed-diary recovery
```

They do not by themselves prove the deterministic horizon-like result.

## Best Next Technical Routes

The review points toward four existing toolchains:

```text
operator spreading / OTOCs:
    quantify growth of [U^{-i} K U^i, O_D]

unitary designs / frame potentials:
    show when deterministic evolution manufactures effectively
    independent record generators

free probability / asymptotic freeness:
    estimate contraction between diary algebra and rotated record
    subalgebras

quantum-control observability:
    use dynamical Lie algebra or observability-Gramian analogues for
    the generated record algebra
```

The largest reasonable next step is to choose one concrete deterministic
scrambling model and try to prove a windowed conditional contraction
bound. A failure there would still be useful: it would identify what
kind of chaotic dynamics is insufficient for horizon-like private
recovery.
