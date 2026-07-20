# DSSYK intrinsic bandwidth and the operational-cutoff gate

Date: 2026-07-19

Status: the native-Hamiltonian gate and the generic detector-action bound are
complete. Together they give a useful negative answer to the literal
cosmological-cutoff reading. A DSSYK-specific detector calculation is
conditional on new physical input; no unrestricted DSSYK dynamics project is
authorized by this note.

## 1. Question and relation to the completed access result

The original motivating question was whether the cosmological constant can be
understood as a UV cutoff in a dual theory, and whether doubled DSSYK gives
that idea operational content. There are two logically different routes:

1. **Constraint-induced access:** does the doubled equal-energy constraint or
   its relational representation create access to a diary that was absent in
   one copy?
2. **Intrinsic dynamical resolution:** does the native DSSYK Hamiltonian impose
   a shortest discrimination or record-formation time whose de Sitter image is
   controlled by the cosmological constant?

The standalone observer-access result closes the first route at the
kinematical level. Exact isometric transport preserves the complete observer
process, and therefore preserves its distinguishability and recovery
capacities. Any difference requires an additional, independently derived
resource restriction.

This note tests the second route directly. It is separate from parked WP2: it
asks first what follows from the already known DSSYK spectrum, before choosing
an operator family or complexity measure.

## 2. Bounded primary-source pass

The narrow pass checked the doubled de Sitter construction, the DSSYK/de
Sitter scale dictionary, bounded-spectrum quantum speed limits, and recent
finite-cutoff DSSYK work.

- Narovlansky and Verlinde define the doubled equal-energy model and identify
  SYK time with the proper-time separation of dressed bulk-field operators.
  Their native chord spectrum is bounded.
- Susskind develops the distinct microscopic and cosmic DSSYK scalings. This
  is important context: a microscopic time scale need not be the de Sitter
  radius.
- Standard quantum-speed-limit work gives a state-independent
  orthogonalization bound from the occupied spectral bandwidth.
- Recent finite-cutoff DSSYK work studies Hamiltonian deformations,
  thermodynamics, correlators, Krylov complexity, entanglement, and the
  stretched-horizon interpretation. It does not, in the quantities advertised
  in the paper, supply a diary-to-record channel or a recovery-grade temporal
  resolution.

Targeted searches for DSSYK together with *quantum speed limit*,
*orthogonalization time*, and *temporal resolution* found no direct treatment
as of the date above. This is a bounded overlap verdict, not a claim that no
related argument exists anywhere. The open niche is specifically the passage
from native DSSYK bandwidth to a controlled observer-record process.

## 3. Exact native-bandwidth check

In the Narovlansky--Verlinde normalization, the continuum one-copy chord
spectrum whose equal-energy label parametrizes the physical doubled states is

$$
E(\theta)=-\frac{2\mathcal J}{\lambda}\cos\theta,
\qquad 0\leq\theta\leq\pi.
$$

Its full spectral width is therefore

$$
B_{\rm DSSYK}=E_{\max}-E_{\min}
=\frac{4\mathcal J}{\lambda}.
$$

For time-independent evolution whose occupied energies lie in this band, the
state-independent bounded-spectrum speed limit gives, in units $\hbar=1$,

$$
t_\perp\geq \frac{\pi}{B_{\rm DSSYK}}
=\frac{\pi\lambda}{4\mathcal J}.
$$

This is a genuine cutoff on how fast native unitary evolution can take a state
to an orthogonal state. It is not yet a bound on measurement resolution,
record formation, channel capacity, or recovery.

Narovlansky and Verlinde use

$$
\mathcal J=\frac{1}{R_{\rm dS}},
\qquad
\frac{R_{\rm dS}}{G_N}=\frac{8\pi}{\lambda}.
$$

Substitution gives

$$
B_{\rm DSSYK}=\frac{1}{2\pi G_N},
\qquad
t_\perp\geq 2\pi^2G_N.
$$

The numerical factors are convention-dependent, but the conclusion within
this dictionary is not: $R_{\rm dS}$, and hence the explicit cosmological-
constant scale, cancels. The full native bandwidth supplies a microscopic,
Planck-scale lower time rather than a de Sitter-radius time. Thus the simplest
claim

> the cosmological constant is the DSSYK UV cutoff because the DSSYK spectrum
> is bounded

does not survive this check. The bounded spectrum is real; its literal
identification with a $\Lambda$-controlled operational cutoff is not.

For a diary restricted to a narrower microcanonical shell, the corresponding
statement is only

$$
t_\perp\geq \frac{\pi}{B_{\rm shell}},
\qquad
B_{\rm shell}=E_{\max}^{\rm shell}-E_{\min}^{\rm shell}.
$$

Any $\Lambda$ dependence then comes from how the physical shell is selected,
not from the equal-energy constraint by itself.

## 4. What the speed limit does not establish

Three distinctions prevent the bandwidth calculation from being promoted to
an observer-access theorem.

1. **Pre-existing distinguishability.** If the allowed observer algebra can
   directly measure orthogonal diary states, their distinguishability is
   nonzero at $t=0$. A speed limit on state evolution is irrelevant.
2. **Unbounded controls.** An observer interaction or control Hamiltonian with
   unconstrained spectral width can evade a bound derived from the native
   DSSYK Hamiltonian alone.
3. **Record versus state motion.** Orthogonalization of a global state does not
   imply that an initially diary-blind observer record has become
   diary-sensitive, much less that the diary is recoverable from that record.

Accordingly, the native result is a kinematical calibration, not the desired
operational cutoff.

## 5. Generic detector-action bound

A continuation must define an observer process before computing a DSSYK
correlator. Let $D$ be the diary, $O$ an initially diary-blind detector with a
clock and time-binned record, and $\mathfrak P(B,G_D)$ a protocol class with
two declared resources:

