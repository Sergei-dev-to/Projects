# From de Sitter observer correlators to observer processes

Date: 2026-07-19

Status: the July anti-scrambling literature update, the two cheap analytic
controls, and an exact two-bin nonuniqueness control are complete. The
gravitational multitime completion gate has now been run in
dssyk_observer_process_wp_a3_2026_07_19.md; its contour-depth obstruction
parks the exact folded DSSYK OTOC. A 2026-07-20 follow-up in
dssyk_wp2_clock_resource_gate_2026_07_20.md derives the general one-read clock
overlap and corrects the earlier selection claim. The canonical POVM gives
the Cauchy completion, but the source does not select its post-measurement
instrument. Fresh, persistent, and contact-disturbed completions differ, and
all have the same one-copy/doubled isometric null.

## 1. Why this branch is being opened

The completed doubled-DSSYK result established an exact kinematical null:
when the diary, observer protocol, records, and decoder are transported through
the equal-energy isometry, all record distances and recovery quantities are
unchanged. The follow-on bandwidth gate then showed that the full native
DSSYK bandwidth is

$$
B_{\rm nat}=\frac{4\mathcal J}{\lambda}
=\frac{1}{2\pi G_N},
$$

so the de Sitter radius cancels from the corresponding orthogonalization
time. Neither result supplied the physically selected observer process needed
for a cosmological operational cutoff.

A cluster of papers submitted on 2026-07-14 and 2026-07-15 supplies new,
more physical input:

- observer recoil and backreaction produce de Sitter time advances and
  anti-scrambling OTOCs;
- the observer-energy endpoint smears the tracial two-point function in time,
  with frequency dependence $e^{-\pi |\omega|}$ in de Sitter-radius-one
  units;
- the Hartle--Hawking state fails to remain tracial for the relevant
  backreacted OTOCs;
- an ordinary forward-time detector coupling does not expose those OTOCs in
  the observer's reduced state;
- folded Euclidean evolution in a Hamiltonian bounded above and below gives a
  possible representation of the milder anti-scrambling correlator, but no
  general rule for all correlators is selected.

These facts do not reopen unrestricted WP2. They identify a better question:

> Which de Sitter observer correlators admit a positive, causal, and
> resource-bounded observer-process completion, and what role does DSSYK's
> bounded spectrum play in the cost of that completion?

This note separates two exact controls from the hard multitime question.

## 2. Claim ladder

The following statements must not be conflated.

1. **Low-point transfer data.** A two-point correlator is smeared with a
   transfer factor $e^{-a|\omega|}$.
2. **Positive completion.** There exists a completely positive trace-
   preserving channel that realizes the same transfer factor.
3. **Selected observer process.** Gravity or the duality selects that channel,
   including its multitime memory structure, as the physical observer comb.
4. **Operational cutoff.** A finite resource budget turns the channel's soft
   suppression into a bound on distinguishability or recovery.
5. **Constraint-induced advantage.** The doubled equal-energy description
   performs differently from its isometrically transported one-copy control.

The calculations below establish item 2, a conditional version of item 4, and
an exact obstruction to inferring item 3 from one-bin data: two causal
completions can have the same one-bin channel and different two-bin outputs.
The existing isometry theorem excludes item 5 for exactly transported classes.

## 3. WP-A1: the Cauchy clock-jitter control

### 3.1 Input from the observer two-point function

Chen, Stanford, Tang, and Yang obtain, in $R_{\rm dS}=1$ units, a tracial
two-point function whose time dependence is a convolution with a Cauchy-shaped
kernel. In frequency space the nontrivial transfer factor is

$$
f(\omega)=e^{-\pi |\omega|}.
$$

Restoring the de Sitter radius gives the scale

$$
a=\pi R_{\rm dS},
\qquad
f_R(\omega)=e^{-a|\omega|}.
$$

The overall normalization of the gravitational correlator is not used below.
The control is the normalized channel with the same frequency dependence.

### 3.2 A canonical positive completion

Define the normalized Cauchy density

$$
k_a(s)=\frac{a}{\pi(a^2+s^2)},
\qquad
\int_{-\infty}^{\infty}ds\,k_a(s)=1,
$$

whose characteristic function is

$$
\int_{-\infty}^{\infty}ds\,k_a(s)e^{-i\omega s}
=e^{-a|\omega|}.
$$

For a system Hamiltonian $H$, define

