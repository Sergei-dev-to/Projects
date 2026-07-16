# Approximate Capacity-Cut Audit

Date: 2026-07-12

Status: **closed as a direct finite-dimensional lemma**. This note audits
target C3b in `evaporation_capacity_metadata_deadline_conjectures.md`.
The result is a standard dimension/decoupling consequence, not a new
black-hole theorem. Its use in an evaporation model still requires an
explicit diary code, accessible record, hidden complement, and error norm.

## 1. Setup

Let `D` be a `d`-dimensional diary code and let a complete evaporation
completion through step `K` be an isometry

```text
W : D -> R tensor X,
```

where `R` is the complete accessible emitted record and `X` is the entire
hidden complement at that time: daughter shell, hidden partners, archive, and
any purifier of initially mixed auxiliary systems. Write

```text
N : D -> R
```

for the record channel. A diary-blind channel is a replacer

```text
C(rho) = sigma_R
```

for one fixed state `sigma_R`, independent of the diary input. The distance
below is the full diamond norm, so its range is `[0,2]`.

The claim is only about blindness on the whole declared code. If the physical
process is tested on a smaller reachable family, replace `d` by an effective
code dimension only after that restriction has been stated explicitly.

## 2. Dimension bound

Assume `x=dim(X)<d`. Feed half of a maximally entangled state
`Phi_AD` through `N`, retaining the reference `A`. The global output is pure
on `A R X`, and the Schmidt rank across `A R | X` is at most `x`.

For any replacer `C`, the corresponding reference-record state is

```text
Phi_AD --id_A tensor C--> (I_A/d) tensor sigma_R.
```

A purification of this product state has at least `d` equal Schmidt
coefficients across `A R | X'` when `sigma_R` is pure; allowing a mixed
`sigma_R` cannot increase the best overlap with a state whose purifying side
has dimension `x<d`. The largest possible root fidelity is therefore at most

```text
F <= sqrt(x/d).
```

Uhlmann's theorem and the Fuchs--van de Graaf inequality then give

```text
|| (id_A tensor N)(Phi_AD)
   - (id_A tensor C)(Phi_AD) ||_1
  >= 2 (1 - sqrt(x/d)).
```

Taking the supremum over reference-assisted inputs yields the capacity-cut
lemma:

```text
inf_(C diary blind) ||N-C||_diamond
  >= 2 (1 - sqrt(x/d)),       x<d.                    (2.1)
```

Equivalently, if the record is `epsilon`-close in full diamond norm to a
diary-blind channel, then

```text
x/d >= (1-epsilon/2)^2.                                (2.2)
```

The bound becomes nontrivial precisely when the hidden complement is smaller
than the diary. It vanishes once `x>=d`, as it must: a complement large enough
to hold the diary can support exact no-hiding.

## 3. Evaporation form

If the hidden complement factors as

```text
X = B_K tensor P_hidden,K,
```

then `x=d_(B_K) d_(P_hidden,K)` and (2.1) becomes

```text
inf_(C_K diary blind) ||N_K-C_K||_diamond
  >= 2 (1 - sqrt[d_(B_K)d_(P_hidden,K)/d_D]),
```

whenever `d_(B_K)d_(P_hidden,K)<d_D`. This is the approximate counterpart of
the exact no-hiding cut

```text
d_(B_K)d_(P_hidden,K) >= d_D
```

for exact blindness. It says that a too-small complement cannot preserve a
large diary while the radiation remains arbitrarily blind.

This does **not** produce a Page-time theorem. The selected diary may be a
small protected subsystem, so `d_D` can remain below the daughter dimension
even after the total shell has crossed the usual Page dimension. A deadline
still needs a uniformity condition over diary embeddings or a dynamical
irreducibility condition.

## 4. Relation to information--disturbance

The same conclusion can be phrased through the standard information--
disturbance tradeoff: if `N` is close to a replacer, its complementary channel
to `X` is approximately reversible, with continuity losses controlled by the
usual square-root dependence. A channel from a `d`-dimensional system into an
`x`-dimensional system cannot transmit a maximally entangled `d`-level input
with entanglement fidelity above `x/d` when `x<d`. The direct Schmidt-rank
proof above avoids importing a particular convention for the continuity
constant.

See Kretschmann--Schlingemann--Werner, *The Information-Disturbance Tradeoff
and the Continuity of Stinespring's Representation*,
<https://arxiv.org/abs/quant-ph/0605009>. The information--disturbance bridge is
standard; equation (2.1) is the dimension-only specialization needed here.

## 5. What this closes and what it does not

Closed:

- C3b has a direct finite-dimensional capacity-cut bound under full-code
  diamond distance.
- The required hidden capacity is controlled by the declared diary dimension,
  not automatically by the total initial shell dimension.
- Approximate blindness cannot persist once the complete hidden complement is
  too small, with an explicit error floor.

Not closed:

- an optimal bound for every error convention or restricted reachable-state
  family;
- a bound using only the daughter dimension when hidden partners are present;
- a Page-time deadline for every diary or every embedding;
- the gravitational identification of the accessible radiation algebra;
- sufficient mixing or recovery once the lower bound becomes order one.

## 6. Steering consequence

C3b should be removed from the open conjecture queue and retained as a
standard lemma with explicit hypotheses. The next live item is C2: separate
charge-varying header information from fixed-charge private payload before
attempting the dressed-pump calculation.
