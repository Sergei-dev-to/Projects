# How Does a Black Hole Give Information Back?

Date: 2026-07-12

Updated: 2026-07-13 after adding the effective dynamical-bridge literature,
the final program endpoint, and the handoff to theory-specific successor work.

Status: final accessible account of the program's question, findings, and
endpoint. The detailed technical ledger is
`evaporation_framework_comparison_map_2026_07_12.md`; the concise wrap-up is
`program_endpoint_and_standalone_results_2026_07_13.md`.

## A furnace that may also be a transmitter

Imagine a sealed furnace whose interior is hidden while every emission remains
available for study. From the color and intensity of its glow, you can infer its
temperature. You can measure how quickly it is losing energy. You can discover
which frequencies escape easily and which are absorbed.

Now suppose someone dropped a book into the furnace. Does the outgoing light
contain the book's information?

Finding that the glow is thermal does not answer the question. The book might
truly have been destroyed. Its contents might appear as tiny changes in
individual photons. They might be spread across delicate correlations among
many photons, so that no small group reveals a readable word. Or the furnace
might retain the information until a final release.

Black-hole evaporation presents an extreme version of this puzzle. Stephen
Hawking's calculation showed that a black hole emits nearly thermal radiation.
The temperature is set by the black hole's mass, and the radiation slowly
drains that mass away. The leading calculation leaves open how the precise
quantum state of the matter that formed the black hole reappears in the
radiation.

The program set out to determine how far that connection had already been
constructed and what a non-gravitational control model could teach us. This
reevaluation records the resulting answer and the questions that belong to
future quantum-gravity work.

The program began by looking for a clean dividing line: gravity would provide
certain special ingredients, and ordinary quantum information theory would do
the rest. That division turned out to depend too much on the description.
Different theories divide the same physics into geometry, fields, particles,
matrices, and quantum codes in different ways.

The better approach is comparative. For each account of evaporation, ask what
it assumes, what it calculates, and exactly what it establishes about the
return of information. Results from the literature count just as much as
results produced here. The goal is an answer to the physical question;
provenance records who supplied each part of that answer.

## The answer in brief

One ordinary unitary quantum process can combine a nearly thermal glow,
black-hole-like heating during shrinkage, a decreasing internal state space, a
Page-like entropy turnover, and recoverable information in the complete
radiation record. The project's unified control model realizes these features
in one evolving state. Independent effective and fixed-Hamiltonian models in
the literature show more directly how state-dependent radiation dynamics can
produce reconstruction.

The project therefore ends with a compatibility result and a dependency map.
Four things have to be supplied by a microscopic account: the state count and
thermodynamics, the physical radiation observables, the emission and mixing
dynamics, and a consistent unitary accounting of every remaining system. Once
those are present, quantum-information results explain much of the encoding
and recovery architecture.

For a real black hole, the hard question moves one level deeper. A fundamental
theory must derive those ingredients rather than select them for a control
model. That top-down task remains open, but it is successor research rather
than an unfinished step in the present program.

## Four claims hidden inside one paradox

People often ask whether information “comes out” of a black hole. That phrase
can mean at least four things.

### The information has a final destination

If the complete evolution is unitary, quantum information is not fundamentally
destroyed. As a black hole evaporates, its capacity to hold information
shrinks. If no large remnant or inaccessible archive remains at the end, the
information must ultimately be in the radiation.

This says where the information has to be once evaporation is over. The time at
which the radiation first becomes sensitive to it remains open.

### The outgoing signal depends on the input

Consider two black holes that are identical in mass and charge but differ in
one private quantum bit. Physicists often imagine throwing in a “diary”: a
small quantum message whose later fate can be tracked.

When do those two choices begin to produce different radiation histories? The
difference might appear in one outgoing particle. It might appear only in
correlations among emissions at widely separated times. It might remain
invisible until the final stage.

This is a question about the actual sequence of emissions.

### The radiation contains a reconstructible encoding

A message can be present in a collection even when it is invisible in each
piece. Quantum error-correcting codes do this deliberately. A logical quantum
bit can be spread across many physical systems so that no small subset contains
it, while a sufficiently large subset can reconstruct it exactly.

Black-hole information can be distributed in the same way. We can therefore
ask whether operations on the radiation can represent the measurements and
transformations needed to reconstruct the diary, even when no simple
measurement reveals it. Physicists express this by saying that the diary is
represented in the radiation's observable algebra.

