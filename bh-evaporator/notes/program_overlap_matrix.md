# Program Overlap Matrix

## Purpose

Compare the evaporator goal against nearby literature and against our current
model, using the current target categories, diagnostics, and model comparisons.

The goal is not to decide publication strategy.

The goal is to see whether the interesting result we want is already present
elsewhere.

## Target Categories, Diagnostics, And Model Comparisons

```text
Spec:
  finite Hilbert space, subsystem split, explicit evolution, purifiability.

Thermo:
  shrinking capacity, S_micro ~ M^2, T ~ 1/M, C < 0, P ~ M^-2,
  tau ~ M0^3.

Info:
  local hard thermality, Page-like fine-grained radiation entropy,
  early/late correlations,
  global/soft purification.

GravityFree:
  gravity-free comparison.

RateDiag:
  emission power from weighted channels.

Scrambling:
  scrambling diagnostics and comparison cases.

Autonomy:
  one repeated unitary cycle, or the stronger simple time-independent
  autonomous-Hamiltonian version.
```

Legend:

```text
Y  = clearly present
P  = partially present / present in a different form
N  = not central or not present
```

## Compact Comparison

```text
Program / paper                 Spec Thermo Info GravityFree RateDiag Scrambling Autonomy
-----------------------------------------------------------------------------------------
Glatthard                       Y    N      Y    Y           N        N          P
Avery                           Y    P      Y    P           P        P          P
Osuga-Page                      Y    P      Y    P           P        P          P
Hotta-Nambu-Yamaguchi           Y    Y      Y    P           P        P          P
Black Hole Waterfall            Y    P      Y    P           P        P          P
Local TFIM Page model           Y    N/P    Y    P           N        P          Y
Track E spin chain              Y    Y      P    P           Y        Y          P
Edge-tension Floquet droplet    Y-   Y      Y-   Y           P        P+         Y-/P
```

## Literature Notes

### Glatthard

References:

```text
Jonas Glatthard,
"Page-curve-like entanglement dynamics in open quantum systems",
arXiv:2401.06042.

Jonas Glatthard,
"Thermodynamics of the Page curve in Markovian open quantum systems",
arXiv:2501.09082.
```

Overlap:

```text
Page-like entropy dynamics outside gravity;
thermodynamic interpretation of Page-like entropy decrease.
```

Missing relative to our target:

```text
black-hole-like negative heat capacity;
shrinking state-count sectors;
accelerating evaporation from a hotter-as-it-shrinks core.
```

Assessment:

```text
Strong overlap with "Page curves are not uniquely gravitational."
Weak overlap with the black-hole thermodynamic engine.
```

### Avery

Reference:

```text
Steven G. Avery,
"Qubit Models of Black Hole Evaporation",
arXiv:1109.2911.
```

Overlap:

```text
general qubit models of black-hole evaporation;
unitary and nonunitary evaporation classes;
requirements for unitary evaporation.
```

Missing relative to our target:

```text
negative heat capacity;
accelerated evaporation;
matrix-element-derived thermodynamic schedule.
```

Assessment:

```text
Strong overlap with qubit evaporation model space.
Weak overlap with the thermodynamic acceleration question.
```

### Osuga-Page

Reference:

```text
H. Osuga and Don N. Page,
"Qubit Transport Model for Unitary Black Hole Evaporation without Firewalls",
arXiv:1607.04642.
```

Overlap:

```text
explicit qubit transport from black-hole degrees to radiation;
unitary evaporation;
changing black-hole/radiation split.
```

Missing relative to our target:

```text
realistic thermodynamic emission schedule;
negative heat capacity as the driver of acceleration.
```

Assessment:

```text
Very relevant to shrinking/register-transfer ideas.
Less relevant to the weighted-power mechanism.
```

### Hotta-Nambu-Yamaguchi

Reference:

```text
Masahiro Hotta, Yasusada Nambu, and Koji Yamaguchi,
"Soft-Hair-Enhanced Entanglement Beyond Page Curves in a Black-hole
Evaporation Qubit Model",
arXiv:1706.07520.
```

Overlap:

```text
multi-qubit evaporation model;
Schwarzschild-like thermal properties;
Hawking-particle and soft-hair channels;
entanglement beyond simple Page curves;
shrinking active sector.
```

Missing or weaker relative to our target:

```text
accelerated emitted power is not the central observable;
emission uses effective Hamiltonians/channels plus phenomenological
probabilities;
no clean weighted-power diagnostic was found;
no mass-law or bath-dimension comparisons were found.
```

