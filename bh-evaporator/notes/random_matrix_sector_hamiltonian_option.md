# Random-Matrix Sector Hamiltonian Option

## Purpose

This note records the analytical alternative to validating the concrete
matrix-free parent by long finite-size simulations.

Instead of asking whether a particular sparse Hamiltonian happens to generate a
typical shrinking map, define an ensemble of autonomous Hamiltonians for which
the one-step map is typical with high probability.  Then use standard Page,
decoupling, golden-rule, and typicality results to get the information-flow
package.

The target statement is:

```text
There exists a non-gravitational autonomous Hamiltonian ensemble whose
large-sector dynamics reproduces the black-hole evaporation package:
S ~ M^2, T ~ 1/M, P ~ M^-2, t_evap ~ M^3, local thermality, and
Page-like information flow.
```

This is weaker than a natural microscopic condensed-matter model.  It is
stronger than a hand-assigned channel or externally scheduled evaporation rule.

## Hilbert Space

Use a fixed total Hilbert space decomposed into core sectors and radiation:

```text
H_total = [direct sum_(n=n_min..n_max) H_n] tensor H_rad.
```

The core sectors have

```text
dim H_n = D_n = q^n,
S_n = log D_n = n log q,
M_n = alpha sqrt(n).
```

The radiation bath has one-particle modes labelled by `lambda`, with energies

```text
omega_lambda > 0
```

and density of modes

```text
J_rad(omega) ~ omega^p.
```

The 4D Schwarzschild target uses

```text
p = 2.
```

## Hamiltonian Ensemble

Take

```text
H_total = H_core + K_scr + H_rad + H_emit.
```

Core:

```text
H_core = direct sum_n H_n^0,
H_n^0 = M_n I_n + epsilon_n.
```

The internal energies `epsilon_n` have a smooth density of states in a thermal
window around `M_n`.  The only needed property is

```text
rho_n(M_n - omega) / rho_n(M_n)
  = exp[-beta_n omega + O(beta_n omega)^2 / S_n]
```

with

```text
beta_n = (S_n - S_(n-1)) / (M_n - M_(n-1)).
```

Scrambling:

```text
K_scr = direct sum_n K_n.
```

For the random-matrix option, choose each `K_n` from a unitarily invariant
ensemble, or from an expander-like random ensemble with known rapid mixing.  Its
role is to erase special basis information before emission:

```text
t_scr(n) << t_emit(n).
```

Emission:

```text
H_emit =
  g sum_n sum_(x=1..n) sum_lambda
    [ A_(n,x,lambda) tensor b_lambda^dagger + h.c. ].
```

Each

```text
A_(n,x,lambda): H_n -> H_(n-1)
```

is a random energy-filtered matrix.  In energy eigenbases,

```text
E[ A_(n,x,lambda;b a) ] = 0,
E[ |A_(n,x,lambda;b a)|^2 ]
  = (1 / D_(n-1)) F_n(E_(n,a) - E_(n-1,b) - omega_lambda).
```

Here `F_n` is a smooth detuning window.  The factor `1/D_(n-1)` keeps each
channel at fixed strength as the final core sector grows.

The sum over

```text
x = 1,...,n
```

is the area-sized emission strength.

## One-Step Map

Define the projected one-emission block:

```text
V_n(t) = P_(n-1,1rad) exp(-i H_total t) P_(n,0rad).
```

In the weak-coupling window,

```text
t_micro << t << t_two-emission,
```

the leading contribution is

```text
V_n(t) approx -i integral_0^t ds
  P_(n-1,1rad) exp[-i H_0(t-s)] H_emit exp[-i H_0 s] P_(n,0rad).
```

After the usual golden-rule time averaging, the emission probability operator is

```text
V_n^dagger V_n approx t G_n,
```

where

```text
G_n = sum_(x,lambda,b)
  |<n-1,b;lambda|H_emit|n,a;0>|^2
  delta(E_(n,a)-E_(n-1,b)-omega_lambda)
```

as an operator on `H_n`.

## Expected Isometry Property

For the random ensemble,

```text
E[G_n] = Gamma_n I_n.
```

The reason is unitary invariance inside `H_n`: no initial core direction is
distinguished.

The variance is suppressed by the number of independent final-state samples:

```text
N_eff(n) ~ n x [number of thermally allowed radiation modes]
           x [number of thermally allowed states in H_(n-1)].
```

So one expects concentration of the form

```text
||G_n / Gamma_n - I_n|| -> 0
```

with high probability as the thermally accessible dimensions grow.

Equivalently,

```text
V_n^dagger V_n = p_n I_n + small fluctuations,
p_n = Gamma_n t.
```

This is the one-step shrinking-isometry hypothesis, derived here as a
large-random-matrix property rather than imposed as a channel.

## Thermal Radiation Marginal

The golden-rule spectrum is

```text
dGamma_n/domega
  ~ n J_rad(omega) exp[S(M_n-omega)-S(M_n)] F_n(M_n,omega).
```

