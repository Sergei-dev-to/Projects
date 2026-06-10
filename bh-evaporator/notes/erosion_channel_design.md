# Erosion Channel Design

## Purpose

Turn the edge-tension gauge droplet from a thermodynamic counting model into
an explicit evaporator channel.

The current core model has:

```text
dim H_L = q^(L^2)
M_L = 4 sigma L
T_L^disc = 4 sigma / ((2L - 1) log q)
```

One erosion step removes the shell:

```text
H_L ~= H_(L-1) tensor H_shell(L)
dim H_shell(L) = q^(2L - 1).
```

The task is to define:

```text
V_L : H_(L-1) tensor H_shell(L)
      -> H_(L-1) tensor H_hard(L) tensor H_soft(L)
```

so that:

```text
hard radiation carries energy and looks thermal;
soft radiation carries the shell information required by unitarity;
the core Hilbert space shrinks from q^(L^2) to q^((L-1)^2).
```

## Plaquette-Flux Factorization

For the abelian finite-gauge droplet, solving Gauss law leaves independent
plaquette flux variables.

For an `L x L` square:

```text
H_L ~= tensor over L^2 plaquette-flux q-dits.
```

The nested square factorization is:

```text
H_L ~= H_(L-1) tensor H_shell(L),
```

with:

```text
dim H_shell(L) = q^(2L - 1).
```

This is the basis used by the first channel diagnostic.

## Level 1: Archive Channel

This is the sanity check.

Let:

```text
|a>_shell,       a = 1,...,D_shell
|h>_hard,        h = 1,...,d_h
```

and choose a thermal hard distribution:

```text
p_L(h) = exp(-epsilon_h / T_L) / Z_L.
```

Define:

```text
V_L |a>
  = sum_h sqrt(p_L(h)) |h>_hard |a,h>_soft.
```

where all soft states `|a,h>` are orthogonal.

Properties:

```text
1. exact isometry;
2. exact hard thermality after tracing soft;
3. exact preservation of shell information;
4. soft dimension = D_shell * d_h.
```

Weakness:

```text
This is an archive channel.
The soft sector stores both the shell label and the hard label.
It proves possibility, not naturalness.
```

## Level 2: Minimal-Soft Random-Unitary Channel

This is the first interesting test.

Require:

```text
dim H_soft(L) = dim H_shell(L).
```

Use random unitaries on the shell space:

```text
U_h : H_shell(L) -> H_soft(L).
```

Define:

```text
V_L |psi>
  = sum_h sqrt(p_L(h)) |h>_hard U_h |psi>_soft.
```

This is an isometry because:

```text
sum_h p_L(h) U_h^dagger U_h = I.
```

Properties:

```text
1. soft capacity is minimal;
2. shell information is encoded across hard-soft correlations;
3. hard radiation is approximately thermal when random-unitary coherences are
   small;
4. no oversized archive is available.
```

The hard reduced state has off-diagonal terms:

```text
rho_hh' = sqrt(p_h p_h') <psi| U_h^dagger U_h' |psi>.
```

For large shell dimension and random `U_h`, these coherences should be small
for typical states. This is a decoupling-style mechanism, not exact storage.

## Why Level 2 Matters

Level 1 can always work because it stores all information in an enlarged soft
register.

Level 2 asks a sharper question:

```text
Can the same shell-sized soft record make hard radiation thermal-ish while
preserving unitarity?
```

If yes, the hard/soft split is less archive-like.

## Diagnostics

For a sequence:

```text
L0 -> L0 - 1 -> ... -> 1
```

track:

```text
S(core)
S(all radiation)
S(hard radiation only)
S(soft radiation only)
I(early hard : late hard)
I(early hard+soft : late hard+soft)
hard-state distance from target thermal distribution
```

Expected:

```text
S(core) = S(all radiation)
```

for a globally pure simulation.

The distinction is:

```text
hard radiation can be thermal-ish and information-poor,
while hard+soft radiation purifies the shrinking core.
```

## First Diagnostic Script

Script:

```text
sim/erosion_channel_diagnostic.py
```

It compares:

```text
level1_archive
level2_minimal_soft
```

on small droplets where full state vectors are still manageable.

This is not yet a local Hamiltonian. It is the first information-flow test of
the proposed hard/soft erosion channel.

