# Analytic Sector Evaporation Result

## Question

For the abstract autonomous sector Hamiltonian,

```text
H_total = H_core + K_scr + H_rad + H_emit,
```

does the black-hole-like evaporation package follow analytically from the
sector structure, or does a key ingredient still have to be supplied?

## Setup

Take core sectors labelled by an area variable `n`:

```text
dim H_core(n) = q^n,
S(n) = n log q,
M_n = alpha sqrt(n).
```

Then

```text
n = M^2 / alpha^2,
S(M) = gamma M^2,
gamma = log(q) / alpha^2.
```

The microcanonical inverse temperature is

```text
beta(M) = dS/dM = 2 gamma M,
T(M) = 1 / (2 gamma M).
```

The heat capacity is

```text
C = dM/dT = -1 / (2 gamma T^2) = -2 gamma M^2 < 0.
```

So the entropy-energy input immediately gives:

```text
T ~ 1/M,
C < 0.
```

## Golden-Rule Reduction

Use an emission Hamiltonian of the form

```text
H_emit = lambda sum_x int d omega [
            O_x(omega) b_x^dagger(omega) + h.c.
         ].
```

Here:

```text
x labels independent emitting channels;
b_x^dagger(omega) creates an outgoing radiation quantum;
O_x(omega) lowers the core energy by omega.
```

For a microcanonical initial core state near energy `M`, weak emission, and
fast in-sector mixing, Fermi's golden rule gives

```text
d Gamma / d omega
  = 2 pi lambda^2 A_emit(M) J_rad(omega)
      F(M, omega)
      exp[S(M - omega) - S(M)].
```

where:

```text
A_emit(M) = number of effectively independent emission channels;
J_rad(omega) = radiation density/phase-space factor;
F(M, omega) = smooth average matrix-element form factor.
```

The density-of-states ratio is

```text
S(M - omega) - S(M)
  = - beta omega + gamma omega^2.
```

For typical Hawking quanta,

```text
omega ~ T ~ 1/M,
```

so

```text
gamma omega^2 ~ O(1/M^2).
```

Thus

```text
exp[S(M - omega) - S(M)]
  = exp(-beta omega) [1 + O(1/M^2)].
```

This is the first positive result:

```text
local thermality follows from the core density-of-states ratio.
```

## Discrete Area Step

For one area-qubit decrement,

```text
Delta M_n = M_n - M_{n-1}
          = alpha(sqrt(n) - sqrt(n-1))
          = alpha / (2 sqrt(n)) + O(n^-3/2).
```

The dimension ratio is

```text
dim H_core(n-1) / dim H_core(n) = q^-1.
```

The Boltzmann exponent for this transition is

```text
beta_n Delta M_n
  = [2 log(q) sqrt(n) / alpha] [alpha / (2 sqrt(n))]
  = log(q) + O(1/n).
```

Therefore

```text
exp(-beta_n Delta M_n) = q^-1 [1 + O(1/n)].
```

So an `n -> n-1` transition emits an energy of order `T` and has exactly the
expected entropy penalty at large `n`. This means one area-qubit loss can be a
microscopic Hawking-scale event in the sector model.

## Power Law

The DOS ratio gives the spectrum shape. It does not fix the total rate.

Assume a massless radiation bath with `d` spatial dimensions:

```text
J_rad(omega) ~ omega^(d-1).
```

In the code this exponent is called `ohmic_power`:

```text
p = ohmic_power = d - 1.
```

Assume smooth matrix elements over the thermal band:

```text
F(M, omega) = F_0(M) [1 + O(omega/M)].
```

Then the number emission rate scales as

```text
Gamma(M) ~ A_emit(M) F_0(M) T^d.
```

The emitted power scales as

```text
P(M) ~ A_emit(M) F_0(M) T^(d+1).
```

Since

```text
T ~ 1/M,
```

we have

```text
P(M) ~ A_emit(M) F_0(M) M^-(d+1).
```

For a Schwarzschild-like 4D target, the exterior bath has `d = 3`.
Therefore the target bath exponent is

```text
p = 2.
```

To obtain

