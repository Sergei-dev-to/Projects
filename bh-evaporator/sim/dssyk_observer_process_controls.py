"""Regression checks for the de Sitter observer-process and WP2 notes.

The checks cover five exact controls:

1. the canonical covariant-time density and energy-overlap autocorrelation of
   the CLPW maximum-entropy clock state;
2. the chosen Cauchy random-offset completion with transfer factor
   exp(-a |Delta E|),
   including the binary phase-diary distance and Chernoff exponent;
3. two causally ordered two-record completions with the same one-record
   channel, including a fixed-total-energy relational diary that separates
   fresh-jitter from common-offset memory;
4. a finite two-contact detector-memory comb, a contact-kick control, and
   exact transport through a nontrivial isometry;
5. the model-specific three-dimensional observer-energy cap and its formal
   endpoint speed scale;
6. the optimal state-independent normalization of a direct backwards
   Euclidean segment, including its DSSYK full-band scaling.

This is not an OTOC calculation. It does not assert that CLPW or a
gravitational two-point function selects a time POVM, an instrument, or a
multitime comb. Fresh, persistent, and contact-disturbed processes are
explicit alternative completions of the same one-read clock data.
"""

from __future__ import annotations

import argparse
import math

import numpy as np


def trace_norm_hermitian(matrix: np.ndarray) -> float:
    hermitian = 0.5 * (matrix + matrix.conj().T)
    return float(np.sum(np.abs(np.linalg.eigvalsh(hermitian))))


def cauchy_multiplier(energies: np.ndarray, scale: float) -> np.ndarray:
    gaps = np.abs(energies[:, None] - energies[None, :])
    return np.exp(-scale * gaps)


def cauchy_channel(
    rho: np.ndarray, energies: np.ndarray, scale: float
) -> np.ndarray:
    return cauchy_multiplier(energies, scale) * rho


def phase_diary_states() -> tuple[np.ndarray, np.ndarray]:
    plus = np.array([1.0, 1.0], dtype=np.complex128) / math.sqrt(2.0)
    minus = np.array([1.0, -1.0], dtype=np.complex128) / math.sqrt(2.0)
    return np.outer(plus, plus.conj()), np.outer(minus, minus.conj())


def maximum_entropy_clock_check(beta: float) -> dict[str, float]:
    """Check the canonical time density and overlap of the CLPW clock state."""
    if beta <= 0.0:
        raise ValueError("beta must be positive")

    scale = 0.5 * beta
    frequencies = scale * np.array(
        [-12.0, -3.1, -1.0, -0.17, 0.0, 0.23, 1.7, 9.0]
    )
    amplitudes = math.sqrt(beta / (2.0 * math.pi)) / (
        scale - 1j * frequencies
    )
    fourier_density = np.abs(amplitudes) ** 2
    cauchy_density = scale / (
        math.pi * (scale * scale + frequencies * frequencies)
    )
    density_error = float(np.max(np.abs(fourier_density - cauchy_density)))

    # Under s=a tan[pi(u-1/2)], k_a(s) ds/du is identically one. This
    # verifies normalization without truncating the Cauchy tails.
    u = np.linspace(0.01, 0.99, 99)
    angles = math.pi * (u - 0.5)
    transformed_s = scale * np.tan(angles)
    jacobian = scale * math.pi / np.cos(angles) ** 2
    transformed_density = (
        scale
        / (math.pi * (scale * scale + transformed_s * transformed_s))
        * jacobian
    )
    normalization_map_error = float(
        np.max(np.abs(transformed_density - 1.0))
    )

    mean_energy = 1.0 / beta

    # Wiener--Khinchin on the half-line: the characteristic function of the
    # canonical time density is the energy-wavefunction autocorrelation.
    gaps = np.array([0.0, 0.13, 0.8, 2.7, 6.0]) / beta
    q = np.linspace(0.0, 40.0 / beta, 200_001)
    f = math.sqrt(beta) * np.exp(-0.5 * beta * q)
    overlap_errors = []
    for gap in gaps:
        shifted = math.sqrt(beta) * np.exp(-0.5 * beta * (q + gap))
        numerical = float(np.trapezoid(shifted * f, q))
        predicted = math.exp(-0.5 * beta * gap)
        overlap_errors.append(abs(numerical - predicted))
    overlap_error = max(overlap_errors)

    if density_error > 2e-12:
        raise AssertionError("maximum-entropy clock density is not Cauchy")
    if normalization_map_error > 2e-12:
        raise AssertionError("Cauchy normalization map failed")
    if overlap_error > 2e-8:
        raise AssertionError("clock autocorrelation identity failed")

    return {
        "scale": scale,
        "mean_energy": mean_energy,
        "fourier_density_error": density_error,
        "normalization_map_error": normalization_map_error,
        "overlap_error": overlap_error,
    }


