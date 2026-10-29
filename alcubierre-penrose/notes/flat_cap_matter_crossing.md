# Matter crossing a regular planar-cap extension

## Status

This note is a follow-up to the scalar-shift extension alternative in
`paper/main.tex`.  It is not used by the theorem.  The conclusions below have
two different strengths:

1. a compact finite-size **test body** can be launched from the ordinary flat
   bubble core and cross the cap extension; this is an exact geodesic statement
   on the prescribed background;
2. a smooth **self-gravitating null-matter pulse** can cross a specially chosen
   flat cap in an exact local solution of the Einstein equations; this is
   nonlinear but local, and does not yet give a globally coupled compact warp
   bubble with a massive passenger.

The symbolic identities are checked by `sim/flat_cap_matter_crossing.py`.

## 1. A finite test body can come from the bubble core

In the cap cylinder \(\rho<a\) of the compact example, the shift depends only
on \(x\).  Let

\[
  P=p_x,
  \qquad Q=(p_y,p_z),
  \qquad \mu^2=1+|Q|^2.
\]

Start at a finite-time event \((t_0,x_0,y_0,z_0)\) in the flat core, where
\(v=0\), with finite outgoing momentum \(P_0>0\).  The Killing energy is

\[
  E=\sqrt{P_0^2+\mu^2}.
\]

Since \(Q\) and \(E\) are conserved while the trajectory stays in the cap
cylinder, the outgoing branch is

\[
  P(v)=\frac{-Ev+\sqrt{E^2-\mu^2(1-v^2)}}{1-v^2},
\]

and

\[
  \dot x=P+v\dot t
  =\sqrt{E^2-\mu^2(1-v^2)}
  =\sqrt{P_0^2+\mu^2v^2}\ge P_0.
\]

It therefore reaches the front cap \(x=L\) monotonically in finite proper
time, with

\[
  \tau_* - \tau_0\le \frac{L-x_0}{P_0}.
\]

The transverse motion is affine in proper time.  The strict inequality

\[
  \rho_0+|Q|\frac{L-x_0}{P_0}<a
\]

keeps the full trajectory inside the planar cap.  It describes an open set of
initial positions and momenta.  A sufficiently small compact bundle of such
initial data, with closure satisfying the same inequality, is therefore a
finite three-dimensional test body whose world tube remains a positive
distance from the cap rim.

Near the cap, \(1+v=\kappa(L-x)+O((L-x)^2)\), and

\[
  P\sim\dot t\sim\frac{E}{\kappa(L-x)},
  \qquad \dot x\longrightarrow E,
  \qquad L-x\sim C e^{-\kappa t}.
\]

Thus \(t\to+\infty\) while \(\tau\to\tau_*<\infty\), and in the cap
coordinates

\[
  U=e^{-\kappa t}\to0,
  \qquad V=(x-L)/U\to-C<0.
\]

The body reaches the extension from the bubble-interior side.  Its different
points cross \(U=0\) at different proper times and values of \(V\); no notion
of a rigid body simultaneous in the stationary \(t\) coordinate is required.

The central comoving rider has \(P_0=Q=0\) and remains complete.  A rider given
finite outward momentum belongs to the crossing family.

## 2. A cap germ with an exactly flat extension

The extension theorem fixes only the wall value and first normal derivative.
It therefore permits the germ

\[
  v_{\rm flat}(s)=-\sqrt{1+2\kappa s},
  \qquad s=x-x_H,
\]

on a smaller transverse disk.  It satisfies

\[
  v_{\rm flat}(0)=-1,
  \qquad v_{\rm flat}'(0)=-\kappa.
\]

For a scalar shift depending only on \(s\), the scalar curvature of the
\(1+1\) factor is

\[
  R_{(2)}=2(vv''+(v')^2)=(v^2)'',
\]

which vanishes identically for this germ.  The transverse \((y,z)\) factor is
also flat, so the full cap neighborhood is locally Minkowski.  On the inside,
putting \(1-v^2=\kappa^2r^2\) brings the metric to the Rindler form

\[
  ds^2=-\kappa^2r^2dT^2+dr^2+dy^2+dz^2.
\]

Its cap extension is consequently an ordinary Minkowski neighborhood written
in null coordinates \((U,V,y,z)\), with the original side represented by
\(U>0\).  The germ can be embedded in a smooth compact flat-capped wall by a
collar interpolation: it agrees in wall value and nonzero normal derivative
with the compact construction and is prescribed only on a smaller cap disk.

## 3. Exact self-gravitating null matter crossing the cap

On the flat extended neighborhood consider the Brinkmann metric

\[
  ds^2=-2\,dU\,dV+dy^2+dz^2+H(V,y,z)\,dV^2.
\]

This is not a perturbation expansion.  For arbitrary smooth amplitude \(H\),
its determinant is \(-1\), its scalar curvature vanishes, and its only nonzero
Ricci component is

\[
  R_{VV}=-\frac12\Delta_\perp H.
\]

Einstein's equation is solved exactly by aligned null matter

\[
  T_{ab}=\rho(V,y,z)(dV)_a(dV)_b,
  \qquad
  \rho=-\frac{\Delta_\perp H}{16\pi G}.
\]

The null vector \(k=-\partial_U\) is covariantly constant.  The matter rays
have fixed \((V,y,z)\), move from decreasing positive \(U\) through \(U=0\),
and continue into \(U<0\).  Both the metric and the stress tensor are smooth at
the crossing.  This gives an exact nonlinear counterexample to the statement
that every nonzero stress-energy perturbation must destroy a regular cap
transit.

A pulse compact in \(V\) and in transverse matter support is obtained by
choosing a smooth \(\rho(V,y,z)\) and solving the transverse Poisson equation.
At a spacelike time slice its null-matter support is then a finite
three-dimensional packet.  Its gravitational potential is not compactly
supported in the transverse plane, just as an ordinary localized source does
not have a compactly supported gravitational field.

There is also a useful strictly local version.  Choose

\[
  H=A F(V)B(y,z),

\]

with \(F\) and \(B\) smooth bumps supported strictly inside the cap.  Then the
metric perturbation itself vanishes near the cap rim and can be matched to the
unperturbed flat germ there.  Because

\[
  \int_{\mathbb R^2}\rho\,dy\,dz
  =-\frac{1}{16\pi G}\int_{\mathbb R^2}\Delta B\,dy\,dz=0,

this compactly supported version necessarily contains both positive and
negative null energy.  A positive core can be surrounded by a compensating
negative shell.  That is compatible with an already exotic warp source, but
it is not a model of ordinary positive matter alone.

## 4. What this does and does not settle

### Settled

- A small finite test body can start well inside the bubble, not merely in an
  asymptotic layer, and cross the cap extension.
- Backreaction does not kinematically forbid all transit: exact self-gravitating
  null matter can cross a flat cap smoothly.
- The stationary scalar-shift rigidity theorem cannot be applied to this
  dynamical Brinkmann geometry.  Breaking stationarity is not by itself a
  singularity theorem.

### Still open

- a globally specified compact warp bubble, including a dynamical model for
  its exotic supporting matter, through which an ordinary positive-energy
  finite packet crosses;
- a self-gravitating **massive** body rather than null dust;
- stability of the cap under generic compact perturbations evolved from a
  Cauchy slice of the original bubble;
- whether the post-crossing region has a useful global completion or any new
  asymptotic end.

The exact pp-wave calculation is therefore a real nonlinear existence result,
but only for the local transit problem.  The global finite-bubble problem is a
constraint-and-evolution problem for the wall-supporting matter, not a question
that the stationary background theorem can decide.
