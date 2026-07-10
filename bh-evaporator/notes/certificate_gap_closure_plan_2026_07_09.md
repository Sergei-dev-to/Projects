# Certificate Gap-Closure Plan

Date: 2026-07-09

Status: superseded as an active plan on 2026-07-10. It remains the audit trail
for the passive certificate results and the tests that closed the static
source-rank branch. The successor direction is recorded in
`static_source_rank_certificate_tombstone.md`,
`finite_energy_parametric_pump_result.md`, and
`demarcation_synthesis.md`.

Closure verdict: no further passive generalization, tomography proposal, or
QNM specialization is on the critical path unless a reopening condition in
the tombstone is met. Microscopic source participation is model-side supplied
data. The live operational target is the temporal diary-visible orbit of the
physical active emission instrument, pursued through Q2.

## Decision Summary

### Historical north star: reduce the necessity trinity from three inputs to two

The operational-horizon draft starts from:

```text
INPUT 1: Schwarzschild state count, S(E) ~ E^2;
INPUT 2: entropy-sized boundary-accessible emission algebra,
         N_access ~ S;
INPUT 3: decoupling/typical encoding of the shrinking channel.
```

This closure program targeted INPUT 2 only. Its original best-case
result was to infer `N_access ~ S` from exterior luminosity, calibrated
response, and an independently measured or operator-specifically calculated
relaxation spectrum.  The invariance audit shows that exterior data cannot
identify an arbitrary microscopic decomposition of a shared jump operator.
The revised target must be either a canonical model-side boundary structure or
an invariant jump/process map and its temporal diary-visible orbit.  Input 1
remains parked.  Q2 sharpens necessary
conditions for input 3 but does not derive decoupling.  Algebraic
factorization and the lived interior are completion questions outside
this factorized necessity theorem, not additional members of the
trinity.

The next technical target at the time was not a universal proof of Planckian
dissipation. It is a frequency-resolved starvation theorem written in
terms of an operator-specific internal relaxation spectrum. The
Planckian/QNM statement should appear only as a black-hole corollary if
the relevant emission operator and retarded correlator justify it.

The historical work order after the Phase-2b red-team audit was:

```text
0. replace or qualify the non-invariant raw source-Gram target;
1. solve the active Gaussian/Bogoliubov route in a finite-energy dilation;
2. audit sample complexity, stationarity, and black-hole intervention scope;
3. repair the HIGH-sector bound and define global multi-time participation;
4. decide whether any feasible tomography controls the ordinary tail;
5. only then generalize passive two-drain separation and open the QNM gate;
6. revise and lock the boundary-saturation flagship;
7. elevate the Q2 latency companion if static identification remains blocked;
8. resume JT/Kerr/dS and phenomenology only after the core locks.
```

This sequence was designed so that a failed black-hole/QNM specialization did
not invalidate the general certificate. The general theorem will remain
parameterized by a measurable or calculable relaxation spectrum.

### Execution status (2026-07-09; branch closed 2026-07-10)

```text
Phase 0: complete.
Phase 1: complete for stationary linear gauge-invariant Gaussian
         channels with additive self-energies; see
         collective_channel_spectral_starvation_theorem.md.
Phase 2a: aggregate signed-cancellation no-go, conditional paired-leg
          Gram-tail bound, and exact plus finite-error two-drain separation
          theorems for the narrow stationary class landed.  The finite-error
          constants require a bounded starvation-ratio scan window.  A static
          ordinary-tail non-identifiability theorem also shows that
          aggregate KMS response plus g2=2 permits an arbitrary Gram
          spectrum; see
          signed_cancellation_and_gram_tail_result.md.
Phase 2b: red-team audit landed four further results:
          (i) the raw source-only Gram participation is not invariant under
          general interaction refactorizations;
          (ii) an anomalous active Gaussian channel exactly reproduces
          Hawking flux, positive absorption, KMS response, and g2=2 without
          passive starvation;
          (iii) full delay-resolved Gaussian correlations do not identify
          hidden source rank;
          (iv) eta~S^-1/2 precision costs O(S) events and therefore an
          order-one evaporation fraction on one black hole.
```

