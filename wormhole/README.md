# Wormhole paper

The active manuscript is `wormhole_paper_v10_working.tex`; its latest compiled
PDF is `wormhole_paper_v10_working.pdf`.

- `figures/` — figures used by the active manuscript
- `scripts/` — figure generators and symbolic/numerical utilities
- `notes/` — research, review, planning, and handoff notes
- `reference-material/` — downloaded papers and extracted source bundles

Superseded drafts and visual-review artifacts remain recoverable from Git
history through commit `2c29f3b`.

Build from this directory with:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error wormhole_paper_v10_working.tex
bibtex wormhole_paper_v10_working
pdflatex -interaction=nonstopmode -halt-on-error wormhole_paper_v10_working.tex
pdflatex -interaction=nonstopmode -halt-on-error wormhole_paper_v10_working.tex
```