This is an existence claim: in principle, the information can be reconstructed
from the radiation.

### An observer can use a decoder

An encoding theorem establishes existence under stated conditions. A usable
decoder asks more. The reconstruction may work only for a controlled family of
states. It may require detailed knowledge of the initial black hole. The
decoding operation may also be fantastically complex.

The strongest claim therefore specifies who has access to which radiation,
what they know, and how accurately they can recover the diary.

These four questions occupy two logical roles. The destination question is a
constraint on the completed evaporation. The other three compare progressively
stronger claims about the radiation available at a chosen time:

```text
endpoint question:
  Where must the information finally reside?

at any chosen time:
  state-dependent radiation
            ↓ stronger claim
  reconstructible encoding
            ↓ stronger claim
  a decoder with stated access and error
```

Different parts of black-hole physics answer different parts of this scheme.

## What successive results have established

### Hawking calculated the furnace

Hawking treated quantum fields on the curved spacetime produced by a collapsing
star. The changing geometry mixes what different observers call positive- and
negative-frequency waves. A distant observer consequently sees particles with
a thermal spectrum.

The calculation explains why a black hole has a temperature and radiates. With
additional propagation through the exterior geometry, it also explains how
the spectrum is filtered by the black hole's gravitational potential. These
are concrete, observable predictions.

At leading order, the radiation depends mainly on coarse features of the
geometry, such as mass, charge, and rotation. A complete outgoing quantum state
for every possible black-hole microstate lies beyond the calculation. Interior
partners remain in the semiclassical description, and so does the problem of a
unitary endpoint after the black hole disappears.

Hawking calculated the furnace. The transmitter remained unspecified.

### Page found the expected shape of purification

Don Page asked what happens in a finite quantum system whose total state is
pure but whose degrees of freedom are divided into a shrinking black hole and
growing radiation. If the total state is otherwise typical, the smaller part
is almost maximally entangled with the larger one.

