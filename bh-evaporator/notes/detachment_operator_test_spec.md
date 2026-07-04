# Detachment Operator Test Spec

## Purpose

This is the execution target for the Matrix/black-hole demarcation program.
The broad demarcation work has reduced to one question:

```text
Does the microscopic Matrix detachment transition behave like a generic
information-export channel, or only like a thermal first-moment emitter?
```

The object to test is the transition operator

```text
O_detach:
  H_clump(N,E)
    -> H_daughter(N-q,E-omega) tensor H_escape(q,omega,p).
```

Equivalently, define transition amplitudes

```text
D_{c alpha} = <c|O_detach|alpha>,
```

where

```text
alpha:
  an initial clumped Matrix black-hole microstate;

c = (m,beta,r):
  full exit channel = emitted record m, daughter state beta, unresolved
  escape labels r.
```

The export question always requires an accessible radiation subsystem. In the
notation above, `beta` belongs to the remaining daughter black hole. The labels
`m` and any physically recoverable escape labels are radiation labels. A label
`r` counts as exported information only if it is included in the recovery
system; if it is traced or permanently inaccessible, it must be treated as an
environmental loss label rather than as part of the exported record.

## Gate 1: Spreading / Transition-Operator ETH

Question:

```text
Does O_detach behave like an ETH transition operator between the clumped shell
and the daughter-plus-escape shell?
```

Observable:

```text
C(t) = < O_detach^\dagger(t) O_detach(0) >_E
```

or spectral function

```text
A_detach(omega)
  = sum_{alpha,c} |D_{c alpha}|^2
    delta(E_c - E_alpha - omega).
```

Pass:

```text
A_detach has a smooth thermal/QNM-scale envelope;
C(t) decays on a thermal, QNM, or scrambling timescale;
matrix elements show ETH-like variance inside exact symmetry sectors.
```

Fail:

```text
A_detach is dominated by a few sharp peaks;
C(t) has persistent doorway oscillations or scars;
matrix elements remain tied to protected nonconserved labels.
```

## Gate 2: Channel-Doorway Participation

Question:

```text
Do the physical exit channels span many independent doorway directions?
```

Observable:

```text
G_{c c'} = sum_alpha D_{c alpha} overline{D_{c' alpha}}.
```

This is singular-value participation of the transition matrix `D`: the
nonzero spectra of `D D^\dagger` and `D^\dagger D` agree. The harness computes
both the channel Gram participation and the initial Gram participation for
this reason. Gate 2 measures whether the full transition has many independent
singular directions. It does not by itself say that the accessible radiation
record carries those directions.

Pass:

```text
G has high participation across full physical exit labels c=(m,beta,r);
no small set of collective doorway vectors dominates the total width.
```

Fail:

```text
G has one or a few large eigenvalues;
many exit channels share the same effective doorway vector;
the process is superradiant/common-doorway dominated.
```

## Working Export Conjecture

If:

```text
1. Gate 1 passes;
2. Gate 2 passes for the full transition;
3. the accessible-record version of Test 4 passes for the radiation system
   allowed in the recovery problem;
4. exact charge/gauge sectors are separated before testing;
5. internal re-scrambling occurs between emissions;
```

then the emitted records are expected to form a generic weak export channel on
the microcanonical shell. Standard decoupling should then give
Page/Hayden-Preskill recovery after the accessible emitted-record entropy
exceeds the diary size plus the usual decoupling budget.

This is a working conjecture, not yet a theorem. Gate 2 supplies the
singular-value participation of the transition. Test 4 checks whether that
participation survives in the accessible radiation record rather than being
stored in the daughter black hole or in unresolved labels. Test 5 is the direct
decoupling validation of the conjecture.

## Minimum Useful Numerical Proxy

A proxy is useful only if it has:

```text
matrix degrees of freedom;
clumped and block-separated sectors;
a transition operator between those sectors;
quantum eigenstates or Krylov dynamics;
daughter-state-resolved exit labels;
enough Hilbert-space dimension to measure G participation.
```

Classical eigenvalue-escape scripts are insufficient for this test. They can
motivate block separation, but they do not produce `D_{c alpha}`.

## Next Action

Build the smallest quantum matrix proxy that can produce `D_{c alpha}` and
measure `A_detach(omega)` and `G_{c c'}`.

The first implementation does not need to be BFSS. It must preserve the
operator structure above.

## Decision Protocol For The Matrix Calculation

The calculation should be built around the actual sector coupling, not around
an invented radiation channel. Define projectors

```text
P:
  clumped Matrix black-hole sector in a fixed energy, D0-number, momentum,
  and gauge-invariant charge window;

Q_m:
  block-separated sector with emitted record bin m, consisting of a daughter
  clump plus an escaped D0/short-string cluster.
```

The primary detachment amplitude is the Feshbach coupling

```text
D_{c alpha} = <c| Q_m H P |alpha>,
```

where `|alpha>` is an eigenstate or microcanonical vector in `P`, and
`c=(m,beta,r)` labels the full exit channel: emitted record, daughter state,
and unresolved escape labels. If the direct matrix element `Q_m H P` is
technically inaccessible, use the projected short-time transition amplitude

```text
D_{c alpha}(t) = <c| Q_m exp(-i H t) P |alpha>
```

and extract the same first- and second-moment diagnostics in the weak-transfer
regime.

The tests are:

