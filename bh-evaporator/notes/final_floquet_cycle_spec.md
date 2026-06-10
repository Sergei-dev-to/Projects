# Final Floquet Cycle Specification

## Purpose

Specify the current evaporator as one finite repeated unitary cycle.

This note is the model definition. The diagnostics in the simulation scripts
are tests of this object, not separate definitions of the model.

## Registers

For an initial droplet size `L0`, the active core is a finite register:

```text
B_L ~= B_(L-1) tensor Shell_L
dim B_L = q^(L^2)
dim Shell_L = q^(2L - 1)
```

The exact state-vector diagnostics use a qubit encoding:

```text
dim B_L0 = 2^(L0^2).
```

The thermodynamic dictionary is:

```text
M_L = 4 sigma L
S_micro(L) = log dim B_L = L^2 log q
T_L = (dS_micro/dM)^(-1) = 2 sigma / (L log q).
```

The state also contains:

```text
accumulator A:
  finite energy counter for emitted hard quanta;

hard radiation H_t:
  visible hard emission register for step t;

bath purifier C_t:
  hidden purifier register for the hard channel at step t;

soft record S_t:
  shell-transfer record for step t, trivial unless the energy threshold is
  crossed.
```

After `n` emission steps the global Hilbert space is:

```text
B_L0 tensor A tensor product_t (H_t tensor C_t tensor S_t).
```

The exact diagnostic stores this as a sparse pure state over:

```text
(core, accumulator, transferred_shell_count, soft_history, hard_history,
 bath_history).
```

## Hard-Emission Weights

At each step, hard-emission weights are generated from the microcanonical
state-count ratio:

```text
Gamma_L(omega) ~ rho_bath(omega) exp[S(M - omega) - S(M)].
```

For the two-bin finite diagnostic, the hard register is:

```text
H_t = span{|0>, |1>}.
```

The probability `p_t = P(H_t = 1)` is obtained by integrating the above
golden-rule weight over two energy bins.

The corresponding mean emitted hard energy is:

```text
<omega>_t = sum_bins P_t(bin) <omega>_bin.
```

The large-`L` weighted-power diagnostic computes:

```text
W_L = boundary * integral d omega
                  omega^d exp[S(M - omega) - S(M)].
```

For `d = 2`, this gives:

```text
W_L ~ M^-2.
```

## One Cycle

One Floquet step maps:

```text
|core, A, records> -> |core', A', records, H_t, C_t, S_t>.
```

It has four stages.

### 1. Scramble The Active Core

Apply a fixed scrambling unitary to the currently active core register:

```text
|core> -> U_scr |core>.
```

The current diagnostics compare:

```text
Margulis-like expander;
grid-like local mixing;
no scrambling.
```

The no-scrambling comparison is part of the model test: hard thermality alone
should not produce the full information-flow behavior.

### 2. Emit A Hard Quantum And Its Purifier

For hard probability `p_t`, apply the isometry:

```text
|psi> -> sqrt(1 - p_t) |psi> |0>_H |0>_C
       + sqrt(p_t)     |psi> |1>_H |1>_C.
```

The hard register is the visible local radiation channel. The bath purifier
keeps the global evolution pure while making the hard-local state thermal or
thermal-like after the purifier is ignored.

The emitted hard energy is:

```text
epsilon(0) = 1
epsilon(1) = 2
```

in the compact exact diagnostic. In the rate diagnostic these labels represent
energy bins from the microcanonical golden-rule distribution.

### 3. Accumulate Emitted Energy

Update the energy accumulator:

```text
A -> A + epsilon(H_t).
```

This is the finite-register version of many small hard emissions adding up to
one coarse shrinkage event.

### 4. Transfer A Shell Record At Threshold

If the accumulator crosses the threshold:

```text
A >= Delta,
```

then:

```text
A -> A - Delta;
extract Shell_L from the active core;
write its label into S_t;
increase transferred_shell_count by one.
```

If the threshold is not crossed:

```text
S_t = trivial record.
```

This step reduces the active internal state capacity while preserving global
purity by moving the shell information into radiation records.

## Observables

The diagnostics use the following subsystem split:

```text
core:
  remaining active core plus accumulator;

hard radiation:
  all H_t registers;

bath purifier:
  all C_t registers;

soft radiation:
  all S_t records;

visible radiation:
  hard radiation plus soft radiation;

full radiation:
  hard radiation plus bath purifiers plus soft radiation.
```

The main entropies are:

```text
S_micro(L):
  Boltzmann/microcanonical entropy of the remaining droplet sector;

S_vN(R):
  von Neumann entropy of the emitted radiation subsystem;

S_2(R):
  second Rényi entropy, used only as an explicitly labeled secondary
  diagnostic;

I(old:new):
  quantum mutual information between early and late radiation records.
```

## Current Status

This cycle closes the model-specification gap under the Floquet toy-model
standard:

```text
finite Hilbert space;
explicit repeated unitary update;
purifiable hard channel;
threshold-triggered shrinking capacity;
time-resolved radiation records;
microcanonical/golden-rule hard weights.
```

Remaining limitations:

```text
the threshold rule is selected as part of the model;
the exact state-vector runs are small;
the hard alphabet is compact;
the rate-generation scale is larger than the exact register scale;
the cycle is driven/stroboscopic, not a simple time-independent Hamiltonian.
```

