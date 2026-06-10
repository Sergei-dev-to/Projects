# Closing the Decoupling Gap Without New Proofs

## Question

Can the remaining scrambling/decoupling gap be closed using known literature,
with no new numerics and no bespoke proof of deterministic expander dynamics?

The gap is:

```text
fixed shell mixer
  -> decoupling of the evaporation code subspace.
```

The direct target is:

```text
early:
  I(Q : R_so_far) small;

late:
  I(Q : B_remaining) small.
```

Equivalently, in trace norm:

```text
rho_QR ~= rho_Q tensor rho_R       early,
rho_QB ~= rho_Q tensor rho_B       late.
```

## Answer

Yes, if the shell mixer is allowed to be a theorem-backed scrambling object:

```text
approximate unitary 2-design,
random circuit with known decoupling,
or quantum tensor-product expander.
```

For a concrete deterministic spin Hamiltonian on an expander graph, the same
closure does not appear to exist off the shelf.  The expander literature gives
fast operator growth and OTOC motivation.  The channel-scrambling literature
turns OTOC decay into mutual-information decoupling.  The exact bridge from a
specified fixed expander spin Hamiltonian to the needed evaporation-channel
decoupling bound remains the hard step.

So the way to close the gap without original work is to change the mixer class.

## Standard Closure Route

Use the following chain:

```text
approximate unitary 2-design
  -> decoupling theorem
  -> Page-purity and code-subspace information flow.
```

This is standard:

```text
Dankert-Cleve-Emerson-Livine:
  approximate unitary 2-designs reproduce the second moments used in many
  quantum-information protocols.

Szehr-Dupuis-Tomamichel-Renner:
  decoupling holds when the unitary is drawn from an approximate two-design.

Brown-Fawzi:
  random quantum circuits can be analyzed directly through decoupling.

Harrow-Low:
  efficient quantum tensor-product expanders give efficient approximate
  unitary k-designs.
```

For the present evaporator, this gives:

```text
choose the in-shell mixer from a known approximate 2-design or tensor-product
expander construction;

apply the approximate-design decoupling theorem to the block evaporation
channel;

recover the Page/island and Hayden-Preskill-style information-flow statements
without a new proof of scrambling.
```

## What This Buys

This closes the fine-grained information-flow part of Result 2.

The full conditional package becomes:

```text
S(E) ~ E^2
  -> T ~ 1/E, negative heat capacity, DOS-ratio thermality.

A(E)-many independent weak channels
  -> Hawking number flux, power, lifetime scaling.

approximate-design / tensor-product-expander shell mixing
  -> Page curve, early/late correlations, code-subspace decoupling.
```

The information-flow calculation can then be cited rather than reproved.

## What It Costs

The mixer becomes more abstract.

The statement is no longer:

```text
a simple deterministic nonintegrable spin Hamiltonian on an expander graph is
proved to scramble enough.
```

The statement becomes:

```text
the shell mixer is chosen from a standard class known to provide the required
low-order randomness or decoupling.
```

This is still a legitimate non-gravitational quantum model.  It is closer to
the tensor-network/random-circuit/unitary-design literature than to an ordinary
condensed-matter Hamiltonian.

## Three Possible Mixer Standards

### 1. Approximate unitary 2-design

Use an exact or approximate unitary 2-design on each active shell.

This is enough for:

```text
second-Renyi Page curve;
Page-purity estimates;
code-subspace decoupling;
Hayden-Preskill-style recovery at the second-moment level.
```

Fixed Renyi-`n` replica moments require the corresponding `n`th moments.

This is the cleanest standard assumption.

### 2. Random circuit decoupling

Use random local circuits of sufficient depth, or the Brown-Fawzi decoupling
result directly.

This keeps the model closer to physical circuit dynamics and existing
evaporator models, but it retains stochastic circuit language.

This route is the best if the paper wants to emphasize:

```text
finite-dimensional unitary quantum dynamics;
known decoupling;
minimal original proof burden.
```

### 3. Quantum tensor-product expander

Use a quantum tensor-product expander as the shell mixer.  Harrow-Low give
efficient constructions of constant-degree, constant-gap quantum
`k`-tensor-product expanders, with approximate unitary `k`-designs as a
corollary.

This is closest in spirit to the expander idea:

```text
expansion is built in as the mathematical object,
and low-order moment control is theorem-backed.
```

The price is that the object is a quantum-information mixer rather than a
simple spin Hamiltonian.

## Best Way To Close the Gap

For Result 2, the cleanest closure is:

```text
Use an approximate 2-design or quantum tensor-product expander as H_mix on each
microcanonical shell.
```

Then state:

```text
The fine-grained information-flow statements follow from standard decoupling
theorems for approximate two-designs.  Higher fixed Renyi moments require the
corresponding higher design/tensor-product-expander order.
```

This avoids a new deterministic-Hamiltonian scrambling proof.

## What Happens to the Expander Spin Hamiltonian?

Keep it as a possible microscopic refinement:

```text
deterministic expander spin Hamiltonian
  -> candidate realization of the design/decoupling mixer.
```

The current literature supports the operator-growth part of that statement.
It does not close the full decoupling implication for the evaporation
partitions.  That refinement should not be required for Result 2.

## Recommended Position

Split the result into two levels:

```text
Result 2A:
  ideal Hamiltonian evaporator with theorem-backed approximate-design or
  tensor-product-expander shell mixing.

Result 2B:
  deterministic expander spin Hamiltonian as a proposed microscopic
  realization of the mixer.
```

Result 2A is closeable using known literature.

Result 2B remains a harder dynamical problem.

This split prevents scope creep.  It also keeps the main result alive without
pretending that the deterministic spin-Hamiltonian proof is already known.

## Key References

```text
Dankert, Cleve, Emerson, Livine,
"Exact and approximate unitary 2-designs and their application to fidelity
estimation", Phys. Rev. A 80, 012304 (2009), arXiv:quant-ph/0606161.

Szehr, Dupuis, Tomamichel, Renner,
"Decoupling with unitary approximate two-designs",
New J. Phys. 15, 053022 (2013), arXiv:1109.4348.

Brown, Fawzi,
"Decoupling with random quantum circuits",
Commun. Math. Phys. 340, 867 (2015), arXiv:1307.0632.

Harrow, Low,
"Efficient Quantum Tensor Product Expanders and k-designs",
arXiv:0811.2597.

Hosur, Qi, Roberts, Yoshida,
"Chaos in quantum channels", JHEP 2016, arXiv:1511.04021.

Yoshida, Kitaev,
"Efficient decoding for the Hayden-Preskill protocol", arXiv:1710.03363.
```
