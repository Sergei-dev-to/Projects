# Constrained Access Program Plan Review

Date: 2026-06-18

Role: conceptual bridge / program plan

Status: current orientation

## Verdict

The plan is right, with one correction in emphasis. The central object
is not the expander branch, the moment-gap branch, or the horizon analogy
by itself. The central object is the access profile of private quantum
information:

```text
publicization != de-protection != coherent export.
```

That separation is now the program's strongest conceptual and technical
spine. It connects the theorem stack, the horizon motivation, the
measurement-cut direction, and possible experiments.

## Core Program

Given:

```text
quantum substrate
specified observer/access algebra
record channel
allowed side information and controls
```

classify what happens to information outside the public center.

The current fates are:

```text
publicized:
    redundantly recorded as commuting/classical data

protected:
    invisible to the current access algebra; commutant/noiseless
    subsystem

de-protected but not recovered:
    no longer protected, but only disturbed, dephased, fragmented, or
    hidden in records that do not support quantum recovery

coherently exported:
    recoverable from allowed records by a quantum decoder
```

The new lesson from the abelian/public-export counterexample is that the
middle category is not cosmetic. De-protection can happen without
recovery. A record can touch the private information and still destroy
coherence relative to the allowed channel.

## Result Shape

The theorem-shaped result should be stated as a constrained-access
classification:

```text
finite-velocity source-local access
=> no location-uniform fast coherent recovery of arbitrary private
   deposits

therefore horizon-like fast private recovery requires either:
    fast routing/scrambling plus coherent export,
or:
    dressed/nonlocal access.
```

Supporting pieces already exist:

```text
public center:
    exact no-broadcasting/cut theorem; approximate side imported from
    Quantum Darwinism and SBS

protected complement:
    commutant/noiseless-subsystem theorem

source-local latency:
    reduced-record Lieb-Robinson obstruction plus constant-channel
    no-recovery lemma

insufficiency results:
    saturation, anonymity, publicization, visibility, and de-protection
    do not imply coherent recovery

positive witness:
    theorem-backed expander/design mixer realizes the fast routed branch
    under explicit decoupling/export assumptions
```

The expander and moment-gap work should be treated as witness machinery:

```text
Can ordinary sparse dynamics realize the coherent-export corner quickly?
```

It is a valuable branch, but it is not the program center.

## Experimental Connection

The experimental or numerical program should measure an access profile,
not attempt to simulate black holes.

Define three operational quantities:

```text
R_public:
    redundant recoverability / distinguishability of public pointer or
    sector data from many fragments

lambda:
    de-protection or observability rate for private operators relative
    to the access algebra

F_export:
    entanglement-fidelity recovery of a private diary from the allowed
    records and admissible side information
```

The central operational separation is:

```text
R_public high
and
lambda high
do not imply
F_export high.
```

That is experimentally legible inside ordinary quantum mechanics. It is
closer in spirit to an operational inequality or protocol than to a new
postulate.

## Minimal Model Suite

The next concrete artifact should compare three small circuit families.

### 1. Public Dephasing Model

Expected profile:

```text
R_public high
lambda high for incompatible/private observables
F_export low
```

Role:

Shows publicization and de-protection without coherent export.

### 2. Coherent Export / Scrambling Model

Expected profile:

```text
R_public possibly high for coarse data
lambda rises after scrambling/routing
F_export rises only after HP/decoupling record budget is met
```

Role:

Positive witness for the coherent-export fate.

### 3. Protected Commutant Model

Expected profile:

```text
R_public high for sector label
lambda approximately zero for private block
F_export low until access algebra is enlarged
```

Role:

Shows true protected privacy rather than dephased privacy.

## Horizon / Measurement Comparison

Use the same access profile for each case.

Ordinary measurement:

```text
publicization dominates;
private coherence is usually de-protected or dephased;
coherent recovery requires moving/enlarging the cut.
```

Ordinary local reservoir:

```text
coherent export can occur, but worst-case private recovery is delayed by
finite-velocity routing.
```

Horizon-like interface:

```text
public no-hair data are easy;
private information must be coherently exported at fast latency,
or recovered through dressed/nonlocal access.
```

Dressed/holographic access:

```text
private information is recoverable because the allowed algebra is larger
or less factorized than the naive source-local record algebra.
```

This comparison should avoid the claim that horizons and measurement
cuts are identical. They share an access skeleton; their private
information fates can differ.

## Main Risks

### Risk 1: Restating Decoherence

The public side alone is mostly known:

```text
redundant public records -> objective classical data.
```

The new content must involve the private complement:

```text
protected vs de-protected vs coherently exported.
```

### Risk 2: Treating De-Protection As Recovery

This is now the central technical warning. The observability gap
`lambda` is useful, but it is not a recovery invariant. Recovery needs a
decoupling/export condition or direct recovery fidelity.

### Risk 3: Expander Drift

The expander/moment-gap branch is a witness problem. It should not set
the program agenda unless it produces a concrete result about coherent
export.

### Risk 4: Experiment Becomes Tomography

An experimental protocol must compare the three quantities
`R_public`, `lambda`, and `F_export`. If it only reconstructs the full
state by tomography, it misses the constrained-access point.

## Immediate Plan

1. Update the main program notes so the three fates are explicit:

   ```text
   publicized / protected / de-protected-not-recovered /
   coherently exported
   ```

2. Build the minimal model suite as a numerical or circuit-level note.

3. Define the access-profile observables precisely:

   ```text
   R_public
   lambda
   F_export
   ```

4. Use those observables to compare:

   ```text
   dephasing measurement;
   protected sector model;
   coherent scrambling/export model.
   ```

5. Return to expander moment gaps only as a positive coherent-export
   witness after the access-profile protocol is clear.

## Success Criteria

A good near-term result would be:

```text
Two or three explicit finite-dimensional channels/circuits have the same
or similar public records but provably different private fates:

    protected,
    de-protected but not recovered,
    coherently exported.
```

A stronger result would provide an experimentally implementable protocol
or inequality:

```text
high public redundancy + high de-protection
does not imply high private recovery fidelity.
```

That would make the constrained-access program testable without leaving
ordinary quantum mechanics.

