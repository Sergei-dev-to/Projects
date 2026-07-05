# Horizon property separation program

Date: 2026-06-13

This note isolates the possible result behind the recent confusion:
Rindler/Unruh physics already gives many "gravity-like" horizon issues,
so the program should not sell thermality, complementarity, or anonymity
as black-hole-specific.  The candidate insight is a separation result.

Companion pass: `notes/rindler_btz_separation_pass.md` works the
recommended sequence Rindler -> BTZ -> flux compression and records the
current dictionary target.

Constraint/access pass: `notes/constrained_access_channel.md` collects
the access-algebra, Gauss-law, Quantum Darwinism, and Heisenberg-cut
language into one object.

Memory-burden pass: `notes/prototype_m0_m1_results.md` and
`notes/prototype_m3_discriminator_table.md` add a live witness system:
the Dvali memory-burden/N-portrait prototype is degeneracy-saturated
but source-rank-unsaturated, and its strict diary latency is blocked by
memory-sector conservation.

## One-sentence target

Thermality, finite horizon entropy, eventual unitary release,
source-rank boundary saturation, fast recovery latency, and gravitational
constraint/nonfactorization are logically distinct properties.  The
factorized black-hole target sits at their intersection; Rindler,
ordinary reservoirs, tape emitters, de Sitter, and BTZ separate the
axes.

The possible paper-grade result is not "horizons anonymize" or
"horizons are thermal."  Those are lore.  The result would be:

> Fast exterior recovery of arbitrary newly deposited information is
> the property that survives the separation tests.  Its model-side
> content is boundary saturation plus routing/mixing; its exterior
> certificate is latency, not instantaneous flux statistics.

## Axes

Use these as independent predicates, not as synonyms.

1. **Modular thermality (T).**  The restricted state is KMS/thermal for
   the observer's algebra.  Rindler already has this by
   Bisognano-Wichmann/Unruh.

2. **Finite information budget (F).**  The horizon sector has a finite
   entropy/state count, such as `S_BH` or `S_dS`.  Rindler does not
   have this without a regulator and an additional physical rule for
   the cutoff.

3. **Evaporating or exchanged record (R).**  There is an exterior record
   that can be collected over time and used for recovery.  Schwarzschild
   has an asymptotic radiation record; AdS/BTZ needs a bath or an
   equilibrium recovery protocol; Rindler has observer-relative
   thermality but no finite emitted record by itself.

4. **Source-side boundary/source-rank saturation (S).**  The
   participation number of the source coupling algebra scales like the
   entropy: `N_eff ~ S`.  Ordinary local reservoirs with surface
   contact have `N_eff <= S^{(d-1)/d}`.  This is separate from both the
   state count and the latency certificate.

5. **Routing/mixing (M).**  Newly deposited information reaches the
   source coupling algebra in logarithmic emitted-record latency.  This
   is the Hayden-Preskill/fast-scrambling ingredient in factorized
   language.

6. **Exterior compression (C).**  The outgoing record has far fewer
   instantaneous radiation modes than source cells.  Flat
   Schwarzschild, small AdS, and dS are serial/one-wavelength cases.
   Large AdS/planar/Rindler are more parallel, but still distinguish
   radiation-mode participation from source-side participation.

7. **Anonymity (A).**  The emitted record carries no resolvable source
   address beyond conserved/no-hair data.  This is close to old
   no-hair/stretched-horizon intuition; the theorem value is only in
   combining it with compression and latency.

8. **Gravitational constraint/nonfactorization (G).**  The exterior
   algebra may be nonlocal or constraint-dressed in the sense relevant
   to holography of information.  This is not part of the factorized
   model; it is one possible realization of the nonlocal-encoder branch.
   Related operator-algebra/edge-mode languages include gauge-theory
   edge modes, gravitational surface degrees of freedom, the split
   property, and crossed-product algebras.

## Witness systems

