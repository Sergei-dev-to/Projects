# Cut sharpness toy model

Date: 2026-06-14

Status: exploratory calculation.  Purpose is to see whether the
quantum/classical cut can be assigned an order-of-magnitude access
number in a minimal public/private record channel.

## Question

Can we put a number on the transition from quantum-private to
classical-public?

Use the access profile:

```text
public label X:
    redundantly readable classical/pointer/no-hair data;

private block Q:
    noncommuting or microscopic information inside a fixed public
    sector;

one record R:
    a fragment of the environment/radiation/apparatus.
```

Define:

```text
xi:
    one-record distinguishability rate for public alternatives X;

gamma:
    one-record leakage rate for private alternatives Q at fixed X;

cut sharpness:
    S_cut = xi/gamma.
```

A sharp cut has `S_cut >> 1`, equivalently a broad window

```text
1/xi << m << 1/gamma
```

where public data are readable but private data remain hidden.
For a target error `delta`, replace `1/xi` by
`log(1/delta)/xi`, and similarly for `gamma`.  The estimates below use
independent identically distributed records and order-one thresholds.

## Minimal binary record model

Let each record be a binary outcome `r in {0,1}`.  Public alternatives
change the outcome bias by `a`; private alternatives change it by `b`.

Public alternatives:

```text
p(r=1|X=+) = 1/2 + a,
p(r=1|X=-) = 1/2 - a.
```

Private alternatives inside a fixed public sector:

```text
p(r=1|Q=+) = 1/2 + b,
p(r=1|Q=-) = 1/2 - b.
```

For two Bernoulli distributions `p` and `q`, the Chernoff information is

```tex
C(p,q)
=
-\log \min_{0\le s\le 1}
\left[
p^s q^{1-s}+(1-p)^s(1-q)^{1-s}
\right].
```

For the symmetric pair `1/2 +/- delta`, the minimum is at `s=1/2`, so

```tex
C(\delta)
=
-{1\over 2}\log(1-4\delta^2)
\simeq
2\delta^2
\qquad (\delta\ll 1).
```

Therefore

```tex
\xi
=
-{1\over 2}\log(1-4a^2),
\qquad
\gamma
=
-{1\over 2}\log(1-4b^2),
```

and

```tex
S_{\rm cut}
=
{\xi\over\gamma}
\simeq
\left({a\over b}\right)^2.
```

This is the first useful result: the cut sharpness is quadratic in the
ratio between public record strength and private leakage.

## Numbers

| public bias `a` | private leakage `b` | `xi` | `gamma` | `xi/gamma` | `m_public ~ 1/xi` | `m_private ~ 1/gamma` |
| --- | --- | --- | --- | --- | --- | --- |
| `0.05` | `0.005` | `5.0e-3` | `5.0e-5` | `1.0e2` | `2.0e2` | `2.0e4` |
| `0.1` | `0.001` | `2.0e-2` | `2.0e-6` | `1.0e4` | `4.9e1` | `5.0e5` |
| `0.1` | `0.0001` | `2.0e-2` | `2.0e-8` | `1.0e6` | `4.9e1` | `5.0e7` |
| `0.2` | `0.002` | `8.7e-2` | `8.0e-6` | `1.1e4` | `1.1e1` | `1.2e5` |
| `0.3` | `0.001` | `2.2e-1` | `2.0e-6` | `1.1e5` | `4.5` | `5.0e5` |
| `0.01` | `1.0e-6` | `2.0e-4` | `2.0e-12` | `1.0e8` | `5.0e3` | `5.0e11` |

Interpretation:

```text
m_public:
    records needed to read the public label at order-one confidence;

m_private:
    records needed before private leakage is order one;

S_cut:
    width of the public/classical but private/quantum window.
```

Even modest leakage suppression gives a large cut.  If public records
have ten percent bias while private leakage is one part in a thousand,
the public label is readable after about `50` records while private
information takes about `5e5` records to leak at order one.

## What this says

The toy model makes the cut quantitative:

```text
public record strength:
    how strongly each record distinguishes the center;

private leakage:
    how much each record distinguishes states inside a block;

transition sharpness:
    their Chernoff-rate ratio.
```

This is not yet a theory of which center is dynamically selected.  It is
a diagnostic once a candidate record channel and candidate public/private
split are specified.

It is also deliberately classical at the one-record level.  For a fully
quantum record fragment, replace the Bernoulli Chernoff information by
the quantum Chernoff information between fragment states.  The same
logic applies:

```text
xi:
    quantum Chernoff rate across public sectors;

gamma:
    quantum Chernoff or trace-distance leakage rate inside a sector.
```

## Why it may matter

For ordinary measurement:

```text
X:
    pointer position or detector outcome;

Q:
    phase/coherence/internal quantum data not locally recorded;

a:
    scattering distinguishability per photon/environment fragment;

b:
    unwanted leakage of incompatible private data into the same
    fragments.
```

For an ideal decoherence channel, local fragments record `X` and carry no
phase-sensitive private information, so `b=0` at this level and
`S_cut` is formally infinite.  Real systems have imperfections, finite
fragment overlap, and global correlations, giving small but nonzero
effective `b`.

For horizons:

```text
X:
    no-hair / thermodynamic bin;

Q:
    microstate or diary data inside the bin;

xi:
    distinguishability of Hawking/exterior records across no-hair bins;

gamma:
    early-fragment leakage about fixed-sector diary states.
```

In the ideal decoupling regime, `gamma` is exponentially or Page-suppressed
while `xi` for coarse no-hair bins is finite, so the cut is very sharp.

## Next calculation

The next nontrivial step is to replace the ad hoc biases `a,b` with a
dynamical model:

```text
pointer + photon/environment fragments:
    compute a from scattering overlap;
    compute b from residual phase-sensitive leakage;

or

finite public/private qubit model:
    simulate repeated weak measurement of X with a tunable parasitic
    coupling to Q, and measure xi/gamma directly.
```

The useful target is not a universal number.  It is a scaling law:

```text
S_cut ~ (public record strength / private leakage)^2
```

and a way to estimate the two rates in concrete physical record
channels.
