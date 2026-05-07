param()

$ErrorActionPreference = "Stop"

# Edit these values before running.
$Repo = "."
$Out = "outputs/my-map"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
. (Join-Path $PSScriptRoot "_logging.ps1")
$Transcript = Start-RunTranscript -ProjectRoot $ProjectRoot -Name "run-map"
$srcPath = Join-Path $ProjectRoot "src"
if ($env:PYTHONPATH) {
    $env:PYTHONPATH = "$srcPath;$env:PYTHONPATH"
} else {
    $env:PYTHONPATH = $srcPath
}

Push-Location $ProjectRoot
try {
    Write-Host "Code Review Agent - map"
    Write-Host "Repo: $Repo"
    Write-Host "Out:  $Out"
    Write-Host ""

    & python -m code_review_agent.cli map `
        --repo $Repo `
        --out $Out

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} finally {
    Pop-Location
    Stop-RunTranscript -Transcript $Transcript
}
