# Observer Access in Doubled DSSYK

Date: 2026-07-19

Status: technically hardened standalone draft. The paper extracts the
completed WP0--WP1.5 result without project-internal sequencing. Its external
claim is a DSSYK-specific demarcation result: exact isometric transport
preserves all record and recovery quantities, so an operational access
difference requires a separately derived resource restriction.

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
```

Regression artifact:

```text
python ../sim/dssyk_wp1_controls.py
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