```text
0. First moment:
   Gamma_m = (1/d_P) Tr_P P H Q_m H P
   or sum_{alpha,c in m} |D_{c alpha}|^2 / d_P.

   This checks whether the chosen sector coupling is the thermodynamic
   evaporation operator. Passing this test only establishes inclusive
   Hawking/Matrix rate behavior. In a toy proxy this test is only a
   normalization check unless an external BFK/Hawking target rate is supplied.

1. Spreading gate:
   Measure the strength function A_detach(omega) or the return correlator
   C(t)=<O_detach^\dagger(t) O_detach(0)>_E. Extract Gamma_spread and compare
   with the per-source escape width Gamma_escape,one ~ 1/(S beta).

   Passing requires Gamma_spread > Gamma_escape,one, preferably
   parametrically. This means the detachment doorway compounds through the
   chaotic Matrix sector before individual escape. Failing means the channel
   sees doorway structure before chaotic spreading.

2. Gram participation gate:
   Compute G_{c c'} = sum_alpha D_{c alpha} overline{D_{c' alpha}},
   N_eff(G) = (Tr G)^2 / Tr G^2, and the largest-width fraction
   lambda_max(G)/Tr G.

   Passing means the physical exit channels span many independent doorway
   directions. Failing means the rate can be thermal while the channel remains
   common-doorway, superradiant, or low-rank.

3. Symmetry-resolved repeat:
   Repeat the spreading and Gram tests inside exact charge, gauge, momentum,
   angular-momentum, and energy windows. A low-rank result is meaningful only
   after exact conserved-sector fragmentation is separated.

4. Full-channel versus radiation-only comparison:
   Compare the Gram matrix using full labels c=(m,beta,r) with the object seen
   by the accessible radiation record. Depending on the recovery question,
   that record may be m alone, m plus recoverable escape labels, or a block of
   records over several emissions.

   High participation in the full channel but low participation in the
   radiation-only object means the Stinespring transition is generic while the
   instantaneous Hawking record is compressed. Low participation even in the
   full channel means generic export is not supplied by this detachment
   process.

5. Direct decoupling validation:
   If Tests 1, 2, and 4 pass, test an explicit diary/reference subspace under
   the channel generated by D and compute the complementary-channel decoupling
   error. This validates that the second-moment diagnostics really imply
   Page/Hayden-Preskill export.
```

The core decision is made by Tests 1, 2, and 4. Test 0 identifies the correct
thermodynamic operator. Test 3 prevents false interpretation. Test 5 is
validation after the covariance gates pass.

Interpretation:

```text
First moment passes, spreading passes, full Gram participation passes, and
accessible-record participation passes:
  the Matrix detachment channel supplies the second-moment input needed for
  generic information export.

First moment passes, spreading passes, full Gram participation passes, but
accessible-record participation fails:
  the full Stinespring transition is high-participation, but the immediately
  accessible radiation record is compressed. Export may require later records,
  finer radiation access, or additional daughter dynamics.

First moment passes, spreading passes, full Gram participation fails:
  the system is chaotic and thermally evaporating, but the physical emission
  channel is low-rank/common-doorway.

First moment passes, spreading fails:
  the channel can reproduce rates while retaining microscopic doorway memory.

First moment fails:
  the chosen P, Q_m, or coupling is not the Matrix evaporation operator.
```

The result we are trying to decide is therefore:

```text
Does the same microscopic sector coupling Q_m H P that gives D0/Matrix
evaporation rates also have the channel covariance needed for generic
Page/Hayden-Preskill information export?
```

## Calibration Harness

Implemented:

```text
sim/detachment_operator_proxy.py
```

This script is not a BFSS simulation. It is a diagnostic harness for the
objects above. It generates controlled transition matrices `D_{c alpha}` and
measures:

```text
A_detach(omega):
  binned strength function;

G_{c c'}:
  channel-doorway Gram matrix;

participation(G):
  inverse-participation rank of the exit-channel coupling;

accessible-record participation:
  the same participation test after coarse-graining full rows to the record
  labels visible to the recovery problem;

C(t):
  Fourier transform of the strength distribution.
```

Calibration runs:

```text
isotropic:
  gamma_total = 1
  channel_gram_participation_norm = 0.560
  largest_channel_width_fraction = 0.037
  decay_time = 3.41

aligned:
  gamma_total = 1
  channel_gram_participation_norm = 0.010
  largest_channel_width_fraction = 1.000
  decay_time = 1.40

doorway_rank, rank 4:
  gamma_total = 1
  channel_gram_participation_norm = 0.066
  largest_channel_width_fraction = 0.253
  decay_time = 3.41

scarred, 8 percent:
  gamma_total = 1
  channel_gram_participation_norm = 0.065
  largest_channel_width_fraction = 0.242
  decay_time = 4.01

record_blocked:
  gamma_total = 1
  channel_gram_participation_norm = 0.453
  largest_channel_width_fraction = 0.054
  decay_time = 3.41
```

Interpretation:

```text
The aligned model has a smooth strength function and fast decay, but its Gram
matrix is rank one. This demonstrates that spreading-like spectral diagnostics
do not imply information-export participation.

The isotropic model is the calibration pass case.

The doorway-rank and scarred models are controlled failures.

The record-blocked model has moderate total participation while preserving
protected block structure; it is a warning that participation must be checked
inside the correct charge/gauge/record sectors.
```

Verification:

```text
wsl.exe -d Ubuntu-24.04 -- bash -lc \
  "cd /mnt/c/Users/serge/Projects/bh-evaporator && \
   python3 -m py_compile sim/detachment_operator_proxy.py"
```

This syntax check does not reproduce the calibration table. A proper
regression check should rerun the fixed-seed harness and assert the published
diagnostic values within tolerance.

The script writes JSON and strength-function CSV files under:

```text
sim/data/
```

Implemented regression:

```text
sim/regression_detachment_diagnostics.py
```

Run:

```text
wsl.exe -d Ubuntu-24.04 -- bash -lc \
  "cd /mnt/c/Users/serge/Projects/bh-evaporator && \
   python3 sim/regression_detachment_diagnostics.py"
```

This fixed-seed check verifies the local and aligned benchmark diagnostics,
including equality of channel and initial Gram participation and the
accessible-record Gram participation.

## First Hamiltonian-Derived Proxy

Implemented:

```text
sim/sector_detachment_diagnostics.py
```

This script builds explicit finite-dimensional sector Hamiltonians `H_n` and
`H_{n-1}`, diagonalizes them, and constructs

```text
D_{c alpha} = < beta, label | O_remove | alpha >
```

