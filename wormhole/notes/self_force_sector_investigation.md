# Fixed-Flux Self-Force Investigation Notes

Date: 2026-05-02

This note records an exploratory investigation separate from the main paper.
The central question was whether the Maxwell flux-sector argument implies a
general sign statement for the electrostatic self-force near an initially
uncharged wormhole.

## Executive Summary

The strong conjecture

> zero Wheeler charge plus compact wormhole topology implies repulsive
> electrostatic self-force

does not survive the checks below.  The robust conclusion is more nuanced:

1. Quasistatic transport of a charge from infinity fixes the Wheeler-flux
   sector, not the relative voltage between two asymptotic ends.
2. Equal-potential Green functions can therefore live in the wrong
   quasistatic sector.
3. Correcting the `ell=0` flux sector can change the self-force sign in some
   models, notably Ellis/Bronnikov-Ellis.
4. Zero Wheeler charge does not remove higher-multipole geometric
   polarization.  Thin-shell and abrupt smooth throats can remain attractive
   even after the `ell=0` sector is corrected.

This suggests that self-force calculations should separate:

- the conserved Wheeler-charge/monopole sector;
- higher-multipole throat polarization;
- the boundary/preparation condition, such as equal voltage versus fixed flux.

## Sector Logic

For a compact throat cut \(S\), the Wheeler charge is

\[
Q_{\rm wh}[S]=\frac{1}{4\pi}\int_S *F .
\]

The local Maxwell/Stokes argument in the main paper implies that \(Q_{\rm wh}\)
is conserved under quasistatic source motion if no electric current crosses the
worldtube swept out by \(S\).  Therefore an initially uncharged wormhole remains
in the sector

\[
\int_S *F=0 .
\]

This is weaker than a Neumann condition.  It only fixes the total period of
\(*F\) on the throat two-cycle:

\[
\int_S *F=0 \not\Rightarrow (*F)|_S=0 .
\]

Field lines may enter one part of the throat and leave another; only the signed
total flux is fixed.

In a two-ended static Green-function problem, the fixed-flux Green function has
the schematic form

\[
G_{\rm fixed}(x,x_0)
=G_{\rm equal\ voltage}(x,x_0)+\alpha(x_0)H(x),
\]

where \(H\) is the harmonic zero mode carrying throat flux, and \(\alpha(x_0)\)
is chosen so that the conserved flux has the desired value.

## Ellis/Bronnikov-Ellis

For the massless Ellis wormhole

\[
ds^2=-dt^2+d\rho^2+(\rho^2+a^2)d\Omega^2 ,
\]

the usual equal-potential Green function gives the attractive force

\[
F_{\rm eq}
=-\frac{e^2a\rho_0}{\pi(\rho_0^2+a^2)^2}.
\]

The equal-potential solution carries a source-position-dependent opposite-end
Coulomb flux.  To represent quasistatic transport from infinity near an
initially uncharged wormhole, add the homogeneous `ell=0` correction.  Its
force contribution is

\[
F_{\rm corr}
=\frac{e^2}{\rho_0^2+a^2}
\left(\frac12-\frac{1}{\pi}\arctan\frac{\rho_0}{a}\right).
\]

Thus

\[
F_{\rm fixed}=F_{\rm eq}+F_{\rm corr}.
\]

Writing \(x=\rho_0/a>0\),

\[
F_{\rm fixed}
=\frac{e^2}{\pi a^2(1+x^2)}
\left[\arctan(1/x)-\frac{x}{1+x^2}\right]>0 .
\]

So Ellis has a real sign flip:

- equal-potential sector: attractive;
- fixed zero-Wheeler-charge sector: repulsive.

This is not because the higher modes are repulsive.  Numerically, at
\(\rho_0/a=0.8\),

```text
Ellis:
  F_equal-potential / polarization part = -9.33e-02
  F_fixed-flux ell=0 correction         = +1.72e-01
  F_fixed total                         = +8.01e-02
```

The repulsive `ell=0` correction dominates the attractive regular
Green-function contribution for Ellis.

### Scripts and Figures

- Calculation and field-line rendering:
  [make_ellis_fixed_sector_field.py](./make_ellis_fixed_sector_field.py)
- Cleaner stream-function rendering:
  [make_ellis_fixed_sector_clean.py](./make_ellis_fixed_sector_clean.py)
