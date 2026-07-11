# Shrinking-Shell Diary Access: Blind Archive Versus Mixing Radiation

Date: 2026-07-10

Status: exact finite-dimensional shell construction, exact no-hiding dimension
bound, and verified blind/weak/mixing comparison. This supplies the first
shrinking-`S(E)` application of the composable Q2 theorem. It is not an
autonomous Hamiltonian model.

## Result in One Line

A shrinking black-hole shell can emit exactly diary-blind thermal radiation
only by moving the lost logical dimension into a hidden partner/remnant
archive. If no entropy-sized hidden archive survives, unitarity plus shell
shrinkage forces eventual exterior information transfer. It does not force
Page-time transfer or sufficient mixing: those remain independent dynamical
conditions.

The numerical control makes the separation explicit. Blind, weak-erasure, and
fully mixing branches have identical `S(E)~E^2` shell thermodynamics and the
same thermal energy qubit at every step, but radically different diary flow.

## 1. Exact Shell Thermodynamics

Take `L` logical shell qubits and a fixed residual entropy `S_res`. At depth
`j`, define

```text
d_j = 2^(L-j),
S_j = S_res + (L-j) log 2,
E_j = sqrt(S_j/alpha).                                    (1.1)
```

Then exactly

```text
S_j = alpha E_j^2.                                        (1.2)
```

For `omega_j=E_j-E_(j+1)` and finite-difference
`beta_j=(S_j-S_(j+1))/omega_j`,

```text
beta_j omega_j = log 2,
exp(-beta_j omega_j) = d_(j+1)/d_j = 1/2.                 (1.3)
```

Attach at every step the same Hawking energy qubit with excited-state
probability

```text
p_H = exp(-beta omega)/(1+exp(-beta omega)) = 1/3.         (1.4)
```

Its thermal partner is explicit and inaccessible in this control. This energy
pair is independent of the logical routing below, so all branches have exactly
the same one-step energy statistics and density-of-states ratio.

## 2. Exact No-Hiding Archive Bound

Let an isometry for one evaporation step be

```text
W : H_j -> H_(j+1) tensor R_j tensor P_j,                 (2.1)
```

where `R_j` is the complete accessible exterior record and `P_j` is hidden
partner/archive state not counted in the daughter shell. Suppose the exterior
channel is exactly constant on the full input shell:

```text
Tr_(H_(j+1) P_j)[W rho W^dag] = sigma_R  for every rho.   (2.2)
```

The no-hiding theorem says that the complementary output
`H_(j+1) tensor P_j` contains a reversible copy of the input. Therefore

```text
d_(j+1) dim(P_j) >= d_j,                                  (2.3)
dim(P_j) >= ceil[d_j/d_(j+1)].                            (2.4)
```

If the fixed exterior state `sigma_R` has rank `r`, a minimal pure dilation
requires `r` orthogonal hidden copies and gives the stronger raw-dimension
bound

```text
d_(j+1) dim(P_j) >= r d_j.                                (2.5)
```

The factor `r` purifies ordinary thermal uncertainty; the factor
`d_j/d_(j+1)` is the information-carrying archive cost.

Across `K` exactly blind shrinking steps, the archive must have logical
capacity at least

```text
prod_(j<K) d_j/d_(j+1) = d_0/d_K
  = exp[S_0-S_K].                                         (2.6)
```