from a concrete sector-removal operator. This is still not BFSS. The point is
that `D` is now derived from Hamiltonian eigenstates and an operator.

Calibration runs at `n=8`, `q=2`, `seed=2468`:

```text
local, bandwidth 0:
  spectral_participation_norm = 1.000
  channel_gram_participation_norm = 1.000
  c_long_mean = 1.000
  decay_time = nan

local, bandwidth 0.25:
  spectral_participation_norm = 0.780
  channel_gram_participation_norm = 0.972
  c_long_mean = 0.0038
  decay_time = 5.81

scrambled, bandwidth 0:
  spectral_participation_norm = 1.000
  channel_gram_participation_norm = 1.000
  c_long_mean = 1.000
  decay_time = nan

scrambled, bandwidth 0.25:
  spectral_participation_norm = 0.780
  channel_gram_participation_norm = 0.972
  c_long_mean = 0.0047
  decay_time = 5.81
```

Interpretation:

```text
With degenerate sector Hamiltonians, the Gram gate can pass while the
spreading gate fails: the correlator does not decay.

With random sector Hamiltonians, even a local removal operator looks
high-participation and has a broad strength function. In this model the
sector eigenbasis scrambling is enough to make both gates pass.

The nearly identical local and scrambled numbers are not a bug in the
diagnostic. They are both generic-class transition operators once the sector
Hamiltonians have random eigenbases. The discriminating axis in this proxy is
generic versus aligned/low-rank, not local versus pre-scrambled.
```

This result is useful as a diagnostic baseline. It says what the BFSS
calculation would need to show in a physical Matrix sector: ordinary
sector-level chaos plus a non-collapsed physical exit-channel Gram matrix.

Strategic status:

```text
This script is on target, but it is not the Matrix/D0 calculation.

It is the analysis backend and calibration bridge. It proves that the
diagnostics can be applied to real transition amplitudes D_{c alpha} derived
from Hamiltonian eigenstates and an operator, and it shows that the spreading
gate and Gram-participation gate are logically independent.

It now also computes accessible-record diagnostics by grouping full rows
`(record label, daughter state)` by record label. This implements Test 4 for
the sector proxy:

```text
accessible_record_gram_participation;
accessible_record_gram_participation_norm;
accessible_record_width_participation;
accessible_record_width_participation_norm;
largest_accessible_record_width_fraction.
```

The next step is not a new diagnostic. The next step is to replace the sector
Hamiltonian frontend with a regulated matrix-model frontend that produces the
same D_{c alpha} from clumped and block-separated matrix sectors.
```

This distinction is important. A positive result in the sector model does not
show that BFSS/Matrix evaporation exports generic information. It only fixes
what the Matrix calculation must output and how it will be judged.

## Sector Scan Result

Implemented:

```text
sim/scan_sector_detachment.py
```

Scan:

```text
n = 8, q = 2
operators = local, scrambled, aligned, low_rank
bandwidths = 0, 0.02, 0.05, 0.1, 0.25, 0.5
seeds = 2468, 2469
```

Main pattern:

```text
Increasing sector bandwidth turns on the spreading gate:
  c_long_mean falls from 1 at bandwidth 0 to O(10^-2) by bandwidth 0.05.

Sector chaos does not repair a bad detachment operator:
  aligned remains Gram-rank one;
  low_rank remains low participation;
  local and scrambled remain high participation.
```

Representative mean scan values:

```text
operator    bw     Gram norm   spectral norm   C-tail   largest width
local       0      1.000       1.000           1.000    0.0039
local       0.05   0.999       0.812           0.016    0.0041
local       0.25   0.972       0.776           0.0048   0.0046

aligned     0      0.004       1.000           1.000    1.000
aligned     0.05   0.004       0.808           0.023    1.000
aligned     0.25   0.004       0.772           0.011    0.999

low_rank    0      0.013       1.000           1.000    0.352
low_rank    0.05   0.013       0.816           0.016    0.352
low_rank    0.25   0.013       0.779           0.0051   0.350
```

Implication:

```text
Chaotic sector eigenstates can make the detachment strength function broad
and the correlator decay. They do not create channel-doorway participation
when the transition operator is structurally aligned or low-rank.
```

This is the clean toy-model analogue of the BFSS question:

```text
Is O_detach a local/scrambled high-participation transition operator,
or an aligned/low-rank doorway into the escape sector?
```

## First Matrix-Coordinate Frontend

Implemented:

```text
sim/matrix_radial_detachment_diagnostics.py
sim/scan_matrix_radial_detachment.py
```

This is the first frontend in which `D_{c alpha}` is generated by a matrix
Hamiltonian coupling rather than by a hand-built sector-removal operator. It
quantizes two real symmetric traceless `2 x 2` matrices,

```text
X_a = [[x_a, y_a], [y_a, -x_a]],  a=1,2,
```

with Hamiltonian

```text
H = 1/2 sum_i p_i^2
  + 1/2 mu^2 sum_i x_i^2
  + g^2 (x_1 y_2 - y_1 x_2)^2.
```

The clumped sector `P` and separated sector `Q` are radial spectral projectors
of

```text
R^2 = sum_i x_i^2.
```

The transition matrix is the actual Feshbach coupling:

```text
D_{c alpha} = <c| Q H P |alpha>,
```

where `|alpha>` diagonalizes `P H P` and `|c>` diagonalizes `Q H Q`. The
accessible-record labels are coarse radial bins inside `Q`.

Representative runs:

```text
cutoff=5, g=1, P=Q=0.30:
  gamma_total = 5.36561
  spectral_participation_norm = 0.410965
  channel_gram_participation_norm = 0.190810
  accessible_record_gram_participation_norm = 0.523783
  c_long_mean = 0.0189411
  decay_time = 0.200501

cutoff=6, g=1, P=Q=0.25:
  gamma_total = 0.666354
  spectral_participation_norm = 0.284051
  channel_gram_participation_norm = 0.0116977
  accessible_record_gram_participation_norm = 0.372338
  c_long_mean = 0.049934
  decay_time = 0.200501
```

