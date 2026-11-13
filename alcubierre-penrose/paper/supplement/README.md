# Supplementary algebra and figure scripts

This supplement contains the symbolic and numerical checks used for the paper
`Extensions and Curvature Singularities of Alcubierre Spacetimes`.
The scripts are intended for verification and inspection, not as a general
software package.

## Requirements

Use Python 3.10 or later with:

```text
numpy
scipy
sympy
matplotlib
```

Install them with:

```bash
python -m pip install -r requirements.txt
```

## Run everything

From this directory:

```bash
python run_all.py
```

On a typical laptop the full run takes a few minutes, mainly because the
symbolic checks and figure generation are deliberately explicit.

The scripts write text outputs under `scripts/output/sech/`. The current
figure script refreshes `bubble_extension_comparison.{png,pdf}` under the
paper's `figures/` directory. The detailed reduced-diagram script also
refreshes its separate supporting figure there.

## Script map

- `front_tip_adm_derivation.py`: ADM/Gauss-Codazzi derivation of the leading
  transverse component \(R(K,Y,K,Y)\).
- `front_tip_full_parallel_frame.py`: full symbolic check of the
  parallel-propagated null frame and Riemann components.
- `front_tip_scalar_invariants.py`: scalar polynomial curvature invariants for
  the local spherical data and the closed-form sech profile.
- `front_tip_general_convex_wall.py`: general front-surface calculation with
  transverse derivatives \(v_A\), \(v_{xA}\), and \(v_{AB}\).
- `front_tip_einstein_parallel_frame.py`: independent check of the null source
  projection in the complete parallel frame.
- `flat_cap_partial_extension.py`: smooth Kruskal continuation of an exact
  planar cap, the positive-boost-weight curvature identities used in the
  transverse-rigidity proof, and the distinct cap-rim obstruction.
- `flat_cap_crossing.py`: conserved timelike first integrals, finite regular
  crossing velocity, and the locally flat product-cap germ.
- `front_tip_taylor_metric_check.py`: local Taylor-metric cross-check near the
  axial endpoint.
- `front_tip_numerical_frame_check.py`: finite-difference numerical check for
  the sech profile.
- `front_tip_parallel_tidal_analytic.py`: direct analytic derivation of the
  parallel-frame tidal component.
- `front_tip_parallel_tidal.py`: numerical Riemann helper used by the
  finite-difference frame check.
- `alcubierre_3p1_set.py`: numerical metric, Christoffel, and Einstein-tensor
  helpers for the sech profile.
- `diagram_derivation_overlay.py`: regeneration of the original detailed
  reduced three-region conformal diagram.
- `meridional_geometry.py`: symbolic pullback of the exact angular quotient,
  its cap extension and off-cap degeneration, the transverse cone metric,
  and numerical null-cone and geodesic checks. It verifies the spherical
  sech profile and the specified compact-cap collar before drawing.
- `bubble_extension_comparison.py`: regenerates the paper's single three-panel
  figure. It checks that the global spherical and capped profiles have the
  same axial shift, verifies the wall sections and timelike crossing, and
  separates the cap attachment from ordinary null infinity. The right panels
  are finite-time spatial sections, not spacetime diagrams.
- `meridional_diagrams.py` and `cap_extension_diagram.py`: retained supporting
  renderers for the 2+1 coordinate views; these are not used in the main paper.
- `sech_extension.py`: closed-form coordinate helpers for the sech profile,
  used by the figure script.

## Scope

The supplement reproduces the local algebraic checks and the conformal figure.
The local tidal and flat-profile calculations include independent checks of
established results; their presence here is not a claim of originality.
The finite-affine and transverse-geodesic background is credited to
Barcelo et al. (2022), the flat product profile is a stationary specialization
of Santos-Pereira et al. (2020), and regular Killing-horizon continuation
uses Racz--Wald. The independent proof content is the global capture and
transverse-disk necessity argument, its compact realization, and the rim
obstruction.
The global rigidity theorem and its sharpness construction are proved
analytically in the paper; no numerical claim is used in those proofs.  The
supplement does not model a dynamical warp bubble.

## Supporting mathematical notes

`supporting_geometry.tex` preserves the matched-profile plotting data,
wall/source relation, transverse-coordinate calculation, and the
qualification on earlier axial continuations. It is a LaTeX source
fragment using the manuscript preamble, notation, and bibliography; it
is not included in the main paper and has no separate compiled PDF.

`prior_result_checks.tex` retains the spherical stationary-generator and
Killing-field checks removed from the main text in favor of citations.
These are supporting reproductions of local background results, not further
contributions. The fragment uses the manuscript preamble and bibliography
and is not included in the main paper.
