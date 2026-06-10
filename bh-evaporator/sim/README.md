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

Dynamic shell evaporator kill test
----------------------------------

The script dynamic_shell_evaporator.py implements the first shell/time-bin test
for the revised paper direction. It is separate from the XXZ ED pipeline.

Run the convex negative-heat-capacity shell model:

```bash
python sim/dynamic_shell_evaporator.py
```

Run a linear-entropy control:

```bash
python sim/dynamic_shell_evaporator.py --curvature 1.0 --output sim/data/dynamic_shell_evaporator_linear_control.npz
```

Outputs:
- sim/data/dynamic_shell_evaporator.npz
- sim/data/dynamic_shell_evaporator_linear_control.npz

The dynamic shell model computes:
- shell entropy, beta, temperature, and dimensions
- density-of-states-driven emission probabilities
- mean core energy and emitted power
- radiation Renyi-2 entropy from the pure emitted time-bin state
- dimension-crossing and Page-turnover diagnostics

Generate the summary figure:

```bash
python figs/generate_dynamic_shell.py
```

Naive Hamiltonian collision test
--------------------------------

Run the first fixed-Hamiltonian collision model:

```bash
python sim/hamiltonian_shell_evaporator.py
```

Run the linear-entropy control:

```bash
python sim/hamiltonian_shell_evaporator.py --curvature 1.0 --output sim/data/hamiltonian_shell_evaporator_linear_control.npz
```

The first result is recorded in:

```text
notes/hamiltonian_naive_first_results.md
```

Short version: the naive binary-channel Hamiltonian is rank-limited and gets
partially trapped in dark subspaces. This is an informative failure, not yet a
working Hamiltonian evaporator.

Fixed high-rank channel probe
-----------------------------

Run the fixed high-rank shell-channel test:

```bash
python sim/fixed_high_rank_shell_channel.py
```

Run the fixed-channel convex/control comparison:

```bash
python sim/fixed_high_rank_shell_channel.py --curvature 3.0 --channel-mode fixed --channels 3 --max-channels 3 --output sim/data/fixed_high_rank_shell_channel_curv3_fixedch3.npz
python sim/fixed_high_rank_shell_channel.py --curvature 1.0 --channel-mode fixed --channels 3 --max-channels 3 --output sim/data/fixed_high_rank_shell_channel_linear_fixedch3.npz
```

The result is recorded in:

```text
notes/fixed_high_rank_channel_results.md
```

Short version: fixed high-rank maps recover the convex/control separation,
suggesting that the naive Hamiltonian failed because of insufficient outgoing
channel capacity.

Reduced-density Hamiltonian channel
-----------------------------------

Run the longer multi-mode Hamiltonian test using the exact reduced core channel:

```bash
python sim/hamiltonian_shell_density_channel.py --curvature 3.0 --channels 8 --g 0.5 --steps 48 --seeds 3 --output sim/data/hamiltonian_shell_density_curv3_ch8_g05_s48.npz
python sim/hamiltonian_shell_density_channel.py --curvature 1.0 --channels 8 --g 0.5 --steps 48 --seeds 3 --output sim/data/hamiltonian_shell_density_linear_ch8_g05_s48.npz
```

The result is recorded in:

```text
notes/hamiltonian_density_channel_results.md
```

Short version: a fixed multi-mode collision Hamiltonian shows convex
acceleration in a weak-coupling working window, while the linear control
decelerates.

Hamiltonian density scan
------------------------

Run the robustness scan:

```bash
python sim/scan_hamiltonian_density.py
python figs/generate_hamiltonian_scan.py
```

Outputs:

```text
sim/data/hamiltonian_density_scan.csv
sim/data/hamiltonian_density_scan.npz
hamiltonian_density_scan.pdf
```

The result is recorded in:

```text
notes/hamiltonian_density_scan_results.md
```

Polished Step 2 figure
----------------------

Generate the polished 12-seed Step 2 comparison:

```bash
python figs/generate_step2_polished.py
```

Default inputs:

```text
sim/data/hamiltonian_shell_density_curv3_ch8_g05_s48_seeds12.npz
sim/data/hamiltonian_shell_density_linear_ch8_g05_s48_seeds12.npz
```

Output:

```text
step2_hamiltonian_polished.pdf
```

The result is recorded in:

```text
notes/step2_polished_status.md
```

Notes
- N=12 (dim 4096) uses dense diagonalization for simplicity. Larger N requires
  sparse methods and longer runtime; extend the code if needed.
- Units are arbitrary up to overall scales; the figure code performs the β fit
  where needed (calibration→prediction storyline).
