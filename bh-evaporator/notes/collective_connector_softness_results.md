# Collective Connector Softness Results

## Question

The simple connector model gives area-like counting:

```text
number of connector modes ~ N^2
S ~ N^2
M ~ N
T ~ 1/N
```

But the first connector gate showed that complete-graph incidence spectra do
not naturally produce microscopic emission energies of order `1/N`.

This note tests a broader possibility:

```text
the connector degrees form collective critical spectra.
```

The question becomes:

```text
Can O(N^2) relational modes have thermally available excitations at T ~ 1/N?
```

Script:

```text
sim/collective_connector_softness_search.py
```

## Diagnostic

For each candidate spectrum and each `N`, set:

```text
T_N = 1/N.
```

Compute one-particle thermal sums:

```text
Z(T) = sum_m exp(-omega_m / T)
<omega>_T = sum_m omega_m exp(-omega_m/T) / Z(T).
```

The energy-scale gate is:

```text
<omega>_T / T = O(1).
```

The local-coupling power proxy assumes a local emission operator has finite
total spectral weight spread over all connector modes:

```text
Gamma_local ~ Z(T) / number_of_modes
P_local ~ Gamma_local <omega>_T.
```

The target power scaling is:

```text
P_local ~ N^-2.
```

## Spectra Tested

```text
complete_line_graph_kac:
  Kac-normalized line graph of K_N connector incidence.

connector_ring_crit:
  ring Laplacian eigenvalues on N(N-1)/2 connector modes. The low-energy
  dispersion is quadratic.

connector_ring_linear_crit:
  square-root ring Laplacian frequencies. The low-energy dispersion is linear,
  as in a massless harmonic chain.

connector_grid_NxN_crit:
  critical two-dimensional grid Laplacian on N^2 connector modes.

connector_rect_exactish_crit:
  rectangular critical grid with mode count close to N(N-1)/2.

powerlaw_alpha1:
  toy spectrum omega_k = k / N_conn.

powerlaw_alpha2:
  toy spectrum omega_k = (k / N_conn)^2.
```

## Result

Run:

```text
python sim/collective_connector_softness_search.py \
  --summary-csv sim/data/collective_connector_softness_summary_v2.csv \
  --rows-csv sim/data/collective_connector_softness_rows_v2.csv
```

Summary:

```text
model                         soft gate  power gate  <omega>/T  participation power  P_local power
complete_line_graph_kac       no         no          128.000    1.030                -49.420
connector_grid_NxN_crit       yes        yes         1.110      0.680                -1.816
connector_rect_exactish_crit  yes        yes         1.238      0.765                -1.738
connector_ring_crit           yes        yes         0.503      1.567                -1.512
connector_ring_linear_crit    yes        yes         1.050      0.991                -1.967
powerlaw_alpha1               yes        yes         1.008      1.030                -1.999
powerlaw_alpha2               yes        no          0.500      1.538                -1.500
```

The complete-graph incidence spectrum still fails. Critical collective
connector spectra pass the energy-scale gate. With local spectral-weight
normalization, several also give a power exponent close to the target window.

The cleanest toy scaling is `powerlaw_alpha1`, mirrored by the linear ring:

```text
omega_k ~ k / N_conn,
N_conn ~ N^2,
Z(T) ~ N,
Gamma_local ~ Z / N_conn ~ 1/N,
<omega> ~ 1/N,
P_local ~ 1/N^2.
```

This reproduces the desired scaling logic without assigning emission
probabilities.

The quadratic ring and `powerlaw_alpha2` are different. They have a denser
soft tail and later perform better in the heating gate, but their simple local
power exponent is closer to `N^-3/2` than to `N^-2`.

## Interpretation

The connector route should not be declared dead. The simpler statement is:

```text
complete-graph incidence connector spectra are too hard;
critical collective connector spectra can have the right softness. The later
heating test shows that the dispersion exponent matters, so softness alone is
not enough.
```

This is a real opening, but it adds a new burden:

```text
Why should the relational connector sector be critical or approximately
gapless?
```

That is now the central model-building question.

## What This Gives Us

At the level of spectral architecture, a critical connector model can supply:

```text
area-like state count:
  O(N^2) connector modes;

Hawking-scale microscopic energy:
  <omega> ~ T ~ 1/N;

Schwarzschild-like power proxy:
  local spectral weight gives Gamma ~ 1/N and P ~ 1/N^2.
```

This is much better than plain connector counting.

## What It Does Not Yet Give

Still missing:

```text
autonomous site/clump dynamics;
actual separation/emission events;
post-emission heating;
unitary radiation tracking;
Page-like information diagnostics.
```

## Next Candidate Model

The next no-settling candidate should be a critical connector clump:

```text
N site variables;
O(N^2) connector modes;
connector sector tuned or naturally placed near a critical/gapless point;
site/radiation coupling through a local connector operator;
core/radiation split by site separation or connector decoupling.
```

Minimal Hamiltonian form:

```text
H = H_sites + H_conn,critical + H_site-conn + H_escape.
```

The next decisive test is:

```text
Can this critical connector sector be coupled to site separation so that
energy loss heats the remaining active core?
```

If yes, the no-settling route is alive again.
