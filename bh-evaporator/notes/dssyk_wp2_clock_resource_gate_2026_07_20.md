# WP2 clock-state and instrument gate

Date: 2026-07-20

Status: **complete negative gate; WP2 is closed at the current bulk input.**
The clock Hamiltonian and clock state determine a natural one-time overlap
kernel after one additionally chooses the canonical covariant time POVM. They
do not determine a post-measurement instrument, a multitime comb, or the
observer--field contacts. Two explicit instruments with the same one-read
statistics give different two-record access, and a finite contact-backreaction
control gives a third completion. All of them transport exactly to the
isospectral one-copy model.

A follow-up detector-backreaction audit sharpens the last point without
reopening the gate. Narovlansky--Verlinde do write a model Unruh-detector
contact with the constraint-preserving dressed operators. What remains absent
is not every contact, but a Lorentzian instrument and a physical law pricing
its normalization, duration, repetition count, or retained memory. The
separate DSSYK observer-energy cap does not imply such a law; the proof and
the closest Euclidean backreaction near-hit are recorded in
`dssyk_detector_backreaction_resource_audit_2026_07_20.md`.

The earlier wording that the CLPW maximum-entropy clock *selects* a Cauchy
timing-error channel and common temporal memory was too strong. The Cauchy
formula survives as a canonical positive completion that matches the tracial
two-point kernel. The claimed physical selection does not.

## 1. Executive verdict

The bounded WP2 question was:

> Does the de Sitter observer construction itself select the clock process
> needed to turn the correlator-level soft filter into a sequential
> diary-to-record channel?

The answer is no for the sources checked here.

CLPW specify a lower-bounded observer Hamiltonian, a clock state, and an
observer algebra. They do not specify a time POVM, its Naimark dilation, the
post-measurement state update, or repeated detector contacts. Chen--Stanford--
Tang--Yang obtain the Cauchy kernel by integrating observer-energy endpoints
in a tracial correlator, not by deriving a measurement channel. The checked
DSSYK observer papers likewise specify physical operators, correlators,
algebras, or thermodynamic bounds, but not a compatible sequential quantum
instrument.

This produces a sharper demarcation than the earlier resource note:

```text
clock Hamiltonian + clock state + one-time correlator/POVM
  do not determine
post-measurement dynamics + multitime observer comb + detector cost.   (1.1)
```

The natural Cauchy completion remains useful as a control. It is not a
prediction of observer record distinguishability until an instrument and
contact model are supplied.

## 2. Primary-source and instrument audit

### 2.1 What the de Sitter sources actually fix

1. **CLPW clock.** The minimal observer has
   $H_{\rm obs}=q\geq0$ and access to all bounded observer operators. Before
   the lower-bound projection, $-p$ is conjugate clock time. After imposing
   $q\geq0$, no self-adjoint $p$ obeying the perfect canonical relation exists.
   Semiclassical clock states are chosen separately as
   $f_\epsilon(q)=\sqrt\epsilon\,g(\epsilon q)$, with time width
   $O(\epsilon)$ and energy $O(1/\epsilon)$. Their maximum-entropy state has

   $$
   f_\beta(q)=\sqrt\beta\,e^{-\beta q/2},\qquad q\geq0,                 \tag{2.1}
   $$

   but CLPW explicitly note that this state is not semiclassical: its clock
   time uncertainty is $O(\beta_{\rm dS})$.
2. **Tracial correlator.** Chen--Stanford--Tang--Yang derive
   $e^{-\pi|\omega|}$ in radius-one units from the allowed observer-energy
   endpoint in a tracial two-point function. Conditioning on a highly excited
   observer approximately restores the QFT correlator.
3. **DSSYK observer data.** Narovlansky--Verlinde supply constraint-preserving
   scaling operators, a model Unruh-detector contact, and detector rates;
   Aguilar-Gutierrez supplies the relational algebra; Tietto--Verlinde supply
   observer thermodynamics and a model-specific energy cap. None supplies the
   instrument data in (1.1) or relates the cap to detector action.
4. **Recent anti-scrambling data.** The OTOC and tracial papers sharpen the
   correlator/algebra story, but do not give a positive passive record comb.
   The separate contour audit shows that a proper 2-OTO functional needs a
   priced compiler before it becomes a passive observer record.

Targeted searches of the primary PDFs for `POVM`, `instrument`,
`post-measurement`, and `Naimark` found no such construction in the bounded
anchor set. This is a bounded source verdict, not an exhaustive theorem about
all de Sitter literature.

### 2.2 Standard measurement-theory input

A POVM fixes outcome probabilities, not the conditional output state. A
quantum instrument is the collection of completely positive maps that fixes
both. Sequential experiments therefore compose instruments, not POVM effects
alone. Covariant observables for half-line generators can be constructed by
Naimark dilation, but the dilation and its retained degrees of freedom are
additional operational data.

