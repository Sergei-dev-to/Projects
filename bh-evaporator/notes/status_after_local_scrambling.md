# Status After Local Scrambling Diagnostic

## Purpose

Review where the edge-tension gauge droplet stands after the initial-state and
local-scrambling tests.

The goal is not to smooth the story. The goal is to keep track of what is
actually established and what remains inserted by hand.

## Current Best Claim

The strongest claim is now:

```text
A non-gravitational constrained 2D droplet with area residual entropy and
boundary energy reproduces the black-hole-like thermodynamic evaporation
scalings. If its soft constrained degrees locally scramble before erosion, a
structured hard/soft erosion channel gives locally thermal hard radiation while
keeping information in hard+soft correlations.
```

This is stronger than the earlier area-register or Track E result because:

```text
S ~ M^2 is no longer assigned by hand.
```

It follows from:

```text
S ~ area,
M ~ boundary length.
```

## What Is Solid

### 1. Thermodynamic backbone

For the finite-group gauge droplet:

```text
dim H_L = q^(L^2)
S_L = L^2 log q
M_L = 4 sigma L
T_L ~ 1/L
C < 0
```

With a 2D exterior bath:

```text
P_L ~ boundary * T_L^3 ~ 1/L^2.
```

So:

```text
S ~ M^2,
T ~ 1/M,
dM/dt ~ -1/M^2,
tau ~ M_0^3.
```

This remains the main result candidate.

### 2. Minimal soft record is enough

The Level 2 erosion channel:

```text
H_shell -> H_hard tensor H_soft,
dim H_soft = dim H_shell
```

does not need an oversized archive. Hard radiation can look thermal while the
soft record carries the information needed for purification.

### 3. The hard/soft split is not purely Haar-random

Structured shift/clock shell maps reproduce the hard/soft pattern when the
shell is locally mixed.

This matters because the radiation result is not entirely a random-unitary
artifact.

### 4. Initial-state dependence is understood

The erosion map does not thermalize arbitrary states.

It works for:

```text
Haar-like full states;
outer-shell maximally mixed states;
locally scrambled shell states.
```

It can fail for:

```text
basis-like or uniform product states,
depending on the erosion map.
```

This is now a feature of the model, not a hidden bug:

```text
thermal hard radiation requires local shell typicality.
```

### 5. Local scrambling can supply shell typicality in small tests

A modest-depth nearest-neighbor plaquette-flux circuit repairs the product-state
failures.

At depth `D = 4`, both generic local gates and flux-conserving local gates make
the hard radiation close to thermal in the tested cases.

The fixed-Floquet follow-up also works:

```text
notes/fixed_floquet_scrambling_results.md
```

There, each local gate is generated once and reused at every layer. The
previously failing product states are still repaired, including with
flux-conserving two-site gates.

A first fixed-Hamiltonian smoke test also works:

```text
notes/hamiltonian_scrambling_smoke_results.md
```

There, a time-independent nearest-neighbor flux-conserving Hamiltonian on
plaquette-flux variables repairs the two clearest product-state failures at
`L0 = 3`.

So the required assumption has narrowed from:

```text
the whole droplet is Haar-scrambled
```

to:

```text
the constrained droplet can plausibly use fixed local dynamics to mix the next
shell before it erodes.
```

That is a meaningful improvement.

## What We May Still Be Missing

### 1. The local Hamiltonian result is still only a smoke test

The latest diagnostic improves on fixed Floquet circuits by using a fixed local
Hamiltonian.

That is not yet:

```text
a broad Hamiltonian parameter scan;
large-size evidence;
link-variable gauge dynamics;
thermalization under one microscopic model.
```

It proves sufficiency in the smallest exact failure test, not generic natural
Hamiltonian occurrence.

### 2. Plaquette-flux locality is not automatically microscopic locality

We represented the gauge droplet by plaquette-flux q-dits.

Nearest-neighbor gates on plaquette fluxes are local in the dual plaquette
variables. That is plausible, because electric link operators in a lattice
gauge theory change adjacent plaquette fluxes.

But we have not yet written the corresponding link-Hilbert-space Hamiltonian.

So current locality is:

```text
local in the effective plaquette-flux representation.
```

Not yet:

```text
derived from local link operators with Gauss-law matching at the boundary.
```

### 3. The flux-conserving proxy is not the full gauge constraint

