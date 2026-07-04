from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PagePoint:
    L: int
    log_dim_bh: float
    log_dim_rad: float
    capacity_entropy: float
    page_entropy: float
    page_correction: float
    rad_fraction: float


@dataclass(frozen=True)
class ShellMutualInformationPoint:
    L_before: int
    L_after: int
    log_dim_old_rad: float
    log_dim_new_shell: float
    log_dim_remaining_bh: float
    old_new_mi: float
    old_new_mi_fraction_of_new_shell: float
    rad_fraction_after: float


def page_entropy_asymptotic(log_dim_a: float, log_dim_b: float) -> tuple[float, float]:
    """Average entropy of the smaller side of a Haar-random bipartite state.

    Page's exact formula for subsystem dimensions m <= n is

        H_mn - H_n - (m - 1)/(2n).

    The dimensions here are enormous, so we use the large-dimension form

        log(m) - m/(2n),

    with endpoint guards. The returned correction is the amount subtracted from
    the capacity min(log dim A, log dim B).
    """

    log_m = min(log_dim_a, log_dim_b)
    log_n = max(log_dim_a, log_dim_b)
    if log_m <= 0.0:
        return 0.0, 0.0

    ratio_log = log_m - log_n
    correction = 0.5 * math.exp(ratio_log) if ratio_log > -745.0 else 0.0
    return log_m - correction, correction


def build_curve(L0: int = 40, q: int = 2) -> list[PagePoint]:
    log_q = math.log(q)
    total_entropy = L0 * L0 * log_q
    points: list[PagePoint] = []

    for L in range(L0, -1, -1):
        log_dim_bh = L * L * log_q
        log_dim_rad = total_entropy - log_dim_bh
        capacity = min(log_dim_bh, log_dim_rad)
        page, correction = page_entropy_asymptotic(log_dim_bh, log_dim_rad)
        points.append(
            PagePoint(
                L=L,
                log_dim_bh=log_dim_bh,
                log_dim_rad=log_dim_rad,
                capacity_entropy=capacity,
                page_entropy=page,
                page_correction=correction,
                rad_fraction=log_dim_rad / total_entropy if total_entropy else 0.0,
            )
        )

    return points


def entropy_of_part(log_dim_part: float, log_dim_total: float) -> float:
    return page_entropy_asymptotic(log_dim_part, log_dim_total - log_dim_part)[0]


def build_shell_mi_curve(L0: int = 40, q: int = 2) -> list[ShellMutualInformationPoint]:
    log_q = math.log(q)
    total_entropy = L0 * L0 * log_q
    points: list[ShellMutualInformationPoint] = []

    for L in range(L0, 0, -1):
        old_rad = (L0 * L0 - L * L) * log_q
        new_shell = (2 * L - 1) * log_q
        remaining = (L - 1) * (L - 1) * log_q

        s_old = entropy_of_part(old_rad, total_entropy)
        s_new = entropy_of_part(new_shell, total_entropy)
        s_old_new = entropy_of_part(old_rad + new_shell, total_entropy)
        mi = max(0.0, s_old + s_new - s_old_new)
        denom = 2.0 * new_shell if new_shell > 0.0 else 1.0

        points.append(
            ShellMutualInformationPoint(
                L_before=L,
                L_after=L - 1,
                log_dim_old_rad=old_rad,
                log_dim_new_shell=new_shell,
                log_dim_remaining_bh=remaining,
                old_new_mi=mi,
                old_new_mi_fraction_of_new_shell=mi / denom,
                rad_fraction_after=(old_rad + new_shell) / total_entropy
                if total_entropy
                else 0.0,
            )
        )

    return points


def write_curve(points: list[PagePoint], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(PagePoint.__dataclass_fields__))
        writer.writeheader()
        for point in points:
            writer.writerow(point.__dict__)


def write_shell_mi_curve(points: list[ShellMutualInformationPoint], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(ShellMutualInformationPoint.__dataclass_fields__)
        )
        writer.writeheader()
        for point in points:
            writer.writerow(point.__dict__)


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "data"
    for L0 in (40, 80):
        points = build_curve(L0=L0, q=2)
        write_curve(points, out_dir / f"random_isometry_page_curve_L{L0}.csv")
        mi_points = build_shell_mi_curve(L0=L0, q=2)
        write_shell_mi_curve(
            mi_points, out_dir / f"random_isometry_shell_mi_L{L0}.csv"
        )

        crossing = min(points, key=lambda p: abs(p.log_dim_bh - p.log_dim_rad))
        peak = max(points, key=lambda p: p.page_entropy)
        first_correlated = next(
            (p for p in mi_points if p.old_new_mi_fraction_of_new_shell > 0.5),
            None,
        )
        print(f"L0={L0}")
        print(
            "  crossing:",
            f"L={crossing.L}",
            f"rad_fraction={crossing.rad_fraction:.6f}",
            f"capacity={crossing.capacity_entropy:.6f}",
            f"page={crossing.page_entropy:.6f}",
            f"correction={crossing.page_correction:.6f}",
        )
        print(
            "  peak:",
            f"L={peak.L}",
            f"rad_fraction={peak.rad_fraction:.6f}",
            f"page={peak.page_entropy:.6f}",
        )
        if first_correlated is not None:
            print(
                "  first strong old/new MI:",
                f"L={first_correlated.L_before}->{first_correlated.L_after}",
                f"rad_fraction_after={first_correlated.rad_fraction_after:.6f}",
                "I/(2S_new)="
                f"{first_correlated.old_new_mi_fraction_of_new_shell:.6f}",
            )


if __name__ == "__main__":
    main()
