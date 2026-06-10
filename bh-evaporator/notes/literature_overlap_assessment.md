# Literature Overlap Assessment

## Purpose

This note checks the current evaporator program against nearby literature.

The question is not:

```text
Has anyone used qubits, spins, random circuits, or Page curves for black-hole
evaporation?
```

The answer to that is yes.

The useful question is:

```text
Has the specific thermodynamic package been built already:

  shrinking finite Hilbert-space sectors
  plus S ~ M^2 state counting
  plus negative heat capacity
  plus matrix-element-derived emission
  plus accelerating power
  plus controls showing that the mass/entropy relation matters
  plus a diagnostic like outgoing weighted phase space W?
```

## Current Program

Our current program has four layers.

```text
Layer 1: non-gravitational Page-like entropy dynamics.
Layer 2: shrinking internal Hilbert-space evaporators.
Layer 3: black-hole-like thermodynamic backbone:
         S ~ M^2, T ~ 1/M, C < 0, accelerating emission.
Layer 4: mechanism diagnostics:
         P(t) = <W>_t with W_i = sum_f Gamma_fi omega_fi,
         plus sector-profile and selection-profile decompositions.
```

Only layers 3 and 4 look potentially distinctive.

## What Is Already Covered

### Page curves without gravity

This is already established.

Glatthard shows Page-curve-like entanglement dynamics in ordinary open
quantum systems relaxing toward low-temperature equilibrium. The mechanism is
not gravitational: entanglement rises during relaxation and falls as the
system approaches its final low-entropy state.

Relevant papers:

```text
Jonas Glatthard,
"Page-curve-like entanglement dynamics in open quantum systems",
arXiv:2401.06042,
https://arxiv.org/abs/2401.06042.

Jonas Glatthard,
"Thermodynamics of the Page curve in Markovian open quantum systems",
arXiv:2501.09082,
https://arxiv.org/abs/2501.09082.
```

Impact:

```text
We should not sell "Page-like curves without gravity" as new.
```

### Qubit and random-unitary black-hole evaporation models

This is crowded.

The Page/Hayden-Preskill line already treats black holes as finite quantum
systems emitting radiation into an external register, often with random
unitary dynamics.

Examples:

```text
Don Page,
"Information in black hole radiation",
Phys. Rev. Lett. 71, 3743 (1993).

Patrick Hayden and John Preskill,
"Black holes as mirrors: quantum information in random subsystems",
JHEP 09 (2007) 120.

Steven G. Avery,
"Qubit Models of Black Hole Evaporation",
arXiv:1109.2911,
https://arxiv.org/abs/1109.2911.

H. Osuga and Don N. Page,
"Qubit Transport Model for Unitary Black Hole Evaporation",
arXiv:1607.04642,
https://arxiv.org/abs/1607.04642.
```

Impact:

```text
We should not sell "finite qubit evaporator" or "unitary radiation register"
as new.
```

### Spin-chain Page-curve models

Spin chains are also not new as black-hole evaporation toy models. There are
recent local-Hamiltonian models where a spin chain plays the black hole and a
growing environment plays the radiation.

Representative recent example:

```text
"Emergence of Page curves in local quantum dynamics",
actually titled:
"Kinematic Emergence of the Page Curve in a Local Transverse-Field Ising
Model",
arXiv:2603.17000,
https://arxiv.org/abs/2603.17000.
```

Impact:

```text
Track E is not novel because it uses a spin chain.

Its only possible value is that it combines the spin chain with the
black-hole thermodynamic schedule and the W-diagnostic controls.
```

### Page-curve models with changing Hilbert-space decomposition

There are toy models where the black-hole/radiation split changes during
evaporation and where qubits are transferred from one side to the other.

Examples include qubit transport models and circuit models of evaporation.
Broda also discusses semicausal black-hole evaporation models with changing
Hilbert-space decompositions.

Relevant references:

```text
H. Osuga and Don N. Page,
"Qubit Transport Model for Unitary Black Hole Evaporation",
arXiv:1607.04642,
https://arxiv.org/abs/1607.04642.

B. Broda,
black-hole evaporation circuit / semicausal-model papers,
including:
"Unitary (semi)causal quantum-circuit representation of black hole
evaporation",
arXiv:2310.04744,
https://arxiv.org/abs/2310.04744.
```

Impact:

```text
We should not sell "shrinking black-hole register and growing radiation
register" as new.
```

### Negative heat capacity in black-hole information discussions

The importance of black-hole thermodynamics has been discussed in qubit
models. Hotta, Nambu, and Yamaguchi are especially relevant because their
abstract says their multi-qubit model reproduces thermal properties of
four-dimensional Schwarzschild black holes while including Hawking-particle
emission and soft-hair evaporation.

Relevant reference:

```text
Masahiro Hotta, Yasusada Nambu, and Koji Yamaguchi,
"Soft-Hair-Enhanced Entanglement Beyond Page Curves in a Black-hole
Evaporation Qubit Model",
arXiv:1706.07520,
https://arxiv.org/abs/1706.07520.
```

Impact:

```text
"Qubit models reproducing aspects of Schwarzschild thermodynamics" are not
new. We need to distinguish our matrix-element/phase-space mechanism and
controls from this line, or concede overlap.
```

## What Seems Less Covered

The part that I did not find clearly pre-existing is the whole combination:

```text
1. A finite non-gravitational evaporator with explicit shrinking sectors.
2. Sector entropy chosen so S_n ~ n and M_n ~ sqrt(n), giving S ~ M^2.
3. Energy-lowering emission rates computed from actual intersector matrix
   elements rather than imposed by hand.
4. A robust acceleration/deceleration contrast between sqrt-mass and
   linear-mass controls.
5. A local-vs-scrambled removal comparison showing that local structure can
   preserve or enhance acceleration.
6. A unifying diagnostic:

      P(t) = <W>_t,
      W_i = sum_f Gamma_fi omega_fi,

   with sector-profile versus selection-profile explanations.
```

This is narrower than the original ambition, but it is also more defensible.

## Current Overlap Table

```text
Claim / Ingredient                                  Covered already?   Our status
-----------------------------------------------------------------------------------------------
Page-like entropy curves without gravity            yes                not novel
Qubit black-hole evaporation models                 yes                not novel
Shrinking BH register / growing radiation register  yes                not novel
Spin-chain evaporation toy models                   yes                not novel
Negative heat capacity is relevant                  yes                not novel
Finite evaporator with S ~ M^2 by area register     partly             useful, but abstract
Local spin-chain blocks with S ~ M^2 schedule       likely nearby       possible bridge result
Matrix-element-derived accelerating emission        unclear            potentially useful
sqrt-mass vs linear-mass controls                   not found clearly   potentially distinctive
W-profile acceleration diagnostic                   not found clearly   best current hook
Full Page turnover with thermodynamic acceleration  not yet achieved   not claimable
```

## Positioning Consequence

The project should not be framed as:

```text
Here is a spin-chain black-hole model.
Here is a Page curve without gravity.
Here is a shrinking Hilbert-space model.
```

Those sound like "me too" claims.

The better framing is:

```text
We use finite quantum evaporators to isolate the thermodynamic backbone of
black-hole evaporation. The key object is the outgoing weighted phase space W.
The simulations show that Page-like information flow, shrinking state space,
and negative heat capacity are not individually enough; acceleration appears
when the evaporation trajectory moves into larger W. In area-counting spin
chains this happens robustly for the black-hole-like sqrt mass law and fails
for linear-mass controls.
```

## Honest Verdict

Most of the vocabulary and model class are already in the literature.

The possible new result is not a new kind of black-hole toy model. It is a
controlled diagnostic statement about black-hole-like thermodynamic
evaporation in finite systems:

```text
accelerating evaporation is controlled by the outgoing weighted phase-space
profile, and the black-hole mass/entropy relation can make this profile
increase along a shrinking quantum trajectory.
```

That is worth pursuing only if we keep the paper centered on the diagnostic
and the controls, not on the existence of qubit/spin-chain Page models.

## Next Literature Checks

Before claiming novelty, check more carefully for papers containing these
specific ingredients:

```text
1. "negative heat capacity" plus "spin chain" plus "Page curve";
2. "shrinking Hilbert space" plus "local Hamiltonian" plus "black hole
   evaporation";
3. "emission rates" or "Fermi golden rule" plus "Page curve" toy evaporator;
4. "black hole evaporation" plus "density of states" plus "matrix elements";
5. "Page curve" plus "thermodynamic black hole evaporation schedule".
```

The current evidence says the broad area is crowded but the W-diagnostic
package may still be open.