### 2.3 Detector-backreaction follow-up

Standard localized-probe and influence-functional frameworks can derive a
quantum instrument or process tensor after a coupling, switching profile,
probe preparation, and readout have been declared. They do not derive those
choices or their gravitational price. The closest bounded near-hit is a 2026
Euclidean Gaussian clock-detector model with a smeared metric source and the
sufficient saddle-stability condition

$$
\frac{\Lambda_{\rm clk}^2}{\Omega_0^2}<\delta_P.              \tag{2.2}
$$

This controls metric susceptibility on a chosen Euclidean channel. It does
not define a Lorentzian CP instrument, couple the detector to the DSSYK diary
operator, or bound the integrated diary-sensitive action used below.

The separate observer-energy cap cannot fill that gap. If
$\Delta H(t)=g(t)X\otimes\Delta O_{\rm phys}(t)$ preserves the constraint,
then rescaling $g\mapsto cg$ leaves the free observer spectrum and its energy
cap unchanged while sending $G_D(T)\mapsto cG_D(T)$. Even a future pointwise
coupling bound would require a duration or contact-count bound before it
controls accumulated action. Thus the checked contact, energy cap, and
backreaction inequality are non-composable at the current level of input.

## 3. General one-time clock overlap

Let the clock Hilbert space be
$\mathcal H_C=L^2(\mathbb R_+,dq)$, with
$H_C=q$, and let $f\in\mathcal H_C$ be normalized. Extend $f$ by zero to the
negative half-line. The canonical covariant time POVM has generalized kets