```text
P(M) ~ M^-2,
```

we need

```text
A_emit(M) F_0(M) ~ M^2.
```

This is the second result:

```text
the Hawking power law requires an area-sized emission strength.
```

In the horizon-qubit sector model this is natural if the emission Hamiltonian is
a sum over area qubits:

```text
A_emit(M) ~ n ~ M^2.
```

Then

```text
Gamma(M) ~ M^2 T^3 ~ 1/M,
<omega> ~ T ~ 1/M,
P(M) ~ Gamma <omega> ~ 1/M^2.
```

The lifetime is

```text
tau ~ int dM M^2 ~ M_0^3.
```

## Negative Result

The entropy-energy law alone is not enough.

If the Hamiltonian has only `O(1)` effective emission channels,

```text
A_emit(M) F_0(M) ~ const,
```

then for a 3D radiation bath:

```text
P(M) ~ T^4 ~ M^-4.
```

That is not Schwarzschild evaporation.

If the radiation bath or matrix-element form factor has a different scaling,
the power law changes accordingly. In general,

```text
P(M) ~ M^a M^-(d+1)
```

when

```text
A_emit(M) F_0(M) ~ M^a.
```

The Schwarzschild exponent requires

```text
a = d - 1.
```

For the physical 3D bath, this is exactly an area law:

```text
a = 2.
```

Equivalently, write the emission strength as

```text
A_emit(M) F_0(M) ~ n^eta.
```

For the square-root mass law, `M ~ sqrt(n)` and `T ~ n^-1/2`, so

```text
P(n) ~ n^eta T^(p+2)
     ~ n^[eta - (p+2)/2],
P(M) ~ M^[2 eta - p - 2].
```

The target values are

```text
eta = 1,
p = 2,
P(M) ~ M^-2.
```

The fixed-strength emission control has

```text
eta = 0,
p = 2,
P(M) ~ M^-4.
```

So fixed-strength emission can still accelerate as the core shrinks.  Its
failure is the power-law exponent and lifetime, not merely the presence or
absence of acceleration.

For the linear mass-law control, `M ~ n` and `T` is constant.  With area
emission,

```text
P(n) ~ n,
P(M) ~ M.
```

That power decreases as the system shrinks, so the linear control should fail
the black-hole-like rate evolution once the finite-radiation transient is under
control.

## Scrambling And Page Behavior

The analytic thermodynamic derivation does not require full fast scrambling.
It requires enough in-sector mixing that the emission operators sample typical
core states rather than a special basis.

A stronger information-flow result needs the hierarchy

```text
t_scr << t_emit << t_evap.
```

Under this condition, the core after each emission is approximately typical in
the remaining sector. Then Page's dimension-counting logic applies to the
core+radiation pure state:

```text
S_rad(t) approximately rises while dim H_rad < dim H_core,
S_rad(t) approximately falls after dim H_rad > dim H_core.
```

Late radiation must then be correlated with early radiation because the final
radiation state is pure.

This is a conditional analytic result:

```text
fast in-sector mixing + shrinking core capacity imply Page-like information flow.
```

It is not a substitute for early/late diagnostics. The numerics should still
check radiation mutual information or second-Renyi versions.

## Combined Verdict

Positive:

```text
1. S(M) ~ M^2 gives T ~ 1/M.
2. The heat capacity is negative.
3. The DOS ratio gives a thermal emission spectrum up to O(1/M^2) corrections.
4. An n -> n-1 area step emits energy O(T) and has the correct entropy penalty.
5. With area-sized emission strength into a 3D bath, the rate law is
   Gamma ~ 1/M, P ~ 1/M^2, tau ~ M_0^3.
6. With fast in-sector mixing, Page-like information transfer follows by
   dimension counting and typicality.
```

Negative:

```text
1. S(M) ~ M^2 alone does not determine the total rate.
2. A Hamiltonian with only O(1) emission strength gives the wrong power law.
3. The area-sized coupling must be present in H_emit or derived from a
   microscopic boundary/horizon interaction.
4. Scrambling remains an assumption unless K_scr is shown to produce the
   required mixing time.
```

