# Microcanonical Emission Weights

## Purpose

Attack the weakest remaining entry:

```text
F7: emission rates from dynamics or matrix elements
```

The previous erosion-channel tests chose hard probabilities by hand:

```text
p_h ~ exp(-epsilon_h / T_L).
```

This note derives the thermal factor at the rate-equation level from the
finite-gauge droplet entropy curve.

## Setup

For the finite-group gauge droplet:

```text
S_L = L^2 log q
M_L = 4 sigma L.
```

Treat the droplet trajectory as a smooth curve:

```text
L = M / (4 sigma).
```

Then:

```text
S(M) = (M / 4 sigma)^2 log q.
```

The microcanonical inverse temperature is:

```text
beta(M) = dS/dM
        = M log q / (8 sigma^2)
        = L log q / (2 sigma).
```

So:

```text
T_L = 2 sigma / (L log q).
```

This is the same continuum temperature already obtained from the thermodynamic
derivative.

## Emission Weight

Suppose the droplet emits a hard quantum of energy `omega` into the exterior.
For weak coupling and approximately flat matrix elements, the transition weight
is proportional to:

```text
Gamma_L(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

Expanding the entropy:

```text
S(M - omega) - S(M)
  = - beta omega + (log q / 16 sigma^2) omega^2.
```

Thus:

```text
exp[S(M - omega) - S(M)]
  = exp(- beta omega) * exp[(log q / 16 sigma^2) omega^2].
```

For typical emitted quanta:

```text
omega ~ T ~ 1/L.
```

The correction term scales as:

```text
(log q / 16 sigma^2) omega^2 ~ O(1/L^2).
```

So the thermal Boltzmann factor is not inserted. It is the leading term in the
microcanonical ratio of final to initial droplet state counts.

## 2D Bath Power

For a two-dimensional exterior bath, the power per boundary length has the
thermal scaling:

```text
int d omega omega^2 exp(-beta omega) ~ T^3.
```

Multiplying by boundary length:

```text
B_L = 4L
```

gives:

```text
P_L ~ B_L T_L^3
    ~ L * (1/L)^3
    ~ 1/L^2.
```

Since:

```text
M_L ~ L,
```

this gives:

```text
dM/dt ~ -1/M^2.
```

The acceleration law therefore follows from:

```text
microcanonical state-count ratio
+ 2D bath phase space
+ boundary emitting length.
```

## Finite-Size Diagnostic

Script:

```text
sim/microcanonical_emission_weights.py
```

Output:

```text
sim/data/microcanonical_emission_weights.csv
```

Command:

```text
python sim/microcanonical_emission_weights.py
```

The script compares:

```text
exact microcanonical weight:
  exp[S(M - omega) - S(M)]

Boltzmann approximation:
  exp(-beta omega)
```

using:

```text
x = beta omega.
```

Representative output for `q = 2`, `sigma = 1`, 2D bath:

```text
L   beta     T        rel@x=1 rel@x=3 rel@x=5 P_exact/P_B  M^2 P_exact
 2    0.693   1.4427   1.0944   2.2513   9.5278     2.8184    7924.0178
 3    1.040   0.9618   1.0409   1.4343   2.7234     1.7855    5414.6614
 4    1.386   0.7213   1.0228   1.2249   1.7569     1.3311    4036.6121
 8    2.773   0.3607   1.0057   1.0520   1.1513     1.0660    3232.6474
36   12.477   0.0801   1.0003   1.0025   1.0070     1.0031    3041.8312
40   13.863   0.0721   1.0002   1.0020   1.0057     1.0025    3040.0644
```

The exact microcanonical weights approach the Boltzmann weights rapidly at
large `L`. The power diagnostic approaches:

```text
M^2 P = constant.
```

For the Boltzmann approximation with the normalization used in the script:

```text
M^2 P -> 1024 / (log q)^3.
```

For `q = 2`, this is approximately:

```text
3075.
```

The exact finite-size values approach that constant from above.

## What This Fixes

This removes one arbitrary ingredient from the hard channel.

Before:

```text
thermal hard probabilities were chosen.
```

Now:

```text
thermal hard weights follow from the microcanonical state-count ratio.
```

The hard spectrum is therefore tied to the same entropy curve that produced:

```text
S ~ M^2
T ~ 1/M
C < 0.
```

## What This Does Not Yet Fix

This is still not the full Hamiltonian evaporator.

Remaining gaps:

```text
1. Matrix elements are assumed flat or slowly varying.
2. The bath spectral density is inserted as ordinary 2D radiation phase space.
3. The derivation is rate-equation / golden-rule level, not a unitary collision
   Hamiltonian.
4. The discrete shell erosion map is still separate from the continuous hard
   quantum spectrum.
5. Greybody factors or boundary selection rules are not derived.
```

The important caveat is the shell issue:

```text
L -> L - 1 releases Delta M = 4 sigma.
```

But a typical hard quantum has:

```text
omega ~ T_L ~ 1/L.
```

So a full shell erosion should be viewed as a coarse-grained process containing
many soft/hard emission events, or as a Stinespring step whose hard subsystem
samples the microcanonical spectrum while the remaining shell energy and
information are carried by soft/bath degrees.

This note derives the hard energy weights, not the complete shell-level
Hamiltonian.

## Consequence For F7

The edge-tension droplet's F7 status should remain:

```text
P
```

but the reason is stronger:

```text
thermal hard weights are derived at the microcanonical rate level;
microscopic matrix elements and the full unitary emission Hamiltonian are still
not derived.
```

So F7 has moved from:

```text
chosen thermal probabilities
```

to:

```text
entropy-derived thermal weights, with assumed smooth matrix elements.
```

That is a real improvement, but not a `Y`.

