# Program: the bubble wall as the single obstruction

Working program note, 2026-08-03. Ambitious framing of the warp-drive sequel.
Companion to `sequel_superluminal_catalogue.md`, which holds the computed cases.

---

## Thesis

> At a stationary scalar-shift wall generator, continuation, null energy, and
> transverse ray stability are three readings of the same geometric tensor:
> the transverse wall curvature \(H_{AB}\). Curvature sees the full tensor,
> matter sees its trace, and the ray phase portrait sees its eigenvalues.

For a semidefinite support point, this reduces to Claude's one-number statement:
the mean transverse curvature simultaneously gives the PP Ricci/source
coefficient and certifies a nonzero tidal tensor. In general the full tensor is
the sharper object: a tracefree saddle obstructs continuation without a leading
null-energy divergence, while a pointwise flat quartic germ requires
neighborhood flow rigidity. A genuine product patch makes all three readings
vanish, but pointwise \(H=0\) alone does not imply a product.

---

## Follow-up theorem audit, 2026-08-03

The maximality proof and the adversarial tests sharpen the program as follows.

1. **Radial maximality is profile-wide.** The global \(C^2\)-inextendibility
   proof does not use a special sech identity. It holds for smooth radial
   nonincreasing profiles with a unique simple \(v=-1\) sphere and an exactly
   constant or uniformly short-range tail. Compactly supported walls are
   included.
2. **A generic nonradial scalar-shift theorem survives.** If the exterior shift
   is exactly constant, \(\Sigma=\{v=-1\}\) is compact and regular, and the
   stationary-geodesic locus
   \[
   \mathcal G=\{v=-1,\ v_y=v_z=0\}
   \]
   is finite with \(H_{AB}\ne0\) at every member, every extension-supplied
   timelike exit is forced to one point of \(\mathcal G\), where the full tidal
   Hessian gives a \(C^2\) contradiction. A Morse height function on
   \(\Sigma\) is a clean sufficient condition.
3. **The one-scalar thesis is a convex corollary, not the general theorem.**
   The curvature obstruction sees \(H_{AB}\), while \(T_{KK}\) sees
   \(\operatorname{tr}H\). At a semidefinite support point they coincide. At a
   saddle, \(H_{AB}\ne0\) and \(\operatorname{tr}H=0\) can occur.
4. **Pointwise flatness is not a product germ.** The quartic support
   \(F=-y^4-z^4\) has \(H_{AB}=0\) at a strict maximum. The Hessian test does
   not see it. The attempted stationary-flow proof overread anchored-extension
   uniqueness: it gives one-sided isometry data, not a two-sided isometry germ.
   This infinitely flat nonproduct rim remains a genuine boundary-rigidity
   problem even at smooth regularity.
5. **Exact open product caps are genuine local exceptions.** A smaller cap
   patch can be glued to the regular product extension without adding its rim.
   Universal full \(C^2\)-inextendibility is therefore false in that class.
   No simultaneous *regular geodesic* resolution of the entire generator
   family remains a plausible ceiling, but is not yet proved.
6. **Natário's local coefficient is now closed.** At the simple front root,
   \[
   R_{tyty}=R_{tztz}
   =-\frac{\kappa(3R_F\kappa+8)}{4R_F}<0.
   \]
   The local PP and negative-null-source divergences hold for every simple-root
   profile. Global \(C^2\) maximality is now proved for the monotone-wall
   profile class. Natario's poloidal streamfunction supplies
   \(d\Psi/dt=\pm\varrho\sqrt{|X|^2-1}\), and both possible branch-switch sets
   are strict local maxima of \(\Psi\). Hence a meridional limiting ray switches
   at most once. Conserved axial angular momentum causes no residual loophole:
   \(J/|P|\to0\) in every high-momentum omega-limit. The only bounded limiting
   orbits are the two axial equilibria; momentum growth selects the front,
   where the Ricci contraction diverges. At the front, the same
   local coefficient obeys
   \[
   R_{tyty}=\det
   \begin{pmatrix}\kappa/2&1\\2\kappa/R_F&-3\kappa/2\end{pmatrix},
   \]
   so it is simultaneously the PP tidal coefficient and the transverse
   stability determinant of the high-frequency ray. Its negativity forces the
   saddle and its stable approach direction.
