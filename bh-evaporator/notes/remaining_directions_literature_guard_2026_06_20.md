# Remaining Directions Literature Guard

Date: 2026-06-20

Role: literature guard / decision matrix

Status: first-pass collision map

Purpose: apply the constrained-access postmortem's start rule to the
remaining proposed directions before investing in more drafting or proof
work.

## Summary Verdict

The remaining bh-evaporator directions are not equally exposed.

```text
most crowded:
    operational Hamiltonian necessity / Page-decoupling model

crowded but maybe still useful:
    super-Hagedorn / corpuscular kinematics
    variance / half-wormhole layer

least obviously preempted, but still needs a sharper ownership check:
    boundary saturation / de Sitter reservoir contrast
```

The program-level lesson is the same as in the constrained-access
postmortem: every candidate must be stated as a mechanism claim, then
checked against its natural owner fields before it becomes a draft.

## 1. Boundary Saturation / de Sitter Reservoir Contrast

### Proposed Mechanism

The proposed invariant is:

```text
horizon-class system:
    the full entropy is coupling-accessible
    N_access ~ S

ordinary local reservoir:
    only the contact surface is coupling-accessible
    N_access ~ S^{(d-1)/d}
```

For de Sitter, the state-count input itself looks ordinary: the
Schwarzschild--de Sitter cosmological-horizon entropy deficit matches
the finite-reservoir expansion through second order, with
`C_eff = S_0`. The proposed contrast is therefore:

```text
state-count input:
    exotic for Schwarzschild
    ordinary finite-reservoir bookkeeping for de Sitter

boundary saturation:
    nontrivial for both
```

### Likely Prior Owners

- black-hole thermodynamics and holographic entropy bounds;
- stretched horizon and membrane paradigm;
- Bekenstein--Mayo / Pendry information-channel bounds;
- de Sitter static-patch algebra and Type II_1 work;
- de Sitter holography of information;
- finite-bath statistical mechanics.

### Collision Findings

Known nearby results:

- CLPW construct a Type II_1 algebra of de Sitter static-patch
  observables, with empty de Sitter as the maximum-entropy state and
  entropy matching generalized entropy up to a constant.
- Chakraborty--Chakravarty--Godet--Paul--Raju formulate holography of
  information in de Sitter: suitably small-region observables can
  specify the state in quantum gravity.
- Bekenstein--Mayo argue that black holes behave as one-dimensional
  entropy/information channels, not as ordinary three-dimensional
  emitters.
- Finite-reservoir corrections are standard statistical mechanics; the
  expansion of `S_R(E_tot - E)` is not new by itself.

What did not immediately appear in the first pass:

```text
"boundary saturation" as a named invariant comparing
source-side coupling-accessible entropy against total entropy,
with ordinary reservoirs giving exponent (d-1)/d and horizons giving 1.
```

This does not prove novelty. It says the exact proposed invariant was
not immediately swallowed by the obvious ancestors.

### Remaining Opening

The plausible opening is narrow:

```text
boundary saturation as a source-side coupling invariant,
not as an entropy bound, transport coefficient, or information-flux
capacity.
```

The dS reservoir lemma is not the result by itself. It is the contrast
engine: dS makes the state-count input look ordinary, so the horizon
content has to sit in saturation and/or constraints.

### Recommendation

Keep this as the leading candidate, but do a focused second-pass search
before drafting:

```text
search target:
    horizon entropy as coupling-accessible channel count
    surface-contact versus whole-entropy accessibility
    membrane/stretched-horizon channel counting
    dS static-patch recovery or HP-like protocols
```

If this second pass also comes back empty, this is the best remaining
bh-evaporator direction.

## 2. Super-Hagedorn State Count / Forced Corpuscular Kinematics

### Proposed Mechanism

From:

```text
S(E) ~ E^2
boundary-accessible cells carry O(1) entropy
energy shared among active cells
```

derive:

```text
N(E) ~ E^2 cells
energy per active cell ~ E/N ~ 1/E ~ T
```

