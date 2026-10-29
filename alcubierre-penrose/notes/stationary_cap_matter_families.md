# Matter families at a regular planar warp cap

## Status and question

This is a follow-up investigation, not an ingredient of the extension theorem
in `paper/main.tex`.  It asks two distinct questions:

1. Which stationary stress tensors can support the exact planar
   constant-inaffinity cap while preserving its Killing horizon?
2. Which self-gravitating matter pulses can cross the same location smoothly
   after the horizon is allowed to become dynamical?

The symbolic identities are audited by
`sim/stationary_cap_matter_families.py`.

## 1. General planar scalar-shift source

Consider

\[
 ds^2=-dt^2+[ds-v(s)dt]^2+dy^2+dz^2.
\]

Put \(A=1-v^2\).  Away from a zero of \(A\), a change of time coordinate
gives the static form

\[
 ds^2=-A(s)dT^2+A(s)^{-1}ds^2+dy^2+dz^2.
\]

The geometry is the direct product of a two-dimensional Lorentzian metric and
the Euclidean transverse plane.  Direct calculation gives

\[
 R=(v^2)''=-A'',
\]

and

\[
 G_{tt}=G_{ts}=G_{ss}=0,
 \qquad
 G_{yy}=G_{zz}=-\frac12(v^2)''=\frac12A''.
\]

Consequently every smooth choice of \(A\) with

\[
 A(0)=0,
 \qquad A'(0)=-2\kappa\ne0
\]

has the same nondegenerate planar Killing horizon at \(s=0\).  The function
\(A''\), and hence the stationary transverse pressure, remains free.

For the more general cap germ used in the paper,

\[
 v=-1-\kappa s+s^2d(s,y,z),
\]

the wall stress in an orthonormal frame is

\[
 8\pi G\,T_{\hat a\hat b}\big|_{s=0}
 =\operatorname{diag}(0,0,2d(0,y,z)-\kappa^2,
                         2d(0,y,z)-\kappa^2).
\]

Thus the extension criterion does not select vacuum.  It leaves an
infinite-dimensional family of finite stationary sources, including pressure
varying across the cap.  What it excludes at the horizon is energy density,
longitudinal pressure, and flux within this unit-lapse, flat-slice ansatz.

## 2. Energy conditions

Write the effective cap stress as

\[
 T_{\hat a\hat b}=\operatorname{diag}(0,0,p_\perp,p_\perp).
\]

Then:

- NEC, WEC, and SEC hold exactly when \(p_\perp\ge0\);
- DEC holds only when \(p_\perp=0\).

The last statement follows because an observer can see a nonzero transverse
momentum flux while the rest-frame energy density is zero.  Therefore every
nonvacuum stationary cap in the scalar-shift ansatz violates the dominant
energy condition, even when it obeys the null and weak conditions.

This also follows directly from horizon mechanics.  A Killing horizon has
zero expansion and shear.  Raychaudhuri and Einstein's equation give

\[
 T_{ab}\chi^a\chi^b=0
\]

on the horizon.  Under the dominant energy condition, the remaining horizon
flux vector is forced to align with the null generator.  Ordinary positive
matter cannot continually cross the horizon while the geometry remains
exactly Killing.

## 3. Constant-curvature family

Take

\[
 v(s)=-\sqrt{1+2\kappa s-\alpha s^2},
 \qquad
 A(s)=-2\kappa s+\alpha s^2.
\]

It retains

\[
 v(0)=-1,
 \qquad v'(0)=-\kappa,
\]

while

\[
 R=-2\alpha,
 \qquad
 G_{\hat a\hat b}=\operatorname{diag}(0,0,\alpha,\alpha).
\]

For \(\alpha=0\), this is the locally Minkowski Rindler cap.  For
\(\alpha>0\), it is locally \(\mathrm{AdS}_2\times\mathbb R^2\), an instance
of the Pleba\'nski--Hacyan direct-product geometry.  The cap is still a regular
nondegenerate Killing horizon, but an infalling body generally experiences
finite nonzero tidal curvature.

The vacuum Rindler germ is not merely one arbitrary profile: within the
strictly planar scalar-shift family it is the unique local vacuum solution.
Indeed, vacuum requires

\[
 (v^2)''=0,
\]

so \(v^2\) is affine and the two-dimensional factor is flat.

## 4. Conventional field realizations

### 4.1 Uniform electromagnetic field and negative cosmological constant

