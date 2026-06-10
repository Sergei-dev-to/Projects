# Reversible Shrinkage Automaton Results

## Question

The stitched evaporator still has an explicit coarse rule:

```text
if emitted energy accumulator A >= Delta M:
  L -> L - 1
```

This can look nonunitary if read too literally.

The question here is narrower:

```text
Can the threshold/shrinkage bookkeeping be represented as a reversible finite
register update?
```

## Script

```text
sim/reversible_shrinkage_automaton.py
```

Outputs:

```text
sim/data/reversible_shrinkage_automaton_sample.csv
sim/data/reversible_shrinkage_automaton_summary.csv
```

## Register Map

The finite registers are:

```text
L:
  active droplet size.

A:
  emitted-energy accumulator for the current shell.

shell_label:
  label of the shell capacity to be transferred if shrinkage fires.

emitted_bin:
  the newly emitted microscopic energy bin.

radiation_record:
  record of emitted_bin.

shrink_record:
  empty unless threshold fires; then stores (L, shell_label).
```

The update is:

```text
A' = A + emitted_bin.
```

If:

```text
A' < Delta M,
```

then:

```text
L -> L
A -> A'
shell_label -> shell_label
radiation_record -> radiation_record + emitted_bin
shrink_record -> empty
```

If:

```text
A' >= Delta M,
```

then:

```text
L -> L - 1
A -> A' - Delta M
shell_label -> 0
radiation_record -> radiation_record + emitted_bin
shrink_record -> (L, shell_label)
```

The shrink record is what preserves reversibility. Without it, many shell
states would collapse into the same smaller droplet state.

## Check

The script enumerates a toy finite register space:

```text
L = 1,...,5
Delta M = 8 integer units
A mod 8
emitted bins = {1,2,3}
dim shell_label(L) = 2^(2L - 1)
```

It then checks whether the computational-basis update is injective using only
the actual output registers:

```text
L_after,
A_after,
shell_label_after,
shrink_record,
radiation_record.
```

## Result

```text
transitions        = 16368
unique outputs     = 16368
injective          = True
shrink transitions = 4080
nonshrink          = 12288
```

So the threshold/shrink rule can be embedded as an isometry on finite registers.
With a large enough output space, it can be extended to a unitary permutation.

## Interpretation

This does not derive shrinkage dynamically from a Hamiltonian.

But it fixes a narrower worry:

```text
the coarse shell update is not intrinsically nonunitary.
```

It is nonunitary only if one discards the shrink record.

With the record retained, the update is ordinary reversible bookkeeping:

```text
the active droplet shrinks;
the lost shell capacity moves into records.
```

This matches the Page/information-flow picture:

```text
the black-hole-like subsystem loses internal capacity;
the full state remains purifiable because the lost capacity is outside.
```

## F15 Impact

This strengthens F15 a little:

```text
the stitched architecture now has an explicit reversible threshold/shrinkage
register map.
```

But F15 is still not a clean `Y`:

```text
the map is still a designed repeated-interaction update, not a consequence of
one autonomous H_total.
```

## Next Naturalness Target

After this, the least natural F15 piece is no longer reversibility of shell
bookkeeping.

It is:

```text
why the bath/emission interaction plus accumulator should implement this map
autonomously.
```

The next step would be to embed this automaton into the stitched Floquet cycle
as the explicit `U_bookkeep` block.
