"""Rebuild upload staging directories from the canonical paper/ source.

The paper/ directory is the source of truth.  This script regenerates the
arXiv and CQG staging directories and zip archives from that source, then
optionally tests that each zip compiles after extraction.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
ARXIV_STAGE = ROOT / "arxiv_source"
ARXIV_ZIP = ROOT / "alcubierre_arxiv_source.zip"
ARXIV_TEST = ROOT / "arxiv_zip_test"
CQG_STAGE = ROOT / "cqg_source"
CQG_ZIP = ROOT / "alcubierre_cqg_source.zip"
CQG_TEST = ROOT / "cqg_zip_test"
IOP_TEMPLATE = ROOT / "templates" / "iop" / "extracted"
TOP_LEVEL_BUILD_ARTIFACTS = (
    "main.aux",
    "main.blg",
    "main.log",
    "main.out",
    "main.pdf",
)


def safe_remove(path: Path) -> None:
    path = path.resolve()
    root = ROOT.resolve()
    if path == root or root not in path.parents:
        raise RuntimeError(f"refusing to remove outside project: {path}")
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def run(cmd: list[str], cwd: Path) -> None:
    print(f"[run] {' '.join(cmd)}  (cwd={cwd})")
    subprocess.run(cmd, cwd=cwd, check=True)


def compile_paper() -> None:
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], PAPER)
    run(["bibtex", "main"], PAPER)
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], PAPER)
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], PAPER)


def referenced_figures(tex: str) -> list[Path]:
    figures: list[Path] = []
    for match in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        rel = Path(match.group(1))
        if rel.suffix == "":
            rel = rel.with_suffix(".pdf")
        figures.append(rel)
    return figures


def transform_for_cqg(tex: str) -> str:
    """Convert the canonical article source to IOP's iopjournal front matter."""
    tex = re.sub(
        r"\\documentclass(?:\[[^\]]*\])?\{article\}",
        r"\\documentclass{iopjournal}",
        tex,
        count=1,
    )
    tex = tex.replace(r"\usepackage{graphicx}" + "\n", "")
    tex = tex.replace(r"\usepackage[margin=1in]{geometry}" + "\n", "")
    tex = tex.replace(r"\usepackage{hyperref}" + "\n", "")
    tex = re.sub(r"\\hypersetup\{.*?\}\n\n", "", tex, count=1, flags=re.S)

    title_match = re.search(r"\\title\{(?P<title>.*?)\}", tex, re.S)
    if not title_match:
        raise RuntimeError("could not find title block")
    title = title_match.group("title")

    # IOP's template class hardcodes proof-stage placeholders such as
    # "Journal Name", "Author et al", and a Crossmark/date margin block.
    # Keep the class for package compatibility, but suppress that template
    # chrome in the generated submission PDF.
    iop_display_overrides = (
        "\\pagestyle{plain}\n"
        "\\renewcommand{\\articletype}[1]{{\\noindent\\scriptsize\\sffamily"
        "\\bfseries\\MakeUppercase{#1}\\par\\vspace{2mm}}}\n"
    )
    front_matter = (
        "\\begin{document}\n\n"
        f"{iop_display_overrides}\n"
        "\\articletype{Paper}\n\n"
        f"\\title{{{title}}}\n\n"
        "\\author{Sergei Slobodov}\n\n"
        "\\affil{Independent researcher}\n\n"
        "\\email{sergei@slobodov.com}\n\n"
        "\\begin{abstract}"
    )
    cqg_keywords = (
        "\\keywords{warp drive, Alcubierre spacetime, Cauchy horizon, "
        "curvature singularity, general relativity}"
    )
    # The canonical (article-class) source places \maketitle before the
    # abstract.  iopjournal typesets the title commands in place and does not
    # use \maketitle, so the whole block from \begin{document} through
    # \begin{abstract} (including \maketitle) is replaced by the IOP front
    # matter.
    tex = re.sub(
        r"\\begin\{document\}\s*"
        r"\\title\{.*?\}\s*"
        r"\\author\{.*?\}\s*"
        r"\\date\{.*?\}\s*"
        r"\\maketitle\s*"
        r"\\begin\{abstract\}",
        lambda _: front_matter,
        tex,
        count=1,
        flags=re.S,
    )
    tex = tex.replace(
        "\\end{abstract}",
        f"\\end{{abstract}}\n\n{cqg_keywords}",
        1,
    )
    return tex