The scan over `cutoff=4,5`, `g=0,0.5,1,2`, and sector fractions
`0.25,0.30,0.35` writes:

```text
sim/data/matrix_radial_detachment_scan.csv
```

Main finding:

```text
The radial matrix frontend gives fast spectral decay but modest or low
full-channel Gram participation, and weak accessible-record participation.
Thus radial matrix block separation alone does not produce the generic export
covariance. The missing ingredient is not merely a matrix coordinate or a
radial escape projector; it is a high-participation coupling to a large
chaotic daughter sector.
```

Limitations:

```text
This is a regulated two-matrix `N=2` oscillator, not BFSS. It has no large
daughter black-hole sector, no gauge-singlet projection, no asymptotic
continuum, and no fractionated Matrix state count. It also cannot test the
compound-spreading gate in the BFSS sense: there is no large entropy `S`, no
parametric dense chaotic sector, and no meaningful
Gamma_spread/Gamma_escape ~ S comparison. Its value is diagnostic for the
participation and accessible-record gates: it shows that a literal `Q H P`
matrix-detachment construction can be fed into the same tests, and that the
first matrix-coordinate version lands in the low-participation class.
```

## Source-Resolved Matrix Participation

Implemented:

```text
sim/matrix_source_participation.py
```

This test asks whether multiple source/tether operators can create
high-participation doorway structure before the physical radiation record
coarse-grains them. It uses the same radial matrix Hamiltonian and the same
`P,Q` sectors, but builds source-resolved transition matrices

```text
D_a = <c| Q O_a P |alpha>.
```

It compares:

```text
source_gram_participation:
  participation of S_ab = Tr D_a D_b^\dagger;

stacked channel participation:
  rows labelled by (a,c), as if the source label were recorded;

collective channel participation:
  sum_a D_a, as if the source labels were unresolved.
```

The source sets include coordinate monomials and a decomposition of the
regulated Hamiltonian into kinetic, harmonic, and quartic terms:

```text
--source-set quadratic
--source-set linear_quadratic
--source-set h_terms
```

Representative runs:

```text
cutoff=4, g=1, P=Q=0.35, source_set=quadratic:
  source_gram_participation_norm = 0.827953
  stacked channel_gram_participation_norm = 0.0988068
  collective_channel_gram_participation_norm = 0.0532681
  accessible_record_gram_participation_norm = 0.352322

cutoff=4, g=1, P=Q=0.35, source_set=h_terms:
  source_gram_participation_norm = 0.385230
  stacked channel_gram_participation_norm = 0.107391
  collective_channel_gram_participation_norm = 0.0774841
  accessible_record_gram_participation_norm = 0.431429

cutoff=5, g=1, P=Q=0.20, source_set=h_terms:
  source_gram_participation_norm = 0.262981
  stacked channel_gram_participation_norm = 0.296818
  collective_channel_gram_participation_norm = 0.218917
  accessible_record_gram_participation_norm = 0.737782
```

Interpretation:

```text
Source labels can create real participation, especially for coordinate
monomial sources. The participation is reduced when sources are summed into a
collective channel, and the Hamiltonian-term decomposition is less
source-participating than arbitrary quadratic sources.

This supports the current prediction in a limited proxy form: source/tether
structure is the right place to look for participation, while unresolved
collective coupling can erase a substantial fraction of it.
```

Caveats:

```text
Some cutoff/fraction choices have extremely small total coupling because
low-order source operators do not bridge the chosen radial sectors. In those
cases participation is a relative shape diagnostic, not evidence of a strong
physical detachment rate. The BFSS-relevant question remains whether the
physical block-detachment operator has both appreciable width and high
source/full/access-record participation.
```

## Repeated Accessible-Record Participation

Implemented:

```text
sim/repeated_record_participation.py
```

This test addresses the current temporal-export prediction: a single Hawking
record may be compressed, while a sequence of records after internal
re-scrambling may become high-participation.

Given the one-step radial matrix transition `D`, rows are grouped into record
Kraus operators `K_m`.  For equal `P` and `Q` dimensions the script iterates

```text
K_{m_k ... m_1} = K_{m_k} U ... K_{m_2} U K_{m_1},
```

where `U` is either identity or a fixed random unitary. It measures the
Hilbert-Schmidt Gram participation of the record-sequence operators and the
participation of their widths.

Run examples:

```text
python3 sim/repeated_record_participation.py \
  --cutoff 5 --g 1 --fraction 0.3 --record-bins 3 \
  --max-depth 5 --scrambling identity --normalize \
  --output-csv sim/data/repeated_record_identity_cut5.csv

python3 sim/repeated_record_participation.py \
  --cutoff 5 --g 1 --fraction 0.3 --record-bins 3 \
  --max-depth 5 --scrambling random --normalize \
  --output-csv sim/data/repeated_record_random_cut5.csv
```

Expected decision:

```text
identity evolution keeps record sequences structurally compressed;
random re-scrambling should increase sequence participation if temporal
export is viable in this proxy.
```

Current execution note:

```text
The script was run with a local uv virtualenv:
  .codex_numpy_venv

Since WSL reported no installed distributions in the current shell context,
NumPy was installed into the local venv with uv.
```

First run:

```text
cutoff=5, g=1, fraction=0.30, record_bins=3, max_depth=5, normalized.

identity:
  depth  seqs  participation_norm  absolute_participation  largest_width
  1      3     0.483               1.45                    0.8123
  2      9     0.198               1.78                    0.7271
  3      27    0.078               2.11                    0.6687
  4      81    0.032               2.59                    0.5969
  5      243   0.013               3.16                    0.5462

random re-scrambling:
  depth  seqs  participation_norm  absolute_participation  largest_width
  1      3     0.483               1.45                    0.8123
  2      9     0.239               2.15                    0.6475
  3      27    0.117               3.16                    0.5175
  4      81    0.058               4.70                    0.4132
  5      243   0.029               7.05                    0.3212
```

