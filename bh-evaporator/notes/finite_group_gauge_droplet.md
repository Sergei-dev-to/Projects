# Finite-Group Gauge Droplet

## Purpose

Test the edge-tension droplet idea with an explicit microscopic Hilbert space.

The question:

```text
Can we get S ~ R^2 and M ~ R from ordinary non-gravitational structures,
instead of assigning M ~ sqrt(S)?
```

For a finite abelian lattice gauge theory, the answer is yes at the counting
level.

## Model

Take a connected planar patch `D` of a square lattice.

Use a finite gauge group:

```text
G = Z_q.
```

Put a `q`-state variable on every oriented edge:

```text
g_e in Z_q.
```

The unconstrained Hilbert space is:

```text
H_link = tensor over edges C^q
dim H_link = q^E
```

where `E` is the number of internal links in the patch.

Impose Gauss constraints at vertices:

```text
sum incoming/outgoing flux = 0 mod q.
```

For a connected graph, only `V - 1` of the `V` vertex constraints are
independent. Therefore the physical gauge-invariant Hilbert-space dimension is:

```text
dim H_phys(D) = q^(E - V + 1).
```

For a planar disk-shaped graph, Euler's formula gives:

```text
E - V + 1 = number of plaquettes inside D.
```

So:

```text
dim H_phys(D) = q^(Area in plaquettes).
```

This is the key result.

The area entropy is not imposed. It is the exact dimension of the constrained
physical Hilbert space.

## Square Patch

For an `L x L` square patch:

```text
plaquettes A_L = L^2
vertices    V_L = (L + 1)^2
edges       E_L = 2L(L + 1)
boundary    B_L = 4L
```

Then:

```text
E_L - V_L + 1
  = 2L(L+1) - (L+1)^2 + 1
  = L^2.
```

Therefore:

```text
dim H_L = q^(L^2)
S_L = L^2 log q.
```

This is exactly the black-hole-like entropy scaling if:

```text
L = linear size.
```

## Hamiltonian

Use a local constraint-enforcing Hamiltonian:

```text
H_constraint = Lambda * sum_v (1 - P_Gauss(v))
```

and then restrict to the physical low-energy sector:

```text
P_Gauss(v) = 1 for every vertex.
```

Inside that sector, take the bulk gauge configurations to be degenerate or
nearly degenerate.

Let the energy be dominated by the interface between the active gauge droplet
and the exterior trivial phase:

```text
M_L = sigma * B_L = 4 sigma L.
```

This is ordinary line tension.

It is not assigned to force `S ~ M^2`; it is the usual energy of a 2D droplet
whose cost lives on the boundary.

## Thermodynamics

With:

```text
S_L = L^2 log q
M_L = 4 sigma L
```

the continuum large-`L` derivative gives:

```text
beta_L = dS/dM
       = (2L log q) / (4 sigma)
       = L log q / (2 sigma).
```

Therefore:

```text
T_L = 2 sigma / (L log q).
```

So as the droplet loses energy and shrinks, it gets hotter.

The heat capacity is:

```text
C = dM/dT
  = -8 sigma^2 / (T^2 log q)
  = -2 L^2 log q.
```

Negative heat capacity is automatic.

## Discrete Shell Version

One erosion step:

```text
L -> L - 1.
```

The shell has:

```text
Delta A_L = L^2 - (L-1)^2 = 2L - 1
Delta S_L = (2L - 1) log q
Delta M_L = 4 sigma
```

The finite-difference inverse temperature is:

```text
beta_L^disc = Delta S_L / Delta M_L
            = ((2L - 1) log q) / (4 sigma).
```

Thus:

```text
T_L^disc = 4 sigma / ((2L - 1) log q)
         ~ 1/L.
```

The shell releases:

```text
O(L) entropy
```

with:

```text
O(1) energy.
```

So the typical energy per entropy unit scales as:

```text
Delta M / Delta S ~ 1/L.
```

That is the Hawking-temperature scaling.

## Radiation Rate

If the boundary radiates into a two-dimensional exterior bath, the thermal
power per unit boundary length scales as:

```text
p(T) ~ T^3.
```

The boundary length is:

```text
B_L = 4L.
```

So:

