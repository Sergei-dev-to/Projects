# Fixed Hamiltonian Property Check

## Purpose

We now have a candidate fixed shell mixer,

```tex
K_N
=
\sum_{(ij)\in G_N}
\left(J_xX_iX_j+J_yY_iY_j+J_zZ_iZ_j\right)
+\sum_i(h_xX_i+h_z(i)Z_i),
```

with `G_N` a deterministic bounded-degree expander.  This note checks what
properties of the candidate follow analytically from the construction, what is
supported by existing scrambling literature, and what remains a theorem target.

The goal is the evaporation decoupling condition, not a full global design.

## Property 0: Fixed Hamiltonian Status

This property passes.

Once `G_N`, the couplings, and the deterministic field pattern are chosen,
`K_N` is fixed.  The full Hamiltonian family is

```tex
H_{\rm tot}
=
H_B^{(0)}
+\bigoplus_E P_EK_{N(E)}P_E
+H_R
+H_I .
```

No unitary is resampled during evaporation.  Randomness may be used only as a
proof device if one proves existence by sampling a Hamiltonian once from an
ensemble.

## Property 1: No Obvious Slow Geometry

This property passes at the graph-theory level.

A bounded-degree expander has logarithmic diameter and no low-dimensional
geometric bottleneck.  This avoids the slow diffusion problem of a line,
surface lattice, or finite-dimensional local grid.  It supports a scrambling
time scaling

```tex
t_{\rm scr}\sim O(\log N)
```

in graph units, subject to the dynamics actually using the graph efficiently.

This is a graph-geometry statement.  It is not yet an OTOC theorem for the
spin Hamiltonian.

## Property 2: Nonintegrability Versus Boundary Homogeneity

This property is plausible by construction, but it competes with the cleanest
boundary-uniformity argument.

The terms

```tex
X_iX_j,\quad Y_iY_j,\quad Z_iZ_j,\quad X_i,\quad h_z(i)Z_i
```

with generic nonzero coefficients and a deterministic inhomogeneous field would
remove the most obvious symmetries:

```text
translation symmetry,
graph automorphism degeneracy,
total spin conservation,
simple Ising integrability.
```

However, arbitrary inhomogeneous fields also make boundary sites inequivalent.
That weakens the route from subsystem ETH to uniform boundary-channel weights.

For the bridge lemma, the better analytical choice is:

```text
use a homogeneous or symmetry-respecting Hamiltonian on a vertex-transitive
expander, then treat symmetry sectors explicitly.
```

This keeps

```tex
{\cal A}_\mu(E,\omega)
=
{\cal A}_\nu(E,\omega)
```

by symmetry for symmetry-related boundary operators.  Nonintegrability then has
to come from the graph/interactions and from working in the appropriate
symmetry sectors, rather than from arbitrary site disorder.

## Property 3: Fast Operator Spreading

This is the first nontrivial property.

The desired statement is:

```tex
{\rm local\ operator}\ O_i(t)
=
e^{iK_Nt}O_ie^{-iK_Nt}
```

has support on an order-one fraction of the `N` active degrees by time

```tex
t\sim c\log N.
```

The expander and sparse-graph literature supports this as the right
expectation.  Barbon-Magan use expander graphs as fast-scrambler geometries.
Bentsen-Gu-Lucas analyze how sparse nonlocal graph structure can support
logarithmic scrambling and operator growth.

What we can use:

```tex
{\rm expander/sparse\ graph}
\Rightarrow
{\rm plausible\ logarithmic\ operator\ growth}.
```

What we do not have:

```tex
K_N{\rm\ specifically}
\Rightarrow
\|[O_i(t),O_j]\|{\rm\ large/small\ in\ the\ needed\ averaged\ OTOC\ sense}
```

with a quantitative bound strong enough for decoupling.

## Property 4: Channel-Scrambling Bridge

This property is supplied by the literature once an OTOC/channel bound is
available.

Hosur-Qi-Roberts-Yoshida study unitary channels as states and show that generic
decay of out-of-time-order correlators implies small mutual information between
input subsystems and almost all output partitions.  Yoshida-Kitaev use OTOC
decay as the scrambling condition guaranteeing Hayden-Preskill recovery.

Thus this implication is usable:

```tex
{\rm averaged\ channel\ OTOC\ decay}
\Rightarrow
I(A:C)_{\rm channel}\ll1
```

for most output partitions `C`, and hence

```tex
{\rm decoupling}
\Rightarrow
{\rm recovery\ from\ the\ complementary\ subsystem}.
```

This bridge is not the bottleneck.

## Property 5: Boundary-Channel Sampling

This is the useful new structure specific to our model.

The radiation is created by area-many weak boundary channels:

```tex
H_I
=
\sum_{\mu=1}^{N(E)}
O_\mu b^\dagger_\mu+{\rm h.c.}.
```

A radiation history is a sampled sequence

```tex
\boldsymbol\mu=(\mu_1,\ldots,\mu_m)
```

