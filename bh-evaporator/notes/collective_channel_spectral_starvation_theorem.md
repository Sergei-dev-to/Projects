# Collective-Channel Spectral Starvation Theorem

Date: 2026-07-09

Status: first theorem-class derivation. Exact for the stationary,
linear, number-conserving Gaussian class with additive internal and
exterior self-energies. This removes the time-local Markov assumption
from `collective_channel_starvation_result.md`. It does not yet close
signed cancellation, nonlinear/non-Gaussian refill, or the full
ordinary-sector Gram tail.

Successor scope correction (2026-07-09): “Gaussian” here means passive,
gauge-invariant, number-conserving Gaussian with no anomalous self-energy.
`anomalous_parametric_channel_result.md` constructs an active Gaussian channel
with Hawking flux, positive absorption, exact calibrated response, and `g2=2`
that has no passive occupation to starve.  The theorem below remains exact in
its class but cannot represent the full Bogoliubov Hawking mechanism without
an active-channel extension.

Role in the necessity trinity: this note targets input 2 only,

```text
N_access(omega) ~ S,
```

by bounding the flux that a rank-one thermal collective eigenchannel
can hide at a calibrated line. It does not derive the Schwarzschild
state count (input 1) or decoupling (input 3).

## 1. Statement in One Line

For a stationary linear collective mode coupled additively to an
internal calibrated thermal environment and an exterior vacuum drain,
the exact frequency-local distribution is

```text
n_eff(omega)
  = Gamma_int(omega) n_ref(omega)
    / [Gamma_int(omega) + Gamma_out(omega)].
```

Consequently the line response is always below the internal calibrated
ratio when `Gamma_out > 0`, and the outgoing spectral number current is
fixed by the measured deficit and the internal relaxation spectrum:

```text
j_out(omega)
  = A(omega) Gamma_int(omega) n_ref(omega)[n_ref(omega)+1]
    delta_-(omega)
    / {2 pi [1+n_ref(omega) delta_-(omega)]}.
```

This is the spectral-starvation identity. No Planckian inequality is
used. A QNM/Planckian ceiling on `Gamma_int` is a later application.

## 2. Scope and Definitions

### 2.1 Effective channel

Take one resolved Gram eigenchannel represented by a bosonic mode `b`
with a linear number-conserving effective Hamiltonian

```text
H = omega_0 b^dag b
  + H_int-bath + H_out-bath
  + sum_q (v_q b^dag a_q + v_q^* a_q^dag b)
  + sum_k (u_k b^dag c_k + u_k^* c_k^dag b).
```

The `a_q` environment is the internal refill sector. Its stationary
correlators obey the calibrated detailed-balance ratio at the line.
The `c_k` environment is the outgoing radiation sector and is empty on
the incoming leg. Both environments are Gaussian and gauge invariant;
there are no anomalous/squeezed self-energies.

This Hamiltonian is a convenient dilation. The derivation below only
uses its exact additive retarded, lesser, and greater self-energies.
Therefore a more complicated microscopic model lies in scope if its
effective channel closes the same linear Dyson/Keldysh relations.

### 2.2 Self-energies and widths

Write

```text
Sigma^R = Sigma_int^R + Sigma_out^R,
Gamma_a(omega) = -2 Im Sigma_a^R(omega) >= 0,
a in {int,out}.
```

The real parts `Delta_a = Re Sigma_a^R` shift and distort the line but
do not enter the frequency-local distribution ratio. Additivity is
load-bearing. Interfering baths or a non-additive vertex lie outside
the theorem.

The exact retarded Green function is

```text
G^R(omega)
  = 1/[omega-omega_0-Sigma_int^R(omega)-Sigma_out^R(omega)],
```

with spectral function

```text
A(omega) = -2 Im G^R(omega)
         = |G^R(omega)|^2 [Gamma_int(omega)+Gamma_out(omega)]
```

when no additional non-dissipative pole contribution is omitted.

### 2.3 Calibrated internal detailed balance

Let the internal environment satisfy

```text
Sigma_int^<(omega) = -i Gamma_int(omega) n_ref(omega),
Sigma_int^>(omega) = -i Gamma_int(omega) [n_ref(omega)+1].
```

For canonical KMS,

```text
n_ref = 1/[exp(beta omega)-1],
R_omega = n_ref/(n_ref+1) = exp(-beta omega).
```

For a finite microcanonical shell, use the calibrated ratio

