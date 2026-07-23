# Smale 6 fixed-mass ramification experiment

The cross-project research history, decision register, and next-search gates
are recorded in `../SMALE6_PROGRAM_RETROSPECTIVE.md`.

This is a new experiment, separate from the archived Roberts positivity-repair
work in `../smale6-repair`.

The target is a positive-dimensional fiber of the mass projection.  After
translation, rotation, and scale are fixed, write the central-configuration
equations as

\[
F(z;m)=0.
\]

At a singular fixed-mass solution, a formal arc

\[
z(t)=z_0+t z_1+t^2z_2+\cdots
\]

must satisfy every Taylor coefficient of `F(z(t);m)=0`.  The script
`jet_sieve.js` evaluates those coefficients with dependency-free truncated
power-series arithmetic.  At each order it solves the bordered linear system

\[
\begin{pmatrix}J&W\\V^T&0\end{pmatrix}
\binom{z_k}{\alpha_k}=\binom{-b_k}{0},
\]

where `V` and `W` span the right and left kernels of `J=D_zF`.  A nonzero
`alpha_k` is the obstruction to continuing the chosen fixed-mass tangent.

Run the calibrations with:

```powershell
node .\jet_sieve.js
```

Run the compact regression checks with:

```powershell
node .\self_test.js
```

The first calibration is Roberts' genuine continuum with masses
`(1,1,1,1,-1/4)` at the rational point `(a,b)=(3/5,4/5)`.  It should survive
all implemented orders.  The second is the positive-mass degenerate
equilateral-triangle-plus-center configuration.  It is expected to fail at a
finite order because degeneracy there produces an ordinary mass bifurcation,
not a fixed-mass continuum.

Finite-order survival is a discovery signal, not a proof of a curve.  Any
positive survivor must subsequently pass an exact local-dimension or ideal
containment test.

The first live target is now implemented as well: the positive Chen--Hsiao
five-body degeneracy on two Albouy--Kaloshin exceptional mass relations.  It
has a genuine one-dimensional shape kernel but fails the fixed-mass
compatibility equation at order two.  See `RESULT.md` for the formulas,
numerics, gauge checks, and literature boundary.

That numerical observation has now been upgraded to an exact fixed-decimal
interval certificate.  See `CERTIFIED_FOLD.md` for the theorem, proof chain,
full-planar symmetry-breaking check, limitations, and reproduction commands.

The compact exact regression is:

```powershell
node .\certificate_self_test.js
```

## Ramification-search pilot

`census.js` now follows singular routes in the `(1,1,mu,mu,nu)` mass family
and applies the jet obstruction as an event filter.  `census_corank2.js`
analyzes the square-plus-center corank-two control.  Run them with:

```powershell
node .\census.js
node .\census_corank2.js
```

The audited findings, literature correction, and limitations are in
`CENSUS.md`.  In particular, this is a candidate-generating pilot, not a
complete census of a discriminant component.
