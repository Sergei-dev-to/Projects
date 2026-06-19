# Directions Review

Date: 2026-06-18

Role: result stack

Status: current research map

## Current Center

The program now has a stable technical spine:

```text
private recovery = access geometry/algebra + coherent export.
```

For source-local finite-velocity access, the record channel is nearly
constant on a remote diary before graph/light-cone access. Recovery then
requires export:

```text
rho_{R_D C} approx rho_{R_D} tensor rho_C.
```

The main warning is:

```text
visibility is not recovery.
```

OTOCs, commutators, or boundary sensitivity can show access/visibility.
They do not by themselves prove decoupling/export.

## Direction 1: Theorem-Backed Expander Mixer

Result target:

```text
bounded-degree/log-diameter access geometry
+ theorem-backed TPE/design or random-circuit decoupling primitive
=> logarithmic or polylogarithmic location-uniform private recovery.
```

Where it leads:

This proves the fast-routing branch is nonempty. It is the clean
positive counterpart to the latency obstruction.

Payoff:

High. It is the first horizon-like fast-recovery existence theorem in
the program.

Risk:

Moderate. The theorem-backed mixer is engineered. The result should be
presented as an existence mechanism, not as a natural Hamiltonian.

Status:

Already incorporated in `main.tex` as the expander mixer theorem.

Next strengthening:

Replace the theorem-backed mixer with a fixed deterministic expander
Hamiltonian or Floquet system by proving the relevant second-moment
export gap.

## Direction 2: Deterministic Expander Export

Result target:

```text
fixed bounded-degree expander Hamiltonian/Floquet dynamics
=> O(log S) collection
=> decoupling/export for the emitted records
=> HP recovery.
```

Where it leads:

This would be the genuinely strong version of the fast-routing branch:
finite-degree deterministic dynamics realizes horizon-like private
recovery without inserting a design mixer.

Payoff:

Very high. This is the first candidate for a field-level result rather
than a theorem-backed construction.

Risk:

High. Known sparse-graph scrambling and OTOC results motivate the route,
but do not automatically imply channel decoupling for the emitted-record
partition.

Key obstruction:

```text
operator growth != decoupling/export.
```

Best route:

Use the moment-gap export criterion now in `main.tex`: prove that the
second-moment channel of the expander dynamics contracts in the
small-subsystem decoupling norm controlling the HP recovery functional
for the fixed diary and emitted-record partition. OTOC/operator-growth
bounds are supporting diagnostics; the load-bearing object is the
second-moment/export gap for that partition. Global approximate-design
convergence is stronger than needed and can have an extensive initial
deviation, which would erase the logarithmic expander advantage.

## Direction 3: Local Tightness / Dual-Unitary Cuts

Result target:

```text
local finite-velocity dynamics:
    no recovery before light-cone access,
    recovery from an appropriate spacetime record cut after access.
```

Where it leads:

This sharpens the slow/local side. It can clarify the distinction
between boundary visibility and actual recovery.

Payoff:

Medium. It is a clean benchmark but not horizon-fast on a large lattice.

Risk:

Moderate. Single-boundary early records may not recover a diary in an
unbiased reversible circuit; complete spacetime cuts may be the correct
object.

Best route:

Dual-unitary or Clifford-dual-unitary circuits, because tilted cuts and
operator spreading are exactly tractable.

## Direction 4: Failure Classification

Result target:

```text
conditions under which generated record algebras remain reducible,
or export fails, so private information stays protected/deep.
```

Where it leads:

This turns the positive theorem into a classification: fast recovery is
not generic decoherence, saturation, anonymity, or symmetry.

Payoff:

Medium-high. It supplies contrast and prevents overgeneralizing.

Risk:

Low to moderate. Many examples are straightforward, but broad necessary
conditions may be hard.

Primary invariant:

```text
irreducibility and reconstructiveness of the generated *-algebra/channel.
```

Krylov growth is a diagnostic, not the invariant.

## Direction 5: Dressed / Nonlocal Access

Result target:

```text
freeze source-local routing;
if recovery remains, the allowed algebra is dressed/nonlocal or the side
information already contains the diary.
```

Where it leads:

This is the holography/Gauss-law branch. It separates fast recovery by
routing from fast recovery by changing the access algebra.

Payoff:

Conceptually high.

Risk:

High. It depends on a fixed factorization and access model; otherwise it
becomes a verbal restatement of known gravitational dressing debates.

Best use:

Classifier and diagnostic, not the next positive theorem.

## Direction 6: Export Capacity / Code-Size Bounds

Result target:

```text
t_export >= (k + recovery overhead) / c_R
```

or a sharper decoupling/code-size capacity bound for the emitted records.

Where it leads:

This closes a loophole: fast graph access does not imply fast recovery
if the export channel is too narrow.

Payoff:

Medium. It is probably standard dimension/decoupling bookkeeping, but it
is necessary for the access/export framework.

Risk:

Low.

Best use:

State as a theoremlet paired with the access lower bound.

Status:

Now incorporated in `main.tex` as the export capacity bound. The proof
uses mutual information: admissible side information starts independent
of the diary reference, a record of dimension `d_R` can increase that
mutual information by at most `2 log d_R`, and high-fidelity recovery of
a k-qubit diary requires nearly `2k` bits of mutual information with the
reference. Thus `log d_R >= k` up to continuity terms, and
`t_export >= k/c_R` at finite coherent record bandwidth.

## Direction 7: Measurement / Heisenberg Cut

Result target:

```text
public pointer data becomes redundantly accessible quickly,
while private coherence recovery has an export-limited regime not
captured by ordinary redundancy counting.
```

Where it leads:

This is the bridge from horizons to quantum-classical emergence.

Payoff:

Potentially high if it produces a new quantitative prediction or
protocol.

Risk:

High. Public/private redundancy separation is already Quantum Darwinism
and SBS. New content must involve private recovery/export, not merely
the known redundancy ratio.

Best route:

Look for protocols where public data are redundantly recorded but
private coherence recovery is limited by decoupling/reversal resources
rather than by simply collecting more environment fragments.

## Direction 8: Experimental / Numerical Access Profile

Result target:

```text
measure:
    t_public,
    t_private,
    de-protection rate,
    recovery fidelity,
    frozen-routing response.
```

Where it leads:

This could make the program testable inside standard quantum mechanics.

Payoff:

Medium now, higher after a sharper theoretical target.

Risk:

High if it reduces to tomography, quantum erasure, or standard
decoherence diagnostics.

## Missing Branches Checked

The main omitted branch was export capacity. It is now explicit.

No separate branch is needed for:

```text
OTOC/operator growth:
    belongs under deterministic export, as a possible route but not a
    recovery condition.

Krylov complexity:
    belongs under failure classification as a diagnostic.

all-to-all/SYK:
    limiting case of log-diameter/constant-diameter access geometry.

Rindler/BTZ:
    stress tests/examples, not separate theorem branches yet.
```

## Recommended Result Sequence

```text
1. Finish theorem-backed expander mixer as the positive existence result.
2. Add the export capacity theoremlet.
3. Attack deterministic expander export.
4. Use dual-unitary cuts as the local benchmark if deterministic export
   stalls.
5. Return to measurement only after private export has a sharper
   operational diagnostic.
```

Steps 1 and 2 are now in the theorem stack, and `main.tex` also contains
the moment-gap export criterion. The next large step is to prove or
refute the required second-moment gap for a natural deterministic
bounded-degree expander dynamics.

The program should not now drift into optimizing expander models for
their own sake. Expanders matter because they isolate access geometry.
The larger target remains constrained-access private recovery.