Interpretation:

```text
Re-scrambling helps: absolute record-sequence participation grows faster and
the largest width fraction drops more quickly than with identity evolution.

It does not make the radial matrix kernel a high-participation export channel:
the number of possible record strings grows as 3^k, while effective
participation remains O(1)-to-O(10) through depth five.

This supports the current diagnosis. Temporal re-scrambling improves a
compressed record channel, but the underlying single-step radial kernel is too
low-participation for re-scrambling alone to produce generic export in this
proxy.
```

## Daughter-Memory Participation

Implemented:

```text
sim/daughter_memory_participation.py
```

This test inserts an explicit daughter-memory system between source-resolved
matrix amplitudes and the collective radiation record. Starting from source
blocks

```text
D_a = <q| Q O_a P |alpha>,
```

each source is assigned a daughter-memory vector `|chi_a>`. Their overlap is
tunable:

```text
<chi_b|chi_a> = (1-rho) delta_ab + rho.
```

Thus:

```text
rho = 0:
  orthogonal daughter memory; source/tether distinctions are retained.

rho = 1:
  identical daughter memory; source/tether distinctions are erased, giving the
  collective-channel limit.
```

Representative runs:

```text
cutoff=4, fraction=0.35, source_set=quadratic:
  rho=0:
    channel_gram_participation_norm = 0.103
    channel_gram_participation = 9.3
    accessible_record_gram_participation_norm = 0.340
  rho=1:
    channel_gram_participation_norm = 0.056
    channel_gram_participation = 5.0
    accessible_record_gram_participation_norm = 0.340

cutoff=5, fraction=0.20, source_set=quadratic:
  rho=0:
    channel_gram_participation_norm = 0.408
    accessible_record_gram_participation_norm = 0.861
    gamma_total = 4.74e-27
  rho=1:
    channel_gram_participation_norm = 0.222
    accessible_record_gram_participation_norm = 0.861
    gamma_total = 7.42e-27

cutoff=5, fraction=0.20, source_set=h_terms:
  rho=0:
    channel_gram_participation_norm = 0.360
    accessible_record_gram_participation_norm = 0.903
    gamma_total = 2.25e-26
  rho=1:
    channel_gram_participation_norm = 0.276
    accessible_record_gram_participation_norm = 0.903
    gamma_total = 3.52e-26
```

Interpretation:

```text
Daughter memory helps preserve source/tether participation. Orthogonal
daughter memories generally give higher full-channel participation than
identical memories.

The important negative qualifier is the width. The cutoff=5 cases with strong
participation have extremely small total coupling across the chosen radial
gap. They show that daughter memory can preserve participation shape, not that
the regulated radial model has a physically strong detachment channel.

The Matrix/BFSS target therefore has two simultaneous requirements:
  appreciable detachment width;
  high source/daughter/access-record participation.
```

## Width-Participation Frontier

Implemented:

```text
sim/scan_width_participation_frontier.py
```

This scan asks whether the regulated daughter-memory/source model can find a
corner with both appreciable transition width and high participation. It ranks
models by a simple combined score:

```text
gamma_total
  * channel_gram_participation_norm
  * accessible_record_gram_participation_norm.
```

First compact scan:

```text
cutoff=4;
g = 0.5, 1, 2;
fraction = 0.25, 0.30, 0.35, 0.40;
source_set = quadratic, h_terms;
rho = 0, 1.
```

Best region:

```text
cutoff=4, g=2, fraction=0.40, source_set=h_terms, rho=0:
  gamma_total = 1.32e3
  channel_gram_participation_norm = 0.140
  channel_gram_participation = 14.24
  accessible_record_gram_participation_norm = 0.338
  largest_channel_width_fraction = 0.117

same, rho=1:
  gamma_total = 8.83e2
  channel_gram_participation_norm = 0.112
  channel_gram_participation = 11.45
  accessible_record_gram_participation_norm = 0.338
  largest_channel_width_fraction = 0.143
```

Interpretation:

```text
The width-participation tradeoff is not absolute in the toy model. There are
corners with large width and nontrivial full-channel participation. Daughter
memory improves full participation modestly in this corner.

The accessible-record participation remains moderate, and one record can
dominate the width. A repeated-record check at this same strong-width corner
shows that random re-scrambling does not help when the one-step record widths
are extremely biased:

  random re-scrambling, depth 5:
    participation_norm = 0.005 out of 243 strings;
    largest width fraction = 0.951.

Thus the refined simultaneous target is:
  appreciable width;
  high full-channel participation;
  balanced accessible-record weights;
  growth under repeated records.
```

## Source-To-Record Map

Implemented:

```text
sim/record_map_participation.py
```

This test inserts an explicit map from source/tether labels to accessible
radiation record labels:

```text
D_{m,ell,q; alpha}
  = sum_a C_{m a} chi_a(ell) D_a(q,alpha).
```

Here `C_{m a}` is a source-to-record map and `chi_a` is the daughter-memory
vector. Tested maps:

```text
aligned:
  all sources feed one record;

round_robin:
  sources are distributed evenly among records;

random_orthogonal:
  orthonormal random record rows;

random_dense:
  dense random record rows.
```

Strong-width corner:

```text
cutoff=4, g=2, fraction=0.40, source_set=h_terms.
```

Representative results:

```text
round_robin, records=3, rho=0:
  gamma_total = 379
  channel_gram_participation_norm = 0.137
  accessible_record_gram_participation_norm = 0.815
  accessible_record_width_participation_norm = 0.815
  largest_accessible_record_width_fraction = 0.506

random_orthogonal, records=4, rho=0:
  gamma_total = 544
  channel_gram_participation_norm = 0.139
  accessible_record_gram_participation_norm = 0.575
  accessible_record_width_participation_norm = 0.894
  largest_accessible_record_width_fraction = 0.339

aligned, records=3, rho=0:
  gamma_total = 120
  channel_gram_participation_norm = 0.140
  accessible_record_gram_participation_norm = 0.333
  accessible_record_width_participation_norm = 0.333
  largest_accessible_record_width_fraction = 1.000
```

