# Frozen-Routing M1-M3 Working Note

Date: 2026-07-02

Role: executes milestones M1-M3 of `frozen_routing_platform_proposal.md`.

Status: working note through M5 first full-text pass.  Early M1-M3
hardware numbers retain `[pin]` markers as provenance flags; M5
supersedes them where full-text values are quoted.  Remaining proposal
flags are listed at the end.

## M1: Platform Decision and Control Split

Decision: superconducting transmons with tunable couplers.

Against Rydberg (the runner-up): coupler switching is ns-scale and
per-edge, the four-arm protocol needs fast cycling, and the
Yoshida-Kitaev decoder needs full two-sided circuit control.  Rydberg
freezing is geometrically cleaner (retract the atoms), so it stays the
backup if freezing certification on couplers is contested.

### The integrability trap (design correction to the plan)

The plan's protocol skeleton said "switch off routing couplers."  Taken
literally as always-on XY hopping, that is wrong twice over: an XY
chain is free-fermionic, hence integrable, hence not a scrambler at
all — the normal arm would test transport of a free excitation, not
scrambling-mediated access.  The routing dynamics must be
nonintegrable.

Resolution: define the dynamics at the circuit level, not the
Hamiltonian level.

```text
dynamics U(t):   brickwork random circuit; two-qubit CZ/iSWAP-family
                 gates from coupler pulses, interleaved random
                 single-qubit layers.

routing terms:   the two-qubit coupler pulses on bulk edges.

record terms:    the two-qubit pulses on the fixed access edge(s) to
                 the record ancillas, plus their readout.  Identical
                 pulse sequence in every arm.

frozen arm:      the identical schedule with bulk coupler pulses
                 replaced by identity (couplers parked at the off
                 point).  Single-qubit layers are RETAINED, so local
                 fields and frame rotations are not confounded; only
                 transport is removed.  Wall-clock identical by
                 construction.
```

Circuit-level freezing is cleaner than Hamiltonian freezing: "what is
frozen" is a well-defined subset of the pulse schedule, which answers
the qi-note's own worry ("requires a clean definition of what is
frozen") and makes confound 3 (record-coupling drift) directly
measurable by interleaved RB on the access edge in both coupler
configurations.

### Freezing certification (the independent v, L handle)

Two certificates are needed, because the frozen arm can fail in two
distinct ways.

Certificate 1 (transport): with couplers parked, prepare an
excitation at the diary site and measure arrival probability at the
access region over the full protocol duration.  This bounds actual
transport in the frozen arm from data, not calibration, and
simultaneously supplies the independent handle on (v, L) that the qi
note's falsifiability caveat demands: the same measurement with
couplers on yields the light-cone velocity for the latency-envelope
companion measurement.

Certificate 2 (operator spreading): the single-excitation test is
blind to interactions that grow operator support without moving
excitations — residual ZZ crosstalk is the specific mechanism
[pin: residual ZZ at the coupler off point].  Under the frozen
schedule, prepare the diary site in |+>, run the full schedule, and
measure decay of <X_diary> together with diary-neighbor two-point
correlators (or a two-site OTOC-style echo on the diary edge).  This
bounds many-body spreading, not just transport.  Both certificates
go into the frozen-arm systematic envelope.

## M2: Minimal Instance

### The two-copy requirement (second correction to the plan)

The plan budgeted a single chain.  But HP recovery needs the
"old black hole" resource: the scrambler in a maximally entangled
state with side information E.  The standard lab realization
(Landsman et al. ion experiment) is the two-copy teleportation-based
YK protocol, U on one copy and U* on the other, with EPR pairs across
copies.  Budget therefore doubles:

```text
diary D:          1 qubit (k=1; F_triv^e = 1/4)
reference A:      1 qubit, held with dynamical decoupling
                  (fallback: randomized-measurement estimation of
                  F_rec^e to avoid idling A)
routing bulk:     L = 8 sites per copy, 1D chain first
records:          m = 2-3 sequential swaps from the access site into
                  ancillas ("emission" at scheduled depths)
copies:           2 (U and U*)
total:            ~20 qubits.  Qubit count is not the constraint;
                  coherent two-copy depth at fidelity is (gate
                  budget below).
```

### U / U* compilation and calibration (budgeted, not free)

The conjugate copy is not schedule reuse; U* requires conjugating
every gate in a fixed basis.  Single-qubit layers conjugate in
software (negate the Y components — exact and free).  The two-qubit
choice decides the cost: CZ is real, hence self-conjugate, so a
CZ-based brickwork makes U* compilation nearly free.  This is the
reason to prefer CZ over iSWAP-family gates, whose conjugate is a
separately calibrated pulse.  Explicit budget items:

```text
a. calibration surface doubles: the same CZ calibrated per edge on
   both copies.
b. cross-copy EPR preparation + final Bell measurement between
   copies: ~L extra two-qubit operations plus correlated readout.
c. conjugation mismatch: software conjugation conjugates the ideal
   gate, not its coherent error, so U*_implemented differs from
   (U_implemented)*.  The mismatch enters the YK decoder as an
   effective epsilon; bound it by cross-copy cycle benchmarking.
```

Net: add ~10-20% to the two-qubit gate budget for (b) plus
calibration overhead, and one dedicated characterization run for (c).

k=1 keeps the probabilistic YK decoder cheap: post-selection overhead
~ d_D^2 = 4 (the Grover-assisted variant is unnecessary at this size).

### Depth and duration

Recovery onset for a 1D chain sits at depth ~ L, so depth 16-24
brickwork layers suffices for onset plus margin.  Per layer ~ 30 ns
CZ + 25 ns single-qubit `[pin]`:

```text
wall-clock per run:  ~1.5-2 us  <<  T1, T2echo ~ 100+ us  [pin]
```

### Gate budget (the tight constraint)

```text
2q gates: ~7 edges x ~20 layers x 2 copies / 2 (brickwork)  ~ 140-280
at 99.5% 2q fidelity [pin]:  raw circuit fidelity  ~ exp(-1.4..-0.7)
                             ~ 25-50%.
```

Marginal but in line with executed scrambling experiments; requires
standard error mitigation for the fidelity estimates.  This, not
qubit count or coherence, is the binding constraint; it argues for
L = 6 as the first instance (onset ~ depth 12, budget halves).

## M3: Confound and Error Envelopes

Numbering follows the plan's confound list.

```text
1. idle loss (frozen arm):
       bulk sites idle ~1.5 us during skipped pulses.  With echo/DD,
       loss ~ 1-(exp(-tau/T2echo)) ~ 1.5-5%  [pin].
       Measured directly by arm 4 (frozen routing, no record
       coupling).  Envelope: eps_idle ~ 0.05.

2. residual coupling at the off point:
       g_off/2pi ~ 10-100 kHz on published couplers (on/off ratios up
       to ~40 dB) [pin].  Nearest-neighbor leakage over tau:
       (g_off tau)^2 ~ up to few % at the pessimistic end — but this
       leakage does not reach the access region: transport across
       L-1 frozen edges is suppressed as (g_off tau)^{2(L-1)},
       i.e. negligible at L >= 6.  The certification measurement
       bounds it from data regardless.  Envelope: eps_res < 1% on
       records.

3. record-coupling drift:
       interleaved RB on the access edge, couplers parked vs active.
       Require |Delta F_gate| < 0.5%; else recalibrate.  Envelope:
       eps_rec ~ 0.005.

4. decoder mismatch:
       report both same-decoder and best-decoder-per-arm numbers.
       For the frozen arm the best decoder is trivial ("read the
       access region"), and its ceiling is set by the certified
       transport bound — so confound 4 folds into envelope 2.

5. statistics:
       F_rec^e via two-qubit tomography on (A, Dhat) or direct
       fidelity estimation: ~10^3 shots per point; eps_stat ~ 0.01-
       0.02.  Negligible against systematics.
```

### Witness inequality (confidence-bound form)

```text
witness routing-mediated access at level alpha if

LCB_alpha[ F_rec^e(normal, t) ]
    >
max[ UCB_alpha[ F_rec^e(frozen, best decoder) ],
     1/4 ]
    + eps_idle + eps_res + eps_rec
```

Statistical uncertainty lives inside the confidence bounds
(LCB/UCB at level alpha); the systematic envelopes are added to the
frozen side, so every unmodeled effect works against the claim.
eps_res here is the certified bound from Certificates 1 and 2, not
the calibration value.

### Margin estimate (paper viability gate)

```text
frozen-arm ceiling:   1/4 + ~0.07  ~ 0.32
normal-arm target:    mitigated F_rec^e ~ 0.5-0.7 past onset
                      (raw circuit fidelity 25-50% is the risk item)
margin:               ~0.2-0.4.  The gate PASSES on paper at L = 6-8.
```

The kill criterion from the plan (idle loss swamps signal) is not
triggered: idle loss enters at the 5% level against a >20% margin.
The genuine risk is the normal arm's own fidelity under the gate
budget, which is a mitigation problem, not a confound problem.

## M4: Pinning Pass (2026-07-02, first web pass)

Historical search-pass estimates, kept for provenance.  M5 below
supersedes these values where full-text checks are available.

