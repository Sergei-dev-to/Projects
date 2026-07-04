# Experimental Prediction Routes

Date: 2026-06-18

Role: conceptual bridge / experimental target

Status: current route map

## Core Question

Which constrained-access claims can become experimentally or numerically
testable inside ordinary quantum mechanics?

The target is not a new Born-rule prediction. The target is an
operational separation:

```text
same or similar public records
different private quantum fates.
```

The three measured quantities are:

```text
R_public:
    redundant public recoverability of pointer/sector data

lambda:
    de-protection or observability rate of private operators

F_export:
    entanglement-fidelity recovery of a private diary from allowed
    records and side information
```

The broad operational separation is:

```text
R_public high + lambda high does not imply F_export high.
```

The sharper empirical target is:

```text
scrambling / OTOC growth does not imply coherent recovery.
```

The interesting version is not the abelian dephasing corner, where the
answer is obvious. It is a structurally constrained but genuinely
scrambling system: OTOCs and operator growth say "scrambled," while
private-diary recovery fidelity remains bounded because symmetry,
fragmentation, conservation, or the record partition obstructs coherent
export.

## Demonstration Versus Discrimination

On a fully engineered platform, many outcomes are known by construction.
If the channel is built as dephasing, coherent scrambling, protected
storage, local routing, or global encoding, the access profile should
confirm that design. That is still useful as calibration, but it is not
yet a discriminating measurement of unknown physics.

The routes below therefore split into two classes:

```text
framework demonstrations:
    show that R_public, lambda, and F_export are distinct measurable
    quantities and can be independently controlled

discriminating measurements:
    test a quantitative access law or distinguish mechanisms in a system
    whose private-information fate is not fixed by inspection
```

The strongest near-term science is the second class. In particular, a
numerical recovery-versus-scrambling phase diagram can decide an open
question for the theory: whether the export transition generically
tracks scrambling, or whether structural obstructions separate them.

## Route 0: Recovery Transition Versus Scrambling Transition

### Protocol

Choose concrete many-body models with tunable structure:

```text
connectivity:
    local lattice -> long-range -> expander/all-to-all

export structure:
    generic chaotic -> symmetry-constrained -> fragmented/integrable
```

Prepare a diary entangled with a reference, evolve, and measure both:

```text
scrambling diagnostics:
    OTOCs, operator size, tripartite information, or related probes

recovery diagnostics:
    F_export from an explicit HP-style decoder or optimized recovery
    over the allowed record partition
```

### Prediction

There should be regimes with:

```text
scrambling high
F_export low
```

because the obstruction is not lack of chaos, but failure of coherent
export through the specified records.

The strongest cell is:

```text
fast access geometry
+ fast OTOC/operator growth
+ symmetry/fragmentation/partition obstruction
=> bounded private recovery fidelity.
```

### Why It Is Interesting

This is the access/export factorization made empirical. It corrects the
common shortcut:

```text
scrambling -> recoverability.
```

Recoverability is a finer probe than OTOC growth because it tests the
channel partition and decoupling condition, not just operator spreading.

### Why Numerical First

The deterministic export gap is theoretically open. A numerical phase
diagram across connectivity, integrability breaking, symmetry, and
record partition would decide which model class is worth proving a
theorem about.

If `F_export` separates cleanly from OTOCs, the experiment has a
well-motivated target. If it does not, the theory learns that coherent
export may be more generic than the current caution suggests.

### Risk

`F_export` is more expensive than OTOCs. Small-system numerics may also
blur the asymptotic distinction, so the model choice and finite-size
scaling matter.

## Route 1: Same Public Record, Different Private Fate

### Protocol

Prepare:

```text
system/pointer S
diary D entangled with reference R_D
environment or record register E_1 ... E_N
```

Run three channels engineered to produce similar redundant public records
for the pointer label:

```text
protected sector:
    public record of x; private block untouched

dephasing/public channel:
    public record of x; private coherence de-protected and dephased

coherent export channel:
    public record of x; private diary recoverable after collecting the
    right records and side information
```

