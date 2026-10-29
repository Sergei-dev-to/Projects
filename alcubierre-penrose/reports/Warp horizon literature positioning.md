# Positioning four dimensional warp extension rigidity

Literature assessment through 29 October 2026. This review compares the proposed manuscript with the primary literature; it does not independently validate its proofs or establish absolute priority.

**The proposed paper fits most convincingly as a classical four-dimensional extension-rigidity theorem for a specified stationary scalar-shift class.** Its strongest claim is that the existence of any proper Hausdorff \(C^2\) extension forces an open planar wall patch with constant nonzero inaffinity. Known Killing-horizon theory supplies the regular continuation once that patch exists. The rounded radial obstruction and the compact cap/rim example explain why the necessity direction matters. The sech coordinates and reduced diagram already occur in Finazzi–Liberati–Barceló (2009), while finite-affine axial limits and transverse shape effects already appear in Barceló et al. (2022). The manuscript should credit those results directly and identify its added contribution as an invariant endpoint obstruction followed by an exhaustive extension criterion. A 2026 classification paper also makes a global-hyperbolicity claim apparently incompatible with the original bounded-shift spacetime; that discrepancy deserves a precise, self-contained clarification.

## Earlier diagrams leave the transverse extension question open

The relevant history is more specific than a progression from two-dimensional pictures to an unexplored four-dimensional problem. Several predecessors study the full metric or transverse dynamics. The defensible distinction is the question they answer: propagation, quantum stress, or scalar geometry, rather than the existence of an arbitrary same-dimensional regular isometric extension.

