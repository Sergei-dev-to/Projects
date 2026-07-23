# Screening method

Date of screen: 2026-07-22.

## Scope

The inventory covers open problems in mathematics, theoretical computer
science, and combinatorial optimization whose resolution would be an exact
mathematical result. Empirical scientific questions are excluded because
their verification and data requirements are not comparable.

The unit being ranked is a *specific attack target*, not the prestige of a
named conjecture. A finite special case, explicit construction problem, or
counterexample hunt may therefore rank above the parent conjecture.

## Hard gates

A candidate enters the scored inventory only if:

1. a current primary or researcher-maintained source still describes it as
   open, or no later resolution can be found;
2. the statement and acceptance test are unambiguous;
3. a claimed result could in principle be checked independently;
4. the target is not merely an empirical prediction or an invitation to
   improve an unspecified bound.

Recent unrefereed solution claims are flagged rather than silently treated as
open or closed.

## Six-factor susceptibility score

Each factor is scored from 0 (hostile to an AI-led attack) to 5 (strong fit).
The unweighted total is out of 30.

1. **Artifact compactness (A):** Is success likely to be a finite graph,
   matrix, polynomial, integer tuple, short reduction, or other compact
   object rather than a long new theory?
2. **Verification exactness (V):** Can the decisive claim be checked by exact
   arithmetic, SAT/SMT, a proof assistant, exhaustive enumeration, or a short
   hand verification?
3. **Search compressibility (S):** Is there a bounded or parameterized search
   class, strong normal form, symmetry reduction, or useful family of
   relaxations?
4. **Representation leverage (R):** Is there a plausible chance that a new
   encoding, duality, transfer, invariant, or cross-field reformulation opens
   territory that human work has not systematically searched?
5. **Low saturation (L):** Has the relevant search space *not* already been
   exhaustively attacked with modern computation and specialist theory?
6. **Trajectory fit (T):** Can a powerful model load enough of the literature,
   run the relevant tools, criticize its own candidates, and produce a final
   certificate within a long but bounded research trajectory?

## Penalties and tie-breakers

- A finite witness that is believed to require astronomical size is scored
  down under S and T.
- A counterexample with easy verification is favored over a nonexistence
  proof whose certificate is unknown.
- Problems with enormous prior computational searches are scored down even
  when the verifier is perfect.
- A viral or recent AI claim is not evidence of a high base rate; it is used
  only to identify task shapes worth testing.
- Among similar scores, prefer targets with independent mathematical value
  even if the full conjecture survives.

## Outcome-side correction

The six-factor score measures *task shape*, not the chance that the easy-to-
verify side is true.  Final ranking therefore applies a separate qualitative
outcome prior:

- **guaranteed:** an optimum or exact finite value exists, although either
  bound may be difficult to certify;
- **favored:** specialists strongly expect the sought construction or
  presentation to exist;
- **live:** the sought side is plausible but genuinely uncertain;
- **long shot:** consensus or extensive evidence favors the opposite side.

This correction is decisive.  A conjecture can have a perfect six-integer
counterexample verifier and still be a poor target if the conjecture is very
probably true.  Likewise, an existence problem is downgraded if failure would
leave only an unbounded nonexistence search.

## Selection protocol

1. Assemble roughly 100 status-checked candidates from multiple independent
   problem lists and research surveys.
2. Score all candidates using only information available before designing an
   attack.
3. Deep-review the highest-scoring 10--15 against primary literature.
4. Select 3--5 only after checking known lower bounds, prior searches,
   certificate shape, and the strongest reason the proposed representation
   might be genuinely new.
5. For each finalist, specify a bounded first experiment and a falsifiable
   stop condition.
