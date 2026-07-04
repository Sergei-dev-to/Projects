# Rindler and BTZ separation pass

Date: 2026-06-13

Purpose: work the sequence `Rindler -> BTZ -> flux compression` before
trying the anonymity alternatives theorem.  The goal is to identify
what the separation program already knows, and where a genuinely
interesting result could live.

Primary anchors:

- Unruh, "Notes on black-hole evaporation" (1976):
  https://link.aps.org/doi/10.1103/PhysRevD.14.870
- Bisognano-Wichmann theorem background:
  https://arxiv.org/abs/math-ph/0001034
- BTZ, "The Black Hole in Three Dimensional Space Time":
  https://arxiv.org/abs/hep-th/9204099
- Brown-Henneaux central charge reference copy:
  https://srv2.fis.puc.cl/~mbanados/Cursos/TopicosRelatividadAvanzada/BrownHenneaux.pdf
- Strominger, "Black Hole Entropy from Near-Horizon Microstates":
  https://arxiv.org/abs/hep-th/9712251
- Maldacena, "Eternal Black Holes in Anti-de-Sitter":
  https://arxiv.org/abs/hep-th/0106112

## 1. Rindler: the null theorem

Rindler is the cleanest way to avoid fooling ourselves.  It has the
thermal horizon phenomenon in almost its purest form:

- The right-wedge algebra of the Minkowski vacuum is thermal/KMS with
  respect to boosts.
- An accelerated detector sees the Unruh temperature.
- The global vacuum has the usual left/right wedge correlations and
  admits the formal Rindler-mode thermofield description.
- The observer has an inside/outside split and a causal horizon.

So Rindler already supplies:

```text
modular thermality + inside/outside entanglement + observer horizon.
```

It does not by itself supply:

```text
finite horizon entropy budget,
shrinking horizon Hilbert space,
asymptotic emitted record,
Page-time accounting,
Hayden-Preskill recovery latency.
```

The reason is structural, not cosmetic.  The wedge algebra is a QFT
local algebra; in the continuum it is type-III rather than a finite
tensor factor with a density matrix and a finite entropy.  A cutoff can
produce an area-divergent entanglement entropy and a finite-dimensional
approximation to the thermofield picture, but then the finite budget is
a regulator-plus-gravity input, not a Rindler theorem.

Plain statement:

> Rindler proves that thermality is not the black-hole information
> problem.  It is horizon kinematics.  The information problem begins
> only after a finite entropy budget and a recoverable exterior record
> are added.

This is the clean null case for the separation theorem:

```text
T does not imply F, R, S, or logarithmic latency.
```

where `T` is modular thermality, `F` is finite budget, `R` is emitted or
exchanged recoverable record, and `S` is source-side boundary
saturation.

Useful paper role: a short control paragraph or appendix.  It should
not be sold as a new result.

## 2. Rindler density form: where it still helps

Rindler is not useless for the saturation program.  It gives the local
density version of the story.

With a stretched-surface/proper-acceleration cutoff, each transverse
thermal cell of size `beta^{d-1}` behaves like an independent channel
density.  The regulated channel count per thermal time scales as

```text
B_Rindler ~ A_perp / beta^{d-1}.
```

This is a parallel horizon, not a serial Schwarzschild-like one.  It
supports the distinction introduced in the saturation note:

- serial horizons: `B = O(1)` per thermal time, e.g. flat
  Schwarzschild-scale emission with `lambda_T ~ R`;
- parallel horizons: `B >> 1`, e.g. planar/Rindler or large AdS,
  where many thermal cells radiate in parallel.

The invariant cannot be "one outgoing mode."  The invariant has to be:

```text
source entropy per thermal cell is coupling-accessible,
and recovery latency is small compared with ordinary transport.
```

Rindler therefore refines the language.  It separates global
Schwarzschild seriality from local horizon channel density.

## 3. BTZ: the positive holographic control

BTZ is the opposite of Rindler in the useful way.  It has a finite
black-hole entropy and a clean holographic description, while the bulk
gravity has no local propagating gravitons.

For nonrotating BTZ,

```text
M = r_+^2 / (8 G l^2),
T = r_+ / (2 pi l^2),
S_BH = 2 pi r_+ / (4G).
```

