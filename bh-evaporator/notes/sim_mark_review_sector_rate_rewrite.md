# Simulated Referee Report

Manuscript:

```text
A Non-Gravitational Sector-Rate Model for Black-Hole-Like Evaporation
```

Recommendation:

```text
Major revision.
```

## Summary

The manuscript proposes a finite non-gravitational comparison model for
black-hole-like evaporation.  The main construction is a sector-rate model
derived from an abstract Hamiltonian.  Core sectors have an area-like state
count, a square-root mass law gives the Schwarzschild-like relation
`S ~ M^2`, and transitions from one sector to the next smaller sector emit
radiation quanta with rates obtained from matrix elements, radiation phase
space, and final-state density.  An energy-resolved sector density of states
is used to obtain a near-thermal emitted spectrum.  A separate
repeated-interaction model is used to track purification and Page-like
information flow.

The program is worthwhile.  The paper is explicit about Hilbert spaces,
entropy definitions, model inputs, and controls.  It is also more quantitative
than many toy-model papers in this area.  The central issue is that the paper
currently has two linked models rather than one complete evaporator: the
sector-rate model supplies the thermodynamic and spectral results, while the
repeated-interaction model supplies purification and information-flow
diagnostics.  That separation is stated, but the headline framing still risks
suggesting a more unified construction than has been demonstrated.

## Strengths

### 1. Clear separation of entropy notions

The paper distinguishes:

```text
microcanonical core entropy;
hard-radiation entropy;
full-radiation von Neumann entropy.
```

This is important.  Many toy evaporation models blur these quantities.

### 2. The thermality diagnostic is meaningful

The hard spectrum in the sector-rate model is compared to:

```text
P(x) ~ x^p exp(-x),  x = beta omega.
```

The reported total-variation distance is around:

```text
TV ~ 0.05.
```

This is a real spectral diagnostic, because the emitted distribution is
generated from energy-resolved sector transitions.  It is not merely the
entropy of a hard register whose probabilities were assigned in advance.

### 3. The acceleration control is useful

The square-root mass law and linear mass law are compared in the same
sector-rate framework.  The square-root case gives:

```text
power ratio ~ 1.10,
```

while the linear control gives:

```text
power ratio ~ 0.99.
```

Both have good hard spectra.  This is a useful separation: the spectrum can be
thermal without producing accelerating evaporation.

### 4. The paper is unusually explicit about model inputs

The listed inputs include:

```text
sector dimensions;
mass law;
energy-resolved sector density of states;
transition operators;
within-sector mixing;
purifier and soft-record registers.
```

This makes the model assessable.  The paper does not hide the fact that the
area count and mass law are supplied.

## Major Concerns

### 1. The manuscript does not yet contain one model with the full package

The sector-rate model gives:

```text
near-thermal hard spectrum;
accelerating emission;
mass-law control;
golden-rule transition rates.
```

The repeated-interaction model gives:

```text
unitary purification;
soft records;
early/late mutual information;
Page-like entropy turnover.
```

These are not the same simulation.  The paper acknowledges this, but the
abstract still opens with:

```text
We construct a finite non-gravitational comparison model...
```

That singular phrasing is too strong.  A reader could reasonably expect the
same model to generate both the thermodynamic sector-rate behavior and the
unitary radiation entropy trajectory.

Suggested fix:

```text
Frame the result as two linked diagnostics:
  (i) a sector-rate thermodynamic/spectral model;
  (ii) a companion finite unitary record model.
```

Then state that combining them into one coherent Hamiltonian evolution remains
the next target.

### 2. Within-sector mixing is an essential assumption

The most important mechanism in the sector-rate model is the idealized map:

```text
p_n(a) -> P_n / dim B_n.
```

Without this map, the exponential density of states improves the hard spectrum
but the evaporation decelerates.  With the map, acceleration returns.  So the
paper's main sector-rate result depends on a strong rethermalization
assumption.