```text
R_omega = rho(E-omega)/rho(E),
n_ref = R_omega/(1-R_omega),
```

provided the internal lesser/greater self-energies obey that generalized
detailed-balance relation in the resolved wave packet. The theorem uses
the relation, not canonical ensemble equivalence.

The exterior incoming state is vacuum:

```text
Sigma_out^<(omega) = 0,
Sigma_out^>(omega) = -i Gamma_out(omega).
```

Population-inverted/superradiant reference ratios require a separate
sign convention and are outside this first statement.

### 2.4 Measured response deficit

Define the effective frequency-local distribution by

```text
G^<(omega) = -i A(omega) n_eff(omega),
G^>(omega) = -i A(omega)[n_eff(omega)+1].
```

The emission/absorption response ratio is

```text
r_eff(omega) = n_eff(omega)/[n_eff(omega)+1].
```

Define the relative LOW-side deficit

```text
delta_-(omega) = 1-r_eff(omega)/R_omega.
```

This is a pointwise or resolved-wave-packet quantity. An aggregate ratio
over unresolved channels can contain signed cancellation and is not
automatically `delta_-` for each Gram eigenchannel.

## 3. Theorem: Exact Spectral Starvation

**Theorem.** Under the assumptions of section 2, at every frequency
where `A > 0`, `Gamma_int > 0`, and the stationary Dyson/Keldysh
solution exists,

```text
n_eff
  = Gamma_int n_ref/(Gamma_int+Gamma_out),                    (3.1)

r_eff/R_omega
  = (n_ref+1)/(n_ref+1+x),                                   (3.2)

delta_-
  = x/(n_ref+1+x),                                           (3.3)

x = Gamma_out/Gamma_int.                                    (3.4)
```

Thus nonzero exterior drain gives a strictly LOW-side calibrated
response whenever the internal reference has `0 < R_omega < 1`.

### Proof

For a linear stationary Gaussian problem, the exact Keldysh equations
are

```text
G^< = G^R [Sigma_int^< + Sigma_out^<] G^A,
G^> = G^R [Sigma_int^> + Sigma_out^>] G^A.
```

Using the self-energies of section 2,

```text
i G^<
  = |G^R|^2 Gamma_int n_ref,

i G^>
  = |G^R|^2 {Gamma_int(n_ref+1)+Gamma_out}.
```

The spectral identity gives

```text
A = i(G^>-G^<)
  = |G^R|^2(Gamma_int+Gamma_out).
```

Dividing `iG^<` by `A` proves (3.1). Substituting (3.1) into
`r_eff=n_eff/(n_eff+1)` gives

```text
r_eff = n_ref/[n_ref+1+x].
```

Dividing by `R_omega=n_ref/(n_ref+1)` proves (3.2), and subtracting from
one proves (3.3). No flat-spectrum approximation was used. The real
self-energy shifts remain inside `G^R` and cancel from the ratio.

## 4. Corollary: Exact Flux-versus-Deficit Identity

The outgoing spectral number current into the empty radiation bath is

```text
j_out(omega)
  = Gamma_out(omega) [iG^<(omega)]/(2 pi)
  = A Gamma_out n_eff/(2 pi).                                (4.1)
```

Invert (3.3):

```text
x = delta_-(n_ref+1)/(1-delta_-).                            (4.2)
```

Then

```text
x/(1+x)
  = delta_-(n_ref+1)/[1+n_ref delta_-].                      (4.3)
```

Using `Gamma_out n_eff = Gamma_int n_ref x/(1+x)` in (4.1) yields

```text
j_out(omega)
  = A(omega) Gamma_int(omega)
    n_ref(omega)[n_ref(omega)+1] delta_-(omega)
    / {2 pi [1+n_ref(omega) delta_-(omega)]}.                (4.4)
```

Equation (4.4) is exact in the theorem class. If a resolved detector
establishes `0 <= delta_- <= eta_-`, then monotonicity gives

```text
j_out(omega)
  <= A Gamma_int n_ref(n_ref+1) eta_-
     / {2 pi [1+n_ref eta_-]}.                               (4.5)
```

For a detector wave packet `B` on which the assumptions hold pointwise,

```text
Ndot_out(B)
  <= integral_B d omega/(2 pi)
       A Gamma_int n_ref(n_ref+1) eta_-
       / [1+n_ref eta_-].                                   (4.6)
```