def cauchy_control_check(scale: float, gap: float) -> dict[str, float]:
    if scale <= 0.0 or gap <= 0.0:
        raise ValueError("scale and gap must be positive")

    # Include irregular gaps so positivity is not checked only on a two-level
    # system. The multiplier is a finite correlation matrix of random time
    # translations; its positivity certifies the Schur channel is CP.
    energies = np.array([-0.7 * gap, 0.0, gap, 1.9 * gap])
    multiplier = cauchy_multiplier(energies, scale)
    min_multiplier_eigenvalue = float(np.min(np.linalg.eigvalsh(multiplier)))
    trace_preservation_error = float(
        np.max(np.abs(np.diag(multiplier) - 1.0))
    )

    first = cauchy_multiplier(energies, 0.37 * scale)
    second = cauchy_multiplier(energies, 0.63 * scale)
    semigroup_error = float(
        np.max(np.abs(first * second - multiplier))
    )

    rho_plus, rho_minus = phase_diary_states()
    two_energies = np.array([0.0, gap])
    out_plus = cauchy_channel(rho_plus, two_energies, scale)
    out_minus = cauchy_channel(rho_minus, two_energies, scale)
    actual_distance = 0.5 * trace_norm_hermitian(out_plus - out_minus)
    predicted_distance = math.exp(-scale * gap)

    eta = predicted_distance
    chernoff_coefficient = math.sqrt(max(0.0, 1.0 - eta * eta))
    chernoff_exponent = -math.log(chernoff_coefficient)
    predicted_exponent = -0.5 * math.log(1.0 - eta * eta)

    population_error = float(
        np.max(np.abs(np.diag(out_plus) - np.diag(rho_plus)))
    )

    if min_multiplier_eigenvalue < -2e-12:
        raise AssertionError("Cauchy Schur multiplier is not positive")
    if trace_preservation_error > 2e-12:
        raise AssertionError("Cauchy channel is not trace preserving")
    if semigroup_error > 2e-12:
        raise AssertionError("Cauchy channel semigroup identity failed")
    if abs(actual_distance - predicted_distance) > 2e-12:
        raise AssertionError("phase-diary trace-distance identity failed")
    if abs(chernoff_exponent - predicted_exponent) > 2e-12:
        raise AssertionError("phase-diary Chernoff identity failed")
    if population_error > 2e-12:
        raise AssertionError("Cauchy channel changed energy populations")

    return {
        "min_multiplier_eigenvalue": min_multiplier_eigenvalue,
        "trace_preservation_error": trace_preservation_error,
        "semigroup_error": semigroup_error,
        "phase_distance": actual_distance,
        "chernoff_exponent": chernoff_exponent,
        "population_error": population_error,
    }


def partial_trace_second(rho: np.ndarray, dimension: int) -> np.ndarray:
    tensor = rho.reshape(dimension, dimension, dimension, dimension)
    return np.trace(tensor, axis1=1, axis2=3)