The July 10 finite-energy dilation completed the decisive active-channel test.
It can emit `O(S)` approximately thermal Hawking/partner pairs from a finite
pump while acting exactly as the identity on an arbitrarily large diary
factor. Its one-use effective process participation remains `O(1)` away from
depletion. Thus finite pump, partner, reset, and depletion accounting do not
rescue a static exterior rank inference. Together with the exact invariance,
non-identifiability, and finite-history results, this closes the branch rather
than merely reordering it. The QNM gate is closed because its intended target
is not exterior-identifiable in the required generality.

## Non-Negotiable Scope

1. Keep source participation and recovery latency separate.
2. Keep per-resolved-line participation distinct from broadband
   participation.
3. Do not identify a total linewidth with internal refill without an
   independent calibration of the radiative width.
4. Do not claim a universal Planckian bound for arbitrary many-body
   systems.
5. Do not make Q2 sufficiency load-bearing for the source-rank paper.
6. Do not open new toy-model families during this closure pass.
7. Treat coherent, nonstationary, and genuinely non-Gaussian refill as
   named exits unless a short exact classification falls out naturally.
8. State finite-accuracy results as participation floors, not full
   entropy-rank measurements unless the required `S` scaling is met.
9. Do not infer the sum of HIGH- and LOW-side bad fluxes from one net
   line ratio: signed deviations can cancel.
10. Audit the full ordinary Gram spectrum, not only its largest
    eigenvalue; a heavy top-`k` tail can keep rank subextensive.
11. Call the result an exterior certificate only when the required
    response kernel or eigenchannel information is operationally
    identifiable.  Otherwise call it a model-side inference.
12. Do not call the source-only `W_mu,nu` an interaction invariant under
    arbitrary refactorization.  Fix a canonical coupling metric or use the
    jump-map Choi spectrum.
13. Treat anomalous/squeezed Gaussian pair creation as a central Hawking-like
    route, not a peripheral non-Gaussian exit.
14. Cost every `eta ~ S^-1/2` claim at `O(S)` events and distinguish a
    one-black-hole protocol from an ensemble or model-side calculation.
15. Do not use aggregate `g2=2` as a HIGH-sector bound when hot Gaussian or
    superbunched cancellation channels are admitted.

## Dependency Graph

```text
definitions
  |
  v
single-channel spectral starvation
  |
  +--> Markovian calculation recovered as a check
  |
  v
Gram-eigenchannel multiplex optimization
  |
  +--> line-local participation theorem
  +--> weighted broadband direct-sum theorem
  |
  v
operator-specific black-hole/QNM gate
  |
  +--> success: black-hole corollary
  +--> failure: linewidth-parameterized theorem remains the endpoint
  |
  v
flagship paper lock

Q2 continuous-time latency theorem runs afterward as a separate companion.
```

## Phase 0: Freeze Definitions and the Theorem Target

### 0.1 Line-local source participation

For each resolved exterior frequency bin or wave packet `omega`, define
the positive source Gram matrix `W_omega` and

```text
N_eff(omega) = Tr(W_omega)^2 / Tr(W_omega^2).
```

All channel fractions used in the line theorem are Gram-eigenchannel
fractions of `W_omega`. Arbitrary microscopic source labels are not the
optimization variables.

### 0.2 Broadband participation

Mixed frequencies cannot be counted as channels of one resolved line.
If a broadband statement is needed, define it explicitly through a
weighted direct sum,

```text
W_B = direct_sum_{omega in B} w_omega W_omega,
N_eff(B) = Tr(W_B)^2 / Tr(W_B^2),
```

