# Access Filtrations, Substrate Screening, and RG

Date: 2026-06-16

Purpose: record the connection between constrained access, renormalization-group coarse graining, and substrate independence. This is a conceptual bridge note, not a theorem stack, and should not be backported into the access-latency paper unless it produces a precise result.

## Core Distinction

The useful bridge to RG is not that every restricted channel is an RG flow. The useful bridge is the contrast:

```text
RG forgets at the effective level.
Constrained access hides at the effective level.
```

RG coarse graining makes microscopic distinctions unavailable to the long-distance effective description. In many constrained-access systems, especially unitary ones, the same effective loss can mask globally preserved information: the information is not erased, but hidden in a commutant, late record, high-depth observable, or dressed/nonlocal access channel.

This is where the analogy becomes physically useful. A black hole is thermodynamically coarse-grained, but unitarity says the information is hidden rather than destroyed. The information puzzle is precisely the place where effective forgetting and recoverable hiding are forced to look the same to the public exterior channel, while remaining different information-theoretically.

## Two Axes To Keep Separate

The note concerns two different objects.

### A. One Substrate, Growing Access

This is the existing latency/private-fate program:

```text
A_0 subset A_1 subset A_2 subset ...
```

Here `A_n` is the algebra available after more records, more time, larger fragments, deeper control, or stronger decoding resources. This is an access filtration, not automatically an RG flow. It need not have a semigroup law, a generator, fixed points, or relevant/irrelevant eigenvalues.

At each access scale:

- `Z(A_n)` is the public center: redundantly classical information.
- `A_n` contains the recorded block: information coupled to records, possibly nonredundant or hard to decode.
- `A_n'` contains the noiseless/private commutant: information invisible to passive records at that scale.

This axis asks:

```text
Given one substrate, what becomes public, recorded-but-deep, protected,
or recoverable as access grows?
```

### B. Many Substrates, Fixed Access

This is the substrate-screening/RG-like axis:

```text
different microscopic substrates -> same accessible channel
```

Here the access restriction is fixed, and the question is whether many microscopic substrates induce approximately the same accessible statistics, public algebra, or effective channel. This is the closer analogue of RG universality.

Two substrates are access-equivalent at access scale `n` if their accessible channels are close, for example

```text
||N_n^(1) - N_n^(2)||_diamond <= epsilon,
```

or if they generate approximately the same public center and accessible block structure.

This axis asks:

```text
Which substrate differences are visible to this channel,
and which are screened from it?
```

The axes interact, but they are not the same. The first is recovery under enlarged access; the second is universality under fixed restricted access.

## What the Literature Already Has

The RG/information connection is well developed. We should not claim that part as new.

Closest direct sources:

- Fowler and Heckman, "Misanthropic entropy and renormalization as a communication channel."
  - Treats RG flow as a noisy communication channel from UV configurations to IR degrees of freedom.
  - Asks how much UV information remains accessible in the IR after coarse graining.
  - Link: https://www.osti.gov/biblio/1980828

- Fowler, "Information Theoretic Interpretations of Renormalization Group Flow."
  - Dissertation version/formulation.
  - Explicitly treats UV variables as channel inputs, IR variables as outputs, and the RG transformation as the communication channel.
  - Link: https://cdr.lib.unc.edu/concern/dissertations/vh53x249b

Information-theoretic RG / information bottleneck:

- Koch-Janusz and Ringel, "Mutual information, neural networks and the renormalization group," Nature Physics 14, 578-582 (2018).
  - Introduces real-space mutual information as a way to learn relevant coarse variables.
  - Link: https://www.nature.com/articles/s41567-018-0081-4

- Lenggenhager, Gokmen, Ringel, Huber, and Koch-Janusz, "Optimal Renormalization Group Transformation from Information Theory," Phys. Rev. X 10, 011037 (2020).
  - Views RG as a compression scheme retaining relevant information.
  - Proves properties of optimal real-space mutual-information coarse graining.
  - Link: https://arxiv.org/abs/1809.09632

- Gordon, Banerjee, Koch-Janusz, and Ringel, "Relevance in the Renormalization Group and in Information Theory," Phys. Rev. Lett. 126, 240601 (2021).
  - Establishes an equivalence between field-theoretic RG relevance and information-bottleneck relevance for statistical field theories.
  - Link: https://arxiv.org/abs/2012.01447

- Kline and Palmer, "Gaussian Information Bottleneck and the Non-Perturbative Renormalization Group."
  - Maps information bottleneck and families of nondeterministic coarse-graining maps in a Gaussian setting.
  - Link: https://arxiv.org/abs/2107.13700

Information geometry / universality:

- Machta, Chachra, Transtrum, and Sethna, "Information loss under coarse graining: A geometric approach," Phys. Rev. E 98, 052112 (2018).
  - Uses Fisher-information geometry to show how most microscopic parameter directions become less distinguishable under RG flow, while relevant ones remain distinguishable.
  - This is the most concrete anchor for the substrate-screening side.
  - Link: https://sethna.lassp.cornell.edu/pubPDF/InfoGeomRG.pdf

Holographic/RG/QEC adjacency:

- Steinberg, Feld, and Jahn, "Holographic codes from hyperinvariant tensor networks," Nature Communications 14, 7314 (2023).
  - Relates holographic quantum error-correcting codes, complementary recovery, and critical RG flow of boundary states.
  - This is already on the hiding side of the forget/hide distinction: tensor-network and holographic RG use isometric encoding plus truncation/bond degrees, so the connection to complementary recovery is not accidental.
  - Link: https://www.nature.com/articles/s41467-023-42743-z

## Translation Table

This table mixes structural parallels and loose analogies. It should not be read as a dictionary of equivalences.

| RG language | Constrained-access language | Status |
| --- | --- | --- |
| Coarse graining | Restricted observation/control channel | Structural |
| Scale parameter | Access parameter: records, time, fragment size, decoder depth, bandwidth, control depth | Analogy unless a composition law is supplied |
| IR observables | Accessible record/observer algebra | Structural |
| Integrated-out modes | Degrees outside the allowed channel | Structural at the effective level |
| Irrelevant operators | Distinctions screened from the accessible channel | Analogy; mechanisms differ |
| Relevant operators | Distinctions preserved by the accessible channel | Analogy; mechanisms differ |
| Universality class | Access-equivalence class | Candidate structure on the substrate-screening axis |
| Fixed point | Stable effective public algebra/channel | Analogy unless a genuine access RG is built |
| RG compression | Substrate screening under restricted access | Structural as channel contraction; not necessarily RG |

## Substrate Screening as a Three-Part Decomposition

The strongest version of the substrate-screening idea should be built from known mechanisms rather than positing a new universality theorem immediately.

Public center:

- Quantum Darwinism and spectrum-broadcast/objectivity results explain how redundant public classical information becomes robust across many fragments.

Recorded-but-deep block:

- Information-geometric sloppiness and compression explain why many microscopic distinctions become hard to distinguish through a restricted effective channel.
- Machta-Sethna-style Fisher-information contraction is the clean anchor here.
- This is the substrate-screening shadow of the latency theorem: sloppy directions are substrate distinctions that require many records, large fragments, or deep access to resolve.

Noiseless/private commutant:

- The access algebra's commutant/noiseless subsystem captures information exactly invisible to passive records at a fixed access scale.
- This is not the same as RG irrelevance. It is algebraic protection under the chosen channel.
- The commutant is where the two axes coincide: substrate differences in the commutant are both access-equivalent under the fixed channel and protected from recovery until the access algebra changes.

The possible synthesis is:

> Restricted access decomposes substrate information into public invariants, sloppy/deep distinctions, and protected commutant information.

That synthesis is closer to a result-facing target than the slogan "access RG."

## Difference From Ordinary RG

Ordinary Wilsonian RG is usually scale-organized:

```text
short distance / high energy -> long distance / low energy
```

Constrained access is access-organized:

```text
full substrate -> allowed record/observer/control channel
```

Scale is one way of restricting access, but not the only one. Other access restrictions include:

- environmental monitoring,
- boundary access,
- observer horizon,
- measurement design,
- control depth,
- computational complexity,
- gauge/dressing constraints,
- available side information.

This matters because private information need not be high-energy or short-distance. It can be low-energy but inaccessible to the chosen channel, or nonlocal but visible through dressed access.

## Why This Matters

The RG analogy gives a disciplined way to talk about substrate independence only if the axes are kept separate:

- Access filtration: how hidden information becomes public, recorded, protected, or recoverable as access grows.
- Substrate screening: how different microscopic substrates become indistinguishable under fixed restricted access.

The conceptual payoff is the forget/hide distinction:

```text
effective forgetting:
    the restricted theory cannot distinguish the microscopic information

unitary hiding:
    the restricted theory cannot distinguish it, but a larger channel can recover it
```

Horizon physics sits at the sharpest point of this distinction. The exterior thermodynamic channel acts coarse-grained, but the unitary Page/Hayden-Preskill story requires recoverable hidden information. That is not ordinary RG forgetting.

## Possible Research Target

A more precise access-screening statement would look like:

> For a fixed restricted channel, microscopic substrate differences decompose into public invariants, sloppy/deep distinguishability directions, and exactly protected commutant directions. Enlarging access then moves information between these categories with de-protection and recovery rates.

This target would not replace RG. It would use RG/information geometry as one anchor, Quantum Darwinism as another, and the access-algebra commutant as the private-complement anchor.

## Cautions

Do not claim RG-as-channel is new.

Do not call an access filtration an RG flow unless a composition law, generator, and fixed-point/linearization structure have been supplied.

Do not claim all RG is quantum-channel RG. Classical statistical RG can be described by stochastic/coarse-graining channels, while quantum RG may involve CPTP maps, isometries plus truncations, tensor networks, or algebra embeddings depending on context.

Do not equate "irrelevant" with "private." In RG, irrelevant means screened by scale. In constrained access, private means screened by the allowed channel. These overlap only when access is scale-organized.

Do not assume substrate information is destroyed. In unitary settings it may remain globally present and only inaccessible to the effective observer/channel.

Keep this note adjacent to the latency paper. The latency result does not need RG vocabulary to be valid or interesting.
