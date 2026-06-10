# Edge-Tension Constrained Droplet

## Purpose

Try to build the evaporator with fewer imposed ingredients.

Instead of declaring:

```text
S_R ~ R^2
M_R ~ R
T_R ~ 1/R
P_R ~ 1/R^2
```

we want a non-gravitational quantum system where these follow from standard
structural ingredients.

## Core Idea

Use a two-dimensional droplet with:

```text
1. extensive soft/constrained internal entropy in the droplet area;
2. energy dominated by boundary line tension;
3. ordinary radiation into a two-dimensional exterior bath.
```

Then:

```text
area entropy       S ~ area ~ R^2
line-tension mass  M ~ perimeter ~ R
temperature        T = (dS/dM)^-1 ~ 1/R
2D radiation       P ~ perimeter * T^3 ~ R * (1/R)^3 ~ 1/R^2
```

This is the cleanest natural thermodynamic engine we have found so far.

It is not gravity. It is a constrained soft droplet plus boundary tension.

## Microscopic Sketch

Take a finite disk-shaped patch `D_R` of a 2D lattice.

Inside the patch, use a constrained local Hilbert space, for example:

```text
finite-group lattice gauge theory;
string-net / fusion-net Hilbert space;
frustrated flat-band constrained model;
non-Abelian anyon/fusion defect network.
```

The low-energy core Hilbert space is:

```text
H_R = constrained physical states on D_R.
```

The important point:

```text
H_R is not a tensor product we attach by hand.
It is the physical constrained Hilbert space of a local model.
```

For many constrained models, the number of allowed configurations grows
exponentially with area:

```text
dim H_R ~ exp(s0 * Area(D_R)).
```

So:

```text
S_R = log dim H_R ~ s0 pi R^2.
```

This is the area law.

## Energy

Let the bulk constrained states be degenerate or nearly degenerate.

Let the dominant energy be the cost of the boundary between the active droplet
phase and the exterior trivial phase:

```text
M_R = sigma * Perimeter(D_R)
    = 2 pi sigma R.
```

This is not imposed as a black-hole mass law. It is the ordinary energy of a
droplet with line tension.

This is the central improvement over Track E:

```text
Track E imposed M ~ sqrt(S).
Here M ~ R and S ~ R^2 come from perimeter energy plus area entropy.
```

## Temperature And Negative Heat Capacity

With:

```text
S_R = s0 pi R^2
M_R = 2 pi sigma R
```

we get:

```text
dS/dR = 2 pi s0 R
dM/dR = 2 pi sigma
```

Therefore:

```text
beta_R = dS/dM = (s0/sigma) R
T_R = sigma / (s0 R).
```

As the droplet shrinks, it gets hotter.

The heat capacity is:

```text
C = dM/dT
  = -2 pi s0 R^2
```

so it is negative.

This is automatic from:

```text
entropy in area;
energy in perimeter.
```

## Evaporation

The droplet shrinks because the boundary line tension favors reducing the
boundary.

Couple the boundary locally to an exterior bath. Boundary erosion removes a
thin layer of constrained degrees of freedom:

```text
D_R -> D_(R-dR) + emitted exterior degrees.
```

For one lattice-thick shell:

```text
Delta Area ~ 2 pi R
Delta S ~ 2 pi s0 R
Delta M ~ 2 pi sigma
```

The shell releases O(R) entropy while releasing O(1) total energy.

That means the typical energy per entropy-carrying emitted quantum is:

```text
Delta M / Delta S ~ 1/R,
```

matching the microcanonical temperature.

## Radiation Rate

For a droplet radiating into a two-dimensional exterior bath, ordinary
blackbody scaling gives:

```text
power per boundary length ~ T^3.
```

The emitting boundary length is:

```text
L_R ~ R.
```

Thus:

```text
P_R ~ L_R T_R^3
    ~ R * (1/R)^3
    ~ 1/R^2.
```

This gives the Schwarzschild-like acceleration law without prescribing the
rate by hand.

Since:

```text
M_R ~ R,
```

we get:

```text
dM/dt ~ -1/M^2,
```

and lifetime:

