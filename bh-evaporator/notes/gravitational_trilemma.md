# The Gravitational Trilemma (working title: "CARs theorem")

**Core claim.** No 3D local non-relativistic Hamiltonian with a
thermodynamic limit can simultaneously satisfy all three of:

- **(C) Cooling law.** $T \sim M^{-1}$ — temperature decreases with
  mass; equivalently, negative heat capacity.
- **(A) Area-entropy law.** $S \sim M^2$ — total entropy scales as the
  area, not the volume, of the system.
- **(R) Radiation law.** $P \sim M^{-2}$ — emitted power (luminosity)
  scales as mass squared inverse.

A Schwarzschild black hole satisfies all three simultaneously. Any two
are achievable by local quantum mechanics; the third is then violated
by a factor that grows without bound ($\sim M^2 \to \infty$ as
$M \to \infty$).

Working name options: "the gravitational trilemma," "CARs theorem," or
"the area-entropy gap."

---

## 1. Setup and conventions

Throughout, Planck units $G = \hbar = c = k_B = 1$. Mass $M$ is the
characteristic energy/mass scale of the system (the "black hole mass"
in the gravitational case). Spatial extent $R \sim M$ (Schwarzschild
radius). Volume $V \sim M^3$. All $\sim$ are up to $O(1)$ numerical
factors.

**Schwarzschild values (the target):**

| Quantity | Value |
|---|---|
| Temperature | $T_{\rm BH} = 1/(8\pi M) \sim M^{-1}$ |
| Entropy | $S_{\rm BH} = 4\pi M^2 \sim M^2$ |
| Luminosity | $P_{\rm BH} \sim 1/(15360\pi M^2) \sim M^{-2}$ |

These satisfy $P_{\rm BH} = \sigma T_{\rm BH}^4 \cdot A_{\rm BH} \cdot f$
for $f = O(1)$ (Stefan-Boltzmann up to greybody factors), and
$T_{\rm BH} = (dS_{\rm BH}/dM)^{-1}$ (first law), confirming internal
consistency.

---

## 2. Checking all three pairs for local QM

### 2.1 (C) + (R) without (A)

A thermal body of radius $R \sim M$ at temperature $T \sim M^{-1}$:

$$
P_{\rm S-B} \sim \sigma T^4 \cdot R^2 \sim M^{-4} \cdot M^2 = M^{-2}
\qquad\text{(R satisfied)}
$$

$$
S_{\rm local} \sim V T^3 \sim M^3 \cdot M^{-3} = O(1)
\qquad\text{(A violated by } M^2\text{)}
$$

**Verdict.** Stefan-Boltzmann radiation from a compact thermal body at
the Hawking temperature matches (C) and (R) exactly, but the entropy
is $O(1)$ — a factor $M^2$ below $S_{\rm BH}$.

This is not a pathological failure: the photon gas (or any local QFT)
in the Schwarzschild volume at the Hawking temperature is almost
vacuum. The black hole has $M^2$ times more entropy than any local
field theory would predict at the same temperature and size.

### 2.2 (C) + (A) without (R)

A system with super-Hagedorn DOS $\rho(E) \sim e^{cE^2}$ has
$T = (2cE)^{-1} \sim E^{-1}$, so $T \sim M^{-1}$ at $E = M$: (C)
is satisfied. The entropy is $S = \log\rho(M) = cM^2 \sim M^2$: (A)
is satisfied.

This is the shell Hamiltonian of the companion paper, with $c = 4\pi$
(Bekenstein-Hawking coefficient). It is a legitimate non-gravitational
quantum system.

**What does its luminosity look like?** For a *local* Hamiltonian with
this DOS, the boundary-accessible modes scale as $N \sim A \sim M^2$
(boundary modes of a 3D box). But the temperature is only $T \sim M^{-1}$,
so the thermal occupation per mode is $n_{\rm mode} \sim e^{-\omega/T}$
for typical $\omega \sim T \sim M^{-1}$. Power:

$$
P_{\rm local} \sim N \cdot T^2 \sim M^2 \cdot M^{-2} = O(1)
\qquad\text{(R violated: wrong power of }M\text{)}
$$

Alternatively, compute by thermal equilibration with a radiation bath
at temperature $T$: Stefan-Boltzmann gives $P \sim T^4 \cdot A_{\rm box}$
where $A_{\rm box}$ is the area of the box. A box with $S = M^2$ and
$T = M^{-1}$ has volume $V = S/(cT^3) = M^2 / (c M^{-3}) = M^5/c$,
so $A_{\rm box} \sim M^{10/3}$ and

$$
P_{\rm local} \sim T^4 \cdot M^{10/3} \sim M^{-4} \cdot M^{10/3} = M^{-2/3}
\qquad\text{(R violated: } P \sim M^{-2/3} \neq M^{-2}\text{)}
$$

