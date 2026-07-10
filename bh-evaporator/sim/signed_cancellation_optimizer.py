"""Support checks for signed cancellation and the Gram-tail bound.

Verifies notes/signed_cancellation_and_gram_tail_result.md:
  1. two bad channels can have an exactly calibrated aggregate ratio;
  2. their participation can remain O(1);
  3. random spectra satisfying Q_H <= eps_g/kappa, F_C <= c, and
     f_i <= p on the ordinary sector obey
         N_eff >= 1/(eps_g/kappa + c^2 + p);
  4. the finite-error two-drain inequalities bound LOW and HIGH balance
     weights over a finite starvation-ratio window.

NumPy only.  This records adversarial examples and checks the analytic
inequality; it is not a proof or a full protocol optimizer.
"""

import numpy as np


def exact_two_channel(beta_omega, occupation, starvation_x):
    r_ref = np.exp(-beta_omega)
    n_ref = r_ref / (1.0 - r_ref)

    r_high = occupation / (occupation + 1.0)
    r_cold = n_ref / (n_ref + 1.0 + starvation_x)
    q_high = r_ref / r_high
    q_cold = r_ref / r_cold

    f_high = (q_cold - 1.0) / (q_cold - q_high)
    f_cold = 1.0 - f_high
    r_total = 1.0 / (f_high / r_high + f_cold / r_cold)
    n_eff = 1.0 / (f_high**2 + f_cold**2)
    return {
        "r_ref": r_ref,
        "r_high": r_high,
        "r_cold": r_cold,
        "f_high": f_high,
        "f_cold": f_cold,
        "r_total": r_total,
        "N_eff": n_eff,
    }


def bounded_partition(total, cap, rng):
    if total <= 1e-15:
        return np.empty(0)
    count = int(np.ceil(total / cap)) + int(rng.integers(0, 6))
    uniform = np.full(count, total / count)
    random = rng.dirichlet(np.ones(count)) * total
    if random.max() <= cap:
        return random

    # Blend continuously toward the admissible uniform partition.
    lo, hi = 0.0, 1.0
    for _ in range(60):
        alpha = 0.5 * (lo + hi)
        trial = (1.0 - alpha) * random + alpha * uniform
        if trial.max() <= cap:
            hi = alpha
        else:
            lo = alpha
    return (1.0 - hi) * random + hi * uniform


def random_bound_check(samples=20000, seed=17):
    rng = np.random.default_rng(seed)
    epsilon_g = 0.012
    kappa = 0.8
    cold_cap = 0.075
    ordinary_cap = 0.01
    q_high_cap = epsilon_g / kappa
    theorem_floor = 1.0 / (
        q_high_cap + cold_cap**2 + ordinary_cap
    )

    weakest = np.inf
    worst = None
    for _ in range(samples):
        n_high = int(rng.integers(1, 8))
        shape = rng.dirichlet(np.ones(n_high))
        shape_q = np.sum(shape**2)
        max_high_total = min(0.55, np.sqrt(q_high_cap / shape_q))
        high_total = rng.random() * max_high_total
        high = shape * high_total

        cold_total = rng.random() * min(cold_cap, 1.0 - high_total)
        n_cold = int(rng.integers(1, 6))
        cold = rng.dirichlet(np.ones(n_cold)) * cold_total

        ordinary_total = 1.0 - high_total - cold_total
        ordinary = bounded_partition(ordinary_total, ordinary_cap, rng)

        q_high = np.sum(high**2)
        q_cold = np.sum(cold**2)
        q_ordinary = np.sum(ordinary**2)
        denominator = q_high + q_cold + q_ordinary
        n_eff = 1.0 / denominator

        if q_high > q_high_cap + 1e-12:
            raise AssertionError("generated HIGH spectrum violates its L2 cap")
        if cold_total > cold_cap + 1e-12:
            raise AssertionError("generated COLD spectrum violates its flux cap")
        if ordinary.size and ordinary.max() > ordinary_cap + 1e-12:
            raise AssertionError("generated ordinary spectrum violates its cap")
        if n_eff + 1e-10 < theorem_floor:
            raise AssertionError("analytic participation floor violated")

        if n_eff < weakest:
            weakest = n_eff
            worst = (q_high, q_cold, q_ordinary, high_total, cold_total)

    return theorem_floor, weakest, worst