The `flux_conserving` circuit conserves two-site total flux mod q.

This is a stricter and more structured test than generic gates, but it is only a
toy proxy. It is not the same as deriving the dynamics from a Kogut-Susskind or
quantum-link Hamiltonian.

### 4. F7 is improved but still partial

The hard probabilities are no longer purely chosen.

Relevant note:

```text
notes/microcanonical_emission_derivation.md
notes/microcanonical_collision_hamiltonian_results.md
```

At the rate-equation level:

```text
Gamma_L(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

Since:

```text
S(M) = (M / 4 sigma)^2 log q,
```

the state-count ratio gives:

```text
exp[S(M - omega) - S(M)] ~ exp(-omega / T_L)
```

with finite-size corrections of order `1/L^2` for typical quanta.

What remains not derived:

```text
microscopic matrix elements;
greybody factors;
one autonomous local emission Hamiltonian;
the absolute normalization of the evaporation rate.
```

The erosion collision step itself is now Hamiltonian-generated by:

```text
H_coll = g (V + V^\dagger).
```

So F7 is much stronger than before, but still `P`.

### 5. Page behavior is still not a full Page curve

The diagnostics show:

```text
hard radiation locally thermal;
hard-hard early/late mutual information near zero;
hard+soft early/late mutual information nonzero.
```

That is Page-like hard/soft information structure.

It is not yet:

```text
a large-system Page curve;
a Page-time turnover;
decoding/recovery;
late hard radiation carrying information visible without soft records.
```

So `F8 = P` and `F9 = P` remain correct.

### 6. The droplet itself is still a sector, not a dynamical phase

We specify an `L x L` active patch.

We have not built a Hamiltonian whose configurations naturally form a compact
droplet with:

```text
soft constrained bulk;
trivial exterior;
positive interface tension;
slow boundary erosion.
```

This is the main physical-model gap.

### 7. The 2D bath is essential

The Schwarzschild-like acceleration uses:

```text
P ~ R T^3.
```

That is the 2D radiation law. In other exterior dimensions the scaling changes.

This is fine, but the claim should remain:

```text
2D non-gravitational analogue.
```

Not:

```text
dimension-independent black-hole universality.
```

### 8. Small-size numerics can hide scaling problems

The exact tests are at:

```text
L0 = 3 mostly;
L0 = 4 spot checks.
```

The evidence is useful because the failure modes already show up there. But
large-system claims need either:

```text
analytic estimates;
tensor-network simulation;
Monte Carlo typicality estimates;
or a much cheaper diagnostic.
```

## Current F-Table Status

The edge-tension row should remain:

```text
Edge-tension gauge droplet    Y  P  P  Y  Y  Y  P  P  P  Y   P   N   P
```

No `P` should be upgraded yet.

The local-scrambling result strengthens the explanation behind:

```text
F8, F9, F13
```

but it does not turn them into `Y`, because the scrambler is still a circuit
diagnostic rather than a derived Hamiltonian.

## Best Next Step

The next step should not be more circuit scans.

The useful next test is:

```text
optimize the Hamiltonian diagnostic and run a broader time/seed/size scan.
```

Minimum viable version:

```text
1. Keep q = 2 plaquette-flux variables.
2. Use a nearest-neighbor flux-conserving Hamiltonian.
3. Cache/eigendecompose H_mix once per seed.
4. Evolve by U(t) = exp(-i H_mix t) before erosion.
5. Measure shell purity, hard trace distance, and hard+soft early/late mutual
   information as a function of evolution time.
```

If that works, the scrambling assumption becomes much less artificial:

```text
one fixed local constrained Hamiltonian is enough across seeds/times/sizes.
```

The harder later step is:

```text
write the same dynamics in link variables as a gauge-local Hamiltonian.
```

## Bottom Line

We did not miss a fatal flaw, but we should not overclaim.

Current result quality:

```text
thermodynamic analogue: strong;
purifiable hard/soft channel: plausible and tested in small systems;
fixed local Floquet dynamics: positive small-system diagnostic;
fixed local Hamiltonian dynamics: positive smoke test only;
microcanonical hard weights: rate-level derivation;
collision Hamiltonian for erosion: positive;
full Page curve: not yet;
autonomous local emission Hamiltonian: not yet.
```

The program is still worth pursuing because each new test has narrowed an
assumption rather than merely adding decoration.
