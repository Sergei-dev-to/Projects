# Demarcation: Where Gravity Stops and Quantum Begins

## Purpose and scope

An understanding note, not a paper and not a steering document. It records where
the demarcation inquiry lands once the von Neumann algebra language and the June
2026 literature audit are taken into account. It sits beside
`demarcation_synthesis.md` (the five-row map) and sharpens its row 3.

Question: which part of black-hole evaporation phenomenology is irreducibly
gravitational, versus forced by quantum mechanics, quantum field theory, or
quantum information?

```text
SCOPE WARNING. The clean version of this note is Schwarzschild + leading-order
semiclassical (G -> 0 / large N). Charges, rotation, near-extremal/JT, de Sitter,
and finite-N/non-perturbative effects each change the statement; they are treated
explicitly in their own sections rather than silently folded in. The earlier
draft of this note over-claimed "type II = gravity" by ignoring exactly these.
```

## The result: the seam is the algebra type -- but the types are a tower of approximations

The boundary is not "the factorization" as a tensor-product line. It is the
**type of the operator algebra of accessible observables**. There are three
regimes -- but, crucially, they are a *tower of approximations*, not a fixed
ladder.

```text
Type I     -- ordinary QM / quantum information; also the EXACT finite-N theory.
Type III_1 -- relativistic QFT; emergent in the strict large-N limit.
Type II    -- semiclassical gravity; the crossed product, leading order in G.
```

### Type I = quantum information (and the exact theory)

Factorized Hilbert space, density matrices, a trace, ordinary von Neumann
entropy. Everything QI supplies for free lives here:

```text
Page behavior; Hayden-Preskill recovery; decoupling; mirror operators.
```

All of it is type-I reasoning on an *assumed* tensor factor, and none of it is
gravity. Note also: the *exact, finite-N* black hole is itself type I -- a finite
`e^{S}`-dimensional system. Hold this; it is the correction the first draft missed.

### Type III_1 = quantum field theory (the key correction on the "quantum" side)

The local algebra of a QFT region is type III_1: no factorization between a region
and its complement, no density matrices, no finite entropy, Reeh-Schlieder
redundancy built in.

```text
The absence of a clean radiation/interior factor, the non-locality, and the
"same information in two places" redundancy are ALREADY forced by relativistic
QFT -- before gravity enters. Much of what felt gravitational about the
factorization problem is a quantum fact about fields.
```

Corollary, often confused: a graviton is a massless spin-2 QFT field, hence type
III_1 like any field. **Perturbative quantum gravity is "quantum," not "gravity,"
in this demarcation.** The gravitational content is non-perturbative.

### Type II = semiclassical gravity

Imposing the gravitational constraint -- equivalently, an observer with an
energy/clock plus gravitational dressing -- turns the type III_1 field algebra
into a **type II** algebra (the crossed product with modular flow; CLPW). Type II
restores a trace, hence a finite, renormalized, observer-relative entropy:

```text
S = A/4G + S_out      (generalized entropy, defined up to a constant).
```

The area term, the 1/4G, the finiteness, and the observer-relativity appear at
exactly this III_1 -> II step.

### The correction the first draft missed: the types are approximations

Type III_1 and type II are features of the `G -> 0` / large-N limit and its
first correction. The exact theory reverts to type I.

```text
exact, finite N:            type I    (finite e^{S} states)
strict N -> infinity:       type III_1 (Leutheusser-Liu, emergent)
+ gravity/observer, O(G):   type II   (CLPW crossed product)
+ 1/N = G corrections:      back toward type I
```

So "gravity = type II" is the *leading semiclassical* statement. The deeper
statement: the algebra *type itself* is a semiclassical artifact, and the genuine
gravitational invariant is the **finiteness** (the type-I dimension `e^{A/4G}`)
that the III/II structure approximates. This unifies the algebra seam with the
state-count residue below: finiteness *is* the state count.

### One-line demarcation (calibrated)

