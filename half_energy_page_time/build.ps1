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

$mainTex = 'half_energy_page_time.tex'
$defaultJobName = 'half_energy_page_time'

function Invoke-PdfLaTeX {
  param(
    [string]$JobName
  )

  if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Error "pdflatex not found on PATH. Install MiKTeX or TeX Live, or add pdflatex to PATH."
    exit 1
  }

  Write-Host "Building with pdflatex (pass 1/3)..."
  pdflatex "-jobname=$JobName" -interaction=nonstopmode -halt-on-error -file-line-error $mainTex

  if (Get-Command bibtex -ErrorAction SilentlyContinue) {
    Write-Host "Running bibtex..."
    bibtex $JobName
  }
  else {
    Write-Warning "bibtex not found; bibliography will be missing."
  }

  Write-Host "Building with pdflatex (pass 2/3)..."
  pdflatex "-jobname=$JobName" -interaction=nonstopmode -halt-on-error -file-line-error $mainTex

  Write-Host "Building with pdflatex (pass 3/3)..."
  pdflatex "-jobname=$JobName" -interaction=nonstopmode -halt-on-error -file-line-error $mainTex
  exit $LASTEXITCODE
}

if ($Clean) {
  if (Get-Command latexmk -ErrorAction SilentlyContinue) {
    try { latexmk -c } catch {}
  }
  # Best-effort cleanup when latexmk is unavailable
  Get-ChildItem -File -Include *.aux,*.bbl,*.blg,*.fdb_latexmk,*.fls,*.log,*.out,*.synctex* -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
  exit 0
}

if (Get-Command tectonic -ErrorAction SilentlyContinue) {
  Write-Host "Building with Tectonic..."
  tectonic $mainTex
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

# Handle locked output by switching jobname
$jobName = $defaultJobName
try {
  if (Test-Path "$defaultJobName.pdf") { Remove-Item "$defaultJobName.pdf" -Force }
}
catch {
  Write-Warning "$defaultJobName.pdf appears to be open/locked; building to ${defaultJobName}_build.pdf instead. Close the viewer to overwrite ${defaultJobName}.pdf next time."
  $jobName = "${defaultJobName}_build"
}

if (Get-Command latexmk -ErrorAction SilentlyContinue) {
  if (-not (Get-Command perl -ErrorAction SilentlyContinue)) {
    Write-Warning "Perl not found; skipping latexmk and falling back to pdflatex."
  }
  else {
    Write-Host "Building with latexmk (pdflatex)..."
    try {
      latexmk -pdf -jobname=$jobName -interaction=nonstopmode -halt-on-error -file-line-error $mainTex
      if ($LASTEXITCODE -eq 0) { exit 0 }
    } catch {}
    Write-Warning "latexmk failed; falling back to pdflatex."
  }
}

# Fallback if latexmk is not found or failed
Invoke-PdfLaTeX -JobName $jobName

if ($Open) {
  $pdf = if (Test-Path "${jobName}.pdf") { "${jobName}.pdf" } else { "${defaultJobName}.pdf" }
  if (Test-Path $pdf) { Start-Process $pdf }
}