This gives the Dvali--Gomez-style corpuscular picture as forced
kinematics rather than as a postulated microscopic model.

### Likely Prior Owners

- Dvali--Gomez quantum N-portrait;
- black-hole holographic principle and entropy bounds;
- local QFT entropy bounds / 't Hooft / Bousso;
- long-range systems, negative heat capacity, ensemble inequivalence;
- self-gravitating statistical mechanics.

### Collision Findings

The core corpuscular scaling is already owned:

- Dvali--Gomez: black holes as condensates of `N` soft gravitons,
  `N` equal to entropy, wavelength `sqrt(N) l_P`, interaction strength
  `1/N`, Hawking temperature `T ~ 1/sqrt(N)`.
- Dvali--Gomez critical-point papers: entropy carried by nearly gapless
  Bogoliubov modes at a quantum critical point.
- Holographic bounds already express the incompatibility between
  ordinary local volume state counting and black-hole entropy.

### Remaining Opening

The only nontrivial remaining angle is not the scaling itself. It is:

```text
given only thermodynamic inputs,
show that any boundary-accessible realization must land on
corpuscular kinematics;
then isolate the missing interaction that stabilizes it.
```

That is a demarcation lemma, not a new corpuscular model.

The larger possible result would be a stabilization mechanism:

```text
derive a non-gravitational or effective many-body interaction
whose stable/critical phase naturally has
N ~ E^2 soft accessible cells with energy per cell ~ 1/E.
```

That remains open, but it is a harder microscopic-model program, not a
short paper from the existing notes.

### Recommendation

Do not present forced corpuscular kinematics as a central new result.
Use it as a bridge and target statement:

```text
the three thermodynamic inputs force the same kinematic destination as
the N-portrait; the open problem is the stabilizing interaction.
```

Worth pursuing only if the next step is a concrete stabilization model,
not another demarcation note.

## 3. Operational Hamiltonian Model / Necessity Claims

### Proposed Mechanism

Given three inputs:

```text
Schwarzschild density of states
boundary-accessible emission algebra
decoupling / mixing
```

derive:

```text
thermality
Schwarzschild luminosity/lifetime
Page/island recovery
mirror algebra
complexity barrier
```

and show each input is necessary for its phenomenology layer.

### Likely Prior Owners

- Page theorem and Hayden--Preskill decoupling;
- one-shot decoupling and black-hole toy models;
- random dynamics / GUE / Haar Page-curve models;
- unitary evaporation toy models;
- replica-wormhole toy models.

### Collision Findings

This is heavily occupied:

- Bradler--Adami: one-shot decoupling and Page curves from a dynamical
  black-hole evaporation model.
- Liu--Vardhan: Page curve from quantum-chaos/operator-gas dynamics.
- de Boer--Hollander--Rolph: Page curves and replica-wormhole-like
  contractions from random dynamics.
- Alsing and related optical/unitary evaporation models: Page curves
  and unitary toy evaporation.
- Standard HP/decoupling literature owns the recovery threshold once
  the state count and subsystem split are supplied.

### Remaining Opening

The existing draft's contribution is mainly:

```text
a conditional, explicitly Hamiltonian bookkeeping model that isolates
which black-hole inputs are doing which phenomenological work.
```

That is valuable as a careful model paper, but it is not an uncovered
mechanism. The strongest version is a modest precision/demarcation paper:

```text
the operational Schwarzschild horizon package is ordinary quantum
mechanics once the three inputs are supplied; the gravitational residue
is exactly the origin of those inputs.
```

### Recommendation

Do not invest in this as a new result direction. Finish or archive it
only if it serves one of two purposes:

1. a technical companion that supports another sharper result;
2. a clean conditional model paper with conservative claims.

## 4. Variance / Half-Wormhole Layer

### Proposed Mechanism

Extend the model's mean-level identity:

```text
replica-wormhole saddle sum
=
Hamiltonian / ETH permutation contraction sum
```

to variance:

```text
connected second-order classes
~
half-wormhole corrections / factorization-restoring terms.
```