```text
Type I is the lab and the exact theory. Type III_1 is relativistic fields. The
trace-restoring crossed product (type II) is semiclassical gravity. The invariant
underneath all of it -- the finite e^{A/4G} state count -- is the gravitational
fact the algebra types are approximating.
```

### July 10 operational join: algebra plus temporal access

The algebra story identifies which radiation subsystem and trace are physically
meaningful; it does not show that the active emission process ever becomes
sensitive to a private diary. That second question must be phrased using the
time-ordered orbit of the physical jump or channel under the dynamics. This is
the representation-invariant join between the former "access rank" and
"scrambling" inputs.

An exact finite-energy parametric-pump control makes the distinction sharp. A
pump with `O(S)` energy can emit `O(S)` approximately thermal Hawking/partner
records while the total channel is the identity on an arbitrarily large
spectator diary. Energy flow, partner production, and thermal statistics
therefore do not establish diary flow. Gravity must supply both the radiation
algebra/instrument and a reason its temporal orbit becomes diary-visible;
ordinary quantum information then analyzes recovery conditional on those
supplied facts.

The shrinking-shell result ties this operational seam back to the state-count
and factorization seams. If the exterior algebra remains exactly diary blind
while the black-hole factor loses dimension, no hiding requires the lost
logical dimension to accumulate in a complementary partner/remnant algebra.
Without such an entropy-sized hidden archive, unitarity forces eventual
information into the exterior algebra. It does not select the Page-time
channel: an exact five-mode code shows that identical one-wavepacket thermal
states can carry zero diary information in one branch and complete diary
information in multi-time correlations in another.

The literature baseline already contains conditional Page/decoupling recovery,
Hawking channels, and the broad statement that thermality alone does not fix
information flow. The potentially distinctive result of this program is
therefore the assembled no-go boundary and the explicit diary-blind persistent
emitter, not another conditional Page theorem. See
`demarcation_scoop_audit_2026_07_10.md`.

## What gravity owns that the algebra story assumes but does not derive

The crossed product gives a trace and a finite "area + matter" entropy, but it
**assumes a spectrum and a state count**; it derives neither. The residue is
layered.

```text
1. The spectrum: S = A/4G and S(E) ~ E^2.
   Same relation for Schwarzschild (A/4G = 4 pi G M^2 ~ G E^2), two contents:
   - magnitude/geometry: the 1/4G normalization, area in Planck units;
   - spectral shape: S ~ E^2 => dS/dE ~ E => T ~ 1/E decreasing => NEGATIVE
     specific heat C < 0 -- the evaporation instability itself -- and Hawking-soft
     quanta (energy per active carrier ~ T ~ 1/E).
   The algebra story needs only "above Hagedorn" (dense, S ~ E). The black hole
   needs S ~ E^2 specifically; that extra growth (negative C) requires
   long-string/fractionation mechanisms (BFKS etc.) and is the most distinctively
   gravitational thermodynamic fact here. Partial tool exists; open for generic
   Schwarzschild.

2. Finiteness, self-averaging, and the ensemble -- one phenomenon.
   The exact type-I dimension e^{S}. This is the same fact as item 1's state
   count, seen from the algebra side: the semiclassical III/II tower is
   approximating a finite type-I system. The microscopic origin of that
   finiteness is the state-count problem.

   Sharpening (notes/self_averaging_variance.md): a finite type-I theory also
   SELF-AVERAGES. For a fixed chaotic Hamiltonian (full ETH), the radiation
   purity Tr rho_R^2 concentrates, SD/mean = O(e^{-S0/2}); the connected Wick
   pairings ARE the model's half-wormhole analogues, explicit and exponentially
   small. So at finite dimension three things arrive together: a genuine trace
   (type I), self-averaging (no ensemble), and no island-replica factorization
   puzzle. They dissolve TOGETHER into the semiclassical limit, where the trace
   goes relative (type II), wormholes appear, and gravity "computes an ensemble
   mean." Hence "why is the gravitational path integral an ensemble average?" is
   NOT a separate residue -- it is a facet of the exact->semiclassical
   transition (this item + the type tower). Finiteness, self-averaging, and
   factorization are the same gravitational fact seen three ways.

   Calibration: the self-averaging is shown at Renyi-2 (not von Neumann), for
   the island/PSSY factorization (not the spectral-form-factor version), in the
   bulk of evaporation (it fails at the small-S endpoint), and conditional on
   full-ETH genericity with uncorrelated records -- which is itself the open
   matrix-channel question, not an established fact.

3. The first law beyond S(E): J, Q, extremality.
   dM = T dS + Omega dJ + Phi dQ. Charges and rotation are gravitational content
   the S(E)-only story drops. Extremal limit: T -> 0 with S -> S_0 != 0; the
   entropy does not vanish. Near-extremal/JT: Schwarzschild's negative-C story is
   replaced by Schwarzian dynamics and log corrections, and -- importantly -- the
   type-II/algebra results are SHARPEST here. This is the regime the program
   itself flagged as the dangerous test; it is not covered by the Schwarzschild
   framing above.

4. The lived interior.
   The algebra story is an exterior/observer construction: it gives generalized
   entropy and the redundancy, not the infalling observer's smooth experience or
   the interior metric. State-dependence (Papadodimas-Raju), interior operators,
   firewalls, and the complexity bound on reconstruction (Harlow-Hayden;
   complexity = volume/action makes the bound geometric) live past even the type
   II exterior algebra. No current tool -- including everything in this program --
   offers leverage. This is the one genuinely open gravitational problem.
```

