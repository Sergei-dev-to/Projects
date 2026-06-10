# Edge-Tension Gauge Droplet: Critical Review

## Purpose

Review the current edge-tension / finite-gauge droplet as a candidate result.

The standard is:

```text
interesting result, not paper-shaped optimism.
```

## What Is Actually Derived

The thermodynamic backbone is now genuinely derived from model ingredients.

For a connected planar finite-group gauge patch:

```text
dim H_phys(D) = q^(E - V + 1).
```

For a disk-like planar patch:

```text
E - V + 1 = number of plaquettes ~ area.
```

Therefore:

```text
S_R ~ R^2.
```

If the droplet energy is dominated by boundary line tension:

```text
M_R ~ perimeter ~ R.
```

Then:

```text
T_R = (dS/dM)^-1 ~ 1/R,
C < 0.
```

If the boundary radiates into a two-dimensional exterior bath:

```text
P_R ~ perimeter * T^3 ~ R * (1/R)^3 ~ 1/R^2.
```

So the strongest derived package is:

```text
S ~ M^2,
T ~ 1/M,
C < 0,
P ~ 1/M^2,
tau ~ M_0^3.
```

This is not coming from a prescribed black-hole schedule. It is coming from:

```text
area residual entropy + perimeter energy + 2D radiation phase space.
```

## Why This Is A Real Improvement

Track E had:

```text
S_n ~ n,
M_n ~ sqrt(n).
```

The mass law was assigned.

The edge-tension droplet has:

```text
S_L ~ L^2
M_L ~ L
```

from standard non-gravitational structures.

That is a meaningful improvement.

It also gives a clean non-gravitational control lesson:

```text
black-hole-like negative heat capacity does not require gravity;
it follows whenever entropy is extensive in area while energy is extensive in
boundary length.
```

## What Is Still Not Natural

### 1. The soft bulk is special

The model needs the constrained bulk states to be degenerate or nearly
degenerate.

For the `Z_q` gauge counting:

```text
Gauss law is imposed;
plaquette fluxes are not energetically lifted.
```

If we add the usual magnetic/flatness term and project to a topological ground
sector on a disk, the degeneracy collapses.

So this is not:

```text
ordinary gapped topological ground-state degeneracy.
```

It is:

```text
residual constrained entropy / flat constrained sector.
```

That is known in ice-rule/frustrated systems, but it is still the central
non-generic ingredient.

### 2. The droplet is kinematic so far

We specify a patch size `L`.

We have not derived a Hamiltonian whose low-energy configurations
spontaneously form a compact active droplet in a trivial exterior.

A more complete model needs:

```text
two phases,
an interface tension,
and some conserved or slow variable fixing the droplet size.
```

Without that, `L` is a sector label rather than a dynamically selected radius.

### 3. Pure line tension wants collapse

Boundary tension alone makes smaller droplets energetically favorable.

That is good for evaporation direction, but too strong if there is no barrier
or channel structure. The droplet would simply shrink/collapse if coupled to
anything that can absorb the released energy.

For an evaporator, that may be acceptable, but then we must explicitly model:

```text
how boundary energy leaves,
how shell entropy leaves,
and why the process is quasi-thermal rather than arbitrary collapse.
```

### 4. The 2D bath is chosen

The Schwarzschild-like power law depends on:

```text
P ~ boundary * T^3.
```

That is natural for radiation into a two-dimensional bath.

But it is a model choice.

In other bath dimensions:

```text
P ~ R * T^(d+1),
```

so the scaling changes.

The current model is therefore:

```text
a 2D black-hole-phenomenology analogue,
not a dimension-independent result.
```

### 5. Information flow is not derived

The shell dimension is:

```text
dim H_shell(L) = q^(2L - 1).
```

But we have not constructed the unitary map:

```text
H_L -> H_(L-1) tensor H_soft_rad(L) tensor H_hard_rad(L).
```

Until we do, claims about Page behavior are only bookkeeping expectations.

### 6. Hard/soft split is plausible but not automatic

The model suggests:

```text
hard radiation carries O(1/L) energy;
soft record carries O(L) entropy.
```

But that split must be implemented.

Otherwise the model could become:

```text
thermal bath plus hidden archive.
```

The soft record must participate in information diagnostics, not just be
declared.

## The Most Serious Attack

The most serious objection is:

```text
This is a residual-entropy droplet, not a black-hole analogue.
```

That objection is fair if the claim is:

```text
this models black holes microscopically.
```

But the better claim is:

```text
this is a non-gravitational quantum/statistical system that reproduces the
black-hole thermodynamic evaporation scalings because it has area entropy and
perimeter energy.
```

That is enough for the original program:

```text
separate generic black-hole phenomenology from genuinely gravitational
mechanisms.
```

## What The Result Would Say

If the channel side works, the message is:

```text
Much of the black-hole evaporation package is not uniquely gravitational.
It follows from a structural mismatch:

entropy lives in one geometric measure;
energy lives in a lower-dimensional boundary measure.
```

In 2D:

```text
S ~ area,
M ~ boundary length.
```

In Schwarzschild black holes:

```text
S ~ horizon area,
M ~ horizon radius.
```

The analogy is direct.

## What Is Still Needed For A Worthwhile Result

Minimum next result:

```text
Construct an explicit shell-eroding Stinespring map for the finite-gauge
droplet and show:

1. the core Hilbert space shrinks as q^(L^2);
2. shell entropy q^(2L-1) is transferred outward;
3. hard radiation energy follows epsilon_L ~ T_L;
4. hard radiation alone can be locally thermal;
5. hard + soft exterior purifies the process;
6. radiation entropy has Page-like turnover or at least Page-like
   hard/soft structure.
```

This would turn the current thermodynamic result into an evaporator result.

## Current Status

The edge-tension gauge droplet is now our strongest candidate core.

Status by feature:

```text
finite explicit quantum Hilbert space       yes
shrinking internal state space              yes, if erosion channel added
S ~ M^2                                     yes
T ~ 1/M, C < 0                              yes
accelerating Hawking-like power             yes, for 2D bath
rates from structural phase space           partially
unitary radiation                           not yet
Page-like diagnostics                       not yet
fully natural Hamiltonian dynamics          not yet
```

## Recommendation

Keep this branch.

Do not oversell it as topological black-hole microphysics.

Treat it as:

```text
a residual-entropy droplet evaporator.
```

The next serious task is not more thermodynamics. That part is done.

The next serious task is:

```text
build the explicit hard/soft erosion channel.
```