- Candidate figures:
  [fig_ellis_fixed_sector_clean.png](./fig_ellis_fixed_sector_clean.png),
  [fig_ellis_fixed_sector_clean.pdf](./fig_ellis_fixed_sector_clean.pdf),
  [fig_ellis_fixed_sector_areal_clean.png](./fig_ellis_fixed_sector_areal_clean.png),
  [fig_ellis_fixed_sector_areal_clean.pdf](./fig_ellis_fixed_sector_areal_clean.pdf)

The field-line figures are useful for diagnostics but should not be inserted in
the paper without a separate final design pass.

## Spherical Ultrastatic Scans

To test whether fixed zero flux generally implies repulsion, we scanned
spherically symmetric ultrastatic wormholes

\[
ds^2=-dt^2+dl^2+r(l)^2d\Omega^2 .
\]

The radial modes satisfy

\[
\frac{d}{dl}\left(r(l)^2\frac{dR_\ell}{dl}\right)
-\ell(\ell+1)R_\ell=-\delta(l-l_0).
\]

The numerical workflow:

1. Solve the radial mode equations on a large finite interval.
2. Build the equal-voltage Green function.
3. Add the homogeneous `ell=0` correction that cancels the opposite-end flux.
4. Estimate the regular field at the charge by subtracting the local Coulomb
   singularity and fitting the smooth remainder.

Exploratory scanner:
[scan_fixed_flux_self_force.py](./scan_fixed_flux_self_force.py)

The scanner is useful for counterexample hunting, but it is not a
publication-grade proof.  It was validated against the exact Ellis formula at
moderate distances, where the fixed-sector force is not too small.

### Fat-Flare Counterexample

One smooth test profile was

\[
r(l)=\sqrt{l^2+1}
+1.25\,\frac{l^2}{l^2+2.8^2}\exp[-(l/2.8)^2].
\]

This profile has the same throat radius as Ellis but a shoulder around
\(|l|\sim 2\).  Its spatial scalar curvature is mixed: more negative than
Ellis at the throat, positive in the shoulders.

The fixed-zero-flux force becomes attractive in an interval around
\(l_0/a\sim0.8\) to \(2.1\).  A convergence check near \(l_0/a=1.1\) gave

```text
L_MAX 75   F = -3.664e-02
L_MAX 95   F = -3.887e-02
L_MAX 125  F = -3.929e-02
L_MAX 155  F = -3.875e-02
```

Diagnostic plot:
[fig_profile_comparison.png](./fig_profile_comparison.png),
[fig_profile_comparison.pdf](./fig_profile_comparison.pdf)

### Nonpositive-Scalar-Curvature Mass-Drop Counterexample

We then tested whether nonpositive energy density on an ultrastatic slice might
be enough.  In this setting

\[
{}^{(3)}R=16\pi G\rho .
\]

Define the spherical Hawking/Misner-Sharp mass

