param(
  [switch]$Clean,
  [switch]$Open,
  [switch]$Regen,
  [string[]]$Figs,
  [switch]$DataQuick
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

# Regenerate data and figures (best-effort)
try {
  if (Get-Command python -ErrorAction SilentlyContinue) {
    # Ensure simulation data exists or regenerate on request
    $thermo = Join-Path "sim" "data/thermo.npz"
    $spectral = Join-Path "sim" "data/spectral.npz"
    $needData = (-not (Test-Path $thermo)) -or (-not (Test-Path $spectral)) -or $Regen
    if ($needData) {
      $N = if ($DataQuick) { 10 } else { 12 }
      $Bins = if ($DataQuick) { 12 } else { 20 }
      Write-Host "Generating simulation data (N=$N, bins=$Bins)..."
      try {
        python "sim/generate_data.py" --N $N --bins $Bins --seed 1 | Write-Output
      }
      catch {
        Write-Warning "Data generation failed; figures may fall back to synthetic data. $($_.Exception.Message)"
      }
    }
    if ($Regen) {
      Write-Host "Regenerating figures (force)..."
      if ($Figs -and $Figs.Length -gt 0) {
        python "figs/generate.py" @Figs | Write-Output
      }
      else {
        python "figs/generate.py" | Write-Output
      }
    }
    else {
      Write-Host "Regenerating figures (only missing)..."
      python "figs/generate.py" --only-missing | Write-Output
    }
    # Best-effort: compute fit diagnostics into figs/metrics.tex
    try { python "figs/metrics.py" | Write-Output } catch { Write-Warning "metrics generation failed: $($_.Exception.Message)" }
  } else {
    Write-Warning "Python not found; skipping figure generation."
  }
}
catch {
  Write-Warning "Figure/ data generation failed (non-fatal): $($_.Exception.Message)"
}

function Invoke-PdfLaTeX {
  if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
    Write-Error "pdflatex not found on PATH. Install MiKTeX or TeX Live, or add pdflatex to PATH."
    exit 1
  }
  $job = $script:JobName
  if (-not $job) { $job = 'main' }

  Write-Host "Building with pdflatex (pass 1/3)..."
  pdflatex "-jobname=$job" -interaction=nonstopmode -halt-on-error -file-line-error main.tex

  if (Get-Command bibtex -ErrorAction SilentlyContinue) {
    Write-Host "Running bibtex..."
    bibtex $job
  } else {
    Write-Warning "bibtex not found; bibliography will be missing."
  }

  Write-Host "Building with pdflatex (pass 2/3)..."
  pdflatex "-jobname=$job" -interaction=nonstopmode -halt-on-error -file-line-error main.tex

  Write-Host "Building with pdflatex (pass 3/3)..."
  pdflatex "-jobname=$job" -interaction=nonstopmode -halt-on-error -file-line-error main.tex
  exit $LASTEXITCODE
}

if ($Clean) {
  if (Get-Command latexmk -ErrorAction SilentlyContinue) {
    try { latexmk -c } catch {}
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
  try {
    latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
    if ($LASTEXITCODE -eq 0) { exit 0 }
  } catch {}
  Write-Warning "latexmk failed (possibly missing Perl). Falling back to pdflatex."
}

# Fallback if latexmk is not found or failed
Invoke-PdfLaTeX