So at fixed AdS radius `l`,

```text
S_BH ~ sqrt(M).
```

This is not Schwarzschild's super-Hagedorn `S ~ E^2`.  In a
holographic CFT with the Brown-Henneaux central charge, the state count
is natural: Brown-Henneaux gives

```text
c = 3l / (2G),
```

and Cardy growth reproduces the BTZ entropy.  Strominger's result is
the standard anchor for this matching.  This is a state-counting
success of the holographic description; the microscopic interpretation
inside pure three-dimensional gravity remains a separate question.

Operational translation:

```text
Schwarzschild model: state count is an external exotic input.
BTZ/CFT: state count is an internal high-energy fact of the
holographic CFT.
```

This is the first place where the "three inputs" might stop being
external knobs and become dictionary entries.

## 4. What is boundary saturation in BTZ?

The tempting answer is "automatic, because the dual theory is on the
boundary."  That is too fast.

The sharper answer:

> BTZ converts boundary saturation into a statement about which CFT
> operator algebra is coupled to the exterior bath and how quickly
> perturbations spread through that algebra.

In a high-temperature 2d CFT on a spatial circle of length `L`,

```text
S_CFT ~ c L / beta
```

up to conventional factors.  The natural thermal-cell count is

```text
number of boundary thermal cells ~ L / beta,
entropy per thermal cell ~ c.
```

Thus the BTZ analogue of source-side saturation is not "Planck cells on
a bulk horizon."  It is closer to:

```text
the exterior bath couples to a thermal-band/code-subspace CFT operator
algebra whose participation is of order the Cardy entropy.
```

If the bath couples along the whole boundary, saturation is plausible.
If the bath couples only at one boundary point or through a small set of
operators, saturation can fail even though the state count is Cardy.

This is an important correction.  Holography makes the state count and
the boundary location of the degrees natural, but the emission/recovery
channel is still a coupling question.

## 5. What is latency in BTZ?

Plain BTZ in global AdS is an equilibrium system; reflecting boundary
conditions do not give asymptotically flat evaporation.  To ask a Page
or Hayden-Preskill question, one usually either:

1. couples the boundary CFT to an external bath, or
2. uses an eternal/equilibrium protocol, as in thermofield-double
   descriptions of eternal AdS black holes.

So the BTZ latency question should be stated conditionally:

> Given a bath-coupled or equilibrium recovery protocol, does a diary
> perturbation become recoverable from the bath/boundary record after
> `O(k + log S)` record units?

In CFT language, this becomes an operator-growth question:

```text
Does the perturbation spread across the thermal CFT degrees quickly
enough that the coupled bath algebra sees it at HP latency?
```

For chaotic holographic CFTs the expected answer is yes.  For rational
or integrable CFTs the answer can fail.  That makes BTZ a useful
discriminator:

```text
Cardy density alone does not imply HP latency.
Chaotic/operator-growth structure is the BTZ image of input 3.
```

## 6. Immediate insight from the Rindler-BTZ pair

Rindler and BTZ separate the roles sharply:

```text
Rindler: thermality is cheap and modular.
BTZ: finite entropy can be natural in a dual Hamiltonian.
Neither by itself removes the access/routing question.
```

That suggests the deeper result:

> The black-hole information puzzle is not the existence of horizon
> thermality and not even the existence of a finite horizon state count.
> It is the existence of a finite entropy sector whose information is
> exterior-recoverable at low latency.

The three inputs of the ideal Hamiltonian paper become:

```text
state count      -> Cardy density / BH entropy
boundary access  -> bath-coupled CFT operator participation
mixing           -> CFT operator growth / chaos
```

This is the BTZ dictionary target.

## 7. How this changes the flux-compression lemma

The flux-compression lemma is not merely a repair for a failed
measurement idea.  After Rindler/BTZ, its role is clearer.

Rindler/large-AdS/planar horizons can have many outgoing thermal cells;
flat Schwarzschild/small-AdS/dS can be serial one-wavelength emitters.
But in all cases there is a distinction between:

```text
radiation-mode participation,
source/operator-algebra participation.
```

