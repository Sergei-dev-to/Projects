# Option C: Detached-Qubit Radiation Design

## Purpose

Option C is the candidate route toward the all-phenomenology goal.

The aim is to combine:

```text
Track E thermodynamic backbone
```

with:

```text
explicit small radiation subsystems suitable for Page/early-late diagnostics.
```

This is different from the exact transition-record Stinespring construction.
The exact construction is faithful but not natural or scalable. Option C gives
up exact reproduction of the old reduced channel in exchange for a more natural
radiation register.

## Core Idea

At evaporation step `t`, the core has `n` spins:

```text
H_n = (C^2)^n.
```

Evaporation detaches one spin and sends it to radiation:

```text
H_n -> H_{n-1} tensor R_t,
R_t = C^2.
```

After multiple emissions:

```text
R = R_1 tensor R_2 tensor ... tensor R_T.
```

This gives a natural early/late split:

```text
R_early = R_1 ... R_k
R_late  = R_{k+1} ... R_T.
```

That is the structure needed for `F9`.

## One-Step Map

For boundary detachment, the computational-basis map is simple:

```text
|prefix>_1...(n-1) |b>_n
  ->
|prefix>_core |b>_R.
```

This is an isomorphism:

```text
(C^2)^n ~= (C^2)^(n-1) tensor C^2.
```

So at the Hilbert-space level, no information is destroyed. The core/radiation
split changes.

The same idea can be generalized:

```text
bulk detachment:
  detach one site from the chain;

scrambled detachment:
  apply random basis rotations before/after detachment as a control.
```

## Energy Bookkeeping

The core Hamiltonian in each sector is:

```text
H_n = M_n I + bandwidth * h_n.
```

with:

```text
M_n = alpha sqrt(n)       black-hole-like case
M_n = alpha n             linear control
```

A detached-qubit map is unitary as a Hilbert-space reshuffling, but it does not
by itself select energy-lowering transitions.

So we need an evaporation rule.

Candidate rule:

```text
1. express the initial n-spin state in the eigenbasis of H_n;
2. detach one qubit into R_t;
3. express the remaining (n-1)-spin core in the eigenbasis of H_{n-1};
4. assign emitted energy omega = E_{n,i} - E_{n-1,f};
5. allow or weight only omega > 0 transitions.
```

This is close to Track E, but radiation now carries the detached spin state
rather than a full transition label.

## Important Caveat

A two-dimensional radiation qubit cannot distinguish all transitions:

```text
|n,i> -> |n-1,f>.
```

Therefore Option C will not reproduce the old Track E reduced channel exactly.

That is acceptable only if it still preserves the thermodynamic backbone:

```text
S ~ M^2
T ~ 1/M
negative heat capacity
shrinking core
accelerating power
sqrt mass beats linear controls
local detachment beats or differs from scrambled controls
```

The success criterion is not exact channel faithfulness. It is phenomenological
faithfulness.

## Two Implementation Variants

### Variant C1: Deterministic Detachment With Energy Diagnostic

At each step:

```text
detach one qubit coherently;
update the core/radiation split;
compute the expected core energy after the split;
define emitted power as the decrease in core energy.
```

Pros:

```text
simple;
fully unitary as a changing bipartition;
excellent for Page/early-late entanglement.
```

Cons:

```text
may not model selective energy-lowering emission;
acceleration may disappear;
evaporation schedule is imposed by one-detachment-per-step.
```

### Variant C2: Energy-Filtered Detachment Channel

At each step:

```text
apply detachment amplitudes;
project/weight energy-lowering components using omega and spectral density;
renormalize as a conditional emission step.
```

Pros:

```text
closer to Track E thermodynamics;
can preserve W-style mechanism;
still emits a small radiation qubit.
```

Cons:

```text
not simply unitary unless no-emission branches and environment labels are kept;
may require a larger radiation/environment bin than one qubit;
more complex to interpret.
```

## Recommended First Test

Variant C1 has now been tested.

Reason:

```text
If deterministic detached-qubit evaporation already gives useful Page/early-late
structure while roughly preserving thermodynamic behavior, it is the cleanest
route.
```

Test only the minimum:

```text
n = 4,...,10
boundary detachment
sqrt mass vs linear mass
local Hamiltonian blocks
pure initial state
```

Observables:

```text
core energy versus step
emitted power
core dimension entropy n log 2
S2(core)
S2(early radiation)
S2(late radiation)
I2(early : late)
```

Success:

```text
1. core Hilbert-space size shrinks by construction;
2. radiation qubit chain is explicit;
3. Page-like core/radiation entropy appears;
4. early/late radiation mutual information becomes nonzero;
5. sqrt mass has a more black-hole-like power profile than linear mass.
```

Failure:

```text
1. emitted power is trivial or decelerates in both sqrt and linear cases;
2. early/late structure is purely kinematic and identical across controls;
3. core energy bookkeeping becomes meaningless;
4. model collapses into the same category as existing spin-chain Page models
   without adding the thermodynamic engine.
```

Result note:

```text
notes/detached_qubit_c1_results.md
```

Short verdict:

```text
C1 gives the desired explicit radiation-qubit architecture and produces a
Page-like core/radiation Renyi-2 profile plus nonzero early/late radiation
mutual information.

But the information structure is purely kinematic and identical for sqrt and
linear mass laws. The sqrt case accelerates only because the imposed mass
spacing M_n - M_{n-1} grows as n shrinks.
```

Therefore C1 is useful but insufficient.

Next move:

```text
move to C2: energy-filtered detached-qubit emission.
```

## What This Would Buy Us

If C1 or C2 works, the model would move toward:

```text
F8: Page-like radiation entropy
F9: early/late radiation structure
```

while retaining the core Track E value:

```text
black-hole-like thermodynamic controls.
```

That is the real all-phenomenology path.
