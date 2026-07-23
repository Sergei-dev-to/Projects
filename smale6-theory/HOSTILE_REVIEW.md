# Hostile review: positive-radical square lift

**Review date:** 2026-07-22  
**Object reviewed:** first draft of SQUARE_LIFT_NOTE.md  
**Review count under the stopping gate:** one

## Verdict before revision

**Survives with material corrections.** No internal counterexample or fatal
gap was found. The radical-splitting argument, square lift, parity
conclusion, and degree-two pole obstruction are valid under a precise
algebraic-curve hypothesis. The first draft should not be accepted without
the corrections below.

## Adversarial checks

### 1. Can positive radicals in one nontrivial square class cancel?

No. In the multiquadratic extension of the curve function field, group the
radicals by their classes in \(K^\times/K^{\times2}\). On a sufficiently
small physical interval, orient one representative radical in each class
positively. Every rational multiplier relating another positive radical in
that class is then positive on the interval. Its class coefficient is a sum
of strictly positive functions and cannot be zero. Independence of the
multiquadratic basis therefore eliminates every nontrivial class.

This check uses all three of: strictly positive masses, collision freedom,
and the positive physical square-root branches.

### 2. Does an identity on a real arc become a function-field identity?

Yes, after deleting the finitely many singular, zero, pole, and branch
points. Lift a smaller physical subarc to the normalization and then to the
multiquadratic cover by its positive branches. The induced map from the
algebraic function field to analytic germs is injective. An algebraic
function vanishing on the subarc is therefore zero.

### 3. Does the rational square lift extend across zeros and poles?

Yes. A rational map from a smooth complete curve to projective space
extends uniquely to a morphism. Locally one may equivalently subtract the
minimum valuation of its homogeneous coordinates. Coordinatewise
squaring agrees with the normalization map generically and hence
everywhere.

### 4. Does the hyperplane-bundle square descend to a singular image curve?

Not proved, and it need not be claimed. The safe statement is

\[
f^*\mathcal O_{\mathbf P^E}(1)
\cong \bigl(g^*\mathcal O_{\mathbf P^E}(1)\bigr)^{\otimes2}
\]

on the normalization \(\widetilde C\). The draft's language must not imply
that \(\mathcal O_C(1)\) itself has a square root through singularities of
\(C\).

### 5. Is the projective/affine normalization unambiguous?

The first draft was unnecessarily fragile here. State the map as

\[
\delta=[1:(s_e)_{e\in E}]\in\mathbf P^E.
\]

The added coordinate is not artificial: at fixed centered inertia,

\[
\sum_e m_i m_j s_e=M I_0,
\]

so \(X_0\) is a fixed linear combination of the squared-distance
coordinates on the image. This formulation makes each
\(s_e=X_e/X_0\) an honest function and makes the lift
\([1:(\rho_e)]\) immediate.

### 6. Could a degree-two image evade the pole argument through a
non-birational lift?

No. If \(\deg C=2\), the lifting bundle \(M=g^*\mathcal O(1)\) has
degree one. If \(D=g(\widetilde C)\) and \(k\) is the generic degree of
\(g\), then

\[
1=\deg M=k\deg D.
\]

Thus \(k=1\), \(D\) is a line, and \(\widetilde C\cong\mathbf P^1\).
Writing \(g=[L_0:(L_e)]\) in real linear forms reduces constant potential
to

\[
\sum_e w_e\frac{L_0}{L_e}=U_0.
\]

At any zero of a denominator different from the zero of \(L_0\), all
denominators with that zero are positive scalar multiples after orientation
on the physical interval. Their residues have one sign, so the pole cannot
cancel. Every \(L_e\) must be proportional to \(L_0\), contradicting
nonconstancy.

### 7. Does the result apply to every imaginable continuum?

The theorem directly concerns a physical arc whose full labelled
squared-distance image has an integral algebraic curve as its Zariski
closure. It should not be advertised as a theorem about an arbitrary
transcendental path with higher-dimensional closure.

For Smale's sixth problem this restriction is adequate: after polynomial
auxiliary distance variables and similarity normalization, a positive
fixed-mass fiber is semialgebraic. If it is infinite, semialgebraic curve
selection gives a nonconstant one-dimensional algebraic distance subarc.
This bridge should be stated separately as a corollary.

## Required revision

1. Use \(\delta=[1:s_e]\) and define the centered inertia convention
   explicitly.
2. Put the line-bundle square only on \(\widetilde C\).
3. State geometric integrality (or pass to the component containing a
   physical subarc).
4. Make the analytic-germ injection explicit in the splitting lemma.
5. Replace the draft's degree-two section argument by the degree-one lift
   and positive partial-fraction proof.
6. Preserve the hypotheses: full labelled distances, fixed masses and
   inertia, strict positivity, and collision freedom.
7. Label the result as a necessary complexity condition, not a finiteness
   theorem.

## Review conclusion

Subject to those corrections, the theorem is mathematically defensible:
every normalized squared-distance function splits in
\(\mathbb R(\widetilde C)\); the normalization factors through
coordinatewise squaring; the projective degree is even; and degrees
\(1,2,3\) are impossible for a nonconstant image.

Novelty is not adjudicated by this proof review; it is handled separately
in PRIOR_ART_MATRIX.md.
