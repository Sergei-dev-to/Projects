# Certificate Precision Versus Evaporation Time

Date: 2026-07-09

Status: asymptotic single-black-hole lower bound.  This is an operational
feasibility audit, not a detector-engineering forecast.

## Result in One Line

For independent counting-limited observations, resolving a response or
correlation defect of size `eta` needs at least `Omega(eta^-2)` events.  A
four-dimensional Schwarzschild black hole changes its mass by a fractional
amount `Omega[1/(S eta^2)]` while emitting that many Hawking quanta.  Therefore
the precision `eta ~ S^-1/2` required for a full entropy-rank certificate costs
an order-one fraction of one black hole's evaporation history.  It is not
compatible with a single fixed stationary line without an ensemble,
cross-window scaling theorem, or stronger prior information.

## 1. Event Lower Bound

Estimating a bounded probability, normalized response, or correlation with
ordinary independent shot noise to additive error `eta` requires

```text
N_events >= c eta^-2,                                     (1.1)
```

for a constant depending on confidence and event contrast.  Correlations,
rare absorption events, detector inefficiency, nuisance-parameter fitting, and
multiple settings can only increase this cost.

Equation (1.1) is deliberately optimistic.  It establishes a lower bound on
the time/resource problem before a detailed protocol is chosen.

## 2. Schwarzschild Event and Drift Scaling

For a four-dimensional Schwarzschild black hole,

```text
S ~ M^2,
T ~ 1/M,
M/T ~ S.                                                  (2.1)
```

A typical Hawking quantum carries energy `O(T)`.  After `N` emissions,

```text
Delta M/M ~ N T/M ~ N/S.                                  (2.2)
```

Combining (1.1) and (2.2),

```text
Delta M/M >= c/(S eta^2).                                 (2.3)
```

The total number of Hawking-scale quanta emitted over an order-one mass change
is `O(S)`, as expected.

## 3. Rank Exponent Versus Stationarity

Suppose a certificate floor scales as

```text
N_eff >= S^alpha
```

only when its signed response/counting accuracy scales as

```text
eta <= S^(-alpha/2).                                      (3.1)
```

The optimistic event and drift costs are then

```text
N_events >= S^alpha,
Delta M/M >= S^(alpha-1).                                 (3.2)
```

Consequences:

```text
alpha < 1:
  a subextensive participation floor can fit in an asymptotically adiabatic
  window;

alpha = 1:
  full entropy-rank precision consumes an order-one evaporation fraction;

alpha > 1:
  impossible from one black hole's Hawking-count budget.
```

Thus the finite-accuracy floor remains operationally meaningful, but the
`N_eff ~ S` endpoint sits exactly at the single-system stationarity boundary.

### Self-consistent fixed-line window

If the analysis treats the line/reference as constant to within the same error
`eta`, require the fractional drift during data collection to satisfy

```text
N_events/S <= eta.                                        (3.3)
```

Combining this with `N_events >= c eta^-2` gives

```text
eta >= O(S^-1/3).                                         (3.4)
```

For a participation floor controlled as `N_eff ~ eta^-2`, a single unmodeled
stationary window can therefore reach at most `N_eff ~ S^(2/3)`.  This is not a
universal black-hole exponent: it follows from independent shot noise, linear
fractional drift, and the demand that drift remain below statistical error.
It shows why full `S` scaling requires explicitly modeling and combining the
nonstationary history rather than merely calling the evaporation adiabatic.

## 4. Multiple Settings and Tomography

If a protocol uses `K` independently calibrated settings with comparable
precision, the optimistic cost becomes

```text
N_events >= K eta^-2,                                     (4.1)
```

unless the same events jointly inform all settings.  A two-drain protocol
already requires separate controlled histories.  Response-kernel tomography
over a family whose size grows with the desired rank can cost parametrically
more than `S` events.

This does not prove tomography impossible.  It establishes the acceptance
test it must pass:

```text
protocol sample complexity
  <= available quanta in a window over which
     the reference temperature, line identity, source decomposition,
     and internal/exterior kernels remain related by a proved scaling law.
```

## 5. Ensemble and Cross-Window Escapes

The lower bound can be evaded as a stationarity obstruction by:

1. An ensemble of identically prepared black holes at the same mass.
2. A theorem allowing data from different masses to collapse onto a known
   dimensionless spectral profile.
3. Strong prior knowledge reducing the number of fitted parameters.
4. Collective/quantum-enhanced metrology, subject to preparation and loss
   constraints.
5. A model-side calculation replacing empirical tomography.

Each escape changes the meaning of “exterior certificate.”  The first is an
ensemble certificate, the second is a gravitational scaling inference, and the
fifth is not observational certification.

## 6. Additional Black-Hole Intervention Cost

Changing the asymptotic detector does not change `Gamma_out` at the source.
A reflecting or cavity boundary can do so only by returning radiation, which
generically introduces incoming occupation, delayed feedback, and altered
line structure.  Therefore a black-hole two-drain experiment must prove that
its intervention preserves:

```text
the internal kernel;
the source/process identity;
the reference temperature after calibration;
the vacuum-drain condition or its generalized replacement;
the assumed common scaling of exterior widths.
```

Without that proof, two-drain separation is a laboratory/model-side theorem,
not a realizable black-hole exterior protocol.

## 7. Consequence for the Program

The strongest single-black-hole claim should normally be an exponent/floor,
not exact entropy-rank saturation.  A flagship statement of `N_access ~ S`
must specify whether it is:

```text
an ensemble asymptotic statement;
a cross-mass scaling inference;
a model-side theorem;
or a literal finite-lifetime observational protocol.
```

These are not interchangeable.

## Next Calculation

For each proposed certificate leg, tabulate:

```text
number of settings;
event probability and detector efficiency;
target error scaling;
integration time;
mass/temperature drift;
nuisance parameters;
whether the same black hole can supply all settings.
```

Do this before deciding that response-kernel tomography can replace the
ordinary-sector envelope.

## Discipline

- Never quote `eta ~ S^-1/2` without its `O(S)` event cost.
- Distinguish one-black-hole, ensemble, and model-side certificates.
- Do not assume a line remains stationary over the full evaporation time.
- Treat multiple settings as separate statistical budgets unless a joint
  estimator is explicitly constructed.
