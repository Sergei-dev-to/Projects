# Direction Plan: Frozen-Routing Platform Proposal

Date: 2026-07-02

Role: research direction plan (experiment-design track)

Status: planning; upgrades Route 2 of
`../experimental_prediction_routes.md` from sketch to protocol.

## One-Line Goal

Turn the frozen-routing diagnostic into a platform-concrete,
error-budgeted experimental protocol: a scrambling-witness control arm
that existing OTOC and teleportation-based experiments do not have.

## What Exists and What Is Missing

The diagnostic is already stated in four notes (qi access note,
Route 2, `../access_profile_verification_target.md`,
`../access_geometry_and_export_bottlenecks.md`), always at the same
altitude: "freeze the transport terms, keep the record coupling, see if
recovery survives."  What no note supplies:

```text
- a named platform whose control graph actually factorizes into
  routing terms and record terms;
- a circuit-level protocol with system sizes and depths;
- an error budget showing the frozen arm is not swamped by idle
  decoherence;
- a confound analysis (what else changes when routing is frozen);
- the discriminating-class variant on dynamics whose access structure
  is not fixed by construction.
```

The selling point against existing experiments: teleportation-based
scrambling witnesses (Landsman et al.) and OTOC experiments control for
decoherence mimicking scrambling, but none has a control arm separating
*dynamical transport* from *prearranged or dressed access*.  That
control arm is this program's most original artifact.

## Protocol Skeleton

```text
system:      diary qubit(s) at distance L from an access/readout
             region, connected by a routing medium (chain or graph).
reference:   purifying qubit A held aside (or replaced by randomized-
             measurement estimation of F_rec^e if idling A is too lossy).

arm 1 (normal):   run U(t), decode from access region, measure
                  F_rec^e onset T_eta.
arm 2 (frozen):   switch off routing couplers, keep record coupling
                  identical, same wall-clock schedule, decode, compare.
arm 3 (echo):     reverse routing mid-protocol (echo variant from
                  ../access_latency_stress_test.md) as a second,
                  differently-confounded control.

verdicts:
    recovery dies in arm 2   => transport-routed access (dynamical).
    recovery survives arm 2  => prearranged / nonlocal / dressed access.
```

## Platform Candidates

```text
A. superconducting, tunable couplers (leading candidate):
       routing = coupler-mediated hopping, switchable per-edge in ns;
       record coupling = fixed readout/ancilla edge.  The control
       graph factorization is native hardware.

B. Rydberg tweezer arrays:
       routing = dipole exchange, frozen by detuning or physically
       retracting atoms; record coupling = local ancilla or imaging.
       Freezing is very clean (geometric), slower cycle.

C. trapped ions:
       programmable but gates are global-bus mediated; freezing
       "routing while keeping records" is a software distinction, so
       the frozen arm is less physically meaningful.  Backup only.
```

Decision input needed: whether this stays a proposal paper (any
platform, pick A for concreteness) or targets a collaboration (pick by
who will run it).

## Minimal Instance Estimate

To be firmed up in M2; starting point:

```text
diary:            1 qubit (k=1, d_D=2; trivial baseline 1/4)
routing medium:   6-10 sites, 1D chain first, then one expander-ish
                  coupling graph for the fast-routing contrast
records:          2-3 emitted/ancilla qubits (m >= k + 2 margin)
decoder:          Yoshida-Kitaev with known U (engineered platform, so
                  U^dagger is available; this is the demonstration
                  class and that is fine for the witness)
depth:            scrambling on 8-12 qubits within current coherence
                  on platform A; comparable to done experiments.
```

## Confounds To Budget

This is the section that decides viability.

```text
1. idle decoherence in the frozen arm:
       freezing routing but keeping the wall-clock schedule means the
       diary idles; recovery can die from T2, not from absent routing.
       Mitigation: dynamical decoupling on frozen sites + a fourth arm
       (frozen routing, no record coupling) to measure pure idle loss.
       The witness statement must be inequality-shaped: recovery decay
       beyond the measured idle-loss envelope.

2. freezing verification:
       "coupler off" must be certified independently, e.g. by a
       light-cone / signaling measurement in the frozen configuration,
       not assumed from calibration.

3. record-coupling drift:
       switching couplers can shift frequencies of neighboring edges;
       the record coupling in arm 2 must be measured, not assumed
       identical to arm 1.

4. decoder mismatch:
       arm 2 has different effective dynamics; the fair comparison is
       best-decoder-per-arm, not same-decoder, or the dead recovery in
       arm 2 is an artifact.  State this in the protocol.
```

## Discriminating-Class Variant

Per the demonstration-vs-discrimination split of Route 2: after the
engineered demonstration, the same arms on a system whose access
structure is not fixed by inspection:

```text
disordered or fragmented routing medium (Hilbert-space fragmentation,
weak-link chains): whether recovery is transport-routed is then a real
question, and the frozen arm answers it.
```

This variant is what makes the proposal a measurement rather than a
calibration, and connects to Route 0's recovery-vs-scrambling question.

## Milestones

```text
M1  platform decision + control-graph factorization writeup for the
    chosen platform (which Hamiltonian terms are "routing", which are
    "record", cited against hardware papers).
M2  minimal instance + depth/coherence feasibility estimate (analytic;
    no simulation required at this stage).
M3  confound/error budget note (section above, quantified).
M4  prior-art sweep: any scrambling experiment with a transport-frozen
    control arm; coupler-off idle characterization literature.
M5  proposal draft: protocol figure, arms table, witness inequality,
    feasibility claim.
```

## Kill Criteria

```text
- M3 shows idle loss in the frozen arm exceeds the recoverable signal
  on every candidate platform at any viable size => the test is
  theory-only for now; record that and stop.
- M4 finds an equivalent control arm already published => downgrade to
  citation + the discriminating-class variant only.
- No platform gives certifiable freezing (confound 2) => stop.
```

## Deliverable and Venue

Proposal paper: PRX Quantum / Quantum / PRA experimental-proposal
track, or directly a collaboration whitepaper if M1 lands a partner.
Numerical simulation of the minimal instance is deliberately out of
scope for this plan (agenda constraint); if a referee or partner needs
it, it is a handoff item, and M2/M3 are written to stand analytically.

## Dependencies

- The witness inequality should quote the corrected qi-note statements
  (one-directional hiding condition).
- Independent handle on v and L (the qi note's own falsifiability
  caveat) is supplied here by the freezing-verification measurement;
  keep that link explicit in the draft.