Measure:

```text
R_public(m):
    public information in m fragments

lambda(n):
    decay of protected private operator component

F_export(m,n):
    recovery fidelity of D from allowed records
```

### Prediction

The three channels can be tuned so that:

```text
R_public(m) nearly identical
```

while:

```text
protected:
    lambda ~ 0, F_export low

dephasing:
    lambda high, F_export low

coherent export:
    lambda high, F_export high after record budget
```

This is the cleanest calibration demo of the program's access-profile
language.

### Why It Is Interesting

It separates:

```text
classical objectivity
loss of protection
recoverable hiding
```

using standard quantum mechanics. The novelty is not any single
ingredient; it is the joint access profile and the engineering
constraint of matching `R_public(m)` while changing the private fate.

### Risk

This is mostly Quantum Darwinism plus dephasing plus coherent
scrambling/eraser logic measured side by side. It should not be billed
as the headline prediction. Its role is to calibrate the access-profile
diagnostics before applying them to less transparent systems.

## Route 2: Frozen-Dynamics Diagnostic

### Protocol

Compare normal dynamics with a frozen internal dynamics:

```text
normal:
    records form while internal dynamics routes/scrambles private
    information

frozen:
    public records still form, but source-local routing is suppressed
```

The clean freeze is:

```text
H_internal -> 0
with the record coupling held fixed.
```

An echo or time-reversal protocol is different: it may enlarge the
accessible control algebra rather than merely halt routing.

Measure whether private diary recovery survives:

```text
F_export^normal
versus
F_export^frozen.
```

### Prediction

```text
if recovery collapses under frozen dynamics:
    private recovery used routed/scrambled access

if recovery survives under frozen dynamics:
    allowed records or side information were already nonlocal/dressed
    relative to the chosen source factorization
```

### Why It Is Interesting

This is the laboratory analogue of the routed-versus-dressed distinction
in horizon models. It gives an operational test of whether recovery
comes from dynamics or from the access algebra already being global.

### Risk

Requires a clean definition of what is frozen. On a fully engineered
simulator, the answer may be known from the construction; the route
becomes a genuine diagnostic when applied to a system whose access
structure is not obvious a priori.

## Route 3: Locality / Interaction-Range Scaling

### Protocol

Use a platform with tunable interaction geometry:

```text
1D or 2D local circuit
long-range power-law circuit
all-to-all or expander-like circuit
```

Deposit a diary at varying distance from the access/readout region.

Measure:

```text
t_public:
    public record time

t_deprotect:
    time for private operators to lose protected component

t_export:
    time/records needed for high F_export
```

### Prediction

For source-local finite-velocity access:

```text
t_export >= routing distance / velocity
```

up to logarithmic corrections. Increasing interaction range should
change private recovery latency while public records may remain similar.

Expected scaling:

```text
local lattice:
    worst-case t_export power-law in system size

long-range / expander-like:
    t_export can become logarithmic or polylogarithmic if coherent
    export is present
```

### Why It Is Interesting

This is the most direct experimental version of the latency theorem. It
predicts a scaling law for private recovery latency as the access
geometry is changed, rather than merely confirming a channel whose fate
was engineered by hand. It turns the horizon/local-reservoir distinction
into a tunable many-body access-profile measurement.

### Risk

Fast operator growth alone is insufficient. The experiment must measure
recovery fidelity, not only OTOCs or commutators.

## Route 4: De-Protection Without Recovery Counterexample

### Protocol

Implement a fast spreading but abelian/public export circuit, for
example controlled-phase or CNOT-style spreading on a graph, with records
restricted to a commuting `Z` algebra.

Measure:

```text
operator de-protection:
    off-diagonal diary operators leave the commutant/are dephased

recovery:
    entanglement fidelity from allowed records remains low
```

### Prediction

```text
lambda high
F_export low
```

even when support growth or selected OTOCs are fast.

### Why It Is Interesting

It is the simplest experimentally clean falsification of the naive
chain:

```text
operator growth -> visibility -> recovery.
```

It also demonstrates why the second-moment/export condition is the
recovery-relevant invariant.

### Risk

The abelian model is simple enough that the result may feel obvious. Its
value is as a calibration and control, not as the headline experiment.

## Route 5: Disturbance Cost Of Private Recovery

### Protocol

After public records have formed, attempt private recovery using an
enlarged access operation. Measure how much the operation disturbs the
public records:

```text
D_pub:
    loss of public decoding fidelity or trace-distance disturbance of
    the public-record state after private recovery
```

One concrete definition is:

```text
D_pub = max_x 1/2 || rho_pub^x(after recovery)
                    - rho_pub^x(before recovery) ||_1
```

or the corresponding drop in the optimal public-label decoding
probability.

Compare:

```text
dephasing channel:
    private recovery requires reversing/erasing public records

coherent export channel:
    private recovery may be possible from late records/side information
    with lower disturbance to established public records

protected sector:
    recovery impossible without changing access to the protected block
```

### Prediction

Private recovery has different disturbance costs in the three fates.
For dephased information, recovery typically requires erasing or
reversing the public which-record. For coherently hidden/exported
information, recovery can be possible from an enlarged record algebra
with lower disturbance to already established public records.

### Why It Is Interesting

This may connect most directly to measurement, Wigner-friend, and
quantum eraser language. It distinguishes "destroyed relative to the
public record" from "hidden in a larger coherent algebra" operationally,
through the disturbance cost of recovery.

### Risk

The disturbance metric must be chosen carefully; otherwise the protocol
collapses into ordinary eraser/tomography language.

## Route 6: Collapse / Noise Comparison

### Protocol

Repeat a coherent-export protocol while adding controlled noise or
testing against an objective-collapse-inspired noise model.

Measure:

```text
F_export as access is enlarged
```

### Prediction

Under unitary quantum mechanics:

```text
effective forgetting can become recoverable hiding when access is
enlarged.
```

Under sufficient irreversible noise or collapse:

```text
F_export remains bounded away from one even with enlarged coherent
access.
```

### Why It Is Interesting

This is the most philosophically provocative route, but it is not the
cleanest near-term program result.

### Risk

It depends on noise modeling and experimental scale. It should follow a
clean access-profile demonstration, not precede it.

## Ranking

For discriminating experimental content:

```text
1. Recovery transition versus scrambling transition.
2. Locality / interaction-range scaling.
3. Disturbance cost of private recovery.
4. Frozen-dynamics diagnostic on a system with non-obvious access
   structure.
5. Collapse / noise comparison.
6. Same public record, different private fate.
7. De-protection without recovery counterexample.
```

For framework calibration:

```text
1. Same public record, different private fate.
2. De-protection without recovery counterexample.
3. Frozen-dynamics diagnostic on an engineered simulator.
4. Disturbance cost of private recovery.
5. Locality / interaction-range scaling.
6. Recovery transition versus scrambling transition.
7. Collapse / noise comparison.
```

## Recommended Next Artifact

Write a numerical phase-diagram protocol first.

Model axes:

```text
connectivity/locality;
structure/export obstruction;
record partition.
```

Measured curves:

```text
OTOC/operator-size/scrambling diagnostic;
F_export from explicit decoder or optimized recovery;
optional R_public and lambda for calibration.
```

Target:

```text
find or rule out a cell with fast scrambling and bounded recovery.
```

Then write a calibration suite with three matched channels:

```text
protected sector;
dephasing/public export;
coherent scrambling/export.
```

For each, compute or simulate:

```text
R_public(m)
lambda(n)
F_export(m,n)
D_pub if recovery is attempted
```

The third artifact is the experimental scaling protocol:

```text
same diary and record channel;
tunable interaction/access geometry;
measure t_export from recovery fidelity, not from OTOCs.
```

The phase diagram tests the central nontrivial claim. The calibration
suite validates the diagnostics. The scaling protocol is the cleanest
path from the theorem stack to a tunable many-body experiment.