Let an electric or magnetic field be normal to the cap.  In an orthonormal
frame its Maxwell stress has the form

\[
 8\pi G\,T^{\rm EM}_{\hat a\hat b}
 =q\,\operatorname{diag}(1,-1,1,1).
\]

The constant-curvature cap solves

\[
 G_{ab}+\Lambda g_{ab}=8\pi G T^{\rm EM}_{ab}
\]

when

\[
 q=\frac{\alpha}{2},
 \qquad
 \Lambda=-\frac{\alpha}{2}.
\]

The positive electromagnetic energy density is cancelled in the total
effective source by the negative cosmological energy.  The longitudinal
pressures cancel as well, while the transverse pressures add.  The Maxwell
field by itself satisfies DEC; the combined effective source does not.

### 4.2 Two transverse axion fields

Two canonical shift-symmetric scalars

\[
 \phi_1=c y,
 \qquad
 \phi_2=c z
\]

have constant combined stress

\[
 8\pi G\,T^{\rm ax}_{\hat a\hat b}
 =\alpha\,\operatorname{diag}(1,-1,0,0)
\]

when \(8\pi Gc^2=\alpha\).  Together with

\[
 \Lambda=-\alpha,
\]

they support the same \(\mathrm{AdS}_2\times\mathbb R^2\) cap.  This is the
standard homogeneous linear-axion mechanism used to support planar
direct-product geometries.

### 4.3 Simple no-go results

An isotropic perfect fluid, even with an independently chosen cosmological
constant, cannot support \(\alpha\ne0\) in this ansatz: its longitudinal and
transverse pressures are equal, whereas the required source has
\(p_s=0\) and \(p_y=p_z\ne0\).

A canonical scalar depending only on the normal coordinate \(s\) also fails.
The simultaneous conditions \(T_{\hat0\hat0}=T_{\hat1\hat1}=0\) force its
kinetic term to vanish, after which the transverse equations force
\(\alpha=0\).

These are no-go statements only within the stationary planar scalar-shift
ansatz.  More general lapse, spatial metric, rotation, or nonminimal couplings
enlarge the possibilities.

## 5. Finite cap and localization

The exact electromagnetic or axion solution is homogeneous over the transverse
plane.  To place it inside the compact cap of the paper, choose a smaller disk
on which the fields and constant-curvature germ are exact, followed by a smooth
transition annulus.  The wall conditions

\[
 v(0,y,z)=-1,
 \qquad v_s(0,y,z)=-\kappa
\]

can remain exact throughout that annulus, so the Killing cap survives.  The
transition stress is then whatever the Einstein tensor requires; realizing the
whole compact bubble with only the simple Maxwell/axion Lagrangian is not
shown.  Currents, domain walls, or the already exotic warp source are needed to
confine the homogeneous fields.

Thus the conventional matter models establish a genuine local realization,
not a globally self-contained compact warp-drive source.

## 6. Exact matter crossing a curved cap

Matter that actually crosses should not be expected to preserve an exact
Killing horizon.  The distinction can be demonstrated nonperturbatively.
Write the constant-curvature cap in ingoing coordinates and add a Kundt pulse:

\[
 ds^2=-2\,du\,dr+
 \left[H(u,y,z)-A(r)\right]du^2+dy^2+dz^2,
 \qquad
 A=-2\kappa r+\alpha r^2.
\]

For arbitrary smooth \(H\), direct calculation gives exactly

\[
 R=-2\alpha,
 \qquad
 G_{uu}=-\frac12\Delta_\perp H,
 \qquad
 G_{yy}=G_{zz}=\alpha,
\]

with all other new Einstein components zero.  Keeping the uniform Maxwell
field and \(\Lambda=-\alpha/2\), the additional source is aligned null matter

\[
 T^{\rm rad}_{ab}=\rho(u,y,z)(du)_a(du)_b,
 \qquad
 \rho=-\frac{\Delta_\perp H}{16\pi G}.
\]

This is an exact Einstein--Maxwell--Lambda--null-dust solution, not a
linearized perturbation.  Its rays are tangent to \(-\partial_r\), are affinely
parametrized, and cross \(r=0\) smoothly.

When \(H\ne0\), however,

\[
 g^{ab}(dr)_a(dr)_b\big|_{r=0}=-H.
\]

