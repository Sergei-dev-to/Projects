# Short note

`main.tex` is a new draft of *Can the Journey Continue? The Boundaries of
Alcubierre Spacetimes*. It contains
one extension proposition, its proof, and a compact example with a crossing
from the core. An infinitely flat transverse perturbation produces an
inextendible comparison profile with identical metric derivatives on the
axis. Section 2 states and explains the criterion and its consequences;
Appendix A contains its complete proof. The longer `../main.tex` is unchanged.

The PDF builds independently in this directory using `pdflatex`, `bibtex`,
and two further `pdflatex` passes. The bibliography and checked figure are
included locally.

The appendix retains the capture, transverse-disk, and Hausdorff-attachment
arguments, organized in three subsections. Standard boundary-geodesic
existence is cited directly; global hyperbolicity is not needed for this
C2 argument. The capture proof uses
the energy identity and uniform continuity instead of auxiliary momentum
variables and a compactified limit flow. The compact regular metric is
checked by `checks/extension_metric.py` against the original metric.

The compact example is specified by the required properties of its smooth
profile rather than numerical shape parameters. It proves one axial
crossing. The longer draft retains the transverse launch-data estimate.
The no-disk consequence also excludes globally real-analytic profiles,
including profiles with asymptotic tails.

The diagram is generated and geometrically checked by
`../supplement/scripts/bubble_extension_comparison.py`. Its checked PDF is
copied to `images/bubble_comparison.pdf`. The project supplement retains the
other algebraic and numerical checks. No claim of first discovery is made
for the reduced passage, local tidal growth, or regular horizon continuation.

For the comparison profile, h(s)=exp(-1/s) for s>0 and zero otherwise.
Then h(y^2+z^2) is flat on the axis, and
W(A+epsilon*h)-W(A) equals epsilon*h times the smooth integral of W'
along the intervening arguments. Thus all metric derivatives agree there.
The modified transverse shape is strictly increasing at every positive
radius, so none of its stationary-limit slices x=constant contains an open
disk. The inextendibility conclusion uses the proved criterion.
