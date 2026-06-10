# Golden-Rule Evaporator Plan

## Purpose

Move one step beyond the collision-channel construction.

The previous channel result showed that an erosion step can be represented by a
finite Hamiltonian block:

```text
H_coll = g(V + V^\dagger).
```

That is useful, but not enough. It still looks like a designed pulse. The next
test is whether the same evaporator logic survives in the standard
weak-coupling language:

```text
transition rate = matrix element squared
                x bath density of states
                x number of available final droplet states.
```

## Minimal Droplet Data

Use the edge-tension finite-gauge droplet:

```text
S_L = L^2 log q
M_L = 4 sigma L
B_L = 4L
```

Treating `L` as a smooth trajectory gives:

```text
S(M) = (M / 4 sigma)^2 log q
beta(M) = dS/dM
T_L ~ 1/L.
```

## Golden-Rule Rate

For weak coupling to an exterior bath:

```text
d Gamma_L(omega)
  ~ B_L |M(omega)|^2 rho_bath(omega)
     exp[S(M_L - omega) - S(M_L)] d omega.
```

The power is:

```text
P_L = integral omega d Gamma_L(omega).
```

For a 2D exterior bath:

```text
rho_bath(omega) x omega ~ omega^2
```

so:

```text
P_L ~ B_L T_L^3 ~ L (1/L)^3 ~ 1/L^2.
```

Since:

```text
M_L ~ L,
```

this gives:

```text
P_L ~ 1/M_L^2.
```

## Important Stress Test

There are two different notions of "emission" that should not be conflated.

### Small-quanta emission

The bath emits quanta with typical energy:

```text
omega ~ T_L ~ 1/L.
```

This is the Schwarzschild-like regime. Many small emissions gradually reduce
the droplet mass.

### Literal shell erosion

A single exact lattice transition:

```text
L -> L - 1
```

has energy:

```text
Delta M = 4 sigma.
```

But:

```text
Delta M / T_L ~ L.
```

So a whole-shell jump is a very high-energy event for large `L`, not a typical
Hawking quantum. It should be Boltzmann suppressed:

```text
exp[S_{L-1} - S_L] = q^(-(2L - 1)).
```

Therefore, if literal shell erosion fails to produce `P ~ 1/M^2`, that is not
necessarily a failure of the edge-tension droplet. It means the physical
interpretation should be:

```text
the droplet loses many small bath quanta, while the discrete L-sector changes
only after enough energy has accumulated to move to the next coarse sector.
```

## Script

```text
sim/golden_rule_evaporator.py
```

The script computes both:

```text
1. small_quantum:
   integrate over omega with smooth matrix elements;

2. whole_shell:
   force one L -> L-1 transition with omega = 4 sigma.
```

Outputs:

```text
sim/data/golden_rule_evaporator.csv
sim/data/golden_rule_evaporator_summary.csv
```

## Success Criteria

For the small-quantum branch:

```text
fit log P vs log M gives slope near -2;
M^2 P approaches a constant;
mean emitted omega is O(T).
```

For the whole-shell branch:

```text
failure is expected.
```

If the whole-shell branch were the only way to formulate evaporation, the model
would be in trouble. But if small-quanta emission works cleanly, the correct
coarse-grained picture is:

```text
mass drains continuously by bath emission;
the finite gauge droplet sectors provide the entropy curve;
erosion is a coarse update of the internal register, not one emitted Hawking
quantum.
```

## What This Does Not Yet Prove

This still assumes:

```text
smooth matrix elements;
a 2D exterior bath;
boundary coupling proportional to B_L;
the edge-tension entropy/mass curve.
```

So this is not yet a fully autonomous Hamiltonian model.

The diagnostic value is narrower:

```text
Does the standard golden-rule calculation preserve the black-hole-like
thermodynamic scalings once the state count and bath dimension are specified?
```
