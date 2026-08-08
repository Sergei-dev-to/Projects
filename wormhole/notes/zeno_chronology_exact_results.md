# Zeno chronology transits: exact results after the first stress test

## Executive result

The Zeno direction survives, but in a more precise form than the original
"infinitely many loops in finite time" picture.

There is a clean invariant phenomenon to study:

> an extendible timelike observer crosses infinitely many **distinct chronology
> classes** in finite proper time, reaches a regular chronological future, and
> carries a finite detector state through the accumulation.

We can now do substantially more than state this as a possibility.

1. There is a symmetry-free theorem: whenever distinct chronology classes are
   not locally finite at an event, that event lies on a lightlike line contained
   in the chronology boundary.  Under null convergence and null genericity, the
   spacetime is null geodesically incomplete.  This needs no compactness,
   asymptotic condition, field equation, Killing field, or traveler assumption.
   With Einstein's equation and null convergence, strictly positive null energy
   in a warm material worldtube at the exit is already enough to force the same
   incompleteness conclusion.
2. A completely explicit smooth cylinder metric realizes the causal pattern.
   The observer and its parallel-propagated frame pass regularly through the
   accumulation event, with bounded curvature.
3. The cylinder can be localized in a spatially compact toroidal region of a
   \(3+1\)-dimensional spacetime that is exactly Minkowski near infinity.  The
   result has no black-hole event horizon, and an open timelike traveler can
   enter from the exterior, cross all of the chronology classes, and leave.
4. The construction is necessarily nonanalytic.  More generally, an analytic
   torus action has only locally finitely many components in its
   symmetry-generated CTC set.
5. In the direct-product core, the null energy condition forbids even one
   bounded circular-CTC band.  The localized model therefore has unavoidable
   NEC violation in its core, not merely in a matching shell.
6. Making every chronology boundary degenerate, with zero surface gravity,
   removes exponential Hawking--Misner monodromy of the closed generator.  It
   does **not** make the spacetime null complete.  The companion null family
   reaches each boundary in finite affine time while winding infinitely around
   the circle.  This is a quasiregular/Misner-type incompleteness with bounded
   curvature.
7. For that winding family, gain and affine compression are reciprocal even at
   a degenerate or flat zero.  A frequency-linear response is not suppressed by
   the shrinking circuit time.  By contrast, the other null family and the
   timelike traveler cross the whole Zeno stack regularly.
8. The scalar wave equation gives an exact chiral filter: smooth passage kills
   the recurrent chirality but leaves an arbitrary regular signal.  Generic
   sources violate a countable set of compatibility moments, while explicitly
   tuned nonzero emitters satisfy them.  Whether transverse compactness upgrades
   this generic restriction to a necessity theorem is a precise scattering
   problem, not an assumption.

This gives a useful separation:

- **regular operational channel:** a timelike visitor, and one null family,
  cross infinitely many distinct chronology classes and escape;
- **singular recurrent channel:** the other null family is trapped at any one
  boundary and winds infinitely at finite affine length;
- **physical cost:** the exact effective stress tensor violates NEC, and a
  generic warm source can excite the recurrent channel.

The bare two-dimensional winding lemma is not new.  Sánchez, Bavard--Mounoud,
Mehidi, Petersen, and most recently Rieger already contain its mathematical
ingredients.  The strongest candidate contribution is now the symmetry-free
non-local-finiteness theorem, together with the causal-class construction, its
\(3+1\) asymptotically flat localization, and the exact operational
classification of the two propagation channels.  A specified matter model or
a finite-body scattering theorem would push the package substantially further.

The symbolic calculations used below are independently reproducible in
[zeno_banded_metric_symbolics.py](zeno_banded_metric_symbolics.py) and
[zeno_scalar_filter_symbolics.py](zeno_scalar_filter_symbolics.py).

---

## 1. The invariant Zeno notion

The chronology-violating set is

\[
\mathcal C=\{p\in M:p\ll p\}.
\]

Its Carter chronology classes are the equivalence classes

\[
[p]=I^+(p)\cap I^-(p),\qquad p\in\mathcal C.
\]

This is a better invariant than "sheet," "copy," or "winding."  A covering
description may change the number of sheets, while distinct chronology classes
are features of the spacetime itself.

### Definition: regular Zeno chronology transit

Let

\[
\gamma:(\tau_0,\tau_*+\delta)\longrightarrow M
\]

be a future-directed timelike curve.  It is a **regular Zeno chronology
transit** if there are pairwise distinct chronology classes
\(\mathcal C_n\) and parameters \(\tau_n\nearrow\tau_*<\infty\) such that
\(\gamma(\tau_n)\in\mathcal C_n\), while \(\gamma\) and the spacetime metric
extend with the stated regularity through \(\tau_*\).

One can strengthen "regular" by requiring bounded parallel-propagated
curvature, an extendible finite-radius worldtube, or a convergent internal
detector state.  These are separate conditions and should not be hidden inside
the definition.

### Interval lemma

If a future timelike curve meets one chronology class at parameters
\(s_1<s_3\), then it meets that class at every \(s_2\in(s_1,s_3)\).

Indeed,

\[
\gamma(s_1)\ll\gamma(s_2)\ll\gamma(s_3),
\]

and membership of \(\gamma(s_1)\) and \(\gamma(s_3)\) in the same chronology
class also gives \(\gamma(s_3)\ll\gamma(s_1)\).  Concatenation puts
\(\gamma(s_2)\) in the same class.  Thus the preimage of any class along a
timelike observer is an interval.  A genuine Zeno transit is not repeated
departure from and re-entry into one class; it requires infinitely many
classes.

This also separates the problem from a Malament--Hogarth supertask.  There the
finite-time observer receives the result of a different worldline with infinite
proper duration.  Here one extendible observer crosses infinitely many causal
regions.

### Non-local-finiteness theorem

The limiting event has a much stronger model-independent causal status than a
mere boundary point.

**Theorem.**  Let \((M,g)\) be a \(C^2\), time-oriented spacetime.  Suppose
\(p_n\to p\), where \(p_n\) belongs to a chronology class \(\mathcal C_n\) and
the \(\mathcal C_n\) are pairwise distinct.  Then there is a lightlike line
\(\eta\) through \(p\) such that

\[
p\in\eta\subset\partial\mathcal C.
\tag{1.1}
\]

Every point of \(\eta\) is approached by a sequence of points, the \(n\)-th
point lying in \(\mathcal C_n\), and strong causality fails everywhere on
\(\eta\).  No compactness, energy condition, symmetry, field equation, or
asymptotic assumption is required.