$$
|s)=\frac1{\sqrt{2\pi}}\int_0^\infty dq\,e^{-iqs}|q\rangle,
\qquad E(ds)=|s)(s|\,ds,                                      \tag{3.1}
$$

and one-read density

$$
p_f(s)=(f|E(ds)|f)/ds
=\left|\frac1{\sqrt{2\pi}}\int_0^\infty dq\,e^{-iqs}f(q)\right|^2.  \tag{3.2}
$$

If one now makes the *additional* classical-offset completion

$$
\Phi_f^H(\rho)=\int ds\,p_f(s)e^{-iHs}\rho e^{iHs},             \tag{3.3}
$$

its coherence multiplier is the clock autocorrelation

$$
M_f(\omega)
:=\int_{\max(0,-\omega)}^\infty dq\,f(q+\omega)f(q)^*
=\int ds\,p_f(s)e^{i\omega s}.                                \tag{3.4}
$$

Thus an energy coherence with gap $\omega$ is multiplied by
$M_f(-\omega)=M_f(\omega)^*$. Equation (3.4) is the exact general filter; it
does not assume the maximum-entropy state.

For (2.1),

$$
p_\beta(s)=\frac{\beta/2}{\pi[(\beta/2)^2+s^2]},
\qquad M_{f_\beta}(\omega)=e^{-\beta|\omega|/2}.                \tag{3.5}
$$

With $\beta_{\rm dS}=2\pi R_{\rm dS}$, (3.5) matches the tracial transfer
factor. This is an equality between a correlator kernel and one chosen
positive completion.

For a CLPW semiclassical family
$f_\epsilon(q)=\sqrt\epsilon\,g(\epsilon q)$,

$$
M_{f_\epsilon}(\omega)
=\int_{\max(0,-\epsilon\omega)}^\infty du\,
g(u+\epsilon\omega)g(u)^*.                                    \tag{3.6}
$$

Its transfer bandwidth is therefore $|\omega|=O(1/\epsilon)$, in agreement
with the energy cost of a high-resolution clock. The de Sitter-radius Cauchy
profile is a property of the maximum-entropy choice, not of every allowed
observer clock.

## 4. A POVM does not select a clock instrument

For any normalized family of clock states $\{\sigma_s\}$, the
measure-and-prepare maps

$$
\mathfrak I^\sigma(ds)(\rho_C)
=\operatorname{Tr}[E(ds)\rho_C]\,\sigma_s                     \tag{4.1}
$$

form a valid instrument with POVM $E(ds)$. Every choice of $\sigma_s$ has the
same first-read distribution (3.2). After a clock interval $\tau$, however,
the two-read law is

$$
p^\sigma(ds_2,ds_1)
=\operatorname{Tr}[E(ds_1)\rho_C]\,
\operatorname{Tr}\!\left[
E(ds_2)e^{-iq\tau}\sigma_{s_1}e^{iq\tau}
\right],                                                       \tag{4.2}
$$

which depends on the post-measurement family $\sigma_s$.

This yields the following elementary but load-bearing proposition.

> **Clock-state/instrument nonidentifiability.** A lower-bounded clock
> Hamiltonian, an initial clock state, and a covariant time POVM determine the
> one-read distribution and the overlap $M_f$. They do not determine a
> two-slot clock process. Distinct compatible instruments can have identical
> one-read statistics and different multitime record channels.

Three explicit completions illustrate the proposition:

1. **Fresh/reset.** Read the canonical POVM, discard the clock, and prepare a
   fresh $|f\rangle$ before the next slot. Relative timing errors are
   independent.
2. **Persistent Naimark memory.** Dilate the first POVM, retain its pointer
   value as a classical or quantum memory, and reuse that offset without
   remeasuring or disturbing it. All slots share one offset.
3. **Contact-disturbed memory.** Retain the first offset but let a detector
   contact apply a bounded clock kick before the next slot. The later error is
   correlated with the first record and with the contact backreaction.

CLPW do not choose among these instruments. Calling the second one “the CLPW
process” would therefore insert the desired multitime answer by hand.

## 5. Explicit finite two-contact observer comb

The ambiguity survives after adding a completely explicit finite detector.
Let two temporal bins be two-level systems with

$$
H_j=\Delta E\,|1\rangle\langle1|_j,
\qquad
|\chi_\pm\rangle
=\frac{|01\rangle\pm|10\rangle}{\sqrt2}.                     \tag{5.1}
$$

Each one-bin marginal is identical for the two diaries. A shared offset gives

$$
\Phi_{f,{\rm com}}^{(2)}(\rho)
=\int ds\,p_f(s)e^{-is(H_1+H_2)}\rho e^{is(H_1+H_2)},          \tag{5.2}
$$

whereas fresh clocks give

$$
\Phi_{f,{\rm fresh}}^{(2)}(\rho)
=\int ds_1ds_2\,p_f(s_1)p_f(s_2)
e^{-i(s_1H_1+s_2H_2)}\rho e^{i(s_1H_1+s_2H_2)}.               \tag{5.3}
$$

The exchange coherence in (5.1) has equal total energy, so

$$
\gamma_{\rm com}=1,
\qquad
\gamma_{\rm fresh}=|M_f(\Delta E)|^2.                        \tag{5.4}
$$

Now introduce one retained detector-memory qubit $R$ in $|0\rangle$. At slot
$j$, use the finite unitary contact

$$
V_j=P_{+,j}\otimes I_R+P_{-,j}\otimes X_R,
\qquad P_{\pm,j}=\frac{I\pm X_j}{2}.                          \tag{5.5}
$$

The ordered contacts $V_2V_1$ store the eigenvalue of $X_1X_2$ in $R$.
Measuring $R$ is therefore a positive causal two-slot record process, with all
contact backaction retained in the unitary dilation. Its diary-record distance
is

$$
\delta_{2,{\rm com}}=1,
\qquad
\delta_{2,{\rm fresh}}=|M_f(\Delta E)|^2.                    \tag{5.6}
$$

For the maximum-entropy completion this becomes
$\delta_{2,{\rm fresh}}=e^{-\beta_{\rm dS}\Delta E}$.

The no-disturbance assumption is also testable. If the first contact adds an
unobserved symmetric clock kick $\pm\kappa$, the second-bin relative phase is
multiplied by

$$
\gamma_{\rm kick}=\cos(\kappa\Delta E),                       \tag{5.7}
$$

and the same fixed parity record has distance
$|\cos(\kappa\Delta E)|$. Equations (5.6)--(5.7) are three distinct
two-slot combs with the same pre-contact one-read distribution. The clock
state alone selects none of them.

The contact in (5.5) is deliberately finite and explicit, but it is not
claimed to be the DSSYK bulk detector. Choosing it demonstrates process
completion; deriving it or its cost from the bulk dictionary is exactly the
missing WP2 input.

## 6. Isometric transport with clock, instrument, and contacts

Let $W:\mathcal H_1\to\mathcal H_{\rm eq}$ be the equal-energy isometry. For
the two-bin clock process and detector memory, extend it to

$$
\widehat W=W_1\otimes W_2\otimes I_C\otimes I_R.              \tag{6.1}
$$

Transport the diary, bin Hamiltonians, instrument maps, contacts, and decoder:

$$
H_j\mapsto WH_jW^\dagger,
\qquad
V_j\mapsto\widehat W V_j\widehat W^\dagger                   \tag{6.2}
$$

on the physical image, while leaving clock and memory unchanged. The complete
record channel is then related by isometric conjugation. Hence, for every
fresh, persistent, or contact-disturbed completion,

$$
\delta_K^{\rm doubled}=\delta_K^{\rm one\ copy},              \tag{6.3}
$$

with the same equality for blind-comb distance, recovery fidelity, and
resource capacity under a transported cost rule.

Adding an explicit instrument therefore does not revive a constraint-induced
advantage. It only makes clear which extra operational input has been chosen.

## 7. What survives of the cutoff calculation

The following statements remain valid with corrected scope:

- The maximum-entropy wavefunction has a canonical covariant-time density
  that is Cauchy with radius-scale width.
- The associated random-offset completion suppresses absolute-time energy
  coherences by $e^{-\pi R_{\rm dS}|\omega|}$.
- A persistent-offset completion preserves fixed-total-energy relational
  coherences; a reset completion does not.
- Higher-energy semiclassical clock states have bandwidth $O(1/\epsilon)$.
- If the model-specific Tietto--Verlinde observer-energy cap is imposed, its
  formal hardest clock scale is Planckian; $R_{\rm dS}$ cancels.
- The native full DSSYK bandwidth is likewise Planckian in the NV dictionary.

None of these statements is a universal hard UV cutoff. The radius-scale
Cauchy law is a state- and completion-dependent soft filter, while the hard
scales are microscopic. A genuine operational cutoff would still require a
bulk-derived instrument and a detector/action budget.

## 8. WP2 decision

The clock-state/instrument gate fires the pre-registered stop condition:

> The natural observer protocol cannot currently be specified independently
> of the desired access conclusion.

Accordingly:

1. **Close WP2 at the current literature input.** Do not call the Cauchy
   channel or common-offset comb physically selected by CLPW.
2. **Retain the canonical Cauchy, fresh, persistent, and kicked processes as
   exact controls.** They prove nonuniqueness and calibrate what a future bulk
   instrument would have to select.
3. **Do not run scaling-operator numerics or an exact DSSYK OTOC.** A chosen
   operator family still does not supply an interaction budget or a clock
   instrument.
4. **Reopen only on new physical input:** an explicit worldline Naimark
   dilation/instrument, retained-memory rule, contact Hamiltonian including
   backreaction, and a common one-copy/doubled implementation cost or action
   bound. A free-observer energy cap or Euclidean saddle-stability condition
   alone is insufficient.

Allowed external framing:

> The CLPW clock state admits a canonical covariant-time completion whose
> one-read kernel matches the de Sitter tracial filter. The same one-read data
> admit inequivalent fresh, persistent, and contact-disturbed two-slot
> instruments, and every completion transports exactly to one-copy DSSYK.
> Current bulk constructions therefore do not yet determine an operational
> observer cutoff.

Not allowed:

> The maximum-entropy clock is a semiclassical observer; CLPW derives a
> Cauchy measurement channel; one autonomous clock uniquely selects common
> temporal memory; or the resulting curve is a fundamental $\Lambda$ cutoff.

## 9. Verification artifact

`sim/dssyk_observer_process_controls.py` checks:

1. the Cauchy Fourier density and overlap for $f_\beta$;
2. the one-bin phase-diary filter;
3. fresh and persistent two-bin completions with equal marginals;
4. the finite two-contact parity-memory record in (5.5)--(5.6);
5. the contact-kick control (5.7);
6. exact one-copy/doubled isometric transport;
7. the model-specific clock cap and Euclidean-fold controls retained from the
   earlier pass.

## Primary sources

- Chandrasekaran, Longo, Penington, and Witten,
  [*An Algebra of Observables for de Sitter Space*](https://arxiv.org/abs/2206.10780).
- Chen, Stanford, Tang, and Yang,
  [*Negative Shocks versus Static Patch Holography*](https://arxiv.org/abs/2607.14042).
- Narovlansky and Verlinde,
  [*Double-scaled SYK and de Sitter Holography*](https://arxiv.org/abs/2310.16994).
- Aguilar-Gutierrez,
  [*Symmetry Sectors in Chord Space and Relational Holography in the DSSYK*](https://arxiv.org/abs/2506.21447).
- Tietto and Verlinde,
  [*A Microscopic Model of de Sitter Spacetime with an Observer*](https://arxiv.org/abs/2502.03869).
- Fewster and Verch,
  [*Quantum Fields and Local Measurements*](https://arxiv.org/abs/1810.06512).
- Polo-Gomez, Garay, and Martin-Martinez,
  [*A Detector-Based Measurement Theory for Quantum Field Theory*](https://arxiv.org/abs/2108.02793).
- Jorgensen and Pollock,
  [*Exploiting the Causal Tensor Network Structure of Quantum Processes to Efficiently Simulate Non-Markovian Path Integrals*](https://arxiv.org/abs/1902.00315).
- Espindola and Ali,
  [*Spectral Admissibility of Real Observers in Euclidean de Sitter Gravity*](https://arxiv.org/abs/2605.30423).
- Egusquiza and Muga,
  [*Free Motion Time-of-Arrival Operator and Probability Distribution*](https://arxiv.org/abs/quant-ph/9905023).
- Leppajarvi and Sedlak,
  [*Post-processing of Quantum Instruments*](https://arxiv.org/abs/2010.15816).
