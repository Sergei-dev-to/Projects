# Adversarial theorem audit checklist

Working checklist, 2026-08-10.  This is a provisional review instrument, not a
claim that every hypothesis must be minimal or that every paper must maximize
generality.  Its purpose is to expose mismatches among theorem statements,
proofs, examples, citations, and interpretation.

## The checklist

### 1. Hypotheses and realizable exclusions

For every hypothesis:

1. Where is it used?
2. What fails if it is removed?
3. Is that failure realizable while the other hypotheses remain true?
4. Is the hypothesis geometric, technical, or merely a proof convenience?
5. If it looks like a normalization, is it genuinely without loss of
   generality?

Minimality is not required.  A stronger transparent hypothesis can be better
than a weaker one with greater cognitive cost, provided its role and excluded
cases are honest.

### 2. Scope of every inference

For every material statement of the form “X shows Y”:

1. Does X have the regularity, causal character, locality, and direction
   required for Y?
2. Are the same curve, endpoint, boundary component, frame, and extension used
   on both sides?
3. Does the cited theorem deliver Y itself, or only an ingredient for Y?
4. Is a local statement being promoted to a global one, or an existence result
   to uniqueness or maximality, without an additional argument?

### 3. Specific objects under general results

For every “this includes,” “applies to,” “follows as a corollary,” or named
control example, verify every hypothesis explicitly: sign, smoothness,
boundedness, compactness, regularity, decay, causal orientation, and any
nondegeneracy condition.  Record a parameter map or direct calculation rather
than relying on resemblance.

### 4. Definitions before use

Every technical term should be defined, paraphrased, or standard enough for
the intended audience before its first substantive use.  Check the body before
the appendices: a definition deferred to an appendix does not introduce a term
already used in the main argument.

### 5. Quantifiers and identities

Track “for every,” “there exists,” subsequences, fixed versus shrinking
neighborhoods, and uniform constants.  Confirm that objects bearing the same
name are actually identical after coordinate changes, Killing translations,
normalizations, and limiting procedures.

### 6. Regularity and implication direction

For every external or internal theorem, record:

- assumed and concluded differentiability;
- timelike, null, or general causal scope;
- future, past, or two-sided scope;
- the direction in which the result is used.

An implication valid at lower regularity may be used at higher regularity, but
not conversely without explanation.

### 7. Conclusion strength

Distinguish:

- an incomplete curve from a singular endpoint;
- obstruction at one endpoint from inextendibility of the spacetime;
- existence of a proper extension from its uniqueness or maximality;
- local continuation from a new global end;
- bounded curvature on one curve from neighborhood or boundary regularity.

### 8. Branch witnesses and boundary cases

For an alternative or if-and-only-if theorem, exhibit a realizable witness for
each branch.  Identify excluded boundary regimes and say whether they are
impossible, covered elsewhere, or genuinely open.  Test intersections of
exceptions rather than only one-at-a-time removals of hypotheses.

### 9. Worked examples that precede the general theory

A concrete computation placed before the abstract result it illustrates is
normally written first and re-anchored last.  It therefore tends to carry
private notation that the later sections silently assume is the general
notation.  Consistency is not enough: the identification must be visible to a
reader who has not recomputed it.

For every symbol, coordinate, constant, or named quantity occurring in both the
example and the general theory:

1. Is it introduced by a closed-form value, or by its geometric meaning?  A
   symbol introduced only as a formula has no stated referent.
2. Is its identification with the general object stated where the reader first
   meets it, rather than derivable from an expansion many lines later?
3. If the example uses a specialized coordinate or restriction — axial,
   planar, polarized, equatorial — is its relation to the general coordinate
   stated?
4. Would a reader who took the example's notation literally land on a
   *different branch* of the general theorem?

Item 4 is the severity test.  A merely invisible identification costs the
reader time; one that reads as a different object in the general classification
can invert the conclusion.