with distribution `P_m` induced by the golden-rule rates.  The radiation
subsystem is therefore sampled from the boundary algebra; it is not a fixed
adversarial output region.

The right condition is:

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:R_{\boldsymbol\mu})
\le \epsilon_{\rm early}
```

before Page time, and

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:B_{\rm rem}(\boldsymbol\mu))
\le \epsilon_{\rm late}
```

after Page time.

If the emission distribution is close enough to the typical-partition measure
used in channel-scrambling results, then the "most output partitions" theorem
can be applied to the actual radiation histories.

This is the sharpest route to closure.

## Property 6: Uniformity Of Boundary Sampling

This is the second nontrivial property.

The inclusive rate is

```tex
{\cal A}(E,\omega)
=
\sum_{\mu=1}^{N(E)}
{\cal A}_\mu(E,\omega).
```

For boundary-channel sampling to mimic typical output partitions, the
shell-averaged channel weights should satisfy

```tex
{\cal A}_\mu(E,\omega)
\simeq {1\over N(E)}{\cal A}(E,\omega)
```

up to fluctuations small on the entropy scale.

This is not a separate rate law.  It is a uniformity condition on the boundary
operator algebra.  It is automatic if the boundary operators are
symmetry-related:

```tex
O_\mu=U_\mu O_0 U_\mu^\dagger,\qquad [U_\mu,K_N]=0.
```

Then `[U_mu,\Pi_E]=0`, and the microcanonical trace gives equal weights.  ETH is
still needed for the common smooth spectral envelope and for local thermality.

If the Hamiltonian is not exactly homogeneous, uniformity remains plausible if:

1. `K_N` mixes local boundary operators across the expander;
2. local boundary environments become asymptotically equivalent;
3. the microcanonical shell average obeys an ETH-like local-operator
   equivalence.

What remains to prove is an ETH/uniformity statement for the chosen
`P_EK_NP_E`.

## Property 7: Block Composition

The fixed-Hamiltonian property has to survive many blocks.

Let `M` be the number of coarse scrambling/emission blocks in the evaporation
window and let `epsilon_j` be the decoupling error of block `j` or of the
corresponding composed channel segment.  A conservative error budget is

```tex
\epsilon_{\rm total}
\lesssim
\sum_{j=1}^M\epsilon_j.
```

For Schwarzschild scaling, using block time `t_scr~M log M`, the number of
scrambling blocks over the evaporation is parametrically

```tex
M_{\rm blocks}\sim {M_0^2\over \log M_0}.
```

So a blockwise proof needs errors much smaller than `log M_0/M_0^2`.  A direct
argument for the composed channel would avoid this conservative union-bound
budget.

This suggests that the cleanest theorem target is the composed channel over a
macroscopic segment, not an overly local per-block statement.

## Literature Check: What We Can Actually Import

The useful literature split is now clear.

### The channel-scrambling implication is standard enough to use

Hosur, Qi, Roberts, and Yoshida, *Chaos in quantum channels*
(`arXiv:1511.04021`), treat a unitary time evolution as a quantum channel and
relate out-of-time-order correlator decay to information-theoretic scrambling.
The result we need is very close to their stated channel criterion:

```text
OTOC decay for the channel
    -> small mutual information between input subsystems and most output
       partitions.
```

Yoshida and Kitaev, *Efficient decoding for the Hayden-Preskill protocol*
(`arXiv:1710.03363`), use the same OTOC logic in the Hayden-Preskill setting:
OTOC decay is the scrambling condition that guarantees faithful recovery.

So this part is not where the model is weak.  If we can show that our fixed
Hamiltonian generates the relevant OTOC/channel scrambling, the decoupling and
recovery interpretation can be cited rather than rederived from scratch.

### Sparse and expander fast scrambling is strongly motivated

Lashkari, Stanford, Hastings, Osborne, and Hayden,
*Towards the fast scrambling conjecture* (`arXiv:1111.6580`), already use
sparse nonlocal models as examples of logarithmic scrambling, while also
explaining why such examples can fall short of an ideal black-hole scrambler.

Barbon and Magan, *Fast Scramblers, Horizons and Expander Graphs*
(`arXiv:1204.6435`), explicitly propose local quantum systems on expander
graphs as microscopic models for horizon thermalization.  This directly
supports using an expander as the interaction geometry.

Bentsen, Gu, and Lucas, *Fast scrambling on sparse graphs*
(`arXiv:1805.08215`), give the modern sparse-graph route: sparse connectivity
can support logarithmic scrambling, and operator growth is the right diagnostic.

Bentsen et al., *Treelike interactions and fast scrambling with cold atoms*
(`arXiv:1905.11430`), give a deterministic nonrandom interaction pattern with
fast spreading in a treelike regime.  This is a useful fallback if expander
Hamiltonians remain too hard to prove.

Belyansky et al., *Minimal Model for Fast Scrambling*
(`arXiv:2005.05362`), show that local chaotic dynamics plus a simple global
interaction can produce fast scrambling.  This is less close to our
boundary-cell expander picture, but it confirms that fast scrambling need not
come from Haar-random dynamics.

