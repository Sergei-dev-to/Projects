# Supplementary algebra and figure scripts

This supplement contains the symbolic and numerical checks used for the paper
`When Warp Horizons Extend: Curvature Boundaries of Alcubierre Spacetimes`.
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

The scripts write text outputs under `scripts/output/sech/`.  The figure script
also refreshes `calculated_three_region_endpoint_patch.{png,pdf,eps}` under the
paper's `figures/` directory.

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
- `diagram_derivation_overlay.py`: regeneration of the reduced three-region
  conformal diagram used as Fig. 1.
- `sech_extension.py`: closed-form coordinate helpers for the sech profile,
  used by the figure script.

## Scope

The supplement reproduces the local algebraic checks and the conformal figure.
The global extension alternative is proved analytically in the paper; no
numerical claim is used in that proof.  The supplement does not model a
dynamical warp bubble.
