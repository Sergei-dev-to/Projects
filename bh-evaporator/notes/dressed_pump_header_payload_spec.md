# Dressed-Pump Header/Payload Specification

Date: 2026-07-12

Status: **parked specification for a named gravitational model; generic pump
simulation retired after the July 12 literature pass**. This is the C2 two-arm test from
`evaporation_capacity_metadata_deadline_conjectures.md`. It defines the
minimum comparison for a named gravitational algebra. Perturbative
gravitational splitting already supplies the static header/payload result at
leading order; see `evaporation_framework_comparison_map_2026_07_12.md`.

## 1. Question

When constraints make an internal state visible outside, what is actually
visible?

```text
header:
  a conserved label such as energy, electric charge, or angular momentum;

payload:
  private quantum information distinguishing states with exactly the same
  declared asymptotic labels.
```

The test must keep these possibilities separate. A signal that reveals a
charge difference is not evidence that the same mechanism reveals an arbitrary
message at fixed charge.

## 2. Common process and record

Start from the finite-energy pump or integrated microcanonical pump already
in the repository. Use the same pump, shell trajectory, event probabilities,
partner bookkeeping, greybody parameters, and observation schedule in both
arms.

Split the declared accessible record as

```text
R = R_asym tensor R_rad,
```

where `R_asym` contains only the chosen asymptotic charge observables and
`R_rad` contains the emitted radiation record. The hidden complement includes
the daughter shell, partners, pump memory, and any unobserved dressing
degrees of freedom.

The process must state the charge resolution and observation budget:

```text
charge alphabet Q,
resolution delta_Q,
energy budget delta_E,
number of emissions K,
detector/control class,
accessible algebra A_R.
```

Without these declarations, "the charge is visible" is not a quantitative
statement.

## 3. Arm H: charge-varying header

Use a classical charge register `Q` with at least two values `q_0 != q_1`.
Prepare the two alternatives with different exact asymptotic charges, while
keeping the ordinary pump/radiation protocol fixed as far as conservation
allows.

The minimal header control is

```text
|q>_Q |0>_(R_asym)  ->  |q>_Q |q>_(R_asym),
```

with orthogonal resolved record states whenever `|q_0-q_1|` exceeds the
declared resolution. This is a charge-record baseline, not a derivation from
gravity: a microscopic dressing calculation must show that its physical
asymptotic algebra realizes the same separation.

Measure:

```text
chi(Q : R_asym),
||N_H(q_0)-N_H(q_1)||_1,
||N_H-C_H^blind||_diamond,
time and precision needed to resolve q_0 versus q_1,
```

and compare them with the same quantities after discarding `R_asym`. The last
comparison prevents a charge header from being mistaken for radiation access
to the whole diary.

Expected outcome when the charge algebra and resolution are correct:

```text
charge distinguishability is nonzero, possibly order one;
the result scales with the charge separation and detector resolution;
no conclusion about fixed-charge payload follows.
```

## 4. Arm P: fixed-charge payload

Choose two orthogonal states `|0>_P, |1>_P` inside one exact sector:

```text
Q |0>_P = q_* |0>_P,
Q |1>_P = q_* |1>_P,
```

and impose equality of every declared asymptotic label, including energy,
momentum, angular momentum, gauge charges, and any other center included in
`A_R`. The payload is a reference-entangled qubit if quantum recovery is
tested.

Use two versions of the fixed-charge arm:

```text
P0, blind control:
  use the existing finite-pump or microcanonical pump tensored with I_P;

P1, dynamical mixer:
  add only an explicitly identified emission-relative coupling that can route
  P into R_rad, leaving all asymptotic charges unchanged.
```

The critical comparison is P0 versus P1, not H versus P alone. H tests forced
metadata. P0 tests fixed-charge privacy. P1 tests whether ordinary temporal
mixing, rather than dressing, supplies payload access.

Measure:

```text
chi(P : R_asym),
I(P : R_rad),
||N_P0-N_P1|| on the complete record,
inf_(C_P blind) ||N_P-C_P||_diamond,
reference-payload decoupling from the hidden complement,
best recovery fidelity and its first time of crossing threshold alpha.
```

The expected null for P0 is exact blindness on the declared record. P1 may
become recoverable, but only with a recorded process-level coupling or mixing
condition. A recovery-grade P0 result would refute the fixed-charge privacy
conjecture and become the stronger result target.

## 5. Required controls

Every run must include:

1. The same charge-blind thermal pump for H and P, where possible.
2. A charge-only record with the payload register removed.
3. A payload-only record with `R_asym` removed.
4. A no-dressing or spectator-dressing control, so energy-history correlations
   are not counted as payload access.
5. A direct reference-decoupling calculation, not only one-particle spectra or
   mutual information with a selected mode.

The charge header and payload should be reported in separate rows. A single
aggregate "information leaked" number is not sufficient.

## 6. Kill conditions

```text
H invisible in the declared correct asymptotic algebra:
  the charge-resolution or dressing model is inadequate, or the proposed
  charge is not actually an accessible center.

P0 recovery-grade while all declared charges are fixed:
  fixed-charge privacy is false for that algebra/model; inspect whether the
  access came from a hidden nonlocal observable rather than radiation.

P1 recovery only after an explicit emission-relative mixer:
  supports the separation between forced header metadata and dynamical
  payload export.

P0 and P1 indistinguishable on the complete declared record:
  the proposed mixer is not coupled to the accessible process, regardless of
  static or one-mode diagnostics.
```

No `log S` metadata floor is allowed until the charge alphabet, resolution,
energy/control cost, and observation time are fixed and the corresponding
Holevo or strategy-distance bound is derived.

## 7. Current implementation boundary

Perturbative gravitational splitting supports charge-only exterior
distinguishability at leading order: different total charges supply the header,
while same-charge localized information can remain private. Strong
holography-of-information arguments remain a competing nonperturbative branch.

A freely designed finite or microcanonical pump cannot decide between them,
because choosing its accessible algebra chooses the answer. Implementation is
therefore paused until the two arms can be placed inside a named asymptotic
algebra with a derived dressing construction. A claim about accumulated
radiation access additionally requires actual emission dynamics, not the static
dressing algebra alone.
