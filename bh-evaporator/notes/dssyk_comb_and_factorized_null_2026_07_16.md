# DSSYK Comb and Matched Factorized Null

Date: 2026-07-16

Status: **superseded for active use** by
`observer_relative_temporal_access_successor_proposal_2026_07_16.md`.
Retained as an audit record; no DSSYK calculation was performed from it. Its
assumption `Omega_eq(E) = rho_DSSYK(E)^2` is incorrect for the
Narovlansky--Verlinde same-disorder paired physical Hilbert space, and the
three-dimensional transport envelope is not the primary isospectral control.

This note closes the first concrete part of the successor gate. The object to
be compared is a finite observer comb, not a one-time correlator.

## 1. Historical incorrect microcanonical data (do not use)

This section records the assumption that caused the route to be superseded.
Equation (1.1) is false for the same-disorder diagonal paired physical space;
the corrected one-copy measure is specified in the active successor proposal.

Let `E` label the energy bins used by the doubled equal-energy model. If
`rho_DSSYK(E)` is the one-copy density of states, the equal-energy shell has

```text
Omega_eq(E) = rho_DSSYK,L(E) rho_DSSYK,R(E)
             = rho_DSSYK(E)^2                         (1.1)
```

up to the chosen bin widths and any exact constraint multiplicity. The control
must reproduce the whole function `Omega_eq(E)` over the tested shell, not
only its value and first derivative at one operating point. Thus it matches
the density of states and the shell shape, including the finite-size
corrections that would otherwise masquerade as access.

Define a control reservoir `Q_mc` with Hamiltonian `H_Q` satisfying

```text
dim Pi_Q(E) = Omega_eq(E)                               (1.2)
```

for every tested bin. The DSSYK and control runs use the same total-energy
shell, bin widths, initial shell state, clock schedule, observer memory, record
registers, and intervention times. Their record marginals after the diary is
removed are required to agree:

```text
p_DSSYK(r_1,...,r_K | diary removed, E)
  = p_mc(r_1,...,r_K | diary removed, E).                (1.3)
```

Matching only `(S_0,T)` is explicitly not admissible.

## 2. Observer comb

For bins `j = 1,...,K`, use a clock register `C`, observer memory `M_j`, and
record bin `R_j`. A time-binned observer step is a channel

```text
Phi_j : Q tensor D tensor M_(j-1) tensor C
        -> Q tensor D tensor M_j tensor C tensor R_j.    (2.1)
```

The channel includes the declared interaction during bin `j`, the clock
advance or clock-conditioned intervention, and the measurement instrument
that deposits `R_j`. The observer memory is retained between bins; the comb is
therefore allowed to be non-Markovian. The allowed input set is the code and
the common energy shell, with an arbitrary reference `A` retained in the
hybrid comparison.

The diary-blind comparison uses the same interfaces and schedule,

```text
Psi_j : Q tensor D tensor M_(j-1) tensor C
        -> Q tensor D tensor M_j tensor C tensor R_j,    (2.2)
```

but its contact interaction is replaced by the label-scrambled/removed one.
The comparison is made on the same shell and with the same diary-removed
record marginal. It is not enough to match each single-bin record state: the
whole sequential process, including memory and clock correlations, must be
diary blind.

For each hybrid-reachable state `sigma` define

```text
eta_j = sup_sigma ||[(Phi_j-Psi_j) tensor id_(A R_<j)](sigma)||_1.  (2.3)
```

Result B then gives

```text
||N_K-C_K||_(code,diamond) <= D_K,
D_K := sum_(j=1)^K eta_j.                              (2.4)
```

This `D_K` is the registered access defect. A recovery claim requires an
order-one cumulative defect against every diary-blind comparison comb.

## 3. Strict factorized control: exact null curve

The strict factorized control is not a claim about an ordinary local contact
reservoir. It is the clean bookkeeping null. Let the diary be a spectator and
let the observer comb act only on `Q_mc`, `M`, and `C`:

```text
Phi_j^0 = I_D tensor Gamma_j^mc,
Psi_j^0 = Phi_j^0.                                      (3.1)
```

Here `Gamma_j^mc` is any shell-preserving sequential reservoir/observer
instrument obeying (1.2)--(1.3). For every hybrid-reachable state, including
states entangled with a reference,

```text
[(Phi_j^0-Psi_j^0) tensor id](sigma) = 0,
eta_j^0 = 0,
D_null^strict(K) = 0   for every K.                    (3.2)
```