\[
m(l)=\frac{r}{2}(1-r'^2).
\]

For \(l>0\), where \(r'>0\),

\[
m'(l)=\frac{r'(l)r(l)^2}{4}\,{}^{(3)}R .
\]

Thus \({}^{(3)}R\le0\) corresponds to \(m'(l)\le0\).  We built profiles from
a monotone decreasing mass, for example

\[
m(l)=\frac{a}{2}\exp[-(l/0.6a)^2],
\]

by solving

\[
r'^2=1-\frac{2m(l)}{r(l)}.
\]

This profile keeps \({}^{(3)}R\le0\) but still gives an attractive
fixed-zero-flux force.  A convergence check at \(l_0/a=0.8\) gave

```text
L_MAX 75   F = -6.946e-02
L_MAX 95   F = -7.159e-02
L_MAX 125  F = -7.178e-02
L_MAX 155  F = -7.184e-02
```

Diagnostic plot:
[fig_profile_comparison_massdrop.png](./fig_profile_comparison_massdrop.png),
[fig_profile_comparison_massdrop.pdf](./fig_profile_comparison_massdrop.pdf)

Force comparison plot:
[fig_self_force_comparison.png](./fig_self_force_comparison.png),
[fig_self_force_comparison.pdf](./fig_self_force_comparison.pdf)

Plot generators:

- [plot_profile_comparison.py](./plot_profile_comparison.py)
- [plot_self_force_comparison.py](./plot_self_force_comparison.py)

### Interpretation

The mass-drop profile has no positive scalar-curvature shell, but its areal
radius opens much more abruptly than Ellis.  The area expansion

\[
\Theta(l)=\frac{2r'(l)}{r(l)}
\]

overshoots Ellis near the throat.  This seems to create a higher-multipole
impedance/scattering feature.  The fixed-flux `ell=0` correction is not strong
enough to dominate the attractive regular Green-function part.

At \(l_0/a=0.8\):

```text
Ellis:
  F_equal-potential part = -9.33e-02
  F_flux correction      = +1.72e-01
  F_fixed                = +8.01e-02

mass-drop R<=0:
  F_equal-potential part = -1.93e-01
  F_flux correction      = +1.20e-01
  F_fixed                = -7.16e-02
```

The attractive force is therefore a genuine higher-mode/geometric polarization
effect, not merely an uncorrected Wheeler-charge artifact.

## Flat Spherical Thin Shell

The flat spherical thin-shell wormhole is the \(M=0\) Visser cut-and-paste
model: remove \(r<c\) from two copies of flat space and identify the boundary
spheres \(r=c\).  The spacetime is flat away from the shell; the shell stress
comes from the Israel junction conditions.

The relevant literature calculation is:

- Rubín de Celis, Santillán, Simeone, "Probing global aspects of a geometry by
  the self-force on a charge: Spherical thin-shell wormholes", Phys. Rev. D 88,
  124012 (2013), arXiv:1309.7533.

Local PDF/text copies:

- [_thin_shell_spherical_1309_7533.pdf](./_thin_shell_spherical_1309_7533.pdf)
- [_thin_shell_spherical_1309_7533.txt](./_thin_shell_spherical_1309_7533.txt)

Their flat-limit force is

\[
f_{\rm paper}
=-\frac{q^2 c}{2r^3}\frac{1}{1-(c/r)^2}.
\]

Their equal-potential solution has a nonzero opposite-end Coulomb flux
proportional to \(qc/(2r)\).  The `ell=0` part of the force is

\[
f_{\ell=0}=-\frac{q^2c}{2r^3}.
\]

Subtracting this wrong-for-quasistatic flux sector leaves

\[
f_{Q_{\rm wh}=0}
=-\frac{q^2c^3}{2r^3(r^2-c^2)} .
\]

Thus a flat spherical thin shell remains attractive even in the fixed
zero-Wheeler-charge sector.  This is an important counterpoint to Ellis:
zero Wheeler charge fixes the monopole sector but does not eliminate
higher-multipole throat polarization.

## Literature Pointers

The following sources are most relevant to this investigation.

- Krasnikov 2008, "Electrostatic interaction of a pointlike charge with a
  wormhole", arXiv:0802.1358.  Krasnikov explicitly separates the
  charge-generated potential from source-free flux sectors and notes that the
  source-free part does not change under quasistatic motion.
  Local files:
  [_krasnikov_0802_1358_abs.html](./_krasnikov_0802_1358_abs.html),
  [_krasnikov_src/resub.tex](./_krasnikov_src/resub.tex)

- Boisseau and Linet 2012, arXiv:1207.0377.  They discuss the arbitrary
  monopole parameter in Ellis-type wormhole electrostatics and show explicitly
  that the self-force depends on the potential choice.
  Local file:
  [_boisseau_linet_1207_0377.tex](./_boisseau_linet_1207_0377.tex)

- Rubín de Celis, Santillán, Simeone 2013, arXiv:1309.7533.  Spherical
  thin-shell self-force; useful because the flat limit separates the
  Wheeler-sector monopole contribution from the remaining attractive
  higher-multipole force.

## Consequences for the Main Paper

This material is probably too large for the current paper except as a short
context paragraph or footnote.  The main paper should keep the robust sector
claim:

> Equal-potential static Green functions in a two-ended wormhole generally do
> not describe quasistatic motion from infinity near an initially uncharged
> wormhole.  The quasistatic constraint fixes Wheeler flux, not relative
> voltage.

If self-force is mentioned, the careful one-paragraph version is:

> A related ambiguity appears in wormhole self-force calculations.  In the
> Ellis case, correcting the `ell=0` flux sector changes the force from
> attractive to repulsive.  This is not a universal repulsion theorem:
> thin-shell and abrupt smooth throats can still attract through genuine
> higher-multipole polarization even at zero Wheeler charge.

That statement is accurate, avoids overclaiming, and preserves the main paper's
focus.
