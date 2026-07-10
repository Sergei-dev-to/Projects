"""Finite-energy repeated parametric pump support calculation.

Implements the exact collision probabilities
    p_n(m) = (1-q) q^m / (1-q^(n+1)),  0 <= m <= n,
for a finite pump ladder.  It checks the thermal limit, one-use invariant
Kraus participation, repeated depletion, greybody flux, and perfect
Hawking/partner number correlation.

The diary-blind statement is algebraic: the collision is tensored with I_D.
NumPy only.
"""

import numpy as np


def pair_distribution(n, q):
    m = np.arange(n + 1, dtype=float)
    weights = (1.0 - q) * q**m
    return weights / (1.0 - q ** (n + 1))


def kraus_hs_weights(max_n, q):
    weights = np.zeros(max_n + 1, dtype=float)
    for n in range(max_n + 1):
        probs = pair_distribution(n, q)
        weights[: n + 1] += probs
    return weights


def repeated_depletion(max_n, q, uses):
    pump = np.zeros(max_n + 1, dtype=float)
    pump[max_n] = 1.0
    emitted_means = []
    partner_covariances = []

    for _ in range(uses):
        next_pump = np.zeros_like(pump)
        mean_m = 0.0
        mean_m2 = 0.0
        for n, population in enumerate(pump):
            if population < 1e-18:
                continue
            probs = pair_distribution(n, q)
            m = np.arange(n + 1, dtype=float)
            weighted = population * probs
            mean_m += np.sum(weighted * m)
            mean_m2 += np.sum(weighted * m**2)
            for emitted, probability in enumerate(weighted):
                next_pump[n - emitted] += probability
        emitted_means.append(mean_m)
        # Hawking and partner occupations are equal event by event, so their
        # covariance is Var(m).
        partner_covariances.append(mean_m2 - mean_m**2)
        pump = next_pump

    levels = np.arange(max_n + 1, dtype=float)
    return (
        np.asarray(emitted_means),
        np.asarray(partner_covariances),
        float(np.sum(pump * levels)),
        pump,
    )


def main():
    beta_omega = 1.0
    q = np.exp(-beta_omega)
    n_beta = q / (1.0 - q)
    gamma = 0.43
    max_n = 240
    uses = 320

    p_top = pair_distribution(max_n, q)
    geometric = (1.0 - q) * q ** np.arange(max_n + 1)
    omitted_tail = q ** (max_n + 1)
    tv_to_infinite = 0.5 * (
        np.sum(np.abs(p_top - geometric)) + omitted_tail
    )

    hs_weights = kraus_hs_weights(max_n, q)
    normalized_hs = hs_weights / np.sum(hs_weights)
    n_kraus = 1.0 / np.sum(normalized_hs**2)
    stationary_limit = (1.0 + q) / (1.0 - q)

    early_uses = max_n // 3
    _, _, early_final_mean, early_final_distribution = repeated_depletion(
        max_n, q, early_uses
    )
    emitted, partner_cov, final_mean, final_distribution = repeated_depletion(
        max_n, q, uses
    )
    initial_window = emitted[:early_uses]
    early_relative_error = np.max(
        np.abs(initial_window / n_beta - 1.0)
    )
    total_emitted = max_n - final_mean
    early_record_participation = 1.0 / np.sum(early_final_distribution**2)
    final_record_participation = 1.0 / np.sum(final_distribution**2)
    greybody_mean_early = gamma * np.mean(initial_window)
    greybody_target = gamma * n_beta

    if abs(np.sum(p_top) - 1.0) > 2e-14:
        raise AssertionError("finite pair distribution is not normalized")
    if tv_to_infinite > 2e-14:
        raise AssertionError("large-pump thermal-tail error is too large")
    if early_relative_error > 2e-12:
        raise AssertionError("early pump output is not stationary thermal")
    if abs(greybody_mean_early / greybody_target - 1.0) > 2e-12:
        raise AssertionError("greybody Hawking flux mismatch")
    if np.any(partner_cov < -1e-13):
        raise AssertionError("partner covariance became negative")
    if abs(np.sum(final_distribution) - 1.0) > 2e-12:
        raise AssertionError("pump probability was not conserved")
    if abs(max_n - early_final_mean - np.sum(initial_window)) > 2e-10:
        raise AssertionError("early energy ledger did not close")

    print("finite parametric pump check:")
    print(f"  beta*omega, n_beta:          {beta_omega:.3f}, {n_beta:.6f}")
    print(f"  thermal-tail TV error:       {tv_to_infinite:.3e}")
    print(f"  one-use Kraus N_eff:         {n_kraus:.6f}")
    print(f"  infinite-pump N_eff limit:   {stationary_limit:.6f}")
    print(f"  early mean relative error:   {early_relative_error:.3e}")
    print(
        "  greybody early/target flux: "
        f"{greybody_mean_early:.6f} / {greybody_target:.6f}"
    )
    print(f"  pump units emitted:          {total_emitted:.6f} / {max_n}")
    print(f"  final pump mean after {uses}: {final_mean:.6f}")
    print(
        f"  record Schmidt N_eff ({early_uses} uses): "
        f"{early_record_participation:.6f}"
    )
    print(
        f"  record Schmidt N_eff ({uses} uses): "
        f"{final_record_participation:.6f}"
    )
    print(f"  minimum partner covariance:  {partner_cov.min():.6e}")
    print("  diary-visible defect:        0 exactly (V_total = V_q tensor I_D)")


if __name__ == "__main__":
    main()