This check differs from §5.  There the question is whether same-named objects
really are identical after transformations; here they are identical, and the
defect is that the text never says so.

## Trial audit: current Alcubierre draft

Target: `paper/main.tex` as of 2026-08-10.

Status: completed.  No new mathematical defect was found.  The audit did expose
two deliberately redundant hypotheses and confirmed which restrictions are
load-bearing rather than normalizations.  A later pass under check 9 found
three previously unstated example-to-theory identifications, and a rerun after
the rim proposition was added found two missing statement-level qualifications.
Both sets have now been corrected in the draft; see §9 and the supplemental
rim pass below.

### 1. Hypothesis audit

| Hypothesis or structural restriction | Role in the argument | What happens if it is removed? | Verdict |
|---|---|---|---|
| Stationary unit-lapse, flat-slice scalar shift on \(\mathbb R^4\) | Gives the conserved Killing energy, the capture system, the simple transverse geodesics, and the explicit cap coordinates. | Time-dependent or vector shifts are readily realizable, but the proof no longer applies. | Structural definition of the theorem's class, not a disposable caveat. |
| \(v\) smooth | Supplies the geodesic flow, curvature, Hadamard factorization, and smooth gluing. | Lower-regularity profiles are realizable but require a different formulation of both curvature and extension. | Intentionally stronger than the nominal \(C^2\) target. |
| \(v\) bounded | Used transparently in the causal-speed/global-hyperbolicity argument. | Under the stated smoothness and exterior-tail hypothesis it is automatic: the exterior is bounded and the remaining spatial region is compact.  Thus no profile satisfies all the other hypotheses while violating this one. | Logically redundant but useful as a signpost. |
| \(v\leq0\) | Fixes the late-time sign \(P>0\) in capture and makes \(\Sigma=\{v=-1\}\) the entire stationary-limit set \(\{|v|=1\}\). | A realizable sign-changing profile can have a rounded \(v=-1\) wall and a separate \(v=+1\) planar cap.  The local cap then extends although a criterion inspecting only \(v=-1\) would miss it. | Load-bearing and not a coordinate normalization.  The theorem now says this explicitly. |
| \(v_s>1\) | Produces the strictly negative exterior drift \(v_s-v_s^{-1}>0\) used to exclude spatial infinity. | Critical or subluminal exteriors are realizable, but the excursion estimate and the physical regime change. | Load-bearing superluminal demarcation. |
| Exactly constant or exponentially short-range exterior | Makes a nonreturning exterior ray have linearly growing radius and integrable \(|\nabla v|\), preventing momentum blow-up at spatial infinity. | Slower tails with an integrable radial gradient envelope are realizable and appear to be covered by the same proof after a more technical restatement; nonintegrable or oscillatory tails need not be. | A transparent sufficient condition, stronger than necessary by choice. |
| \(\Sigma=\{v=-1\}\) compact | Used throughout capture and transverse rigidity. | It is also automatic from \(v\to-v_s<-1\) uniformly: the level set is closed and absent outside a sufficiently large ball. | Logically redundant under the tail hypothesis, but it states the geometry the theorem classifies. |
| \(\Sigma\) regular, \(dv\ne0\) | At \(\mathcal G\), converts \(v_A=0\) into \(v_x\ne0\), hence nonzero inaffinity and the nondegenerate cap alternative. | Smooth walls on which \(dv=0\) are realizable.  The radial degenerate case is covered separately by the corollary; the general nonradial degenerate class is not classified. | Load-bearing boundary of Theorem 1, stated honestly. |
| Open planar disk with constant \(v_x=-\kappa\ne0\) | Necessity follows from the two positive-boost-weight curvature equations on a fixed disk; sufficiency follows from the explicit Kruskal attachment. | Pointwise flatness, a shrinking disk, or nonconstant inaffinity does not give a regular transverse neighborhood. | Sharp within the regular one-sign class. |