```text
P_L ~ B_L T_L^3
    ~ L * (1/L)^3
    ~ 1/L^2.
```

Since:

```text
M_L ~ L,
```

we get:

```text
dM/dt ~ -1/M^2.
```

This is the Schwarzschild evaporation scaling.

It comes from:

```text
area entropy;
perimeter energy;
2D radiation phase space.
```

## Information Bookkeeping

The physical Hilbert space factorizes imperfectly under geometric cuts because
of Gauss constraints. That is good, not bad: it is the gauge-theory version of
edge-mode bookkeeping.

For the simple counting model, the shell loss is:

```text
dim H_L / dim H_(L-1) = q^(2L - 1).
```

So the exterior record must have capacity:

```text
q^(2L - 1)
```

per erosion step if the full process is unitary.

This gives a concrete hard/soft split:

```text
hard radiation:
  ordinary bath quanta carrying energy ~ T_L;

soft record:
  gauge-invariant shell flux / edge-mode data with dimension q^(2L - 1).
```

Hard radiation alone can look thermal. The hard plus soft exterior record can
purify the shrinking gauge droplet.

## Why This Is Less Imposed

Previously:

```text
H_n = (C^d)^n
M_n = alpha sqrt(n)
```

The entropy law was simple, but the mass law was assigned.

Here:

```text
H_L = gauge-invariant states of a Z_q lattice gauge patch
S_L = L^2 log q
M_L = sigma * boundary length = 4 sigma L
```

Both scalings come from standard structures:

```text
Gauss-constrained link Hilbert space;
line-tension interface energy.
```

## What Is Still Put In

This is not a complete natural Hamiltonian evaporator yet.

Still chosen:

```text
1. bulk gauge configurations are degenerate/nearly degenerate;
2. energy is dominated by boundary tension;
3. exterior bath is two-dimensional;
4. erosion is the relevant decay channel;
5. the soft shell information is transferred outward unitarily.
```

But these choices are now physical model ingredients, not black-hole scalings
inserted directly.

## Main Weaknesses

### 1. The entropy is residual constrained entropy, not topological entropy

If we add a magnetic flatness term and select the topological ground state on a
disk, the degeneracy collapses to O(1).

So this model needs a highly degenerate constrained sector, not the usual
fully gapped topological ground-state sector.

That is acceptable for a toy evaporator, but it should be stated plainly.

### 2. The model is very soft

The bulk has many zero-energy states.

This is the point, but it may look artificial unless we identify a physical
mechanism for the flat constrained sector:

```text
frustration;
flat band;
gauge constraints without flux energy;
protected defect/fusion sectors.
```

### 3. Erosion dynamics is not derived yet

The counting says what happens if the droplet loses a boundary layer.

It does not yet derive a local Hamiltonian whose dominant decay channel is
boundary erosion.

## Current Verdict

This is a real improvement over the abstract shrinking register.

It gives a non-gravitational microscopic counting model where:

```text
dim H_L = q^(L^2)
S_L ~ L^2
M_L ~ L
T_L ~ 1/L
C < 0
P_L ~ 1/L^2
```

without assigning the black-hole thermodynamic schedule directly.

The next question is not whether the thermodynamics works. It does.

The next question is:

```text
Can we define a reasonable unitary erosion channel whose hard radiation is
locally thermal while the soft gauge-shell record purifies the process?
```

## Verification Script

Script:

```text
sim/finite_group_gauge_droplet.py
```

Output:

```text
sim/data/finite_group_gauge_droplet.csv
```

For `q = 2`, `sigma = 1`, the script verifies:

```text
gauss_exponent = E - V + 1 = plaquettes = L^2.
```

It also computes:

```text
T_L^disc = 4 sigma / ((2L - 1) log q)
P_L      = boundary * (T_L^disc)^3
```

The diagnostic:

```text
M_L^2 P_L
```

approaches a constant, confirming:

```text
P_L ~ 1/M_L^2.
```

Representative large-`L` rows:

```text
L   exponent   plaquettes   M      T_disc    P_disc     M^2 P
16  256        256          64     0.186     0.413      1691
17  289        289          68     0.175     0.364      1681
18  324        324          72     0.165     0.323      1673
19  361        361          76     0.156     0.288      1665
20  400        400          80     0.148     0.259      1659
```