## Regimes that change the statement

```text
de Sitter / cosmological horizons:
  CLPW give dS static patch -> type II_1, FINITE maximal entropy, and the
  observer-relativity is sharpest (no asymptotic boundary to anchor anything).
  "Where does gravity begin" is cleaner in dS than Schwarzschild. The program's
  dS/Gauss-law leg lives here. Not developed in this note.

Charged / rotating / near-extremal / JT:
  see residue item 3. Different spectrum, different dynamics, and the place the
  algebra machinery is most mature.

Finite N / non-perturbative:
  type I; the III/II tower is the approximation. See the correction above.
```

## The other "factorization": wormholes and the ensemble

Distinct from the tensor-factor seam, same word. Euclidean wormholes make
boundary correlators fail to factorize, suggesting the gravitational path integral
computes an *ensemble* average rather than a single dual theory. This is directly
relevant to the structural seam, because it asks whether the radiation and
interior algebras live in one Hilbert space at all, or only on average -- and it
is entangled with how islands/replica-wormholes deliver unitarity. Jevicki-Yoon's
discussion explicitly proposes using emergent factorization to address this
non-factorization puzzle. The first draft of this note missed the connection even
though the relevant paper was read.

```text
tensor-factor seam: does H_BH (x) H_rad exist? -> resolved into algebra type.
non-factorization puzzle: does a single gravity theory factorize, or only an
  ensemble? -> the QM half self-averages (residue 2), so it is localized to the
  exact->semiclassical transition, not a free-standing puzzle.
```

So this "other factorization" folds into residue item 2: a single finite
microscopic theory has no island-replica factorization puzzle (it self-averages;
notes/self_averaging_variance.md); the ensemble is an artifact of the same
semiclassical limit that produces the type II algebra and the wormholes. What
stays genuinely open is the gravity-side question -- why the semiclassical path
integral takes the ensemble form at all.

## What the literature audit established (June 2026)

The III_1 -> II crossing is the current frontier formalization and is being
realized microscopically.