where the weights specify whether the count is number-flux,
energy-flux, or detector-response weighted. The band `B` must be a
finite detector-defined family of orthogonal wave packets with fixed
resolution; an arbitrary refinement of a continuum is not allowed to
manufacture participation. The theorem must never move between
`N_eff(omega)` and `N_eff(B)` without naming the packets and weights.

### 0.3 Response conventions

For each line, fix:

```text
R_omega       = calibrated microcanonical/grand-canonical ratio;
eta_+(omega)  = relative HIGH-side response allowance;
eta_-(omega)  = relative LOW-side response allowance;
n_ref(omega)  = R_omega/(1-R_omega), when 0 < R_omega < 1.
```

Superradiant/inverted channels require their own sign convention and
are not to be inserted into the positive-occupation formula silently.

### 0.4 Relaxation and drain widths

Define operator-specific spectral widths:

```text
Gamma_int(omega)  = internal thermal refill/relaxation width;
Gamma_out(omega)  = exterior radiative drain width;
Gamma_tot(omega)  = observed total width.
```

The additive relation

```text
Gamma_tot = Gamma_int + Gamma_out
```

is itself an assumption of independent additive self-energies. If it
holds, infer `Gamma_int` only after `Gamma_out` is independently fixed
from the exterior coupling, greybody response, or an input-output
calibration. If the split is not identifiable, leave the theorem in
terms of `Gamma_int`; do not substitute the total width.

### Phase-0 deliverable

Create `collective_channel_spectral_starvation_theorem.md` with the
definitions above and one fully quantified target statement before
starting the derivation.

### Phase-0 acceptance gate

Proceed only if the target statement makes clear:

```text
what is observed;
what is calibrated;
what is inferred;
what is assumed;
which participation number is bounded.
```

## Phase 1: Stationary Gaussian Spectral-Starvation Theorem

### Target class

A linear/quadratic, gauge-invariant bosonic collective eigenchannel
coupled to:

```text
an internal stationary Gaussian thermal environment;
an exterior vacuum radiation environment;
frequency-dependent retarded and Keldysh self-energies;
weak enough line overlap that a resolved spectral channel exists.
```

The internal state is thermal rather than squeezed, so the stationary
Gaussian channel has no anomalous covariance.  No flat-spectrum or
time-local Markov approximation should be assumed.  A nonlinear or
interacting collective operator lies outside the exact Gaussian theorem
unless its exact self-energies close the same relations.

### Target identity

Use fluctuation-dissipation/Keldysh relations to derive a frequency-
local effective distribution of the form

```text
n_eff(omega)
  = Gamma_int(omega) n_ref(omega)
    / [Gamma_int(omega) + Gamma_out(omega)],
```

or the correct spectral generalization if dispersive real parts or
overlapping support prevent this literal form. The corresponding
LOW-side response deficit should reduce to

```text
1 - r_eff/R_omega
  = x/[n_ref + 1 + x],
x = Gamma_out/Gamma_int,
```

in the narrow-line limit.

### Required checks

1. Recover the current Lindblad result exactly in the flat-spectrum
   limit.
2. Keep real self-energy shifts separate from dissipative widths.
3. Check positivity and the zero-drain/zero-refill limits.
4. State when a bound state, dark pole, or non-additive self-energy
   invalidates the line picture.
5. Show that passive Gaussian starvation leaves `g2 = 2` while moving the
   response ratio.

### Named exits

```text
anomalous/parametric drive:
  one-use exact calibrated route 2c landed; build the autonomous finite-energy
  repeated-interaction dilation and compute its process rank;

nonstationary refill:
  use a time-resolved rather than steady spectral certificate;

non-Gaussian refill:
  not closed generically; require higher cumulants or a new theorem;

bound/dark structures:
  classify as failure of the resolved dissipative-channel assumptions.
```

### Phase-1 acceptance gate

The result must be exact for the stated stationary Gaussian class and
must not use `Gamma_int <= c_P T`. That inequality belongs only to a
later corollary.

