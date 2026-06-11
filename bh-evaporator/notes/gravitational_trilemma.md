# The Gravitational Trilemma

**Core claim.** No local Hamiltonian in the thermodynamic limit can
simultaneously satisfy the Schwarzschild thermodynamic package. The
package reduces, via Props 1–2 of the companion paper, to two conditions
that are mutually exclusive in any local quantum system:

---

## 1. The two conditions

**Definition (Super-Hagedorn entropy, SH).** A Hamiltonian $H$ satisfies
SH if its microcanonical entropy $S(E) = \log\rho(E)$ grows
super-linearly with energy:

$$S(E) \;\geq\; c E^\alpha, \qquad \alpha > 1,\quad c > 0,$$

for all $E \geq E_0$.  The Schwarzschild case has $\alpha = 2$:
$S(E) = 4\pi E^2$ (Bekenstein-Hawking, $G=1$).

**Definition (Thermodynamic locality, TL).** A Hamiltonian $H$ satisfies
TL if it is a finite-range sum of local terms on a lattice:

$$H = \sum_{X \subset \Lambda,\, |X| \leq R} h_X, \qquad \|h_X\| \leq J,$$

acting on $\mathcal{H} = \bigotimes_{x\in\Lambda} \mathcal{H}_x$ with
$\dim\mathcal{H}_x = d < \infty$, where $\Lambda \subset \mathbb{Z}^d$
and $|\Lambda| = N$.

**Theorem (SH $\perp$ TL).** *No Hamiltonian satisfies both SH and TL
in the thermodynamic limit $N \to \infty$.*

---

## 2. Proof

Under TL the Hilbert space has dimension $d^N$, so the microcanonical
entropy is bounded by

$$S(E) \;\leq\; \log d^N \;=\; N \log d. \tag{$*$}$$

The local energy is extensive: the maximum energy is $\|H\| \leq J R_d N$
where $R_d$ is the lattice coordination number, so $E \leq C_J N$ for
a constant $C_J = J R_d$.  Hence

$$N \;\geq\; \frac{E}{C_J},$$

but the bound $(*)$ does not require $N$ to grow with $E$; we need the
other direction.  Fix an energy density $e = E/N \in (0, C_J)$; then
$N = E/e$ and

$$S(E) \;\leq\; \frac{E \log d}{e} \;=:\; c_{\rm TL}(e)\, E. \tag{TL bound}$$

The TL bound is *linear* in $E$ at fixed density $e$.

Under SH: $S(E) \geq c E^\alpha$ with $\alpha > 1$.  For $E$ large enough
(specifically $E > (c_{\rm TL}(e)/c)^{1/(\alpha-1)}$), the SH lower
bound exceeds the TL upper bound:

$$c E^\alpha \;>\; c_{\rm TL}(e)\, E,$$

a contradiction.  In the thermodynamic limit $E \to \infty$ (with
$N = E/e \to \infty$), this contradiction is unavoidable for any fixed
density $e$ and any $\alpha > 1$. $\square$

**Remark (superextensivity).** The proof has a clean information-theoretic
reading: TL systems have *extensive* entropy (entropy per site bounded by
$\log d$), while SH requires *superextensive* entropy ($S/N \sim E \to
\infty$ at fixed density).  Superextensive entropy is impossible in any
local system because it would require more entropy per site than the
local Hilbert space can hold.

---

## 3. Connection to the Schwarzschild thermodynamic package

The three observational conditions of the companion paper — cooling
(C), area-entropy (A), and radiation (R) — are not independent:

**Prop. 1 of companion paper:** (C) $\Leftrightarrow$ (A).  The
temperature law $T \sim M^{-1}$ is equivalent (via $T = (dS/dM)^{-1}$)
to $S = cM^2$.  So (C) and (A) together are a single condition: the
DOS is super-Hagedorn with $\alpha = 2$.

**Prop. 2 of companion paper:** (R) $\Rightarrow$ $N(E) \propto A(E)$.
The luminosity law $P \sim M^{-2}$ forces the number of
boundary-accessible emission channels to scale as $M^2$ (area).  This
is a condition on the *emission channel*, not on the internal DOS; it
is independent of (C)/(A) and achievable by local systems
(Stefan-Boltzmann, §4.1 below).

**Consequence:** The trilemma (C) + (A) + (R) reduces to:

> (SH): $S(E) = cE^2$ — imposed by (C)/(A) and impossible for local
> Hamiltonians (Theorem above).
>
> (R): $N(E) \propto E^2$ — imposed by (R) and achievable locally.

The trilemma is therefore not a three-way tension.  It is a single
obstruction — **super-Hagedorn entropy is incompatible with locality**
— with the radiation condition (R) playing a secondary role: it tells
you how the (non-local) system emits information but is not itself the
source of the impossibility.

---

## 4. The three pairs revisited

To keep the record straight, here is what each pair of conditions gives
for local QM:

### 4.1  (C) + (R) without (A): achievable locally