7. **The exact \(C^2\) common-domain lemma is proved, but the scalar
   simultaneous-resolution ceiling is still open.** Genuine fixed-point
   local-isometry germs with pure-boost one-jets share a common neighborhood by
   a Baire-category argument in exponential coordinates. Anchored-extension
   uniqueness, however, supplies a map that is isometric only on the original
   one-sided region; the metric beyond the boundary is unconstrained. Thus it
   does not furnish the germs needed by that lemma, even smoothly. The
   remaining scalar problem is the one-sided noncollapse/holonomy lemma at an
   infinitely flat cap rim.

The detailed proofs and audits are in scalar_shift_followup_theorem.md and
vector_shift_and_finite_duration_audit.md.

---

## What is already established

**From `paper/main.tex`, §5.3.** At a stationary finite-affine generator, with
\(B_A = v_{xA}\) and \(H_{AB} = v_{AB}\):

    R_KNKA = -B_A q          R_KAKB = H_AB q²
    G_KA   = -B_A q          G_KK   = q²(H_yy + H_zz)

**The same \(H_{AB}\) appears in both.** For a convex front,
\(R_{KYKY} = -C_1/[\kappa(\lambda_*-\lambda)^2]\) and
\(G_{KK} = -(C_1+C_2)/[\kappa(\lambda_*-\lambda)^2]\). The paper states both and
does not remark that they are the same tensor.

**Product limit, §5.1.** \(B_A = H_{AB} = 0\) on an open transverse neighbourhood
⟹ both vanish ⟹ the reduced extension lifts. The exceptional case is exactly
the case where the wall has no curvature.

**PG-Schwarzschild control, §3.** \(\partial_t\) geodesic on the *whole* horizon
⟹ \(B_{AB}=0\) ⟹ Sachs forces \(R_{KAKB}=0\) ⟹ extension exists.

## Evidence base — five computed cases

| geometry | surface | geodesic locus | bw +2 | verdict |
|---|---|---|---|---|
| Alcubierre | \(v^2=1\) | two axial points | \(H_{AB}q^2 \ne 0\) | obstructs |
| Natário (2026-08-03) | \(\|X\|=1\) | isolated points | \(-12.75\,q^2 \ne 0\) | obstructs |
| PG-Schwarzschild | \(r=2M\) | whole surface | 0 | extends |
| Ori pseudo-Schwarzschild | \(r=2\mu\) | whole surface | 0 | extends |
| Zeno product core | \(B=0\) | whole surface | 0 | extends |
| Zeno collar critical pt | \(B=0\) | isolated | \(-\tfrac12 f^2B_{AB}\ne0\) | obstructs |

The criterion predicted Natário's outcome before it was computed. That is the
only predictive success in this program so far and is the reason to attempt a
theorem rather than a catalogue.

---

> **REVIEW CORRECTION, same day.** The ordering below is wrong and is kept only
> so the reasoning is traceable. Four fixes:
>
> 1. **Theorem B is the thesis; Theorem A is its lemma.** A's part 1 — a Killing
>    horizon is non-expanding, hence \(R_{KAKB}=0\) — is textbook. The only
>    candidate novelty in A is part 2's formula and its use as a diagnostic. B is
>    the part that is actually ours: that \(R_{KAKB}\) and \(G_{KK}\) carry the
>    *same* \(H_{AB}\) sits in `main.tex` §5.3 unremarked, and nobody else has
>    computed both.
> 2. **The saddle test resolves in B's favour for every catalogued drive.** At the
>    axial generator of an *axisymmetric* bubble \(C_1=C_2\) by symmetry, so
>    tracefree forces \(C_1=C_2=0\) — no wall curvature at all. The exception
>    needs a non-axisymmetric bubble with a stationary generator at a saddle of
>    the profile, which nobody has constructed. Stage 1 is a paragraph, not a
>    project.
> 3. **"Generically \(H_{AB}\ne0\)" is a gap, not a hypothesis.** Split it: the
>    computation \(R_{KAKB}=H_{AB}q^2\), so the obstruction is present iff
>    \(H_{AB}\ne0\); plus a separate lemma characterising when \(H_{AB}=0\),
>    whose answer is essentially the product case.
> 4. **Name Rácz–Wald as the reference frame.** The dichotomy is, in one
>    sentence, *when does Rácz–Wald apply*. `main.tex` already discusses it and a
>    referee will ask immediately.