If a clean pointwise identity fails, fall back to an integrated
spectral inequality over the detector wave packet. Do not return to a
generic "non-Markovian corrections are O(1)" assertion.

## Phase 2: Unequal and Mixed-Frequency Multiplexing

### 2.1 Same-line eigenchannels

For Gram eigenchannels `i` in one resolved line, introduce

```text
f_i, Gamma_int,i, Gamma_out,i, eta_i,
f_i = lambda_i/Tr(W_omega),
sum_i f_i = 1.
```

Any collective or otherwise exceptional subset carries line-flux
fraction `F_sub = sum_{i in sub} f_i`; do not use unnormalized fluxes in
the participation denominator.

Derive a channelwise response/flux cap from Phase 1, then solve the
adversarial problem

```text
minimize    N_eff(omega) = 1/sum_i f_i^2
subject to  calibrated response bounds,
            the observed aggregate line ratio,
            adversarial HIGH/LOW signed cancellation,
            total line flux,
            linewidth/resolution constraints,
            known greybody/input-output data.
```

The desired theorem replaces the current equal-split `m` factor by an
effective participation inequality.  It must optimize the full ordered
Gram spectrum, including a possible heavy top-`k` ordinary tail, rather
than assume that all nonexceptional channels are comparable.  If hiding
the deficit requires many individually dim channels, that multiplicity
must itself earn the rank floor.

### 2.2 Signed-cancellation gate

The aggregate response is absorption-weighted:

```text
r_tot = sum_i Gamma_abs,i r_i / sum_i Gamma_abs,i.
```

Occupation-enhanced channels lie above the reference and starved
collective channels lie below it, so a small net deviation does not by
itself bound `f_occ + f_coll`.  Test, in order:

```text
channel/linewidth-resolved response;
two drain strengths, exploiting the Gamma_out dependence of starvation;
time-resolved drain switching;
the paired g2 statistic;
two detector resolutions;
response-kernel tomography.
```

The theorem may use separate `eta_+` and `eta_-` only after one of these
protocols operationally separates the signed components.  Otherwise
the optimizer must allow exact cancellation and report the weaker bound.

### 2.3 Mixed frequencies

Apply the line theorem independently to each resolvable bin. Combine
bins only through `W_B` with declared weights. Include:

```text
low-frequency packing;
high-frequency Boltzmann suppression;
overlapping linewidths;
unresolved detector bins;
number-flux versus energy-flux weighting.
```

The low-frequency argument must use both flux and resolvability. Do not
count overdamped structures as independent resolved lines.

### Support calculation

Add an adversarial optimization script, provisionally
`sim/multiplexed_starvation_optimizer.py`, that:

```text
reproduces the analytic extremizer;
samples unequal flux and width distributions;
tests low-frequency and broad-line corners;
reports the weakest participation floor consistent with all constraints.
```

The script supports the theorem; it does not replace the proof.

### Phase-2 acceptance gate

Every construction in scope must land in one of three outcomes:

```text
detectable response deviation;
failure of line resolution/channel assumptions;
quantitative source-participation floor.
```

The acceptance gate also requires one of:

```text
signed cancellation is closed by a specified protocol;
or the theorem explicitly reports the cancellation-allowed floor.
```

Separately report whether entropy-sized rank follows from observables or
still uses an ordinary-sector ETH/smooth-envelope tail assumption.

If overlapping frequencies cannot be reduced to a direct-sum or
wave-packet Gram problem, state that scope boundary rather than quoting
a broadband rank theorem.

## Phase 3: Operator-Specific Black-Hole/QNM Gate

### Input hierarchy

Keep three evidentiary levels separate:

```text
Level A — theorem:
  measured or calculated Gamma_int(omega);

Level B — black-hole corollary:
  operator-specific QNM/retarded-correlator control of Gamma_int;

Level C — motivation only:
  generic Planckian-dissipation conjecture.
```

