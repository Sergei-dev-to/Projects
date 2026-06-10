# Literature Map for the Ideal Hamiltonian

Date: 2026-06-07

## Question

We want to know which parts of the ideal evaporator Hamiltonian can be taken
from existing literature, which parts require a short derivation, and which
parts still require numerical checks.

The target Hamiltonian class is:

```text
H_total = H_core + K_scr + H_out + H_int
```

with a finite or regulated core having a black-hole-like density of states,
an outgoing radiation continuum or large lead, weak energy-conserving emission,
and sufficiently mixing dynamics inside each core energy/area sector.

## Short Answer

The individual ingredients are mostly standard.  I do not see an existing
paper that combines them into the exact package we want:

```text
super-Hagedorn core DOS with S(E) ~ E^2
+ continuum radiation Hamiltonian
+ DOS-ratio thermal emission
+ Schwarzschild power law
+ unitary Page-like information flow
```

So the right strategy is not to rederive standard decay theory or Page
typicality.  We should cite those, then derive only the model-specific rate
scaling and test only the finite-Hamiltonian realization.

## Ingredient-by-Ingredient Map

| Ingredient | Standard source class | What we can cite | What remains ours |
|---|---|---|---|
| Black-hole thermodynamics | Bekenstein, Hawking, Page | `S_BH ~ A ~ M^2`, `T_H ~ 1/M`, thermal flux with greybody factors, lifetime scaling | Mapping this target onto a non-gravitational core spectrum |
| Microcanonical emission factor | statistical mechanics; Parikh-Wilczek tunneling | transition probability/rate weighted by final-state DOS, `Gamma ~ exp[Delta S]` | Applying it to our sector DOS and radiation channel |
| Continuum decay Hamiltonian | Wigner-Weisskopf, Friedrichs-Lee, Fermi's golden rule | discrete/many-level system coupled to continuum; weak-coupling rate from matrix element squared times DOS | Our particular core sectors and area-strength matrix elements |
| Radiation phase space | QFT / ordinary wave emission | massless radiation density of states gives powers of `omega`; greybody factors multiply thermal factor | Choosing `p=2` and area strength `eta=1` for the Schwarzschild-like effective model |
| Fast scrambling | Hayden-Preskill; Sekino-Susskind; random circuits | rapidly mixing internal dynamics enables random-subsystem/isometry reasoning | Verifying or assuming the hierarchy for our finite Hamiltonian |
| Page-like information flow | Page theorem; Hayden-Preskill; Osuga-Page; random circuit models | shrinking Hilbert-space capacity plus typical unitaries gives Page-like radiation entropy and late/early correlations | Measuring it in our explicit radiation-chain Hamiltonian |
| Unitary evaporation toy models | Giddings, Avery, Osuga-Page, Alsing, Piroli-Sunderhauf-Qi | many non-gravitational or effective models already realize unitary information transfer/Page behavior | Showing the thermodynamic/rate package in the same Hamiltonian |
| Natural microscopic origin of `S(E) ~ E^2` | black-hole microstate counting, matrix models, string/Hagedorn systems | black holes have the desired entropy; some matrix models have natural clump evaporation | Generating this DOS from a simple non-gravitational many-body Hamiltonian remains a harder, separate goal |

## Closest Existing Model Families

### 1. Wigner-Weisskopf / Friedrichs-Lee decay models

These are the cleanest precedent for the Hamiltonian structure:

```text
discrete or many-level system + continuum modes + weak coupling
```

The standard result is a decay rate proportional to the squared transition
matrix element times the continuum density of final states.  This directly
supports writing `H_out` as a continuum field and deriving the rate equation
from `H_int` rather than assigning rates.

What they do not provide is the black-hole-like core DOS, shrinking area
sectors, or Page-like information flow.

### 2. Microcanonical black-hole emission / tunneling

The factor

```text
exp[S(E - omega) - S(E)]
```

is standard final-state counting.  In black-hole language it is closely related
to Parikh-Wilczek tunneling, where emission is weighted by the change in
black-hole entropy.  We should not present this factor as new.

What is ours is the finite Hamiltonian construction where this factor appears
from the chosen core spectrum and emission matrix elements.

### 3. Page / Hayden-Preskill / random-unitary models

These cover the information-theoretic reduction:

```text
rapid internal mixing + shrinking core Hilbert space
    -> typical isometry
    -> Page-like information flow
```

This means we can cite Page theorem and random-subsystem logic for the ideal
limit.  We still need to show that our explicit Hamiltonian is close enough to
that limit, or else state the hierarchy as an assumption.

### 4. Qubit transport and circuit evaporation models

Giddings, Avery, Osuga-Page, Hotta-Nambu-Yamaguchi, and
Piroli-Sunderhauf-Qi already cover broad families of unitary black-hole
evaporation toy models.  They make it clear that the novelty cannot be
"unitary evaporation" or "a Page curve."

The missing piece in those models, relative to our target, is usually the full
thermodynamic package: energy-resolved radiation, local thermal spectrum,
negative heat capacity, and Hawking-like rate scaling.

### 5. Alsing waterfall / quantum-optical models