The audit therefore does **not** recommend deleting every redundant assumption.
Writing "bounded shift" and "compact wall" makes the theorem easier to parse,
even though the tail condition implies both.  It does recommend retaining the
sentence explaining why \(v\leq0\) is not without loss of generality.

### 2. Scope-of-inference audit

| Inference in the draft | Scope check | Result |
|---|---|---|
| A nonzero tidal form on a null orbit gives a finite-affine curvature endpoint. | Proposition `prop:tidal-amplification` also requires completeness of the Killing field and nonzero inaffinity.  Those conditions hold for the stationary generators to which it is applied. | Pass.  It proves a local endpoint obstruction, not global inextendibility by itself. |
| A proper extension supplies a finite-proper-time timelike exit. | Galloway--Ling--Sbierski Theorem 2 assumes a smooth (at least \(C^2\)) globally hyperbolic spacetime and any \(C^0\) extension, and concludes that a timelike geodesic has an endpoint on the boundary.  A \(C^2\) extension is therefore more than sufficient. | Pass. |
| Capture plus extension regularity forces a planar constant-inaffinity disk. | Capture supplies a subsequential limit in \(\mathcal G\).  The extension argument uses the same boundary geodesic, obtains a disk radius uniform in the subsequence from an open geodesic-flow domain and compact limiting disk, and uses Killing translation only after identifying the curves on the common original region. | Pass.  The fixed, rather than shrinking, disk is explicit. |
| The future necessity proof also covers past extensions. | The map \(T=-t\), \(X=-x\), \(\widehat v(X,Y,Z)=v(-X,Y,Z)\) preserves the scalar-shift form, sign, tail, compactness, and regularity. | Pass. |
| The radial corollary covers \(\kappa=0\). | Its proof invokes capture and the forced planar disk, neither of which needs regularity.  It does not invoke the finite-affine local lemma. | Pass.  The different mechanism is stated explicitly. |
| The cap rim has no \(C^2\) endpoint. | The earlier timelike-capture argument would not cover this null generator.  The current proposition instead proves endpoint-frame convergence directly and then derives nonuniform transverse curvature blow-up. | Pass after the dedicated rim proof; no timelike/null scope leak remains. |
| Finite-duration shifts are complete and \(C^0\)-inextendible. | Choquet-Bruhat--Cotsakis gives future timelike and null completeness under the integrable extrinsic-curvature bound; the draft explicitly applies it in either time direction.  Galloway--Ling--Sbierski Theorem 1 then gives \(C^0\)-inextendibility from timelike completeness and global hyperbolicity. | Pass. |

No local existence statement is used as a claim of a unique or globally maximal
cap completion.  The paper proves that a proper cap extension exists; it does
not claim to have classified all further extensions of that new spacetime.

### 3. Named examples and corollaries

| Object | Explicit hypothesis check | Result |
|---|---|---|
| Sech Alcubierre family \(v(r)=\alpha[\operatorname{sech}(r/a)-1]\), \(\alpha>1\) | Smooth at the origin, nonpositive and radially nonincreasing, \(v(0)=0\), limit \(-\alpha<-1\), unique \(v=-1\) sphere at \(R_F=a\operatorname{arcosh}[\alpha/(\alpha-1)]\), and exponential tail with rate \(1/a\). | Satisfies the radial corollary. |
| Smooth compact-transition radial profiles | Included only when they have the stated sign, monotonicity, unique \(v=-1\) sphere, and constant exterior. | Correctly qualified by the corollary's hypotheses. |
| Compact flat-cap construction | \(W\) can be chosen with range \([-v_s,0]\); \(\Phi=0\) is smooth, compact, connected, and has two open planar caps; the exterior is exactly constant; \(v_x=\mp2cL\) is constant and nonzero on the cap interiors. | Realizes the extendible branch of the theorem. |
| Rounded radial wall, including the degenerate \(\kappa=0\) case | Its \(v=-1\) level is a sphere and therefore contains no open planar disk. | Realizes the inextendible branch and the principal boundary case. |
| Painleve--Gullstrand Schwarzschild control | A direct curvature calculation gives \(R_{t\theta t\theta}=M(r-2M)/r^2\) and \(R_{t\phi t\phi}=M(r-2M)\sin^2\theta/r^2\), so the screen tidal tensor vanishes at \(r=2M\), consistently with the regular Kruskal horizon. | Pass.  It is a local control example, not claimed to lie in the scalar-shift theorem class. |
| Subluminal profiles | If \(|v|<1\), then \(\{|v|=1\}\) is empty. | The statement that this particular stationary-limit obstruction is absent is tautologically correct; no stronger regularity claim is inferred from it. |

