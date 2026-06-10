# Critical Connector Heating Results

## Question

The collective connector softness test found spectra with:

```text
number of relational modes ~ N^2
typical thermal quantum ~ 1/N
local power proxy near 1/N^2 for some spectra
```

This note tests the next gate:

```text
after the core emits energy of order T and the active connector sector changes
from N to N-1, does the remaining core heat?
```

Scale caveat:

```text
if M ~ N and S ~ N^2, then one N -> N-1 change costs order-one energy;
one Hawking-scale quantum has energy ~ T ~ 1/N;
therefore one physical coarse shrink corresponds to O(N) microscopic quanta.
```

So this is a spectral heating gate. It should not be read as a full physical
one-quantum evaporation event.

Scripts:

```text
sim/critical_connector_heating_gate.py
sim/critical_connector_heating_robustness.py
```

## Diagnostic

For each spectrum, set:

```text
T_before = eta / N.
```

Compute the connector-sector energy at `N`, emit:

```text
epsilon = kappa T_before,
```

then solve for `T_after` in the `N-1` connector spectrum:

```text
E_{N-1}(T_after) = E_N(T_before) - epsilon.
```

The gate passes when:

```text
T_after > T_before
```

over the scan.

Two energy proxies were used:

```text
Bose thermal energy:
  E = sum_m omega_m / (exp(omega_m/T) - 1)

classical active-mode cutoff:
  E = number of modes with omega_m <= c T, times T.
```

The second proxy is rough, but useful as a check that the Bose result is not
only a low-mode occupation artifact.

## First Scan

Run:

```text
python sim/critical_connector_heating_gate.py
python sim/critical_connector_heating_gate.py --energy-mode classical_cutoff \
  --rows-csv sim/data/critical_connector_heating_rows_classical.csv \
  --summary-csv sim/data/critical_connector_heating_summary_classical.csv
```

Result:

```text
model                         Bose heating      cutoff heating
connector_grid_NxN_crit       no                no
connector_rect_exactish_crit  no                no
connector_ring_crit           mostly            mostly
powerlaw_alpha1               yes               yes
powerlaw_alpha2               yes               yes
```

The grid-like spectra fail. The one-dimensional critical ring and power-law
spectra survive the first heating gate.

## Robustness Scan

Run:

```text
python sim/critical_connector_heating_robustness.py
```

Parameters:

```text
eta = 0.5, 1.0, 2.0
kappa = 0.25, 0.5, 1.0, 2.0
energy proxies = Bose and classical cutoff
N = 8 to 128
```

Aggregate result:

```text
model                         status    strict pass  mean heating  min ratio at Nmax
connector_grid_NxN_crit       fails     0.04         0.18          0.8348
connector_rect_exactish_crit  fails     0.00         0.06          0.6655
connector_ring_crit           fragile   0.42         0.93          1.0034
powerlaw_alpha1               fragile   0.75         0.81          0.9884
powerlaw_alpha2               robust    1.00         1.00          1.0083
```

Large-core survivor scan:

```text
python sim/critical_connector_heating_robustness.py --n-min 32 --n-max 128 \
  --models connector_ring_crit,powerlaw_alpha1,powerlaw_alpha2
```

Result:

```text
model                 status    strict pass  mean heating  min ratio at Nmax
connector_ring_crit   mostly    0.88         0.97          1.0034
powerlaw_alpha1       fragile   0.75         0.81          0.9884
powerlaw_alpha2       robust    1.00         1.00          1.0083
```

## Linear Versus Quadratic Ring

An important correction was added after the first pass.

The original `connector_ring_crit` used ring Laplacian eigenvalues directly as
the excitation energies:

```text
omega_k ~ 1 - cos(2 pi k/L) ~ k^2/L^2.
```

That is a quadratic low-energy dispersion. A usual massless harmonic chain or
CFT-like ring would instead use square-root Laplacian frequencies:

```text
omega_k ~ sqrt(1 - cos(2 pi k/L)) ~ k/L.
```

The linear case was added as:

```text
connector_ring_linear_crit.
```

Softness result:

```text
model                       soft gate  power gate  <omega>/T  P_local power
connector_ring_crit         yes        yes         0.503      -1.512
connector_ring_linear_crit  yes        yes         1.050      -1.967
```

Heating robustness for `N = 32` to `128`:

```text
model                       status    strict pass  mean heating  min ratio at Nmax
connector_ring_crit         mostly    0.88         0.97          1.0034
connector_ring_linear_crit  fails     0.21         0.46          0.9435
powerlaw_alpha1             fragile   0.75         0.81          0.9884
powerlaw_alpha2             robust    1.00         1.00          1.0083
```

This changes the target.

The natural CFT-like linear ring gives the desired softness and power proxy,
but it does not reliably heat after emission. The quadratic ring heats much
better, and tracks the `alpha=2` thermodynamic guide.

## Interpretation

The heating gate does not reward every critical spectrum. Dimensionality,
soft-mode density, and dispersion exponent matter.

Two-dimensional critical connector spectra cool after emission. They have many
soft modes, but reducing `N` changes the active spectrum in a way that does not
force the smaller core to a higher temperature.

The one-dimensional quadratic ring is the best non-toy survivor so far. It has:

```text
O(N^2) connector modes arranged in a one-dimensional critical band;
thermal quanta of order 1/N;
mostly positive post-emission heating, especially for N >= 32.
```

The `alpha=2` power-law spectrum is the strongest thermodynamic survivor, but
it missed the earlier local-power target. It should be treated as a guide to
the needed spectral density, not as the final model.

The linear ring and the `alpha=1` spectrum have the cleanest simple power
logic, but they cool under enough emission choices to be unreliable.

## Current Model-Selection Consequence

The no-settling route is still alive, but narrower.

The next candidate should use:

```text
a one-dimensional critical relational band with O(N^2) modes,
local emission operators,
an autonomous rule by which active connector count changes from N to N-1.
```

This is now more specific than "critical connector clump":

```text
quadratic critical connector ring/clump.
```

The model still needs an actual autonomous Hamiltonian that makes connector
activity and radiation separation emerge dynamically.

## Main Remaining Risk

The quadratic one-dimensional band may look engineered unless it comes from a
recognizable structure:

```text
ferromagnetic or nonrelativistic Goldstone modes;
a long relational chain of connector states;
an ordering induced by collective coordinates;
a known z=2 critical spin/rotor system living on relational links.
```

The next step should therefore look for a microscopic Hamiltonian whose
connector sector naturally has this critical one-dimensional spectrum.
