# Corner resolution audit: the pointed rider ends are not smooth conformal points

This is a new obstruction check, not the requested completed unified
diagram. It rules out a *smooth* version of one proposed corner
resolution. It does not prove that a global diagram with singular
corners is impossible. No new unified figure has been drawn, and the
paper has not been edited.

## 1. The tube rendering has no continuous metric limit at its tips

In the exact product-cap interior, the current tube rendering has, on
the axis Y=0,

    g_hat = H(T,X)(-dT^2+dX^2)+dY^2.

For any fixed physical x in (-1,1), t going to plus infinity maps to
the same displayed point P+. With the definitions in band_tube_shape.md,
the longitudinal coefficient has the path limit

    H_limit(x) = C(x)(1+F(x))^2/C0.

For the actual bounded profile, the values include

| Fixed x | H_limit |
| --- | --- |
| 0 | 1.442688714823 |
| 0.5 | 1.834436866366 |
| 0.9 | 0.952448502290 |
| 0.95 | 0.974190493595 |

All those paths approach the same coordinates, but give incompatible
metric limits. Multiplying by another scalar conformal factor alone
cannot repair this in the same endpoint coordinates: the transverse
coefficient is identically 1 on each path and there are no transverse
mixed terms there. A continuous nondegenerate limit forces the scalar
multiplier to have the same finite positive path limit, which leaves
the disagreement in H. A singular change of endpoint coordinates is
not excluded by this path test alone.

This is why the pinched image was explicitly described as a coordinate
closure rather than an established conformal completion.

## 2. An invariant obstruction in the 2+1 cap

The global profile agrees exactly with the quadratic collar on an open
set of the planar cap:

    g3 = g2 + dy^2,
    g2 = -dt^2 + (dx-v0(x)dt)^2,
    v0=-(1+x^2)/2.

Its scalar curvature is R=1+3x^2. With Schouten tensor
S_ab=Ric_ab-R g_ab/4 and Cotton tensor
C_abc=derivative_c S_ab-derivative_b S_ac, direct calculation gives

    C_abc C^abc = (1-v0^2)(R')^2/4
                 = 9x^2(1-v0^2).

In three dimensions the all-lowered Cotton tensor is conformally
invariant. Consequently, under g_hat=Omega^2 g,

    (Cotton squared)_hat = Omega^(-6) (Cotton squared)_physical.

The convention and weight are also independently checked by explicitly
rescaling the metric by exp(2x) and recomputing the tensor.

For a standard reference for Cotton conformal invariance see Garcia,
Hehl, Heinicke and Macias, *The Cotton tensor in Riemannian spacetimes*,
https://arxiv.org/abs/gr-qc/0309008.

Consider the stationary timelike orbit x=0.95,y=0.3, inside the open
product cap and inside the communication tube. Its curvature invariant
is the constant 0.772640121094, and its proper time grows without
bound as t does. The proposed tube closure sends this orbit to P+,
with Omega tending to zero. The unphysical Cotton norm therefore
diverges. No coordinate change or different vanishing conformal gauge
can turn that end into a regular C3 unphysical metric while retaining
this endpoint assignment.

This statement uses C3 regularity because the Cotton tensor contains
third derivatives. It does not by itself exclude a C2 unphysical metric.
It also does not show that the central flat rider orbit, considered in
isolation or with a different boundary assignment, has nonzero Cotton
curvature. The assumption is that these fixed cap orbits coalesce at
the same pointed end, as they do in the proposed pinched tube.

## 3. The four-dimensional lift has a C2 obstruction

Inside the planar aperture, the actual 4D metric is

    g4 = g2 + dy^2 + dz^2.

For this product, Riemann squared=R^2, Ricci squared=R^2/2, and the
4D Weyl invariant is R^2/3. The conformal transformation law is

    (Weyl squared)_hat = Omega^(-4) (Weyl squared)_physical.

On the same x=0.95 orbit, the physical Weyl invariant is the nonzero
constant 4.581852083333. Thus a C2 nondegenerate unphysical metric
cannot have a regular zero-Omega endpoint for that orbit, including
the pinched-point assignment above. Bounded C2 metric components in a
regular chart would give bounded unphysical curvature, in contradiction
with this scalar divergence.

The physical curvature on the orbit stays finite. This is an obstruction
to a regular conformal boundary at infinite time; it is not a physical
finite-time curvature singularity or an obstruction to the regular
finite-time cap crossings already constructed.

## 4. The issue is general for a nontrivial planar profile with a flat core

In the product-cap class R=(v0^2)''. If v0 vanishes on a flat core but
reaches |v0|=1 at a nondegenerate horizon, R cannot be identically zero
throughout the interior. Otherwise v0^2 would be affine, and its flat
core would force it to vanish everywhere there. Some fixed timelike
interior cap orbit therefore has nonzero stationary 4D Weyl curvature.

Also R' cannot vanish identically throughout that interior: it would
make R constant, and the flat core would make it zero, giving the same
contradiction. Some interior orbit has nonzero Cotton norm. Thus the
smooth conformal-end obstruction is not specific to the quadratic
numerical sample. An exactly flat crossing neighborhood does not make
all the other stationary interior orbits asymptotically curvature-free.

## 5. What this establishes, and what it leaves open

- The existing pinched tube does not already supply a continuous
  conformal endpoint metric in its displayed coordinates.
- A smooth conformal completion preserving its pointed-end assignment
  is obstructed invariantly: C3 in the 3D meridional geometry, and C2
  in the physical 4D product cap.
- The regular finite cap faces and ordinary scri remain distinct and
  locally regular, as in the existing matching calculation.
- A unified causal/conformal drawing with explicitly singular ideal
  endpoints or a different boundary structure is not ruled out.

The user's request did not require all ideal endpoints to be smooth.
This audit therefore does **not** settle that request negatively and
must not be presented as a no-go theorem for the requested diagram.
The required global singular-boundary construction and its injective
coordinate realization have not been established. Another placement
of the tube inside a cone would not supply that missing argument.

Reproduction: `exploration/corner_resolution_audit.py`. The symbolic
curvature, conformal-weight convention, incompatible metric limits
and growth checks pass. Raw data:
`output/global_2p1/corner_resolution_audit.json`.
