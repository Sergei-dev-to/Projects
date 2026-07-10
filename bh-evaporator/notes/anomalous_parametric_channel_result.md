# Anomalous Parametric Channel: Route 2c

Date: 2026-07-09

Status: exact one-use Gaussian-channel countermodel to passive starvation,
with the finite-system/global source-rank question left explicit.

## Result in One Line

A phase-insensitive active Gaussian channel can simultaneously have positive
net absorption, Hawking-strength spontaneous emission, the exact calibrated
emission/absorption ratio, and thermal `g2=2`, without a populated collective
mode that becomes reservoir-starved.  Therefore the passive additive
starvation theorem does not cover the Gaussian mechanism most closely
analogous to Bogoliubov pair creation.

This is a counterexample to extending the passive starvation conclusion to all
Gaussian channels.  It is not yet a proof that a finite black hole realizes
low global source rank: the pump and fresh partner modes must be included in
that accounting.

## 1. General Active One-Output Channel

Let `a_in` be the exterior probe input, `c` a loss/absorption port, and `b` an
idler/partner port.  Take all three inputs independent and in vacuum.  A
phase-insensitive Gaussian input-output relation is

```text
a_out = r a_in + l c + g b^dagger.                         (1.1)
```

Canonical commutation requires

```text
|r|^2 + |l|^2 - |g|^2 = 1.                                (1.2)
```

The anomalous coefficient `g` is the pair-creation leg excluded by the
gauge-invariant starvation theorem.

Define the net absorptivity

```text
gamma = 1-|r|^2 > 0.                                      (1.3)
```

Equation (1.2) then gives

```text
|l|^2 = gamma+|g|^2.                                      (1.4)
```

For vacuum inputs, the spontaneous outgoing occupation is

```text
E = <a_out^dagger a_out> = |g|^2.                          (1.5)
```

The anti-normal absorption-side coefficient is

```text
B = |l|^2 = gamma+E.                                      (1.6)
```

The net absorption is `B-E=gamma`, as required by the input-output response.

## 2. Exact Hawking/KMS Calibration

At inverse temperature `beta`, let

```text
n_beta = 1/(exp(beta omega)-1),
R = exp(-beta omega) = n_beta/(n_beta+1).                  (2.1)
```

Choose

```text
|r|^2 = 1-gamma,
|g|^2 = gamma n_beta,
|l|^2 = gamma(n_beta+1).                                  (2.2)
```

The commutator identity (1.2) holds exactly.  The spontaneous flux has the
greybody Hawking form

```text
E = gamma/(exp(beta omega)-1),                             (2.3)
```

and the microscopic line ratio is

```text
E/B = n_beta/(n_beta+1) = R.                              (2.4)
```

Thus the channel has all of the following simultaneously:

```text
positive net absorption gamma;
Hawking spontaneous flux gamma n_beta;
exact calibrated detailed balance E/B=R;
no HIGH- or LOW-side response defect.
```

This is the standard thermal attenuator written in a purified active dilation:
the effective thermal environment can be represented by Bogoliubov-mixed
vacuum loss and partner ports.

## 3. Counting Statistics

With vacuum inputs,

```text
<a_out a_out> = 0,
<a_out^dagger a_out> = gamma n_beta.
```

The one-mode reduced state is zero-mean, circular Gaussian.  Wick's theorem
therefore gives

```text
g2(0) = 2.                                                (3.1)
```

The channel passes both aggregate response and thermal photon-counting tests.
It is not a HIGH/LOW cancellation: each active channel is individually
calibrated.

## 4. Why Passive Starvation Does Not Apply

The passive theorem has an occupation obeying

```text
n_eff = Gamma_int n_ref/(Gamma_int+Gamma_out),
```

because emission drains a number-conserving collective mode that must be
refilled.  Equation (1.1) instead creates an exterior quantum together with a
partner, powered by the pump/background.  There is no pre-existing `b`
occupation whose depletion forces a LOW-side deficit.

The energy source is hidden in the coefficients of the active transformation.
In an autonomous finite model those coefficients must arise from a pump
operator that lowers the black-hole energy.  Pump depletion changes the
coefficients over the evaporation time, but a macroscopic pump can remain
locally stationary over a modest observation window without a passive
starvation signature.

## 5. What This Does and Does Not Establish About Rank

For one use of the channel, equations (1.1)--(2.4) require only `O(1)` Gaussian
ports.  That is enough to defeat any claim that calibrated Gaussian statics
alone imply entropy-sized instantaneous source rank.

It does **not** yet establish a rank-one global finite-black-hole model.  A
stationary field channel uses fresh partner wave packets at successive times.
An autonomous realization must account for:

```text
the pump operator and its finite energy;
the partner/idler modes and where they go;
fresh-environment requirements across repeated uses;
the representation-invariant jump/process rank;
energy conservation and pump depletion;
whether partner modes themselves supply an entropy-sized accessible orbit.
```

A classical-pump approximation can hide this global accounting.  The correct
next object is a finite-energy repeated-interaction dilation and its invariant
jump/process Choi spectrum, not the number of symbols in equation (1.1).

## 6. Consequence for the Certificate

The current channel taxonomy needs a third enhanced route:

```text
route 2a: occupation enhanced, passive        -> HIGH response;
route 2b: collective coupling, passive drain  -> LOW starvation response;
route 2c: anomalous/parametric pair creation   -> exactly calibrated active channel.
```

Routes 2a and 2b can be separated by resolved or multi-setting response under
their stated assumptions.  Route 2c is not bounded by that monotonicity
theorem, because changing the exterior boundary can change both attenuation
and gain coefficients and can return partner/probe noise.

Therefore the source-rank flagship must do one of the following:

1. Restrict its theorem explicitly to passive number-conserving emission
   channels and stop identifying that class with the full Hawking mechanism.
2. Derive an active-channel rank/depletion theorem.
3. Use an anomalous-response observable, partner correlation, or temporal
   process test that separates low-rank active pumping from a finite black-hole
   emission map.

## 7. Immediate Active-Channel Calculation Owed

Construct an autonomous finite-energy dilation

```text
H_pair ~ P a^dagger b^dagger + P^dagger a b,
```

where `P` lowers the pump/black-hole energy.  Compute:

```text
the emission and probe-response instrument;
the invariant jump/process Choi spectrum;
partner-mode accumulation or reset cost;
finite-pump drift over N emissions;
whether the emitted record becomes diary-visible.
```

This calculation now precedes the full spectral generalization of the passive
two-drain theorem.

## 8. Verification

`sim/active_gaussian_route_check.py` checks equations (1.2)--(2.4) over a
frequency-dependent greybody profile and verifies the thermal Gaussian
moments.  It is a support calculation; the countermodel is analytic.

## Discipline

- Say “passive stationary Gaussian starvation theorem,” not “Gaussian
  starvation theorem,” when anomalous self-energies are relevant.
- Do not equate a classical pump coefficient with a finite-system source
  operator.
- Do not count fresh partner wave packets as free.
- Keep one-use channel rank separate from global process accessibility.
- Treat exact calibration of route 2c as a counterexample to the observable
  implication, not as proof that real black holes have low source rank.