### Likely Prior Owners

- Saad--Shenker--Stanford--Yao half-wormholes;
- SYK fixed-coupling factorization literature;
- replica wormholes and random-matrix ensemble averaging;
- second-order freeness / random matrix fluctuations;
- random-dynamics Page-curve models.

### Collision Findings

The general idea is occupied:

- SSSY introduce half-wormholes to restore factorization at fixed
  couplings.
- Mukhametzhanov analyzes half-wormholes in the one-time-point SYK
  model.
- de Boer--Hollander--Rolph already connect random dynamics, Page
  curves, and replica-wormhole-like contractions.

What may remain:

```text
a specific second-order-freeness/variance calculation for the present
evaporation Hamiltonian, showing exactly which connected ETH classes
play the role of half-wormholes.
```

That would be a technical bridge, not a conceptual first.

### Recommendation

This is worthwhile only if the calculation is short and concrete. The
question to answer before starting is:

```text
Can we compute a variance that the existing random-dynamics papers do
not already compute, and does it teach anything about fixed Hamiltonians
rather than ensembles?
```

If yes, it may be the best technical add-on. If no, drop.

## Ranking After First Pass

For possible new results:

```text
1. Boundary saturation / dS reservoir contrast
   Still has a possible unclaimed invariant, but needs a second-pass
   literature check before drafting.

2. Variance / half-wormhole calculation
   Crowded conceptually, but a concrete calculation may still add value.

3. Super-Hagedorn / corpuscular kinematics
   Useful demarcation; real result would require a stabilization model.

4. Operational Hamiltonian necessity
   Mostly synthesis/precision; not a result engine.
```

## Immediate Next Step

Do not draft any of these yet.

Run a focused second-pass literature guard on candidate 1:

```text
query family:
    horizon entropy coupling channels
    accessible horizon degrees of freedom
    stretched horizon channel count
    membrane paradigm entropy channel count
    black hole as information channel
    dS static patch recovery / Hayden-Preskill
```

If candidate 1 survives that pass, it is the next serious push. If it
does not, the honest conclusion is that bh-evaporator is now mostly in
cleanup/companion mode, and new-result effort should move to another
program.

---

## Candidate 1 Second-Pass Guard: Boundary Saturation

Date: 2026-06-20

### Search Target

This pass looked specifically for prior ownership of the claim:

```text
horizon-class systems are thermal systems whose full entropy is
coupling-accessible, in the sense that a source-side coupling/channel
participation number scales as N_access ~ S, while ordinary local
reservoirs coupled through a contact surface give
N_access ~ S^{(d-1)/d}.
```

This is narrower than:

- entropy proportional to area;
- entropy located near the horizon;
- membrane transport coefficients;
- black holes as information channels;
- holographic entropy bounds;
- fast scrambling.

### Searches That Did Not Find A Direct Owner

Direct phrase searches for variants of:

```text
coupling-accessible entropy horizon
boundary saturation black hole entropy channels
channel count black hole entropy horizon
accessible degrees of freedom horizon entropy coupling
full entropy horizon recoverable Hayden-Preskill
surface-contact versus whole-entropy accessibility
```

did not return a named invariant or a close formulation.

This is not evidence of novelty by itself, but it means the exact
language is not sitting in the obvious keyword neighborhood.

### Adjacent Ancestors Found

**Bekenstein--Mayo / information-flux channel.**

`gr-qc/0105055`, "Black holes are one-dimensional," argues that, for
entropy or information flow, a black hole behaves like a one-dimensional
channel; entropy output is related to emitted power as in a 1D channel.
This is close to the compression/bandwidth side, not the source-side
participation invariant. It says how entropy flows out; it does not
compare the coupled source-algebra rank to total entropy or contrast it
with ordinary reservoirs.

Related later papers study the "dimension" or rate of the entropy
emission channel. These are flux-capacity relatives, not full-entropy
coupling-accessibility criteria.

**Membrane paradigm / stretched horizon.**

