# Track B: Area-Register Evaporator

## Purpose

Track A showed that shrinking sectors can produce accelerating emission in a
natural variable-N Bose-Hubbard model. Its weakness is entropy scaling.

Track B starts from the opposite end:

```text
build the correct black-hole entropy/temperature scaling into the register
structure, then ask how much dynamics can be made nontrivial.
```

This is not meant to be a microscopic theory of gravity. It is an
entropy-correct quantum evaporator.

## Minimal model

Let `n` be an area-register size.

```text
H_n = (C^q)^{tensor n}
dim H_n = q^n
S_n = log dim H_n = n log q
```

Identify area with `n`:

```text
A_n proportional to n
```

Choose a Schwarzschild-like mass-area relation:

```text
M_n = alpha sqrt(n)
```

Then:

```text
S_n proportional to M_n^2
T_n = dM/dS proportional to 1/M_n
C = dM/dT < 0
```

Discrete temperature estimate:

```text
beta_n = (S_n - S_{n-1}) / (M_n - M_{n-1})
T_n = 1 / beta_n
```

Since:

```text
S_n - S_{n-1} = log q
M_n - M_{n-1} ~ alpha / (2 sqrt(n))
```

we get:

```text
T_n ~ alpha / (2 log q sqrt(n)) ~ 1/M_n
```

## Emission

Evaporation steps:

```text
n -> n - 1
```

with emitted energy:

```text
omega_n = M_n - M_{n-1}
```

Radiation labels can be:

```text
0 = no emission
1..r = emitted channel labels
```

The important design question is the transition operator:

```text
X_n : H_n -> H_{n-1}
```

Possible choices:

```text
1. random isometry/projection-like maps
2. local qudit removal maps
3. scrambled local removal maps
4. anyonic fusion-space reduction maps, later
```

## What must not be hidden

If we choose arbitrary random maps and tune emission probabilities, Track B
collapses back into the engineered shell model.

So the first test should separate:

```text
entropy law
transition matrix elements
emission passband
```

The result should report which ingredient is doing the work.

## First calculation

Use small finite registers:

```text
q = 2
n_max = 12 or 14
n_min = 2
dim H_12 = 4096
```

Avoid storing the full direct-sum density matrix if possible. Use sector blocks
as in the variable-N Kraus code.

Initial state:

```text
pure state in H_nmax
```

Kraus channel:

```text
K_0^(n) = sqrt(1 - p_n) I_n
K_a^(n) = sqrt(p_n / r) X_{n,a}
```

where:

```text
X_{n,a}: H_n -> H_{n-1}
```

The nontrivial part is choosing `p_n`.

Candidate schedules:

### Schedule A: temperature-derived rate

Use a Stefan-like finite-dimensional analogue:

```text
p_n proportional to T_n^gamma
```

For 4D Schwarzschild:

```text
power ~ 1/M^2 ~ 1/n
```

But each quantum has:

```text
omega_n ~ 1/sqrt(n)
```

So the number emission rate should scale roughly:

```text
Gamma_n ~ power / omega_n ~ 1/sqrt(n)
```

Thus:

```text
p_n ~ 1/sqrt(n)
```

Since `n` decreases during evaporation, `p_n` increases.

### Schedule B: matrix-element-derived rate

Do not set `p_n` by hand. Use random maps normalized so that typical transition
strength depends on final-state dimension:

```text
Gamma_n ~ dim H_{n-1} / dim H_n = 1/q
```

This alone does not accelerate; it tests whether entropy scaling by itself is
enough. It probably is not.

### Schedule C: passband plus density of states

Use emitted energy windows and count accessible final states. Since each sector
has only one mass level in the minimal model, this requires adding intra-sector
band structure:

```text
H_n = area register tensor internal band
```

This is more realistic but no longer minimal.

## Expected lesson

Track B will probably show:

```text
S ~ area and T ~ 1/M are easy with an area register.
Accelerating evaporation still requires a rate law or emission matrix element
structure.
```

That is not a failure. It clarifies the decomposition:

```text
black-hole phenomenology = entropy law + shrinking Hilbert space + emission
coupling.
```

## First implementation target

Create:

```text
sim/area_register_evaporator.py
```

Minimum outputs:

```text
1. M_n, S_n, T_n, heat capacity sign.
2. E(t), n(t), emitted power.
3. effective dimension and S2(core).
4. comparison between p_n ~ 1/sqrt(n) and constant p_n.
```

Success criterion:

```text
The temperature-derived schedule should reproduce accelerating emission and
entropy growth. The constant-rate control should not be sold as BH-like even if
the entropy law is correct.
```

If this works, the next refinement is:

```text
replace qudits with anyonic fusion spaces, where dim H_n ~ d^n arises from
2D horizon-like fusion constraints rather than independent qubits.
```

## Kill-test update

The first Track B rate diagnostic has been run.

See:

```text
notes/track_b_area_register_results.md
```

Script and figure:

```text
sim/area_register_rate_scan.py
track_b_area_register_rate_scan.pdf
```

Main result:

```text
sqrt mass law, M_n ~ sqrt(n):
  modest robust acceleration from matrix-element-derived rates

linear mass-law control:
  deceleration, once the emitted-energy passband is opened
```

Best grouped cases:

```text
local removal, sqrt mass, gap >= 4:
  min acceleration over seeds = 1.125

scrambled removal, sqrt mass, gap >= 4:
  min acceleration over seeds = 1.124
```

This means Track B did not collapse into a tautology. The entropy-correct
area register plus BH-like mass relation can produce acceleration from actual
shrinkage matrix elements, although the effect is modest and passband
dependent.

## Kraus update

The successful square-root mass case has also been upgraded to a secular Kraus
channel.

See:

```text
notes/track_b_area_register_results.md
track_b_area_register_kraus.pdf
```

Result:

```text
local and scrambled removal both give mid / early emitted power about 1.124
across seeds 2468 and 2469.
```

The same runs show:

```text
energy decreases
area entropy decreases
effective dimension decreases
S2(core) grows to about 5.34
```

So Track B now has a reduced-density quantum-channel version, not only a
population rate diagnostic.