### What is still not supplied directly

I do not find an off-the-shelf result of the form

```tex
K_N =
\sum_{(ij)\in G_N}
(J_xX_iX_j+J_yY_iY_j+J_zZ_iZ_j)
+\sum_i(h_xX_i+h_z(i)Z_i)
\quad\Longrightarrow\quad
I_2(Q:X_{\rm wrong})\ll 1
```

for deterministic expander `G_N`, deterministic fields, and the evaporation
subsystems selected by the weak boundary emission channel.

The gap is not "fast scrambling exists"; the literature gives several
versions of that.  The missing statement is narrower:

```text
the actual emitted boundary-channel histories generated by H_I behave like
the typical output partitions appearing in channel-scrambling theorems.
```

That requires two ingredients:

1. An OTOC/operator-spreading estimate for the chosen fixed Hamiltonian, or a
   closely related deterministic sparse/treelike Hamiltonian.
2. A boundary-channel sampling statement:

   ```tex
   {\cal A}_\mu(E,\omega)
   \simeq
   {1\over N(E)}{\cal A}(E,\omega)
   ```

   in the microcanonical shell, so emitted channel labels sample the boundary
   algebra without repeatedly selecting special sites.

## Current Judgment

The fixed-Hamiltonian route is worth pushing, but it is not closed by citation
alone.  The best non-micro step is to formulate and prove a conditional lemma:

```text
If K_N has averaged channel OTOC decay on time O(log N), and if H_I samples
boundary channels with microcanonical weights close to uniform, then the
composed evaporation map satisfies the Page decoupling conditions.
```

The first hypothesis is tied to the sparse/expander fast-scrambling literature.
The second is specific to our evaporation Hamiltonian.  Proving that second
condition, or replacing it with a standard ETH-style boundary-operator
equivalence, is the most project-specific remaining analytical task.

## Current Pass/Fail Table

| Property | Status | Reason |
|---|---|---|
| Fixed Hamiltonian | Pass | Graph/couplings fixed once. |
| Sparse fast geometry | Pass at graph level | Expander removes low-dimensional diffusion bottlenecks. |
| Nonintegrability | Plausible | Prefer homogeneous chaotic dynamics plus explicit symmetry-sector treatment; inhomogeneous fields are a fallback with an added uniformity burden. |
| Fast operator spreading | Supported, not closed | Literature supports expander/sparse fast scrambling; no bound for this `K_N`. |
| OTOC to channel decoupling | Pass if OTOC bound supplied | This is the Hosur-Qi-Roberts-Yoshida/Yoshida-Kitaev bridge. |
| Boundary-channel sampling | Promising | Radiation histories are sampled boundary probes, not fixed regions. |
| Sampling uniformity | Open | Needs ETH-like equivalence of boundary emission channels. |
| Many-block composition | Open | Need an error budget or a composed-channel theorem. |

## What Would Close The Fixed-Hamiltonian Route

The strongest useful theorem would be:

```tex
{\bf Theorem\ target.}
```

For the deterministic expander Hamiltonian `K_N`, after time
`t >= c log N`, the block or composed channel satisfies

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:R_{\boldsymbol\mu})
\le \epsilon_{\rm early}(N,d,m),
```

and, after Page time,

```tex
\mathbb E_{\boldsymbol\mu\sim P_m}
I_2(Q:B_{\rm rem}(\boldsymbol\mu))
\le \epsilon_{\rm late}(N,d,m),
```

with errors small compared with the entropy-scale Page separation.

A sufficient proof can be split into two lemmas:

```tex
{\rm OTOC/channel\ scrambling\ lemma}
```

for `K_N`, and

```tex
{\rm boundary\ sampling\ uniformity\ lemma}
```

for the emission operators under shell averaging.

## Near-Term Conclusion

The fixed Hamiltonian candidate survives the first analytical check.  It is a
real candidate, not merely a placeholder.  The graph geometry and Hamiltonian
form are aligned with known fast-scrambling routes, and the radiation sampling
structure makes the required partition less adversarial than an arbitrary
output cut.

The route is still not closed.  The two live problems are:

```tex
K_N\to{\rm OTOC/channel\ scrambling}
```

and

```tex
H_I{\rm\ samples\ typical\ boundary\ partitions}.
```

If either one fails, the deterministic expander mixer does not give Result 2.
If both hold, the abstract shell-mixing condition is replaced by a concrete
fixed Hamiltonian.

## Sources

- Hosur, Qi, Roberts, Yoshida, "Chaos in quantum channels,"
  arXiv:1511.04021.
- Yoshida, Kitaev, "Efficient decoding for the Hayden-Preskill protocol,"
  arXiv:1710.03363.
- Barbon, Magan, "Fast Scramblers, Horizons and Expander Graphs,"
  arXiv:1204.6435.
- Bentsen, Gu, Lucas, "Fast scrambling on sparse graphs,"
  arXiv:1805.08215.