def clean_top_level_build_artifacts(stage: Path) -> None:
    for name in TOP_LEVEL_BUILD_ARTIFACTS:
        path = stage / name
        if path.exists():
            path.unlink()


def copy_required_source(stage: Path, package_name: str) -> None:
    if stage.exists():
        safe_remove(stage)
    stage.mkdir(parents=True)

    tex = (PAPER / "main.tex").read_text(encoding="utf-8-sig")
    if package_name == "CQG":
        tex = transform_for_cqg(tex)
        iop_class = IOP_TEMPLATE / "iopjournal.cls"
        if not iop_class.exists():
            raise FileNotFoundError(f"missing IOP class file: {iop_class}")
        shutil.copy2(iop_class, stage / "iopjournal.cls")
        orcid = IOP_TEMPLATE / "orcid.pdf"
        if orcid.exists():
            shutil.copy2(orcid, stage / "orcid.pdf")
        (stage / "main.tex").write_text(tex, encoding="utf-8")
    else:
        shutil.copy2(PAPER / "main.tex", stage / "main.tex")
        shutil.copy2(PAPER / "main.bbl", stage / "main.bbl")

    shutil.copy2(PAPER / "references.bib", stage / "references.bib")
    for rel in referenced_figures(tex):
        src = PAPER / rel
        if not src.exists():
            raise FileNotFoundError(f"referenced figure not found: {src}")
        dst = stage / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    supplement = PAPER / "supplement"
    if supplement.exists():
        shutil.copytree(
            supplement,
            stage / "supplement",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "paper"),
        )

    readme = stage / "README_STAGING.txt"
    iop_note = (
        "This CQG package uses the official IOP Publishing iopjournal class\n"
        "downloaded from IOP Publishing's LaTeX template package.\n"
        if package_name == "CQG"
        else "This arXiv package uses the canonical paper/main.tex source.\n"
    )
    readme.write_text(
        (
            f"{package_name} staging package generated from paper/.\n\n"
            "The canonical manuscript source is paper/main.tex. This directory is\n"
            "generated by scripts/build_staging.py and should not be edited by hand.\n"
            "It contains main.tex, main.bbl, references.bib, required figures, and\n"
            "the supplemental algebra/figure scripts.\n\n"
            f"{iop_note}"
        ),
        encoding="utf-8",
    )


def make_zip(stage: Path, zip_path: Path) -> None:
    if zip_path.exists():
        safe_remove(zip_path)
    archive_base = zip_path.with_suffix("")
    shutil.make_archive(str(archive_base), "zip", root_dir=stage)


def compile_dir(work_dir: Path, run_bibtex: bool) -> None:
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], work_dir)
    if run_bibtex:
        run(["bibtex", "main"], work_dir)
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], work_dir)
    run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], work_dir)


def test_zip(zip_path: Path, test_dir: Path, run_bibtex: bool) -> None:
    if test_dir.exists():
        safe_remove(test_dir)
    test_dir.mkdir(parents=True)
    shutil.unpack_archive(zip_path, test_dir)
    compile_dir(test_dir, run_bibtex=run_bibtex)


def build_package(stage: Path, zip_path: Path, test_dir: Path, name: str, do_test: bool) -> None:
    copy_required_source(stage, name)
    if name == "CQG":
        compile_dir(stage, run_bibtex=True)
        clean_top_level_build_artifacts(stage)
    make_zip(stage, zip_path)
    if do_test:
        test_zip(zip_path, test_dir, run_bibtex=(name == "CQG"))
    print(f"[ok] rebuilt {stage}")
    print(f"[ok] wrote {zip_path}")
    if do_test:
        print(f"[ok] tested extraction in {test_dir}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-compile", action="store_true", help="skip rebuilding paper/main.bbl")
    parser.add_argument("--no-test", action="store_true", help="skip extracting and compiling the zip")
    parser.add_argument(
        "--target",
        choices=("all", "arxiv", "cqg"),
        default="all",
        help="which staging package to rebuild",
    )
    args = parser.parse_args()

    if not args.no_compile:
        compile_paper()

    do_test = not args.no_test
    if args.target in ("all", "arxiv"):
        build_package(ARXIV_STAGE, ARXIV_ZIP, ARXIV_TEST, "arXiv", do_test)
    if args.target in ("all", "cqg"):
        build_package(CQG_STAGE, CQG_ZIP, CQG_TEST, "CQG", do_test)


if __name__ == "__main__":
    main()
