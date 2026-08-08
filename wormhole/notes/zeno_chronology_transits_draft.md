# Zeno chronology transits: null-line obstructions and asymptotically flat escape

> **Working manuscript — 2 August 2026.**  The novelty assessment is provisional
> pending a systematic priority search and review by a specialist in Lorentzian
> causality.  The prescribed metric below is an exact Lorentzian geometry with
> an effective Einstein source, not yet a solution for a specified constitutive
> matter model.

## Abstract

We introduce a regular Zeno chronology transit, in which an extendible timelike
curve meets infinitely many distinct Carter chronology classes in finite proper
time.  We prove that failure of local finiteness of chronology classes at an
event forces a two-sided inextendible achronal null geodesic through that event,
contained in the boundary of the chronology-violating set.  Under the null
convergence and null generic conditions this line is affine incomplete.  More
locally, null convergence together with strict null convergence at the
accumulation event makes the forced line itself incomplete; in Einstein gravity
this gives a conditional obstruction for a smooth, self-gravitating material
traveler with strict null energy at the accumulation event.  Conversely, null
completeness and null convergence place the line in a rigid totally geodesic
null hypersurface.

We then construct a smooth four-dimensional spacetime that is exactly
Minkowski outside a fixed spatially compact toroidal region and has no
black-hole event horizon.  An open timelike observer can enter the toroidal
core, cross infinitely many distinct chronology classes in finite proper time,
and exit into a chronological future with bounded parallel-propagated
curvature.  The construction is nonanalytic, violates the null energy condition
in its circular core, and possesses an incomplete recurrent null family even
when the corresponding closed null generators in the product core are
degenerate.  Finally, an exact scalar and
Maxwell mode analysis separates a regular local boundary-crossing channel from
a recurrent singular channel.  Smooth passage permits a nontrivial local
record channel but imposes countably many compatibility conditions on sources.
The resulting picture is not a singularity-free time machine: regular timelike
exit and local boundary-crossing communication coexist with null incompleteness
and exotic effective matter.

## 1. Introduction

Can an observer pass through a chronology-violating region, learn something,
and return to an ordinary exterior with a record?  The kinematic answer is
different for closed and open material histories.  A body whose complete
worldline returns to the same event must participate in one single-valued global
solution, including its memory, radiation, and environment.  This aspect of
self-consistency, dissipation, and entropy was studied extensively by Friedman
et al. (1990), Echeverria, Klinkhammer, and Thorne (1991), and Lossev and Novikov
(1992).  An open traveler does not return to the same event, so no periodicity
condition alone requires its final state to equal its initial state.

The more useful invariant question is whether an extendible traveler can cross
infinitely many genuinely different chronology-violating regions in finite
proper time.  Terms such as “sheet,” “copy,” and “winding” depend on a chosen
covering or diagram.  Changing the global quotient can unwrap some closed
timelike curves, but may introduce quasiregular singularities instead (Slobodov
2008); all chronology classes below refer to the fixed spacetime under
discussion.  We therefore formulate the problem using Carter
chronology classes, the equivalence classes of the relation
\(p\sim q\) iff \(p\ll q\ll p\).  A **Zeno chronology transit** samples
infinitely many such classes and accumulates at an interior event.

This paper establishes four groups of results.

1. **A symmetry-free causal obstruction.**  If points in pairwise distinct
   chronology classes converge to \(p\), a two-sided lightlike line passes
   through \(p\) and lies in the boundary of the chronology-violating set.  No
   compactness, asymptotic hypothesis, symmetry, field equation, or energy
   condition is needed.  Null convergence and focusing then make the line
   incomplete under standard genericity, or under strict null convergence at
   \(p\).
2. **A regular timelike realization.**  A smooth circular core contains
   infinitely many distinct chronology bands accumulating at a regular event.
   A timelike geodesic and its parallel-propagated frame cross the accumulation
   with bounded curvature.
3. **An accessible asymptotically flat localization.**  The core can be placed
   inside a smooth toroidal perturbation of Minkowski spacetime.  An open
   timelike curve enters, crosses the full stack, and exits; every event can send
   a causal signal to the standard future null infinity.  The cutoff can be
   chosen so that every transition-region closed null axial orbit is
   nongeodesic.
4. **The price of the construction.**  The direct-product core violates the
   null energy condition somewhere in every bounded CTC band.  Its chronology
   boundaries carry a recurrent null family that winds infinitely in finite
   affine length, even when the closed generator has zero surface gravity.  An
   exact field calculation shows that the other chirality remains a nontrivial
   local boundary-crossing channel.

The first result is closest to Minguzzi’s limit-curve theorem and his result for
an event lying in the boundaries of two fixed chronology classes (Minguzzi
2008, Theorem 4.5; 2016, Theorem 2.1).  In the Zeno setting the limiting event
need not lie in the closure of any one class: the class itself changes with the
sequence.  Minguzzi's fixed-class conclusion does not imply local finiteness,
because pairwise disjoint class closures can still accumulate.  We have not
found the resulting locally-finite-or-lightlike-line formulation stated
explicitly, but it is a short mixed-index extension of that machinery rather
than an independent replacement for it.  Kriele (1989), Hawking (1992), and
Krasnikov (2014) obtain related incompleteness or recurrent-null conclusions
under compactness or Cauchy-horizon hypotheses.  Our theorem does not assume
that the chronology boundary is a Cauchy horizon or that it is compactly
generated.

The explicit geometry is closest in spirit to the spatially localized
prescribed time-machine metric of Fermi and Pizzocchero (2018), while its local
null ribbons belong to the mathematical framework developed by Sánchez (1997),
Bavard and Mounoud (2020), Mehidi (2022), Petersen (2021), and Rieger (2026).
The construction below differs by realizing a finite-time transit through
infinitely many distinct chronology classes and by separating the regular and
recurrent propagation channels explicitly.

Several limitations should be kept visible.  The localized metric has the
conserved effective source \(G_{ab}/(8\pi)\), but no conventional constitutive
matter model is supplied.  The explicit traveler is a timelike curve or test
observer, not a warm self-gravitating body.  The warm-matter statement is a
conditional theorem for any smooth full-backreaction solution satisfying its
hypotheses.  The scalar and Maxwell results are exact in a (1+1) sector but do
not yet constitute a theorem for a transversely compact radiating body.

Section 2 gives the causal theorem and focusing corollaries.  Sections 3 and 4
construct the smooth core and its spatially compact localization.  Section 5
identifies the energy, completeness, and analyticity costs.  Section 6 studies
local record channels.  Technical limit-curve, tensor, null-geodesic, and field
calculations are collected in the appendices.

## 2. Accumulating chronology classes

Let \((M,g)\) be a connected, time-oriented \(C^2\) spacetime and write

\[
\mathcal C=\{p\in M:p\ll p\}
\tag{2.1}
\]

for its chronology-violating set.  For \(p\in\mathcal C\), its Carter class is

\[
[p]=I^+(p)\cap I^-(p).
\tag{2.2}
\]

These classes are open and form the connected causal units relevant here.  We
say that the family of chronology classes is **locally finite at** \(p\) if
some neighborhood of \(p\) meets only finitely many classes.  A **lightlike
line** means a two-sided inextendible achronal causal curve, hence an
inextendible null geodesic.  Affine completeness is not included in this
definition.

### 2.1 Regular Zeno transits

**Definition 2.1.**  A future-directed timelike curve

\[
\gamma:(\tau_0,\tau_*+\delta)\longrightarrow M
\]

is a **regular Zeno chronology transit** if there are pairwise distinct
chronology classes \(\mathcal C_n\) and parameters
\(\tau_n\nearrow\tau_*<\infty\) such that
\(\gamma(\tau_n)\in\mathcal C_n\), while both the curve and the metric extend
through \(\tau_*\) with the stated regularity.  Bounded
parallel-propagated curvature, an extendible finite-radius worldtube, and a
convergent detector state are useful additional conditions, but are not built
into the causal definition.

The distinction between different classes and repeated visits to one class is
not cosmetic.

**Lemma 2.2 (interval lemma).**  If a future timelike curve meets one chronology
class at parameters \(s_1<s_3\), it meets that class at every
\(s_2\in(s_1,s_3)\).

**Proof.**  We have
\(\gamma(s_1)\ll\gamma(s_2)\ll\gamma(s_3)\), while membership of the endpoints
in one class gives \(\gamma(s_3)\ll\gamma(s_1)\).  Concatenation puts the middle
point in the same class.  ∎

Thus the inverse image of each chronology class along a timelike observer is an
interval.  A Zeno transit cannot be manufactured merely by relabeling repeated
windings through one class.  It also differs from a Malament--Hogarth supertask:
there, a finite-time observer receives the output of another worldline with
infinite proper duration; here, one extendible observer crosses infinitely many
causal regions.

### 2.2 The non-local-finiteness theorem

**Theorem 2.3.**  Suppose \(p_n\to p\), where \(p_n\in\mathcal C_n\) and the
chronology classes \(\mathcal C_n\) are pairwise distinct.  Then, for some
subsequence, again denoted \(p_n\in\mathcal C_n\), a lightlike line \(\eta\)
passes through \(p\) and

\[
\eta\subset\partial\mathcal C.
\tag{2.3}
\]

For every point \(q\in\eta\), there are points \(q_n\in\mathcal C_n\) with
\(q_n\to q\).  Strong causality fails at every point of \(\eta\).

**Proof.**  After the subsequence selection and relabeling in Appendix A, the
limit-curve construction supplies either a two-sided inextendible causal curve
through \(p\), or a nonconstant closed causal limit whose periodic extension is
two-sided inextendible.  In either case, call the resulting curve \(\eta\).
Every finite collection of points of \(\eta\) has simultaneous approximants on
the closed timelike curves contained in the successive selected classes.

Suppose \(a,b\in\eta\) and \(a\ll b\).  Choose approximants
\(a_n,b_n\in\mathcal C_n\) and \(a_m,b_m\in\mathcal C_m\) for two sufficiently
large distinct indices.  Openness of \(I^+\), followed by mutual timelike
relatedness within each class, gives

\[
a_n\ll b_m\ll a_m\ll b_n\ll a_n.
\tag{2.4}
\]

This makes \(\mathcal C_n=\mathcal C_m\), a contradiction.  Hence \(\eta\) is
achronal and therefore a lightlike line.  Each point of \(\eta\) is a limit of
chronology-violating points.  It cannot itself lie in \(\mathcal C\), because
its open chronology class would then contain all sufficiently late
approximants.  This proves (2.3).  If strong causality held at a point of
\(\eta\), openness of the strong-causality locus would put all sufficiently
late approximants there in that locus, although each lies on a closed timelike
curve.  Thus strong causality fails everywhere on \(\eta\).  ∎

The theorem immediately gives a local-finiteness criterion.

**Corollary 2.4.**  In a spacetime without lightlike lines, the chronology
classes form a locally finite family.  Consequently every compact set meets
only finitely many classes.

