# Signed Cancellation and the Ordinary Gram Tail

Date: 2026-07-09

Status: exact aggregate-response counterexample plus a conditional
paired-leg participation bound.  This is the first Phase-2 result of
`certificate_gap_closure_plan_2026_07_09.md`.

## Result in One Line

A HIGH-side occupation-enhanced channel and a LOW-side starved channel
can produce an exactly calibrated aggregate emission/absorption ratio at
`N_eff <= 2` (and arbitrarily close to one in an extreme limit).
Therefore one net line ratio cannot bound the total bad flux.  A valid
input-2 certificate must separately control:

```text
HIGH-side L2 weight       through g2 or channel resolution;
LOW-side total flux       through spectral/drain/time-resolved response;
ordinary-sector L2 tail  through an envelope, tomography, or another bound.
```

## 1. Aggregate Response in Emission-Fraction Variables [exact]

Let channel `i` have emission and absorption rates

```text
E_i = Gamma_em,i,
B_i = Gamma_abs,i,
r_i = E_i/B_i.
```

Normalize by total emitted line flux,

```text
f_i = E_i/sum_j E_j,
sum_i f_i = 1.
```

The aggregate line ratio is

```text
r_tot
  = sum_i E_i / sum_i B_i
  = 1 / sum_i (f_i/r_i).                                    (1.1)
```

For calibrated reference `R`, define

```text
q_i = R/r_i.
```

Then

```text
R/r_tot = sum_i f_i q_i.                                   (1.2)
```

Channels above the reference have `q_i < 1`; channels below it have
`q_i > 1`.  Exact aggregate calibration is only the single linear
condition

```text
sum_i f_i q_i = 1.                                         (1.3)
```

It does not require any channel to be individually calibrated.

## 2. Two-Channel Exact-Cancellation Counterexample [exact]

Take one HIGH channel `h` and one LOW channel `c`, with

```text
q_h < 1 < q_c,
f_c = 1-f_h.
```

Equation (1.3) is solved by

```text
f_h = (q_c-1)/(q_c-q_h),
f_c = (1-q_h)/(q_c-q_h).                                   (2.1)
```

Both fractions are positive.  The source participation is

```text
N_eff = 1/(f_h^2+f_c^2) <= 2.                              (2.2)
```

For a Schwarzschild/KMS reference at `beta omega = 1`, use

```text
R = exp(-1),
n_ref = 1/(e-1).
```

Let the HIGH channel have `r_h -> 1`, so `q_h -> R`.  Let the LOW
channel be a starved thermal mode with `x = Gamma_out/Gamma_int = 1`:

```text
r_c = n_ref/(n_ref+1+x),
q_c = 1+x/(n_ref+1).
```

The two fractions are both O(1), while (1.3) is exact and `N_eff < 2`.
As `x -> infinity`, `q_c -> infinity`, `f_h -> 1`, and `N_eff -> 1`:
a very small emitted LOW component carries enough absorption weight to
cancel an almost rank-one HIGH emitted flux.

**No-go.**  A bound on `|r_tot/R-1|` alone cannot bound
`f_bad = f_HIGH+f_LOW`, cannot exclude rank-one/two emission, and cannot
derive input 2 of the necessity trinity.

## 3. Why the Existing Paired Legs Matter

Under the fourth-moment independence/phase-symmetry assumptions of
`statistics_rank_link_result.md`, the resolved-mode composite identity
is

```text
g2_tot = 2 + sum_i f_i^2 (g2_i-2).                          (3.1)
```

Suppose every HIGH occupation-enhanced channel in a set `H` satisfies

```text
g2_i <= 2-kappa,
kappa > 0,
```

while the Gaussian starved and ordinary thermal channels have `g2=2`.
Then a measured `g2_tot >= 2-epsilon_g` gives the exact L2 bound

```text
Q_H = sum_{i in H} f_i^2 <= epsilon_g/kappa.                 (3.2)
```

This does not bound the total HIGH flux without a channel-count input,
but that is the correct quantity for participation.  Splitting HIGH
flux over many channels lowers `Q_H` only by earning rank.

The LOW channels require a separate response protocol.  If the
spectral theorem plus drain/time/resolution data bounds their total
emitted fraction by

```text
F_C = sum_{i in C} f_i <= c,
```

then

```text
Q_C = sum_{i in C} f_i^2 <= F_C^2 <= c^2.                   (3.3)
```

This separate LOW bound cannot be inferred from the net aggregate ratio
without closing cancellation.

## 4. The Ordinary Gram Tail Is the Remaining Input-2 Joint

Let `O` denote all remaining ordinary channels and

```text
Q_O = sum_{i in O} f_i^2.
```

The total line participation is exactly

```text
N_eff = 1/(Q_H+Q_C+Q_O).                                   (4.1)
```

If the ordinary-sector envelope supplies a per-channel cap

```text
f_i <= p   for i in O,
```

then

```text
Q_O <= p sum_{i in O} f_i <= p.                             (4.2)
```

