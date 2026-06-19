# Private Complement Unified Frame

Date: 2026-06-15

Status: conceptual note.  This is not theorem source.  It records the
shared frame behind the Heisenberg-cut and horizon-interface directions.

## Core Question

The useful question is not only how a public classical layer appears.
That is largely decoherence, Quantum Darwinism, and spectrum broadcast
structure.

The sharper question is:

```text
Given a public classical layer, what happens to the quantum information
that is not redundantly public, and what access change makes it public,
recoverable, or physically consequential?
```

The commutant theorem forces a three-compartment structure.  The
two-part language "public center versus private complement" is useful
only as a first pass.

## Three Compartments

For a record-generating algebra,

```tex
\mathcal A_{\rm rec}
=
\bigoplus_x
\mathcal B(\mathcal H_x^L)\otimes I_x^R,
```

the Hilbert space decomposes as

```tex
\mathcal H
=
\bigoplus_x
\mathcal H_x^L\otimes\mathcal H_x^R,
```

and the commutant is

```tex
\mathcal A_{\rm rec}'
=
\bigoplus_x
I_x^L\otimes\mathcal B(\mathcal H_x^R).
```

This gives three operational compartments:

**Public center.**
The sector label `x`, represented by the projectors `P_x`.

Fate:

```text
immediate, redundant, effectively classical.
```

**Recorded-but-deep block.**
The noncommuting algebra `B(H_x^L)` inside a public sector.  It couples
to the record algebra, but not necessarily redundantly or early.

Fate:

```text
hidden from small/passive fragments;
recoverable only from large, late, global, or side-informed records;
latency and decoder complexity matter.
```

**Noiseless commutant.**
The algebra `B(H_x^R)` in `A_rec'`.  It does not couple to the current
record-generating algebra.

Fate:

```text
protected under this access algebra;
not recovered by collecting more of the same passive record;
revealed only by changing the algebra or by later dynamics that changes
the record-generating algebra.
```

The recorded-but-deep block and the noiseless commutant are both
"private" relative to small public records, but they are not the same
object.  They have opposite recovery laws: one is hidden-but-recorded,
the other is protected-because-unrecorded.

## Fixed Cut Versus Moving the Cut

There are two different operations that should not be conflated.

**Recovery within a fixed cut.**
The record-generating algebra is fixed.  The observer collects more
records, waits longer, gains side information, or uses a better decoder.
This can recover recorded-but-deep information in `B(H_x^L)`.

Examples:

```text
late/global environmental fragments;
Page/HP radiation with side information;
ordinary transport into a detector;
scrambling followed by emitted records.
```

**Moving the cut.**
The observer changes the allowed measurement algebra.  This chooses a
new `A_rec`, hence a new commutant and a new private complement.

Examples:

```text
interferometric access instead of position-like records;
quantum-eraser protocols;
mining or adding a new coupling;
dressed/boundary reconstruction relative to a bulk factorization.
```

Changing the measurement algebra does not reveal the old commutant by
collecting more of the same record.  It redraws what counts as recorded
and what counts as noiseless.

## Heisenberg Cut Direction

For ordinary quantum-to-classical emergence:

```text
public center:
    stable pointer/classical data redundantly recorded;

recorded-but-deep block:
    information present only in global correlations or late/large
    fragments;

noiseless commutant:
    coherences or degrees invisible to the chosen measurement algebra;

cut mobility:
    often cheap, because the experimenter may choose a different basis,
    interferometer, quantum eraser, or global environment operation.
```

The recovery law is generally apparatus-dependent.  A private degree may
be inaccessible to ordinary fragments while still being recoverable by
global control or by changing the experimental algebra.

Quantum eraser and recoherence examples usually live near the boundary
of the public-record assumption: if which-path information was never
made robustly objective, recoherence is possible because the public
center was not fully stabilized.  That mechanism is different from
Page/HP recovery from a record that has already been produced.

## Horizon Direction

For horizons:

```text
public center:
    no-hair, thermodynamic, or conserved labels;

recorded-but-deep block:
    diary/microstate information that reaches radiation only after
    scrambling, Page/HP side information, or sufficient access depth;

noiseless commutant:
    degrees invisible to the passive exterior algebra unless the algebra
    is changed by mining, islands, boundary reconstruction, or
    gravitational dressing;

cut mobility:
    physically constrained by causal structure, allowed observer
    algebra, boundary conditions, and decoder complexity.
```

This is the sharper horizon/Heisenberg-cut disanalogy:

```text
Heisenberg cut:
    often chosen or moved by experimental design;

horizon cut:
    fixed by physical access constraints unless a real access
    enlargement or dressed reconstruction is supplied.
```

The horizon recovery law is correspondingly structured.  One cannot
simply re-choose the algebra to make the interior public; the access
change is a physical operation or a different gravitational/boundary
description.

## Unified Statement

The shared skeleton is:

```text
public center
+ recorded-but-deep block
+ noiseless/protected commutant
+ access-dependent transitions between them.
```

The value of the frame is not the vague statement that both measurement
and horizons have public and private information.  The value is the axes:

```text
cut chosen vs cut physically fixed;
recovery within a fixed cut vs moving the cut;
de-protection vs actual decodability;
transport/sampling latency vs nonlocal/dressed access.
```

## De-Protection Versus Decodability

The effective irreducibility rate `lambda` in the paper measures
de-protection:

```tex
\|\mathbb E_n(O)\|_2 \le C e^{-\lambda n},
```

where `E_n` projects onto the commutant of the record algebra generated
up to depth `n`.

Interpretation:

```text
lambda > 0:
    the exact noiseless/protected component is shrinking;

lambda = 0:
    a protected commutant remains under this access.
```

This is necessary for private information to become accessible through
the record algebra, but it is not sufficient for decoding.  Decodability
requires a separate recovery condition:

```text
Petz / complementary-channel recoverability;
Page/HP side information;
enough record depth;
allowed decoder complexity.
```

For horizons, the distinction is the scrambling-time versus Page-time
gap:

```text
scrambling can de-protect information quickly;
Page/HP conditions determine when it is actually recoverable.
```

## Technical Translation

The current theorem stack supports this frame as follows:

```text
cut theorem:
    redundant exact records can only make a commuting center public;

commutant theorem:
    exact protected private complement is the commutant/noiseless
    subsystem of the record-generating algebra;

latency theorem:
    source-local finite-velocity access cannot recover remote
    recorded-but-deep information before routing time;

frozen-dynamics diagnostic:
    recovery that survives frozen routing indicates nonlocal/dressed
    access or trivial diary-containing side information;

horizon-interface separation:
    horizon-like fast private recovery requires fast routing/scrambling
    or nonlocal/dressed access.
```

## Next Technical Target

The live quantitative target is two-stage:

```text
1. derive or bound lambda:
       the rate at which the protected commutant collapses;

2. combine lambda with a recovery theorem:
       the condition under which de-protected information is actually
       decodable from the allowed records and side information.
```

For ordinary measurement, `lambda` may be zero or apparatus-dependent
for the noiseless compartment.  For horizon-like scrambling, the target
is fast de-protection plus a separate Page/HP or dressed-access
recoverability condition.