Early in evaporation, the radiation is the smaller part, so its entropy rises.
Later, after the radiation becomes larger than the remaining black hole, its
entropy falls. The resulting rise and fall is the Page curve
(<https://arxiv.org/abs/gr-qc/9305007>).

This is a profound guide to unitary evaporation. It says that the final
radiation can be pure even while small portions of it look thermal.

Page's argument begins with a division into black-hole and radiation systems,
assumes global purity, and uses typical quantum states. Those ingredients
determine an entropy pattern while leaving the physical evaporation process and
the trajectory of a selected diary unspecified. A small diary could begin to
emerge early, around the Page time, or near the end while the overall entropy
follows a similar curve.

The Page curve constrains the global pattern of entanglement. Many routes for
individual pieces of information remain compatible with it.

### Hayden and Preskill supplied conditional recovery

Patrick Hayden and John Preskill made the diary experiment precise. They
considered an old black hole already highly entangled with its early radiation.
If the black hole rapidly scrambles an added diary and emits part of the
scrambled system, an observer holding the early radiation can recover the diary
after collecting only a little more radiation
(<https://arxiv.org/abs/0708.4025>).

This goes beyond an entropy curve. It is a recovery result. Once the black hole
acts like the assumed quantum encoder, information thrown into it can return
after roughly a scrambling delay.

The assumptions carry much of the physics. The black hole and radiation are
supplied as quantum subsystems. The dynamics are assumed to scramble in the
required way. The observer has the early radiation. The theorem then explains
what follows.

Hayden--Preskill tells a microscopic theory what kind of encoder would be
sufficient. Showing that a particular gravitational Hamiltonian realizes that
encoder is a separate task.

### Islands put the interior in the radiation's encoding

The island results are the central gravitational development in the modern
information problem. Their significance is greater than the phrase “gravity
produces a Page curve” suggests.

In controlled models, an evaporating black hole is coupled to a region where
the radiation can be collected. To calculate the radiation's fine-grained
entropy, gravity instructs us to consider more than the obvious radiation
region. After the Page time, the successful calculation includes an additional
region inside the black hole: an island.

The island does not become a new, independent piece of radiation. Instead, the
theory says that it is encoded in the radiation. In the language of holography,
the island lies in the radiation's entanglement wedge. Interior operations
therefore have counterparts that act on the radiation, within the controlled
family of semiclassical states.

This is a real information result. It establishes that the radiation contains
interior information in a reconstructible form. Penington's analysis also
derives a Hayden--Preskill-like criterion for information thrown into a black
hole after the Page time. Related work finds that infalling information leaves
the black hole's own reconstructible region after a scrambling interval
(<https://arxiv.org/abs/1905.08255>,
<https://arxiv.org/abs/1905.08762>).

There are qualifications. The reconstruction applies to a code subspace: a
controlled family of semiclassical states rather than every imaginable state
of quantum gravity. It may depend on knowledge of the initial state. A decoder
that exists mathematically need not be computationally practical.

Within these limits, the achievement is substantial. Islands show that interior
information is encoded in the radiation and can be reconstructed in principle.

Replica wormholes are part of how gravity derives the island entropy formula.
Entropy is often approached by calculating related quantities for several
copies, or replicas, of a system. In gravity, new spacetime geometries can
connect those copies. Around the Page time, these replica wormholes supply the
contribution that leads to the island formula and the falling side of the Page
curve
(<https://arxiv.org/abs/1911.12333>).

The two ideas play different roles. Replica wormholes help the gravitational
calculation find the island. Entanglement-wedge reconstruction explains what
the island means for information stored in the radiation.

A foundational question remains in the background. Connected replicas can make
the calculation resemble an average over many quantum theories. In some simple
gravitational models, that interpretation is exact. In a proposed single
microscopic theory, however, one must still explain how the wormhole calculation
coexists with ordinary quantum factorization. That foundational question is
separate from deriving the real-time emission process.

### Effective models connect dynamics to reconstruction

The island formula itself does not supply an emission-by-emission account of
how the encoding forms. Several related models do, and they reach further than
the first version of this reevaluation acknowledged.

Hong Liu and Shreya Vardhan developed an “operator gas” description in which
chaotic quantum evolution moves operators from the black hole into the
radiation. The same process produces Page behavior and Hayden--Preskill
information transfer. They proposed this dynamics as a microscopic counterpart
of islands (<https://arxiv.org/abs/2002.05734>).

Replica models also supply explicit recovery maps. Penington, Shenker, Stanford,
and Yang used the Petz map to show how interior operations can be reconstructed
from the radiation in a simple replica-wormhole model
(<https://arxiv.org/abs/1911.11977>). Other work uses an equilibrium
approximation to calculate finite-temperature radiation correlations and the
fidelity with which a diary can be recovered
(<https://arxiv.org/abs/2112.00020>).

There are fixed-Hamiltonian examples as well. An SYK system coupled to a bath of
Majorana chains undergoes a Page transition in its second Renyi entropy. A
control bit inserted into the SYK system becomes correlated with the bath after
the transition, which has the holographic interpretation that the bath's wedge
has acquired an island (<https://arxiv.org/abs/2003.13147>). More generally,
the equilibrium framework shows how replica-wormhole formulas can arise for an
equilibrating system with a fixed Hamiltonian, without an ensemble average
(<https://arxiv.org/abs/2008.01089>).

The most direct bridge is *The Holographic Map of an Evaporating Black Hole*.
Its microscopic model is a sequence of random unitaries, one for each
scrambling interval. The radiation is divided into successive emissions, and
the model includes energy conservation and thermal Hawking weights. From this
same construction, the authors derive the QES entropy formula and show that an
operation on a Hawking partner inside an island can be represented by an
operation on the radiation. They also analyze an infalling system
(<https://arxiv.org/abs/2301.08362>).

These are genuine dynamical bridges. They include random-unitary constructions
and fixed-Hamiltonian many-body systems. Large-N limits, disorder averages,
equilibrium approximations, supplied system-bath splits, or a holographic
interpretation still connect them to gravity. A top-down theory would have to
derive the radiation sector, its constrained observables, and its emission
coupling from fundamental gravitational variables. That is an important
frontier, but the original program asked a prior question: can Hawking-like
thermodynamics and unitary information return coexist in an ordinary quantum
process, and what ingredients make them coexist?

## What the original experiment established

The modern information problem is more advanced than the phrase “information
paradox” sometimes suggests. Semiclassical gravity explains the thermal
radiation. Typical-state reasoning explains the expected entropy pattern.
Hayden--Preskill gives conditions for diary recovery. Islands place interior
information in the radiation's encoding, and effective dynamical models show
how such an encoding can form.

The project began with a proposed non-gravitational evaporator. Its aim was to
make one quantum process heat as it shrank, emit increasingly energetic
quanta, preserve global purity, produce a Page-like entropy turnover, and
return a private input through the radiation. The device was meant as a
control experiment. If the package could exist without geometry, its internal
logic could not by itself be a distinctive effect of gravity.

Successive models separated the ingredients. A chosen density of states fixes
the temperature law. A shrinking state space creates the competition behind a
Page turnover. The emission coupling fixes the rate and decides which part of
the remaining system can enter the radiation. Mixing spreads private
information into the part sampled by that coupling. Unitarity preserves the
information in the complete state.

The unified sector-isometry construction places the thermodynamic and
information diagnostics in the same evolving state. Its hard emissions are
near thermal; the square-root mass law produces negative heat capacity and an
accelerating power window; the internal support shrinks; and the accumulated
radiation shows a Page-like turnover and early/late correlations. The model
supplies its sector count, equilibration, and emission isometry, so it is a
control model rather than a microscopic black hole. It nevertheless answers
the compatibility question it was built to ask.

The literature reaches the same conclusion with stronger dynamical machinery.
Random-unitary, operator-gas, equilibrium, and fixed-Hamiltonian models connect
state-dependent emission to reconstruction. Hawking-like coarse radiation and
unitary information return are therefore known to coexist at the model level.

## Why thermal appearance does not determine the information route

This program built several deliberately simple evaporation models to separate
conclusions that are often run together. They serve as controls for the
reasoning about an astrophysical black hole.

One model emits many thermal Hawking-partner pairs while remaining completely
blind to a spectator diary. It loses energy and produces the expected local
statistics without transmitting the private message.

Another model makes every individual radiation packet independent of the
diary. Even every pair of packets can be independent of it. Yet three packets
together recover the diary exactly because the information lives entirely in
their shared correlations.

Together they establish a limited but durable result:

> Thermal appearance, energy loss, and partner production do not determine how
> private information is routed.

Two processes can look the same to every coarse or local measurement while
differing completely in global recoverability. The controls therefore explain
why the microscopic record is needed. Selecting the record produced in nature
requires a real gravitational theory. Building more abstract emitters would
add little unless a new model tests a concrete physical claim.

The same lesson appeared in a named black-hole-inspired model. The strict
memory-burden prototype contains an entropy-sized family of assisted memory
states, yet its specified master-radiation vertex has only one bright source
direction. Within a sector of fixed total memory occupation, the private
pattern does not enter that radiation record. A large number of internal
states, a large number of active radiation sources, and rapid information
release are therefore three different properties, even in a model designed
around black-hole-like memory.

This conclusion belongs to the strict Hamiltonian and its declared radiation
mode. Additional exchange, rescattering, pair-annihilation, dressing, or
continuum radiation channels can change it. The value of the calculation is
that it identifies exactly which missing interaction would have to do the
information-routing work.

## A possible successor: Matrix theory

Matrix theory offers a very different description of a black hole. In the BFSS
model, the underlying quantum system is built from large matrices rather than
from fields living on a preexisting spacetime. A black zero-brane appears as a
hot bound clump. Evaporation can occur when one constituent, called a D0-brane,
escapes from the clump.

This supplies something resembling a microscopic emission event. Existing
work gives concrete Matrix-theory accounts of D0-brane escape, near-thermal
spectra, negative specific heat, and faster evaporation as the clump gets
smaller (<https://arxiv.org/abs/1603.03055>).

An effective 2024 construction goes further. It divides the system into a
black-hole part and a radiation part, assigns time-dependent weights to D0
emission, and obtains a Page curve ending in pure radiation
(<https://arxiv.org/abs/2407.13336>).

Together, these works provide a microscopic candidate for energy emission and
an effective account of purification. Their full state-dependent connection
remains open. The complete BFSS black-hole state and the action of the full
Hamiltonian on it are not known in the form required to derive the entire
evaporation history. The division into black hole and radiation, together with
the emission weights, does substantial work before the entropy is calculated.

The live BFSS question is therefore narrower than “does it evaporate?” or “does
it have a Page curve?” It is this:

> Starting with two distinguishable, gauge-invariant black-hole states, can
> the BFSS Hamiltonian be used to calculate the differences in the escaped
> D0-brane or radiation record over time?

BFSS is one candidate for a successor project connecting microscopic gravity
with information reconstruction. Entering it would require a new commitment to
Matrix-theory dynamics rather than another refinement of the present control
models.

## Two lessons for any quantum-gravity successor

Two other parts of the literature sharpen the requirements for any such
successor.

### What the gravitational return address reveals

A localized object cannot be described in complete isolation once
gravitational constraints are respected. Its physical description includes a
gravitational field extending outward. A distant observer can therefore learn
total energy, momentum, angular momentum, and other asymptotic charges.

One can think of this exterior field as a return address. If two diary states
have different energies, their gravitational fields must differ. But that does
not mean the field reveals the contents of the diary.

Perturbative gravitational-splitting results show that localized states can
share the same exterior data apart from their total Poincare charges. At this
order, gravity necessarily exposes charge information but not an arbitrary
private message stored among states with identical charges
(<https://arxiv.org/abs/1805.11095>,
<https://arxiv.org/abs/1903.06160>).

There is a serious competing view. Strong holography-of-information arguments
hold that the exact boundary observables of a gravitational theory contain all
the information on a complete spatial slice. If so, the fixed-charge privacy
seen perturbatively may fail in the full theory
(<https://arxiv.org/abs/2012.05770>).

A freely designed toy model cannot decide between these positions. Choosing
which exterior measurements exist would choose the answer in advance. The
question becomes physical only inside a gravitational theory whose observable
algebra is derived rather than selected for the experiment.

### A clock makes the question possible

Ordinary physics often speaks as though space and time were a fixed stage. In
gravity, the stage is dynamical. Saying that something happened “here” or “at
this time” requires a physical way to identify here and now.

A clock need not be a device with hands. It can be any physical process that
changes predictably enough for other quantities to be defined relative to it.
An observer, a boundary charge, a rolling field, or even an evaporating black
hole can play that role.

This relational construction also helps gravity acquire the mathematical
machinery needed to assign entropy to an observer's measurements. In technical
language, several such constructions turn a type-III field algebra into a
type-II gravitational algebra with a suitable trace
(<https://arxiv.org/abs/2112.12828>,
<https://arxiv.org/abs/2206.10780>). Recent work shows that out-of-equilibrium
black-hole dynamics can itself supply the physical clock
(<https://arxiv.org/abs/2406.02116>).

This connection concerns dynamics and observable structure. A theory of
information transfer requires the additional step of identifying which
radiation measurements distinguish two diary states and how to decode them.

## Where the original program ends

The original question was whether one coherent quantum process could look
Hawking-like thermodynamically while returning information unitarily. The
answer is yes. The project models establish the compatibility and separate the
roles of state count, shrinking capacity, emission coupling, mixing, and
unitarity. The literature supplies more developed realizations connecting
state-dependent dynamics to reconstruction.

The durable lesson is simple:

> A nearly thermal glow can be the visible surface of a unitary transmitter.
> The message resides in how the complete radiation record depends on the
> initial state, often through correlations invisible in individual quanta.

For an actual black hole, a fundamental theory must explain why the required
ingredients exist and why they take their particular form. It must account for
the area-sized state count and thermodynamics, identify the physical radiation
observables, derive the emission and mixing dynamics, preserve a consistent
unitary accounting, and explain the interior. Those are active problems in
quantum gravity.

They do not remain as unpaid steps in this control-model program. A BFSS
calculation, a nonperturbative resolution of gravitational factorization, or a
microscopic derivation of the interior would begin a new theory-specific
project.

Two observation-facing branches are parked deliberately. The program's
starvation and asymmetry diagnostics remain useful inside declared passive
model classes, while its no-go results rule out treating them as universal
microscopic certificates. The frozen-routing witness remains a separate
experimental control proposal. Neither branch changes the central conclusion.

The present program ends with a more useful result than the original proposed
boundary. Ordinary quantum mechanics supplies an architecture in which
Hawking-like thermodynamics and information return coexist. The comparison
identifies the ingredients that architecture requires and the claims that
coarse exterior data cannot establish. Quantum gravity must explain the actual
black hole that realizes the architecture.
