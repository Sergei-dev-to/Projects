# Access-latency stress test

Date: 2026-06-14

Status: focused program note.  Purpose is to test the access-latency
classification against standard cases and decide whether it is a real
organizing result.

## Classification to test

The current firm theorem is:

```text
finite LR velocity + source-local emission
=> no location-uniform fast recovery of arbitrary private deposits.
```

Equivalently:

```text
location-uniform fast private recovery
=> fast internal routing/scrambling
   OR nonlocal/dressed access.
```

Here:

```text
source-local emission:
    the record is produced by coupling to a bounded region X of the
    source in factorized source variables;

finite LR velocity:
    information deposited far from X cannot reach X faster than the
    LR/operator-growth light cone;

location-uniform fast recovery:
    arbitrary deposits throughout the source are recoverable from the
    allowed record/access algebra in sub-power-law, usually logarithmic,
    record depth or time.
```

The theorem is about private quantum information.  It does not require
public-record redundancy, compression, anonymity, or source-side
saturation.  Those are extra horizon-profile predicates.

## Case 1: ordinary local reservoir

Example:

```text
d-dimensional spin/fluid/solid reservoir;
finite-range bounded Hamiltonian;
records emitted through a surface or contact region X;
diary deposited in the bulk.
```

Classification:

```text
finite LR velocity:
    yes;

source-local emission:
    yes, for surface/contact monitoring;

location-uniform fast private recovery:
    no.
```

Reason:

```text
T_rec >= d(X,Y)/v.
```

For worst-case bulk deposits in a `d`-dimensional system with entropy
`S~R^d`,

```text
T_rec = Omega(R) = Omega(S^{1/d})
```

up to logarithmic and geometry-dependent factors.

Verdict:

```text
fits classification.
```

Ordinary reservoirs can be thermal and Darwinian-public, but their
private quantum information is transport-limited.

## Case 2: saturated slow router

Theorem construction:

```text
S source cells, one private qubit per cell;
normalized local source jumps J_i with Gram matrix W_ij = delta_ij;
therefore N_eff(W)=(Tr W)^2/Tr W^2=S;
each emitted record samples only one cell.
```

Classification:

```text
source-side saturation:
    yes;

finite LR velocity:
    yes;

source-local emission:
    yes;

location-uniform fast recovery:
    no.
```

Reason:

Saturation is a capacity/participation statement.  It says many source
operators participate in the access family.  It does not say that a new
diary is quickly sampled by the emitted record.

For a diary deposited in a fixed cell `j`, after `n` records the
probability that cell `j` has been sampled is at most `n/S`.  Conditioned
on no sample of `j`, the emitted record is independent of the diary.  The
diary-to-record channel therefore has the form

```text
N_n = (1-p_n) C_n + p_n M_n,
p_n <= n/S,
```

with `C_n` constant on the diary.  Hence

```text
||N_n-C_n||_diamond <= 2n/S,
F_rec <= 1/d_D + O(n/S).
```

Order-one recovery advantage requires

```text
n = Omega(S).
```

Verdict:

```text
fits classification.
```

This separates source-side saturation from latency.  A horizon-class
channel needs both saturation and a fast-recovery mechanism.

## Case 3: collective charge pointer

Example:

```text
S source qubits;
microscopic source operators J_i = sigma_i^z, W_ij = delta_ij;
Q = sum_i sigma_i^z.
finite pointer controlled shift U = sum_q P_q \otimes V^q.
```

Classification:

```text
source-side saturation:
    yes, N_eff(W)=S;

record-label anonymity:
    yes, records contain no microscopic source address;

source permutation symmetry:
    yes, Q is permutation invariant;

unitary record formation:
    yes;

private-block recovery:
    no.
```

Reason:

Fresh pointers can redundantly record the collective charge `Q`.  The
public algebra is the commutative algebra of `Q`-sector projectors.
Inside a fixed charge sector, whose dimension is

```text
binomial(S,(S+q)/2),
```

all states produce the same record statistics forever.  The private
noncommuting block is invisible to this access channel.

Verdict:

```text
fits classification.
```

This kills the tempting shortcut

```text
saturation + anonymity + unitarity => mixing/routing.
```

Mixing remains an independent ingredient unless one adds a stronger
condition than anonymous saturated unitary coupling.

## Case 4: fast scrambler / stretched horizon / Hayden-Preskill

Example:

```text
finite horizon sector;
emission local to stretched-horizon degrees or a boundary layer;
internal dynamics scrambles in t_scr ~ beta log S;
post-Page/HP side information available.
```

Classification:

```text
source-local emission:
    can be treated as yes in a stretched-horizon description;

finite LR velocity in ordinary geometry:
    no, not in the relevant source graph;

fast private recovery:
    yes after scrambling and HP side information.
```

Mechanism:

```text
branch 1: fast internal routing/scrambling.
```

Latency floor:

```text
T_rec ~ t_scr + O(k + log(1/epsilon)) records/time units
```

after the relevant Page/HP side-information condition.

Verdict:

```text
fits classification.
```

The theorem does not say fast recovery is impossible.  It says fast
recovery requires evading the finite-velocity source-local bottleneck.
Fast scrambling is exactly that escape.

## Case 5: nonlocal anonymous encoder

Example:

```text
dense global encoder G acts on the full source sector before emission;
emitted records hide the microscopic source address by permutation
covariance;
record operators have global Heisenberg pullbacks.
```

Classification:

```text
source-local emission:
    no;

fast private recovery:
    possible;

fast internal routing forced:
    no.
```

Mechanism:

```text
branch 2: nonlocal access.
```

Verdict:

```text
fits classification.
```

This witness prevents the false inference:

```text
anonymity + fast recovery -> scrambling.
```

The correct inference needs source-locality.

## Case 6: holography of information / Gauss-law dressing

Example:

```text
gravitational or gauge constraints make the exterior algebra
nonfactorizing;
asymptotic/dressed observables may contain information that is not
available in a naive factorized bulk-local algebra.
```

Classification:

```text
source-local emission in factorized bulk variables:
    no, or at least not the complete allowed access algebra;

fast private recovery:
    possible in principle, depending on allowed dressed algebra and
    complexity;

fast internal routing forced:
    no.
```

Mechanism:

```text
branch 2: dressed/nonlocal access.
```

Verdict:

```text
sorted, with a scope warning.
```

The theorem treats this as a different access algebra, not as a
counterexample to source-local propagation.  The classification therefore
matches the conceptual split between HP scrambling and Raju-style
holography of information:

```text
HP/stretched horizon:
    fast routing branch;

holography of information:
    dressed-access branch.
```

Open issue:

```text
complexity and operational implementability of the dressed observable
must be specified.  Algebraic availability is not the same as feasible
decoding.
```

## Case 7: AdS boundary reconstruction

Example:

```text
bulk information reconstructed from the boundary CFT;
boundary dynamics may be local in boundary variables;
bulk operators are encoded nonlocally in boundary degrees.
```

Classification from bulk-source viewpoint:

```text
source-local emission/access in bulk variables:
    no;

access algebra:
    boundary/nonlocal code algebra;

fast private recovery:
    possible, subject to entanglement wedge, time, and complexity
    conditions.
```

Mechanism:

```text
branch 2 from the bulk viewpoint.
```

Classification from boundary viewpoint:

```text
the boundary theory has its own locality and its own LR/chaos bounds;
the theorem can be reapplied there with boundary source-locality.
```

Verdict:

```text
sorted, but viewpoint-dependent.
```

This is acceptable because source-locality is a statement about a chosen
factorization and access map.  Holography changes that map.

## Case 8: Rindler wedge

Example:

```text
Minkowski vacuum restricted to a Rindler wedge;
thermal modular state for wedge observer;
no finite black-hole entropy without cutoff/gravity;
no Page/HP evaporation channel.
```

Classification:

```text
thermality:
    yes;

finite horizon-class sector:
    no, unless regulated and supplemented;

location-uniform private recovery law:
    no finite-sector HP analogue.
```

Mechanism:

```text
not in the full horizon-class profile.
```

Verdict:

```text
sorted as a thermality-only witness.
```

Rindler shows why thermality is not enough.  It supplies a
quantum/classical or observer-algebra lesson, but not the finite-sector
private recovery structure by itself.

## Case 9: BTZ / AdS3 black holes

Example:

```text
finite-temperature state in a 2d CFT dual to BTZ;
bulk black-hole exterior;
boundary reconstruction and CFT dynamics available.
```

Classification:

```text
finite horizon sector:
    yes in the holographic/large-c sense;

public center:
    mass/angular momentum/temperature data;

private blocks:
    microstates / diary operators;

fast recovery:
    via boundary reconstruction and/or chaotic CFT dynamics;

source-local bulk emission:
    not the whole story, because boundary access is nonlocal from the
    bulk viewpoint.
```

