# BFSS Detachment Feasibility and Go/No-Go Dossier

Date: 2026-07-10

Status: primary-source and local-capability audit for Phase B of the
demarcation plan.

## Executive Verdict

```text
Full BFSS black-hole information-export calculation now:
  NO-GO as a local project.

Gauge-controlled small-N bosonic/BMN detachment pilot:
  CONDITIONAL GO, if it uses a genuine gauge-invariant separation projector,
  physical projected time evolution, truncation convergence, and direct
  process/decoupling diagnostics.

Another generic doorway, random-matrix, shell, or source-Gram proxy:
  NO-GO. The diagnostic calibration is already complete.
```

The pilot can decide whether the operator/algebra measurement pipeline works
in a matrix Hamiltonian. It cannot establish that a large-N BFSS black hole
exports information generically.

## 1. Demarcation Target

The question is no longer whether BFSS is chaotic or whether D0 emission has a
Hawking-like inclusive rate. It is:

```text
Does the physical, gauge-invariant D0-detachment process become sufficiently
diary-visible and isotropic that the accessible escaped-D0 record decouples a
diary reference from the daughter clump?
```

Let `P_E` project onto a clumped microcanonical shell and `Q_m` onto a separated
daughter-plus-radiation sector with accessible radiation label `m`. The primary
finite-time object is

```text
D_m(t) = Q_m exp(-i H t) P_E.                             (1.1)
```

With initial shell basis `|i>`, daughter basis `|f>`, and radiation labels
`|m>`, define

```text
A_(i->f,m)(t) = <f,m|D_m(t)|i>,                           (1.2)

K_ij^(mn)(t) = sum_f A_(i->f,m)(t) A*_(j->f,n)(t).       (1.3)
```

`K` is the radiation channel's invariant second-moment/Choi data once the
physical projectors and accessible algebra are fixed. It is the correct object
for the temporal-access/decoupling program.

The singular spectrum of a canonical transition matrix is a useful model
diagnostic, but it is not the theorem target. A smooth strength function or
high full-channel participation can coexist with a compressed accessible
radiation channel. Direct process moments and decoupling are load bearing.

## 2. Gauge-Invariant Algebra and Projectors

### Clumped versus separated sectors

A labeled matrix index is not a physical D0 label. The pilot should define
separation through gauge-invariant spectral data. A practical candidate is the
adjoint-covariant radial matrix

```text
R^2 = sum_I X_I X_I,                                     (2.1)
```

whose eigenvalues are gauge invariant as an unordered set. A separated sector
can be defined by one radial eigenvalue lying beyond a threshold with a stable
gap from the remaining clump. `P` and `Q` must be spectral projectors of a
gauge-invariant function of this data, not projectors onto a labeled matrix
row/column.