This is an exact result, not a large-entropy approximation. The microcanonical
matching matters because it proves that the zero is not caused by changing the
DOS, temperature, energy shell, or record schedule. It is the pre-registered
answer for the strictly diary-blind factorized control.

## 4. Ordinary-contact control: what remains to be instantiated

The physical factorized foil has a source-contact Hamiltonian rather than the
spectator idealization. Once its contact generator `V_j^mc` and the
diary-removed generator `V_j^0` are declared on the common shell, the
Hamiltonian corollary of Result B gives the registered bound

```text
eta_j^contact <= 2 |g_j|
  ||V_j^mc - V_j^0||_(cb, shell),                       (4.1)

D_null^contact(K) <= 2 sum_(j=1)^K |g_j|
  ||V_j^mc - V_j^0||_(cb, shell).                       (4.2)
```

For a local reservoir with the diary initially a distance `d` from the
contact, a Lieb--Robinson or transport estimate can be substituted for the
shell-restricted norm; schematically the early-bin contribution is suppressed
until the transport time `d/v`. That estimate is not yet a number because the
contact geometry, clock bin width, and diary placement have not been fixed.
It must be fixed before calling the ordinary-contact curve closed.

The program's existing local-reservoir estimate supplies the scale once those
choices are made. For a diary block `B` at distance `L` from a contact region
`partial Lambda`, a finite-range model gives the early-time envelope

```text
eta_j^contact <= min(2,
  c0 exp(2k) |B| |partial Lambda|
  exp(-(L-v t_j)/xi)),                                    (4.3)

D_null^contact(K) <= sum_(j=1)^K eta_j^contact.             (4.4)
```

Here `k` is the diary entropy, `t_j` is the end of bin `j`, and the constants
are fixed by the declared contact model. With thermal-cell volume held fixed,
`S ~ L^d`, so the ballistic onset is `K ~ S^(1/d)` bins (and a diffusive
ordinary-reservoir realization gives the expected `K ~ S^(2/d)` scale). This
is a transport envelope, not an equality: the control's exact curve is
obtained by evaluating its declared contact instrument, while (4.4) is the
pre-registered upper bound that any such realization must obey before the
light cone reaches the diary.

For the first comparison, freeze the following ordinary-contact convention:
three spatial dimensions, one bin per DSSYK thermal time (`Delta t = beta`),
thermal-cell entropy `s_cell = O(1)`, and a diary block in the bulk. Set

```text
L(E) = (S_eq(E)/s_cell)^(1/3),
|partial Lambda(E)| = c_partial S_eq(E)^(2/3),

b_j(E) = min(2,
  c0 exp(2k) |B| c_partial S_eq(E)^(2/3)
  exp(-(L(E)-v j beta)/xi)),

B_null^contact(K;E) = sum_(j=1)^K b_j(E).              (4.5)
```

The control reservoir is required to realize the exact shell multiplicity
`Omega_eq(E)` while obeying this finite-range transport convention. If no such
realization is available for the chosen shell, the comparison is declared
unmatched and the DSSYK test stops; the DOS cannot be silently relaxed to save
it. `B_null^contact`, rather than an after-the-fact fitted curve, is the
benchmark the constrained model must beat.

Writing `A(E) = c0 exp(2k) |B| c_partial S_eq(E)^(2/3)` and
`q = exp(v beta/xi)`, the unsaturated part of the registered envelope is the
geometric sum

```text
B_null^contact(K;E)
  <= A(E) exp(-L(E)/xi) q (q^K-1)/(q-1),                (4.6)
```

until `A(E) exp(-(L(E)-v K beta)/xi)` reaches `2`; afterwards each additional
bin contributes at most `2`. This makes the pre-registered distinction
explicit: the ordinary contact control has a transport onset at
`K = O(S_eq^(1/3))` in the ballistic convention, while the strict factorized
control remains exactly zero.

Therefore the current gate has two honest nulls:

1. the exact strict factorized curve (3.2), already derived;
2. the ordinary-contact curve (4.2)--(4.4), whose contact realization and
   constants are the next bounded control deliverable.

The DSSYK curve cannot be interpreted against the strict zero alone. A
nonzero constrained signal beats (3.2) trivially; it is interesting only if it
also beats the instantiated ordinary-contact curve under the same
microcanonical data.

## 5. Stop rule for the next calculation

Before evaluating any DSSYK correlator, choose the contact geometry and write
the numerical or asymptotic form of (4.2). If that choice cannot be made
without importing a diary-sensitive record algebra, the successor stops at the
definition gate. If it can be made, evaluate the factorized control first and
freeze its curve. Only then is the equal-energy DSSYK comb evaluated.