Combining (3.2), (3.3), and (4.2) gives

```text
N_eff
  >= 1/[epsilon_g/kappa + c^2 + p].                         (4.3)
```

For `p ~ 1/S`, `epsilon_g -> 0`, and `c -> 0`, this yields
`N_eff ~ S`.  At finite accuracy it gives the explicit floor.

Equation (4.3) makes the dependency transparent:

```text
g2 leg                    controls the HIGH L2 contribution;
spectral response leg     controls the LOW total/L2 contribution;
ordinary-sector envelope  controls the residual Gram tail.
```

The first two close the dangerous enhanced branches.  They do not by
themselves prove `Q_O ~ 1/S`.  Unless the ordinary tail is measured or
derived from a stronger principle, the smooth-envelope statement
remains the unremoved part of input 2.

### Static ordinary-tail non-identifiability theorem

The limitation is exact, not merely a missing estimate.  Choose any
probability vector `{f_i}` and independent thermal Gaussian channel
modes

```text
A_i = c_i a_i,
<a_i^dag a_i> = n_ref,
|c_i|^2 proportional to f_i.
```

Every channel has

```text
r_i = R,
g2_i = 2.
```

Under the same phase-symmetry/fourth-moment independence assumptions,
the aggregate line also has

```text
r_tot = R,
g2_tot = 2,
```

while the Gram eigenvalues are proportional to `{f_i}` and

```text
N_eff = 1/sum_i f_i^2
```

is arbitrary.  It can be one, subextensive, or entropy-sized without
changing either static observable.

**No-go.**  Calibrated aggregate response plus thermal `g2` cannot
determine the ordinary Gram tail.  To remove the last part of input 2,
one needs at least one additional ingredient:

```text
ordinary-sector coupling/envelope physics;
operator- or response-kernel tomography;
channel-resolved drain/relaxation data;
a microscopic theorem tying the coupling spectrum to the state count.
```

The spectral-starvation theorem can constrain a channel when its
internal and exterior widths are identified.  It does not turn two
static moments into a universal tail measurement.

## 5. Full-Tail Form Without a Per-Channel Cap

A more general theorem should avoid privileging `f_max`.  Sort ordinary
fractions

```text
f_(1) >= f_(2) >= ...
```

and define the cumulative Lorenz profile

```text
L_O(k) = sum_{i=1}^k f_(i).
```

Any bound on `L_O(k)` gives an upper bound on `Q_O`; conversely a heavy
top-`k` tail can keep `N_eff` subextensive even if no single channel
dominates.  Phase 2 should therefore optimize `Q_O` or the sorted
profile directly under the available response/tomography constraints.

Possible outcomes:

```text
observable tail bound:
  input 2 is genuinely exterior-certified;

ETH/smooth-envelope tail bound:
  input 2 is reduced to a clearly named genericity assumption;

no tail control:
  only the assumption-light floor is earned.
```

## 6. Operational Routes That Can Close Signed Cancellation

The following are candidate protocols, not yet theorems:

1. Resolve channels or linewidth components directly.
2. Measure at two exterior drain strengths.  The starved ratio changes
   with `Gamma_out/Gamma_int`; an equilibrium occupation ratio has a
   different drain dependence.
3. Switch the drain and measure the time-resolved response.
4. Combine aggregate response with the `g2` identity (3.1).
5. Repeat at two detector resolutions to expose hidden sub-lines.
6. Tomographically reconstruct the response kernel for a probe family.

The next optimizer must allow exact cancellation under (1.2), then add
these protocols one at a time.  A protocol closes the loophole only if
the worst-case participation floor improves under its actual observable
constraints.

## 7. Theorem: Two Drain Strengths Close Exact Cancellation in the Narrow Stationary Class

Scale every exterior drain in the resolved line by a known positive
factor `s`.

### HIGH sector

Assume HIGH occupation-enhanced channels have fixed source occupations
over the scan, so

```text
E_h(s) = s a_h,
r_h > R independent of s.
```

Their aggregate balance contribution after dividing by `s` is the
negative constant

```text
-H = sum_h a_h (1/r_h - 1/R),
H >= 0.                                                       (7.1)
```

### LOW sector

For each starved thermal channel `c`, take fixed internal refill
`g_c = Gamma_int,c`, base exterior width `gamma_c`, and

```text
Gamma_out,c(s) = s gamma_c.
```

In the narrow stationary Gaussian limit,

```text
E_c(s)
  = s gamma_c g_c n_ref/(g_c+s gamma_c),

1/r_c(s)-1/R
  = s gamma_c/(g_c n_ref).                                  (7.2)
```

Therefore

```text
[E_c(s)/s][1/r_c(s)-1/R]
  = s gamma_c^2/(g_c+s gamma_c).                             (7.3)
```

### Aggregate balance

Exact aggregate calibration is equivalent to

```text
D(s) = sum_i E_i(s)[1/r_i(s)-1/R] = 0.
```