If \(\overline{\bigcup_n\mathcal C_n}\) is compact, or if representative closed
timelike curves can all be chosen in one compact set, the line supplied by
Theorem 2.3 is totally imprisoned there.  Compactness is a consequence in that
case, not a hypothesis of the theorem.

### 2.3 Focusing, rigidity, and matter at the accumulation event

Assume now that \(\dim M=d\ge3\).  Under the null convergence condition

\[
R_{ab}k^ak^b\ge0
\tag{2.5}
\]

and the null generic condition along \(\eta\), an affine-complete null geodesic
develops conjugate points.  A lightlike line cannot contain such points.

**Corollary 2.5.**  If null convergence holds and the null generic condition
holds along the line forced by Theorem 2.3, that line is affine incomplete in
at least one direction.

The generic condition may be replaced by a strictly local matter hypothesis.

**Corollary 2.6 (strict focusing at the exit).**  Suppose null convergence holds
globally and, at the accumulation event \(p\),

\[
R_{ab}v^av^b>0
\quad\text{for every nonzero null }v\in T_pM.
\tag{2.6}
\]

Then the line forced through \(p\) is affine incomplete in at least one
direction.

**Proof.**  Suppose the line were affine complete, affinely parametrize it on
\(\mathbb R\), put \(p=\eta(0)\) and \(k=\dot\eta\), and take a parallel
orthonormal screen frame \(E_i\).  For a compactly supported function \(f\), the
summed null index form is