| System | T | F | R | S | M/latency | C/A | What it separates |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Rindler wedge QFT | yes | no finite budget | no finite collected record | only density/regulator form | no Page/HP problem by itself | parallel thermal cells; anonymous only coarse-grained | Thermality and inside/outside entanglement are cheap. |
| Ordinary local reservoir | yes, if thermal | yes | yes, through a surface | no: `S^{(d-1)/d}` | power-law lower bound by LR | can be compressed by apparatus but source access remains surface-limited | Finite entropy plus thermality does not imply horizon recovery. |
| Serial tape emitter | optional | yes | yes, unitary eventual release | can be arranged label-wise | slow for arbitrary new deposits | compressed, but normally non-anonymous via time/source address | Eventual purity does not imply HP latency. |
| Saturated but slow emitter | optional | yes | yes | yes | no, if no routing | may be anonymous | Boundary saturation alone does not imply fast recovery. |
| Memory-burden / N-portrait prototype | model-dependent thermal line | yes: `K ~ S` assisted memory modes | partial: master radiation record exists, memory diary record does not | no: `N_eff = 1` at the flux line | no: strict `N_m` conservation blocks fixed-sector diary exit; BH mapping gives post-burden power-law release | compressed collective master line; at most coarse energy/frequency tags | Degeneracy saturation does not imply source-rank saturation or HP latency. |
| Fast scrambler with small contact | optional | yes | yes | no | only surface fraction visible quickly | depends | Mixing alone does not imply full-entropy exterior recovery. |
| Horizon-class factorized model | yes by DOS/detailed balance | yes | yes | yes | logarithmic by decoupling + thermal tie | compressed/anonymous collective record | The operational package is `F+R+S+M`, not thermality alone. |
| BTZ / AdS3 black hole | yes | yes, Cardy | equilibrium unless bath-coupled | should be CFT operator-access statement | chaotic CFT expectation; model-dependent | less serial for large AdS, cleaner holographic dual | Tests whether the three inputs are natural in a real dual Hamiltonian. |
| Large AdS / black brane | yes | yes | equilibrium or bath-coupled | density version of saturation | butterfly/operator-growth controlled | parallel horizon, high bandwidth | Tests the serial-vs-parallel refinement; flux may regain partial diagnostic value. |
| Near-extremal / JT throat | yes | yes, with large `S0` plus active entropy | bath-coupled island setups common | ambiguous: all `S0` or only active `Delta S(T)`? | Schwarzian/SYK-like expectation | low-temperature throat | Dangerous case: may force "dynamically active entropy" rather than total entropy. |
| de Sitter static patch | yes | yes | equilibrium exchange, not asymptotic radiation | horizon-register assumption/open | conditional HP-like protocol | serial one-wavelength | State-count expansion can be ordinary while saturation/constraints carry the horizon content. |
| Causal diamond | yes in special conformal settings | finite only with gravity/cutoff | observer-patch record unclear | open | open | observer-horizon control | Tests whether the framework extends beyond event/cosmological horizons. |
| Analogue horizon | yes kinematically | no universal finite area budget | no BH Page record | no | no | possible | Negative control: thermality alone is not the information problem. |

The point of the table is not taxonomy for its own sake.  It provides
witnesses that the predicates are independent enough that any proposed
"horizon invariant" must specify which axis it means.

## Theorem candidates

### Theorem A: local reservoir latency bound

Status: drafted in `paper_boundary_saturation/main.tex`.

For a finite-range `d`-dimensional reservoir coupled to an arbitrary
adaptive exterior apparatus only through its contact surface, information
deposited at depth `L` remains decoupled from the exterior until a
Lieb-Robinson traversal time.  For deposits at radius scale, recovery
latency is at least `S^{1/d}` up to additive diary/contact/error logs.

This is the cleanest proved half of the separation: ordinary finite
systems can be thermal and entropic but still fail low-latency exterior
recovery.

### Theorem B: flux statistics do not certify source saturation

Status: conceptual result from the failed HBT route; needs formal
statement if used.

For collective emission into shared outgoing modes, instantaneous flux
moments measure the radiation coherence matrix, not the source Gram
kernel.  Thus HBT/flux statistics can report `O(1)` radiation-mode
participation even when the source-side participation is `N_eff ~ S`.

This is a real lesson: horizon structure is temporally visible through
records and recovery, not spectrally visible in an instantaneous source
count.

Formal version.  Let microscopic source operators `O_mu` feed `r`
resolvable outgoing radiation modes through collective jumps

```text
J_a = sum_mu C_{a mu} O_mu,        a = 1,...,r .
```

Let the source Gram kernel be

```text
W_{mu nu} = < O_mu^\dagger O_nu >_E
```

on the relevant microcanonical/thermal shell.  The one-emission
radiation coherence matrix is

```text
Gamma_{ab} = < J_a^\dagger J_b >
           = (C W C^\dagger)_{ab}.
```