The membrane paradigm supplies surface transport coefficients and a
surface description of exterior black-hole physics. Stretched-horizon
and complementarity lore say infalling information is absorbed,
scrambled, and re-emitted by horizon degrees of freedom. This is the
closest conceptual ancestor. The difference is that it presupposes a
surface/horizon description and does not formulate a normalization-free
exponent:

```text
log N_access / log S
```

nor the ordinary-reservoir comparison `S^{(d-1)/d}`.

**Entropy-location literature.**

Das--Shankaranarayanan and related entanglement-entropy work ask where
the degrees of freedom responsible for black-hole entropy are located.
The answer is near the horizon for ground-state entanglement, with
excited states contributing differently. Teitelboim's surface-field
work gives black-hole entropy from additional horizon surface fields.
These are location/counting claims, not coupling-accessibility claims.

**Holographic and Bekenstein/Bousso bounds.**

The holographic principle and covariant entropy bounds say entropy is
bounded by area. They are bounds or geometric state-count statements.
They do not distinguish an ordinary local reservoir that satisfies an
area bound from a horizon whose full entropy is exposed to the coupling
algebra.

**Fast scrambling / expander / SYK lore.**

Fast-scrambler literature addresses the internal mixing graph and the
`log S` timescale. It is orthogonal to the proposed invariant unless
combined with the emission/coupling algebra. This was the same
separation learned in the constrained-access postmortem.

**de Sitter algebra / HoI.**

CLPW and dS HoI are crowded and important. They cover static-patch
observer algebras, Type II_1 structure, maximum-entropy empty de Sitter,
and small-region determination of the gravitational state. They do not,
in the searched formulations, package the operational distinction as a
source-side coupling-saturation exponent.

### What Survives

The candidate survives as a narrow invariant:

```text
boundary saturation =
    the participation rank of the source-side coupling algebra scales
    like the total entropy.
```

The clean contrast is:

```text
horizon:
    N_eff(source coupling) ~ S

ordinary d-dimensional reservoir with contact surface:
    N_eff(source coupling) <= const * S^{(d-1)/d}
```

The dS reservoir lemma then plays a supporting role:

```text
dS state-count input can look like ordinary finite-bath bookkeeping,
but a bath that matches that spectrum still fails boundary saturation.
```

This is not "entropy lives on the horizon" and not "black holes emit
through a one-dimensional channel." It is a statement about the rank and
participation structure of the coupling algebra relative to the state
count.

### Main Weakness

The invariant is model-side and source-side. The original flux/HBT
measurement route failed because radiation-mode participation is not
source-kernel participation. The latency certificate partly repairs
this, but latency itself is heavily overlapped with HP/locality
literature.

So the paper must be honest:

```text
model-side invariant:
    N_eff of the source-side coupling Gram kernel;

exterior certificate:
    recovery latency, conditional on mixing/export assumptions;

not claimed:
    direct extraction of N_eff from instantaneous flux statistics.
```

### Decision

Candidate 1 survives the second-pass guard better than the constrained
access direction did.

The next worthwhile work is not broad drafting. It is one technical
tightening:

```text
make the source-side N_eff theorem and ordinary-reservoir bound
referee-proof, then decide whether the dS contrast is strong enough
to carry a short note.
```

If that theorem is solid, the result is modest but real:

> Holographic horizons are not merely high-entropy thermal systems or
> fast scramblers; relative to ordinary local reservoirs, they saturate
> the coupling-accessible fraction of their entropy.

That statement appears less mined than the access/recovery program.

### Follow-Up Patch Status

The boundary-saturation working draft has been tightened to match this
decision:

```text
primary result:
    source-side Gram-kernel participation exponent

ordinary-reservoir theorem:
    local contact coupling gives sigma_acc <= (d-1)/d

latency theorem:
    exterior certificate once mixing/export are included
```

This keeps the candidate away from the crowded HP/recovery literature
as much as the idea allows. The remaining technical risk is now sharply
localized: whether the source-side horizon calibration
`N_eff ~ S` can be defended as a physical horizon input rather than a
model convention, especially in the de Sitter leg.
