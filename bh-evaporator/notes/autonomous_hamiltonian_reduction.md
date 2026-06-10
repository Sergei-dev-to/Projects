# Autonomous Hamiltonian Candidate And Reduction

## Purpose

The sector-Hamiltonian model now has three successful ingredients:

```text
energy-resolved core sectors
intra-sector Hamiltonian scrambling
golden-rule shrinkage transitions
```

This note states the corresponding autonomous Hamiltonian and explains why its
weak-coupling/secular limit is the effective model already tested.

## Candidate Hamiltonian

The autonomous model is:

```text
H_total = H_core + K_scramble + H_rad + H_int
```

Core:

```text
H_core = direct sum_n H_n
H_n |n,a> = E_{n,a} |n,a>
E_{n,a} = M_n + epsilon_{n,a}
dim H_n = q^n
```

Black-hole-like mass law:

```text
M_n = alpha sqrt(n)
S_micro(n) = n log q
```

Scrambling:

```text
K_scramble = direct sum_n K_n
```

where `K_n` is an intra-sector Hamiltonian. Tested choices in the effective
model include:

```text
dense random symmetric K_n
expander-adjacency K_n
sparse random graph K_n
```

Radiation:

```text
H_rad = sum_alpha omega_alpha b_alpha^\dagger b_alpha
```

Interaction:

```text
H_int =
  g sum_{n,a,b,alpha}
    C_{n,b,a,alpha}
    |n-1,b><n,a| b_alpha^\dagger
  + h.c.
```

The coefficient `C` contains the shrinkage matrix element and a smooth
energy-window factor:

```text
C_{n,b,a,alpha}
  = <b,n-1|X_n|a,n> F(E_{n,a} - E_{n-1,b} - omega_alpha)
```

where `F` is peaked near zero detuning.

## Weak-Coupling Limit

Start in a core state with empty radiation. For small `g`, transitions from:

```text
|n,a; 0_rad>
```

to:

```text
|n-1,b; 1_alpha>
```

occur at the golden-rule rate:

```text
Gamma_{n,a -> n-1,b,alpha}
  = 2 pi g^2
    |<b,n-1|X_n|a,n>|^2
    |F(E_{n,a} - E_{n-1,b} - omega_alpha)|^2
    rho_rad(omega_alpha)
```

After summing over radiation modes in an energy bin, this gives the sector
transition rate used in the effective model:

```text
Gamma_{n,a -> n-1,b}
  proportional to |<b,n-1|X_n|a,n>|^2 omega^p
```

with:

```text
omega = E_{n,a} - E_{n-1,b}
```

The intra-sector Hamiltonian gives:

```text
rho_n(t + tau) = exp(-i K_n tau) rho_n(t) exp(i K_n tau)
```

At the population level in the `H_n` energy basis:

```text
p_n' = |exp(-i K_n tau)|^2 p_n
```

This is exactly the Hamiltonian mixing map tested in:

```text
sim/sector_hamiltonian_scrambling.py
```

So the effective sector model is the weak-emission, secular, stroboscopic
limit of `H_total`.

## What The Autonomous Model Must Reproduce

The effective tests say that the autonomous Hamiltonian should satisfy:

```text
1. K_n mixes each occupied sector before emission traps the state in low-rate
   energy regions.

2. H_int couples energy-resolved sector transitions to radiation modes with
   the correct density of states.

3. The square-root mass law yields accelerating emitted power.

4. The linear mass law comparison remains near flat or mildly decelerating.

5. The hard radiation spectrum is close to thermal in x = beta omega.
```

## Tiny Direct Test

A tiny direct simulation is implemented in:

```text
sim/tiny_autonomous_sector_evaporator.py
```

It keeps:

```text
n = 2,3,4
dim H_n = 2^n
six radiation modes
at most two emitted quanta
```

and evolves:

```text
|psi(t)> = exp(-i H_total t) |psi(0)>
```

This is a smoke test for the autonomous embedding. The finite radiation bath is
too small to support a clean long evaporation curve; coherent reabsorption and
recurrences appear at longer times.

The tiny test checks:

```text
H_total energy conservation,
radiation population growth,
sector shrinkage,
rough hard-spectrum shape,
effect of K_scramble on the trajectory.
```

## Current Status

Candidate autonomous Hamiltonian:

```text
defined
```

Weak-coupling reduction:

```text
clear
```

Tiny autonomous smoke test:

```text
implemented
```

Full autonomous evaporation curve:

```text
open
```

The next major step would require a larger radiation bath or an absorbing
continuum approximation, so emitted quanta remain in radiation on the timescale
of the diagnostic.