Any instantaneous flux/HBT observable built only from the emitted modes
is a functional of `Gamma` and higher radiation-mode tensors.  At the
second-moment level its participation rank is bounded by `rank Gamma <=
r`, while the source participation

```text
N_eff(W) = (Tr W)^2 / Tr W^2
```

can be order `S` when `W` has `S` comparable eigenvalues.  Therefore no
instantaneous radiation-mode statistic can identify source saturation
when `r << N_eff(W)` without additional temporal records, probes, or
model assumptions.  In Schwarzschild-scale emission `r=O(1)` per
thermal time, so the obstruction is parametric.

The proof is almost linear algebra: `C W C^\dagger` is a compression of
`W` to the resolvable radiation-mode space.  Many source kernels with
different `N_eff(W)` have the same compressed `Gamma`.  Flux/HBT can
distinguish coherent/superradiant versus incoherent radiation-mode
structure inside the compressed image, but it cannot invert the
source-side participation count.

### Theorem C: anonymity alternatives

Status: promising, not proved.

Given compression, anonymity, and source-local emission access, fast
unitary release of arbitrary newly deposited microscopic information
requires either:

1. internal routing/mixing that brings the deposit into the coupling
   algebra within the latency window, or
2. an emission map whose action is already nonlocal on the source
   algebra.

The value is not "horizons anonymize."  The value is the no-free-lunch
fork.  An anonymous compressed channel can serialize information
eventually; fast HP-style release forces the routing burden somewhere.

### Theorem C': memory-burden as a frozen-routing countermodel

Status: note-level verified for the strict prototype.  A
visible-algebra obstruction lemma is drafted in
`operator_overlap_latency_lemma.md`; the broader theorem generalization
is still open.

The Dvali memory-burden prototype realizes the slow/frozen-routing horn
of Theorem C as a physical model class rather than as a circuit control.
Its flux line is fed by a single collectively enhanced master mode, so
the source Gram kernel has `N_eff = 1` even though the assisted memory
sector has `K ~ S` degeneracy.  Separately, total memory occupation
`N_m` is conserved in the strict Hamiltonian, and no term routes memory
ladder operators into the master radiation ladder.  Diaries encoded
inside a fixed diagonal burden sector therefore do not become quantum
recoverable from the emitted master record at any time.  Generic loads
may leak coarse energy/frequency tags, but that is not HP recovery of an
arbitrary new diary.

This countermodel supplies the proved negative arm:

```text
degeneracy saturation + flux != source-rank saturation,
source-rank saturation != HP latency,
and burden-class frozen routing fails HP latency for an independent
mechanistic reason.
```

The remaining theorem target is the bridge under explicit model
assumptions: in a compressed anonymous factorized channel, fast
new-deposit recovery requires either order-one overlap with the full
visible algebra generated by the coupled source algebra, or a
nonlocal/constraint-dressed emission map.  The risky step is reducing
that visible-algebra condition to a simple instantaneous routing profile
such as `G_D(t)`; multi-time products are the likely counterexample
route if the simple bridge fails.  The natural first theorem class is a
fresh-ancilla or weak-collision record model with bounded per-collision
strength and bounded total record budget.  The strict memory-burden
prototype itself is not in that bridge class, because the `b0` record
mode is persistent; it satisfies the visible-algebra lemma by exact
sector structure instead.

### Theorem D: Rindler null case

Status: literature theorem plus interpretation; likely cheap but useful.

The Rindler wedge has exact modular thermality, but without a regulator
and an added finite horizon-register rule it has no finite entropy
budget, no shrinking Hilbert-space bookkeeping, and no finite Page/HP
recovery problem.

This theorem is mostly defensive, but it matters.  It prevents the
program from confusing Unruh thermality with black-hole information
recovery.

### Theorem E: BTZ/holographic dictionary test

Status: research direction.

In BTZ/AdS3, the state-count input is Cardy density and the source
algebra should translate into CFT operator access/growth.  The question
is whether boundary saturation and latency become natural CFT
statements rather than externally imposed Hamiltonian assumptions.

If yes, this is the best answer to "where is the dual Hamiltonian
hiding?"  It is hiding in the theory where state count, access, and
mixing are internal properties of the same boundary Hamiltonian.

### Theorem F: active mining changes the channel

Status: scoping item.