A compact thermal body of radius $\sim M$ at temperature $T \sim M^{-1}$
radiates by Stefan-Boltzmann:

$$P \;\sim\; \sigma T^4 \cdot M^2 \;\sim\; M^{-4} \cdot M^2 \;=\; M^{-2}
\qquad \text{(R satisfied)}$$

$$S_{\rm local} \;\sim\; V T^3 \;\sim\; M^3 \cdot M^{-3} \;=\; O(1)
\qquad \text{(A violated by } M^2\text{)}$$

This is possible locally: the photon gas in the Schwarzschild volume at
the Hawking temperature is nearly vacuum.  It carries $O(1)$ nats of
entropy, $M^2$ times less than $S_{\rm BH}$.

### 4.2  (A) + (C) [i.e., SH]: impossible locally

By the theorem: any $\alpha > 1$ growth of $S(E)$ contradicts TL.
The Schwarzschild case $S = 4\pi M^2$ requires superextensive entropy
with $\alpha = 2$.

### 4.3  (A) + (R): achievable only at the wrong temperature

Requiring $S = cM^2$ (A) and $P \sim M^{-2}$ (R) simultaneously fixes
the temperature via Stefan-Boltzmann ($P \sim T^4 M^2 = M^{-2}$
$\Rightarrow$ $T = M^{-1}$, which recovers (C)). But as §4.2 shows,
local QM with $S = cM^2$ requires spatial volume $V \sim M^5$
(from $V T^3 = M^2$ and $T = M^{-1}$), which violates the Schwarzschild
spatial scale $V \sim M^3$.  The system matching (A) and (R) has the
right temperature and luminosity but lives in a spatial region $M^{2/3}$
times larger than the BH.

---

## 5. The entropy gap

The central quantitative result: for any local QFT in the Schwarzschild
volume at the Hawking temperature,

$$\frac{S_{\rm BH}}{S_{\rm local}} \;=\; \frac{4\pi M^2}{O(1)} \;=\; O(M^2),
\qquad M \to \infty.$$

The BH entropy exceeds the local entropy budget by $M^2$ — exactly the
Schwarzschild area in Planck units.  This is not a quantitative mismatch
in coupling constants; it is a qualitative separation that grows without
bound.

Phrased another way: the BH is the unique thermodynamic object that
saturates the Bekenstein bound $S \leq 2\pi RM$ (with $R = 2M$,
$S = 4\pi M^2$) at temperature $T = 1/(8\pi M)$.  Local QFT at the
same temperature and spatial extent has $S = O(1)$, a factor $M^2$
below the Bekenstein maximum.

---

## 6. What is and is not claimed

**Claimed:**

- SH $\perp$ TL is a theorem (§2).  No citation needed beyond the
  dimension formula $S \leq N \log d$ for a local Hilbert space.
- Props 1–2 of the companion paper reduce the three-condition trilemma
  to a single obstruction (SH), so the "trilemma" is really a *lemma*.
- The entropy gap is $O(M^2)$, precisely the Schwarzschild area.

**Speculative:**

- Whether the theorem extends to non-relativistic QFT with a UV cutoff
  (the bound $S \leq N \log d$ requires a finite-dimensional per-site
  Hilbert space; in QFT the number of modes per volume is UV-divergent).
  The gap $O(M^2)$ likely survives after renormalization but needs checking.
- Whether interacting non-local systems (SYK, random matrices) can
  evade the theorem by having $N \sim E^2$ without a lattice structure.
  They are not TL systems, but they are also not obviously "gravitational."
  The right statement for them is an open question.

**Out of scope:**

- Why gravity achieves SH (positive result, requires holography or a
  microscopic theory of BH degrees of freedom).
- Whether the theorem characterizes BHs uniquely among all thermodynamic
  objects, or whether exotic near-Hagedorn string states approach the
  bound.

---

## 7. Open questions

1. **Lattice theorem.** State the $\alpha > 1$ impossibility for
   non-relativistic QM on $\mathbb{Z}^3$ with a clean set of
   assumptions.  The proof in §2 is essentially this; write it as a
   self-contained proposition.

2. **Continuum limit.** The QFT version requires a UV regulator.
   Replacing the lattice by a QFT with UV cutoff $\Lambda_{\rm UV}$:
   $N \to V \Lambda_{\rm UV}^3$, $d \to e^{s_{\rm UV}}$ where
   $s_{\rm UV}$ is the entropy density at the cutoff scale.  The TL
   bound becomes $S \leq V \Lambda_{\rm UV}^3 s_{\rm UV}$, still linear
   in $V$ (and hence in $E$ for extensive energy).  Super-Hagedorn
   still violates this for $M \gg \Lambda_{\rm UV}^{-1}$.

3. **Bekenstein saturation as a positive characterization.** The
   theorem says: local systems fall short of the Bekenstein bound by
   $O(M^2)$.  The BH saturates it.  This suggests a stronger claim:
   **BH entropy = Bekenstein saturation = impossibility of local
   description**.  Making this a biconditional would be the sharpest
   possible demarcation.
