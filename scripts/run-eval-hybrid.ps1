param()

$ErrorActionPreference = "Stop"

# Edit these values before running.
# The eval command currently supports rules / hybrid-fake / all only.
# This script uses hybrid-fake so it does not default to rules.
$Cases = "examples/eval_cases"
$Out = "outputs/my-eval-hybrid"
$Mode = "hybrid-fake"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
. (Join-Path $PSScriptRoot "_logging.ps1")
$Transcript = Start-RunTranscript -ProjectRoot $ProjectRoot -Name "run-eval-hybrid"
$srcPath = Join-Path $ProjectRoot "src"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $srcPath
}

Push-Location $ProjectRoot
try {
    Write-Host "Code Review Agent - eval hybrid"
    Write-Host "Cases: $Cases"
    Write-Host "Out:   $Out"
    Write-Host "Mode:  $Mode"
    Write-Host ""

    & python -m code_review_agent.cli eval `
        --cases $Cases `
        --out $Out `
        --mode $Mode

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
    Stop-RunTranscript -Transcript $Transcript
}