### 4. Definitions-before-use audit

- "Screen" is now introduced in the main text as "transverse, or screen,
  components" before the Painleve--Gullstrand comparison and the later formal
  quotient definition in the appendix.
- "Regular" is defined in the theorem as \(dv\ne0\) on \(\Sigma\).
- Inaffinity is standard terminology for the intended relativity audience, and
  the defining equation \(\nabla_\chi\chi=\alpha\chi\) appears before it is used
  in an argument.
- "Tidal form" is summary language in the Introduction and is formally defined
  at the start of the proof appendix before any proof depends on it.
- No symbol needed to interpret Figure 1 is introduced only in the caption or
  after the figure.

No undefined technical term affecting a proof was found.

### 5. Quantifiers and identities

- The capture result concludes only subsequential convergence to
  \(p\in\mathcal G\); the rigidity proof requires only that subsequence and does
  not silently assume convergence of the full exit.
- The transverse radius \(\delta\) is fixed independently of all sufficiently
  large \(n\).  Compactness of the limiting data disk inside an open flow domain
  supplies the uniformity.
- The observer vectors, rather than the scalar-shift coordinate vectors, are
  the bounded objects in the extension chart.  The proof does not identify
  boundedness in one chart with boundedness after stationary translation.
- The theorem's existential cap criterion matches both directions: any
  extension forces at least one cap, and any one cap produces a proper
  extension.  It does not require every stationary generator to extend.
- The two cap signs and the two time directions are related by stated
  reflections; no global sign flip is treated as a normalization of a
  sign-changing profile.

### 6. Regularity and direction of cited results

| Result | Assumptions actually needed here | Direction used | Result |
|---|---|---|---|
| Galloway--Ling--Sbierski Theorem 2 | Original spacetime smooth/at least \(C^2\), time-oriented, globally hyperbolic; extension \(C^0\). | Extension implies a timelike boundary geodesic. | Valid for the assumed \(C^2\) extension a fortiori. |
| Galloway--Ling--Sbierski Theorem 1 | Smooth/at least \(C^2\), timelike geodesically complete, globally hyperbolic. | Completeness implies \(C^0\)-inextendibility. | Used only for finite-duration shifts. |
| Choquet-Bruhat--Cotsakis Theorems 2.1 and 3.2 | Complete uniformly controlled slices, bounded lapse and shift; integrable lapse gradient and extrinsic curvature for completeness. | Slicing bounds imply global hyperbolicity; time-integrable deformation implies future completeness. | Unit lapse and flat slices meet the geometric hypotheses; time reversal supplies the past statement. |
| Racz--Wald local extension theorem | A nondegenerate constant-surface-gravity Killing horizon with a suitable cross-section. | Identifies the local cap geometry with the known branch. | The paper does not delegate global gluing to this citation; it supplies explicit coordinates and the Hausdorff argument. |

The paper consistently asks for \(C^2\) when curvature continuity is used and
does not promote a \(C^2\)-inextendibility result to lower regularity.  The
separate finite-duration conclusion is stronger because it uses completeness
and a \(C^0\) theorem.