| Closest work | Relevant established contribution | Distinction from the proposed result |
|---|---|---|
| [Hiscock (1997)](https://arxiv.org/html/gr-qc/9707024) | Axial reduction and a quantum stress-tensor divergence | A selected quantum field/state, rather than classical four-dimensional inextendibility |
| [Clark–Hiscock–Larson (1999)](https://arxiv.org/html/gr-qc/9907019) | Full-metric photon trajectories, energy shifts and signal-access horizons | No global extension classification |
| [González-Díaz (2000)](https://arxiv.org/html/gr-qc/9907026) | Reduced Kruskal/Misner constructions and a generalized four-dimensional expression | A faithful isometric lift of the original radial metric is not established by the displayed derivation |
| [Finazzi–Liberati–Barceló (2009)](https://arxiv.org/html/0904.0141) | The same sech coordinates and compactified reduced diagram; semiclassical instability | The proposed diagram construction reproduces/adapts this work |
| [Barceló et al. (2022)](https://arxiv.org/html/2207.06458) | Finite-affine axial limits, transverse deflection and shape-dependent energy accumulation | Its stability criterion differs from classical \(C^2\) endpoint regularity |
| [Rácz–Wald (1992, 1996)](https://arxiv.org/html/gr-qc/9507055) | Regular extension of suitable nondegenerate Killing horizons | The proposed necessity proof must first force such a horizon patch to exist |

**Section 2 should explicitly reproduce/adapt Finazzi–Liberati–Barceló.** Their §II.1, Eqs. (3)–(25), contains the sech profile, roots, signed horizon scales, closed-form null coordinates, and the same piecewise exponential/tanh compactification. Figure 2 is expressly nonmaximal. They leave the added regions undrawn because the far-side matter continuation is undetermined. Redrawing that diagram is useful exposition and reproducibility, but neither the antiderivatives nor the possibility of extra reduced regions is the paper's novelty. Their dynamical model forms a bubble and retains its final superluminal state; it does not switch it off after a finite lifetime. ([Finazzi et al., §II.1 and §§IV.2–IV.3](https://arxiv.org/html/0904.0141#S2.SS1))

González-Díaz needs a more direct comparison than “a previous two-dimensional continuation.” Section II starts from an axial reduction but does write a generalized four-dimensional expression, Eq. (2.10). The narrow issue is whether it establishes a same-dimensional isometric extension of the original radial Alcubierre metric. With \(\xi=x-v_0t\) and \(r=\sqrt{\xi^2+y^2+z^2}\), the identity used on the axis becomes, off axis,

\[
dr=\frac{\xi}{r}\,d\xi+\frac{y}{r}\,dy+\frac{z}{r}\,dz.
\]

Restoring transverse terms therefore requires a full pullback calculation. A second independent differential check concerns the proposed redefinition \(dt'=A(r)^{1/4}dt\): its exterior derivative is generally nonzero, so it cannot simply be treated as a coordinate differential. These are checks of the displayed derivation, not a published refutation or a proof that every alternative isometry is impossible. The manuscript's invariant obstruction is the stronger way to settle the original radial geometry. ([González-Díaz, §II, Eqs. (2.3)–(2.15)](https://arxiv.org/html/gr-qc/9907026#S2))

The numerical geodesic literature should also be credited. Müller–Weiskopf already uses a parallel-transported Sachs screen and the Jacobi equation for optical propagation; McMonigal–Lewis–O'Byrne studies trapping, growing velocity components, and release after a variable-speed bubble becomes subluminal. Those phenomena should not be reintroduced as new. The inspected sections do not give the proposed invariant extension criterion. ([Müller–Weiskopf, §§2–3.1](https://arxiv.org/html/1107.5650); [McMonigal et al., §§II–III.2](https://arxiv.org/html/1202.5708))

## Killing horizon theory supplies the regular branch

**A planar constant-inaffinity cap is a specialized realization of established regular-horizon theory.** Rácz–Wald's 1992 result begins with an actual Killing-horizon hypersurface, real-line Killing orbits, and a suitable smooth cross-section. It relates a nonzero surface-gravity gradient to a parallelly propagated curvature obstruction and permits a regular bifurcate extension when the surface gravity is constant and nonzero. These statements were checked in the publisher's abstract and the authors' explicit 1996 recap; the complete 1992 PDF was not retrieved. An unverified theorem number should not be assigned to it. ([Rácz–Wald 1992](https://doi.org/10.1088/0264-9381/9/12/008); [Rácz–Wald 1996, §1](https://arxiv.org/html/gr-qc/9507055))

That starting hypothesis is exactly where the proposed paper differs. The rounded stationary-limit wall is generally timelike, and its stationary null orbits are pregeodesic only on the generator locus. Rácz–Wald therefore does not directly turn the rounded wall into a regular extension, nor does it prove that every possible extension must find a planar patch somewhere. The proposed capture and fixed transverse observer-disk argument supplies that global necessity statement. Its importance is that an arbitrary extension is allowed to choose a different boundary chart; divergence in a preferred coordinate chart alone would not suffice.

The 1996 paper should be added to the bibliography. Example 1 warns that local regularity and global hyperbolicity do not automatically provide the desired global bifurcate attachment. Its Theorem 4.2 uses additional stationary black-hole assumptions, including a controlled asymptotic end, absence of a white-hole region, and compact horizon cross-sections. Those hypotheses do not directly describe our finite open aperture. The explicit Hausdorff attachment remains useful, provided it is presented as the specialized sharpness construction rather than a new general Kruskal theorem. ([Rácz–Wald 1996, §§1–4](https://arxiv.org/html/gr-qc/9507055))

The rim example earns a place because it tests neighborhood regularity sharply. A generator can have bounded propagated curvature while every fixed transverse neighborhood imports divergent contractions. General extension theory already requires neighborhood control; Rácz's extension results use synchronized geodesic neighborhoods and bounds on curvature and derivatives. The distinctive contribution would be the explicit compact warp-wall example and its invariant obstruction. ([Rácz 2010, Theorem 4.2 and §5](https://arxiv.org/html/0803.0648))

## Endpoint regularity differs from quantum stability

The 2022 aerodynamics paper is the closest modern physical comparison. Section III.1, Eq. (9), already identifies finite-affine axial limits at infinite stationary time. Sections III.2–III.3 distinguish special transverse-gradient-zero points and analyze flat versus rounded fronts, transverse escape and accumulation. Its conclusions concern a heuristic estimate of integrated quantum-energy buildup; it does not compute an exact higher-dimensional renormalized stress tensor or prove a classical \(C^2\) extension theorem. The proposed result therefore addresses a different criterion. A small set of rays can obstruct regular endpoint attachment even when an estimated energy accumulation is spatially integrable. That distinction does not refute the earlier quantum-energy calculation or establish generic backreaction instability. ([Barceló et al., §§III–IV](https://arxiv.org/html/2207.06458))

The scalar-invariant studies provide another concrete comparison. Mattingly et al. calculates and plots invariants at finite spacetime coordinates. Its §6 then extrapolates scalar regularity toward conclusions about horizons and removal of causal discontinuities. Our endpoint is approached at infinite stationary time in a parallel frame, so the proposed divergence is compatible with finite values in those plots. The manuscript should target the inference that bounded scalar invariants decide extendibility, without saying the finite-point calculations are wrong. ([Mattingly et al., §§4 and 6, Appendix A](https://arxiv.org/html/2010.13693))

Rodal revisits those invariant plots and emphasizes that a radial wall profile does not make the full Alcubierre metric spherically symmetric. That supports careful use of “axial restriction” for the reduced diagram. The article does not supply a regular-endpoint theorem. Its 2023 publication date and December 2025 arXiv posting are compatible; the mixed dates in our bibliography are not intrinsically erroneous. ([Rodal, §3](https://arxiv.org/html/2512.20738); [publisher metadata](https://link.springer.com/article/10.1007/s10714-023-03182-9))

The useful progression is consequently: previous papers locate special rays and characterize scalar or quantum behavior; the proposed paper computes the classical transverse tidal obstruction and then asks whether any other boundary exit remains. The global step, rather than the familiar existence of blueshift, must carry the novelty claim.

## The 2026 hyperbolicity claim needs clarification

Barzegar–Buchert–Vigneron's 2026 preprint is relevant beyond broad classification. Definition III.1 uses zero comoving shift in the core and \(-V_s(t)\) outside; Eqs. (3.25)–(3.27) give the unit-lapse flat-slice setting, and Eq. (3.44) is explicitly comoving. Remark IV.4 associates increasing-time orientation with shift norm below lapse. Theorem IV.7 concludes that the constructed superluminal R-Warp models cannot be globally hyperbolic. The accessible record lists only the February 2026 version, and the targeted search found no correcting revision. ([Definitions](https://arxiv.org/html/2602.16495#S3); [Remark IV.4 and Theorem IV.7](https://arxiv.org/html/2602.16495#S4.SS1); [version record](https://arxiv.org/abs/2602.16495))

**This appears to conflict with a direct calculation for the original bounded-shift spacetime, not merely with a lab/comoving convention.** A smooth compact-transition profile, multiplied by a bounded startup function, has their stated comoving asymptotics; transforming back to lab coordinates makes the perturbation spatially localized. For the prescribed metric on the full \(\mathbb R^4\), the independent calculation is

\[
g^{tt}=-1,\qquad
\left|\frac{d\boldsymbol x}{dt}-v e_x\right|\le1,
\qquad
\left|\frac{d\boldsymbol x}{dt}\right|\le1+\|v\|_\infty.
\]

A causal curve with a finite endpoint of its time range consequently has convergent spatial coordinates and can continue in the smooth metric. Every inextendible causal curve therefore crosses every constant-time slice. The metric is globally hyperbolic. This is the manuscript's own argument, and it does not use matter energy conditions.

The apparent logical issue is the distinction between a temporal covector and a timelike coordinate vector. The normal to the slices remains timelike even where \(\partial_t\) becomes spacelike. Choquet-Bruhat–Cotsakis Theorem 2.1 requires bounded shift, not shift norm below lapse; its proof orients causal curves using the slice normal. A sufficient slicing condition also cannot be used as an unproved converse. The paper should state this distinction and its self-contained Cauchy-slice proof, while carefully specifying the original full spacetime rather than a further reduced extension. ([Choquet-Bruhat–Cotsakis, Theorem 2.1](https://arxiv.org/html/gr-qc/0201057#S2))

This warrants a measured clarification in related work, not a broad verdict on the 2026 paper. The comparison does not solve the separate physical initial-value problem for a specified supporting matter model.

## Keep the paper centered on necessity and sharpness

The recommended contribution statement is:

> We determine when continuations suggested by reduced stationary warp-drive diagrams survive as Hausdorff \(C^2\) extensions of the original four-dimensional scalar-shift spacetime. Under the stated sign, exterior-decay and regular-wall hypotheses, any extension forces an open planar constant-inaffinity Killing-horizon patch. Standard regular-horizon continuation realizes this exceptional branch; the stated radial profiles are globally inextendible.

The regular-wall criterion and the separate radial corollary should retain their different hypotheses: the radial result includes the degenerate case, whereas the general classification uses wall regularity to obtain nonzero inaffinity. Neither should expand rhetorically into a claim about all warp drives, general vector shifts, time-dependent geometries, or lower-regularity extension.

The practical editorial priorities are straightforward. Rewrite the reduced-diagram introduction as an adaptation of Finazzi et al.; expand the historical paragraph to address González-Díaz's actual four-dimensional expression; identify the finite-affine and shape-dependent observations already present in Barceló et al.; distinguish the forced-horizon necessity step from Rácz–Wald sufficiency; and add a short hyperbolicity clarification addressing the 2026 claim. Give the cap example the role of sharpness, with the rim demonstrating the transverse-neighborhood requirement. A finite test-body crossing corollary would make that example operational without requiring a global matter-evolution claim.

Finite-duration completeness is useful, but it specializes established slicing/completeness results and the theorem that timelike completeness plus global hyperbolicity implies \(C^0\)-inextendibility. Exact local null-matter pulses likewise adapt known pp/Kundt families. They can be supporting material or later work; they should not compete with the extension criterion. ([Choquet-Bruhat–Cotsakis, Theorem 3.2](https://arxiv.org/html/gr-qc/0201057); [Galloway–Ling–Sbierski, Theorems 1–2](https://arxiv.org/html/1704.00353v4); [Podolský–Ortaggio](https://arxiv.org/html/gr-qc/0212073); [Krtouš et al.](https://arxiv.org/html/1201.2813))

| Bibliographic priority | References and purpose |
|---|---|
| Essential closest comparisons | [Finazzi et al. 2009](https://arxiv.org/abs/0904.0141), [González-Díaz 2000](https://arxiv.org/abs/gr-qc/9907026), [Barceló et al. 2022](https://arxiv.org/abs/2207.06458): identify the precise advance over existing diagrams, extensions and transverse dynamics |
| Essential geometric framework | [Rácz–Wald 1992](https://doi.org/10.1088/0264-9381/9/12/008), [Rácz–Wald 1996](https://arxiv.org/abs/gr-qc/9507055), [Galloway–Ling–Sbierski](https://arxiv.org/abs/1704.00353): separate standard tools from specialized necessity |
| Essential current clarification | [Barzegar–Buchert–Vigneron 2026](https://arxiv.org/abs/2602.16495), read with [Choquet-Bruhat–Cotsakis](https://arxiv.org/abs/gr-qc/0201057): make the global-hyperbolicity issue explicit |
| Add or strengthen supporting citations | [Müller–Weiskopf](https://arxiv.org/abs/1107.5650), [McMonigal et al.](https://arxiv.org/abs/1202.5708), [Rácz 2010](https://arxiv.org/abs/0803.0648), [Rodal](https://arxiv.org/abs/2512.20738): propagation precedent, neighborhood regularity, and symmetry terminology |

## Conclusion

The focused paper has a credible literature position if the global proof withstands scrutiny: it determines whether the original full metric permits any regular continuation, rather than selecting an interesting universe to glue onto a known regular horizon. The necessity theorem is therefore the result that deserves the most mathematical review and the strongest prominence. The cap and its rim explain why its conclusion is sharp.

No matching four-dimensional global cap-classification theorem was located in the inspected corpus. That is a bounded search finding, not proof of firstness. Full texts were closely inspected for the main predecessors; the additional numerical geodesic papers were checked in their directly relevant sections, and the original 1992 Rácz–Wald PDF remained unavailable. No manuscript changes were made. The three underlying research notes preserve source locators, differential checks, search scope and evidence limitations.