$$
\operatorname{bw}(H_{\rm native})\leq B,
\qquad
G_D(T)=\sum_j\int_{I_j}\!dt\,
\lVert H_j(t)-H_j^{(0)}(t)\rVert.
$$

Here $H_j^{(0)}$ generates a diary-blind comparison step with the same
interfaces, clock, initial detector, and resource budgets. Thus the first
resource is native bandwidth and the second is specifically the integrated
diary-sensitive generator defect, not the norm of background detector
dynamics.

This generic extension does not require a new theorem. Time-ordered Duhamel
evolution on each common reachable sector gives

$$
\lVert U_j-U_j^{(0)}\rVert
\leq\int_{I_j}\!dt\,
\lVert H_j(t)-H_j^{(0)}(t)\rVert.
$$

Comb telescoping and the channel/isometry norm bound from Result B then give

$$
\lVert\mathcal N_T-\mathcal C_T\rVert_{\diamond,D}
\leq 2G_D(T),
$$

where $\mathcal C_T$ is diary blind on the code. Consequently the normalized
record distinguishability of any two diary inputs obeys

$$
\delta_{\rm rec}(T)
=\frac12\lVert\mathcal N_T(\rho)-\mathcal N_T(\sigma)\rVert_1
\leq 2G_D(T).
$$

If a record decoder recovers two orthogonal diary states with trace-norm error
at most $\alpha$ for each state, the recovery converse implies

$$
G_D(T)\geq\frac{1-\alpha}{2}.
$$

The factors use the program's full trace- and diamond-norm convention. The
scientific point is invariant: accurate recovery requires order-one integrated
diary-sensitive detector action. Arbitrarily large diary-blind native DSSYK
evolution is free in this bound.

A suitable target is then a latency functional such as

$$
\tau_{\delta_*}(B,G_D)
=\inf\left\{T:
\sup_{\mathcal P\in\mathfrak P(B,G_D)}
\delta_{\rm rec}^{\mathcal P}(T)\geq\delta_*
\right\},
$$

where $\delta_{\rm rec}$ is a declared record-process distance from the
diary-blind comb. Recovery fidelity or observer capacity can replace the
distance, but the protocol class may not be changed after seeing the DSSYK
answer.

The generic bound is therefore finished. The only remaining question is
whether DSSYK or its bulk dictionary fixes $G_D(T)$---or relates it to $B$---in
a way that is physically mandatory and transports consistently to the
isospectral one-copy control. Without such a relation, the proposed latency is
an assumed detector budget rather than a prediction of the duality.

## 6. Pre-registered decision rule

The detector extension may proceed only in this order:

1. derive the diary-blind comb and the detector resource budget independently
   of the desired answer;
2. prove the generic record-distance or recovery bound for that class;
3. map every budget through the de Sitter dictionary before numerical work;
4. transport the identical class to the paired one-copy control;
5. compute a DSSYK-specific remainder only if steps 1--4 leave one.

Step 2 is complete generically, and the native-bandwidth part of step 3 is
complete. Step 1 remains open at the physical level because no derived de
Sitter detector budget has been identified. The sequence therefore stops
before steps 4--5 rather than filling that gap with a chosen operator family.

Stop if any of the following occurs:

- the de Sitter radius cancels from all physically fixed budgets, as it does
  in the full native-bandwidth check;
- the result is only the generic bounded-spectrum speed limit;
- allowed controls bypass the proposed cutoff because the detector budget was
  not physically fixed;
- the observable reduces to a correlator, entropy, or complexity of a chosen
  operator family without a record or recovery interpretation;
- the one-copy and doubled implementations differ only because nontransported
  resource classes were assigned to them;
- no independent bulk argument selects the detector interaction budget.

## 7. Verdict and next action

The cheap part was worthwhile and is complete. It sharpens the answer to the
original question:

- DSSYK has a native bounded spectrum and therefore a native dynamical speed
  limit.
- In the explicit Narovlansky--Verlinde de Sitter dictionary, its full-band
  time scale is microscopic, with the de Sitter radius canceling.
- The equal-energy constraint does not turn that scale into observer access.
- A cosmological operational cutoff could still arise from a physically
  derived shell or detector-resource restriction, but that is new input, not
  a consequence already contained in the doubled representation.

The program should therefore not launch unrestricted WP2. The generic
detector-action continuity bound is already supplied in section 5. Unless it
can be paired with an independently derived de Sitter detector budget, the
branch closes without DSSYK numerics.

## Primary sources

- Vladimir Narovlansky and Herman Verlinde, [*Double-scaled SYK and de Sitter
  Holography*](https://arxiv.org/abs/2310.16994), arXiv:2310.16994.
- Leonard Susskind, [*De Sitter Space, Double-Scaled SYK, and the Separation
  of Scales in the Semiclassical Limit*](https://arxiv.org/abs/2209.09999),
  arXiv:2209.09999.
- Gal Ness, Andrea Alberti, and Yoav Sagi, [*Quantum Speed Limit for States
  with a Bounded Energy Spectrum*](https://arxiv.org/abs/2206.14803), Phys.
  Rev. Lett. 129, 140403 (2022).
- Konstantin Herb and Christian L. Degen, [*Quantum speed limit in quantum
  sensing*](https://arxiv.org/abs/2406.18348), Phys. Rev. Lett. 133, 210802
  (2024).
- Sergio E. Aguilar-Gutierrez, [*Deforming the Double-Scaled SYK & Reaching
  the Stretched Horizon From Finite Cutoff
  Holography*](https://arxiv.org/abs/2602.06113), arXiv:2602.06113.