$$
\Phi_a(\rho)
=\int_{-\infty}^{\infty}ds\,k_a(s)
e^{-iHs}\rho e^{iHs}.
$$

This is a random-unitary CPTP channel. In an energy eigenbasis,

$$
\Phi_a\!\left(|E_m\rangle\langle E_n|\right)
=e^{-a|E_m-E_n|}|E_m\rangle\langle E_n|.
$$

It also obeys the semigroup law

$$
\Phi_a\circ\Phi_b=\Phi_{a+b}.
$$

Thus the observer two-point transfer factor has at least one exact positive
completion: Cauchy-distributed uncertainty in clock time, equivalently a
dephasing channel generated spectrally by $|\operatorname{ad}_H|$.

This completion is a control, not a uniqueness claim. A two-point function
does not determine whether successive clock errors are independent, share a
common offset, form a Lévy process, or arise from another memoryful dilation.

### 3.3 Exact phase-diary discrimination

Take the binary, equal-population phase code

$$
|\psi_\pm\rangle
=\frac{|E_0\rangle\pm|E_1\rangle}{\sqrt 2},
\qquad
\Delta E=|E_1-E_0|,
$$

and let

$$
\eta=e^{-a\Delta E}.
$$

After the channel, the two states have identical energy populations and
opposite off-diagonal entries of magnitude $\eta/2$. Their one-record trace
distance is exactly

$$
\delta_1
=\frac12\left\|\Phi_a(\psi_+)-\Phi_a(\psi_-)\right\|_1
=\eta
=e^{-a\Delta E}.
$$

The two outputs commute. In their common eigenbasis their probability vectors
are

$$
\left(\frac{1+\eta}{2},\frac{1-\eta}{2}\right),
\qquad
\left(\frac{1-\eta}{2},\frac{1+\eta}{2}\right).
$$

The quantum Chernoff exponent for independent records is therefore

$$
\xi(\eta)
=-\frac12\log(1-\eta^2)
=\frac{\eta^2}{2}+O(\eta^4).
$$

At fixed target error in the strongly smeared regime, the required record
count scales as

$$
N_{\rm rec}=\Theta(\eta^{-2})
=\Theta\!\left(e^{2a\Delta E}\right).
$$

With $a=\pi R_{\rm dS}$, a finite record budget consequently gives the soft
operational frequency scale

$$
\Delta E_{\rm op}
\sim\frac{\log N_{\rm rec}}{2\pi R_{\rm dS}}
$$

up to the target-error constant. Since $R_{\rm dS}^{-1}\propto\sqrt\Lambda$,
this is a precise conditional sense in which the cosmological constant sets
an observer-relative temporal bandwidth.

### 3.4 One-bin data do not select the multitime comb

The ambiguity can be made exact without choosing a gravitational four-point
function. For two record bins, compare a fresh-jitter completion,

$$
\Phi_{a,\mathrm{fresh}}^{(2)}
=\Phi_a\otimes\Phi_a,
$$

with a common-offset completion,

$$
\Phi_{a,\mathrm{common}}^{(2)}(\rho)
=\int_{-\infty}^{\infty}ds\,k_a(s)
(U_s\otimes U_s)\rho(U_s^\dagger\otimes U_s^\dagger),
\qquad U_s=e^{-iHs}.
$$

Both are random-unitary CPTP processes. The first draws a new classical clock
error in each bin; the second samples one error at the start and retains it as
classical memory. Both are causally ordered and have exactly the same
one-bin restriction $\Phi_a$.

Their two-bin predictions nevertheless differ. For

$$
|\chi\rangle
=\frac{|E_0E_1\rangle+|E_1E_0\rangle}{\sqrt2},
\qquad
\chi=|\chi\rangle\langle\chi|,
$$

the common-offset channel preserves the exchange coherence because the two
branches have the same total energy. The fresh-jitter channel multiplies that
coherence by $\eta^2=e^{-2a\Delta E}$. Hence

$$
\frac12\left\|
\Phi_{a,\mathrm{common}}^{(2)}(\chi)
-\Phi_{a,\mathrm{fresh}}^{(2)}(\chi)
\right\|_1
=\frac{1-\eta^2}{2},
$$

and, using the full diamond-norm convention,

$$
\left\|
\Phi_{a,\mathrm{common}}^{(2)}
-\Phi_{a,\mathrm{fresh}}^{(2)}
\right\|_\diamond
\geq 1-\eta^2.
$$

