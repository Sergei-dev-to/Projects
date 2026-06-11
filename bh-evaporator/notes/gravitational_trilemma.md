# The Entropy-Budget Gap (formerly "the gravitational trilemma")

**Status (2026-06-10).** Demoted from standalone-theorem ambition to
positioning material, after review. Two findings forced the demotion:

1. **It is not a trilemma.** Props 1–2 of the conditional-Hamiltonian paper
   collapse (C)+(A) into a single condition (super-Hagedorn DOS), and (R)
   is locally achievable. One obstruction, not three-way tension.
2. **The obstruction is not new.** It is the founding observation of
   holography. A standalone paper would be re-deriving 't Hooft/Susskind in
   lattice notation.

The salvageable content has been distributed:

- **Conditional-Hamiltonian paper** (`paper_ideal_hamiltonian/main.tex`,
  Section "Necessity of the two inputs" + open problem 1): a paragraph
  stating the gap, citing the classics, and claiming only the
  factorization. Done 2026-06-10.
- **Super-Hagedorn companion paper** (`paper_super_hagedorn_evaporator/`):
  the escape-route classification (Section 3 below) as the framing question
  its construction partially answers. **Pending.**

---

## 1. The established impossibility (cite, don't claim)

That black-hole entropy exceeds any local state counting is classical:

- Bekenstein 1981 (PRD 23, 287): universal entropy bound $S \leq 2\pi RM$.
- 't Hooft 1993 (gr-qc/9310026): gravitational collapse implies
  dimensional reduction; DOF count bounded by area.
- Susskind 1995 (J. Math. Phys. 36, 6377): the holographic principle.
- Bousso 2002 (RMP 74, 825): covariant entropy bounds, review.
- Cohen–Kaplan–Nelson 1999 (PRL 82, 4971) and Yurtsever 2003 (PRL 91,
  041302): cutoff local QFT restricted to non-collapsing states maxes out
  at $S \sim A^{3/4}$ — sharper than the Stefan-Boltzmann estimate below.

**Evaporation-adapted version (exposition, not a result).** A local field
theory occupying the Schwarzschild volume $V \sim M^3$ at the Hawking
temperature $T \sim M^{-1}$ carries

$$S_{\rm local} \sim VT^3 = O(1) \quad\text{vs}\quad S_{\rm BH} = 4\pi M^2 .$$

The local body matched to the black hole's actual $T$ and $R$ is
essentially vacuum; the gap is $O(M^2)$ — the area in Planck units. Vivid
for the evaporation context, implicit in the literature.

**Lattice version (elementary lemma, not a theorem).** A finite-range
Hamiltonian on $N$ sites of local dimension $d$ has $S \leq N\log d$ with
extensive energy $E \leq C_J N$. At fixed energy density this gives
$S(E) \leq c_{\rm TL}\,E$, linear — incompatible with $S \geq cE^\alpha$,
$\alpha > 1$, at large $E$.

*Known gap in the old "SH ⊥ TL theorem" framing:* the fixed-density
argument does not cover the Schwarzschild regime ($N \sim M^3$, energy
density $\to 0$). The correct general statement is not the fixed-density
bound but the contrapositive bookkeeping of $S \leq N\log d$ — which is
exactly the escape-route classification below. The theorem packaging is
dropped.

## 2. What is actually ours: the factorization

The classics say "the package requires holography." Props 1–2 say which
half:

- **State count** ($S = cM^2$, equivalently $T \sim M^{-1}$): provably
  non-local (Section 1). All the gravity is here.
- **Rate condition** ($P \sim M^{-2}$, equivalently area-many comparable
  emission channels): locally achievable. A Stefan-Boltzmann body at
  $T \sim M^{-1}$ radiating from area $\sim M^2$ has exactly this power
  law while carrying $O(1)$ entropy.

The imported gravitational structure is exactly one scaling law's worth,
concentrated entirely in the state count. This demarcation is the paper's
move; it is now stated there.

## 3. The live question: escape-route classification (→ companion paper)

$S \leq N\log d$ has exactly three escape routes. Any system with
$S(E) \geq cE^\alpha$, $\alpha > 1$, must have at least one of:

1. **Unbounded local dimension** ($d$ grows with $E$);
2. **Growing interaction range / participation** (terms couple $O(E)$-sized
   sets, e.g. SYK-like — though SYK itself has $S \sim N$, not
   super-Hagedorn);
3. **Variable degree-of-freedom count** ($N$ grows with $E$ — the
   variable-$N$ constructions: `variable_n_bose_hubbard`,
   `variable_length_spin_chain`, and the super-Hagedorn evaporator itself).

Open questions, in scope for the companion paper:

- Which routes are individually *sufficient* for $S \propto E^2$ over a
  finite window, and which the companion construction actually uses.
- Whether boundary accessibility (area-many comparably coupled emitters)
  can coexist with each route — route 3 seems natural for it; route 2 may
  conflict with any boundary notion.
- Whether a route can support the full evaporation package (negative heat
  capacity trajectory + Page curve), or only the static state count.
- The Bekenstein-saturation angle (BH = unique saturator at its own $T$,
  $R$) — keep as remark only; the biconditional needs a definition of
  "local description" that circles back to the same bookkeeping.

## 4. What died

- The name "trilemma" and the three-condition framing.
- The "SH ⊥ TL" theorem (proof gap at Schwarzschild scaling; corrected
  content absorbed into Sections 1 and 3).
- Standalone-paper ambition. Codex review (2026-06) was right: core
  't Hooft/Susskind/Bousso territory, with Yurtsever/CKN as the
  quantitative sharpening already in the literature.