## What This Means For The Model

The abstract sector Hamiltonian can produce the full thermodynamic evaporation
package if `H_emit` has the form

```text
H_emit = sum over area-sized local emitters
```

with smooth matrix elements and ordinary 3D radiation phase space.

The minimal successful sector model is therefore:

```text
dim H_core(n) = q^n;
M_n = alpha sqrt(n);
K_scr mixes each n sector faster than emission;
H_emit is a sum over n horizon-qubit emission operators;
H_rad has 3D massless radiation phase space;
emission is weak enough for golden-rule dynamics.
```

This is a positive analytic result, with one explicit condition:

```text
the emission strength must scale with area.
```

That condition is physically natural for horizon qubits, but it is still a
condition on the Hamiltonian. It should be tested by comparing:

```text
area-scaled H_emit;
O(1)-scaled H_emit;
altered bath dimension;
scrambling removed.
```

## Discrete Rate Equation

The continuous power-law result can be written directly in the sector variable
`n`.  This is the useful form for the autonomous parent.

For the target model,

```text
M_n = alpha sqrt(n),
T_n = 1 / beta_n ~ alpha / [2 log(q) sqrt(n)].
```

One sector step emits

```text
Delta M_n = M_n - M_(n-1)
          = alpha / [2 sqrt(n)] + O(n^-3/2)
          ~ T_n.
```

The golden-rule number rate is

```text
Gamma_n ~ n^eta T_n^(p+1).
```

Here `eta` is the rate-level area-emission exponent and `p` is the radiation
phase-space exponent in

```text
dGamma/domega ~ omega^p exp(-beta omega).
```

For the 4D Schwarzschild target,

```text
eta = 1,
p = 2.
```

Therefore

```text
Gamma_n ~ n T_n^3 ~ n n^-3/2 ~ n^-1/2.
```

Since each emission lowers `n` by one,

```text
dn/dt ~ - Gamma_n ~ - n^-1/2.
```

Integrating gives

```text
t_evap(n_0) ~ int_0^n0 sqrt(n) dn ~ n_0^(3/2).
```

Because `M_0 ~ sqrt(n_0)`,

```text
t_evap ~ M_0^3.
```

The power follows from

```text
P_n ~ Gamma_n Delta M_n
    ~ n^-1/2 n^-1/2
    ~ n^-1
    ~ M^-2.
```

The fixed-strength emission control has `eta = 0`, so

```text
Gamma_n ~ T_n^3 ~ n^-3/2,
P_n ~ n^-2 ~ M^-4,
t_evap ~ n_0^(5/2) ~ M_0^5.
```

The linear mass-law control has `M_n ~ n` and constant `T_n`.  With area
emission,

```text
Gamma_n ~ n,
P_n ~ n ~ M.
```

Its power decreases as the object shrinks.  That is the discrete control
against the square-root mass law.

## Weak-Coupling And Scrambling Hierarchy

The calculation uses ordinary golden-rule reasoning: weak coupling to a large
set of final radiation states gives transition rates proportional to squared
matrix elements times final-state density.  In this note we only need the
standard consequence, not a new derivation of Fermi's golden rule.

The hierarchy should be stated as

```text
t_micro << t_scr(n) << t_emit(n) << t_evap(n).
```

where

```text
t_micro     = microscopic time set by internal level spacings/couplings;
t_scr(n)   = time for K_n to mix typical states inside H_core(n);
t_emit(n)  = 1 / Gamma_n;
t_evap(n)  = n / Gamma_n.
```

For the target rate,

```text
t_emit(n) ~ sqrt(n),
t_evap(n) ~ n^(3/2).
```

So the hierarchy asks for

```text
t_scr(n) << sqrt(n)
```

in sector units.  If `K_n` is a fast scrambler with logarithmic scrambling
time, this condition is parametrically satisfied at large `n`.

What this buys us:

```text
1. The core state re-equilibrates before the next emission.
2. Emission matrix elements sample typical states rather than a special basis.
3. The step map from H_core(n) to H_core(n-1) x H_rad_step can be approximated
   by a typical isometry over the thermally allowed band.
```

