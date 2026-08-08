# Simplified argument skeleton

Logical map for restructuring the paper. The main spine is:

1. exact Maxwell flux balance;
2. first-order gravitational charge conservation on the stationary
   Schwarzschild background used by Dai and Stojkovic (DS);
3. application to the DS static families.

ADM, Komar, Brown--York, and Bondi statements remain useful as asymptotic,
stationary, quasi-local, and radiative extensions, but they are not the primary
route to the finite-radius DS observable.

## Central claim

The DS signal requires the observer-side monopole coefficient to vary with the
position of a source near the other mouth. In Maxwell theory that coefficient is
a conserved flux through the observer's measuring surface. In the DS
gravitational model it is a conserved first-order Hamiltonian charge. A family
of static solutions in which either quantity varies therefore does not represent
the dynamical history of one system with fixed charge data.

## Quantities that must remain distinct

- **Maxwell surface charge**
  \[
    Q[S]=\frac{1}{4\pi}\int_S \star F .
  \]
  In a source-free region it is a period of the closed form \(\star F\).

- **ADM mass** is a Hamiltonian charge at spatial infinity. A spacetime with
  multiple asymptotically flat ends has a separate ADM charge at each end under
  the usual Regge--Teitelboim boundary conditions.

- **Bondi mass** is a charge on cuts of future null infinity. It changes through
  gravitational news and, when present, outgoing matter flux.

- **Brown--York energy** is a quasi-local charge associated with a chosen
  worldtube, time flow, foliation, and reference prescription.

- **Finite-radius mouth coefficient** is the coefficient of the nonradiative
  \(\ell=0\), \(1/r\) perturbation in an observer-side vacuum region. It is the
  DS observable. It agrees with an ADM, Komar, or linearized Hamiltonian charge
  only under additional stationary, asymptotic, or perturbative hypotheses.

In the specific DS two-copy Schwarzschild model, the observer-side perturbation
is \(h_{tt}=2b_{tt}/r\) throughout the exterior, so \(b_{tt}\) is both the local
mouth coefficient and the linearized ADM mass perturbation at that asymptotic
end. This coincidence should not be assumed in a generic radiative geometry.

## Result 1: Maxwell flux rigidity

Let \(S_t\) be a smooth family of closed two-surfaces and let
\(\mathcal T=\bigcup_{t\in[t_0,t_1]}S_t\) be the three-dimensional worldtube
they sweep out. Maxwell's equation

\[
  d\star F=4\pi\star j
\]

and Stokes' theorem give the exact balance law

\[
  Q[S_{t_1}]-Q[S_{t_0}]
  =\int_{\mathcal T}\star j .
\]

Therefore \(Q[S_t]\) is constant whenever the net electric current through
\(\mathcal T\) vanishes. This result requires neither stationarity nor a
perturbative expansion, and the individual surfaces need not bound compact
spatial regions.

### Topological content

In a source-free region, \(d\star F=0\), so the flux depends only on the homology
class of the measuring surface and the cohomology class \([\star F]\). Wormhole
topology permits nonzero source-free periods; it does not determine their
values. The numerical flux is initial sector data conserved by source-free
evolution.

Source-free electromagnetic waves carry energy and momentum but no electric
current, so they do not alter the monopole. Charged matter is already covered by
the current term in the balance law.

### Measuring surface versus throat cut

The observer-side measuring surface \(S_A\) and a cut through the throat define
different fluxes.

- Motion near the other mouth does not change \(Q[S_A]\).
- Crossing the throat changes the flux through the throat cut.
- Throat crossing alone does not change \(Q[S_A]\) if the charge remains between
  the throat and \(S_A\).
- If the charge later moves outward through \(S_A\), its current crosses the
  measuring worldtube and \(Q[S_A]\) changes by the ordinary Maxwell balance
  law.

Thus the relevant condition is always whether current crosses the specified
measuring surface, not whether a particle crosses the throat.

### Application to the DS electrostatic family

DS obtain

\[
  Q_2^{\rm DS}(A)=\frac{qR}{2A} .
\]

For two source positions,

