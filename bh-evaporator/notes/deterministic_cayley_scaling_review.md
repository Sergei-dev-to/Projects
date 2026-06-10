# Review of the deterministic Cayley scaling result

## Short assessment

The calculation is useful, but the current interpretation is too strong.

It gives encouraging finite-size evidence that one deterministic chaotic
translation-invariant Hamiltonian produces Haar-like radiation entropies in the
`scramble-then-reveal` qubit evaporation test.  It does not yet close the
deterministic expander/open-channel gap in the paper.

## What the test actually measures

The script evolves an `n`-qubit state under a fixed Hamiltonian and then treats
blocks of qubits as emitted radiation.  In each step, the remaining leading
qubits are evolved under the Hamiltonian for that smaller core size.

So the tested channel is:

```text
scramble active core with exp(-i K_c t_mix)
then expose a fixed block of qubits as radiation.
```

This is a good proxy for the abstract shrinking-isometry/Page step.  It is not
the same as the weak-emission open channel in the ideal-Hamiltonian paper:

```text
Hamiltonian mixing + energy-conserving weak boundary emission + radiation
record/tracing.
```

Thus the result supports the deterministic mixer direction, but it does not
test the two-replica weak-emission channel identified in
`gap2_open_channel_contraction.md`.

## Positive findings

The seed-averaged entropy diagnostic is genuinely encouraging.

For the chaotic family, the deviation from the Page formula tracks the Haar
reference:

```text
n=6:   H = 0.060, Haar = 0.057
n=8:   H = 0.028, Haar = 0.026
n=10:  H = 0.015, Haar = 0.012
```

This means that for this scalar entropy diagnostic, at these sizes, the fixed
Hamiltonian behaves like a Haar scrambler up to the finite-size Page correction.

The controls are also useful:

```text
free_chain:  deviation grows with n;
integ_xxz:   deviation stays above the Haar floor;
chaotic case: tracks the Haar floor.
```

The spectral diagnostics point in the expected direction: the chaotic family
has no near-degeneracies in the measured sector, while the free/integrable
families carry degeneracy or non-chaotic signatures.

## Main problem: the graph is not an expander family

The positive family is called `chaos_expander`, but the graph used is the
circulant Cayley graph on `Z_n` with generators

```text
{+1, -1, n/2}.
```

This graph is vertex-transitive and Cayley.  It is not an expander family.

The adjacency eigenvalues are

```tex
\lambda_k=2\cos(2\pi k/n)+(-1)^k,
```

so the second eigenvalue approaches the degree `3` as `n` grows:

```tex
3-\lambda_2 \sim O(n^{-2}).
```

Numerically:

```text
n=20:   gap ~ 0.382
n=50:   gap ~ 0.063
n=100:  gap ~ 0.016
n=200:  gap ~ 0.004
```

Therefore this is a deterministic Cayley/circulant Hamiltonian test, not a
Cayley-expander test.  The name should be changed unless the graph is replaced
by a genuine expander family.

## Second problem: the result is a scalar diagnostic, not full channel decoupling

The entropy curve is the most important diagnostic, but matching it does not by
itself prove the channel decoupling statement needed for the paper:

```tex
I_2(Q:X_{\rm wrong})\ll 1.
```

The current test starts from product states, evolves, and measures radiation
entropy.  A closer test would purify a code subspace by a reference `Q` and
measure:

```text
before Page time:  I_2(Q:R_early)
after Page time:   I_2(Q:B_remaining)
```

for the same deterministic Hamiltonian and reveal rule.

That would still be a reveal-channel test rather than the full weak-emission
open-channel test, but it would match the information-theoretic target more
directly.

## Third problem: the asymptotic claim is not established

The positive case is tested only up to `n=10` in the seed-averaged CSV.  The
note also reports a single-seed `n=12` row, but that row is not present in the
current CSV and was not seed-averaged.

The data justify:

```text
At ED sizes n <= 10, this deterministic chaotic Cayley/circulant Hamiltonian
matches the Haar Page-entropy benchmark within a few millinats.
```

The data do not justify:

```text
This Hamiltonian converges asymptotically to the Page curve.
```

That stronger statement needs either larger sizes, a stronger analytic
argument, or a graph/Hamiltonian family whose scrambling behavior can be tied
to known results.

## What to do next

The right next step is not to put this into the paper as a closed gap.

The useful next steps are:

1. Rename the positive family from `chaos_expander` to something accurate, such
   as `chaos_circulant`, or replace the graph with an actual Cayley/Ramanujan
   expander family.
2. Add a reference-purified decoupling diagnostic:
   ```text
   I_2(Q:R_early), I_2(Q:B_remaining)
   ```
   for the deterministic Hamiltonian reveal model.
3. If the result survives, present it as finite-size evidence that explicit
   deterministic chaotic Hamiltonians can realize the Page/island shrinking
   isometry, while keeping the full weak-emission open-channel theorem as the
   remaining analytical gap.

## Paper implication

This is interesting enough to keep.

It should not be used to say that the deterministic sparse-Hamiltonian gap is
closed.  It can support a more careful statement:

```text
As a finite-size check of the deterministic route, an explicit chaotic
Cayley/circulant Hamiltonian reproduces the Haar Page benchmark in a
scramble-then-reveal evaporation test, while free and integrable controls fail.
```

That is a real result.  It is narrower than the current note's strongest
language.