\[
\sum_{i=1}^{d-2}I(fE_i,fE_i)
=(d-2)\int(f')^2\,d\lambda
-\int f^2R_{ab}k^ak^b\,d\lambda.
\tag{2.7}
\]

By continuity, there are \(\epsilon,A>0\) such that
\(R_{ab}k^ak^b\ge A\) on \([-\epsilon,\epsilon]\); null convergence keeps this
quantity nonnegative elsewhere.  Choose \(f_L=1\) on this interval, taper it to
zero on two ramps of affine length \(L\), and smooth the corners without
materially changing the estimates.  Then

\[
\int (f_L')^2\,d\lambda\longrightarrow0,
\qquad
\int f_L^2R_{ab}k^ak^b\,d\lambda\ge2\epsilon A.
\]

For large \(L\), (2.7) is negative.  At least one screen variation therefore
has negative index form, contradicting the achronality of the null line.  ∎

Only positivity in the actual tangent direction of the forced line is
logically necessary.  Condition (2.6) avoids having to know that direction in
advance.  With

\[
G_{ab}+\Lambda g_{ab}=8\pi G\,T_{ab},
\]

null contraction gives \(R_{ab}k^ak^b=8\pi G\,T_{ab}k^ak^b\).  A smooth perfect
fluid satisfies

\[
T_{ab}k^ak^b=(\rho+p)(u\!\cdot\!k)^2,
\tag{2.8}
\]

which is strictly positive for every nonzero null \(k\) when
\(\rho+p>0\); positive-density dust behaves similarly.  Pure null dust and
electromagnetic fields can saturate the condition in special principal null
directions.

**Matter-at-the-accumulation consequence.**  In a smooth full-backreaction
solution obeying the global NEC, if the Zeno accumulation event lies inside a
finite material worldtube with strict null energy in every direction, the
forced boundary line is incomplete.  This statement does not apply to a test
body, a distributional point particle or thin shell, a vacuum exit event, or a
missing boundary point.
It says neither that memory must reset nor that the traveler cannot exit; it
says that such an exit cannot belong to a null-complete NEC-respecting
spacetime.

For comparison, if a smooth spacetime is null complete and obeys null
convergence, Galloway’s null splitting theorem places \(\eta\) in a smooth,
properly embedded, achronal, totally geodesic null hypersurface.  Its expansion
and shear vanish, and Raychaudhuri gives \(R_{ab}k^ak^b=0\) along every
generator.  The complete branch is therefore rigid and necessarily nongeneric;
the theorem does not imply that the full chronology boundary is a smooth
hypersurface.

## 3. An exactly solvable smooth Zeno core

Consider

\[
M_0=\mathbb R_t\times S^1_\psi\times\mathbb R^2,
\qquad \psi\sim\psi+P,
\]

with metric

\[
ds^2=-dt^2+2\,dt\,d\psi+b(t)d\psi^2+dx^2+dy^2,
\qquad b(t)>-1.
\tag{3.1}
\]

We time-orient the spacetime by declaring \(\partial_t\) future directed.
Writing \(a(t)=\sqrt{1+b(t)}\) gives

\[
ds^2=-(dt-d\psi)^2+a(t)^2d\psi^2+dx^2+dy^2,
\tag{3.2}
\]

so the metric remains smooth and Lorentzian at \(b=0\).  The periodic Killing
field \(K=\partial_\psi\) has norm

\[
g(K,K)=b(t).
\tag{3.3}
\]

Its orbits are closed timelike curves for \(b<0\), closed null curves for
\(b=0\), and spacelike circles for \(b>0\).  In every positive band,

\[
g^{-1}(dt,dt)=-\frac{b}{1+b}<0,
\tag{3.4}
\]

so \(t\) is temporal.  At a zero of \(b\), every future causal vector has
\(dt\geq0\), with equality only in the direction of the closed null generator.
The zero is therefore a one-way causal barrier.  A closed timelike curve cannot
cross it and later return across it in the opposite direction.  It follows that

\[
\mathcal C=\{b(t)<0\}.
\tag{3.5}
\]

Every negative component is one chronology class.  Indeed, join any two of its
points by a smooth path whose image is compactly contained in the component.
On a lift of the circular coordinate, adding sufficiently many turns in the
future-timelike direction of \(K\) makes the path timelike while preserving its
endpoints on the quotient; applying the same construction in reverse makes the
two points mutually chronological.  Different components are separated by
temporal positive bands.

### 3.1 A flat accumulating stack

Choose the global smooth function

\[
b(t)=
\begin{cases}
\varepsilon e^{-1/t^2}\sin^3(-1/t),&t<0,\\[3pt]
0,&t=0,\\[3pt]
\varepsilon e^{-1/t^2},&t>0,
\end{cases}
\qquad 0<\varepsilon<1.
\tag{3.6}
\]

The chronology boundaries

\[
t_n=-\frac1{n\pi},\qquad n=1,2,\ldots,
\tag{3.7}
\]

accumulate at \(t=0\).  The function and all of its derivatives vanish at the
accumulation event.  The cubic is chosen so that

\[
b'(t_n)=b''(t_n)=0,
\tag{3.8}
\]

making the closed null generators degenerate in the normalization used in
Section 5.  Degeneracy is not needed for the timelike transit; it isolates what
zero surface gravity does and does not cure.

The curve

\[
\gamma(t)=(t,\psi_0,x_0,y_0)
\tag{3.9}
\]

is a unit timelike geodesic.  It crosses infinitely many distinct chronology
classes in finite proper time, passes through \(t=0\), and continues into the
chronological region \(t>0\).

### 3.2 Parallel propagation and curvature

Along \(\gamma\), the frame

\[
e_{\hat0}=\partial_t,
\qquad
e_{\hat1}=\frac{\partial_t+\partial_\psi}{a},
\qquad
e_{\hat2}=\partial_x,
\qquad
e_{\hat3}=\partial_y
\tag{3.10}
\]

is orthonormal and parallel propagated.  The scalar curvature and nonzero
Einstein components are

\[
R=\frac{2(1+b)b''-(b')^2}{2(1+b)^2}
=2\frac{a''}{a},
\qquad
G_{xx}=G_{yy}=-\frac{R}{2}=-\frac{a''}{a}.
\tag{3.11}
\]

Appendix B gives the connection and tensor calculation.  Since (3.6) is flat to
all orders at \(t=0\), all curvature components in the parallel frame remain
bounded and vanish at the accumulation event.  The selected timelike traveler
therefore crosses a smooth, curvature-regular event.  This disproves the purely
kinematic claim that finite-proper-time transit through infinitely many
chronology classes must cause curvature blow-up.  It does not imply null
geodesic completeness; Section 5.2 shows that the opposite null family is
incomplete.

Theorem 2.3 is visible explicitly at the accumulation event.  The closed null
orbit of \(K\) at \(t=0\), periodically extended, is a lightlike line in
\(\partial\mathcal C\).  It is affinely complete and nongeneric, while a
different null family approaching the same surface is incomplete.

## 4. A spatially compact asymptotically flat localization

The circular core can be localized without a thin shell.  Use cylindrical
coordinates on

\[
M=\mathbb R_t\times\mathbb R^3,
\]

fix \(R>0\), and choose a smooth cutoff

\[
0\le\chi(\rho,z)\le1
\]

that has spatially compact support away from the rotation axis and equals one
on an open toroidal core.  Sections 4.1--4.3 use only these properties.  Section
4.4 shows that, for the explicit function (3.6), the cutoff may additionally be
chosen toroidally radial and transverse to its Killing-null locus.  Define

\[
Q^2(t,\rho,z)=(1-\chi)\rho^2+\chi R^2[1+b(t)]
\tag{4.1}
\]

and

\[
ds^2=-(dt-R\chi\,d\phi)^2
     +Q^2d\phi^2+d\rho^2+dz^2.
\tag{4.2}
\]

We retain the time orientation determined by the everywhere timelike field
\(\partial_t\).
Because \(\chi\) vanishes on a neighborhood of the axis, every term containing
\(d\phi\) is smooth there.  Off the axis, \(Q^2>0\) follows from \(b>-1\),
and the determinant of the \((t,\phi)\) block is \(-Q^2\).  Thus (4.2) is
a smooth Lorentzian metric.  Outside one fixed spatially compact set it is
exactly

\[
ds^2=-dt^2+d\rho^2+\rho^2d\phi^2+dz^2.
\tag{4.3}
\]

It is therefore exactly Minkowskian outside the spatially compact timelike
worldtube \(\mathbb R_t\times\operatorname{supp}\chi\), and in particular has
the standard asymptotically flat end and null infinity.

### 4.1 Distinct full chronology classes

The axial Killing norm is

\[
B:=g_{\phi\phi}
=(1-\chi)(\rho^2+R^2\chi)+R^2\chi b(t).
\tag{4.4}
\]

The one-way property can be checked without relying on coordinates becoming
singular at the axis.  Off the axis, introduce the orthonormal coframe

\[
\vartheta^0=dt-R\chi\,d\phi,
\qquad
\vartheta^1=Q\,d\phi.
\tag{4.5}
\]

For a nonzero future causal vector \(V\),
\(\vartheta^0(V)>0\) and
\(\lvert\vartheta^1(V)\rvert\leq\vartheta^0(V)\).  Since

\[
dt(V)=\vartheta^0(V)+\frac{R\chi}{Q}\vartheta^1(V),
\qquad
B=Q^2-(R\chi)^2,
\tag{4.6}
\]

the condition \(B\geq0\) implies \(dt(V)\geq0\).  Equality is possible only when
\(B=0\), the transverse components vanish, and \(V\) is tangent to the null
axial direction.  The axis is ordinary Minkowski space and is treated
separately.

On the toroidal core, \(B=R^2b\), so the axial circles are timelike when
\(b<0\).  Whenever \(b>0\), \(B>0\) away from the harmless cylindrical axis and

\[
g^{-1}(dt,dt)=-\frac{B}{Q^2}<0.
\tag{4.7}
\]

The axis itself is Minkowskian.  Hence every positive-\(b\) band is a global
temporal slab.  The full chronology set may extend beyond the core during a
negative band, but it cannot enter a positive band or join classes lying on
opposite sides of one.  The safe global statement is

\[
\{b<0,\ \chi=1\}\subseteq\mathcal C\subseteq\{b<0\}.
\tag{4.8}
\]

The central core curve therefore encounters infinitely many distinct classes
of the full spacetime, not merely sign changes of a local Killing norm.

### 4.2 Entry, transit, and exit

At a fixed point of the core, \(\partial_t\) is again a unit timelike geodesic.
An observer can also enter from and return to the flat exterior.  Along a curve
with \(d\phi=dz=0\),

\[
ds^2=-dt^2+d\rho^2.
\tag{4.9}
\]

Choose a smooth radial profile with 

\[
\left|\frac{d\rho}{dt}\right|<1.
\tag{4.10}
\]

The resulting timelike curve may enter before the Zeno stack, remain in the
core while it crosses all late chronology classes, and leave after \(t=0\).
This is an open kinematic observer history, not a closed material loop.  Its
state is not required to reset merely by single-valuedness.

### 4.3 Absence of a black-hole event horizon

From every event, the outward radial curve

\[
t=t_0+s,
\qquad
\rho=\rho_0+s,
\qquad
\phi=\phi_0,
\qquad
z=z_0
\tag{4.11}
\]

is future null away from the coordinate axis; at the axis one chooses any
outward Cartesian radial direction.  After leaving the support of \(\chi\), it
becomes an ordinary Minkowski outgoing ray reaching \(\mathscr I^+\).  It need
not be geodesic in
the interior; causal reachability is sufficient.  Thus

\[
M\subseteq J^-(\mathscr I^+)
\tag{4.12}
\]

and the black-hole event horizon is empty relative to the standard conformal
completion of the exactly Minkowskian end.

Equations (4.2)--(4.12) give a positive kinematic answer to the motivating
question: an accessible, spatially localized chronology stack can coexist with
an ordinary asymptotic end and a regular exterior-to-exterior timelike transit.
The qualification is essential.  The metric is prescribed and solves
Einstein’s equation only with the conserved effective source

\[
T_{ab}=\frac{1}{8\pi}G_{ab}.
\tag{4.13}
\]

No conventional matter model realizing that source has been supplied.

### 4.4 The cutoff rim: regularity and axial transversality

The equality \(B=g_{\phi\phi}=0\) makes the axial Killing field null, but in the
transition region it does not by itself define a null hypersurface or a family
of null generators.  Put

\[
\alpha=R\chi,
\qquad x^A=(\rho,z),
\qquad K=\partial_\phi,
\qquad \mathcal Z=\{B=0,\ 0<\chi<1\}.
\]

On \(\mathcal Z\), equation (4.4) gives

\[
b(t)=-\frac{(1-\chi)(\rho^2+R^2\chi)}{R^2\chi}<0.
\tag{4.14}
\]

Thus the transition Killing-null locus occurs only inside a negative-\(b\)
band, not on the temporal slabs that separate the chronology classes.

**Proposition 4.1 (transition-rim diagnostic).**  At a point of \(\mathcal Z\),
the metric is smooth and nondegenerate, with \(Q^2=\alpha^2>0\).  Moreover,

\[
g^{-1}(dB,dB)=B_\rho^2+B_z^2.
\tag{4.15}
\]

Consequently a regular portion of \(\mathcal Z\) is generically timelike.  It
can be null only at a transverse critical point \(B_A=0\), with \(B_t\ne0\).
On \(\mathcal Z\),

\[
\nabla_KK
=-\frac{B_t}{2\alpha}K-\frac12B_A\partial_A.
\tag{4.16}
\]

The closed null \(K\)-orbit is therefore a null pregeodesic if and only if
\(B_A=0\).  Its non-affinity at such an orbit is

\[
\kappa=-\frac{B_t}{2\alpha}=-\frac R2 b'(t).
\tag{4.17}
\]

With the Riemann-sign convention specified in Appendix B, a parallel screen
\(E_A\) along a critical orbit satisfies

\[
R(K,E_A,K,E_B)=-\frac12B_{AB}.
\tag{4.18}
\]

If \(\kappa\ne0\), the closed orbit is affine incomplete in one direction.  For
its affine tangent \(k=fK\), one has

\[
R(k,E_A,k,E_B)=-\frac12f^2B_{AB},
\qquad
|f|\asymp|\lambda-\lambda_*|^{-1}.
\tag{4.19}
\]

Hence a nonzero transverse Hessian produces a genuine parallel-propagated
curvature divergence of order \(|\lambda-\lambda_*|^{-2}\), although scalar
invariants remain finite.  If \(\kappa=0\), the closed orbit itself is complete;
the two-dimensional companion recurrent ray is not automatically a
four-dimensional geodesic in the transition region.

Appendix B proves the proposition and records the full, not-yet-specialized
optical tidal matrix.  At a generic point with \(B_A\ne0\), the closed null
orbit is nongeodesic.  The push-up lemma then places it inside the
chronology-violating set.  Thus generic portions of \(\mathcal Z\) are not the
chronology boundary; \(B=0\) is only the boundary of the manifest axial-timelike
set \(B<0\).

The additional transversality condition

\[
\nabla_\perp B\ne0
\quad\hbox{on}\quad
\mathcal Z
\tag{4.20}
\]

would exclude this particular axial-geodesic PP mechanism.  The present
construction can in fact be made to satisfy it.

**Proposition 4.2 (transverse toroidal cutoff).**  For the function \(b(t)\) in
(3.6), there exists a smooth compactly supported cutoff of the form

\[
s=\sqrt{(\rho-R)^2+z^2},
\qquad
\chi(\rho,z)=h(s),
\tag{4.21}
\]

equal to one on an inner toroidal core and zero outside a slightly larger solid
torus, which satisfies (4.20) at every point of \(\mathcal Z\).

Appendix B constructs such an \(h\) by scaling a standard flat step across a
sufficiently narrow annulus.  We henceforth choose \(\chi\) from this class.
Then \(\mathcal Z\) is a smooth timelike hypersurface, all of its closed null
axial orbits are nongeodesic, and the push-up lemma gives
\(\mathcal Z\subset\mathcal C\).  In particular, the axial PP-divergence
mechanism in (4.19) is absent from the chosen localization.  Proposition 4.2
controls only the periodic axial orbits; it neither classifies non-axial
transition-region null geodesics nor proves bounded PP curvature along them.
The explicit recurrent rays used below remain in the open \(\chi=1\) product
core, where \(B_A=B_{AB}=0\).

## 5. The price of the construction

The timelike transit is smooth, accessible, and curvature-regular, but the
spacetime is neither energy-condition respecting nor null complete.  These are
separate statements and should not be compressed into the ambiguous word
“singular.”

### 5.1 An exact null-energy obstruction in the core

For the product metric (3.1), decompose a four-dimensional null vector as
\(k=v+w\), where \(v\) is tangent to the \((t,\psi)\) cylinder and \(w\) is
transverse.  The two-dimensional Ricci tensor is

\[
\operatorname{Ric}^{(2)}=\frac{a''}{a}g^{(2)},
\]

and nullity gives

\[
\operatorname{Ric}(k,k)=-\frac{a''}{a}|w|^2.
\tag{5.1}
\]

**Proposition 5.1.**  In the direct-product circular core, null convergence is
equivalent to

\[
a''\le0.
\tag{5.2}
\]

It therefore forbids every bounded component of \(b<0\).

**Proof.**  Condition (5.1) for all null \(k\) is exactly (5.2), so \(a\) must
be concave.  If a negative band is bounded by \(t_-\) and \(t_+\), then

\[
a(t_-)=a(t_+)=1,
\qquad
a(t)<1\quad(t_-<t<t_+).
\tag{5.3}
\]

A concave function lies above the chord joining equal endpoint values and would
have to satisfy \(a\geq1\), a contradiction.  \(\square\)

Thus NEC is violated at least somewhere in every bounded negative component of
the Zeno stack.  The violation occurs in the open \(\chi=1\) core, where all
derivatives of the cutoff vanish, so it cannot be assigned solely to the
localization region.  In the parallel frame (3.10),

\[
T_{\hat a\hat b}=\operatorname{diag}(0,0,p,p),
\qquad
p=-\frac{a''}{8\pi a}.
\tag{5.4}
\]

The dominant energy condition forces \(p=0\) in this ansatz.  These statements
are exact but ansatz-specific: transverse curvature or a nonsymmetric
chronology mechanism can change (5.1).

### 5.2 A regular null channel and an incomplete recurrent channel

The local mechanism is clearest in the general circular metric

\[
g_2=-A(t)dt^2+2C(t)dt\,d\phi+B(t)d\phi^2,
\qquad
\phi\sim\phi+P,
\tag{5.5}
\]

with \(C^2\) coefficients and

\[
\Delta=C^2+AB>0.
\]

Assume that \(B(0)=0\), that \(K=\partial_\phi\) does not vanish, and that the
zero is isolated on one side.  Lorentz signature gives \(C(0)\neq0\).

**Proposition 5.2.**  One null family crosses \(B=0\) regularly.  Every
geodesic in the companion family with nonzero Killing momentum \(L\), directed
toward the zero, approaches \(t=0\) in finite affine parameter while winding
infinitely around the circle.  It therefore reaches no endpoint on the
\(t=0\) hypersurface and is affinely incomplete.

The essential identities are

\[
L=C\dot t+B\dot\phi,
\qquad
L^2=\Delta\dot t^2,
\tag{5.6}
\]

and, on the recurrent branch,

\[
\frac{d\phi}{dt}\sim-\frac{2C(0)}{B(t)}.
\tag{5.7}
\]

For \(L\neq0\), equation (5.6) puts \(t=0\) at finite affine distance.  Since a
\(C^1\) function vanishing at zero obeys
\(\lvert B(t)\rvert\leq M\lvert t\rvert\), the angular integral in (5.7)
diverges.  On the chosen one-sided interval its sign is fixed, so
\((\phi\bmod P)\) has no limit.  Appendix C supplies the normal form and detailed
asymptotics.

The null generator on \(B=0\) obeys

\[
\nabla_KK=\kappa K,
\qquad
\kappa=-\frac{B'(0)}{2C(0)}.
\tag{5.8}
\]

For \(B'(0)\neq0\), repeated circuits give the usual exponential
Hawking--Misner monodromy.  For \(B'(0)=0\), the closed generator itself is
affinely complete, but Proposition 5.2 still makes its companion branch
incomplete.  If \(B(t)=b_mt^m+o(t^m)\) with odd \(m>1\), the \(q\)-th late
circuit has

\[
|t_q|\asymp q^{-1/(m-1)},
\qquad
\ell_q\asymp q^{-m/(m-1)},
\qquad
\bar\omega_q\asymp q^{m/(m-1)}.
\tag{5.9}
\]

The cubic zeros in (3.6) give \(\ell_q\asymp q^{-3/2}\) and
\(\bar\omega_q\asymp q^{3/2}\).  Smooth flattening replaces an
exponential sequence by a polynomial or stronger one; it does not restore
affine completeness.

For the exact core, let \(u=\partial_t\) and
\(E=-g(u,\dot\gamma)\).  The two measured frequencies are

\[
E_{\mathrm{reg}}=\frac{L}{1+a},
\qquad
E_{\mathrm{rec}}=\frac{L}{1-a}.
\tag{5.10}
\]

The regular family crosses every boundary with
\(E_{\mathrm{reg}}\to L/2\).  The recurrent family has
\(E_{\mathrm{rec}}\sim-2L/b\), winds at one fixed boundary, and never proceeds
to the next one.  It is therefore incorrect to multiply one-circuit gains over
all boundaries as if one geodesic experienced both the cross-stack and
within-boundary repetitions.  The same two families remain exact geodesics in
the open \(\chi=1\) core of (4.2).  The full localized spacetime is consequently
null incomplete even though the selected timelike observer crosses the entire
stack smoothly and parallel-propagated curvature stays bounded along these
exact product-core incomplete rays.  Propositions 4.1 and 4.2 show that the
chosen transition-rim axial null orbits are nongeodesic.  The product-core
boundedness statement therefore does not extend by continuity to a second
axial geodesic family in the cutoff; non-axial transition dynamics remain a
separate question.

The resulting bounded-curvature incompleteness is quasiregular in character.
Slobodov (2008) studies a complementary global operation: unwrapping
CTC-producing identifications can trade chronology violation for naked
quasiregular singularities.  No such unwrapping is performed here.

The local ribbon mechanism itself is established prior art, particularly in
Sánchez (1997), Bavard and Mounoud (2020), Mehidi (2022), Petersen (2021), and
Rieger (2026).  Its role here is to identify precisely which null sector pays
for the regular timelike Zeno transit.

### 5.3 Why the construction is nonanalytic

The flat oscillation in (3.6) is structural rather than decorative.  Let an
analytic Lorentzian spacetime admit an analytic isometric action of a torus
\(T^k\).  At \(p\), let

\[
\mathsf B_p(\xi,\eta)=g_p(K_\xi,K_\eta)
\tag{5.11}
\]

be the Gram form on the torus Lie algebra, and let \(\mathcal C_T\) denote the
set of points lying on a timelike orbit of some closed one-parameter subgroup.

**Proposition 5.3.**  The symmetry-generated set \(\mathcal C_T\) is
semianalytic and its connected components form a locally finite family.  Along
an analytically extendible geodesic, the inverse image of \(\mathcal C_T\) has
only finitely many components on each compact parameter interval.

Indeed, density of rational lattice directions gives

\[
\mathcal C_T
=\{p:\mathsf B_p\text{ is not positive semidefinite}\}
=\bigcup_{\varnothing\ne I}\{\Delta_I<0\},
\tag{5.12}
\]

where the finitely many principal minors \(\Delta_I\) are analytic.  Standard
semianalytic structure theory then gives local finiteness.  Appendix D records
the details.

The caveat is decisive:

\[
\mathcal C_T\subseteq\mathcal C
\tag{5.13}
\]

may be strict.  Proposition 5.3 is not a theorem that all chronology classes of
an analytic spacetime are locally finite.  It applies to the full chronology
set only when a separate symmetry-exhaustion argument proves
\(\mathcal C=\mathcal C_T\).  In the core circular model (3.1), that equality is
available,
and the nonanalyticity of (3.6) is exactly how the stack evades the proposition.

## 6. Records and an exact chiral field filter

An open observer is not subject to periodic reset: its worldline does not
return to the same event.  That kinematic fact permits, but does not by itself
dynamically construct, a retained record.  Nor does it guarantee that arbitrary
radiation can pass smoothly through a chronology boundary.  In the circular
core, the boundary-crossing problem can be solved exactly for a massless
scalar.

### 6.1 Homogeneous fields

On one punctured side of a zero, use the canonical ribbon

\[
ds^2=2\,dT\,d\psi+B(T)d\psi^2,
\qquad
\psi\sim\psi+P,
\tag{6.1}
\]

and define

\[
H(T)=2\int^T\frac{dS}{B(S)},
\qquad
u=\psi,
\qquad
v=\psi+H(T).
\tag{6.2}
\]

Then

\[
ds^2=B\,du\,dv,
\qquad
\Box\Phi=\frac4B\,\partial_u\partial_v\Phi.
\tag{6.3}
\]

Locally, every homogeneous solution is

\[
\Phi=F(u)+G(v).
\tag{6.4}
\]

The cylinder quotient is diagonal:
\((u,v)\sim(u+P,v+P)\).  Single-valuedness permits opposite additive
monodromies of \(F\) and \(G\); their nonperiodic remainder is a zero mode
proportional to \(H(T)\), and regularity eliminates it.  After that removal,
take \(F\) and \(G\) periodic.  On a side on which the zero of \(B\) is
isolated, \(H(T)\) is monotone and unbounded.  It consequently winds through
every phase modulo \(P\), so a nonconstant \(G(v)\) has no continuous limit at
\(B=0\).
Moreover,

\[
\partial_T\Phi=\frac{2}{B}G'(v),
\tag{6.5}
\]

and hence the angularly averaged squared transverse derivative is

\[
\int_0^P|\partial_T\Phi|^2\,d\psi
=\frac4{B^2}\int_0^P|G'|^2\,d\psi.
\tag{6.6}
\]

**Proposition 6.1 (chiral filter).**  Continuous extension through the
chronology boundary removes the zero-mode monodromy and forces the recurrent
component \(G\) to be constant.  The regular component \(F(u)\) remains an
arbitrary periodic one-way signal across the boundary.  \(C^1\) or
finite-stress extension imposes the same conclusion a fortiori.

Thus smoothness does not erase every record.  It selects one characteristic
channel.

### 6.2 Compactly operated sources and compatibility moments

Expand

\[
\Phi=\sum_{n\in\mathbb Z}f_n(T)e^{ik_n\psi},
\qquad
J=\sum_{n\in\mathbb Z}J_n(T)e^{ik_n\psi},
\qquad
k_n=\frac{2\pi n}{P}.
\tag{6.7}
\]

For \(\Box\Phi=J\),

\[
(Bf_n')'-2ik_nf_n'=-J_n.
\tag{6.8}
\]

The recurrent amplitude

\[
\mathcal A_n=B e^{-ik_nH}f_n'
\tag{6.9}
\]

satisfies

\[
\mathcal A_n(T_b)-\mathcal A_n(T_a)
=-\int_{T_a}^{T_b}J_n(T)e^{-ik_nH(T)}\,dT.
\tag{6.10}
\]

Choose \(T_a<T_b\) on the same punctured band, with the source supported away
from \(B=0\) between them.  If no recurrent mode is present at \(T_a\), then
output which remains regular at the subsequent boundary requires
\(\mathcal A_n(T_b)=0\), and hence

\[
\int_{T_a}^{T_b}J_n(T)e^{-ik_nH(T)}\,dT=0\quad(n\ne0),
\qquad
\int_{T_a}^{T_b}J_0(T)\,dT=0.
\tag{6.11}
\]

These are compatibility conditions, not an impossibility theorem.  Their
kernel is infinite-dimensional; for instance
\(J_n=e^{ik_nH}q_n'\), with \(q_n\) compactly supported away from the zero,
satisfies the \(n\)-th condition.  Conjugate modes may be paired to obtain a
real source.  A direct regular-only emitter is obtained by
putting

\[
\tau=\frac{v-u}{2}=\frac{H(T)}2,
\qquad
\Phi=q(\tau)F(u),
\tag{6.12}
\]

where \(q\) changes smoothly from zero to one over a compact interval in
\(\tau\) whose preimage lies away from the boundary.  Then

\[
J=\Box\Phi
=\frac{-q''(\tau)F(u)+2q'(\tau)F'(u)}{B(T)}
\tag{6.13}
\]

is smooth and compactly supported in the transition, while the post-source
field is the nonzero regular signal \(F(u)\) with no recurrent component.

Equations (6.8)--(6.13) are a one-boundary, bandwise statement.  They do not
assume a global retarded Green operator on the non-globally-hyperbolic stack.
Friedman and Morris (1997) show that existence and uniqueness for massless
fields on asymptotically flat CTC spacetimes depend on the global geometry;
either property can fail in smooth examples with a compact nonchronal region.

### 6.3 Maxwell embedding and its limitation

In the product core, set

\[
A=\alpha(T,\psi)\,dx.
\tag{6.14}
\]

Lorenz gauge is automatic, \(F=d\alpha\wedge dx\), and the \(x\)-component of
Maxwell's equation is
\(\nabla_bF^{bx}=\Box\alpha=4\pi J^x\).  The current
\(J^a=\delta^a_xJ^x(T,\psi)\) is automatically conserved and obeys the same
compatibility conditions, up to the immaterial factor \(4\pi\).

This is not yet a finite warm body.  The mode is transversely uniform and has
infinite transverse extent.  It proves that nontrivial classical communication
through the regular channel is possible in the exact product geometry; it does
not prove that a compact radiating source can avoid the recurrent sector.

### 6.4 A finite exit state

The infinite number of chronology classes does not by itself supply infinite
operational information.  Let a detector state \(X(\tau)\) take values in a
complete metric space and be absolutely continuous with metric derivative

\[
|\dot X|(\tau)\le h(\tau),
\qquad
\int_{\tau_0}^{\tau_*}h(\tau)\,d\tau<\infty.
\tag{6.15}
\]

Then \(X(\tau)\) is Cauchy as \(\tau\to\tau_*\), has a unique exit limit, and

\[
\operatorname{Var}(X)
\le\int_{\tau_0}^{\tau_*}h(\tau)\,d\tau.
\tag{6.16}
\]

If every reliably distinguishable successive update requires state-space
displacement at least \(\epsilon>0\), their number obeys

\[
N_\epsilon
\le\frac1\epsilon
\int_{\tau_0}^{\tau_*}h(\tau)\,d\tau.
\tag{6.17}
\]

Infinitely many nonzero updates may still converge to one finite aggregate
record.  What regularity excludes is an infinite sequence of uniformly
distinguishable records produced by integrably bounded local dynamics.  This is
an elementary supporting lemma, not the geometric source of the obstruction.

## 7. Discussion and outlook

### 7.1 What the results answer

The motivating questions now have qualified answers.

**Can one visit and exit?**  Yes at the level of exact Lorentzian geometry.
Metric (4.2) admits an exterior-to-core-to-exterior timelike transit through
infinitely many distinct chronology classes, and no black-hole event horizon
blocks causal access to \(\mathscr I^+\).

**Must the traveler's memory reset?**  No kinematic periodicity condition
requires it: the observer's history is open.  Under integrably bounded detector
dynamics it has a well-defined, potentially nonzero exit state.  The exact
scalar/Maxwell sector also has a nontrivial regular channel across the local
chronology boundary.  It does not by itself construct radiation from a compact
source that subsequently reaches \(\mathscr I^+\).  In the bandwise model,
unrestricted excitation of both characteristic sectors is incompatible with a
smooth prescribed boundary.

**What is the cost?**  In the explicit model the established cost is threefold:
nonanalyticity, NEC violation somewhere in every bounded chronology band, and
an incomplete recurrent product-core null sector with infinite winding but
bounded parallel-propagated curvature along those exact rays.  Proposition 4.1
identifies a possible axial PP-divergence mechanism at a transverse critical
orbit, while Proposition 4.2 shows that the cutoff used here may be chosen to
contain no such orbit.  This removes that axial mechanism, not every possible
transition-region null pathology.  In a hypothetical smooth full-backreaction
solution satisfying global NEC, the strict inequality
\(T_{ab}k^ak^b>0\) for every nonzero null \(k\) at the actual accumulation event
would force the boundary line itself to be incomplete.

Appendix C sharpens the recurrent-sector cost into a gain--compression
relation: the measured frequency grows at the reciprocal rate to the shrinking
affine lapse per circuit.  This is the same broad boost-amplification pattern
that can turn finite coordinate or scalar data into a divergent
parallel-propagated observable.  In the present product core, however, the
non-scalar check (B.9) stays bounded; amplification appears in the recurrent
frequency and affine compression, not in a hidden tidal-curvature divergence.
The transition-region calculation separates this product statement from the
selected cutoff rim, which is smooth, timelike, and foliated by nongeodesic
closed null axial orbits.  Non-axial transition geodesics have not been
classified.

These conclusions concern chronology boundaries, not automatically Cauchy
horizons.  Hawking's compact-generation argument, Minguzzi's horizon rigidity,
and the Kay--Radzikowski--Wald semiclassical obstruction remain important
neighboring results, but none is assumed in Theorem 2.3.

### 7.2 What is not established

The paper does not provide:

- a conventional Einstein--matter model producing (4.2);
- a smooth, finite, self-gravitating warm worldtube that realizes the transit;
- null completeness or a curvature-singularity-free spacetime;
- a classification of non-axial transition-region null geodesics and their
  parallel-propagated curvature;
- operational reusability of the chronology region;
- a global Cauchy problem for fields on the entire stack; or
- a theorem that every finite radiating source excites the recurrent channel.

The exact source \(G_{ab}/8\pi\) is conserved but exotic.  Calling it "matter"
does not solve a constitutive field equation.  Likewise, a timelike geodesic in
a prescribed geometry is not a warm observer until its stress and radiation
are included in the coupled solution.

### 7.3 The finite-body scattering problem

For frozen \(B>0\), an exact one-sheet condition involves the transverse
operator

\[
\sqrt{k_\psi^2-B\Delta_\perp}.
\tag{7.1}
\]

For fixed \(k_\psi\ne0\), a Paley--Wiener branch-point argument rules out
simultaneous compact support of a nonzero datum \(f\) and
\(\sqrt{k_\psi^2-B\Delta_\perp}f\), subject to the usual smooth compact-support
hypotheses.  At \(k_\psi=0\), the corresponding statement is the anti-locality
of \(|D_\perp|\), closely related to the fractional-Laplacian unique-continuation
theorem of Ghosh, Salo, and Uhlmann (2020).  The massless \(1+1\) chiral sector
is exceptional because its one-way condition is local.

This frozen statement is only motivation.  Regularity at the Zeno boundary
defines a time-dependent Jost or scattering map, not the instantaneous
square-root operator.  The main field-theory problem is therefore:

> Does the exact time-dependent regular-channel scattering map have a
> support-uniqueness property which, under specified no-incoming and
> finite-energy conditions, forbids a nonzero transversely compact source with
> nonzero free output from exciting only the regular channel?

The zero circular mode, continuous emission extending to the boundary, Maxwell
constraints, and the toroidal matching region must all be treated separately.
Words such as “generic” or “thermal” should be used only after specifying a
topology, probability law, or constitutive current model.

### 7.4 Two next upgrades

The most valuable geometric upgrade is a specified Einstein--matter
realization, or a no-go theorem showing that the causal boundary conditions and
a chosen matter model are incompatible.  The most direct operational upgrade
is the finite-body scattering theorem just stated, followed by controlled
backreaction.

The novelty claim should remain narrow.  The two-dimensional ribbon mechanism,
compact-horizon focusing, self-consistency of closed histories, and localized
test-particle time machines are established subjects.  The candidate
contribution is their combination with the distinct-class accumulation theorem,
the explicit horizonless asymptotically flat Zeno transit, and the
regular/recurrent channel separation.  A final submission should include
forward and backward citation
searches from Minguzzi (2008, 2016), Kriele (1989), Sánchez (1997), and the
Lorentzian-surface literature before claiming priority.

## 8. Conclusion

Chronology-class accumulation has an unavoidable null causal skeleton.  If
infinitely many pairwise distinct chronology classes accumulate at an interior
event, a lightlike line lies in the chronology boundary through that event.
Focusing makes this line incomplete under null convergence and genericity.
Together with global null convergence, strict null convergence in every null
direction at the accumulation event gives a local matter version of the same
result.

Nevertheless, a smooth timelike observer can cross such an accumulation and
reach an ordinary asymptotic future.  The explicit model demonstrates that
regular timelike passage, bounded curvature along the traveler, causal access
to infinity, a nontrivial local boundary-crossing field channel, and the
absence of a black-hole event horizon are mutually compatible.  They are not
compatible here with acceptable energy conditions or null completeness.  The
right conclusion is therefore neither "memory must reset" nor "a
singularity-free time machine exists."  It is a sharper dichotomy: an open
observer may leave with a convergent, nonzero record under bounded detector
dynamics, while the geometry pays through exotic stress, nongeneric null
rigidity, or affine incompleteness.

---

## Appendix A. Limit-curve details for Theorem 2.3

Choose a complete auxiliary Riemannian metric \(h\).  For each \(n\), select a
smooth closed future timelike curve through \(p_n\), parametrize it by
\(h\)-arclength, and denote its length by \(\ell_n\).  Its image lies in
\(\mathcal C_n\), because every two points on one closed timelike curve are
mutually chronologically related.

The loops have a uniform positive length bound.  Choose relatively compact
coordinate neighborhoods

\[
p\in W\Subset V\Subset U
\tag{A.1}
\]

such that \(U\) admits a local temporal coordinate, and take \(n\) large enough
that \(p_n\in W\).  No closed causal curve can remain in \(U\).  Every selected
loop must therefore leave \(U\), and in particular cross from \(W\) through
\(M\setminus V\) and return.  Since

\[
\delta=d_h(\overline W,M\setminus V)>0,
\]

we have \(\ell_n\ge2\delta\).

Pass to a subsequence, relabeling all indexed objects by \(n\), for which

\[
\ell_n\longrightarrow\ell\in(0,\infty].
\tag{A.2}
\]

Every further subsequence used below is relabeled in the same way.

Minguzzi’s coalescing-endpoint limit-curve theorem (2008, Theorem 3.1(2))
applies.

- If \(\ell<\infty\), the loops converge, after a further subsequence, to a
  nonconstant closed continuous causal curve through \(p\).
- If \(\ell=\infty\), the theorem supplies a past-inextendible causal half-curve
  ending at \(p\) and a future-inextendible causal half-curve starting there.
  Their concatenation is a two-sided inextendible continuous causal limit
  curve.

For the simultaneous-approximant property, use the usual diagonal realization
of the theorem: periodically extend each loop to a future causal map
\(\widetilde\sigma_n:\mathbb R\to M\) with
\(\widetilde\sigma_n(0)=p_n\).  On every compact parameter interval its image
lies in a compact \(h\)-ball, by completeness of \(h\), and a diagonal
Arzelà--Ascoli argument gives uniform convergence on compact sets.  Local
collapse to a constant is excluded by the temporal coordinate.  Orient it to
increase on future causal curves.  Compactness of \(\overline V\) gives
\(c>0\) such that

\[
dT(v)\ge c|v|_h
\tag{A.3}
\]

for every future causal vector \(v\) based in \(\overline V\).  For
\(0<s<\delta\), the initial segment of every sufficiently late loop remains in
\(V\), and hence
\(T(\widetilde\sigma_n(s))-T(p_n)\ge cs\).  This is the local anti-collapse
estimate behind the standard limit-curve theorem.

Uniform-on-compact convergence along this relabeled subsequence gives
simultaneous approximants: for any finite collection \(q^1,\ldots,q^r\) on the
limit curve, points
\(q_n^j\in\mathcal C_n\) can be chosen with \(q_n^j\to q^j\).  The mixed-index
chain (2.4) then proves achronality.

In the finite-\(\ell\) branch, the closed achronal causal limit is a null
pregeodesic.  It cannot have a corner at the closing event, since smoothing a
causal corner would produce timelike-related points and violate achronality.
Its periodic extension is consequently a two-sided lightlike line in the sense
used by Minguzzi (2008, Theorem 2.16).  It need not be affine complete: a return
map may rescale the tangent after each circuit.

For any fixed point \(q\) on the limit line, approximants
\(q_n\in\mathcal C_n\) show \(q\in\overline{\mathcal C}\).  If
\(q\in\mathcal C\), its open chronology class would contain all sufficiently
late \(q_n\), contradicting pairwise distinctness.  Thus the whole line lies in
\(\partial\mathcal C\).  If strong causality held at any point of the line, its
open strong-causality locus would contain all sufficiently late approximants,
which is impossible because each approximant lies on a closed timelike curve.

## Appendix B. Core and transition-rim geometry and effective stress tensor

For the \((t,\psi)\) block of (3.1),

\[
g_{(2)}=
\begin{pmatrix}-1&1\\[2pt]1&b\end{pmatrix},
\qquad
g_{(2)}^{-1}=\frac1{1+b}
\begin{pmatrix}-b&1\\[2pt]1&1\end{pmatrix}.
\tag{B.1}
\]

The independent nonzero Christoffel symbols are

\[
\Gamma^t{}_{t\psi}=\frac{b'}{2(1+b)},
\qquad
\Gamma^t{}_{\psi\psi}=\frac{bb'}{2(1+b)},
\]

\[
\Gamma^\psi{}_{t\psi}=\frac{b'}{2(1+b)},
\qquad
\Gamma^\psi{}_{\psi\psi}=-\frac{b'}{2(1+b)}.
\tag{B.2}
\]

These immediately give

\[
R=\frac{2(1+b)b''-(b')^2}{2(1+b)^2}.
\tag{B.3}
\]

Since \(a=\sqrt{1+b}\),

\[
\frac{a''}{a}
=\frac{2(1+b)b''-(b')^2}{4(1+b)^2},
\tag{B.4}
\]

and therefore \(R=2a''/a\).  The two-dimensional identity
\(\operatorname{Ric}^{(2)}=(R/2)g^{(2)}\) gives

\[
\operatorname{Ric}^{(2)}=\frac{a''}{a}g^{(2)}.
\tag{B.5}
\]

Taking the direct product with a flat transverse plane leaves the cylinder
Ricci tensor unchanged.  The Einstein tensor vanishes on the \((t,\psi)\) block
and obeys

\[
G_{xx}=G_{yy}=-\frac{a''}{a}.
\tag{B.6}
\]

Direct substitution of (B.2) verifies

\[
\nabla_{\partial_t}e_{\hat a}=0
\]

for every vector in the frame (3.10).  In that frame the effective Einstein
source is

\[
T_{\hat a\hat b}
=\operatorname{diag}\!\left(0,0,-\frac{a''}{8\pi a},
-\frac{a''}{8\pi a}\right).
\tag{B.7}
\]

To obtain the null-convergence test, let \(k=v+w\) be null, with \(v\) tangent
to the cylinder and \(w\) transverse.  Then
\(g^{(2)}(v,v)=-\lvert w\rvert^2\), so (B.5) gives

\[
\operatorname{Ric}(k,k)
=-\frac{a''}{a}|w|^2.
\tag{B.8}
\]

This proves (5.1)--(5.4).  It also shows why purely two-dimensional null vectors
saturate the NEC while transverse null directions detect its violation.

There is also a direct non-scalar curvature check on the recurrent rays.  Along
an affinely parametrized null geodesic tangent to the cylinder, choose the
parallel null frame \(k,n,e_{\hat2},e_{\hat3}\), where
\(g(k,n)=-1\) and the last two vectors are the constant transverse directions.
The product structure and the two-dimensional curvature identity give

\[
R(k,n,k,n)=-\frac R2,
\tag{B.9}
\]

with all mixed transverse components zero.  Thus bounded scalar curvature is
enough to give bounded parallel-propagated curvature for these particular
product-core rays.  This conclusion is not automatic in a general spacetime:
unbounded boosts can reveal parallel-propagated divergences even when scalar
polynomial invariants remain finite.

For the localized metric (4.2), the determinant of the \((t,\phi)\) block is
\(-Q^2\).  Smoothness at the axis follows because \(\chi\) vanishes identically
on a neighborhood there, leaving the standard polar combination
\(d\rho^2+\rho^2d\phi^2\).  On the open toroidal core, \(\chi=1\) and all of its
derivatives vanish, so the preceding product calculation applies after the
constant rescaling \(\psi=R\phi\).

### Transition-rim calculation

For Proposition 4.1, write \(\alpha=R\chi\), \(x^A=(\rho,z)\), and
\(e_A=\partial_A\).  The nontrivial block and its inverse are

\[
g_{(t,\phi)}=
\begin{pmatrix}-1&\alpha\\[2pt]\alpha&B\end{pmatrix},
\qquad
g_{(t,\phi)}^{-1}=\frac1{Q^2}
\begin{pmatrix}-B&\alpha\\[2pt]\alpha&1\end{pmatrix},
\qquad Q^2=\alpha^2+B.
\tag{B.10}
\]

At \(B=0\) in the transition, \(Q^2=\alpha^2>0\), so this is an ordinary
interior locus of a smooth Lorentzian metric.  Because \(B\) is independent of
\(\phi\), equation (B.10) gives

\[
g^{-1}(dB,dB)\big|_{B=0}=B_A B_A.
\tag{B.11}
\]

Furthermore,

\[
\nabla B\big|_{B=0}=\frac{B_t}{\alpha}K+B_Ae_A,
\qquad
\nabla_KK=-\frac12\nabla(K^2)
=-\frac{B_t}{2\alpha}K-\frac12B_Ae_A.
\tag{B.12}
\]

This proves the causal-character and pregeodesic statements in Proposition
4.1.  Notice in particular that freezing \((\rho,z)\) gives a geodesic
two-dimensional ribbon only when the transverse force \(B_A\) vanishes.

Use the curvature convention

\[
R^a{}_{bcd}
=\partial_c\Gamma^a{}_{bd}-\partial_d\Gamma^a{}_{bc}
+\Gamma^a{}_{ce}\Gamma^e{}_{bd}-\Gamma^a{}_{de}\Gamma^e{}_{bc}.
\]

A direct connection calculation, with no field equation imposed, gives the
exact transition-rim optical tidal matrix

\[
R(K,e_A,K,e_B)\big|_{B=0}
=-\frac12B_{AB}
+\frac{\alpha_A B_B+\alpha_B B_A}{4\alpha}
+\frac{B_A B_B}{4\alpha^2}.
\tag{B.13}
\]

At a geodesic \(K\)-orbit, \(B_A=0\), this reduces to (4.18).  This is a
parallel-propagated statement, not merely a coordinate component: at
\(B=B_A=0\),

\[
\nabla_Ke_A=\frac{\alpha_A}{2\alpha}K.
\tag{B.14}
\]

Functions \(c_A(\phi)\) can therefore be chosen so that
\(E_A=e_A+c_AK\) is parallel along the affine lift of the orbit.  Adding a
multiple of \(K\) to a screen vector does not change
\(R(K,E_A,K,E_B)\).  Equivalently, for the normalized null direction
\(\ell=-K/(\sqrt2\alpha)\),

\[
R(\ell,E_A,\ell,E_B)=-\frac{B_{AB}}{4\alpha^2}.
\tag{B.15}
\]

If \(k=fK\) is affine, then

\[
\frac{df}{d\phi}+\kappa f=0,
\qquad
\kappa=-\frac{B_t}{2\alpha}=-\frac R2b'(t).
\tag{B.16}
\]

For \(\kappa\ne0\), repeated circuits put one direction of the orbit at finite
affine distance and give
\(f\asymp|\lambda-\lambda_*|^{-1}\).  Combining (B.13)--(B.16) proves
(4.19).  The metric and its scalar invariants stay smooth because every circuit
returns to the same regular manifold point; the divergence is produced by the
unbounded affine-frame boost.

For checking a specified cutoff, it is useful to set

\[
D=R^2(1+b)-\rho^2-2R^2\chi.
\]

Direct differentiation of (4.4) gives

\[
B_\rho=2\rho(1-\chi)+D\chi_\rho,
\qquad
B_z=D\chi_z,
\tag{B.17}
\]

and

\[
B_{AB}
=2(1-\chi)\delta_A^\rho\delta_B^\rho
-2\rho\bigl(\delta_A^\rho\chi_B+\delta_B^\rho\chi_A\bigr)
-2R^2\chi_A\chi_B+D\chi_{AB}.
\tag{B.18}
\]

On the positive-\(\chi\) root of \(B=0\), one has
\(D=-\rho^2/\chi-R^2\chi<0\).  Equations (B.17)--(B.18) make both the
transversality condition and the conditional PP divergence checkable for any
explicit cutoff.  We now use them to prove Proposition 4.2.

Write \(x=-1/t\) for \(t<0\).  If the function (3.6) is negative, then
\(\sin x<0\), hence \(x>\pi\), and

\[
0<-b(t)\leq\beta_0:=\varepsilon e^{-\pi^2}.
\tag{B.19}
\]

Let \(F\) be the standard flat increasing step

\[
F(u)=
\begin{cases}
0,&u\leq0,\\[2pt]
\displaystyle
\frac{e^{-1/u}}{e^{-1/u}+e^{-1/(1-u)}},&0<u<1,\\[8pt]
1,&u\geq1.
\end{cases}
\tag{B.20}
\]

Set

\[
\delta=\beta_0<1,
\qquad
u_\delta=F^{-1}(\delta),
\qquad
m_\delta=\inf_{0<u\leq u_\delta}\frac{F'(u)}{F(u)}>0.
\tag{B.21}
\]

The final inequality follows because \(F'/F\) is positive and continuous on
\((0,u_\delta]\), and tends to \(+\infty\) as \(u\downarrow0\).  Choose

\[
0<w<\min\{R/2,Rm_\delta\},
\qquad
s_1=R/2,
\qquad
s_0=s_1-w,
\qquad
h(s)=1-F\!\left(\frac{s-s_0}{w}\right).
\tag{B.22}
\]

Then \(h=1\) for \(s\leq s_0\), \(h=0\) for \(s\geq s_1\), and \(h'<0\)
throughout the open wall.  Its rotated support is a compact solid torus with
\(\rho\geq R-s_1=R/2\), so it stays away from the rotation axis.  Although the
distance \(s\) is nonsmooth at the central circle \(s=0\), the composition
\(h(s)\) is smooth there because it is constant on a neighborhood; flatness of
\(F\) gives smoothness across both wall interfaces.

At a rim point put \(y=1-h\) and \(\beta=-b\).  Equation (4.14) gives

\[
y=\frac{\beta R^2h}{\rho^2+R^2h}
\leq\beta\leq\beta_0=\delta.
\tag{B.23}
\]

Thus the rim can meet only the near-plateau part of the wall, where

\[
-\frac{h'}{1-h}
=\frac1w\frac{F'}F
>\frac1R.
\tag{B.24}
\]

Since \(D\ne0\), \(h'\ne0\), and
\(\chi_z=h'z/s\), equation (B.17) shows that a transverse critical rim point
would have to satisfy \(z=0\).  On the outer equator \(\rho=R+s\), one has
\(\chi_\rho=h'<0\), and hence \(B_\rho>0\).  On the inner equator
\(\rho=R-s\), put \(q=-h'>0\).  There \(\chi_\rho=q\), and the exact rim
identity for \(D\), followed by the arithmetic--geometric mean inequality,
gives

\[
B_\rho
=2\rho y-q\left(\frac{\rho^2}{h}+R^2h\right)
\leq2\rho y-2R\rho q<0.
\tag{B.25}
\]

The last inequality is (B.24).  Hence \(B_\rho\) and \(B_z\) cannot vanish
simultaneously anywhere on \(\mathcal Z\), which proves (4.20) for the cutoff
(B.22).  This is pointwise transversality, not a uniform lower bound: as
\(b\to0^-\), rim points approach the flat \(h=1\) edge and
\(|\nabla_\perp B|\) may tend to zero.

Finally, when \(B_A\ne0\), the periodic \(K\)-orbit is a closed causal curve
which is not a null pregeodesic.  The push-up lemma deforms it to a closed
timelike curve through each of its points.  For the cutoff (B.22), every
transition-rim axial orbit therefore lies in \(\mathcal C\), rather than
generating \(\partial\mathcal C\).  With the opposite Riemann convention the
signs in (B.13), (4.18), and (4.19) reverse, but the vanishing and divergence
conclusions are unchanged.

## Appendix C. Circular null geodesics and gain--compression reciprocity

This appendix proves Proposition 5.2 and separates three notions that are easy
to conflate: completeness of the closed null orbit, completeness of nearby
null geodesics, and the energy measured by a chosen timelike observer.

### C.1 First integrals and the two null families

For

\[
g_2=-A(t)dt^2+2C(t)dt\,d\phi+B(t)d\phi^2,
\qquad
\Delta=C^2+AB>0,
\tag{C.1}
\]

let a dot denote affine differentiation.  The circular Killing momentum is

\[
L=g(\partial_\phi,\dot\gamma)
  =C\dot t+B\dot\phi.
\tag{C.2}
\]

Combining (C.2) with the null equation gives

\[
L^2=\Delta\dot t^{\,2},
\qquad
\frac{d\phi}{dt}
=\frac{-C\pm\sqrt{\Delta}}{B}.
\tag{C.3}
\]

Suppose \(B(0)=0\), \(C(0)\ne0\), and \(L\ne0\).  Then \(t\) is monotone and

\[
\left|\frac{d\lambda}{dt}\right|
=\frac{\sqrt{\Delta}}{|L|}.
\tag{C.4}
\]

Thus \(t=0\) lies at finite affine distance.  Of the two roots in (C.3), one
has the finite limit

\[
\frac{d\phi}{dt}\longrightarrow \frac{A(0)}{2C(0)},
\tag{C.5}
\]

while the other obeys

\[
\frac{d\phi}{dt}
=-\frac{2C(0)}{B(t)}+O(1).
\tag{C.6}
\]

The labels of the signs in (C.3) interchange when \(C(0)\) changes sign.
Equation (C.5) is the regular family and (C.6) is the recurrent family.

If the zero of \(B\) is isolated on the side under consideration and the
coefficients are \(C^2\), then \(B\) has fixed sign there and
\(\lvert B(t)\rvert\le M\lvert t\rvert\).  Consequently

\[
\int^0\frac{dt}{\lvert B(t)\rvert}=\infty.
\tag{C.7}
\]

The recurrent angle is monotone and unbounded.  Modulo its period it therefore
has no limit, although \(t\to0\) in finite affine parameter.  The corresponding
geodesic has no endpoint in the spacetime and is affine incomplete.  This
argument requires neither a simple zero nor curvature blow-up.

### C.2 Ribbon normal form

After reversing \(\phi\) if necessary, take \(C>0\) in a neighborhood of the
zero and set

\[
\psi=\phi+\int^t\frac{C-\sqrt{\Delta}}{B}\,ds,
\qquad
T=\int^t\sqrt{\Delta}\,ds.
\tag{C.8}
\]

The quotient remains \(\psi\sim\psi+P\), and the metric becomes

\[
g_2=2\,dT\,d\psi+B(T)d\psi^2.
\tag{C.9}
\]

The apparent quotient issue is harmless because the shift in (C.8) depends
only on \(t\).  The two null directions are now transparent:

\[
d\psi=0,
\qquad
\frac{d\psi}{dT}=-\frac{2}{B(T)}.
\tag{C.10}
\]

The first crosses the null orbit regularly; the second is precisely the
incomplete recurrent family.  This is the circular ribbon form used in
Section 6.

### C.3 Surface gravity and the closed orbit

In (C.9), \(K=\partial_\psi\), \(K^2=B\), and the Killing identity gives

\[
\nabla_KK=-\frac12\nabla(K^2).
\tag{C.11}
\]

On \(B=0\),

\[
\nabla_KK=\kappa K,
\qquad
\kappa=-\frac12B_T(0)
       =-\frac{B_t(0)}{2C(0)}.
\tag{C.12}
\]

If \(\kappa=0\), \(K\) is affinely parametrized on the closed orbit; its
periodic extension is affine complete.  If \(\kappa\ne0\), an affine tangent
has the form \(fK\) with

\[
\frac{df}{d\psi}+\kappa f=0.
\tag{C.13}
\]

The affine lapse per circuit then scales exponentially, and one time direction
has finite total affine length.  This is a property of the generator itself.
Even when \(\kappa=0\), the companion family in (C.10) remains incomplete.

### C.4 Simple and degenerate compression

For a simple zero,

\[
B(T)=-2\kappa T+O(T^2).
\tag{C.14}
\]

Integrating the recurrent equation in (C.10) shows that consecutive circuits
obey, up to orientation,

\[
\frac{|T_{q+1}|}{|T_q|}
\longrightarrow e^{-|\kappa|P}.
\tag{C.15}
\]

In the exact core, the affine lapse of a late circuit is proportional to
\(\lvert T_q\rvert\), while the energy measured by \(u=\partial_t\) is
proportional to \(1/\lvert T_q\rvert\).  Hence the one-circuit blueshift factor
is the reciprocal of the affine-compression factor.  This is the local
gain--compression relation; it is not a product over different chronology
boundaries.

For a degenerate zero of finite odd order,

\[
B(t)=b_mt^m+o(t^m),
\qquad m>1,
\tag{C.16}
\]

equation (C.6) gives

\[
q\asymp |t_q|^{1-m},
\qquad
|t_q|\asymp q^{-1/(m-1)}.
\tag{C.17}
\]

Since \(d\lambda/dt\) tends to a nonzero constant,

\[
\ell_q\asymp q^{-m/(m-1)}.
\tag{C.18}
\]

For the recurrent family in the exact core,

\[
\bar E_q\asymp |B(t_q)|^{-1}
              \asymp q^{m/(m-1)},
\qquad
\bar E_q\ell_q\asymp1.
\tag{C.19}
\]

Thus degeneracy changes exponential compression into polynomial compression
but does not remove the reciprocal growth.  At the accumulation surface
\(t=0\) of (3.6), all derivatives of \(b\) vanish and the closed \(K\)-orbit is
complete.  Each nonzero boundary \(t_n\), however, still has its own incomplete
recurrent family.  A recurrent ray captured at one \(t_n\) does not traverse
the later members of the stack.

## Appendix D. Analytic torus actions

Let a real-analytic torus \(T^k\) act analytically and isometrically on an
analytic Lorentzian spacetime.  Choose a basis \(K_1,\ldots,K_k\) of Killing
fields for its Lie algebra \(\mathfrak t\), adapted to the integral lattice,
and define the analytic symmetric matrix

\[
\mathsf B_{ij}(p)=g_p(K_i,K_j).
\tag{D.1}
\]

A rational direction \(\xi\in\mathfrak t\) generates a closed one-parameter
subgroup.  If \(\mathsf B_p(\xi,\xi)<0\), its orbit through \(p\) is a closed
timelike curve: the norm is constant along that orbit.  Conversely, this is
exactly the type of curve used to define \(\mathcal C_T\).

If \(\mathsf B_p\) is not positive semidefinite, its negative cone is open and
contains a rational direction because rational lattice directions are dense.
Therefore

\[
\mathcal C_T
=\{p:\mathsf B_p\text{ is not positive semidefinite}\}.
\tag{D.2}
\]

A real symmetric matrix is positive semidefinite precisely when all of its
principal minors are nonnegative.  If \(\Delta_I\) denotes the minor indexed by
a nonempty subset \(I\subset\{1,\ldots,k\}\), then

\[
\mathcal C_T
=\bigcup_{\varnothing\ne I}\{p:\Delta_I(p)<0\}.
\tag{D.3}
\]

This is a finite union of basic open semianalytic sets.  Standard local
structure theory for semianalytic sets implies that their connected components
form a locally finite family (Bierstone and Milman 1988).

There is also an elementary one-dimensional version.  If
\(\gamma:J\to M\) is an analytically extendible geodesic, then each
\(\Delta_I\circ\gamma\) is analytic.  Unless it vanishes identically, it has
only finitely many zeros on every compact subinterval of \(J\).  The finitely
many sign conditions in (D.3) therefore cut such an interval into only
finitely many components.

Neither argument says that \(\mathcal C_T\) equals the full
chronology-violating set \(\mathcal C\).  Nonsymmetric closed timelike curves
may enlarge \(\mathcal C\), and different pieces of \(\mathcal C_T\) may join
inside that larger set.  The proposition becomes a statement about all
chronology classes only after a separate proof of
\(\mathcal C_T=\mathcal C\), as supplied for the circular core by the temporal
barriers in Section 3.

## Appendix E. Scalar, Maxwell, and detector derivations

### E.1 The scalar wave operator

For the canonical ribbon (6.1), the metric and its inverse are

\[
(g_{\mu\nu})
=\begin{pmatrix}0&1\\[2pt]1&B\end{pmatrix},
\qquad
(g^{\mu\nu})
=\begin{pmatrix}-B&1\\[2pt]1&0\end{pmatrix},
\qquad
\det g=-1.
\tag{E.1}
\]

Hence

\[
\Box\Phi
=-B\Phi_{TT}-B'\Phi_T+2\Phi_{T\psi}.
\tag{E.2}
\]

With \(H'=2/B\), \(u=\psi\), and \(v=\psi+H(T)\), one has

\[
g_2=B\,du\,dv,
\qquad
\Box\Phi=\frac4B\,\partial_u\partial_v\Phi.
\tag{E.3}
\]

Thus every local homogeneous solution is \(F(u)+G(v)\).

### E.2 Quotient monodromy and regularity

The quotient acts diagonally:

\[
(u,v)\sim(u+P,v+P).
\tag{E.4}
\]

Periodicity of \(F(u)+G(v)\) implies a constant \(c\) such that

\[
F(u+P)-F(u)=c,
\qquad
G(v+P)-G(v)=-c.
\tag{E.5}
\]

Writing

\[
F(u)=F_{\mathrm p}(u)+\frac cP u,
\qquad
G(v)=G_{\mathrm p}(v)-\frac cP v
\tag{E.6}
\]

with periodic \(F_{\mathrm p},G_{\mathrm p}\), the nonperiodic remainder of
their sum is

\[
-\frac cP H(T).
\tag{E.7}
\]

Because \(H\) diverges at the isolated zero, continuous extension forces
\(c=0\).  If the remaining periodic \(G_{\mathrm p}\) is nonconstant, then
\(H(T)\bmod P\) traverses every phase infinitely often and
\(G_{\mathrm p}(\psi+H(T))\) has no limit.  Therefore \(G_{\mathrm p}\) must
be constant.  The periodic \(F_{\mathrm p}(\psi)\) is unrestricted.  At the
derivative level,

\[
\partial_T\Phi=\frac2B G_{\mathrm p}'(v),
\tag{E.8}
\]

so the angular average of \(\lvert\partial_T\Phi\rvert^2\) is

\[
\frac4{B^2}\int_0^P\lvert G_{\mathrm p}'\rvert^2\,d\psi.
\tag{E.9}
\]

This also proves the \(C^1\) and finite-derivative-energy versions of
Proposition 6.1.

### E.3 Sourced modes

For a Fourier mode \(f_n(T)e^{ik_n\psi}\), equation (E.2) gives

\[
(Bf_n')'-2ik_nf_n'=-J_n.
\tag{E.10}
\]

Since \(H'=2/B\),

\[
\frac d{dT}\!\left(Be^{-ik_nH}f_n'\right)
=-J_ne^{-ik_nH}.
\tag{E.11}
\]

On a punctured band \((T_a,T_b)\), impose no incoming recurrent amplitude at
\(T_a\) and require regular-only output at \(T_b\).  Integration gives

\[
\int_{T_a}^{T_b}J_n(T)e^{-ik_nH(T)}\,dT=0
\quad(n\ne0),
\qquad
\int_{T_a}^{T_b}J_0(T)\,dT=0.
\tag{E.12}
\]

The source is assumed smooth and compactly supported where \(B\ne0\).  For a
real field, the data for \(n\) and \(-n\) must also satisfy the usual complex
conjugacy relation.

The kernel of (E.12) is nontrivial.  For example,

\[
J_n=e^{ik_nH}q_n'
\tag{E.13}
\]

with compactly supported \(q_n\) has zero moment.  More geometrically, let
\(\tau=H/2=(v-u)/2\) and set

\[
\Phi=q(\tau)F(u),
\tag{E.14}
\]

where \(q\) changes from zero to one in a compact transition interval on which
\(B\) is bounded away from zero.  Direct differentiation yields

\[
\Box\Phi
=\frac{-q''(\tau)F(u)+2q'(\tau)F'(u)}{B(T)}.
\tag{E.15}
\]

The source in (E.15) is smooth and compactly operated, the incoming field is
zero, and the outgoing local field is the nonzero regular component \(F(u)\).
This construction is bandwise; it does not define a global retarded solution
on the entire non-globally-hyperbolic spacetime.

### E.4 Maxwell reduction

On the direct product with flat coordinates \(x,y\), take

\[
\mathcal A=\alpha(T,\psi)\,dx.
\tag{E.16}
\]

Then \(\nabla_a\mathcal A^a=0\) automatically and

\[
\mathcal F=d\alpha\wedge dx,
\qquad
\nabla_a\mathcal F^{ax}=\Box_{g_2}\alpha.
\tag{E.17}
\]

All other Maxwell equations vanish identically.  A current
\(\mathcal J=J(T,\psi)\partial_x\) is conserved because it is independent of
\(x\), and it obeys the same mode conditions (E.12).  The embedding is exact
but transversely uniform, so its total transverse energy is infinite unless a
further localization mechanism is supplied.

### E.5 Bounded detector response

Let \(X:[\tau_0,\tau_*)\to(\mathcal X,d)\) be an absolutely continuous curve in
a complete metric space, with metric derivative bounded almost everywhere by
an integrable function \(h\).  For \(s<t<\tau_*\),

\[
d(X(s),X(t))\le\int_s^t h(\tau)\,d\tau.
\tag{E.18}
\]

The tail integral tends to zero, so \(X(\tau)\) is Cauchy and has a unique
limit as \(\tau\to\tau_*\).  Its total variation is at most \(\int h\).
If \(N_\epsilon\) successive updates each require displacement at least
\(\epsilon\), total variation is at least \(N_\epsilon\epsilon\), proving
(6.17).  The lemma permits infinitely many diminishing updates and therefore
does not impose a literal memory reset.

## Reproducibility note

The inverse metric, connection, curvature, Einstein tensor, and parallel-frame
identities used in Sections 3 and 5 are checked by
[zeno_banded_metric_symbolics.py](zeno_banded_metric_symbolics.py).  The
transition-rim inverse, Killing acceleration, optical tidal matrix, and
parallel-screen identities used in Section 4.4 and Appendix B are checked by
[zeno_transition_rim_symbolics.py](zeno_transition_rim_symbolics.py).  The wave
operator, homogeneous chiral solution, and integrating-factor identity used in
Section 6 are checked by
[zeno_scalar_filter_symbolics.py](zeno_scalar_filter_symbolics.py).  These
scripts use exact symbolic algebra and are supplementary checks rather than
substitutes for the proofs.

## References

- C. Bavard and P. Mounoud, “Extensions maximales et classification des tores
  lorentziens munis d'un champ de Killing,” *Annales de l'Institut Fourier*
  **70**, 67--168 (2020).
  [doi:10.5802/aif.3309](https://doi.org/10.5802/aif.3309)
- E. Bierstone and P. D. Milman, “Semianalytic and subanalytic sets,”
  *Publications Mathématiques de l'IHÉS* **67**, 5--42 (1988).
  [doi:10.1007/BF02699126](https://doi.org/10.1007/BF02699126)
- B. Carter, “Causal structure in space-time,” *General Relativity and
  Gravitation* **1**, 349--391 (1971).
  [doi:10.1007/BF00759217](https://doi.org/10.1007/BF00759217)
- F. Echeverria, G. Klinkhammer, and K. S. Thorne, “Billiard balls in wormhole
  spacetimes with closed timelike curves: Classical theory,” *Physical Review
  D* **44**, 1077--1099 (1991).
  [doi:10.1103/PhysRevD.44.1077](https://doi.org/10.1103/PhysRevD.44.1077)
- D. Fermi and L. Pizzocchero, “A time machine for free fall into the past,”
  *Classical and Quantum Gravity* **35**, 165003 (2018).
  [doi:10.1088/1361-6382/aace6e](https://doi.org/10.1088/1361-6382/aace6e);
  [arXiv:1803.08214](https://arxiv.org/abs/1803.08214)
- J. L. Friedman, M. S. Morris, I. D. Novikov, F. Echeverria, G. Klinkhammer,
  K. S. Thorne, and U. Yurtsever, “Cauchy problem in spacetimes with closed
  timelike curves,” *Physical Review D* **42**, 1915--1930 (1990).
  [doi:10.1103/PhysRevD.42.1915](https://doi.org/10.1103/PhysRevD.42.1915)
- J. L. Friedman and M. S. Morris, “Existence and uniqueness theorems for
  massless fields on a class of spacetimes with closed timelike curves,”
  *Communications in Mathematical Physics* **186**, 495--529 (1997).
  [doi:10.1007/s002200050118](https://doi.org/10.1007/s002200050118);
  [arXiv:gr-qc/9411033](https://arxiv.org/abs/gr-qc/9411033)
- G. J. Galloway, “Maximum principles for null hypersurfaces and null splitting
  theorems,” *Annales Henri Poincaré* **1**, 543--567 (2000).
  [doi:10.1007/s000230050006](https://doi.org/10.1007/s000230050006);
  [arXiv:math/9909158](https://arxiv.org/abs/math/9909158)
- T. Ghosh, M. Salo, and G. Uhlmann, “The Calderón problem for the fractional
  Schrödinger equation,” *Analysis & PDE* **13**, 455--475 (2020).
  [doi:10.2140/apde.2020.13.455](https://doi.org/10.2140/apde.2020.13.455);
  [arXiv:1609.09248](https://arxiv.org/abs/1609.09248)
- S. W. Hawking, “Chronology protection conjecture,” *Physical Review D* **46**,
  603--611 (1992).
  [doi:10.1103/PhysRevD.46.603](https://doi.org/10.1103/PhysRevD.46.603)
- S. W. Hawking and G. F. R. Ellis, *The Large Scale Structure of Space-Time*,
  Cambridge University Press (1973).
- B. S. Kay, M. J. Radzikowski, and R. M. Wald, “Quantum field theory on
  spacetimes with a compactly generated Cauchy horizon,” *Communications in
  Mathematical Physics* **183**, 533--556 (1997).
  [doi:10.1007/s002200050042](https://doi.org/10.1007/s002200050042);
  [arXiv:gr-qc/9603012](https://arxiv.org/abs/gr-qc/9603012)
- S. Krasnikov, “Time machines with the compactly determined Cauchy horizon,”
  *Physical Review D* **90**, 024067 (2014).
  [doi:10.1103/PhysRevD.90.024067](https://doi.org/10.1103/PhysRevD.90.024067);
  [arXiv:1405.2277](https://arxiv.org/abs/1405.2277)
- M. Kriele, “The structure of chronology violating sets with compact closure,”
  *Classical and Quantum Gravity* **6**, 1607--1611 (1989).
  [doi:10.1088/0264-9381/6/11/014](https://doi.org/10.1088/0264-9381/6/11/014)
- A. Lossev and I. D. Novikov, “The Jinn of the time machine: Non-trivial
  self-consistent solutions,” *Classical and Quantum Gravity* **9**, 2309--2321
  (1992).
  [doi:10.1088/0264-9381/9/10/014](https://doi.org/10.1088/0264-9381/9/10/014)
- L. Mehidi, “Maximal simply connected Lorentzian surfaces with a Killing field
  and their completeness,” *Mathematische Zeitschrift* **301**, 739--780
  (2022).
  [doi:10.1007/s00209-021-02915-3](https://doi.org/10.1007/s00209-021-02915-3);
  [arXiv:2001.03149](https://arxiv.org/abs/2001.03149)
- E. Minguzzi, “Limit curve theorems in Lorentzian geometry,” *Journal of
  Mathematical Physics* **49**, 092501 (2008).
  [doi:10.1063/1.2973048](https://doi.org/10.1063/1.2973048);
  [arXiv:0712.3942](https://arxiv.org/abs/0712.3942)
- E. Minguzzi, “Area theorem and smoothness of compact Cauchy horizons,”
  *Communications in Mathematical Physics* **339**, 57--98 (2015).
  [doi:10.1007/s00220-015-2415-8](https://doi.org/10.1007/s00220-015-2415-8);
  [arXiv:1406.5919](https://arxiv.org/abs/1406.5919)
- E. Minguzzi, “The boundary of the chronology violating set,” *Classical and
  Quantum Gravity* **33**, 225004 (2016).
  [arXiv:1603.08190](https://arxiv.org/abs/1603.08190)
- E. Minguzzi, “Lorentzian causality theory,” *Living Reviews in Relativity*
  **22**, 3 (2019).
  [doi:10.1007/s41114-019-0019-x](https://doi.org/10.1007/s41114-019-0019-x)
- O. L. Petersen, “Extension of Killing vector fields beyond compact Cauchy
  horizons,” *Advances in Mathematics* **391**, 107953 (2021).
  [doi:10.1016/j.aim.2021.107953](https://doi.org/10.1016/j.aim.2021.107953);
  [arXiv:1903.09135](https://arxiv.org/abs/1903.09135)
- N. E. Rieger, “Causal classification of pathological Misner-type
  spacetimes,” *Annals of Physics* **489**, 170455 (2026).
  [doi:10.1016/j.aop.2026.170455](https://doi.org/10.1016/j.aop.2026.170455);
  [arXiv:2501.00841](https://arxiv.org/abs/2501.00841)
- M. Sánchez, “Structure of Lorentzian tori with a Killing vector field,”
  *Transactions of the American Mathematical Society* **349**, 1063--1080
  (1997).
  [doi:10.1090/S0002-9947-97-01745-5](https://doi.org/10.1090/S0002-9947-97-01745-5)
- S. Slobodov, “Unwrapping Closed Timelike Curves,” *Foundations of Physics*
  **38**, 1082--1109 (2008).
  [doi:10.1007/s10701-008-9253-x](https://doi.org/10.1007/s10701-008-9253-x);
  [arXiv:0808.0956](https://arxiv.org/abs/0808.0956)
