# Smale 6 positivity-repair experiment

The cross-project research history, decision register, and revisit rules are
recorded in `../SMALE6_PROGRAM_RETROSPECTIVE.md`.

## Status: archived 2026-07-22

This branch is closed as a Roberts-specific repair experiment.  Its exact
results are retained in `RESULT.md`, but fixed-cloud, affine-distance, and
co-moving-shell repairs should not be extended into further bespoke nested
rhombus or nested-square searches without a new mechanism.  Future Smale 6
work should treat this repository as a calibration case for a broader
fixed-mass exceptional-fiber search.

This workspace tests whether the Roberts continuum

\[
 (\pm a,0),(0,\pm b),(0,0),\qquad a^2+b^2=1,
\]

with masses `(1,1,1,1,-1/4)` can be repaired using additional positive
bodies.  The first ansatz consists of concentric, homothetic rhombi:
level `k` has four equal masses `m_k` at

\[
 (\pm r_k a,0),(0,\pm r_k b).
\]

`nested_rhombi.js` searches positive radii and masses for a fixed-mass
continuum and independently evaluates the exact central-configuration
residual at held-out shapes.