### 7. Conclusion-strength audit

- The local null-orbit calculation proves a finite-affine parallel-propagated
  curvature singularity at the rounded front/rear generators.  Global
  inextendibility comes only after the GLS and capture-rigidity steps.
- The cap construction proves existence of a proper smooth extension, not its
  uniqueness and not the maximal extension of the extended spacetime.
- The rim proposition distinguishes bounded curvature on the generator from
  regularity of a transverse neighborhood.  It proves no \(C^2\) endpoint for
  that generator but does not label it quasi-regular or claim a complete
  classification at lower regularity.
- "Already its own maximal Hausdorff \(C^2\) extension" in the radial corollary
  is exactly the no-proper-extension conclusion, not a claim about the reduced
  \(1+1\) metric.

### 8. Branch witnesses and boundary regimes

- **Inextendible regular branch:** the sech family and ordinary rounded radial
  profiles.
- **Extendible regular branch:** the compact connected flat-cap construction.
- **Degenerate boundary:** radial \(\kappa=0\) walls are covered by the radial
  corollary through global rigidity rather than finite-affine blow-up; general
  nonradial nonregular walls remain outside Theorem 1.
- **Aperture boundary:** the cap-rim generator is pointwise curvature-bounded
  but has no \(C^2\) endpoint because every transverse neighborhood encounters
  the curved side.
- **Sign-changing boundary:** explicitly excluded because \(v\leq0\) is
  load-bearing, not a normalization.
- **Different model classes:** persistent vector shifts, general time-dependent
  shifts, and lower-regularity extensions are not silently claimed.

### 9. Example-to-theory identifications

Section 2 computes the sech chart before Section 3 states the general result.
Three symbols are shared.  All three identifications are **true** — each was
checked by direct computation — but the audited version did not state them
where the reader met them.

| Section 2 object | General-theory object | Identification | Stated? |
|---|---|---|---|
| \(v(\xi)\), axial profile | \(v(r)\), radial profile | \(r=\lvert\xi\rvert\) on the axis; agrees because \(\operatorname{sech}\) is even | Yes: the bridge before Theorem 1 states that Section 2 is the axial restriction |
| \(\kappa=(\alpha/a)\sqrt{\beta^2-1}/\beta^2\), "local peeling scale" | \(\kappa=-v_x\), inaffinity | Both equal \(\sqrt{2\alpha-1}\,(\alpha-1)/(a\alpha)\); difference vanishes identically | Yes: the bridge identifies \(\kappa=|v_x|\), with \(-v_x=-v_r(R_F)\) at the front |
| \(\xi_2=a\operatorname{arcosh}\beta\), horizon location | \(R_F\), wall radius | Equal, since \(\operatorname{sech}(R_F/a)=1/\beta\) | Yes: the bridge states \(\xi_{1,2}=\mp R_F\) |

The second row was found only by computing both routes and comparing.  The
agreement is exact, but the version under audit did not make it visible.

The first row was the one that failed item 4.  Section 2 writes \(\xi=x\) "to
avoid conflict with the radial coordinate used later."  A reader who takes
\(v=v(\xi)\) literally as a four-dimensional profile has the exact planar
product \(v=v(x)\) — whose wall is a noncompact plane, and which sits in the
*extendible* branch of the theorem.  The intended reading is the axial
restriction of a radial profile, which is in the inextendible branch.

Remedy applied: one sentence at the start of the general section identifies
Section 2's \(\xi\), \(\kappa\), and \(\xi_2\) with the axial restriction, the
inaffinity, and the wall radius.  This is cheaper than three separate patches
and fixes the class rather than the instances.

### Supplemental pass: endpoint-frame lemma and flat-cap rim

These approximately fifty lines were added after the initial trial audit.  A
fresh pass through checks 1--8 gives:

| Check | Endpoint-frame lemma | Flat-cap rim proposition | Result |
|---|---|---|---|
| 1. Hypotheses | It needs an affinely parametrized future causal geodesic, a **finite** affine endpoint, convergence to a point of a \(C^2\) extension, and a local relatively compact chart with temporal coordinate.  The chart and temporal coordinate exist locally; the finite-affine condition was used but not stated. | It uses the preceding compact example, including \(0<a<b\), \(L,c>0\), \(W\) affine near the wall, and the infinitely flat transition of \(\psi\) at \(\rho=a\).  All are explicit and jointly realizable. | Pass after adding \(\lambda_*<\infty\) to the lemma. |
| 2. Inference scope | The proof treats causal, hence null, geodesics directly.  It does not invoke the timelike GLS/capture route. | The hypothetical endpoint supplies limits of the same generator tangent and transverse parallel vector used to launch the geodesic family. | Pass; no timelike/null substitution. |
| 3. Specific object | For the constructed front rim, \(v=-1\), \(v_x=-2cL\), and every transverse derivative of \(v\) vanishes on the generator. | Thus \(q=q_0e^{2cLt}\), the future affine length is finite, and the curvature on the generator is bounded. | Pass by direct substitution into the construction. |
| 4. Definitions | “Temporal coordinate,” “parallel vector,” and “affine tangent” are standard; the cap, rim, and generator have already been constructed. | “Parallel-propagated curvature” is used in its standard componentwise sense and is demonstrated in the displayed null frame. | Pass. |
| 5. Quantifiers and uniformity | Compactness of the normalized causal-cone slice gives a uniform \(C\) in \(|f'|\leq Cf^2\).  The fixed transverse radius follows from compact limiting data inside an open flow domain. | One angular point was computed although the proposition says “each circular” generator.  Axisymmetry supplies the rest, and the rear is the time reverse. | Pass after stating the rotational-symmetry step. |
| 6. Regularity | A \(C^2\) metric has continuous curvature and \(C^1\) Christoffel symbols; the geodesic and parallel-transport equations have the required uniqueness and continuous dependence. | The contradiction uses only continuity of Riemann and convergence of the transported frame, exactly the \(C^2\) endpoint data. | Pass. |
| 7. Conclusion strength | The lemma concludes finite limits for the tangent and parallel vectors, not extension of a whole neighborhood. | The proposition concludes that this null generator has no \(C^2\) endpoint.  It does not claim a quasi-regular classification, lower-regularity obstruction, or a maximal extension. | Pass. |
| 8. Branch and boundary witness | The cap interior is a realized smooth extendible branch. | Its rim is a realized boundary case: curvature is bounded on the generator but diverges on every fixed transverse neighborhood. | Pass; this is the intended nonuniform obstruction. |

The analytic core of the endpoint-frame lemma also checks independently.  With
\(f=dT(K)>0\), compactness of the causal vectors normalized by \(dT=1\) gives
\(|f'|\leq Cf^2\), hence \(|(1/f)'|\leq C\).  If \(f\) were unbounded along a
sequence approaching \(\lambda_*\), then
\(1/f(\lambda)\leq C(\lambda_*-\lambda)\), forcing
\(\int^\lambda_* f\,d\lambda=\infty\), contrary to convergence of \(T\).
Bounded \(K\), followed by the geodesic and parallel-transport equations, gives
the asserted limits.

## Evaluation of the checklist

The trial was useful.  It recovered the previously missed sign issue and the
timelike-versus-null rim attribution as exactly the kinds of errors checks 1,
2, and 7 are designed to find.  The rerun found no new mathematical defect, but
did catch an unstated finite-affine hypothesis and an implicit symmetry step.
More generally, the audit distinguished harmless redundancy from hidden
load-bearing scope and forced every named example through the actual
hypotheses.

Keep the checklist.  Its best use is after a theorem or corollary changes, and
again before submission.  It is not a substitute for line-by-line algebra or
bibliography verification; those are separate audits.
