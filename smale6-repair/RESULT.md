# Result: exact exclusions for positive Roberts-inspired continua

## 1. Exact starting point

Let

\[
q_1=(a,0),\quad q_2=(-a,0),\quad
q_3=(0,b),\quad q_4=(0,-b),\quad q_0=(0,0),
\qquad a^2+b^2=1.
\]

Give the four noncentral bodies mass `1` and the central body mass `M`.
The acceleration multipliers read

\[
\lambda_x=2+\frac{1/4+M}{a^3},\qquad
\lambda_y=2+\frac{1/4+M}{b^3}.
\]

Consequently, for a nonsquare rhombus (`a != b`) the configuration is
central if and only if

\[
M=-\frac14.
\]

For this signed value, `lambda=2` for every `0<a<1`; this is Roberts's
continuum. The script `nested_rhombi.js` independently evaluates the full
force equations and obtains residuals at floating-point roundoff.

There is also a useful invariant factorization.  On the inertia slice
`a^2+b^2=1`, the potential restricted to the rhombus-with-center stratum is

\[
U=4+2\left(M+\frac14\right)\left(\frac1a+\frac1b\right),
\]

and the reduced central-configuration equation factors as

\[
\left(M+\frac14\right)(a^{-3}-b^{-3})=0.
\]

Thus the symmetric incidence variety is the union of the vertical Roberts
component `M=-1/4` and the square section `a=b`.  If `u=a^2`, the full labelled
squared-distance vector consists of

\[
4u,\quad 4(1-u),\quad
\underbrace{1,1,1,1}_{\text{cross edges}},\quad
u,u,\quad 1-u,1-u.
\]

It is an affine line.  At `M=-1/4`, the coefficients of both nonconstant
square-root classes are `1/2+2M=0`, so the potential identity survives at
every parameter value.  This makes the mechanism explicit: reducibility and
a vertical component of the mass projection, enabled by signed cancellation.

The cancellation can be isolated as a neutral-cluster phenomenon. For a
finite cluster of distinct points with positive masses `mu_i`, define its
internal accelerations

\[
B_i=\sum_{j\ne i}\mu_j\frac{x_j-x_i}{|x_j-x_i|^3}.
\]

The `B_i` cannot all equal a common vector. Indeed, mass-summing gives
`sum_i mu_i B_i=0`, so a common vector would have to be zero; but, with `c`
the cluster center of mass,

\[
\sum_i\mu_i(x_i-c)\mathbin{\cdot}B_i
=-\sum_{i<j}\frac{\mu_i\mu_j}{|x_i-x_j|}<0.
\]

Thus a finite positive cluster cannot be neutral. Roberts's signed triple at
scaled locations `(-1,0,1)`, with masses `(1,-1/4,1)`, is neutral exactly.

## 2. Affine squared-distance obstruction

**Proposition 1.** Let all masses be positive and normalize the center of mass
and inertia. A nontrivial connected family of central configurations cannot
trace a nonconstant affine segment in squared-distance space.

**Proof.** Write `s_ij=r_ij^2` and `w_ij=m_i m_j>0`. Along a differentiable
family on a fixed-inertia slice,

\[
U=\sum_{i<j}w_{ij}s_{ij}^{-1/2}
\]

is constant: every point is critical for the restriction of `U`, so the
derivative of `U` along the family vanishes. If
`s_ij(t)=s_ij(0)+t h_ij`, then

\[
U''(t)=\frac34\sum_{i<j}w_{ij}
\frac{h_{ij}^2}{s_{ij}(t)^{5/2}}>0
\]

unless every `h_ij=0`. Thus a nonconstant affine squared-distance path cannot
have constant `U`. `QED`

More generally, every twice differentiable normalized positive-mass central-
configuration curve must satisfy the curvature identity