\[
  Q_2^{\rm DS}(A_1)-Q_2^{\rm DS}(A_0)
  =\frac{qR}{2}\left(\frac{1}{A_1}-\frac{1}{A_0}\right).
\]

In particular, moving from \(A=\infty\) to \(A=R\) changes the observer-side
flux by \(q/2\), even though no current crosses the observer-side measuring
worldtube. The static solutions therefore lie in different flux sectors. Each
is a legitimate elliptic boundary-value solution, but the family is not the
quasistatic history of one Maxwell initial datum.

This result refutes the DS electrostatic model. Their gravitational S2 proposal
requires the separate result below.

## Result 2: first-order gravitational mouth rigidity

### Hypotheses

Let \(\bar g_{\mu\nu}\) be the stationary wormhole background obtained in the DS
model by joining two Schwarzschild exteriors. Require:

1. an observer-side neighborhood of the measuring worldtube \(\mathcal T\) in
   which \(\bar g_{\mu\nu}\) solves the vacuum Einstein equation and admits the
   normalized, field-independent Schwarzschild time-translation Killing field
   \(\xi^\mu\);
2. a perturbation \(h_{\mu\nu}\) satisfying the sourced linearized Einstein
   equation, with perturbative parameter \(\epsilon=\mu/M\ll1\);
3. a fixed asymptotic frame and gauge transformations compatible with the
   stated boundary conditions; and
4. no linearized matter or support-field source support in a neighborhood of
   \(\mathcal T\).

For an on-shell stationary background, define the covariant first-order surface
charge form

\[
  k_\xi[h;\bar g]=\delta Q_\xi-\xi\mathbin{\cdot}\theta(\bar g,h)
\]

in the Iyer--Wald notation, equivalently using the appropriate
Abbott--Deser/Hamiltonian superpotential. Use the standard Einstein--Hilbert
symplectic potential and normalize the charge to agree with the ADM mass
variation at the observer end. For closed \(S_t\), the standard exact-form
ambiguities integrate to zero, and proper gauge transformations preserving the
surface and asymptotic frame do not change the charge. In the vacuum
neighborhood of \(\mathcal T\), the linearized field equations and
\(\mathcal L_\xi\bar g=0\) imply

\[
  d k_\xi[h;\bar g]=0 .
\]

Hence

\[
  \delta H_\xi[S_t]=\int_{S_t}k_\xi[h;\bar g]
\]

is constant along the measuring worldtube. With an external first-order source,
write the sourced linearized identity as

\[
  d k_\xi=\mathcal J^{(1)}_\xi,
  \qquad
  \delta H_\xi[S_{t_1}]-\delta H_\xi[S_{t_0}]
  =\int_{\mathcal T}\mathcal J^{(1)}_\xi,
\]

where \(\mathcal J^{(1)}_\xi\) is the linearized constraint/Killing-energy
current three-form, with its normalization and orientation fixed by the
displayed convention. The endpoint charges are equal precisely when its
integrated flux through \(\mathcal T\) vanishes.

This argument is local to the worldtube. The sections need not bound compact
spatial regions, and the proof does not require two asymptotic ends. It therefore
also applies to a single-ended handle whenever the same stationary-background,
vacuum-neighborhood, gauge, and normalization hypotheses hold. The per-end ADM
cross-check below is the topology-specific statement.

### Identification with the DS monopole

In a Schwarzschild vacuum region, an even-parity \(\ell=0\) perturbation has the
form

\[
  h^{(\ell=0)}_{\mu\nu}
  =\delta M\,\partial_M\bar g_{\mu\nu}
   +\mathcal L_\eta\bar g_{\mu\nu},
\]

where the second term is gauge. The surface charge is \(\delta H_\xi=\delta M\).
The balance law therefore makes \(\delta M\) constant when no first-order source
crosses the observer-side worldtube. The absence of an independent radiative
\(\ell=0\) gravitational degree of freedom is a consequence of this constraint
structure; radiative tensor modes begin at \(\ell=2\).

DS define their observer-side monopole by