## Theorem A (dichotomy) — the actual prize

*Let \((M,g)\) be stationary with Killing field \(\xi\), and let
\(\Sigma = \{g(\xi,\xi)=0\}\) be a smooth surface to which \(\xi\) is tangent.
Let \(\mathcal G = \{p\in\Sigma : \nabla_\xi\xi \parallel \xi\}\) be the geodesic
locus, and suppose a stationary generator through \(p\in\mathcal G\) has
\(\kappa\ne0\), hence reaches finite affine parameter \(\lambda_*\).*

1. *If \(\operatorname{int}_\Sigma\mathcal G \ne \emptyset\), then on that open
   set \(\Sigma\) is a Killing horizon, \(B_{AB}=0\), and the Sachs equation
   forces \(R_{KAKB}=0\): no non-scalar obstruction, extension permitted.*
2. *If \(\operatorname{int}_\Sigma\mathcal G = \emptyset\), the stationary
   generators are isolated, no Sachs constraint applies, and*
   \[
   R_{KAKB} = H_{AB}\,q^2,\qquad q=\frac{1}{\kappa(\lambda_*-\lambda)},
   \]
   *with \(H_{AB}\) the transverse Hessian of the Killing norm. If
   \(H_{AB}\ne0\) the endpoint is a non-scalar curvature singularity and no
   \(C^2\) extension exists.*

**Why this beats a catalogue.** It covers all six rows above in one statement and
applies to warp drives not yet invented — and people keep inventing them.

**Third case to fold in, from the Zeno work:** \(\Sigma\) may fail to be null
away from a smaller set, in which case there are no generators at all and the
components are irrelevant however large. The full trichotomy is null-with-
congruence / not-null / null-without-congruence.

## Theorem B (unification) — the thesis proper

*Under the hypotheses of Theorem A(2),*
\[
R_{KAKB}=H_{AB}q^2,\qquad
T_{KK}=\frac{G_{KK}}{8\pi}=\frac{q^2}{8\pi}\,\delta^{AB}H_{AB}.
\]
*Hence the \(C^2\) obstruction is nonzero iff \(H_{AB}\ne0\), and \(T_{KK}\) is
unbounded below iff \(\operatorname{tr}H<0\). The two coincide except when
\(H_{AB}\) is nonzero and tracefree.*

### The falsification test, and it is sharp

The exception is real and checkable: a **saddle-shaped front** at the stationary
generator, \(C_1=-C_2\), would obstruct the extension while leaving \(T_{KK}\)
finite. If such a configuration is geometrically admissible for a closed bubble,
the two obstructions come apart and Theorem B is false as stated — reducing to
"the causal obstruction is strictly stronger than the energy-condition one,"
which is still worth having but is not a unification.

**This is the first thing to test, because it can kill the thesis cheaply.**
Note the stationary generator sits at a critical point of the profile restricted
to \(\Sigma\) (\(v_A=0\)), and the Hessian at a critical point can be indefinite,
so the question is genuinely open rather than obviously closed by Gauss–Bonnet.

---

## Theorem C (global rigidity) — the real ceiling

**Target statement, not yet a theorem:**

> **No wall shaping evades the obstruction globally.** No single Hausdorff
> \(C^2\) spacetime extension of a compact superluminal stationary bubble can
> resolve all of its finite-affine boundary generators.

This must be stated globally. A generator in the interior of an open planar cap
has a regular local product extension. The proposed no-go result is therefore
not that every generator is locally singular; it is that the local extensions
required around all finite-affine generators cannot be assembled with the
original finite bubble into one Hausdorff \(C^2\) extension.

Two elementary facts establish why compact bubbles are forced into the problem;
a third, genuinely global lemma remains to be proved.

**Fact 1 — a closed bubble always has a stationary generator, with no genericity
assumption.** \(\Sigma=\{v=-1\}\) is a level set, so \(\nabla v\perp\Sigma\). At
the frontmost point of a compact \(\Sigma\) (max of \(x\)) the normal is along
\(\partial_x\), hence \(v_A=0\) — precisely the stationary-generator condition of
Eq. (16). Front and rear both. The spherical case's two axial points are a
corollary, not an input; **no symmetry is used.**

