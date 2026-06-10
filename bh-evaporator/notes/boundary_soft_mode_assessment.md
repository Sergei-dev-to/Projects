# Boundary Soft Modes Assessment

## Question

Can boundary soft modes solve the microscopic-emission problem?

The problem after the golden-rule test was:

```text
small Hawking-like quanta work;
literal L -> L-1 shell removal is too energetic and exponentially suppressed.
```

So we want microscopic events with:

```text
omega ~ T_L ~ 1/L,
```

without losing:

```text
S_L ~ L^2,
M_L ~ L,
T_L ~ 1/L,
P_L ~ 1/L^2.
```

## Candidate Model

Use a three-layer droplet:

```text
H_L = H_bulk,L tensor H_edge,L tensor H_bath.
```

Bulk:

```text
dim H_bulk,L = q^(L^2)
S_bulk,L = L^2 log q.
```

Boundary tension:

```text
M_L = 4 sigma L.
```

Boundary soft modes:

```text
omega_n(L) = v n / L.
```

These can be acoustic, capillary-like, edge-CFT-like, or simply the low-energy
sector of a finite boundary qdit chain. The harmonic notation is only the
infrared approximation. For F1 purposes, the actual boundary system should be
finite and truncated.

## Why This Helps

At the droplet temperature:

```text
T_L = 2 sigma / (L log q),
beta_L = L log q / (2 sigma),
```

the dimensionless boundary-mode energy is:

```text
beta_L omega_n(L)
  = (L log q / 2 sigma) (v n / L)
  = v n log q / (2 sigma).
```

This is independent of `L`.

Therefore thermally active boundary quanta automatically have:

```text
omega_n ~ T_L ~ 1/L.
```

That is exactly what literal shell removal lacked.

## Diagnostic

Script:

```text
sim/boundary_soft_mode_diagnostic.py
```

Baseline:

```text
q = 2
sigma = 1
v = 1
two boundary branches
200 soft modes retained
2D exterior bath
L = 2 ... 100
```

The script computes:

```text
S_edge / S_bulk;
E_edge / M;
mean emitted omega / T;
golden-rule boundary-mode power.
```

For a `d`-dimensional exterior bath, the mode-level golden-rule power is:

```text
P_L ~ sum_n omega_n^d n_B(beta omega_n).
```

Since:

```text
omega_n ~ n/L,
beta omega_n independent of L,
```

the leading scaling is:

```text
P_L ~ L^(-d) ~ M^(-d).
```

So a 2D bath gives:

```text
P_L ~ M^-2.
```

## Results

Baseline 2D bath:

```text
power slope logP/logM: -2.0000
mean M^2 P last10: 1840.3841
mean S_edge last10: 15.0876
mean S_edge/S_bulk last10: 2.393135e-03
mean omega/T last10: 1.6213
```

3D bath control:

```text
power slope logP/logM: -3.0000
```

Velocity control `v=2`:

```text
power slope logP/logM: -2.0000
mean S_edge/S_bulk last10: 9.974054e-04
mean omega/T last10: 1.7933
```

So the scaling is robust:

```text
2D bath -> P ~ M^-2;
3D bath -> P ~ M^-3;
boundary quanta have omega = O(T);
edge entropy is subleading at large L.
```

## Important Caveat

Boundary soft modes solve the frequency problem, not the full energy-reservoir
problem.

At `T ~ 1/L`, the boundary thermal energy is small:

```text
E_edge ~ 1/L,
E_edge / M ~ 1/L^2.
```

So the boundary modes cannot be the entire mass reservoir for evaporation.

The correct interpretation is:

```text
boundary tension stores the coarse mass;
boundary soft modes provide microscopic small-frequency channels;
the bath drains energy through those channels;
after many emissions, the coarse droplet register updates L -> L-1.
```

This is not bad. It is close to the black-hole picture:

```text
Hawking quanta are soft compared with M;
the mass parameter changes gradually;
the horizon area/state-count register updates only coarse-grained.
```

But it means we still need an explicit coupling between:

```text
boundary tension / shape coordinate,
boundary soft modes,
exterior bath,
bulk constrained register.
```

## F1-F13 Assessment

```text
Feature   Status   Reason
F1        Y/P      finite if implemented as finite boundary qdit chain; harmonic
                  mode description is only the IR approximation.
F2        P        unitary bath coupling is straightforward, but full autonomous
                  evaporation is not built.
F3        P        shrinking state space remains a coarse register update.
F4        Y        bulk gauge count still gives S ~ L^2 and M ~ L.
F5        Y        T ~ 1/M and C < 0 unchanged.
F6        Y        2D bath plus soft modes gives P ~ M^-2.
F7        P+       microscopic omega ~ T emissions now exist; still need explicit
                  matrix elements from one Hamiltonian.
F8        P        radiation entropy bookkeeping plausible, not yet Page-tested
                  with many microscopic emissions.
F9        P        early/late correlations require bulk-to-boundary scrambling or
                  coupling; not automatic from edge modes alone.
F10       Y        still a non-gravitational control system.
F11       P        mode-level W = sum Gamma omega can now be computed naturally.
F12       N        not relevant to this branch.
F13       P+       emission is boundary-local in a natural sense; local-vs-scrambled
                  information transfer still needs testing.
```

The main upgrade is:

```text
F7 and F13 become more natural.
```

The main unchanged weakness is:

```text
F8/F9 are still not derived for microscopic emissions.
```

## Does This Make The Approach Better?

Yes, but only if we keep the roles distinct.

Bad interpretation:

```text
the boundary soft modes themselves are the black hole entropy and mass.
```

That fails because their entropy and energy are subleading.

Good interpretation:

```text
bulk constrained states provide the area entropy;
boundary tension provides the mass;
boundary soft modes provide small microscopic emission frequencies;
the exterior bath carries away energy;
bulk/boundary scrambling determines information flow.
```

This is a much better microscopic picture than literal shell deletion.

## Next Test

The next useful test is not another power-law diagnostic. The power law works.

The next test should be an information-flow diagnostic with many microscopic
events:

```text
bulk constrained register -> boundary soft mode -> hard bath quantum,
```

with scrambling/coupling varied between:

```text
1. no bulk-boundary scrambling;
2. local boundary coupling only;
3. scrambled bulk-to-boundary coupling.
```

Measure:

```text
hard radiation thermality;
hard-only early/late mutual information;
hard+soft or full-radiation purification;
coarse Page-like behavior.
```

That would tell us whether boundary soft modes only fix the energy scale, or
whether they also support the information-flow part of the program.
