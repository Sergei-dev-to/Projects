# dS literature collision matrix: first source pass (2026-06-12)

Purpose: record the first primary-source pass through the Raju/CLPW/dS-HoI/QRF
literature, translate the relevant claims into the operational-horizon program,
and prepare precise packets for Claude to review.  This pass used arXiv TeX
sources where available, not PDF text.

## Source files used

Local source cache used for this pass:

- Raju, "Lessons from the Information Paradox", arXiv:2012.05770:
  [lessons.tex](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2012.05770/lessons.tex)
  ([arXiv](https://arxiv.org/abs/2012.05770), [source](https://arxiv.org/e-print/2012.05770))
- Chandrasekaran-Longo-Penington-Witten, "An Algebra of Observables for de Sitter Space",
  arXiv:2206.10780:
  [DeSitter.tex](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2206.10780/DeSitter.tex)
  ([arXiv](https://arxiv.org/abs/2206.10780), [source](https://arxiv.org/e-print/2206.10780))
- Chakraborty-Chakravarty-Godet-Paul-Raju, "The Hilbert Space of de Sitter Quantum Gravity",
  arXiv:2303.16315:
  [hilbqg.tex](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16315/hilbqg.tex)
  ([arXiv](https://arxiv.org/abs/2303.16315), [source](https://arxiv.org/e-print/2303.16315))
- Chakraborty-Chakravarty-Godet-Paul-Raju, "Holography of Information in de Sitter Space",
  arXiv:2303.16316:
  [dsholinfo.tex](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16316/dsholinfo.tex)
  ([arXiv](https://arxiv.org/abs/2303.16316), [source](https://arxiv.org/e-print/2303.16316))
- De Vuyst-Eccles-Hohn-Kirklin, "Gravitational Entropy is Observer-Dependent",
  arXiv:2405.00114:
  [shortversion.tex](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2405.00114/shortversion.tex)
  ([arXiv](https://arxiv.org/abs/2405.00114), [source](https://arxiv.org/e-print/2405.00114))
- De Vuyst-Eccles-Hohn-Kirklin, "Crossed Products and Quantum Reference Frames:
  On the Observer-Dependence of Gravitational Entropy", arXiv:2412.15502:
  [therealdraft.tex](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2412.15502/therealdraft.tex)
  ([arXiv](https://arxiv.org/abs/2412.15502), [source](https://arxiv.org/e-print/2412.15502))

The local cache path is temporary.  The arXiv source links are the durable
reconstruction path.

## Executive picture

The literature pass supports the current demarcation but changes where the
emphasis should go.

1. The dS reservoir lemma survives, but only if stated as a second-order
   refinement.  CLPW already says the first-order thermal factor is entropic.
   The apparent new point is the finite-reservoir match through second order,
   with `C_eff = S_0`.
2. Raju strongly supports treating the Schwarzschild Hamiltonian model as an
   explicit factorized foil.  His claim is that gravity violates factorization
   radically; our construction is useful precisely because it makes the
   nongravitational bookkeeping explicit.
3. The dS HoI paper supports the Stage-B constraint question, but also makes a
   crucial distinction: mathematical state determination by gauge-fixed
   correlators is not operational local accessibility by an observer.
4. The Hohn/QRF line makes the clock/crossed-product part crowded.  Stage B
   should not be framed as discovering "Page-Wootters equals CLPW"; that is
   already their claim.  Our differentiator is the operational-horizon trinity
   and finite factorized/constrained benchmark.
5. Boundary saturation still looks least crowded: `N_access ~ S` as an
   operational invariant is adjacent to membrane/holographic lore, but it did
   not appear in this first source pass as a named channel-count criterion.

## Claim packet A: dS reservoir lemma

### Literature claims

CLPW already gives the first-order entropic suppression story.  In the
introduction they describe a particle of energy `E` in the static patch as
reducing the cosmological horizon area by a first-law term,

```tex
A_{\mathrm{hor}}/4G = A_{\dS}/4G - \beta_{\dS} E.
```

See [DeSitter.tex, around lines 292-304](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2206.10780/DeSitter.tex:292).
They then say that if the full static-patch microstates are equiprobable, the
probability of seeing energy `E` is

```tex
p(E) = \exp(-\beta_{dS} E).
```

Their language is explicitly entropic: the thermal distribution arises from
entropic rather than energetic suppression on the full static-patch Hilbert
space.

CLPW also frames empty de Sitter as the maximum-entropy state of the Type
II_1 algebra, with density matrix the identity.  See
[DeSitter.tex, around lines 327-333](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2206.10780/DeSitter.tex:327).

### Our claim

The first-order term is not new.  The new candidate observation is the
second-order finite-reservoir interpretation:

```tex
S_c(M)=S_0-\beta M-2\pi M^2+\cdots
```

matches an ordinary reservoir expansion

```tex
S_R(E_{\rm tot}-E)
 = S_0-\beta E-\frac{E^2}{2T^2C}+\cdots
```

with

```tex
C_{\rm eff}=S_0.
```

This says that dS input 1 is not merely "compatible with" ordinary bath
physics; through second order it is exactly the generic large finite reservoir
form, with an unremarkable effective heat capacity of order entropy.

### Program consequence

For Schwarzschild, input 1 is exotic: `S(E) ~ E^2` is super-Hagedorn and
cannot be supplied by ordinary local finite-density state counting.

For de Sitter, input 1 is ordinary: `S(E) = S_0 - beta E - E^2/(2T^2C)+...`
is finite-bath thermodynamics.

Therefore the dS gravitational residue must live in one of two places:

- boundary saturation, `N_access ~ S_0`;
- constraint/observer/Gauss-law structure.

### Claude question

Ask Claude:

> CLPW already states first-order entropic suppression in de Sitter:
> `p(E) ~ exp(-beta E)`.  Does the second-order SdS/reservoir match
> `C_eff = S_0` appear in CLPW, Raju, Hohn/QRF, or nearby dS
> thermodynamics?  If not, is it a useful demystification of dS input 1,
> or too elementary to foreground?

## Claim packet B: Raju and the factorized benchmark

### Literature claims

Raju's review states the holography-of-information principle very strongly:
in quantum gravity, information on a Cauchy slice is also available near the
boundary, and applied to black holes the exterior retains a complete copy of
the interior information.  See [lessons.tex, abstract around line 307](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2012.05770/lessons.tex:307).

The key factorization passage is even stronger.  Raju says the assumption of
factorization fails "as completely as possible": the degrees of freedom in the
exterior region contain the would-be interior degrees of freedom.  See
[lessons.tex, around lines 1256-1261](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2012.05770/lessons.tex:1256)
and [lessons.tex, around lines 3307-3314](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2012.05770/lessons.tex:3307).

Raju also warns that for asymptotically flat black holes the Page curve should
not be interpreted as information emerging from the black hole; the information
is already outside in the gravitational theory.  See
[lessons.tex, around lines 3321-3325](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2012.05770/lessons.tex:3321).

### Our claim

The Schwarzschild Hamiltonian model should be positioned as the explicit
factorized benchmark:

- It intentionally uses `B tensor R` bookkeeping.
- It therefore has an ordinary Page/island/recovery story.
- That story is valuable because it shows what follows from factorized quantum
  mechanics plus the three inputs.
- Raju's gravity claim is not contradicted; it identifies exactly what the
  model leaves for the Gauss-law/constrained completion.

### Program consequence

Do not fight Raju on his own terrain.  Use him as the reason the Stage 0
factorized benchmark is useful: it is the clean nongravitational foil whose
Page curve can be compared with Stage A/B constraints.

### Claude question

Ask Claude:

> Given Raju's claim that gravitational factorization fails completely, is our
> factorized Hamiltonian model best framed as (i) a countermodel, (ii) a
> benchmark/foil, or (iii) the nongravitational bookkeeping limit of the
> island/Page-curve story?  Which phrasing avoids sounding like a rebuttal
> while preserving the contribution?

## Claim packet C: dS holography of information and operational access

### Literature claims

The dS HoI paper proves that cosmological correlators in an arbitrarily small
region determine the state.  This appears already in the abstract:
[dsholinfo.tex, around lines 614-616](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16316/dsholinfo.tex:614).

But the paper repeatedly cautions that this is not the same as a physical
observer locally measuring the whole state.  The relevant caveats:

- the "small region" on the late-time Cauchy slice still has infinite physical
  volume;
- cosmological correlators are gauge-fixed observables;
- they are secretly nonlocal;
- high-point correlators may be effectively inaccessible.

See [dsholinfo.tex, around lines 647-651](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16316/dsholinfo.tex:647),
[dsholinfo.tex, around lines 771-773](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16316/dsholinfo.tex:771),
and [dsholinfo.tex, around lines 1431-1440](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16316/dsholinfo.tex:1431).

They also explicitly say the effect is not from measuring small gravitational
tails but from imposing the gravitational Gauss law.  See
[dsholinfo.tex, around lines 1366-1371](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2303.16316/dsholinfo.tex:1366).

### Our claim

This is almost tailor-made for Stage B.  The finite constrained model should
separate:

- mathematical redundancy: the state is determined by a restricted algebra;
- operational access: a physical observer can extract the information with
  feasible measurements;
- error scale: exact availability vs `O(exp(-S_0))` availability.

### Program consequence

The Stage B question should not simply be "does HoI occur?"  It should be:

1. Which HoI signature is reproduced by ordinary constraints?
2. Which requires the Hamiltonian/clock constraint?
3. Which requires full gravitational gauge structure?
4. Does the finite model produce exact availability or only exponentially
   small distinguishability?

### Claude question

Ask Claude:

> The dS HoI paper distinguishes mathematical state determination by
> gauge-fixed correlators from operational local measurement by an observer.
> In our finite constrained model, what is the right observable analogue:
> reduced states of small subsystems, restricted algebras, high-point moments,
> or relational correlators?  Which analogue best tests exact vs `e^{-S_0}`
> information availability?

## Claim packet D: Hohn/QRF overlap and Stage B

### Literature claims

The QRF/crossed-product line is highly overlapping with any naive Stage B.
The long QRF paper says that accounting for gauge invariance and observer
degrees of freedom converts Type III QFT algebras to Type II crossed products,
and that entropy becomes observer-dependent.  See
[therealdraft.tex, abstract around line 71](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2412.15502/therealdraft.tex:71).

It has an explicit section titled:

```tex
Realisation in perturbative quantum gravity: PW = CLPW
```

See [therealdraft.tex, around lines 587-600](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2412.15502/therealdraft.tex:587).

They also discuss semiclassical and antisemiclassical clock regimes, with
entropy formulas depending on clock properties.  See
[therealdraft.tex, around lines 115-119](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2412.15502/therealdraft.tex:115)
and [therealdraft.tex, around lines 1909-1915](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2412.15502/therealdraft.tex:1909).

The short version makes an operational point: the choice of which QRFs can be
used is an operational input, and different QRF choices can describe different
physical degrees of freedom in the same region.  See
[shortversion.tex, around lines 56-64](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2405.00114/shortversion.tex:56),
[shortversion.tex, around lines 368-370](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2405.00114/shortversion.tex:368),
and [shortversion.tex, around lines 501-503](C:/Users/serge/AppData/Local/Temp/bh_evaporator_lit_sources_20260612/2405.00114/shortversion.tex:501).

### Our claim

Stage B is crowded if framed as:

- "constraints plus clocks produce crossed products";
- "Page-Wootters explains CLPW";
- "observer entropy is QRF-dependent."

Those are already in the Hohn/QRF line.

The remaining differentiated Stage B is:

- finite-dimensional operational-horizon benchmark;
- Stage 0/Stage A/Stage B comparison;
- trinity discipline: state count, boundary access, recovery/mixing;
- exact vs exponentially small information availability;
- relation to Page/island/recovery signatures, not only algebraic entropy.

### Program consequence

Do not build the next paper around "PW = CLPW."  Build it around:

```text
Which operational-horizon signatures appear in a finite constrained model?
```

Stage table:

| Signature | Stage 0 factorized | Stage A ordinary charge | Stage B Hamiltonian/clock | Gravity residue |
|---|---|---|---|---|
| constant-T detailed balance | yes | yes | yes | no |
| maximum-entropy empty state | yes, via reservoir | yes | yes | no |
| boundary saturation N_access~S_0 | input | input | input | microscopic origin |
| Page/recovery bookkeeping | yes, if R chosen | deformed? | question | HoI/factorization |
| observer-relative entropy | no | limited | likely | exact gravitational version |
| HoI exact availability | no | charge only | question | maybe |

### Claude question

Ask Claude:

> Hohn/QRF already claims PW = CLPW and develops observer-dependent entropy
> from clocks and crossed products.  What differentiated Stage-B claim remains
> for us if we restrict to finite operational-horizon models and the
> Stage-0/A/B signature table?  Is that enough for a paper, or should Stage B
> be subordinate to boundary saturation?

## Claim packet E: boundary saturation

### Literature claims found in this pass

This first source pass did not find the proposed invariant in the Raju/CLPW/dS
HoI/QRF sources:

```tex
N_{\rm access} \sim S
```

meaning that the full entropy of the thermal horizon system is carried by
coupling-accessible contact cells.

There are adjacent ideas:

- CLPW/Banks/Susskind: finite static-patch Hilbert space of size
  `exp(A_dS/4G)`;
- membrane/stretched-horizon lore: horizon degrees of freedom live at a
  surface;
- QRF line: "access" to algebras depends on clocks/reference frames;
- holographic principle: entropy scales like area.

But these are not the same operational statement.

### Our claim

Boundary saturation says:

```tex
N_{\rm access} \sim S
```

For an ordinary local reservoir in three spatial dimensions,

```tex
S \sim V,\qquad N_{\rm contact}\sim A \sim S^{2/3}.
```

For Schwarzschild and de Sitter horizons, the operational evidence points to
the saturated scaling:

```tex
N_{\rm access}\sim S.
```

In Schwarzschild this is measured by the luminosity law:

```tex
P \sim N_{\rm access} T^4,\qquad
T\sim E^{-1},\qquad P\sim E^{-2}
```

so `N_access ~ E^2 ~ S`.

In de Sitter there is no net luminosity, so the measurement leg should be
relaxation/fluctuation response of static-patch perturbations.  The candidate
claim is that the channel-count exponent is visible in how equilibrium
relaxation rates or fluctuation spectral weights scale with `S_0`:

```tex
N_{\rm access}\sim S_0
```

for a horizon reservoir versus

```tex
N_{\rm contact}\sim S_0^{2/3}
```

for an ordinary local reservoir with only surface contact.

### Pressure point

Rates measure something closer to total spectral weight:

```tex
\Gamma \sim N_{\rm access} g^2 \rho
```

not bare `N_access`.  The lemma needs a comparable-channel normalization, or
an operational definition of `N_eff` from measured inclusive rates and single
channel smoothness.  This is the dS analogue of the Schwarzschild
boundary-accessibility caveat.

### Program consequence

Boundary saturation is currently the best candidate central invariant because:

- it survives the Schwarzschild/dS comparison;
- it is not obviously already in the Raju/CLPW/QRF source set;
- it is method-native: it emerged only by running the same trinity discipline
  on two horizons;
- it avoids the crowded "PW = CLPW" lane.

### Claude question

Ask Claude:

> Is boundary saturation, defined operationally as
> `N_access ~ S` rather than ordinary contact scaling `S^{2/3}`, already
> present in membrane paradigm, stretched horizon, brick wall, CLPW, Raju HoI,
> or QRF literature?  If adjacent but not identical, what is the cleanest way
> to distinguish it?

## Proposed next note/paper skeleton

Working title:

```text
Boundary Saturation as the Operational Horizon Invariant
```

Core claims:

1. The operational-horizon trinity has three inputs: state count, boundary
   accessibility, and recovery/mixing.
2. Schwarzschild makes the state-count input exotic: `S(E) ~ E^2`.
3. de Sitter makes the state-count input ordinary: finite-reservoir
   thermodynamics through second order.
4. The input that remains nontrivial in both cases is boundary saturation:
   the coupling-accessible channel count scales as the full entropy.
5. Constraint/observer/Gauss-law structure is a second dS residue, not a
   replacement for boundary saturation.

Minimal lemmas:

1. Schwarzschild luminosity fixes `N_access ~ S`.
2. SdS entropy deficit matches a finite reservoir through second order with
   `C_eff = S_0`.
3. Ordinary local reservoirs have contact-channel scaling below entropy
   scaling, e.g. `N_contact ~ S^{2/3}` in three dimensions.
4. dS horizon response must be measured by equilibrium relaxation/fluctuation
   spectral weight; this is the unresolved measurement lemma.

What to ask Claude after this note:

1. Does packet A overclaim novelty?
2. Does packet E already exist under another name?
3. Is packet D enough to justify postponing Stage B?
4. What is the cleanest definition of `N_access` that cannot be dismissed as a
   coupling-normalization convention?