The saturation and compression claims refer to the natural Hawking/
Gibbons-Hawking channel, or to a specified bath coupling.  Active
near-horizon mining can alter the effective exterior access by inserting
apparatus close to the horizon and coupling to modes that the natural
asymptotic channel treats as inaccessible or greybody-suppressed.  This
does not refute the latency criterion, but it changes the protocol.

The paper therefore needs a scope sentence: distinguish passive
radiation recovery from active mining protocols.  Mining belongs to
the "which exterior algebra is coupled?" question, not to the
state-count or thermality layer.

## What is already lore

Do not claim novelty for these:

- Rindler/Unruh thermality.
- No-hair/anonymity as intuition.
- Stretched-horizon absorption and reradiation.
- Hayden-Preskill recovery assuming scrambling.
- Sekino-Susskind fast scrambling.
- Holographic entropy bounds.
- Raju-style challenges to factorization from gravitational constraints.
- Gauge-theory/gravity edge modes and crossed-product attempts to make
  subregion entropy finite.
- Black-hole mining as active modification of the exterior channel.

## What may be new

The candidate original content is narrower:

1. **The separation itself.**  The usual words "horizon," "thermal,"
   "black-hole information," "scrambling," and "holography" mix axes
   that the witness systems separate.  The memory-burden prototype now
   gives a live state-count-saturated but source-rank/latency-poor
   witness from the black-hole model literature itself.

2. **Latency as the exterior certificate.**  Source-side saturation is
   not seen in instantaneous radiation-mode counts.  It becomes visible
   through recovery latency once routing/mixing is included.

3. **The two-horizon contrast.**  Schwarzschild makes the state count
   exotic; de Sitter makes the state-count expansion ordinary through
   second order.  Boundary saturation is the input that survives both.

4. **The routing-vs-encoder fork.**  Under compressed anonymous emission,
   fast recovery demands either internal routing or nonlocal emission
   access.  This connects the factorized HP picture and the
   Gauss-law/HoI picture without making either one the default.

5. **Passive-vs-active access as a clean axis.**  Natural Hawking
   radiation, specified bath coupling, and active mining are different
   exterior algebras.  The same finite horizon can have different
   recovery certificates depending on which algebra the observer is
   allowed to couple.

## Immediate next work

1. Turn Theorem B into a precise two-line lemma about collective
   source-to-radiation maps: radiation coherence rank is bounded by
   outgoing mode rank, while source Gram participation can scale as
   `S`.

2. Formalize Theorem C in terms of an operator-growth overlap:
   `G_B(t) = || P_E U(t) O_B U(t)^\dagger ||` against the coupling
   algebra.  Fast recovery implies `G_B(t)` becomes order one by the
   recovery time unless the emission map is nonlocal on `O_B`.  Use
   the memory-burden prototype as the strict zero-overlap countermodel.

3. Write the Rindler null lemma as a short appendix-level note:
   modular thermality yes; finite recoverable register no.  This should
   be a control, not a new paper.

4. For BTZ, identify the CFT image of `N_eff`: likely an operator
   participation or OPE-channel participation measure in a thermal
   band, not a bulk source-cell count.

5. Add a passive/active channel scope note to the saturation paper:
   natural radiation and specified bath protocols are the target;
   mining is a different exterior coupling.

6. Add references/positioning for edge modes and crossed products on
   the `G` axis: Donnelly-Freidel local subsystems, Donnelly edge-state
   entropy, and Witten crossed product.

Update after the Rindler/BTZ pass: in BTZ, boundary saturation is not
simply automatic because the theory is holographic.  The sharper CFT
statement is that the exterior bath must couple to a
thermal-band/code-subspace CFT operator algebra whose participation is
of order the Cardy entropy, and chaotic operator growth must bring
arbitrary perturbations into that coupled algebra at HP latency.  State
count is natural by Cardy in the holographic CFT; access and routing
remain operational questions.

## Provisional conclusion

The road seems to lead to a classification theorem, not a unique model
of quantum gravity.  Gravity is one realization of the combined spec:
finite horizon budget, saturated source access, fast routing or
constraint-dressed nonlocal access, and a recoverable exterior record.
Rindler supplies thermal kinematics; ordinary reservoirs supply finite
entropy without saturation; tape emitters supply unitary eventual
release without latency; BTZ may supply the clean dual Hamiltonian
realization.

That is an insightful result if made precise: the black-hole
information problem is not thermality, not anonymity, and not unitarity
alone.  It is the conjunction of finite budget and low-latency exterior
recoverability.
