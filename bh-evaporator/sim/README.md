Data generation for figures
===========================

This folder contains a small exact‑diagonalization (ED) pipeline to generate
thermodynamic and spectral data used by the figures. The goal is to make the
plots reproducible from versioned code and seeds, while keeping runtime modest.

What it computes
- Spectrum of a fully‑connected disordered XXZ core (default N=12 qubits).
- Microcanonical entropy S(E), temperature T_mu(E), and a convex‑intruder window.
- Edge spectral function of X=1/sqrt(N) sum σ_i^− in energy bins; extracts ω*(E).
- Packs arrays into NPZ files under sim/data/ for consumption by figs/generate.py.

Quick start
1) Ensure Python 3.9+ with SciPy is available
   pip install -r sim/requirements.txt

2) Generate data (defaults are chosen to run in a minute or two on a laptop):
   python sim/generate_data.py --N 12 --bins 20 --seed 1

Outputs
- sim/data/thermo.npz: E_centers, hist_E (DOS), S, T_mu, C_mu
- sim/data/spectral.npz: E_centers, omega_star

Notes
- N=12 (dim 4096) uses dense diagonalization for simplicity. Larger N requires
  sparse methods and longer runtime; extend the code if needed.
- Units are arbitrary up to overall scales; the figure code performs the β fit
  where needed (calibration→prediction storyline).

