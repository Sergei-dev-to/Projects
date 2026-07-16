# Channel/Code Separation: The Program's Results as One-Shot Information Theory of a Self-Provisioned Serial Channel

Date: 2026-07-11

**SUPERSEDED as a thesis (same day, after joint review).**  Parent
framework: `evaporation_completion_problem_2026_07_11.md`. The useful
questions are restated in corrected form in
`evaporation_capacity_metadata_deadline_conjectures.md`: local-to-temporal
process information, charge headers versus fixed-charge payload, diary-size
capacity cuts with explicit uniformity conditions, and nonstationary
single-history estimation.
Five conflations are corrected there (coarse carrier data vs full
channel; dynamics vs code; destination vs onset; quanta budget vs
quantum capacity; interior vs encoder).  In particular the thesis
sentence's "unique self-provisioned serial channel" is withdrawn
pending an argument (candidate: T ~ 1/R pins the thermal wavelength to
the horizon size, forcing O(1) transverse channels at every stage —
unwritten).  The retro-diction ledger below remains the motivation
record; do not cite the frame as a result or use channel/code shorthand
in external text.

Final status (2026-07-13): historical reframing note. Its useful distinctions
feed the final comparison and endpoint, but none of its proposed steering steps
remain active. See `program_endpoint_and_standalone_results_2026_07_13.md`.

## 1. Thesis

The program's results, June through today, organize without remainder as
the one-shot information theory of a single, capacity-critical, serial
communication channel:

```text
the CHANNEL (temperature, greybody, capacity, forced metadata)
  is specified by the gravitational/semiclassical structure;

the CODE (how microstate information is routed into the emission process)
  is the microscopic dynamics;

exterior static measurements measure the CHANNEL;
only decoding attempts measure the CODE;

the information paradox is a source-channel DEADLINE:
  an S-sized source must pass losslessly through a budget-S channel
  with no residual archive;

S = A/4 read operationally: the channel is SELF-PROVISIONED —
  total transmission budget equals source entropy, with zero slack.
```

The trunk of this was in hand on 2026-06-12 and named without being
recognized: "critically provisioned, O(1) nats/beta over S steps"
(compression pivot; Bekenstein-Mayo one-dimensionality, Pendry capacity),
and "structure exterior-visible only temporally."  The month of
certificate work then proved, in exact adversarial form, statements that
are generic to any such channel.

## 2. Retro-diction Ledger

Every landed result maps onto a channel-theory or coding-theory
counterpart.  The sorting is the evidence that this is one object: every
impossibility is a channel statement, every survivor is a code quantity.

```text
static non-identifiability family
  (representation freedom, Gaussian tail, signed cancellation,
   active mimic, sec. static tombstone)
  <-> output statistics of a capacity-achieving channel are
      code-independent; well-coded data is indistinguishable from noise.
      Hawking thermality is a property of the channel, not the message.
      This is WHY the static certificate had to fail.       [proven, ours]

finite pump / blind comb
  <-> the zero-rate code exists: a thermal carrier bearing no message.
      Exterior statistics and payload are independent in BOTH
      directions (mimic + blind control).                   [proven, ours]

starvation / route 2b / route 2c taxonomy
  <-> carrier physics under a power constraint: which waveforms can
      carry the flux (brightness temperature, radiance; Pendry's bound
      IS the single-channel capacity formula).              [proven, ours]

time-budget theorem
  <-> finite-blocklength / one-shot coding: a single black hole is a
      single codeword; rate-level quantities are not estimable from
      one codeword.                                          [proven, ours]

three-rung ladder (g2 / response / latency)
  <-> measure the channel / probe the channel / run the decoder.
      Only the third touches the code — which is why it alone
      survived every no-go.                                  [structural]

anonymity theorem (2026-06, unused since)
  <-> coding without timestamps or return addresses:
      permutation-covariant codes force the routing-vs-nonlocal-encoder
      alternative.                                           [proven, ours]

latency exponent / decoder-complexity exponent
  <-> streaming-decode delay / complexity-constrained capacity.
      The proposed fourth rung has an existing name.         [structural]

dressing / burden tags / mass-spread hair
  <-> forced HEADER leakage: constraints stamp protocol metadata
      (energy, charge, ~log S tags) onto the channel.  The
      holography-of-information dispute is exactly "do the constraints
      put the PAYLOAD in the headers?"                       [reframing]

no-hiding + partner disposition + Page onset
  <-> the source-channel deadline: blindness is sustainable only while
      remaining budget exceeds remaining source entropy.     [reframing]

algebra-type seam (type III -> II via crossed product)
  <-> CONJECTURE: the streaming limit with no per-symbol state
      accounting; adjoining the clock/energy reference restores the
      trace — entropy bookkeeping exists only once timing metadata is
      included.  If right, "static/temporal dichotomy = operational
      shadow of type-III-ness" becomes a corollary.  One think-pass
      owed.                                                  [conjecture]
```

The two June demarcation residues rename cleanly:

```text
value of A/4G  <-> the channel is self-provisioned (zero slack);
                   "why is entropy area-sized" becomes
                   "why is the channel critically provisioned"
                   (Bousso bound as covariant capacity statement:
                    lore-grade, not to be claimed);
lived interior <-> the encoder-side description of the same process.
```

## 3. What the Frame Makes Precise

