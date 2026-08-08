# Wormhole paper

The active manuscript is `wormhole_paper_v7_working.tex`; its latest compiled
PDF is `wormhole_paper_v7_working.pdf`.

- `figures/` — figures used by the active manuscript
- `scripts/` — figure generators and symbolic/numerical utilities
- `notes/` — research, review, planning, and handoff notes
- `reference-material/` — downloaded papers and extracted source bundles
- `artifacts/` — visual QA and legacy rendered figures
- `archive/legacy-drafts/` — superseded manuscript versions

Build from this directory with:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error wormhole_paper_v7_working.tex
```