Alsing's models are the closest recent phenomenological comparison.  They use
quantum-optical squeezed-state and beam-splitter structures to model unitary
evaporation, approximate thermality, Page curves, and energy transfer into
radiation.

They are not the same as our target because the emission spectrum and rate law
are not derived from a super-Hagedorn core density of states coupled to an
ordinary outgoing continuum.  Alsing 2025 explicitly gives a useful comparison:
one can get unitarity, energy bookkeeping, and Page behavior without getting
the Hawking rate law.

### 6. Matrix-model black-hole evaporation

BFSS/matrix black-hole models are the closest thing to natural microscopic
evaporation: a clump of matrices/D0-branes emits along flat directions, and
the active degrees of freedom decrease when a D0-brane separates.

This is promising for a stronger future result, but it is a different program:
it is holographic/gravitationally motivated and much harder to reduce to the
clean non-gravitational Hamiltonian package we are testing here.

## What We Should Derive

Only these derivations are really model-specific:

1. From `S(E) = c E^2`, derive

```text
beta(E) = dS/dE ~ E,
T(E) ~ 1/E,
C < 0.
```

2. From the weak-coupling rate

```text
dGamma/domega
  ~ A^eta omega^p exp[S(E - omega) - S(E)]
```

derive the emitted spectrum and power scaling.

3. For the Schwarzschild-effective choice

```text
p = 2, eta = 1, A ~ M^2, beta ~ M
```

derive

```text
P ~ M^-2,
dM/dt ~ -M^-2,
tau ~ M0^3.
```

4. Under

```text
t_scr << t_emit << t_evap
```

connect the Hamiltonian to the standard typical shrinking-isometry picture.
This should be framed as a reduction to known Page/decoupling logic, not as a
new theorem unless we prove concentration bounds for the actual finite model.

## What We Should Calculate or Simulate

The finite-Hamiltonian checks should be limited to places where standard
literature does not decide the issue:

1. **Finite autonomous realization.**  Does the explicit `H_total` actually
produce shrinkage and radiation energy growth without excessive reabsorption?

2. **Local thermality in the finite model.**  Does the measured flux spectrum
approach the DOS-ratio prediction as the outgoing channel and core sectors are
enlarged?

3. **Rate scaling in the finite model.**  Does the measured power follow the
predicted `p=2, eta=1` trend over the accessible evaporation window?

4. **Information flow in the same model.**  With explicit radiation records,
does radiation entropy turn over and do early/late radiation correlations grow
after the Page point?

5. **Scrambling control.**  Does removing or weakening `K_scr` spoil the
information-flow behavior and/or late-time power growth?

## What We Should Not Spend Time Deriving

These are standard enough to cite:

```text
Fermi's golden rule / weak-coupling continuum decay;
Page theorem;
Hayden-Preskill random-subsystem reasoning;
fast-scrambling motivation;
Hawking/Page greybody spectrum as the physical target;
Parikh-Wilczek entropy-difference emission factor.
```

## Literature-Based Bottom Line

The strongest fair claim is:

```text
We combine standard continuum decay theory, black-hole microcanonical
state-counting logic, and Page/random-subsystem information flow into one
finite non-gravitational Hamiltonian model with an imposed super-Hagedorn core
spectrum.  The remaining work is to verify that the finite Hamiltonian realizes
the combined thermodynamic and information-flow package, rather than merely
the separate ingredients.
```

The claim should not be:

```text
No one has modeled black-hole evaporation without gravity.
```

That is false.  Many papers do.

The claim also should not be:

```text
We derived Fermi's golden rule or the Page curve.
```

Those are known.  Our value is in the assembled Hamiltonian target and the
finite checks of the full evaporation package.

## Sources Checked

- Bekenstein, "Black Holes and Entropy" (1973).
- Hawking, "Particle Creation by Black Holes" (1975).
- Page, "Particle Emission Rates from a Black Hole" (1976).
- Page, "Average Entropy of a Subsystem" (1993).
- Page, "Information in Black Hole Radiation" (1993).
- Parikh and Wilczek, "Hawking Radiation as Tunneling" (1999).
- Hayden and Preskill, "Black holes as mirrors: quantum information in random
  subsystems" (2007).
- Sekino and Susskind, "Fast Scramblers" (2008).
- Giddings, "Models for unitary black hole disintegration" (2011).
- Avery, "Qubit Models of Black Hole Evaporation" (2011).
- Hotta, Nambu, Yamaguchi, "Soft-Hair-Enhanced Entanglement Beyond Page Curves
  in a Black-hole Evaporation Qubit Model" (2017).
- Osuga and Page, "Qubit transport model for unitary black hole evaporation
  without firewalls" (2018).
- Piroli, Sunderhauf, Qi, "A random unitary circuit model for black hole
  evaporation" (2020).
- Alsing, "Black Hole Waterfall: a unitary phenomenological model for black
  hole evaporation with Page curve" (2025).
- Alsing, "Quantum Optical Inspired Models for Unitary Black Hole Evaporation"
  (2026).
- Jones, Altaie, Varcoe, "Kinematic Emergence of the Page Curve in a Local
  Transverse-Field Ising Model" (2026).
- Arias, "Microcanonical Energy Sharing and a Page-like Curve for the Capacity
  of Entanglement" (2026).
