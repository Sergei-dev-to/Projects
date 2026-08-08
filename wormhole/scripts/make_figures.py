"""
Figures for the wormhole paper.

Geometry: Dai-Stojkovic short-throat wormhole = two flat R^3, each with a
ball of radius R removed, identified at r=R. Conventions match D-S Eqs.5-10
with q=1, R=1.

Multipole coefficients (corrected from earlier draft):
  B_l(A) = (2l+1)/(2(l+1)) * q * R^{2l+1} / A^{l+1}      (D-S Eq.8 / Eq.9)
  T_l(A) = -(1/(2(l+1))) * q * R^{2l+1} / A^{l+1}        (D-S Eq.7)
B_0(A) = qR/(2A) reproduces D-S Eq.9; T_0(A) = -qR/(2A) gives Q_1 = q+T_0
        = q - qR/(2A) which matches D-S Eq.10.

The CONSERVATION-PRESERVING potentials enforce per-end charges Q_+ = q,
Q_- = 0, regardless of source position. They are obtained from the D-S
solution by a uniform harmonic-flux shift that reabsorbs the spurious
position-dependent monopole on the opposite side.

Cartoon coordinates for the transit panels: a single (u, rho) meridional
plane with u < 0 = side 1 (where the charge starts) and u > 0 = side 2
(where the charge transits to). The mouth is the disc u^2 + rho^2 < R^2.
Each side's potential is rendered in its own region of (u, rho).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as _cm
from matplotlib.colors import LogNorm, LinearSegmentedColormap

from short_throat_fields import (
    E_field_conserved as shared_E_field_conserved,
    draw_tube as shared_draw_tube,
)

# ---------------------------------------------------------
# Multipole coefficients (corrected)
# ---------------------------------------------------------
def B_coef(l, A, R=1.0, q=1.0):
    return (2*l + 1) / (2*(l + 1)) * q * R**(2*l + 1) / A**(l + 1)

def T_coef(l, A, R=1.0, q=1.0):
    return -1.0 / (2*(l + 1)) * q * R**(2*l + 1) / A**(l + 1)

def P(l, x):
    if l == 0:
        return np.ones_like(x)
    if l == 1:
        return np.asarray(x, dtype=float)
    Pm1 = np.ones_like(x)
    Pm0 = np.asarray(x, dtype=float)
    for k in range(2, l + 1):
        Pnew = ((2*k - 1)*x*Pm0 - (k - 1)*Pm1) / k
        Pm1, Pm0 = Pm0, Pnew
    return Pm0

L_MAX = 30

# ---------------------------------------------------------
# D-S potentials on each side (charge on side 1 at distance A on the axis)
# ---------------------------------------------------------
def V_side1_DS(r1, cos_t1, A, R=1.0, q=1.0):
    """Side-1 potential, source charge q on side-1 axis at r=A>R."""
    dist = np.sqrt(r1**2 + A**2 - 2*A*r1*cos_t1 + 1e-30)
    out = q / dist
    for l in range(0, L_MAX + 1):
        out = out + T_coef(l, A, R, q) * P(l, cos_t1) / r1**(l + 1)
    return out

def V_side2_DS(r2, cos_t2, A, R=1.0, q=1.0):
    """Side-2 potential under D-S matching: includes B_0 = qR/(2A)."""
    out = np.zeros_like(r2 * cos_t2)
    for l in range(0, L_MAX + 1):
        out = out + B_coef(l, A, R, q) * P(l, cos_t2) / r2**(l + 1)
    return out

# ---------------------------------------------------------
# Conservation-preserving potentials.
# Initial state: charge far on side 1, Q_+ = q, Q_- = 0 (the "natural" zero
# harmonic flux: D-S at A_0 -> infinity has B_0 -> 0, so the implicit
# harmonic shift relative to the no-source vacuum is zero in that limit).
#
# At later A (charge anywhere outside the mouth), conservation requires
#   Q_+ = q,  Q_- = 0.
# This is achieved by adding a harmonic flux DeltaQ_wh to the D-S solution.
# For source on side 1 at A > R: D-S gives Q_-^DS = qR/(2A); to bring it
# to 0 we add DeltaQ_wh = qR/(2A) (which adds qR/(2A)/r_1 to V_1 and
# subtracts qR/(2A)/r_2 from V_2). Equivalently we just delete the B_0 term
# from V_2 and add qR/(2A)/r_1 to V_1.
#
# For source on side 2 at A' = |S| > R: by mirror symmetry of the setup,
# V_2^DS plays the role V_1^DS played, etc. After the conservation shift
# DeltaQ_wh = q - qR/(2A'), we get Q_+ = q on side 1 and Q_- = 0 on side 2.
# ---------------------------------------------------------
def V_side1_cons(r1, cos_t1, S, R=1.0, q=1.0):
    """Conservation-preserving side-1 potential. S > 0 = source on side 1 at r=S;
    S < 0 = source on side 2 at r=|S|."""
    if S > R:
        A = S
        # Source on side 1: V_1 = V_1^DS + (qR/(2A))/r1
        dist = np.sqrt(r1**2 + A**2 - 2*A*r1*cos_t1 + 1e-30)
        out = q / dist
        for l in range(0, L_MAX + 1):
            out = out + T_coef(l, A, R, q) * P(l, cos_t1) / r1**(l + 1)
        out = out + (q*R/(2*A)) / r1
        return out
    elif S < -R:
        Ap = -S  # |S|
        # Source on side 2 at distance Ap. V_1 has only B_l(Ap) from D-S
        # mirror, plus harmonic-flux shift +(q - qR/(2Ap))/r1.
        out = np.zeros_like(r1 * cos_t1)
        for l in range(0, L_MAX + 1):
            out = out + B_coef(l, Ap, R, q) * P(l, cos_t1) / r1**(l + 1)
        out = out + (q - q*R/(2*Ap)) / r1
        return out
    else:
        raise ValueError("S inside the mouth")

def V_side2_cons(r2, cos_t2, S, R=1.0, q=1.0):
    """Conservation-preserving side-2 potential."""
    if S > R:
        A = S
        # Source on side 1: V_2 has only l>=1 terms (B_0 deleted by Qwh shift).
        out = np.zeros_like(r2 * cos_t2)
        for l in range(1, L_MAX + 1):
            out = out + B_coef(l, A, R, q) * P(l, cos_t2) / r2**(l + 1)
        return out
    elif S < -R:
        Ap = -S
        # Source on side 2 at distance Ap: full Coulomb + matched homogeneous,
        # minus harmonic-flux shift -(q - qR/(2Ap))/r2.
        dist = np.sqrt(r2**2 + Ap**2 - 2*Ap*r2*cos_t2 + 1e-30)
        out = q / dist
        for l in range(0, L_MAX + 1):
            out = out + T_coef(l, Ap, R, q) * P(l, cos_t2) / r2**(l + 1)
        out = out - (q - q*R/(2*Ap)) / r2
        return out
    else:
        raise ValueError("S inside the mouth")

# ---------------------------------------------------------
# Embedding-cartoon coordinates: long-tube wormhole drawn with visible length
# L_TUBE between the two mouths.
#   side 1 region:  u < -L_TUBE/2,  with side-1 mouth centered at u=-L_TUBE/2
#   tube region:    |u| <= L_TUBE/2  (purely visual; the cut-and-paste model
#                                     identifies the two mouth spheres directly)
#   side 2 region:  u > +L_TUBE/2,  with side-2 mouth centered at u=+L_TUBE/2
# Source position S (signed cartoon u):
#   S <= -L_TUBE/2 - R: source on side 1 at distance A = -L_TUBE/2 - S
#   S >=  L_TUBE/2 + R: source on side 2 at distance A =  S - L_TUBE/2
# ---------------------------------------------------------
L_TUBE = 4.0  # visible length between the two mouths, in units of R

def _side_coords_1(U, RHO, L=L_TUBE):
    """Side-1 spherical coords: r_1 = distance from side-1 mouth centre at
    cartoon (u=-L/2, rho=0); cos_t1 = -((u+L/2))/r_1 so that theta_1=0 points
    outward (toward decreasing u)."""
    u1 = U + L/2
    r1 = np.sqrt(u1**2 + RHO**2) + 1e-12
    cos_t1 = -u1 / r1
    return r1, cos_t1

def _side_coords_2(U, RHO, L=L_TUBE):
    """Side-2 spherical coords."""
    u2 = U - L/2
    r2 = np.sqrt(u2**2 + RHO**2) + 1e-12
    cos_t2 = u2 / r2
    return r2, cos_t2

def potential_field(U, RHO, S, R=1.0, q=1.0, L=L_TUBE):
    V = np.zeros_like(U + RHO)
    side1 = U < -L/2
    side2 = U > +L/2
    r1, cos_t1 = _side_coords_1(U, RHO, L)
    r2, cos_t2 = _side_coords_2(U, RHO, L)
    if S <= -L/2 - R:
        A = -L/2 - S
        V_s1 = V_side1_cons(r1, cos_t1, +A, R, q)   # source on side 1 -> S_arg = +A
        V_s2 = V_side2_cons(r2, cos_t2, +A, R, q)
    elif S >= L/2 + R:
        A = S - L/2
        V_s1 = V_side1_cons(r1, cos_t1, -A, R, q)   # source on side 2 -> S_arg = -A
        V_s2 = V_side2_cons(r2, cos_t2, -A, R, q)
    else:
        raise ValueError("S inside the tube")
    V = np.where(side1, V_s1, V)
    V = np.where(side2, V_s2, V)
    return V

def E_field(U, RHO, S, R=1.0, q=1.0, eps=2e-3, L=L_TUBE):
    V_pu = potential_field(U + eps, RHO, S, R, q, L)
    V_mu = potential_field(U - eps, RHO, S, R, q, L)
    V_pr = potential_field(U, RHO + eps, S, R, q, L)
    V_mr = potential_field(U, np.maximum(RHO - eps, 1e-4), S, R, q, L)
    E_u = -(V_pu - V_mu) / (2*eps)
    E_r = -(V_pr - V_mr) / (2*eps)
    return E_u, E_r

# ---------------------------------------------------------
# FIGURE 1: 6-panel transit sequence (cylindrical-tube wormhole).
#
# Embedding cartoon: tube of radius R and length L_TUBE connecting two flat
# sheets (side + on the left, side - on the right).  In the meridional (u,y)
# plane the tube appears as a gray stadium (rectangle + two semicircular caps).
# Side + occupies u < -L/2, side - occupies u > +L/2.
#
# Source positions are in cartoon u-coordinates:
#   S <= -L/2 - R  =>  on side +, distance A = -L/2 - S from the left mouth
#   S >=  L/2 + R  =>  on side -, distance A =  S - L/2 from the right mouth
#
# Per-end charges are conserved: Q+ = q, Q- = 0 throughout all panels.
# In panels (d)-(f) the charge has transited; side + shows a monopole field
# (flux "snagged" on the original side), while side - has zero net monopole.
# ---------------------------------------------------------
def _draw_tube(ax, L, R):
    """Fill the wormhole throat as a gray stadium in the (u,y) plane."""
    # Stadium outline: left semicircle + top/bottom straights + right semicircle
    n = 120
    theta_l = np.linspace(np.pi / 2, 3 * np.pi / 2, n)
    theta_r = np.linspace(-np.pi / 2, np.pi / 2, n)
    xs = np.concatenate([-L/2 + R * np.cos(theta_l),
                          L/2 + R * np.cos(theta_r)])
    ys = np.concatenate([R * np.sin(theta_l),
                          R * np.sin(theta_r)])
    ax.fill(xs, ys, color='0.87', edgecolor='k', linewidth=1.3, zorder=3)
    # Horizontal wall lines (overdrawn for crispness)
    ax.plot([-L/2, L/2], [ R,  R], 'k-', lw=1.3, zorder=4)
    ax.plot([-L/2, L/2], [-R, -R], 'k-', lw=1.3, zorder=4)


def make_figure1():
    R = 1.0; q = 1.0; L = L_TUBE   # L_TUBE = 4.0

    # Source positions in cartoon u-coordinates (outside the tube by > R)
    half = L / 2
    S_vals = [-(half + 5.0), -(half + 2.0), -(half + 1.05),
              +(half + 1.05), +(half + 2.0), +(half + 5.0)]
    titles = [
        r'(a) $Q_+{=}q,\;Q_-{=}0$: far on side $+$',
        r'(b) approaching left mouth',
        r'(c) just outside left mouth',
        r'(d) just emerged on side $-$',
        r'(e) receding on side $-$',
        r'(f) $Q_+{=}q,\;Q_-{=}0$: far on side $-$',
    ]

    fig, axes = plt.subplots(2, 3, figsize=(18.0, 8.5),
                             sharex=True, sharey=True,
                             gridspec_kw={'hspace': 0.22, 'wspace': 0.06})
    axes = axes.ravel()

    side_ext  = 6.0   # extent of each side beyond the mouth edge (in R)
    ext_rho   = 4.0   # half-height of the plot (in R)
    N         = 420

    u_lo = -(half + side_ext)
    u_hi = +(half + side_ext)
    u_1d = np.linspace(u_lo, u_hi, N)
    y_1d = np.linspace(-ext_rho, ext_rho, N)
    U, Y  = np.meshgrid(u_1d, y_1d)
    RHO   = np.abs(Y) + 1e-4   # cylindrical radius (always >= 0)

    # Physical region masks: outside the mouth sphere on each side
    side1_phys = (U < -half) & ((U + half)**2 + Y**2 > R**2)
    side2_phys = (U >  half) & ((U - half)**2 + Y**2 > R**2)

    # Color streamlines by field magnitude on a shared log scale.
    # Truncated colormaps start at a light-but-visible shade (not white)
    # so lines remain legible in grayscale and print reproduction.
    # Strong Coulomb/monopole fields → dark; weak dipole leakage → light.
    _blues = LinearSegmentedColormap.from_list(
        'blues_trunc', _cm.Blues(np.linspace(0.25, 1.0, 256)))
    _reds  = LinearSegmentedColormap.from_list(
        'reds_trunc',  _cm.Reds(np.linspace(0.25, 1.0, 256)))
    lognorm_blue = LogNorm(vmin=4e-3, vmax=2.0)
    lognorm_red  = LogNorm(vmin=4e-3, vmax=2.0)

    for ax, S, title in zip(axes, S_vals, titles):
        E_u, E_rho = shared_E_field_conserved(U, RHO, S, R, q)
        E_y = E_rho * np.sign(Y)   # rotate rho -> signed y

        # Split by side; NaN everywhere else so streamplot stops at boundaries
        Eu_s1 = np.where(side1_phys, E_u, np.nan)
        Ey_s1 = np.where(side1_phys, E_y, np.nan)
        Eu_s2 = np.where(side2_phys, E_u, np.nan)
        Ey_s2 = np.where(side2_phys, E_y, np.nan)

        # Field magnitude (NaN outside the valid region)
        mag_s1 = np.sqrt(Eu_s1**2 + Ey_s1**2)
        mag_s2 = np.sqrt(Eu_s2**2 + Ey_s2**2)

        ax.streamplot(U, Y, Eu_s1, Ey_s1,
                      color=mag_s1, cmap=_blues, norm=lognorm_blue,
                      density=1.1, linewidth=0.85,
                      arrowsize=0.85, broken_streamlines=True)
        ax.streamplot(U, Y, Eu_s2, Ey_s2,
                      color=mag_s2, cmap=_reds, norm=lognorm_red,
                      density=1.1, linewidth=0.85,
                      arrowsize=0.85, broken_streamlines=True)

        # Draw the cylindrical throat on top of the field lines
        shared_draw_tube(ax, L, R)

        # Source marker
        ax.plot([S], [0], 'o', color='k', ms=7, zorder=6)
        nudge = 0.25
        ax.annotate(r'$q$', xy=(S, 0), xytext=(S + nudge, nudge),
                    fontsize=13, fontweight='bold', zorder=6)

        # Conservation-charge annotation in lower panel strip
        q_label = (r'$Q_+{=}q,\;Q_-{=}0$')
        ax.text(0, -ext_rho + 0.25, q_label, fontsize=8.5,
                ha='center', va='bottom', color='0.35',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.6,
                          boxstyle='round,pad=0.15'))

        # Side labels
        ax.text(u_lo + 0.3, ext_rho - 0.3, r'side $+$',
                fontsize=10.5, color='C0', ha='left', va='top',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.75,
                          boxstyle='round,pad=0.2'))
        ax.text(u_hi - 0.3, ext_rho - 0.3, r'side $-$',
                fontsize=10.5, color='C3', ha='right', va='top',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.75,
                          boxstyle='round,pad=0.2'))

        ax.set_xlim(u_lo, u_hi)
        ax.set_ylim(-ext_rho, ext_rho)
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=10.5)

    for ax in axes[3:]:
        ax.set_xlabel(r'$u/R$  (side $+$: $u < -L/2$;  throat: $|u| \leq L/2$;  side $-$: $u > L/2$)',
                      fontsize=9)
    for i in [0, 3]:
        axes[i].set_ylabel(r'$\rho / R$')

    fig.suptitle(
        'Illustrative short-throat example: '
        r'$Q_+{=}q,\;Q_-{=}0$ enforced throughout.  '
        'In this model, after transit (d)\u2013(f) side $+$ carries '
        'the harmonic-flux monopole; side $-$ carries none.',
        fontsize=11, y=1.01)
    fig.tight_layout()
    fig.savefig('fig1_fieldlines.pdf', bbox_inches='tight')
    plt.close(fig)
    print('wrote fig1_fieldlines.pdf')


# ---------------------------------------------------------
# FIGURE 2 (multipoles vs A) -- unchanged in spirit, uses corrected B_l.
# ---------------------------------------------------------
def make_figure2():
    fig, (ax0, ax1) = plt.subplots(
        1, 2, figsize=(11.2, 4.4), gridspec_kw={'width_ratios': [1.0, 1.05]}
    )
    A = np.linspace(1.01, 10.0, 400)
    R = 1.0; q = 1.0

    # Panel (a): the whole D-S effect sits in the monopole channel.
    B0_ds = 0.5 * R / A
    ax0.plot(A, B0_ds, 'k--', lw=2.0,
             label=r'D-S static family: $B_0^{\rm DS}(A)=qR/(2A)$')
    ax0.plot(A, np.zeros_like(A), color='C3', lw=3.0,
             label=r'Dynamical sector: $B_0=0$')
    ax0.fill_between(A, 0, B0_ds, color='C3', alpha=0.10)
    ax0.annotate(
        r'would require changing' + '\n' + r'the harmonic sector',
        xy=(3.0, 0.5 / 3.0), xytext=(4.3, 0.34),
        arrowprops=dict(arrowstyle='->', color='0.25', lw=1.0),
        fontsize=9, color='0.25', ha='left', va='center'
    )
    ax0.set_title(r'(a) Forbidden monopole drift', fontsize=10.5)
    ax0.set_xlabel(r'Source distance $A/R$')
    ax0.set_ylabel(r'Monopole coefficient $B_0$  (units of $q/R$)')
    ax0.set_xlim(1.0, 10.0)
    ax0.set_ylim(-0.03, 0.55)
    ax0.grid(alpha=0.25)
    ax0.legend(loc='upper right', fontsize=8.4, framealpha=0.95)

    # Panel (b): allowed higher multipoles are real, but are not a Coulomb term.
    for l, col in [(1, 'C0'), (2, 'C2'), (3, 'C3'), (4, 'C4')]:
        vals = np.array([B_coef(l, a, R, q) for a in A])
        ax1.plot(A, np.abs(vals), color=col, lw=1.8, label=fr'$\ell={l}$')
    ax1.set_title(r'(b) Allowed higher multipoles', fontsize=10.5)
    ax1.set_xlabel(r'Source distance $A/R$')
    ax1.set_ylabel(r'$|B_\ell|$  (units of $q/R$)')
    ax1.set_yscale('log')
    ax1.set_ylim(1e-5, 1.0)
    ax1.set_xlim(1.0, 10.0)
    ax1.grid(which='both', alpha=0.28)
    ax1.legend(loc='upper right', fontsize=9, framealpha=0.95)
    ax1.text(
        0.05, 0.07,
        r'$\ell\geq 1$ channels may vary,' + '\n' + r'but they are not a $1/r$ monopole.',
        transform=ax1.transAxes,
        fontsize=9,
        ha='left', va='bottom',
        bbox=dict(facecolor='white', edgecolor='0.7', alpha=0.9, boxstyle='round,pad=0.25')
    )

    fig.suptitle(
        r'Dai--Stojkovic monopole induction is a drift in the $\ell=0$ sector; '
        r'conservation pins that sector instead.',
        fontsize=11, y=1.02
    )
    fig.tight_layout()
    fig.savefig('fig2_multipoles.pdf', bbox_inches='tight')
    plt.close(fig)
    print('wrote fig2_multipoles.pdf')


# ---------------------------------------------------------
# FIGURE 3 (attenuation) -- unchanged.
# ---------------------------------------------------------
def make_figure3():
    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    LR = np.linspace(0, 12, 400)
    ax.semilogy(LR, np.ones_like(LR), 'k-', lw=2.5,
                label=r'$\ell = 0$: unattenuated, but conservation-forbidden')
    for l, col in [(1, 'C0'), (2, 'C2'), (3, 'C3'), (4, 'C4')]:
        k = np.sqrt(l*(l + 1))
        ax.semilogy(LR, np.exp(-k*LR), color=col, lw=1.8,
                    label=fr'$\ell = {l}$,  $\sqrt{{\ell(\ell+1)}} \approx {k:.2f}$')
    ax.axhspan(1e-3, 2.0, color='gold', alpha=0.12)
    ax.text(11.5, 5e-2, 'plausible detection band',
            fontsize=9, alpha=0.65, ha='right', va='center', style='italic')
    ax.set_xlabel(r'Throat aspect ratio $L/R$')
    ax.set_ylabel(r'Mode transmission bound  $e^{-\sqrt{\ell(\ell+1)}\,L/R}$')
    ax.set_ylim(1e-8, 2.0)
    ax.set_xlim(0, 12)
    ax.grid(which='both', alpha=0.3)
    ax.legend(loc='lower left', fontsize=9)
    ax.set_title(r'Throat attenuation (long-thin-throat bound).  '
                 r'The only unsuppressed channel ($\ell=0$) is the one conservation forbids.',
                 fontsize=10)
    fig.tight_layout()
    fig.savefig('fig3_attenuation.pdf', bbox_inches='tight')
    plt.close(fig)
    print('wrote fig3_attenuation.pdf')


if __name__ == '__main__':
    make_figure1()
    make_figure2()
    make_figure3()