```text
2q gate error:    ~0.33% mean (Google Willow, Nature 638, 2025 "QEC below
                  the surface code threshold"); CZ > 99.8% on
                  long-distance tunable couplers (PRX Quantum 4,
                  010314, 2023).  Pins the 99.5% budget assumption as
                  conservative.

T1:               ~68-100 us mean (Willow).  Pins the coherence
                  assumption.  T2echo still [pin] — infer T1-limited
                  for now.

residual ZZ off:  < 5 kHz, down to 2pi x 6.3 kHz idle-point values;
                  ZZ on/off ratios up to ~10^4 reported.  Over the
                  ~1.5 us protocol: phase ~ 0.05 rad at the diary
                  edge => Certificate-2 systematic ~ 10^-3 level.
                  MAJOR REVISION: eps_res drops from ~1% to ~0.1%;
                  the frozen-arm ceiling tightens from ~0.32 to
                  ~0.31, dominated by idle loss and record drift.
```

### L decision

At 0.33% 2q error:

```text
L=6: ~85 2q gates incl. U/U* overhead  => raw fidelity ~ 0.75
L=8: ~160-300 gates                    => raw fidelity ~ 0.40-0.60
```

Decision: L=6 first instance (5 routing edges per copy, depth ~12-14,
onset comfortably inside budget); L=8 as the stretch instance with
error mitigation.  L=6 keeps the normal-arm raw fidelity high enough
that the witness margin survives even without mitigation.

### Prior-art sweep result

No published scrambling experiment with a transport-frozen control arm
was located in this first pass.  Existing controls are of two kinds:
teleportation-fidelity verification against decoherence (Landsman et
al. Nature 2019, ion YK; Blok et al. PRX 11, 021010, 2021,
superconducting-qutrit YK-style decoding) and circuit-class comparisons
(Google, Mi et al., "Information scrambling in computationally complex
quantum circuits"; Zhu et al. arXiv:2112.11204, fully controllable
superconducting simulator).  This pass found no control separating
dynamical transport from prearranged/dressed access.  The transport-
frozen control arm remains the candidate contribution.  Blok et al. is
the closest hardware lineage and the right citation anchor for the
decoder half of the protocol.

## M5 Part 1: Verified Pinning (2026-07-02, full-text pass)

Read against the papers (arXiv full text), superseding the M4 search
values:

```text
Willow (arXiv:2408.13687, Nature 638, 2025):
    T1 = 68 us mean, T2,CPMG = 89 us mean (105-qubit processor).
    CZ error: main text gives only the Fig. 1b distribution; the
    ~0.33% mean is from secondary sources.  RESIDUAL FLAG: confirm
    the SI value before the proposal draft cites it.

IQM long-distance coupler (arXiv:2208.09460, PRX Quantum 4, 010314):
    CZ fidelity 99.81 +/- 0.02% (error 1.9e-3), duration 33 ns.
    Residual ZZ at coupler idle point: |zeta| < 2 kHz.  VERIFIED —
    better than the M4 search value (<5 kHz).
    1q errors ~7e-4.  Caveat: effective T1 during gate operation on
    that device was 14/43 us — device-dependent; do not mix with
    Willow coherence in one budget.

Blok et al. (arXiv:2003.03307, PRX 11, 021010):
    5 qutrits, YK-style teleportation decoding, F_avg = 0.568 vs the
    1/2 classical bound.  Anchors the decoder half and calibrates
    expectations: a hardware YK fidelity of ~0.57-0.8 is realistic.

Landsman et al. (arXiv:1806.02807, Nature 2019):
    7 ions = two 3-qubit copies + ancilla (the U/U* two-copy
    structure assumed in M2), teleportation fidelity ~80%.
```

T2echo on a tunable-coupler device: Willow's T2,CPMG = 89 us is the
pinned stand-in; closes the last [pin] in M3 item 1 at the
architecture level (per-device confirmation belongs in the proposal's
device table).

## M5 Part 2: Proposal-Ready Margin Table (L=6 instance)

Assumptions: Willow-class coherence (T1 68 us / T2,CPMG 89 us),
IQM-class CZ (error 1.9e-3, 33 ns), depth ~13 brickwork layers,
~85 2q gates including U/U* and record overhead, wall-clock ~1 us
including m=3 record swaps and Bell measurement.

```text
quantity                        value       source
------------------------------------------------------------------
trivial baseline F_triv^e       0.250       k=1
eps_idle  (1 - exp(-1.5/89))    ~0.02       Willow T2,CPMG; arm 4
                                            measures it directly
eps_res   (ZZ phase 0.02 rad)   ~0.002      IQM |zeta| < 2 kHz;
                                            Certificates 1+2 bound
                                            it from data
eps_rec   (interleaved RB gate) ~0.005      protocol requirement
------------------------------------------------------------------
frozen-arm ceiling              ~0.28       sum + UCB_alpha
------------------------------------------------------------------
raw circuit fidelity, L=6       0.75-0.85   85 gates x (1.9-3.3)e-3
normal-arm F_rec^e estimate     ~0.6-0.75   F_circ x F_YK-ideal
                                            + (1-F_circ)/4, with
                                            F_YK-ideal ~ 0.9 (k=1);
                                            Blok 0.568 as the
                                            pessimistic floor
------------------------------------------------------------------
witness margin                  >= 0.25     normal LCB - frozen
                                            ceiling, no mitigation
                                            required at L=6
```

