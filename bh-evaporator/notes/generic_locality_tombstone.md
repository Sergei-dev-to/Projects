# Tombstone: Generic Emergence of Locality (2026-07-03)

**Status: CLOSED as a research direction.** Explored in one session
(Carroll–Singh mad-dog Everettianism → emergence-of-locality thread).
Verdict: no theorem-shaped wedge; the tractable question is someone
else's open problem with a discouraging conjectured answer; the
attractive mechanisms are occupied. Kept here so the reasoning does not
have to be re-derived if the topic resurfaces.

## The question

Cotler–Penington–Ranard (1702.06142): exact k-locality of a Hamiltonian
in some tensor product structure is measure-zero over spectra
(exponentially many spectral parameters vs. polynomially many local
couplings); given existence, the local TPS is generically unique
(exceptions: free theories, dualities — CPR §4.2 prove conditional
finite/constant-dual genericity; restricted numerics support zero duals).
Question explored: what change of definition or theory structure could
make locality generic rather than fine-tuned?

## The four-family map (every escape route is one of these)

Any escape must change one of: the **measure**, the **target**, the
**ambient structure**, or add a **selection principle**.

1. **Measure (simplicity/compressibility prior).** Locality =
   describability; laws must be finite strings. FAILURE MODE: simplicity
   ≠ locality — mean-field/LMG/p-spin/permutation-invariant models are
   compressible and non-local. Needs the observer cut (family 4) to
   finish. The combined move is OCCUPIED: Markus Müller, "Law without
   law" (Quantum 4, 301 (2020), arXiv:1712.01826) — algorithmic prior +
   observer states.
2. **Target (weaker locality).** Sector/code-subspace locality
   (holography delivers it; the tuning moves into holography).
   Hydrodynamic/RG attractor: explains ROBUSTNESS within the local
   class (many-to-one screening of microscopic tuning), not emergence
   from outside it — generic H conserves only energy, and "densities"
   presuppose space. Variational TPS (minimize entanglement/operator
   growth over factorizations; Carroll–Singh mereology 2005.12938 did
   small-system numerics): the flat-measure version reduces to CPR's
   own open problem §4.1 — approximate locality conjectured still
   fine-tuned (exceptional sets heuristically have codimension
   exponential in system size, making ε-tubes negligibly small).
   Structured-ensemble version is rigged: choosing the ensemble is
   choosing the answer.
   Spectral-ensemble subtlety: spectrum-defined ensembles cannot
   distinguish H from its scrambled conjugate, so "locality generic in
   ensemble X" collapses back to distance-to-local-spectra-manifold.
3. **Structure (rigidity replaces measure).** Fine-tuning is an
   artifact of continuous parameter spaces; discrete/rigid choices
   (algebras, graphs, inclusions) admit uniqueness theorems instead.
   Instances, all crowded: Weinberg cluster-decomposition folk theorem
   + bootstrap (smuggles Lorentz — in tension with finite-dim
   programs); Hojman–Kuchař–Teitelboim hypersurface-deformation
   algebra ⇒ GR (1976); half-sided modular inclusions ⇒ translation
   group / local nets (Wiesbrock, Borchers, Longo industry); random
   tensor networks ⇒ RT geometry with high probability at large bond
   dimension
   (Hayden–Nezami–Qi–Thomas–Walter–Yang 1601.01694) — the one honest
   genericity theorem, via the two-level trick (discrete skeleton +
   generic tensors below it). "Why the skeleton" is the residual
   question and is at least discrete.
4. **Selection (observers/records).** Quantum Darwinism /
   predictability sieve: only quasi-local dynamics supports redundant
   records and self-modeling subsystems. Converges with family 1 on
   compressibility; that synthesis is Müller's.

## Corrections on record (from the review pass)

- CPR do NOT prove computational hardness of finding the local TPS
  (earlier session statements attributed hardness to them — wrong; CPR
  only make informal/practical complexity remarks in §7.6 and the final
  remarks).
- CPR §4.1 already poses the approximate-locality question and
  conjectures the discouraging answer; the "L(H) interpolation
  program" floated in-session is therefore half their open problem,
  half rigged, and was withdrawn.
- Free-theory (normal-modes) counterexample to TPS uniqueness: not
  verified against CPR's text this session; verify §4.2 before citing.

## Harvested (already done)

- Two edits to `paper_boundary_saturation/main.tex` (2026-07-03, user
  approved): temporal-certificate forcing argument (Discussion) and
  arrival-latency vs decoder-complexity two-exponent remark (Dynamical
  Counterpart). Recorded in `boundary_saturation_invariant.md` §5.10.
- Seam observation, PENDING a home: fast scramblers are k-local
  WITHOUT geometric locality — the delamination point of the locality
  tower (TPS → interaction graph → Lieb–Robinson cones → geometry),
  where LR-type statements retain content but have no low-dimensional
  geometry to be about. Horizons as probes of which layer of locality
  is fundamental. Belongs in the §5.7 taxonomy discussion when
  written; anchors already in refs.bib (Barbón–Magán, Bentsen–Gu–Lucas,
  Sekino–Susskind).

## Reopen conditions

Only plausible deliverable: a synthesis essay, "What would it take for
locality to be generic?" (taxonomy of locality notions + the
four-family map + the rigidity principle), Foundations-of-Physics
genre, adjacent to the planned Heisenberg-cut essay. Precursor reading
(also the scoop check): CPR §4 in full; Müller 2020; Carroll–Singh
2005.12938; HNQTWY 1601.01694; plus a 2023–26 sweep for recent
emergent-TPS work (not done this session). KILL CRITERION: if the
four-family punchline feels obvious after the CPR + Müller reads, drop
the essay.