Here **lightlike line** means a two-sided inextendible achronal causal curve,
hence an inextendible null geodesic.  Affine completeness is not part of the
definition.

**Proof.**  Choose a complete auxiliary Riemannian metric \(h\).  Through each
\(p_n\), choose a smooth closed future timelike curve \(\sigma_n\), parametrized
by \(h\)-arclength, with length \(\ell_n\).  Its image lies in
\(\mathcal C_n\).  The loops cannot collapse to \(p\): take a relatively
compact coordinate neighborhood \(U\) carrying a local temporal coordinate and
a smaller neighborhood \(V\Subset U\) containing all late \(p_n\).  No closed
causal curve can remain inside \(U\), so each \(\sigma_n\) must cross
\(U\setminus V\); consequently the \(\ell_n\) have a positive lower bound.

Apply Minguzzi's coalescing-endpoint limit-curve theorem (Theorem 3.1(2) of the
2008 paper cited below).  If a subsequence of
\(\ell_n\) is bounded, it converges to a nonconstant closed causal curve through
\(p\).  If \(\ell_n\to\infty\), the limit consists of past- and
future-inextendible causal halves joined at \(p\).  In either case, call the
limit \(\eta\), periodically extending the closed limit when necessary.

It remains to prove achronality.  If \(a,b\in\eta\) satisfied \(a\ll b\), take
simultaneous approximants \(a_n,b_n\in\mathcal C_n\) and
\(a_m,b_m\in\mathcal C_m\) for two sufficiently large distinct indices.
Openness of \(I^+\), together with mutual timelike relatedness inside each
class, gives

\[
a_n\ll b_m\ll a_m\ll b_n\ll a_n.
\]

This makes \(\mathcal C_n=\mathcal C_m\), a contradiction.  Thus \(\eta\) is
achronal.  An inextendible achronal causal curve is a lightlike line; in the
bounded branch, the closed achronal null curve becomes such a line by taking
infinitely many circuits.  A closed lightlike line need not be affine complete,
because its tangent can rescale after each circuit.

For each fixed point of \(\eta\), the limit construction supplies nearby points
from the successive \(\mathcal C_n\), so \(\eta\subset\overline{\mathcal C}\).
Achronality gives \(\eta\cap\mathcal C=\varnothing\), proving (1.1).  If strong
causality held at a point of \(\eta\), it would hold throughout some
neighborhood there, contradicting the chronology-violating approximants.
Thus it fails at every point of \(\eta\).  \(\square\)

This has five immediate consequences.

1. If a spacetime has no lightlike lines, its chronology classes form a locally
   finite family; hence every compact set meets only finitely many classes.
2. In dimension at least three, null convergence plus the null generic
   condition makes a complete null geodesic develop conjugate points.  A line
   cannot contain such points.  Therefore the forced Zeno line itself is affine
   incomplete in at least one direction under those two hypotheses, with no
   compact-generation assumption.
3. For a smooth spacetime, if it is instead null complete and obeys null
   convergence, genericity must fail along \(\eta\).  Galloway's null splitting
   theorem then places \(\eta\) in a smooth, properly embedded, achronal, totally
   geodesic null hypersurface.  It does not say that the whole chronology
   boundary is smooth.
4. In dimension at least three, strict null convergence at \(p\) in the forced
   direction supplies the null generic condition there.  Under null convergence,
   the direct focusing/index-form argument therefore makes \(\eta\) itself
   affine incomplete.  Since its direction is not known in advance, the
   convenient local hypothesis is strict positivity for every nonzero null
   vector at \(p\).  With Einstein's equation this is
   \(T_{ab}k^ak^b>0\); a perfect fluid gives
   \((\rho+p)(u\!\cdot\!k)^2>0\) when \(\rho+p>0\), and positive-density dust
   behaves similarly.  A null beam or electromagnetic field can saturate the
   condition in a principal null direction.  The null-splitting hypersurface of
   consequence 3 provides an independent rigidity check: its zero expansion
   and shear make Raychaudhuri give \(R_{ab}k^ak^b=0\) along every generator.
5. If \(\overline{\bigcup_n\mathcal C_n}\) is compact, or representative loops
   can all be chosen in one compact set, the resulting line is totally
   imprisoned there.

The physically useful form of consequence 4 is worth isolating.

> **Warm-exit corollary.**  Let a smooth spacetime of dimension at least three
> have pairwise distinct chronology classes accumulating at \(p\).  If null
> convergence holds globally and
> \(R_{ab}v^av^b>0\) at \(p\) for every nonzero null \(v\), then the spacetime is
> null geodesically incomplete; more precisely, the forced boundary line is
> affine incomplete in at least one direction.  Under the Einstein equation,
> global NEC and strict NEC at \(p\) are the equivalent matter hypotheses.

Indeed, if \(\eta\) were affine complete, take a parallel screen frame
\(E_i\) and a compactly supported plateau function \(f\).  The summed null
index form is

