from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import LinearOperator, expm_multiply


@dataclass(frozen=True)
class SpinPageRow:
    seed: int
    model: str
    L0: int
    warmup_time: float
    cycle_time: float
    L_before: int
    L_after: int
    rad_qubits: int
    shell_qubits: int
    remaining_qubits: int
    page_capacity: float
    s_rad: float
    old_new_mi: float
    entropy_deficit: float


def grid_id(L0: int, x: int, y: int) -> int:
    return x * L0 + y


def active_qubits(L0: int, L: int) -> list[int]:
    return [grid_id(L0, x, y) for x in range(L) for y in range(L)]


def shell_qubits(L0: int, L: int) -> set[int]:
    return {
        *(grid_id(L0, L - 1, y) for y in range(L)),
        *(grid_id(L0, x, L - 1) for x in range(L - 1)),
    }


def margulis_edges(L0: int) -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    for x in range(L0):
        for y in range(L0):
            src = grid_id(L0, x, y)
            targets = [
                ((x + 2 * y) % L0, y),
                ((x - 2 * y) % L0, y),
                ((x + 2 * y + 1) % L0, y),
                ((x - 2 * y - 1) % L0, y),
                (x, (y + 2 * x) % L0),
                (x, (y - 2 * x) % L0),
                (x, (y + 2 * x + 1) % L0),
                (x, (y - 2 * x - 1) % L0),
            ]
            for tx, ty in targets:
                dst = grid_id(L0, tx, ty)
                if src != dst:
                    edges.add((min(src, dst), max(src, dst)))
    return list(edges)


class SpinHamiltonian:
    def __init__(
        self,
        n_qubits: int,
        active: set[int],
        edges: list[tuple[int, int]],
        seed: int,
        model: str,
    ) -> None:
        self.n = n_qubits
        self.dim = 1 << n_qubits
        self.basis = np.arange(self.dim, dtype=np.uint64)
        self.active = sorted(active)
        self.edges = [(i, j) for i, j in edges if i in active and j in active]
        self.rng = np.random.default_rng(seed)
        self.model = model
        self.fields = self._build_fields()
        self.couplings = self._build_couplings()

    def _build_fields(self) -> dict[int, tuple[float, float]]:
        fields: dict[int, tuple[float, float]] = {}
        for q in self.active:
            if self.model == "deterministic":
                hx = 0.73 + 0.11 * ((q % 5) - 2)
                hz = 0.37 + 0.07 * ((q % 7) - 3)
            elif self.model == "random_heisenberg":
                hx = self.rng.normal(scale=0.7)
                hz = self.rng.normal(scale=0.7)
            else:
                raise ValueError(f"unknown model: {self.model}")
            fields[q] = (hx, hz)
        return fields

    def _build_couplings(self) -> dict[tuple[int, int], tuple[float, float, float]]:
        degree_scale = math.sqrt(max(1.0, 2.0 * len(self.edges) / max(1, len(self.active))))
        couplings: dict[tuple[int, int], tuple[float, float, float]] = {}
        for i, j in self.edges:
            if self.model == "deterministic":
                code = ((i + 3) * (j + 5)) % 17
                jx = (0.50 + 0.03 * code) / degree_scale
                jy = (0.43 + 0.02 * ((code + 5) % 17)) / degree_scale
                jz = (0.61 + 0.025 * ((code + 11) % 17)) / degree_scale
            elif self.model == "random_heisenberg":
                jx, jy, jz = self.rng.normal(size=3) / degree_scale
            else:
                raise ValueError(f"unknown model: {self.model}")
            couplings[(i, j)] = (jx, jy, jz)
        return couplings

    def _z_sign(self, q: int) -> np.ndarray:
        bit = (self.basis >> np.uint64(q)) & np.uint64(1)
        return 1.0 - 2.0 * bit.astype(float)

    def matvec(self, vector: np.ndarray) -> np.ndarray:
        vector = np.asarray(vector, dtype=np.complex128).reshape(-1)
        out = np.zeros_like(vector, dtype=np.complex128)

        for q, (hx, hz) in self.fields.items():
            out += hz * self._z_sign(q) * vector
            out[self.basis ^ np.uint64(1 << q)] += hx * vector

        for (i, j), (jx, jy, jz) in self.couplings.items():
            zi = self._z_sign(i)
            zj = self._z_sign(j)
            flip = self.basis ^ np.uint64(1 << i) ^ np.uint64(1 << j)

            out += jz * zi * zj * vector
            out[flip] += jx * vector
            out[flip] += jy * (-(zi * zj)) * vector

        return out

    def linear_operator(self) -> LinearOperator:
        return LinearOperator(
            shape=(self.dim, self.dim),
            matvec=self.matvec,
            rmatvec=self.matvec,
            dtype=np.complex128,
        )

    def sparse_matrix(self) -> csr_matrix:
        basis = self.basis.astype(np.int64)
        rows: list[np.ndarray] = []
        cols: list[np.ndarray] = []
        data: list[np.ndarray] = []

        diag = np.zeros(self.dim, dtype=np.complex128)
        for q, (hx, hz) in self.fields.items():
            diag += hz * self._z_sign(q)
            rows.append((self.basis ^ np.uint64(1 << q)).astype(np.int64))
            cols.append(basis)
            data.append(np.full(self.dim, hx, dtype=np.complex128))

        for (i, j), (jx, jy, jz) in self.couplings.items():
            zi = self._z_sign(i)
            zj = self._z_sign(j)
            flip = (self.basis ^ np.uint64(1 << i) ^ np.uint64(1 << j)).astype(
                np.int64
            )

            diag += jz * zi * zj
            rows.append(flip)
            cols.append(basis)
            data.append((jx + jy * (-(zi * zj))).astype(np.complex128))

        rows.append(basis)
        cols.append(basis)
        data.append(diag)

        return coo_matrix(
            (np.concatenate(data), (np.concatenate(rows), np.concatenate(cols))),
            shape=(self.dim, self.dim),
        ).tocsr()