1. **The identifiability program in one sentence.**  The channel is
   exterior-identifiable (flux law, temperature-mass relation, greybody,
   response); the code is not (static no-go family), except by decoding
   (latency rung).  The reassessment's obligations table is this
   sentence expanded: thermodynamic obligation = channel parameters
   (identifiable); dynamical obligation = code (identifiable only by
   decoding); subsystem/consistency obligations = channel definition and
   end-to-end losslessness (supplied, not measured).

2. **Headers versus payload.**  Constraint dressing forbids exact
   spectator diaries; the proven examples force ~log S bits of metadata
   (tags), not recovery-grade access.  The sharp open question, now
   nameable: does gravitational dressing force PAYLOAD leakage or only
   HEADERS?  This is the quantitative content of the
   holography-of-information dispute, and the dressed-pump calculation
   (add energy coupling of the diary to the pump's emission frequencies;
   compute the forced defect accumulation A_K^min) is a header-bandwidth
   computation.  First calculation of the reframed program.

3. **The deadline theorem (promoted target).**  Typicality-free Page
   onset: unitarity + shrinking state count + no residual archive should
   force cumulative access A_K = O(1) no later than the point where
   emitted-record budget crosses remaining source entropy — from
   bookkeeping already in `shrinking_shell_diary_access_result.md`, with
   no ETH/design input.  If provable, the Page TIME becomes a channel
   statement while the Page CURVE's shape stays code-dependent.

4. **Single codeword ⇒ ensemble phenomenology.**  Rate quantities are
   ensemble quantities; the PBH-population setting is not a fallback but
   the natural home of every certificate the time-budget theorem caps at
   single-history level.

## 4. Consequences for Steering

No machinery is discarded; three things reprioritize:

```text
1. dressed-pump header calculation: unchanged as first task, new aim
   (header/payload split; HoI collision made quantitative);
2. deadline theorem: promoted — looks provable from shelf results;
3. algebra-seam/timing-reference think-pass: one session, conjecture
   grade until worked.
```

The synthesis rewrite gains its thesis, replacing the defensive
"assumption audit" framing:

> The black hole is the unique self-provisioned serial channel.  We give
> the complete separation of what its exterior physics can and cannot
> reveal — channel identifiable, code not, except by decoding — with
> exact witnesses on both sides, a composable decoding converse, and the
> constraint-forced header floor as the localized gravitational input.

Same theorems, an actual claim.  The reassessment's retirement of the
naive gravity/QI umbrella stands; this frame is the invariant successor
("channel vs code" is duality-stable where "gravity vs QI" was not).

## 5. Ownership Honesty and Scoop Obligations [before ink]

Occupied territory (do not claim):

```text
"black hole as quantum channel":
  Bradler-Adami 1310.7914 (capacities; on record in
  demarcation_scoop_audit_2026_07_10.md);
  Hayden-Preskill 0708.4025 (mirrors, on record);
  Bekenstein-Mayo 2001 one-dimensionality (on record);
  Pendry 1983 capacity bound (verified 2026-07-07);
  Bekenstein's information/energy channel bounds [UNVERIFIED ref,
  check: Bekenstein 1981 "energy cost of information" line];
  Lloyd computational-capacity line [UNVERIFIED];
  one-shot decoupling applied to evaporation [check Dupuis-Renner
  line and Hayden lecture notes].
```

Plausibly ours, pending targeted search:

```text
the assembled finite-blocklength, single-codeword,
  identifiability-SEPARATED treatment: exact no-gos severing channel
  from code + exact blind/coded controls + composable decoding
  converse (A_K);
headers-vs-payload as the quantitative form of the constraint/HoI
  dispute;
deadline-without-typicality onset statement;
critical provisioning as the operational reading of the area law.
```

Targeted searches owed: "finite blocklength black hole," "one-shot
Hawking decoding," "Hawking source tomography" (already flagged in the
scoop audit), "information-theoretic Page time without typicality,"
constraint/soft-hair channel-capacity treatments.

## Discipline

- This note contains NO new theorems; never cite the frame as a result.
  The results are the ledger entries; the frame is their organization.
- "Output statistics are code-independent" is proven here only via the
  program's specific no-go family for this setting; do not assert a
  general Shannon-style theorem without writing one.
- Keep header/payload terminology provisional until the dressed-pump
  calculation fixes what dressing actually forces; do not equate
  headers with "classical hair" in ink yet.
- The algebra-seam and Bousso connections carry [conjecture]/[lore]
  tags; they gate no downstream work.
- Run section 5's scoop pass before the synthesis rewrite uses any of
  this language.
- The self-provisioning statement ("budget = source entropy") is
  standard bookkeeping (quanta ~ S); the CLAIM is only that reading the
  area law through it is the productive residue question.

## Feeds

- `program_reassessment_2026_07_10.md`: supplies the reframed umbrella's
  positive thesis; makes survival-test targets nameable (test 2: the
  readout/quantum-hair claim class; test 4: named-model adjudications as
  code-level conclusions).
- `demarcation_synthesis.md` rewrite: section 4 thesis paragraph.
- Dressed-pump calculation spec: section 3.2 (first task).
- Deadline theorem target: section 3.3 (second task).
- `demarcation_scoop_audit_2026_07_10.md`: section 5 items to append to
  its search list.
