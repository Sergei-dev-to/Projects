# DSSYK WP1: Isometric, Charge, and Twirl Controls

Date: 2026-07-16

Status: **completed formal control package**. The unrestricted and exactly
transported DSSYK comparison is an exact null. Charge-only access is proved to
be metadata access, and the same-shell diary twirl is an exact blind control.
The remaining nontrivial question is resource-relative implementability, not
Hilbert-space capacity.

This note uses the full trace norm and full diamond norm, both ranging from
`0` to `2`, consistently with `q2_composable_diary_access_theorem.md`.

## 1. Isometric no-free-access theorem

Let `H` and `H'` be Hilbert spaces and let

```text
W: H -> H'                                                (1.1)
```

be an isometry onto the declared physical subspace. Let `V:D->H` encode a
diary. A `K`-step protocol consists of CPTP maps with retained system memory
and fresh record outputs,

```text
Phi_j: H tensor M_(j-1) -> H tensor M_j tensor R_j.       (1.2)
```

Transport the encoder and every system leg by `W`:

```text
V' = W V,
Phi'_j = (Ad_W tensor id_(M_j R_j))
         o Phi_j
         o (Ad_(W^dagger) tensor id_(M_(j-1))).          (1.3)
```

On the physical image, `Ad_(W^dagger)` is trace preserving. Extensions away
from that image are irrelevant because no allowed input reaches them.

### Theorem

The two protocols induce the same diary-to-record channel:

```text
N_K' = N_K.                                               (1.4)
```

If the allowed protocol class, diary-blind comparison class, and decoders are
transported by the same isometry, then all of the following are equal:

```text
pairwise record distinguishability delta_K;
restricted code-diamond distance to diary blindness;
the cumulative Result-B quantity A_K;
optimal classical error and quantum recovery fidelity;
C_obs(K,epsilon;P).                                      (1.5)
```

### Proof

Insert (1.3) at each step. Every adjacent `W^dagger W` cancels. The remaining
`W` acts only on the final hidden system and disappears under its partial
trace, leaving exactly the same joint record state for every diary-reference
input. This proves (1.4), including reference-assisted inputs. Trace and
diamond norms are invariant under isometric conjugation. Transport maps
diary-blind combs bijectively to diary-blind combs and preserves every
hybrid-reachable step defect `eta_j`; taking the infimum preserves `A_K`.
Transporting a decoder gives the same recovered state, proving the remaining
claims. QED.

### DSSYK corollary

For a shared-disorder spectrum made nondegenerate by fixing a common symmetry
sector,

```text
W|E_i> = |E_i>_L|E_i>_R                                (1.6)
```

is unitary from one DSSYK onto the equal-energy physical Hilbert space.
Therefore the constraint, the paired notation, and the one-copy physical DOS
cannot alone change any recovery or access capacity. In particular, the exact
one-copy control obtained from

```text
A_one = W^dagger A_phys W                               (1.7)
```

has the same complete `K`-record channel as the doubled protocol.

If an energy has multiplicity `g_E>1`, the full equal-energy kernel has
multiplicity `g_E^2`. The corollary then applies to a declared diagonal paired
subspace, or sector by sector after an additional pairing or gauge fixing; it
does not identify that larger kernel with one copy automatically.

Any difference must be a statement about a non-isometrically transported
resource restriction: which operators are simple, buildable, low-cost, or
available to a specified observer.

## 2. Charge control: exact metadata/payload split

Let a finite constrained system decompose into charge sectors

```text
H = direct_sum_q H_q,                                    (2.1)
```

and define the charge-record channel

```text
N_Q(rho) = sum_q Tr(P_q rho) |q><q|_R.                  (2.2)
```

For states supported in distinct sectors `q!=q'`,

```text
delta_Q = (1/2)||N_Q(rho_q)-N_Q(rho_q')||_1 = 1.         (2.3)
```

The public charge is perfectly available. Within a fixed sector,

```text
N_Q(rho) = |q><q|_R for every rho supported in H_q,      (2.4)
```

so every pair of fixed-charge payload states has `delta_Q=0` and the channel
is exactly diary blind on that payload code. If `dim H_q=d`, feeding half of
a maximally entangled payload state and applying any decoder to the constant
record gives entanglement fidelity at most

```text
F_e <= 1/d^2.                                            (2.5)
```

