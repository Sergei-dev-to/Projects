# Recent 2025--2026 Evaporation-Model Overlap Review

## Purpose

Check whether recent arXiv work already contains the project we are trying to
build:

```text
a gravity-free quantum model whose own dynamics produces black-hole-like
thermodynamics, emission, shrinking active state count, and unitary radiation
information flow.
```

The answer is mixed. Several recent papers are close on individual pieces. I do
not see a paper in this batch that combines all of the ingredients we care
about in one autonomous Hamiltonian.

## Main Papers Read

| Paper | Main construction | Closest overlap | Main difference from our target |
|---|---|---|---|
| Jones, Altaie, Varcoe, 2603.17000 | Local transverse-field Ising chains with a dynamically shrinking system chain and growing environment chain. | Page curve from a shrinking subsystem; MPS simulation; local spin model. | The subsystem split is externally resized. The result warns that Page behavior can be mostly kinematic. |
| Alsing, 2601.09820 | Quantum-optical Gaussian evaporation model using beam splitters and squeezers. | Unitary evolution, approximate thermality, Page curve, early/late correlations. | Evaporation is an optical protocol with chosen optical elements and Gaussian structure, not a fixed sector Hamiltonian with DOS-ratio emission. |
| Abutaleb, 2601.05305 | Time-dependent Hamiltonian model with independent interior-radiation qubit pairings. | Explicit microscopic unitary evolution and Page-like information transfer. | Independent pair assumption and time-dependent pairing structure replace many-body core dynamics. |
| Alsing, 2501.00948 | SPDC-inspired "waterfall" model with black-hole pump depletion and partner-particle cascade. | Unitary evaporation, Page curve, total energy carried by radiation, Hamiltonian-inspired squeezed-state dynamics. | Strong optical analogy and phenomenological cascade; the active core state count and DOS-ratio thermality are not derived from a horizon-area many-body spectrum. |
| Akil et al., 2507.17031 | Repeated quantum-controlled unitaries generating superposed evaporation histories. | Unitary evaporation with coherent backreaction and recoverable final radiation state. | Repeated update map; no autonomous many-body Hamiltonian producing a thermal emission law. |
| Ballav, Tai, Wen, 2511.14350 | Four-qubit circuit with controlled causal leakage. | Tracks entropy, mutual information, negativity. | Very small circuit model of information leakage; not a thermodynamic evaporator. |
| Basu et al., 2510.18967 | Stabilizer complexity of Hawking radiation in gravitational and toy evaporation models. | Useful diagnostics beyond entropy; dynamical evaporation toy models. | Complexity diagnostic paper, not a construction of the full evaporation phenomenology we want. |
| Gil, 2602.18503 | Population/coherence decomposition of purity in Page-type models. | Late-time purification can be coherence-dominated even when populations remain nearly uniform. | No explicit Hamiltonian; energy-free Page-type varying-dimension model. |
| Arias, 2605.19725 | Microcanonical energy sharing and capacity of entanglement. | DOS/energy-sharing logic close to our thermodynamic reduction; capacity has a Page-like single-hump curve. | Thermodynamic typicality mechanism, not a dynamical evaporation Hamiltonian. |

## What These Papers Already Cover

### Page behavior from shrinking Hilbert space

Jones--Altaie--Varcoe is the strongest warning for us. They show that a Page
curve can arise robustly from controlled subsystem resizing, even when explicit
Hamiltonian coupling across the system/environment boundary is removed. This
means a Page curve by itself is weak evidence. In our language, shrinking active
state count must be tied to emission, energy flow, thermality, and scrambling
controls.

### Unitary evaporation protocols

Alsing 2025, Alsing 2026, Akil et al., Abutaleb, and Ballav et al. all show
unitary evaporation-like processes in different finite or effective quantum
models. It would be inaccurate to claim that unitary non-gravitational
evaporation models are missing from the literature.

### Approximate thermality

The optical papers explicitly care about approximate thermality. Their route is
through squeezed states, beam splitters, and optical analogies. Our route, if it
works, is different: a density-of-states ratio from an active core spectrum,

```text
Gamma(n, omega) ~ rho_rad(omega) |g(omega)|^2
                  exp[S_core(E_n - omega, n-1) - S_core(E_n, n)].
```

This is the thermality mechanism we should emphasize.

### Information diagnostics beyond entropy

Basu et al. is useful because it shows that modern discussions look beyond the
Page curve. Stabilizer complexity, Wigner negativity, mutual information, and
early/late correlations are fair diagnostics. Our draft should not present
radiation entropy alone as the information result.

Gil adds a related warning: in Page-type models, late-time recovery of purity can
be carried mainly by coherences rather than by visibly nonuniform populations.
This means a thermal-looking radiation population is compatible with information
return, provided the phase/coherence structure is measured.