For smooth `F_n` and

```text
S(M) = gamma M^2,
```

we have

```text
S(M_n-omega)-S(M_n)
  = - beta_n omega + gamma omega^2.
```

For thermal quanta,

```text
omega ~ T_n ~ n^-1/2,
gamma omega^2 = O(1/n).
```

Therefore

```text
dGamma_n/domega
  ~ n omega^p exp(-beta_n omega) [1 + O(1/n)].
```

For `p=2`, the normalized variable

```text
x = beta_n omega
```

has

```text
P_n(x) dx ~ x^2 exp(-x) dx.
```

## Rate And Lifetime

The number rate is

```text
Gamma_n ~ n T_n^(p+1).
```

For the target `p=2`,

```text
Gamma_n ~ n T_n^3.
```

Since

```text
T_n ~ n^-1/2,
```

we get

```text
Gamma_n ~ n^-1/2.
```

Each event changes

```text
n -> n-1,
Delta M_n ~ n^-1/2.
```

So

```text
dn/dt ~ -n^-1/2,
P_n ~ Gamma_n Delta M_n ~ n^-1 ~ M^-2,
t_evap ~ n_0^(3/2) ~ M_0^3.
```

## Information Flow

Once the one-step maps are typical isometries,

```text
V_n: H_n -> H_(n-1) tensor R_n,
```

the information-flow claims are standard Page/decoupling consequences.

After `r` emissions,

```text
dim H_core = q^(n_0-r),
dim H_rad  ~ q^r
```

in the one-qubit-per-area-step idealization.  Page's theorem gives

```text
S_rad(r) ~ min[r log q, (n_0-r) log q]
```

up to order-one corrections and deviations from exact Haar typicality.

Early radiation is nearly uninformative before the Page crossing.  After the
crossing, newly emitted radiation is correlated with earlier radiation because
the remaining core no longer has enough Hilbert-space capacity to purify the
old radiation by itself.

## What Can Be Cited

The proof strategy uses known results:

```text
Fermi golden rule / weak-coupling limit:
  standard transition-rate derivation; Davies weak-coupling Markovian limit.

Typical subsystem entropy:
  Page, "Average Entropy of a Subsystem".

Information return and decoupling:
  Hayden and Preskill, "Black holes as mirrors".

Fast scrambling:
  Sekino and Susskind, "Fast Scramblers".

Thermal behavior in chaotic systems:
  canonical typicality and ETH literature.
```

The project-specific content is the Hamiltonian ensemble and the scaling chain:

```text
dim H_n=q^n, M_n~sqrt(n), area emission, p=2
  -> T~1/M, P~M^-2, t~M^3
  -> typical shrinking isometries
  -> Page-like flow.
```

## Pros

```text
1. B becomes mostly analytical.
2. The one-step typicality condition follows from ensemble symmetry and
   concentration, rather than from long simulations.
3. The Hamiltonian is autonomous and non-gravitational.
4. It cleanly separates the three mechanisms:
   entropy-energy law, area emission, scrambling.
5. It gives an existence result for a quantum Hamiltonian ensemble with the
   full black-hole-like phenomenology package.
```

## Cons

```text
1. The model is abstract.
2. The random matrices may look like they build in typicality.
3. It does not solve the natural microscopic-origin problem.
4. It is close in spirit to random-subsystem / Hayden-Preskill models, though
   with an explicit autonomous Hamiltonian and rate law.
5. A reviewer may still ask for finite-size examples to show the asymptotic
   concentration is visible before astronomically large dimensions.
```

## Relation To Option 1

Option 1 is the concrete matrix-free parent:

```text
sparse K_n;
sampled emission graph;
finite radiation modes;
direct time evolution.
```

Its role after Option 2 changes.  It no longer has to prove the full result
from scratch.  It should test whether a less idealized Hamiltonian lies near
the random-matrix ensemble's behavior.

Useful Option 1 checks:

```text
1. singular values of V_n^dagger V_n / p_n;
2. thermal radiation marginal in x=beta omega;
3. sensitivity to removing K_n;
4. sensitivity to eta=0 fixed-strength emission;
5. sensitivity to p != 2 bath exponent;
6. finite multi-step Page/early-late diagnostics where feasible.
```

If Option 1 passes, it strengthens the result by showing the ensemble behavior
survives in a sparse concrete parent.  If Option 1 fails at accessible sizes,
Option 2 still gives a coherent analytical existence result.

## Current Assessment

This is probably the best route for the abstract-Hamiltonian version of the
project.

It does not reach the most ambitious goal:

```text
a natural microscopic system where the sector architecture emerges.
```

It does reach a meaningful intermediate goal:

```text
an autonomous, non-gravitational Hamiltonian ensemble whose evaporation has the
black-hole thermodynamic rate law and Page-like information flow.
```

The next analytical task is to make the concentration statement precise enough:

```text
under what growth of D_n, thermal bandwidth, and radiation mode count does
||V_n^dagger V_n / p_n - I|| go to zero?
```

