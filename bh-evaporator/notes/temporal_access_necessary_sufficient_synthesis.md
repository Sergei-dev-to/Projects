# Temporal Access: Necessary/Sufficient Demarcation Bracket

Date: 2026-07-10

Status: synthesis theorem stack. The necessary side is the new composable Q2
bound; the sufficient side is the existing ETH/design decoupling derivation,
rewritten around the invariant physical emission process rather than a
microscopic source list. This closes the conditional finite-model demarcation.
The remaining problem is to derive or verify the sufficient process condition
in a microscopic gravity emitter.

## 1. Invariant Objects

Let `N_K` be the physical channel from a diary code to the exterior record
through evaporation step `K`. Two different questions require two different
process quantities.

### Necessary access quantity

```text
A_K = inf_(C_K diary blind) sum_(j<=K) eta_j,              (1.1)
```

where `eta_j` is the actual-versus-blind step defect on all
hybrid-reachable states. The composable theorem gives

```text
distance(N_K, diary-blind channels) <= A_K.               (1.2)
```

Reliable recovery requires `A_K=O(1)`.

### Sufficient mixing quantity

For diary reference `Q`, remaining hidden system `B_K`, and record `R_K`, use

```text
D_K = ||rho_(Q B_K)-rho_Q tensor rho_(B_K)||_1.           (1.3)
```

Small `D_K` is equivalent, up to standard information-disturbance continuity
bounds, to recovery of the diary from `R_K`.

`A_K=O(1)` is not sufficient for small `D_K`: a channel can expose one charge,
dephase the diary, or repeatedly sample one direction. The missing condition is
directional/isotropic temporal mixing of the physical emission process.

## 2. Necessary Theorem

From `q2_composable_diary_access_theorem.md`, for arbitrary sequential
processes with shared memory, changing shell dimension, accumulated partners,
and reachable energy constraints,

```text
A_K=o(1)  =>  no order-one diary recovery by step K.      (2.1)
```

For Hamiltonian collisions, a sufficient upper bound is

```text
A_K <= 2 inf_blind sum_j |g_j| ||H_j-H_j^blind||,         (2.2)
```

with no exponential in the blind evolution budget.

## 3. Sufficient Theorem Already in the Program

`eth_decoupling_derivation.md` considers the actual energy-resolved jump
operators

```text
K_m : H_E -> H_(E-omega),                                (3.1)
```

including channel/frequency and waiting-time records. It assumes, sectorwise:

```text
E1. nondegenerate spectrum with controlled near resonances;
E2. ETH matrix elements for the physical K_m;
E3. fourth-moment factorization/freeness across record labels;
E4. the weak-coupling shell window;
E5. a shell-typical diary code.                           (3.2)
```

The resulting second-moment calculation gives

```text
E ||rho_(Q B_K)-rho_Q tensor rho_(B_K)||_1
  <= exp[-(S2_record-S_remaining-k)/2] + epsilon_ETH,      (3.3)
```

where `k=log dim diary` and `epsilon_ETH` contains the linewidth/shell,
connected-fourth-moment, envelope, and flat-rate errors. Thus

```text
S2_record >= S_remaining+k+w
and epsilon_ETH << 1
  => D_K <= exp(-w/2)+epsilon_ETH
  => diary recovery from the exterior record.            (3.4)
```

Approximate two-design or tensor-product-expander shell mixing supplies an
alternative standard sufficient hypothesis.

The important correction is what (3.2) applies to: the invariant physical jump
or process map, not an arbitrarily factorized list of microscopic boundary
sources. No static claim `N_access~S` is needed.

## 4. Closed Conditional Bracket

The finite-model demarcation is now:

```text
NECESSARY:
  order-one cumulative process distance from every diary-blind evaporation
  comb;

SUFFICIENT:
  physical jump-process second moments satisfy decoupling/ETH/design uniformly
  until the record entropy exceeds the remaining-shell-plus-diary entropy;

CONSEQUENCE:
  standard recovery, Page behavior, and complementary reconstruction.       (4.1)
```

No-hiding supplies an independent endpoint constraint:

```text
shrinking state count + unitarity + no entropy-sized hidden archive
  => eventual A_K=O(1),                                   (4.2)
```

but does not imply the sufficient condition (3.2) or locate its onset.

## 5. Exact Controls

```text
finite active pump:
  A_K=0 for all K; thermal energy/partner records; no diary flow;

blind shrinking shell:
  A_K=0 externally; lost dimension accumulates in a hidden archive;

weak erasure shell:
  A_K grows, but D_K remains large at weak access;

five-mode coded shell:
  every one- and two-mode record is diary blind, while any three-mode record
  has D_K=0 and recovers the logical diary;

ETH/design shell:
  generic rather than hand-coded route to D_K << 1 after the entropy threshold.
```

These controls show that emitted energy, record rank, cumulative access, and
decoupling are distinct axes.

## 6. What Gravity Must Supply

The conditional QI problem is closed once gravity supplies:

1. the shell state count and energy relation `S(E)~E^2`;
2. the physical exterior algebra and active emission instrument;
3. an actual jump-process moment structure satisfying (3.2), or an equivalent
   temporal decoupling/design condition;
4. the disposition of partners/hidden algebras needed to interpret no hiding.

Ordinary quantum information then supplies the recovery theorem. Gravity's
unresolved dynamical burden is item 3, not a static entropy-sized source rank.

## 7. Genuine Research Impasse

The next step cannot be selected by abstract channel reasoning alone. It
requires a microscopic target and its physical emission operator. The clean
options already present in the program are:

```text
Matrix/BFSS:
  compute the radiation-resolved detachment tensor
  K_ij^(mn)=sum_f A_(i->f,m) A*_(j->f,n)
  and test the ETH/design contractions;

holographic boundary theory:
  identify the dressed exterior emission algebra and test process moments in a
  controlled evaporating setup;

named many-body Hamiltonian surrogate:
  prove uniform full-ETH/freeness for its physical jump operators, a problem
  at least as hard as proving ETH for a deterministic chaotic Hamiltonian.
```

The Matrix route has the most concrete diagnostic but needs microscopic
amplitudes or new simulation data. The holographic route needs a model choice
and factorization prescription. The deterministic surrogate route encounters
the general open problem of proving ETH. Continuing without choosing one would
only add supplied mixers or circuit-to-Hamiltonian encodings and would no
longer advance the demarcation.

Phase-B successor: `bfss_detachment_feasibility_2026_07_10.md` gives a
conditional go for a design-stage small-`N` bosonic/BMN pilot, but a no-go for
claiming that a full BFSS information-export calculation is locally ready. The
pilot must establish a gauge-invariant separation algebra and a converged
clump/escape window before process-moment implementation.