Equation (2.2) is therefore pure metadata access: order-one visibility of a
constraint label with zero fixed-sector payload access. It calibrates the
metadata branch of the successor's trichotomy.

## 3. Same-shell twirl control

For a `d`-dimensional shell code, let

```text
T_D(rho) = integral dU U rho U^dagger = I_D Tr(rho)/d,   (3.1)
C_K^twirl = N_K o T_D.                                  (3.2)
```

`C_K^twirl` uses the same shell and observer instrument as `N_K` and is exactly
diary blind. Hence every pairwise witness evaluated on the control vanishes:

```text
delta_K(C_K^twirl)=0.                                   (3.3)
```

For any two code states with actual outputs `sigma_0,sigma_1`, define

```text
delta_K = (1/2)||sigma_0-sigma_1||_1.                   (3.4)
```

For every blind channel `C_K`, whose output on the code is one state `omega`,
the triangle inequality gives

```text
||N_K-C_K||_(code,diamond) >= delta_K.                  (3.5)
```

This uses the full diamond norm. With the normalized convention
`(1/2)||.||_diamond`, the right side would be `delta_K/2`.

For the binary *classical* diary fixed in WP0, write the cq record channel as
`b -> sigma_b`. The uniform classical twirl outputs
`bar_sigma=(sigma_0+sigma_1)/2`. Directly,

```text
||N_K^cq-C_K^twirl||_diamond = delta_K.                 (3.6)
```

Thus the twirl saturates the universal pairwise lower bound in this binary cq
case. For a coherent quantum diary, (3.5) remains valid but (3.6) need not:
coherent inputs and references can reveal a larger channel distance.

The twirl is a channel-level blind control. It does not by itself provide a
stepwise decomposition minimizing Result B's `A_K`; that remains a separate
comb optimization.

## 4. Control table

| control | spectrum/shell | allowed protocol | public label | private code | exact witness |
| --- | --- | --- | --- | --- | --- |
| transported one-copy DSSYK | identical to equal-energy physical spectrum and WP0 shell | exact isometric transport of every step | identical | identical | complete record channel, `delta_K`, `A_K`, and recovery all equal |
| unrestricted relational algebra | same | all `B(H_0^S)` relationally dressed | any measurable label | no algebraic restriction protects payload | no constraint advantage; isometric null applies |
| charge record | arbitrary fixed charge sectors | measure sector projector only | `q`, with `delta=1` across sectors | all states within fixed `q` | `delta=0` within sector; `F_e<=1/d_q^2` |
| same-shell twirl | exactly the actual shell | same instrument after input twirl | shell metadata unchanged | all diary directions erased | control `delta=0`; binary cq actual-to-control diamond distance equals actual `delta` |
| NV-simple detector versus one-copy-simple detector | same physical spectrum | restricted operator families not related by exact transport | energy/clock matched | WP0 phase bit | scientifically open only after a common implementation-cost rule is fixed |

## 5. Consequence for the successor program

WP1 rules out the following proposed mechanism:

```text
equal-energy constraint + paired representation + full relational algebra
  => new diary access.                                  (5.1)
```

It leaves open a narrower mechanism:

```text
the constraint changes the cost or simplicity of implementing a
code-sensitive temporal record, relative to a pre-registered one-copy
resource class.                                         (5.2)
```

Equation (5.2) is closer to the original operational-cutoff question, but it
requires a resource theory. Before WP2, choose one common cost measure, for
example:

```text
word length in the declared simple matter/chord generators;
number and scaling dimensions of allowed insertions;
integrated detector coupling and number of record contacts;
operator/Krylov complexity with a fixed generator set.  (5.3)
```

The measure must be defined on both sides and must not assign a lower cost to
the desired doubled operator by fiat. Until then, a nonzero NV-detector
`delta_K` would show only that the chosen operator sees the phase code, not
that the cosmological constraint supplies an operational cutoff or access
advantage.

## 6. Verification artifact

`sim/dssyk_wp1_controls.py` numerically checks, on finite random channels:

1. equality of two-step record states under exact isometric transport;
2. perfect charge-header visibility and zero fixed-sector payload visibility;
3. the binary cq twirl identity (3.6).

The script is a finite linear-algebra regression test for the formal controls,
not a DSSYK dynamics simulation.
