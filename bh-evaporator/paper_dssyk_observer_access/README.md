# Observer Access in Doubled DSSYK

Date: 2026-07-16

Status: first standalone technical draft. The paper extracts the completed
WP0--WP1 result without project-internal sequencing. Its external claim is a
DSSYK-specific demarcation result: exact isometric transport preserves all
record and recovery quantities, so an operational access difference requires
a separately derived resource restriction.

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

Before external circulation:

```text
- line-edit after technical review;
- verify bibliographic publication metadata where journal details are added;
- decide author/affiliation block;
- retain the bounded wording of the DSSYK overlap claim;
- do not present the abstract isometry lemma as a new general QI theorem.
```
