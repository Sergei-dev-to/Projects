# Autonomous Sector-Parent Build Spec

## Goal

Test the autonomous parent of the successful sector-Hamiltonian model.

The target result is one time-independent Hamiltonian whose direct evolution

```text
|psi(t)> = exp(-i H_total t) |psi(0)>
```

produces, in the same run:

```text
sector shrinkage;
thermal hard-radiation flux;
accelerating evaporation for the square-root mass law;
failure of the same acceleration for a linear mass-law control;
core/radiation entanglement;
early/late radiation correlations.
```

This is the bridge between the successful sector-rate/isometry results and a
single autonomous Hamiltonian.

## Hamiltonian

Use

```text
H_total = H_core + K_scramble + H_rad + H_int .
```

Core:

```text
H_core |n,a; m> = E_(n,a) |n,a; m>
E_(n,a) = M_n + epsilon_(n,a)
dim B_n = q^n
```

Mass-law cases:

```text
sqrt:   M_n = alpha sqrt(n)
linear: M_n = alpha n
```

Scrambling:

```text
K_scramble = direct sum_n K_n
```

where `K_n` is sparse random or expander-like and acts only inside sector
`B_n` at fixed radiation occupation.

Radiation:

```text
H_rad = sum_lambda omega_lambda b_lambda^\dagger b_lambda .
```

Emission:

```text
H_int =
  g sum_(n,x,a,b,lambda)
    X_(n,b,a) F(E_(n,a) - E_(n-1,b) - omega_lambda)
    |n-1,b; m + lambda><n,a; m|
  + h.c.
```

Here `x` labels the independent horizon emitters in sector `n`.  The target
area-emission Hamiltonian has

```text
x = 1,...,n
```

with fixed per-emitter coupling.  In the matrix-free implementation this can be
compressed into a sampled transition graph by using

```text
g_n = g (n / n_ref)^(1/2),
```

so the rate-level emission strength scales as `n`.  The fixed-strength control
sets the exponent to zero.

`F` is a detuning filter.  The radiation modes are chosen in bins of

```text
x = beta_n omega
```

so the measured flux can be compared to

```text
P(x) proportional to x^p exp(-x).
```

For the 4D Schwarzschild target, the outgoing radiation has three spatial
dimensions, so

```text
p = 2.
```

Other values of `p` are useful bath-dimension controls.

## Basis And Truncation

Basis states:

```text
|n, a, occ>
```

where

```text
n          = core sector
a          = core-state index in B_n
occ        = truncated radiation occupation bitmask
```

Use a fermionic/hard-core radiation truncation at first:

```text
at most one quantum per radiation mode;
at most k emitted quanta total.
```

This is sufficient for testing finite evaporation trajectories.  Bosonic mode
multiplicity can be added later if needed.

Initial state:

```text
n = n_max;
empty radiation;
Haar or microcanonical packet inside B_(n_max).
```

## Core Spectrum

Start with the successful energy-resolved sector spectrum:

```text
rho_n(epsilon) proportional to exp(beta_n epsilon)
```

over a window of order

```text
width_x * T_n .
```

This deliberately uses the sector model that already passed the hard-spectrum
and acceleration tests.  The goal is to test the autonomous parent, not search
for a natural microscopic core in this step.

## Matrix-Free Implementation

Do not build the full sparse Hamiltonian.

Implement

```text
y = H_action(psi)
```

as the sum of four structured actions:

```text
H_core action:
  diagonal energy multiplication

K_scramble action:
  sparse intra-sector graph edges at fixed radiation occupation

H_rad action:
  diagonal radiation energy multiplication

H_int action:
  energy-filtered transitions between n and n-1 with one radiation mode added
  or removed
```

Wrap `H_action` as a SciPy `LinearOperator` for Krylov evolution.

The first implementation should remain CPU matrix-free.  GPU support is useful
only after the action kernel is stable.

## Observables

Measure directly from the same evolved state:

```text
sector probabilities P(n,t);
mean sector <n>(t);
core energy;
radiation energy;
emitted power dE_rad/dt;
band-resolved outward flux;
hard spectrum in x = beta omega;
core/radiation von Neumann entropy where feasible;
core/radiation Renyi-2 entropy;
early/late radiation mutual information where feasible.
```

For larger runs, exact entropy may be replaced by:

```text
sparse Gram entropy on reachable support;
Renyi-2 from purity estimates;
trajectory-sampled entropy bounds.
```

Flux should be preferred over final occupation when diagnosing the spectrum,
because finite radiation spaces can reabsorb or redistribute emitted quanta.

## Controls

Run at least:

```text
sqrt mass law;
linear mass-law control;
no-scrambling K_n = 0;
fixed-strength emission control;
changed bath exponent p;
small radiation-sector control;
different seeds for K_n and X_n.
```

The linear mass-law control should keep the hard spectrum similar while
removing the black-hole-like acceleration.  That is the important contrast.
The fixed-strength emission control checks that the Hawking-rate scaling is
coming from area-sized emission strength rather than only from the sector DOS.
The bath-exponent control checks that the power law is tied to ordinary
radiation phase space rather than a fitted time dependence.

## First Runnable Targets

Smoke test:

```text
n = 3..5
q = 2
k = 2 emitted quanta
m = 8..12 radiation modes
```

Meaningful first target:

```text
n = 4..7
q = 2
k = 3 emitted quanta
m = 16..24 radiation modes
```

Large-compute target:

```text
n = 5..9 or 5..10
q = 2
k = 4..6 emitted quanta
m = 30..60 radiation modes
```

## Success Criteria

The parent Hamiltonian is a success if one autonomous run shows:

```text
1. H_total energy conserved to numerical precision.
2. Mean sector decreases over the diagnostic window.
3. Radiation energy increases over the same window.
4. Hard flux spectrum is close to x^p exp(-x), ideally TV < 0.1--0.2.
5. Square-root mass law accelerates over the window.
6. Linear mass-law control remains flat or decelerating.
7. Scrambling control shows why K_n matters.
8. Core/radiation entropy grows and, in small complete runs, begins to turn over.
9. Early/late radiation mutual information is measurable after enough emissions.
```

If the run gets 1--7 but not 8--9 because of entropy scaling, it is still a
strong autonomous thermodynamic/spectral result.

If it gets 1--3 but not 4--7, the autonomous parent has not reproduced the
successful sector model.

## Main Risks

1. Radiation recurrence:
   too few modes or too small a radiation truncation causes reabsorption.

2. Coherent Rabi cycling:
   coupling `g` too large prevents the golden-rule regime.

3. No visible evaporation:
   coupling `g` too small, or detuning filter too narrow.

4. Entropy computation:
   exact reduced-density calculations can dominate runtime.

5. Endpoint distortion:
   smallest sectors may spoil thermal-spectrum diagnostics.

The first implementation should prioritize flux, power, and sector evolution.
Entropy diagnostics can be added after the autonomous thermodynamic/spectral
behavior is visible.
