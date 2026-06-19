# Wigner Friend, Horizons, and Constrained Access: Literature Pass

Date: 2026-06-15

Purpose: check whether the constrained-access / private-complement framing is already present in the Wigner-friend and horizon literature, and identify what should be treated as prior art before pushing the analogy further.

## Sources Checked

- Hausmann and Renner, "The firewall paradox is Wigner's friend paradox," arXiv:2504.03835.
- Walleghem, "Wigner's friend's black hole adventure," arXiv:2507.05369.
- Elouard et al., "Quantum erasing the memory of Wigner's friend," arXiv:2009.09905.
- Relano, "Decoherence framework for Wigner's friend experiments," arXiv:1908.09737.
- Witten, "Algebras, Regions, and Observers," arXiv:2303.02837.
- Lower-priority adjacent hits: Adlam, "What do black holes teach us about Wigner's Friend?"; recent circuit/Frauchiger-Renner followups.

Search used arXiv TeX sources where available rather than only PDFs.

## What Is Already in the Literature

The Wigner-friend / black-hole analogy is active prior art. The strongest direct source is Hausmann-Renner: they frame the firewall paradox as a Wigner-friend-style inconsistency caused by combining conclusions from observers who cannot operationally access a single common record. In their Hayden-Preskill-like protocol, the outside observer's reconstruction and the infalling observer's measurement are not jointly available to one physicist; treating them as a single global classical record recreates the no-cloning/monogamy tension.

Walleghem develops a similar direction by putting Wigner-friend operations and black-hole decoding into one protocol. The emphasis is again on paradox generation: sealed-lab unitarity, black-hole unitarity, reversals, and incompatible observer descriptions.

Elouard et al. are directly useful for the "moving cut" distinction. In the full-control context, Wigner can erase the friend's memory and restore interference. In a different context, some memory degrees remain outside Wigner's control and classical records persist. Their lesson is that the apparent contradiction depends on which degrees are in the accessible algebra.

Relano makes a related decoherence point: an external interference measurement can modify the memory records of internal observers. Stable classical claims require accounting for which records have actually become monitored by uncontrolled degrees of freedom.

Witten supplies the gravity-side algebraic language. In gravity, region algebras are not the clean primitive; the operational question is closer to which algebra is accessible to an observer or worldline. This supports access algebra as the correct language, though it is not by itself a finite-dimensional latency/recovery framework.

## The Opening That Seems Not Yet Occupied

The existing literature supports the analogy, but it does not appear to formulate the specific access-channel structure used in this project:

1. Public center: redundantly recoverable classical sector labels.
2. Recorded-but-deep block: degrees that couple to the record algebra but require large fragments, late records, decoding, or Page/Hayden-Preskill conditions.
3. Noiseless commutant: degrees in the commutant of the current record algebra, protected from passive records until the access algebra changes.

The useful distinction is not simply "black holes are Wigner's friend." That claim is already close to the literature. The sharper possible contribution is:

> Horizon and measurement-cut puzzles can be compared as constrained-access interfaces by decomposing the relevant record algebra into a public center, a recorded-but-deep block, and a noiseless commutant, then separating de-protection of the commutant from decodability of the deep block.

This also keeps two rate notions separate:

- De-protection rate: how quickly initially commutant degrees stop being in the commutant as the access algebra grows or changes.
- Decodability/recovery rate: once information is in the recorded block, how quickly a decoder can recover it from records.

The horizon case is special because the second rate is tied to Page/Hayden-Preskill recovery and the first rate is constrained by locality, scrambling, or dressed/nonlocal access. The ordinary Wigner-friend case is often an experimental-design question: Wigner changes the cut by choosing which laboratory degrees to control.

## Mapping to Our Current Framework

The cut theorem imports the no-broadcasting/decoherence lesson: exact redundant objectivity forces a commutative public algebra. This is not the new part; it is the entry ticket.

The commutant theorem gives a finite-dimensional version of the private complement: passive records cannot reveal operators in the commutant of the record algebra. This matches the quantum-eraser literature's distinction between memories inside and outside Wigner's control, but recasts it in algebraic channel terms.

The latency theorem is where the horizon interface separates from an ordinary adjustable cut. For a source-local finite-velocity bath, remote private information cannot become recoverable from emitted records before the routing time. A black-hole-like interface evades that conclusion only through fast internal routing/scrambling or nonlocal/dressed access.

The frozen-dynamics diagnostic is the clean test:

- If recovery dies when internal dynamics are frozen, the interface used routing/scrambling.
- If recovery survives, the record algebra was already nonlocal/dressed or side information already held the diary.

That diagnostic has no obvious analogue in the older Wigner-friend paradox literature, which usually treats control of the lab as a primitive rather than as a channel with a measurable locality profile.

## Cautions

Do not claim that the Wigner-friend / black-hole analogy is new. It is not.

Do not describe quantum erasure as Hayden-Preskill recovery. Quantum erasure changes the effective access algebra and may erase the friend's memory record; HP recovery extracts a diary from radiation records after sufficient mixing and emission.

Do not collapse the private complement into one thing. The useful structure has three compartments: public center, recorded-but-deep block, and noiseless commutant.

Do not treat observer relativity alone as the result. The result-facing content is the algebra/rate structure: what is public, what is recorded but hard/late, what is protected, and what operations move information between those categories.

## Immediate Research Use

1. Cite Hausmann-Renner and Walleghem when motivating the Wigner-friend / black-hole connection.
2. Cite Elouard and Relano for the memory-erasure / moving-cut distinction.
3. Cite Witten for observer-access algebras in gravity.
4. Push the next technical step through the commutant/rate language, not through another paradox protocol.
5. Treat the possible result as:

> A constrained-access interface has a canonical public/private decomposition; horizons and measurement cuts differ by the dynamics and physical cost of changing the access algebra.