**Verdict.** A system with the right DOS matches (C) and (A), but the
luminosity is $M^{4/3}$ times too large (or $M^{-2/3}$ vs $M^{-2}$
depending on the spatial geometry). The discrepancy grows with $M$.

*Note:* the companion paper's shell Hamiltonian gets (R) right by
*imposing* $N(E) \propto A(E)$ as an input (Prop. 2). That is not
derived from the local structure of the Hamiltonian — it is the one
place where spatial geometry enters. This is the operational form of
(A) failing for the generic local system.

### 2.3 (A) + (R) without (C)

Fix $S \sim M^2$ (A) and $P \sim M^{-2}$ (R). From Stefan-Boltzmann:

$$
P \sim T^4 \cdot R_{\rm box}^2 = M^{-2}
\implies T^4 R_{\rm box}^2 = M^{-2}.
$$

From $S \sim V_{\rm box} T^3 = M^2$:

$$
R_{\rm box}^3 T^3 = M^2.
$$

Solving both simultaneously: from the entropy equation,
$R_{\rm box} = M^{2/3}/T$; substituting into the luminosity equation,
$T^4 \cdot M^{4/3}/T^2 = M^{-2}$, giving $T^2 M^{4/3} = M^{-2}$,
so

$$
T = M^{-5/3}.
$$

But the Hawking temperature is $T_{\rm BH} \sim M^{-1}$. The local
system matching (A) and (R) runs at $T \sim M^{-5/3}$, which is
*much colder* than the Hawking temperature: $T_{\rm local}/T_{\rm BH}
\sim M^{-2/3} \to 0$.

**Verdict.** Conditions (A) and (R) together determine a temperature
$T \sim M^{-5/3}$, which differs from the Hawking temperature by the
factor $M^{-2/3}$. Condition (C) fails.

---

## 3. The quantitative gap

All three pairwise failures share a common factor: $M^{2/3}$ or $M^2$
depending on which condition is tested. The natural way to state this
uniformly is via the *entropy deficit*:

$$
\boxed{
  \frac{S_{\rm BH}}{S_{\rm local}(T_{\rm BH}, V_{\rm BH})}
  = \frac{M^2}{O(1)} = M^2
}
$$

A 3D local system in the Schwarzschild volume at the Hawking temperature
has entropy $O(1)$; the black hole has entropy $M^2$. The ratio is
$M^2 = (T_{\rm BH}^{-1})^2$ — the square of the thermal length in
Planck units, which is precisely the Schwarzschild area.

Equivalently, the black hole saturates the Bekenstein-Hawking entropy
while being anomalously cold: it packs $M^2$ nats of entropy into a
region whose field-theory entropy budget is $O(1)$.

---

## 4. Connection to Props 1–2 of the companion paper

**Prop. 1 (DOS rigidity).** The requirement $T \sim M^{-1}$ forces
$\rho(E) \sim e^{cE^2}$, so $S = cM^2$. This is condition (C) $\Rightarrow$
(A): given cooling, the entropy law follows automatically from the
first law $T = (dS/dM)^{-1}$.

**Consequence:** (C) and (A) are not independent — cooling implies
area-entropy for any system with a smooth DOS. The trilemma therefore
reduces to:

> Given (C) [which forces (A) via Prop. 1], can a local QM system
> also achieve (R)?

**Prop. 2 (luminosity measures boundary accessibility).** The requirement
$P \sim M^{-2}$ forces $N(E) \propto A(E) \sim M^2$. For a local
Hamiltonian, the natural $N(E)$ is the number of boundary-layer modes
$\sim A$; the issue is that this count gives the wrong *rate* unless
the system has the anomalous entropy of the BH (Section 2.2 above).

**The demarcation refined:** The trilemma reduces, via Props 1–2, to a
single question: can a local QM Hamiltonian simultaneously have
$\rho(E) \sim e^{cE^2}$ **and** emit at the rate $N(E)/\beta \sim A(E)/M$?
The entropy is forced by the DOS; the emission rate is forced by the
luminosity law; and the two together overconstrain any local system
because the volume required to hold the entropy is $M^{5/3}$ times too
large for the emission rate to scale as $M^{-2}$.

---

## 5. The one-line impossibility

Let $M$ be the system mass, $R = 2M$ the Schwarzschild radius,
$V = (4\pi/3)R^3 \sim M^3$ the Schwarzschild volume. For any 3D local
QFT at temperature $T$ in volume $V$:

$$
S \leq c_d V T^d \quad (d = 3)
$$

where $c_3$ is the Stefan-Boltzmann constant of the QFT.
Condition (C): $T = 1/(8\pi M)$. Then

$$
S_{\rm local} \leq c_3 M^3 \cdot M^{-3} = c_3.
$$

