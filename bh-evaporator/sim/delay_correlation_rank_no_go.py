"""Numerical support for delay-correlation source-rank non-identifiability.

Constructs rank-one and rank-many independent Gaussian source decompositions
with the same aggregate power spectrum.  Their full g1(tau) and g2(tau) are
identical although the source participation ratios differ.

NumPy only.
"""

import numpy as np


def normalized_coherence(omega, spectrum, tau):
    phase = np.exp(-1j * tau[:, None] * omega[None, :])
    numerator = np.trapezoid(phase * spectrum[None, :], omega, axis=1)
    denominator = np.trapezoid(spectrum, omega)
    return numerator / denominator


def main():
    omega = np.linspace(-5.0, 5.0, 6001)
    tau = np.linspace(-18.0, 18.0, 1201)

    # A deliberately structured, positive, non-Lorentzian aggregate spectrum.
    spectrum = (
        0.68 * np.exp(-0.5 * ((omega - 0.7) / 0.55) ** 2)
        + 0.22 * np.exp(-0.5 * ((omega + 1.25) / 0.18) ** 2)
        + 0.10 / (1.0 + ((omega - 2.1) / 0.35) ** 4)
    )

    rank_one_weights = np.array([1.0])
    rank_many_weights = np.arange(1.0, 65.0)
    rank_many_weights /= rank_many_weights.sum()

    rank_one_components = rank_one_weights[:, None] * spectrum[None, :]
    rank_many_components = rank_many_weights[:, None] * spectrum[None, :]
    aggregate_one = np.sum(rank_one_components, axis=0)
    aggregate_many = np.sum(rank_many_components, axis=0)

    g1_one = normalized_coherence(omega, aggregate_one, tau)
    g1_many = normalized_coherence(omega, aggregate_many, tau)
    g2_one = 1.0 + np.abs(g1_one) ** 2
    g2_many = 1.0 + np.abs(g1_many) ** 2

    spectrum_error = np.max(np.abs(aggregate_one - aggregate_many))
    g1_error = np.max(np.abs(g1_one - g1_many))
    g2_error = np.max(np.abs(g2_one - g2_many))
    n_eff_one = 1.0 / np.sum(rank_one_weights**2)
    n_eff_many = 1.0 / np.sum(rank_many_weights**2)

    if spectrum_error > 2e-14:
        raise AssertionError("aggregate spectra differ")
    if g1_error > 2e-13 or g2_error > 2e-13:
        raise AssertionError("delay correlations differ")
    if n_eff_many < 45.0:
        raise AssertionError("high-rank comparison is not sufficiently broad")

    print("delay-correlation source-rank no-go check:")
    print(f"  N_eff rank-one decomposition: {n_eff_one:.6f}")
    print(f"  N_eff rank-many decomposition:{n_eff_many:.6f}")
    print(f"  max aggregate-spectrum error: {spectrum_error:.3e}")
    print(f"  max g1(tau) error:             {g1_error:.3e}")
    print(f"  max g2(tau) error:             {g2_error:.3e}")


if __name__ == "__main__":
    main()