def two_drain_monotonicity_check(seed=29):
    rng = np.random.default_rng(seed)
    gamma = rng.uniform(0.03, 0.8, size=9)
    g_int = rng.uniform(0.15, 1.7, size=9)
    high_balance = 0.73
    s_grid = np.linspace(0.03, 8.0, 5000)

    low_terms = np.array(
        [
            np.sum(s * gamma**2 / (g_int + s * gamma))
            for s in s_grid
        ]
    )
    balance = -high_balance + low_terms
    derivative = np.sum(
        gamma[None, :] ** 2
        * g_int[None, :]
        / (g_int[None, :] + s_grid[:, None] * gamma[None, :]) ** 2,
        axis=1,
    )

    if np.any(np.diff(balance) <= 0.0) or np.any(derivative <= 0.0):
        raise AssertionError("two-drain balance is not strictly monotone")

    sign_changes = np.count_nonzero(balance[:-1] * balance[1:] < 0.0)
    if sign_changes > 1:
        raise AssertionError("monotone balance crossed zero more than once")

    return balance[0], balance[-1], derivative.min(), sign_changes


def two_drain_finite_error_check(seed=41):
    rng = np.random.default_rng(seed)
    gamma = rng.uniform(0.03, 0.8, size=12)
    g_int = rng.uniform(0.15, 1.7, size=12)
    s_1, s_2 = 0.45, 2.3
    high_balance = 0.61

    def low_balance(s):
        return np.sum(s * gamma**2 / (g_int + s * gamma))

    low_1 = low_balance(s_1)
    low_2 = low_balance(s_2)
    f_1 = -high_balance + low_1
    f_2 = -high_balance + low_2
    epsilon_1 = abs(f_1)
    epsilon_2 = abs(f_2)
    x_max = np.max(s_2 * gamma / g_int)
    coefficient = s_1 * (1.0 + x_max) / (s_2 - s_1)
    low_bound = coefficient * (epsilon_1 + epsilon_2)
    high_bound = low_bound + epsilon_1

    if low_1 > low_bound + 1e-12:
        raise AssertionError("finite-error LOW balance bound violated")
    if high_balance > high_bound + 1e-12:
        raise AssertionError("finite-error HIGH balance bound violated")

    return low_1, low_bound, high_balance, high_bound, x_max


def main():
    print("exact HIGH/LOW aggregate-cancellation examples:")
    print(
        f"{'x':>7} {'f_HIGH':>10} {'f_LOW':>10} {'r_tot/R':>10} "
        f"{'N_eff':>10}"
    )
    for x in (0.25, 1.0, 5.0, 25.0, 100.0):
        row = exact_two_channel(beta_omega=1.0, occupation=1e6, starvation_x=x)
        print(
            f"{x:7.2f} {row['f_high']:10.6f} {row['f_cold']:10.6f} "
            f"{row['r_total']/row['r_ref']:10.8f} {row['N_eff']:10.6f}"
        )
        if abs(row["r_total"] / row["r_ref"] - 1.0) > 2e-12:
            raise AssertionError("two-channel cancellation is not exact")

    theorem_floor, weakest, worst = random_bound_check()
    print("\nconditional paired-leg/ordinary-tail bound:")
    print(f"  analytic floor:              {theorem_floor:.6f}")
    print(f"  weakest of random spectra:   {weakest:.6f}")
    print(
        "  worst sampled denominator pieces "
        f"Q_H={worst[0]:.6f}, Q_C={worst[1]:.6f}, "
        f"Q_O={worst[2]:.6f}"
    )
    print(
        "  corresponding totals "
        f"F_H={worst[3]:.6f}, F_C={worst[4]:.6f}"
    )

    start, end, min_derivative, crossings = two_drain_monotonicity_check()
    print("\ntwo-drain exact-separation check:")
    print(f"  balance range:              [{start:.6f}, {end:.6f}]")
    print(f"  minimum analytic derivative: {min_derivative:.6e}")
    print(f"  zero crossings on scan:       {crossings}")

    low, low_bound, high, high_bound, x_max = two_drain_finite_error_check()
    print("\ntwo-drain finite-error check:")
    print(f"  starvation-window maximum X: {x_max:.6f}")
    print(f"  LOW actual / bound:           {low:.6f} / {low_bound:.6f}")
    print(f"  HIGH actual / bound:          {high:.6f} / {high_bound:.6f}")


if __name__ == "__main__":
    main()
