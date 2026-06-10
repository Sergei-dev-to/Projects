# Step 3 Natural-Core Probe Results

## Question

Can a standard finite many-body Hamiltonian supply the convex
microcanonical entropy window that Step 2 currently imposes by hand?

The decision criterion is deliberately conservative:

```text
positive beta
positive S''(E)
several adjacent occupied bins
survival under multiple histogram resolutions
```

This is still only a thermodynamic density-of-states test. It is not yet a
unitary evaporator.

## Probe 1: long-range spin core

Script:

```text
sim/scan_natural_core_dos.py
```

Model:

```text
long-range transverse-field Ising-like spin system
N = 10
alpha in {0, 0.5, 1, 2}
Jz in {0.5, 1, 2}
hx in {0.2, 0.5, 1}
weak z-disorder
```

Output:

```text
sim/data/natural_core_spin_scan.csv
sim/data/natural_core_spin_scan.npz
```

Result:

```text
No robust convex window was found.
```

The scan finds isolated one-bin or binning-dependent positive-curvature
patches, but the best cases do not survive the 16/20/24 bin comparison. This
is exactly the failure mode we wanted the diagnostic to catch.

Interpretation:

```text
The simple long-range spin core is not presently a good Step 3 candidate.
```

This does not rule out more specialized long-range spin models, larger sizes,
or models closer to known first-order microcanonical transitions. It does mean
the cheap spin route did not give us a clean natural core.

## Probe 2: attractive Bose-Hubbard core

Script:

```text
sim/scan_bose_hubbard_dos.py
```

Model family:

```text
fixed-particle Bose-Hubbard systems
ring and weakly coupled dimer geometries
attractive onsite interaction U < 0
optional attractive nearest-neighbor interaction V < 0
small disorder to break exact degeneracies
```

General scan:

```text
sites L in {4, 6}
particles N in {6, 8}
geometries in {ring, dimers}
J in {0.2, 0.5, 1.0}
U in {-0.5, -1.0, -2.0, -4.0}
V in {0.0, -0.2}
bins in {16, 20, 24}
```

Output:

```text
sim/data/natural_core_bose_hubbard_scan.csv
sim/data/natural_core_bose_hubbard_scan.npz
```

The first scan found two all-binning candidates:

```text
L=6, N=6, ring, J=0.5, U=-1, V=-0.2
  passes 16/20/24 bins

L=6, N=8, dimers, J=1, U=-0.5, V=0
  passes 16/20/24 bins
```

Focused scan:

```text
L = 6
N in {6, 8}
geometries in {ring, dimers}
J in {0.5, 1.0}
U in {-0.5, -1.0}
V in {0.0, -0.2}
bins in {14, 16, 18, 20, 22, 24, 28, 32}
seeds 2468 and 1357
```

Output:

```text
sim/data/natural_core_bose_hubbard_focus_seed2468.csv
sim/data/natural_core_bose_hubbard_focus_seed2468.npz
sim/data/natural_core_bose_hubbard_focus_seed1357.csv
sim/data/natural_core_bose_hubbard_focus_seed1357.npz
step3_natural_core_probe.pdf
```

Best focused candidate:

```text
L=6, N=8, ring, J=0.5, U=-1, V=-0.2
```

Seed 2468:

```text
passes 6/8 bin choices
mean convex bins = 3.12
common energy-window overlap = 0.326
```

Seed 1357:

```text
passes 6/8 bin choices
mean convex bins = 3.12
common energy-window overlap = 1.303
```

This is the first Step 3 probe that looks genuinely worth pushing. The signal
is not perfect, but it survives more than a single cherry-picked binning and is
stable across two disorder seeds.

## Current verdict

The long-range spin route is weak.

The attractive Bose-Hubbard route is promising enough for the next test:

```text
attach the existing radiation-bin collision Hamiltonian to the best
Bose-Hubbard core and ask whether the convex DOS window actually produces
accelerating emission.
```

That is the real Step 3 test. A convex DOS window by itself is not enough; it
must remain visible once the core is coupled to outgoing modes.

## Immediate next checks

Before claiming more than "promising candidate", do three things:

```text
1. Recompute the DOS diagnostic with an alternate estimator
   such as kernel smoothing or cumulative-state smoothing.

2. Check the best candidate at nearby sizes, especially L=6, N=7/9 or
   L=5/6 with nearby particle counts, if exact diagonalization remains cheap.

3. Build an energy-lowering emission operator for the Bose-Hubbard core and
   run the reduced-density collision evolution.
```

If check 3 fails, the result is still useful:

```text
natural convex DOS exists, but coupling it to radiation without dark-state
or selection-rule failures is the hard part.
```

## Dynamical emission probe update

Script:

```text
sim/bose_hubbard_emission_markov.py
```

Diagnostic figure:

```text
step3_bose_hubbard_emission_probe.pdf
```

Scan output:

```text
sim/data/bose_hubbard_emission_markov.npz
sim/data/bose_hubbard_emission_markov_scan.csv
```

Method:

```text
Use the best Bose-Hubbard DOS candidate.
Diagonalize H_core.
Use local density and hopping operators as system-bath couplings.
Keep only energy-lowering transitions in the energy eigenbasis.
Evolve populations with a trace-preserving weak-coupling Markov map.
```

This is not yet the full collision-Hamiltonian model. It is the cheap
screening test for whether the natural core plus physical local couplings
actually produces the desired emission schedule.

Default run:

```text
L=6, N=8 ring
J=0.5, U=-1, V=-0.2
operator mode = density + hopping
initial energy window = [-18.5, -17.0]
max emitted gap = 2.0
```

Result:

```text
initial energy = -17.6681
final energy = -18.3937
early emitted power = 0.009812
middle emitted power = 0.009121
late emitted power = 0.008305
mid / early = 0.930
```

So the first dynamical probe emits, but it decelerates.

Focused scan:

```text
operator modes = density, hopping, both
max emitted gap = 0.5, 1, 2, 4, 8
initial windows = [-18.5,-17], [-19,-17], [-20,-18],
                  [-21,-19], [-22,-20]
seeds = 2468, 1357
```

Main outcome:

```text
Most local-coupling runs decelerate.
```

The only meaningful acceleration found is narrow:

```text
hopping operator only
initial window [-21, -19]
max emitted gap = 2
seed 2468: mid / early = 1.126
seed 1357: mid / early = 1.077
```

This is not strong enough to call a natural evaporator. It is a small
parameter-pocket effect, not the robust black-hole-like schedule we wanted.

Interpretation:

```text
The convex DOS window is not sufficient.
The coupling matrix elements matter.
```

A natural core can have a plausible convex intruder and still fail to evaporate
like the engineered shell model when coupled through ordinary local operators.
That is a useful obstruction: Step 3 is not just "find negative heat capacity";
it is "find negative heat capacity plus emission operators whose matrix
elements sample the growing final-state phase space in the right way."

Democratic spectral-coupling control:

```text
Rates depending only on available lower-energy states and gap size were also
tested informally.
```

They also did not give a strong acceleration signal in the target window. This
suggests that the binned convexity is either too weak/finite-size-sensitive for
the dynamical purpose, or that the relevant emission observable has to be more
carefully matched to the microcanonical structure.

Updated Step 3 verdict:

```text
Bose-Hubbard remains interesting, but it is no longer an easy win.
The natural-core problem has split into two requirements:

1. convex microcanonical entropy;
2. compatible energy-lowering matrix elements.
```

For the paper, this supports a conservative statement:

```text
The engineered shell model isolates the mechanism. Replacing it by a natural
many-body Hamiltonian is nontrivial, because a natural convex DOS alone does
not guarantee a black-hole-like emission schedule.
```

## Variable-N particle-loss update

The fixed-N failure was not the end of the Bose-Hubbard route. It exposed a
conceptual mismatch: black holes shrink, while the fixed-N probe only relaxed
inside one Hilbert-space sector.

The next test used sectors:

```text
H_core = H_8 direct_sum H_7 direct_sum H_6 direct_sum H_5 direct_sum H_4 direct_sum H_3
```

with particle-loss emission operators:

```text
b_i : H_N -> H_{N-1}
```

Detailed note:

```text
notes/variable_n_bose_hubbard_results.md
```

Script and figure:

```text
sim/variable_n_bose_hubbard_evaporation.py
step3_variable_n_bose_hubbard.pdf
```

Main result:

```text
variable-N particle loss does produce robust accelerating emission
in several scan regions.
```

Best grouped case across two seeds:

```text
mu = 6
max emitted gap = 4
initial N=8 internal-energy window = [-18.5, -17]

seed 2468: mid / early emitted power = 1.359
seed 2469: mid / early emitted power = 1.362
```

Mean over those two seeds:

```text
early emitted power  = 0.0525
middle emitted power = 0.0714
late emitted power   = 0.0756
final mean N         = 5.61
```

This changes the status of Step 3. The correct lesson is now sharper:

```text
fixed-N convex DOS is insufficient;
shrinking sectors plus particle-loss operators can recover the desired
accelerating schedule.
```

Still, this is a weak-coupling population diagnostic, not a full unitary
collision model. The next serious test is to build the reduced-density
collision version for the same variable-N sectors.

## Secular Kraus update

The reduced-density version has now been run in a secular Kraus formulation.

See:

```text
notes/variable_n_kraus_results.md
step3_variable_n_kraus.pdf
```

For the same best parameter point:

```text
mu = 6
max emitted gap = 4
initial N=8 window = [-18.5, -17]
```

the acceleration survives:

```text
seed 2468: mid / early = 1.364, peak S2(core) = 3.956
seed 2469: mid / early = 1.340, peak S2(core) = 3.848
```

The effective core dimension shrinks from 1287 to roughly 480-490, and the
core Renyi-2 entropy grows. Since this is a reduced-density channel purified
by emitted bins, the core entropy is the entropy of all radiation, though not
an early/late radiation diagnostic.
