"""
New figures for wormhole paper v3.

  fig_ds_claimed.pdf   -- 6-panel D-S picture (monopole induction as they claim)
  fig_memory_timeline.pdf -- radiation memory timeline schematic
  fig_signal_hierarchy.pdf -- signal amplitude bar chart

All utility functions copied/adapted from make_figures.py so this file
runs standalone.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.cm as _cm
from matplotlib.colors import LogNorm, LinearSegmentedColormap
import matplotlib.gridspec as gridspec

from short_throat_fields import (
    E_field_ds as shared_E_field_ds,
    draw_tube as shared_draw_tube,
)

plt.rcParams.update({
    'font.family': 'serif',
    'mathtext.fontset': 'cm',
    'axes.linewidth': 0.8,
})

# -------------------------------------------------------------------
# Multipole coefficients (D-S conventions: q=1, R=1)
# -------------------------------------------------------------------
def B_coef(l, A, R=1.0, q=1.0):
    return (2*l + 1) / (2*(l + 1)) * q * R**(2*l + 1) / A**(l + 1)

def T_coef(l, A, R=1.0, q=1.0):
    return -1.0 / (2*(l + 1)) * q * R**(2*l + 1) / A**(l + 1)

def P(l, x):
    if l == 0: return np.ones_like(x)
    if l == 1: return np.asarray(x, dtype=float)
    Pm1 = np.ones_like(x); Pm0 = np.asarray(x, dtype=float)
    for k in range(2, l + 1):
        Pnew = ((2*k-1)*x*Pm0 - (k-1)*Pm1) / k
        Pm1, Pm0 = Pm0, Pnew
    return Pm0

L_MAX = 20

def V_side1_DS(r1, cos_t1, A, R=1.0, q=1.0):
    dist = np.sqrt(r1**2 + A**2 - 2*A*r1*cos_t1 + 1e-30)
    out = q / dist
    for l in range(0, L_MAX + 1):
        out = out + T_coef(l, A, R, q) * P(l, cos_t1) / r1**(l + 1)
    return out

def V_side2_DS(r2, cos_t2, A, R=1.0, q=1.0):
    """D-S side-2 potential including the spurious monopole B_0 = qR/(2A)."""
    out = np.zeros_like(r2 * cos_t2)
    for l in range(0, L_MAX + 1):
        out = out + B_coef(l, A, R, q) * P(l, cos_t2) / r2**(l + 1)
    return out

# Embedding cartoon layout
L_TUBE = 4.0

def _side_coords_1(U, RHO, L=L_TUBE):
    u1 = U + L/2; r1 = np.sqrt(u1**2 + RHO**2) + 1e-12
    return r1, -u1 / r1

def _side_coords_2(U, RHO, L=L_TUBE):
    u2 = U - L/2; r2 = np.sqrt(u2**2 + RHO**2) + 1e-12
    return r2, u2 / r2

def potential_field_DS(U, RHO, S, R=1.0, q=1.0, L=L_TUBE):
    """D-S field: source on side 1 at cartoon coordinate S < -L/2."""
    A = -L/2 - S  # physical distance from left mouth
    r1, cos_t1 = _side_coords_1(U, RHO, L)
    r2, cos_t2 = _side_coords_2(U, RHO, L)
    V_s1 = V_side1_DS(r1, cos_t1, A, R, q)
    V_s2 = V_side2_DS(r2, cos_t2, A, R, q)
    side1 = U < -L/2; side2 = U > L/2
    return np.where(side1, V_s1, np.where(side2, V_s2, 0.0))

def E_field_DS(U, RHO, S, R=1.0, q=1.0, eps=2e-3, L=L_TUBE):
    V_pu = potential_field_DS(U + eps, RHO, S, R, q, L)
    V_mu = potential_field_DS(U - eps, RHO, S, R, q, L)
    V_pr = potential_field_DS(U, RHO + eps, S, R, q, L)
    V_mr = potential_field_DS(U, np.maximum(RHO - eps, 1e-4), S, R, q, L)
    return -(V_pu - V_mu) / (2*eps), -(V_pr - V_mr) / (2*eps)

def _draw_tube(ax, L, R):
    n = 120
    theta_l = np.linspace(np.pi/2, 3*np.pi/2, n)
    theta_r = np.linspace(-np.pi/2, np.pi/2, n)
    xs = np.concatenate([-L/2 + R*np.cos(theta_l), L/2 + R*np.cos(theta_r)])
    ys = np.concatenate([R*np.sin(theta_l), R*np.sin(theta_r)])
    ax.fill(xs, ys, color='0.87', edgecolor='k', linewidth=1.2, zorder=3)
    ax.plot([-L/2, L/2], [ R,  R], 'k-', lw=1.2, zorder=4)
    ax.plot([-L/2, L/2], [-R, -R], 'k-', lw=1.2, zorder=4)


# ===================================================================
# FIGURE: fig_ds_claimed.pdf
# The D-S picture: source on side 1 (blue), approaching the throat.
# Side 2 (red) develops a growing monopole field as claimed by D-S.
# ===================================================================
def make_fig_ds_claimed():
    R = 1.0; q = 1.0; L = L_TUBE
    half = L / 2

    # Source positions (all on side 1, approaching)
    A_vals = [8.0, 4.0, 2.0, 1.4, 1.15, 1.03]
    S_vals = [-(half + A) for A in A_vals]
    Q2_vals = [q * R / (2*A) for A in A_vals]

    panel_labels = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']

    fig, axes = plt.subplots(2, 3, figsize=(17.5, 8.2),
                             sharex=True, sharey=True,
                             gridspec_kw={'hspace': 0.25, 'wspace': 0.06})
    axes = axes.ravel()

    side_ext = 6.0; ext_rho = 4.0; N = 380
    u_lo = -(half + side_ext); u_hi = +(half + side_ext)
    u_1d = np.linspace(u_lo, u_hi, N)
    y_1d = np.linspace(-ext_rho, ext_rho, N)
    U, Y = np.meshgrid(u_1d, y_1d)
    RHO = np.abs(Y) + 1e-4

    side1_phys = (U < -half) & ((U + half)**2 + Y**2 > R**2)
    side2_phys = (U >  half) & ((U - half)**2 + Y**2 > R**2)

    _blues = LinearSegmentedColormap.from_list('bl', _cm.Blues(np.linspace(0.25, 1.0, 256)))
    _reds  = LinearSegmentedColormap.from_list('rd', _cm.Reds(np.linspace(0.25, 1.0, 256)))
    lnorm  = LogNorm(vmin=4e-3, vmax=2.0)

    for ax, S, A, Q2, lbl in zip(axes, S_vals, A_vals, Q2_vals, panel_labels):
        Eu, Er = shared_E_field_ds(U, RHO, S, R, q, l_max=L_MAX)
        Ey = Er * np.sign(Y)

        Eu_s1 = np.where(side1_phys, Eu, np.nan)
        Ey_s1 = np.where(side1_phys, Ey, np.nan)
        Eu_s2 = np.where(side2_phys, Eu, np.nan)
        Ey_s2 = np.where(side2_phys, Ey, np.nan)

        ax.streamplot(U, Y, Eu_s1, Ey_s1,
                      color=np.sqrt(Eu_s1**2 + Ey_s1**2), cmap=_blues, norm=lnorm,
                      density=1.0, linewidth=0.8, arrowsize=0.8, broken_streamlines=True)
        ax.streamplot(U, Y, Eu_s2, Ey_s2,
                      color=np.sqrt(Eu_s2**2 + Ey_s2**2), cmap=_reds, norm=lnorm,
                      density=1.0, linewidth=0.8, arrowsize=0.8, broken_streamlines=True)

        shared_draw_tube(ax, L, R)
        ax.plot([S], [0], 'o', color='k', ms=7, zorder=6)
        nudge = 0.3
        ax.annotate(r'$q$', xy=(S, 0), xytext=(S + nudge, nudge),
                    fontsize=12, fontweight='bold', zorder=6)

        # Annotate the claimed D-S monopole on side 2
        ax.text(u_hi - 0.35, -ext_rho + 0.35,
                r'$Q_2 = \frac{qR}{2A} = %.3g\,q$' % Q2,
                fontsize=8.5, ha='right', va='bottom', color='C3',
                bbox=dict(facecolor='white', edgecolor='C3', alpha=0.85,
                          boxstyle='round,pad=0.2', linewidth=0.8))

        ax.text(u_lo + 0.3, ext_rho - 0.3, r'side $+$',
                fontsize=10, color='C0', ha='left', va='top',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.75,
                          boxstyle='round,pad=0.15'))
        ax.text(u_hi - 0.3, ext_rho - 0.3, r'side $-$',
                fontsize=10, color='C3', ha='right', va='top',
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.75,
                          boxstyle='round,pad=0.15'))

        ax.text(0.03, 0.97, lbl, transform=ax.transAxes,
                fontsize=11, va='top', ha='left', fontweight='bold')

        ax.set_xlim(u_lo, u_hi); ax.set_ylim(-ext_rho, ext_rho)
        ax.set_aspect('equal')

    for ax in axes[3:]:
        ax.set_xlabel(r'$u/R$  (side $+$: left;  throat: center;  side $-$: right)',
                      fontsize=9)
    for i in [0, 3]:
        axes[i].set_ylabel(r'$\rho / R$')

    fig.suptitle(
        r'The Dai--Stojkovic picture: claimed monopole $Q_2(A) = qR/(2A)$ grows '
        r'on side $-$ as source approaches throat on side $+$.  '
        r'Red field lines radiate from side$-$ mouth with no source present --- '
        r'the effect our conservation theorems forbid.',
        fontsize=10.5, y=1.005)
    fig.tight_layout()
    fig.savefig('fig_ds_claimed.pdf', bbox_inches='tight')
    plt.close(fig)
    print('wrote fig_ds_claimed.pdf')


# ===================================================================
# FIGURE: fig_memory_timeline.pdf
# Top row: wormhole cartoon at 3 moments.
# Bottom: M_throat(t) vs t showing permanent deficit.
# ===================================================================
def _draw_wormhole_cartoon(ax, radiation_pos, label):
    """
    Draw a schematic wormhole (two circles connected by an arc) with a radiation
    burst at position radiation_pos:
      'B'  = approaching from mouth B
      'throat' = transiting
      'A'  = past mouth A, dispersing
      None = no burst
    """
    ax.set_xlim(-1.0, 1.0); ax.set_ylim(-0.5, 0.5)
    ax.set_aspect('equal'); ax.axis('off')

    # Two mouth circles
    r = 0.18
    for cx, col, lbl in [(-0.55, '#3a6fbf', '$B$'), (+0.55, '#bf3a3a', '$A$')]:
        circle = plt.Circle((cx, 0), r, fill=False, edgecolor=col, linewidth=2.5)
        ax.add_patch(circle)
        ax.text(cx, -r - 0.08, lbl, ha='center', va='top', fontsize=12, color=col)

    # Throat tube (simplified arc)
    theta = np.linspace(np.pi, 0, 80)
    x_top = 0.37 * np.cos(theta)
    y_top = 0.12 * np.sin(theta) + 0.18
    ax.plot(x_top, y_top, 'k-', lw=1.5)
    y_bot = 0.12 * np.sin(theta) - 0.18
    ax.plot(x_top, y_bot, 'k-', lw=1.5)
    ax.fill_between(x_top, y_bot, y_top, color='0.88', zorder=0)

    # Radiation burst
    burst_styles = {
        'B':      {'pos': (-0.78, 0), 'color': 'goldenrod'},
        'throat': {'pos': (0.00, 0),  'color': 'goldenrod'},
        'A':      {'pos': (+0.78, 0), 'color': 'goldenrod'},
    }
    if radiation_pos in burst_styles:
        px, py = burst_styles[radiation_pos]['pos']
        col = burst_styles[radiation_pos]['color']
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            dx, dy = 0.07*np.cos(angle), 0.07*np.sin(angle)
            ax.annotate('', xy=(px+dx, py+dy), xytext=(px, py),
                        arrowprops=dict(arrowstyle='->', color=col, lw=1.5))
        ax.plot(px, py, 's', color=col, ms=8, zorder=5)

    ax.set_title(label, fontsize=10, pad=3)


def make_fig_memory_timeline():
    fig = plt.figure(figsize=(13.0, 6.5), layout='constrained')
    gs = gridspec.GridSpec(2, 3, figure=fig,
                           height_ratios=[1.0, 1.0],
                           hspace=0.45, wspace=0.35)

    # Top row: wormhole cartoons at three moments
    moments = [
        ('B',      r'$t < 0$: burst on $B$ side'),
        ('throat', r'$t = 0$: burst transiting'),
        ('A',      r'$t > 0$: burst past mouth $A$'),
    ]
    for col, (rad_pos, lbl) in enumerate(moments):
        ax = fig.add_subplot(gs[0, col])
        _draw_wormhole_cartoon(ax, rad_pos, lbl)

    # Bottom row: M_throat(t) plot spanning all three columns
    ax_bot = fig.add_subplot(gs[1, :])

    t = np.linspace(-3, 6, 600)
    M0 = 1.0
    dM = -0.35  # throat mass deficit after transit

    # Smooth step: transit centred at t=0, width ~0.5
    def smooth_step(t, t0=0.0, width=0.5):
        return 0.5 * (1 + np.tanh((t - t0) / width))

    M_throat = M0 + dM * smooth_step(t)
    M_DS_claimed = M0 - dM * smooth_step(t)  # D-S would predict opposite sign

    ax_bot.axhline(M0, color='0.6', ls=':', lw=1.0)
    ax_bot.axvline(0, color='0.6', ls=':', lw=1.0)
    ax_bot.plot(t, M_DS_claimed, 'k--', lw=1.5,
                label=r'D-S prediction (heavier throat) — ruled out')
    ax_bot.plot(t, M_throat, 'C3', lw=2.2,
                label=r'Throat memory: $\delta M_{\rm throat} = -E/c^2 < 0$')

    ax_bot.annotate('', xy=(-3.0, M0 + dM - 0.01),
                    xytext=(-3.0, M0 - 0.01),
                    arrowprops=dict(arrowstyle='<->', color='C3', lw=1.5))
    ax_bot.text(-2.5, M0 + dM/2,
                r'$\delta M_{\rm throat} = -E/c^2$',
                fontsize=10, color='C3', va='center')

    ax_bot.fill_betweenx([M0 + dM - 0.05, M0 + 0.08],
                          -0.4, 0.4, color='goldenrod', alpha=0.12,
                          label='Radiation transiting throat')
    ax_bot.text(0.0, M0 + 0.06, 'transit', fontsize=8.5,
                ha='center', va='top', color='goldenrod', style='italic')

    ax_bot.set_xlabel(r'Time $t$ (arbitrary units)', fontsize=10)
    ax_bot.set_ylabel(r'$M_{\rm throat}(t)$  (normalised to $M_0$)', fontsize=10)
    ax_bot.set_xlim(-3, 6)
    ax_bot.set_ylim(M0 + dM - 0.12, M0 + 0.12 - dM)
    ax_bot.legend(loc='upper right', fontsize=9, framealpha=0.92)
    ax_bot.set_title(
        r'Throat mass $M_{\rm throat}(t)$: permanent deficit after radiation transit (red). '
        r'D-S prediction (dashed): opposite sign.', fontsize=9.5)
    ax_bot.grid(alpha=0.25)

    fig.savefig('fig_memory_timeline.pdf')
    plt.close(fig)
    print('wrote fig_memory_timeline.pdf')


# ===================================================================
# FIGURE: fig_signal_hierarchy.pdf
# Horizontal log-scale bar chart of fractional acceleration amplitude δa/a
# for signals in the Sgr A* / S2 scenario.
# ===================================================================
def make_fig_signal_hierarchy():
    # Signal amplitudes in log10(|δa/a|)
    # Basis: acceleration perturbation on S2 from each effect,
    # normalised to the Keplerian acceleration from M_SgrA*.
    #
    # D-S claimed: Q_2 = q*R/(2A) acting as extra mass at mouth A.
    # For q = 1 M_sun, A = 10 AU, R = 1e4 m, M_SgrA* = 4e6 M_sun:
    # Q_2 ~ 6.7e21 kg; |δa/a| ~ Q_2/M_SgrA* ~ 8e-16.
    # D-S choose params to make this ~10^-6 for favorable configurations.
    # We use their optimistic 10^-6 as the benchmark.
    #
    # Dipole (L/R=5): same geometry but amplitude suppressed by e^(-sqrt(2)*5)
    # relative to monopole, then another (R_throat/r_S2) factor for falloff.
    # Net: ~10^-3 x 10^-6 = 10^-9.
    #
    # GW memory: δM_throat = 250 kg / M_SgrA* ~ 3e-35.
    # EM memory: δM_throat ~ 1e-11 kg/year / M_SgrA* ~ 1e-48 per year.

    labels = [
        'D-S claimed monopole\n(ruled out)',
        r'Cross-throat dipole ($L/R = 5$)',
        r'GW throat memory ($10\,M_\odot$ merger, 1 pc)',
        r'EM throat memory (solar star, 1 AU, 1 yr)',
    ]
    log10_vals = [-6, -9, -35, -48]
    colors = ['#d62728', '#1f77b4', '#2ca02c', '#9467bd']
    hatch   = ['//', '',   '',      '']
    ruled_out = [True, False, False, False]

    fig, ax = plt.subplots(figsize=(10.5, 4.2))

    y_pos = np.arange(len(labels))[::-1]  # top to bottom

    for i, (lv, col, ht, ro, yp) in enumerate(
            zip(log10_vals, colors, hatch, ruled_out, y_pos)):
        bar = ax.barh(yp, lv, height=0.55, color=col, hatch=ht,
                      alpha=0.75, edgecolor='k', linewidth=0.6)
        # Numeric label at end of bar
        ax.text(lv - 0.4, yp, fr'$10^{{{lv}}}$',
                ha='right', va='center', fontsize=9.5, color='k',
                fontweight='bold')
        if ro:
            ax.text(lv + 0.4, yp, r'$\times$ forbidden', ha='left', va='center',
                    fontsize=9, color='#d62728', style='italic')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel(r'$\log_{10}|\delta a / a_{\rm Kepler}|$  '
                  r'(fractional acceleration on S2)', fontsize=10.5)
    ax.set_xlim(-56, -2)
    ax.axvline(-6, color='0.5', lw=0.8, ls=':')
    ax.text(-6.0, len(labels) - 0.3, 'D-S\nclaim', fontsize=8, color='0.4',
            ha='center', style='italic')

    # Shade "current observational limit"
    ax.axvspan(-7, -2, color='gold', alpha=0.12, zorder=0)
    ax.text(-4.5, -0.55, 'observable\ntoday', fontsize=8, color='goldenrod',
            ha='center', va='bottom', style='italic')

    ax.grid(axis='x', alpha=0.3)
    ax.set_title(
        r'Signal hierarchy: Sgr~A$^*$ wormhole scenario ($r_{S2} \approx 1000$ AU). '
        r'The claimed monopole (ruled out) sits orders of magnitude above '
        r'any permitted effect.',
        fontsize=10)
    fig.tight_layout()
    fig.savefig('fig_signal_hierarchy.pdf', bbox_inches='tight')
    plt.close(fig)
    print('wrote fig_signal_hierarchy.pdf')


if __name__ == '__main__':
    import os
    os.chdir(r'c:\Users\serge\Projects\wormhole')
    make_fig_ds_claimed()
    make_fig_memory_timeline()
    make_fig_signal_hierarchy()
    print('all done.')
