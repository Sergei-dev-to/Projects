"""Verify the stationary Gaussian spectral-starvation identities.

Checks notes/collective_channel_spectral_starvation_theorem.md for:
  1. strongly frequency-dependent positive internal/exterior widths;
  2. arbitrary real dispersive self-energy shifts;
  3. the exact effective distribution and LOW-side deficit;
  4. the exact outgoing spectral-current/deficit identity;
  5. recovery of the constant-width Lindblad formulas.

NumPy only.  This is an algebraic support calculation, not a substitute
for the theorem.
"""

import numpy as np


def relative_error(actual, expected, floor=1e-14):
    scale = np.maximum(np.abs(expected), floor)
    return np.max(np.abs(actual - expected) / scale)


def spectral_check():
    omega = np.linspace(0.25, 2.5, 12001)
    omega0 = 1.15
    beta = 0.9

    # Deliberately structured, non-flat positive widths.
    gamma_int = (
        0.34
        + 0.16 * np.exp(-((omega - 0.82) / 0.23) ** 2)
        + 0.07 * (1.0 + np.sin(5.1 * omega))
    )
    gamma_out = (
        0.08
        + 0.21 * np.exp(-((omega - 1.34) / 0.31) ** 2)
        + 0.035 * (1.0 + np.cos(7.3 * omega))
    )

    # Real parts strongly distort and shift the line but should cancel
    # from the frequency-local distribution and response ratios.
    delta_int = 0.13 * np.sin(2.7 * omega) + 0.05 / (1.0 + omega**2)
    delta_out = -0.09 * np.cos(3.4 * omega) + 0.025 * omega

    sigma_r = (
        delta_int
        + delta_out
        - 0.5j * (gamma_int + gamma_out)
    )
    g_r = 1.0 / (omega - omega0 - sigma_r)
    spectral = np.abs(g_r) ** 2 * (gamma_int + gamma_out)

    n_ref = 1.0 / np.expm1(beta * omega)
    sigma_less = -1j * gamma_int * n_ref
    g_less = np.abs(g_r) ** 2 * sigma_less

    n_num = (1j * g_less).real / spectral
    n_pred = gamma_int * n_ref / (gamma_int + gamma_out)

    r_num = n_num / (n_num + 1.0)
    r_ref = n_ref / (n_ref + 1.0)
    deficit_num = 1.0 - r_num / r_ref
    x = gamma_out / gamma_int
    deficit_pred = x / (n_ref + 1.0 + x)

    current_num = gamma_out * (1j * g_less).real / (2.0 * np.pi)
    current_pred = (
        spectral
        * gamma_int
        * n_ref
        * (n_ref + 1.0)
        * deficit_num
        / (2.0 * np.pi * (1.0 + n_ref * deficit_num))
    )

    errors = {
        "distribution": relative_error(n_num, n_pred),
        "deficit": relative_error(deficit_num, deficit_pred),
        "spectral_current": relative_error(current_num, current_pred),
    }
    return errors, omega, spectral, deficit_num


def markov_check():
    beta_omega = 1.0
    nbar = 1.0 / np.expm1(beta_omega)
    gamma_int = 1.0
    rows = []
    for x in (0.1, 0.5, 1.0, 3.0):
        gamma_out = x * gamma_int
        n_spectral = gamma_int * nbar / (gamma_int + gamma_out)
        n_lindblad = nbar / (1.0 + x)
        r_spectral = n_spectral / (n_spectral + 1.0)
        r_kms = nbar / (nbar + 1.0)
        deficit_spectral = 1.0 - r_spectral / r_kms
        deficit_lindblad = x / (nbar + 1.0 + x)
        rows.append(
            (
                x,
                n_spectral,
                n_lindblad,
                deficit_spectral,
                deficit_lindblad,
            )
        )
    return rows


def main():
    errors, omega, spectral, deficit = spectral_check()
    print("frequency-dependent spectral check:")
    for key, value in errors.items():
        print(f"  max relative error, {key:>16}: {value:.3e}")
    print(
        "  sampled ranges: "
        f"omega=[{omega[0]:.2f},{omega[-1]:.2f}], "
        f"A=[{spectral.min():.3e},{spectral.max():.3e}], "
        f"delta_-=[{deficit.min():.3e},{deficit.max():.3e}]"
    )

    print("\nconstant-width Lindblad recovery:")
    print(
        f"{'x':>6} {'n spectral':>12} {'n Lindblad':>12} "
        f"{'def spectral':>14} {'def Lindblad':>13}"
    )
    for row in markov_check():
        print(
            f"{row[0]:6.2f} {row[1]:12.8f} {row[2]:12.8f} "
            f"{row[3]:14.8f} {row[4]:13.8f}"
        )

    tolerance = 2e-11
    if max(errors.values()) > tolerance:
        raise AssertionError(
            f"spectral identity error exceeds tolerance {tolerance:g}"
        )


if __name__ == "__main__":
    main()