### Thermodynamic typicality and energy sharing

Arias 2605.19725 is relevant to our analytic direction. It studies an
effectively additive bipartite system in the microcanonical ensemble and shows
that the capacity of entanglement is controlled by energy-sharing fluctuations.
The example is a Schwarzian "black-hole" sector coupled to a two-dimensional CFT
radiation sector. As the radiation sector grows at fixed total energy, the
capacity develops a Page-like single-hump profile.

This does not give a dynamical evaporation Hamiltonian, but it supports the idea
that microcanonical energy sharing and density-of-states data can generate
Page-like entanglement diagnostics without imposing an entropy curve by hand.

### Alsing's self-identified rate issue

The 2025 waterfall paper explicitly notes that its mass/energy loss does not
follow the Hawking rate law

```text
dM/dt ~ -1/M^2.
```

Instead, the reported behavior is approximately linear before Page time and
approximately exponential after Page time. This is important for us because our
rate/acceleration test is not cosmetic. A model can have unitarity, energy
bookkeeping, thermality, and Page behavior while still missing the Hawking
evaporation rate structure.

## What Still Looks Distinct

The strongest remaining target is:

```text
one fixed Hilbert space;
one time-independent H_total;
horizon-area qubits or another explicit active state count;
measured core/radiation split;
energy-conserving emission channels;
DOS-ratio thermal spectrum;
negative heat capacity and accelerating power;
scrambling controls;
early/late radiation correlations.
```

The recent papers approach this target from several sides, but each leaves out a
major piece:

```text
Jones: local Hamiltonian and Page curve, but externally resized subsystem.
Alsing: unitarity, thermality, Page curve, but optical protocol/squeezing model.
Abutaleb: explicit unitary Hamiltonian language, but independent pair dynamics.
Akil et al.: coherent evaporation histories, but repeated controlled unitaries.
Ballav et al.: information-flow circuit, but very small/non-thermodynamic.
Basu et al.: advanced radiation diagnostics, but diagnostic focus.
```

## Consequences for Our Paper

### 1. The novelty cannot be "a Page curve"

That space is occupied. The Page curve is still necessary, but it must be one
diagnostic among several.

### 2. The central claim should be the package

The paper should claim a package of properties only when the calculation
supports all of them:

```text
shrinking active state count;
area-like entropy count;
energy-defined mass;
DOS-ratio thermality;
negative heat capacity;
accelerating emission;
scrambling dependence;
unitary early/late radiation correlations.
```

### 3. The strongest comparison is against Jones and Alsing

Jones forces us to separate kinematic Page behavior from dynamical emission.
Alsing forces us to be precise about thermality and energy conservation, because
those are already explicit goals in the optical models.

### 4. The autonomous-parent angle remains valuable

The literature includes repeated maps, shrinking subsystem protocols,
time-dependent pair Hamiltonians, and optical element sequences. A fixed
time-independent Hamiltonian that realizes the evaporation package would still
be a stronger result.

## Current Positioning

A fair positioning sentence would be:

```text
Recent models show that Page-like information recovery, unitary evaporation
maps, and approximate thermal radiation can each be realized in quantum
systems. Here we ask whether these features, together with negative heat
capacity and an area-like active state count, can arise from a single
autonomous non-gravitational Hamiltonian.
```

This is a narrower claim than "no one has modeled black-hole evaporation
without gravity." It is still an interesting claim if the autonomous-parent
calculation works.

## Sources

- Jones, Altaie, Varcoe, "Kinematic Emergence of the Page Curve in a Local
  Transverse-Field Ising Model", arXiv:2603.17000.
- Alsing, "Quantum Optical Inspired Models for Unitary Black Hole Evaporation",
  arXiv:2601.09820.
- Abutaleb, "Microscopic Unitarity and the Quantization of Black Hole
  Evaporation Time", arXiv:2601.05305.
- Alsing, "Black Hole Waterfall: a unitary phenomenological model for black
  hole evaporation with Page curve", arXiv:2501.00948.
- Akil et al., "A Quantum Superposition of Black Hole Evaporation Histories:
  Recovering Unitarity", arXiv:2507.17031.
- Ballav, Tai, Wen, "Quantum Circuit Model of Black Hole Evaporation with
  Controlled Causal Leakage", arXiv:2511.14350.
- Basu et al., "On the stabilizer complexity of Hawking radiation",
  arXiv:2510.18967.
- Gil, "Population-coherence routes to purity in Page-type models of
  black-hole evaporation", arXiv:2602.18503.
- Arias, "Microcanonical Energy Sharing and a Page-like Curve for the Capacity
  of Entanglement", arXiv:2605.19725.