This is a process-discrimination witness, not yet a claim that the passive
static-patch observer can prepare and read the coherent two-bin tester
$\chi$. Pricing or excluding that tester is part of WP-A3.

The disagreement becomes order one precisely when each individual bin is
strongly smeared. Thus the one-bin transfer factor does not merely leave a
formal dilation ambiguity: it permits operationally different multitime
records. Gravitational four-point data or an independently derived clock
model must select or exclude the memory structure.

### 3.5 What the controls do not prove

The result is deliberately weaker than a fundamental UV cutoff.

- The suppression is soft: no finite energy coherence is set exactly to zero.
- Unlimited records can overcome any fixed nonzero suppression.
- The Chernoff scaling assumes fresh, independent records. A shared clock
  offset gives a correlated record process and need not obey that scaling.
- Every energy population is preserved, so information encoded diagonally in
  energy is not cut off at all.
- Other encodings can use small gaps or degeneracies.
- The two-point data do not uniquely select this multitime channel.
- Under the equal-energy isometry, the same channel and phase code transport
  to one copy with identical performance. The effect is therefore not access
  created by the doubled constraint.

The gain is narrower but real: this is an exact positive process with the
correct de Sitter transfer scale, and it shows explicitly how a finite record
budget converts correlator smearing into an operational limitation.

## 4. WP-A2: direct implementation cost of a Euclidean fold

### 4.1 Deterministic versus heralded evolution

Let $H$ have spectral range

$$
E_{\min}\leq H\leq E_{\max},
\qquad B=E_{\max}-E_{\min},
$$

and consider a backwards Euclidean segment $A_\tau=e^{\tau H}$ with
$\tau>0$. The normalized state transformation

$$
\mathfrak B_\tau(\rho)
=\frac{A_\tau\rho A_\tau}
{\operatorname{Tr}(A_\tau\rho A_\tau)}
$$

is nonlinear unless $H$ is constant on the declared input domain. It is
therefore not a deterministic quantum channel on arbitrary inputs.

The optimally normalized direct heralded branch is

$$
K_\tau=e^{\tau(H-E_{\max})}.
$$

Indeed, a successful Kraus operator proportional to $e^{\tau H}$ is trace
nonincreasing only if

$$
K_\tau^\dagger K_\tau\leq I,
$$

and scaling by $e^{-\tau E_{\max}}$ is the largest state-independent
normalization that satisfies this condition. Its success probability is

$$
p_\tau(\rho)
=\operatorname{Tr}\!\left[
\rho e^{-2\tau(E_{\max}-H)}\right].
$$

The exact uniform bounds are

$$
e^{-2\tau B}\leq p_\tau(\rho)\leq 1,
\qquad
p_{\rm worst}=e^{-2\tau B}.
$$

If the operation is required only on a code shell $D$ with occupied spectral
width $B_D=E_+^D-E_-^D$, the optimal shell normalization instead gives

$$
p_{\rm worst}(D)=e^{-2\tau B_D}.
$$

For the maximally mixed state on that shell, the directly relevant average is

$$
\bar p_D(\tau)
=\frac{1}{d_D}\operatorname{Tr}_D
e^{-2\tau(E_+^D-H_D)}.
$$

This last expression, rather than the full-band worst case, is the quantity to
evaluate if a future bulk argument physically selects a microcanonical diary
shell.

### 4.2 DSSYK scaling

For the native DSSYK spectrum,

$$
B_{\rm nat}=\frac{4\mathcal J}{\lambda}.
$$

Using

$$
\mathcal J=\frac1{R_{\rm dS}},
\qquad
\frac{R_{\rm dS}}{G_N}=\frac{8\pi}{\lambda},
$$

gives

$$
B_{\rm nat}=\frac{1}{2\pi G_N}.
$$

For a fold whose backwards Euclidean extent is
$\tau=cR_{\rm dS}$,

$$
p_{\rm worst}^{\rm full}
=\exp\!\left[-\frac{cR_{\rm dS}}{\pi G_N}\right]
=e^{-O(S_{\rm dS})}.
$$

The exact coefficient relating $R_{\rm dS}/G_N$ to entropy depends on the
dimensional convention, but the semiclassical entropy scaling does not. Thus
finite upper energy makes a Euclidean fold mathematically well-defined while
its direct, full-band, state-independent implementation can be
nonperturbatively unlikely.