### Required work

1. Identify the semiclassical or microscopic operator corresponding to
   the proposed collective emission eigenchannel.
2. Identify its retarded correlator and the spectral feature that
   measures internal refill rather than exterior escape.
3. Determine whether relevant poles and cuts imply
   `Gamma_int(omega ~ T) = O(T)`.
4. Check whether the operator has overlap with a parametrically faster
   sector not represented by the lowest QNM.
5. Explain how `Gamma_out` is separated from the total damping rate.

### Go/no-go gate

Promote the Planckian/QNM closure to a black-hole corollary only if an
explicit operator-to-correlator chain supports it. A statement that the
lowest black-hole QNM is `O(T)` is motivation, not by itself an upper
bound on every microscopic collective refill channel.

If this gate fails:

```text
retain the Gamma_int-parameterized theorem;
state the QNM estimate as an application hypothesis;
do not claim that real black holes are certificate-closed.
```

That outcome is acceptable and still leaves a useful operational
theorem: a measured relaxation spectrum decides whether a rank-one
thermal collective channel can carry the observed flux.

## Phase 4: Flagship Paper Lock

Revise `paper_boundary_saturation/main.tex` around three nested claims:

```text
1. exact observable floor:
   N_eff >= 1/f_max;

2. spectral-starvation theorem:
   response + calibrated Gamma_int/Gamma_out bounds collective flux;

3. optional black-hole corollary:
   operator-specific QNM control implies a thermal-scale refill ceiling.
```

### Finite-accuracy presentation

State the scaling consequence explicitly:

```text
eta ~ S^(-alpha)
  => N_eff >= S^(min(1,2 alpha))
```

up to the frequency, refill, and ordinary-sector constants in the
formal theorem, and only when those prefactors remain `O(1)` in `S`.
At fixed `eta`, advertise a quantitative floor, not full entropy-rank
certification.

### Paper acceptance gate

Before locking:

1. Every theorem statement has one dependency list.
2. Line-local and broadband ranks are never conflated.
3. Static, spectral, and black-hole-corollary claims are visibly nested.
4. QNM and Planckian language follows the Level A/B/C hierarchy.
5. The strict memory-burden result remains fork-not-refutation.
6. The paper builds without undefined references or substantive layout
   warnings.
7. The active roadmap and theorem notes match the paper.

## Phase 5: Q2 Latency Companion

This phase is independent of the source-rank theorem.

### Necessary side

Extend the generator-defect result to a continuous-time or persistent-
record formulation. State a bound of the form

```text
small integrated distance from a diary-blind interaction algebra
  => emitted record channel is diamond-close to diary-independent
  => no decoder obtains order-one diary recovery.
```

The strict memory-burden prototype remains the exact zero-defect case.
For bosonic persistent records, either impose an explicit energy/Fock
cutoff or use an energy-constrained channel norm; do not quote an
unconstrained finite-dimensional diamond bound for an unbounded mode.

### Sufficient side

State separately:

```text
order-one access to the coupled algebra
+ explicit moment-gap/decoupling hypothesis
  => recoverability after the stated record budget.
```

Large access is necessary, not sufficient. Do not let the positive
random-circuit/expander witness become a claim about a real horizon.

### Persistent-channel test

Apply the continuous-time theorem to the bright collective emitter,
which is not naturally a fresh-ancilla channel. Determine whether it
falls inside the bounded-interaction comparison class or requires a
separate dilation statement.

### Phase-5 acceptance gate

The companion must distinguish:

```text
arrival in the accessible record;
information-theoretic decodability;
computational decoding complexity.
```

Only the first two belong to Q2's theorem stack.

## Phase 6: Deferred Stress Tests and Applications

Historical deferral list at the time of the certificate plan:

