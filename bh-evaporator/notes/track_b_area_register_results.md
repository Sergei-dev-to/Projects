# Track B Area-Register Kill-Test Results

## Synthesis note

The Track B result is summarized in the broader project synthesis:

```text
notes/project_synthesis_after_tracks.md
```

## Question

Can an entropy-correct area register produce accelerating evaporation when
rates are derived from concrete Hamiltonian blocks and shrinkage-operator
matrix elements, rather than assigned by hand?

## Model

Script:

```text
sim/area_register_rate_scan.py
```

Figure:

```text
track_b_area_register_rate_scan.pdf
```

Data:

```text
sim/data/area_register_rate_scan.csv
sim/data/area_register_rate_scan_wide.csv
sim/data/area_register_rate_best.npz
sim/data/area_register_rate_wide_best.npz
```

Area-register sectors:

```text
H_n = n qubits
dim H_n = 2^n
S_n = n log 2
n = 4,...,10
```

BH-like mass law:

```text
M_n = alpha sqrt(n)
```

Control mass law:

```text
M_n = alpha n
```

Hamiltonian blocks:

```text
H_n = M_n I + small random symmetric perturbation
```

Shrinkage operators:

```text
local removal:
  project/remove one qubit

scrambled removal:
  orthogonally scrambled version of the same removal map
```

Rates:

```text
Gamma_{n,i -> n-1,f}
  proportional to |<f,n-1|X_n|i,n>|^2 J(omega)

omega = E_{n,i} - E_{n-1,f}
```

This is a population/rate kill test, not yet a Kraus simulation.

## Thermodynamics

For the BH-like mass law:

```text
S_n = n log 2
M_n = alpha sqrt(n)
T_n ~ 1 / sqrt(n) ~ 1/M_n
C < 0
```

The generated grid has negative heat capacity under the discrete diagnostic.

For the linear mass-law control:

```text
M_n = alpha n
```

the temperature is approximately constant, not black-hole-like.

## Result

The Track B kill test did not fail.

With the BH-like square-root mass law, both local and scrambled removal produce
modest but robust acceleration in the matrix-element-derived rate model.

Best grouped cases across two seeds:

```text
local removal, sqrt mass, gap >= 4:
  min acceleration over seeds = 1.125
  mean acceleration = 1.125

scrambled removal, sqrt mass, gap >= 4:
  min acceleration over seeds = 1.124
  mean acceleration = 1.125
```

For gap `2`, acceleration remains but is weaker:

```text
local removal, sqrt mass, gap=2:
  min acceleration = 1.063

scrambled removal, sqrt mass, gap=2:
  min acceleration = 1.066
```

For gap `1`, the model decelerates strongly:

```text
sqrt mass, gap=1:
  acceleration ~ 0.38
```

So the emission passband matters.

## Control

The first control run accidentally used too small a passband for the linear
mass law, so no transitions were open. A corrected wide-passband control was
run:

```text
sim/data/area_register_rate_scan_wide.csv
```

With the linear mass law and open transitions:

```text
linear mass, gap=8:
  acceleration ~ 0.60

linear mass, gap=10 or 12:
  acceleration ~ 0.91
```

Thus the linear control decelerates even when transitions are allowed.

This matters: the Track B acceleration is not just a generic consequence of
shrinking Hilbert-space dimension or arbitrary matrix elements. The BH-like
mass-area relation is doing real work.

## Interpretation

This is a useful Track B result.

It shows that:

```text
1. S ~ area can be implemented by an area register.
2. M ~ sqrt(area) gives the expected negative-heat-capacity thermodynamics.
3. Matrix-element-derived shrinkage rates can produce modest acceleration.
4. The linear mass-law control decelerates.
```

The result is weaker than the variable-N Bose-Hubbard acceleration, but it has
the entropy scaling that Bose-Hubbard lacks.

## Caveats

Important limitations:

```text
1. The model is still abstract: qubits are area bits, not a derived quantum
   gravity Hilbert space.

2. The Hamiltonian blocks are random symmetric matrices around M_n, not a
   local microscopic Hamiltonian.

3. The calculation is a population/rate diagnostic, not a Kraus or full unitary
   evolution.

4. Acceleration is modest and passband-dependent.

5. The local and scrambled removal maps behave almost identically, suggesting
   the current test is dominated by the sector energy structure more than by
   operator details.
```

## Current verdict

Track B is worth one more step.

The next step should be:

```text
upgrade the successful sqrt-mass area-register rate model to a secular Kraus
channel, then check whether core-radiation S2 grows while acceleration
survives.
```

If that works, Track B gives the entropy-correct complement to Track A:

```text
Track A: natural dynamics, wrong entropy law.
Track B: correct entropy law, abstract but concrete quantum register dynamics.
```

## Secular Kraus update

The successful square-root mass area-register rate model has now been upgraded
to a secular Kraus channel.

Script:

```text
sim/area_register_kraus.py
```

Figure:

```text
track_b_area_register_kraus.pdf
```

Data:

```text
sim/data/area_register_kraus_local_seed2468.npz
sim/data/area_register_kraus_local_seed2469.npz
sim/data/area_register_kraus_scrambled_seed2468.npz
sim/data/area_register_kraus_scrambled_seed2469.npz
```

Parameters:

```text
n = 4,...,10
q = 2
M_n = 8 sqrt(n)
gap = 4
steps = 80
```

The Kraus evolution preserves the acceleration:

```text
local removal:
  seed 2468: mid / early = 1.123
  seed 2469: mid / early = 1.124

scrambled removal:
  seed 2468: mid / early = 1.124
  seed 2469: mid / early = 1.124
```

Core-radiation entropy grows:

```text
peak S2(core) = about 5.34
```

Area entropy shrinks:

```text
dimension entropy:
  initial = log(2^10) = 6.93
  final   = about 4.21-4.26
```

Effective dimension shrinks:

```text
initial = 1024
final   = about 140-146
```

Interpretation:

```text
The entropy-correct area-register model survives the first quantum-channel
upgrade. It gives decreasing energy, decreasing area entropy, modest
accelerating emission, and growing core-radiation Renyi-2 entropy.
```

This is now the Track B counterpart to the variable-N Bose-Hubbard result.
