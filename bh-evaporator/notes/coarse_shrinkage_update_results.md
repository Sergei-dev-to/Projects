# Coarse Shrinkage Update Results

## Question

After microscopic emissions, can the effective internal register shrink while
preserving global information?

This targets the next bottleneck:

```text
many microscopic emissions drain energy;
the effective internal capacity shrinks H_L -> H_(L-1);
information that no longer fits in the smaller bulk must already be in emitted
records or a shrink/soft record.
```

## Script

```text
sim/coarse_shrinkage_update.py
```

Outputs:

```text
sim/data/coarse_shrinkage_update_none_n3.csv
sim/data/coarse_shrinkage_update_none_n3_summary.csv
sim/data/coarse_shrinkage_update_local_n3.csv
sim/data/coarse_shrinkage_update_local_n3_summary.csv
sim/data/coarse_shrinkage_update_scrambled_n3.csv
sim/data/coarse_shrinkage_update_scrambled_n3_summary.csv
sim/data/coarse_shrinkage_update_local_n4.csv
sim/data/coarse_shrinkage_update_local_n4_summary.csv
sim/data/coarse_shrinkage_update_scrambled_n4.csv
sim/data/coarse_shrinkage_update_scrambled_n4_summary.csv
```

## Model

Start with:

```text
n_bulk qubits maximally entangled with a reference.
```

Run a few microscopic energy-aware emissions:

```text
bulk -> boundary edge -> hard bath + soft record.
```

Then apply a coarse shrink update:

```text
n_bulk -> n_keep.
```

The lost bulk qubits are moved into a shrink record:

```text
|i>_lost |0>_shrink -> |0>_lost |i>_shrink.
```

The reset lost qubits are no longer counted as effective bulk.

This is a unitary bookkeeping model of shrinking capacity. It is not yet a
physical local `L -> L-1` Hamiltonian.

## Complete Small Control

For:

```text
n_bulk = 3
n_keep = 2
n_events = 2
```

the result is:

```text
variant      D_hard   I(R:hard)   I(R:micro)   I(R:shrink)   I(R:allrec)   I(R:bulk)
none         0.0000     0.0000      1.3863       1.3863        2.7726       1.3863
local        0.0000     0.0000      2.2107       1.3863        3.5970       0.5619
scrambled    0.0000     0.0000      2.1765       0.7993        3.3152       0.8437
```

Here:

```text
I(R:micro):
  reference information in microscopic emission records.

I(R:shrink):
  reference information in the coarse shrink record.

I(R:allrec):
  reference information in microscopic + shrink records.

I(R:bulk):
  reference information still in the smaller effective bulk.
```

Hard radiation alone remains locally thermal and reference-decoupled:

```text
D_hard = 0
I(R:hard) = 0.
```

The information that does not fit in the smaller bulk is carried by records.

## Larger Spot Check

For:

```text
n_bulk = 4
n_keep = 3
n_events = 2
```

the nontrivial branches give:

```text
variant      D_hard   I(R:hard)   I(R:micro)   I(R:shrink)   I(R:allrec)   I(R:bulk)
local        0.0000     0.0000      2.2107       1.3863        3.5970       1.9482
scrambled    0.0000     0.0000      2.2417       0.8607        3.4950       2.0502
```

This is consistent with the smaller control.

## Interpretation

The shrink update behaves as required at the bookkeeping level:

```text
the effective bulk can shrink;
hard radiation alone remains thermal;
the lost capacity is purified by emitted records;
global information is not destroyed.
```

This strengthens:

```text
F2: unitary/purifiable evaporation;
F3: shrinking effective internal state space;
F8/F9: information in records/correlations rather than hard marginals.
```

## What This Does Not Prove

This is not yet the real finite-gauge `L -> L-1` update.

Still artificial:

```text
qubit shrinkage stands in for q^(L^2) -> q^((L-1)^2);
the shrink record is supplied as an explicit ancilla;
the update is scheduled after a chosen number of microscopic emissions;
no energetic threshold triggers the shrink;
no local boundary rule selects which degrees are lost.
```

So the result is:

```text
unitary coarse shrinkage is compatible with the microscopic emission picture.
```

not:

```text
the physical droplet dynamically shrinks.
```

## Why This Still Matters

The previous fear was that once the bulk Hilbert space shrinks, information
might be lost unless the model smuggles in an oversized record.

This test shows the minimal requirement:

```text
the record dimension must cover the lost effective capacity.
```

That is exactly the same logic as the earlier shell erosion channel, now placed
after multiple microscopic emissions.

## Next Step

The next natural upgrade is to replace:

```text
lose one abstract qubit
```

with the actual finite-gauge shell count:

```text
dim H_L / dim H_(L-1) = q^(2L - 1).
```

That would make the shrink record size match the real edge-tension droplet
instead of a qubit surrogate.
