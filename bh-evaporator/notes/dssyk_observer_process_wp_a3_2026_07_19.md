# WP-A3 result: the contour-depth obstruction

Date: 2026-07-19

Status: complete. The pre-registered completion gate has fired a stop
condition. The de Sitter anti-scrambling four-point function is a proper
two-fold OTO functional, while the declared passive observer record is an
ordinary one-fold Schwinger--Keldysh object. A physical compiler between those
objects requires an extra resource. No exact DSSYK OTOC is authorized by this
result.

## 1. Question and verdict

WP-A3 asked whether the gravitational four-point data could be assigned to
the slots of a positive, causal diary-to-record comb and thereby select
between the fresh-jitter and common-offset completions of the observer
two-point filter.

The answer is no at the declared passive level:

> The anti-scrambling OTOC is not a linear statistic of the passive
> observer's final record. It has greater contour depth than the record
> process. Turning it into a record requires a timefold compiler--for example
> Hamiltonian reversal, a coherent copy or ancilla protocol, repeated
> state preparation with global measurements, a probe OTOC, or a postselected
> Euclidean fold.

This is a typing obstruction, not a claim that OTOCs are unmeasurable. It
means that the implementation of the OTOC, rather than the correlator alone,
is the missing observer-resource rule.

## 2. Primary-source facts used

1. The gravitational object has the alternating early/late ordering of a
   chaos OTOC. Milekhin, Narovlansky, and Xu explicitly study one-sided,
   two-sided, and thermally regularized four-point OTO configurations.
2. In the standard classification, the chaos commutator square and its
   alternating Wightman terms are proper 2-OTO objects: two forward and two
   backward contour legs are required. This is the contour-depth statement,
   not a statement about Lyapunov behavior.
3. Cui and Kolchmeyer analyze the ordinary coupling
   \(H_{\rm int}(t)=X(t)\phi(t)\) and state that the observer's reduced density
   matrix is insensitive to their OTOCs; an observer who cannot reverse the
   arrow of time cannot observe the KMS failure by that evolution.
4. Harlow and Zhao reproduce the milder anti-scrambling sign using a
   backwards Euclidean fold in a system bounded above and below. Their
   continuation depends on the operator ordering, contains an arbitrary
   integer \(n\), and is not offered as a general rule for de Sitter
   correlators.
5. Forward-only OTOC reconstruction protocols exist, but they change the
   resource declaration. For arbitrary \(V\), the Blocher et al. route uses
   repeated preparation of a basis and coherent superpositions and requires
   up to \(2d^2\) expectation values. It is therefore a tomography-like
   cross-run estimator, not one passive observer record.
6. The out-of-time-order tensor of Zonnios et al. already supplies a positive
   higher-order operational object for OTO experiments. Its implementation
   takes the requisite forward and reversed processes as resources. It does
   not derive their availability or cost from a de Sitter observer model.

These points are supported by:

- [Haehl, Loganayagam, Narayan, and Rangamani, *Classification of
  out-of-time-order correlators*](https://arxiv.org/abs/1701.02820);
- [Blocher et al., *Measuring out-of-time-ordered correlation functions
  without reversing time evolution*](https://arxiv.org/abs/2003.03980);
- [Chaudhuri and Loganayagam, *Probing Out-of-Time-Order
  Correlators*](https://arxiv.org/abs/1807.09731);
- [Zonnios et al., *Signatures of Quantum Chaos in an Out-of-Time-Order
  Tensor*](https://arxiv.org/abs/2105.08282);
- [Milekhin, Narovlansky, and Xu, *Out-of-Time-Ordered Correlators in de
  Sitter Revisited*](https://arxiv.org/abs/2607.13137);
- [Cui and Kolchmeyer, *A de Sitter Anti-Scrambling
  Algebra*](https://arxiv.org/abs/2607.13665);
- [Chen, Stanford, Tang, and Yang, *Negative Shocks versus Static Patch
  Holography*](https://arxiv.org/abs/2607.14042);
- [Harlow and Zhao, *Anti-Scrambling and Euclidean Folds from Observer
  Correlators in de Sitter Space*](https://arxiv.org/abs/2607.14215).

## 3. Passive-record contour proposition

Let \(S\) be the static-patch fields and \(D\) the observer memory. In the
declared passive class, their joint evolution from \(0\) to \(T\) is

$$
U(T)=\mathcal T\exp\left[-i\int_0^Tdt\,H_{\rm int}(t)\right],
$$

with no Hamiltonian sign reversal, replica, precursor, or postselected
Euclidean segment. A final record probability is

$$
p(r)=\operatorname{Tr}\left[
(M_r\otimes I_S)U(T)(\rho_D\otimes\rho_S)U(T)^\dagger
\right].
$$

Expanding \(U\) and \(U^\dagger\) gives environmental coefficients of the
form

$$
\operatorname{Tr}_S\left[
\widetilde{\mathcal T}\{\phi(t'_1)\cdots\phi(t'_m)\}
\rho_S
\mathcal T\{\phi(t_1)\cdots\phi(t_n)\}
\right].
$$

They live on one ordinary closed-time Schwinger--Keldysh contour. Causal
adaptive measurements do not change this conclusion: by deferred
measurement they can be dilated to forward controlled unitaries on a larger
observer memory followed by one final POVM.

**Passive-record contour proposition.** Every linear statistic of the final
record in this class depends only on 1-OTO environmental functionals. A
proper 2-OTO four-point functional cannot be such a statistic unless the
protocol class is enlarged.

The proposition is a direct Dyson-expansion statement. It is also exactly the
operational distinction made in the probe literature: ordinary reduced-state
dynamics is determined by 1-OTO influence data, whereas system 2-OTO data can
appear only in corresponding OTO correlators of the probe. Cui and
Kolchmeyer's de Sitter observer coupling is the model-specific instance.

## 4. Slot-assignment audit

The anti-scrambling configurations alternate early and late insertions. If
their algebraic product order is preserved, a two-fold contour is required.
If the insertions are instead placed into monotonically ordered causal slots,
the product is changed into a time-ordered or ordinary Schwinger--Keldysh
correlator. That is a different observable and loses the anti-scrambling
sign.

Accordingly, the gravitational functional cannot be inserted as a positive
tester on the passive comb merely by naming its four operators as four
observer slots. The missing object is a physical 2-OTO-to-record compiler.
Without it:

- there is no normalized positive tester;
- there is no diary-labelled record channel;
- there is no diary-blind comparison comb;
- the correlator violation cannot yet be converted into a strategy-distance
  or recovery bound.

The positivity and cyclicity failures found by Chen et al. sharpen this
conclusion. They separate the gravitational functional from a conventional
tracial realization; they do not themselves provide a positive record
tester.

## 5. Fresh versus common Cauchy memory

The fresh-jitter and common-offset constructions remain useful controls, but
the four-point data do not select between them.

- Both are positive, causal 1-OTO record processes.
- Both reproduce the same one-bin Cauchy dephasing channel.
- They differ on a coherent two-bin process tester, as proved in
  dssyk_observer_process_completion_2026_07_19.md.
- The gravitational anti-scrambling functional is not that tester and is not
  a passive-record statistic.

One may append a chosen 2-OTO compiler to either Cauchy process and then
calculate a four-point response. That comparison would measure the composite
of clock memory and compiler. It could not be attributed to the de Sitter
constraint or to the Cauchy filter alone.

Thus WP-A3 deliverable 2 had a definite outcome: neither completion is
selected or excluded by the gravitational four-point discriminator, because
that discriminator and the passive record process have different operational
types.

A later clock-state/instrument pass sharpens this statement. Choosing the
canonical time POVM gives the Cauchy one-read density, but CLPW do not select
its post-measurement instrument. Retaining an undisturbed Naimark pointer gives
a common offset; resetting the clock gives fresh offsets; contact disturbance
gives further completions. None compiles the proper 2-OTO gravitational
functional into a record, and every completed process has an exact
one-copy/doubled null. The derivation is in
`dssyk_wp2_clock_resource_gate_2026_07_20.md`.

## 6. Resource audit for possible compilers

| Compiler route | Added resource | Why it is outside the passive class |
|---|---|---|
| Loschmidt echo | \(H\mapsto-H\) or implementation of \(U^\dagger\) | explicit reversal of native evolution |
| Interferometric/copy protocol | ancilla, replica, controlled operations, or coherent branch comparison | extra system and coherent control |
| Randomized or basis reconstruction | repeated preparation, many measurement settings, classical nonlinear estimator | not one sequential observer record |
| Blocher forward-only reconstruction | known basis states and their superpositions; up to \(2d^2\) expectations for arbitrary \(V\) | tomography-like global preparation and readout |
| Probe-OTOC route | measurement of the probe's own 2-OTO correlator | the probe reduced density matrix is insufficient |
| Out-of-time-order tensor | a higher-order process containing forward and reversed evolutions | operationally positive, but reversal remains a supplied rather than de Sitter-derived resource |
| Euclidean fold | backwards imaginary-time segment or negative-temperature/sign-flipped description | nonunitary direct branch, with postselection cost \(e^{-2\tau B}\) |

These routes are not interchangeable for an access claim. They can estimate
the same algebraic correlator while generating different physical records,
success probabilities, sample costs, and failure modes.

## 7. DSSYK decision

Four pre-registered stop conditions fire:

1. The gravitational correlator cannot be assigned to passive operational
   slots while preserving its ordering.
2. Standard realizations require an added controller, copy, repeated
   preparation, probe OTOC, or Euclidean postselection.
3. The two-point smearing alone does not determine the multitime memory
   structure. An explicit ideal no-reset clock can do so, but is additional
   model input and remains 1-OTO.
4. An exact DSSYK OTOC would presently reproduce a correlator curve without a
   diary-record consequence.

Therefore:

> Do not compute the exact folded DSSYK OTOC as the next project step.

The full-band Euclidean success bound remains relevant if a future bulk
dictionary selects the fold as the physical compiler. Until then, calculating
the folded correlator would test Harlow--Zhao's analytic-continuation proposal,
not observer recovery and not a constraint-induced access advantage.

## 8. Surviving promising direction

The only potentially useful successor is a **bulk-selected contour-conversion
cost for observer access**, not a new OTOC curve. Its central quantity would be

$$
C_{\rm fold}(\mathcal F;\epsilon)
=\inf_{\Gamma}
\left\{\operatorname{cost}(\Gamma):
\Gamma\text{ compiles the 2-OTO functional }\mathcal F
\text{ into a 1-OTO record to error }\epsilon\right\}.
$$

The compiler \(\Gamma\), its allowed controls, record, and comparison process
must be declared before evaluating DSSYK. This is not proposed as a new
general classification of OTO contours; that classification is standard.
The potentially new use is to make contour-conversion cost the missing
operational datum in static-patch holography.

The broad move from OTO correlators to positive higher-order processes already
exists in the out-of-time-order-tensor literature. The possibly new de Sitter
question is only whether the bulk observer dictionary selects a compiler and
fixes its cost. The CLPW clock pass prices time resolution but not reversal,
copy, postselection, detector action, or contact count. This direction earns
another work package only if one of those resources is derived from the bulk
construction. Otherwise the current contour-depth demarcation is the endpoint.
