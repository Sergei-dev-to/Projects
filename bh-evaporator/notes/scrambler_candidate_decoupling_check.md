# Scrambler Candidate Decoupling Check

## Question

Can one or two concrete deterministic choices of `H_mix` be connected to the
decoupling condition needed by the evaporator, using known scrambling
literature rather than proving a full unitary-design theorem?

The target is:

```text
early:
  I(Q:R) small, or ||rho_QR - rho_Q tensor rho_R||_1 small;

late:
  I(Q:B) small, or ||rho_QB - rho_Q tensor rho_B||_1 small.
```

`Q` purifies the code subspace, `R` is the emitted radiation, and `B` is the
remaining core.  This is the Hayden-Preskill/decoupling target.  Approximate
2-design behavior is sufficient, but not necessary.

The literature bridge we can use is:

```text
operator growth / OTOC decay
  -> channel mutual-information scrambling
  -> Hayden-Preskill-style decoupling/recovery.
```

The important references for the bridge are Hosur-Qi-Roberts-Yoshida and
Yoshida-Kitaev.  The former relates OTOC decay in a unitary channel to small
mutual information between input subsystems and most output partitions.  The
latter uses OTOC decay as the condition that guarantees faithful
Hayden-Preskill recovery.

## Time-Scale Tweak

The candidate `H_mix` should not be required to randomize the core before every
single emitted quantum.  For a Schwarzschild black hole,

```text
t_emit ~ M,
t_scr  ~ M log M.
```

So one scrambling time contains `O(log M)` emitted quanta, while the Page time
contains parametrically many scrambling times:

```text
t_Page / t_scr ~ M^2 / log M.
```

The right coarse statement is therefore:

```text
over each scrambling block, the core dynamics spreads local code information
over O(A) active degrees of freedom before Page's theorem or decoupling is
applied at the coarse trajectory level.
```

This is enough for the Page/island entropy calculation, which is a coarse
entropy-flow statement.  It is also the natural setting for Hayden-Preskill
recovery, where the retrieval delay is of order the scrambling time plus a
small amount of extra radiation.

## Candidate 1: Expander-Graph Spin Hamiltonian

### Hamiltonian

Use `N_A(E) ~ A(E)` core degrees of freedom in each area sector.  On that set,
choose a deterministic bounded-degree expander graph `G_A` and define

```text
K_A =
  P_A [
    sum_{(ij) in G_A}
      (J_x X_i X_j + J_y Y_i Y_j + J_z Z_i Z_j)
    + sum_i (h_x X_i + h_z Z_i)
  ] P_A.
```

Here `P_A` projects to the active microcanonical/area sector.  The generic
noncommuting couplings and fields are included to avoid integrable or
symmetry-protected dynamics inside the sector.

### What is known

Barbon and Magan propose local quantum systems on expander graphs as models of
horizon thermalization.  The key structural point is that bounded degree plus
expander connectivity gives logarithmic graph diameter and rapid mixing without
a complete graph.

Bentsen, Gu, and Lucas analyze fast scrambling on sparse graphs.  Their result
is directly relevant in spirit: sparse connectivity can still support
logarithmic scrambling, and graph geometry controls operator growth and OTOC
spreading.

### Match to our decoupling target

The expander route gives the cleanest chain:

```text
bounded-degree expander geometry
  -> operator support reaches O(A) sites in O(log A) graph time
  -> OTOCs between initially local operators and most output partitions decay
  -> channel mutual information between the input code and wrong output
     partitions becomes small
  -> Page-level decoupling and Hayden-Preskill-style recovery.
```

The match is good because the candidate graph is area-sized, the emission
channels are also area-sized, and the expander geometry is a known way to model
horizon-like fast scrambling without complete all-to-all coupling.

### What remains unproved

The known expander/sparse-graph results do not by themselves prove the exact
bound

```text
I(Q:B) << 1
```

for the composed evaporation map after Page time.  They give the operator
growth/OTOC part of the bridge.  The remaining step is to turn that scrambling
diagnostic into the specific reference-core/reference-radiation decoupling
bound for the evaporation code subspace.

### Failure modes

The candidate can fail if:

```text
1. the chosen Hamiltonian has extra conserved quantities inside the area sector;
2. operator growth is fast but does not give sufficiently uniform mixing over
   the emitted channel labels;
3. the code subspace is too large for the available decoupling margin;
4. the emission process samples only a small fixed subset of graph sites rather
   than the area-sized active set.
```