The shell alternative is a genuine fork:

- if $B_D=O(R_{\rm dS}^{-1})$, then a fold of extent $O(R_{\rm dS})$ can have
  order-one worst-case success;
- if $B_D=O(G_N^{-1})$, the entropy-suppressed cost remains;
- choosing the shell after seeing the answer is not allowed. Its width and
  stability under the inserted operators must follow from the bulk observer
  construction.

### 4.3 Scope of the cost statement

This is a theorem about direct, single-branch physical implementation of the
normalized nonunitary segment. It is not a lower bound on every algorithm for
estimating an imaginary-time correlator. Adaptive imaginary-time algorithms,
block encodings, randomized measurements, replicas, tomography, Hamiltonian
inversion, or classical spectral knowledge can trade postselection for other
resources. Those alternatives reinforce rather than remove the operational
question: a correlator becomes observer access only after the allowed
resources are declared and budgeted.

## 5. Combined interpretation

The two controls expose a useful asymmetry.

| Input | Positive observer realization | Cost statement | What is still missing |
|---|---|---|---|
| Two-point smearing $e^{-\pi R|\omega|}$ | canonical Cauchy random-offset completion; fresh and persistent instruments agree in one read but differ in two | independent phase-diary records cost $e^{2\pi R\Delta E}$ only within the chosen fresh completion | time POVM, instrument, contact backreaction, and preparation/reset rule |
| Folded Euclidean correlator | direct realization is a heralded nonunitary branch | full DSSYK band costs $e^{-O(S_{\rm dS})}$ in worst-case success | selected shell or alternative measurement resource |
| Doubled equal-energy representation | exact isometric transport to one copy | all transported costs and records agree | a nontransported restriction derived by the bulk dictionary |

The original cutoff question can therefore be answered more precisely:

> The de Sitter radius can set a soft observer-time filter, and finite DSSYK
> bandwidth can make folded correlators mathematically admissible. Neither is
> a fundamental UV regulator or free information access. An operational
> cutoff arises only relative to a finite record, control, or postselection
> budget.

### 5.1 Clock-state/instrument correction (2026-07-20)

The CLPW maximum-entropy clock fixes a state, not a measurement process. Its
energy wavefunction

$$
f_\beta(x)=\sqrt\beta\,e^{\beta x/2}\Theta(-x)
$$

has canonical covariant-time density

$$
|\widetilde f_\beta(s)|^2
=\frac{\beta/2}{\pi[(\beta/2)^2+s^2]}.
$$

Thus $a=\beta_{\rm dS}/2=\pi R_{\rm dS}$, exactly reproducing the
Cauchy density above after choosing the canonical covariant time POVM. A
random-time system channel is a further positive completion. CLPW do not
specify that POVM's Naimark dilation or post-measurement instrument. In
particular, retaining one undisturbed pointer gives common-offset memory,
while discarding and preparing a fresh clock gives independent offsets; a
contact kick gives a third process. The clock state selects none of them.

The alternative completions expose a relational sector rather than a hard UV
cutoff. For

$$
|\chi_\pm\rangle
=\frac{|E_0E_1\rangle\pm|E_1E_0\rangle}{\sqrt2},
$$

either one-bin marginal is diary blind, while the common-clock two-bin trace
distance is one because both branches have the same total energy. Fresh clocks
would instead give $e^{-2\pi R_{\rm dS}\Delta E}$. Extending the equal-energy
isometry by the identities on clock and detector memory reproduces all these
statements exactly in the isospectral one-copy control. The unresolved input
begins with the clock instrument and continues through detector interaction
action, contact count, and compiler cost.

## 6. WP-A3: pre-registered multitime completion gate

The next hard step is not an unrestricted DSSYK OTOC. It is a completion test
using the gravitational four-point data already available.

Outcome: this gate is complete. The anti-scrambling four-point functional is
a proper 2-OTO object, while a passive observer's reduced record is a 1-OTO
Schwinger--Keldysh object. A timefold compiler is therefore an additional
resource, and no positive diary-record tester is selected by the correlator
alone. The proof and resource audit are in
dssyk_observer_process_wp_a3_2026_07_19.md. The declarations below are
retained as the pre-registration against which that verdict was reached.

### 6.1 Declared passive class

Begin with a passive observer class containing:

- forward-time unitary system--detector couplings;
- one observer memory initialized independently of the diary;
- causal adaptive measurements on that memory;
- no Hamiltonian sign reversal;
- no postselected Euclidean segment;
- no independently prepared replica, precursor state, or full tomography.

Any enlarged class must name and charge for the added resource.

### 6.2 Deliverables

1. Assign the gravitational four-point functional to operational time-bin
   slots without changing its operator ordering after the fact.
2. Test the exact fresh-jitter and common-offset controls against that
   functional. If neither applies, state the additional memory structure
   independently of the desired access verdict.
3. Define the diary-blind comparison by scrambling the phase label while
   leaving the clock process fixed.
4. Determine whether the witness is realizable in the passive class. If not,
   lower-bound the strategy distance to that class or identify the minimum
   extra timefold/copy/postselection resource.
5. Transport the complete allowed class through the equal-energy isometry and
   verify that any surviving difference is not a representation artifact.

### 6.3 Stop conditions

Stop before an exact DSSYK OTOC if any of the following occurs:

- the gravitational correlator cannot be assigned to operational slots
  independently of the desired conclusion;
- the proposed witness only restates the known trace/KMS positivity failure;
- a standard OTOC measurement protocol realizes it once an unpriced external
  controller, replica, or precursor is added;
- the two-point smearing alone does not determine the multitime memory
  structure;
- the one-copy and doubled results differ only because different resource
  classes were assigned;
- the DSSYK calculation would merely reproduce an existing OTOC, entropy, or
  complexity curve without a diary-record consequence.

Proceed to an exact DSSYK calculation only if the completion test leaves a
model-specific quantity, such as a physically selected shell-averaged fold
success, a finite-$\lambda$ correction to the observer filter, or a
disorder-stable distance from the passive class.

## 7. Decision

WP-A1, its exact two-bin nonuniqueness witness, and the generic/direct part of
WP-A2 are cheap, exact, and useful. WP-A3 has supplied the structural verdict:
the gravitational anti-scrambling functional has greater contour depth than
the passive observer record. The clock follow-up supplies a stronger negative
result: the state and canonical one-read data do not select a multitime
instrument, while explicit fresh, persistent, and contact-disturbed
completions all have zero one-copy/doubled differential. This gives the
reopened program a concrete contribution without competing head-on with the
new gravitational OTOC literature. An exact folded DSSYK OTOC remains parked.
A further branch is warranted only if the bulk dictionary selects a clock
instrument and prices a detector interaction or 2-OTO-to-record compiler.

## Primary sources

- Alexey Milekhin, Vladimir Narovlansky, and Jiuci Xu,
  [*Out-of-Time-Ordered Correlators in de Sitter Revisited*](https://arxiv.org/abs/2607.13137),
  arXiv:2607.13137.
- Wentao Cui and David K. Kolchmeyer,
  [*A de Sitter Anti-Scrambling Algebra*](https://arxiv.org/abs/2607.13665),
  arXiv:2607.13665.
- Yiming Chen, Douglas Stanford, Haifeng Tang, and Zhenbin Yang,
  [*Negative Shocks versus Static Patch Holography*](https://arxiv.org/abs/2607.14042),
  arXiv:2607.14042.
- Daniel Harlow and Ying Zhao,
  [*Anti-Scrambling and Euclidean Folds from Observer Correlators in de Sitter Space*](https://arxiv.org/abs/2607.14215),
  arXiv:2607.14215.
- Venkatesa Chandrasekaran, Roberto Longo, Geoff Penington, and Edward Witten,
  [*An Algebra of Observables for de Sitter Space*](https://arxiv.org/abs/2206.10780),
  arXiv:2206.10780.
- Magdalini Zonnios, Jesper Levinsen, Meera M. Parish, Felix A. Pollock, and
  Kavan Modi,
  [*Signatures of Quantum Chaos in an Out-of-Time-Order Tensor*](https://arxiv.org/abs/2105.08282),
  arXiv:2105.08282.
- Chiara Leadbeater, Nathan Fitzpatrick, David Munoz Ramo, and Alex J. W. Thom,
  [*Non-unitary Trotter Circuits for Imaginary Time Evolution*](https://arxiv.org/abs/2304.07917),
  arXiv:2304.07917.
- Philip Daniel Blocher et al.,
  [*Measuring Out-of-Time-Ordered Correlation Functions without Reversing Time Evolution*](https://arxiv.org/abs/2003.03980),
  arXiv:2003.03980.