If additionally `Gamma_int <= Gamma_max` and the remaining factors have
known extrema on `B`, (4.6) gives the earlier parametric starvation
bound. Setting `Gamma_max = c_P T` is a black-hole/many-body application
hypothesis, not part of this theorem.

## 5. Markovian Limit [recovery check]

Take constant widths near a narrow line,

```text
Gamma_int(omega) = Gamma_th,
Gamma_out(omega) = Gamma',
n_ref(omega) = nbar_T.
```

The equal-time occupation is then

```text
n* = Gamma_th nbar_T/(Gamma_th+Gamma'),
```

and

```text
1-r*/r_KMS
  = x/(nbar_T+1+x),
x = Gamma'/Gamma_th,
```

exactly reproducing `collective_channel_starvation_result.md` and
`sim/collective_channel_starvation_check.py`.

## 6. Counting Statistics

The total Hamiltonian and both bath states are Gaussian and gauge
invariant. The reduced stationary state of the single mode is therefore
a zero-mean, unsqueezed Gaussian state. Wick's theorem gives

```text
<b^dag b^dag b b> = 2 <b^dag b>^2,
g2(0) = 2.
```

This remains true with frequency-dependent memory kernels. A coherent
drive, anomalous/squeezed self-energy, or nonlinear non-Gaussian refill
can move `g2`; those mechanisms leave the theorem class and acquire
additional observables rather than invalidating (3.1) inside its scope.

## 7. What the Theorem Does and Does Not Close

### Closed

```text
time-local Markovianity is unnecessary;
arbitrary frequency dependence of additive Gaussian bath kernels is allowed;
real dispersive shifts do not hide starvation in a resolved response ratio;
the outgoing spectral flux is exactly tied to the LOW-side deficit and
  Gamma_int.
```

### Still open

```text
signed cancellation between HIGH occupation-enhanced and LOW starved channels;
operational reconstruction of Gram eigenchannel-resolved response;
unequal same-line multiplexing and the full ordered Gram tail;
overlapping/unresolved wave packets;
non-additive or interfering self-energies;
nonlinear/non-Gaussian collective refill;
population-inverted/superradiant reference channels;
operator-specific identification of Gamma_int for a real black hole.
```

The first five are Phase-2 proof obligations. The last black-hole item
is the Phase-3 QNM gate. None should be hidden inside a generic
Planckian statement.

## 8. Operational Interpretation

There are three evidentiary levels:

```text
theorem level:
  use independently calibrated Gamma_int(omega) and Gamma_out(omega);

black-hole corollary level:
  identify the collective operator and derive Gamma_int from its
  retarded correlator/QNM structure;

motivation only:
  invoke generic Planckian dissipation.
```

The total observed linewidth cannot be substituted for `Gamma_int`
unless additive self-energies hold and `Gamma_out` is independently
known. If the split cannot be identified, (4.4) remains a conditional
model-side identity rather than an exterior certificate.

## 9. Consequence for the Necessity Trinity

This theorem does not yet remove input 2. It removes one technical
escape from its proposed exterior certification:

```text
a stationary linear Gaussian collective source cannot carry persistent
resolved-line flux while remaining exactly calibrated unless its internal
refill spectrum dominates the exterior drain.
```

Input 2 becomes derived only after:

```text
signed cancellation is closed or included in the bound;
the full ordinary Gram tail is controlled;
the relevant response/width data are operationally identifiable;
and the resulting participation floor reaches N_access ~ S.
```

Input 1 (`S(E) ~ E^2`) and input 3 (decoupling/typical encoding) remain
separate supplied structures.

## 10. Verification and Next Step

Required support script:

```text
sim/spectral_starvation_check.py
```

It should verify (3.1)--(4.4) for strongly frequency-dependent positive
widths and arbitrary dispersive shifts, then recover the constant-width
Lindblad limit.

After that check, stop the single-channel phase and move to the signed-
cancellation/full-spectrum optimizer. Do not begin the black-hole/QNM
literature gate before Phase 2 fixes what observable the corollary must
actually bound.

## Discipline

- Say "stationary linear Gaussian spectral theorem," not generic
  non-Markovian no-go.
- Keep `Gamma_int`, `Gamma_out`, and `Gamma_tot` separate.
- Do not call `Gamma_int <= c_P T` part of the theorem.
- Do not infer channelwise LOW deficits from one aggregate line ratio.
- Do not claim input 2 is removed until the ordinary Gram tail and
  operational-identifiability gates close.
- Keep the Markovian calculation as a verified limit, not the main
  theorem.
