# Eternal 1+1 Alcubierre Calculation

This folder contains a first-principles numerical calculation for the stationary
1+1 axial warp-drive geometry.

Metric convention:

```text
ds^2 = -dt^2 + [dr - v(r) dt]^2
v(r) = v_s [f(r) - 1]
```

with the Alcubierre wall profile

```text
f(r) = [tanh(sigma(r + R)) - tanh(sigma(r - R))] / [2 tanh(sigma R)].
```

The rider at the bubble center is

```text
r = 0
```

and since `v(0) = 0`,

```text
ds^2|r=0 = -dt^2.
```

So the rider is timelike and has proper time `tau = t`.

## Null Families

Setting `ds^2 = 0` gives

```text
dr/dt = v(r) +/- 1.
```

For `v_s > 1`, the horizons in the stationary patch occur where

```text
v(r) + 1 = 0
```

or equivalently

```text
f(r_h) = 1 - 1/v_s.
```

For the default parameters `v_s = 2`, `R = 1`, `sigma = 6`, the two roots are
very close to `r = -1` and `r = +1`.

## Null Coordinates

The script computes

```text
F_+(r) = integral dr / [v(r) + 1]
F_-(r) = integral dr / [v(r) - 1]
u = t - F_+(r)
w = t - F_-(r)
```

then compactifies with

```text
U = arctan(u)
W = arctan(w)
T = (U + W) / 2
X = (W - U) / 2
```

The `F_+` integral diverges logarithmically at both horizon roots, which is why
those horizons become null boundaries of the stationary conformal patch.

## Running

```text
python eternal_1p1.py
```

Expected outputs are written to `output/`:

```text
summary.txt
null_slopes.png
central_conformal_patch.png
extended_paper_patch.png
trip_overlay.png
proper_trip_overlay.png
```

`central_conformal_patch.png` is only the middle region containing the rider.

`extended_paper_patch.png` uses the three-region construction described by
Finazzi, Liberati, and Barcelo for the eternal warp-drive diagram:

```text
I:   r < r1
II:  r1 < r < r2
III: r > r2
```

Each region has its own `u_i` chart because `u` diverges logarithmically at the
horizons. The regularized coordinate is then taken piecewise as

```text
U_I   =  1/2 + exp(-kappa u_I)
U_II  =  1/2 tanh(kappa u_II / 2)
U_III = -1/2 - exp(kappa u_III)
```

and the global left-going coordinate is compactified as

```text
mathcal W = arctan(w).
```

The final plotted coordinates are

```text
mathcal U = arctan(U)
T = (mathcal W + mathcal U) / 2
X = (mathcal W - mathcal U) / 2
```

The result is the same kind of non-maximal, three-region conformal patch as the
eternal warp-drive figure in the literature, with the additional `r = 0` rider
worldline drawn explicitly.

The grey boundary skeleton in `extended_paper_patch.png` is drawn directly from
the compactified null-coordinate limits:

```text
mathcal W = +/- pi/2
mathcal U = +/- pi/2
```

It labels the left, central, and right null infinities:

```text
mathscr I_L^+/-, mathscr I_C^+/-, mathscr I_R^+/-
```

as well as the timelike and spatial infinities:

```text
i^+, i^-, i_L^0, i_R^0
```

## Trip Overlays

`trip_overlay.png` is an exploratory overlay of asymptotic lab-frame curves
transformed by

```text
r = x - v_s t.
```

`proper_trip_overlay.png` adds the missing causal-character check. For a lab
curve `x(t)` in the original metric,

```text
ds^2/dt^2 = -1 + [dx/dt - v_s f(x - v_s t)]^2.
```

For a static asymptotic star, `dx/dt = 0`, so

```text
ds^2/dt^2 = -1 + v_s^2 f(r)^2.
```

In the superluminal case this becomes positive when the bubble core passes over
the star. Therefore a static `x=const` star worldline is timelike only in the
asymptotic exterior portions and spacelike through the bubble. The eternal
stationary diagram can show coordinate crossing events, but it cannot honestly
represent a full trip from one intact static star to another without changing to
a dynamical spacetime in which the bubble is created and destroyed.

## 2+1 Conformal-Background Trip Diagram

`conformal_2p1_trip.py` creates a separate 2+1 compactified Minkowski-background
diagram:

```text
u = t - rho
v = t + rho
U = arctan(u)
V = arctan(v)
T = U + V
chi = V - U
X = chi cos(phi)
Y = chi sin(phi)
```

This gives the double-cone conformal boundary of 2+1 Minkowski space, where the
spatial-infinity cross-section is an `S^1` circle. The script overlays a
finite-radius bubble world tube, an internal bubble rider, two static stars kept
off the bubble axis, and an ordinary subluminal rider.

This is deliberately not claimed to be the exact 2+1 Alcubierre conformal
compactification. It is a background comparison diagram showing how the trip
comparison can be represented without forcing the stars through the 1+1 bubble
core.

Outputs:

```text
conformal_2p1_trip.png
conformal_2p1_trip_side.png
conformal_2p1_trip_top.png
conformal_2p1_trip_summary.txt
```

## 3+1 Front-Tip PP Curvature

The 1+1 endpoint extension does not automatically lift to the real 3+1
Alcubierre metric. The local 3+1 calculation is summarized in:

```text
notes/front_tip_pp_curvature_singularity.md
```

For

```text
ds^2 = -dt^2 + [dx - v(r) dt]^2 + dy^2 + dz^2,
r = sqrt(x^2 + y^2 + z^2),
v(R) = -1,
v_r(R) = -kappa,
```

the front axis generator has

```text
R(K, e_y, K, e_y)
  = -1 / [kappa R (lambda_* - lambda)^2]
```

in a parallel-propagated transverse frame. Thus the isolated front endpoint is
a null parallel-propagated curvature singularity in 3+1, not a smooth Cauchy
horizon like the 1+1 reduced model.

Supporting scripts and outputs:

```text
front_tip_parallel_tidal_analytic.py
front_tip_full_parallel_frame.py
front_tip_general_convex_wall.py
front_planar_cap_extension.py
front_tip_einstein_parallel_frame.py
front_tip_scalar_invariants.py
front_tip_tipler_krolak.py
front_tip_singularity_strength.py
front_tip_taylor_metric_check.py
front_tip_numerical_frame_check.py
front_tip_adm_derivation.py
output/sech/front_tip_parallel_tidal_analytic.txt
output/sech/front_tip_full_parallel_frame.txt
output/sech/front_tip_general_convex_wall.txt
output/sech/front_planar_cap_extension.txt
output/sech/front_tip_einstein_parallel_frame.txt
output/sech/front_tip_scalar_invariants.txt
output/sech/front_tip_tipler_krolak.txt
output/sech/front_tip_singularity_strength.txt
output/sech/front_tip_taylor_metric_check.txt
output/sech/front_tip_numerical_frame_check.txt
output/sech/front_tip_adm_derivation.txt
```
