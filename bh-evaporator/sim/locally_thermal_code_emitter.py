"""Five-mode locally thermal diary emitter.

Uses the perfect [[5,1,3]] stabilizer code as a shrinking-shell emission code.
Every individual degeneracy qubit is exactly maximally mixed for every logical
diary state, while any three emitted code qubits recover the diary. Appending
the same fixed thermal energy qubit to each wave packet makes all one-packet
states identical between blind and information-bearing branches.

NumPy only. This is a kinematic code emitter, not an autonomous Hamiltonian.
"""

from __future__ import annotations

import itertools

import numpy as np


I2 = np.eye(2, dtype=np.complex128)
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)


def kron_all(operators: list[np.ndarray]) -> np.ndarray:
    result = np.array([[1.0]], dtype=np.complex128)
    for operator in operators:
        result = np.kron(result, operator)
    return result


def pauli_word(word: str) -> np.ndarray:
    table = {"I": I2, "X": X, "Y": Y, "Z": Z}
    return kron_all([table[letter] for letter in word])


def five_qubit_code() -> np.ndarray:
    stabilizers = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    projector = np.eye(32, dtype=np.complex128)
    for word in stabilizers:
        projector = projector @ (np.eye(32) + pauli_word(word)) / 2.0
    projector = 0.5 * (projector + projector.conj().T)
    values, vectors = np.linalg.eigh(projector)
    code = vectors[:, values > 0.5]
    if code.shape != (32, 2):
        raise AssertionError("five-qubit stabilizer projector did not have rank two")
    logical_z = pauli_word("ZZZZZ")
    compressed_z = code.conj().T @ logical_z @ code
    z_values, z_vectors = np.linalg.eigh(compressed_z)
    order = np.argsort(z_values)[::-1]
    return code @ z_vectors[:, order]


def entropy(matrix: np.ndarray) -> float:
    values = np.linalg.eigvalsh(0.5 * (matrix + matrix.conj().T)).real
    values = values[values > 1e-14]
    return float(-np.sum(values * np.log(values)))


def reference_subset_mutual_information(
    bell_code_state: np.ndarray, subset: tuple[int, ...]
) -> float:
    # State axes are reference Q followed by five emitted modes.
    complement = tuple(index for index in range(5) if index not in subset)
    permutation = (0,) + tuple(index + 1 for index in subset) + tuple(
        index + 1 for index in complement
    )
    state = np.transpose(bell_code_state, permutation)
    d_a = 2 ** len(subset)
    d_c = 2 ** len(complement)
    matrix_qa_c = state.reshape(2 * d_a, d_c)
    rho_qa = matrix_qa_c @ matrix_qa_c.conj().T
    rho4 = rho_qa.reshape(2, d_a, 2, d_a)
    rho_q = np.trace(rho4, axis1=1, axis2=3)
    rho_a = np.trace(rho4, axis1=0, axis2=2)
    return entropy(rho_q) + entropy(rho_a) - entropy(rho_qa)


def main() -> None:
    code = five_qubit_code()
    isometry_error = np.linalg.norm(code.conj().T @ code - np.eye(2))

    # Knill-Laflamme condition for erasure of any one physical mode: every
    # one-mode Pauli compresses to a scalar on the logical code.
    max_local_code_defect = 0.0
    for site in range(5):
        for pauli in (X, Y, Z):
            operators = [I2] * 5
            operators[site] = pauli
            compressed = code.conj().T @ kron_all(operators) @ code
            scalar = np.trace(compressed) / 2.0
            max_local_code_defect = max(
                max_local_code_defect,
                float(np.linalg.norm(compressed - scalar * np.eye(2))),
            )

    bell_code = (code.T / np.sqrt(2.0)).reshape(2, 2, 2, 2, 2, 2)
    by_size: dict[int, list[float]] = {}
    for size in range(6):
        by_size[size] = [
            reference_subset_mutual_information(bell_code, subset)
            for subset in itertools.combinations(range(5), size)
        ]

    # A thermal energy qubit with exp(-beta omega)=1/2 is appended to every
    # degeneracy mode. Its state is independent of the diary and branch.
    thermal_energy = np.diag([2.0 / 3.0, 1.0 / 3.0])
    local_wavepacket = np.kron(thermal_energy, I2 / 2.0)
    local_wavepacket_eigenvalues = np.linalg.eigvalsh(local_wavepacket)

    single_mode_max_mutual = max(by_size[1])
    two_mode_max_mutual = max(by_size[2])
    three_mode_min_mutual = min(by_size[3])
    full_mutual = by_size[5][0]
    target_full = 2.0 * np.log(2.0)
    if isometry_error > 2e-12:
        raise AssertionError("code isometry failed")
    if max_local_code_defect > 2e-12:
        raise AssertionError("single-mode marginals are diary dependent")
    if single_mode_max_mutual > 2e-12 or two_mode_max_mutual > 2e-12:
        raise AssertionError("sub-threshold radiation subset leaked diary information")
    if abs(three_mode_min_mutual - target_full) > 2e-12:
        raise AssertionError("three emitted modes did not recover the diary")
    if abs(full_mutual - target_full) > 2e-12:
        raise AssertionError("full record did not recover the diary")

    print("locally thermal five-mode code emitter:")
    print(f"  code-isometry error:          {isometry_error:.3e}")
    print(f"  max local code defect:        {max_local_code_defect:.3e}")
    print(
        "  one-wavepacket eigenvalues:   "
        + ", ".join(f"{value:.6f}" for value in local_wavepacket_eigenvalues)
    )
    print("  subset size  min I(Q:R_A)  max I(Q:R_A)")
    for size in range(6):
        print(
            f"  {size:11d}  {min(by_size[size]):12.6e}  "
            f"{max(by_size[size]):12.6e}"
        )
    print("  blind branch full I(Q:R):    0 exactly (product local records)")
    print(f"  mixing branch full I(Q:R):   {full_mutual:.6f} = 2 log 2")


if __name__ == "__main__":
    main()