**Fact 2 — a compact \(\Sigma\) is never a Killing horizon.** \(\partial_t\) is
geodesic on all of \(\Sigma\) iff \(v_A=0\) everywhere, i.e. \(\nabla v\parallel
\partial_x\) at every point. On a closed surface the normal direction varies.
Topology alone excludes the Killing-horizon branch. **This is the converse the
program was missing.**

**Fact 3 — the extreme point has semi-definite second fundamental form.** \(x\)
attains a maximum on \(\Sigma\) there, so \(F_{AB}\le0\). If \(F_{AB}\) is
nonzero, \(H_{AB}=\kappa F_{AB}\ne0\) and the PP obstruction bites. If it
vanishes or is degenerate, nothing pointwise forces a product: for example
\(F=-y^4-z^4\) has a strict maximum and zero Hessian without being locally
flat. The regularized-coordinate argument must instead show that a \(C^2\)
extension through a *neighborhood* of the endpoint forces \(F_A=0\) on an open
transverse set, not merely \(F_{AB}=0\) at one point.

**Missing Lemma C1 — local extension rigidity.** At a simple finite-affine
stationary generator, a \(C^2\) extension through a full endpoint neighborhood
forces a Killing-horizon or transverse-product germ. This must cover finite-order
degeneracy and \(C^\infty\)-flat but nonconstant transverse profiles.

**Missing Lemma C2 — simultaneous-extension/rim obstruction.** Let a compact
bubble contain open planar caps, so that each interior cap generator extends
locally. Prove that these product extensions cannot be assembled with the
transition region into one Hausdorff \(C^2\) spacetime resolving all incomplete
generators. The term
\[
g_{UA}=-\frac{F_A}{\kappa U}+O(U)
\]
is the candidate mechanism, but the present calculation proves only that a
single product chart cannot include points arbitrarily close to a nonproduct
rim. It does not yet exclude an atlas of smaller local cap extensions whose
domains avoid the rim.

Carry \(\kappa\ne0\) at the extreme generator as an explicit hypothesis; if it
vanishes, §5.4's degenerate-root analysis takes over and crossing geodesics still
see the divergence.

**Status: open at exactly one adversarial geometry.** Strictly curved support
points are already settled. The decisive case is a smooth compact bubble with
exactly planar open front and rear caps joined to the wall by \(C^\infty\)
transitions. Either Lemma C2 rules it out, giving the global theorem, or this
geometry is a counterexample and fixes the optimal result at local rigidity plus
a generic/strictly-convex compact-bubble theorem.

**Scope caveat — resist overselling.** Facts 2 and 3 both use *compactness of
\(\Sigma\)*, which is the warp-drive-specific input doing the real work. The
general result is the trichotomy; the rigidity is what compactness buys on top.
The honest general class is "stationary spacetimes whose Killing-norm zero set is
compact," which is real but narrow. Do **not** advertise this as a general
theorem about ergosurfaces.

**Required definition before proof.** "Resolves the finite-affine boundary" must
mean that every incomplete causal geodesic in the relevant stationary-generator
family acquires an endpoint in one Hausdorff \(C^2\) extension. Local
extendibility of one cap generator is deliberately weaker and is not what
Theorem C denies.

## Work plan, in the order the evidence says to run it

**Stage 0 -- Natario. Complete for a profile class.** The local coefficient,
the exact projectivized dynamics, the streamfunction branch-switching lemma,
the angular-momentum omega-limit reduction, and the global \(C^2\) curvature
contradiction are all closed. The hypotheses are a monotone inner
\(|X|=1\) wall with \(\partial_r|X|^2>0\) and an exact or exponentially
short-range exterior tail.

**Stage 1 — the saddle test. Largely resolved on inspection.** For an
axisymmetric bubble \(C_1=C_2\) at the axial generator, so tracefree ⟹
\(C_1=C_2=0\) ⟹ no wall curvature. **Theorem B is therefore safe for every
construction in the catalogue.** What remains is a remark: the exception requires
a non-axisymmetric front with a stationary generator at a saddle of the profile.
Write it as a scope statement, not a project.

