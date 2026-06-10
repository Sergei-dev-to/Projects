# Golden-Rule Evaporator Results

## Question

Does the edge-tension droplet still give black-hole-like evaporation when the
emission schedule is computed by a golden-rule rate, rather than inserted as a
collision-channel probability?

## Script

```text
sim/golden_rule_evaporator.py
```

Outputs:

```text
sim/data/golden_rule_evaporator.csv
sim/data/golden_rule_evaporator_summary.csv
sim/data/golden_rule_evaporator_mild_power.csv
sim/data/golden_rule_evaporator_mild_power_summary.csv
sim/data/golden_rule_evaporator_soft_cutoff.csv
sim/data/golden_rule_evaporator_soft_cutoff_summary.csv
sim/data/golden_rule_evaporator_3d_bath.csv
sim/data/golden_rule_evaporator_3d_bath_summary.csv
```

## Baseline Setup

```text
q = 2
sigma = 1
bath_dim = 2
matrix profile = flat
L = 2 ... 80
fit range = L >= 20
```

The small-quantum golden-rule branch computes:

```text
d Gamma_L(omega)
  ~ B_L |M(omega)|^2 rho_bath(omega)
     exp[S(M_L - omega) - S(M_L)] d omega.
```

The whole-shell stress test forces:

```text
L -> L - 1
omega = 4 sigma.
```

## Main Result

Baseline output:

```text
model          slope log P/log M   mean M^2 P last10
small_quantum            -2.0058           3068.6102
whole_shell             -60.6575          1.7783e-35
```

So:

```text
small-quanta golden-rule emission gives P ~ M^-2;
literal whole-shell emission fails exponentially.
```

This is exactly the distinction we needed to expose.

## Why Whole-Shell Emission Fails

The shell gap is:

```text
Delta M = M_L - M_{L-1} = 4 sigma.
```

But the droplet temperature is:

```text
T_L ~ 1/L.
```

Therefore:

```text
Delta M / T_L ~ L.
```

For large `L`, a literal shell-removal event is not a typical Hawking quantum.
It is a very hard emission event. Its entropy factor is:

```text
exp[S_{L-1} - S_L] = q^(-(2L - 1)).
```

This becomes exponentially small.

Representative baseline rows:

```text
L   T          <omega>/T small   shell omega/T   M^2 P small      M^2 P shell
 2    1.44270           2.7786          2.7726       7924.0177      1.0240e+03
 6    0.48090           2.1256          8.3178       3481.5700      1.0800e+02
76    0.03797           1.9962        105.3584       3068.5705      1.5747e-37
80    0.03607           1.9961        110.9035       3068.3521      7.1746e-40
```

The small branch settles to:

```text
<omega> ~ 2T
M^2 P ~ constant.
```

The whole-shell branch becomes irrelevant.

## Smooth Matrix-Element Robustness

Two non-flat but smooth matrix-element profiles were tested.

```text
profile       small-quantum slope    mean M^2 P last10
flat                  -2.0058              3068.6102
mild_power            -2.0054              2741.2124
soft_cutoff           -2.0054              2729.9664
```

The coefficient changes, but the scaling does not. This is the expected result:
smooth matrix elements modify greybody factors, not the leading thermodynamic
power law.

## Bath-Dimension Control

A 3D bath was also tested:

```text
bath_dim = 3
small-quantum slope = -3.0093
```

This confirms that the exact Schwarzschild-like acceleration law in this model
depends on the 2D exterior-bath assumption.

For general bath dimension `d` in this convention:

```text
P ~ B_L T_L^(d+1)
  ~ L (1/L)^(d+1)
  ~ L^(-d)
  ~ M^(-d).
```

So:

```text
d = 2 gives P ~ M^-2;
d = 3 gives P ~ M^-3.
```

## Interpretation

The golden-rule test improves F7, but it also changes how we should think about
erosion.

The natural picture is not:

```text
one emitted Hawking quantum removes one full lattice shell.
```

The natural picture is:

```text
the droplet emits many small bath quanta with omega ~ T;
mass drains continuously along the entropy curve;
the integer L sectors are coarse-grained internal registers;
shell erosion is a bookkeeping update after enough mass/area has drained.
```

This is closer to real black-hole evaporation: the black hole does not lose one
Planck-thick horizon shell as a single Hawking quantum.

## What This Fixes

Before:

```text
hard emission weights were imposed by the collision channel.
```

Now:

```text
the leading hard emission weights and accelerating power law follow from
golden-rule state counting, smooth matrix elements, and bath phase space.
```

So F7 should remain `P`, but it is a stronger `P`.

## What Remains Imposed

This calculation still assumes:

```text
smooth matrix elements;
boundary coupling proportional to B_L;
an effectively 2D exterior bath;
the edge-tension entropy/mass relation;
a coarse-grained continuous trajectory through L sectors.
```

The next possible upgrade would be:

```text
construct an explicit finite Hamiltonian with droplet sectors, bath modes, and
boundary coupling whose weak-coupling limit reproduces this golden-rule rate.
```

That is a harder but now better-defined target.

## Current Verdict

This is encouraging.

The golden-rule calculation does not kill the model. It sharpens it:

```text
BH-like acceleration is natural for small-quanta emission from an
area-entropy / boundary-energy droplet into a 2D bath.
```

The price is that literal shell erosion cannot be interpreted as individual
Hawking quanta. It must be a coarse-grained update of the internal register.
