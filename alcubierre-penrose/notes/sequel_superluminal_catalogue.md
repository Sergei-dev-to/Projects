# Sequel: horizon extendibility across the superluminal warp-drive catalogue

Working note, 2026-08-02. Continues `paper/main.tex`, now titled **"Warp Horizons
as Curvature Boundaries: The Eternal Alcubierre Spacetime and Beyond."**

> **STATUS 2026-08-04 — the scope of this note has shrunk, because paper 1 grew.**
>
> The **general scalar-shift maximality theorem is now IN paper 1**, not here. Paper 1
> proves global \(C^2\)-inextendibility for any stationary scalar shift with a
> compact regular wall and nonzero transverse Hessian on its stationary-generator
> locus (Morse height sufficient; finiteness of \(\mathcal G\) not assumed). So
> "generalize off the sech profile" is **done and shipped**.
>
> What remains for the sequel is the **vector-shift** case, which paper 1 explicitly
> disclaims. Natário is done both locally (below) and globally
> (`natario_global_maximality_proof.md`), by a genuinely different technique —
> poloidal streamfunction, branch-switching lemma, \(\omega\)-limit sets — because
> the scalar route (ratio equation + Barbălat) does not survive to a vector shift.
>
> **The sequel's known weakness**: its hypotheses are *profile conditions*
> (single wall, \(\partial_rS^2>0\), \(f,f'\ge0\), simple front root), where paper 1's
> are *geometric* (compact, regular, Morse). Finding the vector-shift analogue of the
> Morse condition — stated invariantly rather than as radial monotonicity — is the
> prize for paper 2 and is what would make it as strong as paper 1.
>
> Still untouched: **Van Den Broeck pocket check**, solitons.

## The target

Apply the paper's diagnostic to the rest of the superluminal warp-drive
catalogue. The instrument already exists and is independently verified: locate
the finite-affine null generator, build the parallel-propagated frame, compute
the boost-weight +2 components, with PG-Schwarzschild as the control that tells
you when the answer is "extends."

## Why it is open — primary source, not a keyword search

Barzegar, Buchert & Vigneron, arXiv:2602.16495, "General formalism,
classification, and demystification of the current warp-drive spacetimes," is
the field's current audit paper. It catalogues the literature, classifies it,
and proves no-go theorems. On p. 2 it states its own scope:

> "as a consequence of Principle I, we do not consider: (i) quantum theoretical
> aspects of such spacetimes, such as quantum inequalities, **(ii) the horizon
> problem** (except from the discussion around the global hyperbolicity in
> Section IV A), (iii) proposals in theories beyond GR"

They exclude horizons deliberately, while auditing everything else. This is
stronger evidence than the earlier keyword check (their source has zero
occurrences of conformal diagram, maximal extension, extendib/inextendib,
parallel-propagated, Kretschmann — recorded 2026-07-29).

Second clarification from the same source: **"the horizon problem" in this
literature means something else.** BBV attribute it to Krasnikov and to
Everett–Roman — a crew cannot create or control a superluminal bubble on
demand, i.e. causal disconnection of the front from the rider. That is a control
problem. Extendibility through the horizon is a different question, and nobody
in the chain is asking it.

## Scope boundary — this is the thesis, not a limitation

The diagnostic needs a \(|v|\ge1\) surface, so that \(\partial_t\) goes null and
a generator reaches it at finite affine parameter. That partitions the
catalogue.

**In scope (superluminal):** Van Den Broeck, Natário, the Lentz and
Fell–Heisenberg soliton family, and the Abellán, Bolívar, Fuchs and Helmerich
follow-ups BBV lists. Alcubierre is done.

**Out of scope by construction:** Bobrick–Martire's main result is the first
general model for *subluminal* positive-energy spherically symmetric warp
drives. No superluminal region, no null \(\partial_t\), no finite-affine
endpoint. The obstruction cannot bite.

**Probably exclude:** the Krasnikov tube — different global structure, should
not be forced into the same frame.

Because the boundary is the result, this is **one paper, not several**. The
statement is positive and requires nobody to be wrong: the non-scalar curvature
obstruction is the price of superluminality, and the subluminal constructions
avoid it precisely by giving up the superluminal regime. Bobrick–Martire come
out vindicated rather than corrected.

## Gate before computing anything

Novelty currently rests on BBV's scope exclusion, which is strong evidence about
BBV and weak evidence about the whole literature. **Read "A Closer Look at
Natário's Zero-Expansion Warp Drive" first** (surfaced 2026-08-02, not yet
read). Same discipline that killed the Killing-tensor target in six searches —
see `ai-open-problem-screen/physics/CANDIDATES.md`.

## Work plan

**Step 1, cheap, decides the paper's shape.** Does the Van Den Broeck pocket
reach the \(|v|=1\) surface? VdB is designed for a large interior volume behind
a *small* surface area, so the conformal factor \(B\) plausibly returns to 1
well inside the shift wall. If so, \(B=1\) at the front axial point and VdB
inherits the Alcubierre result verbatim — trivial rather than interesting.
(Note: on 2026-08-02 I initially called VdB the case most likely to break the
result. That was probably wrong, for this reason.)

**Step 2, the actual work: Natário.** The zero-expansion construction uses a
genuine divergence-free shift vector field, not \(v(r)\partial_x\), so the
front-axial-point analysis must be redone from scratch: where is
\(\partial_t\) null, where is it *also* geodesic, does a generator reach the
boundary at finite affine parameter, and only then compute \(H_{AB}\).

Expectation: \(\nabla\cdot X=0\) is one scalar condition and \(H_{AB}\) is a
symmetric 2-tensor, so it should survive generically. But "zero expansion saves
it" is exactly the objection a referee will raise, and settling it is the core
of the paper.

**Step 3:** soliton family. Should be mechanical once the method is set up.

## RESULT 2026-08-03 — Natário obstructs. Zero expansion does not save it.

Scripts: `sim/natario_geodesic_locus.py` (symbolic), `sim/natario_curvature_fd.py`
(finite-difference curvature).

### Gate passed first

**Rodal, "A Closer Look at Natário's Zero-Expansion Warp Drive," IJTP 63:168
(2024), [arXiv:2512.19837](https://arxiv.org/abs/2512.19837),
doi:10.1007/s10773-024-05700-0** — the only recent dedicated paper. It is
**scalar curvature invariants and Petrov classification only**: it establishes
Natário is **Petrov type I** (as Alcubierre is) and compares invariant
amplitudes. No horizons, no extendibility, no causal structure.

**The monoculture is documented three times over, by two disputing parties.**
`MattinglyEtAl2021` (already in the bib) is literally titled *"Curvature
Invariants for the Alcubierre **and Natário** Warp Drives"*; `Rodal2023`
critiques it on the Alcubierre side; and Rodal 2024 redoes Natário. So the
Natário scalar-invariant question has been worked by two groups who disagree
with each other — **and neither side computes anything about causal structure or
extendibility.** That is a stronger monoculture statement than the earlier "twice
by the same person," and it is the one to use.

### Setup

Natário (gr-qc/0110086) Def. 1.1 is the same ADM form as our Eq. (5):
`ds² = -dt² + h_ij(dx^i - X^i dt)(dx^j - X^j dt)`, with expansion `θ = ∇·X`
(Cor. 1.5). His explicit zero-expansion field (§2, p. 5), in orthonormal
spherical components with **x** as polar axis:

    X^r̂ = -2 v_s f(r) cos θ,   X^θ̂ = v_s (2f + r f') sin θ,   X^φ̂ = 0

with f → 1/2 at large r, f → 0 at small r. Converted to Cartesian:

    X^x = -v_s [ 2f x² + (2f + r f')(y²+z²) ] / r²
    X^y =  v_s f' x y / r
    X^z =  v_s f' x z / r

Checks: `f→1/2, f'→0 ⟹ X → (-v_s,0,0)`; `div X = 0` verified identically.

### Step 1 — the geodesic locus. Case 3, same as Alcubierre.

**Control first.** For Alcubierre (`X = v(r)∂_x`, i.e. `X^r̂ = v cosθ`,
`X^θ̂ = -v sinθ`) the script gives, on `v² = 1`:

    a^t = v' cosθ,   a^r = v' sin²θ,   a^θ = v' sin2θ/(2r),   a^φ = 0

so the spatial part vanishes **iff sinθ = 0** — the two axial points, reproducing
Eq. (16) of the paper.

**Natário.** `|X|² = v_s²[4F² + 4F F' r sin²θ + F'²r² sin²θ]`. On the axis, with
the on-shell condition `4v_s²f² = 1`, the `a^r` terms carry an overall
`(cos 4θ - 1)` which vanishes at θ = 0, and `a^θ = a^φ = 0` identically, leaving
only `a^t = -2 v_s f'`. So **∂_t is geodesic at the axial points.** On the
equator `a^r = v_s(6f - r²f'')/r - 3/r`, which vanishes only if the profile
satisfies `6f - r²f'' = 3/v_s` — a condition, not an identity. Elsewhere
`a^θ ∝ sinθ cosθ × [bracket] ≠ 0`.

> **∂_t is null on the whole |X| = 1 surface but geodesic only on isolated
> points.** No generator congruence, no Sachs constraint. This is case 3 of the
> criterion, exactly as predicted.

### Step 2 — the curvature. Nonzero.

Finite-difference evaluation at the front axial point with an explicit profile
`f(r) = ¼(1 + tanh σ(r-r₀))`, `v_s = 2`, `r₀ = R_F = 1`, `σ = 3`:

| quantity | value | check |
|---|---|---|
| `X^x` | `-1.0` | matches the v = -1 convention |
| `|X|²` | `1.0` | on the surface |
| `κ = Γ^t_tt` | `-2.99999991` | predicted `-2v_s f'(R_F) = -3.0` ✓ to 7 digits |
| **`R_tyty`** | **`-12.7503`** | **nonzero** |
| **`R_tztz`** | **`-12.7503`** | equal, as axisymmetry requires |
| `R_tytz` | `0.0` | vanishes, as axisymmetry requires |
| `R_txtx` | `-8.9965` | `= -κ²` exactly (here f''(R_F) = 0 at the inflection), matching the paper's `R_KNKN = μ - κ²` |

Three independent consistency checks pass: the κ prediction from the symbolic
axis calculation, the axisymmetry pattern, and `R_KNKN = -κ²` at an inflection
point.

In the parallel-propagated frame `R_KYKY = q² R_tyty` with
`q = 1/[κ(λ*-λ)]`, so the component **diverges as `(λ*-λ)^-2`** while scalar
invariants stay finite.

> **Conclusion: the non-scalar obstruction extends to Natário. Zero expansion
> does not evade it.** The referee's objection is answered.

Note the coefficient is *not* the Alcubierre value `-κ/R_F = +3` — it is `-12.75`
for the same κ and R_F. Natário's field has transverse components off-axis that
Alcubierre's lacks, so the transverse structure genuinely differs; the obstruction
is the same mechanism with a different coefficient.

### Closed local-jet result, 2026-08-03

Script: sim/natario_local_jet.py.

Write
\[
  \kappa=2v_s f'(R_F)>0,
\]
so that \(X^x=-1\) and \(\Gamma^t{}_{tt}=-\kappa\) at the front axial
generator. A Cartesian two-jet calculation gives
\[
  R_{tyty}=R_{tztz}
  =-\frac{\kappa(3R_F\kappa+8)}{4R_F}
  =-\frac{2\kappa}{R_F}-\frac{3\kappa^2}{4},
\]
and
\[
  R_{txtx}=-\kappa^2-2v_s f''(R_F).
\]
For the numerical check \(v_s=2\), \(R_F=1\), \(f'(R_F)=3/4\), and
\(f''(R_F)=0\), these give
\[
  R_{tyty}=-12.75,\qquad R_{txtx}=-9,
\]
exactly reproducing the finite-difference calculation.

The transverse coefficient is strictly negative for every simple front root:
it does not require \(f''\), a profile inflection, or a genericity assumption.
Axisymmetry gives
\[
  R_{tt}=2R_{tyty}
  =-\frac{\kappa(3R_F\kappa+8)}{2R_F}<0.
\]
Thus the Natário front generator carries both a PP curvature divergence and an
unbounded negative null Einstein component for the whole simple-root profile
class, not just the numerical tanh example.

### Global maximality theorem

In cylindrical coordinates, Natario's poloidal field has streamfunction
\[
\Psi=-v_sf(r)\varrho^2,
\qquad X\cdot\nabla\Psi=0.
\]
On either zero-angular-momentum high-frequency ray branch in \(|X|>1\),
\[
\frac{d\Psi}{dt}=\pm\varrho\sqrt{|X|^2-1}.
\]
For a monotone inner wall with \(\partial_r|X|^2>0\), both possible zeros of
this derivative are strict local maxima along the ray. On the axis,
\(\Psi''=-a y'^2<0\); at a nonaxial \(|X|=1\) turning point,
\[
\Psi''=-\frac{\sin^2\theta}{2}
\left[r(a+b)\partial_r|X|^2+2a(2ab+b^2)\cos^2\theta\right]<0.
\]
A limiting ray can therefore switch branches at most once. Nonzero conserved
angular momentum does not survive a finite-proper-time exit:
\(J/|P|\to0\). Every bounded omega-limit is governed by the meridional system,
whose only compact complete orbits are the axial equilibria. Momentum growth
selects the front equilibrium, and the Ricci coefficient above gives the
\(C^2\) contradiction. Thus the eternal Natario spacetime is globally
\(C^2\)-inextendible for this monotone-wall profile class. Details and the
analytic proof is in `natario_global_maximality_proof.md`; the ray scans are
now falsification checks rather than load-bearing evidence.

### Still not done

- **The Van Den Broeck pocket check** (step 1 of the work plan) — still not run.
- Solitons untouched.

## Draft abstract

Deliberately non-technical; no parallel-propagated frames, boost weight, \(C^2\)
or affine parameter in the prose.

> **Superluminality and the Continuation of Warp-Drive Horizons**
>
> A warp drive that moves faster than light relative to distant observers
> necessarily develops surfaces, ahead of and behind the ship, that light cannot
> cross. Whether spacetime continues smoothly through these surfaces, as it does
> through the horizon of a black hole, is normally decided using a reduced
> description that keeps only time and the direction of travel. That description
> answers its own question correctly: the reduced geometry does continue. We
> show that the full geometry does not for the standard radial family and for a
> generic class of finite scalar-shift bubbles. At a stationary ray on the
> bubble wall, transverse wall curvature is registered in a frame boosted
> without limit, so finite local curvature becomes an unbounded tidal
> measurement. The same wall tensor supplies the null energy seen by that ray:
> its full shape controls continuation, while its mean controls the sign and
> size of the source. We compute the analogous effect for Natario's
> zero-expansion drive and find it for every simple front wall in that family.
> Exactly planar wall patches are locally extendible, so the result is not that
> every point of every wall is singular. Rather, curvature gives the generic
> obstruction and stationary-flow rigidity limits how the exceptional patches
> can be assembled into one continuation of a finite bubble.

The remaining scope sentence for a submitted abstract depends on closing the
exactly \(C^2\) stationary-flow germ lemma and Natario's global ray dynamics. If
some additional catalogue metric evades the local obstruction, the abstract
becomes "with one instructive exception," which is a better paper — it
identifies which geometric feature buys
extendibility.

"That description answers its own question correctly" is the load-bearing
diplomatic sentence toward FLB. Leave it.

Alternative title if the demarcation should lead: *What Superluminal Warp Drives
Cost, and What Subluminal Ones Do Not.*

## Connection: boost amplification as a common mechanism

Worth a discussion section in whichever paper submits first — not a standalone.

The same structure appears in three places: Hawking's blueshift on recurrent
almost-closed null generators at a chronology horizon; this paper's transverse
obstruction, where \(q=1/[\kappa(\lambda_*-\lambda)]\) converts a finite tidal
component into a divergent one; and §4.5 of
`wormhole/groundhog_day_ctc_research_note.md`, whose dichotomy between bounded
propagation and an unbounded transfer factor is the same \(q\)-factor structure.
This paper is a fully worked instance of that note's amplifying regime, with the
rate computed.

(An earlier attempt to unify this paper with Slobodov 2008 via Killing-norm
transverse jets was **closed as prior art** — Gibbons–Hawking plus the VSI/CSI
boost-weight program. See `ai-open-problem-screen/physics/A2_FINDING.md`. The
boost-amplification version is sturdier because all three instances are
Lorentzian boost effects rather than a Euclidean pattern-match.)

## Also outstanding on the main paper

Add **Cropp, Liberati & Visser, "Surface gravities for non-Killing horizons,"
CQG 30 (2013) 125001, arXiv:1302.2383.** The \(v^2=1\) surface is exactly a
non-Killing horizon — \(\partial_t\) is null there but geodesic only at the two
axial points, Eq. (16) — and the draft uses \(\kappa\) throughout as though the
notion were unambiguous. Referee liability, cheap fix.

Softer: cite the VSI/CSI boost-weight literature (Coley, Hervik, Pelavas,
Milson) alongside the Sec. 4.2 argument, which the draft currently derives from
scratch.