This is $O(1)$, independent of $M$. No local QFT in the Schwarzschild
volume at the Hawking temperature can have entropy growing with $M$.
Since $S_{\rm BH} = 4\pi M^2$, the BH entropy exceeds the local QFT
entropy budget by $S_{\rm BH}/c_3 \sim M^2$ — the Schwarzschild area
in Planck units.

*This is the one-line proof that (C) + (R) $\not\Rightarrow$ (A) for
local QFT, and hence that all three together require a non-local
(gravitational) mechanism.*

---

## 6. Why locality is the obstruction

The proof in §5 uses only the extensivity of entropy in local QFT:
$S \leq c_d V T^d$. This is a consequence of locality (interactions
decay with distance) and the thermodynamic limit (no long-range
correlations dominate). Specifically:

- **Volume law** is a theorem for local Hamiltonians at finite
  temperature in the thermodynamic limit (it follows from subadditivity
  and cluster decomposition).
- **Area law** for total entropy requires either: (i) only boundary
  degrees of freedom contribute (holographic/non-local theory), or
  (ii) the bulk is nearly vacuum at the given temperature (which is
  Section 2.1: the local system IS near-vacuum at $T_{\rm BH}$, with
  entropy $O(1)$).

The black hole achieves area-law total entropy because it is not
described by a local bulk QFT — it *is* the boundary theory (or,
in the holographic language, the boundary IS the theory). From the
QM side, this is the statement that $d_B = e^{S_{\rm BH}}$ is the
total Hilbert space dimension, and the system has no additional
volume-law bulk. From the gravity side, this is why the Bekenstein
bound is an equality for black holes and an inequality for everything
else.

---

## 7. What is and is not claimed

**Claimed (immediately doable):**
- For non-relativistic QM on a lattice or local QFT, the trilemma
  is a theorem: (C) + (R) → $S = O(1)$ in the Schwarzschild volume,
  which contradicts (A) by $O(M^2)$.
- The gap is *quantitatively* $M^2$ — the Schwarzschild area — not
  just "large."
- Props 1–2 reduce the three conditions to one: can a local QM system
  have the BH entropy $S = cM^2$ and the BH emission rate
  $P \sim M^{-2}$ simultaneously? It cannot.

**Not yet claimed (speculative):**
- Whether the argument extends cleanly to relativistic QFT (UV
  divergences affect $S_{\rm local}$ but not the gap; needs checking).
- Whether interacting non-local but non-gravitational theories (SYK,
  random matrices) can satisfy all three, and if so at what cost to
  "locality."
- The exact coefficient in the gap formula (numerical factors in
  Stefan-Boltzmann vs. BH thermodynamics).

**Genuinely hard (out of scope for now):**
- Why gravity *achieves* all three — that requires a positive result
  about gravity, not just a negative result about locality.
- Whether the trilemma uniquely characterizes black holes among all
  thermodynamic systems, or if other exotic objects (e.g., certain
  string states near the Hagedorn temperature) can satisfy two of
  three in a qualitatively different way.

---

## 8. Open questions and next steps

1. **The lattice theorem.** State the trilemma as a formal theorem for
   non-relativistic QM on $\mathbb{Z}^3$ with finite-range interactions.
   The proof is §5 plus a lattice version of the volume-law entropy
   bound. Straightforward.

2. **The non-relativistic to QFT bridge.** The companion paper works
   in non-relativistic QM. The trilemma argument is cleanest there.
   QFT adds UV divergences but doesn't change the $O(1)$ vs $O(M^2)$
   gap. Need to check this doesn't require renormalization of the gap.

3. **The positive statement.** The trilemma shows local QM cannot
   achieve (C)+(A)+(R). What *can* achieve it? The answer involves
   holography ($S = A/4G$), i.e., a theory that lives on the boundary.
   Connecting the trilemma's impossibility to the necessity of
   holography would be the strongest possible version of the demarcation.

4. **Relation to Bekenstein bound.** The Bekenstein bound says
   $S \leq 2\pi RE$ for any system of radius $R$ and energy $E$.
   The BH saturates this with $R = 2M$ and $E = M$: $2\pi \cdot 2M
   \cdot M = 4\pi M^2 = S_{\rm BH}$. Local QFT in the same region has
   $S = O(1) \ll 4\pi M^2$. So the BH is simultaneously the
   Bekenstein-maximal system AND the one that no local QFT can match.
   The trilemma is essentially the statement that Bekenstein saturation
   requires non-local (gravitational) physics.

5. **Higher dimensions.** In $d$ spatial dimensions, the Schwarzschild
   scaling changes: $T \sim M^{-(d-2)/(d-1)}$, $S \sim M^{(d-1)/(d-2)}$
   (area-law in $d$-dim Planck units), $P \sim M^{-2(d-1)/(d-2)}$.
   The local entropy bound becomes $S_{\rm local} \sim V T^d \sim
   M^d M^{-d(d-2)/(d-1)}$. Check whether the gap persists in all
   $d \geq 3$.