Ordinary calibrated channels contribute zero.  Using (7.1)--(7.3),

```text
D(s)/s
  = -H + sum_c s gamma_c^2/(g_c+s gamma_c).                  (7.4)
```

The derivative is

```text
d[D(s)/s]/ds
  = sum_c gamma_c^2 g_c/(g_c+s gamma_c)^2 > 0               (7.5)
```

whenever any LOW channel is coupled.  Hence `D(s)/s` is strictly
increasing and can cross zero at most once.

**Two-drain exact-separation theorem.**  Under the assumptions above, if
the same resolved line is exactly calibrated at two distinct drain
strengths `s_1 != s_2`, then `H=0` and every `gamma_c=0`: neither the
fixed-occupation HIGH sector nor the starved LOW sector carries flux.

This closes the exact signed-cancellation counterexample with one extra
control setting.

### Finite-error two-drain bound [exact conditional inequality]

Let `s_2 > s_1`, define

```text
F_j = D(s_j)/s_j,
L_j = sum_c s_j gamma_c^2/(g_c+s_j gamma_c),
```

and suppose the measured aggregate ratios obey

```text
y_j = r_tot(s_j)/R,
|y_j-1| <= eta_j < 1.
```

Because

```text
D(s_j) = E_tot(s_j)[1/r_tot(s_j)-1/R],
```

the directly observable error budget is

```text
|F_j| <= epsilon_j,
epsilon_j
  = [E_tot(s_j)/(s_j R)] eta_j/(1-eta_j).                  (7.6)
```

Assume the LOW sector in the scan has the finite parameter window

```text
x_c(s_2) = s_2 gamma_c/g_c <= X.
```

For each LOW channel,

```text
l_c(s_2)-l_c(s_1)
  = l_c(s_1) [(s_2-s_1)/s_1] g_c/(g_c+s_2 gamma_c)
  >= l_c(s_1) [(s_2-s_1)/s_1]/(1+X).                     (7.7)
```

Since `F_2-F_1=L_2-L_1`, equations (7.6)--(7.7) give

```text
L_1
  <= [s_1(1+X)/(s_2-s_1)](epsilon_1+epsilon_2),

H <= L_1+epsilon_1.                                       (7.8)
```

Thus two finite-accuracy settings separately bound the LOW balance weight
and the HIGH balance weight.  If the channels classified as LOW also satisfy

```text
x_c(s_1) >= x_min > 0,
```

their emitted flux at the first setting obeys

```text
E_C(s_1)
  <= [s_1 n_ref/x_min] L_1,

F_C(s_1) = E_C(s_1)/E_tot(s_1)
  <= [s_1 n_ref/(x_min E_tot(s_1))] L_1.                  (7.9)
```

Equations (7.6), (7.8), and (7.9) supply the `c` entering the
participation bound (4.3).  The constants necessarily deteriorate as
`X -> infinity`, as `x_min -> 0`, or as the two drain settings merge.  This is
not a defect of the estimate: channels with arbitrarily large or small
starvation ratio are not uniformly identifiable from a finite scan without
another width or flux prior.  Channels below `x_min` must be assigned to the
ordinary/near-calibrated sector, whose Gram tail remains a separate problem.

### Scope of the theorem

Load-bearing assumptions:

```text
the same Gram/source decomposition persists across the scan;
all exterior widths scale by the known factor s;
HIGH occupations and ratios are drain-independent over the scan;
internal refill widths remain fixed;
the LOW channels obey the narrow stationary Gaussian starvation law;
all channels share the same calibrated reference R.
```

If HIGH occupations deplete with the drain, source weights rearrange,
or the spectral line changes identity between settings, monotonicity
need not hold.  Those failures are experimentally visible dynamics but
require a generalized multi-setting theorem rather than (7.4).

## 8. Consequence for the Current Program

The two-sided response result remains physically informative, but its
aggregate interpretation must be corrected:

```text
one signed aggregate ratio:
  detects net departure only;

resolved or multi-setting response:
  may separately bound HIGH and LOW sectors;

g2 + separately bounded LOW flux + ordinary tail control:
  gives the participation bound (4.3).
```

Best-case reduction of the necessity trinity still requires the last
two Phase-2 gates:

```text
close signed cancellation operationally;
replace or sharply isolate the ordinary-sector tail assumption.
```

## 9. Verification

`sim/signed_cancellation_optimizer.py` records the exact two-channel
counterexample, checks (4.3) on random admissible spectra, and checks the
exact and finite-error two-drain inequalities.  It is a support calculation;
the equations above are analytic.

## Discipline

- Never use one aggregate asymmetry tolerance as separate
  `eta_+` and `eta_-` bounds.
- State whether response is Gram-eigenchannel resolved, line-shape
  resolved, or only aggregate.
- Keep flux fractions normalized to emitted line flux when computing
  `N_eff`.
- Do not say the response legs remove the ordinary-sector envelope
  until `Q_O` is independently bounded.
- Treat many-channel splitting as earned participation, not a loophole.