\[
\sum_{i=1}^{d-2} I(fE_i,fE_i)
=(d-2)\int (f')^2\,d\lambda
-\int f^2 R_{ab}k^ak^b\,d\lambda.
\tag{1.2}
\]

Continuity makes the second integrand strictly positive on an interval around
\(p\).  Null convergence keeps it nonnegative elsewhere, while moving the
ramps of \(f\) arbitrarily far out makes the first integral arbitrarily small.
The index form becomes negative, contradicting achronality of the line.

The strict condition need only hold for the tangent of the forced line; asking
for every null direction avoids having to know that tangent in advance.  The
stress must belong to a smooth full-backreaction solution.  A test body, point
particle, thin shell, a vacuum exit point, or a missing limiting event does not
satisfy the hypotheses.

Thus the observer in the definition is not needed for the theorem.  An
extendible finite-proper-time Zeno transit simply supplies the convergent
sequence \(p_n\to\gamma(\tau_*)\).  The sharp alternatives are null
incompleteness, failure of null convergence, or a nongeneric rigid limiting null
geometry.  Our explicit model uses the last two loopholes at its accumulation
line and also contains the incomplete companion sectors analyzed below.

---

## 2. The exactly solvable core

Consider

\[
M_0=\mathbb R_t\times S^1_\psi\times\mathbb R^2,
\qquad \psi\sim\psi+P,
\]

with

\[
ds^2=-dt^2+2\,dt\,d\psi+b(t)d\psi^2+dx^2+dy^2,
\qquad b(t)>-1.
\tag{2.1}
\]

Let

\[
a(t)=\sqrt{1+b(t)}.
\]

Then

\[
ds^2=-(dt-d\psi)^2+a(t)^2d\psi^2+dx^2+dy^2,
\tag{2.2}
\]

so the metric is Lorentzian for every \(a>0\), including at \(b=0\).

The periodic Killing field \(K=\partial_\psi\) obeys

\[
g(K,K)=b(t).
\]

Consequently its orbits are timelike for \(b<0\), null for \(b=0\), and
spacelike for \(b>0\).  In the positive bands,

\[
g^{-1}(dt,dt)=-\frac{b}{1+b}<0,
\tag{2.3}
\]

so \(t\) is a temporal function.

At a zero of \(b\), future causal vectors have \(dt\geq0\); equality occurs
only along the closed null generator.  Each zero is therefore a one-way causal
barrier.  A closed timelike curve cannot cross it and later cross back in the
opposite direction.  It follows that for this cylinder

\[
\mathcal C=\{b(t)<0\}.
\tag{2.4}
\]

Each negative component is separated from the next by a temporal positive
band and hence belongs to a different chronology class.

### A smooth accumulating stack

Near \(t=0\), take

\[
b(t)=
\begin{cases}
\varepsilon e^{-1/t^2}\sin^3(-1/t),&t<0,\\[3pt]
0,&t=0,\\[3pt]
\varepsilon e^{-1/t^2},&t>0,
\end{cases}
\qquad 0<\varepsilon<1,
\tag{2.5}
\]

and extend it smoothly and positively away from the displayed neighborhood.
Its negative and positive components alternate between

\[
t_n=-\frac1{n\pi},\qquad n=1,2,\ldots,
\]

and accumulate at \(t=0\).  The function and all of its derivatives vanish at
the accumulation point.  The cubic is not essential for the transit; it is
chosen so that

\[
b'(t_n)=b''(t_n)=0
\]

at every finite chronology boundary.  Thus every closed null generator has
zero surface gravity in the normalization used below.

The curve

\[
\gamma(t)=(t,\psi_0,x_0,y_0)
\tag{2.6}
\]

is a unit timelike geodesic.  It crosses infinitely many distinct chronology
classes in finite proper time, passes through \(t=0\), and continues into the
chronological region \(t>0\).

### Exact curvature and parallel propagation

An orthonormal frame is

\[
e_{\hat0}=\partial_t,
\qquad
e_{\hat1}=\frac{\partial_t+\partial_\psi}{a},
\qquad
e_{\hat2}=\partial_x,
\qquad
e_{\hat3}=\partial_y.
\tag{2.7}
\]

All four vectors are parallel propagated along \(\gamma\).  The scalar
curvature is

\[
R=\frac{2(1+b)b''-(b')^2}{2(1+b)^2}
  =2\frac{a''}{a}.
\tag{2.8}
\]

The Einstein tensor has only

\[
G_{xx}=G_{yy}=-\frac{R}{2}=-\frac{a''}{a}
\tag{2.9}
\]

nonzero in the displayed coordinate/frame split.  Since (2.5) is smooth and
flat to all orders at \(t=0\), scalar curvature and parallel-propagated
curvature stay bounded and in fact vanish at the accumulation.  The selected
traveler encounters no local curvature singularity there.

This is already enough to disprove the naive claim that infinitely many
chronology classes in finite proper time force curvature blow-up.  It does not
establish null geodesic completeness; Section 5 shows that completeness fails.

---

## 3. Spatial localization: an AF, horizonless Zeno metric

The cylinder can be embedded into an exactly flat exterior without a thin
shell.

Use cylindrical coordinates on

\[
M=\mathbb R_t\times\mathbb R^3,
\]

choose \(R>0\), and choose a smooth function

\[
0\leq\chi(\rho,z)\leq1
\]

which is compactly supported away from the rotation axis and equals one on an
open toroidal core.  Define

\[
Q^2(t,\rho,z)
=(1-\chi)\rho^2+\chi R^2[1+b(t)]
\tag{3.1}
\]

and

\[
ds^2=-(dt-R\chi\,d\phi)^2
     +Q^2d\phi^2+d\rho^2+dz^2.
\tag{3.2}
\]

Because \(\chi\) vanishes on a neighborhood of the axis, every term containing
\(d\phi\) is globally smooth despite the cylindrical chart.  In the support of
\(\chi\), \(Q^2>0\) follows from \(b>-1\).  Outside that spatially compact
support,

\[
ds^2=-dt^2+d\rho^2+\rho^2d\phi^2+dz^2.
\]

Thus the spacetime is exactly Minkowski near spatial and null infinity, not
merely asymptotically so.

The axial Killing norm is

\[
B:=g_{\phi\phi}
=(1-\chi)(\rho^2+R^2\chi)+R^2\chi b(t).
\tag{3.3}
\]

On the core, \(B=R^2b\), giving circular CTCs whenever \(b<0\).  Whenever
\(b>0\), (3.3) is positive everywhere away from the harmless coordinate axis,
and

\[
g^{-1}(dt,dt)=-\frac{B}{Q^2}<0.
\tag{3.4}
\]

Every positive-\(b\) time band is therefore a **global temporal barrier**.  The
full chronology set may spread beyond the core during a negative band, but it
cannot enter a positive band and cannot join chronology classes on opposite
sides of one.  Hence the core observer meets infinitely many genuinely
distinct chronology classes, not merely infinitely many sign changes of a
local norm.

At \(b=0\), chronology is excluded by openness of \(\mathcal C\) and the
adjacent temporal band, although the core contains closed null axial orbits.
The safe global inclusion is

\[
\{b<0,\ \chi=1\}\subseteq\mathcal C\subseteq\{b<0\}.
\tag{3.5}
\]

### The traveler

At a fixed core point, \(\partial_t\) is again a unit timelike geodesic because

\[
g_{tt}=-1,
\qquad
g_{t\phi}=R\chi(\rho,z)
\]

are independent of \(t\) in the relevant Christoffel expression.  It crosses
the entire stack regularly.

An actual visitor can come from the flat exterior and return to it.  Set
\(d\phi=dz=0\) and choose a smooth radial profile with

\[
\left|\frac{d\rho}{dt}\right|<1.
\]

Along this path,

\[
ds^2=-dt^2+d\rho^2<0,
\]

independently of \(\chi\) and \(b\).  The observer may enter before the Zeno
sequence, remain in the core while it crosses the accumulating chronology
classes, and leave after \(t=0\).  This is an open material trajectory, not a
closed geodesic, so single-valuedness does not require its memory to reset.

### No event horizon

From every event, the outward radial curve

\[
t=t_0+s,
\quad
\rho=\rho_0+s,
\quad
\phi=\phi_0,
\quad
z=z_0
\]

is future null.  After it leaves the support of \(\chi\), it is an ordinary
Minkowski outgoing ray reaching \(\mathscr I^+\).  It need not be geodesic in
the interior: causal reachability is enough.  Therefore every event lies in

\[
J^-(\mathscr I^+),
\]

and the black-hole event horizon is empty.

This gives a positive kinematic answer to the motivating question: an AF
spacetime with no event horizon can contain a regular finite-proper-time
traveler that enters an infinite Zeno chronology stack and later returns to a
chronological exterior.

The qualification is important.  Equation (3.2) is a prescribed exact metric.
It solves Einstein's equation with the conserved effective source

\[
T_{ab}=\frac1{8\pi}G_{ab},
\]

but no conventional constitutive matter model has yet been supplied.  The next
section shows that this source is necessarily exotic.

---

## 4. Exact energy-condition obstruction in the core

For (2.1), or for the open \(\chi=1\) core of (3.2), decompose a four-dimensional
null vector as \(k=v+w\), with \(v\) tangent to the \(t,\psi\) cylinder and \(w\)
transverse.  Since the two-dimensional Ricci tensor is

\[
\operatorname{Ric}^{(2)}=\frac{a''}{a}g^{(2)},
\]

nullness gives

\[
\operatorname{Ric}(k,k)
=-\frac{a''}{a}|w|^2.
\tag{4.1}
\]

The null convergence condition, equivalently the NEC under Einstein's
equation, is therefore exactly

\[
a''\leq0.
\tag{4.2}
\]

Thus \(a\) must be concave.  If a negative CTC band is bounded by \(t_-\) and
\(t_+\), then

\[
a(t_-)=a(t_+)=1,
\qquad
a(t)<1\quad(t_-<t<t_+).
\]

But a concave function lies above the chord joining its endpoint values, so it
would have to satisfy \(a\geq1\).  Contradiction.

Hence:

> In the direct-product circular ansatz, the NEC forbids even one bounded
> circular-CTC band.  An infinite alternating Zeno stack necessarily violates
> NEC in every negative component.

The violation occurs in the open core, where all derivatives of the spatial
cutoff vanish.  It cannot be blamed on, or repaired by, the toroidal matching
region.

In the parallel frame (2.7),

\[
T_{\hat a\hat b}=\operatorname{diag}(0,0,p,p),
\qquad
p=-\frac{a''}{8\pi a}.
\tag{4.3}
\]

The dominant energy condition forces \(p=0\), hence \(a''=0\), throughout this
core family.  The zero ADM four-momentum of the exactly flat exterior is another
warning: positive-mass rigidity would force triviality if DEC held on a
complete asymptotically Euclidean slice.

This no-go is exact and nonlinear, but ansatz-specific.  Extra transverse
curvature or a nonsymmetric chronology mechanism can change (4.1).  Extending
the concavity argument with Raychaudhuri or null splitting methods is one of the
best routes to a genuinely general theorem.

---

## 5. The unavoidable recurrent null sector

Zero surface gravity is not enough to make the circular construction globally
regular.

Consider the general two-dimensional circular ansatz

\[
g_2=-A(t)dt^2+2C(t)dt\,d\phi+B(t)d\phi^2,
\qquad \phi\sim\phi+P,
\tag{5.1}
\]

with

\[
\Delta=C^2+AB>0.
\]

Suppose \(B(0)=0\), the Killing field \(\partial_\phi\) does not vanish, and the
zero is isolated on one side.  Lorentz signature gives \(C(0)\neq0\).

For any null geodesic, the Killing momentum

\[
L=C\dot t+B\dot\phi
\]

and nullity imply the exact identity

\[
L^2=\Delta\dot t^{,2}.
\tag{5.2}
\]

One null branch crosses \(B=0\) regularly.  The other has

\[
\frac{d\phi}{dt}\sim-\frac{2C(0)}{B(t)}.
\tag{5.3}
\]

Equation (5.2) puts \(t=0\) at finite affine distance.  But \(C^1\) regularity
gives

\[
|B(t)|\leq M|t|,
\]

so (5.3) has infinite total angular variation.  The angle is monotone on the
chosen punctured side, and (phi\bmod P) has no limit.  The null geodesic has
no endpoint and is affinely incomplete despite the smooth, nondegenerate
metric and bounded curvature.

Equivalently, after a regular angular shift and a reparametrization of \(t\),
(5.1) takes the ribbon form

\[
g_2=2\,dT\,d\psi+\mathcal B(T)d\psi^2.
\tag{5.4}
\]

The null branches are simply

\[
d\psi=0,
\qquad
\frac{d\psi}{dT}=-\frac2{\mathcal B(T)},
\tag{5.5}
\]

and \(T\) is affine on the second branch.  This is the familiar Misner ribbon
mechanism.

### Closed generator versus companion branch

On \(B=0\), with \(K=\partial_\phi\),

\[
\nabla_KK=\kappa K,
\qquad
\kappa=-\frac{B'(0)}{2C(0)}.
\tag{5.6}
\]

If \(B'(0)\neq0\), one circuit produces the standard Hawking--Misner logarithmic
boost

\[
h=P|\kappa|=\frac{P|B'(0)|}{2|C(0)|},
\tag{5.7}
\]

with energy multiplication \(e^h\) and inverse affine compression \(e^{-h}\).

If \(B'(0)=0\), the closed null generator itself is affinely complete.  The
companion branch (5.3) is nevertheless incomplete.  For a finite odd-order
zero

\[
B(t)=b_m t^m+o(t^m),\qquad m>1,
\]

successive circuits \(q\to\infty\) obey

\[
|t_q|\asymp q^{-1/(m-1)},
\qquad
\ell_q\asymp q^{-m/(m-1)},
\qquad
\bar\omega_q\asymp q^{m/(m-1)}.
\tag{5.8}
\]

Here \(\ell_q\) is affine circuit length and \(\bar\omega_q\) is the circuit-
averaged frequency measured by a smooth timelike frame.  The cubic choice in
(2.5) gives \(\ell_q\asymp q^{-3/2}\) and
\(\bar\omega_q\asymp q^{3/2}\).

The same warning applies at the Zeno accumulation surface itself.  In (2.5),
\(b\) is positive and flat on the \(t>0\) side of \(t=0\).  The closed null
generator at \(t=0\) is complete and has \(\kappa=0\), but the singular branch
approaching it from \(t>0\) has finite affine length and more-than-polynomial
winding.  The timelike traveler and regular null branch cross \(t=0\); null
geodesic completeness of the spacetime still fails there in the opposite
channel.

More invariantly,

\[
\int_{I_q}\omega\,d\lambda
\longrightarrow
\Omega_U=
\int_0^P |g(U,K)|_{B=0}\,d\phi>0,
\tag{5.9}
\]

for each late circuit \(I_q\) and any smooth unit timelike laboratory field
\(U\).  Thus

\[
\bar\omega_q\ell_q\longrightarrow\Omega_U.
\tag{5.10}
\]

This is gain--compression reciprocity: flattening the horizon changes an
exponential Zeno sequence into a polynomial or stronger one, but does not make
a frequency-linear affine response summable.  Equation (5.9) is also the
limiting circuit length in the standard auxiliary Riemannian metric, so it
should be presented as a useful geometric repackaging rather than a major new
theorem.

### The two natural channels in the exact core

For (2.1), with \(L=p_\psi\) and \(a=\sqrt{1+b}\), the two null families have
frequencies measured by \(u=\partial_t\)

\[
E_{\rm reg}=\frac{L}{1+a},
\qquad
E_{\rm sing}=\frac{L}{1-a}.
\tag{5.11}
\]

The regular family crosses every \(b=0\) surface with

\[
E_{\rm reg}\longrightarrow\frac L2.
\]

It therefore supplies a bounded communication/escape channel through the
entire stack.  The singular family has \(E\sim-2L/b\), winds infinitely, and
never proceeds from one horizon to the next.

This prevents a common bookkeeping error.  Let \(j\) label different
chronology boundaries and \(q\) label repeated circuits near one boundary.
For the simple-zero version

\[
b(t)=\varepsilon e^{-1/t^2}\sin(-1/t),
\]

the one-circuit monodromies \(h_j\) are absolutely summable across the stack.
But a singular ray at fixed \(j\) executes \(q=1,2,\ldots\) circuits and is
amplified without bound; it never samples \(h_{j+1}\).  Conversely, the regular
ray and the timelike visitor cross each \(j\) only once and acquire no automatic
factor \(e^{h_j}\).  A formal product over horizons is not the gain of either
natural geodesic family.

The standard literature already contains the essential local theorem:

- Sánchez treats incomplete null geodesics asymptotic to a null Killing orbit
  for isolated zeros of arbitrary degeneracy.
- Bavard--Mounoud distinguish completeness of the null Killing orbit itself,
  which occurs at a degenerate zero.
- Petersen gives zero-surface-gravity compact Cauchy-horizon examples of the
  form \(2dt\,dx+(-t)^m dx^2\).
- Rieger derives the same two null families in general Misner-type ribbons.
- Hawking and Krasnikov already analyze repeated-return boost and measured
  energy near chronology/Cauchy horizons.

Our useful conclusion is therefore synthetic, not a claim that the ribbon
calculation itself is new:

> The timelike Zeno transit is curvature-regular, but every circular sign-change
> boundary carries a quasiregular null incompleteness, including when its closed
> generator is complete and has zero surface gravity.

---

## 6. Analyticity obstruction beyond a single circle

Let an analytic Lorentzian spacetime admit an analytic isometric action of a
torus \(T^k\).  At \(p\in M\), define the Gram form on its Lie algebra

\[
\mathsf B_p(\xi,\eta)=g_p(K_\xi,K_\eta).
\]

Let \(\mathcal C_T\) be the points lying on a timelike orbit of some closed
one-parameter subgroup.  Since rational lattice directions are dense,

\[
\mathcal C_T
=\{p:\mathsf B_p\text{ is not positive semidefinite}\}.
\tag{6.1}
\]

In a fixed basis, a symmetric matrix is positive semidefinite iff all of its
principal minors are nonnegative.  Therefore

\[
\mathcal C_T
=\bigcup_{\varnothing\ne I}\{\Delta_I<0\},
\tag{6.2}
\]

where the finitely many \(\Delta_I\) are analytic.  Thus \(\mathcal C_T\) is
semianalytic.  By standard Łojasiewicz structure theory, its connected
components form a locally finite family.  An analytic spacetime cannot have
infinitely many distinct symmetry-generated CTC components accumulating at an
interior event, even if the winding generator changes from band to band.

If an observer is an analytically extendible geodesic, the inverse image of
\(\mathcal C_T\) is a one-dimensional semianalytic set and has only finitely
many components on a compact parameter interval.

This is stronger than applying the identity theorem to one function
\(g_{\phi\phi}\), but it has a sharp limitation:

\[
\mathcal C_T\subseteq\mathcal C
\]

may be strict.  The full chronology set is global and need not be semianalytic.
Minguzzi's results describe its boundaries through achronal, null-generated
sets rather than local sign loci.  The analytic theorem reaches the true
chronology classes only when an additional symmetry-exhaustion statement

\[
\mathcal C=\mathcal C_T
\]

can be proved in the region of interest.

The theorem also does not constrain an arbitrary smooth accelerated observer
which oscillates across one analytic boundary.  It naturally constrains
geodesics and observers governed by a regular analytic finite-dimensional ODE.

The smooth flat function in (2.5) is therefore not decorative.  Nonanalyticity
is exactly how the model escapes local finiteness.  General hyperbolic
Einstein--matter evolution permits smooth nonanalytic data, so Einstein's
equation alone does not restore the obstruction.  Strictly stationary vacuum
or electrovac subclasses, and regular analytic cohomogeneity-one reductions,
are much less permissive.

---

## 7. What an escaping detector can and cannot retain

The geometry supplies both a regular traveler and a bounded null escape
channel.  It therefore does **not** force an open observer's memory to reset.
The observer's worldline does not return to the same event.

It also does not automatically provide infinite usable information.

### Exact classical radiation filter

The canonical ribbon (5.4) makes the warm-radiation issue exactly solvable for
a massless scalar.  Let

\[
ds^2=2\,dT\,d\psi+B(T)d\psi^2,
\qquad
\psi\sim\psi+P,
\tag{7.1}
\]

and define, on one punctured side of a zero of \(B\),

\[
H(T)=2\int^T\frac{dS}{B(S)},
\qquad
u=\psi,
\qquad
v=\psi+H(T).
\tag{7.2}
\]

Then

\[
ds^2=B\,du\,dv,
\qquad
\Box\Phi=\frac4B\,\partial_u\partial_v\Phi.
\tag{7.3}
\]

Every homogeneous solution is therefore

\[
\Phi=F(u)+G(v),
\tag{7.4}
\]

up to the familiar zero-mode term.  The cylinder identification is diagonal:
\((u,v)\sim(u+P,v+P)\).  Since \(H(T)\) winds through every phase modulo
\(P\) infinitely often as \(B\to0\), a nonconstant periodic \(G\) has no
continuous limit at the chronology boundary.  Moreover,

\[
\partial_T\Phi=\frac{2}{B}G'(v),
\tag{7.5}
\]

and the angularly averaged derivative energy grows as

\[
\frac1{B^2}\int_0^P|G'|^2\,d\psi.
\tag{7.6}
\]

Thus \(C^0\) extension forces \(G\) to be constant, and \(C^1\) or finite-stress
extension does so a fortiori.  The \(F\) sector crosses smoothly and remains an
arbitrary one-way communication channel.  Regularity removes one chirality; it
does not force the field, or the traveler's record, to be trivial.

The sourced problem gives an exact measure of the required tuning.  Expand

\[
\Phi=\sum_{n\in\mathbb Z}f_n(T)e^{ik_n\psi},
\qquad
J=\sum_{n\in\mathbb Z}J_n(T)e^{ik_n\psi},
\qquad
k_n=\frac{2\pi n}{P}.
\]

For \(\Box\Phi=J\),

\[
(Bf_n')'-2ik_nf_n'=-J_n.
\tag{7.7}
\]

The recurrent characteristic amplitude

\[
\mathcal A_n(T)
=B(T)e^{-ik_nH(T)}f_n'(T)
\tag{7.8}
\]

obeys

\[
\mathcal A_n(T_b)-\mathcal A_n(T_a)
=-\int_{T_a}^{T_b}J_n(T)e^{-ik_nH(T)}\,dT.
\tag{7.9}
\]

Assuming no incoming recurrent field, smooth passage after a compact source
therefore requires the countable moment conditions

\[
\int J_n(T)e^{-ik_nH(T)}\,dT=0
\quad(n\ne0),
\qquad
\int J_0(T)\,dT=0.
\tag{7.10}
\]

These conditions are **genericity constraints, not impossibility conditions**.
Their kernel is nonempty and infinite-dimensional; for example,
\(J_n=e^{ik_nH}q_n'\), with \(q_n\) compactly supported away from \(B=0\),
satisfies the \(n\)-th condition.  A generic bidirectional or thermal source
does not satisfy all of them.  It excites the recurrent sector and produces a
nonsmooth field/stress at the boundary unless the radiation is later
reabsorbed with exactly the compensating data.

There is also a direct retarded construction showing that the regular channel
is genuinely usable.  Put \(\tau=(v-u)/2=H(T)/2\), choose a smooth switch
\(q(\tau)\) which is zero before and one after a compact transition away from
\(B=0\), and let \(F\) be periodic.  Then

\[
\Phi=q(\tau)F(u),
\qquad
J=\Box\Phi
=\frac{-q''(\tau)F(u)+2q'(\tau)F'(u)}{B(T)}.
\]

The source is smooth and supported only in the transition region.  Its field
vanishes before the transition and is exactly \(F(u)\), with no recurrent
\(G(v)\) component, afterwards.  Thus the kernel in (7.10) is not merely a
formal cancellation: it contains compactly operated emitters with a nonzero
regular outgoing signal.

This is a precise classical version of the warm-traveler restriction:

> A visitor may retain memory and radiate through the regular channel, but a
> smooth prescribed chronology boundary acts as a chiral radiation filter.
> Ordinary warmth generically violates the filter; exact self-consistency or
> deliberately one-way emission can satisfy it.

The statement is exact for the \(1+1\) field sector and is not a linearized
Einstein calculation.  It also has an exact Maxwell embedding in the product
core: take

\[
A=\alpha(T,\psi)\,dx.
\]

Lorenz gauge is automatic, \(F=d\alpha\wedge dx\), and the \(x\)-component of
Maxwell's equation is the same two-dimensional wave equation for \(\alpha\).
The conserved current \(J^a=\delta^a_xJ^x(T,\psi)\) therefore obeys the same
regular/recurrent channel criterion.  This mode is transversely uniform, so it
is not yet a finite-size warm body.

Finite transverse size does not make the dangerous directions measure zero.
For transverse momentum magnitude \(q\) and angular Killing momentum \(L\),
null rays in the product core satisfy

\[
\dot\psi
=\frac{L\pm\sqrt{L^2+Bq^2}}{B}.
\tag{7.11}
\]

One sheet stays finite and the other behaves as \(2L/B\) for an open family of
directions.  A generic local scalar or Maxwell source has nonzero Hadamard
direct-term projection onto both sheets.

Nevertheless, no theorem can say that **every** finite source must excite the
recurrent sheet.  Given a smooth compact field \(\Phi_0\) inside a prescribed
worldtube, \(J=\Box\Phi_0\) is an exactly tuned nonradiating scalar source.
Similarly, a compact potential \(A_0\) gives
\(J^a=(4\pi)^{-1}\nabla_b(dA_0)^{ba}\), which is automatically conserved and
has no free outgoing branch.  These sources are active cancellations, not
ordinary warm matter, but they prove that the restriction is generic rather
than logically necessary without emissivity or stochastic assumptions.

They do **not** settle the sharper finite-body question.  In the product core,
an exact one-sheet condition on Cauchy data is a half-wave projection whose
principal frequency is

\[
\sqrt{k_\psi^2+B|q_\perp|^2}.
\]

That projector is nonlocal in the transverse directions.  For a frozen
\(B>0\) and a fixed nonzero circular Fourier mode, Paley--Wiener gives a sharp
statement: if both the field and its exact one-sheet normal derivative are
compactly supported transversely, the field vanishes.  The anti-locality
theorem for fractional Laplacians gives the corresponding familiar result for
\(|D|\).  The massless \(1+1\) chiral sector is the important exception, since
there the square root becomes a local first-order operator and compact one-way
pulses do exist.

This frozen theorem cannot simply be imported into the Zeno spacetime.
Regularity at the chronology boundary defines a time-dependent Jost/scattering
map, not the instantaneous square-root operator; the zero circular mode and
Maxwell constraints also require separate treatment.  The precise open problem
is whether that exact scattering map has the same support-uniqueness property,
so that a nonzero, genuinely radiative, transversely compact source cannot have
regular-only output in the localized spacetime.  This is stronger than the
already-false claim about arbitrary compact currents.

Because the full chronology stack is not globally hyperbolic, a global
retarded Green operator is not automatic.  The theorem should be stated
bandwise, or in a local Hadamard region.  Extending it to a constitutive thermal
current and a self-gravitating worldtube is the next operational step.
Friedman and Morris's existence and uniqueness results for massless fields on
asymptotically flat CTC spacetimes show why this qualification is substantive:
some wormhole classes admit regular finite-energy solutions, whereas in smooth
AF examples with a compact nonchronal region either existence or uniqueness can
fail.  The present mode calculation supplies an exact local compatibility
condition; it does not silently assume a globally well-posed Cauchy problem.

For (2.5), the \(n\)-th time band has width of order

\[
\Delta t_n\asymp n^{-2},
\]

while its metric amplitude and every fixed finite derivative at the late bands
decay faster than any power.  A bounded-power detector can accumulate a finite
state change

\[
\sum_n\delta X_n,
\]

and emerge with a nonzero aggregate record, but late stages become
operationally indistinguishable at any fixed resolution.  For a finite-
dimensional quantum detector, the analogous statement is convergence of a
product of channels when

\[
\sum_n\|\Phi_n-\mathrm{id}\|_\diamond<\infty.
\]

This is ordinary channel theory and should remain a supporting lemma.

If a source emits bounded local power \(P\) during stage durations
\(\ell_n\), and the transfer factor to infinity is \(Z_n\), the basic outgoing
energy series is

\[
\sum_n E_n^+
\lesssim
P\sum_n Z_n\ell_n.
\tag{7.12}
\]

For

\[
\ell_n\sim e^{-\alpha n},
\qquad
Z_n\sim e^{\beta n},
\]

the threshold is \(\beta<\alpha\).  At \(\beta=\alpha\), every late pulse
delivers order-one energy and total positive Bondi flux would be infinite.
Finite initial mass then forces attenuation, termination, negative flux, or
backreaction that destroys the assumed geometry.

The new geometric lesson is that there are two different \(Z_n\)'s:

- along the regular null channel of (5.11), \(Z_n\) remains bounded and the
  diminishing stage widths win;
- along the recurrent channel at any fixed boundary, boost is the inverse of
  affine compression and a frequency-linear response is non-summable.

A cold or finely directed probe can use the first channel.  A genuinely warm
body generically emits into both null sectors.  Establishing what happens then
requires an exact coupled field/worldtube solution; one cannot infer it from a
test geodesic.  The likely obstruction is not that the traveler's memory must
reset, but that generic radiation excites the incomplete recurrent sector and
invalidates the prescribed background.

The symmetry-free theorem gives a complementary result for an actual
self-gravitating warm body.  If the accumulation event on the traveler's
worldline lies inside smooth perfect-fluid or positive-density dust matter,
then strict null energy holds there for every null direction.  Einstein's
equation, global null convergence, and Zeno accumulation are therefore
incompatible with null completeness by consequence 4 of Section 1.  This does
not say that the body must forget, cannot exit, or cannot radiate.  It says that
a null-complete, NEC-respecting completion of that warm exit is impossible;
the forced limiting boundary line must itself be affine incomplete in at least
one direction, or the energy/regularity hypotheses must fail.

No-cloning is not the primary issue.  A quantum detector may emerge in a
different state without cloning an unknown state.  The restrictions are finite
detector dimension, distinguishability, energy/bandwidth, and the existence of
a globally self-consistent quantum state near the chronology boundaries.  The
Kay--Radzikowski--Wald obstruction and detector divergences near Cauchy horizons
remain directly relevant.

---

## 8. Novelty map after the deeper audit

### Already occupied

- Infinite null windings in finite affine time and exponential boost:
  Hawking/Misner and later chronology-protection literature.
- Repeated laboratory passages and arbitrarily large measured photon-energy
  tails near compactly determined Cauchy horizons: Krasnikov.
- Compact chronology-boundary components and incomplete almost-closed null
  geodesics under focusing hypotheses: Kriele.
- A null line through a point shared by the boundaries of two fixed chronology
  classes, and the general coalescing-endpoint limit-curve machinery: Minguzzi.
- Degenerate Killing horizons and incomplete companion null geodesics:
  Sánchez, Bavard--Mounoud, Petersen, Mehidi, and Rieger.
- Infinite chains or accumulating bands in abstract Lorentzian surfaces:
  Bavard--Mounoud and Mehidi provide close mathematical neighbors.
- Finite covers and infinite-sheet Misner extensions: Rieger.
- Finite-time receipt of the output of an infinite computation:
  Malament--Hogarth spacetimes.
- A smooth toroidal prescribed time-machine metric equal to Minkowski outside
  a compact region, with transiting timelike geodesics: Fermi--Pizzocchero.

### Defensible new synthesis/candidate result

The strongest result not located in the targeted search is the countable-class
strengthening proved in Section 1:

> Failure of local finiteness of Carter chronology classes at any event forces
> a lightlike line in the chronology boundary.  With null convergence and null
> genericity, it forces null geodesic incompleteness; with null completeness and
> null convergence, the alternative is a rigid totally geodesic null sheet.
> Strict null energy in an ordinary warm worldtube at the accumulation event
> excludes that complete rigid alternative locally.

Minguzzi proves the adjacent result when one event lies in the boundaries of
two **fixed** classes.  In a Zeno sequence, the limiting event need not lie in
the closure of any individual class, so that theorem does not directly apply.
Our proof is a short mixed-index strengthening of his limit-curve argument.  A
targeted search did not find this locally-finite-or-null-line formulation, but
priority should still be checked by a causality specialist before submission.

The accompanying constructive conjunction is:

> A smooth, Hausdorff, \(3+1\)-dimensional, exactly AF spacetime with no event
> horizon contains infinitely many distinct chronology classes accumulating at
> a regular event; an open timelike observer enters from the exterior, crosses
> all of them in finite proper time, exits to a chronological future, and has a
> regular parallel-propagated frame.  In the circular construction, this is
> possible only with nonanalyticity and NEC violation, and every band boundary
> carries a quasiregular incomplete null sector even when its closed generator
> is degenerate.

The AF localization in Section 3 materially improves the earlier toy model,
but remains a prescribed-metric/effective-source construction.  The theorem
and the example now complement one another: the theorem says what any Zeno
accumulation must pay, while the example displays the allowed NEC-violating,
nongeneric branch explicitly.

### What remains to make the package submission-ready

The symmetry-free obstruction is now proved.  The main remaining tasks are:

1. **Causality-literature verification.**  Have the non-local-finiteness theorem
   checked against older limit-curve and chronology-class literature, then
   write its regularity and parametrization details in journal form.
2. **Specified Einstein--matter realization.**  Produce (3.2), or a replacement,
   from a definite classical matter model and quantify exactly which energy
   condition must fail and by how much.
3. **Finite-body radiation theorem.**  Prove or disprove anti-locality for the
   exact time-dependent scattering map, then add backreaction.  This would
   decide whether every nonzero compact radiative body excites the recurrent
   sector, not merely whether a generic source does.
4. **Global analytic lift.**  Find a physically meaningful class in which the
   full chronology set equals the torus-generated set, turning Section 6 into a
   theorem about actual chronology classes.

The theorem plus the explicit AF example is already a plausible mathematical-
relativity paper.  Item (2) is the strongest physical upgrade; item (3) is the
one most directly connected to the warm Groundhog-Day visitor.

---

## 9. Recommended paper architecture

A credible first paper would no longer lead with the elementary bounded-state
lemma.  It would proceed as follows.

1. Define Zeno chronology transit, prove the interval lemma, and lead with the
   symmetry-free non-local-finiteness/null-line theorem.
2. Give the exact smooth cylinder and prove the full causal classification.
3. Localize it to the AF toroidal metric (3.2), prove absence of an event
   horizon, and exhibit an entering/exiting timelike traveler.
4. Compute the exact Einstein tensor in the core and prove the NEC concavity
   obstruction.
5. Separate the regular crossing null channel from the recurrent incomplete
   channel, explicitly acknowledging the Sánchez--Rieger prior art.
6. Prove analytic local finiteness for a general \(T^k\) action.
7. Prove the exact chiral scalar/Maxwell filter and state the finite-transverse
   anti-locality problem, with detector convergence as a supporting lemma.
8. End with the null-incomplete versus rigid-null-sheet dichotomy and the
   specified-matter problem.

A suitable restrained claim is:

> Non-local finiteness of chronology classes forces a boundary lightlike line;
> under null convergence and null genericity it forces null incompleteness.
> Smooth AF transit by an open observer is nevertheless kinematically possible
> on the allowed nongeneric, NEC-violating branch, without curvature blow-up at
> the accumulation event.

That is more substantial than the original bounded-response observation and
more honest than advertising a "singularity-free time machine."

---

## References most directly controlling the new result

- S. W. Hawking, "The Chronology Protection Conjecture," *Phys. Rev. D* 46,
  603 (1992), [doi:10.1103/PhysRevD.46.603](https://doi.org/10.1103/PhysRevD.46.603).
- M. Sánchez, "Structure of Lorentzian tori with a Killing vector field,"
  *Trans. AMS* 349, 1063 (1997),
  [doi:10.1090/S0002-9947-97-01745-5](https://doi.org/10.1090/S0002-9947-97-01745-5).
- C. Bavard and P. Mounoud, "Extensions maximales et classification des tores
  lorentziens munis d'un champ de Killing,"
  [arXiv:1510.01253](https://arxiv.org/abs/1510.01253).
- L. Mehidi, "Maximal simply connected Lorentzian surfaces with a Killing field
  and their completeness,"
  [arXiv:2001.03149](https://arxiv.org/abs/2001.03149).
- O. L. Petersen, "Extension of Killing vector fields beyond compact Cauchy
  horizons," *Adv. Math.* 391, 107953 (2021),
  [arXiv:1903.09135](https://arxiv.org/abs/1903.09135).
- N. E. Rieger, "Causal classification of pathological Misner-type
  spacetimes," *Ann. Phys.* 489, 170455 (2026),
  [arXiv:2501.00841](https://arxiv.org/abs/2501.00841).
- S. Krasnikov, "Time machines with the compactly determined Cauchy horizon,"
  *Phys. Rev. D* 90, 024067 (2014),
  [arXiv:1405.2277](https://arxiv.org/abs/1405.2277).
- M. Kriele, "The structure of chronology violating sets with compact
  closure," *Class. Quantum Grav.* 6, 1607 (1989),
  [doi:10.1088/0264-9381/6/11/014](https://doi.org/10.1088/0264-9381/6/11/014).
- E. Minguzzi, "Limit curve theorems in Lorentzian geometry,"
  *J. Math. Phys.* 49, 092501 (2008),
  [arXiv:0712.3942](https://arxiv.org/abs/0712.3942),
  [doi:10.1063/1.2973048](https://doi.org/10.1063/1.2973048).
- E. Minguzzi, "The boundary of the chronology violating set,"
  *Class. Quantum Grav.* 33, 225004 (2016),
  [arXiv:1603.08190](https://arxiv.org/abs/1603.08190).
- E. Minguzzi, "Lorentzian causality theory," *Living Rev. Relativ.* 22, 3
  (2019),
  [doi:10.1007/s41114-019-0019-x](https://doi.org/10.1007/s41114-019-0019-x).
- G. J. Galloway, "Maximum principles for null hypersurfaces and null splitting
  theorems," *Ann. Henri Poincare* 1, 543 (2000),
  [arXiv:math/9909158](https://arxiv.org/abs/math/9909158).
- D. Fermi and L. Pizzocchero, "A time machine for free fall into the past,"
  *Class. Quantum Grav.* 35, 165003 (2018),
  [arXiv:1803.08214](https://arxiv.org/abs/1803.08214).
- J. L. Friedman and M. S. Morris, "Existence and uniqueness theorems for
  massless fields on a class of spacetimes with closed timelike curves,"
  *Commun. Math. Phys.* 186, 495 (1997),
  [arXiv:gr-qc/9411033](https://arxiv.org/abs/gr-qc/9411033),
  [doi:10.1007/s002200050118](https://doi.org/10.1007/s002200050118).
- T. Ghosh, M. Salo, and G. Uhlmann, "The Calderon problem for the fractional
  Schrodinger equation," *Anal. PDE* 13, 455 (2020),
  [arXiv:1609.09248](https://arxiv.org/abs/1609.09248),
  [doi:10.2140/apde.2020.13.455](https://doi.org/10.2140/apde.2020.13.455).
- S. V. Slobodov, "Unwrapping Closed Timelike Curves," *Found. Phys.* 38,
  1082 (2008), [arXiv:0808.0956](https://arxiv.org/abs/0808.0956).
- B. S. Kay, M. J. Radzikowski, and R. M. Wald, "Quantum field theory on
  spacetimes with a compactly generated Cauchy horizon," *Commun. Math. Phys.*
  183, 533 (1997),
  [arXiv:gr-qc/9603012](https://arxiv.org/abs/gr-qc/9603012).
- B. A. Juárez-Aubry and J. Louko, "Quantum kicks near a Cauchy horizon,"
  *AVS Quantum Sci.* 4, 013201 (2022),
  [arXiv:2109.14601](https://arxiv.org/abs/2109.14601).