Mechanism:

```text
mixed:
    branch 1 if emphasizing chaotic boundary/stretched-horizon
    scrambling;
    branch 2 if emphasizing boundary reconstruction as the access
    algebra.
```

Verdict:

```text
sorted, but not single-mechanism.
```

BTZ is useful because both mechanisms can appear depending on the
operational protocol.  This supports the classification: the branches
are mechanisms, not mutually exclusive ontologies.

## Current verdict

The classification survives the stress test.

```text
ordinary reservoir:
    slow because finite LR + source-local;

saturated slow router:
    saturated but slow, showing saturation != latency;

collective charge pointer:
    saturated, anonymous, symmetric, and unitary, but no private-block
    recovery, showing those predicates do not imply mixing;

fast scrambler / HP:
    branch 1;

nonlocal encoder:
    branch 2 witness;

Gauss-law / HoI:
    branch 2;

AdS boundary:
    branch 2 from bulk viewpoint, or branch 1 inside boundary dynamics;

Rindler:
    thermality-only, not finite horizon-class;

BTZ:
    mixed protocol-dependent horizon case.
```

This is enough to keep the theorem as a central result.  It does not
classify all of horizon physics, but it does classify the private
information-recovery mechanism.

## What this implies for the larger program

The horizon-interface theorem should be split:

```text
public layer:
    redundant records select a classical center;

private layer:
    source-local finite-velocity access cannot recover private blocks
    quickly;

fast-recovery layer:
    horizon-class systems use fast routing/scrambling or
    nonlocal/dressed access;

profile layer:
    compression, anonymity, source-side saturation, Page/HP recovery,
    and complexity discipline distinguish black holes from ordinary
    measurement channels.
```

This keeps the quantum/classical-transition idea without forcing the
gravity/geometry branch.

## Routing versus dressed-access diagnostic

The cheapest sharpening is the frozen-dynamics test:

```text
freeze internal source dynamics;
keep the record coupling near X;
ask whether a diary deposited far from X is still recoverable.
```

If recovery disappears, the original protocol used internal
routing/scrambling.  If recovery survives, the recovering algebra was
not generated by source-local emission in the factorized variables, or
the supplied side information already contained the diary.  This turns
the branch distinction into an operational diagnostic rather than a
word-choice about the same model.

For AdS/BTZ this is the relevant viewpoint test.  Bulk-factorized
source-local access fails when bulk routing is frozen; boundary or
dressed access can survive because it is nonlocal relative to the bulk
factorization.

## Deferred public-side stability

The qualitative public-side theorem is imported from no-broadcasting,
Quantum Darwinism, and SBS:

```text
many redundant stable records
=> approximately commuting public algebra
=> effective center/block decomposition.
```

The deferred public-side target is quantitative stability:

```text
given an approximate objectivity criterion,
how close is the selected public algebra to commuting,
and how large is the center/block leakage?
```

This pairs with the access-latency classification:

```text
public center:
    why coarse data become classical;

private latency classification:
    why fine quantum data require scrambling or dressed access.
```

Together these support the constrained-access horizon-interface theorem.
For this draft, however, the public side is a standard objectivity input.
The active result-facing target remains the private complement: which
access channels erase it, delay it, scramble it into recoverability, or
expose it through nonlocal/dressed algebras.

## Next result-facing target

The structural protected-versus-mixed result is now in the TeX draft.
The right language is the interaction algebra and its commutant:

```text
A_int:
    system algebra generated by the operators that couple to the record;

A_int':
    commutant/noiseless algebra invisible to those records.
```

Noiseless-subsystem theory says that persistent private blocks are the
commutant factors of the record-generating algebra.  The collective
charge pointer is the abelian extreme: functions of Q are public, while
the whole fixed-Q sector lies in the protected commutant.  Mixing is
forced structurally when the interaction algebra acts irreducibly on
each public block, leaving only the center in the commutant.

The next genuinely new question is deriving the rate: under
ETH/random-matrix or spectral-gap assumptions, how many records are
needed before the interaction algebra covers a private block well enough
that the commutant is effectively trivial?  In the TeX draft this is
isolated as an effective irreducibility rate `lambda`, with protected
component collapse after

```text
n >= lambda^{-1} log(C/epsilon).
```