Weaker-coupling, better-balance corner:

```text
cutoff=4, g=0.5, fraction=0.40, source_set=h_terms.

round_robin, records=6, rho=0:
  gamma_total = 16.7
  channel_gram_participation_norm = 0.298
  accessible_record_gram_participation_norm = 0.899
  accessible_record_width_participation_norm = 0.899
  largest_accessible_record_width_fraction = 0.210
```

Interpretation:

```text
Balanced source-to-record coupling is the first proxy ingredient that
simultaneously improves width, full-channel participation, and accessible
record balance. Aligned coupling is the expected failure: full participation
can remain similar, but all accessible width sits in one record.

This sharpens the Matrix/BFSS target again. The physical detachment operator
must not only have many source/tether doorways and daughter memory; the
outgoing radiation channel must receive those doorways through a sufficiently
balanced source-to-record map.
```

## Recycled Record-Map Dynamics

Implemented:

```text
sim/recycled_record_map_dynamics.py
```

The source-to-record map is generally non-square: it maps an input shell to a
daughter-memory/output space. To test temporal record accumulation, this
script adds a random recycling isometry `R` from the full output space back to
the next input shell and defines square record Kraus operators

```text
K_m = R P_m D.
```

This is a controlled proxy for daughter reprocessing between emissions. It is
not a BFSS evolution.

Strong-width corner:

```text
cutoff=4, g=2, fraction=0.40, source_set=h_terms, rho=0.
```

Control failure:

```text
aligned record map, random scrambling:
  depth 1: participation_norm = 0.333 out of 3 strings;
           largest width fraction = 1.000
  depth 5: participation_norm = 0.004 out of 243 strings;
           largest width fraction = 1.000
```

Balanced positive cases:

```text
round_robin, records=3, identity:
  depth 1: participation_norm = 0.820 out of 3 strings;
           largest width fraction = 0.4968
  depth 5: participation_norm = 0.216 out of 243 strings;
           absolute participation ~ 52.5;
           largest width fraction = 0.0316

round_robin, records=3, random:
  depth 5: participation_norm = 0.187 out of 243 strings;
           absolute participation ~ 45.4;
           largest width fraction = 0.0488

random_orthogonal, records=4, identity:
  depth 1: participation_norm = 0.820 out of 4 strings;
           largest width fraction = 0.3804
  depth 5: participation_norm = 0.157 out of 1024 strings;
           absolute participation ~ 161;
           largest width fraction = 0.0077
```

Longer-depth check:

```text
round_robin, records=3, identity:
  depth 7:
    sequence count = 2187;
    Gram participation norm = 0.040;
    absolute Gram participation ~ 87.5;
    width participation norm = 0.217;
    absolute width participation ~ 474;
    largest width fraction = 0.0090.

random_orthogonal, records=4, identity:
  depth 6:
    sequence count = 4096;
    Gram participation norm = 0.051;
    absolute Gram participation ~ 209;
    width participation norm = 0.333;
    absolute width participation ~ 1364;
    largest width fraction = 0.0033.
```

Daughter-memory comparison:

```text
round_robin, records=3, rho=1, identity:
  depth 7:
    Gram participation norm = 0.041;
    absolute Gram participation ~ 90;
    width participation norm = 0.209;
    largest width fraction = 0.0087.

random_orthogonal, records=4, rho=1, identity:
  depth 6:
    Gram participation norm = 0.033;
    absolute Gram participation ~ 135;
    width participation norm = 0.296;
    largest width fraction = 0.0024.
```

Interpretation:

```text
This is the first positive proxy for temporal accessible export. Balanced
source-to-record coupling plus daughter recycling generates broad record
histories. Aligned coupling fails completely.

The growth is submaximal but exponential over the tested window. Widths spread
over record histories faster than the full Hilbert-Schmidt Gram participation:
record probabilities can become broad before the corresponding record
operators become close to independent.

In this recycled proxy, balanced source-to-record coupling is more important
for record-width spreading than orthogonal daughter memory. Orthogonal
daughter memory still helps full operator independence, especially for
random-orthogonal records.

In this proxy the extra random internal unitary is not the essential step; the
recycling map and balanced record coupling already mix the effective channel.
The physical Matrix/BFSS question is therefore whether block detachment
provides a comparable balanced map from many source/tether doorways into
emitted records over the evaporation sequence.
```

## Record Entropy-Rate Scan

Implemented:

```text
sim/record_entropy_rate_scan.py
```

This scan reports the effective record-history entropy rates

```text
h_gram(k)  = log N_eff,Gram(k) / k
h_width(k) = log N_eff,width(k) / k
```

and normalizes them by `log M`, where `M` is the number of accessible record
labels. In any fixed finite proxy this is a pre-saturation slope: the input
dimension bounds `N_eff`, so `log N_eff(k)/k` eventually goes to zero at fixed
cutoff. The physically relevant question is whether the pre-saturation slope
persists as the shell dimension grows.

`h_width` is the participation entropy of the probability distribution over
record strings. It is a useful balance diagnostic, but it is classical: a
balanced Markov-like record source can have large `h_width` without exporting
arbitrary quantum information. The stronger diagnostic is `h_gram`, the
Hilbert--Schmidt independence of the record-history Kraus operators. The
natural-bin scans below therefore treat width entropy as the scalable first
screen and Gram entropy as the export-relevant check where it is computable or
sampled.

Runs at the strong-width corner:

```text
cutoff=4, g=2, fraction=0.40, source_set=h_terms.
```

Control:

```text
aligned, records=3, rho=0, identity, depth=6:
  Gram participation = 1.00;
  width participation = 1.00;
  h_gram/log(3) = 0.000;
  h_width/log(3) = 0.000;
  largest width fraction = 1.0000.
```

Balanced maps:

```text
round_robin, records=3, rho=0, identity, depth=6:
  Gram participation = 71.44;
  width participation = 193.01;
  h_gram/log(3) = 0.648;
  h_width/log(3) = 0.798;
  largest width fraction = 0.0206.

random_orthogonal, records=4, rho=0, identity, depth=5:
  Gram participation = 160.58;
  width participation = 412.74;
  h_gram/log(4) = 0.733;
  h_width/log(4) = 0.869;
  largest width fraction = 0.0077.

random_dense, records=3, rho=0, identity, depth=5:
  Gram participation = 94.44;
  width participation = 219.15;
  h_gram/log(3) = 0.828;
  h_width/log(3) = 0.981;
  largest width fraction = 0.0091.
```

Variant checks:

```text
For round_robin, records=3, depth=6, changing rho from 0 to 1 and identity
to random inter-step dynamics leaves h_width/log(3) in the range 0.762--0.800.

For random_orthogonal, records=4, depth=5, the corresponding h_width/log(4)
range is 0.855--0.869.

For random_orthogonal and random_dense, records=4, rho=0, identity, depth=5,
two additional seeds gave h_width/log(4) in the range 0.831--0.931 and
h_gram/log(4) in the range 0.677--0.744.
```

Interpretation:

```text
The inserted-map proxy shows constructive existence: if a balanced
source-to-record map and a recycling map are supplied, record histories become
broad and the corresponding Kraus operators are independent over the tested
window. This is a useful control, but it is not evidence that the physical
Matrix detachment operator supplies those structures.

The main non-engineered numerical test starts with the natural record-bin
scan below, where the accessible labels are inherited from the matrix proxy
instead of inserted as a designed map.
```

## Natural Record-Bin Test

Implemented:

```text
sim/natural_record_entropy_rate.py
```

This removes the inserted source-to-record map `C_{ma}`. Starting from
source-resolved matrix amplitudes `D_a(q,alpha)`, it adds optional daughter
memory and uses the matrix proxy's own `Q`-sector radial/energy bin of `q` as
the accessible radiation record. This is the first non-engineered positive
test in the numerical chain: record balance is whatever the proxy dynamics and
sector cut provide.

Strong-width corner:

```text
cutoff=4, g=2, fraction=0.40, source_set=h_terms, record_bins=3:
  depth=6, rho=0:
    h_width/log(3) = 0.008;
    largest width fraction = 0.9726.

  depth=6, rho=1:
    h_width/log(3) = 0.017;
    largest width fraction = 0.9444.
```

With six natural bins:

```text
cutoff=4, g=2, fraction=0.40, source_set=h_terms, record_bins=6:
  depth=5, width-only, rho=0:
    h_width/log(6) = 0.240;
    largest width fraction = 0.2845.

  depth=5, width-only, rho=1:
    h_width/log(6) = 0.262;
    largest width fraction = 0.2442.
```

Weaker-coupling natural-bin corner:

```text
cutoff=4, g=0.5, fraction=0.40, source_set=h_terms, record_bins=6:
  one-step gamma_total = 31.8 at rho=0 and 20.6 at rho=1;
  accessible_record_gram_participation_norm = 0.744;
  accessible_record_width_participation_norm = 0.602--0.692.

  depth=4, full Gram:
    rho=0:
      h_gram/log(6) = 0.713;
      h_width/log(6) = 0.736;
      largest width fraction = 0.0291.

    rho=1:
      h_gram/log(6) = 0.741;
      h_width/log(6) = 0.797;
      largest width fraction = 0.0215.

  depth=5, width-only:
    rho=0:
      h_width/log(6) = 0.738;
      largest width fraction = 0.0113.

    rho=1:
      h_width/log(6) = 0.794;
      largest width fraction = 0.0082.
```

Interpretation:

```text
The hand-inserted balanced source-to-record map is not the only way to obtain
a positive record entropy rate. The matrix proxy's own natural record bins can
produce a large temporal width entropy rate in a weaker-coupling regime with
non-negligible one-step width.

The strong-width corner remains compressed under natural bins. More coupling
does not monotonically improve export; it can concentrate the record weights
into a few bins. This makes accessible-record balance a real dynamical gate,
not a cosmetic diagnostic.
```

## Natural-Bin Phase Scan

Implemented:

```text
sim/natural_record_phase_scan.py
```

This is the headline numerical result of the current proxy. It scans natural
matrix record bins without normalizing away the physical one-step width. The
broad diagnostic is the width entropy rate at depth five, followed by Gram
checks where feasible.

For `source_set=h_terms`, `record_bins=6`, `cutoff=4`, the scan shows three
regimes:

```text
1. Broad but inactive:
   fraction = 0.25--0.30 gives h_width/log(6) ~ 0.8--0.98, but
   one-step width is ~10^{-29}--10^{-27}. These points are boundary artifacts
   of the finite radial-sector cut.

2. Active and broad:
   fraction = 0.40, g = 0.25--0.5 gives one-step width ~1.6--2.9 and
   h_width/log(6) ~ 0.70--0.81.

3. Active but compressed:
   fraction = 0.35--0.40, g = 1--2 gives one-step width from O(1) to O(100)
   while h_width/log(6) falls to 0.01--0.37. At g=2, fraction=0.35 one
   history carries more than 90 percent of the width.
```

The quadratic-source scan over the active region has the same shape but lower
entropy rates:

```text
best active point:
  source_set=quadratic, g=0.5, fraction=0.40, record_bins=6, rho=0:
    one-step width = 8.42;
    h_width/log(6) = 0.535 at depth five;
    h_gram/log(6) = 0.516 at depth four.
```

Interpretation:

```text
The natural-bin proxy now has a phase boundary. Increasing coupling or moving
the sector cut can turn on width while simultaneously compressing accessible
records. The active export window is intermediate: enough width to detach, but
not so much concentration that one record history dominates.

This is the first calculation in the current chain that separates three
physical possibilities rather than only pass/fail:
  negligible detachment;
  active balanced export;
  active compressed emission.
```

