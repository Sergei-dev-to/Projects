# Private Information Behind Public Records: Experiment Ideas

Date: 2026-06-15

Purpose: record possible observational directions suggested by the constrained-access framework, especially tests that look for a private quantum complement behind already-saturated public classical records.

## Basic Question

Can an experiment show that public classical objectivity is incomplete in a resource-sensitive way?

More concretely:

> Public records saturate early, but private quantum information becomes recoverable only with larger fragments, deeper control, later time, or nonlocal access.

This is not primarily a Born-rule, weak-measurement, or Wigner-friend test. It is a constrained-access test: what information is visible to the ordinary public channel, what remains hidden from that channel, and what resources reveal it?

Equivalently, the experiment should distinguish effective forgetting from recoverable hiding:

```text
effective forgetting:
    the public channel cannot distinguish the private information

recoverable hiding:
    the public channel cannot distinguish it, but an enlarged channel can
```

## Clean Target Signature

The desired signature is a separation of access scales:

```text
public redundancy scale << private recovery scale
```

For instance:

- `m_public`: number of environment fragments/qubits needed to infer the public pointer value.
- `m_private`: number of environment fragments/qubits, circuit depth, or elapsed record time needed to recover a diary qubit or complementary coherence.

The interesting regime is:

```text
m_public = O(1),       m_private large / late / complexity-sensitive.
```

This would demonstrate that classical objectivity can saturate while private quantum information remains inaccessible to all small public fragments.

## Prototype Protocol

1. Prepare a system qubit `S` and a diary qubit `D`, with `D` entangled with a reference `R`.
2. Couple `S` to many environment/register qubits so that fragments redundantly record a pointer observable, for example `Z_S`.
3. Verify ordinary public objectivity:

   ```text
   I(Z_S : F_m)
   ```

   reaches a plateau for small fragments `F_m`.

4. Verify privacy:

   small public fragments do not recover `D`, `R`, or complementary phase information.

5. Increase access by collecting larger fragments, allowing deeper decoding circuits, waiting for more records, or applying a global eraser/recovery operation.
6. Measure when diary/reference entanglement or complementary coherence becomes recoverable.

The experiment is successful if public objectivity is already present while private recovery still requires substantially greater access.

## Frozen-Dynamics Diagnostic

Run two versions.

Normal dynamics:

```text
public records form;
diary becomes recoverable after enough time/records/control.
```

Frozen or echoed internal dynamics:

```text
public records still form;
diary recovery fails or is strongly delayed.
```

Interpretation:

- If recovery dies under frozen dynamics, private information reached the record channel through internal routing or scrambling.
- If recovery survives, the record channel was already nonlocal/dressed relative to the naive decomposition, or side information already contained the diary.

This is the closest laboratory analogue of the horizon-interface question. It distinguishes information becoming accessible through dynamics from information being accessible because the chosen record algebra was already global.

## Relation to Existing Experiments

Quantum Darwinism experiments already test the emergence of redundant public records. The proposed addition is to measure what survives outside that objective layer.

Quantum eraser experiments already show that coherence can be restored by changing the accessible degrees of freedom. The proposed addition is to quantify the access gap between public objectivity and private recovery.

Hayden-Preskill simulators already test recovery from scrambled records. The proposed addition is to place HP-style recovery behind a public-record layer and compare recovery with and without internal routing.

So the experiment should not be advertised as "observing Quantum Darwinism" or "doing a quantum eraser." The sharper claim is:

> Measure the resource cost of revealing private quantum information behind an already-objective public record.

## Candidate Platforms

Superconducting qubits:

- Good for engineered scramblers, partial measurements, controlled reservoirs, and echo/frozen-dynamics variants.
- Likely best for testing routing versus nonlocal access.

Trapped ions:

- Good for tunable locality and long-range interactions.
- Useful for measuring latency scaling as interactions are made more or less local.

Photonic cluster states:

- Good for Quantum-Darwinism-plus-eraser variants.
- Existing public-objectivity tests are already near this architecture.

## The Conceptual Payoff

The experiment would operationalize "private information" without requiring direct public observation of it.

The witness is comparative:

```text
ordinary public channel: private information invisible
expanded/control channel: private information recoverable
```

That comparison is the operational test of forgetting versus hiding. Public records alone may make two global states look identical; enlarged access decides whether the difference was absent for the effective description or merely hidden from it.

This turns the private complement into a resource question:

- How much of the environment must be controlled?
- How deep must the decoder be?
- How long must records accumulate?
- Does recovery require internal dynamics?
- Does recovery disturb or erase the public record?

These questions are the experimental counterpart of the algebraic decomposition:

```text
public center
recorded-but-deep block
noiseless commutant / private complement
```

## Cautions

The first naive version is too close to "Quantum Darwinism plus quantum eraser." The version worth pursuing measures the access-scale separation.

The private information is not directly visible to the public channel. Its presence is inferred from a controlled recovery that succeeds only after access is enlarged.

The experiment should keep de-protection and decodability separate:

- De-protection: the information stops lying in the commutant of the current record algebra.
- Decodability: the information can actually be reconstructed from records by an allowed decoder.

The public-record layer may be classical and redundant while the private complement remains coherent, recoverable, or protected under the current access algebra.