The margin conclusion strengthens with verified numbers: idle loss
fell from 5% to ~2% (T2,CPMG = 89 us), residual coupling fell from 1%
to ~0.2% (|zeta| < 2 kHz), and even the pessimistic Blok-level
normal-arm fidelity (0.568) clears the 0.28 frozen ceiling by ~0.29.
At L=6 the witness works without error mitigation; mitigation is
reserved for the L=8 stretch instance.

## M5 Part 3: Consistent Budget (worst-of-both row)

The Part 2 table mixes device families (Willow coherence, IQM gates).
For the proposal, the honest envelope is the worst published value on
each axis, so no single-device assumption is needed:

```text
quantity                     best-combined   worst-of-both
------------------------------------------------------------------
2q (CZ) error                1.9e-3 (IQM)    3.3e-3 (Willow, pending
                                             SI confirmation)
T2 for idle loss             89 us (Willow)  40 us (conservative,
                                             below both families)
residual ZZ at off point     2 kHz (IQM)     5 kHz (search envelope)
------------------------------------------------------------------
eps_idle (1.5 us window)     ~0.02           ~0.037
eps_res                      ~0.002          ~0.005
eps_rec                      0.005           0.005
frozen-arm ceiling           ~0.28           ~0.30
raw circuit fidelity (L=6)   ~0.85           ~0.75
normal-arm F_rec^e           ~0.70           ~0.55-0.70
witness margin               >= 0.30         >= 0.25
------------------------------------------------------------------
```

The margin survives the worst-of-both row without mitigation, so the
proposal's feasibility claim does not depend on any best-in-class
number, including the one still-unverified Willow CZ figure.

## M5 Part 4: Public-Record Layer (completing the access-cut demo)

The protocol so far tests only the private axis.  The full
Heisenberg-cut demonstration needs the simultaneous profile: same
public record, different private fate.  Addition:

```text
stage 0 (identical in all arms):
    a pointer/label qubit X at the access region is branched into
    n_frag = 2-3 fragment ancillas by CNOTs (a small Darwinism
    broadcast).  X is chosen to commute with the record coupling.

stage 1 (arms differ):
    normal / frozen / echo routing of the distant diary D, as above.

measured profile per arm:
    P_guess(X | F_i)   per fragment   (public objectivity)
    F_rec^e(D)         via YK decoder (private recovery)
```

Predicted signature — the operational content of "cut motion moves
private recoverability, not public statistics":

```text
P_guess(X | F_i):  high and EQUAL across arms (freezing routing does
                   not touch the broadcast channel).
F_rec^e(D):        order-one in the normal arm, pinned at the frozen
                   ceiling in the frozen arm.
```

Budget: +3-4 qubits (label + fragments) and ~n_frag CNOTs — total
~24 qubits, still inside the Part 3 envelope (the added gates act
before the deep circuit and are not on the diary's error path).
Design constraint carried from theory: X must originate at the access
region (or be broadcast in stage 0, before arms diverge), otherwise
the public layer would itself require routing and the arms would not
share public statistics by construction.

## M5 Part 5: Discriminating-Class Variant (sizing answer)

The open design question resolves cheaply: the variant fits the same
budget because it is a parameter sweep, not a new instance.

```text
option A (weak link):    replace the middle bulk edge's CZ by a
                         partial-entangling gate with tunable angle
                         lambda; sweep lambda.
option B (disorder):     draw the single-qubit layers from a
                         disordered distribution of strength W;
                         sweep W toward the localization regime.
```

Either way the qubit count and depth are unchanged; only the pulse
parameters sweep.  The mechanism question becomes real: at strong
disorder / weak link, OTOC-style spreading diagnostics and diary
recovery can separate — this is Route 0's recovery-versus-scrambling
question run on hardware, in the same apparatus as the witness.  The
frozen arm then serves as the zero-transport anchor point of the
sweep rather than a standalone control.

## Remaining before the proposal draft

```text
- confirm Willow SI value for mean CZ error (affects only the
  best-combined column; worst-of-both already absorbs it).
- proposal draft itself: arms table, confidence-bound witness,
  Part 3 budget, Part 4 public layer, Part 5 sweep — the note now
  contains all inputs.
```
