# Certified local structure of the Chen--Hsiao degeneracy

## Result

There are exact positive masses

\[
(m_1,m_2,m_3,m_4,m_5)=(1,1,\mu_*,\mu_*,\nu_*)
\]

with

\[
\mu_*\in[7.2147031443368988,7.2147031443409734],
\]

\[
\nu_*\in[0.5180857510792461,0.5180857510793568],
\]

for which the Chen--Hsiao three-collinear configuration is an isolated
fixed-mass planar central configuration modulo translations, rotations, and
positive scale.  Its seven-variable full-planar shape-plus-multiplier
Jacobian has corank exactly one.

More precisely, holding \(\mu=\mu_*\) and using \(c\) for the signed height
of body 5 above the line through bodies 1 and 2, the local solution set is a
nondegenerate fold:

\[
\nu(c)=\nu_*-\kappa c^2+O(c^3),
\qquad
\kappa\in[1.8106433164582837,1.8106433170382977].
\]

Consequently the singular configuration at \(\nu=\nu_*\) is not the germ of
a fixed-mass continuum.  Locally, the fold opens toward decreasing \(\nu\).
This is a local statement; it does not prove that the entire fiber at these
masses is finite.

## Symmetric polynomial system

Use the scale-fixed symmetric chart

\[
q_1=(-a,0),\quad q_2=(a,0),\quad
q_3=(-b,1),\quad q_4=(b,1),\quad q_5=(0,c).
\]

For \(A_i=\sum_{j\ne i}m_j(q_j-q_i)/r_{ij}^3\), define the four relative
central-configuration equations

\[
G=(A_1-A_5+\lambda(q_1-q_5),
   A_3-A_5+\lambda(q_3-q_5))=0.
\]

Introduce the six distinct positive reciprocal distances

\[
u_{12},u_{13},u_{14},u_{15},u_{34},u_{35}
\]

and impose \(u_{ij}^2r_{ij}^2-1=0\).  Reflection supplies the other four
pair distances.  The singular point is the zero of a 16-variable polynomial
Moore--Spence system consisting of

- the four equations \(G=0\);
- the four kernel equations \(D_{(a,b,c,\lambda)}G\,v=0\);
- the normalizations \(v_c=1\) and \(c=0\);
- the six reciprocal-distance equations.

Here \(D_{(a,b,c,\lambda)}G\) is the derivative of the physical force map
after eliminating the positive reciprocal variables.  The code inserts the
exact chain-rule formula

\[
D(d\,r^{-3})[e]=e\,r^{-3}-3d\,r^{-5}(d\mathbin{\cdot}e),
\]

rather than differentiating while incorrectly holding the lifted
reciprocals fixed.

The variables, in order, are

\[
(a,b,c,\lambda,\mu,\nu,v_a,v_b,v_c,v_\lambda,
u_{12},u_{13},u_{14},u_{15},u_{34},u_{35}).
\]

No radicals, fractional powers, determinants, or singular-value
decompositions occur in the certified system.

## Root certificate

`fold_interval_certificate.js` evaluates a Krawczyk operator using exact
BigInt fixed-decimal intervals with 90 digits after the point.  A floating
point inverse is used only to choose a rational preconditioner; all inclusion
decisions after that conversion are exact integer comparisons.

For the radius-\(10^{-8}\) trial box, it proves

\[
K(X)\subset\operatorname{int}X,
\qquad
\lVert I-RDG(X)\rVert_\infty
<0.000273550632<1.
\]

Thus the augmented polynomial system has a unique zero in \(X\).  The much
tighter Krawczyk image encloses, among the other variables,

\[
a\in[0.4725469440362187,0.4725469440362979],
\]

\[
b\in[0.5632957284873544,0.5632957284873662],
\]

\[
\lambda\in[11.2092711131915881,11.2092711131970592].
\]

All reciprocal distances and both nontrivial masses are certified positive,
so the polynomial lift is locally equivalent to the collision-free Newtonian
equations.

## Corank and Lyapunov--Schmidt coefficients

At the exact root, the augmented equations provide a nonzero right kernel
vector with \(v_c=1\).  A cofactor of the physical \(4\times4\) symmetric
Jacobian satisfies

