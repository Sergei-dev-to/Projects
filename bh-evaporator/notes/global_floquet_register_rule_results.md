# Global Floquet Register Rule Results

## Purpose

This test asks whether the evaporation architecture can be written as one
repeated finite-register rule, rather than as disconnected emission and
shrinkage gadgets.

It combines, in one update cycle:

```text
incoming bath microstate
-> hard-bin emission label
-> emitted-energy units
-> accumulator update
-> conditional shell shrinkage
-> radiation/shrink records
```

This is still a register-level Floquet rule, not a time-independent
Hamiltonian.

## Setup

The core is the nested shell system used in the multi-shell shrinkage test:

```text
L0 = 3
q = 2
shell_gap = 8
accumulator modulus = 8
sequence length = 3
```

The bath is a tiny one-particle 2D box:

```text
(nx, ny) in {-1,0,1}^2 \ {(0,0)}
```

Axis modes have:

```text
energy = 1
hard bin = 1
emitted units = 1
```

Diagonal modes have:

```text
energy = sqrt(2)
hard bin = 2
emitted units = 2
```

The rule keeps the bath microstate sequence, the hard-bin sequence, the
emitted-unit sequence, and any shrink records.

## Result

Exhaustive enumeration gives:

```text
inputs                       = 1048576
unique full outputs           = 1048576
full map injective            = True

unique outputs without bath microstate = 16384
injective without bath microstate      = False

unique outputs without shrink record   = 477184
injective without shrink record        = False

total shrink events            = 589824
max shrinks in a sequence      = 1
hard bin histogram             = 1:1572864, 2:1572864
```

## Interpretation

The full finite-register rule is injective. So the combined process:

```text
bath input
+ hard emission
+ accumulator evolution
+ shell shrinkage
```

can be represented as reversible finite-register bookkeeping in this test.

The two erasure checks are more informative than the positive injectivity
alone.

If the incoming bath microstate is erased, the map is not injective. This is
expected: several bath modes can produce the same coarse hard bin and emitted
energy.

If the shrink record is erased, the map is also not injective. This means a
unitary evaporation model cannot simply reduce the internal Hilbert space and
forget which shell label was expelled. The missing information must live in a
soft/shrink/radiation record.

## What This Improves

This strengthens F15:

```text
autonomy / one repeated update rule
```

The result is stronger than the separate shrinkage automaton because the bath
microstate, hard emission label, emitted energy, accumulator, and shrink record
are all handled in one repeated rule.

It also clarifies F2 and F3:

```text
shrinking capacity is compatible with purifiability
only if the expelled shell data is retained somewhere.
```

## What This Does Not Do

This does not yet include:

```text
explicit state-vector hard/soft radiation dynamics;
internal scrambling;
thermal edge typicalization;
a single autonomous Hamiltonian;
many-shell evaporation to completion.
```

So the correct status is:

```text
one global finite-register Floquet rule: supported
one autonomous physical Hamiltonian: still missing
```

## Files

Script:

```text
sim/global_floquet_register_rule.py
```

Data:

```text
sim/data/global_floquet_bath_modes.csv
sim/data/global_floquet_register_rule_sample.csv
sim/data/global_floquet_register_rule_summary.csv
```
