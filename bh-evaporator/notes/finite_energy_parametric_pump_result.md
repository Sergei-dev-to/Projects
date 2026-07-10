# Finite-Energy Parametric Pump and the Surviving Access Question

Date: 2026-07-10

Status: exact repeated-interaction isometry with finite pump energy, thermal
pair output up to a controlled truncation, greybody attenuation, explicit
partner accounting, and a diary-blind control.  This is the pivot emitter for
the post-static demarcation program.

## Result in One Line

A finite pump ladder can emit `O(S)` Hawking/partner pairs through a stationary
`O(1)`-participation one-use instrument while remaining exactly blind to an
entropy-carrying spectator diary.  Finite energy and partner accounting do not
by themselves force diary-visible access.  What forces information export, if
anything, must be a dynamical coupling of the diary into the temporal orbit of
the pump/jump instrument.

This is not a complete Schwarzschild model: the shrinking microcanonical
degeneracy and exact `S(E) ~ E^2` structure are not yet built into the pump
ladder.  It is an exact countermodel to the claim that finite pump depletion or
fresh partner accounting alone repairs the static certificate.

## 1. Finite Pump

Let the pump have number states

```text
|n>_P,    n=0,...,N,
H_P = (omega_h+omega_b) sum_n n |n><n|.
```

One use couples the pump to fresh Hawking and partner modes `h_j,b_j`, initially
in vacuum.  Put

```text
q = exp(-beta omega),
Z_n = 1-q^(n+1).
```

Define the energy-conserving isometry on the vacuum input by

```text
V_q |n>_P |0,0>_(h,b)
  = sum_(m=0)^n sqrt[(1-q)q^m/Z_n]
      |n-m>_P |m,m>_(h,b).                                (1.1)
```

The pump loses exactly `m` pair-energy units while Hawking and partner modes
are created in perfectly correlated occupation `m`. Normalization follows from
the finite geometric sum.

Every isometry extends to a unitary on a sufficiently large finite Hilbert
space.  Equation (1.1) is therefore an exact finite-energy collision model,
although deriving this precise isometry from a simple time-independent
trilinear Hamiltonian remains a separate synthesis problem.

## 2. Thermal Limit and Controlled Error

For pump level `n`, the emitted pair-number distribution is

```text
p_n(m) = (1-q)q^m/(1-q^(n+1)),    0<=m<=n.                (2.1)
```

Its distance from the infinite geometric/thermal distribution is controlled by
the omitted tail `q^(n+1)`.  Away from the bottom of the pump,

```text
p_n(m) = (1-q)q^m [1+O(q^(n+1))],
<m> = q/(1-q) + O(n q^n)
    = n_beta + exponentially small truncation.            (2.2)
```

Thus each fresh Hawking mode is thermal to exponentially small error while the
pump has many remaining units.

## 3. Greybody Exterior Channel

Mix `h_j` with an exterior input `a_in,j` on a beam splitter of transmissivity
`gamma`:

```text
a_out,j = sqrt(1-gamma) a_in,j + sqrt(gamma) h_j.          (3.1)
```

For vacuum exterior input,

```text
<n_out> = gamma n_beta + truncation error.                 (3.2)
```

The complementary beam-splitter output absorbs the incident fraction.  In the
large-pump limit, the purification by the joint pump-plus-partner environment
in (1.1), followed by (3.1), realizes exactly the exterior reduced channel of
active Gaussian route 2c:

```text
Hawking flux       gamma n_beta;
net absorptivity   gamma;
line ratio         n_beta/(n_beta+1)=exp(-beta omega);
exterior g2        2.
```

The purifying environment is explicit rather than hidden in an anomalous
self-energy. For a pump number state, the Hawking mode is entangled with the
joint pump-plus-`b` environment; `b` alone is number-correlated with it but is
not its pure two-mode-squeezed purification.

## 4. One-Use Pump Instrument

After tracing the two fresh modes, the pump channel has Kraus operators

```text
K_m
  = sum_(n=m)^N sqrt[p_n(m)] |n-m><n|,
m=0,...,N.                                                (4.1)
```

Different `m` have orthogonal Hilbert-Schmidt support.  Use their Choi weights

```text
w_m = Tr(K_m^dag K_m)
```

and define

```text
N_K = (sum_m w_m)^2/sum_m w_m^2.                          (4.2)
```

For a large pump, normalized weights approach the geometric distribution and

```text
N_K -> (1+q)/(1-q) = 2 n_beta+1 = O(1)                   (4.3)
```