Cutoff-five scaling check:

```text
sim/natural_record_phase_scan.py was rerun at cutoff=5 for h_terms sources,
six natural bins, and the active sector fractions 0.35--0.40.

At depth five:
  g=0.25, fraction=0.40:
    one-step width = 5.32;
    h_width/log(6) = 0.873;
    largest width fraction = 0.0013.

  g=0.5, fraction=0.40:
    one-step width = 5.34;
    h_width/log(6) = 0.842;
    largest width fraction = 0.0016.

  g=0.5, fraction=0.35:
    one-step width = 1.58;
    h_width/log(6) = 0.822;
    largest width fraction = 0.0022.

  g=2, fraction=0.40:
    one-step width = 5.31;
    h_width/log(6) = 0.582;
    largest width fraction = 0.0351.
```

Full-Gram cutoff-five checks are memory-limited beyond depth three in the
current implementation. At depth three:

```text
  g=0.25, fraction=0.40:
    h_gram/log(6) = 0.872;
    h_width/log(6) = 0.874.

  g=0.5, fraction=0.35:
    h_gram/log(6) = 0.820;
    h_width/log(6) = 0.823.

  g=2, fraction=0.40:
    h_gram/log(6) = 0.582;
    h_width/log(6) = 0.582.
```

Interpretation:

```text
The active balanced window is not a cutoff-four artifact for the h_terms
source family. It persists at cutoff five with comparable or better width
entropy rates. The early-depth Gram check tracks the width check closely in
the sampled points, so operator-history distinguishability is positive in the
regime small enough for direct Gram checks.

The quadratic-source family at cutoff five is broad but inactive in this
sector cut: one-step widths are ~10^{-27}. It is not counted as a positive
physical window.
```

Cutoff-six check:

```text
sim/natural_record_phase_scan.py was run at cutoff=6 for h_terms sources,
six natural bins, and selected active-window points.

At depth four:
  g=0.25, fraction=0.40:
    one-step width = 16.4;
    h_width/log(6) = 0.854;
    largest width fraction = 0.0096.

  g=0.5, fraction=0.40:
    one-step width = 16.3;
    h_width/log(6) = 0.775;
    largest width fraction = 0.0230.

  g=0.5, fraction=0.35:
    one-step width = 6.43;
    h_width/log(6) = 0.803;
    largest width fraction = 0.0121.

  g=1, fraction=0.40:
    one-step width = 16.4;
    h_width/log(6) = 0.573;
    largest width fraction = 0.0739.

  g=2, fraction=0.40:
    one-step width = 16.4;
    h_width/log(6) = 0.519;
    largest width fraction = 0.1008.
```

Sampled Gram checks at cutoff six:

```text
  g=0.25, fraction=0.40, depth=4, 1000 weighted samples:
    h_gram/log(6) = 0.807;
    h_width/log(6) = 0.854.

  g=2, fraction=0.40, depth=4, 500 weighted samples:
    h_gram/log(6) = 0.545;
    h_width/log(6) = 0.519.
```

Interpretation:

```text
The active balanced window persists through cutoff six in the width-entropy
diagnostic. The window remains intermediate: lower coupling gives broader
record histories, while stronger coupling increases compression. Sampled Gram
participation is positive at cutoff six and tracks the width rate well in the
best active point. The stronger-coupling point remains lower-rate in both
diagnostics. The operator-history claim at cutoff six rests on sampled Gram
estimates, not exact full-Gram enumeration.
```

Cutoff-seven resource probe:

```text
One h_terms active-window point was pushed to cutoff seven:

  g=0.25, fraction=0.40, record_bins=6.

At depth three:
  one-step width = 36.9;
  h_width/log(6) = 0.867;
  largest width fraction = 0.0228.

At depth four:
  one-step width = 36.9;
  h_width/log(6) = 0.867;
  largest width fraction = 0.0065.
```

The sampled Gram estimator is not reliable at cutoff seven with the small
sample count affordable in this implementation. The cutoff-seven result is
therefore a width-entropy scaling check, not an operator-Gram confirmation.

## Direct Decoupling Check

Implemented:

```text
sim/natural_record_decoupling_test.py
```

This is Test 5 for the proxy. For a sequence of natural-record Kraus operators
`K_s`, it forms the complementary state `rho_{R B}` for a random code diary
and computes

```text
|| rho_{R B} - rho_R tensor rho_B ||_1.
```

The test first whitens

```text
T = sum_s K_s^\dagger K_s
```

and restricts to the support of `T`, so the resulting record-history channel
is trace preserving on the tested support. This means the direct decoupling
check tests the channel shape after conditioning on the active support. The
one-step width remains a separate gate.

Cutoff-four, two-dimensional diary:

```text
active natural-bin point:
  cutoff=4, g=0.5, fraction=0.40, source_set=h_terms, record_bins=6

  depth 1: error = 1.475
  depth 2: error = 1.303
  depth 3: error = 0.857
  depth 4: error = 0.485

compressed point:
  cutoff=4, g=2, fraction=0.35, source_set=h_terms, record_bins=6

  depth 1: error = 1.498
  depth 2: error = 1.352
  depth 3: error = 1.127
  depth 4: error = 0.841
```

Cutoff-four, four-dimensional diary:

```text
active point:
  depth 4: error = 0.693

compressed point:
  depth 4: error = 1.159
```

Cutoff-five, two-dimensional diary:

```text
active point:
  cutoff=5, g=0.25, fraction=0.40
  depth 3: error = 1.069

more compressed point:
  cutoff=5, g=2, fraction=0.40
  depth 3: error = 1.280
```

Interpretation:

```text
The direct decoupling test agrees qualitatively with the entropy-rate
diagnostics: active natural-bin points decouple faster than compressed points.
It does not yet show near-perfect recovery in the accessible depths. The
current conclusion is therefore comparative, not asymptotic: the phase
diagram predicts the direction of decoupling improvement, but a small
decoupling error has not been demonstrated at larger cutoff/depth.
```
