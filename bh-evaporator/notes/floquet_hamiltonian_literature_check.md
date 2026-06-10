# Floquet Hamiltonian Literature Check

## Question

Is a repeated unitary cycle meaningfully Hamiltonian evolution?

## Answer

It is Hamiltonian evolution in the standard Floquet/stroboscopic sense.

Use this distinction:

```text
driven or stroboscopic Hamiltonian protocol
versus
simple time-independent autonomous Hamiltonian.
```

## Literature Baseline

Floquet theory for a periodically driven quantum system starts from a
time-periodic Hamiltonian:

```text
H(t + T) = H(t).
```

The one-period evolution operator is:

```text
U(T) = T exp[-i integral_0^T H(t) dt].
```

One then defines a Floquet Hamiltonian by:

```text
U(T) = exp[-i H_F T].
```

So a repeated unitary cycle:

```text
|psi_{n+1}> = U_cycle |psi_n>
```

is exactly stroboscopic Hamiltonian evolution:

```text
|psi_n> = exp[-i n H_F T] |psi_0>.
```

The logarithm is not unique, so `H_F` has branch/quasienergy ambiguities. But
the stroboscopic equivalence is standard.

## Useful References

### Floquet engineering reviews

Bukov, D'Alessio, and Polkovnikov review high-frequency periodically driven
systems and the effective Floquet Hamiltonian framework:

```text
Marin Bukov, Luca D'Alessio, Anatoli Polkovnikov,
"Universal High-Frequency Behavior of Periodically Driven Systems:
from Dynamical Stabilization to Floquet Engineering",
arXiv:1407.4803.
https://arxiv.org/abs/1407.4803
```

Goldman and Dalibard review effective Hamiltonians and engineered gauge fields
in periodically driven systems:

```text
N. Goldman and J. Dalibard,
"Periodically-driven quantum systems: Effective Hamiltonians and engineered
gauge fields",
Phys. Rev. X 4, 031027 (2014).
https://arxiv.org/abs/1404.4373
https://doi.org/10.1103/PhysRevX.4.031027
```

Oka and Kitamura review Floquet engineering in quantum materials, explicitly
framing it as control by periodic driving and effective Hamiltonians:

```text
Takashi Oka and Sota Kitamura,
"Floquet Engineering of Quantum Materials",
Annual Review of Condensed Matter Physics 10, 387-408 (2019).
https://arxiv.org/abs/1804.03212
https://doi.org/10.1146/annurev-conmatphys-031218-013423
```

Weitenberg and Simonet review Floquet engineering in quantum gases as a way to
realize new Hamiltonians by periodic driving:

```text
Christof Weitenberg and Juliette Simonet,
"Tailoring quantum gases by Floquet engineering",
Nature Physics 17, 1342-1348 (2021).
https://www.nature.com/articles/s41567-021-01316-x
```

### Autonomous Hamiltonian computation / clock constructions

The stronger question is whether an externally staged unitary circuit can be
embedded into a time-independent Hamiltonian with a clock. That is also a known
theme, going back to Benioff, Feynman, and later Feynman-Kitaev clock
constructions.

```text
Paul Benioff,
"The computer as a physical system: A microscopic quantum mechanical
Hamiltonian model of computers as represented by Turing machines",
Journal of Statistical Physics 22, 563-591 (1980).
https://doi.org/10.1007/BF01011339
```

```text
Richard P. Feynman,
"Quantum Mechanical Computers",
Foundations of Physics 16, 507-531 (1986).
https://authors.library.caltech.edu/records/q2nej-gkv15/latest
```

For a modern discussion using the Feynman/Kitaev clock idea:

```text
"Feynman's clock, a new variational principle, and parallel-in-time quantum
dynamics",
PNAS 110, 17949-17954 (2013).
https://pmc.ncbi.nlm.nih.gov/articles/PMC3799300/
```

## Implication For Our Model

The current evaporator cycle is Hamiltonian-realizable:

```text
The repeated unitary cycle is Hamiltonian-realizable as a driven/stroboscopic
system.
```

Open naturalness question:

```text
derive the same staged behavior from a simple time-independent autonomous
Hamiltonian without an engineered protocol.
```

This is a naturalness gap.

## How To Phrase The Standard

Use:

```text
Hamiltonian-realizable driven/stroboscopic cycle
```

for the current result.

Use:

```text
simple time-independent autonomous Hamiltonian
```

for the stronger follow-up.

Avoid this framing:

```text
Floquet versus Hamiltonian.
```

That phrasing is misleading.
