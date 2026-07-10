# Delay-Resolved Gaussian Correlations Do Not Identify Source Rank

Date: 2026-07-09

Status: exact non-identifiability theorem plus numerical support.

## Result in One Line

For a zero-mean circular Gaussian output field, fixing the aggregate power
spectrum fixes `g1(tau)`, `g2(tau)`, and every Gaussian field moment, while the
spectrum can be decomposed into independent source contributions with an
arbitrary participation ratio.  Therefore delay-resolved photon bunching is a
useful linewidth diagnostic but not a source-rank certificate without an
additional per-source flux/linewidth constraint.

## 1. Gaussian Output Field

Let the detected stationary field be

```text
A(t) = sum_i A_i(t),
```

where the `A_i` are independent, zero-mean, circular Gaussian source fields.
Let their power spectra be `S_i(omega) >= 0`.  The aggregate spectrum is

```text
S_A(omega) = sum_i S_i(omega).                             (1.1)
```

The normalized first-order coherence is

```text
g1(tau)
  = integral d omega S_A(omega) exp(-i omega tau)
    / integral d omega S_A(omega).                         (1.2)
```

For a circular Gaussian field, Wick's theorem gives the Siegert identity

```text
g2(tau)-1 = |g1(tau)|^2.                                  (1.3)
```

Thus `g2(tau)` depends only on the aggregate spectrum (1.1), not on its source
decomposition.

## 2. Arbitrary-Rank Decomposition [exact]

Choose any normalized nonnegative spectrum `S(omega)` and any probability
vector `{f_i}`.  Define independent Gaussian source fields by

```text
S_i(omega) = f_i S(omega),
sum_i f_i = 1.                                             (2.1)
```

Every such decomposition has the same aggregate spectrum,

```text
sum_i S_i(omega) = S(omega),                               (2.2)
```

and therefore exactly the same:

```text
mean flux;
g1(tau) for every delay;
g2(tau) for every delay;
all higher moments determined by Gaussian Wick contractions;
all passive measurements on the aggregate Gaussian output state.
```

But its source-weight participation is

```text
N_eff = 1/sum_i f_i^2,                                    (2.3)
```

which can be one, subextensive, or arbitrarily large.

**Theorem.**  No measurement determined solely by the aggregate stationary
Gaussian output state can identify the decomposition participation (2.3).

This strengthens the static ordinary-tail theorem: adding the complete delay
dependence of Gaussian intensity correlations does not remove the
non-identifiability.

## 3. Why a Long Coherence Tail Is Not Automatically Rank

A long bunching time shows that some aggregate spectral weight is narrow.  It
does not say how many independent internal sources produced that weight.

The proposed inference

```text
rank-many emission -> per-source radiative width ~ T/S
                  -> g2(tau)-1 persists to tau ~ S/T
```

requires each source's total linewidth to be tied to its radiative flux.  In
the spectral-starvation notation,

```text
Gamma_tot = Gamma_int+Gamma_out.
```

An honest weakly outcoupled channel can have

```text
Gamma_out ~ T/S,
Gamma_int ~ T,
```

and hence coherence time `O(1/T)`, not `O(S/T)`.  Conversely, one weak narrow
source can have a long coherence tail.  Delay persistence becomes a
participation bound only after adding a source-resolved width law or another
envelope assumption.

## 4. What Delay Correlations Are Still Good For

`g2(tau)` remains a valuable passive diagnostic for:

```text
aggregate linewidth distributions;
unresolved narrow spectral tails;
beating between sub-lines;
nonstationarity and coherence revivals;
violations of circular Gaussian statistics.
```

It can tighten a model-side certificate once the source-to-linewidth map is
fixed.  It cannot replace that map.

Anomalous Gaussian route 2c may also require measuring phase-sensitive
correlations or partner cross-correlations.  Aggregate `g2(tau)` alone traces
over precisely the information that distinguishes a purified squeezed source
from a thermal environment.

## 5. Verification

`sim/delay_correlation_rank_no_go.py` constructs rank-one and high-rank
decompositions with the same non-Lorentzian spectrum and verifies identical
`g1(tau)` and `g2(tau)` to numerical precision while their participation ratios
differ parametrically.

## Consequence for the Plan

Do not promote delay-resolved bunching to a replacement for the ordinary-tail
envelope.  Use it as a low-cost spectroscopy leg and as a test for assumptions
entering a stronger source-resolved theorem.

## Discipline

- Output spectral rank is not internal source rank.
- A coherence time is not a channel count without a flux/width law.
- Gaussian output tomography cannot reveal an arbitrary hidden Gaussian
  source decomposition.
- State explicitly which non-Gaussian or cross-channel observable would break
  the equivalence class (2.1).
