# Stitched Floquet Evaporator Specification

## Goal

Move from a set of separate modules to one explicit repeated-interaction
evaporator.

This is not yet a time-independent Hamiltonian. It is a single Floquet-style
update rule:

```text
state at cycle n -> state at cycle n + 1
```

that includes:

```text
internal scrambling;
boundary emission;
energy bookkeeping;
coarse shell shrinkage.
```

This directly targets F15.

## Registers

At droplet size `L`, the active system is:

```text
B_L:
  internal droplet register, dim B_L = q^(L^2).

E_L:
  boundary/edge emission register.

R:
  accumulated radiation hard modes.

Q:
  accumulated soft/shrink records.

A:
  emitted-energy accumulator for the current shell.
```

The idealized finite-gauge factorization is:

```text
B_L ~= B_(L-1) tensor Shell_L,
dim Shell_L = q^(2L - 1).
```

## One Floquet Cycle

Each microscopic cycle is:

```text
U_cycle(L) = U_bookkeep U_emit U_edge U_scramble(L).
```

### 1. Internal scrambling

Use the interacting spin/algebraic-expander scrambling module:

```text
U_scramble(L) ~= exp[-i H_scr(L) dt],
```

where:

```text
H_scr(L)
  = sum_i (h_x,i X_i + h_z,i Z_i)
  + sum_(ij in E_L) (J_x,ij X_i X_j + J_y,ij Y_i Y_j + J_z,ij Z_i Z_j).
```

The graph `E_L` is inherited from the deterministic algebraic graph restricted
to the active droplet.

Evidence:

```text
interacting spin Page diagnostic;
entanglement-growth diagnostic;
OTOC/operator-spreading diagnostic.
```

### 2. Boundary-to-edge refresh

The boundary/edge register is assumed to be typical at:

```text
T_L = 2 sigma / (L log q).
```

In the stitched model this can be represented either by:

```text
U_edge:
  a weak mixing step between the active boundary and E_L;
```

or, at the coarse level:

```text
canonical edge weights derived from microcanonical state counting.
```

Evidence:

```text
edge thermal occupation diagnostic;
edge canonical typicality diagnostic;
edge dynamical typicalization diagnostic.
```

### 3. Emission block

The emission step uses a weak-coupling golden-rule channel:

```text
p_h(L) ~ int_bin d omega omega^(d-1)
         exp[S(M_L - omega) - S(M_L)].
```

For a 2D bath:

```text
d = 2.
```

The finite Hamiltonian block form is:

```text
|i>_port |h>_edge |in> |0>_hard |0>_soft
  <->
|0>_port |0>_edge |out> |h>_hard |record(i,h)>_soft.
```

This keeps hard radiation locally thermal while soft/global records purify the
capacity transferred out of the droplet.

At the bin-distribution level, the emission Hamiltonian can be written as:

```text
H_emit = sum_h g_h ( |h><in| + |in><h| ),
```

with:

```text
g_h^2 / sum_k g_k^2 = p_h^golden.
```

Then:

```text
P(h | emit) = p_h^golden.
```

This finite Hamiltonian implementation is checked in:

```text
notes/finite_emission_hamiltonian_results.md
```

A more natural finite-bath version uses equal microscopic coupling to bath
microstates:

```text
H_emit = g sum_(h,a) ( |h,a><in| + |in><h,a| ),
```

where:

```text
a = 1,...,N_h.
```

Then:

```text
P(h | emit) = N_h / sum_k N_k.
```

This shifts the golden-rule weight from bin-dependent matrix elements to finite
bath degeneracy. It is checked in:

```text
notes/finite_bath_density_emission_results.md
```

Evidence:

```text
boundary emission Hamiltonian block;
energy-conserving emission block;
microscopic golden boundary emission diagnostic.
finite emission Hamiltonian.
finite bath density emission.
```

### 4. Energy accumulator

Each emitted hard bin contributes:

```text
omega_h.
```

The accumulator updates:

```text
A -> A + omega_h.
```

The current shell mass gap is:

```text
Delta M = M_L - M_(L-1) = 4 sigma.
```

### 5. Coarse shell shrinkage

When:

```text
A >= Delta M,
```

apply the shell update:

```text
B_L -> B_(L-1) tensor Shell_L,
Shell_L -> Q,
L -> L - 1,
A -> A - Delta M.
```

This transfers the lost internal capacity into the soft/shrink record `Q`,
preserving global unitarity/purifiability.

The bookkeeping block can be represented as a reversible finite-register map:

```text
|L, A, shell_label, emitted_bin, records>
  ->
|L', A', shell_label', radiation_record, shrink_record, records>.
```

If the threshold does not fire:

```text
L' = L,
A' = A + emitted_bin,
shrink_record = empty.
```

If the threshold fires:

```text
L' = L - 1,
A' = A + emitted_bin - Delta M,
shrink_record = (L, shell_label).
```

The shrink record is what makes the map reversible. This is checked explicitly
in:

```text
notes/reversible_shrinkage_automaton_results.md
```

Evidence:

```text
finite gauge shell shrinkage;
finite gauge evaporation cycle;
autonomous repeated cycle;
many-cycle evaporation tracker.
reversible shrinkage automaton.
```

## Coarse Simulator

At the capacity/trajectory level, the stitched model reduces to:

```text
repeat:
  sample microscopic emitted quanta from golden-rule weights;
  accumulate emitted energy;
  apply L -> L - 1 when threshold is crossed;
  update internal/radiation capacities;
  estimate Page entropy from min(S_internal, S_external);
  use scrambling diagnostics as the F14 justification.
```

This is exactly the many-cycle tracker, now interpreted as the coarse limit of
one stitched Floquet update.

## What Is Now Stitched

The model now has one repeated update rule connecting:

```text
internal scrambling;
edge thermalization;
microscopic emission;
energy accumulation;
shell shrinkage;
radiation/record capacity.
```

This improves F15 from:

```text
separate modules
```

to:

```text
one explicit repeated-interaction architecture.
```

## What Is Still Not Fully Autonomous

Remaining caveats:

```text
1. U_edge and U_emit are represented at the channel/block level, not derived
   from one time-independent H_total.

2. The shell shrinkage threshold is still a coarse update rule.

3. The hard/soft record bookkeeping is explicit rather than emergent.

4. The large-L Page behavior uses Page/typicality reasoning rather than direct
   state-vector evolution.
```

So this is:

```text
F15 = P+
```

not:

```text
F15 = Y.
```

## Next Test

The immediate computational test is a stitched coarse simulator:

```text
given L0, q, sigma, bath dimension;
run the repeated cycle;
track emissions, shell transitions, lifetime, Page estimate, and F14 status.
```

This should not introduce new physics. It should make the current stitched
architecture explicit and auditable.
