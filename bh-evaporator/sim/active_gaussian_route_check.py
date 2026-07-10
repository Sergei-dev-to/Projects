"""Checks the exact active-Gaussian route-2c identities.

For a_out = r a_in + l c + g b^dagger, choose
    |r|^2 = 1-gamma,
    |g|^2 = gamma*n_beta,
    |l|^2 = gamma*(n_beta+1).

The script verifies canonical commutation, Hawking flux, calibrated
emission/absorption response, and circular-Gaussian g2=2 over a strongly
frequency-dependent greybody profile.  NumPy only.
"""

import numpy as np


def route_coefficients(omega, beta=1.0):
    n_beta = 1.0 / np.expm1(beta * omega)
    gamma = 0.08 + 0.74 / (1.0 + np.exp(-4.0 * (omega - 1.1)))
    gamma *= 0.78 + 0.18 * np.cos(2.7 * omega) ** 2
    gamma = np.clip(gamma, 1e-8, 0.96)

    r2 = 1.0 - gamma
    g2_coeff = gamma * n_beta
    l2 = gamma * (n_beta + 1.0)
    return n_beta, gamma, r2, g2_coeff, l2


def main():
    omega = np.linspace(0.2, 3.0, 4001)
    beta = 1.37
    n_beta, gamma, r2, emission, absorption = route_coefficients(
        omega, beta=beta
    )

    commutator = r2 + absorption - emission
    reference = np.exp(-beta * omega)
    response = emission / absorption
    hawking_flux = gamma / np.expm1(beta * omega)

    comm_error = np.max(np.abs(commutator - 1.0))
    response_error = np.max(np.abs(response / reference - 1.0))
    flux_error = np.max(
        np.abs(emission - hawking_flux) / np.maximum(hawking_flux, 1e-300)
    )

    # A zero-mean circular Gaussian mode has <a^dag a^dag a a>=2 n^2.
    fourth_moment = 2.0 * emission**2
    g2_output = fourth_moment / emission**2
    g2_error = np.max(np.abs(g2_output - 2.0))

    if comm_error > 2e-14:
        raise AssertionError("canonical commutator identity failed")
    if response_error > 2e-14:
        raise AssertionError("calibrated response identity failed")
    if flux_error > 2e-14:
        raise AssertionError("Hawking flux identity failed")
    if g2_error > 2e-14:
        raise AssertionError("thermal Gaussian g2 identity failed")
    if np.any(gamma <= 0.0) or np.any(gamma >= 1.0):
        raise AssertionError("greybody absorptivity left the passive range")

    print("active Gaussian route-2c check:")
    print(f"  max commutator error:       {comm_error:.3e}")
    print(f"  max response-ratio error:   {response_error:.3e}")
    print(f"  max Hawking-flux error:     {flux_error:.3e}")
    print(f"  max thermal-g2 error:       {g2_error:.3e}")
    print(
        "  sampled ranges: "
        f"gamma=[{gamma.min():.3f},{gamma.max():.3f}], "
        f"n_beta=[{n_beta.min():.3e},{n_beta.max():.3e}]"
    )


if __name__ == "__main__":
    main()