The linear-algebra obstruction says instantaneous radiation observables
see the compressed matrix

```text
Gamma = C W C^\dagger
```

not the full source Gram kernel `W`.  Therefore the right universal
diagnostic is not a raw instantaneous channel count.  It is the
recoverability of arbitrary deposited information over time.

BTZ sharpens this: in a parallel/holographic setting, some source
structure may become visible spectrally, but the finite-information
question still asks whether the coupled record has enough operator
growth and participation to recover arbitrary perturbations.

## 8. Next concrete moves

1. Add a short Rindler null paragraph to the separation program:
   thermality yes, finite recoverable register no.

2. Add a BTZ dictionary paragraph to the separation program:
   `N_eff` should become CFT operator-algebra participation in a
   thermal band, not a bulk source-cell count.

3. Keep the flux-compression lemma in the saturation paper, but phrase
   it as a distinction between radiation-mode participation and
   source/operator-algebra participation.  That will cover both serial
   Schwarzschild and parallel BTZ/Rindler limits.

4. Do not attempt the anonymity alternatives theorem until the BTZ
   dictionary is clearer.  Otherwise "source-local" and "nonlocal
   encoder" will mean different things in bulk and CFT language.

## 9. Gap check after this pass

The Rindler/BTZ sequence did not exhaust the stress tests.  The
following items should stay visible:

1. **Active mining.**  The compression discussion refers to the natural
   Hawking channel or to a specified bath coupling.  Black-hole mining
   is a different protocol: an apparatus placed near the horizon changes
   the exterior algebra and can access channels that are greybody-
   suppressed or absent in passive asymptotic radiation.  This belongs
   to "which algebra is coupled?", not to state count or thermality.
   Anchor: Unruh-Wald mining,
   https://static1.squarespace.com/static/5852e579be659442a01f27b8/t/586fd5d2d2b8572578ff3e0e/1483724242667/unruh_wald.pdf

2. **Edge modes and crossed products.**  The Gauss/nonfactorization
   axis has more than Raju's holography-of-information formulation.
   Gauge-theory edge modes, gravitational surface symmetries, split
   property issues, and crossed-product algebras are neighboring
   languages for how finite entropy and exterior algebras may arise.
   Anchors:
   Donnelly-Freidel local subsystems, https://arxiv.org/abs/1601.04744
   Donnelly edge entropy, https://arxiv.org/abs/1109.0036
   Witten crossed product, https://arxiv.org/abs/2112.12828

3. **Near-extremal/JT.**  This is the dangerous low-temperature case.
   The finite entropy has a large `S0` piece plus thermally active
   excitations.  The saturation/latency invariant may need to count the
   dynamically active entropy `Delta S(T)` rather than total `S0`, or
   else state explicitly which recovery protocol accesses `S0`.
   Anchor example: JT/near-extremal BTZ thermodynamics,
   https://link.aps.org/doi/10.1103/PhysRevD.107.066019

4. **Large AdS and black branes.**  These are parallel horizons.  They
   test the refinement from "one outgoing mode" to "radiation-mode
   participation versus source/operator-algebra participation."  The
   right language is channel density and butterfly/operator-growth
   velocity, not global seriality.

5. **Causal diamonds.**  These are observer-horizon controls between
   Rindler and de Sitter.  They may help isolate which parts of the
   framework need a true event/cosmological horizon and which need only
   finite observer access.

Net effect: the plan is still Rindler -> BTZ -> flux compression, but
with two added scope guards.  First, specify passive radiation/bath
coupling versus active mining.  Second, keep edge/crossed-product
language on the nonfactorization axis so the Gauss branch is not
underdeveloped.

## Provisional conclusion

The strongest insight so far is not a new horizon slogan.  It is a
factorization of the problem:

```text
Rindler explains thermal kinematics.
BTZ explains how finite state count can be natural in a dual Hamiltonian.
Boundary saturation and latency explain why finite information becomes
operationally recoverable.
```

Gravity-like issues appear already at the Rindler level, but the
black-hole information problem requires the finite-budget/recovery
layer.  BTZ is the best test of whether the three inputs are merely a
toy-model scaffold or the operational image of holography.