The fourth failure mode is avoidable: emission should be written as an
inclusive sum over area channels, with no preferred contact site.

### Assessment

This is the strongest candidate among the two checked here.  It gets the hard
part into a standard form:

```text
prove or cite OTOC/operator-growth scrambling for a nonintegrable Hamiltonian
on an expander, then apply channel-scrambling/decoupling logic to the
evaporation code subspace.
```

This gives a concrete research route.

## Candidate 2: Treelike / Power-of-Two Coupling Hamiltonian

### Hamiltonian

Use deterministic nonlocal couplings whose range is a power of two:

```text
K_A =
  P_A [
    sum_i sum_{m=0}^{log N_A}
      J_m O_i O_{i+2^m}
    + local noncommuting fields
  ] P_A.
```

This is the structure studied in the treelike-interaction cold-atom model.
The effective geometry can be tuned from a line to an ultrametric/tree-like
geometry.

### What is known

Bentsen et al. propose an experimentally motivated deterministic spin model
with non-random power-of-two couplings.  In the treelike regime they find
exponentially fast spreading of quantum information and enhanced entanglement
growth.

This is useful because it gives a concrete, non-random interaction pattern.
It is less arbitrary than choosing a random sparse graph.

### Match to our decoupling target

The route is:

```text
power-of-two deterministic couplings
  -> treelike effective geometry
  -> exponential information spreading / fast entanglement growth
  -> candidate OTOC decay or channel scrambling
  -> decoupling along the evaporation channel.
```

The first three arrows are well aligned with the literature.  The last two are
less directly established than in the expander route, because the cited
treelike work emphasizes spreading and entanglement dynamics more than a direct
channel mutual-information theorem.

### What remains unproved

For our purpose, the missing statement is:

```text
the treelike Hamiltonian makes I(Q:B) and I(Q:R) obey the same Page-time
decoupling thresholds as the random-isometry calculation.
```

The literature gives a plausible dynamical mechanism.  It does not give the
evaporation-channel decoupling bound.

### Failure modes

The candidate can fail if:

```text
1. the treelike geometry spreads information quickly but unevenly;
2. the emitted area channels couple in a way that samples the tree
   nonuniformly;
3. the ultrametric structure leaves distinguishable large-scale sectors;
4. the fast entanglement-growth regime is parameter-sensitive.
```

These are more serious than for the expander graph because an expander is
designed to suppress bottlenecks, while a tree-like geometry can have
hierarchical structure that may survive in correlations.

### Assessment

This is the better concrete deterministic Hamiltonian if we want an
experimentally motivated coupling pattern.  It is the weaker candidate if the
goal is to connect immediately to decoupling proofs.

## Comparison

```text
criterion                         expander H_mix        treelike H_mix
---------------------------------------------------------------------------
deterministic possible             yes                   yes
bounded degree / sparse             yes                   yes
known fast scrambling motivation    strong                strong
direct graph mixing intuition       very strong           medium
OTOC/operator-growth route          strong                medium/strong
decoupling theorem off the shelf    no                    no
obvious bottleneck risk             low                   medium
emission-channel match              strong                medium
best use                            main candidate        concrete backup
```

## What We Can Tweak

The main tweak is to state the `H_mix` requirement as a decoupling condition
and then use OTOC/operator-growth literature as a route toward it.

Replace the stronger requirement

```text
K_A generates a full approximate unitary design on H_A.
```

with the direct information-theoretic requirement

```text
the composed emission channel decouples the reference from the wrong subsystem
on the code subspace being tested.
```

Then it can state:

```text
approximate 2-design behavior is sufficient;
OTOC/channel scrambling is the standard Hamiltonian diagnostic;
expander H_mix is the leading deterministic candidate;
treelike H_mix is a concrete deterministic backup.
```

## Bottom Line

For the hard deterministic-scrambler part, the expander Hamiltonian is the best
candidate to push first.  It has the cleanest match between area-sized degrees
of freedom, bounded-degree nonlocal connectivity, fast operator growth, and
uniform channel sampling.

The treelike Hamiltonian is worth keeping because it is explicit and
physically motivated, but it is less obviously aligned with the decoupling
condition needed by the evaporation channel.

The remaining hard step is now sharply identified:

```text
expander or treelike Hamiltonian scrambling
  -> quantitative reference/core and reference/radiation decoupling for the
     composed evaporation channel.
```

That bridge is narrower than proving a full design theorem and is the right
place to use the existing channel-scrambling literature.
