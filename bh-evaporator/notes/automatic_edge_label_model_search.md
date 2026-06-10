# Search For A Model Where Edge Labels Are Automatic

## Question

Instead of justifying by hand:

```text
H_soft(R) = tensor over Mat_R labels,
```

can we find a model where the soft edge/operator Hilbert space appears
naturally?

## Short Answer

No single surveyed model gives the full evaporator automatically.

But there are three close mechanisms:

```text
1. Matrix Chern-Simons / quantum Hall droplets:
   natural flat-band softness and edge modes.

2. Gauge/Chern-Simons edge-mode factorization:
   natural boundary Hilbert spaces from constraints.

3. Fuzzy-sphere matrix/gauge theory:
   natural Mat_R mode algebra with R^2 degrees.
```

The likely best path is a hybrid:

```text
fuzzy-sphere / noncommutative Chern-Simons droplet
```

because it combines:

```text
flat-band quantum Hall softness;
matrix/fuzzy angular algebra;
edge-mode Hilbert spaces.
```

## Candidate 1: Matrix Chern-Simons Quantum Hall Droplet

Key references:

```text
Susskind,
"The Quantum Hall fluid and non-commutative Chern Simons theory",
arXiv:hep-th/0101029.

Polychronakos,
"Quantum Hall states as matrix Chern-Simons theory",
arXiv:hep-th/0103013.

Polychronakos,
"Quantum Hall states on the cylinder as unitary matrix Chern-Simons theory",
arXiv:hep-th/0106011.
```

What is natural:

```text
finite matrix variables;
quantum Hall droplet of finite extent;
lowest-Landau-level / noncommutative geometry;
edge excitations;
constraints / gauge structure;
matrix model Hilbert space is not an arbitrary register.
```

Why it helps:

```text
The softness of angular/guiding-center labels is natural. They come from
projected Landau-level physics, not from ordinary spherical harmonics.
```

What is missing:

```text
The standard quantum Hall droplet entropy does not automatically scale as
exp(R^2) with R as linear size in the way we need.

The model does not naturally evaporate via R -> R-1 with Schwarzschild-like
negative heat capacity.
```

Assessment:

```text
Best candidate for natural soft edge labels.
Not yet a black-hole-like evaporator.
```

## Candidate 2: Chern-Simons Edge-Mode Factorization

Reference:

```text
Gabriel Wong,
"A note on entanglement edge modes in Chern Simons theory",
arXiv:1706.04666.
```

Relevant abstract-level point:

```text
extended Hilbert-space factorization arises naturally from regularizing an
entangling surface; the stretched surface hosts Chern-Simons edge modes.
```

What is natural:

```text
edge Hilbert spaces are required by gauge constraints / factorization;
edge modes are not arbitrary hidden registers;
topological/soft character is built in.
```

Why it helps:

```text
This directly addresses the worry that soft labels are merely declared.
```

What is missing:

```text
No automatic R^2 count of independent angular labels in our sense;
no sector-changing evaporation;
no Hawking-like rate law.
```

Assessment:

```text
Best candidate for making the shell Hilbert space conceptually legitimate.
Weak as a complete evaporator.
```

## Candidate 3: Fuzzy-Sphere Gauge/Matrix Theory

References:

```text
Aoki, Iso, Kawai, Kitazawa, Tada,
"Noncommutative Gauge Theory on Fuzzy Sphere from Matrix Model",
arXiv:hep-th/0101102.

Steinacker and related fuzzy-sphere gauge theory literature.
```

What is natural:

```text
Mat_R is not invented;
it is the finite matrix algebra of functions/gauge fields on fuzzy S^2;
there are R^2 matrix modes.
```

Why it helps:

```text
This makes the Mat_R label set automatic.
```

What is missing:

```text
Ordinary fuzzy-sphere field modes have Laplacian energies l(l+1);
so softness is not automatic unless the theory is topological/constrained or
projected to a flat band.
```

