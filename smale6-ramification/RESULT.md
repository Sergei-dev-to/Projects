# A fixed-mass jet test at a positive exceptional five-body degeneracy

## Status

The jet calculation below records the discovery phase.  Its main conclusion
has now been upgraded to a directed-rounding computer-assisted proof,
including a full-planar corank check and a certified transverse mass fold.
See `CERTIFIED_FOLD.md` for the exact theorem and verifier.

## Question

Does the known positive degenerate configuration in the Chen--Hsiao
five-body family continue as a local central-configuration curve when the
masses are frozen?

The answer from the jet computation is **no**: its unique shape-kernel
direction is obstructed at order two.

## Target

Chen and Hsiao use masses

\[
(m_1,m_2,m_3,m_4,m_5)=(1,1,\mu,\mu,\nu)
\]

and the unrotated center-of-mass-zero positions

\[
q_1=(-\alpha,-\gamma_1),\quad q_2=(\alpha,-\gamma_1),
\]
\[
q_3=(-\beta,\gamma_2),\quad q_4=(\beta,\gamma_2),\quad
q_5=(0,-\gamma_1).
\]

Let \(\theta=r_{13}^{-3}\).  Their equations give the explicit
one-parameter mass-and-shape curve

\[
A=\theta^{-2/3},\quad B=(2-\theta)^{-2/3},
\]
\[
\alpha=\sqrt{(A+B-2)/2},\qquad
\beta=(B-A)/(4\alpha),\qquad \gamma=\sqrt{1-\beta^2},
\]
\[
s_{12}=\frac1{8\alpha^3},\qquad s_{34}=\frac1{8\beta^3},
\]
\[
\mu=\frac{(\theta-1)\alpha}{(s_{34}-1)\beta},
\]
\[
\nu=-\frac{(2-2s_{12})(s_{34}-1)+2(\theta-1)^2}
{(1-8s_{12})(s_{34}-1)}.
\]

Writing \(M=2+2\mu+\nu\), set

\[
\gamma_1=\frac{2\mu\gamma}{M},\qquad
\gamma_2=\frac{(2+\nu)\gamma}{M}.
\]

At their scale the multiplier is \(\lambda=M\).  The positive degenerate
point is the root of the gauge-fixed Jacobian determinant.  A sign-changing
bracket is

\[
\det J(1.49343109)\approx-69.4332,qquad
\det J(1.49343110)\approx 36.7178.
\]

Bisection in double precision gives

\[
\theta_*=1.493431096540984,
\]
\[
\mu_*=7.214703144339055,qquad
\nu_*=0.518085751079310.
\]

The other numerical data are

\[
\alpha=0.411720290484599,\quad
\beta=0.490787812488223,
\]
\[
\gamma_1=0.741823069410284,\quad
\gamma_2=0.129456061014074,
\]
\[
\lambda=M=16.9474920397574,\qquad I=5.44220376412791.
\]

These masses lie on two of the Albouy--Kaloshin exceptional relations:
\(m_1=m_2,\ m_3=m_4\), and \(m_1m_3=m_2m_4\).

## Fixed-mass calculation

After eliminating translation and fixing rotation and scale, write the
central-configuration equations as \(F(z;m)=0\).  The base residual is

\[
\lVert F(z_*;m_*)\rVert=9.61\times10^{-15}.
\]

The Jacobian has a one-dimensional numerical kernel.  Its smallest two
computed singular residuals are

\[
2.10\times10^{-13},\qquad 0.2084418804,
\]

so the shape mode is well separated from all other modes.

For a putative fixed-mass arc

\[
z(t)=z_*+t v+t^2z_2+\cdots,
\]

the second coefficient equation is

\[
Jz_2+b_2(v,v)=0.
\]

Projection onto the left kernel is a necessary compatibility condition.  The
bordered solve returns

\[
\lVert\mathcal O_2\rVert=0.177255403655.
\]

This is twelve orders of magnitude above the tangent residual.  Four
independent permutations/reduced gauges give nonzero obstruction norms
\(0.1773,0.2796,0.3543,1.3040\); their numerical values differ because the
equations and null vectors are normalized differently.

