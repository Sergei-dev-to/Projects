$ErrorActionPreference = 'Stop'

param(
  [switch]$Clean
)

# Switch to the script directory so paths are stable
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

if ($Clean) {
  if (Get-Command latexmk -ErrorAction SilentlyContinue) {
    latexmk -c
    exit 0
  }
  # Best-effort cleanup when latexmk is unavailable
  Get-ChildItem -File -Include *.aux,*.fdb_latexmk,*.fls,*.log,*.out,*.synctex* | Remove-Item -Force -ErrorAction SilentlyContinue
  exit 0
}

if (Get-Command latexmk -ErrorAction SilentlyContinue) {
  Write-Host "Building with latexmk (pdflatex)..."
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  exit $LASTEXITCODE
}

if (Get-Command tectonic -ErrorAction SilentlyContinue) {
  Write-Host "Building with Tectonic..."
  tectonic main.tex
  exit $LASTEXITCODE
}

Write-Warning "No LaTeX toolchain found. Install one of the following:"
Write-Host "  winget install -e --id MiKTeX.MiKTeX    # (includes latexmk)"
Write-Host "  winget install -e --id Tectonic.Tectonic # (auto-fetches packages)"
exit 1

