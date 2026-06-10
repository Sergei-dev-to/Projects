# Track E: Variable-Length Spin-Chain Pilot

## Why a spin chain?

The target missing model is:

```text
right state count
concrete quantum Hamiltonian
shrinking sectors
matrix-element-derived emission
```

The area register has the right state count but abstract Hamiltonian blocks:

```text
H_n = n qubits
dim H_n = 2^n
random block around M_n
```

The variable-N Bose-Hubbard model has concrete many-body dynamics but the
wrong asymptotic state count:

```text
dim H_N = binomial(N + L - 1, N)
S_N ~ (L - 1) log N
```

A variable-length spin chain is the simplest bridge:

```text
H_n = (C^2)^{tensor n}
dim H_n = 2^n
S_n = n log 2
```

The entropy scaling is natural because it comes from adding/removing local
quantum degrees of freedom, not from assigning shell dimensions by hand.

It is not meant to say that a black-hole horizon is literally a spin chain.
It is a controlled test of whether area-law sector counting plus a concrete
many-body Hamiltonian can reproduce the Track B acceleration.

## Model

Sectors:

```text
H = direct sum_n H_n
H_n = n-spin Hilbert space
n = 4,...,10
```

Mass law:

```text
sqrt case:   M_n = alpha sqrt(n)
linear case: M_n = alpha n
```

Hamiltonian block:

```text
H_n = M_n I + bandwidth * h_n
```

where `h_n` is a local chaotic spin-chain Hamiltonian:

```text
h_n =
  Jx sum_i X_i X_{i+1}
  + Jz sum_i Z_i Z_{i+1}
  + hx sum_i X_i
  + sum_i hz_i Z_i
```

with weak random fields.

Shrinkage maps:

```text
boundary removal:
  remove the last spin and record its value.

bulk removal:
  remove any one spin and record site/value.

scrambled removal:
  orthogonally scrambled boundary-removal control.
```

Rates:

```text
Gamma_{f i} ~ |<f,n-1|X_n|i,n>|^2 J(omega)
omega = E_{n,i} - E_{n-1,f}
```

## Questions

Primary:

```text
Can a concrete variable-length spin-chain Hamiltonian reproduce the Track B
sqrt-mass acceleration?
```

Secondary:

```text
Does local/bulk removal behave differently from scrambled removal?
```

If local and scrambled behave the same, the model is still mostly a
sector-profile area register. If they differ, the Hamiltonian/removal structure
is doing dynamical work.

## Kill conditions

Stop if:

```text
1. sqrt mass does not accelerate;
2. local/bulk/scrambled behave essentially the same;
3. the result is indistinguishable from Track B random-block area register.
```

## Positive signs

Continue if:

```text
1. sqrt mass accelerates while linear mass does not;
2. local or bulk removal differs from scrambled removal;
3. the W decomposition shows nontrivial selection, not only sector profile;
4. the result is robust across seeds and Hamiltonian parameters.
```