def evolve(
    state: np.ndarray,
    hamiltonian: SpinHamiltonian,
    time: float,
) -> np.ndarray:
    if time == 0.0:
        return state
    matrix = hamiltonian.sparse_matrix()
    evolved = expm_multiply((-1j * time) * matrix, state, traceA=0.0)
    return evolved / np.linalg.norm(evolved)


def entropy_of_subset(state: np.ndarray, n_qubits: int, subset: set[int]) -> float:
    if not subset or len(subset) == n_qubits:
        return 0.0

    use_subset = set(subset)
    if len(use_subset) > n_qubits // 2:
        use_subset = set(range(n_qubits)) - use_subset
    if not use_subset:
        return 0.0

    axes_for_qubits = {q: n_qubits - 1 - q for q in range(n_qubits)}
    keep_axes = [axes_for_qubits[q] for q in sorted(use_subset)]
    trace_axes = [axis for axis in range(n_qubits) if axis not in keep_axes]
    tensor = state.reshape((2,) * n_qubits)
    matrix = np.transpose(tensor, keep_axes + trace_axes).reshape(
        1 << len(keep_axes), -1
    )
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    probs = singular_values**2
    probs = probs[probs > 1e-12]
    return float(-np.sum(probs * np.log(probs)))


def random_product_state(n_qubits: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    state = np.array([1.0 + 0.0j])
    for _ in range(n_qubits):
        theta = rng.uniform(0.0, math.pi)
        phi = rng.uniform(0.0, 2.0 * math.pi)
        qubit = np.array(
            [math.cos(theta / 2.0), np.exp(1j * phi) * math.sin(theta / 2.0)]
        )
        state = np.kron(state, qubit)
    return state / np.linalg.norm(state)


def run_spin_page_diagnostic(
    L0: int,
    model: str,
    warmup_time: float,
    cycle_time: float,
    seed: int,
) -> list[SpinPageRow]:
    n_qubits = L0 * L0
    edges = margulis_edges(L0)
    state = random_product_state(n_qubits, seed + 10_000)
    radiation: set[int] = set()
    rows: list[SpinPageRow] = []

    h0 = SpinHamiltonian(
        n_qubits=n_qubits,
        active=set(active_qubits(L0, L0)),
        edges=edges,
        seed=seed,
        model=model,
    )
    state = evolve(state, h0, warmup_time)

    for L in range(L0, 0, -1):
        h_l = SpinHamiltonian(
            n_qubits=n_qubits,
            active=set(active_qubits(L0, L)),
            edges=edges,
            seed=seed,
            model=model,
        )
        state = evolve(state, h_l, cycle_time)

        old_radiation = set(radiation)
        shell = shell_qubits(L0, L)
        radiation |= shell

        remaining = L * L - len(shell)
        capacity = min(len(radiation), remaining) * math.log(2.0)
        s_old = entropy_of_subset(state, n_qubits, old_radiation)
        s_new = entropy_of_subset(state, n_qubits, shell)
        s_rad = entropy_of_subset(state, n_qubits, radiation)
        old_new_mi = max(0.0, s_old + s_new - s_rad)

        rows.append(
            SpinPageRow(
                seed=seed,
                model=model,
                L0=L0,
                warmup_time=warmup_time,
                cycle_time=cycle_time,
                L_before=L,
                L_after=L - 1,
                rad_qubits=len(radiation),
                shell_qubits=len(shell),
                remaining_qubits=remaining,
                page_capacity=capacity,
                s_rad=s_rad,
                old_new_mi=old_new_mi,
                entropy_deficit=capacity - s_rad,
            )
        )
    return rows


def write_rows(rows: list[SpinPageRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(SpinPageRow.__dataclass_fields__))
        writer.writeheader()
        for row in rows:
            writer.writerow(row.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    cases = [
        ("random_heisenberg", 3, 4.0, 1.0),
        ("deterministic", 3, 4.0, 1.0),
    ]
    seeds = list(range(2))

    for model, L0, warmup, cycle in cases:
        all_rows: list[SpinPageRow] = []
        deficits: list[float] = []
        first_mis: list[str] = []
        for seed in seeds:
            rows = run_spin_page_diagnostic(
                L0=L0,
                model=model,
                warmup_time=warmup,
                cycle_time=cycle,
                seed=seed,
            )
            all_rows.extend(rows)
            deficits.append(sum(max(0.0, row.entropy_deficit) for row in rows))
            first_mi = next((row for row in rows if row.old_new_mi > 1e-6), None)
            if first_mi is not None:
                first_mis.append(f"{first_mi.L_before}->{first_mi.L_after}")

        out_path = out_dir / (
            "interacting_spin_page_"
            f"{model}_L{L0}_warm{warmup:g}_cyc{cycle:g}.csv"
        )
        write_rows(all_rows, out_path)
        print(
            model,
            f"L0={L0}",
            f"warmup={warmup:g}",
            f"cycle={cycle:g}",
            f"mean total deficit={sum(deficits) / len(deficits):.3f}",
            f"max total deficit={max(deficits):.3f}",
            "first MI modes=" + ",".join(sorted(set(first_mis))) if first_mis else "",
        )


if __name__ == "__main__":
    main()