\[
\det J_{\widehat{2},\widehat{4}}
\in[-2839.0500932713346710,-2839.0500932321192783],
\]

so its rank is exactly three.  Using the resulting unnormalised left
cofactor vector \(w\), directed interval evaluation gives

\[
\frac12w^TD_x^2G[v,v]
\in[2141.8420327015787860,2141.8420333017505017],
\]

and, with \(\mu\) fixed,

\[
w^TG_\nu
\in[1182.9177028666256677,1182.9177029140877845].
\]

Both intervals exclude zero.  The first proves fixed-mass local isolation by
the corank-one Lyapunov--Schmidt reduction; the second proves transversality
in the \(\nu\) direction.  Their ratio is the stated fold coefficient.

`fold_hessian_crosscheck.js` independently recomputes the second directional
derivative by propagating second-order Taylor jets and deriving the reciprocal
distance series from \(u^2r^2=1\).  Every component and the projected
coefficient overlap the closed-form interval calculation.

## Full planar check

The symmetric calculation could in principle miss a symmetry-breaking
kernel.  Use the full local shape slice

\[
\begin{aligned}
q_1&=(-a,0),&q_2&=(a,0),\\
q_3&=(s-b,1+y),&q_4&=(s+b,1-y),\\
q_5&=(x_5,c).
\end{aligned}
\]

The midpoint and line through \(q_1,q_2\) fix translations and rotation;
the average height of \(q_3,q_4\) fixes positive scale.  The relevant
involution is reflection across the vertical axis composed with the label
swaps \((1\,2)(3\,4)\), which is a symmetry because the two mass pairs are
equal.  It splits the Jacobian into the four-dimensional even block above and
a three-dimensional odd block in \((s,y,x_5)\).  Interval evaluation gives

\[
\det J_{\mathrm{odd}}
\in[-4595.0345387961370430,-4595.0345387402991432].
\]

The product with the symmetric rank minor gives the full \(6\times6\)
minor

\[
[13045533.2356154544863171,13045533.2359541771645383],
\]

which excludes zero.  Since the certified even kernel maps to the full
system, the full seven-variable shape-plus-multiplier Jacobian has rank six
and corank one.

`fold_full_planar_certificate.js` repeats the odd-block calculation through
an independently organised pair-force derivative implementation; its entry
intervals overlap those from `full_planar_certificate.js`.

For completeness, let \(E_i=A_i-A_5+\lambda(q_i-q_5)\), \(i=1,\ldots,4\).
The seven symmetry-adapted equations retain all components except
\(O_4=(E_{3y}-E_{4y})/2\).  If those seven equations vanish, set

\[
S=\sum_{i=1}^4m_iE_i,\quad
R=\sum_{i=1}^4m_i(q_i-q_5),\quad
T=\sum_{i=1}^4m_i(q_i-q_5)\mathbin{\times}E_i.
\]

The exact force and torque identities give \(MT=R\times S\).  The seven
equations imply \(S=0\), hence

\[
0=T=-2\mu b\,O_4.
\]

The certified inequalities \(\mu>0\) and \(b>0\) recover the omitted
equation, so this square system is locally equivalent to the complete
central-configuration equations.

## Reproduction and checks

From this directory, run

```powershell
node .\fold_interval_certificate.js
node .\fold_invariants_certificate.js
node .\full_planar_certificate.js
node .\fold_hessian_crosscheck.js
node .\certificate_self_test.js
```

`certificate_self_test.js` exhaustively tests signed floor and ceiling
division on small integers, checks negative interval products and
reciprocals, reruns the Krawczyk contraction, and validates every nonzero
witness.  The full suite also passes independently at 70, 90, and 130 fixed
decimal digits by setting `CERT_INTERVAL_PRECISION` before loading it.

## Scope and next step

This closes the Chen--Hsiao degeneracy as a possible *local* source of an
infinite fixed-mass fiber: it is an ordinary mass fold, not a fixed-mass arc.
It does not close Smale's sixth problem for five bodies, because a different
configuration at the same exceptional masses could still exist and a global
proof must cover the entire normalized collision-free configuration space.

The natural next step is a certified global enumeration at the exact mass
box above, with a dedicated singular chart around this fold and ordinary
interval boxes elsewhere.