For a corank-one analytic system, a nonzero quadratic term in the
Lyapunov--Schmidt reduction makes the zero locally isolated.  Therefore an
interval certification of the displayed separation and obstruction would
prove that this configuration is not on a fixed-mass continuum.

## The previously unexamined direction

Modulo an infinitesimal rotation, the kernel can be represented in the
unrotated symmetric coordinates by

\[
\begin{aligned}
\delta q_1&=( .05858408,-.58571754),&
\delta q_2&=(-.05858408,-.58571754),\\
\delta q_3&=(-.02437623,-.00989390),&
\delta q_4&=( .02437623,-.00989390),\\
\delta q_5&=(0,2.53664213).&&
\end{aligned}
\]

Thus the derivative of the vertical separation between \(q_5\) and the line
through \(q_1,q_2\) is approximately

\[
3.12235966446\ne0.
\]

The null direction immediately leaves the special trapezoid stratum with
three collinear bodies.  This matters because Liu--Zhang's later uniqueness
and nondegeneracy result is internal to that geometrically constrained
stratum.  It does not analyze this transverse full-configuration-space mode.

Moczurad--Zgliczyński make the complementary omission explicit: their
certified enumeration samples avoid bifurcation loci, and at this particular
degenerate point their Newton--Krawczyk pipeline would not establish
finiteness.  The fixed-mass transverse jet is therefore almost exactly the
piece lying between the two existing approaches.

## Controls

The same code gives the expected opposite outcomes on two controls.

1. Roberts' signed five-body continuum has zero base residual and survives
   through order six; every obstruction is between \(5\times10^{-16}\) and
   \(8\times10^{-15}\).  The family is in fact exact to all orders.
2. Palmore's positive centered-triangle degeneracy has a two-dimensional
   kernel and is rejected at order two.  A 72-direction sweep gives
   obstruction norms between \(0.4896\) and \(1.5841\), consistent with the
   exact cubic calculation.

## Novelty assessment

The configuration and its Hessian degeneracy are not new: Chen--Hsiao found
them in 2012.  The mass locus is not new either.  What appears not to have
been reported is:

- the refined root and an explicit genuine shape-kernel vector;
- identification of that kernel as transverse to the three-collinear
  trapezoid stratum;
- the fixed-mass order-two obstruction and resulting local-isolation test.

This is a plausible computationally new observation, not a priority claim.
A literature search found no higher-order or Lyapunov--Schmidt analysis of
this numerical point.

## Sources

- K.-C. Chen and J.-S. Hsiao, *Convex central configurations of the n-body
  problem which are not strictly convex*, J. Dynam. Differential Equations
  24 (2012), 119--128. DOI: 10.1007/s10884-011-9233-2.
- M. Moczurad and P. Zgliczyński, *Central Configurations with Unequal
  Masses: Finiteness in Several Exceptional Cases of Five Bodies*,
  arXiv:2601.01165 (2026), Section 6.1.
- Y. Liu and S. Zhang, *A characterization of a special planar 5-body
  central configuration with a trapezoidal convex hull*, J. Geom. Phys. 213
  (2025), 105494; arXiv:2305.01376.

Moczurad--Zgliczyński's TeX gives \(\nu\approx0.5180855751\), apparently a
digit transposition.  Chen--Hsiao print \(0.518085751\), which agrees with the
independent determinant refinement above.

## Completed proof-sized step

The interval certification is complete.  A 16-variable polynomial
Moore--Spence system has a unique exact root in the certified box; the full
planar quotient Jacobian has corank exactly one; the fixed-mass quadratic
projection and the transverse \(\nu\)-derivative both exclude zero.  The
configuration is therefore locally isolated at its exact masses and is a
nondegenerate fold when \(\nu\) varies with \(\mu\) fixed.

The remaining step is global rather than local: exhaust the entire normalized
configuration space at this exceptional mass, using the certified fold chart
for the singular neighborhood.