\[
  h_{tt}^{\rm our}=\frac{2b_{tt}}{r_2},
  \qquad
  h_{rr}^{\rm our}=\frac{2b_{rr}r_2}{(r_2-r_g)^2},
\]

and set \(b_{tt}=b_{rr}\). Since
\(\partial_M\bar g_{tt}=2/r\) and
\(\partial_M\bar g_{rr}=2r/(r-r_g)^2\) in their \(G=1\) convention, this
verifies directly that \(b_{tt}=b_{rr}=\delta M\). DS report

\[
  b_{tt}^{\rm DS}(A)=\frac{\mu R}{A}
\]

and treat \(A=A(t)\) as an orbit. Their printed normalization is internally
problematic. For \(R<A\), continuity of their own ansatz gives

\[
  b_{tt}-a_{tt}=\frac{\mu R}{A}.
\]

Using the opposite-normal derivative matching imposed in their electromagnetic
calculation gives \(b_{tt}=-a_{tt}\), and hence

\[
  b_{tt}=\frac{\mu R}{2A},
  \qquad
  a_{tt}=-\frac{\mu R}{2A}.
\]

The same-sign derivative condition printed in their gravitational section is
instead incompatible with continuity for \(\mu\ne0\). A consistent thin-shell
calculation would in any event require the appropriate junction conditions, so
the factor is a separate issue from the conservation theorem.

Whether one takes DS's reported coefficient or the coefficient obtained by
applying their earlier opposite-normal matching consistently, \(b_{tt}(A)\)
varies as \(1/A\). Since
\(b_{tt}=\delta M\), either version makes the first-order Hamiltonian charge vary
without a first-order source crossing the measuring worldtube. The reported
static family therefore cannot arise as one on-shell first-order evolution from
fixed initial Hamiltonian-charge data.

The full orbit may be nonspherical, but the claimed unsuppressed DS term is its
\(\ell=0\) mass perturbation. Nonsphericity can excite higher multipoles and
waves; it does not turn the constrained \(\ell=0\) charge into a position-tracking
mode.

Linearization is justified by \(\epsilon=\mu/M\ll1\), not by the speed of S2.
The far-side source in the proposed observation can lie at only a few
gravitational radii and need not be slow.

## Perturbative order of the radiative channel

Write the metric and news expansions as

\[
  g_{\mu\nu}=\bar g_{\mu\nu}
  +\epsilon h^{(1)}_{\mu\nu}
  +\epsilon^2 h^{(2)}_{\mu\nu}+\cdots,
  \qquad
  N_{AB}=\epsilon N^{(1)}_{AB}+O(\epsilon^2).
\]

The proposed DS monopole is \(O(\epsilon M)\). Substitution into the vacuum Bondi
mass-loss law gives

\[
  \frac{dM_B}{du}
  =-\frac{\epsilon^2}{32\pi}
    \int N^{(1)}_{AB}N_{(1)}^{AB}\,d\Omega
   +O(\epsilon^3).
\]

with an additional outgoing-matter term when present. Over a fixed dynamical
time interval, the fractional mass change from vacuum gravitational-wave flux
is therefore second order. Vacuum gravitational-wave energy flux vanishes at
strict first order, so it cannot generate or restore the reversible
\(O(\epsilon)\) monopole proposed by DS. First-order matter or support-field
flux is a separate channel excluded by Result 2's no-source-crossing hypothesis.

At second order, gravitational radiation can change the Bondi mass at an
asymptotically flat end. In vacuum, or with nonnegative outgoing matter flux,
this is a dissipative flux effect. Over radiation-reaction time scales it can
accumulate secularly, but it remains a different mechanism from the
instantaneous first-order relation \(\delta M\propto1/A(t)\). A generic
finite-radius nonlinear response remains model-dependent.

## Exact asymptotic cross-check: per-end ADM mass

The original DS idealization has two asymptotically flat Schwarzschild ends.
Under the standard Regge--Teitelboim evolution hypotheses, the ADM mass at each
end is separately conserved. Since \(b_{tt}\) is the observer-end linearized ADM
mass perturbation in the DS model, this gives an independent asymptotic version
of the same diagnosis: static solutions with different \(b_{tt}\) belong to
different asymptotic sectors.

