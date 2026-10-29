# An explicit globally smooth Natario profile

Verification note, 2026-08-03. This supplies a nonempty, globally smooth
example for the profile class in the Natario global-maximality proof.

## 1. The flat smooth step

Define
\[
w(s)=
\begin{cases}
\exp\!\left[-\dfrac1{s(1-s)}\right],&0<s<1,\\[5pt]
0,&s\notin(0,1),
\end{cases}
\qquad
I=\int_0^1w(u)\,du,
\tag{1.1}
\]
and
\[
\eta(s)=
\begin{cases}
0,&s\leq0,\\[2pt]
I^{-1}\displaystyle\int_0^s w(u)\,du,&0<s<1,\\[7pt]
1,&s\geq1.
\end{cases}
\tag{1.2}
\]
This is a \(C^\infty\) nondecreasing step, flat to all orders at \(s=0,1\).
Symmetry of \(w\) gives
\[
\eta(1-s)=1-\eta(s),\qquad \eta(1/2)=1/2.
\tag{1.3}
\]
On \(0<s<1\),
\[
\eta'(s)=\frac{w(s)}I>0,\qquad
\eta''(s)
=\frac{w(s)}I\,\frac{1-2s}{s^2(1-s)^2}.
\tag{1.4}
\]
Consequently
\[
\eta''(s)\geq0\quad\hbox{for}\quad0<s\leq\frac12,
\tag{1.5}
\]
with strict inequality before \(1/2\).

## 2. The radial profile

Fix a desired axial wall radius \(R_F>0\) and a width
\[
0<W<2R_F.
\]
Put
\[
R_-=R_F-\frac W2>0,\qquad
s(r)=\frac{r-R_-}{W},
\tag{2.1}
\]
choose \(v_s=2\), and set
\[
f(r)=\frac12\eta(s(r)).
\tag{2.2}
\]
Then
\[
f(r)=0\quad(r\leq R_-),\qquad
f(r)=\frac12\quad(r\geq R_-+W).
\tag{2.3}
\]
Because the profile is exactly zero on a ball about the origin, its radial
extension to \(\mathbb R^3\) is \(C^\infty\). Natario's shift is identically
zero there. Because it is exactly \(1/2\) outside the transition annulus, the
shift is exactly the constant vector \(-2e_x\) there. Thus neither the origin
nor the exterior involves a hidden smoothness or tail qualification.

It is also exactly zero-expansion, not merely an axisymmetric vector profile.
In orthonormal spherical components,
\[
X^{\hat r}=-2v_sf\cos\theta,\qquad
X^{\hat\theta}=v_s(2f+rf')\sin\theta.
\]
Directly,
\[
\nabla\cdot X
=-\frac{2v_s\cos\theta}{r}(2f+rf')
 +\frac{2v_s\cos\theta}{r}(2f+rf')=0.
\tag{2.4}
\]

For
\[
a(r)=2v_sf(r)=2\eta(s(r)),\qquad
b(r)=v_srf'(r)=\frac r2a'(r),
\tag{2.5}
\]
one has
\[
a(R_F)=1,\qquad
\kappa=a'(R_F)=\frac{2\eta'(1/2)}W>0.
\tag{2.6}
\]
The front and rear axial roots are therefore simple.

## 3. One regular monotone wall

In polar coordinates about the \(x\)-axis,
\[
S^2:=|X|^2=a^2+D\sin^2\theta,\qquad
D=2ab+b^2.
\tag{3.1}
\]
Throughout the transition \(a\geq0\), \(a'>0\), and \(b>0\). If \(S=1\),
then \(S^2\geq a^2\) implies \(a\leq1\), hence
\[
r\leq R_F,\qquad s(r)\leq\frac12.
\tag{3.2}
\]
On this entire radial range, (1.5) gives \(a''\geq0\), and therefore
\[
b'=\frac12(a'+ra'')>0.
\tag{3.3}
\]
Differentiating (3.1),
\[
\partial_rS^2
=2aa'+2\{a'b+(a+b)b'\}\sin^2\theta>0
\tag{3.4}
\]
at every point of \(S=1\). In particular, the level is regular.

For each fixed \(\theta\), \(S^2=0\) at \(r=R_-\), while at \(r=R_F\)
\[
S^2=1+D(R_F)\sin^2\theta\geq1.
\]
Strict radial monotonicity through this range gives exactly one root. For
\(r>R_F\), \(a>1\) until the exterior value \(a=2\), so \(S^2\geq a^2>1\)
and no second root can occur. The union of the angular roots is one compact
smooth inner \(S=1\) surface.

This proves all profile assumptions used by the global maximality theorem:

1. a globally \(C^\infty\) Natario shift;
2. a flat central region;
3. an exactly constant superluminal exterior;
4. a single compact regular \(S=1\) wall;
5. \(\partial_rS^2>0\) everywhere on that wall;
6. a simple front axial root.

## 4. Concrete normalization

Taking \(R_F=1\) and \(W=1\) makes the transition annulus
\[
\frac12<r<\frac32.
\]
Numerically,
\[
I=0.007029858406609656\ldots,\qquad
\eta'(1/2)=2.605406514520028\ldots,
\]
and hence
\[
\kappa=5.210813029040055\ldots.
\]
These numbers merely set the wall thickness. The proof above is analytic and
holds for every \(R_F>0\) and \(0<W<2R_F\).

## 5. Scope review

This construction is intentionally conservative. It is Natario's standard
zero-expansion ansatz with a compact smooth transition, not the raw logistic
function used for the earlier local numerical jet. It proves that the global
maximality theorem's profile class is nonempty and contains ordinary
finite-thickness bubbles. It does not prove the theorem for every monotone
profile: profiles whose \(S=1\) surface enters a concave part of the transition
may fail (3.4) and require a separate phase-portrait analysis.