def two_record_memory_check(scale: float, gap: float) -> dict[str, float]:
    """Compare fresh and persistent completions of one canonical time POVM."""
    if scale <= 0.0 or gap <= 0.0:
        raise ValueError("scale and gap must be positive")

    energies = np.array([0.0, gap])
    one_bin = cauchy_multiplier(energies, scale)

    # Basis order: |00>, |01>, |10>, |11>. Fresh jitter factors across
    # bins, whereas a shared offset sees only the total-energy difference.
    fresh_multiplier = np.kron(one_bin, one_bin)
    total_energies = (
        energies[:, None] + energies[None, :]
    ).reshape(-1)
    common_multiplier = cauchy_multiplier(total_energies, scale)

    exchange_plus = np.array(
        [0.0, 1.0, 1.0, 0.0], dtype=np.complex128
    ) / math.sqrt(2.0)
    exchange_minus = np.array(
        [0.0, 1.0, -1.0, 0.0], dtype=np.complex128
    ) / math.sqrt(2.0)
    exchange_plus_state = np.outer(exchange_plus, exchange_plus.conj())
    exchange_minus_state = np.outer(exchange_minus, exchange_minus.conj())
    fresh_output = fresh_multiplier * exchange_plus_state
    common_output = common_multiplier * exchange_plus_state

    witness_distance = 0.5 * trace_norm_hermitian(
        common_output - fresh_output
    )
    eta = math.exp(-scale * gap)
    predicted_distance = 0.5 * (1.0 - eta * eta)
    full_diamond_lower_bound = 2.0 * witness_distance

    # The +/- exchange code is invisible in either one-bin marginal. A common
    # clock preserves its equal-total-energy coherence exactly; fresh clocks
    # attenuate it once in each bin.
    one_bin_diary_distance = 0.5 * trace_norm_hermitian(
        partial_trace_second(exchange_plus_state, 2)
        - partial_trace_second(exchange_minus_state, 2)
    )
    fresh_diary_distance = 0.5 * trace_norm_hermitian(
        fresh_multiplier * (exchange_plus_state - exchange_minus_state)
    )
    common_diary_distance = 0.5 * trace_norm_hermitian(
        common_multiplier * (exchange_plus_state - exchange_minus_state)
    )

    # Both correlated channels must reduce to the same one-bin channel even
    # on an entangled input. This explicitly checks that the witness is a
    # memory distinction, not a changed marginal.
    vector = np.array(
        [1.0, 0.4 + 0.2j, -0.3j, 0.7], dtype=np.complex128
    )
    vector /= np.linalg.norm(vector)
    correlated_state = np.outer(vector, vector.conj())
    input_marginal = partial_trace_second(correlated_state, 2)
    expected_marginal = cauchy_channel(input_marginal, energies, scale)
    fresh_marginal = partial_trace_second(
        fresh_multiplier * correlated_state, 2
    )
    common_marginal = partial_trace_second(
        common_multiplier * correlated_state, 2
    )
    one_bin_marginal_error = max(
        float(np.max(np.abs(fresh_marginal - expected_marginal))),
        float(np.max(np.abs(common_marginal - expected_marginal))),
    )

    minimum_output_eigenvalue = min(
        float(np.min(np.linalg.eigvalsh(fresh_output))),
        float(np.min(np.linalg.eigvalsh(common_output))),
    )

    if abs(witness_distance - predicted_distance) > 2e-12:
        raise AssertionError("two-record memory witness identity failed")
    if one_bin_marginal_error > 2e-12:
        raise AssertionError("two-record completions changed a one-bin channel")
    if minimum_output_eigenvalue < -2e-12:
        raise AssertionError("two-record completion produced a nonpositive state")
    if one_bin_diary_distance > 2e-12:
        raise AssertionError("relational diary leaked into a one-bin marginal")
    if abs(fresh_diary_distance - eta * eta) > 2e-12:
        raise AssertionError("fresh-clock relational diary identity failed")
    if abs(common_diary_distance - 1.0) > 2e-12:
        raise AssertionError("common clock failed to preserve relational diary")

    return {
        "one_bin_marginal_error": one_bin_marginal_error,
        "witness_distance": witness_distance,
        "full_diamond_lower_bound": full_diamond_lower_bound,
        "minimum_output_eigenvalue": minimum_output_eigenvalue,
        "one_bin_diary_distance": one_bin_diary_distance,
        "fresh_diary_distance": fresh_diary_distance,
        "common_diary_distance": common_diary_distance,
    }