```text
Type III_1 in QFT/gravity:
  CLPW crossed product; Witten "gravity and the crossed product";
  Leutheusser-Liu emergent type III_1 at large N.

Type III_1 from an explicit matrix model:
  Gesteau-Santilli, "Explicit large N von Neumann algebras from matrix models"
  (2402.10262) -- type III_1 above the Hagedorn temperature (the black-hole
  regime).

Type II / generalized entropy:
  "Generalized black hole entropy is von Neumann entropy" (2309.15897);
  truncated-vs-full "algebra of accessible observables", Jevicki-Mukherjee-Yoon
  (2404.07862, PRD 2025); operator algebra for bulk regions from SYM, Jevicki
  group (JHEP01(2025)019).

Radiation subsystem + evaporation/Page in a matrix model:
  Gautam-Hanada-Jevicki-Peng, "Matrix Entanglement" (2204.06472), via partial
  deconfinement.
```

Calibrated verdict:

```text
The CONCEPTUAL move -- define a radiation algebra for an evaporating matrix black
hole and exhibit interior/radiation redundancy -- is taken, but at MECHANISM
level in TOY models (single-matrix collective field; partial deconfinement).

The rigor gap (a genuine vN algebra for accessible observables) and the realism
gap (N=4 SYM / BFSS instead of toy) are in progress, by the same incumbents.

NOT done: a rigorous + evaporating + realistic version combined. A wedge may
exist there, but it is a race against incumbents on their turf; whether it is a
real opening depends on speed and on collaborating rather than competing. The
earlier flat "scooped / no wedge" was over-compressed in the pessimistic
direction.
```

## Relation to the prior moment/channel framing

The detachment-operator second-moment program (`K_{ij}^{mn}`) was a
**type-I-shaped question**: it presupposed a clean radiation factor and asked
whether the channel was generic.

```text
Row 3 (factorization) = the algebra type. The seam.
Row 4 (channel second moment) = a type-I consistency check presupposing row 3.
```

It was premature before the audit (the factor was undefined). With the matrix-model
algebra now supplied by the incumbents, the numerics could become a *dynamical-
consistency check* on their construction: do the real-time dynamics fill the
kinematically-defined radiation algebra generically? Real but junior, and most
naturally pursued with one of those groups.

## Is there anything worth contributing?

```text
Construction (define the algebra, show redundancy, get the Page curve):
  taken (toy level). Owned by Hanada, Jevicki, Yoon, Gesteau, CLPW, Leutheusser-Liu.

Rigor + realism gaps:
  in progress by the same groups; a possible but contested opening, not a clear
  differential advantage.

Demarcation framing itself (algebra-type tower; what gravity must supply):
  clarifying pedagogy, not novel physics; a perspective chasing a moving target.

Dynamical-consistency check on the supplied algebra (row 4 repositioned):
  the only place the existing numerics still plug in; supporting role, ideally
  collaborative.

The interior (value of A/4G; S~E^2; lived geometry; complexity):
  the genuinely open gravitational problem, and the one place no current tool --
  here or elsewhere -- offers leverage. The only target worth a real bet, and it
  needs a new tool this program does not have.
```

Default conclusion: the understanding goal is met. No solo paper is warranted on
the construction. A real contribution exists only if (a) the dynamical-consistency
check is pursued in collaboration, or (b) the interior is attacked with a
genuinely new tool.

## Sources

- Gesteau-Santilli, Explicit large N von Neumann algebras from matrix models: https://arxiv.org/abs/2402.10262
- Jevicki-Mukherjee-Yoon, Emergent factorization of Hilbert space at large N and black hole: https://arxiv.org/abs/2404.07862
- Jevicki group, Operator algebra, entanglement, emergent geometry from matrix dof: https://link.springer.com/article/10.1007/JHEP01(2025)019
- Gautam-Hanada-Jevicki-Peng, Matrix Entanglement: https://arxiv.org/abs/2204.06472
- Generalized black hole entropy is von Neumann entropy: https://arxiv.org/abs/2309.15897
- Operator-algebraic approach to black hole information (JHEP02(2025)207): https://link.springer.com/article/10.1007/JHEP02(2025)207
- Leutheusser-Liu, emergent type III_1 / half-sided modular: search "Leutheusser Liu emergent times causal structure holography"
- Chandrasekaran-Longo-Penington-Witten (CLPW), An algebra of observables for de Sitter space: https://arxiv.org/abs/2206.10780
