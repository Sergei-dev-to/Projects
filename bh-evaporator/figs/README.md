Regenerating figures
====================

Goal: every figure in the paper is generated from versioned code and data.

Quick start
- Ensure Python 3.9+ is available (`python --version`).
- Optionally install deps: `pip install -r figs/requirements.txt`.
- Generate figures: `python figs/generate.py --only-missing`.

Notes
- The build script (`build.ps1`) calls `python figs/generate.py --only-missing` before compiling the PDF. If Python or matplotlib are not available, it prints a warning and continues without failing the LaTeX build.
- Figures are written directly into `bh-evaporator/` with the filenames expected by `main.tex`.
- Each figure has a dedicated generator function; add new ones by extending `TARGETS` in `generate.py`.
- The script embeds the current Git commit hash in the PDF metadata for provenance.