Known literature covers the ingredients: fast scrambling as a black-hole
expectation was formulated by Sekino and Susskind; Hayden and Preskill use
rapid mixing/random-subsystem logic for information return; ETH and canonical
typicality give standard ways to justify local thermal behavior in chaotic
many-body systems.

## One-Step Map From The Autonomous Hamiltonian

Define the projected one-emission block

```text
V_n(t) = P_(n-1,1rad) exp(-i H_total t) P_(n,0rad).
```

This maps

```text
V_n(t): H_core(n) -> H_core(n-1) x H_rad,1.
```

In the weak-coupling regime, take `t` long compared to microscopic oscillation
times but short compared to the time for two emissions.  To second order in
`H_emit`, the emission probability out of an initial state `|i,n>` is governed
by the golden-rule operator

```text
G_n = V_n^dagger V_n / t
```

with matrix elements controlled by

```text
sum_(b,lambda)
  |<n-1,b;lambda| H_emit |n,i;0>|^2
  delta(E_(n,i) - E_(n-1,b) - omega_lambda).
```

If `K_n` mixes the core before emission and the emission operators are
statistically unbiased in the scrambled basis, then the off-diagonal terms in
`G_n` self-average and the diagonal terms concentrate around a common value:

```text
G_n = Gamma_n I_n + small fluctuations.
```

Equivalently,

```text
V_n^dagger V_n = p_n I_n + small fluctuations,
p_n = Gamma_n t.
```

This is the isometry condition needed by the Page/decoupling argument.  It is
not a new theorem; it is the standard golden-rule/random-matrix concentration
expectation applied to this sector Hamiltonian.

The emitted-energy marginal follows from the same golden-rule expression.  For
a smooth emission form factor,

```text
dGamma_n/domega
  ~ n^eta omega^p exp[S(M_n-omega)-S(M_n)].
```

Using `S(M)=gamma M^2`,

```text
S(M_n-omega)-S(M_n)
  = - beta_n omega + gamma omega^2.
```

For thermal quanta `omega ~ T_n`, the correction is `O(1/n)`, so

```text
dGamma_n/domega ~ n^eta omega^p exp(-beta_n omega) [1 + O(1/n)].
```

For the 4D Schwarzschild target, `p=2`, and in the variable

```text
x = beta_n omega
```

the normalized one-step radiation spectrum is

```text
P_n(x) dx ~ x^2 exp(-x) dx
```

up to finite-`n` and form-factor corrections.

Thus the first two properties of `V_n` can be established analytically under
standard assumptions:

```text
1. V_n^dagger V_n approximately p_n I_n
   from weak coupling plus scrambled/random emission matrix elements.

2. The radiation marginal is thermal
   from final-state DOS ratio plus 3D phase space.
```

The remaining nontrivial check is quantitative:

```text
How small are the fluctuations in V_n^dagger V_n and in the radiation marginal
for the finite sectors we can simulate?
```

## Page-Like Information Flow

Assume the total evolution is unitary and the core is sufficiently scrambled
between emissions.  After `r` emission steps, the state lies approximately in

```text
H_core(n_0 - r) x H_rad(r),
```

with

```text
dim H_core(n_0 - r) = q^(n_0-r),
dim H_rad(r)        ~ q^r
```

for one qubit-equivalent of radiation per area step.  More generally, replace
`q^r` by the effective dimension of the emitted radiation records.

For a typical pure state on a bipartite Hilbert space, Page's theorem says the
smaller subsystem is nearly maximally mixed.  Therefore the radiation entropy
obeys the Page-counting estimate

```text
S_rad(r) ~ min[r log q, (n_0-r) log q]
```

up to order-one Page corrections and deviations from exact typicality.

The Page time is therefore

```text
r_Page ~ n_0 / 2
```

in the equal-qubit idealization.  Before this point, early radiation alone
looks nearly thermal and uninformative about the precise initial state.  After
this point, newly emitted radiation must be correlated with earlier radiation,
because the remaining core has less Hilbert-space capacity than the radiation
already emitted.