In a single-ended geometry with two mouths, there is one total ADM mass but no
separate ADM charge for each mouth. The local first-order theorem above remains
the relevant statement in the stationary Schwarzschild-type regime.

## Nonlinear and special-case extensions

### Stationary vacuum: Komar propagation

For a normalized Killing field in a stationary vacuum shell,

\[
  d\star d\xi^\flat=0 .
\]

The Komar integral is therefore the same on homologous inner and outer
surfaces. This propagates a fixed inner Komar charge to the exterior \(1/r\)
coefficient. It does not by itself prove that the inner charge is fixed.
Identifying fixed throat data with a fixed inner Komar integral requires an
additional stationary exterior uniqueness result, so Komar propagation is a
conditional extension rather than part of the main proof.

### Fully dynamical boundary: Brown--York balance

For a chosen timelike worldtube, time flow, foliation, and reference
prescription, the Brown--York identity gives an exact quasi-local balance law.
The Brown--York energy changes through stress-energy flux across the worldtube
and through the geometric boundary-work term. It is not generally identical to
the finite-radius mouth \(1/r\) coefficient.

This is the appropriate exact statement for a dynamical throat boundary. The
paper does not claim a general canonical finite-radius mouth-charge theorem in
a generic fully nonlinear radiative spacetime.

## Logical diagnosis of the DS construction

The same error appears in both parts of the DS argument:

- In Maxwell theory, \(Q_2^{\rm DS}(A)\) varies across a static family even though
  the observer-side measuring surface receives no current.
- In linearized gravity, \(b_{tt}^{\rm DS}(A)\) varies across a static family even
  though the corresponding first-order Hamiltonian charge receives no source
  flux.

The missing step is dynamical reachability. A parameterized family of elliptic
or stationary boundary-value solutions is not automatically a time evolution.
In the DS families, changing the source-position parameter also changes the
conserved surface-charge data. The members belong to different sectors rather
than successive times of one physical system.

## Status of the ingredients

| Statement | Status | Principal hypotheses | Quantity controlled |
|---|---|---|---|
| Maxwell balance | Exact | Maxwell equation; specified measuring worldtube | Electric surface charge |
| Maxwell rigidity | Exact consequence | Zero net current through that worldtube | Observer-side monopole flux |
| First-order gravitational balance | Exact identity in the linearized theory; valid through \(O(\epsilon)\) | On-shell stationary background, normalized Killing field, valid linearized equations, admissible gauge | Linearized Hamiltonian charge |
| DS gravitational corollary | First-order | Observer-side Schwarzschild vacuum region; vanishing integrated linearized constraint flux | \(\ell=0\) mouth coefficient \(b_{tt}=\delta M\) |
| Per-end ADM conservation | Exact asymptotic statement | Multiple asymptotically flat ends; Regge--Teitelboim evolution | ADM mass at each end |
| Bondi balance | Exact null-infinity statement | Asymptotic flatness; include news and matter flux | Bondi mass |
| Komar propagation | Exact stationary statement | Normalized Killing field; vacuum shell | Komar charge between homologous surfaces |
| Brown--York balance | Exact quasi-local identity | Chosen worldtube, time flow, foliation, and reference | Brown--York boundary energy |

## Proposed manuscript order

1. Define the distinct charges and the finite-radius observable.
2. Prove Maxwell flux rigidity and diagnose the DS electrostatic family.
3. State and prove the first-order gravitational mouth theorem.
4. Apply it to the reported DS relation \(b_{tt}^{\rm DS}=\mu R/A\), record
   the separate factor-of-two matching inconsistency, and emphasize that the
   no-go depends only on the claimed \(1/A\) variation.
5. Explain the \(O(\epsilon)\) versus \(O(\epsilon^2)\) radiative hierarchy.
6. Present per-end ADM, Komar, and Brown--York results as cross-checks,
   special cases, and nonlinear boundaries.
7. Close with the remaining higher-multipole, wave, transit, and backreaction
   channels.
