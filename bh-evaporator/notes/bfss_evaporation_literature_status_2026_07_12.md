# BFSS Evaporation Literature Status

Date: 2026-07-12

Status: **major overlap found; BFSS parked as successor research**. This is a
targeted primary-source pass, not an exhaustive review. It narrowed the live
BFSS question, while the final program endpoint declined to treat a BFSS pilot
as required continuation.

## 1. What is already in the literature

### Matrix-theory emission rates

Banks, Fischler, and Klebanov model a Schwarzschild black hole as a metastable
bound state of D0-branes and estimate Hawking emission through small D0-brane
clusters, finding agreement with the semiclassical rate up to an order-one
coefficient:

<https://arxiv.org/abs/hep-th/9712236>

Related large-`N` Matrix-theory work also derives the expected evaporation-rate
scaling from the D0-cluster picture:

<https://arxiv.org/abs/hep-th/9806245>

### Real-time matrix evaporation

Berkowitz, Hanada, and Maltz study real-time classical matrix dynamics. They
identify D0-brane escape through flat directions, negative specific heat, and a
possible route from matrix-model evaporation to Hawking radiation:

<https://arxiv.org/abs/1602.01473>

Berenstein and Guan study a simplified `2 x 2` matrix model and analyze the
separation of D-particles and the lifetime of the bound state:

<https://arxiv.org/abs/2105.04577>

These works address emission mechanisms, rates, and classical or semiclassical
real-time behavior. They do not calculate the diary-conditioned,
radiation-resolved quantum process used by the present program.

### A BFSS Page curve

Choudhury and Laurenzano explicitly construct a quantized black-0-brane plus
radiation description, calculate the radiation entropy, and obtain a Page
curve with complete purification after the black hole has evaporated:

<https://arxiv.org/abs/2407.13336>

This is direct overlap with any claim that BFSS evaporation, D0-brane
emission, or a BFSS Page curve has not been studied.

The important qualification is stated in the paper itself: the full action of
the BFSS Hamiltonian on the black-hole state is not known, so the calculation
uses an effective description with a factorized black-hole/radiation Hilbert
space and time-dependent emission probabilities. The authors describe a full
Matrix-theory description of the black-hole state and its evolution as future
work.

### Adjacent matrix-entanglement work

Matrix-entanglement methods have also been used to discuss Page curves and
factorization in gauge theories, including a small black hole in
`AdS_5 x S^5`:

<https://arxiv.org/abs/2204.06472>

That is relevant methodology, but it is not the same as a radiation-resolved
BFSS D0-detachment process.

## 2. What this settles for our program

We should retire these as target claims:

```text
BFSS can produce D0-brane evaporation;
Matrix theory can reproduce Hawking-like emission rates;
BFSS evaporation can be assigned a Page curve;
unitary D0-brane emission can purify the final radiation.
```

Those questions already have published answers at the mechanism,
semiclassical, or effective-Hilbert-space level.

The literature also confirms one of the program's warnings: a Page curve is
not by itself evidence that a microscopic emission channel has been derived.
In the 2024 BFSS calculation, the probability model and black-hole/radiation
factorization do substantial work before the entropy is evaluated.

## 3. The remaining question

The live question is narrower and more operational:

```text
Does the BFSS Hamiltonian, with a declared gauge-invariant separation
criterion and radiation algebra, determine the time-ordered channel from
black-hole microstates to escaped-D0 or massless-radiation records?
```

The relevant data would be radiation-resolved transition amplitudes or an
equivalent process tensor, for example

```text
A_(i->f,m)(t) = <f,m| Q_m exp(-i H t) P_E |i>,

K_ij^(mn)(t) = sum_f A_(i->f,m)(t) A*_(j->f,n)(t).
```

From this one could ask questions not answered by an emission rate or Page
curve:

- Do different initial microstates produce different radiation histories?
- Are one-particle records nearly identical while multitime records differ?
- Does the remaining clump decouple from a diary reference?
- Which labels belong to the accessible radiation algebra, and which remain
  hidden daughter or partner data?
- Is recovery a consequence of the Hamiltonian, or of an imposed emission
  probability and factorization rule?

## 4. Program consequence

The next BFSS project should not reproduce evaporation or the Page curve. It
should audit or extend the existing BFSS Page-curve construction at the
process level.

There are two useful outcomes:

```text
the existing effective calculation already determines the required process:
  translate it into the A/K, access, and decoupling language and identify the
  assumptions that supply the result;

the existing calculation does not determine the process:
  quantify the missing gauge-invariant amplitudes and treat the Page curve as
  an effective completion, not a microscopic BFSS derivation.
```

Either result advances the program. A new generic BFSS chaos, thermality, or
Page-curve simulation would not.

## 5. Revised wording

Do not say:

> BFSS evaporation and information recovery remain unstudied.

Say:

> BFSS literature contains D0-brane evaporation mechanisms, Hawking-rate
> estimates, real-time matrix studies, and an effective Page-curve
> construction. The unresolved process-level issue is whether the BFSS
> Hamiltonian itself supplies the gauge-invariant, radiation-resolved channel
> and the multitime decoupling needed for recovery.

## Sources checked

- Banks--Fischler--Klebanov, *Evaporation of Schwarzschild Black Holes in
  Matrix Theory*, arXiv:hep-th/9712236.
- Gao--Zhang, *Evaporation of Schwarzschild Black Hole in the Large N Matrix
  Theory*, arXiv:hep-th/9806245.
- Berkowitz--Hanada--Maltz, *Chaos in Matrix Models and Black Hole
  Evaporation*, arXiv:1602.01473.
- Berenstein--Guan, *Improved semiclassical model for real time evaporation of
  Matrix black holes*, arXiv:2105.04577.
- Choudhury--Laurenzano, *Entanglement Entropy for the Black 0-Brane*,
  arXiv:2407.13336.
- Gautam--Hanada--Jevicki--Peng, *Matrix Entanglement*, arXiv:2204.06472.