Target-space entanglement work supplies a more principled algebraic route:
gauge-invariant projectors define target-space regions and their observable
subalgebras. This supports the use of a separated-D0 exterior algebra, while
also showing that factorization requires explicit gauge/edge-sector choices:
[Das et al., arXiv:2011.13857](https://arxiv.org/abs/2011.13857) and
[Hampapura--Harper--Lawrence, arXiv:2012.15683](https://arxiv.org/abs/2012.15683).

### Accessible radiation labels

At minimum the exterior record should include:

```text
escaped radial-energy/momentum bin;
angular or matrix-direction labels that survive gauge reduction;
exact asymptotic charges;
emission time bin.
```

Daughter-clump state labels are traced in (1.3). Gauge, edge, or off-diagonal
string labels count as radiation only if the selected exterior algebra can
measure them. Otherwise they are hidden environment labels.

The BFSS S-matrix/soft-theorem literature supports asymptotic submatrix
excitations and their charges, but does not supply the thermal detachment
channel from a black-hole-like clump. See
[Miller et al., arXiv:2208.14547](https://arxiv.org/abs/2208.14547) and
[Tropper--Wang, arXiv:2303.14200](https://arxiv.org/abs/2303.14200).

## 3. Minimal Observable Stack

### Gate 0: sector and truncation validity

```text
Gauss-law violation below tolerance;
P and Q stable under cutoff and threshold variation;
clumped and separated states both represented below the truncation ceiling;
probability conservation and energy drift controlled.
```

Failure here ends the pilot.

### Gate 1: physical first moment

```text
Gamma_m(t) = (1/d_E) Tr[D_m(t)^dag D_m(t)].               (3.1)
```

This establishes that the selected projector/channel actually sees
detachment. It does not establish information export.

### Gate 2: operator spectral structure

Compute the return/strength data associated with `QHP` or `Q exp(-iHt)P`:

```text
C_detach(t), A_detach(omega), spreading width, scars/recurrences. (3.2)
```

This tests whether the physical doorway relaxes on a thermal/QNM scale. It is
necessary context, not sufficient export evidence.

### Gate 3: radiation-resolved process moments

Compute (1.3) within exact symmetry sectors and test:

```text
state-to-state variance smoothness in (E,omega);
radiation-label covariance;
connected fourth moments/crossing terms;
stability against changes of basis inside P and daughter sectors;
full-channel versus accessible-radiation coarse graining.                (3.3)
```

The sufficient comparison is the ETH/design condition in
`eth_decoupling_derivation.md`, not raw participation alone.

### Gate 4: direct diary decoupling

Embed a small code diary in `P_E`, apply the projected physical channel, and
compute

```text
Delta(t) = ||rho_(Q_ref,daughter)-rho_Q tensor rho_daughter||_1. (3.4)
```

This is the decisive pilot observable. A decrease relative to blind/aligned
controls verifies that the computed process moments have operational export
content.

## 4. What Existing Methods Actually Supply

### Classical and semiclassical real-time BFSS

Classical BFSS/matrix simulations support clump formation, flat-direction D0
escape, negative-specific-heat behavior, and chaos. They do not produce the
quantum transition amplitudes or connected fourth moments in (1.2)--(1.3):

- [Aoki--Hanada--Iizuka, arXiv:1503.05562](https://arxiv.org/abs/1503.05562)
  studies real-time formation in the classical limit.
- [Berkowitz--Hanada--Maltz, arXiv:1602.01473](https://arxiv.org/abs/1602.01473)
  develops the chaotic flat-direction evaporation mechanism.
- [Berenstein--Guan, arXiv:2105.04577](https://arxiv.org/abs/2105.04577)
  studies a simplified semiclassical `2x2` evaporation model.

Verdict: useful for defining separation events and timescales; insufficient for
the information-export gate.

### Gaussian real-time BFSS

[Buividovich--Hanada--Schäfer, arXiv:1810.03378](https://arxiv.org/abs/1810.03378)
uses general Gaussian density matrices to study Lyapunov growth, entanglement
saturation, and quasinormal decay. This supports the possible thermal timescale
tie, but a Gaussian variational state does not supply the full non-Gaussian
transition fourth moments required by the current sufficient theorem.

Verdict: adjacent evidence for Gate 2, not a Gate-3/4 calculation.

### Euclidean lattice and bootstrap methods

Thermal lattice BFSS/BMN calculations constrain equilibrium phases and
thermodynamics; for example
[Bergner et al., arXiv:2110.01312](https://arxiv.org/abs/2110.01312).
They do not directly provide real-time radiation-resolved amplitudes.

Verdict: useful for shell/state preparation and thermodynamic calibration;
analytic continuation is not presently a controlled route to the required
multi-time channel tensor.

### Hamiltonian truncation and quantum simulation

[Gharibyan et al., arXiv:2011.06573](https://arxiv.org/abs/2011.06573)
gives an explicit Fock cutoff, state-preparation, real-time simulation, and
measurement framework for BMN/string-theory matrix models.

More recently, [Hartnett--Liao--Rinaldi,
arXiv:2604.14094](https://arxiv.org/abs/2604.14094) reports a digital real-time
simulation of a bosonic `SU(2)` quartic matrix model, including Fock truncation,
Trotter and hardware-error analysis, and gauge-violation postselection. The
authors also find scaling to holographically interesting regimes remains
formidable.

Verdict: this is the most relevant technical route for a small-N pilot. It does
not make full BFSS locally tractable.

### Literature gap

This targeted primary-source audit found no calculation of the
radiation-resolved black-hole-clump detachment tensor (1.3), its connected
fourth moments, or direct diary decoupling in BFSS. This is an inference from a
targeted rather than exhaustive search and should be rechecked before
publication or outreach.

## 5. Local Repository Capability

Already implemented:

```text
detachment_operator_proxy.py:
  calibrates isotropic, aligned, scarred, and record-blocked transition
  diagnostics;

matrix_radial_detachment_diagnostics.py:
  computes a genuine QHP transition in a quantized two-real-matrix N=2
  oscillator, but is not BFSS and has no gauge-singlet/large-entropy clump;

classical_matrix_clump.py:
  tests stripped classical separation and settling, not quantum export;

natural_record_decoupling_test.py:
  validates direct decoupling for supplied record Kraus maps.
```

These have completed the diagnostic-calibration role. Extending their random
or stripped-matrix families would not answer the BFSS question.

Missing locally:

```text
a gauge-singlet SU(2) bosonic/BMN Hamiltonian basis;
stable clump/separation spectral projectors;
sector-resolved Q exp(-iHt) P amplitudes;
radiation/daughter label extraction;
cutoff extrapolation of second/fourth moments;
direct diary-reference evolution in that physical channel.
```

## 6. Smallest Faithful Pilot

### Model

```text
gauge group:       SU(2);
matrices:          2 or 3 bosonic adjoint matrices initially;
Hilbert regulator: oscillator/Fock cutoff;
gauge treatment:   exact singlet basis if practical, otherwise Gauss-projector
                   preparation plus quantified postselection;
IR regulator:      weak BMN/mass deformation for state preparation, followed
                   by a controlled reduction toward the flat-direction window;
evolution:         sparse exact/Krylov evolution locally;
records:           radial separation, energy/momentum, exact charges, time.
```

The raw Fock dimension scales approximately as

```text
cutoff^(3 * number_of_matrices)
```

before gauge reduction for `SU(2)`. Two matrices at cutoff five are modest;
three matrices already reach roughly two million raw states. Full BFSS has nine
bosonic matrices plus fermions and is not a local exact-diagonalization target.

### Regulator tension

A mass/BMN deformation stabilizes the spectrum and state preparation but lifts
the flat directions responsible for D0 escape. The pilot is meaningful only if
there is a cutoff- and mass-stable window containing both a metastable clump and
a distinguishable separated sector. If no such window appears, the pilot does
not model detachment and must stop.

### Minimal outputs

```text
1. cutoff/gauge/projector convergence table;
2. nonzero projected transition probability and energy-resolved strength;
3. K_ij^(mn) for a two-dimensional diary code and several radiation bins;
4. connected fourth-moment/ETH residuals where sample size permits;
5. direct Delta(t) decoupling curve;
6. blind/aligned control with the same first moment.
```

## 7. Go/No-Go Gates

### GO to implementation

Proceed with the small-N pilot only if a design pass can show:

```text
a gauge-invariant P/Q construction in the regulated Hilbert space;
raw or singlet-reduced dimension within local sparse-evolution resources;
a mass/cutoff window that supports both clump and separation;
accessible radiation bins distinct from daughter/hidden labels;
direct decoupling computable for at least a qubit diary;
truncation scans affordable at three or more cutoffs.
```

### NO-GO / collaboration gate

Stop local implementation if:

```text
P/Q is gauge-fixing dependent or labels a fictitious D0;
the regulator removes escape before convergence;
gauge leakage or cutoff drift is comparable to the process-moment signal;
only inclusive rates or classical trajectories are obtainable;
fourth moments/direct decoupling require the full BFSS Hilbert space;
the pilot cannot distinguish accessible radiation from hidden partner data.
```

At that point the correct next action is a collaboration/data proposal to a
matrix-quantum-simulation or BFSS group, not another proxy.

## 8. Final Phase-B Decision

```text
Decision: CONDITIONAL GO for a design-only small-N SU(2) bosonic/BMN pilot.

Authorization for heavy implementation: NOT YET.

Next required artifact:
  a compact pilot build specification that explicitly constructs the
  gauge-singlet basis/projector, estimates dimensions at candidate cutoffs,
  and demonstrates a viable clump/separation window before implementing
  process moments.
```

The full BFSS claim remains collaboration-scale. Publication of the current
demarcation theorem package does not depend on this pilot succeeding.
