# Observer Access in Doubled DSSYK

Date: 2026-07-20

Status: technically hardened standalone draft. The paper extracts the
completed isometric controls, contour audit, and clock-instrument gate without
project-internal sequencing. Its external claim is a DSSYK-specific
demarcation result: exact isometric transport preserves all record and
recovery quantities, so an operational access difference requires a
separately derived resource restriction. The bounded
literature section includes the 2026-07-14--15 observer anti-scrambling
cluster and distinguishes its correlator, trace, and algebra results from a
diary-record process. The completed WP-A3 audit adds a passive-record contour
proposition: a proper 2-OTO anti-scrambling functional requires an explicitly
priced compiler before it becomes an observer record.
The completed clock-instrument gate corrects the earlier positive reading.
Choosing the canonical covariant time POVM for the CLPW maximum-entropy clock
gives a Cauchy one-read density matching the tracial kernel, but CLPW does not
select that POVM's post-measurement instrument. Fresh, persistent, and
contact-disturbed instruments have the same one-read data and different
two-record access. A finite two-contact detector makes the difference
operational, while isometric transport reproduces every completed process in
one-copy DSSYK. The missing inputs are therefore the clock instrument,
detector action, and compiler cost.

Build from this directory with:

```text
latexmk -pdf main.tex
```

If `latexmk` has no Perl engine, use:

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Source notes:

```text
../notes/dssyk_wp0_protocol_and_overlap_2026_07_16.md
../notes/dssyk_wp1_formal_controls_2026_07_16.md
../notes/observer_relative_temporal_access_successor_proposal_2026_07_16.md
../notes/dssyk_observer_process_completion_2026_07_19.md
../notes/dssyk_observer_process_wp_a3_2026_07_19.md
../notes/dssyk_wp2_clock_resource_gate_2026_07_20.md
```

Regression artifact:

```text
python ../sim/dssyk_wp1_controls.py
python ../sim/dssyk_observer_process_controls.py
```

External source package:

```text
main.tex
refs.bib
```

The source package builds without external figures, data files, or custom
classes. `main.pdf` is the verified local rendering and is intentionally not
part of the source package.

Completed external-readiness checks:

```text
- technical and adversarial claim review;
- sector/degeneracy and finite-N versus chord-limit scope pass;
- bounded primary-source overlap pass;
- stable bibliography with no unresolved citations;
- clean PDF build with no layout warnings;
- numerical regression for the exact finite controls;
- no project-internal WP language in the manuscript.
```

Remaining human-supplied submission item:

```text
- author and affiliation block.
```

The bounded overlap wording and the statement that the general isometry lemma
is elementary are part of the scientific scope and should be retained.