```text
near-extremal/JT greybody and Schwarzian verification;
Kerr/RN grand-canonical and superradiant calibration;
de Sitter no-asymptotic-line contrast;
tabletop refill/response protocol;
PBH late-stage signatures;
decoder-complexity fourth rung;
degeneracy-to-access crossover D2.
```

These remain applications or new programs, but the condition tied to locking a
static flagship no longer applies because that branch is closed.

## Risk Register

### R1. Total linewidth does not identify refill

Mitigation: independently calibrate `Gamma_out`; otherwise leave the
theorem parameterized by `Gamma_int`.

### R2. QNMs do not bound the relevant microscopic operator

Mitigation: require the operator-specific retarded-correlator chain.
Failure means no black-hole corollary, not failure of the general
theorem.

### R3. Channel basis ambiguity

Mitigation: optimize only in the Gram eigenbasis at fixed frequency.

### R4. Mixed frequencies are counted as one line

Mitigation: prove linewise statements and use a declared weighted
direct sum for broadband participation.

### R5. Finite precision is oversold

Mitigation: quote the floor or exponent `min(1,2 alpha)`; reserve
`N_eff ~ S` for the required accuracy scaling.

### R6. Non-Gaussian refill expands without bound

Mitigation: record it as a named exit and test only immediately visible
coherence/cumulant consequences during the core pass.

### R7. The flagship absorbs the latency program

Mitigation: keep Q2 in a separate companion and cite only the logical
separation in the source-rank paper.

### R8. Broadband rank depends on arbitrary binning

Mitigation: define a finite detector wave-packet family before forming
`W_B`; report its resolution and weights as part of the observable.

### R9. Persistent bosonic channels invalidate finite-dimensional norms

Mitigation: use a stated Fock/energy cutoff or an energy-constrained
diamond norm in the Q2 extension.

### R10. HIGH- and LOW-side defects cancel in aggregate

Mitigation: include signed cancellation in the adversarial optimizer and
require drain, time, resolution, `g2`, or tomography data before quoting
separate bad-flux bounds.

### R11. The ordinary sector has a heavy top-k tail

Mitigation: optimize cumulative sorted Gram weight/Lorenz curves.  If
exterior data do not control the tail, retain the ordinary-sector smooth
envelope as an explicit remnant of input 2.

## Immediate Work Packet

The next work session should do only this:

1. Replace the raw source-list Gram quantity by a canonical coupling-weighted
   jump/process invariant, or explicitly demote it to a model-side quantity.
2. Build the finite-energy repeated-interaction version of anomalous route 2c
   and compute its global process rank, partner/reset cost, and pump drift.
3. Repair the HIGH-sector theorem without assuming all HIGH channels are
   antibunched or all positive fourth cumulants vanish.
4. Cost response, delay-correlation, and tomography protocols in settings,
   events, and fractional mass drift.
5. Test an honest finite-S ETH model for completeness at the required
   calibration scaling.
6. Decide whether any exterior protocol bounds the operational target; if
   not, lock microscopic boundary saturation as a structural input and move
   the exterior theorem emphasis to latency.
7. Stop for review before opening the black-hole/QNM literature gate.

No literature expansion, new phenomenology, or additional toy models
belongs in that packet.

## Completion Criteria for the Gap-Closure Program

The closure pass is complete when:

```text
the passive stationary Gaussian spectral theorem is proved;
the anomalous active Gaussian route has a finite-energy yes/no outcome;
the participation target is invariant under physical interaction
  refactorization or explicitly labeled model-side;
the protocol sample budget is compatible with its stationarity claim or
  explicitly labeled ensemble/model-side;
unequal same-line multiplexing has an analytic participation bound;
mixed-frequency scope is defined by a weighted direct-sum theorem or
  an explicit boundary;
the black-hole/QNM gate has a documented yes/no outcome;
the flagship paper reflects that outcome and is internally consistent;
the Q2 necessary theorem covers persistent records or states why not.
```

Anything beyond this list is follow-on work, not a reason to delay the
certificate result.