def partial_trace_data(rho: np.ndarray, data_dimension: int) -> np.ndarray:
    """Trace the data factor from data x one-qubit-memory."""
    tensor = rho.reshape(data_dimension, 2, data_dimension, 2)
    return np.trace(tensor, axis1=0, axis2=2)


def two_contact_instrument_check(
    scale: float, gap: float, kick: float
) -> dict[str, float]:
    """Check a finite sequential parity record and a clock-contact kick.

    The two data bins carry the exchange diary. A retained memory qubit meets
    bin 1 and bin 2 in sequence and records X_1 X_2 parity. The input states
    are first passed through fresh, persistent, or contact-disturbed clock
    completions. A nontrivial isometry then transports the full contacts and
    record to a larger physical image.
    """
    if scale <= 0.0 or gap <= 0.0 or kick < 0.0:
        raise ValueError("contact-check parameters are outside their range")

    identity = np.eye(2, dtype=np.complex128)
    pauli_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
    memory_zero = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=np.complex128)

    x1 = np.kron(pauli_x, identity)
    x2 = np.kron(identity, pauli_x)
    data_identity = np.eye(4, dtype=np.complex128)
    p1_plus = 0.5 * (data_identity + x1)
    p1_minus = 0.5 * (data_identity - x1)
    p2_plus = 0.5 * (data_identity + x2)
    p2_minus = 0.5 * (data_identity - x2)
    v1 = np.kron(p1_plus, identity) + np.kron(p1_minus, pauli_x)
    v2 = np.kron(p2_plus, identity) + np.kron(p2_minus, pauli_x)
    total_contact = v2 @ v1
    contact_unitarity_error = float(
        np.max(np.abs(total_contact.conj().T @ total_contact - np.eye(8)))
    )

    exchange_plus = np.array(
        [0.0, 1.0, 1.0, 0.0], dtype=np.complex128
    ) / math.sqrt(2.0)
    exchange_minus = np.array(
        [0.0, 1.0, -1.0, 0.0], dtype=np.complex128
    ) / math.sqrt(2.0)
    plus_state = np.outer(exchange_plus, exchange_plus.conj())
    minus_state = np.outer(exchange_minus, exchange_minus.conj())

    energies = np.array([0.0, gap])
    one_bin = cauchy_multiplier(energies, scale)
    fresh_multiplier = np.kron(one_bin, one_bin)
    total_energies = (
        energies[:, None] + energies[None, :]
    ).reshape(-1)
    persistent_multiplier = cauchy_multiplier(total_energies, scale)

    # An uncontrolled symmetric shift +/- kick between contacts models a
    # finite disturbance of the retained clock offset. It leaves the first
    # read untouched and dephases only the relative time of bin 2.
    kick_multiplier_one = np.cos(
        kick * (energies[:, None] - energies[None, :])
    )
    kick_multiplier = np.kron(np.ones((2, 2)), kick_multiplier_one)
    disturbed_multiplier = persistent_multiplier * kick_multiplier

    def record_state(data_state: np.ndarray) -> np.ndarray:
        joint = np.kron(data_state, memory_zero)
        output = total_contact @ joint @ total_contact.conj().T
        return partial_trace_data(output, 4)

    def record_distance(multiplier: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
        plus_record = record_state(multiplier * plus_state)
        minus_record = record_state(multiplier * minus_state)
        distance = 0.5 * trace_norm_hermitian(plus_record - minus_record)
        return distance, plus_record, minus_record

    fresh_distance, fresh_plus_record, fresh_minus_record = record_distance(
        fresh_multiplier
    )
    persistent_distance, persistent_plus_record, persistent_minus_record = (
        record_distance(persistent_multiplier)
    )
    disturbed_distance, _, _ = record_distance(disturbed_multiplier)

    eta = math.exp(-scale * gap)
    predicted_fresh = eta * eta
    predicted_persistent = 1.0
    predicted_disturbed = abs(math.cos(kick * gap))

    # Transport both data bins and both contacts through a nontrivial 2 -> 3
    # isometry, acting as the identity on the retained detector memory.
    rng = np.random.default_rng(20260720)
    raw = rng.normal(size=(3, 2)) + 1j * rng.normal(size=(3, 2))
    isometry, _ = np.linalg.qr(raw)
    isometry_error = float(
        np.max(np.abs(isometry.conj().T @ isometry - identity))
    )
    two_bin_isometry = np.kron(isometry, isometry)
    extended_isometry = np.kron(two_bin_isometry, identity)
    image_projector = extended_isometry @ extended_isometry.conj().T
    complement = np.eye(18, dtype=np.complex128) - image_projector
    transported_contact = (
        extended_isometry @ total_contact @ extended_isometry.conj().T
        + complement
    )
    transported_unitarity_error = float(
        np.max(
            np.abs(
                transported_contact.conj().T @ transported_contact
                - np.eye(18)
            )
        )
    )

    def transported_record(data_state: np.ndarray) -> np.ndarray:
        transported_data = (
            two_bin_isometry @ data_state @ two_bin_isometry.conj().T
        )
        joint = np.kron(transported_data, memory_zero)
        output = (
            transported_contact @ joint @ transported_contact.conj().T
        )
        return partial_trace_data(output, 9)

    transported_records = [
        transported_record(fresh_multiplier * plus_state),
        transported_record(fresh_multiplier * minus_state),
        transported_record(persistent_multiplier * plus_state),
        transported_record(persistent_multiplier * minus_state),
    ]
    original_records = [
        fresh_plus_record,
        fresh_minus_record,
        persistent_plus_record,
        persistent_minus_record,
    ]
    transport_record_error = max(
        float(np.max(np.abs(actual - expected)))
        for actual, expected in zip(transported_records, original_records)
    )

    if contact_unitarity_error > 2e-12:
        raise AssertionError("finite detector contacts are not unitary")
    if abs(fresh_distance - predicted_fresh) > 2e-12:
        raise AssertionError("fresh-instrument contact record failed")
    if abs(persistent_distance - predicted_persistent) > 2e-12:
        raise AssertionError("persistent-instrument contact record failed")
    if abs(disturbed_distance - predicted_disturbed) > 2e-12:
        raise AssertionError("contact-kick record failed")
    if isometry_error > 2e-12:
        raise AssertionError("transport map is not an isometry")
    if transported_unitarity_error > 2e-12:
        raise AssertionError("transported contact is not unitary")
    if transport_record_error > 2e-12:
        raise AssertionError("isometric contact-record transport failed")

    return {
        "contact_unitarity_error": contact_unitarity_error,
        "fresh_record_distance": fresh_distance,
        "persistent_record_distance": persistent_distance,
        "disturbed_record_distance": disturbed_distance,
        "isometry_error": isometry_error,
        "transported_unitarity_error": transported_unitarity_error,
        "transport_record_error": transport_record_error,
    }


def observer_clock_cap_check(newton: float) -> dict[str, float]:
    """Check the formal endpoint of the 3D SdS observer-energy cap."""
    if newton <= 0.0:
        raise ValueError("newton must be positive")

    psi = np.linspace(0.0, 2.0 * math.pi, 257)
    energies = psi * (4.0 * math.pi - psi) / (
        32.0 * math.pi * math.pi * newton
    )
    sampled_maximum = float(np.max(energies))
    expected_maximum = 1.0 / (8.0 * newton)
    endpoint_error = abs(sampled_maximum - expected_maximum)
    orthogonalization_time = math.pi / expected_maximum
    expected_time = 8.0 * math.pi * newton
    speed_scale_error = abs(orthogonalization_time - expected_time)

    if endpoint_error > 2e-12 * expected_maximum:
        raise AssertionError("observer-energy endpoint identity failed")
    if speed_scale_error > 2e-12 * expected_time:
        raise AssertionError("observer-clock speed-scale identity failed")

    return {
        "formal_maximum_energy": sampled_maximum,
        "endpoint_error": endpoint_error,
        "orthogonalization_time": orthogonalization_time,
        "speed_scale_error": speed_scale_error,
    }


def fold_control_check(
    radius: float, newton: float, fold_time: float, shell_width: float
) -> dict[str, float]:
    if min(radius, newton, fold_time, shell_width) <= 0.0:
        raise ValueError("fold parameters must be positive")

    coupling = 1.0 / radius
    deformation = 8.0 * math.pi * newton / radius
    bandwidth = 4.0 * coupling / deformation
    expected_bandwidth = 1.0 / (2.0 * math.pi * newton)

    # A finite sample of the exact cosine band includes both endpoints.
    theta = np.linspace(0.0, math.pi, 129)
    energies = -2.0 * coupling * np.cos(theta) / deformation
    e_max = float(np.max(energies))
    e_min = float(np.min(energies))
    kraus_values = np.exp(fold_time * (energies - e_max))
    success_eigenvalues = kraus_values * kraus_values

    contraction_excess = max(0.0, float(np.max(success_eigenvalues)) - 1.0)
    actual_worst_success = float(np.min(success_eigenvalues))
    predicted_worst_success = math.exp(-2.0 * fold_time * bandwidth)
    shell_worst_success = math.exp(-2.0 * fold_time * shell_width)

    if abs(bandwidth - expected_bandwidth) > 2e-12 * expected_bandwidth:
        raise AssertionError("DSSYK bandwidth dictionary failed")
    if abs((e_max - e_min) - bandwidth) > 2e-12 * bandwidth:
        raise AssertionError("sampled cosine band missed its declared width")
    if contraction_excess > 2e-12:
        raise AssertionError("normalized Euclidean-fold branch is not contractive")
    if abs(actual_worst_success - predicted_worst_success) > max(
        2e-12 * predicted_worst_success, 1e-300
    ):
        raise AssertionError("Euclidean-fold worst-case identity failed")

    return {
        "deformation": deformation,
        "bandwidth": bandwidth,
        "bandwidth_dictionary_error": abs(bandwidth - expected_bandwidth),
        "contraction_excess": contraction_excess,
        "full_worst_success": actual_worst_success,
        "shell_worst_success": shell_worst_success,
        "entropy_scale_exponent": 2.0 * fold_time * bandwidth,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", type=float, default=1.0)
    parser.add_argument("--newton", type=float, default=0.05)
    parser.add_argument(
        "--fold-time",
        type=float,
        default=None,
        help="defaults to one de Sitter radius",
    )
    parser.add_argument(
        "--shell-width",
        type=float,
        default=None,
        help="defaults to one inverse de Sitter radius",
    )
    parser.add_argument("--phase-gap", type=float, default=1.0)
    parser.add_argument(
        "--clock-kick",
        type=float,
        default=0.37,
        help="symmetric retained-clock disturbance between two contacts",
    )
    args = parser.parse_args()

    if args.radius <= 0.0:
        raise ValueError("radius must be positive")
    fold_time = args.radius if args.fold_time is None else args.fold_time
    shell_width = (
        1.0 / args.radius if args.shell_width is None else args.shell_width
    )
    cauchy_scale = math.pi * args.radius
    clock_beta = 2.0 * math.pi * args.radius

    clock = maximum_entropy_clock_check(clock_beta)
    cauchy = cauchy_control_check(cauchy_scale, args.phase_gap)
    memory = two_record_memory_check(cauchy_scale, args.phase_gap)
    instrument = two_contact_instrument_check(
        cauchy_scale, args.phase_gap, args.clock_kick
    )
    clock_cap = observer_clock_cap_check(args.newton)
    fold = fold_control_check(
        args.radius, args.newton, fold_time, shell_width
    )

    print("DSSYK observer-process controls:")
    print("  CLPW maximum-entropy clock")
    print(f"    Cauchy scale beta/2:           {clock['scale']:.6e}")
    print(f"    mean clock energy:             {clock['mean_energy']:.6e}")
    print(
        "    Fourier-density error:        "
        f"{clock['fourier_density_error']:.3e}"
    )
    print(
        "    normalization-map error:      "
        f"{clock['normalization_map_error']:.3e}"
    )
    print(
        "    energy-overlap error:         "
        f"{clock['overlap_error']:.3e}"
    )
    print("  Chosen Cauchy random-offset completion")
    print(
        "    minimum multiplier eigenvalue: "
        f"{cauchy['min_multiplier_eigenvalue']:.3e}"
    )
    print(f"    semigroup error:               {cauchy['semigroup_error']:.3e}")
    print(f"    phase-diary distance:          {cauchy['phase_distance']:.6e}")
    print(f"    Chernoff exponent:             {cauchy['chernoff_exponent']:.6e}")
    print(f"    population error:              {cauchy['population_error']:.3e}")
    print("  Two-bin instrument ambiguity")
    print(
        "    one-bin marginal error:       "
        f"{memory['one_bin_marginal_error']:.3e}"
    )
    print(
        "    output trace distance:        "
        f"{memory['witness_distance']:.6e}"
    )
    print(
        "    full-diamond lower bound:     "
        f"{memory['full_diamond_lower_bound']:.6e}"
    )
    print(
        "    one-bin relational distance:  "
        f"{memory['one_bin_diary_distance']:.6e}"
    )
    print(
        "    fresh-clock diary distance:   "
        f"{memory['fresh_diary_distance']:.6e}"
    )
    print(
        "    common-clock diary distance:  "
        f"{memory['common_diary_distance']:.6e}"
    )
    print("  Finite two-contact record comb")
    print(
        "    contact unitarity error:      "
        f"{instrument['contact_unitarity_error']:.3e}"
    )
    print(
        "    fresh record distance:        "
        f"{instrument['fresh_record_distance']:.6e}"
    )
    print(
        "    persistent record distance:   "
        f"{instrument['persistent_record_distance']:.6e}"
    )
    print(
        "    contact-kick distance:        "
        f"{instrument['disturbed_record_distance']:.6e}"
    )
    print(
        "    isometric record error:       "
        f"{instrument['transport_record_error']:.3e}"
    )
    print("  3D observer-clock cap")
    print(
        "    formal maximum energy:        "
        f"{clock_cap['formal_maximum_energy']:.6e}"
    )
    print(
        "    endpoint orthogonalization:   "
        f"{clock_cap['orthogonalization_time']:.6e}"
    )
    print("  Direct Euclidean-fold branch")
    print(f"    lambda:                        {fold['deformation']:.6e}")
    print(f"    native bandwidth:              {fold['bandwidth']:.6e}")
    print(f"    contraction excess:            {fold['contraction_excess']:.3e}")
    print(f"    full-band worst success:       {fold['full_worst_success']:.6e}")
    print(f"    shell worst success:           {fold['shell_worst_success']:.6e}")
    print(f"    full-band exponent 2 tau B:    {fold['entropy_scale_exponent']:.6e}")


if __name__ == "__main__":
    main()