The old surface \(r=0\) is no longer null.  The pulse therefore deforms the
Killing horizon rather than preserving it.  If \(H\) is a sandwich profile
compact in \(u\), the geometry is the same stationary
\(\mathrm{AdS}_2\times\mathbb R^2\) cap before and after the pulse, while the
intermediate transit is dynamical and regular.

A positive null-density pulse can have compact matter support in \((y,z)\),
but solving the two-dimensional Poisson equation gives its gravitational field
a logarithmic transverse tail.  If \(H\) itself is required to be a compact
transverse bump, then

\[
 \int\rho\,dy\,dz=0,
\]

so the source must contain compensating negative null energy.

## 7. Massive matter and local evolution

Einstein--Vlasov is a convenient model for a small but finite cloud of massive
collisionless matter: its distribution function can have compact support in
both position and timelike momentum, and the coupled system has a standard
local existence and uniqueness theorem for smooth constraint-satisfying
initial data.  See Rendall's introduction to the Einstein--Vlasov system
([arXiv:gr-qc/9604001](https://arxiv.org/abs/gr-qc/9604001)) and his review of
Einstein evolution theorems
([arXiv:gr-qc/0001008](https://arxiv.org/abs/gr-qc/0001008)).

This nearly settles the local massive-transit question, but not quite.  If one
has a constraint-satisfying initial data set sufficiently close to the regular
cap background and containing a small Vlasov packet whose timelike momenta
point through the cap, local existence and continuous dependence give a smooth
development for a common finite interval.  By starting the packet sufficiently
close to the cap, its crossing occurs within that interval.  Transit is then an
open property of the data rather than an exactly tuned worldline.

The premise is the unresolved part: the local evolution theorem assumes the
Einstein constraint equations have already been solved.  It does not construct
a global slice that simultaneously contains

- the compact flat-capped warp wall and its supporting exotic fields;
- the electromagnetic or axion cap core;
- a compact Vlasov packet representing the massive traveler.

Constraint deformation or gluing methods are the natural tool, but their
nondegeneracy hypotheses have not been checked for this background and the
wall-supporting matter has not been given a dynamical Lagrangian.  Therefore
the correct present statement is conditional:

> Smooth massive transit follows from standard local Einstein--Vlasov
> evolution once suitable coupled constraint data are supplied.

This locates the remaining difficulty in the initial constraints and the
choice of exotic wall matter, not at the horizon crossing itself.

## 8. Conclusions and next boundary

The exploration establishes:

1. The stationary extendible branch contains an infinite-dimensional family
   of finite nonvacuum sources, not only vacuum Rindler space.
2. A particularly simple curved member has exact electromagnetic-plus-negative-
   cosmological-constant and axion-plus-negative-cosmological-constant
   realizations.
3. Nonvacuum stationary caps in the scalar-shift ansatz necessarily fail DEC.
4. Exact positive null matter can cross the curved cap smoothly when the
   horizon is allowed to become dynamical.
5. Standard Einstein--Vlasov evolution makes small massive transit locally
   robust conditional on constructing the coupled constraint data.

The remaining physically sharper problem is no longer local existence.  It is
to construct Cauchy data for a compact wall and a finite massive body, evolve a
specified exotic-matter model, and determine whether a regular dynamical
horizon persists long enough for the body's entire world tube to pass.

## References used for classification

- R\'acz and Wald, regular extensions of constant-nonzero-surface-gravity
  Killing horizons: [DOI 10.1088/0264-9381/9/12/008](https://doi.org/10.1088/0264-9381/9/12/008).
- Ashtekar, Corichi, and Krasnov, isolated horizons and the absence of matter
  or gravitational flux:
  [arXiv:gr-qc/9905089](https://arxiv.org/abs/gr-qc/9905089).
- Amsel, Marolf, and Virmani, matter flux through a bifurcate Killing horizon:
  [arXiv:0708.2738](https://arxiv.org/abs/0708.2738).
- Podolsk\'y and Ortaggio, exact Kundt waves on Pleba\'nski--Hacyan and related
  direct-product backgrounds:
  [arXiv:gr-qc/0212073](https://arxiv.org/abs/gr-qc/0212073).
- Krtou\v{s}, Podolsk\'y, Zelnikov, and Kadlecov\'a, exact radiation and
  gyratons on direct-product Einstein--Maxwell backgrounds:
  [arXiv:1201.2813](https://arxiv.org/abs/1201.2813).