This is the information-flow result we can cite rather than derive from
scratch:

```text
Page theorem + rapidly mixing unitary evaporation -> Page-like radiation
entropy and early/late correlations.
```

What is specific to this model is the shrinking capacity

```text
dim H_core(n) = q^n
```

and the rate law that tells us how quickly the system moves through `r` or
`n`.

## Literature Inventory

The calculation above leans on standard results at four points:

```text
Page entropy and Page curve:
  Don Page, "Average Entropy of a Subsystem"
  https://arxiv.org/abs/gr-qc/9305007

Information in black-hole radiation:
  Don Page, "Information in Black Hole Radiation"
  https://arxiv.org/abs/hep-th/9306083

Time dependence of Hawking-radiation entropy:
  Don Page, "Time Dependence of Hawking Radiation Entropy"
  https://arxiv.org/abs/1301.4995

Rapid mixing / Hayden-Preskill information return:
  Hayden and Preskill, "Black holes as mirrors"
  https://arxiv.org/abs/0708.4025

Fast scrambling:
  Sekino and Susskind, "Fast Scramblers"
  https://arxiv.org/abs/0808.2096

Canonical typicality:
  Goldstein, Lebowitz, Tumulka, and Zanghi, "Canonical Typicality"
  https://arxiv.org/abs/cond-mat/0511091

ETH / chaotic thermalization:
  D'Alessio, Kafri, Polkovnikov, and Rigol, "From quantum chaos and
  eigenstate thermalization to statistical mechanics and thermodynamics"
  https://arxiv.org/abs/1509.06411

Black-hole particle emission rates and greybody factors:
  Don Page, "Particle emission rates from a black hole: Massless particles
  from an uncharged, nonrotating hole", Phys. Rev. D 13, 198-206 (1976).
```

The part not supplied by those references is the assembled sector-Hamiltonian
claim:

```text
dim H_core(n)=q^n,
M_n=alpha sqrt(n),
area-summed H_emit,
3D radiation phase space,
fast K_n
```

imply the black-hole-like thermodynamic rate package and, under standard
typicality assumptions, Page-like information flow.

## Implementation Audit

The matrix-free autonomous parent initially used a fixed number of sampled
emission targets per source state and radiation mode.  In golden-rule terms,
that corresponds to

```text
A_emit(M) F_0(M) ~ O(1)
```

unless an explicit area factor is included in the matrix-element variance.
That version can test energy conservation, DOS-ratio thermality, and the need
for scrambling, but it is not the asymptotic Hawking-rate Hamiltonian.

The parent Hamiltonian now has an emission-area exponent:

```text
g_n = g (n / n_ref)^(eta / 2)
```

at matrix-element level.  Therefore the rate-level emission strength scales as

```text
|g_n|^2 ~ n^eta.
```

The target horizon-emission case is

```text
eta = 1.
```

This is the compressed version of a Hamiltonian with `n` independent horizon
emitters and fixed per-emitter coupling.  The fixed-strength control is

```text
eta = 0.
```

The next decisive numerical comparison is therefore:

```text
sqrt mass law + scrambling + eta = 1 + p = 2;
linear mass law + scrambling + eta = 1 + p = 2;
sqrt mass law + no scrambling + eta = 1 + p = 2;
sqrt mass law + scrambling + eta = 0 + p = 2;
bath-dimension control with p != 2.
```

Expected outcome if the analytic picture is correct:

```text
1. eta = 1 radiates parametrically faster than eta = 0 at the same initial n.
2. sqrt + eta = 1 should show the Hawking direction of rate evolution.
3. linear + eta = 1 should fail the same acceleration because T is constant.
4. no scrambling should degrade the thermal flux and information-flow tests.
5. p != 2 should change the power-law exponent in the predicted way.
6. eta = 0 may still accelerate, but with P(M) ~ M^-4 rather than M^-2.
```

The previous k=3 run did not include this area-emission control and used
`p = 1`.  Its main lesson is therefore narrower: finite radiation space and
scrambling diagnostics worked well enough to continue, but the run did not
decide the full 4D Hawking-rate question.