```text
tau ~ M_0^3.
```

## Information Flow

The constrained shell has many internal states:

```text
dim H_shell(R) ~ exp(const * R).
```

When the boundary erodes, those shell degrees must be transferred into the
exterior if the total evolution is unitary.

This naturally gives a hard/soft split:

```text
hard radiation:
  ordinary bath quanta carrying energy ~ T ~ 1/R;

soft radiation / memory:
  constrained shell state, fusion labels, gauge labels, or defect labels
  needed to purify the emitted hard radiation.
```

The Page question then becomes concrete:

```text
Does hard radiation alone look thermal while hard+soft radiation purifies?
Do late shells carry correlations with early shells after the remaining core
Hilbert space becomes smaller than the exterior record?
```

This is not solved automatically, but the Hilbert-space bookkeeping is now
physical rather than abstract.

## Why This Is Better Than The Previous Anyon Gas Idea

The bad anyon version was:

```text
put R^2 gapped anyons in the droplet.
```

Then:

```text
energy ~ R^2,
```

which destroys the black-hole scaling.

The better version is:

```text
bulk constrained/topological/fusion degeneracy is soft;
energy is carried mainly by the boundary tension.
```

So:

```text
entropy ~ area;
energy ~ perimeter.
```

This is the key separation.

## What Is Still Chosen

This model is not assumption-free.

Still chosen:

```text
1. a constrained local model with extensive soft entropy;
2. a boundary line tension;
3. coupling to an exterior 2D radiation bath;
4. a unitary erosion channel that transfers shell information outward.
```

But these are ordinary physical structures, not a prescribed black-hole
schedule.

Derived from those structures:

```text
S ~ R^2;
M ~ R;
T ~ 1/R;
C < 0;
P ~ 1/R^2;
tau ~ R_0^3;
Delta S_shell ~ R;
energy per shell state ~ 1/R.
```

## Best Microscopic Candidates

### 1. Finite-group lattice gauge droplet

Physical Hilbert space:

```text
gauge-invariant states on links inside D_R.
```

At weak/zero Hamiltonian inside the constrained sector:

```text
dim H_R grows exponentially with area.
```

Boundary line tension comes from the interface between the active gauge phase
and the exterior trivial phase.

Pros:

```text
very explicit constrained Hilbert space;
easy counting;
non-gravitational.
```

Cons:

```text
bulk degeneracy is a strong flat-sector assumption;
not automatically topologically protected.
```

### 2. String-net / fusion-net droplet

Physical Hilbert space:

```text
allowed fusion/string-net configurations on D_R.
```

Pros:

```text
natural anyonic/fusion interpretation;
physical constrained states after local fusion rules;
closer to the horizon/fusion story.
```

Cons:

```text
ordinary string-net ground states on a disk are not exponentially degenerate;
we need a constrained/flat or defect-rich sector.
```

### 3. Frustrated flat-band constrained droplet

Physical Hilbert space:

```text
macroscopically many local zero-energy configurations.
```

Pros:

```text
extensive residual entropy is natural in frustrated systems;
energy can be boundary dominated.
```

Cons:

```text
less topological;
may look too classical unless quantized carefully.
```

## Current Verdict

This is the most promising "least imposed" model so far.

The key mechanism is:

```text
black-hole-like thermodynamics = area entropy + boundary/perimeter energy.
```

No gravity is needed for that.

The model would test whether the black-hole evaporation package follows from:

```text
soft extensive constrained entropy;
boundary-tension energy;
ordinary radiative phase space;
unitary shell erosion.
```

This is more natural than:

```text
generic shrinking qubits with M ~ sqrt(n)
```

and more viable than:

```text
R^2 energetic anyons.
```

## Next Work

The next step should be analytic, not numerical:

```text
1. Pick the simplest constrained Hilbert space whose dimension can be counted.
2. Derive S_R, M_R, T_R, C_R, P_R.
3. Define a shell-eroding Stinespring map.
4. Check whether Page-like hard/soft diagnostics are meaningful.
5. Only then run a small simulation.
```

The finite-group lattice-gauge droplet is probably the easiest first version.

