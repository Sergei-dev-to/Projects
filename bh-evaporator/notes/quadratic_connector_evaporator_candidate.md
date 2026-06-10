# Quadratic Connector Evaporator Candidate

## Purpose

State the strongest current candidate in the form needed for the main goal:

```text
Here is H_total.
Here is the Hilbert space.
Here is the initial state class.
Here is what must be measured.
```

This is not yet a successful autonomous model. It is the most constrained
target left after the no-settling gates.

## Hilbert Space

For a maximum core size `N_max`, take:

```text
site sector:
  N_max constituent degrees of freedom;

connector sector:
  one connector degree for each unordered pair (i,j);

radiation sector:
  outgoing modes coupled to connector excitations;

optional bound/separation sector:
  variables that diagnose whether a site belongs to the active core.
```

The active core at size `N` contains:

```text
N active sites;
L(N) = N(N-1)/2 active connector modes.
```

The area-like state count comes from the connector sector:

```text
S_core,max(N) ~ L(N) log q ~ N^2.
```

## Hamiltonian Target

The target Hamiltonian is:

```text
H_total =
  H_site
+ H_conn,z=2
+ H_site-conn
+ H_rad
+ H_emit.
```

### Site energy

The site sector gives the mass scale:

```text
H_site ~ mu * number of active sites + binding/separation terms.
```

So:

```text
M_core ~ mu N.
```

Together with `S ~ N^2`, this gives:

```text
T ~ dM/dS ~ 1/N.
```

### Quadratic connector band

The connector sector should have a protected quadratic low-energy band:

```text
omega_k ~ k^2 / L(N)^2.
```

Since `L(N) ~ N^2`, thermal occupation at `T ~ 1/N` samples many soft
connector modes and gives typical emitted energies of order `1/N`.

Standard physics language:

```text
z = 2 dispersion;
type-B Goldstone-like mode;
ferromagnetic-magnon-like connector band.
```

### Emission coupling

The power scan shows that the naive local weight gives:

```text
P ~ N^-3/2
```

for the quadratic band.

To recover:

```text
P ~ N^-2,
```

the emission matrix element should scale as:

```text
|g(omega)|^2 ~ omega^{1/2}.
```

Script:

```text
sim/connector_power_coupling_scan.py
```

Result:

```text
connector_ring_crit, a=0.50: P exponent = -2.005
powerlaw_alpha2, a=0.50: P exponent = -2.000
```

So the emission coupling is now a hard requirement. It cannot be left as an
unspecified local operator.

## Initial State Class

Use states with:

```text
one compact active core of size N_init;
connector sector internally mixed or thermal around T ~ 1/N_init;
radiation sector initially empty or low-occupation;
total state pure, with optional purifier for mixed-core preparation.
```

The initial-state class should include:

```text
microcanonical connector-shell states;
random pure states in an energy window;
scrambled low-radiation states;
controls with weak or absent connector mixing.
```

## Evolution Picture

The corrected scale picture is:

```text
microscopic emission:
  one connector/radiation quantum with energy ~ 1/N;

coarse shrink:
  after O(N) microscopic emissions, the active core changes from N to N-1;

temperature change:
  O(1/N^3) per microscopic quantum;
  O(1/N^2) per coarse N -> N-1 shrink.
```

The autonomous Hamiltonian must produce this without an external deletion rule.

## Measured Diagnostics

The candidate must be tested in one combined run:

```text
state count:
  S_core,max(N) ~ N^2;

mass:
  M_core measured from H_site + active connector energy;

temperature:
  microcanonical T(E) or finite-difference T(N);

soft spectrum:
  emitted omega ~ 1/N;

power:
  P(N) ~ N^-2 if |g(omega)|^2 ~ omega^{1/2};

heating:
  T_core rises as M_core decreases;

information flow:
  core-radiation entropy and early/late radiation mutual information;

controls:
  linear connector band;
  grid connector band;
  no spectral coupling weight;
  weak mixing.
```

## What Is Now Fixed By The Gates

The gates have fixed these choices:

```text
linear connector band:
  good power proxy, poor heating;

grid critical band:
  poor heating;

quadratic connector band:
  good heating, needs spectral emission weight for P ~ N^-2;

one quantum per N -> N-1 step:
  wrong scale;

many quanta per N -> N-1 step:
  required.
```

## Main Remaining Objection

The model still needs a natural origin for:

```text
1. the one-dimensional ordering of O(N^2) connector modes;
2. the protected quadratic dispersion;
3. the |g(omega)|^2 ~ omega^{1/2} emission weight;
4. the autonomous slow shrinkage of the active core.
```

If those four are supplied by a recognizable microscopic Hamiltonian, this
branch reaches the main target. If they have to be assigned independently, the
branch becomes another engineered model.
