# Current Audit After Structured Erosion

## Purpose

Pause before adding more construction and check whether the current edge-tension
gauge droplet result is being overcounted.

The standard is still:

```text
interesting result, not paper-shaped closure.
```

## What Looks Solid

The thermodynamic core is the strongest part.

For the finite-group gauge droplet:

```text
S_L = L^2 log q
M_L = 4 sigma L
T_L ~ 1/L
C < 0
```

With a two-dimensional exterior bath:

```text
P_L ~ boundary * T_L^3 ~ 1/L^2
tau ~ L_0^3.
```

This is not just the old Track E with a mass law inserted by hand. The scaling
comes from:

```text
area residual entropy + boundary energy + 2D radiation phase space.
```

That is the main result candidate.

## What The Erosion Tests Actually Show

The Level 2 erosion channel shows that minimal soft capacity is enough:

```text
H_shell -> H_hard tensor H_soft
dim H_soft = dim H_shell.
```

The structured shift/clock controls show that the hard/soft split does not
require Haar-random shell unitaries.

Observed pattern:

```text
hard radiation alone:
  close to thermal and weakly correlated across early/late bins;

hard + soft radiation:
  keeps strong early/late correlations.
```

This supports:

```text
F8 = P
F9 = P
F13 = P
```

but does not justify upgrading them to `Y`.

## Main Thing We May Have Missed

The positive radiation diagnostics start from a Haar-random pure state over the
full droplet Hilbert space.

That means the shell being eroded is already close to locally mixed, as expected
for a typical highly entangled state. The shift/clock maps then suppress hard
coherences because:

```text
rho_hh' ~ sqrt(p_h p_h') Tr(rho_shell U_h^dagger U_h')
```

and a locally mixed `rho_shell` makes different structured shell operations look
nearly orthogonal.

So the present result should be read as:

```text
a scrambled/typical droplet emits thermal-looking hard radiation while preserving
information in hard+soft correlations.
```

It should not yet be read as:

```text
any initial droplet state thermalizes under erosion.
```

That distinction matters. For basis-like or low-entanglement shell states, the
hard marginal may depend strongly on microscopic shell data.

## Other Possible Overcounts

### F6 depends on the bath dimension

The acceleration result uses:

```text
P ~ R T^3
```

which is natural for a two-dimensional exterior bath. In a different bath
dimension the power law changes.

### F7 is still the weakest physics entry

The hard probabilities are chosen thermally:

```text
p_h ~ exp(-epsilon_h / T_L).
```

They are not yet derived from boundary matrix elements or from a bath spectral
density. This is the largest remaining imposed ingredient.

### F2/F3 are channel-level, not Hamiltonian-level

The map:

```text
H_L -> H_(L-1) tensor H_hard tensor H_soft
```

is well-defined as a Stinespring erosion channel, but not yet derived as the
dominant transition of a local Hamiltonian.

### F13 is structured, not truly local

Shift/clock operations are structured operations on shell flux labels. They are
not yet explicit boundary-local link/plaquette moves with Gauss-law matching.

### Residual entropy is not topological ground-state entropy

The bulk entropy is residual constrained entropy. If a standard flatness or
magnetic term selects a unique disk ground state, the area degeneracy disappears.

This is not a flaw, but it must remain explicit.

## Current Conservative Status

```text
F1  Y  finite explicit gauge Hilbert space
F2  P  purifiable channel, not Hamiltonian evaporation
F3  P  shrinking sector under erosion, not dynamically selected yet
F4  Y  S ~ M^2
F5  Y  T ~ 1/M and C < 0
F6  Y  accelerating power for 2D bath
F7  P  thermal probabilities chosen, not derived
F8  P  hard/soft entropy bookkeeping, no large Page curve
F9  P  hard+soft early/late correlations in small runs
F10 Y  non-gravitational control system
F11 P  structural phase-space estimate, not old W diagnostic
F12 N  not a current control axis
F13 P  structured controls, not boundary-local Hamiltonian erosion
```

No downgrades are needed, but none of the `P` entries should be promoted yet.

## Best Next Test

Before pursuing a microscopic Hamiltonian, test initial-state dependence.

Compare:

```text
1. Haar-random full droplet state;
2. random state with shell locally mixed but controlled core entanglement;
3. product state between core and shell;
4. shell basis state;
5. low-entanglement shell superposition.
```

Run the same structured shift/clock/flux-partition channels and measure:

```text
latest hard trace distance from thermal;
hard-hard early/late mutual information;
hard+soft early/late mutual information.
```

Expected outcome:

```text
thermal hard radiation is robust for typical/scrambled shells;
it can fail for structured low-entanglement shells.
```

If that is what happens, the honest claim becomes sharper:

```text
the droplet needs scrambling/typicality for local hard thermality, while the
thermodynamic scaling itself comes from area entropy and boundary energy.
```

That would be a better result than pretending the channel works state-by-state.

## Test Completed

This test has now been run.

Relevant note:

```text
notes/initial_state_erosion_dependence_results.md
```

Result:

```text
The channel does not thermalize arbitrary initial states.
Thermal hard radiation is robust for typical or locally mixed shells.
Low-entanglement product states succeed or fail depending on the relation
between the shell state and the chosen structured map.
```

Therefore the correct next target is:

```text
derive or model internal scrambling of the constrained droplet before erosion.
```
