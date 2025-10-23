param(
  [switch]$Clean,
  [switch]$Open
)

${ErrorActionPreference} = 'Stop'

# Switch to the script directory so paths are stable
Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

# Try to ensure MiKTeX binaries are on PATH for this process
$miKTeXUser = Join-Path $env:LOCALAPPDATA 'Programs\MiKTeX\miktex\bin\x64'
$miKTeXProgram = Join-Path $env:ProgramFiles 'MiKTeX\miktex\bin\x64'
foreach ($p in @($miKTeXUser, $miKTeXProgram)) {
  if ($p -and (Test-Path $p) -and ($env:PATH -notlike "*${p}*")) {
    $env:PATH = "$p;$env:PATH"
  }
}

function Invoke-PdfLaTeX {
  if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Error "pdflatex not found on PATH. Install MiKTeX or TeX Live, or add pdflatex to PATH."
    exit 1
  }
  Write-Host "Building with pdflatex (2 passes)..."
  $job = $script:JobName
  if (-not $job) { $job = 'main' }
  pdflatex "-jobname=$job" -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
  pdflatex "-jobname=$job" -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  exit $LASTEXITCODE
}

if ($Clean) {
  if (Get-Command latexmk -ErrorAction SilentlyContinue) {
    latexmk -c
  }
  # Best-effort cleanup when latexmk is unavailable
  Get-ChildItem -File -Include *.aux,*.fdb_latexmk,*.fls,*.log,*.out,*.synctex* -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
  exit 0
}

if (Get-Command tectonic -ErrorAction SilentlyContinue) {
  Write-Host "Building with Tectonic..."
  tectonic main.tex
  exit $LASTEXITCODE
}

# Handle locked main.pdf by switching jobname
$script:JobName = 'main'
try {
  if (Test-Path 'main.pdf') { Remove-Item 'main.pdf' -Force }
}
catch {
  Write-Warning "main.pdf appears to be open/locked; building to main_build.pdf instead. Close the viewer to overwrite main.pdf next time."
  $script:JobName = 'main_build'
}

if (Get-Command latexmk -ErrorAction SilentlyContinue) {
  Write-Host "Building with latexmk (pdflatex)..."
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  if ($LASTEXITCODE -eq 0) { exit 0 }
  Write-Warning "latexmk failed (possibly missing Perl). Falling back to pdflatex."
  Invoke-PdfLaTeX
}

# Final fallback
Invoke-PdfLaTeX