at `beta omega=O(1)`.  Finite energy therefore does not force entropy-sized
one-use jump participation.

This `N_K` is an invariant of the pump channel, unlike the arbitrary
microscopic source-list Gram participation.  It counts pair-number Kraus
outcomes, not the number of record histories accumulated over many uses.

## 5. Repeated Uses and Depletion

Apply (1.1) to fresh mode pairs repeatedly.  While the pump distribution stays
far from `n=0`, each use removes mean energy

```text
<Delta n_P> = n_beta+exponentially small corrections.      (5.1)
```

An initial pump with `N=O(S)` therefore supports

```text
K_evap = O(S/n_beta) = O(S)                               (5.2)
```

thermal uses before boundary depletion. The output history has many possible
pair-number strings. Starting from a pump number state, the exact Schmidt
spectrum across

```text
remaining pump | all emitted records
```

is the final pump-number distribution, equivalently the distribution of total
emitted pair number `M`. Before depletion it approaches the negative-binomial
law

```text
P_K(M) = binom(M+K-1,M) (1-q)^K q^M.                     (5.3)
```

Its inverse participation grows as `O(sqrt(K))`, so the global energy-history
rank is not `O(1)` even though the one-use channel rank is. This growth is
forced by the stochastic energy ledger and partner record; it is not
microscopic diary access. The distinction is decisive because the
diary-visible rank below remains exactly zero.

The pump shift algebra generated by the `K_m` contains powers of the lowering
shift and has at most `N+1=O(S)` linear directions.  Its size comes from the
finite energy ladder, not from an entropy-sized microstate register.

## 6. Exact Diary-Blind Control

Attach a spectator diary/memory register `D` and take

```text
H_total_space = H_P_space tensor H_D_space,
V_total = V_q tensor I_D.                                 (6.1)
```

The diary may have dimension `exp(S_D)`.  Every emitted Hawking/partner record
is exactly independent of the diary state:

```text
N_record(rho_D) = N_record(sigma_D)
for all rho_D,sigma_D.                                    (6.2)
```

The temporal source orbit acts as the identity on `D`, so its Q2
diary-visible defect is exactly zero.  The model can radiate `O(S)` energy
units with thermal one-use statics and no diary export.

This is the finite-energy active analogue of the frozen-routing witness.  It
shows that partner production does not automatically carry private black-hole
information; the partner can be correlated with energy loss while remaining
blind to the microstate label.

## 7. What the Model Decides

```text
Question:
  Does finite pump/partner accounting force the corrected invariant input 2b
  to be large?

Answer in this class:
  Partner/energy-history participation grows globally (as O(sqrt(K)) before
  depletion), but one-use invariant participation remains O(1), and the
  diary-visible temporal orbit can remain exactly zero. Global record rank and
  global diary-access rank are different invariants.
```

The ontic residue is now precise:

```text
What gravitational/microscopic mechanism couples the entropy-carrying code
subspace into the temporal orbit of the active Hawking pump before evaporation
ends?
```

This is input 2 merged with input 3 for the earned definitional reason: after
removing representation-dependent microscopic labels, access is a property of
the Heisenberg/process orbit under the dynamics.

## 8. What Is Still Missing for Schwarzschild

1. A shrinking family of pump shells with degeneracy `dim H_E ~ exp[S(E)]` and
   `S(E) ~ E^2`, rather than a fixed spectator diary.
2. A single autonomous Hamiltonian that generates (1.1), the greybody mixing,
   and the changing temperature without step-dependent control.
3. A choice between diary-blind and diary-mixing pump operators in that
   shrinking shell family.
4. Extension of Q2 from bounded fresh collisions to this persistent bosonic
   pump and its emitted record, using an energy-constrained norm.
5. A decoupling/sufficiency theorem for the diary-mixing branch.

The first two are black-hole thermodynamics/channel construction.  The last
three are the surviving dynamical demarcation problem.

## 9. Verification

`sim/finite_parametric_pump.py` verifies:

```text
normalization and thermal-tail error of p_n(m);
O(1) one-use Choi/Kraus participation;
mean pump depletion over repeated uses;
global pump-record Schmidt participation and its energy-history growth;
greybody Hawking flux;
perfect Hawking-partner number correlation;
exact diary blindness by construction.
```

## Discipline

- Fresh partner modes are counted explicitly; they are not free refill.
- Record-history multiplicity is not diary-visible source participation.
- A finite-energy active emitter is not yet a Schwarzschild density of states.
- Do not infer information export from energy export or Hawking/partner
  entanglement.
- Use this model as the persistent-emitter test case for Q2.
