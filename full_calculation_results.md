# Calculation Results — Updated Summary

## Calculation 1: KNdS Entropy Deficit

### Result
The geometric mean formula ΔS = √(S_BH · S_cosmo) is an accident of SdS. 
The correct generalization for all Kerr-Newman-de Sitter is:

**ΔS = π[(r_b + r_-)(r_c + r_-) - a²] / G**

This is an algebraic identity (Vieta's relations for the quartic horizon 
equation), verified to machine precision. The inner Cauchy horizon radius 
r_- enters essentially.

### Literature status
The "entropy product" literature (Cvetič-Larsen and followers) studies 
S_+ · S_- = mass-independent quantities. Our identity is about the 
entropy *deficit* S_dS - S_BH - S_cosmo in terms of all horizon radii.
This specific identity does not appear to be stated explicitly in the 
literature, though the Vieta relations for KNdS horizons are well-known.
Would need a more targeted search to confirm novelty definitively.

### Publishability
Marginal as a standalone result — it's a classical algebraic identity.
Best used as a component of a broader SdS thermodynamics paper (Thread B).

---

## Calculation 2: Log Corrections

### Result
Inconclusive. The CS framework predicts the total one-loop Nariai 
correction should decompose as:
  +3/2 ln S₀ (Schwarzian boundary mode) 
  -1 ln S₀ (regularized CS TEE)
  = +1/2 ln S₀ (total prediction)

This cannot be verified without the full 4d one-loop result on dS₂×S², 
which is an active research topic (Castro et al. 2503.14623, Maulik et al.
2503.08617, both 2025). Filed as a prediction to check when those results
mature.

---

## Calculation 3: Parmentier SU(2) Model Diagonalization

### Model
H = J_x² - J_y² = (1/2)(J_+² + J_-²) in the spin-j representation.
This is Parmentier's (2024) model for emergent de Sitter quasinormal modes.

### Results

**1. E → -E spectral symmetry: EXACT**
Confirmed to machine precision (10^{-12} relative) for all tested j up to 500.
The symmetry is algebraic: U = exp(iπJ_z/2) satisfies UHU† = -H.
U² = (-1)^m (m-parity). Each m-parity sector is independently symmetric.
This is a rotation by π/2 around z, which swaps J_x ↔ J_y with a sign.

**2. Maximum eigenvalue: E_max = j(j+1) - √2 j + O(1)**
This is a clean quantitative result. The classical maximum is the Casimir 
j(j+1) (achieved when J_y = J_z = 0, J_x² = j(j+1)). The quantum 
correction is exactly -√2 j. Verified for j up to 500:

  j=100: j(j+1) - E_max = 141.41,  √2·j = 141.42
  j=200: j(j+1) - E_max = 282.83,  √2·j = 282.84
  j=500: j(j+1) - E_max = 707.07,  √2·j = 707.11

The √2 likely comes from the zero-point energy of the quadratic 
fluctuations around the classical maximum (two modes of frequency 1, 
combined as √(1²+1²) = √2 in some sense). Worth checking analytically.

**3. Spectral density: approximately uniform, NOT sinh-like**
The density of states is approximately uniform across the spectrum 
(best fit is uniform, slightly better than semicircle). Near the edges,
the level spacing is ε_n ≈ a·n + b·n² with a ≈ 2.83j, b ≈ -0.007,
giving a polynomial (not exponential) density.

The spectrum does NOT reproduce the JT gravity ρ(E) ∝ sinh(2π√(2S₀E)).
This is expected: the Parmentier model is a single spin-j system with
O(j) levels. The sinh density requires exponentially many levels (e^{S₀}),
which would only appear in the MANY-BODY version (filling single-particle
levels with fermions à la Banks).

**4. Robustness of the symmetry**
The E → -E symmetry would be broken by any term that does not commute 
with U = exp(iπJ_z/2). Specifically:
- Terms even in both J_x and J_y (e.g., J_x⁴ + J_y⁴): PRESERVE symmetry
- Terms odd in J_z (e.g., B·J_z, magnetic field): BREAK symmetry
- J_z² terms: PRESERVE (commute with U)
- J_x·J_y + J_y·J_x terms: need to check case by case

The symmetry is SPECIFIC to the H = J_x² - J_y² structure and is not
a generic property of SU(2) Hamiltonians. It corresponds to a discrete
dihedral symmetry of the Hamiltonian.

### What this means for the dS program

The Parmentier model confirms the E → -E single-particle symmetry 
analytically expected. But the model does NOT produce the key feature 
of de Sitter thermodynamics (exponential density of states) at the 
single-particle level. The interesting question — whether a many-body 
version produces a particle-hole duality mapping particle-like to 
black-hole-like states — requires the many-body calculation (#5 in 
section 16 of the working notes), which is a larger computation.

The √2 quantum correction to E_max is a concrete, potentially publishable 
finding if it connects to known results about quantum corrections to 
classical extrema in spin systems.

---

## Overall Assessment

Three calculations attempted:
1. **KNdS** — completed, clean classical identity, demotes geometric mean
2. **Log corrections** — blocked on external input, prediction filed
3. **Parmentier** — completed, confirms symmetry, finds √2 correction, 
   shows single-particle spectrum is not sinh-like

None of these calculations changes the status of Thread A (Kiefer-Kolland 
anyonic resolution). The path forward is writing.