This is not a fatal flaw, but it needs to be elevated from caveat to central
mechanism.  In black-hole language, this is standing in for fast internal
scrambling or equilibration.

Suggested fix:

```text
Make the main result a three-part mechanism:
  square-root mass law;
  exponential local density of states;
  fast within-sector equilibration.
```

The abstract already mentions mixing, but the paper should emphasize that
mixing is not optional for the acceleration result in the energy-resolved
model.

### 3. The exponential local density of states is selected

The paper uses:

```text
rho_n(epsilon) ~ exp(beta_n epsilon)
```

over a window of order `T_n`.  This is exactly the local form needed for a
thermal emission spectrum.  That is acceptable in a diagnostic model, but it
is still an input.  The paper should explain more clearly why this is the
finite-sector version of the usual microcanonical derivation.

Suggested fix:

```text
Add a paragraph deriving the local exponential density from
Omega(E - omega) / Omega(E) in a generic large bath/core system.
```

This would make the density-of-states choice look less arbitrary.

### 4. The sector-rate model is not a full Hamiltonian evolution

The paper writes a Hamiltonian and then simulates the secular rate equation.
That is a reasonable approximation, but it should be named consistently.  The
title says "sector-rate model," which helps.  The abstract says
"Hamiltonian-derived," which is also acceptable.

The remaining risk is that some readers will interpret the paper as having
simulated:

```text
|psi(t)> = exp(-i H_total t)|psi(0)>.
```

It has not.  It has simulated the weak-coupling rate limit.

Suggested fix:

```text
Use "Hamiltonian-derived sector-rate model" consistently.
Reserve "Hamiltonian simulation" for the future coherent wave-packet upgrade.
```

### 5. The Page-like diagnostic is too small to carry much weight

The Page-like table uses:

```text
L_init = 3;
one seed;
one threshold;
one fixed eight-emission schedule;
two scramblers.
```

The table is useful because it includes the support bound and mean active
capacity.  But it remains a proof of compatibility, not evidence for a robust
Page curve.

The no-scrambling trajectory does not turn over over the same window even
though the support bound shrinks.  The paper explains this as a routing issue.
That explanation is plausible, but it also means the turnover is not simply the
Page kinematic bound.

Suggested fix:

```text
Keep the phrase "Page-like" but avoid "Page curve" except as a target.
Add a seed/threshold ensemble if the result is meant to carry more weight.
```

### 6. Figures are needed

The manuscript is currently table-heavy.  Three figures would materially
improve the paper:

```text
1. hard spectrum vs x^p exp(-x);
2. power ratio for square-root and linear mass laws;
3. radiation entropy trajectory with core-support bound.
```

Without these figures, the reader has to infer the main story from small
tables.

## Minor Points

The title is accurate, but "sector-rate" may be unfamiliar.  The phrase is
defined well enough in the body.

The paper cites the appropriate toy-model literature and the modern
island/QES literature.  The Bekenstein and Hawking thermodynamic references are
now included.

The microscopic connector-model section is interesting, but it reads like a
research-plan paragraph rather than a result.  That is acceptable if kept
short.  It should not compete with the sector-rate result.

## Recommendation

The manuscript has a real result at the diagnostic-model level:

```text
an energy-resolved sector-rate model can generate a near-thermal hard spectrum,
and with within-sector equilibration it accelerates for the square-root
mass law while the linear control does not.
```

That is worth developing.  The companion unitary record model is useful, but
it should be presented as a separate compatibility diagnostic.

Before publication-level assessment, I would ask for:

```text
1. sharper abstract language saying this is a two-diagnostic construction;
2. stronger emphasis on within-sector mixing as a central assumption;
3. one paragraph justifying the exponential local density of states;
4. figures for spectrum, power, and Page-like trajectory;
5. either ensemble support for the Page-like diagnostic or softer claims about
   it.
```

With those changes, the paper would be a clear and useful comparison model. It
would not solve the microscopic-origin problem, but it would state cleanly what
has been constructed and what remains open.