**Stage 1b — attack the flat-cap counterexample.** First define the extension
claim precisely. Then construct a compact \(C^\infty\) level surface with exact
open planar front and rear caps and smooth nonproduct rims. Build the standard
product extension over the interior of each cap and determine whether all such
local extensions can coexist in one Hausdorff \(C^2\) manifold. Track sequences
approaching the rim from the cap and from the original spacetime. **This is the
highest-value step in the program:** failure of Hausdorffness, continuity, or
curvature control proves the missing global lemma; a successful atlas is a
counterexample to Theorem C and establishes the honest ceiling.

**Stage 1c — prove local rigidity.** Replace the pointwise condition
\(H_{AB}=0\) by a neighborhood statement derived from extension regularity.
Treat quartic transverse contact and a \(C^\infty\)-flat nonproduct profile
explicitly before stating the lemma. Do not use "degenerate Hessian" as a
synonym for "flat wall."

**Stage 2 — complete the catalogue.** Van Den Broeck pocket check (probably
inherits Alcubierre verbatim if the pocket doesn't reach the wall), then the
Lentz / Fell–Heisenberg solitons. *Mechanical; gives the paper its examples
whatever happens to the theorems.*

**Stage 3 — novelty check on Theorem A.** Against the isolated-horizon and
Killing-horizon-rigidity literature (Ashtekar–Krishnan; Rácz–Wald; the
non-Killing-horizon surface-gravity work of Cropp–Liberati–Visser). **High risk:**
"Killing horizons are non-expanding, so boost-weight +2 vanishes" is close to
standard, and the novelty is in the *converse* and in its use as a diagnostic.

**Stage 4 — write.** Shape depends on what survives Stages 1 and 3.

Deliberate ordering: calculations first, novelty check third. Across the 2026-08-02/03
sessions, novelty checks ran about one survivor in eight while every calculation
with a control returned something. Stage 3 is still necessary — it decides whether
this is a theorem paper or a catalogue paper — but it should not gate the cheap
work that is valuable either way.d

---

## Risk register

| risk | severity | mitigation |
|---|---|---|
| Theorem A is standard isolated-horizon theory | high prob., high impact | Stage 3; fall back to catalogue paper |
| Saddle front exists ⟹ Theorem B false | medium | Stage 1, before writing |
| "generically \(H_{AB}\ne0\)" needs a real hypothesis | medium | characterise when \(H_{AB}=0\) without the product structure |
| Open planar caps admit a global extension | high impact, unknown | construct the extension atlas or prove the rim is non-Hausdorff |
| Pointwise flatness does not imply a product germ | certain | prove neighborhood rigidity from extension regularity |
| Niche audience | certain | unavoidable; see below |

**On audience, honestly.** Nobody thinks warp drives are physical, and the
energy-condition objection already settled that. This is a "yes, obviously, but
nobody had shown it" result. The counterweight: BBV (arXiv:2602.16495) cite
FLB's Penrose diagrams seven times as authority while **explicitly excluding the
horizon problem from their own audit**, so an incorrect causal picture is
propagating unchallenged into careful work by a serious group. Correcting that is
worth doing whether or not warp drives are buildable.

---

## Fallback ladder

- **Theorem C holds** → strongest paper: no compact superluminal stationary
  bubble admits a single Hausdorff \(C^2\) extension resolving its finite-affine
  boundary; the wall-curvature/energy identity is the convex corollary.
- **C fails only for exact planar caps** → local-rigidity plus generic or
  strictly-convex no-go theorem, with the flat-capped geometry as the sharp
  exceptional class.
- **Theorems A and B hold but global rigidity fails** → PRD paper: *the two
  objections to standard superluminal warp drives are one object, the curvature
  of the wall.*
- **A holds, B fails on the saddle** → the causal obstruction is strictly stronger
  than the energy-condition one. Still a theorem paper, weaker thesis.
- **A is prior art** → catalogue paper: the obstruction across the superluminal
  catalogue, absent from subluminal. CQG-level.
- **Everything collapses** → Natário as a section in the existing paper. Already
  banked, with three consistency checks.

The floor is not zero, which is the main argument for continuing.

---

## References

**Already in `paper/references.bib`** — reuse these keys, do not re-enter:

- `Alcubierre1994` — M. Alcubierre, *The warp drive: hyper-fast travel within
  general relativity*, Class. Quantum Grav. **11**, L73 (1994).
- `FinazziLiberatiBarcelo2009` — S. Finazzi, S. Liberati, C. Barceló,
  *Semiclassical instability of dynamical warp drives*, Phys. Rev. D **79**,
  124017 (2009), [arXiv:0904.0141](https://arxiv.org/abs/0904.0141).
- `RaczWald1992` — I. Rácz, R. M. Wald, *Extension of spacetimes with Killing
  horizon*, Class. Quantum Grav. **9**, 2643–2656 (1992),
  [doi:10.1088/0264-9381/9/12/008](https://doi.org/10.1088/0264-9381/9/12/008).
  **The reference frame for Theorem A.**
- `EllisSchmidt1977` — G. F. R. Ellis, B. G. Schmidt, *Singular space-times*,
  Gen. Rel. Grav. **8**, 915–953 (1977),
  [doi:10.1007/BF00759240](https://doi.org/10.1007/BF00759240). The
  quasi-regular / non-scalar / scalar taxonomy.
- `MattinglyEtAl2021` — B. Mattingly *et al.*, *Curvature invariants for the
  Alcubierre and Natário warp drives*, Universe **7** (2021).
- `Rodal2023` — J. Rodal, *Visualization and analysis of the curvature invariants
  in the Alcubierre warp-drive spacetime*, Gen. Rel. Grav. **55**, 134 (2023),
  [arXiv:2512.20738](https://arxiv.org/abs/2512.20738).
- `BarzegarBuchertVigneron2026` — H. Barzegar, T. Buchert, Q. Vigneron, *General
  formalism, classification, and demystification of the current warp-drive
  spacetimes*, [arXiv:2602.16495](https://arxiv.org/abs/2602.16495). **Excludes
  the horizon problem from scope, p. 2.**
- `Sbierski2018`, `Visser1998`, `LemosSilva2021`, `GallowayLingSbierski2018`.

**To be added to the bib:**

- J. Natário, *Warp drive with zero expansion*, Class. Quantum Grav. **19**, 1157
  (2002), [arXiv:gr-qc/0110086](https://arxiv.org/abs/gr-qc/0110086). Def. 1.1
  (metric), Cor. 1.5 (θ = ∇·X), §2 p. 5 (the zero-expansion field).
- J. Rodal, *A closer look at Natário's zero-expansion warp drive*, Int. J.
  Theor. Phys. **63**, 168 (2024),
  [arXiv:2512.19837](https://arxiv.org/abs/2512.19837),
  [doi:10.1007/s10773-024-05700-0](https://doi.org/10.1007/s10773-024-05700-0).
  Scalar invariants + Petrov type I only.
- B. Cropp, S. Liberati, M. Visser, *Surface gravities for non-Killing horizons*,
  Class. Quantum Grav. **30**, 125001 (2013),
  [arXiv:1302.2383](https://arxiv.org/abs/1302.2383). **Also the outstanding
  citation gap in `paper/main.tex` — the v²=1 surface is exactly a non-Killing
  horizon and the draft uses κ as though unambiguous.**
- A. Ashtekar, B. Krishnan, isolated-horizons review, Living Rev. Relativ.
  **7**, 10 (2004), gr-qc/0407042. **Cited from memory — verify before use.**
  Needed for the Stage 3 novelty check on Theorem A.
- A. Ori, *Formation of closed timelike curves in a composite vacuum/dust
  asymptotically-flat spacetime*, Phys. Rev. D **76**, 044002 (2007),
  [arXiv:gr-qc/0701024](https://arxiv.org/abs/gr-qc/0701024). Source of the
  pseudo-Schwarzschild row in the evidence table.

**Cross-file, in this repo:**

- `sequel_superluminal_catalogue.md` — the Natário computation and the catalogue
  scoping; scripts `sim/natario_geodesic_locus.py`, `sim/natario_curvature_fd.py`.
- `../wormhole/ctc_warm_traversal_findings.md` — the criterion in both its forms;
  the Ori row; script `../wormhole/sim/ori_core_pp.py`.
- `../wormhole/zeno_chronology_transits_review.md` — the Zeno product-core and
  collar rows; scripts `../wormhole/sim/zeno_rim.py`, `zeno_normchar.py`.