Thus a completely evaporated system with `d_K=1`, no hidden remnant/archive,
and global unitarity cannot keep the full exterior record diary blind. This is
an application of the established no-hiding theorem, not a claim that the
no-hiding principle itself is new; see Braunstein--Pati,
[arXiv:gr-qc/0603046](https://arxiv.org/abs/gr-qc/0603046).

## 3. Three Routing Branches

Represent each shell as qubits. Before the `j`th split, apply a fixed Haar
unitary to the remaining shell and peel one logical degeneracy qubit.

```text
blind branch, lambda=0:
  route the peeled qubit to hidden P_j;
  exterior receives only the independent thermal energy record;

weak branch, 0<lambda<1:
  pass the peeled qubit through a flagged erasure channel;
  with probability lambda it reaches the exterior degeneracy record,
  otherwise it enters P_j;

mixing branch, lambda=1:
  route every scrambled peeled qubit to the exterior record.
```

The exterior degeneracy record may be read as polarization/species data inside
an emitted wave packet. The construction guarantees equality of the energy
statistics, not equality of every possible observable on that degeneracy
register. Establishing a fully Hawking-Gaussian, locally indistinguishable
mixing encoding is a stricter follow-up.

The flagged-erasure step has distance at most `2 lambda` from the blind record
channel, so the composable Q2 theorem gives the deliberately loose bound

```text
distance(record_lambda, record_blind) <= 2 K lambda.       (3.1)
```

The simulation computes the actual information flow rather than relying on
this worst-case bound.

## 4. Verified Information-Flow Diagnostic

Entangle a one-qubit diary with reference `Q`, initialize the other shell
qubits in a fixed state, and use the same shell unitaries for every routing
branch. At each depth and each erasure pattern, compute

```text
Delta_dec = ||rho_(Q,H) - rho_Q tensor rho_H||_1,          (4.1)
I(Q:R),                                                    (4.2)
```

where `H` contains the daughter shell and every erased partner qubit, and `R`
contains the accessible logical record. Average over the flagged erasure
patterns. Small `Delta_dec` is the standard recovery/decoupling condition for
the exterior record.

For `L=6`, three fixed random-shell seeds, and shell dimensions

```text
64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1,
```

`sim/shrinking_shell_diary_channel.py` gives at complete evaporation:

| access `lambda` | hidden-system decoupling error | `I(Q:R)` |
| ---: | ---: | ---: |
| 0.00 | 1.500000 | 0 |
| 0.25 | 1.339282 | 0.205286 |
| 0.75 | 0.410211 | 1.181008 |
| 1.00 | `4.8e-16` | `1.386294 = 2 log 2` |

For the blind branch, `I(Q:R)` stays below `7.1e-16` at every depth. For the
fully accessible branch, the hidden system decouples to machine precision at
the endpoint. The intermediate branches show that nonzero access need not be
sufficient for accurate recovery.

The thermodynamic checks give

```text
max |S-alpha E^2| = 4.4e-16,
beta_j omega_j = log 2 at every step,
p_H = 1/3 in every branch and step.                        (4.3)
```

## 5. Demarcation Consequence

The result separates three statements that had been conflated:

```text
state-count shrinkage + unitarity + no hidden archive
  => eventual information must leave the shrinking shell;

order-one cumulative Q2 process distance from every blind comb
  => necessary for reliable exterior recovery by that time;

sufficiently isotropic/decoupling temporal mixing
  => exterior recovery actually occurs.
```

The first is a kinematic/no-hiding statement. The second is the new composable
access obstruction. The third consumes standard decoupling machinery but is a
model-side dynamical hypothesis until verified for a microscopic gravity
emitter.

This means `S(E)~E^2` does contribute more than a temperature: together with
unitarity and the absence of remnants, it forces the *eventual destination* of
the information. It still does not specify the channel, Page-time onset, or
scrambling rate.

## 6. Remaining Gap

### Locally identical multi-time control

`sim/locally_thermal_code_emitter.py` closes the kinematic part of the stricter
control. It uses the perfect `[[5,1,3]]` code as the shell's diary subspace and
emits its five physical degeneracy modes sequentially. Append to every mode the
same independent energy qubit with `exp(-beta omega)=1/2`. Then every individual
outgoing wave packet has exactly the diary-independent state

```text
rho_one = diag(2/3,1/3)_energy tensor I_2/2_degeneracy.    (6.1)
```

The stabilizer calculation verifies, to `3.2e-16`, that every one-mode Pauli
compresses to a scalar on the logical code. More strongly:

```text
I(Q : any one emitted mode) = 0,
I(Q : any two emitted modes) = 0,
I(Q : any three emitted modes) = 2 log 2.                 (6.2)
```

Thus the mixing branch and a blind product branch have identical one-wavepacket
states, while only the mixing branch carries the diary in multi-time
correlations. This is an exact finite example of locally thermal radiation
with a sharp recovery threshold.

It is not yet the full Hawking construction. The degeneracy factor is a
finite code label rather than a bosonic Gaussian mode, and the encoder is a
supplied stabilizer isometry rather than dynamics generated by the finite pump.
The remaining harder target is to realize the same correlation-only encoding
with the finite pump, partner bookkeeping, changing temperature, and a simple
autonomous Hamiltonian—or to verify the corresponding temporal design/ETH
condition in a named microscopic gravity model.

That construction, or a proof that a named microscopic gravity model has the
required temporal design/ETH property, is the remaining positive dynamical
step.
