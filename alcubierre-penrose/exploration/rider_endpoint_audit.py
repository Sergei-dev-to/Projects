"""Quantitative checks for the rider causal-endpoint proof.

This does not construct a global conformal diagram. See sections 6--10 of
notes/joint_boundary_limits.md for the proofs and regularity qualifications.
"""
import json
from pathlib import Path

import numpy as np
from scipy.integrate import quad

import capped_horizon_atlas as cap
from band_tube_shape import Tube, WEIGHT

OUT = Path(__file__).resolve().parents[1] / "output/rider_endpoint_audit"


def sending_time(x):
    """Exact infimum from the center on the positive subsonic axis."""
    return quad(lambda z: 1 / (1 + float(cap.shift(z, 0))), 0, x,
                epsabs=2e-11, epsrel=2e-11, points=[p for p in (.5, .8)
                                                               if p < x])[0]


def main():
    transfers = []
    for endpoint in ((.4, .3), (.95, .3), (-.95, .3), (.3, .9)):
        z = np.array(endpoint)
        positions = np.linspace(0, 1, 1001)[:, None] * z
        v = cap.shift(positions[:, 0], positions[:, 1])
        margin = 1 - float(np.max(np.abs(v)))
        assert margin > 0
        duration = 2 * np.linalg.norm(z) / margin
        largest_norm = -1.
        for orientation in (-1, 1):
            velocity = orientation * z / duration
            causal_norm = -1 + (velocity[0] - v)**2 + velocity[1]**2
            assert np.max(causal_norm) < 0
            largest_norm = max(largest_norm, float(np.max(causal_norm)))
        transfers.append(dict(endpoint=list(endpoint), duration=duration,
                              largest_sampled_g_dot_dot=largest_norm,
                              analytic_upper_bound=-1 + (1-margin/2)**2))

    join = .9
    sj = sending_time(join)
    cs = sj - np.log((1+join)/(1-join)) + np.log(2)
    primitive_errors = []
    for x in (.91, .95, .99, .999):
        exact = -np.log1p(-x) + cs + np.log((1+x)/2)
        primitive_errors.append(abs(sending_time(x)-exact))
    assert max(primitive_errors) < 2e-9

    cap_rows = []
    for lam in (-.25, -1., -4.):
        errors = []
        for time in (6., 10., 14.):
            delta = -lam*np.exp(-time)
            x = 1-delta
            # Evaluate in delta, avoiding subtraction loss in 1-x.
            emission = np.log(-lam)-cs-np.log1p(-delta/2)
            error = abs(emission-(np.log(-lam)-cs))
            errors.append(error)
            cap_rows.append(dict(t=time, cap_lambda=lam, x=x,
                                 latest_emission=emission,
                                 predicted_limit=np.log(-lam)-cs))
        assert errors[2] < errors[1] < errors[0]

    # Event sequences, not claims that these parameterized paths are timelike.
    rate_rows = []
    for rate in (.5, 1., 1.5):
        for time in (10., 20., 30.):
            delta = np.exp(-rate*time)
            emission = (1-rate)*time-cs-np.log1p(-delta/2)
            rate_rows.append(dict(rate=rate, t=time, latest_emission=emission,
                                  log_minus_cap_lambda=(1-rate)*time))

    tube = Tube()
    y = .9
    x = float(tube.horizon.h(y))
    assert -1 < x < 1 and x > 0
    v = float(cap.shift(x, y))
    assert v < -1  # a fixed-position sequence here is not a timelike observer
    hslope = -np.sqrt(v*v-1)
    barrier = v + np.hypot(1, hslope)
    assert abs(barrier) < 1e-13
    ps = sending_time(x)
    log_q_prefactor = quad(lambda z: 1/(float(cap.shift(z, 0))-1), 0, x,
                          epsabs=2e-12, epsrel=2e-12)[0]
    tip = np.array([-.5, 0., 1.5])
    wrong_limits = []
    for time in (4., 8., 12., 16.):
        logp = time-ps
        logq = -time+log_q_prefactor
        alpha = WEIGHT*np.tanh(logp/2)
        beta = -np.tanh(logq/2)
        omega = np.sqrt(WEIGHT/tube.C0)*(1-alpha*beta/WEIGHT)
        image = np.array([(beta-alpha)/2, omega*y, (alpha+beta)/2])
        wrong_limits.append(dict(t=time, image=image.tolist(),
                                 distance_to_wrong_rider_tip=float(np.linalg.norm(image-tip))))
    distances = [row['distance_to_wrong_rider_tip'] for row in wrong_limits]
    assert all(b < a for a, b in zip(distances, distances[1:]))
    assert distances[-1] < 1e-4

    report = dict(
        scope="Numerical checks of analytic arguments; not a global diagram",
        stationary_transfer_checks=transfers,
        axial_sending_constant=cs,
        max_primitive_error=max(primitive_errors),
        finite_cap_emission_limits=cap_rows,
        near_cap_event_sequences=rate_rows,
        sending_wing_counterexample=dict(x=x, y=y, v=v, barrier=barrier,
            original_rider_reachability=False, old_coordinate_limits=wrong_limits),
        conclusion="Two rider causal points; cap negative-infinite end attaches to future rider point; old whole-tube closure fails chronology.")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'checks.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(dict(checks="passed", axial_sending_constant=cs,
                         max_primitive_error=max(primitive_errors),
                         sending_wing_x=x, wrong_tip_distance=distances[-1],
                         output=str(OUT / 'checks.json')), indent=2))


if __name__ == '__main__':
    main()
