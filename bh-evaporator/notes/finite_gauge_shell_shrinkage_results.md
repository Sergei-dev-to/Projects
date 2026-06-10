# Finite-Gauge Shell Shrinkage Results

## Question

Can we replace the abstract qubit shrinkage surrogate with the actual
finite-gauge shell ratio?

For the edge-tension finite-gauge droplet:

```text
dim H_L = q^(L^2)
dim H_(L-1) = q^((L-1)^2)
```

Therefore:

```text
dim H_L / dim H_(L-1) = q^(2L - 1).
```

This is the exact shell capacity that must be transferred to records when the
effective bulk shrinks:

```text
H_L -> H_(L-1) tensor H_shell(L).
```

## Script

```text
sim/finite_gauge_shell_shrinkage.py
```

Output:

```text
sim/data/finite_gauge_shell_shrinkage.csv
```

## Result

For `q = 2`:

```text
L  dim H_L  dim core  dim shell  DeltaS   I(R:core) after  I(R:shellrec) after  I(R:all) after
2       16         2          8   2.079            1.386                 4.159          5.545
3      512        16         32   3.466            5.545                 6.931         12.477
4    65536       512        128   4.852           12.477                 9.704         22.181
5 33554432     65536        512   6.238           22.181                12.477         34.657
```

The identity is exact:

```text
dim H_L = dim H_(L-1) dim H_shell
```

with:

```text
dim H_shell = q^(2L - 1).
```

The entropy transferred to the shell record is:

```text
Delta S = (2L - 1) log q.
```

If the original bulk is maximally entangled with a reference, then after the
coarse shrink map:

```text
I(R : core)        = 2 log dim H_(L-1)
I(R : shell_record)= 2 log dim H_shell
I(R : all output)  = 2 log dim H_L.
```

So the lost finite-gauge capacity is exactly accounted for by the shell record.

## Interpretation

This directly strengthens F3.

The previous coarse shrinkage diagnostic used:

```text
lose one abstract qubit.
```

This diagnostic uses the actual finite-gauge shell ratio:

```text
q^(L^2) -> q^((L-1)^2)
```

with lost capacity:

```text
q^(2L - 1).
```

So the shrinking-state-space part is no longer just a qubit analogy. At the
Hilbert-space level, the finite-gauge droplet has the exact factorization
needed for a unitary shrink update.

## What This Does Not Yet Prove

This is still a factorization/bookkeeping result.

It does not yet provide:

```text
a local gauge Hamiltonian that dynamically performs L -> L-1;
a physical boundary rule selecting the shell degrees;
coupling between many microscopic emissions and the shell update threshold;
large radiation Page curve.
```

So:

```text
F3 is close to Y at the Hilbert-space level;
F3 is still not Y as autonomous dynamics.
```

## Matrix Consequence

Conservative status:

```text
F3 = P+
```

If the matrix allows only `Y/P/N`, it can remain `P`, but the note should state
that the remaining gap is dynamical, not kinematic:

```text
the actual finite-gauge shrink ratio is implemented;
the local Hamiltonian that triggers the shrink is not.
```

## Next Step

To push F3 all the way to `Y`, we would need a dynamical update rule:

```text
after enough microscopic energy emissions sum to Delta M = 4 sigma,
apply or derive the shell-factor map
H_L -> H_(L-1) tensor H_shell(L).
```

The hard part is deriving that update from a local boundary Hamiltonian, not the
state counting.