\[
\sum_{i<j}w_{ij}s_{ij}^{-3/2}s_{ij}''
=\frac32\sum_{i<j}w_{ij}s_{ij}^{-5/2}(s_{ij}')^2>0
\]

at every nontrivial tangent. Thus the curve must bend with a strictly positive
weighted normal component in squared-distance space. Roberts's signed family
evades this because signed edge weights cancel and its squared-distance path
is affine.

This proposition directly eliminates positive lifts whose **normalized**
squared distances remain affine. In particular it applies to mass-balanced
nested rhombi with `a^2+b^2` fixed. For a general template
`q_i=diag(a,b)p_i`, one must first check that its centered inertia is constant;
otherwise normalization itself bends the Gram path.

## 2A. Projective-conic squared-distance obstruction

**Proposition 1A (project lemma).** Fix strictly positive masses and normalize
the center of mass and inertia.  Let `gamma` be a collision-free connected
arc of central configurations.  If the projective image of its **full
labelled** squared-mutual-distance vector is contained in a real algebraic
curve of degree at most two, then every mutual distance is constant.  Hence
the arc is trivial in shape space.  The statement concerns the full distance
vector, not a conic appearing only in a coordinate projection.

**Proof.** A reducible or nonreduced degree-two curve reduces to a line on a
connected nonconstant arc, so only an irreducible real conic needs attention.
Along a fixed-inertia central-configuration arc,

\[
dU=-\lambda\,dI=0,
\]

and therefore

\[
U=\sum_e w_e s_e^{-1/2}=U_0,
\qquad w_e=m_i m_j>0,
\]

where `e` ranges over all labelled edges.

The normalization of a real conic containing a real arc is
`P^1`.  Pulling its homogeneous coordinates back to `P^1` gives binary
quadratic forms `D,N_e` such that, on a smaller physical interval if
necessary,

\[
s_e=\frac{N_e}{D},\qquad D>0,\quad N_e>0.
\]

Constancy of the potential becomes the function-field identity

\[
\sum_e w_e\sqrt{\frac{D}{N_e}}=U_0. \tag{1}
\]

Let `K=R(t)` and adjoin the square roots in (1).  The resulting
multiquadratic extension splits as a direct sum of `K`-subspaces indexed by
the generated square classes in `K*/K*^2`.  Terms in a nontrivial common
square class would have to sum to zero independently of the trivial class.
Choose one positive square root for that class on the physical interval.
Every rational multiplier in the group is then positive there, and all
`w_e` are positive, so such a sum cannot vanish.  Consequently every
`D/N_e` is itself a square in `K`.

Unique factorization, applied homogeneously on `P^1`, now gives a common
squarefree binary form `H`, positive constants `c_0,c_e`, and forms `L_0,L_e`
such that

\[
D=c_0H L_0^2,\qquad N_e=c_eH L_e^2.
\]

All `D,N_e` have degree two.  If `H` has positive degree, the `L` factors are
constant and every `N_e/D` is already constant.  Otherwise the `L` factors
are linear, and (1), with signs oriented on the physical interval, is a
rational identity

\[
\sum_e a_e\frac{L_0}{L_e}=U_0,
\qquad a_e>0. \tag{2}
\]

If some `L_e` has a projective zero different from the zero of `L_0`, (2)
has a pole there.  All denominators with that zero are positive scalar
multiples on the physical interval, so their nonzero residues have the same
sign and cannot cancel.  Hence every `L_e` is proportional to `L_0`.
Thus every `s_e=N_e/D` is constant.  The complete labelled distance matrix
determines a configuration up to Euclidean isometry, proving the claim.
`QED`

This closes the proposed search over conic paths before symbolic fitting is
attempted.  It uses positivity essentially: the Roberts line evades both the
square-class and pole arguments through signed cancellation.  A
degree-four projective distance ansatz is not excluded by this proof, but no
claim is made here that such an ansatz satisfies Euclidean realizability or
the central-configuration equations.

## 3. Fixed-cloud obstruction

**Proposition 2.** Fix finitely many pairwise distinct auxiliary points `p_k`
in the plane and
give every original and auxiliary body a positive mass. No open interval of
the Roberts shear

\[
Q(a)=\{(\pm a,0),(0,\pm\sqrt{1-a^2})\},\qquad 0<a<1,
\]

augmented by those fixed auxiliary bodies can consist of central
configurations with fixed masses.

**Proof.** Remove from `(0,1)` the finitely many parameters at which a moving
vertex meets an auxiliary point. On each remaining component, all distances,
the center of mass, the inertia `I`, the potential `U`, and the normalized
central-configuration residuals are real analytic. If the residuals vanish on
an open subinterval, the real-analytic identity theorem makes them vanish on
the whole component.

At either endpoint of that component, one or more proper positive-mass
collision clusters occur:
either the pair `(+-a,0)` or `(0,+-sqrt(1-a^2))` collides, or a moving vertex
meets an auxiliary body. Since another original vertex remains separated, the
centered inertia has a positive finite limit. The positive Newtonian potential
diverges, so the central multiplier (given by the Euler identity, with
`I=(1/2) sum_i m_i |q_i-c|^2`, by `lambda=U/(2I)`) diverges.

To avoid assuming that an individually chosen body is not part of another
simultaneous collision, partition the bodies by their limiting positions and
sum `m_i A_i` over one whole limiting cluster whose position differs from the
limiting center of mass. Internal forces cancel pairwise in this sum, while all
cross-cluster forces stay bounded. The right side of the summed central-
configuration equation is the diverging multiplier times a vector with a
nonzero limit. Contradiction. `QED`

## 4. Co-moving-shell obstruction

**Proposition 3.** The same conclusion holds if the fixed cloud is replaced by
any finite positive co-moving shell whose trajectories have the form

\[
p_k(a)=(\alpha_k a,\,\beta_k\sqrt{1-a^2})
\]

with fixed real coefficients, provided bodies are collision-free for
`0<a<1`. This includes any finite collection of nested homothetic rhombi or
rectangles, with arbitrary positive masses and an optional positive central
mass.

**Proof.** All residuals are again real analytic throughout `(0,1)`, so an
identity on an open interval extends to the whole interval. As `a -> 0`, at
least the two original bodies `(+-a,0)` undergo a proper positive collision,
while the other original pair remains separated at `(0,+-1)`. Applying the
same limiting-cluster sum used in Proposition 2 gives a contradiction. `QED`

For nested axis rhombi there is also a direct force proof. At the outermost
positive x-axis body `(R a,0)`, every other member of the collapsing x-axis
cluster pulls inward, so

\[
A_x=-C a^{-2}+O(a),\qquad C>0,
\]

and its equation demands `lambda=C/(R a^3)+O(1)`. A noncollapsing y-axis
body has bounded acceleration and nonzero limiting position, demanding bounded
`lambda`. This is impossible. A signed neutral cluster can make `C=0`; a
positive cluster cannot, because its outermost body is pulled strictly inward.

There is an instructive near miss. For `k>1`, positive masses `mu` at `(+-ka,0)` exactly
reproduce the missing outward force at the inner x-pair for every `a` when

\[
\mu=\frac{(k^2-1)^2}{16k}.
\]

Adding the analogous y-pair, however, changes the inner x and y multipliers by
`2 mu/(a^2+k^2b^2)^(3/2)` and
`2 mu/(b^2+k^2a^2)^(3/2)`, respectively. They agree along an aspect interval
only for the trivial cases `k=1`, `mu=0`, or the isolated square `a=b`.
Thus perfect local emulation of the signed force fails through cross-coupling.

## 5. Consequence for the search

The negative mass is not a local defect that can be repaired by a finite fixed
cloud or by a finite coefficient-wise co-moving shell of Proposition 3.
Positivity changes the geometry required of a counterexample.

Any successful positive-mass continuation inspired by Roberts must have compact
collision-free closure after normalization. It must turn, branch, or meet
degenerate/singular central configurations before the Roberts collision
endpoints. A shear-retaining lift therefore needs genuinely nonlinear auxiliary
motion or branching; fixed clouds and coefficient-wise co-moving shells cannot
work. The affine squared-distance obstruction further says that a viable lift
must bend in distance space with the strictly positive weighted curvature in
Proposition 1, while Proposition 1A excludes every line or conic in the full
projective squared-distance image.  Any exact low-degree successor must evade
both statements rather than merely be nonlinear in a chosen parameter.

This is the concrete output of the first repair experiment: a broad class of
the most natural positivity repairs is eliminated exactly, and the remaining
target is a nonlinear, potentially topology-changing repair rather than an
effective-negative-mass module.

## 6. Prior-art scope

Roberts already gave the constrained-potential identity `U=4`, observed that
the signed continuum approaches triple collisions, and cited Shub's
positive-mass compactness result to explain why those endpoints cannot survive
with positive masses. Hachmeister--Little--McGhee--Pelayo--Sasarita later
generalized the signed mechanism using neutral configurations and orthogonal
doubling. The mass-incidence/square-class packaging, the affine and conic
squared-distance lemmas, and the fixed/co-moving-cloud exclusions above are
project deductions tailored to this repair experiment.  Their broader
literature priority has not been established, and no priority claim is made
here.  A targeted search found no equivalent line/conic theorem in the
primary mutual-distance, finiteness, and signed-continuum literature, but
that is not enough to exclude unpublished folklore or establish priority.
Hampton--Jensen's finiteness theorem for extensions of fixed subconfigurations
is adjacent prior art, but does not cover the moving Roberts vertices with an
arbitrary fixed auxiliary cloud.

- Gareth E. Roberts, *A Continuum of Relative Equilibria in the 5-Body
  Problem*, Physica D 127 (1999), 141--145,
  DOI `10.1016/S0167-2789(98)00315-7`.
- J. Hachmeister et al., *Continua of central configurations with a negative
  mass in the n-body problem*, Celestial Mechanics and Dynamical Astronomy
  115 (2013), 427--438, DOI `10.1007/s10569-013-9471-1`.
- A. Albouy and V. Kaloshin, *Finiteness of central configurations of five
  bodies in the plane*, Annals of Mathematics 176 (2012), 535--588, DOI
  `10.4007/annals.2012.176.1.10`.
- A. Albouy and A. Chenciner, *Le problème des n corps et les distances
  mutuelles*, Inventiones Mathematicae 131 (1998), 151--184, DOI
  `10.1007/s002220050200`.
- M. Hampton and A. Jensen, *Finiteness of relative equilibria in the
  planar n-body problem with fixed subconfigurations*, Journal of Geometric
  Mechanics 7 (2015), 35--42, DOI `10.3934/jgm.2015.7.35`.