Assessment:

```text
Closest program-level overlap.
It covers shrinking qubits plus Schwarzschild-like thermal relations better
than we initially assumed. The remaining distinction is the acceleration
diagnostic and comparisons.
```

### Black Hole Waterfall

Reference:

```text
Paul M. Alsing,
"Black Hole Waterfall: a unitary phenomenological model for black hole
evaporation with Page curve",
arXiv:2501.00948.
```

Overlap:

```text
unitary phenomenological evaporation;
Page curve;
finite initial black-hole energy;
black hole reaches zero mass while radiation carries energy away;
Hamiltonian/squeezed-state generation perspective.
```

Missing or weaker relative to our target:

```text
finite shrinking-sector state-count mechanism;
microcanonical entropy scaling `S_micro ~ M^2` as a central diagnostic;
negative heat capacity / accelerating power comparisons;
weighted-power decomposition.
```

Assessment:

```text
Strong overlap with unitary phenomenological evaporation and Page curves.
Less direct overlap with the finite-sector thermodynamic diagnostic program.
```

### Local TFIM Page Model

Reference:

```text
"Kinematic Emergence of the Page Curve in a Local Transverse-Field Ising
Model",
arXiv:2603.17000.
```

Overlap:

```text
local spin-chain dynamics;
black-hole subsystem and growing environment analogy;
Page-curve-like behavior from local quantum dynamics.
```

Missing relative to our target:

```text
Schwarzschild core-entropy/mass law;
negative heat capacity;
accelerated evaporation as a thermodynamic observable;
weighted-power diagnostic.
```

Assessment:

```text
Strong overlap with spin-chain/Page dynamics.
Weak overlap with thermodynamic acceleration comparisons.
```

## Our Previous Track E

What it showed:

```text
finite variable-length spin-chain sectors;
state count S_n = n log 2;
black-hole-like behavior if M_n ~ sqrt(n);
negative heat capacity;
matrix-element-derived energy-lowering emission;
robust acceleration under the square-root mass law;
robust deceleration under the linear mass law;
local-vs-scrambled removal comparisons;
weighted-power diagnostic.
```

Main weakness:

```text
M ~ sqrt(S) was assigned rather than naturally generated.
```

Assessment:

```text
The strongest content was the diagnostics-and-comparisons package.
```

## Current Edge-Tension Floquet Droplet

Core mechanism:

```text
2D constrained droplet;
area-like residual microcanonical entropy S_micro(L) = L^2 log q;
boundary-tension energy M_L = 4 sigma L;
therefore S_micro ~ M^2;
T ~ 1/M;
C < 0;
2D bath gives P ~ boundary * T^3 ~ M^-2.
```

Quantum architecture:

```text
finite droplet sectors;
hard radiation registers;
soft/shrink records;
hidden bath purifiers;
emitted-energy accumulator;
threshold-triggered shell transfer;
scrambling comparisons;
global finite-register rule;
state-vector lift.
```

Current best diagnostic:

```text
notes/final_floquet_candidate_scan_results.md
notes/final_floquet_toy_model_result.md
```

Current requirements and gaps:

```text
notes/phenomenology_requirements_review.md
notes/phenomenology_gap_audit.md
```

Assessment:

```text
This is now the strongest integrated candidate.
It gets the thermodynamic package from ordinary non-gravitational ingredients:
area-like constrained entropy, boundary tension, and 2D bath phase space.
It also has finite quantum diagnostics for hard thermality, soft/global
purification, threshold shrinkage, and scrambling comparisons.
```

Remaining weaknesses:

```text
small final diagnostic;
finite hard alphabet;
threshold rule still designed;
weighted-power diagnostic not yet computed in the final model;
early/late mutual information not yet added to the best final scan;
no simple time-independent autonomous Hamiltonian.
```

## Takeaway

The broad ingredients are represented in the literature:

```text
Page curves without gravity;
qubit evaporation;
unitary transport;
spin-chain Page dynamics;
Schwarzschild-like qubit evaporation.
```

The less obviously duplicated package is:

```text
finite non-gravitational system
+ Schwarzschild-like thermodynamic scaling
+ accelerating evaporation from weighted outgoing channels
+ shrinking capacity
+ locally thermal hard radiation
+ global/soft purification
+ scrambling comparisons.
```

That is the interesting result candidate.
