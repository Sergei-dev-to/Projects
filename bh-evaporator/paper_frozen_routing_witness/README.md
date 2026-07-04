# Frozen-Routing Witness Proposal

Date: 2026-07-02

Status: first full draft, PDF builds cleanly.

Proposal paper: a transport-frozen control arm for scrambling
experiments.  Freeze bulk routing gates, keep the record coupling and
schedule, and test whether decoding survives — separating dynamical
routing from prearranged/nonlocal/dressed access.  Includes the
confidence-bound witness inequality, two freezing certificates, an
L=6 two-copy Yoshida-Kitaev instance (~24 qubits with the public
layer), a worst-of-published-values error budget (margin >= 0.25
without mitigation), the stage-0 public-record layer (simultaneous
access profile / operational Heisenberg-cut demonstration), and the
weak-link/disorder discriminating sweep.

Sources and planning trail:

```text
paper_access_latency_classification/notes/directions/
    frozen_routing_platform_proposal.md      (the plan)
    frozen_routing_m1_m3_working_note.md     (M1-M5: design, pinning,
                                              budgets — all inputs)
paper_access_latency_classification/notes/qi_access_inequality_note.md
                                             (theory backdrop)
```

Support numerics (2026-07-02): exact statevector simulation of the
L=6 instance in `../figs/generate_frozen_routing_witness_figs.py`
(support role only — two rigorous bounds, no modeling of hardware
noise).  It CORRECTED the draft: m=2-3 records insufficient (ideal
achievable ~0.4); emission must wait for scrambling onset; final
config m=4, depth 24, emissions at layers 14/17/20/23, ideal
achievable 0.84 +/- 0.04.  Frozen-arm upper bound pins at 1/4 to
numerical precision.  Figures: fig_arms.pdf (schedule schematic),
fig_signature.pdf (witness signature).

Open items before external use:

```text
- confirm the Willow SI mean CZ error (footnote in Sec. 5; the
  worst-of-both conclusion does not depend on it).
- replace the two-family budget with a single-device budget once a
  target device/collaboration is fixed.
- companion access-profile note cited as "in preparation" — decide
  its fate before submission.
```

Done 2026-07-02 (third simulation pass,
`../figs/generate_frozen_routing_decoder_check.py`): direct two-copy
YK decoder simulation.  F_YK = 0.764 +/- 0.050 at P_success = 0.048
(normal arm); exactly 1/4 at P = 1/8 (frozen arm).  Corrections
folded into the paper: post-selection overhead ~20x not ~4x (run
budget now ~1e6 executions/curve, still under an hour); margin table
now uses the decoder's own number (margins >= 0.35 / >= 0.25);
limitation (v) rescoped to noise-model composition.

Post-review fixes (2026-07-02, second review): Blok 0.568 is F_avg
(qutrit) — converted to F_e ~ 0.42 vs 1/9 baseline and demoted from
margin input to hardware-realism reference; echo arm redefined as
refocusing cycles per inter-emission window (single mid-run reversal
would let late emissions sample the return path — not a null
control); abstract hedged to match discussion; "required the frozen
transport" wording fixed.

Resolved 2026-07-02: arXiv:2112.11204 is Wang et al. (not Zhu),
unpublished as of this date; Google QEC = Nature 638, 920-926 (2025)
confirmed.