Assessment:

```text
Best candidate for natural R^2 mode algebra.
Needs Chern-Simons/topological/LLL ingredient for softness.
```

## Candidate 4: Quantum Hall Droplet Edge CFT

What is natural:

```text
edge excitations of quantum Hall droplets;
outer orbitals;
chiral boson dynamics;
angular momentum labels tied to droplet edge/radius.
```

Why it helps:

```text
high angular labels can correspond to outer edge structure rather than high
bulk kinetic energy.
```

What is missing:

```text
edge CFT entropy is not simply d^(R^2);
it gives partition/counting behavior depending on edge energy.
```

Assessment:

```text
Good for dynamics of hard/edge radiation.
Not enough for the full area-like soft Hilbert space.
```

## Candidate 5: Large-N Matrix Quantum Mechanics

What is natural:

```text
N^2 adjoint/matrix degrees;
rank reduction N -> N-1 in D0-brane evaporation;
off-diagonal connector decoupling;
negative specific heat in black-zero-brane interpretation.
```

Why it helps:

```text
This is the known successful relational-entropy mechanism.
```

What is missing for us:

```text
It is holographic/black-hole-adjacent, and not a clean 2D angular/edge model.
```

Assessment:

```text
Mechanism precedent, not the desired non-gravitational angular model.
```

## Comparative Table

```text
Model                          Mat_R natural  soft labels  edge Hilbert  evaporation  BH scaling
-------------------------------------------------------------------------------------------------
Matrix Chern-Simons QH droplet  P              Y            Y            P/N          N
Chern-Simons edge modes         N/P            Y            Y            N            N
Fuzzy-sphere gauge theory       Y              N/P          P            N            N
QH edge CFT                     P              P            Y            P            N
Large-N matrix QM               Y              P            N/P          Y            Y, but holographic
```

Legend:

```text
Y   = strong match
P   = partial / depends on construction
N   = not present as needed
```

## Best Hybrid Direction

The best natural candidate is:

```text
fuzzy-sphere / matrix Chern-Simons quantum Hall droplet with edge modes.
```

Why:

```text
1. Fuzzy sphere supplies finite angular Mat_R algebra.
2. Landau-level projection supplies softness.
3. Chern-Simons/gauge constraints supply edge Hilbert spaces naturally.
4. Quantum Hall droplet gives outer-orbital shrinkage intuition.
```

What remains to add:

```text
1. identify R as linear size/mass sector;
2. define evaporation as R -> R-1;
3. couple hard edge/radiation modes to a 3D bath;
4. track soft edge labels as memory/purification.
```

This is still not fully automatic, but it minimizes arbitrary register
insertion.

## Important Warning

If we use actual quantum Hall droplet physics too literally, the scaling may
change.

Quantum Hall usually gives:

```text
orbital degeneracy ~ area.
```

Our desired black-hole-like sector uses:

```text
R = linear size;
soft label count ~ R^2.
```

So the model should use:

```text
fuzzy/operator/edge label count
```

rather than:

```text
single-particle orbital degeneracy only.
```

Otherwise we fall back into the area-register ambiguity.

## Current Judgment

The most natural available model family is:

```text
noncommutative Chern-Simons / quantum Hall matrix droplet on a fuzzy sphere.
```

It does not hand us the whole black-hole evaporator.

But it gives the best non-gravitational mechanism for:

```text
soft angular labels;
finite matrix/angular geometry;
edge Hilbert spaces that are not arbitrary registers.
```

Follow-up review:

```text
matrix_cs_qh_deep_review.md
```

That deeper read sharpened the conclusion:

```text
matrix CS / QH edge physics naturalizes soft boundary labels,
but the Gauss-law-constrained physical Hilbert space does not automatically
contain N^2 independent soft qudits.
```

So this family should be used to motivate edge labels and the hard/soft split,
not as an automatic derivation of the full evaporator.
