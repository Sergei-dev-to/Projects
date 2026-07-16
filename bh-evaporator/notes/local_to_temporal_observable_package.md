# Local-to-Temporal Information: Observable Package

Date: 2026-07-12

Status: **finite control verified; retained technical interface**. This note
consolidates the C1 control and states the measurements a named evaporation
process would have to supply. Applying the interface to a top-down emitter is
successor research rather than unfinished program work.

## 1. Exact finite control

Use the perfect `[[5,1,3]]` code as a one-qubit diary encoded into five emitted
degeneracy modes. Append to each mode the same independent thermal energy
qubit with excited probability `1/3`, so every wave packet has the same local
state

```text
rho_one = diag(2/3,1/3)_energy tensor I_2/2_degeneracy.
```

The existing support calculation gives:

```text
any one emitted mode:  I(Q:R_A) = 0,
any two modes:         I(Q:R_A) = 0,
any three modes:       I(Q:R_A) = 2 log 2,
full mixing record:    I(Q:R)   = 2 log 2,
blind product record:  I(Q:R)   = 0.
```

The numerical checks run on 2026-07-12 returned code-isometry error
`2.3e-16`, maximum one-mode code defect `3.1e-16`, and the exact three-mode
threshold to numerical precision. The shrinking-shell check also returned
the same thermal probability `1/3` on every branch and blind mutual
information below `7.1e-16`.

This proves only a kinematic point: local thermal-looking records can be
identical while multitime correlations carry the diary. It is not an
autonomous Hamiltonian and does not derive the encoder from gravity.

## 2. Required physical-emitter calculation

For a named completion, fix:

```text
diary code D and reference Q;
accessible radiation algebra A_R;
one-wavepacket record R_j;
two- and higher-record algebras R_[1:K];
hidden daughter/partner complement X_K;
energy, charge, detector, and control restrictions.
```

Then calculate, at each step and for the accumulated record:

```text
local distinguishability:
  sup_rho,sigma ||N_j(rho)-N_j(sigma)||_1;

local blindness:
  inf_Cj blind ||N_j-C_j|| on the declared code;

multitime access:
  I(Q:R_[1:K]), coherent information, or strategy distance;

direct recovery:
  best decoder fidelity and first K at which it crosses the target;

decoupling:
  ||rho_(Q X_K)-rho_Q tensor rho_XK||_1;

charge/payload split:
  repeat all quantities after fixing the asymptotic charge sector.
```

The comparison must include a blind completion with the same local data and
the same shell trajectory. A local no-go is meaningful only if it is stated
against that comparison; a positive multitime result is meaningful only if it
also decouples the hidden complement.

## 3. Interpretation rules

```text
local blindness + multitime access:
  correlation-only export; compatible with the control and not a paradox;

order-one cumulative Q2 defect + no decoupling:
  access to some direction, not sufficient recovery of the diary;

decoupling + a decoder:
  recovery-grade export;

one-mode distinguishability:
  local leakage, not evidence for a universal black-hole mechanism;

charge-only distinguishability:
  metadata/header access, not fixed-charge payload access.
```

The scalar cumulative distance from a blind comb is a necessary recovery
condition, not a sufficient one. The physical target is directional temporal
mixing or a direct complementary-channel decoupling estimate.

## 4. What remains genuinely open

The exact code control should not be expanded into more abstract encoders. The
remaining positive target is one of:

1. derive the same local/multitime separation from a natural time-independent
   Hamiltonian with a shrinking shell and thermal emission;
2. prove a process-ETH, approximate-design, or equivalent second/fourth-moment
   condition for a named microscopic emitter;
3. show that a proposed gravity model selects a different accessible algebra
   in which the fixed-charge test changes.

Until one of these is done, the control establishes the logical separation but
not a gravitational information-export result.
